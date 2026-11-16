---
tag: A0NX9X
kind: algorithm
slug: graph-cut-stereo
name: Graph cut stereo
aliases:
- Kolmogorov-Zabih stereo
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Solve stereo by minimizing an energy with data, smoothness, occlusion and uniqueness terms over sets of pixel matches, by expansion moves that are each one minimum cut.
solves: [stereo-matching]
model: real-ram
complexity:
  vars: {n: the number of pixels W H, D: the number of disparities, k: the number of cycles over the disparities, F: the time of one max flow on O(n) nodes and O(n) edges}
  time: {worst: O(k D (F + n)), average: O(k D (F + n)), best: O(D (F + n))}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Vladimir Kolmogorov, Ramin Zabih]
  note: Kolmogorov and Zabih (ICCV 2001) modeled stereo with occlusions as an energy over pixel matches with a uniqueness constraint and minimized it by expansion moves, each solved by a minimum cut.
prereqs: [stereo-matching, alpha-expansion, graph-representable-energies]
see_also: [boykov-kolmogorov-max-flow, semi-global-matching, scanline-dynamic-programming-stereo, alpha-beta-swap, potts-model, left-right-consistency-check, image-segmentation-graph-cuts, markov-random-field]
sources:
  - paper: doi:10.1109/ICCV.2001.937668
    title: Vladimir Kolmogorov and Ramin Zabih, Computing visual correspondence with occlusions using graph cuts, Proceedings of the Eighth IEEE International Conference on Computer Vision (ICCV 2001), volume 2, 508-515
    locator: the energy over assignments with data, occlusion, smoothness and uniqueness terms, and its minimization by expansion moves
  - paper: doi:10.5201/ipol.2014.97
    title: Vladimir Kolmogorov, Pascal Monasse and Pauline Tan, Kolmogorov and Zabih's graph cuts stereo matching algorithm, Image Processing On Line 4, 2014, 220-250
    locator: the detailed description of the energy and the graph of a move, the cap CUTOFF = 30 on the data cost, the smoothness weight 3 lambda when both intensity differences are below 8 and lambda otherwise, the default lambda = K / 5, and the choice of K in Section 4.2
  - paper: doi:10.1109/TPAMI.2004.1262177
    title: Vladimir Kolmogorov and Ramin Zabih, What energy functions can be minimized via graph cuts?, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(2), 2004, 147-159
    locator: Theorem 4.1 (regular binary energies of at most two variables per term are graph representable), used for each move
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239
    locator: Section 3 (expansion moves) and Section 8 (stereo with disparity labels and a Potts smoothness term)
  - paper: doi:10.1109/ICCV.1998.710763
    title: Sébastien Roy and Ingemar J. Cox, A maximum-flow formulation of the N-camera stereo correspondence problem, Proceedings of the Sixth International Conference on Computer Vision (ICCV 1998), 492-499
    locator: the first formulation of stereo as one maximum flow problem over the whole image
  - paper: doi:10.1109/TPAMI.2003.1233908
    title: Hiroshi Ishikawa, Exact optimization for Markov random fields with convex priors, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(10), 2003, 1333-1336
    locator: the exact minimum cut for labels on a line with a convex pairwise term, which covers stereo with a convex smoothness term
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: graph cuts (GC) among the global methods of the taxonomy and in the evaluation
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (global optimization with graph cuts)
---

Graph cut stereo treats [stereo matching](/stereo-matching/) as the minimization of one energy over the whole image, and minimizes it by minimum cuts. The simplest form gives each pixel a disparity label, with a data cost for the label and a [Potts](/potts-model/) cost for neighbors with different labels, and runs [alpha-expansion](/alpha-expansion/). The form of Kolmogorov and Zabih (2001), which this page implements, goes further. Its variables are not labels but assignments, possible matches between a left pixel and a right pixel, each active or not. The energy has four parts: a data cost for each active match, a cost $K$ for each pixel of either image that is matched to nothing (an occluded pixel), a smoothness cost when one of two neighboring matches with the same disparity is active and the other is not, and an infinite cost if a pixel takes part in two matches. The last term enforces uniqueness in both images, so occlusions are found by the energy itself and treat both images alike. An expansion move on a disparity $\alpha$ may drop old matches and switch matches of disparity $\alpha$ on or off. The best such move is a regular binary energy, so one minimum cut finds it, by the [Kolmogorov-Zabih theorem](/graph-representable-energies/). The method stops at a configuration that no expansion move improves. It costs one maximum flow per disparity and cycle, which is much more than [semi-global matching](/semi-global-matching/).

