# SPDX-License-Identifier: AGPL-3.0-only
"""Keep native SDK diagnostics off the normal result stream."""
from contextlib import contextmanager
import ctypes
import os
from pathlib import Path
import shutil
import sys
import tempfile


def flush():
    sys.stdout.flush()
    sys.stderr.flush()
    ctypes.CDLL(None).fflush(None)


@contextmanager
def sdk_output(log_path=None):
    with tempfile.TemporaryFile() as capture:
        flush()
        saved = [os.dup(fd) for fd in (1, 2)]
        try:
            for fd in (1, 2):
                os.dup2(capture.fileno(), fd)
            yield
        finally:
            flush()
            for fd, original in zip((1, 2), saved):
                os.dup2(original, fd)
                os.close(original)
            if log_path:
                path = Path(log_path)
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                with os.fdopen(descriptor, 'wb') as output:
                    os.fchmod(output.fileno(), 0o600)
                    capture.seek(0)
                    shutil.copyfileobj(capture, output)
