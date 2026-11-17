# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eigenfaces/. The authors are listed in prov/22X5JB.jsonl.

"""Eigenfaces of Turk and Pentland (1991).

A face image is a flat list of P gray values (row by row). The training set
has M images with labels. The eigenfaces are the leading eigenvectors of
A A^T, where the columns of A are the training images minus their mean. They
are found from the small M x M matrix A^T A: if A^T A v = lambda v, then
A A^T (A v) = lambda (A v). Recognition projects a new image on the
eigenfaces and takes the nearest class mean in that space.
"""

import math

from cvla import sym_eig


def train(images, labels, k):
    """Return a model dict with the mean, the k eigenfaces, their eigenvalues
    (of A^T A) and the mean weight vector of each class."""
    m = len(images)
    p = len(images[0])
    mean = [sum(img[j] for img in images) / m for j in range(p)]  # @line L1
    phi = [[img[j] - mean[j] for j in range(p)] for img in images]  # @line L2
    small = [[sum(a * b for a, b in zip(phi[i], phi[j])) for j in range(m)] for i in range(m)]  # @line L3
    w, v = sym_eig(small)  # @line L4
    order = sorted(range(m), key=lambda i: -w[i])
    faces, values = [], []
    for i in order[:k]:
        if w[i] <= 1e-10 * max(w[order[0]], 1e-300):
            break
        u = [sum(v[r][i] * phi[r][j] for r in range(m)) for j in range(p)]
        nu = math.sqrt(sum(x * x for x in u))
        faces.append([x / nu for x in u])  # @line L5
        values.append(w[i])
    classes = {}
    for img, lab in zip(images, labels):
        classes.setdefault(lab, []).append(project_on(faces, mean, img))
    centers = {lab: [sum(c) / len(ws) for c in zip(*ws)] for lab, ws in classes.items()}  # @line L6
    return {"mean": mean, "faces": faces, "values": values, "centers": centers}  # @line L7


def project_on(faces, mean, img):
    """The weights omega_l = u_l^T (img - mean)."""
    d = [x - y for x, y in zip(img, mean)]
    return [sum(a * b for a, b in zip(u, d)) for u in faces]


def project(model, img):
    return project_on(model["faces"], model["mean"], img)


def reconstruct(model, weights):
    """mean + sum of weights[l] * u_l."""
    out = list(model["mean"])
    for wl, u in zip(weights, model["faces"]):
        for j in range(len(out)):
            out[j] += wl * u[j]
    return out


def distance_from_face_space(model, img):
    """|| (img - mean) - its projection on the eigenfaces ||."""
    rec = reconstruct(model, project(model, img))
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(img, rec)))


def recognize(model, img, theta_face=math.inf, theta_class=math.inf):
    """Return (label, distance). label is "not a face" if the image is far
    from face space and None if it is far from every class."""
    omega = project(model, img)  # @line L8
    eps_face = distance_from_face_space(model, img)  # @line L9
    if eps_face > theta_face:  # @line L10
        return "not a face", eps_face
    best, dist = None, math.inf
    for lab, c in model["centers"].items():  # @line L11
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(omega, c)))
        if d < dist:
            best, dist = lab, d
    if dist > theta_class:  # @line L12
        return None, dist
    return best, dist  # @line L13


def covariance_eigen(images):
    """Eigenvalues (descending) and eigenvectors of the P x P matrix A A^T, the
    direct way, for tests on tiny images."""
    m = len(images)
    p = len(images[0])
    mean = [sum(img[j] for img in images) / m for j in range(p)]
    phi = [[img[j] - mean[j] for j in range(p)] for img in images]
    big = [[sum(f[a] * f[b] for f in phi) for b in range(p)] for a in range(p)]
    w, v = sym_eig(big)
    order = sorted(range(p), key=lambda i: -w[i])
    return [w[i] for i in order], [[v[r][i] for r in range(p)] for i in order]
