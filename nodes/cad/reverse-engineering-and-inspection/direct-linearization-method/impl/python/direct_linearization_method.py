# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-linearization-method/. The authors are listed in prov/3NRTQF.jsonl.

"""Direct linearization method (DLM) for 2D vector loops.

An assembly is a list of closed vector loops in the plane. Each vector is a
triple (sign, length, angle):

- sign is +1 or -1;
- length is a number or the name of a variable;
- angle is a pair (const, coefs): the absolute angle in radians is
  const + sum(coef * value[name] for name, coef in coefs.items()).

The variables are split into manufactured ones x (part dimensions with
tolerances) and kinematic ones u (the adjustments of the assembly, such as a
gap, a contact position or a joint angle). Loop closure is h(x, u) = 0, two
equations per loop. DLM solves the loops at the nominal x, forms the partial
derivatives A = dh/dx and B = dh/du, and takes the sensitivities of a
kinematic output u_k as the k-th row of -B^-1 A. The worst-case and RSS
variations then follow from the stack-up formulas.
"""

import math


def vector_angle(angle, values):
    """Absolute angle of a vector from its (const, coefs) description."""
    const, coefs = angle
    return const + sum(c * values[name] for name, c in coefs.items())


def vector_length(length, values):
    return values[length] if isinstance(length, str) else float(length)


def loop_residual(loops, values):
    """h(x, u): the x and y sums of each loop, 2 numbers per loop."""
    out = []
    for loop in loops:
        sx = sy = 0.0
        for sign, length, angle in loop:
            L = vector_length(length, values)
            th = vector_angle(angle, values)
            sx += sign * L * math.cos(th)
            sy += sign * L * math.sin(th)
        out += [sx, sy]
    return out


def loop_jacobian(loops, values, names):
    """Partial derivatives of h with respect to the variables in names.

    d/d(length L) of sign * L * (cos t, sin t) is sign * (cos t, sin t), and
    d/d(angle variable with coefficient c) is sign * L * c * (-sin t, cos t).
    """
    col = {n: j for j, n in enumerate(names)}
    rows = [[0.0] * len(names) for _ in range(2 * len(loops))]
    for i, loop in enumerate(loops):
        for sign, length, angle in loop:
            L = vector_length(length, values)
            th = vector_angle(angle, values)
            ct, st = math.cos(th), math.sin(th)
            if isinstance(length, str) and length in col:
                j = col[length]
                rows[2 * i][j] += sign * ct
                rows[2 * i + 1][j] += sign * st
            for name, c in angle[1].items():
                if name in col:
                    j = col[name]
                    rows[2 * i][j] += -sign * L * c * st
                    rows[2 * i + 1][j] += sign * L * c * ct
    return rows


def solve_linear(M, rhs):
    """Solve M y = rhs by Gaussian elimination with partial pivoting.

    Raises ValueError if M is singular to working precision.
    """
    n = len(M)
    if any(len(r) != n for r in M) or len(rhs) != n:
        raise ValueError("the system is not square")
    a = [list(map(float, r)) + [float(b)] for r, b in zip(M, rhs)]
    scale = max((abs(v) for r in M for v in r), default=0.0) or 1.0
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if abs(a[p][k]) <= 1e-12 * scale:
            raise ValueError("B is singular: the loops do not fix the kinematic variables")
        a[k], a[p] = a[p], a[k]
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            if f:
                for j in range(k, n + 1):
                    a[i][j] -= f * a[k][j]
    y = [0.0] * n
    for k in range(n - 1, -1, -1):
        s = a[k][n] - sum(a[k][j] * y[j] for j in range(k + 1, n))
        y[k] = s / a[k][k]
    return y


