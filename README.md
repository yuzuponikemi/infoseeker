# Infoseeker: Automated Paper Collection Agent

Infoseeker is a Python-based agent that automatically fetches new research papers from arXiv based on a set of keywords, stores them in a local database, and sends notifications to a Slack channel.

## Features

-   **Automated Paper Fetching**: Fetches new papers from arXiv based on user-defined keywords.
-   **Local Database Storage**: Stores paper details in a local SQLite database to prevent duplicate notifications.
-   **Slack Notifications**: Sends notifications to a Slack channel when new papers are found.
-   **Flexible Execution**: Can be run continuously in the foreground or as a scheduled background task using `launchd` on macOS.

## Project Structure

```
├── core.py                 # Core logic for fetching and notifying
├── main.py                 # Entry point for single-run execution (for launchd/cron)
├── scheduler.py            # Entry point for continuous execution with a scheduler
├── database.py             # Database models and initialization
├── config.py.example       # Example configuration file
├── requirements.txt        # Python dependencies
├── doc/
│   ├── data_flow.md        # Data flow diagram and explanation
│   └── com.user.infoseeker.plist # Example launchd configuration file
└── ...
```

## Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd infoseeker
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the configuration file**:
    *   Copy the example configuration file:
        ```bash
        cp config.py.example config.py
        ```
    *   Open `config.py` and add your Slack webhook URL.

## Usage

You can run the application in two ways:

### Method 1: Using the Python Scheduler

This method is ideal for environments where the script can run continuously in the foreground.

```bash
python3 scheduler.py
```

The scheduler will run the task every day at 8:00 AM (Asia/Tokyo time).

### Method 2: Using `launchd` on macOS

This method uses macOS's built-in scheduler to run the script in the background, even if your computer is asleep.

1.  **Review the Configuration File**:
    The `doc/com.user.infoseeker.plist` file is pre-configured to run the `main.py` script. If your python executable is not at `/usr/bin/python3`, you will need to edit this file. You can find the correct path by running `which python3`.

2.  **Copy the File to `LaunchAgents`**:
    ```bash
    cp doc/com.user.infoseeker.plist ~/Library/LaunchAgents/
    ```

3.  **Load the Job**:
    ```bash
    launchctl load ~/Library/LaunchAgents/com.user.infoseeker.plist
    ```

Your Mac will now automatically run the script every day at 8:00 AM.

## Data Flow

For a visual representation of the data flow and a detailed explanation of how the components interact, please see the [Data Flow Document](doc/data_flow.md).
