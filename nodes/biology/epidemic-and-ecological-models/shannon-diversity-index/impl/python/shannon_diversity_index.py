# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-diversity-index/. The authors are listed in prov/4HC8AE.jsonl.
"""The Shannon diversity index of a list of species counts.

Input: counts n_i >= 0 with a positive sum. Output: the plug-in index H in
nats, the effective number exp(H), Pielou's evenness H / ln S (None when
fewer than two species are present) and the Miller-Madow form
H + (S - 1) / (2 n). Cost: Theta(k) time for k counts and O(1) extra space.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class Shannon:
    h: float
    effective_number: float
    evenness: Optional[float]
    miller_madow: float


def shannon(counts: Sequence[float]) -> Shannon:
    """Compute the Shannon index and its derived values from the counts."""
    if any(c < 0 for c in counts):
        raise ValueError("counts must be >= 0")
    n = sum(counts)  # @line L1
    if n <= 0:
        raise ValueError("counts must have a positive sum")
    s = sum(1 for c in counts if c > 0)
    h = 0.0  # @line L2
    for c in counts:
        if c > 0:
            p = c / n
            h -= p * math.log(p)  # @line L3
    evenness = h / math.log(s) if s >= 2 else None
    return Shannon(h, math.exp(h), evenness, h + (s - 1) / (2 * n))  # @line L4