## In plain words

We want to match pixels of the left image with pixels of the right image in the same row. Each match costs the difference of the two colors. A pixel that stays unmatched pays a fixed price, because it might be hidden in the other view. Neighboring pixels like to move together, so we pay a little when one neighbor uses a certain shift and the other does not. No pixel may be in two matches. Start with nothing matched. Then, for one shift at a time, ask which old matches to drop and which new matches with this shift to add, all at once. A minimum cut in a graph answers this question exactly. Repeat for all shifts until nothing improves.

## The problem

**Input.** A rectified pair of $W \times H$ images $I_L$ and $I_R$, disparities $0, \dots, D - 1$, an occlusion cost $K \ge 0$, a smoothness weight $\lambda \ge 0$, and a data cost cap.

An assignment $a = (p, d)$ matches left pixel $p = (u, v)$ with right pixel $(u - d, v)$. A configuration is a set $A$ of active assignments. Two assignments are neighbors if they have the same disparity and their left pixels are 4-neighbors. The energy is

$$E(A) = \sum_{a \in A} D(a) + K \cdot \#\{\text{unmatched pixels of both images}\} + \sum_{\{a_1, a_2\} \in \mathcal{N}} V_{a_1 a_2} [\,|\{a_1, a_2\} \cap A| = 1\,] + \infty \cdot [\text{a pixel is in two active assignments}].$$

Here $D(a) = \min(|I_L(p) - I_R(q)|, \text{cutoff})$, and $V_{a_1 a_2} = 3\lambda$ if both the left and the right intensity differences of the two pixel pairs are below 8, and $\lambda$ otherwise, as in the IPOL version of the method.

**Output.** A unique configuration that no expansion move improves, and from it a disparity for each left pixel, or "occluded".

## The algorithm

For a disparity $\alpha$, an $\alpha$-expansion of $A$ is any configuration that keeps a subset of the active assignments with disparity other than $\alpha$ and adds any set of assignments with disparity $\alpha$.

```pseudo id=main
KZ-STEREO(I_L, I_R, D, K, λ)
L1  A ← ∅   (every pixel occluded)
L2  repeat
L3      success ← false
L4      for each disparity α do
L5          build the binary energy of the α-expansion: a variable per active assignment with d ≠ α (keep or drop) and per assignment with d = α (on or off)
L6          A' ← the configuration of a minimizer, found by one minimum cut
L7          if E(A') < E(A) then A ← A'; success ← true
L8  until success = false
L9  return the disparity of the active assignment of each left pixel, or occluded
```

For line L5, a kept old assignment has $x = 0$ and an active new one has $x = 1$. With this choice every term is regular. A pixel covered by an old assignment $a_0$ and by the new assignment $a_\alpha$ gets the term $\theta(x_{a_0}, x_{a_\alpha})$ with $\theta(1, 0) = K$ (both off: occluded), $\theta(0, 1) = \infty$ (both on: uniqueness fails) and 0 otherwise. A neighbor pair with the same disparity gets $V [x_1 \ne x_2]$. The data costs and the pixels with only one candidate give unary terms. The code uses a number larger than the current energy in place of $\infty$.

## Example

One row, $I_L = (10, 50, 50, 90)$, $I_R = (50, 50, 90, 20)$, $D = 2$, $K = 10$, $\lambda = 2$. The right row is the left row moved by one pixel, with a new value at the end.

| step | active assignments (left pixel, $d$) | $E$ |
|---|---|---|
| start | none: 8 pixels occluded | 80 |
| $\alpha = 0$ | (1, 0) | 64 |
| $\alpha = 1$ | (1, 1), (2, 1), (3, 1) | 20 |
| second cycle | no move lowers $E$ | 20 |

In the move on $\alpha = 0$, only left pixel 1 and right pixel 1 have equal values, so one match is added. It costs 0 for the data, saves $2K = 20$ of occlusion cost, and pays $\lambda = 2$ twice, for its two neighbors at disparity 0 that stay off: $E = 60 + 4 = 64$. In the move on $\alpha = 1$, the cut drops $(1, 0)$, because it shares left pixel 1 with $(1, 1)$, and switches on three exact matches. Left pixel 0 and right pixel 3 stay occluded, for $E = 2K = 20$. All 128 configurations of this row give at least 20, so here the result is the global minimum.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The variables of a move are in one-to-one correspondence with its move space. Each part of the energy is written as a term of at most two variables: two assignments with disparity $\alpha$ never share a pixel, and two old assignments do not either, so a pixel can only be claimed by one old and one new assignment. Every pair term is regular, so one minimum cut gives a minimizer. The current configuration is in the move space and has finite energy, so the minimizer never pays the stand-in for $\infty$ and is unique, and its energy is the least in the move space. The energy falls with each accepted move, so the method stops, at a configuration that no expansion move improves.

