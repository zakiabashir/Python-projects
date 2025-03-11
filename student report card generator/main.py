import streamlit as st
import json
import os
from fpdf import FPDF
import tempfile

def main():
    # Add custom CSS for background gradient and title animation
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96e6a1);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .title-animation {
            background: linear-gradient(to right, #2c3e50, #8e44ad, #2980b9, #16a085);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: titleFade 2s ease-in;
            text-align: center;
        }

        @keyframes titleFade {
            0% {opacity: 0; transform: translateY(-20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for students list if it doesn't exist
    if 'students' not in st.session_state:
        st.session_state.students = []

    st.markdown("<h1 class='title-animation'>Student Report Card Generator App</h1>", unsafe_allow_html=True)
    
    # Add app description and creator info
    st.markdown("""
    #### About this App
    This is a comprehensive Student Report Card Management System that allows you to:
    - Add new student records with marks in different subjects
    - Calculate total marks, percentages and grades automatically  
    - Search existing student records
    - Generate and download PDF report cards
    - Store all records persistently
    
    #### Created By
    **Developer:** Zakia Bashir  
    **Contact:** nshafeys0@gmail.com
    """)
    
    st.markdown("---")
    
    # Load existing students from file if it exists
    try:
        if os.path.exists('students.json'):
            with open('students.json', 'r') as f:
                st.session_state.persistent_students = json.load(f)
        else:
            if 'persistent_students' not in st.session_state:
                st.session_state.persistent_students = []
    except Exception as e:
        st.error(f"Error loading students data: {str(e)}")
        st.session_state.persistent_students = []

    # Add search functionality
    st.markdown("## Search Existing Report Card")
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_name = st.text_input("Search by Name")
    with search_col2:    
        search_roll = st.number_input("Search by Roll Number", min_value=0)
    
    if search_name or search_roll > 0:
        found_student = None
        for student in st.session_state.persistent_students:
            if (search_name and search_name.lower() in student['name'].lower()) or \
               (search_roll and search_roll == student['roll_no']):
                found_student = student
                break
                
        if found_student:
            st.success("Student Found!")
            with st.expander(f"Report Card - {found_student['name']}", expanded=True):
                st.write(f"**Student Name:** {found_student['name']}")
                st.write(f"**Roll Number:** {found_student['roll_no']}")
                
                st.write("\n**Subject-wise Marks:**")
                for subject, marks in found_student['marks'].items():
                    st.write(f"{subject}: {marks}")
                
                st.write(f"**Total Marks:** {found_student['total']}/500")
                st.write(f"**Percentage:** {found_student['percentage']:.2f}%")
                st.write(f"**Grade:** {found_student['grade']}")
                st.markdown("---")

                if st.button(f"Download Report Card - {found_student['name']}", key=f"search_btn_{found_student['roll_no']}"):
                    try:
                        pdf = FPDF()
                        pdf.add_page()
                        
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(190, 10, "Student Report Card", ln=True, align='C')
                        pdf.line(10, 30, 200, 30)
                        
                        pdf.set_font("Arial", size=12)
                        pdf.cell(190, 10, f"Student Name: {found_student['name']}", ln=True)
                        pdf.cell(190, 10, f"Roll Number: {found_student['roll_no']}", ln=True)
                        
                        pdf.cell(190, 10, "Subject-wise Marks:", ln=True)
                        for subject, marks in found_student['marks'].items():
                            pdf.cell(190, 10, f"{subject}: {marks}", ln=True)
                        
                        pdf.cell(190, 10, f"Total Marks: {found_student['total']}/500", ln=True)
                        pdf.cell(190, 10, f"Percentage: {found_student['percentage']:.2f}%", ln=True)
                        pdf.cell(190, 10, f"Grade: {found_student['grade']}", ln=True)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            pdf.output(tmp_file.name)
                            with open(tmp_file.name, "rb") as f:
                                st.download_button(
                                    label="Click here to download PDF",
                                    data=f.read(),
                                    file_name=f"report_card_{found_student['name']}.pdf",
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
        else:
            st.error("No student found with given name or roll number!")
    
    st.markdown("---")
    st.markdown("## Add New Student")
    
    with st.form("student_form"):
        # Get student details
        name = st.text_input("Enter Student Name",placeholder="Enter student Name")
        roll_no = st.number_input("Enter Roll Number", min_value=1, placeholder="Enter student Roll number")
        
        # Get subject marks
        math = st.number_input("Enter Math marks", min_value=0, max_value=100)
        physics = st.number_input("Enter Physics marks", min_value=0, max_value=100)
        urdu = st.number_input("Enter Urdu marks", min_value=0, max_value=100)
        english = st.number_input("Enter English marks", min_value=0, max_value=100)
        computer = st.number_input("Enter Computer marks", min_value=0, max_value=100)
        
        submit_button = st.form_submit_button("Add Student")
        
        if submit_button:
            try:
                # Validate name contains only English characters and is not empty
                if not name or not all(c.isalpha() or c.isspace() for c in name):
                    st.error("Please enter a valid student name (English letters only)!")
                    return
                    
                # Calculate total and percentage
                total_marks = math + physics + urdu + english + computer
                percentage = (total_marks / 500) * 100
                
                # Determine grade
                if percentage >= 80:
                    grade = "A+"
                elif percentage >= 70:
                    grade = "A"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C"
                else:
                    grade = "F"
                    
                # Store student data in persistent storage
                if 'persistent_students' not in st.session_state:
                    st.session_state.persistent_students = []
                    
                student = {
                    "name": name,
                    "roll_no": int(roll_no),
                    "marks": {
                        "Math": math,
                        "Physics": physics,
                        "Urdu": urdu,
                        "English": english,
                        "Computer": computer
                    },
                    "total": total_marks,
                    "percentage": percentage,
                    "grade": grade
                }
                st.session_state.persistent_students.append(student)
                
                # Save to file
                with open('students.json', 'w') as f:
                    json.dump(st.session_state.persistent_students, f)
                    
                st.success(f"Record of {name} inserted successfully!")
            except Exception as e:
                st.error(f"Error adding student: {str(e)}")

    # Generate report cards from persistent storage
    if 'persistent_students' in st.session_state and st.session_state.persistent_students:
        st.markdown("## All Student Report Cards")
        st.markdown("---")
        
        for student in st.session_state.persistent_students:
            with st.expander(f"Report Card - {student['name']}"):
                st.write(f"**Student Name:** {student['name']}")
                st.write(f"**Roll Number:** {student['roll_no']}")
                
                st.write("\n**Subject-wise Marks:**")
                for subject, marks in student['marks'].items():
                    st.write(f"{subject}: {marks}")
                
                st.write(f"**Total Marks:** {student['total']}/500")
                st.write(f"**Percentage:** {student['percentage']:.2f}%")
                st.write(f"**Grade:** {student['grade']}")
                st.markdown("---")

                # Add download PDF button
                if st.button(f"Download Report Card - {student['name']}", key=f"btn_{student['roll_no']}"):
                    try:
                        pdf = FPDF()
                        pdf.add_page()
                        
                        # Add content to PDF
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(190, 10, "Student Report Card", ln=True, align='C')
                        pdf.line(10, 30, 200, 30)
                        
                        pdf.set_font("Arial", size=12)
                        pdf.cell(190, 10, f"Student Name: {student['name']}", ln=True)
                        pdf.cell(190, 10, f"Roll Number: {student['roll_no']}", ln=True)
                        
                        pdf.cell(190, 10, "Subject-wise Marks:", ln=True)
                        for subject, marks in student['marks'].items():
                            pdf.cell(190, 10, f"{subject}: {marks}", ln=True)
                        
                        pdf.cell(190, 10, f"Total Marks: {student['total']}/500", ln=True)
                        pdf.cell(190, 10, f"Percentage: {student['percentage']:.2f}%", ln=True)
                        pdf.cell(190, 10, f"Grade: {student['grade']}", ln=True)
                        
                        # Save PDF to temp file and create download button
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            pdf.output(tmp_file.name)
                            with open(tmp_file.name, "rb") as f:
                                st.download_button(
                                    label="Click here to download PDF",
                                    data=f.read(),
                                    file_name=f"report_card_{student['name']}.pdf",
                                    mime="application/pdf"
                                )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
