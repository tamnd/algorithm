# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fastslam/. The authors are listed in prov/RCNQFQ.jsonl.

import math
import random

import rbm
import robest
from fastslam import (
    Tree,
    best_particle,
    fastslam_step,
    initial_particles,
    map_estimate,
    measure,
    motion,
    new_landmark,
    update_landmark,
)

ALPHAS = (0.02, 0.01, 0.01, 0.02)
Q = [[0.01, 0.0], [0.0, 0.0009]]
# eight landmarks around the circle of radius 4 about (0, 4) that the robot drives
LANDMARKS = [[(3.0 if k % 2 else 5.0) * math.cos(k * math.pi / 4.0), 4.0 + (3.0 if k % 2 else 5.0) * math.sin(k * math.pi / 4.0)] for k in range(8)]


def test_tree_matches_a_dict_and_keeps_old_versions():
    rng = random.Random(1)
    tree, ref, versions = Tree(), {}, []
    for _ in range(300):
        i = rng.randrange(200)
        tree = tree.set(i, i * 10 + len(versions))
        ref[i] = i * 10 + len(versions)
        versions.append((tree, dict(ref)))
        assert tree.created == tree.depth + 1
        assert tree.depth <= 8  # 2^8 = 256 >= 200
    for t, r in versions[::25]:
        for i in range(210):
            assert t.get(i) == r.get(i)
        assert sorted(t.items()) == sorted(r.items())


def test_set_shares_all_but_one_path():
    tree = Tree()
    for i in range(64):
        tree = tree.set(i, i)
    new = tree.set(37, -1)
    shared, node_a, node_b = 0, tree.root, new.root
    for level in range(tree.depth - 1, -1, -1):
        bit = (37 >> level) & 1
        assert node_a[1 - bit] is node_b[1 - bit]  # the sibling subtree is shared
        shared += 1
        node_a, node_b = node_a[bit], node_b[bit]
    assert shared == tree.depth == 6
    assert tree.get(37) == 37 and new.get(37) == -1


def ekf_landmark(pose, readings):
    """An independent EKF over one landmark seen from a known pose, written with full matrices."""
    mean = None
    for z in readings:
        if mean is None:
            a = pose[2] + z[1]
            mean = [pose[0] + z[0] * math.cos(a), pose[1] + z[0] * math.sin(a)]
            jac = rbm.num_jacobian(lambda m: measure(pose, m), mean)
            jinv = rbm.inv(jac)
            cov = rbm.mul(rbm.mul(jinv, Q), rbm.transpose(jinv))
            continue
        h = rbm.num_jacobian(lambda m: measure(pose, m), mean, 1e-7)
        zhat = measure(pose, mean)
        s = rbm.add(rbm.mul(rbm.mul(h, cov), rbm.transpose(h)), Q)
        k = rbm.mul(rbm.mul(cov, rbm.transpose(h)), rbm.inv(s))
        nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
        mean = rbm.add(mean, rbm.matvec(k, nu))
        cov = rbm.mul(rbm.sub(rbm.eye(2), rbm.mul(k, h)), cov)
    return mean, cov


def test_with_a_known_pose_each_landmark_is_an_ekf():
    rng = random.Random(2)
    pose = [0.5, -0.2, 0.3]
    readings = []
    for _ in range(6):
        z = measure(pose, LANDMARKS[0])
        readings.append([z[0] + rng.gauss(0.0, 0.1), z[1] + rng.gauss(0.0, 0.03)])
    particles = initial_particles(3, pose)
    for z in readings:
        particles = fastslam_step(particles, (0.0, 0.0), 1.0, [z], [0], rng, (0.0, 0.0, 0.0, 0.0), Q)
    want_mean, want_cov = ekf_landmark(pose, readings)
    for p in particles:
        mean, cov = p.tree.get(0)
        assert max(abs(a - b) for a, b in zip(mean, want_mean)) < 1e-6
        assert max(abs(cov[i][j] - want_cov[i][j]) for i in range(2) for j in range(2)) < 1e-6


