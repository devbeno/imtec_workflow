# tests/test_utils.py
import pytest
from unittest import mock
from scripts.imrun import stream_logs
import subprocess

# Test stream_logs function
def test_stream_logs():
    with mock.patch('subprocess.run') as mocked_run:
        mocked_run.return_value = mock.Mock(returncode=0)
        stream_logs('test_machine', delay=0.1)
        mocked_run.assert_called_with('orb logs test_machine --all', shell=True, check=True)

# Test stream_logs function with failure
def test_stream_logs_failure():
    with mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'orb logs test_machine --all')):
        stream_logs('test_machine', delay=0.1)  # No error should propagate, and it should exit cleanly
