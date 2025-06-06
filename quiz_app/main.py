import streamlit as st
import time
import json
import os
from datetime import datetime

# Define questions globally
QUESTIONS = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
    {"question": "Which of the following is required to register a custom tool in the OpenAI Agents SDK?", "options": ["toolkit.register(tool)", "agent.tools.add(tool)", "agent.register_tool(tool)", "tools.register_agent(tool)"], "answer": "agent.register_tool(tool)"},
    {"question": "What does the @tool decorator provide in OpenAI's Agents SDK?", "options": ["A way to create UI components", "Syntax for model routing", "Metadata and registration for a callable tool", "Performance optimization"], "answer": "Metadata and registration for a callable tool"},
    {"question": "What file typically defines the tools used by an OpenAI agent in a structured project?", "options": ["tools.json", "agent.py", "main.py", "tools.py"], "answer": "tools.py"},
    {"question": "In the OpenAI Agents SDK, which method is responsible for executing tool logic?", "options": ["__call__", "execute", "run", "invoke"], "answer": "__call__"},
    {"question": "What is the purpose of 'OpenAIToolFunction' in the Agents SDK?", "options": ["Wraps synchronous tools as agents", "Provides schema validation and formatting", "Connects the OpenAI API to LangChain", "Handles tool usage logs"], "answer": "Provides schema validation and formatting"},
    {"question": "Which of these best describes the signature of a tool function in OpenAI Agents SDK?", "options": ["Must take *args and **kwargs", "Must have type-annotated keyword-only arguments", "Can return JSON only", "Must return a tuple (result, status)"], "answer": "Must have type-annotated keyword-only arguments"},
    {"question": "What does the `agent.chat()` method do?", "options": ["Initiates a prompt loop", "Starts a websocket connection", "Takes a user prompt and returns a tool-routed response", "Registers tools automatically"], "answer": "Takes a user prompt and returns a tool-routed response"},
    {"question": "In OpenAI's Agents SDK, how are tools chosen for a prompt?", "options": ["Random selection", "Based on semantic similarity", "LLM decides based on the tool descriptions", "Priority-based round-robin"], "answer": "LLM decides based on the tool descriptions"},
    {"question": "Which method is used to run the full agent loop including tool execution?", "options": ["agent.run()", "agent.execute()", "agent.invoke()", "agent.loop()"], "answer": "agent.run()"},
    {"question": "What argument is used in `@tool` to define human-readable documentation?", "options": ["info", "desc", "docstring", "description"], "answer": "description"},
    {"question": "What will happen if two tools have the same name in an agent?", "options": ["The first one takes priority", "An error is thrown", "They both get executed", "The agent ignores both tools"], "answer": "An error is thrown"},
    {"question": "Which package provides the OpenAI Agents SDK?", "options": ["openai-agents", "openai", "openai_sdk", "openai.tools"], "answer": "openai"},
    {"question": "What is the role of `openai.FunctionTool`?", "options": ["Executes OpenAI functions on the cloud", "Wraps functions for compatibility with agents", "Creates new toolkits", "Defines new agent classes"], "answer": "Wraps functions for compatibility with agents"},
    {"question": "Which protocol does the tool execution in Agents SDK adhere to?", "options": ["JSON Schema", "OpenAPI", "gRPC", "SOAP"], "answer": "JSON Schema"},
    {"question": "Which feature allows agents to reason over multiple steps?", "options": ["Function trees", "ReAct-style planning", "State chains", "Async steps"], "answer": "ReAct-style planning"},
    {"question": "What is the result of calling `agent.run()` with a prompt that doesn't match any tool?", "options": ["Returns an error", "Returns a default tool result", "LLM provides a direct answer", "Skips the prompt"], "answer": "LLM provides a direct answer"},
    {"question": "Which of the following is NOT a core concept in OpenAI Agents SDK?", "options": ["Tools", "AgentExecutor", "ReAct planning", "Tool Call"], "answer": "AgentExecutor"},
    {"question": "Why are type annotations required for tool arguments?", "options": ["To comply with Python standards", "For CLI generation", "For LLM tool invocation and schema inference", "To enable multi-threading"], "answer": "For LLM tool invocation and schema inference"},
    {"question": "Which object encapsulates the model and toolchain in the SDK?", "options": ["ToolKit", "Agent", "AgentRuntime", "ToolRunner"], "answer": "Agent"},
    {"question": "Which feature of OpenAI Agents SDK allows tool composition?", "options": ["Chained tools", "Tool decorators", "Tool graphs", "Calling tools from tools"], "answer": "Calling tools from tools"},
    {"question": "Which version of the OpenAI Python library introduced `openai.tools`?", "options": ["0.25.0", "1.0.0", "1.10.0", "1.2.3"], "answer": "1.10.0"},
    {"question": "What is the maximum number of tools an agent can handle as per SDK limits?", "options": ["10", "16", "64", "No documented limit"], "answer": "No documented limit"},
    {"question": "What is required in the return value of a tool function?", "options": ["Always a JSON object", "A string or dictionary", "Only JSON serializable types", "Only string values"], "answer": "Only JSON serializable types"},
    {"question": "Which class or decorator registers a function as a tool?", "options": ["@openai.agent", "@openai.function_tool", "@tool", "@function"], "answer": "@tool"},
    {"question": "How can you inspect tool schema in the SDK?", "options": ["agent.tool_schema()", "tool.schema", "tool.__schema__", "tool.openai_schema"], "answer": "tool.openai_schema"},
    {"question": "What will be the output of the following code?\n\n```python\nfrom openai import tool\n\n@tool\ndef multiply(x: int, y: int) -> int:\n    return x * y\n\nprint(multiply.openai_schema['parameters']['properties'])\n```\n", "options": ["{'x': {'type': 'integer'}, 'y': {'type': 'integer'}}", "{'x': int, 'y': int}", "TypeError", "None"], "answer": "{'x': {'type': 'integer'}, 'y': {'type': 'integer'}}"},
    {"question": "What will happen if the tool is defined as follows?\n\n```python\n@tool\ndef greet(name):\n    return f\"Hello, {name}!\"\n```\n", "options": ["Tool works as expected", "TypeError: Missing type annotation", "Returns None", "Tool registers but fails at runtime"], "answer": "TypeError: Missing type annotation"},
    {"question": "Which part of this code is incorrect for OpenAI tool registration?\n\n```python\n@tool(name=\"AddNumbers\")\ndef add(x: int, y: int):\n    return x + y\n```\n", "options": ["The function name", "The decorator", "The name 'AddNumbers' should be lowercase", "The return type is missing"], "answer": "The name 'AddNumbers' should be lowercase"},
    {"question": "What happens if you return a non-serializable object from a tool?\n\n```python\nfrom openai import tool\nimport datetime\n\n@tool\ndef today() -> datetime.datetime:\n    return datetime.datetime.now()\n```\n", "options": ["Works fine", "Returns a stringified datetime", "Raises serialization error", "LLM parses the object automatically"], "answer": "Raises serialization error"},
    {"question": "What is the result of running this?\n\n```python\n@tool\ndef echo(msg: str = \"Hello\") -> str:\n    return msg\n```\n", "options": ["Tool works and uses default value", "Raises error: default values not allowed", "Tool is ignored", "Returns None if no input"], "answer": "Tool works and uses default value"},
    {"question": "Which output matches `tool.openai_schema` if a tool is declared as below?\n\n```python\n@tool\ndef divide(numerator: int, denominator: int) -> float:\n    return numerator / denominator\n```\n", "options": ["Includes both arguments and return types", "Includes only argument schema", "Only includes function name", "Not a valid method"], "answer": "Includes both arguments and return types"},
    {"question": "What is wrong with this tool?\n\n```python\n@tool\ndef log(x: int) -> None:\n    print(x)\n```\n", "options": ["Nothing is wrong", "Return type None is not serializable", "Print can't be used", "Tool must return a dictionary"], "answer": "Return type None is not serializable"},
    {"question": "What does this return?\n\n```python\n@tool\ndef weather(city: str) -> str:\n    return f\"Weather in {city} is sunny.\"\n\nprint(weather(\"Paris\"))\n```\n", "options": ["Tool object", "Decorated output", "String 'Weather in Paris is sunny.'", "Nothing"], "answer": "String 'Weather in Paris is sunny.'"},
    {"question": "Which issue occurs here?\n\n```python\n@tool\ndef sum_all(*args: int) -> int:\n    return sum(args)\n```\n", "options": ["Works correctly", "Raises error: *args not allowed", "Sum must be explicitly defined", "@tool can't handle lists"], "answer": "Raises error: *args not allowed"},
    {"question": "What is the result if a tool returns a Python object not listed in the schema?\n", "options": ["Object is coerced", "SDK throws ValueError", "Ignored at runtime", "Object is stringified"], "answer": "SDK throws ValueError"},
    {"question": "In the following snippet, what is returned?\n\n```python\n@tool\ndef show_pi() -> float:\n    return 3.14159\n```\n", "options": ["3.14159", "\"3.14159\"", "Schema validation error", "None"], "answer": "3.14159"},
    {"question": "Which of these tools is valid?\n\n```python\n@tool\ndef tool1(x: str, y: int = 0):\n    return f\"{x}-{y}\"\n```\n", "options": ["Yes, default values are supported", "No, all parameters must be required", "No return type", "@tool cannot accept mixed types"], "answer": "Yes, default values are supported"},
    {"question": "What error occurs here?\n\n```python\n@tool\ndef parse_json(data: dict) -> str:\n    return json.dumps(data)\n```\n", "options": ["Missing import json", "dict not supported as param type", "Return type mismatch", "Tool not registered"], "answer": "dict not supported as param type"},
    {"question": "Which of these return types is valid?\n\n```python\n@tool\ndef get_flag() -> bool:\n    return True\n```\n", "options": ["True", "\"True\"", "None", "Raises error: bool not supported"], "answer": "True"},
    {"question": "If you omit the return type from a tool, what happens?\n\n```python\n@tool\ndef say_hi(name: str):\n    return f\"Hi {name}!\"\n```\n", "options": ["Tool fails to register", "SDK infers type", "Raises schema error", "Returns raw object"], "answer": "Raises schema error"},
    {"question": "What's wrong here?\n\n```python\n@tool\ndef calc(x: float, y: float) -> float:\n    return f\"Result: {x + y}\"\n```\n", "options": ["Nothing", "Return type mismatch", "Decorator missing", "Float cannot be returned"], "answer": "Return type mismatch"},
    {"question": "What will be the schema type for the following?\n\n```python\n@tool\ndef is_even(n: int) -> bool:\n    return n % 2 == 0\n```\n", "options": ["'boolean'", "'number'", "'string'", "'int'"], "answer": "'boolean'"},
    {"question": "If a tool's name conflicts with another, what will happen?\n", "options": ["Last tool wins", "Agent uses first tool", "Raises DuplicateToolNameError", "Undefined behavior"], "answer": "Raises DuplicateToolNameError"},
    {"question": "What will this tool return if invoked by the agent?\n\n```python\n@tool\ndef answer() -> str:\n    return 42\n```\n", "options": ["'42'", "42", "Error: Return type mismatch", "None"], "answer": "Error: Return type mismatch"},
    {"question": "Can a tool return a list?\n\n```python\n@tool\ndef list_numbers() -> list:\n    return [1, 2, 3]\n```\n", "options": ["Yes", "No, list is not serializable", "Only string lists are allowed", "Only dicts allowed"], "answer": "Yes"},
    {"question": "Which of the following return types is invalid for a tool?", "options": ["str", "int", "dict", "set"], "answer": "set"},
    {"question": "Why is this tool invalid?\n\n```python\n@tool\ndef calculate(a, b) -> int:\n    return a + b\n```\n", "options": ["Missing return type", "Missing parameter types", "Return must be string", "Tools can't use integers"], "answer": "Missing parameter types"},
    {"question": "What will `agent.run(\"add 3 and 4\")` return given this tool?\n\n```python\n@tool\ndef add(x: int, y: int) -> int:\n    return x + y\n```\n", "options": ["7", "'7'", "Error", "Tool not triggered"], "answer": "'7'"},
    {"question": "Which argument signature is invalid for OpenAI tools?", "options": ["def tool(x: int, y: int)", "def tool(x: str = \"hi\")", "def tool(*args: int)", "def tool(x: int = 5)"], "answer": "def tool(*args: int)"},
    {"question": "Which behavior is expected from OpenAI's `tool.openai_schema`?", "options": ["Returns OpenAPI-like schema", "Returns plain function", "Returns a tuple", "Returns execution result"], "answer": "Returns OpenAPI-like schema"}
]

