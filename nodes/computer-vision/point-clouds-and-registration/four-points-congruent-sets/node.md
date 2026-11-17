---
tag: 2MMXJS
kind: algorithm
slug: four-points-congruent-sets
name: 4-points congruent sets
aliases:
- 4PCS
- Super4PCS
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Global rigid registration that finds coplanar four-point bases in one cloud and their affine-invariant ratio matches in the other, verified like RANSAC."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of points in each cloud, k: the number of candidate sets in a trial, N: the number of trials}
  time: {worst: O(N (n^2 + k n^2)), average: O(N (n^2 + k n)), best: Θ(N n^2)}
  space: {extra: O(n^2 + k)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Dror Aiger, Niloy J. Mitra, Daniel Cohen-Or]
  note: "Aiger, Mitra and Cohen-Or presented 4PCS at SIGGRAPH 2008. Mellado, Aiger and Mitra (2014) made the extraction of the candidate sets much faster."
prereqs: [point-cloud-registration, ransac]
see_also: [ransac-iteration-bound, kabsch-algorithm, geometric-hashing, go-icp, fast-global-registration, teaser-registration, iterative-closest-point, alignment-recognition]
sources:
  - paper: doi:10.1145/1360612.1360684
    title: "Dror Aiger, Niloy J. Mitra and Daniel Cohen-Or, 4-points congruent sets for robust pairwise surface registration, ACM Transactions on Graphics 27(3), Article 85, 2008 (SIGGRAPH 2008)"
    locator: "The affine invariant ratios of a coplanar four-point base, the extraction of the congruent sets from the pairs at the two base distances, the largest common pointset score, the number of trials, and the experiments on scans with noise, outliers and partial overlap"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The best rigid motion between point sets by the SVD with the sign fix, used to fit each candidate set"
---

4-points congruent sets (4PCS) aligns two [point clouds](/point-cloud/) $P$ and $Q$ that overlap only in part, from any start pose and without features or correspondences. It follows the [RANSAC](/ransac/) pattern: guess a motion from a small sample, then count how many points it explains. The sample is a base of four nearly coplanar points of $P$ whose two segments $ab$ and $cd$ cross at a point $e$. The two ratios at which $e$ cuts the segments do not change under any affine map, and so not under a rigid motion. So 4PCS does not try all 4-tuples of $Q$. It finds the pairs of $Q$ at the two segment lengths, computes on each pair the point that the ratio gives, and keeps the pairs of pairs whose points meet. Each such 4-tuple is a candidate image of the base. The [best rigid motion](/kabsch-algorithm/) from the base to the candidate is scored by the largest common pointset (LCP): the number of points of $P$ that land within $\delta$ of a point of $Q$. The best motion over several trials wins.

## In plain words

Pick four points on the first scan that lie on one flat patch, like the corners of a kite, and draw its two crossing sticks. Note where the sticks cross: say a third of the way along one stick and half way along the other. These fractions stay the same however the kite is turned or moved.

In the second scan, find all pairs of points as far apart as the first stick, and mark the point a third of the way along each. Do the same for the second stick at half way. Where two marks meet, the four ends may be the kite.

For each such kite, move the first scan onto it and count how many points land on points of the second scan. Try a few kites and keep the best move.

## The problem

**Input.** Two finite sets $P$ and $Q$ in $\mathbb{R}^3$, each with $n$ points, that sample overlapping parts of one surface; an error bound $\delta > 0$; and a number of trials $N$.

**Output.** A rigid motion $T = (R, t)$ with $R \in SO(3)$ that tries to maximize the LCP score

$$\operatorname{LCP}(T) = \left| \{ p \in P : \min_{q \in Q} |T p - q| \le \delta \} \right| .$$

4PCS is a randomized search for a large LCP. It gives no guarantee of the maximum. This is global [point cloud registration](/point-cloud-registration/): the result does not depend on the start pose.

## The algorithm

**The base and its invariants.** Pick three points $a, b, c$ of $P$, far apart but not farther than the expected size of the overlap. Pick a fourth point $d$ close to their plane, and pair the four points into two segments that cross: $ab$ and $cd$ meet at $e$. Let

$$r_1 = \frac{|a - e|}{|a - b|}, \qquad r_2 = \frac{|c - e|}{|c - d|}, \qquad d_1 = |a - b|, \qquad d_2 = |c - d| .$$

If an affine map $A$ sends the base to $A(a), A(b), A(c), A(d)$, then the image segments cross at $A(e)$, at the same ratios $r_1$ and $r_2$.

**The search in Q.** For a pair $(q_i, q_j)$ at a distance near $d_1$, the image of $e$ would be $e_1 = q_i + r_1 (q_j - q_i)$. For a pair $(q_k, q_l)$ at a distance near $d_2$, it would be $e_2 = q_k + r_2 (q_l - q_k)$. A 4-tuple of $Q$ that is congruent to the base, up to $\delta$, has $e_1 \approx e_2$. Each pair is used in both orders, because the order of $q_i$ and $q_j$ is not known.

