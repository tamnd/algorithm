# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-value-cache/. The authors are listed in prov/JVESYS.jsonl.

"""A key-value cache for the decoding of a decoder-only transformer.

The network is a toy: seeded random weights, model width d, h query heads,
g key-value heads (g divides h; g = h is multi-head attention, g = 1 is
multi-query attention), L layers, sinusoidal positions, a ReLU feed-forward
block, residual connections and no layer normalization. It is not trained;
it only gives the cache real keys and values to store. Vectors are lists of
floats.
"""

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from nlslog import argmax, softmax

Vec = List[float]
Mat = List[List[float]]


@dataclass
class Layer:
    wq: Mat
    wk: Mat
    wv: Mat
    wo: Mat
    w1: Mat
    w2: Mat


@dataclass
class Params:
    emb: Mat
    layers: List[Layer]
    d: int
    heads: int
    kv_heads: int
    counter: Dict[str, int] = field(default_factory=lambda: {"scores": 0})

    @property
    def d_k(self) -> int:
        return self.d // self.heads


def make_params(seed: int, vocab: int = 7, d: int = 8, heads: int = 2, kv_heads: int = 2, layers: int = 2, d_ff: int = 16) -> Params:
    """Return a toy network with weights drawn from random.Random(seed)."""
    if d % heads or heads % kv_heads:
        raise ValueError("heads must divide d and kv_heads must divide heads")
    rng = random.Random(seed)
    d_k = d // heads

    def mat(rows: int, cols: int) -> Mat:
        return [[rng.gauss(0.0, 1.0 / math.sqrt(rows)) for _ in range(cols)] for _ in range(rows)]

    emb = mat(vocab, d)
    ls = [Layer(mat(d, d), mat(d, kv_heads * d_k), mat(d, kv_heads * d_k), mat(d, d), mat(d, d_ff), mat(d_ff, d)) for _ in range(layers)]
    return Params(emb, ls, d, heads, kv_heads)


def matvec(x: Vec, w: Mat) -> Vec:
    cols = len(w[0])
    return [math.fsum(x[i] * w[i][j] for i in range(len(x))) for j in range(cols)]


