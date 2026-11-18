---
title: Direct manipulation of blendshapes returns the unique minimizer of the regularized energy, with and without bounds
proves: [correctness]
status: full
---

We use the notation of the page.
$S \in \mathbb{R}^{3m \times k}$, $\mathbf{m} \in \mathbb{R}^{3m}$, $w_0 \in \mathbb{R}^k$, $\alpha > 0$ or $\mu > 0$ with $\alpha, \mu \ge 0$, and

$$E(w) = \lVert S w - \mathbf{m} \rVert^2 + \alpha \lVert w - w_0 \rVert^2 + \mu \lVert w \rVert^2.$$

Let $A = S^T S + (\alpha + \mu) I$ and $c = S^T \mathbf{m} + \alpha w_0$, as in lines L2 and L3.
The arithmetic is exact.

## The energy

**Lemma 1.** $E(w) = w^T A w - 2 c^T w + \text{const}$, so $\nabla E(w) = 2(A w - c)$ and $\nabla^2 E = 2A$.

*Proof.*
Expand the three squares: $\lVert S w - \mathbf{m} \rVert^2 = w^T S^T S w - 2 \mathbf{m}^T S w + \mathbf{m}^T \mathbf{m}$, $\alpha \lVert w - w_0 \rVert^2 = \alpha w^T w - 2 \alpha w_0^T w + \alpha w_0^T w_0$, and $\mu \lVert w \rVert^2 = \mu w^T w$.
Collect the quadratic terms into $w^T A w$ and the linear terms into $-2 c^T w$. $\square$

**Lemma 2.** $A$ is symmetric positive definite, so $E$ is strictly convex.

*Proof.*
$S^T S$ is symmetric and $x^T S^T S x = \lVert S x \rVert^2 \ge 0$.
So $x^T A x \ge (\alpha + \mu) \lVert x \rVert^2 > 0$ for $x \ne 0$. $\square$

## The free problem

**Theorem 1.** Line L4 returns the unique minimizer of $E$ over $\mathbb{R}^k$.

*Proof.*
By Lemma 2, $A$ is invertible, so $A w = c$ has exactly one solution $w^\ast$.
For any $w$, Lemma 1 gives $E(w) - E(w^\ast) = (w - w^\ast)^T A (w - w^\ast)$, because $A w^\ast = c$.
This is positive for $w \ne w^\ast$ by Lemma 2. $\square$

## The bounded problem

Let $Q(w) = \tfrac12 w^T A w - c^T w$, which is $E / 2$ up to a constant, and let $\mathcal{B} = [0, t]^k$.

**Lemma 3 (KKT).** A point $w \in \mathcal{B}$ minimizes $Q$ over $\mathcal{B}$ if and only if, with $g = A w - c$, for every $j$: $g_j = 0$ if $0 < w_j < t$, $g_j \ge 0$ if $w_j = 0$, and $g_j \le 0$ if $w_j = t$.
There is exactly one such point.

*Proof.*
$Q$ is convex and $\mathcal{B}$ is convex, so $w$ is a minimizer if and only if $g^T (y - w) \ge 0$ for all $y \in \mathcal{B}$.
Because $\mathcal{B}$ is a product of intervals, this splits into $g_j (y_j - w_j) \ge 0$ for all $y_j \in [0, t]$ and each $j$, which is the stated sign condition.
$\mathcal{B}$ is compact, so a minimizer exists; it is unique because $Q$ is strictly convex. $\square$

**Lemma 4 (one step).** Fix all coordinates but $j$, and let $w_j$ be replaced by $w_j' = \operatorname{clamp}((c_j - \sum_{l \ne j} A_{jl} w_l) / A_{jj}, 0, t)$, as in line L7.
Then $w_j'$ minimizes $Q$ in the coordinate $j$ over $[0, t]$, and $Q(w) - Q(w') \ge \tfrac12 A_{jj} (w_j - w_j')^2$.

*Proof.*
As a function of $w_j$ alone, $Q = \tfrac12 A_{jj} w_j^2 - r w_j + \text{const}$ with $r = c_j - \sum_{l \ne j} A_{jl} w_l$ and $A_{jj} > 0$.
Its unconstrained minimum is at $r / A_{jj}$, and on an interval the minimum of a convex parabola is at the clamped point.
Let $h(x) = \tfrac12 A_{jj} x^2 - r x$ and $x' = w_j'$.
By the one-dimensional case of Lemma 3, $h'(x')(x - x') \ge 0$ for all $x \in [0, t]$.
Then $h(x) - h(x') = h'(x')(x - x') + \tfrac12 A_{jj} (x - x')^2 \ge \tfrac12 A_{jj} (x - x')^2$. Take $x = w_j$. $\square$

**Theorem 2.** The iterates of lines L5 to L8 stay in $\mathcal{B}$, $Q$ does not increase, and the iterates converge to the unique minimizer $w^\ast$ of $Q$ over $\mathcal{B}$.

*Proof.*
Line L5 and every step of line L7 clamp into $[0, t]$, so every iterate is in $\mathcal{B}$.
By Lemma 4, $Q$ does not increase at any step.
$Q$ is bounded below on the compact set $\mathcal{B}$, so the total decrease is finite.
By Lemma 4 the sum over all steps of $\tfrac12 A_{jj} \delta^2$ is finite, where $\delta$ is the change of the step, and $A_{jj} \ge \alpha + \mu > 0$.
So the changes tend to 0, and the change of a whole sweep tends to 0.

Let $\bar w$ be a limit point of the iterates at the ends of sweeps, which exists because $\mathcal{B}$ is compact.
The map that performs one step of line L7 is continuous in $w$.
Along the subsequence that tends to $\bar w$, the change of each step tends to 0, so by continuity each coordinate of $\bar w$ is a fixed point of its own step.
A fixed point of the step for $j$ meets the sign condition of Lemma 3 for $j$, by the one-dimensional case of that lemma.
So $\bar w$ meets all the conditions of Lemma 3, and $\bar w = w^\ast$.
Every limit point is $w^\ast$ and the iterates are in a compact set, so the whole sequence converges to $w^\ast$. $\square$

The stopping rule of line L8 ends the loop after finitely many sweeps, because the change of a sweep tends to 0.
At that point the iterate is close to $w^\ast$ but not equal to it in general; the test compares it with a brute force over all splits of the coordinates into free, at 0 and at $t$, with the tolerance $10^{-9}$.

## The check values

In the example of the page, $S = \begin{pmatrix} 1 & 1 \\ 0 & 1 \\ 0 & 0 \end{pmatrix}$, $\alpha = 0.1$, $\mu = 0$ and $w_0 = 0$.
For $\mathbf{m} = (1, 0.5, 0)$, $A = \begin{pmatrix} 1.1 & 1 \\ 1 & 2.1 \end{pmatrix}$ and $c = (1, 1.5)$.
By Cramer's rule, $w^\ast = (2.1 \cdot 1 - 1 \cdot 1.5,\; 1.1 \cdot 1.5 - 1 \cdot 1) / 1.31 = (0.6, 0.65) / 1.31$.
For $\mathbf{m} = (2, 1.5, 0)$, $c = (2, 3.5)$ and the free solution is $(0.7, 1.85) / 1.31$, with $w_2 > 1$.
The point $(1 / 1.1, 1)$ has $g_1 = 1.1 \cdot (1 / 1.1) + 1 - 2 = 0$ and $g_2 = 1 / 1.1 + 2.1 - 3.5 < 0$ with $w_2 = t = 1$, so by Lemma 3 it is the bounded minimizer.
