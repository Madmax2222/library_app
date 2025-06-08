import frappe
from frappe.model.document import Document
from library_app.library.doctype.utils import calculate_penalty

class LibraryTransaction(Document):
    def validate(self):
        self.validate_dates()
        self.update_status()
        self.calculate_and_set_penalty()
        self.validate_availability()

    def validate_dates(self):
        if self.return_date and self.return_date < self.issue_date:
            frappe.throw("Return Date cannot be before Issue Date.")
        if self.due_date < self.issue_date:
            frappe.throw("Due Date cannot be before Issue Date.")

    def update_status(self):
        if self.return_date:
            self.status = "Returned"
        else:
            self.status = "Issued"

    def calculate_and_set_penalty(self):
        self.penalty = calculate_penalty(self)

    def validate_availability(self):
        if self.status == "Issued":
            # Check if enough copies are available before issuing
            available_qty = self.get_available_quantity()
            if available_qty <= 0:
                frappe.throw(f"No available copies for book: {self.book}")

    def get_available_quantity(self):
        total = frappe.db.get_value("Library Book", self.book, "quantity") or 0
        issued_count = frappe.db.count("Library Transaction", {
            "book": self.book,
            "status": "Issued"
        })
        return total - issued_count

    def before_submit(self):
        # Additional logic if you want on submit
        pass

    def before_cancel(self):
        # Additional logic if you want on cancel
        pass
