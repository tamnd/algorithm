---
title: Correctness of dynamic programming stereo on a scanline
proves: [correctness]
status: full
---

Fix one row of width $W$, the left intensities $l_0, \dots, l_{W-1}$, the right intensities $r_0, \dots, r_{W-1}$, a disparity range $D \ge 2$, an occlusion cost $\kappa \ge 0$ and a match cost $c$. A matching is a set $M$ of pairs $(i, j)$ with $0 \le i - j \le D - 1$ that is strictly increasing in both coordinates. Its cost is $\mathrm{cost}(M) = \sum_{(i,j) \in M} c(l_i, r_j) + 2\kappa (W - |M|)$, since $W - |M|$ pixels of each image stay unmatched. We prove that the program returns a matching of least cost.

## Paths and matchings

A path is a sequence of grid points from $(0, 0)$ to $(W, W)$ in which each step is one of: a match step $(i, j) \to (i+1, j+1)$, allowed only if $0 \le i - j \le D - 1$, with cost $c(l_i, r_j)$; a left step $(i, j) \to (i+1, j)$ with cost $\kappa$ (left pixel $i$ unmatched); a right step $(i, j) \to (i, j+1)$ with cost $\kappa$ (right pixel $j$ unmatched). The match steps of a path, read as pairs $(i, j)$, form a matching, because $i$ and $j$ only grow and a match step raises both. Each left pixel is passed by exactly one step that raises $i$, so it is either matched once or skipped once by a left step, and the same holds for right pixels. So the cost of a path equals the cost of its matching. Conversely, every matching is the matching of some path: visit its pairs in order and, between two consecutive pairs and at the two ends, add the needed left and right steps.

## The band lemma

Call $(i, j)$ in the band if $0 \le i - j \le D - 1$. Claim: every matching is the matching of a path that stays in the band.

Let $(i, j)$ be the point just after a match (or $(0, 0)$), and $(i', j')$ the point where the next match starts (or $(W, W)$). Both points are in the band: a match step keeps $i - j$, and the ends have $i - j = 0$. Let $k = i - j$ and $k' = i' - j'$. Between them we need $a = i' - i$ left steps, each raising $i - j$ by 1, and $b = j' - j$ right steps, each lowering it by 1, with $a - b = k' - k$. First take $|k' - k|$ steps of the needed kind to move from $k$ to $k'$; all the values on the way lie between $k$ and $k'$, so in the band. The steps left over come in pairs of one left and one right step. Since $D \ge 2$, either $k' + 1 \le D - 1$ or $k' - 1 \ge 0$; in the first case do each pair as left then right, and in the second as right then left. The difference then moves between $k'$ and a neighbor in the band. So the whole path stays in the band. (With $D = 1$ the band is the diagonal, and no pixel could be skipped; that is why the code requires $D \ge 2$.)

So the least cost of a matching equals the least cost of a path in the band.

## The recurrence

Let $C(i, j)$ be the least cost of a path in the band from $(0, 0)$ to $(i, j)$. Then $C(0,0) = 0$, and for every other point in the band the last step of such a path is a match step from $(i-1, j-1)$, a left step from $(i-1, j)$ or a right step from $(i, j-1)$, from a point that must itself be in the band. Removing the last step leaves a path in the band to that point, so

$$C(i, j) = \min\big(C(i-1, j-1) + c(l_{i-1}, r_{j-1}),\ C(i-1, j) + \kappa,\ C(i, j-1) + \kappa\big),$$

over the terms whose start point exists and is in the band. These are the three candidates of lines L4 to L6: the match from $(i-1, j-1)$ has the same $k = i - j$; the left step comes from $k - 1$ and needs $k \ge 1$; the right step comes from $k + 1$ in the same $i$ and needs $j \ge 1$ and $k + 1 \le D - 1$.

The loops visit $i$ in increasing order and, for each $i$, $k$ in decreasing order. The point $(i-1, \cdot)$ belongs to an earlier $i$, and $(i, j-1)$ has the larger $k + 1$ in the same $i$, so every term is final when it is read. By induction over this order, the table holds $C(i, j)$ at every point, and $C(W, W)$ is the least cost of a matching.

## The traceback

Line L7 stores which candidate gave the minimum. Starting at $(W, W)$, line L8 follows the stored steps back. Each stored step leads to a point whose value plus the step cost equals the current value, so the steps form a path from $(0, 0)$ to $(W, W)$ in the band of cost exactly $C(W, W)$. Its match steps are the returned matching, and each match $(i, j)$ gives the disparity $i - j$ of left pixel $i$. By the first section this matching has cost $C(W, W)$, the least possible. $\square$

## Cost

There are $(W + 1) D$ table entries, each found in $O(1)$ time from three earlier entries, and the traceback has at most $2W$ steps. So one row costs $\Theta(W D)$ time and space, and an image of $H$ rows costs $\Theta(W H D)$ time.
