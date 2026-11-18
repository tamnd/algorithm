---
title: Each step of the skinning decomposition is an exact minimization, and the error does not increase
proves: [correctness]
status: full
---

We use the notation of the page.
For one vertex $i$, let $a_b \in \mathbb{R}^{dF}$ be the stacked positions $R_{f,b} v_i + T_{f,b}$ over the frames, and $y \in \mathbb{R}^{dF}$ the stacked targets $q_{f,i}$, with $d = 2$ in the code.
The error of vertex $i$ is $e(w) = \lVert A w - y \rVert^2$ with $A = (a_1, \ldots, a_B)$, and $E = \sum_i e_i$.
The arithmetic is exact.

## The weight step

Let $\Delta_S = \{ w : w \ge 0, \sum_b w_b = 1, w_b = 0 \text{ for } b \notin S \}$ for a set $S$ of bones.

**Lemma 1.** For a support $T \subseteq S$, if the matrix
$$M_T = \begin{pmatrix} 2 A_T^\top A_T & \mathbf{1} \\ \mathbf{1}^\top & 0 \end{pmatrix}$$
is invertible, its solution $(u, \lambda)$ of $M_T (u, \lambda) = (2 A_T^\top y, 1)$ gives the unique minimizer $u$ of $e$ over the affine set $\{ w : \sum_b w_b = 1, w_b = 0 \text{ for } b \notin T \}$, when $A_T$ has full column rank.

*Proof.*
On this set, $e$ is a convex quadratic in $u$, and the Lagrange conditions of $\min \lVert A_T u - y \rVert^2$ subject to $\mathbf{1}^\top u = 1$ are $2 A_T^\top (A_T u - y) + \lambda \mathbf{1} = 0$ and $\mathbf{1}^\top u = 1$, which is the system above up to the sign of $\lambda$.
For a convex problem with linear constraints, these conditions are sufficient, and the minimizer is unique when $A_T^\top A_T$ is positive definite. $\square$

**Theorem 1.** `simplex_lsq(A, y, S)` returns a minimizer of $e$ over $\Delta_S$, when every $A_T$ with $T \subseteq S$ has full column rank.

*Proof.*
$\Delta_S$ is compact and $e$ is continuous, so a minimizer $w^*$ exists.
Let $T$ be the support of $w^*$.
Then $w^*$ minimizes $e$ over the relative interior of $\Delta_T$, which is open in the affine set of Lemma 1, so it is a local and therefore a global minimizer of the convex $e$ over that affine set.
By Lemma 1, the code finds $w^*$ when it tries the support $T$, and $w^*$ is nonnegative, so it is a candidate.
Every other candidate is a point of $\Delta_S$, so its error is at least $e(w^*)$, and the code returns a point with the error $e(w^*)$. $\square$

If a matrix $M_T$ is singular, the code skips $T$.
The minimizer over $\Delta_S$ then still has a support with an invertible $M_T$ whenever $A_S$ has full column rank, because a subset of independent columns is independent.
For the tests, the columns are random or come from distinct rigid motions, and the rank condition holds.

**Corollary.** Line L3 gives the minimizer over all of the simplex, and line L4 gives the minimizer over $\Delta_S$ for the set $S$ of the $K$ largest entries, which has at most $K$ nonzero entries.
Line L5 then returns the weights $w^{\text{new}}_i$ with $e_i(w^{\text{new}}_i) \le e_i(w^{\text{old}}_i)$.
The old weights are feasible: they are one-hot after line L1, and every later value comes from line L4 or line L5.

## The bone step

**Theorem 2.** Fix all weights, all bones except $b$, and the frame $f$.
Let $u_i = w_{i,b}$, $\bar p = \sum_i u_i^2 v_i / \sum_i u_i^2$ and $\bar q = \sum_i u_i r_i / \sum_i u_i^2$, with $r_i$ from line L6, and assume $\sum_i u_i^2 > 0$.
Then $(R, T)$ of line L7 minimizes $G(R, T) = \sum_i \lVert r_i - u_i (R v_i + T) \rVert^2$ over all rotations $R$ and translations $T$.

