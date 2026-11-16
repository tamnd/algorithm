---
tag: V82D4Y
kind: algorithm
slug: alpha-expansion
name: Alpha-expansion
aliases:
- expansion move algorithm
- Boykov-Veksler-Zabih expansion
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Minimize a multi-label energy with a metric pairwise term by repeated min cuts, each letting any set of sites switch to one label alpha. Within 2c of the optimum, so 2 for Potts.
solves: [map-inference]
model: real-ram
complexity:
  vars: {n: the number of sites, m: the number of neighbor pairs, L: the number of labels, k: the number of cycles over the labels, F: the time of one max flow on n + 2 nodes and n + m edges}
  time: {worst: O(k L (F + n + m)), average: O(k L (F + n + m)), best: O(L (F + n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Yuri Boykov, Olga Veksler, Ramin Zabih]
  note: Boykov, Veksler and Zabih introduced the expansion and swap moves for vision energies, solved each move by a minimum cut, and proved the factor 2c for expansion local minima.
prereqs: [graph-representable-energies, potts-model, max-flow-min-cut-theorem]
see_also: [alpha-beta-swap, qpbo, iterated-conditional-modes, boykov-kolmogorov-max-flow, graph-cut-stereo, multiway-cut-problem, markov-random-field, loopy-belief-propagation]
sources:
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239
    locator: Section 3 (the move spaces and the expansion algorithm), Section 5 with Theorem 5.4 and Corollary 5.5 (the graph of an expansion move), Section 6.1 with Theorem 6.1 (the bound 2c), Section 7 and the Appendix (NP-hardness of the Potts energy), Section 8 (experiments)
  - paper: doi:10.1109/TPAMI.2004.1262177
    title: Vladimir Kolmogorov and Ramin Zabih, What energy functions can be minimized via graph cuts?, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(2), 2004, 147-159
    locator: Theorem 4.1 and Section 4.1 (the graph for a regular binary energy, used here for each move)
  - paper: doi:10.1109/TPAMI.2007.70844
    title: Richard Szeliski, Ramin Zabih, Daniel Scharstein, Olga Veksler, Vladimir Kolmogorov, Aseem Agarwala, Marshall Tappen and Carsten Rother, A comparative study of energy minimization methods for Markov random fields with smoothness-based priors, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(6), 2008, 1068-1080
    locator: the comparison of expansion, swap, ICM, loopy belief propagation and TRW-S on stereo, segmentation, photomontage and denoising energies
  - book: isbn:9780262015776
    title: Andrew Blake, Pushmeet Kohli and Carsten Rother (editors), Markov Random Fields for Vision and Image Processing, MIT Press, 2011
    locator: Part I, Algorithms for inference of MAP estimates for MRFs (the chapters on graph cuts and move making algorithms)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 4, Model fitting and optimization (Markov random fields, graph cuts and alpha-expansion)
---

Alpha-expansion is a method for labeling problems: give each of $n$ sites one of $L$ labels so that a sum of costs is small. Each site pays a cost for its own label, and each neighbor pair pays a cost $V$ that depends on the two labels, for example a fixed penalty when they differ. The method improves a labeling by moves. An $\alpha$-expansion move picks one label $\alpha$ and lets any subset of the sites change to $\alpha$ at once, while the other sites keep their labels. There are $2^n$ such subsets, but when $V$ is a metric the best one is found exactly by one [minimum cut](/min-cut-problem/), because the energy of the move is a regular binary energy (the [Kolmogorov-Zabih theorem](/graph-representable-energies/)). The algorithm cycles over the labels until no move lowers the energy. Finding the best labeling is NP-hard already for the [Potts model](/potts-model/) with three labels, but the result of alpha-expansion is within a factor $2c$ of the optimum, where $c$ is the ratio of the largest to the smallest cost of two different labels, so within 2 for Potts. It is a standard method for [MAP inference](/map-inference/) in [Markov random fields](/markov-random-field/) on images and meshes: stereo, segmentation, image stitching and mesh segmentation.

## In plain words

Each pixel needs a label, such as a depth or a color class. A label that fits the pixel is cheap, and two neighbors with different labels pay a penalty. Start with any labeling. Now pick one label and ask: which pixels should switch to this label, all at once, to lower the total cost the most? Any group of pixels may switch, which is far more than trying one pixel at a time, and a minimum cut in a graph finds the best group exactly. Do this for each label in turn, and repeat the whole round until no label helps. The answer is not always the best one, but it cannot be worse than twice the best for the simple penalty.

## The problem

**Input.** A set of $n$ sites, a set $\mathcal{N}$ of $m$ neighbor pairs with weights $w_{pq} \ge 0$, a set of $L$ labels, data costs $D_p(\ell) \ge 0$, and a metric $V$ on the labels: $V(a, b) = 0$ exactly when $a = b$, $V(a, b) = V(b, a) \ge 0$, and $V(a, b) \le V(a, c) + V(c, b)$.

**Output.** A labeling $f$ with small energy

$$E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq}\, V(f_p, f_q),$$

which no $\alpha$-expansion improves, for any label $\alpha$. An $\alpha$-expansion of $f$ is any labeling $g$ with $g_p \in \{f_p, \alpha\}$ for all $p$.

Examples of metrics are the Potts model $V(a,b) = \lambda [a \ne b]$ and the truncated linear distance $V(a,b) = \min(|a - b|, K)$ on ordered labels. The truncated quadratic $\min((a - b)^2, K)$ is not a metric; it is only a semimetric, which suits [alpha-beta swap](/alpha-beta-swap/).

## The algorithm

```pseudo id=main
ALPHA-EXPANSION(D, V, N, f)
L1  repeat
L2      success ← false
L3      for each label α do
L4          build the binary energy B(x) = E(g(x)), where g(x)_p = α if x_p = 1 and f_p if x_p = 0
L5          x ← a minimizer of B by one minimum cut
L6          f' ← g(x)
L7          if E(f') < E(f) then f ← f'; success ← true
L8  until success = false
L9  return f
```

For a pair $(p, q)$, the move energy has the four values $w V(f_p, f_q)$, $w V(f_p, \alpha)$, $w V(\alpha, f_q)$ and $w V(\alpha, \alpha) = 0$ for $(x_p, x_q) = (0,0), (0,1), (1,0), (1,1)$. It is regular when $V(f_p, f_q) \le V(f_p, \alpha) + V(\alpha, f_q)$, which is the triangle inequality. Line L5 builds the graph of the [theorem page](/graph-representable-energies/): an edge $p \to q$ of capacity $w(V(f_p, \alpha) + V(\alpha, f_q) - V(f_p, f_q))$ for each pair, and an edge from the source or to the sink for the linear part of each site. Boykov, Veksler and Zabih built a different graph, with an extra node on each pair whose ends have different labels; both give the same minimum. The code checks regularity and stops with an error on a nonregular pair term, which happens when $V$ is not a metric.

## Example

Take four sites in a row, labels 0, 1, 2, the Potts model with $\lambda = 4$, and the data costs

| site | $D(0)$ | $D(1)$ | $D(2)$ |
|---|---|---|---|
| 0 | 0 | 5 | 1 |
| 1 | 2 | 6 | 0 |
| 2 | 6 | 0 | 5 |
| 3 | 0 | 2 | 5 |

Start from the best label of each site, $f = (0, 2, 1, 0)$, with $E = 0 + 3 \cdot 4 = 12$.

| cycle | $\alpha$ | best $\alpha$-expansion | $E$ | accepted |
|---|---|---|---|---|
| 1 | 0 | $(0, 0, 0, 0)$ | 8 | yes |
| 1 | 1 | $(0, 0, 1, 1)$ | 8 | no |
| 1 | 2 | $(0, 0, 0, 0)$ | 8 | no |
| 2 | 0, 1, 2 | no move below 8 | 8 | no |

The algorithm stops after two cycles at $(0, 0, 0, 0)$ with $E = 8$. The optimum is $(2, 2, 1, 1)$ with $E = 1 + 0 + 0 + 2 + 4 = 7$. From $(0,0,0,0)$, no single move reaches it, because it uses two new labels. Every 2-expansion that changes a site costs at least 10, for example $(2, 2, 2, 0)$, and the best 1-expansion $(0, 0, 1, 1)$ only ties at 8. The ratio $8/7$ is well below the bound 2.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts. First, the binary energy of line L4 equals the energy of the labeling it describes, and its pair terms are regular by the triangle inequality, so the cut of line L5 gives the best expansion. Second, each accepted move lowers the energy strictly and there are finitely many labelings, so the loop stops, and in the last cycle no label gives an improving expansion. Third, the bound of Theorem 6.1 of Boykov, Veksler and Zabih: compare the output $\hat f$ with the expansion that copies an optimal labeling $f^*$ on the sites where $f^*_p = \alpha$. Each such comparison bounds the energy of $\hat f$ on those sites and their pairs. Summed over $\alpha$, every pair with $f^*_p \ne f^*_q$ appears twice and pays at most $c$ times its cost in $f^*$, which gives $E(\hat f) \le E_D(f^*) + 2c\, E_V(f^*) \le 2c\, E(f^*)$.

## Complexity

The model is the real RAM; the tests use integer costs, so that the cuts and the comparisons are exact.

- **One move.** Building the graph takes $O(n + m)$ time, and the cut takes the time $F$ of one max-flow computation on $n + 2$ nodes and at most $n + m$ edges. The code uses [Edmonds-Karp](/edmonds-karp/) for clarity; programs on images use the [Boykov-Kolmogorov algorithm](/boykov-kolmogorov-max-flow/), whose speed on such grids is measured, not bounded.
- **One cycle.** $L$ moves and $L$ energy evaluations, $O(L(F + n + m))$.
- **Number of cycles.** With integer costs each accepted move lowers $E$ by at least 1, so $k \le E(f_0) - \min E + 1$. There is no better general bound. On image energies programs usually stop after a few cycles; this is an observation, not a bound.
- **Space.** $O(n + m)$ for the graph and the labeling.

## Properties

- **Approximation.** $E(\hat f) \le 2c\, E(f^*)$ for a metric $V$ and $D \ge 0$. For Potts, $c = 1$. For truncated linear on the integer labels $0, \ldots, L - 1$ with $1 \le K \le L - 1$, $c = K$.
- **Strong moves.** A local minimum for expansion moves is also a local minimum for single-site changes, the moves of [ICM](/iterated-conditional-modes/), because changing one site $p$ to $\alpha$ is an $\alpha$-expansion.
- **Hard problem.** Minimizing the Potts energy with $L \ge 3$ labels is NP-hard, by a reduction from the [multiway cut problem](/multiway-cut-problem/) (Section 7 and the Appendix of the paper). So an exact polynomial algorithm is not expected, and a guarantee like $2c$ is the realistic goal.
- **Two labels.** For $L = 2$, start from the labeling with all sites at 0. The move space of label 1 then contains every labeling, so one move gives the exact minimum.
- **Deterministic.** For a fixed order of labels and fixed tie-breaking in the cut, the output is fixed. Different orders can stop at different local minima.

## Variants and improvements

- **Graph with auxiliary nodes.** The original construction puts an extra node on each pair with $f_p \ne f_q$. It gives the same move.
- **Swap moves.** [Alpha-beta swap](/alpha-beta-swap/) needs only a semimetric but has no constant factor bound.
- **Fusion moves.** Lempitsky, Rother, Roth and Blake (2010) combine the current labeling with any proposal labeling, not only a constant one; the move energy is then often nonregular and is solved by [QPBO](/qpbo/).
- **Primal-dual view.** Komodakis and Tziritas (2007) explained expansion as a primal-dual method for the [linear programming relaxation](/lp-relaxation/), and the FastPD code of Komodakis, Tziritas and Paragios reuses the dual solution between moves.
- **Reuse of flows.** Consecutive cuts differ a little, so dynamic max-flow codes reuse the residual graph of the last cycle.
- **Ordered labels.** For a convex $V$ on ordered labels, Ishikawa (2003) gives an exact solution by one cut on a graph with $n L$ nodes.

## When to use it

Use alpha-expansion for energies with a metric pairwise term, such as Potts or truncated linear: stereo with a smoothness prior ([graph cut stereo](/graph-cut-stereo/)), segmentation into several regions, image stitching and the segmentation of 3D meshes. In the comparison of Szeliski et al. (2008), expansion was among the best methods on most of the energies and much better than [ICM](/iterated-conditional-modes/). Use swap or [loopy belief propagation](/loopy-belief-propagation/) when $V$ is not a metric, and TRW-S when a lower bound is needed.

## Pitfalls

- **Nonmetric terms.** With truncated quadratic or another semimetric, some move energies are not regular, and a cut does not give the best move. Truncating the nonregular terms makes the method run but voids the bound.
- **Negative data costs.** The bound needs $D_p \ge 0$. Add a constant to each site to make the costs nonnegative; this changes the bound but not the moves.
- **Ties.** Accept a move only if it lowers the energy strictly, or the loop can cycle between labelings of equal energy.
- **Floating point.** Large and small costs together make the cut inexact. Scale costs to integers when possible.
- **The bound is loose.** In practice the result is usually much closer to the optimum than $2c$, but $2c$ is all that is proved. Do not quote the measured gap as a guarantee.

## Implementations

## History

Boykov, Veksler and Zabih introduced expansion and swap moves at ICCV 1999 and in the journal paper of 2001, with a graph for each move and the proof of the factor $2c$. They also showed that the Potts energy is NP-hard to minimize. Kolmogorov and Zabih (2004) gave the general rule for which binary energies a cut can minimize, which explains the metric condition. Szeliski et al. (2008) compared the move algorithms with ICM, loopy belief propagation and TRW-S on a common benchmark of vision energies, and expansion became a default method for multi-label problems in vision and graphics.

## References
