from unittest import mock
from invoke import Context
from scripts.imrun import build, destroy, stop

# Mock subprocess.run, subprocess.Popen, stream_logs, and input for the build task
@mock.patch('scripts.imrun.subprocess.run')  # Mock subprocess.run calls
@mock.patch('scripts.imrun.subprocess.Popen')  # Mock subprocess.Popen calls
@mock.patch('scripts.imrun.run_command')      # Mock run_command function
@mock.patch('scripts.imrun.stream_logs')      # Mock stream_logs function
@mock.patch('os.path.exists', return_value=True)  # Mock os.path.exists to always return True
@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="FRAPPE_USER=frappe")  # Mock open to simulate reading .env file
@mock.patch('builtins.input', return_value='test_project')  # Mock user input
@mock.patch('invoke.config.Config.merge', return_value=None)  # Prevent config merge
def test_build_task(mock_config_merge, mock_input, mock_open, mock_exists, mock_stream_logs, mock_run_command, mock_popen, mock_run):
    # Mock the behavior of Popen().communicate() to return stdout and stderr
    mock_process = mock_popen.return_value
    mock_process.communicate.return_value = (b"mock stdout", b"mock stderr")
    mock_process.returncode = 0

    # Mock subprocess.run to simulate running the shell command
    mock_run.return_value.returncode = 0

    # Now run the build task
    c = Context()
    build(c)

    # Ensure run_command, stream_logs, and Popen were all called correctly
    mock_run_command.assert_called()
    mock_stream_logs.assert_called()
    mock_popen.assert_called()
    mock_run.assert_called_with(['bash', './projects/generate-env'], check=True)

# Mock os.path.exists to always return True and run_command for destroy task
@mock.patch('os.path.exists', return_value=True)  # Mock os.path.exists to always return True
@mock.patch('scripts.imrun.run_command')          # Mock run_command
@mock.patch('builtins.input', return_value='test_project')  # Mock user input
def test_destroy_task(mock_input, mock_run_command, mock_exists):
    c = Context()
    destroy(c)
    mock_run_command.assert_called()

# Mock os.path.exists and file operations for stop task
@mock.patch('os.path.exists', return_value=True)  # Mock os.path.exists to always return True
@mock.patch('builtins.open', new_callable=mock.mock_open, read_data="FRAPPE_USER=frappe")  # Mock open to simulate reading .env file
@mock.patch('scripts.imrun.run_command')          # Mock run_command
@mock.patch('builtins.input', return_value='test_project')  # Mock user input
@mock.patch('invoke.config.Config.merge', return_value=None)  # Prevent config merge
def test_stop_task(mock_config_merge, mock_input, mock_run_command, mock_exists, mock_open):
    # Now run the stop task
    c = Context()
    stop(c)

    mock_run_command.assert_called()
