# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-length-code/. The authors are listed in prov/8GCPPW.jsonl.
"""A harness that measures error propagation in a variable-length prefix code.

Encode a random message, flip one bit, decode the damaged stream, and count the
decoded symbols until the codeword boundaries of the two parses meet again.
"""

import random
from typing import Mapping, Sequence


def parse_boundaries(bits: str, code: Mapping[str, str]) -> tuple[list[str], list[int]]:
    """Greedy prefix decoding. Return the symbols and the end position of each codeword.

    The code must be a prefix code. Decoding stops at the first point where no
    codeword fits (an incomplete code) or at the end of the bits.
    """
    inverse = {w: s for s, w in code.items()}
    max_len = max(len(w) for w in inverse)
    out, ends, i = [], [], 0
    while i < len(bits):
        for length in range(1, max_len + 1):
            w = bits[i:i + length]
            if len(w) < length:
                return out, ends
            if w in inverse:
                out.append(inverse[w])
                i += length
                ends.append(i)
                break
        else:
            return out, ends
    return out, ends


def symbols_until_resync(code: Mapping[str, str], message: Sequence[str], flip: int) -> int | None:
    """Flip bit `flip` of the encoded message. Return the number of symbols that the decoder
    emits from the damaged codeword up to the first common boundary after the flip,
    or None if the parses never meet again before the end.
    """
    bits = "".join(code[s] for s in message)
    damaged = bits[:flip] + ("1" if bits[flip] == "0" else "0") + bits[flip + 1:]
    _, true_ends = parse_boundaries(bits, code)
    _, bad_ends = parse_boundaries(damaged, code)
    true_set = set(true_ends)
    start = next(i for i, e in enumerate(bad_ends + [len(bits) + 1]) if e > flip)
    for j in range(start, len(bad_ends)):
        if bad_ends[j] in true_set:
            return j - start + 1
    return None


def never_resync_starts(code: Mapping[str, str]) -> list[tuple[str, int]]:
    """For a complete binary prefix code, the flips after which no continuation brings the parses back in step.

    A state is a pair of nodes of the code tree (proper prefixes of codewords):
    where the true parse is and where the damaged parse is. Both read the same
    bits, and a node goes back to the root at a leaf. A flip of bit b while the
    true parse is at node u starts the pair (u + b, u + (1 - b)). The parses are
    in step again when both are at the root. Return each (u, b) from which the
    pair (root, root) cannot be reached.
    """
    words = set(code.values())
    nodes = {w[:i] for w in words for i in range(len(w))}

    def step(u: str, b: str) -> str:
        v = u + b
        if v in words:
            return ""
        if v not in nodes:
            raise ValueError("the code is not complete")
        return v

    def start(u: str, b: str) -> tuple[str, str]:
        return step(u, b), step(u, "1" if b == "0" else "0")

    bad = []
    for u in sorted(nodes):
        for b in "01":
            s = start(u, b)
            seen, stack = {s}, [s]
            ok = False
            while stack:
                x, y = stack.pop()
                if x == "" and y == "":
                    ok = True
                    break
                for c in "01":
                    nxt = (step(x, c), step(y, c))
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            if not ok:
                bad.append((u, int(b)))
    return bad


def measure(code: Mapping[str, str], probs: Mapping[str, float], length: int, trials: int, seed: int) -> dict:
    """Average and largest number of symbols until resync, over random messages and flip positions.

    Messages are drawn from the memoryless source `probs`. A trial that does not
    resync before the end of the message counts in `never`.
    """
    rng = random.Random(seed)
    syms = list(probs)
    weights = [probs[s] for s in syms]
    total, count, worst, never = 0, 0, 0, 0
    for _ in range(trials):
        msg = rng.choices(syms, weights=weights, k=length)
        nbits = sum(len(code[s]) for s in msg)
        flip = rng.randrange(nbits // 2)  # flip in the first half, so a resync has room to happen
        r = symbols_until_resync(code, msg, flip)
        if r is None:
            never += 1
        else:
            total += r
            count += 1
            worst = max(worst, r)
    return {"mean": total / count if count else None, "max": worst, "never": never}
