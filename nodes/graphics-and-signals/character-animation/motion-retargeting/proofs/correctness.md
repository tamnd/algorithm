---
title: Each retargeting step is the smallest change that meets the linearized constraints, and a fixed point is a first order optimum
proves: [correctness]
status: full
---

We use the notation of the page.
$c \in \mathbb{R}^s$ holds the control points, $W$ is diagonal with positive entries, and $G(c) = p$ collects the $m$ constraint rows $g_f(q(t_f) + d(t_f)) = p_f$.
$J(c)$ is the $m \times s$ Jacobian of $G$, and $r(c) = G(c) - p$.
The displacement is linear in $c$, so $G$ is a smooth function of $c$ whenever the forward kinematics is smooth.
The arithmetic is exact.

## One step

**Lemma 1.** If $J$ has full row rank, then $J W^{-1} J^\top$ is symmetric positive definite.

*Proof.*
For $y \ne 0$, $y^\top J W^{-1} J^\top y = \lVert W^{-1/2} J^\top y \rVert^2$, and $J^\top y \ne 0$ because the rows of $J$ are independent. $\square$

**Theorem 1.** Let $b = J c_k - r(c_k)$, the right side of line L4.
Line L6 gives the unique minimizer of $c^\top W c$ subject to $J c = b$.

*Proof.*
The problem is a strictly convex quadratic with linear equality constraints, so a point is the unique minimizer if and only if it is feasible and satisfies the Lagrange condition $2 W c = J^\top \lambda$ for some $\lambda$.
The point $c = W^{-1} J^\top \mu$ of line L6 satisfies the Lagrange condition with $\lambda = 2\mu$.
It is feasible because $J c = J W^{-1} J^\top \mu = b$ by line L5, which has exactly one solution by Lemma 1. $\square$

The constraint $J c = b$ is $r(c_k) + J (c - c_k) = 0$, the linearization of $r(c) = 0$ at $c_k$.
So each step is a step of sequential quadratic programming for $\min c^\top W c$ subject to $r(c) = 0$, with the Hessian $2W$ of the objective and without the curvature of the constraints.

## Fixed points

**Theorem 2.** If $c_{k+1} = c_k = c$ and $r(c) = 0$, then $c$ is a first order point of the constrained problem: $r(c) = 0$ and $2 W c = J(c)^\top \lambda$ for some $\lambda$.

*Proof.*
By line L6, $c = W^{-1} J^\top \mu$, so $2 W c = J^\top (2\mu)$. $\square$

The test checks this condition by projecting $c$ onto the null space of $J$, with $W = I$.
Theorem 2 gives a necessary condition only.
The tests add a second check: from random feasible neighbors, the value of $c^\top c$ is not smaller.

## The same character

**Theorem 3.** If the source motion meets the constraints of the new character, the first step gives $c = 0$, and the method returns the source motion.

*Proof.*
At $c_0 = 0$, $r = 0$, so $b = J \cdot 0 - 0 = 0$, and line L5 gives $\mu = 0$, so $c_1 = 0$.
Then $c_1 = c_0$ and $r = 0$, so line L7 stops, and line L8 returns $q(t) + 0$. $\square$

## Frames far from the constraints

**Theorem 4.** If a control point $c_{kj}$ has $B(t_f / \delta - j + 1) = 0$ for every constrained frame $t_f$, then line L6 gives $c_{kj} = 0$.
A frame $t$ at which every control point with $B(t / \delta - j + 1) \ne 0$ has this property keeps its source pose.

*Proof.*
The entries of $J$ in the column of $c_{kj}$ are $\partial g_f / \partial q_k \cdot B(t_f / \delta - j + 1) = 0$, so the column is zero, and the entry $kj$ of $W^{-1} J^\top \mu$ is zero.
At such a frame, $d_k(t) = \sum_j c_{kj} B(t / \delta - j + 1)$ has only zero terms. $\square$

## The check value

With one constraint at a knot, only on the root height, and the other degrees of freedom made very costly, $J$ has the single row $(\ldots, 0, \frac16, \frac46, \frac16, 0, \ldots)$ in the root height control points, and the constraint is linear.
By Theorem 1, $c = J^\top \mu$ with $\mu \lVert J \rVert^2 = -0.2$, and $\lVert J \rVert^2 = 1/36 + 16/36 + 1/36 = 1/2$.
So $\mu = -0.4$ and $c = (-0.4/6, -1.6/6, -0.4/6) = (-0.0667, -0.2667, -0.0667)$.
