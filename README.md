# AI Agent Calculator

This project is a simple command-line AI agent that uses Google's Gemini API to interact with a small calculator application. The agent can decide when to call specific tools (Python functions) to inspect and manipulate files in the `calculator` working directory.

## Features

- CLI chatbot powered by Gemini (`gemini-2.5-flash`)
- Tool calling via the Gemini tools API:
  - `get_files_info` – list files in a directory
  - `get_file_content` – read a file’s contents
  - `write_file` – write text to a file
  - `run_python_file` – run a Python file (e.g. `tests.py`)
- Safe working directory configuration (`./calculator`) so tools can’t wander outside the project sandbox
- Verbose mode for debugging tool calls and model usage

## Project Structure

```text
.
├── main.py               # CLI entrypoint, calls Gemini and handles responses
├── call_function.py      # Tool definitions and function-call handling
├── config.py             # Configuration (e.g. WORKING_DIR, limits)
├── prompts.py            # System prompt(s) for the model
├── functions/
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
└── calculator/
    ├── main.py
    ├── tests.py
    ├── lorem.txt
    └── pkg/
        ├── calculator.py
        └── render.py

How It Works
CLI Input

The user runs main.py with a natural-language prompt:

uv run main.py "run tests.py" --verbose

Model Call

main.py:

Loads environment variables (e.g. GEMINI_API_KEY).
Builds a types.Content message from the user prompt.
Calls client.models.generate_content with:
The system prompt.
The user message.
The available tools (from available_functions in call_function.py).
Tool Calling

If Gemini decides to call a tool, the response includes function_calls. For each call:

call_function(function_call, verbose=...) is invoked.
call_function:
Logs the call (with args in verbose mode).
Looks up the function in a function_map.
Adds working_directory=WORKING_DIR (./calculator) to the arguments.
Executes the function.
Wraps the result in a types.Content with from_function_response.
Output

In verbose mode, the agent prints the tool output in a structured way.
For simple prompts with no tools, the model’s text response is printed directly.
Usage
Prerequisites
uv installed
Python environment that can install the required packages
A valid GEMINI_API_KEY in your environment
Set your API key:

export GEMINI_API_KEY="your-api-key-here"

Install dependencies (if needed):

uv sync

Running the Agent
Call the agent with a natural language prompt:

uv run main.py "run tests.py"

Use --verbose to see detailed information about tool calls, token usage, and results:

uv run main.py "get the contents of lorem.txt" --verbose
uv run main.py "create a new README.md file with the contents '# calculator'" --verbose
uv run main.py "what files are in the root?" --verbose

Example verbose output:

User prompt: run tests.py
Prompt tokens: ...
Response tokens: ...
Response:
Calling function: run_python_file({'file_path': 'tests.py'})
-> {'result': 'STDERR:...\n----------------------------------------------------------------------\nRan 9 tests in 0.000s\n\nOK\n'}

Configuration
config.py currently defines:

MAX_CHARS = 10000
WORKING_DIR = "./calculator"

WORKING_DIR controls which directory the tools operate in.
MAX_CHARS can be used to cap file sizes or responses if needed.
Tools
Each tool is defined in functions/ with two parts:

A Python function that does the work.
A schema_* declaration (a types.FunctionDeclaration) that describes the tool to Gemini.
Current tools:

get_files_info(working_directory, directory=".")
Lists files in directory relative to WORKING_DIR.
Returns a human-readable string with file size and is_dir information.
get_file_content(working_directory, file_path)
Safely reads file contents within WORKING_DIR.
write_file(working_directory, file_path, content)
Writes text to a file under WORKING_DIR.
run_python_file(working_directory, file_path)
Executes a Python file and returns its output.
Development Notes
call_function.py centralizes:
Tool registration (available_functions).
Name → function mapping (function_map).
Execution, error handling, and response wrapping.
main.py is responsible for:
Argument parsing.
Calling Gemini.
Detecting function_calls.
Delegating to call_function and printing results.
As the project evolves, you can:

Add new tools in functions/ and register them in call_function.py.
Extend the system prompt in prompts.py to steer the agent’s behavior.
Pass tool outputs back into the model for multi-step reasoning.