```pseudo id=main
4PCS(P, Q, δ, N)
L1  for trial = 1 .. N
L2      (a, b, c, d) ← a wide, nearly coplanar base of P whose segments ab and cd meet at e
L3      r₁ ← |a - e| / |a - b| ;  r₂ ← |c - e| / |c - d| ;  d₁ ← |a - b| ;  d₂ ← |c - d|
L4      R₁ ← ordered pairs of Q at distance d₁ ± δ ;  R₂ ← ordered pairs at distance d₂ ± δ
L5      U ← {(i, j, k, l) : (i, j) ∈ R₁, (k, l) ∈ R₂, |q_i + r₁(q_j - q_i) - q_k - r₂(q_l - q_k)| ≤ δ}
L6      for each (i, j, k, l) in U:  T ← best rigid motion from (a, b, c, d) to (q_i, q_j, q_k, q_l)
L7          if T fits the four points:  score T by LCP(T) ;  keep the best
L8  return the best T
```

Line L2 chooses the base. The reference code takes the widest of a few random triangles whose sides are at most a given width, then the point nearest to their plane for which one of the three ways to pair the four points gives two segments that meet within $\delta$. Line L3 computes the invariants. Line L4 finds the pairs by brute force over all pairs; the paper uses a faster search. Line L5 puts the points $e_1$ in a grid of cubes of side $\delta$, a [hash table](/hash-table/) of cells, and looks up each $e_2$ in its cube and the 26 around it. Line L6 fits the motion by the SVD with the sign fix of Umeyama. Line L7 drops a candidate if a base point is more than $2\delta$ from its partner after the fit, since the ratios also accept affine images that are not congruent, and then scores the rest with the same grid on $Q$. The paper scores on a random sample of $P$ to save time.

## Example

Take the base $a = (0, 0, 0)$, $b = (4, 2, 0)$, $c = (0, 3, 0)$, $d = (3, 0, 0)$ in the plane $z = 0$. The segment $ab$ is $(4s, 2s, 0)$ and the segment $cd$ is $(3u, 3 - 3u, 0)$. They meet where $4s = 3u$ and $2s = 3 - 3u$, so $s = 1/2$, $u = 2/3$, and $e = (2, 1, 0)$. So $r_1 = 0.5$, $r_2 = 2/3$, $d_1 = \sqrt{20} \approx 4.472$ and $d_2 = \sqrt{18} \approx 4.243$.

Let $P$ be the base and four more points, $(1, 1, 2)$, $(3, 3, 1)$, $(-1, 2, 1)$ and $(2, -1, 2)$. Let $Q$ be $P$ turned by 90 degrees about the $z$ axis and moved by $(5, 0, 1)$, plus two outliers $(0, 0, 0)$ and $(6, 4, 1)$. So $q_0, \ldots, q_3$ are the images of $a, b, c, d$: $(5, 0, 1)$, $(3, 4, 1)$, $(2, 0, 1)$, $(5, 3, 1)$. With $\delta = 0.01$:

- $Q$ has 45 pairs. Only $\{q_0, q_1\}$ is at the distance 4.472, so $R_1$ holds $(0, 1)$ and $(1, 0)$.
- Three pairs are at the distance 4.243: $\{q_2, q_3\}$, $\{q_5, q_7\}$, and $\{q_5, q_9\}$, where $q_9$ is an outlier. $R_2$ holds the six ordered pairs.
- With $r_1 = 0.5$, both orders of $(q_0, q_1)$ give the midpoint $(4, 2, 1)$. The pair $(q_2, q_3)$ gives $(2, 0, 1) + \frac{2}{3}(3, 3, 0) = (4, 2, 1)$ as well. No other point of $R_2$ is near. So $U$ has two tuples: $(0, 1, 2, 3)$ and $(1, 0, 2, 3)$.
- The tuple $(0, 1, 2, 3)$ fits exactly: the 90 degree turn and the shift $(5, 0, 1)$, with LCP 8 of 8.
- The tuple $(1, 0, 2, 3)$ has the same ratios, because $r_1 = 0.5$ is symmetric, but it is only an affine image of the base, a mirror image. The best rigid fit leaves a residual of 0.81, so line L7 drops it. Its LCP would be 0.

On a larger case, a curved patch of 200 points split into two clouds of 100 points that share about half their points, with noise of standard deviation 0.003 and $\delta = 0.03$, 30 trials found between 2300 and 4100 candidate sets, and the best LCP gave a rotation error between 0.27 and 1.17 degrees in each of six random cases.

## Correctness

If a trial picks a base that lies in the overlap, then that trial finds the image of the base. Suppose each base point has a partner in $Q$ within $\varepsilon$ of its image under the true motion $T$, and $2\varepsilon$ plus the gap between the two segments is at most $\delta$. A rigid motion keeps distances, so both pairs pass line L4. The point $q_i + r_1 (q_j - q_i)$ is a weighted mean of points within $\varepsilon$ of $T a$ and $T b$, so it is within $\varepsilon$ of $T e_1$; the same holds for the other pair, so the two points meet within $\delta$ in line L5. The Kabsch fit of the four points has a residual at most $2\varepsilon$, because $T$ itself has a sum of squares at most $4 \varepsilon^2$. So line L7 scores a motion close to $T$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

