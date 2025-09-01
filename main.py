import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import re

# Database setup
conn = sqlite3.connect('students.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT,
    gpa REAL,
    email TEXT
)
''')
conn.commit()

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-z)-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_inputs(name, age, gpa, email):
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")
    if not (18 <= age <= 100):
        errors.append("Age must be between 18 and 100.")
    if not(0.0 <= gpa <= 4.0):
        errors.append("GPA must be between 0.0 and 4.0.")
    if not validate_email(email):
        errors.append("Invalid email format.")
    return errors

# CRUD functions
def add_student(name, age, major, gpa, email):
    c.execute('INSERT INTO students (name ,age, major, gpa, email) VALUES (?, ?, ?, ?, ?)',
              (name, age, major, gpa, email))
    conn.commit()

def view_students():
    return pd.read_sql_query('SELECT * FROM students', conn)

def update_student(student_id, name, age, major, gpa, email):
    c.execute('UPDATE students SET name=?, age=?, major=?, gpa=?, email=? WHERE id=?',
              (name, age, major, gpa, email, student_id))
    conn.commit()

def delete_student(student_id):
    c.execute('DELETE FROM students WHERE id=?', (student_id,))
    conn.commit()

def search_students(query):
    return pd.read_sql_query("SELECT * FROM students WHERE name LIKE ? OR major LIKE ?",
                             conn, params=('%' + query + '%', '%' + query + '%'))

# ML : Predict student performance
def train_and_predict(df):
    if len(df) < 10:  # Ensure enough data
        return df, None, None
    df['performance'] = np.where(df['gpa'] >= 3.0, 'High Performer', 'Needs Improvement')
    X = df[['age', 'gpa']]
    y = df['performance']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(max_depth=3)
    model.fit(X_train, y_train)
    df['predicted_performance'] = model.predict(X)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    feature_importance = dict(zip(['Age', 'GPA'], model.feature_importances_))
    return df, accuracy, feature_importance

# Visualizations
def plot_gpa_distribution(df):
    fig, ax = plt.subplots()
    sns.histplot(df['gpa'], bins=10, kde=True, ax=ax)
    ax.set_title('GPA Distribution')
    ax.set_xlabel('GPA')
    ax.set_ylabel('Count')
    return fig

def plot_major_breakdown(df):
    fig, ax = plt.subplots()
    sns.countplot(y='major', data = df, ax=ax)
    ax.set_title('Students by Major')
    ax.set_xlabel('Count')
    ax.set_ylabel('Major')
    return fig

# Streamlit App
st.set_page_config(page_title="Student Database Management System", layout="wide")
st.title('Student Database Management System')
st.markdown("A robust system for managing student records with analytics and ML-driven insights.")

menu = ['Home', 'Add Student', 'View Students', 'Update Student', 'Delete Student', 'Search Students', 'Analytics & Reports', 'ML Recommendations']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Add Student':
    st.subheader('Add New Student')
    with st.form('add_student_form'):
        name = st.text_input('Name')
        age = st.number_input('Age', min_value = 18, max_value = 100, step = 1)
        major = st.text_input('Major')
        gpa = st.number_input('GPA', min_value = 0.0, max_value = 4.0, step = 0.1)
        email = st.text_input('Email')
        submitted = st.form_submit_button('Add Student')
        if submitted:
            errors = validate_inputs(name, age, gpa, email)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                add_student(name, age, major, gpa, email)
                st.success(f'Student {name} added successfully!')

elif choice == 'View Students':
    st.subheader('All Students')
    df = view_students()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info('No students in database.')

elif choice == 'Update Student':
    st.subheader('Update Student')
    student_id = st.number_input('Student ID', min_value=1, step=1)
    df = view_students()
    if student_id in df['id'].values:
        row = df[df['id'] == student_id].iloc[0]
        with st.form('update_student_form'):
            name = st.text_input('Name', value=row['name'])
            age = st.number_input('Age', min_value=18, max_value=100, step=1, value=int(row['age']))
            major = st.text_input('Major', value=row['major'])
            gpa = st.number_input('GPA', min_value=0.0, max_value=4.0, step=0.1, value=float(row['gpa']))
            email = st.text_input('Email', value=row['email'])
            submitted = st.form_submit_button('Update Student')
            if submitted:
                errors = validate_inputs(name, age, gpa, email)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    update_student(student_id, name, age, major, gpa, email)
                    st.success(f'Student ID {student_id} updated!')
    else:
        st.error('Student ID not found.')

elif choice == 'Delete Student':
    st.subheader('Delete Student')
    student_id = st.number_input('Student ID', min_value=1, step=1)
    if st.button('Delete'):
        df = view_students()
        if student_id in df['id'].values:
            delete_student(student_id)
            st.success(f'Student ID {student_id} deleted!')
        else:
            st.error('Student ID not found.')

elif choice == 'Search Students':
    st.subheader('Search Students')
    query = st.text_input('Search by Name or Major')
    if query:
        df = search_students(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info('No results found.')

elif choice == 'Analytics & Reports':
    st.subheader('Analytics & Reports')
    df = view_students()
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"** Average GPA ** : {df['gpa'].mean():.2f}")
            st.write(f"** Total Students ** : {len(df)}")
            st.write(f"** Top Major ** : {df['major'].mode()[0]}")
        with col2:
            st.pyplot(plot_gpa_distribution(df))
        st.pyplot(plot_major_breakdown(df))
        st.download_button('Download CSV Report', df.to_csv(index=False), file_name='students_report.csv')
    else:
        st.info('No data for analysis.')

elif choice == 'ML Recommendations':
    st.subheader('ML-based Student Performance Predictions')
    df = view_students()
    if not df.empty:
        predicted_df, accuracy, feature_importance = train_and_predict(df)
        if accuracy:
            st.write(f"** Model Accuracy ** :{accuracy:.2f}")
            st.write("** feature Importance ** : ")
            st.json(feature_importance)
            st.dataframe(predicted_df[['id', 'name', 'gpa', 'predicted_performance']], use_container_width=True)
            at_risk = predicted_df[predicted_df['predicted_performance'] == 'Needs Improvement']
            if not at_risk.empty:
                st.warning('Students who may need improvement: ')
                st.dataframe(at_risk, use_container_width=True)
        else:
            st.info('Not enough data for ML predictions (need at least 10 students).')
    else:
        st.info('Add students to enable ML.')

conn.close()
