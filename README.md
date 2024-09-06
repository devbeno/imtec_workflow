# imtec_workflow

`imtec_workflow` is a dynamic workflow tool designed for managing Frappe installations and ORB machines. It provides a command-line interface for performing various operations related to ORB machines.

## Installation

To install `imtec_workflow`, you can use [Poetry](https://python-poetry.org/) to manage dependencies and run the commands.

1. **Clone the Repository:**

```bash
git clone https://github.com/devbeno/imtec_workflow.git
cd imtec_workflow
```


2. **Install Poetry**
Install the project dependencies and create a virtual environment using Poetry:
```bash
poetry install
```

3. **Activate the Virtual Environment**
Activate the Poetry-managed virtual environment:
```bash
poetry shell
```

## Usage

You can use `imrun` to execute various subcommands. The available subcommands and options are as follows:

### Core Options

- `--complete`: Print tab-completion candidates for given parse remainder.
- `--hide=STRING`: Set default value of run()'s `hide` kwarg.
- `--print-completion-script=STRING`: Print the tab-completion script for your preferred shell (bash|zsh|fish).
- `--prompt-for-sudo-password`: Prompt user at start of session for the `sudo.password` config value.
- `--write-pyc`: Enable creation of .pyc files.
- `-d`, `--debug`: Enable debug output.
- `-D INT`, `--list-depth=INT`: When listing tasks, only show the first INT levels.
- `-e`, `--echo`: Echo executed commands before running.
- `-f STRING`, `--config=STRING`: Runtime configuration file to use.
- `-F STRING`, `--list-format=STRING`: Change the display format used when listing tasks. Should be one of: flat (default), nested, json.
- `-h [STRING]`, `--help[=STRING]`: Show core or per-task help and exit.
- `-l [STRING]`, `--list=[STRING]`: List available tasks, optionally limited to a namespace.
- `-p`, `--pty`: Use a pty when executing shell commands.
- `-R`, `--dry`: Echo commands instead of running.
- `-T INT`, `--command-timeout=INT`: Specify a global command execution timeout, in seconds.
- `-V`, `--version`: Show version and exit.
- `-w`, `--warn-only`: Warn, instead of failing, when shell commands fail.

### Subcommands

- `build`: Build the ORB machine and initialize it using environment variables.
- `destroy`: Destroy the ORB machine and remove its project directory.
- `generate-env`: Run the shell script to generate the .env file for the project.
- `list`: List the ORB machines and corresponding project directories in the WORKBASE.
- `stop`: Stop the ORB machine.
