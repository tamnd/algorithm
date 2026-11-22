# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sisa-training/. The authors are listed in prov/P6S600.jsonl.

"""SISA training of Bourtoule et al. (2021): sharded, isolated, sliced and aggregated training with exact deletion.

Each constituent model is a logistic regression trained by deterministic full-batch
gradient descent, so that deletion can be checked bit for bit against retraining. The
tests use synthetic blobs from mlkit with a fixed seed.
"""

import random
from dataclasses import dataclass, field
from typing import Sequence

import mlkit

Vector = list[float]
Record = tuple[Vector, int]
Params = tuple[Vector, float]


@dataclass
class Sisa:
    """The state of SISA: records by id, the ids of each slice of each shard, and the checkpoints.

    slices[k][r] is the sorted list of ids in slice r of shard k. ckpt[k][r] is the model of
    shard k after slice r, and ckpt[k][0] is the zero start. The cost counter adds one for
    each record whose gradient is computed.
    """

    records: dict[int, Record]
    slices: list[list[list[int]]]
    ckpt: list[list[Params]]
    steps: int
    lr: float
    l2: float
    cost: int = field(default=0)


def assign(ids: Sequence[int], shards: int, slices: int, seed: int) -> dict[int, tuple[int, int]]:
    """A fixed partition of the ids into shards and slices, from a seeded shuffle.

    After the shuffle, the j-th id goes to shard j mod shards, and within its shard to the
    slice given by its rank, in nearly equal runs. Cost O(N log N) for N ids.
    """
    order = sorted(ids)
    random.Random(seed).shuffle(order)
    per_shard: list[list[int]] = [order[k::shards] for k in range(shards)]
    out: dict[int, tuple[int, int]] = {}
    for k, part in enumerate(per_shard):
        for rank, i in enumerate(part):
            out[i] = (k, rank * slices // max(len(part), 1))
    return out


def gd_steps(start: Params, data: Sequence[Record], steps: int, lr: float, l2: float) -> tuple[Params, int]:
    """Full-batch gradient descent on the mean logistic loss plus (l2 / 2) ||w||^2, from start.

    Returns the new parameters and the number of per-record gradients computed. An empty
    data set leaves the parameters unchanged. Cost O(steps |data| d).
    """
    w, b = list(start[0]), start[1]
    n = len(data)
    if n == 0:
        return (w, b), 0
    d = len(w)
    for _ in range(steps):
        gw = [0.0] * d
        gb = 0.0
        for x, y in data:
            g = mlkit.sigmoid(mlkit.dot(w, x) + b) - y
            for j in range(d):
                gw[j] += g * x[j]
            gb += g
        w = [w[j] - lr * (gw[j] / n + l2 * w[j]) for j in range(d)]
        b -= lr * gb / n
    return (w, b), steps * n


def _prefix(model: Sisa, k: int, r: int) -> list[Record]:
    """The records of slices 0..r of shard k, slice by slice and by id inside a slice."""
    return [model.records[i] for t in range(r + 1) for i in model.slices[k][t]]


def sisa_train(
    records: dict[int, Record], where: dict[int, tuple[int, int]], shards: int, slices: int, steps: int, lr: float, l2: float
) -> Sisa:
    """Train one model per shard, slice by slice, and keep a checkpoint after each slice.

    Precondition: where maps every id of records to (shard, slice) with shard < shards and
    slice < slices, and all records have the same dimension d. Cost O(steps d sum_k sum_r |prefix k r|),
    which is O(steps d N R / 2) for N records in equal slices, and O(S R d) space for checkpoints.
    """
    d = len(next(iter(records.values()))[0])
    parts: list[list[list[int]]] = [[[] for _ in range(slices)] for _ in range(shards)]
    for i in sorted(records):  # @line L1
        k, r = where[i]
        parts[k][r].append(i)
    model = Sisa(dict(records), parts, [], steps, lr, l2)
    for k in range(shards):  # @line L2
        theta: Params = ([0.0] * d, 0.0)  # @line L3
        row = [theta]
        for r in range(slices):  # @line L4
            theta, c = gd_steps(theta, _prefix(model, k, r), steps, lr, l2)  # @line L5
            model.cost += c
            row.append(theta)
        model.ckpt.append(row)
    return model


def predict(model: Sisa, x: Sequence[float]) -> int:
    """Majority vote of the shard models on x, with a tie going to label 0. Cost O(S d)."""
    votes = sum(1 for row in model.ckpt if mlkit.dot(row[-1][0], x) + row[-1][1] > 0)  # @line L6
    return 1 if 2 * votes > len(model.ckpt) else 0


def sisa_delete(model: Sisa, i: int) -> int:
    """Remove record i and retrain its shard from the checkpoint before its slice. Returns the cost.

    Precondition: i is a record of the model. After the call the model equals sisa_train on
    the remaining records with the same partition. Cost O(steps d sum_{t >= r} |prefix k t|)
    for the shard k and slice r of i; the other shards are not touched.
    """
    k, r = next((k, r) for k in range(len(model.slices)) for r in range(len(model.slices[k])) if i in model.slices[k][r])  # @line L7
    model.slices[k][r].remove(i)
    del model.records[i]
    theta = model.ckpt[k][r]  # @line L8
    spent = 0
    for t in range(r, len(model.slices[k])):  # @line L9
        theta, c = gd_steps(theta, _prefix(model, k, t), model.steps, model.lr, model.l2)
        spent += c
        model.ckpt[k][t + 1] = theta
    model.cost += spent
    return spent
