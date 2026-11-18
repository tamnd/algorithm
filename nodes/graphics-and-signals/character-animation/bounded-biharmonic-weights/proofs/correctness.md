---
title: Each bounded biharmonic weight is the unique minimizer of a strictly convex box QP, and the active set method finds it
proves: [correctness]
status: full
---

We use the notation of the page.
$L$ is the symmetric stiffness matrix with zero row sums of a connected mesh, $M$ is diagonal with positive entries, and $Q = L M^{-1} L$.
For one handle, $D$ is the set of handle vertices with the fixed values $x_D$, and $F$ is the set of the other vertices.
The arithmetic is exact.

## The problem is strictly convex

**Lemma 1.** $x^\top L x \ge 0$, with equality exactly for constant $x$.

*Proof.*
$L$ is the stiffness matrix of piecewise linear finite elements, so $x^\top L x = \int_\Omega \lVert \nabla x_h \rVert^2$ for the piecewise linear function $x_h$ with the values $x$ at the vertices.
This is at least 0, and it is 0 exactly when $\nabla x_h = 0$ on every triangle, that is, when $x_h$ is constant on every triangle.
Neighboring triangles share vertices, so on a connected mesh $x$ is constant. $\square$

This holds on every mesh, also with obtuse angles, where some cotangent weights are negative.

**Lemma 2.** $Q$ is positive semidefinite, its null space is the constant vectors, and if $D \ne \emptyset$, the block $Q_{FF}$ is positive definite.

*Proof.*
$x^\top Q x = (L x)^\top M^{-1} (L x) \ge 0$, with equality if and only if $L x = 0$.
$L x = 0$ implies $x^\top L x = 0$, so $x$ is constant by Lemma 1, and constants satisfy $L x = 0$.
For $y \in \mathbb{R}^F$, let $x$ be $y$ on $F$ and 0 on $D$.
Then $y^\top Q_{FF} y = x^\top Q x$, which is zero only if $x$ is constant, and $x = 0$ on $D \ne \emptyset$, so $y = 0$. $\square$

**Theorem 1.** The problem of line L4, $\min \frac12 x^\top Q x$ subject to $x_D$ fixed and $0 \le x_F \le 1$, has exactly one minimizer, and a feasible $x$ is the minimizer if and only if, with $g = Q x$, for every $i \in F$: $g_i = 0$ if $0 < x_i < 1$, $g_i \ge 0$ if $x_i = 0$, and $g_i \le 0$ if $x_i = 1$.

*Proof.*
In the variables $x_F$, the objective is $\frac12 x_F^\top Q_{FF} x_F + x_F^\top Q_{FD} x_D + \text{const}$, which is strictly convex by Lemma 2, and the feasible set is a nonempty compact box.
So a minimizer exists and is unique.
The gradient in $x_F$ is $(Q x)_F = g_F$, and the conditions above are the KKT conditions of a box, with the multiplier $g_i$ of a lower bound and $-g_i$ of an upper bound.
For a convex problem with linear constraints, they are necessary and sufficient. $\square$

## The active set method

Let $W \subseteq F$ be the working set, with each $i \in W$ held at a bound $b_i \in \{0, 1\}$.
One iteration computes the minimizer $\hat x$ of the objective with $x_D$ fixed and $x_W = b_W$, over the free variables $F \setminus W$ with no bounds; it exists and is unique by Lemma 2.

**Lemma 3.** Every iterate is feasible, and the objective never increases.

*Proof.*
The first iterate is $x_F = 0$, which is feasible.
The step $p = \hat x - x$ is taken with the length $\alpha \in [0, 1]$, the largest that keeps every free variable in $[0, 1]$, so the new point is feasible.
The objective along the segment from $x$ to $\hat x$ is a convex quadratic with its minimum at $\hat x$, so it does not increase on $[0, 1]$. $\square$

**Theorem 2.** If the method stops, it returns the minimizer of Theorem 1.

*Proof.*
It stops only when $p = 0$, that is, $x = \hat x$, and every multiplier of $W$ is nonnegative.
$x = \hat x$ means $g_i = 0$ for every $i \in F \setminus W$.
The multipliers are $g_i$ for $i$ at the lower bound and $-g_i$ at the upper bound, so the KKT conditions of Theorem 1 hold for $i \in W$.
For $i \in F \setminus W$ with $x_i$ at a bound, $g_i = 0$ satisfies the condition too. $\square$

**Theorem 3.** If no step has the length $\alpha = 0$, the method stops after a finite number of iterations.

*Proof.*
After a release, the point $x$ minimizes the objective on the old working set, and the released variable $r$ has a negative multiplier, so moving $x_r$ into the box decreases the objective to first order, and $\hat x$ on the new working set has a strictly smaller objective than $x$.
With $\alpha > 0$, the new point has a strictly smaller objective.
Between two releases, each blocked step adds one variable to $W$, so there are at most $|F|$ steps before $p = 0$.
When $p = 0$ for a working set $W$, the point is the minimizer of the objective on $W$, and its value is a function of $W$.
These values strictly decrease from one release to the next, so no working set repeats at a release, and there are finitely many working sets. $\square$

Steps of the length zero can happen at degenerate points, where a variable is at a bound but not in $W$.
The tests compare the result with a brute force search on small problems and check the KKT conditions on a larger one.

## The brute force reference

For every assignment of each $i \in F$ to $\{0, 1, \text{free}\}$, the reference solves the equality problem and keeps the feasible result of the smallest objective.
The minimizer of Theorem 1 has some assignment: its variables at a bound and the others free.
On that face, it minimizes the objective over the open set of its free variables inside the box, so it is the unconstrained minimizer of the face, which the reference computes.
So the reference returns the minimizer.

## The normalization

Line L4 gives $w_k(v_i) \in [0, 1]$ and $w_k = \delta_{jk}$ at handle $j$.
At a handle vertex $h_j$, $\sum_k w_k(h_j) = 1$, so line L5 changes nothing there, and the interpolation holds.
At any other vertex, the sum $s_i$ is positive whenever some weight is positive, and then $w_k(v_i) / s_i \in [0, 1]$ and the new sum is 1.
If all weights at a vertex are 0, the division is not defined; this does not happen on a connected mesh in the tests, and the code would raise an error.
