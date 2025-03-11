import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    # Set page config and background color with enhanced styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(45deg, #FF69B4, #9370DB, #4B0082, #00CED1, #32CD32, #FFD700);
            background-size: 600% 600%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Enhanced title styling */
        h1 {
            background: linear-gradient(120deg, #FF69B4, #9370DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGlow 2s ease-in-out infinite;
        }

        @keyframes titleGlow {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }

        /* Card-like styling for tasks */
        .stButton button {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            color: white;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            background: rgba(255, 255, 255, 0.3);
        }

        /* Fancy divider */
        hr {
            border: none;
            height: 3px;
            background: linear-gradient(90deg, #FF69B4, #9370DB, #4B0082);
        }

        /* Form styling */
        .stTextInput input, .stSelectbox select, .stDateInput input {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            color: white;
        }

        .stTextInput input:focus, .stSelectbox select:focus, .stDateInput input:focus {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            border-color: #FF69B4;
        }

        /* Additional styling for better visibility */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            border-radius: 10px;
            padding: 10px;
        }

        .stMarkdown {
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ Todo App")
    st.write("### Welcome to Todo App! 🌈")
    st.write("This simple but powerful todo application helps you stay organized and productive.")
    st.write("Created by: Zakia Bashir")
    st.write("---")
    # Initialize session state for todos if it doesn't exist
    if 'todos' not in st.session_state:
        st.session_state.todos = pd.DataFrame(columns=['Task', 'Due Date', 'Priority', 'Status'])

    # Load todos from CSV if file exists
    try:
        st.session_state.todos = pd.read_csv('todos.csv')
        # Convert Due Date strings to datetime objects
        st.session_state.todos['Due Date'] = pd.to_datetime(st.session_state.todos['Due Date']).dt.date
    except:
        pass

    # Add new todo
    with st.form("add_todo", clear_on_submit=True):
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            task = st.text_input("Task")
        with col2:
            due_date = st.date_input("Due Date")
        with col3:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        if st.form_submit_button("Add Task"):
            new_todo = pd.DataFrame({
                'Task': [task],
                'Due Date': [due_date],
                'Priority': [priority],
                'Status': ['Pending']
            })
            st.session_state.todos = pd.concat([st.session_state.todos, new_todo], ignore_index=True)
            # Save to CSV after adding
            st.session_state.todos.to_csv('todos.csv', index=False)
            st.success("Task added successfully!")

    # Display todos
    if not st.session_state.todos.empty:
        st.write("### Your Tasks")
        for idx, todo in st.session_state.todos.iterrows():
            col1, col2, col3, col4 = st.columns([2,1,1,1])
            with col1:
                st.write(todo['Task'])
            with col2:
                st.write(todo['Due Date'])
            with col3:
                st.write(todo['Priority'])
            with col4:
                if st.button('Complete', key=f'complete_{idx}'):
                    st.session_state.todos.at[idx, 'Status'] = 'Completed'
                    # Save to CSV after status change
                    st.session_state.todos.to_csv('todos.csv', index=False)
                    st.rerun()
                if st.button('Delete', key=f'delete_{idx}'):
                    st.session_state.todos = st.session_state.todos.drop(idx)
                    # Save to CSV after deletion
                    st.session_state.todos.to_csv('todos.csv', index=False)
                    st.rerun()

        # Filter and sort options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        with col2:
            sort_by = st.selectbox("Sort by", ["Due Date", "Priority"])

        filtered_todos = st.session_state.todos
        if status_filter != "All":
            filtered_todos = filtered_todos[filtered_todos['Status'] == status_filter]
        
        if sort_by == "Due Date":
            # Convert Due Date to datetime for sorting
            filtered_todos = filtered_todos.copy()
            # Use format='mixed' to handle different date formats
            filtered_todos['Due Date'] = pd.to_datetime(filtered_todos['Due Date'], format='mixed')
            filtered_todos = filtered_todos.sort_values('Due Date')
            filtered_todos['Due Date'] = filtered_todos['Due Date'].dt.date
        else:
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            filtered_todos = filtered_todos.sort_values('Priority', key=lambda x: x.map(priority_order))

        st.write("### Filtered Tasks")
        st.dataframe(filtered_todos)

if __name__ == "__main__":
    main()
