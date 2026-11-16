# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monoslam/. The authors are listed in prov/HXRXPQ.jsonl.

"""A TOY core of MonoSLAM, in the plane. It is not MonoSLAM itself.

It keeps the structure of Davison, Reid, Molton and Stasse (2007): one EKF
over a camera with a constant velocity model and a sparse map of points;
a search for each point only inside the gate of its predicted image
position; new points that start as a ray with 100 depth samples from 0.5 m
to 5 m and enter the map when the depth spread is small; deletion of points
that often fail to match. What it leaves out makes it a toy:

- The world is a plane and the camera has a one-dimensional image: a point
  at (a, b) in the camera frame (a > 0) appears at the pixel u = F b / a.
- There is no image processing. A "detection" is a pixel with the id of the
  true point, and the id stands for the appearance of the image patch: the
  search of line L4 finds a point if its detection lies inside the gate.
- The state has no quaternion: the camera is (x, y, theta, vx, vy, omega).

  MonoSLAM(...)                    the filter; .frame(detections) is one step, lines L1 to L8
  project(cam, p), project_jac     the camera model and its Jacobians
  simulate_detections(...)         a simulated image for the tests
"""

import math

import robest

F = 500.0  # the focal length in pixels
HALF_WIDTH = 400.0  # the image spans u in [-400, 400], about +-38.7 degrees
CAM = 6  # x, y, theta, vx, vy, omega


def project(cam, p):
    """Return the pixel of the world point p, or None if p is behind the camera."""
    c, s = math.cos(cam[2]), math.sin(cam[2])
    dx, dy = p[0] - cam[0], p[1] - cam[1]
    a = c * dx + s * dy
    b = -s * dx + c * dy
    if a <= 1e-9:
        return None
    return F * b / a


def project_jac(cam, p):
    """Return (d u / d(x, y, theta), d u / d p) at the camera pose and the point."""
    c, s = math.cos(cam[2]), math.sin(cam[2])
    dx, dy = p[0] - cam[0], p[1] - cam[1]
    a = c * dx + s * dy
    b = -s * dx + c * dy
    # u = F b / a; du/da = -F b / a^2, du/db = F / a
    ua, ub = -F * b / (a * a), F / a
    dp = [ua * c - ub * s, ua * s + ub * c]  # d u / d p
    dth = ua * b + ub * (-a)  # da/dtheta = b, db/dtheta = -a
    return [-dp[0], -dp[1], dth], dp


def in_view(u):
    return u is not None and -HALF_WIDTH <= u <= HALF_WIDTH


class Ray:
    """A new point whose depth is not known yet: 100 depth samples along a ray."""

    def __init__(self, origin, angle, n=100, near=0.5, far=5.0):
        self.origin, self.angle = origin, angle
        self.depths = [near + (far - near) * (k + 0.5) / n for k in range(n)]
        self.logw = [0.0] * n

    def point(self, d):
        return [self.origin[0] + d * math.cos(self.angle), self.origin[1] + d * math.sin(self.angle)]

    def stats(self):
        top = max(self.logw)
        w = [math.exp(v - top) for v in self.logw]
        t = sum(w)
        mean = sum(wi * d for wi, d in zip(w, self.depths)) / t
        var = sum(wi * (d - mean) ** 2 for wi, d in zip(w, self.depths)) / t
        return mean, var


