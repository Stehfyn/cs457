
import pytest
import os
import sys
import database.database as db

@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1
    
    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer

def get_expected_stdout(script):
    with open(script, "r") as file:
        lines = file.readlines()

        # Convention:
        #-- Expected output
        #--
        #-- Database db_1 created. <- start index

        start_index = lines.index("-- Expected output\n") + 2
        lines = lines[start_index:]

        for i, line in enumerate(lines):
            if line.startswith("-- "):
                lines[i] = line[len("-- "):]

        return "".join(lines)

@pytest.mark.parametrize("script, stdout", 
    [
        ("PA1_test.sql", pytest.lazy_fixture("capture_stdout")), 
        ("PA2_test.sql", pytest.lazy_fixture("capture_stdout")),
        ("PA3_test.sql", pytest.lazy_fixture("capture_stdout")),
        ("PA4_test.sql", pytest.lazy_fixture("capture_stdout")),
    ]
)

def test_assignments(script, stdout):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_script = os.path.realpath(root + "/scripts/" + script)

    expected_stdout = get_expected_stdout(test_script)
    db.batch_processor([test_script])

    assert stdout["stdout"] == expected_stdout + '\n'