# Add custom CSS for animated background
st.markdown("""
<style>
    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* Make content more readable on animated background */
    .stApp > header {
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    .main > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Style for buttons */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.9);
        color: #333;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 1);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Style for input fields */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
    }

    /* Style for radio buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 5px;
    }

    /* Style for success/error messages */
    .stSuccess, .stError {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 5px;
    }

    /* Style for tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.9);
    }

    /* Custom styles for result boxes */
    .result-box {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }

    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }

    .result-box h3 {
        color: #2c3e50;
        margin-bottom: 15px;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }

    .result-box p {
        margin: 10px 0;
        color: #34495e;
        font-size: 1.1em;
    }

    .result-box .score {
        font-size: 1.3em;
        color: #2980b9;
        font-weight: bold;
    }

    .result-box .time {
        color: #27ae60;
    }

    .result-box .date {
        color: #7f8c8d;
        font-style: italic;
    }

    /* Style for admin panel results */
    .admin-result-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 240, 255, 0.95));
        border-left: 5px solid #3498db;
    }

    /* Style for user's own result */
    .user-result-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 240, 240, 0.95));
        border-left: 5px solid #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Function to load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Function to save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Function to load quiz results
def load_quiz_results():
    if os.path.exists('quiz_results.json'):
        with open('quiz_results.json', 'r') as f:
            return json.load(f)
    return {}

# Function to save quiz results
def save_quiz_result(username, score, total_questions, time_taken, completion_time):
    results = load_quiz_results()
    if username not in results:
        results[username] = []
    
    # Check if user has already attempted the quiz
    if len(results[username]) > 0:
        return False  # User has already attempted
    
    results[username].append({
        "score": score,
        "total_questions": total_questions,
        "time_taken": time_taken,
        "completion_time": completion_time,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open('quiz_results.json', 'w') as f:
        json.dump(results, f)
    return True  # Successfully saved

# Function to check if user has attempted quiz
def has_attempted_quiz(username):
    results = load_quiz_results()
    return username in results and len(results[username]) > 0

# Function to format time
def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

# Function to handle user registration
def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = password
    save_users(users)
    return True, "Registration successful"

# Function to handle user login
def login(username, password):
    users = load_users()
    # First check if it's admin login
    if username == "admin" and password == "admin":
        return True
    # Then check other users
    if username in users and users[username] == password:
        return True
    return False

# Function to check if user is admin
def is_admin(username):
    return username == "admin"

# --- App Initialization ---
st.title("Comprehensive Quiz Application")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'show_registration' not in st.session_state:
    st.session_state.show_registration = False
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'show_admin_panel' not in st.session_state:
    st.session_state.show_admin_panel = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}  # Store user's answers for each question

# --- Login/Registration Section ---
if not st.session_state.logged_in:
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["Login", "Signup"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username_input = st.text_input("Username:", key="login_username_input")
        password_input = st.text_input("Password:", type="password", key="login_password_input")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Login", key="login_button", use_container_width=True):
                if login(username_input, password_input):
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.start_time = time.time()
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        # Add signup link below login
        st.markdown("---")
        st.markdown("Don't have an account? Click on the Signup tab above to create one!")

    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Choose Username:", key="new_username_input")
        new_password = st.text_input("Choose Password:", type="password", key="new_password_input")
        confirm_password = st.text_input("Confirm Password:", type="password", key="confirm_password_input")

        if st.button("Signup", key="signup_button", use_container_width=True):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters long!")
            else:
                success, message = register_user(new_username, new_password)
                if success:
                    st.success(message)
                    # Auto login after successful signup
                    st.session_state.logged_in = True
                    st.session_state.username = new_username
                    st.session_state.start_time = time.time()
                    st.rerun()
                else:
                    st.error(message)

# --- Quiz Section (visible after login) ---
if st.session_state.logged_in:
    # Admin Panel
    if st.session_state.username == "admin":  # Direct check for admin
        st.write("### Admin Dashboard")
        if st.button("View Admin Panel", key="admin_panel"):
            st.session_state.show_admin_panel = True
            st.rerun()
        
        if st.button("Logout", key="admin_logout"):
            st.session_state.logged_in = False
            st.session_state.show_admin_panel = False
            st.rerun()

    if st.session_state.show_admin_panel and st.session_state.username == "admin":  # Direct check for admin
        st.subheader("Admin Panel - All Quiz Results")
        results = load_quiz_results()
        
        if results:
            for username, user_results in results.items():
                if user_results:  # Check if user has any results
                    result = user_results[0]  # Get the first (and only) attempt
                    # Create a container for each result
                    with st.container():
                        st.markdown(f"""
                        <div class="result-box admin-result-box">
                            <h3>User: {username}</h3>
                            <p class="date">Date: {result['date']}</p>
                            <p class="score">Score: {result['score']} out of {result['total_questions']}</p>
                            <p class="time">Time taken: {format_time(result['time_taken'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Check if there are any results other than admin's
            has_other_results = any(username != "admin" for username in results.keys())
            if not has_other_results:
                st.write("No quiz results found from other users.")
        else:
            st.write("No quiz results found.")
        
        if st.button("Back to Admin Dashboard", key="back_from_admin"):
            st.session_state.show_admin_panel = False
            st.rerun()
    
    # Regular user quiz interface
    elif st.session_state.username != "admin":  # Only show quiz for non-admin users
        # Check if user has already attempted the quiz
        if has_attempted_quiz(st.session_state.username):
            st.write("You have already attempted the quiz.")
            results = load_quiz_results()
            if st.session_state.username in results:
                result = results[st.session_state.username][0]
                # Create a container for user's result
                with st.container():
                    st.markdown(f"""
                    <div class="result-box user-result-box">
                        <h3>Your Quiz Result</h3>
                        <p class="date">Date: {result['date']}</p>
                        <p class="score">Score: {result['score']} out of {result['total_questions']}</p>
                        <p class="time">Time taken: {format_time(result['time_taken'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
                # Show all questions with correct answers only for user's own result
                st.subheader("📝 Complete Quiz Questions")
                for i, question in enumerate(QUESTIONS):  # Use the global QUESTIONS list
                    with st.container():
                        st.markdown(f"""
                        <div class="result-box" style="margin-bottom: 20px;">
                            <h4>Question {i+1}: {question['question']}</h4>
                            <p><strong>Correct Answer:</strong> {question['answer']}</p>
                            <p><strong>All Options:</strong> {', '.join(question['options'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            if st.button("Logout", key="logout_after_attempt"):
                st.session_state.logged_in = False
                st.session_state.quiz_completed = False
                st.session_state.current_question_index = 0
                st.session_state.score = 0
                st.rerun()
        else:
            # Regular quiz interface for normal users
            st.write(f"Welcome, {st.session_state.username}!")

            # Define the time limit in seconds
            time_limit = 7200  # 120 minutes in seconds

            # Create a placeholder for the timer
            timer_placeholder = st.empty()

            # Use the global QUESTIONS list
            questions = QUESTIONS

            # Check if quiz is completed
            if st.session_state.quiz_completed:
                time_taken = time.time() - st.session_state.start_time
                
                # Create a container for completion result
                with st.container():
                    st.markdown(f"""
                    <div class="result-box user-result-box">
                        <h3>🎉 Quiz Completed! 🎉</h3>
                        <p><strong>Username:</strong> {st.session_state.username}</p>
                        <p class="score">Final Score: {st.session_state.score} out of {len(questions)}</p>
                        <p class="time">Time taken: {format_time(time_taken)}</p>
                        <p class="date">Completion Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Show all questions with answers
                st.subheader("📝 Complete Quiz Summary")
                for i, question in enumerate(questions):
                    user_answer = st.session_state.user_answers.get(i, "Skipped")
                    
                    # Create a container for each question
                    with st.container():
                        st.markdown(f"""
                        <div class="result-box" style="margin-bottom: 20px;">
                            <h4>Question {i+1}: {question['question']}</h4>
                            <p><strong>Your Answer:</strong> {user_answer}</p>
                            <p><strong>Correct Answer:</strong> {question['answer']}</p>
                            <p><strong>Options:</strong> {', '.join(question['options'])}</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Save the result
                if save_quiz_result(
                    st.session_state.username,
                    st.session_state.score,
                    len(questions),
                    time_taken,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ):
                    st.success("Your result has been saved!")
                else:
                    st.error("You have already attempted the quiz!")

                if st.button("Logout", key="logout_button"):
                    st.session_state.logged_in = False
                    st.session_state.quiz_completed = False
                    st.session_state.current_question_index = 0
                    st.session_state.score = 0
                    st.session_state.user_answers = {}
                    st.rerun()
            else:
                # --- Timer ---
                elapsed_time = time.time() - st.session_state.start_time
                time_left = max(0, time_limit - elapsed_time)
                
                # Update timer display
                minutes, seconds = divmod(int(time_left), 60)
                timer_placeholder.write(f"⏱️ Time left: {minutes:02d}:{seconds:02d}")

                # Check if time is up
                if time_left <= 0:
                    time_taken = time_limit  # If time's up, use the full time limit
                    st.write("⏰ Time's up!")
                    st.write(f"Your final score is: {st.session_state.score} out of {len(questions)}")
                    st.write(f"Time taken: {format_time(time_taken)}")
                    
                    # Save the result
                    save_quiz_result(
                        st.session_state.username,
                        st.session_state.score,
                        len(questions),
                        time_taken,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    
                    st.session_state.quiz_completed = True
                    st.rerun()
                else:
                    # --- Question Display and Interaction ---
                    if st.session_state.current_question_index < len(questions):
                        current_question = questions[st.session_state.current_question_index]

                        st.subheader(f"Question {st.session_state.current_question_index + 1} of {len(questions)}: {current_question['question']}")

                        user_answer = st.radio("Choose your answer:", current_question['options'], key=f"q{st.session_state.current_question_index}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Submit Answer", key=f"submit_{st.session_state.current_question_index}"):
                                # Store user's answer
                                st.session_state.user_answers[st.session_state.current_question_index] = user_answer
                                
                                if user_answer == current_question['answer']:
                                    st.session_state.score += 1
                                
                                st.session_state.current_question_index += 1
                                
                                # Check if all questions are completed
                                if st.session_state.current_question_index >= len(questions):
                                    time_taken = time.time() - st.session_state.start_time
                                    # Save the result
                                    save_quiz_result(
                                        st.session_state.username,
                                        st.session_state.score,
                                        len(questions),
                                        time_taken,
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    )
                                    st.session_state.quiz_completed = True
                                st.rerun()

                        with col2:
                            if st.button("Skip Question", key=f"skip_{st.session_state.current_question_index}"):
                                # Store skipped answer
                                st.session_state.user_answers[st.session_state.current_question_index] = "Skipped"
                                st.session_state.current_question_index += 1
                                
                                # Check if all questions are completed
                                if st.session_state.current_question_index >= len(questions):
                                    time_taken = time.time() - st.session_state.start_time
                                    # Save the result
                                    save_quiz_result(
                                        st.session_state.username,
                                        st.session_state.score,
                                        len(questions),
                                        time_taken,
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    )
                                    st.session_state.quiz_completed = True
                                st.rerun()

                    # Add auto-refresh for timer only if quiz is not completed
                    if not st.session_state.quiz_completed:
                        time.sleep(1)
                        st.rerun()