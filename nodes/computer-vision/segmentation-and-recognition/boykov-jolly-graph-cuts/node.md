---
tag: DCZHC7
kind: algorithm
slug: boykov-jolly-graph-cuts
name: Boykov-Jolly interactive graph cuts
aliases:
- interactive graph cut segmentation
area: computer-vision/segmentation-and-recognition
level: core
summary: "Segment an object from user seeds by a minimum s-t cut. Seeds are hard constraints, and new seeds reuse the old flow, so each correction gives a new global optimum fast."
solves: [interactive-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {worst: O(W^3 H^3), average: O(W^3 H^3), best: O(W H)}
  space: {extra: O(W H)}
properties: {deterministic: true, exact: true, global_optimum: true, binary_labels: true, interactive: true}
history:
  year: 2001
  people: [Yuri Boykov, Marie-Pierre Jolly]
  note: Boykov and Jolly (ICCV 2001) used user seeds as hard constraints in a minimum cut segmentation and reused the flow when the user adds seeds.
prereqs: [interactive-segmentation, image-segmentation-graph-cuts, max-flow-min-cut-theorem]
see_also: [grabcut, edmonds-karp, boykov-kolmogorov-max-flow, graph-representable-energies, intelligent-scissors, random-walker-segmentation, alpha-expansion, markov-random-field]
sources:
  - paper: doi:10.1109/ICCV.2001.937505
    title: "Yuri Y. Boykov and Marie-Pierre Jolly, Interactive graph cuts for optimal boundary and region segmentation of objects in N-D images, ICCV 2001, vol. I, 105-112"
    locator: "Section 2 (energy with hard constraints, equations 1 to 5), Section 3 (graph, Lemma 1 and Theorem 1, the update for new seeds), Section 4 (examples)"
  - paper: doi:10.1109/TPAMI.2004.60
    title: "Yuri Boykov and Vladimir Kolmogorov, An experimental comparison of min-cut/max-flow algorithms for energy minimization in vision, IEEE TPAMI 26(9), 1124-1137, 2004"
    locator: "The augmenting path algorithm used for the max flow, and its timings on vision graphs"
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 5.5, Graph cuts and energy-based methods"
---

Boykov-Jolly interactive graph cuts is an algorithm that cuts one object out of an image, or out of a 3D volume, from pixels that the user marks as object or background. These marks, the *seeds*, are hard constraints. Among all labelings that obey them, a minimum cut of one graph finds a labeling of least energy, where the energy adds a region term (how well each pixel fits the object or the background) and a boundary term (a cost for cutting between similar neighbors). When the user adds seeds, the algorithm continues from the old maximum flow instead of starting again. This page covers the hard constraints, the constant $K$ and the interactive loop. The general energy-to-cut construction is on [image segmentation via graph cuts](/image-segmentation-graph-cuts/), and the method that refits color models in a loop is [GrabCut](/grabcut/).

## In plain words

The user paints a few strokes on the object and a few on the background. The program learns the typical brightness of each from the strokes. Then it looks for the best split of the image into two parts. A good split puts each pixel with the side it looks like, and it runs along strong edges, where neighbor pixels differ a lot. The program never moves a painted pixel to the wrong side.

The best split is found exactly, by a classic method for networks of pipes. Pipes join neighbor pixels and join each pixel to an object tap and a background drain. The weakest set of pipes that stops all flow is the best split.

If the result is wrong somewhere, the user paints one more stroke there. The program keeps the old flow and only adds what the new stroke changes, so the answer comes back fast.

## The problem

The input is an image $I$ with the pixel set $P$, $n = WH$ pixels in 2D, a neighbor system $\mathcal N$ (8 neighbors in 2D and 26 in 3D in the paper), the object seeds $O \subset P$ and the background seeds $G \subset P$ with $O \cap G = \emptyset$, and a weight $\lambda \ge 0$. A labeling $A$ gives each pixel $A_p = 1$ (object) or $A_p = 0$ (background). The energy is (Boykov and Jolly 2001, equations 1 to 3)
$$E(A) = \lambda \sum_{p \in P} R_p(A_p) + \sum_{\{p, q\} \in \mathcal N} B_{pq}\, [A_p \ne A_q],$$
with the hard constraints (equations 4 and 5)
$$A_p = 1 \text{ for } p \in O, \qquad A_p = 0 \text{ for } p \in G.$$
The output is a labeling that satisfies the constraints and has the least energy among those that do. The paper writes "obj" and "bkg" for the labels 1 and 0 and $\mathcal B$ for the background seeds; this page uses $G$ to keep $B$ for the boundary term.

The region term in the paper is $R_p(1) = -\ln \Pr(I_p \mid O)$ and $R_p(0) = -\ln \Pr(I_p \mid G)$, from intensity histograms of the seeds. The boundary term is
$$B_{pq} = \frac{1}{\operatorname{dist}(p, q)} \exp\Bigl(-\frac{(I_p - I_q)^2}{2 \sigma^2}\Bigr),$$
with $\sigma$ set like the camera noise. Boykov and Jolly call this term ad hoc: it is a modeling choice, not derived from a model of the image. The method needs only $B_{pq} \ge 0$, so other region and boundary terms work too.

## The algorithm

The first block is the segmentation from the first seeds. The second block is the update when the user adds an object seed at a pixel $p$; a background seed is the mirror case. $S$ is the object terminal and $T$ the background terminal.

```pseudo id=main
BOYKOV-JOLLY(I, O, G, λ, σ)
L1  R_p(1) ← -ln Pr(I_p | histogram of O),  R_p(0) ← -ln Pr(I_p | histogram of G)
L2  for each pair {p, q} in N do B_pq ← exp(-(I_p - I_q)² / (2σ²)) / dist(p, q)
L3  K ← 1 + max_p Σ_q B_pq
L4  make nodes P ∪ {S, T}; for each pair {p, q} add arcs p → q and q → p of capacity B_pq
L5  for each p in O do c(S, p) ← K, c(p, T) ← 0
L6  for each p in G do c(S, p) ← 0, c(p, T) ← K
L7  for each other p do c(S, p) ← λ R_p(0), c(p, T) ← λ R_p(1)
L8  f ← a maximum flow from S to T
L9  A_p ← 1 if p is reachable from S in the residual graph of f, else 0
L10 return A
```

```pseudo id=add-seed
ADD-OBJECT-SEED(p)            ▷ p is a free pixel; f is the current flow
L11 c_p ← λ (R_p(1) + R_p(0))
L12 c(S, p) ← K + c_p,  c(p, T) ← c_p        ▷ both capacities grow
L13 continue the max flow from f, then relabel as in L9 and L10
```

The constant $K$ is larger than the total boundary weight at any pixel. A cut through a seed's $K$ arc always costs more than any change of that pixel's boundary terms, so a minimum cut never puts a seed on the wrong side. Line L12 is the hard constraint $(K, 0)$ with $c_p$ added to both terminal arcs. Every cut contains exactly one of the two arcs, so the shift adds the same $c_p$ to every cut. The shift makes both capacities at least their old values, so the old flow is still feasible and line L13 only adds flow.

## Example

Take one row of 5 pixels with the gray values $20, 40, 140, 200, 220$, the object seed $O = \{4\}$, the background seed $G = \{0\}$, $\lambda = 1$ and $\sigma = 30$. The histograms have 4 bins of width 64 with add-one smoothing, so a value in the bin of the seed has probability $2/5$ and other values have $1/5$:

| pixel | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| value | 20 | 40 | 140 | 200 | 220 |
| $R_p(1)$ | 1.6094 | 1.6094 | 1.6094 | 0.9163 | 0.9163 |
| $R_p(0)$ | 0.9163 | 0.9163 | 1.6094 | 1.6094 | 1.6094 |

The boundary weights of the pairs (0,1), (1,2), (2,3), (3,4) are $0.8007$, $0.0039$, $0.1353$, $0.8007$, and $K = 1 + 0.1353 + 0.8007 = 1.9361$. Pixel 2 has equal region costs, so the boundary term decides. A cut between pixels 1 and 2 costs $0.0039$, and a cut between 2 and 3 costs $0.1353$. The maximum flow is $3.4459$, and the labels are $0, 0, 1, 1, 1$. Theorem 1 of the correctness section says that the flow is the energy minus the region terms of the seeds: $E = 5.2785$, and the seeds add $0.9163 + 0.9163 = 1.8326$.

The user now says that pixel 2 is background. Line L11 gives $c_2 = 3.2189$. Line L12 raises $c(S, 2)$ from $1.6094$ to $3.2189$ and $c(2, T)$ from $1.6094$ to $K + c_2 = 5.1550$. Line L13 pushes more flow, up to $5.1868$, and the new labels are $0, 0, 0, 1, 1$. The flow minus the shift, $5.1868 - 3.2189 = 1.9679$, equals the maximum flow of a new graph built from zero with the seeds $\{4\}$ and $\{0, 2\}$. Brute force over the labelings of the free pixels gives the same labels. The test file checks these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The facts that are proved, for $\lambda \ge 0$, $R_p \ge 0$ and $B_{pq} \ge 0$:
- **Lemma (feasibility).** A minimum cut never cuts a $K$ arc of a seed, because moving the seed to its own side saves $K$ and costs less than $K$. This is Lemma 1 of the paper.
- **Theorem (optimality).** For each labeling $A$ that obeys the seeds, the cut that puts the object pixels on the side of $S$ costs $E(A)$ minus the region terms of the seeds, a constant. So a minimum cut gives a minimum of $E$ under the hard constraints. This is Theorem 1 of the paper. Negative region costs are handled by adding a constant to both terms of a pixel.
- The reachable set from $S$ in the residual graph of a maximum flow is a minimum cut ([max-flow min-cut theorem](/max-flow-min-cut-theorem/)).
- **Flow reuse.** After line L12 all capacities are at least the old ones, so the old flow is feasible. The shift $c_p$ adds the same constant to every cut, so the minimum cut does not change. Continuing the max flow from the old flow gives the new optimum.

What is not proved: that the minimum energy labeling is the object the user has in mind. With few seeds, a short cut around a seed can win. That is a property of the energy, not of the algorithm.

## Complexity

The graph has $V = WH + 2$ nodes. With 8 neighbors it has about $4WH$ neighbor pairs, so $E = O(WH)$ arcs in all. The cost model is the [real-RAM](/real-ram/): the capacities are real numbers. Lines L1 to L7 cost $O(WH)$ time, plus the number of histogram bins. The max flow of line L8 dominates. With [Edmonds-Karp](/edmonds-karp/), as in the code of this page, it costs $O(V E^2) = O(W^3 H^3)$ time in the worst case. [Push-relabel](/push-relabel/) has the bound $O(V^3)$, the same order here. The paper uses the augmenting path algorithm of Boykov and Kolmogorov (2004). Its worst case bound depends on the cost of the minimum cut, so it is not strongly polynomial, but on 2D grids it was faster than the other methods in their tests. That is a benchmark result on their graphs, not a bound.

After a new seed, line L13 starts from the old flow. The worst case bound is the same, but only the flow that the new seed changes must be found. Boykov and Jolly report that the update is fast in practice; that is a measurement. The extra space is $O(WH)$ for the graph and the flow. The front matter gives the bound of the code. The best case $O(WH)$ is a graph where one search finds no augmenting path.

## Properties

- **Global optimum for two labels.** The result is an exact minimum of the energy under the seeds, not a local one, unlike [active contours](/active-contours/).
- **Hard constraints.** Seeds always keep their labels, so the user has direct control.
- **Any dimension.** Only the neighbor system changes from 2D to 3D, as in the medical volumes of the paper.
- **Topology is free.** The object can have holes and several parts. Each part does not need a seed.
- **Shrinking bias.** The boundary term adds up along the cut, so short boundaries are cheaper. Thin parts of an object can be cut off.
- **Binary.** The exact result is for two labels. With more labels the [Potts](/potts-model/) energy is NP-hard, and methods such as [alpha-expansion](/alpha-expansion/) give approximations.

## Variants and improvements

- **GrabCut** (Rother, Kolmogorov and Blake 2004) replaces the seeds by a box, the histograms by color Gaussian mixtures, and refits the mixtures between cuts. See [GrabCut](/grabcut/).
- **Lazy Snapping** (Li, Sun, Tang and Shum 2004) runs the cut on presegmented regions instead of pixels, which makes the graph small enough for very fast interaction.
- **Other boundary terms.** The term can use color, gradients in 3D, or a metric that approximates a geometric length when the neighbor system is large enough.
- **Other max flow methods.** Push-relabel, or the Boykov-Kolmogorov method, in the [Boykov-Kolmogorov max flow](/boykov-kolmogorov-max-flow/) page.
- **Other energies.** The same cut works for every regular pairwise binary energy, see [graph representable energies](/graph-representable-energies/).

## When to use it

Use it to cut out one object when the user can mark a few pixels inside and outside, and when the object differs from the background in brightness or color, or has a clear edge. It suits 3D medical volumes as well as photos. Use [intelligent scissors](/intelligent-scissors/) when the user prefers to trace the boundary, and the [random walker](/random-walker-segmentation/) when there are more than two labels or weak edges, where the shrinking bias of the cut hurts. Use [GrabCut](/grabcut/) when the user gives only a box.

## Pitfalls

- **K must be larger than the boundary weight at any pixel.** A smaller value can let a cut move a seed to the wrong side.
- **Directed terminal arcs.** The arc from $S$ goes to $p$, and the arc to $T$ comes from $p$. Swapping $R_p(0)$ and $R_p(1)$ on them inverts the region term.
- **Empty histogram bins.** A bin with no seed gives $-\ln 0$. Smoothing (add-one in the code) or a floor avoids infinite costs.
- **Histograms from few seeds.** A few strokes give a poor model, and $\lambda$ needs tuning. The paper shows results for several values of $\lambda$.
- **Refitting the histograms.** If the histograms change after a new seed, all terminal capacities change and some can decrease. The old flow may then be infeasible, and the flow reuse of line L13 no longer applies.
- **Floating point.** Capacities are real numbers. Use a small tolerance when the code tests for a residual capacity of zero.

## Implementations

The Python code in `impl/python/boykov_jolly_graph_cuts.py` builds the graph of lines L1 to L7 for a gray image with 4 or 8 neighbors, finds the maximum flow with Edmonds-Karp, and supports adding object or background seeds with flow reuse (lines L11 to L13). The tests compare the labels with brute force over all labelings of the free pixels on images of up to 12 pixels, check the identity of Theorem 1 between the flow and the energy, check that the reused flow equals a flow computed from zero after each new seed, and check the example above.

## History

Greig, Porteous and Seheult (1989) showed that a minimum cut gives the exact maximum a posteriori estimate of a binary image under an Ising prior. For a decade after that, graph cuts in vision were used mostly for stereo and restoration. Boykov and Jolly (2001) turned the cut into an interactive tool: the user's seeds became hard constraints, the region term came from the seeds, and the flow was reused after each correction. They showed results on photos and on medical images, among them a kidney in a 3D MR angiography volume. Boykov and Kolmogorov (2004) published the max flow algorithm that made such cuts fast on image grids. GrabCut and Lazy Snapping followed in 2004.

## References