## Complexity

The model is the real RAM. Let $n = W H$.

- **One move.** There are at most $n$ old assignments, one per left pixel, and at most $n$ assignments of disparity $\alpha$. The graph has $O(n)$ nodes and $O(n)$ edges, and building it costs $O(n)$. Then one max flow costs $F$; with the [Boykov-Kolmogorov algorithm](/boykov-kolmogorov-max-flow/) this is fast in practice on such grids, although its worst case bound is not polynomial in $n$ alone.
- **All moves.** A cycle has $D$ moves, so the total is $O(k D (F + n))$. With integer costs, $k \le 2 K n + 1$, because $E(\emptyset) = 2 K n$ and each cycle except the last lowers $E$ by at least 1. In practice a few cycles suffice; this is an observation.
- **Space.** $O(n)$ for the configuration and the graph of one move.

The reference code builds each move over all assignments, which costs $O(n D)$ per move, and uses Edmonds-Karp for the cut.

## Properties

- **Symmetric occlusions.** Both images are treated alike: uniqueness holds in both, and occluded pixels in either image are part of the result.
- **No ordering constraint.** Unlike [dynamic programming stereo](/scanline-dynamic-programming-stereo/), matches need not keep their order, so thin objects can be matched.
- **Local minimum.** The result is optimal only for single expansion moves, and the factor $2c$ of [alpha-expansion](/alpha-expansion/) does not apply to this energy as it stands.
- **Depends on the order.** The order of the disparities and the start can change the result.
- **Edges follow intensity.** The smoothness weight is larger where the image is uniform, so depth edges tend to line up with intensity edges.

## Variants and improvements

- **Labels instead of assignments.** Give each pixel a disparity, use a Potts or truncated linear smoothness term and run [alpha-expansion](/alpha-expansion/) or [alpha-beta swap](/alpha-beta-swap/), as in Boykov, Veksler and Zabih (2001). This is simpler but has no symmetric occlusion model.
- **Exact convex models.** For a convex smoothness term on ordered disparities, Ishikawa (2003) finds the global minimum with one minimum cut on a graph with a layer per disparity; Roy and Cox (1998) gave an earlier max-flow formulation of stereo of this kind. Convex terms smooth depth edges too much.
- **Choice of $K$ and $\lambda$.** The IPOL version sets $\lambda = K / 5$ by default and chooses $K$ by a heuristic from the data costs (its Section 4.2).
- **Several cameras.** The same idea extends to more than two views, with visibility terms.

## When to use it

Use it when accuracy at occlusion boundaries matters more than speed, for example for offline reconstruction or to produce reference results. For real time use, take [semi-global matching](/semi-global-matching/). When you only need disparity labels with a smoothness term and no occlusion model, plain alpha-expansion on labels is simpler.

## Pitfalls

- **Wrong encoding of a move.** If old and new assignments use the same meaning of $x$, the uniqueness and occlusion terms are not regular and the cut is wrong. Old assignments must use $x = 0$ for "kept", new ones $x = 1$ for "on".
- **Infinite capacities.** Use a finite number larger than any finite energy for $\infty$, and make sure the current configuration is a valid point of the move, so the minimum is finite.
- **Accepting worse moves.** Accept a move only if the energy drops; with ties the method may cycle.
- **Balance of $K$ and $\lambda$.** A small $K$ gives large occluded areas; a large $K$ forces matches in true occlusions. Scale both with the data cost and its cap.
- **Large disparity ranges.** Each cycle costs one cut per disparity, so the time grows with $D$; restrict the range or work coarse to fine.

## Implementations

## History

Roy and Cox (1998) solved stereo over a whole image with one maximum flow. Boykov, Veksler and Zabih (2001) introduced swap and expansion moves and used them for stereo with disparity labels, and Ishikawa (2003) gave an exact cut for convex priors. Kolmogorov and Zabih (2001) moved the variables from pixels to assignments, which allowed a symmetric model of occlusion with uniqueness, and showed that each expansion move of this energy is a minimum cut. Their later paper of 2004 gave the general condition, regularity, under which such moves are cuts. Kolmogorov, Monasse and Tan (2014) published a detailed description and a reference implementation in IPOL.

## References