def test_the_weight_is_the_innovation_density():
    pose = [0.0, 0.0, 0.0]
    lm = new_landmark(pose, [2.0, 0.5], Q)
    z = [2.1, 0.48]
    (_, cov), factor = update_landmark(pose, lm, z, Q)
    zhat = measure(pose, lm[0])
    h = rbm.num_jacobian(lambda m: measure(pose, m), lm[0], 1e-7)
    s = rbm.add(rbm.mul(rbm.mul(h, lm[1]), rbm.transpose(h)), Q)
    assert abs(factor - robest.gauss_pdf(z, zhat, s)) < 1e-6 * factor
    # first reading: Sigma = H^-1 Q H^-T, so S = 2 Q and the update halves the covariance
    assert max(abs(cov[i][j] - lm[1][i][j] / 2.0) for i in range(2) for j in range(2)) < 1e-12


def test_page_example():
    lm = new_landmark([0.0, 0.0, 0.0], [2.0, 0.5], Q)
    assert abs(lm[0][0] - 1.7552) < 1e-4 and abs(lm[0][1] - 0.9589) < 1e-4
    assert abs(lm[1][0][0] - 0.008529) < 1e-6 and abs(lm[1][0][1] - 0.002693) < 1e-6 and abs(lm[1][1][1] - 0.005071) < 1e-6
    factors = []
    for pose in ([0.0, 0.0, 0.0], [0.0, 0.0, 0.05], [0.3, 0.0, 0.0]):
        (mean, _), f = update_landmark(pose, lm, [2.0, 0.5], Q)
        factors.append(f)
    assert abs(factors[0] - 26.53) < 0.01 and abs(factors[1] - 13.25) < 0.01 and abs(factors[2] - 1.067) < 0.001
    assert abs(mean[0] - 1.914) < 1e-3 and abs(mean[1] - 0.962) < 1e-3
    zhat = measure([0.3, 0.0, 0.0], lm[0])
    assert abs(zhat[0] - 1.7427) < 1e-4 and abs(zhat[1] - 0.5826) < 1e-4
    weights = [f / sum(factors) for f in factors]
    assert [round(w, 2) for w in weights] == [0.65, 0.32, 0.03]


def run(seed, n, steps=60):
    rng = random.Random(seed)
    truth = [0.0, 0.0, 0.0]
    odo = [0.0, 0.0, 0.0]
    particles = initial_particles(n, truth)
    for _ in range(steps):
        u = (0.4, 0.1)
        v, w = u
        vn = v + math.sqrt(ALPHAS[0] * v * v + ALPHAS[1] * w * w) * rng.gauss(0.0, 1.0)
        wn = w + math.sqrt(ALPHAS[2] * v * v + ALPHAS[3] * w * w) * rng.gauss(0.0, 1.0)
        truth = motion(truth, vn, wn, 1.0)
        odo = motion(odo, v, w, 1.0)
        zs, ids = [], []
        for j, lm in enumerate(LANDMARKS):
            z = measure(truth, lm)
            if z[0] < 4.0:
                zs.append([z[0] + rng.gauss(0.0, 0.1), z[1] + rng.gauss(0.0, 0.03)])
                ids.append(j)
        particles = fastslam_step(particles, u, 1.0, zs, ids, rng, ALPHAS, Q)
    return particles, truth, odo


def test_simulation_maps_the_landmarks():
    """A measurement on one loop of 60 steps around 8 landmarks, 30 particles, 2 seeds."""
    errs, pose_errs, odo_errs = [], [], []
    for seed in range(2):
        particles, truth, odo = run(seed, 30)
        est = map_estimate(particles)
        assert len(est) == 8
        errs.extend(math.hypot(est[j][0] - LANDMARKS[j][0], est[j][1] - LANDMARKS[j][1]) for j in est)
        x = sum(p.pose[0] for p in particles) / len(particles)
        y = sum(p.pose[1] for p in particles) / len(particles)
        pose_errs.append(math.hypot(x - truth[0], y - truth[1]))
        odo_errs.append(math.hypot(odo[0] - truth[0], odo[1] - truth[1]))
        assert best_particle(particles).tree.get(0) is not None
    assert sum(errs) / len(errs) < 0.5
    assert max(pose_errs) < 0.3
    assert min(odo_errs) > 0.9


def test_resampling_shares_trees():
    particles, _, _ = run(5, 20, steps=10)
    trees = {id(p.tree) for p in particles}
    assert len(trees) < len(particles)
    assert all(abs(p.weight - 1.0 / 20) < 1e-15 for p in particles)
