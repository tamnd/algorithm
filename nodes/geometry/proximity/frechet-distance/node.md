---
tag: Y4D31R
kind: problem
slug: frechet-distance
name: Fréchet distance
aliases:
- dog-leash distance
- discrete Frechet distance
- Frechet distance
- coupling distance
area: geometry/proximity
level: advanced
summary: Compute the minimum leash length needed for two monotone walks along two polygonal curves.
prereqs: [hausdorff-distance, point-to-segment-distance, euclidean-distance]
see_also: [alt-godau-algorithm, edit-distance, edit-distance-hardness, longest-common-subsequence, curve-simplification, strong-exponential-time-hypothesis, orthogonal-vectors-hypothesis, conditional-lower-bound]
sources:
  - paper: doi:10.1142/S0218195995000064
    title: Helmut Alt and Michael Godau, Computing the Fréchet distance between two polygonal curves, International Journal of Computational Geometry and Applications 5(1-2), 1995, 75-91
    locator: the definition for polygonal curves, the free-space diagram, the O(mn) decision procedure, the O(mn log(mn)) algorithm, and the weak Fréchet distance
  - paper: "Thomas Eiter and Heikki Mannila, Computing discrete Fréchet distance, Technical Report CD-TR 94/64, Christian Doppler Laboratory for Expert Systems, TU Vienna, 1994"
    locator: the discrete Fréchet distance, the O(mn) dynamic program, and the bound relating it to the continuous distance
  - paper: "Karl Bringmann, Why walking the dog takes time, Fréchet distance has no strongly subquadratic algorithms unless SETH fails, Proceedings of the 55th Annual IEEE Symposium on Foundations of Computer Science, 2014, 661-670"
    locator: the reduction from orthogonal vectors, for the continuous and the discrete distance and for small approximation factors
  - paper: "Pankaj K. Agarwal, Rinat Ben Avraham, Haim Kaplan and Micha Sharir, Computing the discrete Fréchet distance in subquadratic time, SIAM Journal on Computing 43(2), 2014, 429-449"
    locator: the O(mn log log n / log n) algorithm for the discrete distance on the word RAM
  - paper: "Kevin Buchin, Maike Buchin, Wouter Meulemans and Wolfgang Mulzer, Four Soviets walk the dog, improved bounds for computing the Fréchet distance, Discrete and Computational Geometry 58(1), 2017, 180-216"
    locator: the first algorithm for the continuous distance faster than O(n^2 log n) on the real RAM
  - paper: "Anne Driemel, Sariel Har-Peled and Carola Wenk, Approximating the Fréchet distance for realistic curves in near linear time, Discrete and Computational Geometry 48(1), 2012, 94-127"
    locator: (1 + epsilon)-approximation for c-packed curves in near-linear time
---

The Fréchet distance measures how far apart two curves are when both are traversed from start to end without going back. A person walks along curve $P$ and a dog along curve $Q$, each at any speed, possibly stopping, but never backwards; the Fréchet distance is the shortest leash that makes this possible. Unlike the [Hausdorff distance](/hausdorff-distance/), which only compares the sets of points, it respects the order along the curves, so it tells a path from the same path walked back and forth. For polygonal curves with $m$ and $n$ segments, the [Alt-Godau algorithm](/alt-godau-algorithm/) (1995) decides $d_F \le \varepsilon$ in $O(mn)$ time and computes $d_F$ in $O(mn \log(mn))$ time. The discrete variant, which only matches vertices, has an $O(mn)$ dynamic program (Eiter and Mannila, 1994). Bringmann (2014) showed that neither version has an $O(n^{2 - \delta})$ algorithm unless the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) fails.

## In plain words

Two people walk two routes from start to finish. Each may walk fast, slowly, or wait, but never turn back. How short can a rope between them be so that it never has to stretch further during the walk?

That shortest rope length is the Fréchet distance. It is small only if the two routes are close and also go through their parts in the same order. A route that runs right, back left and right again is far from a route that simply runs right once, even though both cover the same ground.

In the discrete version the walkers hop from stop to stop on their routes, and only the stops are compared. That version is easier to compute but can give a larger answer.

## Definition

**Curves.** A polygonal curve $P = (P_0, \ldots, P_m)$ is the map $P : [0, m] \to \mathbb{R}^d$ that is linear on each $[i, i+1]$ with $P(i) = P_i$.