def position(pos: int, d: int) -> Vec:
    """The sinusoidal position vector of Vaswani et al. 2017."""
    out = []
    for i in range(d):
        angle = pos / 10000 ** (2 * (i // 2) / d)
        out.append(math.sin(angle) if i % 2 == 0 else math.cos(angle))
    return out


def split(x: Vec, parts: int) -> List[Vec]:
    size = len(x) // parts
    return [x[i * size : (i + 1) * size] for i in range(parts)]


def attend(params: Params, q: Vec, keys: List[Vec], values: List[Vec]) -> Vec:
    """softmax(q K^T / sqrt(d_k)) V for one query."""
    params.counter["scores"] += len(keys)
    scale = math.sqrt(len(q))
    weights = softmax([math.fsum(a * b for a, b in zip(q, k)) / scale for k in keys])
    return [math.fsum(w * v[j] for w, v in zip(weights, values)) for j in range(len(values[0]))]


def ffn(layer: Layer, x: Vec) -> Vec:
    hidden = [max(0.0, v) for v in matvec(x, layer.w1)]
    return matvec(hidden, layer.w2)


class KVCache:
    """The keys and values of the past positions, per layer and per key-value head."""

    def __init__(self, layers: int, kv_heads: int, d_k: int) -> None:
        self.layers, self.kv_heads, self.d_k = layers, kv_heads, d_k
        self.k: List[List[List[Vec]]] = [[[] for _ in range(kv_heads)] for _ in range(layers)]
        self.v: List[List[List[Vec]]] = [[[] for _ in range(kv_heads)] for _ in range(layers)]

    def append(self, layer: int, keys: List[Vec], values: List[Vec]) -> None:
        """Store the key and the value of the next position of layer, one per head."""
        for g in range(self.kv_heads):
            self.k[layer][g].append(keys[g])
            self.v[layer][g].append(values[g])

    def keys(self, layer: int, g: int) -> List[Vec]:
        return self.k[layer][g]

    def values(self, layer: int, g: int) -> List[Vec]:
        return self.v[layer][g]

    def __len__(self) -> int:
        return len(self.k[self.layers - 1][0])

    def num_floats(self) -> int:
        """2 * L * n * g * d_k numbers; with g = h this is 2 * L * n * d."""
        return 2 * self.layers * len(self) * self.kv_heads * self.d_k


def decode_step(params: Params, token: int, pos: int, cache) -> Vec:
    """Run one new token at position pos through the network, using and filling the cache.

    Return the logits of the next token (tied output embedding).
    """
    x = [e + p for e, p in zip(params.emb[token], position(pos, params.d))]  # @line L1
    per_group = params.heads // params.kv_heads
    for l, layer in enumerate(params.layers):  # @line L2
        qs = split(matvec(x, layer.wq), params.heads)  # @line L3
        ks = split(matvec(x, layer.wk), params.kv_heads)
        vs = split(matvec(x, layer.wv), params.kv_heads)
        cache.append(l, ks, vs)  # @line L4
        heads = [attend(params, qs[j], cache.keys(l, j // per_group), cache.values(l, j // per_group)) for j in range(params.heads)]  # @line L5
        x = [a + b for a, b in zip(x, matvec([v for hd in heads for v in hd], layer.wo))]  # @line L6
        x = [a + b for a, b in zip(x, ffn(layer, x))]  # @line L7
    return [math.fsum(a * b for a, b in zip(x, e)) for e in params.emb]  # @line L8


def forward_full(params: Params, tokens: List[int]) -> List[Vec]:
    """Recompute every position from scratch with causal attention; return the logits of each."""
    xs = [[e + p for e, p in zip(params.emb[t], position(i, params.d))] for i, t in enumerate(tokens)]
    per_group = params.heads // params.kv_heads
    for layer in params.layers:
        qs = [split(matvec(x, layer.wq), params.heads) for x in xs]
        ks = [split(matvec(x, layer.wk), params.kv_heads) for x in xs]
        vs = [split(matvec(x, layer.wv), params.kv_heads) for x in xs]
        new = []
        for i, x in enumerate(xs):
            heads = []
            for j in range(params.heads):
                g = j // per_group
                heads.append(attend(params, qs[i][j], [ks[t][g] for t in range(i + 1)], [vs[t][g] for t in range(i + 1)]))
            y = [a + b for a, b in zip(x, matvec([v for hd in heads for v in hd], layer.wo))]
            new.append([a + b for a, b in zip(y, ffn(layer, y))])
        xs = new
    return [[math.fsum(a * b for a, b in zip(x, e)) for e in params.emb] for x in xs]


def generate(params: Params, prompt: List[int], steps: int, use_cache: bool = True, cache=None) -> List[int]:
    """Greedy generation of steps new tokens, with the cache or by recomputing each time."""
    tokens = list(prompt)
    if not use_cache:
        for _ in range(steps):
            tokens.append(argmax(forward_full(params, tokens)[-1]))
        return tokens
    if cache is None:
        cache = KVCache(len(params.layers), params.kv_heads, params.d_k)
    logits: Optional[Vec] = None
    for i, t in enumerate(tokens):
        logits = decode_step(params, t, i, cache)
    for s in range(steps):
        tokens.append(argmax(logits))
        if s + 1 < steps:
            logits = decode_step(params, tokens[-1], len(tokens) - 1, cache)
    return tokens


def cache_numbers(layers: int, n: int, d: int, heads: int, kv_heads: int) -> int:
    """The number of stored numbers for one sequence: 2 * layers * n * d * kv_heads / heads."""
    return 2 * layers * n * d * kv_heads // heads


class BlockPool:
    """Fixed size blocks shared by many sequences, as in PagedAttention (Kwon et al. 2023)."""

    def __init__(self, layers: int, kv_heads: int, d_k: int, block_size: int, num_blocks: int) -> None:
        self.layers, self.kv_heads, self.d_k, self.block_size = layers, kv_heads, d_k, block_size
        self.store = [[[[None] * block_size for _ in range(kv_heads)] for _ in range(layers)] for _ in range(num_blocks)]
        self.free = list(range(num_blocks - 1, -1, -1))

    def new_sequence(self) -> "PagedSequence":
        return PagedSequence(self)


class PagedSequence:
    """The cache of one sequence: a block table that maps position // block_size to a block."""

    def __init__(self, pool: BlockPool) -> None:
        self.pool = pool
        self.table: List[int] = []
        self.lengths = [0] * pool.layers

    def append(self, layer: int, keys: List[Vec], values: List[Vec]) -> None:
        pos = self.lengths[layer]
        b = pos // self.pool.block_size
        if b == len(self.table):
            if not self.pool.free:
                raise MemoryError("no free block")
            self.table.append(self.pool.free.pop())
        block = self.pool.store[self.table[b]]
        for g in range(self.pool.kv_heads):
            block[layer][g][pos % self.pool.block_size] = (keys[g], values[g])
        self.lengths[layer] = pos + 1

    def _entries(self, layer: int, g: int):
        bs = self.pool.block_size
        return [self.pool.store[self.table[p // bs]][layer][g][p % bs] for p in range(self.lengths[layer])]

    def keys(self, layer: int, g: int) -> List[Vec]:
        return [kv[0] for kv in self._entries(layer, g)]

    def values(self, layer: int, g: int) -> List[Vec]:
        return [kv[1] for kv in self._entries(layer, g)]

    def __len__(self) -> int:
        return self.lengths[-1]

    def release(self) -> None:
        """Give every block of the sequence back to the pool."""
        for b in reversed(self.table):
            for layer in self.pool.store[b]:
                for slots in layer:
                    for i in range(len(slots)):
                        slots[i] = None
            self.pool.free.append(b)
        self.table = []
        self.lengths = [0] * self.pool.layers
