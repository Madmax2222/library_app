# ERPNext Library App

A minimal custom Library Management application compatible with ERPNext 15 and the Education app.  
This app helps institutions manage books, issue/return transactions, and syncs with students and tutors from the Education app.

---

## Features

- Manage Books with details: ISBN, Title, Author, Edition, Publication, Description, Quantity, Location  
- Issue and Return books to/from Library Members (Students & Tutors)  
- Role-based access: Librarian, Student, Instructor  
- Dashboard with book stats and due alerts  
- Email reminders for due books  
- Search and filter books (Librarian view)  
- Student and Faculty portals to view issued books and due dates

---

## Installation

1. Clone the repository into your `frappe-bench/apps` directory:
   ```bash
   cd frappe-bench/apps
   git clone <repository_url> library_app
2. Install the app on your ERPNext site:
    bench --site your-site-name install-app library_app

3. Migrate and restart:
   bench --site your-site-name migrate
   bench restart

4. Set up roles and permissions as needed (create Librarian role, assign permissions).

**Usage**
Access Library pages via /library, /faculty-library, /library-dashboard, /librarian-book-search routes

Students and Tutors are automatically synced as Library Members

Librarian manages books, issues, returns, and monitors dashboard alerts

**Development**
Developed for ERPNext version 15

Frappe framework app structure

Uses scheduler for due date email reminders

**Credentials**
Developed and maintained by: Mahesh,vollstek business solutions

**License**
MIT License. Feel free to use, modify, and contribute.

**Support**
For issues, feature requests, or contributions, please open an issue on the GitHub repository.

---

If you want me to customize it further or add your GitHub profile/contact details, just say!
