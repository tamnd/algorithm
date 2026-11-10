# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-grep/. The authors are listed in prov/EX8YJV.jsonl.

"""Distributed grep: a map-only MapReduce job, on a small simulator.

The input is one large text cut into byte ranges (splits). A line belongs to
the split that holds its first character; a split reads past its end to finish
its last line and skips the partial line at its start. Each map task emits the
matching lines with their byte offsets. With R = 0 nothing is shuffled; with
R = 1 and the identity reducer, only the matches are shuffled.
"""

import re
from typing import Iterator


def byte_splits(text: str, size: int) -> list[tuple[int, int]]:
    """Cut [0, len(text)) into ranges of `size` characters (the last one may be shorter)."""
    return [(a, min(a + size, len(text))) for a in range(0, len(text), size)]


def read_lines(text: str, start: int, end: int) -> Iterator[tuple[int, str]]:
    """The record reader: the lines whose first character is in [start, end), as (offset, line)."""
    if start == 0 or text[start - 1] == "\n":
        pos = start
    else:
        nl = text.find("\n", start)
        pos = len(text) if nl < 0 else nl + 1
    while pos < end:
        nl = text.find("\n", pos)
        stop = len(text) if nl < 0 else nl
        yield pos, text[pos:stop]
        pos = stop + 1


def grep_map(pattern: re.Pattern, offset: int, line: str) -> Iterator[tuple[int, str]]:
    if pattern.search(line):
        yield (offset, line)


def distributed_grep(text: str, regex: str, split_size: int, r: int = 0
                     ) -> tuple[list[tuple[int, str]], dict[str, int]]:
    """Run the job. Returns (the matching (offset, line) pairs in file order, the costs).

    costs: map_tasks, bytes_read (each input character once), pairs_sent and
    bytes_sent in the shuffle (0 when r = 0), and output_pairs.
    """
    pattern = re.compile(regex)
    splits = byte_splits(text, split_size)
    # Map phase: each task reads its own lines; the tasks are independent.
    task_outputs = [[kv for off, line in read_lines(text, a, b) for kv in grep_map(pattern, off, line)]
                    for a, b in splits]
    lines_read = sum(1 for a, b in splits for _ in read_lines(text, a, b))
    costs = {"map_tasks": len(splits), "lines_read": lines_read, "bytes_read": len(text),
             "pairs_sent": 0, "bytes_sent": 0}
    if r == 0:
        # Map only: each task writes its own output file; concatenated in split order.
        result = [kv for out in task_outputs for kv in out]
    elif r == 1:
        # Identity reduce on one reducer: the shuffle carries only the matches, sorted by offset.
        shuffled = [kv for out in task_outputs for kv in out]
        costs["pairs_sent"] = len(shuffled)
        costs["bytes_sent"] = sum(len(str(k)) + len(v) for k, v in shuffled)
        result = sorted(shuffled)
    else:
        raise ValueError("distributed grep uses r = 0 or r = 1")
    costs["output_pairs"] = len(result)
    return result, costs


def grep_one_machine(text: str, regex: str) -> list[tuple[int, str]]:
    pattern = re.compile(regex)
    out, pos = [], 0
    for line in text.split("\n"):
        if pos < len(text) and pattern.search(line):
            out.append((pos, line))
        pos += len(line) + 1
    return out


def count_matches_job(text: str, regex: str, split_size: int) -> tuple[int, int]:
    """grep -c as MapReduce: each map task emits one (pattern, count) pair (a combiner); returns (count, pairs sent)."""
    pattern = re.compile(regex)
    partial = [sum(1 for _, line in read_lines(text, a, b) if pattern.search(line))
               for a, b in byte_splits(text, split_size)]
    return sum(partial), len(partial)
