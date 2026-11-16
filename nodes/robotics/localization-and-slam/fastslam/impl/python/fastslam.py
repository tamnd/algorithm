# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fastslam/. The authors are listed in prov/RCNQFQ.jsonl.

"""FastSLAM 1.0 with known correspondences, for planar landmark SLAM.

After Montemerlo, Thrun, Koller and Wegbreit (2002) and Thrun, Burgard and
Fox (2005), Table 13.1. Each particle holds a sampled pose and one small EKF
(a 2-vector mean and a 2x2 covariance) per landmark. The landmarks of a
particle live in a persistent complete binary tree, indexed by the landmark
id: an update copies only the path from the root to one leaf, O(log m), and
resampling copies a particle by sharing its tree, O(1).

  Tree                                   the persistent tree (get, set)
  Particle                               pose, tree, weight
  fastslam_step(ps, u, dt, zs, ids, rng)  one step, lines L1 to L9

The motion model is the velocity model with the noise
M = diag(a1 v^2 + a2 w^2, a3 v^2 + a4 w^2) on the control, and the
readings are (range, bearing) with the noise covariance Q.
"""

import math

import rbm
import robest

STRAIGHT = 1e-9


# ---------------------------------------------------------------- persistent tree


class Tree:
    """A persistent map from the ids 0 .. 2^depth - 1 to values.

    Inner nodes are pairs (left, right); a missing subtree is None. set
    returns a new tree and leaves the old one valid: it creates depth + 1
    nodes and shares all others.
    """

    __slots__ = ("root", "depth", "created")

    def __init__(self, root=None, depth=0):
        self.root = root
        self.depth = depth
        self.created = 0  # nodes created by the set that made this tree

    def get(self, i):
        if i >> self.depth:
            return None
        node = self.root
        for level in range(self.depth - 1, -1, -1):
            if node is None:
                return None
            node = node[(i >> level) & 1]
        return node[0] if node is not None else None

    def set(self, i, value):
        root, depth = self.root, self.depth
        while i >> depth:  # grow: the old tree becomes the left subtree
            root = (root, None) if root is not None else None
            depth += 1
        out = Tree(_set(root, depth, i, value), depth)
        out.created = depth + 1
        return out

    def items(self):
        out = []
        _items(self.root, self.depth, 0, out)
        return out


def _set(node, level, i, value):
    if level == 0:
        return (value,)
    bit = (i >> (level - 1)) & 1
    left, right = node if node is not None else (None, None)
    if bit == 0:
        return (_set(left, level - 1, i, value), right)
    return (left, _set(right, level - 1, i, value))


def _items(node, level, prefix, out):
    if node is None:
        return
    if level == 0:
        out.append((prefix, node[0]))
        return
    _items(node[0], level - 1, prefix << 1, out)
    _items(node[1], level - 1, (prefix << 1) | 1, out)


# ---------------------------------------------------------------- models


def motion(x, v, w, dt):
    """Return the pose after moving with the control (v, w) for dt along an arc."""
    th = x[2]
    if abs(w) < STRAIGHT:
        return [x[0] + v * dt * math.cos(th), x[1] + v * dt * math.sin(th), th]
    r = v / w
    return [
        x[0] - r * math.sin(th) + r * math.sin(th + w * dt),
        x[1] + r * math.cos(th) - r * math.cos(th + w * dt),
        robest.wrap_angle(th + w * dt),
    ]


def sample_motion(rng, x, u, dt, alphas):
    """Draw a pose from the velocity motion model: line L2."""
    v, w = u
    a1, a2, a3, a4 = alphas
    vn = v + math.sqrt(a1 * v * v + a2 * w * w) * rng.gauss(0.0, 1.0)
    wn = w + math.sqrt(a3 * v * v + a4 * w * w) * rng.gauss(0.0, 1.0)
    return motion(x, vn, wn, dt)


def measure(x, m):
    dx, dy = m[0] - x[0], m[1] - x[1]
    return [math.hypot(dx, dy), robest.wrap_angle(math.atan2(dy, dx) - x[2])]


