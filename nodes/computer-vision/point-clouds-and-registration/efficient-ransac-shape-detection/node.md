---
tag: NAW12G
kind: algorithm
slug: efficient-ransac-shape-detection
name: Efficient RANSAC for shape detection
aliases:
- Schnabel RANSAC
area: computer-vision/point-clouds-and-registration
level: advanced
summary: Detect planes, spheres, cylinders, cones and tori in a point cloud by RANSAC with local sampling in an octree and lazy scoring on random subsets.
model: real-ram
complexity:
  vars: {n: the number of points, s: the number of draws, r: the number of random subsets, k: the number of shapes found, d: the depth of the octree}
  time: {worst: O(s^2 n + n d), average: O(s n / r + k n + n d), best: Ω(n d)}
  space: {extra: Θ(n d + s)}
properties: {deterministic: false, exact: false, randomized: true, online: false, recursive: false, needs_normals: true}
history:
  year: 2007
  people: [Ruwen Schnabel, Roland Wahl, Reinhard Klein]
  note: "Schnabel, Wahl and Klein made RANSAC practical for large point clouds with many shapes, by drawing minimal sets from octree cells, scoring candidates on random subsets, and fitting planes, spheres, cylinders, cones and tori from points with normals."
prereqs: [ransac, octree, point-cloud-normal-estimation]
see_also: [primitive-segmentation, geometric-primitive-fitting, msac, ransac-iteration-bound, robust-model-fitting, hough-transform, j-linkage, connected-components]
sources:
  - paper: doi:10.1111/j.1467-8659.2007.01016.x
    title: "Ruwen Schnabel, Roland Wahl and Reinhard Klein, Efficient RANSAC for point-cloud shape detection, Computer Graphics Forum 26(2), 2007, 214-226"
    locator: "The shapes and their minimal sets with normals, the score of compatible points in the largest connected component, the localized sampling in an octree, the score evaluation on random subsets, and the probability of having missed a shape"
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "The RANSAC paradigm of fitting models to minimal random samples and keeping the model with the largest consensus set"
---

Efficient RANSAC for shape detection breaks a point cloud with normals into simple shapes: planes, spheres, cylinders, cones and tori, plus the points that fit none of them. It is a form of [RANSAC](/ransac/) built for clouds of millions of points that hold many shapes of very different sizes, such as scans of buildings and machine parts. Plain RANSAC fails there for two reasons. A random sample of three points rarely falls on one small shape, and scoring each candidate on every point is too slow. Schnabel, Wahl and Klein (2007) fix the first problem by drawing the second and third points from an [octree](/octree/) cell around the first one, and the second by scoring candidates on a random subset first and on more subsets only when the decision is close. Normals from [normal estimation](/point-cloud-normal-estimation/) make the minimal sets small and let the method reject wrong candidates at once. The method finds the largest shape first, removes its points, and searches again.

## In plain words

You have a scan of an object made of flat faces, balls and pipes, and you want to know which points belong to which part.

Pick three points at random. If they lie on one face, the face through them is a guess. Count how many points of the scan lie on that guess, and keep the guess with the largest count. Take its points out, and start again for the next part.

Three tricks make this fast. Pick the second and third points close to the first, so that they are likely on the same part. Count the points of a guess on a small random sample first, and count more only when two guesses are close. Use the direction each point faces: a point that sits on a guess but faces the wrong way does not count.

## The problem

The input is a set $P$ of $n$ points with unit normals, a distance tolerance $\varepsilon$, an angle tolerance $\alpha$, a connection distance $\beta$, a least support $\tau$ and a wanted probability $p_t$. A point is *compatible* with a shape when it lies within $\varepsilon$ of the shape and its normal makes an angle of at most $\alpha$ with the shape normal there, up to sign.

The output is a list of shapes, each with a set of at least $\tau$ points that are compatible with it and connected by steps of at most $\beta$. The sets are disjoint. The points of no set are the rest. The wanted result is the decomposition of the scanned object into its parts, which has no exact form; the method searches greedily for the shape with the largest compatible connected set, and finds it with a probability that it controls with $p_t$.

## The algorithm

```pseudo id=main
EFFICIENT-RANSAC(P, ε, α, β, τ, p_t)
L1  build an octree on P and split P into random subsets S_1, …, S_r
L2  R ← P; C ← ∅; s ← 0; shapes ← an empty list
L3  while |R| ≥ τ do
L4      draw p from R and a level ℓ; draw two more points of R from the cell of p at level ℓ; s ← s + 1
L5      fit a plane, a sphere and a cylinder to the three points; keep those that all three points are compatible with
L6      score each new candidate on S_1, extrapolate the score to an interval, and add it to C
L7      m ← the candidate with the largest expected score; score m and every candidate whose interval overlaps it on the next subsets, until no overlap
L8      if 1 - (1 - P(ŝ(m)))^s ≥ p_t then
L9          A ← the largest β-connected set of points of R compatible with m
L10         if |A| ≥ τ then append (m, A) to shapes; R ← R \ A; C ← ∅; s ← 0
L11         else remove m from C
L12     if no shape was taken at line L10 and 1 - (1 - P(τ))^s ≥ p_t then stop
L13 return shapes
```

