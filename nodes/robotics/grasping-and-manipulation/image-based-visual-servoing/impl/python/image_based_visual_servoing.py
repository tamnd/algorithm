# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/image-based-visual-servoing/. The authors are listed in prov/A4GWRN.jsonl.

"""Image-based visual servoing (IBVS) with point features.

The camera frame has its z axis along the optical axis. A point with
camera coordinates (X, Y, Z) has the normalized image coordinates
x = X / Z and y = Y / Z (a calibrated camera with unit focal length).
The camera twist V = (omega, v) is expressed in the camera frame,
angular part first, and the camera pose T_wc moves by T_wc exp([V] dt).
The law is V = -lambda L^+ (s - s*), with L the stacked interaction
matrix of the points.

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

from rbm import T_apply, T_inv, mul, norm, pinv_right, se3_exp, sub, transpose


def project(t_wc, p_w):
    """Return (x, y, Z) of the world point p_w seen from the camera pose t_wc."""
    x, y, z = T_apply(T_inv(t_wc), p_w)
    if z <= 0.0:
        raise ValueError("point is behind the camera")
    return x / z, y / z, z


def point_interaction(x, y, z):
    """Return the 2 by 6 interaction matrix of the image point (x, y) at depth z.

    The columns are for (omega_x, omega_y, omega_z, v_x, v_y, v_z).
    """
    return [
        [x * y, -(1.0 + x * x), y, -1.0 / z, 0.0, x / z],
        [1.0 + y * y, -x * y, -x, 0.0, -1.0 / z, y / z],
    ]


def interaction_matrix(s, depths):
    """Stack the point interaction matrices; s = (x1, y1, x2, y2, ...)."""
    rows = []
    for i, z in enumerate(depths):
        rows.extend(point_interaction(s[2 * i], s[2 * i + 1], z))
    return rows


def ibvs_step(s, s_star, depths, lam, choice="current", depths_star=None):
    """Return the camera twist V = -lam L^+ (s - s*).

    choice selects the matrix: "current" uses s and the current depths,
    "desired" uses s* and depths_star, and "mean" uses the mean of the two.
    """
    e = sub(s, s_star)  # @line L1
    if choice == "current":
        lmat = interaction_matrix(s, depths)  # @line L2
    elif choice == "desired":
        lmat = interaction_matrix(s_star, depths_star)
    elif choice == "mean":
        a, b = interaction_matrix(s, depths), interaction_matrix(s_star, depths_star)
        lmat = [[(p + q) / 2.0 for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]
    else:
        raise ValueError("unknown choice of interaction matrix")
    # L has full column rank 6 for three or more points in general position;
    # then L^+ = (L^T L)^-1 L^T, the transpose of the right pseudoinverse of L^T.
    lplus = transpose(pinv_right(transpose(lmat)))  # @line L3
    v = [-lam * sum(lplus[i][j] * e[j] for j in range(len(e))) for i in range(6)]  # @line L4
    return v  # @line L5


def features(t_wc, points_w):
    """Return the feature vector s and the depths of the points."""
    s, depths = [], []
    for p in points_w:
        x, y, z = project(t_wc, p)
        s.extend([x, y])
        depths.append(z)
    return s, depths


def simulate(points_w, t_wc, s_star, lam, dt, steps, choice="current", depths_star=None):
    """Run IBVS with exact features and depths; the twist is held for dt.

    Return a list of (t_wc, s, |e|) for the steps 0 to steps.
    """
    out = []
    for k in range(steps + 1):
        s, depths = features(t_wc, points_w)
        out.append((t_wc, s, norm(sub(s, s_star))))
        if k < steps:
            v = ibvs_step(s, s_star, depths, lam, choice, depths_star)
            t_wc = mul(t_wc, se3_exp([dt * c for c in v]))
    return out
