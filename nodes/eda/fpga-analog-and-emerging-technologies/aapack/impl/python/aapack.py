# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aapack/. The authors are listed in prov/11GQMP.jsonl.

"""AAPack: greedy packing with a placement and an intra-cluster route for each candidate.

The logic block has N slots. Slot s holds one LUT with K inputs and, if
has_ff[s], a flip-flop. The block has I input pins. The local routing is a
sparse crossbar: LUT input j of slot s can be driven by the sources in
conn[s][j], where ("pin", p) is input pin p and ("fb", t) is the output of
slot t. LUT inputs of one LUT can be permuted, so a net may use any LUT input
of its slot whose source carries it.

AAPack routes inside the block with PathFinder. This file routes inside the
block with an exact search (pin assignment by backtracking, then one
bipartite matching per slot), so a failed route is a real failure.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional

Source = tuple[str, int]


@dataclass(frozen=True)
class Ble:
    inputs: tuple[str, ...]
    output: str
    registered: bool = False


@dataclass
class Block:
    has_ff: list[bool]
    i_pins: int
    k: int
    conn: list[list[frozenset[Source]]]  # conn[s][j]

    @property
    def n_slots(self) -> int:
        return len(self.has_ff)


@dataclass
class Config:
    slot_of: dict[int, int]  # BLE -> slot
    pin_of: dict[str, int] = field(default_factory=dict)  # external net -> input pin
    lut_in: dict[tuple[int, str], int] = field(default_factory=dict)  # (BLE, net) -> LUT input


def external_inputs(bles: list[Ble], members) -> list[str]:
    driven = {bles[i].output for i in members}
    return sorted({n for i in members for n in bles[i].inputs if n not in driven})


def _match_slot(block: Block, s: int, nets: list[str], source_of: dict[str, Source]) -> Optional[dict[str, int]]:
    """Kuhn's augmenting paths: give each net a distinct LUT input of slot s whose source carries it."""
    owner: dict[int, str] = {}

    def augment(x: str, seen: set[int]) -> bool:
        for j in range(block.k):
            if source_of[x] in block.conn[s][j] and j not in seen:
                seen.add(j)
                if j not in owner or augment(owner[j], seen):
                    owner[j] = x
                    return True
        return False

    for x in nets:
        if not augment(x, set()):
            return None
    return {x: j for j, x in owner.items()}


def route_cluster(bles: list[Ble], block: Block, slot_of: dict[int, int]) -> Optional[Config]:
    """An exact intra-cluster route for fixed slots, or None if none exists."""
    members = list(slot_of)
    driver_slot = {bles[i].output: slot_of[i] for i in members}
    ext = external_inputs(bles, members)
    if len(ext) > block.i_pins:
        return None
    pin_of: dict[str, int] = {}

    def finish() -> Optional[Config]:
        source_of: dict[str, Source] = {x: ("pin", p) for x, p in pin_of.items()}
        source_of.update({x: ("fb", t) for x, t in driver_slot.items()})
        cfg = Config(dict(slot_of), dict(pin_of))
        for i in members:
            m = _match_slot(block, slot_of[i], sorted(set(bles[i].inputs)), source_of)
            if m is None:
                return None
            cfg.lut_in.update({(i, x): j for x, j in m.items()})
        return cfg

    def assign(t: int) -> Optional[Config]:
        if t == len(ext):
            return finish()
        for p in range(block.i_pins):
            if p not in pin_of.values():
                pin_of[ext[t]] = p
                cfg = assign(t + 1)
                if cfg is not None:
                    return cfg
                del pin_of[ext[t]]
        return None

    return assign(0)


def fits_by_count(bles: list[Ble], block: Block, slot_of: dict[int, int]) -> bool:
    """The counting checks of speculative packing: slots, flip-flops, LUT inputs and pins."""
    return (
        len(set(slot_of.values())) == len(slot_of)
        and all(block.has_ff[s] or not bles[i].registered for i, s in slot_of.items())
        and all(len(set(bles[i].inputs)) <= block.k for i in slot_of)
        and len(external_inputs(bles, slot_of)) <= block.i_pins
    )