Here $P(n)$ is the probability that one draw puts all three sample points on a shape with $n$ points of $R$, and $\hat s(m)$ is the expected score of $m$. For uniform draws $P(n) = (n / |R|)^3$; Schnabel and his coauthors use a bound for the localized draws of line L4.

Line L4 draws the first point uniformly and the other two from one octree cell around it, at a random level. A coarse cell holds the large shapes, and a fine cell isolates a small shape among clutter. Line L5 uses the normals. A plane needs three points. A sphere needs two points with normals: its center lies on both normal lines. A cylinder needs two points with normals: the cross product of the normals gives the axis direction, and the normal lines meet the axis. The third point then only checks the candidate. Cones and tori need more sample points; they follow the same pattern and are left out of the code below. Lines L6 and L7 are the lazy score: most candidates are poor, and one small subset shows that. Line L8 decides when to take the best candidate: once a shape of its size would have been drawn with probability $p_t$, a larger shape is unlikely to be still missing. Line L9 keeps only one connected piece, so two coplanar faces far apart are two shapes. Line L12 stops when a shape of size $\tau$ would have been found by now with probability $p_t$.

## Example

The fits of line L5, on exact data:

| shape | points | normals | fit |
|---|---|---|---|
| plane | $(0,0,0)$, $(1,0,0)$, $(0,1,0)$ | $(0,0,1)$, $(0,0,-1)$, $(0,0,1)$ | normal $(0,0,1)$ from the cross product, $d = 0$; the signs of the normals do not matter |
| sphere | $(1,0,0)$, $(0,1,0)$, check $(0,0,1)$ | $(1,0,0)$, $(0,1,0)$, $(0,0,1)$ | the normal lines meet at $(0,0,0)$, radius 1; the third point is on it |
| cylinder | $(1,0,0)$, $(0,1,5)$, check $(-1,0,2)$ | $(1,0,0)$, $(0,1,0)$, $(-1,0,0)$ | axis direction $(1,0,0) \times (0,1,0) = (0,0,1)$; seen along it, the normal lines meet at $(0,0)$, so the axis is the $z$ axis and the radius is 1 |

The search, on a scene of 840 points: a plane with 300 points, a sphere and a cylinder with 250 points each, and 40 points of clutter, with $\tau = 100$ and $p_t = 0.99$. The rule of line L8 with uniform draws needs this many draws:

| $\lvert R \rvert$ | best shape | $(n / \lvert R \rvert)^3$ | draws for 0.99 |
|---|---|---|---|
| 840 | plane, 300 | 0.0456 | 99 |
| 540 | sphere or cylinder, 250 | 0.0992 | 45 |
| 290 | the last one, 250 | 0.641 | 5 |

After the third shape, 40 points remain, fewer than $\tau$, and the loop ends. Before that, a shape of only $\tau = 100$ points among 840 would need 2728 draws to reach the same probability. This is why small shapes in large clouds are slow for plain RANSAC, and why line L4 samples locally: once the first point is on the small shape, the other two come from a cell that the shape fills, so the draw hits it much more often.

## Correctness

On exact data, the fits of line L5 return the true plane, sphere or cylinder whenever the sample is not degenerate: three points that are not collinear for a plane, and two normals that are not parallel for a sphere or a cylinder. After a candidate is scored on all subsets, its score is the exact count of compatible points of $R$, because the subsets partition the points. The refinement of line L7 ends after at most $r$ steps per candidate. Every output shape has at least $\tau$ compatible points that are connected by steps of at most $\beta$, and the point sets of different shapes are disjoint. The loop ends for every $p_t < 1$, because the draw count grows between extractions and each extraction removes at least $\tau$ points. That the best shape is found is a statement of probability: if each draw hits a shape with probability at least $q$, the chance of $s$ misses is at most $(1 - q)^s$. With localized draws the value of $q$ is an estimate or a bound, not an exact number. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points, $s$ draws in total, $r$ subsets, $k$ shapes found and an octree of depth $d$.

