---
tag: HDGW2G
kind: algorithm
slug: normalized-cut
name: Normalized cut
aliases:
- Shi-Malik normalized cut
- ncut
- Shi-Malik segmentation algorithm
area: machine-learning/clustering
level: advanced
summary: "Split a weighted graph in two by the second generalized eigenvector of (D - W) y = λ D y and the best threshold cut along it; recurse while the normalized cut stays small."
solves: [clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of output parts}
  time: {worst: "O(k n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 2000
  people: [Jianbo Shi, Jitendra Malik]
  note: Shi and Malik presented the normalized cut at CVPR 1997 and published the full paper in IEEE PAMI in 2000. Its appendix gives a proof by Papadimitriou that the exact minimum is NP-complete.
prereqs: [cut, laplacian-matrix, generalized-eigenvalue-problem, rayleigh-quotient]
see_also: [spectral-clustering, cheeger-inequality, conductance, graph-partitioning-problem, sparsest-cut-problem, image-segmentation-graph-cuts, kernel-k-means, eigengap-heuristic]
sources:
  - paper: doi:10.1109/34.868688
    title: "Jianbo Shi and Jitendra Malik, Normalized cuts and image segmentation, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(8), 2000, pages 888 to 905"
    locator: "Section 2 (the Ncut criterion, Ncut = 2 - Nassoc, and the relaxation to (D - W) y = λ D y), Section 3 (the grouping algorithm and the recursive 2-way cut) and the appendix (NP-completeness, due to Papadimitriou)"
  - paper: doi:10.1007/s11222-007-9033-z
    title: "Ulrike von Luxburg, A tutorial on spectral clustering, Statistics and Computing 17(4), 2007, pages 395 to 416"
    locator: "Section 5 (RatioCut and Ncut, their NP-hardness citing Wagner and Wagner 1993, and the relaxations for k = 2 and general k)"
  - paper: "Dorothea Wagner and Frank Wagner, Between min cut and graph bisection, Mathematical Foundations of Computer Science (MFCS 1993), Lecture Notes in Computer Science 711, Springer, 1993, pages 744 to 750"
    locator: the NP-hardness of balanced cut criteria
  - paper: "Lars Hagen and Andrew B. Kahng, New spectral methods for ratio cut partitioning and clustering, IEEE Transactions on Computer-Aided Design 11(9), 1992, pages 1074 to 1085"
    locator: the ratio cut criterion and its spectral relaxation by the second eigenvector of L
---

The normalized cut of Shi and Malik splits a weighted graph into two parts $A$ and $B$ so that little weight crosses the split and both parts carry a large share of the total weight. The criterion is $\mathrm{Ncut}(A, B) = \mathrm{cut}(A, B)/\mathrm{vol}(A) + \mathrm{cut}(A, B)/\mathrm{vol}(B)$. Its exact minimum is NP-hard, so the algorithm solves a relaxation: it takes the second smallest generalized eigenvector $y$ of $(D - W) y = \lambda D y$, sorts the vertices by $y$, and returns the best of the $n - 1$ threshold cuts. To get more than two parts, it splits each part again while the normalized cut of the split stays below a threshold. With a dense eigensolver one split costs $O(n^3)$ time.

## In plain words

Think of a picture as a net of pixels. Neighbor pixels of similar color are tied by strong strings, and pixels of different color by weak strings. To cut the picture into two regions, cut strings so that the cut strings are weak in total.

The weakest cut often cuts off one lonely pixel, which is not useful. The normalized cut fixes this: it divides the cut weight by the total string weight that each side holds. A tiny side holds little weight, so cutting it off costs a lot.

Finding the best such cut exactly is too hard for large pictures. The algorithm lets each pixel take any number instead of "left" or "right". This easier problem has a fast answer, an eigenvector. Sort the pixels by their number, try each place to split the sorted list, and keep the best split. Repeat on each region.

## The problem

The input is a symmetric matrix $W = (w_{ij})$ of size $n \times n$ with $w_{ij} \ge 0$ and $w_{ii} = 0$: the weighted similarity graph. The degree of vertex $i$ is $d_i = \sum_j w_{ij}$, and $D = \mathrm{diag}(d_1, \ldots, d_n)$. For a set $A$ of vertices and its complement $B = V \setminus A$,

$$\mathrm{cut}(A, B) = \sum_{i \in A,\, j \in B} w_{ij}, \qquad \mathrm{vol}(A) = \sum_{i \in A} d_i, \qquad \mathrm{Ncut}(A, B) = \frac{\mathrm{cut}(A, B)}{\mathrm{vol}(A)} + \frac{\mathrm{cut}(A, B)}{\mathrm{vol}(B)}.$$

Shi and Malik write $\mathrm{assoc}(A, V)$ for $\mathrm{vol}(A)$. The goal is a bipartition with both sides non-empty and the least Ncut. The related **RatioCut** of Hagen and Kahng (1992) divides by the sizes instead: $\mathrm{RatioCut}(A, B) = \mathrm{cut}(A, B)/|A| + \mathrm{cut}(A, B)/|B|$.

Shi and Malik also define the normalized association $\mathrm{Nassoc}(A, B) = \mathrm{assoc}(A, A)/\mathrm{vol}(A) + \mathrm{assoc}(B, B)/\mathrm{vol}(B)$, the share of weight that stays inside each side. Because $\mathrm{vol}(A) = \mathrm{assoc}(A, A) + \mathrm{cut}(A, B)$, $\mathrm{Ncut}(A, B) = 2 - \mathrm{Nassoc}(A, B)$. So one criterion makes the cut small and the groups tight at the same time.

**Hardness.** Minimizing Ncut is NP-complete, even on grid graphs; Shi and Malik give the proof, due to Papadimitriou, in their appendix. Wagner and Wagner (1993) showed that balanced cut criteria of this type are NP-hard, and von Luxburg (Section 5) cites them for both RatioCut and Ncut. So the algorithm below is a heuristic with a lower bound, not an exact method; see [NP-hard](/np-hard/).

**The relaxation.** For a bipartition put $b = \mathrm{vol}(A)/\mathrm{vol}(B)$ and $y_i = 1$ for $i \in A$, $y_i = -b$ for $i \in B$. Then $y^T D \mathbb{1} = 0$ and

$$\mathrm{Ncut}(A, B) = \frac{y^T (D - W) y}{y^T D y}.$$

For RatioCut the same holds with $f_i = |B|$ on $A$, $f_i = -|A|$ on $B$, the plain [Laplacian](/laplacian-matrix/) $L = D - W$ and $f^T f$ in the denominator. Shi and Malik drop the condition that $y$ takes two values. The least [Rayleigh quotient](/rayleigh-quotient/) $y^T L y / y^T D y$ over real $y \ne 0$ with $y^T D \mathbb{1} = 0$ is the second smallest eigenvalue $\lambda_2$ of the [generalized eigenproblem](/generalized-eigenvalue-problem/) $L y = \lambda D y$, and the minimizer is its eigenvector.

## The algorithm

```pseudo id=main
NCUT-BIPARTITION(W)
L1  d_i ← Σ_j w_ij for each i,  D ← diag(d_1, ..., d_n)       ▷ needs each d_i > 0
L2  M ← I − D^(−1/2) W D^(−1/2)                              ▷ L_sym, symmetric
L3  (λ_2, v) ← the second smallest eigenvalue of M and a unit eigenvector
L4  y ← D^(−1/2) v                                            ▷ now (D − W) y = λ_2 D y
L5  sort the vertices so that y_π(1) ≤ y_π(2) ≤ ... ≤ y_π(n)
L6  for s ← 1 to n − 1: A_s ← {π(1), ..., π(s)}, value_s ← Ncut(A_s, V \ A_s)
L7  return the A_s with the least value_s and its complement

RECURSIVE-NCUT(W, τ)
    put V on a stack;  repeat until the stack is empty:
L8      pop S;  if |S| = 1, output S;  if S is not connected, push its components
L9      (A, B) ← NCUT-BIPARTITION(W restricted to S)
L10     if Ncut(A, B) > τ then output S                       ▷ the split is not good enough
L11     else push A and push B
```

Line L6 updates the cut and the volume when one vertex moves from $B$ to $A$, so the $n - 1$ cuts cost $O(n^2)$ in all, not $O(n^3)$. Shi and Malik try a fixed number of evenly spaced thresholds instead of all $n - 1$, and they also stop when the eigenvector is not stable (when its values do not form clear groups). Line L8 splits a part that is not connected into its components first, because such a split has $\mathrm{Ncut} = 0$ and the eigenvector of a disconnected part is not unique.

The sign of $v$ in line L3 does not matter: reversing the order in line L5 gives the same $n - 1$ cuts.

## Example

**A 2-way cut that finds the optimum.** Take six vertices with the edges $\{0,4\}$ of weight 1, $\{1,2\}$, $\{1,3\}$ and $\{2,4\}$ of weight 3, and $\{4,5\}$ of weight 2. The degrees are $1, 6, 6, 3, 6, 2$, and the total volume is 24.

Line L3 gives $\lambda_2 = 1 - 1/\sqrt{2} \approx 0.2929$, and line L4 gives $y \approx (0.289, -0.204, 0, -0.289, 0.204, 0.289)$. The sweep order is $3, 1, 2, 4, 0, 5$:

| $A_s$ | cut | vol($A_s$) | vol($B$) | Ncut |
|---|---|---|---|---|
| $\{3\}$ | 3 | 3 | 21 | $8/7 \approx 1.143$ |
| $\{1, 3\}$ | 3 | 9 | 15 | $8/15 \approx 0.533$ |
| $\{1, 2, 3\}$ | 3 | 15 | 9 | $8/15$ |
| $\{1, 2, 3, 4\}$ | 3 | 21 | 3 | $8/7$ |
| $\{0, 1, 2, 3, 4\}$ | 2 | 22 | 2 | $12/11 \approx 1.091$ |

Line L7 returns $\{1, 3\}$ against $\{0, 2, 4, 5\}$ with $\mathrm{Ncut} = 8/15$. A brute force over all $2^5 - 1 = 31$ bipartitions confirms that $8/15$ is the minimum, and $\lambda_2 \approx 0.293 \le 8/15$, as the relaxation promises.

**Ncut against RatioCut.** On the same graph the least RatioCut is $6/5$: it cuts off vertex 0, whose only edge has weight 1, since $1/1 + 1/5 = 6/5$. The Ncut of that split is $1/1 + 1/23 = 24/23$, much worse than $8/15$, because vertex 0 has volume 1. The other way round, the Ncut optimum $\{0, 4, 5\}$ against $\{1, 2, 3\}$ has RatioCut $3/3 + 3/3 = 2$. RatioCut balances the number of vertices; Ncut balances the weight.

**A case where the sweep misses.** Take six vertices with the edges $\{0,1\}$ of weight 1, $\{0,3\}$, $\{1,5\}$, $\{3,4\}$ and $\{3,5\}$ of weight 2, and $\{2,4\}$, $\{2,5\}$ and $\{4,5\}$ of weight 3. Then $\lambda_2 \approx 0.552$, $y \approx (-0.367, -0.197, 0.188, -0.148, 0.118, 0.051)$, and the sweep order is $0, 1, 3, 5, 4, 2$, with the Ncut values $12/11$, $4/5$, $3/4$, $72/77$ and $6/5$. The algorithm returns $\{0, 1, 3\}$ with $3/4$. The true optimum is $\{0, 3\}$ with $5/9 + 5/27 = 20/27 \approx 0.741$, which is not a threshold set of $y$. The relaxation is a heuristic.

## Correctness

The algorithm always returns a bipartition with both sides non-empty, because line L6 takes $1 \le s \le n - 1$. Its value is at least the optimum, and the optimum is at least $\lambda_2$:

$$\lambda_2 \;\le\; \min_{A} \mathrm{Ncut}(A, V \setminus A) \;\le\; \mathrm{Ncut}(\text{output}).$$

The left inequality holds because each bipartition gives a feasible vector $y$ of the relaxation with Rayleigh quotient equal to its Ncut, and $\lambda_2$ is the least quotient over all feasible vectors (the generalized form of the [Courant-Fischer theorem](/courant-fischer-theorem/)). So $\lambda_2$ certifies how good the output is: if the output value is close to $\lambda_2$, it is close to optimal.

There is also an upper bound. $\lambda_2$ is the spectral gap of the random walk $D^{-1} W$, and the sweep along $y$ is the sweep in the proof of the [Cheeger inequality](/cheeger-inequality/). It finds a set with [conductance](/conductance/) $\mathrm{cut}(A, B)/\min(\mathrm{vol}(A), \mathrm{vol}(B)) \le \sqrt{2 \lambda_2}$, and Ncut is at most twice the conductance. Hence the output has $\mathrm{Ncut} \le 2\sqrt{2\lambda_2} \le 2\sqrt{2\,\mathrm{OPT}}$. This bound is weak when the optimum is small, and Guattery and Miller (1998) gave graphs on which spectral sweeps are far from optimal. The full proof is in the correctness proof.

The recursion stops: each split in line L11 makes two non-empty parts, so there are at most $n - 1$ splits.

## Complexity

The costs are in the [real RAM](/real-ram/) model with a dense eigensolver.

- **One 2-way cut.** Lines L1 and L2 cost $\Theta(n^2)$. A dense symmetric eigensolver costs $O(n^3)$. Sorting costs $O(n \log n)$, and the incremental sweep costs $O(n^2)$, since moving one vertex changes the cut by the sum of one row of $W$.
- **Recursion.** Let the output have $k$ parts. There are $k - 1$ successful splits and $k$ final tries that fail the test in line L10, and each costs $O(n^3)$, so the total is $O(k n^3)$.
- **Sparse graphs.** Only one eigenvector is needed. For a graph with $m$ edges, the [Lanczos method](/lanczos-algorithm/) costs $O(m)$ per iteration, and Shi and Malik report about $O(n^{1.5})$ for the sparse graphs of images. The number of iterations grows when the gap between $\lambda_2$ and $\lambda_3$ is small.

The memory is $\Theta(n^2)$ for a dense $W$ and $O(n + m)$ for a sparse one.

## Properties

- **A lower bound for free.** The eigenvalue $\lambda_2$ is a lower bound on the optimal Ncut, so each run reports how far from optimal it can be.
- **Balanced by weight.** Ncut prefers splits where both sides have a large volume, and $\mathrm{Ncut} = 2 - \mathrm{Nassoc}$, so it also prefers tight groups.
- **Deterministic.** The eigenvector is unique up to sign when $\lambda_2 < \lambda_3$, and the sign does not change the set of sweep cuts.
- **Scale invariant.** Multiplying $W$ by a positive constant does not change Ncut or $y$.

## Variants and improvements

- **Simultaneous k-way cut.** Use the first $k$ generalized eigenvectors and cluster their rows, as in the Shi and Malik variant of [spectral clustering](/spectral-clustering/). Shi and Malik also discuss this, and von Luxburg (Section 5) derives it from the $k$-way Ncut.
- **RatioCut.** Replace $D$ by $I$ in the relaxation: the second eigenvector of $L$ (the Fiedler vector) relaxes RatioCut. This is the older method of Hagen and Kahng (1992).
- **Conductance and sparsest cut.** Dividing by $\min(\mathrm{vol}(A), \mathrm{vol}(B))$ gives the conductance, and dividing by $|A| \cdot |B|$ gives the [sparsest cut](/sparsest-cut-problem/). These have approximation algorithms with proven ratios that do not depend on $\lambda_2$.
- **Kernel k-means.** The $k$-way Ncut equals a weighted [kernel k-means](/kernel-k-means/) objective (Dhillon, Guan and Kulis 2004), so kernel k-means iterations can minimize it without eigenvectors.
- **Min cut with seeds.** If some pixels are labeled in advance, a minimum $s$-$t$ cut solves the labeling exactly; see [image segmentation by graph cuts](/image-segmentation-graph-cuts/).

## When to use it

Use the normalized cut to split a similarity graph, such as an image graph, into a few regions of comparable weight, when an eigensolver for one sparse matrix is affordable. It is good when the regions are not convex, and it reports the lower bound $\lambda_2$. Do not use it when you need an exact minimum on a large graph, which is NP-hard, or when you need a proven approximation ratio; see the [graph partitioning problem](/graph-partitioning-problem/) for other methods. For more than a few parts, the simultaneous $k$-way version is usually more stable than deep recursion.

## Pitfalls

- **Zero degrees.** Line L2 divides by $\sqrt{d_i}$. Remove isolated vertices first.
- **Disconnected graph.** Then $\lambda_2 = 0$ with multiplicity at least 2, and the eigenvector in line L3 is any mix of component indicators. Split into components first, as line L8 does.
- **Splitting at zero.** Splitting at $y_i = 0$ or at the median is simpler than the sweep, but it can be much worse. The sweep in line L6 is cheap, so try all thresholds.
- **Sorting by the wrong vector.** The vector $v$ of line L3 is an eigenvector of $L_{\mathrm{sym}}$. The cut uses $y = D^{-1/2} v$. When the degrees differ, sorting by $v$ gives a different order and different cuts.
- **Reading $\lambda_2$ as the answer.** $\lambda_2$ is only a lower bound, and the gap to the true optimum can be large (Guattery and Miller 1998).

## Implementations

## History

Fiedler (1973) related the second eigenvector of the Laplacian to the connectivity of a graph, and Hagen and Kahng (1992) used it to relax the ratio cut in circuit partitioning. Shi and Malik presented the normalized cut at CVPR 1997 and published the full paper in 2000. They defined Ncut, showed $\mathrm{Ncut} = 2 - \mathrm{Nassoc}$, derived the generalized eigenproblem $(D - W) y = \lambda D y$, and applied the recursive 2-way cut to image segmentation; the appendix gives Papadimitriou's proof of NP-completeness. Von Luxburg (2007) put RatioCut and Ncut side by side as the relaxations behind unnormalized and normalized [spectral clustering](/spectral-clustering/).

## References
