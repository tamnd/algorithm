# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-count/. The authors are listed in prov/9P6PN4.jsonl.

"""Word count on a small MapReduce simulator, with and without a combiner.

The simulator core is the one of the mapreduce-model page: M independent map
tasks, a partitioner, a shuffle that is an explicit list of messages, and
reducers that sort and group their input. It counts the pairs and bytes sent
and the input of each reducer. The rest of the file is the word count job, a
Zipf text generator, and the cost formulas of the page.
"""

import itertools
import random
import zlib
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

Pair = tuple[Any, Any]


def pair_size(key: Any, value: Any) -> int:
    """Bytes of a pair in a plain text encoding: the UTF-8 length of key and value."""
    return len(str(key).encode("utf-8")) + len(str(value).encode("utf-8"))


def stable_hash(key: Any) -> int:
    return zlib.crc32(repr(key).encode("utf-8"))


def hash_partitioner(key: Any, r: int) -> int:
    return stable_hash(key) % r


@dataclass
class RoundStats:
    map_tasks: int = 0
    reducers: int = 0
    map_output_pairs: int = 0
    messages: list[tuple[int, int, Any, Any]] = field(default_factory=list)
    reducer_pairs: list[int] = field(default_factory=list)

    @property
    def pairs_sent(self) -> int:
        return len(self.messages)

    @property
    def bytes_sent(self) -> int:
        return sum(pair_size(k, v) for _, _, k, v in self.messages)

    @property
    def max_reducer_pairs(self) -> int:
        return max(self.reducer_pairs, default=0)


def group_sorted(pairs: list[Pair]) -> list[tuple[Any, list[Any]]]:
    ordered = sorted(pairs, key=lambda kv: kv[0])
    return [(k, [v for _, v in run]) for k, run in itertools.groupby(ordered, key=lambda kv: kv[0])]


def run_round(splits: list[list[Pair]], mapper: Callable, reducer: Callable, r: int,
              combiner: Callable | None = None, spill: int | None = None, merge_combine: bool = False,
              rng: random.Random | None = None) -> tuple[list[list[Pair]], RoundStats]:
    """One MapReduce round. The combiner runs on each spill of at most `spill`
    pairs, and once more on the merged spills when merge_combine is set."""
    stats = RoundStats(map_tasks=len(splits), reducers=r)
    sent = []
    for split in splits:  # the map tasks are independent
        emitted = [kv for k, v in split for kv in mapper(k, v)]
        stats.map_output_pairs += len(emitted)
        out = emitted
        if combiner is not None:
            size = spill or max(1, len(emitted))
            out = [kv for i in range(0, len(emitted), size)
                   for key, vals in group_sorted(emitted[i:i + size]) for kv in combiner(key, vals)]
            if merge_combine:
                out = [kv for key, vals in group_sorted(out) for kv in combiner(key, vals)]
        sent.append(out)
    inbox: list[list[Pair]] = [[] for _ in range(r)]
    for src, out in enumerate(sent):
        for k, v in out:
            dst = hash_partitioner(k, r)
            stats.messages.append((src, dst, k, v))
            inbox[dst].append((k, v))
    if rng is not None:
        for box in inbox:
            rng.shuffle(box)
    stats.reducer_pairs = [len(box) for box in inbox]
    outputs = [[kv for key, vals in group_sorted(box) for kv in reducer(key, vals)] for box in inbox]
    return outputs, stats


def make_splits(records: list[Pair], m: int) -> list[list[Pair]]:
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


# The word count job.

def word_count_map(doc_id: Any, text: str) -> Iterable[Pair]:
    for w in text.split():
        yield (w, 1)


def sum_reduce(word: str, counts: list[int]) -> Iterable[Pair]:
    yield (word, sum(counts))


def word_count(docs: list[tuple[Any, str]], m: int, r: int, use_combiner: bool = False,
               spill: int | None = None, merge_combine: bool = False,
               rng: random.Random | None = None) -> tuple[dict[str, int], RoundStats]:
    """Count the words of docs with M = m map tasks and R = r reducers.

    The combiner is sum_reduce itself: integer addition is associative and
    commutative, and the combiner output has the type of the map output.
    """
    outputs, stats = run_round(make_splits(docs, m), word_count_map, sum_reduce, r,
                               combiner=sum_reduce if use_combiner else None,
                               spill=spill, merge_combine=merge_combine, rng=rng)
    return {w: c for out in outputs for w, c in out}, stats


def in_mapper_combining(docs: list[tuple[Any, str]], m: int, r: int) -> tuple[dict[str, int], RoundStats]:
    """Lin and Dyer's in-mapper combining: each map task keeps a Counter over
    its whole split and emits one pair per distinct word at the end."""
    splits = [[(i, " ".join(d for _, d in split))] for i, split in enumerate(make_splits(docs, m))]

    def mapper(_, text):
        return Counter(text.split()).items()

    outputs, stats = run_round(splits, mapper, sum_reduce, r)
    return {w: c for out in outputs for w, c in out}, stats


# A Zipf corpus and the cost formulas of the page.

def zipf_probs(vocab: int, s: float) -> list[float]:
    weights = [1.0 / (i ** s) for i in range(1, vocab + 1)]
    total = sum(weights)
    return [x / total for x in weights]


def zipf_docs(rng: random.Random, n_docs: int, words_per_doc: int, vocab: int,
              s: float = 1.0) -> list[tuple[int, str]]:
    """Documents whose words are drawn independently: word w_i has probability proportional to 1/i^s."""
    names = [f"w{i}" for i in range(1, vocab + 1)]
    probs = zipf_probs(vocab, s)
    return [(d, " ".join(rng.choices(names, weights=probs, k=words_per_doc))) for d in range(n_docs)]


def bytes_without_combiner(counts: dict[str, int]) -> int:
    """Each occurrence of w sends the pair (w, 1): len(w) + 1 bytes."""
    return sum(c * (len(w.encode("utf-8")) + 1) for w, c in counts.items())


def pairs_with_combiner(docs: list[tuple[Any, str]], m: int) -> int:
    """With one combiner pass per map task, task i sends one pair per distinct word of its split."""
    return sum(len({w for _, t in split for w in t.split()}) for split in make_splits(docs, m))


def expected_distinct(tokens: int, probs: list[float]) -> float:
    """E[number of distinct words among `tokens` independent draws] = sum over w of 1 - (1 - p_w)^tokens."""
    return sum(1.0 - (1.0 - p) ** tokens for p in probs)
