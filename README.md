<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Handling-150458?logo=pandas" />
  <img src="https://img.shields.io/badge/Plotly-Visualizations-3F4F75?logo=plotly" />
</p>

<h1 align="center">Library Management System</h1>

<p align="center">
A streamlined and interactive Streamlit application for managing books, member interactions, donations, and library analytics.
</p>

---

## Features

- **Dashboard**
  - Displays the most popular books
  - Genre-wise book distribution
  - Issued vs available book status visualization

- **Issue Book**
  - Search for a book by name
  - Enter member and issue details
  - Automatically updates status and popularity
  - Includes a recommendation system based on genre and availability

- **Return Book**
  - Search based on member ID
  - Updates inventory status and return record

- **Donate Book**
  - Collects donor details and book metadata
  - Supports new genres and auto-generates book IDs
  - Stores the record in both library and donation logs

- **CSV Persistence**
  - All operations write back to CSV files ensuring data retention

---

## Tech Stack

| Component | Technology |
|----------|------------|
| Frontend Interface | Streamlit |
| Data Processing | Pandas |
| Data Visualization | Plotly Express |
| Storage Format | CSV Files |

---

## Required Files

Ensure the following files are present in the project directory:

```

library_books.csv
donated_books.csv
issue_books.csv

````

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
````

### Step 2: Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

Access the application from the browser at:

```
http://localhost:8501/
```

---

## Team Members
- Hannah Janawa
- Harmehar Kaur
- Disha Pokhariyal

---

## Future Enhancements

* Authentication system (Admin/User Roles)
* Overdue notification system
* Exporting reports to PDF
* API-based integration for cloud storage and book metadata lookup

---

<p align="center">
End of Document
</p>
