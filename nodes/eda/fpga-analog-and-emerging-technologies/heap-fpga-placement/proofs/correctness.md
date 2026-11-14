---
title: Every iterate of HeAP is a legal placement of each block type in its own columns, and the quadratic step finds the exact minimum of its model
proves: [correctness]
status: full
---

## Setting

The grid has columns $0, \ldots, n_x - 1$ and rows $0, \ldots, n_y - 1$. Column $x$ has a type $\tau(x)$, and $S_t$ is the set of sites $(x, y)$ with $\tau(x) = t$. Block $i$ has the type $\mathrm{type}(i)$, and $n_t$ is the number of blocks of type $t$. A placement is **legal** when it maps the blocks injectively to sites and puts every block on a site of its own type. The algorithm is the one of the [node page](../node.md), as written in the implementation; it rejects the input when $n_t > |S_t|$ for some $t$, so below $n_t \le |S_t|$ for all $t$.

## The quadratic step

Fix one coordinate, say $x$. For a net with $p \ge 2$ terminals, every pair of terminals gets the weight $w = 1 / (p - 1)$ (the [clique net model](/clique-net-model/)). The model of the quadratic step is

$$\Phi(x) = \sum_{\text{pairs } \{i, j\} \text{ of blocks}} w_{ij} (x_i - x_j)^2 + \sum_{\text{pairs } \{i, q\},\ q \text{ a pad}} w_{iq} (x_i - X_q)^2 + \beta \sum_i (x_i - a_i)^2 + \varepsilon \sum_i (x_i - c)^2,$$

where $X_q$ is the fixed position of pad $q$, $a_i$ is the anchor of block $i$ (the term is absent in the first solve, $\beta = 0$), $c$ is the center of the grid and $\varepsilon > 0$ is a small constant ($10^{-3}$ in the implementation).

**Lemma 1.** $\Phi(x) = x^\top A x - 2 b^\top x + \mathrm{const}$, where $A$ and $b$ are the matrix and vector that `build_system` returns (with $\varepsilon c$ added to $b$). $A$ is symmetric positive definite, so $\Phi$ has exactly one minimum, $x^* = A^{-1} b$.

*Proof.* Expand each term. $w (x_i - x_j)^2 = w x_i^2 + w x_j^2 - 2 w x_i x_j$ adds $w$ to $A_{ii}$ and $A_{jj}$ and $-w$ to $A_{ij}$ and $A_{ji}$. $w (x_i - X_q)^2 = w x_i^2 - 2 w X_q x_i + \mathrm{const}$ adds $w$ to $A_{ii}$ and $w X_q$ to $b_i$. The anchor and center terms add $\beta$ and $\varepsilon$ to $A_{ii}$ and $\beta a_i$ and $\varepsilon c$ to $b_i$. These are the updates of `build_system`. For any $z \ne 0$,

$$z^\top A z = \sum w_{ij} (z_i - z_j)^2 + \sum w_{iq} z_i^2 + \beta \sum z_i^2 + \varepsilon \sum z_i^2 \ge \varepsilon \lVert z \rVert^2 > 0,$$

since every weight is nonnegative. So $A$ is positive definite. The gradient of $\Phi$ is $2 (A x - b)$, and a strictly convex quadratic has its one minimum where the gradient is zero. $\square$

**Lemma 2.** In exact arithmetic, the [conjugate gradient method](/conjugate-gradient-method/) on $A x = b$ reaches $x^*$ in at most $n$ steps.

*Proof.* This is the finite termination theorem of Hestenes and Stiefel (1952) for symmetric positive definite matrices, which this page cites and does not prove again: the search directions are $A$-conjugate, so after $m$ steps the iterate minimizes $\Phi$ over an $m$-dimensional affine subspace, and these subspaces grow until they are the whole space. Lemma 1 gives the hypothesis. $\square$

In floating point the implementation stops when the residual is below a tolerance, so it returns an approximation of $x^*$. The tests compare it with exact Gaussian elimination over the rationals. This is a measurement, not a proof. The legality below does not depend on how good the approximation is: SPREAD accepts any real positions.

## The spreading step