The method is still randomized: the claim needs a good base, which each trial finds only with some probability. And the motion with the best LCP need not be the true one when the shape has symmetries or the overlap is small.

## Complexity

The model is the [real RAM](/real-ram/). Line L2 takes $O(n)$ time. Line L4 takes $\Theta(n^2)$ time by brute force over the pairs. Line L5 builds the grid in time linear in $|R_1|$ and finds the $k$ candidate sets with one grid query for each pair of $R_2$; when the points are spread evenly, each query looks at $O(1)$ stored points, so the extraction takes $O(n^2 + k)$, the bound stated in the paper. Each candidate costs $O(1)$ for the fit and $O(n)$ grid queries for the LCP, each $O(1)$ when the points are spread evenly and $O(n)$ in the worst case. So $N$ trials take $O(N(n^2 + k n))$ time on evenly spread points and $O(N(n^2 + k n^2))$ in the worst case. The space is $O(n^2 + k)$ for the pairs and the candidates.

The number $k$ depends on the data and on $\delta$. With exact data and $\delta = 0$, the number of pairs at one distance is far below $n^2$ for points in general position, so $k$ is small; with a large $\delta$ or a regular shape, many pairs pass, and $k$ can be large. The number of trials $N$ follows the [RANSAC bound](/ransac-iteration-bound/): if a trial picks a base in the overlap with probability $w$, then $N \ge \log(1 - p) / \log(1 - w)$ trials succeed with probability at least $p$. A base needs only 4 points in the overlap, and wide bases are allowed, so $w$ is much larger than for methods that need more points.

## Properties

- **Global.** The start pose does not matter.
- **No features.** It uses only the positions of the points, so it works on surfaces with little texture or with noisy normals.
- **Randomized.** The result depends on the random bases. More trials give a higher chance of success.
- **Robust to partial overlap and outliers.** The LCP score counts only the points that fit, and the base needs only 4 points in the overlap.
- **Approximate.** The motion comes from four points. A local method such as ICP usually refines it.
- **Quadratic per trial.** The brute force pair search costs $\Theta(n^2)$, so the clouds are usually downsampled first.

## Variants and improvements

- **Faster extraction.** Mellado, Aiger and Mitra (2014) find the pairs at a given distance with a spatial index instead of a scan of all pairs, and filter the pairs of pairs by the angle between the two segments, which the ratios alone do not fix. The authors report a cost per trial close to linear in $n$ plus the size of the output.
- **Sampling of the score.** Scoring on a random sample of $P$ and stopping a candidate early when it cannot beat the best score saves much time.
- **Other bases.** Later methods in the same family use bases that are not coplanar.

## When to use it

Use 4PCS to align two scans with an unknown start pose when features are not reliable, for example on smooth or noisy surfaces, and when the overlap is moderate. Downsample the clouds first, for example with a [voxel grid](/voxel-grid-downsampling/), because the cost grows as $n^2$ per trial, and refine the result with [ICP](/iterative-closest-point/). When good features exist, [fast global registration](/fast-global-registration/) or [TEASER](/teaser-registration/) are usually faster. When a proof of the global optimum is needed, use [Go-ICP](/go-icp/). For recognition of many models in one scene, [geometric hashing](/geometric-hashing/) stores bases of the models in advance.

## Pitfalls

- **The choice of delta.** $\delta$ must cover the noise and the sampling: two scans of the same surface do not sample the same points, so the image of a base point is only near some point of $Q$. A too small $\delta$ misses the true candidates; a too large one lets $k$ and the cost explode.
- **Base width.** A narrow base gives a poor estimate of the rotation. A base wider than the overlap cannot lie in it. The paper sets the width from an estimate of the overlap.
- **Affine but not rigid.** The ratios accept every affine image of the base. Check the rigid fit, or the score of many wrong candidates is wasted, and a wrong one may win on a degenerate shape.
- **Mirror images.** With $r_1 = 0.5$ or $r_2 = 0.5$, both orders of a pair give the same point, which doubles the candidates.
- **Flat or symmetric shapes.** A plane, a sphere or a cylinder has many motions with the same LCP. No score based on point positions alone can pick the right one.
- **Coplanar base in a curved scene.** On a strongly curved surface, few wide quadruples are coplanar within $\delta$, so base selection fails often.

## Implementations

## History

Aiger, Mitra and Cohen-Or presented 4PCS at SIGGRAPH 2008. It belongs to a long line of methods that align shapes by matching small sets of points, from RANSAC and the [alignment method](/alignment-recognition/) of object recognition to [geometric hashing](/geometric-hashing/). The key step of 4PCS is the use of affine invariant ratios, which lets it extract all congruent 4-point sets from the pairs of points, instead of trying all 4-tuples. Mellado, Aiger and Mitra (2014) gave a much faster way to extract these sets, which made the method practical on large scans. Open source versions of 4PCS and its faster forms exist, and they are a common first step of scan registration before ICP.

## References