- **Build.** The octree costs $O(n d)$ time and space. The random split costs $O(n)$.
- **One draw.** Lines L4 and L5 cost the size of the cell for the sample, and $O(1)$ for the fits. Line L6 costs $O(n / r)$ per candidate.
- **Refinement.** In the worst case every candidate is refined to the full set at every draw, $O(s n)$ per draw and $O(s^2 n)$ in total. In practice most candidates are poor, their intervals end far below the best one after one subset, and the cost is $O(s n / r)$ in total.
- **Extraction.** Lines L9 to L11 cost $O(n)$ for the compatible points, and the connected set costs $O(n)$ more on clouds of bounded density with a grid of side $\beta$. With $k$ shapes and a bounded number of failed extractions, this is $O(k n)$.
- **Space.** $\Theta(n d)$ for the octree and $\Theta(s)$ for the candidates.

The number of draws is set by the rule of lines L8 and L12, not by $n$. It grows when the shapes are small compared with $|R|$, which localized sampling is meant to offset.

## Properties

- **Randomized.** Two runs with different seeds can return different shapes in a different order. With a fixed seed the result is fixed.
- **Greedy.** The largest shape goes first and keeps its points. A wrong early shape, such as a plane that cuts across two faces within $\varepsilon$, takes points from the shapes that follow.
- **Needs normals.** The fits and the compatibility test use them. Without normals the minimal sets are larger and many more candidates are wrong.
- **Sign free.** The normals need no consistent orientation; the test uses the absolute value of the dot product.
- **Robust to clutter.** Points of no shape do not affect a candidate's score, unless they happen to be compatible with it.

## Variants and improvements

- **Refit.** After line L9, fit the shape again to all its points by least squares, as in [geometric primitive fitting](/geometric-primitive-fitting/), and collect the compatible points again. This lowers the error of a shape fitted from three noisy points.
- **Bitmap connectivity.** The original method finds the connected set in a 2D bitmap over the parameter domain of the shape, with a cell size set by $\beta$, which is faster than a 3D search and follows the shape itself.
- **Adaptive levels.** The original method uses the scores of past candidates to learn which octree levels give good candidates, and draws the levels with these rates in place of uniformly.
- **Keep the candidates.** After an extraction, only candidates that used removed points need to go; the others can be scored again on the smaller $R$. This saves draws.
- **More shapes.** Cones, tori and other surfaces that can be fitted from a few oriented points fit the same frame.
- **MSAC scores.** Score by a truncated sum of distances, as in [MSAC](/msac/), in place of a count.
- **Region growing and Hough methods.** Region growing from seed points with similar normals, and the [Hough transform](/hough-transform/) for planes, are the main other ways to find shapes in clouds. Multi-model methods such as [J-linkage](/j-linkage/) group all hypotheses at once.

## When to use it

Use efficient RANSAC to turn a scan of a building, a machine part or an indoor room into simple shapes, for [primitive segmentation](/primitive-segmentation/), reverse engineering, compression or detection of walls and floors. It needs normals and a good choice of $\varepsilon$, $\alpha$ and $\beta$ for the noise and the sampling density. For a cloud of only planes, region growing or a plane Hough transform is often simpler. For free-form surfaces with no simple shapes, use a surface reconstruction method.

## Pitfalls

- **ε below the noise.** If $\varepsilon$ at line L5 or line L9 is smaller than the noise of the scan, the fits fail their check and each shape breaks into many small pieces. Measure the noise on a known flat part first.
- **Too loose an angle.** A large $\alpha$ lets line L9 accept points from a neighboring face near an edge, and lets a sphere of large radius pass as a plane. A small $\alpha$ fails on noisy normals.
- **β and the density.** At line L9, a $\beta$ smaller than the sampling spacing breaks one face into pieces; one larger than the gap between parts joins them.
- **Huge spheres and cylinders.** Near-flat samples give spheres and cylinders of very large radius at line L5, which compete with the true plane. Bound the radius by the size of the scene.
- **Trusting the probability.** The rule of lines L8 and L12 assumes that a draw hits a shape with a known probability. With localized draws or a poor model of the clutter this is only an estimate, so a small shape can still be missed.
- **Normals across edges.** Normals estimated near edges are blends of the two faces, so points near edges fail the check of line L9 and stay unassigned. This is expected; assign them afterwards to the nearest shape if needed.

## Implementations

## History

Fischler and Bolles (1981) introduced RANSAC: fit a model to a random minimal sample and keep the model that most data points agree with. For point clouds, RANSAC was used early on to find planes and other shapes, but on large clouds with many shapes it needed far too many samples and far too many evaluations. Schnabel, Wahl and Klein (2007) addressed both costs. They sampled minimal sets locally in an octree, so that small shapes were found as fast as large ones, scored candidates on random subsets with confidence intervals, and used the normals to fit planes, spheres, cylinders, cones and tori from very small samples. They defined the score as the largest connected set of compatible points, and gave the probability of having missed a shape as the rule for when to extract a candidate and when to stop. Their method became a standard tool for shape detection in point clouds, with implementations in libraries for geometry processing.

## References
