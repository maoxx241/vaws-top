"""Never send intentional test failures to the user's diagnostic worker."""
import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def isolated_diagnostics(tmp_path_factory):
    from vaws_diagnostics import configure

    root = tmp_path_factory.mktemp("top-diagnostics")
    previous = os.environ.get("VAWS_DIAGNOSTICS_ROOT")
    os.environ["VAWS_DIAGNOSTICS_ROOT"] = str(root)
    recorder = configure("vaws-top", root=root)
    yield root
    recorder.close()
    if previous is None:
        os.environ.pop("VAWS_DIAGNOSTICS_ROOT", None)
    else:
        os.environ["VAWS_DIAGNOSTICS_ROOT"] = previous
