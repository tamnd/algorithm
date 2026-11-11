# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziv-lempel-entropy-theorem/. The authors are listed in prov/X1WQQT.jsonl.

import math
import random

from ziv_lempel_entropy_theorem import (
    bernoulli,
    binary_entropy,
    code_length,
    decode,
    distinct_parsing_bound,
    encode,
    lz78_parse,
    markov,
    markov_entropy_rate,
    markov_log2_prob,
    max_distinct_phrases_string,
    phrases_as_strings,
    ziv_sum,
)


def _lz78_brute(x: str) -> list[str]:
    """Incremental parse with a set of strings: the shortest prefix of the rest that is new."""
    seen, out, i = set(), [], 0
    while i < len(x):
        j = i + 1
        while j <= len(x) and x[i:j] in seen:
            j += 1
        out.append(x[i:j])
        seen.add(x[i:j])
        i = j
    return out


def test_page_example() -> None:
    x = "1011010100010"
    assert phrases_as_strings(x) == ["1", "0", "11", "01", "010", "00", "10"]
    assert lz78_parse(x) == [(0, "1"), (0, "0"), (1, "1"), (2, "1"), (4, "0"), (2, "0"), (1, "0")]
    code = encode(x)
    assert len(code) == code_length(7) == 21
    assert decode(code, len(x)) == x


def test_edges() -> None:
    assert lz78_parse("") == [] and encode("") == "" and decode("", 0) == ""
    assert phrases_as_strings("0") == ["0"]
    run = "0" * 55  # 1 + 2 + ... + 10 = 55
    assert phrases_as_strings(run) == ["0" * m for m in range(1, 11)]
    assert phrases_as_strings("0" * 57) == ["0" * m for m in range(1, 11)] + ["00"]
    for x in ("0" * 57, "01" * 40, "1"):
        assert decode(encode(x), len(x)) == x


def test_parse_and_code_on_random_input() -> None:
    rng = random.Random(1978)
    for _ in range(400):
        x = "".join(rng.choice("01") for _ in range(rng.randrange(1, 300)))
        pieces = phrases_as_strings(x)
        brute = _lz78_brute(x)
        assert pieces == brute
        assert "".join(pieces) == x
        # All phrases are distinct, except that the last one may repeat an earlier one.
        assert len(set(pieces[:-1])) == len(pieces) - 1
        assert decode(encode(x), len(x)) == x


def test_distinct_parsing_bound() -> None:
    for e in range(10, 19, 2):
        n = 2 ** e
        x = max_distinct_phrases_string(n)
        c = len(lz78_parse(x))
        assert c <= distinct_parsing_bound(n)
        # Here c is of the order n / log2 n.
        assert c >= n / math.log2(n)
    rng = random.Random(5)
    for n in (2 ** 12, 2 ** 15):
        assert len(lz78_parse(bernoulli(n, 0.5, rng))) <= distinct_parsing_bound(n)


def test_ziv_inequality() -> None:
    rng = random.Random(13)
    for _ in range(60):
        k = rng.randrange(0, 3)
        q = {}
        for v in range(2 ** k):
            q[format(v, "0{}b".format(k)) if k else ""] = rng.uniform(0.05, 0.95)
        x = markov(rng.randrange(50, 3000), 0.3, 0.4, rng)
        pieces = phrases_as_strings(x)
        if len(set(pieces)) < len(pieces):  # keep a distinct parse
            pieces = pieces[:-1]
            x = "".join(pieces)
        assert markov_log2_prob(x, k, q) <= -ziv_sum(pieces, x, k) + 1e-9


def test_monte_carlo_rate_approaches_entropy() -> None:
    # Fixed seeds. The LZ78 code length per symbol is above the entropy rate
    # and goes down, but slowly: at n = 2^16 it is still 0.12 to 0.17 above it.
    sources = [
        (lambda n, r: bernoulli(n, 0.5, r), 1.0),
        (lambda n, r: bernoulli(n, 0.1, r), binary_entropy(0.1)),
        (lambda n, r: markov(n, 0.05, 0.2, r), markov_entropy_rate(0.05, 0.2)),
    ]
    for gen, h in sources:
        rates = []
        for e in (12, 14, 16):
            n = 2 ** e
            x = gen(n, random.Random(e))
            rates.append(len(encode(x)) / n)
        assert rates[0] > rates[1] > rates[2] > h
        assert rates[2] - h < 0.25
