---
tag: PEAR14
kind: problem
slug: image-segmentation-graph-cuts
name: Image segmentation via graph cuts
aliases:
- graph cut segmentation
area: graphs/flows-and-cuts
level: advanced
summary: Label pixels by minimizing an energy with unary and pairwise terms via a min-cut.
prereqs: [min-cut-problem, max-flow-min-cut-theorem, energy-function]
see_also: [image-segmentation, markov-random-field, potts-model, grabcut, submodular-function, map-inference, normalized-cut, maximum-weight-closure]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.10, Image Segmentation (likelihoods, separation penalties and the reduction to a minimum cut)
  - paper: doi:10.1111/j.2517-6161.1989.tb01764.x
    title: D. M. Greig, B. T. Porteous and A. H. Seheult, Exact maximum a posteriori estimation for binary images, Journal of the Royal Statistical Society, Series B 51(2), 271 to 279 (1989)
    locator: the whole paper (exact MAP for the binary Ising prior by a minimum cut)
  - paper: doi:10.1109/ICCV.2001.937505
    title: Yuri Y. Boykov and Marie-Pierre Jolly, Interactive graph cuts for optimal boundary and region segmentation of objects in N-D images, ICCV 2001, 105 to 112
    locator: the whole paper (the graph with terminal and neighbourhood links and hard seed constraints)
  - paper: doi:10.1109/TPAMI.2004.1262177
    title: Vladimir Kolmogorov and Ramin Zabih, What energy functions can be minimized via graph cuts?, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(2), 147 to 159 (2004)
    locator: the regularity (submodularity) condition for pairwise binary energies
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 1222 to 1239 (2001)
    locator: the expansion move algorithm and its factor 2 bound for the Potts model
---

Graph cut segmentation splits the pixels of an image into foreground and background by minimizing an [energy](/energy-function/) that adds a cost for each pixel's label and a penalty for each pair of neighbouring pixels with different labels. For two labels and nonnegative pair penalties, the energy of each labelling equals the capacity of an s-t cut in a network with one vertex per pixel, so one [minimum cut](/min-cut-problem/) gives an exact minimizer. This is exact MAP inference in a binary [Markov random field](/markov-random-field/) with an Ising or [Potts](/potts-model/) prior. It underlies interactive tools such as [GrabCut](/grabcut/), and with more than two labels it is the inner step of move-making algorithms.

## In plain words

Each pixel must be called object or background. Looking at a pixel alone, its colour makes one answer more likely, and each wrong-looking choice has a cost. Neighbouring pixels usually belong together, so each pair of neighbours with different answers adds a penalty. We want the labelling with the smallest total cost.

Build a network with a source for object, a sink for background, and one point per pixel. A pipe from the source to a pixel holds the cost of calling it background, a pipe from the pixel to the sink holds the cost of calling it object, and pipes between neighbours hold the penalty. Any way of cutting source from sink is a labelling, and the cheapest cut is the best labelling.

## Definition

**Input.** A set $P$ of pixels, a neighbourhood system $\mathcal N$ of unordered pairs (for example the 4-neighbours of a grid), and real numbers

- $D_p(1) \ge 0$ and $D_p(0) \ge 0$: the cost of labelling $p$ foreground or background,
- $w_{pq} \ge 0$ for $\{p, q\} \in \mathcal N$: the penalty for giving $p$ and $q$ different labels.

Costs are real; a common choice is negative log-likelihoods of colour models, $D_p(\ell) = -\log \Pr(I_p \mid \ell)$, shifted to be nonnegative, and $w_{pq}$ decreasing in the contrast $|I_p - I_q|$.

**Output.** A labelling $x \in \{0, 1\}^P$ minimizing

$$E(x) = \sum_{p \in P} D_p(x_p) + \sum_{\{p, q\} \in \mathcal N} w_{pq} [x_p \ne x_q].$$

**The network.** The graph is directed with vertices $P \cup \{s, t\}$ and, for each pixel $p$, an arc $s \to p$ of capacity $D_p(0)$ and an arc $p \to t$ of capacity $D_p(1)$; for each pair $\{p, q\} \in \mathcal N$, two antiparallel arcs $p \to q$ and $q \to p$, each of capacity $w_{pq}$. A labelling $x$ corresponds to the cut with source side $S = \{s\} \cup \{p : x_p = 1\}$. The cut pays $D_p(0)$ for each $p$ on the sink side (label 0), $D_p(1)$ for each $p$ on the source side (label 1), and $w_{pq}$ once for each pair with different labels, through whichever of the two antiparallel arcs leaves $S$. So $c(S) = E(x)$, and a minimum cut gives a minimum energy labelling. The two antiparallel arcs of a pair are kept as separate arcs with separate flows; merging them into one arc of capacity $2 w_{pq}$, or into one arc only, would charge the penalty wrongly.

**Edge cases.** An arc of capacity 0, for instance $s \to p$ when $D_p(0) = 0$, is the same as no arc and never appears in a residual graph. If no arc enters $t$ at all (all $D_p(1) = 0$), there is no s-t path, the maximum flow is 0, and labelling everything foreground costs 0, which is optimal since all costs are nonnegative.