*Proof.*
The error of frame $f$ is $\sum_i \lVert q_{f,i} - \sum_c w_{i,c} (R_{f,c} v_i + T_{f,c}) \rVert^2 = G(R_{f,b}, T_{f,b})$, by the definition of $r_i$.
For fixed $R$, $G$ is a convex quadratic in $T$ with the gradient $-2 \sum_i u_i (r_i - u_i R v_i - u_i T)$.
It is zero at $T = \bar q - R \bar p$, which is the minimizer in $T$.
With this $T$, $r_i - u_i (R v_i + T) = (r_i - u_i \bar q) - R\, u_i (v_i - \bar p)$.
Let $x_i = u_i (v_i - \bar p)$ and $z_i = r_i - u_i \bar q$.
Then $G = \sum_i \lVert z_i \rVert^2 + \sum_i \lVert x_i \rVert^2 - 2 \sum_i z_i^\top R x_i$, because $R$ keeps lengths.
So minimizing $G$ over $R$ is maximizing $\sum_i z_i^\top R x_i$.
In 2D, with $R$ the rotation by $\theta$, $\sum_i z_i^\top R x_i = \cos\theta \sum_i x_i \cdot z_i + \sin\theta \sum_i x_i \times z_i$, where $\times$ is the scalar cross product.
This is $\rho \cos(\theta - \varphi)$ with $\varphi = \operatorname{atan2}(\sum_i x_i \times z_i, \sum_i x_i \cdot z_i)$, which is largest at $\theta = \varphi$, the angle of line L7.
Every rotation has this form, so $(R, T)$ is the global minimizer. $\square$

In 3D, the same reduction gives the Kabsch problem $\max \operatorname{tr}(R^\top \sum_i z_i x_i^\top)$, which the SVD solves.
If $\sum_i u_i^2 = 0$, the bone has no influence, $G$ does not depend on $(R, T)$, and any value is a minimizer; the code returns the identity.

## The error does not increase

**Theorem 3.** The values `errors[k]` returned by `ssdr` are nonincreasing in $k$.

*Proof.*
One iteration first replaces the weights of every vertex.
$E$ is the sum of the $e_i$, and each $e_i$ depends only on the weights of vertex $i$ for fixed bones, so by the Corollary $E$ does not increase.
Then it replaces bone $b = 1, \ldots, B$ in turn.
For fixed weights and other bones, $E$ is the sum over the frames of the $G$ of Theorem 2, and the transforms of bone $b$ in different frames appear in different terms, so the new transforms minimize $E$ over bone $b$, and the old transforms are feasible.
So $E$ does not increase in any step. $\square$

$E \ge 0$, so the values converge.
The theorem does not say that the limit is a global minimum, or that the weights and bones converge.

## The ground truth is a fixed point

**Theorem 4.** If $q_{f,i} = \sum_b w^\circ_{i,b} (R^\circ_{f,b} v_i + T^\circ_{f,b})$ with $w^\circ_i \in \Delta$ and at most $K$ nonzero entries per vertex, then from $(w^\circ, R^\circ, T^\circ)$ one iteration keeps $E = 0$.

*Proof.*
$E \ge 0$ and $E = 0$ at the start, and by Theorem 3 $E$ does not increase. $\square$

## The check values

With $a_1 = (1, 0)$ and $a_2 = (0, 1)$, the set $\{ w_1 a_1 + w_2 a_2 : w \in \Delta \}$ is the segment from $(1, 0)$ to $(0, 1)$.
For $y = (0.5, 0.5)$, the point $w = (0.5, 0.5)$ gives $y$, so $e = 0$.
For $y = (1, 1)$, the support $\{1, 2\}$ gives $2 w_1 + \lambda = 2$, $2 w_2 + \lambda = 2$ and $w_1 + w_2 = 1$, so $w = (0.5, 0.5)$, and $e = 0.5^2 + 0.5^2 = 0.5$.
For $y = (2, 0)$, the support $\{1, 2\}$ gives $2 w_1 + \lambda = 4$, $2 w_2 + \lambda = 0$, so $w_1 - w_2 = 2$ and $w = (1.5, -0.5)$, which is not allowed.
The support $\{1\}$ gives $e = \lVert (1, 0) - (2, 0) \rVert^2 = 1$, and the support $\{2\}$ gives $e = 4 + 1 = 5$, so the result is $w = (1, 0)$ with $e = 1$.
