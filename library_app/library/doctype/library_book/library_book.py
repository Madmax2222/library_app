# library_app/library/doctype/library_book/library_book.py

import frappe
from frappe.model.document import Document

class LibraryBook(Document):
    def validate(self):
        self.validate_quantity()

    def validate_quantity(self):
        if self.quantity < 0:
            frappe.throw("Quantity cannot be negative")

    def before_delete(self):
        # Prevent deletion if book is issued
        issued = frappe.db.exists(
            "Library Transaction",
            {"book": self.name, "status": "Issued"}
        )
        if issued:
            frappe.throw("Cannot delete book while copies are issued.")
