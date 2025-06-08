# library_app/hooks.py

scheduler_events = {
    "daily": [
        "library_app.library.doctype.utils.send_due_reminders"
    ]
}

doc_events = {
    "Student": {
        "after_insert": "library_app.library.doctype.utils.create_user_for_student"
    },
    "Instructor": {
        "after_insert": "library_app.library.doctype.utils.create_user_for_tutor"
    },
    "Employee": {
        "after_insert": "library_app.library.doctype.utils.create_user_for_employee"
    }
}

website_route_rules = [
    {"from_route": "/library", "to_route": "student_library"},
    {"from_route": "/library-dashboard", "to_route": "library_dashboard"},
    {"from_route": "/faculty-library", "to_route": "faculty_library"},
    {"from_route": "/librarian-book-search", "to_route": "librarian_book_search"}
]

portal_menu_items = [
    {
        "title": "My Library Books",
        "route": "/library",
        "reference_doctype": "Library Transaction",
        "role": "Student"
    },
    {
        "title": "Faculty Library Books",
        "route": "/faculty-library",
        "reference_doctype": "Library Transaction",
        "role": "Instructor"
    },
    {
        "title": "Library Dashboard",
        "route": "/library-dashboard",
        "reference_doctype": "Library Transaction",
        "role": "Librarian"
    },
    {
        "title": "Book Search",
        "route": "/librarian-book-search",
        "reference_doctype": "Library Book",
        "role": "Librarian"
    }
]
