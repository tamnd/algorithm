# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bio-encoding/. The authors are listed in prov/ANKPZQ.jsonl.

"""Convert between labeled spans and token tags in the IOB1, IOB2 (BIO) and BIOES schemes.

A span is (i, j, label) with 0 <= i < j <= n. It covers the tokens i+1 .. j
(fencepost indices), which are the list positions i .. j-1. Spans must not
overlap.

IOB2: B-X on the first token of a span, I-X on the others, O outside.
IOB1: I-X on every token of a span, except B-X on the first token of a span
      that directly follows a span with the same label.
BIOES: S-X for a one-token span; B-X, I-X ... I-X, E-X for longer spans.

decode() accepts only valid tag sequences. repair() turns any sequence of
O, B-X and I-X tags into a valid IOB2 sequence with the rule of the CoNLL-2000
evaluation: an I-X that follows O, the sentence start, or a tag with another
label starts a new span.
"""

from typing import List, Optional, Sequence, Tuple

Span = Tuple[int, int, str]
SCHEMES = ("IOB1", "IOB2", "BIOES")


def split(tag: str) -> Tuple[str, Optional[str]]:
    if tag == "O":
        return "O", None
    prefix, sep, label = tag.partition("-")
    if not sep or prefix not in ("B", "I", "E", "S") or not label:
        raise ValueError("bad tag " + repr(tag))
    return prefix, label


def check_spans(spans: Sequence[Span], n: int) -> List[Span]:
    out = sorted(spans)
    end = 0
    for i, j, _ in out:
        if not (0 <= i < j <= n) or i < end:
            raise ValueError("spans must satisfy 0 <= i < j <= n and must not overlap")
        end = j
    return out


def encode(spans: Sequence[Span], n: int, scheme: str = "IOB2") -> List[str]:
    """Return the n tags of a set of spans."""
    if scheme not in SCHEMES:
        raise ValueError("unknown scheme " + scheme)
    tags = ["O"] * n  # @line L1
    prev_end, prev_label = None, None
    for i, j, x in check_spans(spans, n):  # @line L2
        for p in range(i, j):
            tags[p] = "I-" + x  # @line L3
        if scheme == "IOB2":
            tags[i] = "B-" + x  # @line L4
        elif scheme == "IOB1":
            if prev_end == i and prev_label == x:
                tags[i] = "B-" + x  # @line L5
        else:
            if j - i == 1:
                tags[i] = "S-" + x  # @line L6
            else:
                tags[i], tags[j - 1] = "B-" + x, "E-" + x
        prev_end, prev_label = j, x
    return tags  # @line L7


def decode(tags: Sequence[str], scheme: str = "IOB2") -> List[Span]:
    """Return the spans of a valid tag sequence. Raise ValueError if it is not valid."""
    if scheme not in SCHEMES:
        raise ValueError("unknown scheme " + scheme)
    bioes = scheme == "BIOES"
    spans: List[Span] = []
    start, label = None, None  # the open span, if any

    def close(p):
        nonlocal start, label
        if start is not None:
            if bioes:
                raise ValueError("a BIOES span must end with E-X")
            spans.append((start, p, label))
        start, label = None, None

    for p, tag in enumerate(tags):
        prefix, x = split(tag)
        if prefix in ("E", "S") and not bioes:
            raise ValueError(tag + " is not a tag of " + scheme)
        inside = start is not None and label == x
        if prefix == "O":
            close(p)
        elif prefix == "B":
            if scheme == "IOB1" and not inside:
                raise ValueError("IOB1 uses B-X only right after a span labeled X")
            close(p)
            start, label = p, x
        elif prefix == "S":
            close(p)
            spans.append((p, p + 1, x))
        elif inside:
            if prefix == "E":
                spans.append((start, p + 1, label))
                start, label = None, None
        elif scheme == "IOB1" and prefix == "I":
            close(p)
            start, label = p, x
        else:
            raise ValueError("an inside tag must continue a span with the same label")
    close(len(tags))
    return spans


def repair(tags: Sequence[str]) -> List[str]:
    """Make any sequence of O, B-X and I-X tags valid IOB2, by the CoNLL-2000 rule."""
    out = []
    prev = "O"
    for tag in tags:  # @line L8
        prefix, x = split(tag)
        if prefix not in ("B", "I", "O"):
            raise ValueError("repair takes O, B-X and I-X tags")
        if prefix == "I" and (prev == "O" or split(prev)[1] != x):  # @line L9
            tag = "B-" + x  # @line L10
        out.append(tag)
        prev = tag
    return out  # @line L11


def is_valid(tags: Sequence[str], scheme: str = "IOB2") -> bool:
    try:
        decode(tags, scheme)
    except ValueError:
        return False
    return True


def convert(tags: Sequence[str], source: str, target: str) -> List[str]:
    return encode(decode(tags, source), len(tags), target)
