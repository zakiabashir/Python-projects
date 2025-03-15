# Import required libraries
import streamlit as st  # For creating web interface
import json  # For handling JSON data storage
import os  # For file operations
from fpdf import FPDF  # For generating PDF reports
import tempfile  # For creating temporary files

def main():
    """
    Main function that runs the entire student report card application.
    Contains all the core functionality and UI components.
    """

    # Add custom CSS styling for better visual appearance
    # Creates gradient background animation and title animation effects
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

    # Initialize empty students list in session state if not already present
    # Session state persists data between reruns
    if 'students' not in st.session_state:
        st.session_state.students = []

    # Display the main title of the app with animation effect
    st.markdown("<h1 class='title-animation'>Student Report Card Generator App</h1>", unsafe_allow_html=True)
    
    # Display app description and developer information
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
    
    # Load existing student data from JSON file
    # Try-except block handles any errors during file operations
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

    # Search section - allows searching students by name or roll number
    st.markdown("## Search Existing Report Card")
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_name = st.text_input("Search by Name")
    with search_col2:    
        search_roll = st.number_input("Search by Roll Number", min_value=0)
    
    # Search logic - finds matching student based on name or roll number
    if search_name or search_roll > 0:
        found_student = None
        for student in st.session_state.persistent_students:
            if (search_name and search_name.lower() in student['name'].lower()) or \
               (search_roll and search_roll == student['roll_no']):
                found_student = student
                break
                
        if found_student:
            # Check for duplicate roll numbers to prevent conflicts
            roll_exists = False
            for student in st.session_state.persistent_students:
                if student['roll_no'] == found_student['roll_no'] and student != found_student:
                    roll_exists = True
                    break
                    
            if roll_exists:
                st.error("This roll number already exists. Cannot generate report card.")
                return
                
            st.success("Student Found!")
            # Display found student's report card in expandable section
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

                # PDF generation functionality for searched student
                if st.button(f"Download Report Card - {found_student['name']}", key=f"search_download_{found_student['roll_no']}"):
                    try:
                        # Create PDF with student details and formatting
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
                        
                        # Save PDF to temporary file and create download button
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            pdf.output(tmp_file.name)
                            with open(tmp_file.name, "rb") as f:
                                st.download_button(
                                    label="Click here to download PDF",
                                    data=f.read(),
                                    file_name=f"report_card_{found_student['name']}.pdf",
                                    mime="application/pdf",
                                    key=f"search_pdf_{found_student['roll_no']}"
                                )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
        else:
            st.error("No student found with given name or roll number!")
    
    st.markdown("---")
    st.markdown("## Add New Student")
    
    # Form key for resetting form after submission
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0
    
    # Form for adding new student details
    with st.form(f"student_form_{st.session_state.form_key}"):
        # Input fields for student information
        name = st.text_input("Enter Student Name",placeholder="Enter student Name")
        roll_no = st.number_input("Enter Roll Number", min_value=1, placeholder="Enter student Roll number")
        
        # Input fields for subject marks
        math = st.number_input("Enter Math marks", min_value=0, max_value=100)
        physics = st.number_input("Enter Physics marks", min_value=0, max_value=100)
        urdu = st.number_input("Enter Urdu marks", min_value=0, max_value=100)
        english = st.number_input("Enter English marks", min_value=0, max_value=100)
        computer = st.number_input("Enter Computer marks", min_value=0, max_value=100)
        
        submit_button = st.form_submit_button("Add Student")
        
        # Handle form submission
        if submit_button:
            try:
                # Validate student name contains only letters and spaces
                if not name or not all(c.isalpha() or c.isspace() for c in name):
                    st.error("Please enter a valid student name (English letters only)!")
                    return

                # Check if roll number already exists
                for existing_student in st.session_state.persistent_students:
                    if existing_student['roll_no'] == int(roll_no):
                        st.warning(f"Roll number {roll_no} already exists. Please use a different roll number.")
                        return
                    
                # Calculate total marks and percentage
                total_marks = math + physics + urdu + english + computer
                percentage = (total_marks / 500) * 100
                
                # Determine grade based on percentage ranges
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
                    
                # Initialize storage if not exists
                if 'persistent_students' not in st.session_state:
                    st.session_state.persistent_students = []
                    
                # Create student record dictionary
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
                
                # Add student to session state storage
                st.session_state.persistent_students.append(student)
                
                # Save updated records to JSON file
                with open('students.json', 'w') as f:
                    json.dump(st.session_state.persistent_students, f)
                    
                st.success(f"Record of {name} inserted successfully!")
                
                # Reset form by incrementing form key
                st.session_state.form_key += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"Error adding student: {str(e)}")

    # Display grid view of all students
    if 'persistent_students' in st.session_state and st.session_state.persistent_students:
        st.markdown("## Students Overview")
        
        # Create 3-column layout for grid display
        cols = st.columns(3)
        
        # Display each student as a card in grid
        for idx, student in enumerate(st.session_state.persistent_students):
            with cols[idx % 3]:
                # Card with student basic info
                st.markdown(f"""
                <div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px;'>
                    <h4>{student['name']}</h4>
                    <p>Roll No: {student['roll_no']}</p>
                    <p>Grade: {student['grade']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Button to view detailed student info
                unique_key = f"grid_btn_{student['roll_no']}_{idx}"
                if st.button(f"View Details", key=unique_key):
                    st.session_state.selected_student = student
        
        # Show detailed view of selected student
        if 'selected_student' in st.session_state:
            with st.expander(f"Detailed Report Card - {st.session_state.selected_student['name']}", expanded=True):
                st.write(f"**Student Name:** {st.session_state.selected_student['name']}")
                st.write(f"**Roll Number:** {st.session_state.selected_student['roll_no']}")
                
                st.write("\n**Subject-wise Marks:**")
                for subject, marks in st.session_state.selected_student['marks'].items():
                    st.write(f"{subject}: {marks}")
                
                st.write(f"**Total Marks:** {st.session_state.selected_student['total']}/500")
                st.write(f"**Percentage:** {st.session_state.selected_student['percentage']:.2f}%")
                st.write(f"**Grade:** {st.session_state.selected_student['grade']}")

                # PDF download functionality for selected student
                unique_download_key = f"download_btn_{st.session_state.selected_student['roll_no']}_{int(st.session_state.selected_student['percentage'])}"
                if st.button(f"Download Report Card", key=unique_download_key):
                    try:
                        # Create PDF with student details
                        pdf = FPDF()
                        pdf.add_page()
                        
                        # Add formatted content to PDF
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(190, 10, "Student Report Card", ln=True, align='C')
                        pdf.line(10, 30, 200, 30)
                        
                        pdf.set_font("Arial", size=12)
                        pdf.cell(190, 10, f"Student Name: {st.session_state.selected_student['name']}", ln=True)
                        pdf.cell(190, 10, f"Roll Number: {st.session_state.selected_student['roll_no']}", ln=True)
                        
                        pdf.cell(190, 10, "Subject-wise Marks:", ln=True)
                        for subject, marks in st.session_state.selected_student['marks'].items():
                            pdf.cell(190, 10, f"{subject}: {marks}", ln=True)
                        
                        pdf.cell(190, 10, f"Total Marks: {st.session_state.selected_student['total']}/500", ln=True)
                        pdf.cell(190, 10, f"Percentage: {st.session_state.selected_student['percentage']:.2f}%", ln=True)
                        pdf.cell(190, 10, f"Grade: {st.session_state.selected_student['grade']}", ln=True)
                        
                        # Save PDF and create download button
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            pdf.output(tmp_file.name)
                            with open(tmp_file.name, "rb") as f:
                                st.download_button(
                                    label="Click here to download PDF",
                                    data=f.read(),
                                    file_name=f"report_card_{st.session_state.selected_student['name']}.pdf",
                                    mime="application/pdf",
                                    key=f"pdf_download_{st.session_state.selected_student['roll_no']}_{int(st.session_state.selected_student['percentage'])}"
                                )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")

# Entry point of the application
if __name__ == "__main__":
    main()