def aapack(
    bles: list[Ble],
    block: Block,
    lam: Fraction = Fraction(0),
    crit: Optional[dict[tuple[int, int], Fraction]] = None,
    speculative: bool = False,
) -> list[Config]:
    """Pack the BLEs into blocks. Returns one Config per block, with the route inside it."""
    crit = crit or {}
    g = block.k + 1
    nets_of = [set(b.inputs) | {b.output} for b in bles]
    ble_crit = [Fraction(0)] * len(bles)
    pair_crit: list[dict[int, Fraction]] = [{} for _ in bles]
    for (u, v), c in crit.items():
        ble_crit[u] = max(ble_crit[u], c)
        ble_crit[v] = max(ble_crit[v], c)
        pair_crit[u][v] = max(pair_crit[u].get(v, Fraction(0)), c)
        pair_crit[v][u] = max(pair_crit[v].get(u, Fraction(0)), c)

    def legal(slot_of: dict[int, int], counting_only: bool) -> bool:
        if not fits_by_count(bles, block, slot_of):
            return False
        return counting_only or route_cluster(bles, block, slot_of) is not None

    def grow(seed: int, unclustered: set[int], counting_only: bool) -> dict[int, int]:
        slot_of: dict[int, int] = {}
        for s in range(block.n_slots):  # @line L3
            if legal({seed: s}, counting_only):
                slot_of = {seed: s}
                break
        if not slot_of:
            raise ValueError(f"BLE {seed} fits in no slot of an empty block")
        while len(slot_of) < block.n_slots:  # @line L4
            cluster_nets = set().union(*(nets_of[i] for i in slot_of))

            def attraction(b: int) -> Fraction:
                c = max((pair_crit[b].get(m, Fraction(0)) for m in slot_of), default=Fraction(0))
                return lam * c + (1 - lam) * Fraction(len(nets_of[b] & cluster_nets), g)

            order = sorted(unclustered - set(slot_of), key=lambda b: (-attraction(b), -len(bles[b].inputs), b))  # @line L5
            added = False
            for b in order:  # @line L6
                for s in range(block.n_slots):
                    if s not in slot_of.values() and legal({**slot_of, b: s}, counting_only):  # @line L7
                        slot_of[b] = s
                        added = True
                        break
                if added:
                    break
            if not added:  # @line L8
                break
        return slot_of

    unclustered = set(range(len(bles)))
    out = []
    while unclustered:  # @line L1
        seed = max(unclustered, key=lambda i: (ble_crit[i], len(bles[i].inputs), -i))  # @line L2
        slot_of = grow(seed, unclustered, speculative)
        cfg = route_cluster(bles, block, slot_of)  # @line L9
        if cfg is None:  # @line L10
            slot_of = grow(seed, unclustered, False)
            cfg = route_cluster(bles, block, slot_of)
        assert cfg is not None
        out.append(cfg)  # @line L11
        unclustered -= set(slot_of)
    return out


def check_config(bles: list[Ble], block: Block, cfg: Config) -> bool:
    """Check a configuration directly against the block, with no search."""
    slot_of = cfg.slot_of
    members = set(slot_of)
    if len(set(slot_of.values())) != len(slot_of) or not all(0 <= s < block.n_slots for s in slot_of.values()):
        return False
    if any(bles[i].registered and not block.has_ff[s] for i, s in slot_of.items()):
        return False
    driver_slot = {bles[i].output: slot_of[i] for i in members}
    ext = set(external_inputs(bles, members))
    if set(cfg.pin_of) != ext or len(set(cfg.pin_of.values())) != len(ext):
        return False
    if not all(0 <= p < block.i_pins for p in cfg.pin_of.values()):
        return False
    for i in members:
        used = [cfg.lut_in.get((i, x)) for x in set(bles[i].inputs)]
        if None in used or len(set(used)) != len(used):
            return False
        for x in set(bles[i].inputs):
            j = cfg.lut_in[(i, x)]
            src = ("fb", driver_slot[x]) if x in driver_slot else ("pin", cfg.pin_of[x])
            if not 0 <= j < block.k or src not in block.conn[slot_of[i]][j]:
                return False
    return True