SPREAD$(B, S)$ takes a list of blocks $B$ with $m = |B|$, a list of distinct sites $S$, and the current positions. If $B$ is empty it returns. If $|S| = 1$ it puts the first block of $B$ on the one site. Otherwise it picks the axis along which the sites spread more, sorts the sites by that axis, and cuts them into a low part of $c_1$ sites and a high part of $c_2$ sites. The cut is at $\lfloor |S| / 2 \rfloor$, moved down to the first site with the same coordinate when that leaves the low part nonempty. It sorts the blocks by their position along the axis, sends the first $k$ blocks to the low part and the others to the high part, where

$$k = \max\left(m - c_2,\ \min\left(c_1,\ \left\lfloor \frac{m c_1}{c_1 + c_2} + \frac{1}{2} \right\rfloor\right)\right),$$

and recurses on both parts.

**Lemma 3.** If $m \le |S|$, then SPREAD$(B, S)$ ends and puts the blocks of $B$ on distinct sites of $S$.

*Proof.* By induction on $|S|$. If $B$ is empty there is nothing to show. If $|S| = 1$, then $m \le 1$, so $m = 1$ and the one block gets the one site.

Let $|S| \ge 2$. First, $1 \le c_1 \le |S| - 1$. The default cut $\lfloor |S| / 2 \rfloor$ is in that range. The moved cut is the number of sites whose coordinate is strictly below that of the site at the default cut; that site is not counted, so the number is at most the default cut, and the code uses it only when it is at least 1. So both parts are nonempty, and $c_1 + c_2 = |S|$.

Next, the value $k$ satisfies $0 \le k \le m$, $k \le c_1$ and $m - k \le c_2$. Let $r = \min(c_1, \lfloor m c_1 / (c_1 + c_2) + 1/2 \rfloor)$. Since $0 \le m c_1 / (c_1 + c_2) \le m$, the rounded value is in $[0, m]$, so $0 \le r \le \min(c_1, m)$. If $r \ge m - c_2$, then $k = r$, and $k \le c_1$, $k \le m$, $m - k \le c_2$ all hold. Otherwise $k = m - c_2 > r \ge 0$; then $m - k = c_2$, $k \le m$, and $k = m - c_2 \le c_1$ because $m \le |S| = c_1 + c_2$.

So the low call gets $k \le c_1$ blocks on $c_1 < |S|$ sites, and the high call gets $m - k \le c_2$ blocks on $c_2 < |S|$ sites. By the induction hypothesis both end and place their blocks on distinct sites of their own part. The two parts are disjoint and the two block lists are disjoint, so all blocks of $B$ get distinct sites of $S$. $\square$

The rounded value in $k$ is the share of the blocks that matches the share of the sites. The clamp only changes it when a part would get more blocks than sites, and then it sends the excess to the other part.

## The whole algorithm

**Theorem 4 (legality).** Every placement that line L4 builds is legal, and so is the placement that HEAP returns.

*Proof.* Line L4 calls SPREAD once per type $t$, with the blocks of type $t$ and the sites $S_t$. Since $n_t \le |S_t|$, Lemma 3 puts every block of type $t$ on a distinct site of $S_t$. The sets $S_t$ for different types are disjoint, because each column has one type. So the whole map is injective and every block is on a site of its type. HEAP returns one of these placements. $\square$

**Theorem 5 (the returned cost).** HEAP ends after `iters` iterations. It returns the placement of least HPWL among the placements of line L4, and that HPWL is at least the least HPWL over all legal placements.

*Proof.* The loop of line L3 runs `iters` times, each solve ends (the conjugate gradient loop has a step cap), and each SPREAD ends by Lemma 3. Line L5 keeps the placement of least HPWL so far, so at the end `best` has the least HPWL in the history. It is legal by Theorem 4, so its HPWL is at least the minimum over all legal placements. $\square$

## What is not proved

Nothing here bounds the ratio of the returned HPWL to the optimum, and nothing proves that the anchored solves converge to a legal placement or that the HPWL decreases from one iteration to the next. HeAP, like SimPL, is a heuristic: the tests measure that on small seeded instances the returned HPWL is close to the exhaustive optimum, and they check the lower bound of Theorem 5 on every instance. $\blacksquare$