def solve_assembly(loops, x, u_guess, kin_names, tol=1e-13, max_iter=60):
    """Newton's method for h(x, u) = 0 in the kinematic variables u.

    x and u_guess are dicts. Returns the dict of all values at the solution.
    Raises ValueError if Newton does not converge.
    """
    values = dict(x)
    values.update(u_guess)
    for _ in range(max_iter):  # @line L9
        r = loop_residual(loops, values)  # @line L10
        B = loop_jacobian(loops, values, kin_names)
        step = solve_linear(B, [-v for v in r])  # @line L11
        for name, d in zip(kin_names, step):
            values[name] += d
        if max(abs(d) for d in step) <= tol * (1.0 + max(abs(values[n]) for n in kin_names)):  # @line L12
            if max(abs(v) for v in loop_residual(loops, values)) <= 1e-9:
                return values  # @line L13
    raise ValueError("Newton's method did not converge")


def dlm(loops, x0, u_guess, man_names, kin_names, tolerances, output):
    """Direct linearization of a kinematic output.

    loops: the vector loops; x0: nominal manufactured values (dict);
    u_guess: a starting guess for the kinematic values (dict);
    man_names, kin_names: the variable names in order;
    tolerances: dict name -> symmetric tolerance T_j;
    output: the name of the kinematic variable that is the assembly output.

    Returns a dict with the nominal output, the sensitivities, the worst-case
    half-width sum |S_j| T_j and the RSS half-width sqrt(sum S_j^2 T_j^2).
    """
    if 2 * len(loops) != len(kin_names):
        raise ValueError("need exactly two kinematic variables per loop")
    values = solve_assembly(loops, x0, u_guess, kin_names)  # @line L1
    A = loop_jacobian(loops, values, man_names)  # @line L2
    B = loop_jacobian(loops, values, kin_names)
    k = kin_names.index(output)
    sens = {}
    for j, name in enumerate(man_names):  # @line L3
        col = solve_linear(B, [-A[i][j] for i in range(len(A))])  # @line L4
        sens[name] = col[k]  # @line L5
    worst = sum(abs(sens[n]) * tolerances[n] for n in man_names)  # @line L6
    rss = math.sqrt(sum((sens[n] * tolerances[n]) ** 2 for n in man_names))  # @line L7
    return {"nominal": values[output], "values": values, "sens": sens, "worst": worst, "rss": rss}  # @line L8


# Example assemblies used on the page and in the tests.

def clutch_loops():
    """One-way clutch: hub flat at distance a, roller radius c, ring radius e.

    Kinematic variables: b (contact point along the flat) and phi (the
    pressure angle between the two contact normals). The loop goes from the
    ring centre along the flat (b), up to the flat (a), up to the roller
    centre (c), and back to the ring centre along the line of radius e - c,
    whose angle is 90 degrees minus phi.
    """
    half_pi = math.pi / 2
    back = (half_pi, {"phi": -1.0})
    return [[
        (1, "b", (0.0, {})),
        (1, "a", (half_pi, {})),
        (1, "c", (half_pi, {})),
        (1, "c", back),
        (-1, "e", back),
    ]]


def fourbar_loops():
    """Four-bar linkage with fixed input angle th2 (a constant of the model).

    Manufactured: crank a, coupler b, rocker c, ground d.
    Kinematic: coupler angle th3 and rocker angle th4.
    """
    return [[
        (1, "a", (0.0, {"th2": 1.0})),
        (1, "b", (0.0, {"th3": 1.0})),
        (-1, "c", (0.0, {"th4": 1.0})),
        (-1, "d", (0.0, {})),
    ]]


def linear_stack_loops():
    """End gap of a 1D stack: G = A - B - C - D, written as a vector loop.

    The vertical vectors (kinematic h, constant 1) only make B square.
    """
    return [[
        (1, "A", (0.0, {})),
        (-1, "B", (0.0, {})),
        (-1, "C", (0.0, {})),
        (-1, "D", (0.0, {})),
        (-1, "G", (0.0, {})),
        (1, "h", (math.pi / 2, {})),
        (-1, 1.0, (math.pi / 2, {})),
    ]]
