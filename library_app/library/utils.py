import frappe
from frappe.utils import getdate, nowdate, add_days, formatdate
from frappe.email.doctype.email_template.email_template import send_templated_email

PENALTY_PER_DAY = 10  # INR 10 per day late penalty, adjust as needed

def calculate_penalty(doc):
    """
    Calculate penalty based on due_date and return_date
    Returns 0 if returned on or before due_date or not yet returned.
    """
    if not doc.return_date:
        # If not returned yet, calculate penalty based on today's date
        days_late = (getdate(nowdate()) - getdate(doc.due_date)).days
    else:
        days_late = (getdate(doc.return_date) - getdate(doc.due_date)).days

    if days_late > 0:
        return days_late * PENALTY_PER_DAY
    return 0


def send_due_reminders():
    """
    Scheduled task to send email reminders for overdue books.
    """
    today = getdate(nowdate())
    overdue_transactions = frappe.get_all("Library Transaction",
        filters={
            "due_date": ["<", today],
            "status": "Issued"
        },
        fields=["name", "member", "member_type", "book", "due_date"]
    )

    for trans in overdue_transactions:
        # Fetch member email
        member_email = get_member_email(trans["member_type"], trans["member"])
        if not member_email:
            continue

        book_title = frappe.db.get_value("Library Book", trans["book"], "title")

        # Prepare context for email template
        context = {
            "member_name": trans["member"],
            "book_title": book_title,
            "due_date": formatdate(trans["due_date"]),
            "days_overdue": (today - trans["due_date"]).days
        }

        # Send templated email (you may create a template named "Library Due Reminder")
        send_templated_email(
            recipient=member_email,
            template="Library Due Reminder",
            args=context,
            subject=f"Library Book Due Reminder: {book_title}"
        )


def get_member_email(member_type, member_name):
    """
    Get email of member based on their type.
    Supports Student, Instructor, Employee
    """
    if member_type == "Student":
        email = frappe.db.get_value("Student", member_name, "email")
    elif member_type == "Instructor":
        email = frappe.db.get_value("Instructor", member_name, "email")
    elif member_type == "Employee":
        email = frappe.db.get_value("Employee", member_name, "company_email") or frappe.db.get_value("Employee", member_name, "personal_email")
    else:
        email = None
    return email


def create_user_for_student(doc, method=None):
    """
    Hook after Student creation to create User with 'Student' role
    """
    if not frappe.db.exists("User", doc.student_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": doc.student_email,
            "first_name": doc.student_name,
            "roles": [{"role": "Student"}],
            "send_welcome_email": True,
            "enabled": True
        })
        user.insert(ignore_permissions=True)


def create_user_for_tutor(doc, method=None):
    """
    Hook after Instructor creation to create User with 'Instructor' role
    """
    if not frappe.db.exists("User", doc.email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": doc.email,
            "first_name": doc.employee_name or doc.instructor_name,
            "roles": [{"role": "Instructor"}],
            "send_welcome_email": True,
            "enabled": True
        })
        user.insert(ignore_permissions=True)


def create_user_for_employee(doc, method=None):
    """
    Hook after Employee creation to create User with 'Employee' role if none exists
    """
    if not frappe.db.exists("User", doc.user_id):
        user_email = doc.user_id or doc.company_email or doc.personal_email
        if user_email:
            user = frappe.get_doc({
                "doctype": "User",
                "email": user_email,
                "first_name": doc.employee_name,
                "roles": [{"role": "Employee"}],
                "send_welcome_email": False,
                "enabled": True
            })
            user.insert(ignore_permissions=True)