## Variants

- **Hard constraints (seeds).** A user marks some pixels as object or background; give $s \to p$ or $p \to t$ an infinite capacity. This is the interactive method of Boykov and Jolly.
- **Pairwise energies of general form.** A binary energy $\sum_p \theta_p(x_p) + \sum_{pq} \theta_{pq}(x_p, x_q)$ reduces to a minimum cut exactly when every pair term is submodular, $\theta_{pq}(0,0) + \theta_{pq}(1,1) \le \theta_{pq}(0,1) + \theta_{pq}(1,0)$ (Kolmogorov and Zabih). Negative unary costs are handled by adding a constant to both $D_p(0)$ and $D_p(1)$.
- **More than two labels.** For the [Potts model](/potts-model/) with three or more labels, exact minimization is NP-hard. The expansion move algorithm solves a binary graph cut problem per label in each sweep and reaches a local minimum within a factor 2 of the optimum; swap moves handle more general metrics. For convex pair terms on ordered labels, Ishikawa's construction gives an exact minimum cut.
- **Iterated models.** [GrabCut](/grabcut/) alternates between fitting colour models and a graph cut.
- **Higher-order and non-submodular terms** need other methods, such as QPBO, which labels part of the pixels optimally.
- **Spectral segmentation.** [Normalized cut](/normalized-cut/) uses a different objective, balanced by segment size, and is NP-hard; it is approximated by eigenvectors, not solved by maximum flow.

## Examples

**A strip of five pixels.** Pixels $p_1, \dots, p_5$ in a row, with neighbours $p_i p_{i+1}$ and costs:

| pixel | $p_1$ | $p_2$ | $p_3$ | $p_4$ | $p_5$ |
|---|---|---|---|---|---|
| $D_p(1)$, foreground | 0 | 1 | 3 | 1 | 5 |
| $D_p(0)$, background | 5 | 4 | 2 | 4 | 0 |

Pixel $p_3$ alone slightly prefers background, as a noisy pixel inside an object would.

- With $w = 0$ the pixels are independent: $x = (1, 1, 0, 1, 0)$ with energy $0 + 1 + 2 + 1 + 0 = 4$.
- With $w = 2$ on every pair, the minimum is $x = (1, 1, 1, 1, 0)$ with energy $0 + 1 + 3 + 1 + 0 + 2 = 7$; the independent labelling now costs $4 + 3 \cdot 2 = 10$. The minimum cut has source side $\{s, p_1, p_2, p_3, p_4\}$ and cuts the arcs $p_1 t$, $p_2 t$, $p_3 t$, $p_4 t$ of capacities $0, 1, 3, 1$ and the arc $p_4 p_5$ of capacity 2; the arc $s p_5$ has capacity 0 and costs nothing. The noisy pixel is smoothed over.
- With $w = 10$ the penalty dominates and the minimum is all foreground, energy $0 + 1 + 3 + 1 + 5 = 10$.

A maximum flow algorithm gives values 4, 7 and 10 in the three cases, matching a brute force over all 32 labellings.

**A grid.** On an image the pixels form a grid with 4 or 8 neighbours, so the network has about $n$ vertices and $3n$ or $5n$ edges for $n$ pixels, and the method scales to images with millions of pixels.

## Known algorithms

- **Any maximum flow algorithm** on the network: [push-relabel](/push-relabel/), [Dinic](/dinic/), or the almost-linear algorithm in theory.
- **Boykov-Kolmogorov.** An augmenting path method that grows search trees from $s$ and $t$ and reuses them between augmentations. Its worst case bound is weak, but on grid graphs from vision it is usually the fastest in practice, and it is the standard tool in vision libraries.
- **Grid-specific parallel methods.** Push-relabel parallelizes well on GPUs because each pixel talks only to its neighbours.
- **Dynamic graph cuts.** When the costs change a little between frames or iterations, reusing the previous flow (Kohli and Torr) saves most of the work.

## Bounds

The problem with two labels and submodular pair terms is a minimum cut on a graph with $O(|P|)$ vertices and $O(|P| + |\mathcal N|)$ edges, so it costs one maximum flow. The Potts model with $k \ge 3$ labels is NP-hard, and the expansion algorithm is a 2-approximation. Non-submodular binary energies include maximum cut and are NP-hard in general.

## Reductions

- **To minimum s-t cut**, as above.
- **From [maximum weight closure](/maximum-weight-closure/).** Both are instances of minimizing a sum of unary terms and submodular pairwise terms over binary variables, which is exactly the class of energies representable by s-t cuts.
- **From MAP inference.** The minimum energy labelling is the MAP estimate in a binary [Markov random field](/markov-random-field/) with an [Ising](/ising-model/) prior, as observed by Greig, Porteous and Seheult.

## Applications

Interactive object selection in photo editors, medical image segmentation in 2D and 3D, stereo correspondence, image restoration and denoising, texture synthesis and image stitching along seams of least cost, and video segmentation with links between frames.

## References
