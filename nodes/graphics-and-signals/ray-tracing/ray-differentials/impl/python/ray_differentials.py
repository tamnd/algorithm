# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-differentials/. The authors are listed in prov/TZFVTD.jsonl.
"""Ray differentials (Igehy 1999).

A ray is a point P and a unit direction D. Its differential with respect to an image coordinate
x is the pair (dP, dD) of derivatives of P and D with respect to x. The functions below start
the differentials at a pinhole camera and carry them through transfer to a surface, reflection
and refraction. The differential of the hit point gives the footprint of a pixel on a surface,
which selects a texture filter such as a mipmap level.
"""

import math


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def camera_ray(cam, x, y):
    """Ray through image point (x, y) and its differentials in x and in y.

    cam = (eye, view, right, up): the unnormalized direction is view + x right + y up, where x
    and y are in pixels from the image center, so right and up are the pixel steps.
    """
    eye, view, right, up = cam
    d = add(view, add(scale(x, right), scale(y, up)))
    dd = dot(d, d)
    s = dd ** 1.5
    big_d = scale(1 / math.sqrt(dd), d)
    diffs = []
    for e in (right, up):
        d_dir = scale(1 / s, sub(scale(dd, e), scale(dot(d, e), d)))  # @line L1
        diffs.append(((0.0, 0.0, 0.0), d_dir))
    return (eye, big_d), diffs


def transfer(ray, diff, t, n):
    """Move the ray to its hit P + t D on a surface with unit normal n; differential of the hit."""
    p, d = ray
    dp, dd = diff
    q = add(dp, scale(t, dd))
    dt = -dot(q, n) / dot(d, n)  # @line L3
    return add(q, scale(dt, d)), dd  # @line L4


def reflect(d, n, dd, dn):
    """Mirror direction and its derivative, for unit n."""
    dn_dot = dot(d, n)
    r = sub(d, scale(2 * dn_dot, n))
    d_dn = dot(dd, n) + dot(d, dn)
    dr = sub(dd, scale(2, add(scale(dn_dot, dn), scale(d_dn, n))))  # @line L6
    return r, dr


def refract(d, n, dd, dn, eta):
    """Refracted direction T = eta D - mu N and its derivative, for unit D and N with D.N < 0.

    eta is the ratio of the index of the incident side to the index of the other side. Returns
    None on total internal reflection.
    """
    c = dot(d, n)
    k = 1 - eta * eta * (1 - c * c)
    if k < 0:
        return None
    ct = -math.sqrt(k)  # T . N
    mu = eta * c - ct
    t_dir = sub(scale(eta, d), scale(mu, n))
    dc = dot(dd, n) + dot(d, dn)
    dmu = (eta - eta * eta * c / ct) * dc
    dt_dir = sub(scale(eta, dd), add(scale(mu, dn), scale(dmu, n)))  # @line L7
    return t_dir, dt_dir


def hit_sphere(ray, center, radius):
    """Smallest t > 1e-9 where the ray meets the sphere, or None."""
    p, d = ray
    oc = sub(p, center)
    b = dot(oc, d)
    c = dot(oc, oc) - radius * radius
    disc = b * b - c
    if disc < 0:
        return None
    r = math.sqrt(disc)
    for t in (-b - r, -b + r):
        if t > 1e-9:
            return t
    return None


def hit_plane(ray, n, h):
    """t where the ray meets the plane n . x = h, or None."""
    p, d = ray
    den = dot(n, d)
    if den == 0:
        return None
    t = (h - dot(n, p)) / den
    return t if t > 1e-9 else None


def trace(cam, x, y, surfaces):
    """Follow the camera ray through a list of surfaces; return the last hit and its differentials.

    Each surface is ("sphere", center, radius, action) or ("plane", n, h, action), where action is
    "reflect", ("refract", eta) or "stop". Returns (P, D, [dP/dx, dP/dy], [dD/dx, dD/dy]).
    """
    ray, diffs = camera_ray(cam, x, y)
    for kind, a, b, action in surfaces:
        p, d = ray
        if kind == "sphere":
            t = hit_sphere(ray, a, b)  # @line L2
            q = add(p, scale(t, d))
            n = scale(1 / b, sub(q, a))
        else:
            t = hit_plane(ray, a, b)
            q = add(p, scale(t, d))
            n = a
        new = [transfer(ray, df, t, n) for df in diffs]
        dps = [dp for dp, _ in new]
        dns = [scale(1 / b, dp) if kind == "sphere" else (0.0, 0.0, 0.0) for dp in dps]  # @line L5
        if action == "stop":
            return q, d, dps, [dd for _, dd in new]
        if action == "reflect":
            outs = [reflect(d, n, dd, dn) for (_, dd), dn in zip(new, dns)]
        else:
            if dot(d, n) > 0:  # leaving the object: flip the normal, invert the ratio
                n, dns, eta = scale(-1, n), [scale(-1, dn) for dn in dns], 1 / action[1]
            else:
                eta = action[1]
            outs = [refract(d, n, dd, dn, eta) for (_, dd), dn in zip(new, dns)]
        ray = (q, outs[0][0])
        diffs = [(dp, out[1]) for dp, out in zip(dps, outs)]
    return ray[0], ray[1], [dp for dp, _ in diffs], [dd for _, dd in diffs]


def mip_level(du_dx, du_dy, texels):
    """Isotropic mipmap level from the footprint vectors in texture space (units of the texture).

    The footprint side is the longer of the two vectors, measured in texels.
    """
    rho = max(norm(du_dx), norm(du_dy)) * texels  # @line L8
    return max(0.0, math.log2(rho)) if rho > 0 else 0.0
