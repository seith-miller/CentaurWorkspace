# CentaurWorkspace

CentaurWorkspace is a project designed for tech teams to leverage AI capabilities in their workflows using CrewAI.

## Setup

1. **Install Dependencies:**

    Ensure you have Poetry installed. If not, install it from [Poetry's official documentation](https://python-poetry.org/docs/#installation).

    ```bash
    poetry install
    ```

2. **Set Up Environment Variables:**

    Create a `.env` file in the root directory and add your environment variables, especially for the OpenAI API key and Google credentials.

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. **Authenticate with Google Drive:**

    Run the authentication script to authenticate with Google Drive and save the credentials token.

    ```bash
    poetry run python scripts/manual_tests/auth_google.py
    ```

## Running the Application

1. **Activate the Virtual Environment:**

    Activate the Poetry virtual environment.

    ```bash
    source $(poetry env info --path)/bin/activate
    ```

2. **Set the PYTHONPATH:**

    Set the `PYTHONPATH` to include the project directory.

    ```bash
    export PYTHONPATH=$(pwd)
    ```

3. **Run the Main Script:**

    Run the main script to interact with the AI assistants and utilize the Google Drive tools.

    ```bash
    python centaur_workspace/main.py
    ```

4. **Alternative Method:**

    You can also run the script using `poetry run`, which sets up the environment correctly.

    ```bash
    poetry run python centaur_workspace/main.py
    ```

## Running Tests

1. **Run Unit Tests:**

    Ensure all unit tests pass to verify that your tools are working as expected.

    ```bash
    poetry run pytest tests/unit
    ```

2. **Run Integration Tests:**

    Verify integration with Google Drive by running the integration tests.

    ```bash
    poetry run pytest tests/integration
    ```

3. **Run Manual Tests:**

    Manual tests are not run by default. You need to specifically include the `manual` marker to run them. For example:

    ```bash
    pytest -v -s tests/manual/manual_google_drive_write.py
    ```

4. **Run Individual Tests:**

    You can run individual test cases using the `-k` option followed by the test case name. For example:

    ```bash
    poetry run pytest -k test_integration_list_files
    ```

5. **Run Tests in Verbose Mode:**

    To see detailed output, including print statements, use the `-v` and `-s` options:

    ```bash
    poetry run pytest -k test_integration_list_files -v -s
    ```

## Interacting with the AI

1. **Chat with the AI assistant:**

    Simply type your input when prompted.

2. **Interact with the Product Manager (Dave):**

    Type `Dave` when prompted to switch to interacting with Dave and ask product-related questions.

    Example commands:
    - **Chat with AI assistant**: Type your input.
    - **Switch to Dave**: Type `Dave` to start interacting with Dave.
    - **End conversation with Dave**: Type `stop` to end the conversation with Dave and switch back to the general AI.