class MonoSLAM:
    """The EKF state is the camera (6 numbers) and then two numbers per map point."""

    def __init__(self, cam, cam_cov, known_points, known_var=1e-6, accel_sd=1.0, alpha_sd=1.0, pixel_sd=1.0, dt=1.0 / 30.0, target=6, ratio=0.3):
        self.mu = list(cam)
        n = CAM + 2 * len(known_points)
        self.cov = [[0.0] * n for _ in range(n)]
        for i in range(CAM):
            for j in range(CAM):
                self.cov[i][j] = cam_cov[i][j]
        self.ids = []
        for pid, p in known_points:  # the known target fixes the scale
            k = len(self.mu)
            self.mu += list(p)
            self.cov[k][k] = self.cov[k + 1][k + 1] = known_var
            self.ids.append(pid)
        self.tries = {pid: [0, 0] for pid, _ in known_points}  # attempts, failures
        self.rays = {}
        self.accel_sd, self.alpha_sd, self.r = accel_sd, alpha_sd, pixel_sd * pixel_sd
        self.dt, self.target, self.ratio = dt, target, ratio

    # -------------------------------------------------------------- the EKF parts

    def predict(self):
        """Constant velocity: only the camera rows and columns of the covariance change."""
        dt, mu, cov = self.dt, self.mu, self.cov
        mu[0] += mu[3] * dt
        mu[1] += mu[4] * dt
        mu[2] = robest.wrap_angle(mu[2] + mu[5] * dt)
        fc = [[1.0 if i == j else 0.0 for j in range(CAM)] for i in range(CAM)]
        fc[0][3] = fc[1][4] = fc[2][5] = dt
        n = len(mu)
        # rows of F Sigma for the camera; the map rows stay
        rows = [[sum(fc[i][k] * cov[k][j] for k in range(CAM) if fc[i][k] != 0.0) for j in range(n)] for i in range(CAM)]
        for i in range(CAM):
            cov[i] = rows[i]
        for i in range(n):  # then (F Sigma) F^T on the camera columns
            row = cov[i]
            new = [sum(row[k] * fc[j][k] for k in range(CAM) if fc[j][k] != 0.0) for j in range(CAM)]
            row[:CAM] = new
        qa = (self.accel_sd * dt) ** 2
        qw = (self.alpha_sd * dt) ** 2
        # a velocity change V over the frame moves the position by V dt
        for pos, vel, q in ((0, 3, qa), (1, 4, qa), (2, 5, qw)):
            cov[pos][pos] += q * dt * dt
            cov[pos][vel] += q * dt
            cov[vel][pos] += q * dt
            cov[vel][vel] += q

    def scalar_update(self, h, nu, s):
        """EKF update with one scalar reading: h is a dict {index: derivative}."""
        cov, n = self.cov, len(self.mu)
        pht = [sum(cov[i][k] * v for k, v in h.items()) for i in range(n)]
        gain = [x / s for x in pht]
        for i in range(n):
            self.mu[i] += gain[i] * nu
            gi = gain[i]
            if gi != 0.0:
                row = cov[i]
                for j in range(n):
                    row[j] -= gi * pht[j]
        self.mu[2] = robest.wrap_angle(self.mu[2])

    def predicted(self, k):
        """Return (u_hat, h, s) for the map point at state index k, or None if out of view."""
        cam, p = self.mu[:3], self.mu[k : k + 2]
        u = project(cam, p)
        if not in_view(u):
            return None
        dc, dp = project_jac(cam, p)
        h = {0: dc[0], 1: dc[1], 2: dc[2], k: dp[0], k + 1: dp[1]}
        s = self.r + sum(a * self.cov[i][j] * b for i, a in h.items() for j, b in h.items())
        return u, h, s

    # -------------------------------------------------------------- one frame

    def frame(self, detections, gate=robest.CHI2[(1, 0.99)]):
        """One frame. detections maps a point id to its measured pixel u."""
        self.predict()  # @line L1
        for idx, pid in enumerate(self.ids):  # @line L2
            k = CAM + 2 * idx
            pred = self.predicted(k)  # @line L3
            if pred is None:
                continue
            u_hat, h, s = pred
            self.tries[pid][0] += 1
            u = detections.get(pid)  # @line L4
            if u is None or (u - u_hat) ** 2 / s > gate:
                self.tries[pid][1] += 1
                continue
            self.scalar_update(h, u - u_hat, s)  # @line L5
        self.update_rays(detections)  # @line L6
        visible = sum(1 for idx in range(len(self.ids)) if self.predicted(CAM + 2 * idx) is not None)
        for pid, u in sorted(detections.items()):  # @line L7
            if visible + len(self.rays) >= self.target:
                break
            if pid not in self.ids and pid not in self.rays:
                self.rays[pid] = Ray(self.mu[:2], self.mu[2] + math.atan2(u, F))
        self.delete_bad()  # @line L8

    def update_rays(self, detections):
        cam = self.mu[:3]
        for pid in list(self.rays):
            ray = self.rays[pid]
            u = detections.get(pid)
            if u is None:
                continue
            for i, d in enumerate(ray.depths):
                p = ray.point(d)
                u_hat = project(cam, p)
                if u_hat is None:
                    ray.logw[i] = -1e300
                    continue
                dc, _ = project_jac(cam, p)
                s = self.r + sum(dc[a] * self.cov[a][b] * dc[b] for a in range(3) for b in range(3))
                ray.logw[i] += -0.5 * (u - u_hat) ** 2 / s - 0.5 * math.log(s)
            mean, var = ray.stats()
            if math.sqrt(var) / mean < self.ratio:
                self.add_point(pid, ray, u, mean, var)
                del self.rays[pid]

    def add_point(self, pid, ray, u, depth_mean, depth_var):
        """Put a ray into the map: p = cam + d (cos(theta + b), sin(theta + b)), b = atan(u / F)."""
        cam = self.mu[:3]
        p0 = ray.point(depth_mean)
        d = math.hypot(p0[0] - cam[0], p0[1] - cam[1])
        b = math.atan2(u, F)
        ang = cam[2] + b
        c, s = math.cos(ang), math.sin(ang)
        p = [cam[0] + d * c, cam[1] + d * s]
        jc = [[1.0, 0.0, -d * s], [0.0, 1.0, d * c]]  # d p / d (x, y, theta)
        db = F / (F * F + u * u)  # d b / d u
        ju = [-d * s * db, d * c * db]
        jd = [c, s]
        n = len(self.mu)
        cross = [[sum(jc[r][a] * self.cov[a][j] for a in range(3)) for j in range(n)] for r in range(2)]
        pp = [[sum(cross[r][a] * jc[q][a] for a in range(3)) + ju[r] * ju[q] * self.r + jd[r] * jd[q] * depth_var for q in range(2)] for r in range(2)]
        for i in range(n):
            self.cov[i] += [cross[0][i], cross[1][i]]
        self.cov.append(cross[0] + pp[0])
        self.cov.append(cross[1] + pp[1])
        self.mu += p
        self.ids.append(pid)
        self.tries[pid] = [0, 0]

    def delete_bad(self, min_tries=10):
        for idx in range(len(self.ids) - 1, -1, -1):
            pid = self.ids[idx]
            tries, fails = self.tries[pid]
            if tries >= min_tries and 2 * fails > tries:
                k = CAM + 2 * idx
                del self.mu[k : k + 2]
                del self.cov[k : k + 2]
                for row in self.cov:
                    del row[k : k + 2]
                del self.ids[idx]
                del self.tries[pid]

    def point(self, pid):
        idx = self.ids.index(pid)
        return self.mu[CAM + 2 * idx : CAM + 2 * idx + 2]


def simulate_detections(cam, points, rng, pixel_sd=1.0):
    """Return {id: pixel} for the points in view of the true camera, with noise."""
    out = {}
    for pid, p in points.items():
        u = project(cam, p)
        if in_view(u):
            out[pid] = u + pixel_sd * rng.gauss(0.0, 1.0)
    return out