def landmark_jacobian(x, m):
    """Return the 2x2 Jacobian of measure with respect to the landmark."""
    dx, dy = m[0] - x[0], m[1] - x[1]
    q = dx * dx + dy * dy
    s = math.sqrt(q)
    return [[dx / s, dy / s], [-dy / q, dx / q]]


def inverse_measure(x, z):
    a = x[2] + z[1]
    return [x[0] + z[0] * math.cos(a), x[1] + z[0] * math.sin(a)]


# ---------------------------------------------------------------- the filter


class Particle:
    __slots__ = ("pose", "tree", "weight")

    def __init__(self, pose, tree, weight):
        self.pose = pose
        self.tree = tree
        self.weight = weight


def initial_particles(n, pose):
    return [Particle(list(pose), Tree(), 1.0 / n) for _ in range(n)]


def update_landmark(pose, lm, z, q):
    """One EKF update of a landmark (mean, cov) with the reading z from a known pose.

    Return the new (mean, cov) and the importance factor N(z; zhat, S).
    """
    mean, cov = lm
    zhat = measure(pose, mean)  # @line L5
    h = landmark_jacobian(pose, mean)
    s = rbm.add(rbm.mul(rbm.mul(h, cov), rbm.transpose(h)), q)
    k = rbm.mul(rbm.mul(cov, rbm.transpose(h)), rbm.inv(s))  # @line L6
    nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
    new_mean = rbm.add(mean, rbm.matvec(k, nu))
    new_cov = rbm.mul(rbm.sub(rbm.eye(2), rbm.mul(k, h)), cov)
    new_cov = [[new_cov[0][0], (new_cov[0][1] + new_cov[1][0]) / 2.0], [(new_cov[0][1] + new_cov[1][0]) / 2.0, new_cov[1][1]]]
    factor = robest.gauss_pdf(nu, [0.0, 0.0], s)  # @line L7
    return (new_mean, new_cov), factor


def new_landmark(pose, z, q):
    """Initialize a landmark from its first reading: mean h^(-1)(z) and cov H^(-1) Q H^(-T)."""
    mean = inverse_measure(pose, z)
    hinv = rbm.inv(landmark_jacobian(pose, mean))
    return (mean, rbm.mul(rbm.mul(hinv, q), rbm.transpose(hinv)))


def fastslam_step(particles, u, dt, zs, ids, rng, alphas, q, p0=1.0, resample=True):
    """One FastSLAM 1.0 step, in place. Return the new list of particles."""
    for p in particles:  # @line L1
        p.pose = sample_motion(rng, p.pose, u, dt, alphas)  # @line L2
        for z, j in zip(zs, ids):  # @line L3
            lm = p.tree.get(j)
            if lm is None:
                p.tree = p.tree.set(j, new_landmark(p.pose, z, q))  # @line L4
                p.weight *= p0
            else:
                lm, factor = update_landmark(p.pose, lm, z, q)
                p.tree = p.tree.set(j, lm)
                p.weight *= factor
    total = sum(p.weight for p in particles)
    if not resample:
        for p in particles:
            p.weight /= total
        return particles
    idx = robest.low_variance_resample(rng, [p.weight for p in particles])  # @line L8
    n = len(particles)
    return [Particle(list(particles[i].pose), particles[i].tree, 1.0 / n) for i in idx]  # @line L9


def best_particle(particles):
    return max(particles, key=lambda p: p.weight)


def map_estimate(particles):
    """Return the weighted mean of each landmark over the particles that have it."""
    sums = {}
    for p in particles:
        for j, (mean, _) in p.tree.items():
            s = sums.setdefault(j, [0.0, 0.0, 0.0])
            s[0] += p.weight * mean[0]
            s[1] += p.weight * mean[1]
            s[2] += p.weight
    return {j: [s[0] / s[2], s[1] / s[2]] for j, s in sums.items()}