**Continuous Fréchet distance.**
$$d_F(P, Q) = \inf_{\alpha, \beta} \max_{u \in [0, 1]} \|P(\alpha(u)) - Q(\beta(u))\|,$$
where $\alpha : [0, 1] \to [0, m]$ and $\beta : [0, 1] \to [0, n]$ are continuous, nondecreasing and onto. For polygonal curves the infimum is attained. It is a pseudometric on curves: two curves at distance $0$ are reparametrizations of each other.

**Discrete Fréchet distance.** A coupling is a sequence of index pairs $(i_1, j_1) = (0, 0), \ldots, (i_k, j_k) = (m, n)$ in which each step increases $i$, $j$ or both by one. Then
$$d_{dF}(P, Q) = \min_{\text{couplings}} \max_r \|P_{i_r} - Q_{j_r}\|.$$
It satisfies the recurrence $D(i, j) = \max(\|P_i - Q_j\|, \min(D(i-1, j), D(i, j-1), D(i-1, j-1)))$, computed in $O(mn)$ time with no square roots if squared distances are stored.

**Order of the distances.** For polygonal curves,
$$d_H(P, Q) \le d_{wF}(P, Q) \le d_F(P, Q) \le d_{dF}(P, Q) \le d_F(P, Q) + \max(\lambda_P, \lambda_Q),$$
where $d_H$ is the Hausdorff distance of the point sets, $d_{wF}$ the weak Fréchet distance below, and $\lambda_P$, $\lambda_Q$ the longest segment lengths. The first two inequalities hold because a pair of walks covers every point of both curves and a monotone pair is a special pair; the third because a coupling, filled in by walking each segment at constant speed during a step, is a monotone pair whose leash is largest at the vertices, by convexity of the distance; the last is from Eiter and Mannila.

**Decision version.** Given $\varepsilon$, decide whether $d_F(P, Q) \le \varepsilon$. With integer coordinates and rational $\varepsilon^2$ all tests are exact; see the [Alt-Godau algorithm](/alt-godau-algorithm/).

## Variants

- **Weak Fréchet distance.** The walks may go back: $\alpha$ and $\beta$ need only be continuous and onto, with the right endpoints. The decision is connectivity in the free-space diagram, $O(mn)$ time (Alt and Godau).
- **Discrete Fréchet distance.** Vertices only, as defined above.
- **Closed curves.** The start points are free as well; Alt and Godau also handle this case.
- **Partial matching.** Find a subcurve of $Q$ closest to $P$, as in map matching of a trajectory onto a road network.
- **Fréchet distance with shortcuts, geodesic and homotopic versions.** The walks may skip parts of a curve, the leash is measured inside a polygon, or the leash must move continuously in a domain with obstacles.
- **Surfaces.** Defined with homeomorphisms between surfaces; computing it is NP-hard in general (Godau).

## Examples

**Back and forth.** Let $P = ((0,0), (4,0))$ and $Q = ((0,0), (4,0), (0,0), (4,0))$. Both cover the segment from $(0,0)$ to $(4,0)$, so $d_H = 0$. The weak distance is also $0$: the person walks right, back and right again together with the dog. With monotone walks, while the dog runs from $(4,0)$ back to $(0,0)$ the person must stand somewhere, and the best place is the middle $(2,0)$, so $d_F = 2$. The discrete dynamic program on squared distances gives

| $D(i, j)$ | $Q_0 = (0,0)$ | $Q_1 = (4,0)$ | $Q_2 = (0,0)$ | $Q_3 = (4,0)$ |
| --- | --- | --- | --- | --- |
| $P_0 = (0,0)$ | 0 | 16 | 16 | 16 |
| $P_1 = (4,0)$ | 16 | 0 | 16 | 16 |

so $d_{dF} = 4$: some vertex of $P$ must be matched with a vertex at distance 4. The four distances are $0 \le 0 \le 2 \le 4$, and $4 \le 2 + 4$ as the last inequality allows.

**Parallel segments in opposite directions.** For $P = ((0,0), (6,0))$ and $Q = ((6,1), (0,1))$ the start points must be matched, so $d_F \ge \sqrt{37}$, and $d_F = \sqrt{37}$ because both walks can run at the same speed. The Hausdorff distance is $1$.

