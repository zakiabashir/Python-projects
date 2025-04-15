# Import required libraries
import streamlit as st  # Streamlit for creating web apps
import numpy as np  # NumPy for numerical operations
import time  # For animation delays

def binary_search(arr, target):
    """
    Binary search implementation with step visualization
    Args:
        arr: Sorted array to search in
        target: Value to find
    Returns:
        Index of target if found, -1 if not found and search steps
    """
    left = 0
    right = len(arr) - 1
    steps = []
    
    while left <= right:
        mid = (left + right) // 2
        steps.append({
            'left': left,
            'right': right,
            'mid': mid,
            'current_value': arr[mid]
        })
        
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1, steps

def visualize_search_steps(arr, steps, target):
    """
    Visualize binary search steps with colored segments
    """
    for step in steps:
        # Create three columns for visual organization
        left_col, mid_col, right_col = st.columns(3)
        
        with left_col:
            st.write(f"Left Index: {step['left']}")
        with mid_col:
            st.write(f"Middle Index: {step['mid']}")
        with right_col:
            st.write(f"Right Index: {step['right']}")
        
        # Display array with colored segments
        html_str = "<div style='display: flex; justify-content: center;'>"
        for i, num in enumerate(arr):
            if i == step['mid']:
                color = "#ff6b6b"  # Red for middle
            elif step['left'] <= i <= step['right']:
                color = "#4ecdc4"  # Teal for search range
            else:
                color = "#95a5a6"  # Gray for eliminated range
                
            html_str += f"<span style='margin: 0 5px; padding: 5px 10px; background-color: {color}; border-radius: 5px;'>{num}</span>"
        html_str += "</div>"
        
        st.markdown(html_str, unsafe_allow_html=True)
        st.markdown("---")
        time.sleep(0.8)  # Animation delay

def main():
    # Set page config
    st.set_page_config(page_title="Binary Search Visualizer", layout="wide")
    
    # Apply custom CSS for better styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #4b6cb7, #6b8cce);
            color: white;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Set page title and description with styling
    st.title("🔍 Binary Search Visualization")
    st.write("Enter numbers and watch the binary search algorithm in action!")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        # Get input array from user
        numbers = st.text_input(
            "Enter numbers separated by spaces:",
            "1 3 5 7 9 11 13 15",
            help="Enter space-separated numbers"
        )
        try:
            arr = np.array([int(x) for x in numbers.split()])
            arr.sort()  # Ensure array is sorted
        except ValueError:
            st.error("Please enter valid numbers!")
            return
    
    with col2:
        # Get target number from user
        target = st.number_input(
            "Enter number to search for:",
            value=7,
            help="Enter the number you want to find"
        )
    
    if st.button("Start Search", key="search_button"):
        # Perform binary search with visualization
        result, steps = binary_search(arr, target)
        
        # Create container for search visualization
        with st.container():
            st.subheader("Search Progress:")
            visualize_search_steps(arr, steps, target)
        
        # Display final result with animation
        if result != -1:
            st.balloons()  # Celebration animation
            st.success(f"🎉 Found {target} at index {result}")
        else:
            st.error(f"😕 {target} not found in the array")
        
        # Display the sorted array
        st.info("Sorted array: " + " ".join(map(str, arr)))

if __name__ == "__main__":
    main()
