# Correct import order and group separation
import subprocess  # Stdlib imports
from unittest import mock  # Stdlib imports

from scripts.imrun import stream_logs  # Third-party / Local imports


# Test stream_logs function for successful run
def test_stream_logs_success():
    with mock.patch("subprocess.run") as mocked_run:
        # Mock successful subprocess.run calls
        mocked_run.return_value = mock.Mock(returncode=0)

        # Mock time.sleep to avoid delays in tests
        with mock.patch("time.sleep", return_value=None):
            # Test with max_iterations=2 to avoid infinite loops
            stream_logs("test_machine", delay=0.1, max_iterations=2)

        # Assert subprocess.run was called with the correct command
        mocked_run.assert_called_with("orb logs test_machine --all", shell=True, check=True)


# Test stream_logs function handling subprocess failure
def test_stream_logs_failure():
    with mock.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "orb logs test_machine --all"),
    ):
        # Mock time.sleep to avoid delays in tests
        with mock.patch("time.sleep", return_value=None):
            # Ensure the function does not propagate the exception and exits cleanly
            stream_logs("test_machine", delay=0.1, max_iterations=2)
