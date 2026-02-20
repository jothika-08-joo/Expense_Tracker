📌 Expense Tracker Web App:

   A simple and secure web application to track daily expenses, built using Python, Flask, and SQLite.
   This project is currently under active development.

🧠 Project Overview:

  The Expense Tracker allows users to:

  Add daily expenses
        
  View recorded expenses
        
  Store expense data securely using SQLite database
        
  Authenticate users with password hashing

This project is focused on strengthening backend fundamentals using Flask and database integration.

🚀 Features:

      ✅ Add new expenses
      
      ✅ View stored expenses
      
      ✅ SQLite database integration
      
      ✅ Secure password hashing implementation
      
      ✅ Clean backend structure using Flask routes

🛠️ Tech Stack:

      Backend: Python, Flask
      
      Database: SQLite
      
      Frontend: HTML
      
      Authentication: Password hashing

📂 Project Structure
Expense_Tracker/
        │
				
        ├── app.py
				
        ├── templates/
				
        ├── static/
				
        ├── database.db
				
        └── README.md

app.py → Main Flask application

templates/ → HTML files

static/ → CSS (planned improvements)

database.db → SQLite database

🔐 Security Improvements:

Implemented password hashing for secure user authentication.

Improved route handling to avoid duplicate route conflicts.

Handled database locking issues during development.

📈 Future Improvements:

📄 Export expenses as CSV file for user convenience

🎨 Add CSS styling for better UI

📊 Add expense summary dashboard (monthly/weekly insights)

🌐 Deploy the application online

🔎 Add filtering and search functionality

▶️ How to Run Locally:

  Clone the repository:

    git clone https://github.com/jothika-08-joo/Expense_Tracker.git

  Navigate into the project folder:

    cd Expense_Tracker

  Install required dependencies:

     pip install flask

  Run the application:

     python app.py

  Open your browser and go to:

     http://127.0.0.1:5000/
