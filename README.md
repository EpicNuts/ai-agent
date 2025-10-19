# AI Agent

A conversational AI agent powered by Google's Gemini API that can interact with files, run Python code, and maintain context across multiple function calls.

## Features

- **Conversational Interface**: Multi-turn conversations with persistent context
- **File System Operations**: List, read, and write files in the working directory
- **Python Code Execution**: Run Python scripts and capture both stdout and stderr output
- **Function Calling**: Intelligent use of available tools based on user requests
- **Safety Controls**: Sandboxed execution within the project directory
- **Verbose Logging**: Optional detailed output for debugging and learning

## Available Functions

The AI agent has access to the following functions:

- **`get_files_info`**: List files and directories in the working directory
- **`get_file_content`**: Read the contents of specific files
- **`write_file`**: Create or modify files with new content
- **`run_python_file`**: Execute Python scripts and capture their output

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:EpicNuts/ai-agent.git
   cd ai-agent
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_google_ai_api_key_here
   ```

## Usage

### Basic Usage

```bash
uv run main.py "your prompt here"
```

### Examples

```bash
# Ask the AI to analyze project files
uv run main.py "What files are in this project and what do they do?"

# Run tests
uv run main.py "run the calculator tests (tests.py)"

# Debug code
uv run main.py "check if there are any bugs in the calculator and fix them"

# Create new files
uv run main.py "create a simple hello world script"
```

### Command Line Options

- `--verbose`: Enable detailed logging of function calls and responses
- `--model`: Specify which Gemini model to use (default: `gemini-2.0-flash-001`)

### Verbose Mode

Use verbose mode to see the detailed conversation flow:

```bash
uv run main.py "run tests.py" --verbose
```

This will show:
- Function calls being made
- Function responses
- Token usage statistics

## Project Structure

```
ai-agent/
├── main.py                # Main application entry point
├── config.py              # Configuration settings
├── functions/             # Available AI functions
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/            # Example calculator project
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## How It Works

1. **Initialization**: The agent starts with your prompt as the first message
2. **AI Processing**: Gemini analyzes the request and decides what functions to call
3. **Function Execution**: The agent executes the requested functions safely
4. **Context Preservation**: Results are added to the conversation history
5. **Iteration**: The process repeats until the AI provides a final text response
6. **Safety Limits**: Maximum 20 iterations to prevent infinite loops

## Example Session

```bash
$ uv run main.py "analyze and run the calculator tests" --verbose

--- Iteration 1 ---
 - Calling function: get_files_info
-> {'result': 'Found calculator/ directory with tests.py and other files'}

--- Iteration 2 ---
 - Calling function: get_file_content
-> {'result': 'Content of calculator/tests.py with 9 unit tests'}

--- Iteration 3 ---
 - Calling function: run_python_file
-> {'result': 'STDERR:\n.........\n----------------------------------------------------------------------\nRan 9 tests in 0.001s\n\nOK\n'}

Final Response:
I analyzed the calculator project and ran the tests. The calculator has 9 unit tests covering addition, subtraction, multiplication, division, and error handling. All tests passed successfully!
```

## Development

### Adding New Functions

1. Create a new function file in `functions/`
2. Implement the function with proper error handling
3. Define the function schema using `types.FunctionDeclaration`
4. Add the function to the imports and `available_functions` in `main.py`

### Requirements

- Python 3.12+
- Google AI API key
- uv package manager

## Safety Features

- **Directory Restrictions**: Functions can only operate within the project directory
- **File Type Validation**: Python execution is limited to `.py` files
- **Timeout Protection**: Function execution has timeout limits
- **Iteration Limits**: Maximum 20 conversation turns to prevent infinite loops

## License

Open Source. Do what you want with it :)

## Contributing

Open a PR if you have something useful or interesting to add :)