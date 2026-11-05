# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-myrvold-planarity-test/. The authors are listed in prov/1RE4H8.jsonl.
"""Entry point named after the slug. The code is in boyer_myrvold_planarity.py,
because the tools treat a file whose name ends in _test as a test file."""

from boyer_myrvold_planarity import is_planar, kuratowski_subgraph, planar_embedding

__all__ = ["is_planar", "kuratowski_subgraph", "planar_embedding"]
