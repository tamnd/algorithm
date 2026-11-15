# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twin-plant-diagnosability-test/. The authors are listed in prov/4TC48W.jsonl.

"""The twin plant diagnosability test. The code is in twin_plant.py; this
module re-exports it under the name of the page (a file name ending in _test
is read as a test file by some tools, so the implementation itself lives in
twin_plant.py)."""

from twin_plant import (  # noqa: F401
    build_verifier,
    diagnosable,
    diagnosable_jiang,
    out_edges,
    witness,
)
