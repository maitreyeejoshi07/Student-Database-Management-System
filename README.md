# Student Database Management System (SDMS)

## Overview
The Student Database Management System (SDMS) is a Python-based web application designed to manage student records efficiently. Built with Streamlit, SQLite, and Scikit-learn, it provides a user-friendly interface for performing CRUD operations, generating analytical reports, and leveraging machine learning to predict student performance. This project showcases skills in data analysis, database management, and machine learning.

## Features
- **CRUD Operations**: Create, read, update, and delete student records with robust input validation.
- **Search Functionality**: Search students by name or major with fuzzy matching.
- **Data Analytics**: Generate reports with metrics like average GPA and visualizations (GPA distribution, major breakdown) using Pandas and Seaborn.
- **Machine Learning**: A decision tree classifier predicts student performance ("High Performer" vs. "Needs Improvement") based on GPA and age, with feature importance analysis.
- **Exportable Reports**: Download student data as CSV for further analysis.
- **User-Friendly Interface**: Built with Streamlit for an intuitive, web-based experience without front-end development.

## Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Web app framework for interactive UI.
- **SQLite**: Lightweight database for persistent storage.
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning for performance predictions.
- **Matplotlib/Seaborn**: Data visualizations.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd sdms
   ```
2. **Install Dependencies**:
   ```bash
   pip install streamlit pandas scikit-learn matplotlib seaborn
   ```
3. **Run the Application**:
   ```bash
   streamlit run sdms_app.py
   ```
   Open the provided URL (usually `http://localhost:8501`) in your browser.

## Usage
- **Add Student**: Input student details (name, age, major, GPA, email) with validation.
- **View Students**: See all records in a table.
- **Update/Delete**: Modify or remove records by ID.
- **Search**: Find students by name or major.
- **Analytics**: View GPA distribution, major counts, and download CSV reports.
- **ML Recommendations**: Identify at-risk students based on ML predictions.

## Deployment
- Deployed on Streamlit Sharing for live demo: [Link to your deployed app, if applicable].
- Local SQLite database ensures portability; for production, integrate with PostgreSQL.

## Future Enhancements
- Add course enrollment tracking.
- Integrate with external APIs (e.g., academic performance metrics).
- Enhance ML model with additional features like attendance or past grades.
