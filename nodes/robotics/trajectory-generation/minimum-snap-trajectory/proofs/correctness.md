---
title: The KKT system of minimum snap is nonsingular, its solution is the unique minimizer, and the optimum is C6 at inner waypoints
proves: [correctness]
status: full
---

We use the notation of the page. There are $m \ge 1$ segments with durations $T_1, \dots, T_m > 0$ and waypoints $w_0, \dots, w_m$ of one coordinate. Segment $i$ is a polynomial $p_i$ of degree at most 7 in local time $t \in [0, T_i]$, with coefficient vector $c_i \in \mathbb R^8$, and $c = (c_1, \dots, c_m) \in \mathbb R^{8m}$. The cost is

$$f(c) = \sum_{i=1}^m \int_0^{T_i} p_i^{(4)}(t)^2\, dt = c^{\mathsf T} Q c,$$

with $Q$ block diagonal (lines L1 and L2). Lines L3 to L5 collect the linear constraints $Ac = b$: $p_i(0) = w_{i-1}$ and $p_i(T_i) = w_i$; $p_1^{(k)}(0) = 0$ and $p_m^{(k)}(T_m) = 0$ for $k = 1, 2, 3$; and $p_i^{(k)}(T_i) = p_{i+1}^{(k)}(0)$ for $i < m$ and $k = 1, 2, 3$. That is $2m + 6 + 3(m - 1) = 5m + 3$ rows. The proof is in exact arithmetic.

## Hermite data

**Lemma 1.** For $T > 0$, the map from the 8 coefficients of a polynomial of degree at most 7 to the values $(p, p', p'', p''')$ at $0$ and at $T$ is a bijection.

*Proof.* It is a linear map between spaces of dimension 8. If all 8 values are zero, then $0$ and $T$ are roots of multiplicity at least 4, so $t^4 (t - T)^4$, of degree 8, divides $p$, and $p = 0$. So the map is injective, hence bijective. $\square$

So a piecewise polynomial that meets all the constraints is the same thing as a choice of knot data $(p, p', p'', p''')$ at each waypoint with the positions and the end derivatives fixed: build each segment from the data at its two ends by Lemma 1. The free values are the derivatives $1, 2, 3$ at the $m - 1$ inner waypoints. Function `_hermite_inverse` computes the inverse map of Lemma 1, and `min_snap_free_derivatives` uses this parameterization.

## The KKT system is nonsingular

**Lemma 2.** $A$ has full row rank.

*Proof.* Let $b$ be any right-hand side. Choose knot data as follows: positions and end derivatives as $b$ prescribes, any values for the derivatives at the right end of segment $i < m$, and the left end values of segment $i + 1$ equal to those minus the prescribed difference. Lemma 1 builds segments with this data, and they satisfy $Ac = b$. So $A$ maps onto $\mathbb R^{5m+3}$. $\square$

**Lemma 3.** If $Ac = 0$ and $c^{\mathsf T} Q c = 0$, then $c = 0$.

*Proof.* $c^{\mathsf T} Q c = 0$ means $p_i^{(4)} = 0$ on each segment, so each $p_i$ is a cubic. A cubic is fixed by $(p, p', p'', p''')$ at its left end. $Ac = 0$ gives $p_1(0) = 0$ and $p_1'(0) = p_1''(0) = p_1'''(0) = 0$, so $p_1 = 0$. If $p_i = 0$, then $p_{i+1}(0) = 0$ by the position row and $p_{i+1}^{(k)}(0) = p_i^{(k)}(T_i) = 0$ for $k = 1, 2, 3$ by the continuity rows, so $p_{i+1} = 0$. $\square$

**Theorem 1.** The matrix $K = \begin{pmatrix} 2Q & A^{\mathsf T} \\ A & 0 \end{pmatrix}$ of line L6 is nonsingular. Its solution $(c^*, \lambda)$ gives the unique minimizer $c^*$ of $f$ subject to $Ac = b$.

*Proof.* Suppose $K (x, y) = 0$, so $2Qx + A^{\mathsf T} y = 0$ and $Ax = 0$. Then $2x^{\mathsf T} Q x = -x^{\mathsf T} A^{\mathsf T} y = -(Ax)^{\mathsf T} y = 0$. $Q$ is positive semidefinite (it is a sum of integrals of squares), so $x^{\mathsf T} Q x = 0$, and Lemma 3 gives $x = 0$. Then $A^{\mathsf T} y = 0$, and Lemma 2 gives $y = 0$. So $K$ is nonsingular.

Let $c$ be feasible and $d = c - c^*$, so $Ad = 0$. Then

$$f(c) = f(c^*) + 2 d^{\mathsf T} Q c^* + d^{\mathsf T} Q d = f(c^*) - d^{\mathsf T} A^{\mathsf T} \lambda + d^{\mathsf T} Q d = f(c^*) + d^{\mathsf T} Q d,$$

because $2Qc^* = -A^{\mathsf T}\lambda$ and $Ad = 0$. So $f(c) \ge f(c^*)$, and by Lemma 3 equality holds only for $d = 0$. $\square$

## The free-derivative method gives the same answer

`min_snap_free_derivatives` writes $f$ as a quadratic form in the knot data, fixes the known values, and solves the linear system that sets the gradient with respect to the free values to zero. By Lemma 1 the knot data parameterize exactly the feasible set, so this minimizes the same strictly convex function (Theorem 1) over the same set. The reduced matrix is positive definite by Lemma 3, so its system has one solution, and it is $c^*$. The tests check that both methods return the same exact coefficients.

## The optimum is smooth up to order 6

**Theorem 2.** At every inner waypoint, the derivatives of order 4, 5 and 6 of the optimum are continuous. Moreover the optimum minimizes the cost over all functions that are piecewise of class $H^4$ on the segments and meet the constraints, not only over polynomials of degree 7.

*Proof.* Let $\eta$ be a variation: on each segment a function with square-integrable fourth derivative, zero at every waypoint, with $\eta', \eta'', \eta'''$ zero at both outer ends and continuous at inner waypoints. Write $x^*$ for the optimum and $\Delta_r(k)$ for the jump $x^{*(r)}(t_k^+) - x^{*(r)}(t_k^-)$ at inner waypoint $k$. Integrating by parts four times on each segment and using $x^{*(8)} = 0$ and $\eta = 0$ at the waypoints,

$$\sum_i \int_0^{T_i} x^{*(4)} \eta^{(4)} = \sum_{k=1}^{m-1} \big( -\Delta_4(k)\, \eta'''(t_k) + \Delta_5(k)\, \eta''(t_k) - \Delta_6(k)\, \eta'(t_k) \big).$$

The outer end terms vanish because $\eta', \eta'', \eta'''$ are zero there. Take $\eta$ to be a piecewise polynomial of degree 7 built by Lemma 1 from any values of $\eta', \eta'', \eta'''$ at the inner waypoints. It is a feasible direction, so by Theorem 1 $f(c^* + \varepsilon \eta)$ has its minimum at $\varepsilon = 0$, and the left side is zero. Since the values at the waypoints are arbitrary, every jump $\Delta_4, \Delta_5, \Delta_6$ is zero. Then the left side is zero for every variation $\eta$, so the cost of $x^* + \eta$ is the cost of $x^*$ plus the cost of $\eta$, as in Theorem 1. $\square$

The seventh derivative is not continuous in general; the tests show a jump. The code uses a local time per segment, which shifts the variable but does not change the derivatives at the waypoints.