**A float trap.** For $A = (0, 0)$, $B = (10^8, 1)$ and $C = (-10^8, 0)$, the squared distances $\|A - B\|^2 = 10^{16} + 1$ and $\|A - C\|^2 = 10^{16}$ differ, but their square roots round to the same double. A program that compares leash lengths after `sqrt` reports a tie that is not there; comparing squared lengths in integers does not.

## Known algorithms

| method | problem | time | model |
| --- | --- | --- | --- |
| dynamic program (Eiter and Mannila, 1994) | discrete | $O(mn)$ | real RAM, integers suffice |
| free-space diagram (Alt and Godau, 1995) | continuous, decision | $O(mn)$ | real RAM |
| [Alt-Godau algorithm](/alt-godau-algorithm/) with sorting of critical values | continuous | $O((m^2 n + mn^2) \log(mn))$ | real RAM |
| Alt-Godau with [parametric search](/parametric-search/) | continuous | $O(mn \log(mn))$ | real RAM |
| randomized search over critical values (Har-Peled and Raichel, 2014) | continuous | $O(mn \log(mn))$ expected | real RAM |
| Agarwal, Ben Avraham, Kaplan and Sharir (2014) | discrete | $O(mn \log \log n / \log n)$ | word RAM |
| Buchin, Buchin, Meulemans and Mulzer (2017) | continuous, $m = n$ | $O(n^2 \sqrt{\log n} (\log \log n)^{3/2})$ | real RAM |
| Driemel, Har-Peled and Wenk (2012) | $(1 + \varepsilon)$-approximation for $c$-packed curves | $O(cn/\varepsilon + cn \log n)$ | real RAM |

## Bounds

- **Upper bound.** Quadratic up to logarithmic factors for both versions, and slightly below $n^2 \log n$ for the continuous one.
- **Conditional lower bound.** Bringmann (2014) showed that for any $\delta > 0$ an $O(n^{2 - \delta})$ algorithm for the continuous or the discrete Fréchet distance of two planar curves with $n$ vertices would refute the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/). The bound also holds for approximation within a small constant factor (1.001 in the paper). This is a [conditional lower bound](/conditional-lower-bound/) through the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/).
- **Unbalanced inputs.** The same reduction rules out $O((mn)^{1 - \delta})$ time for curves of very different sizes, under the same hypothesis.
- **Algebraic lower bound.** The continuous decision problem needs $\Omega(n \log n)$ time in the algebraic decision tree model (Buchin, Buchin, Knauer, Rote and Wenk, 2007).

## Reductions

- **Orthogonal vectors to Fréchet distance.** Bringmann encodes each vector of one set as a short gadget curve in $P$ and each vector of the other set as one in $Q$, so that the leash fits exactly when some pair of vectors is orthogonal; a strongly subquadratic Fréchet algorithm would give a strongly subquadratic orthogonal vectors algorithm.
- **Optimization to decision.** The distance is one of $O(m^2 n + mn^2)$ critical values, so a search with the decision procedure computes it; parametric search avoids listing them.
- **Relation to sequence alignment.** The discrete dynamic program has the same grid shape as [edit distance](/edit-distance/) and [longest common subsequence](/longest-common-subsequence/), with $(\max, \min)$ in place of $(+, \min)$. Replacing the maximum along the coupling by a sum gives dynamic time warping. All of these share quadratic SETH lower bounds; see [edit distance hardness](/edit-distance-hardness/).
- **Hausdorff distance as a lower bound.** $d_H$ is computable in $O((m + n) \log(m + n))$ time in the plane and bounds $d_F$ from below, a cheap filter before an exact computation.

## Applications

- **Trajectory analysis.** Comparing and clustering GPS tracks of vehicles, animals or athletes, and matching a track to a road network (map matching).
- **Curve simplification.** Simplifying a polygonal curve so that the result stays within a given Fréchet distance of the original preserves its shape and order; see [curve simplification](/curve-simplification/) and [polygon simplification](/polygon-simplification/).
- **Handwriting and gesture recognition.** Strokes are compared as ordered curves.
- **Structural biology.** The discrete version aligns protein backbones, where the order of residues matters.
- **Shape matching.** Comparing outlines and contours when the Hausdorff distance ignores the order of points.

## References
