# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-axis-printing-decomposition/. The authors are listed in prov/N5ERYT.jsonl.

"""Support-free decomposition of a voxel model by planar cuts.

A model is a set of integer voxels (x, y, z) with z >= 0. The platform lies
under z = 0. A part P is printed in a direction d, layer by layer in the order
of <v, d>. A voxel v can be deposited when one voxel of its support block
S(v, d), the 3 x 3 block of voxels one layer below v, is already solid. In the
direction +z a voxel with z = 0 rests on the platform. This is a 45 degree
overhang rule on the voxel grid.

The search peels parts off the top: from the remaining set R it cuts
P = {v in R : <v, d> >= c}. Every voxel of P must have a support in R. The
remaining set after the last cut is the base, printed in +z. The parts are
printed in the reverse order of the cuts.
"""

DIRECTIONS = {"+z": (0, 0, 1), "+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0)}


def dot(v, d):
    return v[0] * d[0] + v[1] * d[1] + v[2] * d[2]


def support_block(v, d):
    """The 9 voxels one layer below v in the direction d."""
    axis = [i for i in range(3) if d[i] != 0][0]
    others = [i for i in range(3) if i != axis]
    below = list(v)
    below[axis] -= d[axis]
    out = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            w = list(below)
            w[others[0]] += a
            w[others[1]] += b
            out.append(tuple(w))
    return out


def supported(v, d, solid):
    if d == (0, 0, 1) and v[2] == 0:
        return True  # the platform
    return any(w in solid for w in support_block(v, d))


def unsupported(region, d):
    """Voxels of the region with no support inside the region."""
    return [v for v in region if not supported(v, d, region)]


def is_base(region):
    return not unsupported(region, (0, 0, 1))


def cuts(region, name):
    """All valid planar cuts of the region in one direction (lines L6 to L8).

    The validity of P = {<v, d> >= c} only asks that every voxel of P has a
    support in the region, so the valid thresholds are all c above the top
    level of the unsupported voxels. A cut must leave a nonempty rest.
    """
    d = DIRECTIONS[name]
    levels = sorted({dot(v, d) for v in region})
    bad = unsupported(region, d)
    low = max((dot(v, d) for v in bad), default=None)  # @line L6
    out = []
    for c in levels:
        if (low is None or c > low) and c > levels[0]:  # @line L7
            part = frozenset(v for v in region if dot(v, d) >= c)
            out.append((name, c, part, region - part))  # @line L8
    return out


def score(region):
    """Smaller is better: unsupported voxels of the base, then fewer voxels cut."""
    return (len(unsupported(region, (0, 0, 1))), -len(region))


def beam_decompose(model, width=4, max_cuts=5):
    """Beam search over cut sequences. Return the plan or None.

    A plan is a list of (direction, voxels) in print order: the base first,
    with direction "+z".
    """
    beam = [(frozenset(model), [])]  # @line L1
    for level in range(max_cuts + 1):  # @line L2
        for region, seq in beam:
            if is_base(region):  # @line L3
                return plan_from(region, seq)
        if level == max_cuts:
            break
        children = {}  # @line L4
        for region, seq in beam:
            for name in DIRECTIONS:  # @line L5
                for d, c, part, rest in cuts(region, name):
                    if rest not in children:
                        children[rest] = seq + [(d, c, part)]
        ranked = sorted(children.items(), key=lambda kv: (score(kv[0]), sorted(kv[0])))
        beam = ranked[:width]  # @line L9
    return None  # @line L10


def plan_from(base, seq):
    """The base, then the parts in the reverse order of the cuts."""
    plan = [("+z", base)]  # @line L11
    for d, c, part in reversed(seq):
        plan.append((d, part))
    return plan


def exhaustive_min_parts(model, max_parts=4):
    """Breadth first search over all cut sequences. Return the least number
    of parts (base included) or None if more than max_parts are needed."""
    level = {frozenset(model)}
    seen = set(level)
    for k in range(1, max_parts + 1):
        if any(is_base(r) for r in level):
            return k
        nxt = set()
        for region in level:
            for name in DIRECTIONS:
                for _, _, _, rest in cuts(region, name):
                    if rest not in seen:
                        seen.add(rest)
                        nxt.add(rest)
        level = nxt
    return None


def simulate(model, plan):
    """Independent check of a plan, voxel by voxel.

    Print each part in its order, each part in increasing <v, d>. Every voxel
    must touch a solid voxel of its support block (or the platform), and no
    solid voxel may lie strictly above the current layer, which is where the
    print head is (half-space head model). Return (ok, message).
    """
    solid = set()
    seen = set()
    for name, part in plan:
        d = DIRECTIONS[name]
        if seen & set(part):
            return False, "parts overlap"
        seen |= set(part)
        for v in sorted(part, key=lambda v: dot(v, d)):
            layer = dot(v, d)
            ok = d == (0, 0, 1) and v[2] == 0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        w = (v[0] + dx, v[1] + dy, v[2] + dz)
                        if w in solid and dot(w, d) == layer - 1:
                            ok = True
            if not ok:
                return False, "overhang at %s in %s" % (v, name)
            if any(dot(w, d) > layer for w in solid):
                return False, "head collision at %s in %s" % (v, name)
            solid.add(v)
    if solid != set(model):
        return False, "parts do not cover the model"
    return True, "ok"


def gallows(arm=6, height=6, depth=2):
    """A column of 2 x depth voxels with an arm at the top that sticks out."""
    vox = set()
    for z in range(height):
        for x in range(2):
            for y in range(depth):
                vox.add((x, y, z))
    for z in range(height - 2, height):
        for x in range(2, 2 + arm):
            for y in range(depth):
                vox.add((x, y, z))
    return frozenset(vox)


def tee(arm=4, height=6, depth=2):
    """A column with arms on both sides at the top."""
    vox = set()
    for z in range(height):
        for x in range(2):
            for y in range(depth):
                vox.add((x, y, z))
    for z in range(height - 2, height):
        for x in list(range(-arm, 0)) + list(range(2, 2 + arm)):
            for y in range(depth):
                vox.add((x, y, z))
    return frozenset(vox)
