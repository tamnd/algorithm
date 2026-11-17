# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-reflection-method/. The authors are listed in prov/EA23M6.jsonl.
"""Double reflection method for a rotation minimizing frame (Wang, Juttler, Zheng and Liu 2008).

The input is a list of points x_0, ..., x_N on a space curve, the unit
tangents t_0, ..., t_N at these points, and a unit normal r_0 at x_0. Each
step maps the frame at x_i to the frame at x_(i+1) by two reflections:

    R1 is the reflection in the plane through the midpoint of x_i x_(i+1)
       that is perpendicular to v1 = x_(i+1) - x_i,
    R2 is the reflection that takes R1 t_i to t_(i+1), with v2 = t_(i+1) - R1 t_i,

and r_(i+1) = R2 R1 r_i, s_(i+1) = t_(i+1) x r_(i+1). The product R2 R1 is a
rotation that takes t_i to t_(i+1), so every frame (r_i, s_i, t_i) is a right
handed orthonormal frame. For points u_i = a + i h on a smooth curve, the
global error is O(h^4) (Theorem 4.5 of the paper).

If v1 = 0 (a repeated point), this implementation uses v1 = t_i, the limit
of the chord direction; then the step is the smallest rotation from t_i to
t_(i+1). For small steps on a smooth curve, R1 t_i is close to -t_(i+1) and
v2 . v2 is close to 4. If v2 . v2 < C2_MIN, the direction of v2 is not
determined and ValueError is raised: the step is too coarse.
"""

from anim import cross, dot, normalize, scale, sub

C2_MIN = 1e-16


def reflect(a, v, c):
    """Return the reflection a - (2 / c) (v . a) v of a in the plane normal to v, with c = v . v."""
    return sub(a, scale(v, 2.0 * dot(v, a) / c))


def double_reflection(points, tangents, r0):
    """Return the frames [(r_i, s_i, t_i)] of the double reflection method.

    points and tangents have the same length N + 1 >= 1. The tangents are
    normalized here. r0 is projected onto the plane normal to t_0 and
    normalized, so any vector that is not parallel to t_0 is accepted.
    """
    if len(points) != len(tangents) or len(points) == 0:
        raise ValueError("points and tangents must be nonempty lists of the same length")
    ts = [normalize(t) for t in tangents]
    t0 = ts[0]
    r = normalize(sub(r0, scale(t0, dot(r0, t0))))
    frames = [(r, cross(t0, r), t0)]
    for i in range(len(points) - 1):  # @line L1
        v1 = sub(points[i + 1], points[i])  # @line L2
        c1 = dot(v1, v1)
        if c1 == 0.0:
            # A repeated point: use the limit direction of the chord, the tangent.
            v1, c1 = ts[i], 1.0
        r_l = reflect(r, v1, c1)  # @line L3
        t_l = reflect(ts[i], v1, c1)  # @line L4
        v2 = sub(ts[i + 1], t_l)  # @line L5
        c2 = dot(v2, v2)
        if c2 < C2_MIN:
            raise ValueError("step %d is too coarse: the reflected tangent equals the next tangent" % i)
        r = reflect(r_l, v2, c2)  # @line L6
        frames.append((r, cross(ts[i + 1], r), ts[i + 1]))  # @line L7
    return frames  # @line L8


def sample_curve(c, dc, a, b, n):
    """Return the points c(u_i) and the unit tangents of dc(u_i) for u_i = a + i (b - a) / n."""
    us = [a + (b - a) * i / n for i in range(n + 1)]
    return [tuple(c(u)) for u in us], [normalize(dc(u)) for u in us]


def rotation_minimizing_frames(c, dc, a, b, n, r0):
    """Return the frames of the double reflection method at n + 1 equally spaced parameters of c."""
    points, tangents = sample_curve(c, dc, a, b, n)
    return double_reflection(points, tangents, r0)
