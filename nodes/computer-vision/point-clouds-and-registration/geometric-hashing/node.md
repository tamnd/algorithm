---
tag: 56HCXG
kind: algorithm
slug: geometric-hashing
name: Geometric hashing
aliases:
- Lamdan-Wolfson geometric hashing
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Store each model's points in coordinates of every basis of its own points in a hash table, then recognize a scene by voting over bases picked from it."
solves: [object-recognition]
model: real-ram
complexity:
  vars: {m: the number of points in each model, K: the number of models, n: the number of scene points, N: the number of scene bases tried}
  time: {worst: O(K m^4 + N K m^4 n), average: O(K m^4 + N m n), best: Θ(K m^4 + n + m)}
  space: {extra: Θ(K m^4)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1988
  people: [Yehezkel Lamdan, Haim J. Wolfson]
  note: "Lamdan and Wolfson presented geometric hashing at ICCV 1988. Grimson and Huttenlocher (1990) showed how fast it degrades with noise and clutter."
prereqs: [hash-table, object-recognition]
see_also: [alignment-recognition, generalized-hough-transform, four-points-congruent-sets, ransac, affine-camera-model, locality-sensitive-hashing, point-cloud-registration, similarity-transformation]
sources:
  - paper: "Yehezkel Lamdan and Haim J. Wolfson, Geometric hashing: a general and efficient model-based recognition scheme, Proceedings of the Second International Conference on Computer Vision (ICCV 1988), 238-249"
    title: "Yehezkel Lamdan and Haim J. Wolfson, Geometric hashing: a general and efficient model-based recognition scheme, Proceedings of the Second International Conference on Computer Vision (ICCV 1988), 238-249"
    locator: "The preprocessing of the models into a hash table of coordinates in every basis, the recognition by voting from bases picked in the scene, and the verification of the candidates"
  - paper: doi:10.1109/ICCV.1990.139544
    title: "W. Eric L. Grimson and Daniel P. Huttenlocher, On the sensitivity of geometric hashing, Proceedings of the Third International Conference on Computer Vision (ICCV 1990), 334-338"
    locator: "The analysis of how noise in the point positions and clutter in the scene lower the performance of geometric hashing"
  - paper: doi:10.1109/99.641604
    title: "Haim J. Wolfson and Isidore Rigoutsos, Geometric hashing: an overview, IEEE Computational Science and Engineering 4(4), 1997, 10-21"
    locator: "A survey of the method, its forms for other groups of transformations, and its uses"
---

Geometric hashing recognizes known shapes in a scene of points, even when a shape is seen under an unknown transformation, partly hidden, and mixed with other points. It is a method of [object recognition](/object-recognition/) by indexing. Before any scene is seen, each model is stored many times in a [hash table](/hash-table/): for every basis, a small ordered set of its own points, the coordinates of the other model points in the frame of that basis go into the table. In the version for the affine group in the plane, a basis is three points, and the coordinates of a point do not change under any affine map applied to the whole model. To recognize, pick a basis in the scene, compute the coordinates of all scene points in it, and look them up. Each hit is a vote for a (model, basis) pair. A pair with many votes says which model is present and which of its points match the scene basis. A check of the whole model against the scene then accepts or rejects it.

## In plain words

Draw a shape with a few dots. Pick three of its dots and use them as a ruler: one dot is the zero, and the other two set the two directions and the units. Write down where every other dot lies on this ruler. Do this for every choice of three dots, and file all the notes by position in a big index, each with the name of the shape and the three dots used.

Now take a picture where the shape may be stretched, turned or slid, among stray dots. Pick any three dots of the picture as a ruler and read off where the other dots lie. Look each place up in the index. If one shape with one ruler comes up again and again, the three picked dots are likely its ruler. Lay the whole shape on the picture to make sure.

## The problem

**Input.** A set of $K$ models, each a set of $m$ points in the plane, and a scene of $n$ points. The scene may contain the image of one model under an unknown affine map $T(x) = A x + t$, with some noise, together with points that belong to no model.

**Output.** A model and an affine map under which the model points land near scene points, or no model if none is present.

The method is a randomized search. The same idea works for other groups of maps: for rigid motions or [similarity transformations](/similarity-transformation/) of the plane, a basis is two points; in 3D, it needs more points.

## The algorithm

**Affine coordinates.** Three points $o, a, b$ not on one line form a basis. Every point $p$ has unique coordinates $(\alpha, \beta)$ with

$$p = o + \alpha (a - o) + \beta (b - o).$$

If an affine map with an invertible linear part is applied to $p$, $o$, $a$ and $b$, the coordinates stay the same.

```pseudo id=main
GeometricHashing(models, scene, s, v, τ)
L1  for each model M and each ordered basis (i, j, k) of its points not on one line
L2      for each other point y_l of M:  (α, β) ← coordinates of y_l in the basis
L3          add (M, (i, j, k)) to the table bin (⌊α/s⌋, ⌊β/s⌋)
L4  repeat:  pick an ordered basis of three scene points
L5      for each other scene point:  (α, β) ← its coordinates in the scene basis
L6          give one vote to each entry in its bin and in the 8 bins around it
L7      for each entry (M, basis) with at least v votes:  fit the affine map from the basis of M to the scene basis
L8          if the map puts the points of M within τ of scene points:  return M and the map
```

Lines L1 to L3 are the preprocessing. They run once, whatever the scene. Lines L4 to L8 are the recognition. Each trial in the reference code picks a random ordered triple of scene points. The 8 neighbour bins of line L6 allow for noise near a bin edge; this is a choice of the reference code. Line L7 tries the entries in order of their votes. Three point pairs fix an affine map, so line L7 solves a small linear system. Line L8 is the verification: the reference code asks, by default, that every model point land near a scene point.

## Example

The model $M$ is a house of five points: $y_0 = (0, 0)$, $y_1 = (2, 0)$, $y_2 = (0, 1)$, $y_3 = (2, 1)$ and the roof top $y_4 = (1, 2)$. No three of them are on one line, so all $5 \cdot 4 \cdot 3 = 60$ ordered triples are bases, and the table holds $60 \cdot 2 = 120$ entries. With the bin size $s = 0.25$, they fall into 39 bins. In the basis $(0, 1, 2)$, $y_3$ has the coordinates $(1, 1)$ and $y_4$ has $(0.5, 2)$, so $(M, (0, 1, 2))$ goes into the bins $(4, 4)$ and $(2, 8)$.

The scene is the image of $M$ under $A = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$ and $t = (3, 1)$, which gives $(3, 1)$, $(5, 1)$, $(4, 3)$, $(6, 3)$ and $(6, 5)$, plus a stray point $(1, 4)$. Take the first three scene points as the basis: $u = (2, 0)$ and $v = (1, 2)$.

| Scene point | Coordinates | Bin | Entries found |
|---|---|---|---|
| $(6, 3)$ | $(1, 1)$ | $(4, 4)$ | 8 entries, among them $(M, (0, 1, 2))$ and $(M, (1, 0, 3))$ |
| $(6, 5)$ | $(0.5, 2)$ | $(2, 8)$ | $(M, (0, 1, 2))$ and $(M, (1, 0, 3))$ |
| $(1, 4)$ | $(-1.75, 1.5)$ | $(-7, 6)$ | none, also none in the 8 bins around |

Two entries get 2 votes. $(M, (0, 1, 2))$ is the true one. $(M, (1, 0, 3))$ is there because the house is symmetric: the mirror $x \mapsto 2 - x$ swaps $y_0$ with $y_1$ and $y_2$ with $y_3$, and keeps $y_4$. A mirror is an affine map, so this basis also fits, and its verification also passes, with a map that maps the house onto the same five scene points. The stray point gets no votes.

On a larger case, three random models of 8 points give a table of 5040 entries in 2645 bins of side 0.1. Each model was placed in a scene with 12 stray points and noise of standard deviation 0.002. The reference code found the right model, with 5 votes out of 5 and all 8 points verified, after 28, 32 and 10 random scene bases.

## Correctness

The coordinates in a basis do not change under an invertible affine map $T$, since $T(p) - T(o) = A(p - o)$ and $A$ is linear. So in the exact case, when the scene basis is the image of a model basis in the same order, each of the other $m - 3$ model points has an image with the same coordinates, in the same bin, and the true entry gets $m - 3$ votes. With noise that moves each coordinate by less than $s$, the bin moves by at most one step in each direction, so the 8 neighbour bins still catch it. Three point pairs fix the affine map, so the fit is $T$, and the verification passes. Any result that the code returns has passed the verification. The full proof is in [proofs/correctness.md](proofs/correctness.md).

What is not guaranteed: a trial must pick three scene points that are images of model points, which happens only with some probability, and with noise a thin basis can move the coordinates by much more than $s$.

## Complexity

The model is the [real RAM](/real-ram/), with a hash table that does a lookup in expected constant time. A model has $m(m-1)(m-2)$ ordered bases, and each stores $m - 3$ entries, so the preprocessing takes $\Theta(K m^4)$ time and space. This is the price for fast recognition, and it is paid once.

One trial computes $n - 3$ coordinates and does 9 lookups for each. If the entries are spread over many bins, so that each bin holds a constant number of entries, the voting takes $O(n)$ time, and a constant number of hypotheses cost $O(m n)$ each to verify by brute force. In the worst case a bin holds all $K m^4$ entries, and up to $K m^3$ hypotheses must be verified, so one trial takes $O(K m^4 n)$. With $N$ trials, the total is $O(K m^4 + N m n)$ when the entries are spread out and $O(K m^4 + N K m^4 n)$ in the worst case. A first trial that succeeds at once needs $\Theta(n + m)$ after the preprocessing.

## Properties

- **Indexing, not search.** The work per trial does not grow with the number of models when the bins stay sparse; all models are tried at once by the lookup.
- **Invariant.** The coordinates do not depend on the unknown map, so no pose search is needed.
- **Robust to occlusion and clutter.** The votes come from whatever model points are visible, and points that are not in the model only add scattered votes.
- **Randomized.** Each trial picks a random scene basis, and the number of trials follows the same bound as [RANSAC](/ransac-iteration-bound/).
- **Large memory.** The table grows as $K m^4$ for affine bases, and as $K m^3$ for bases of two points.
- **Sensitive to noise.** Coordinates in a thin or small basis change much with small errors in the points.

## Variants and improvements

- **Other groups.** For rigid motions or similarity maps of the plane, a basis is an ordered pair of points, and the table has $K m^3$ entries. For 3D models under rigid motions, a basis needs three points.
- **Weighted votes.** A vote can be weighted by how likely the scene coordinates are given the noise, instead of a hard bin test. This is closer to a likelihood and lowers the effect of bin edges.
- **Coarser bins near unstable bases.** Skip bases that are too thin or too small, or use bins that grow with the expected error in that basis.
- **Features instead of points.** Points with a direction, lines or curvature extrema can form a basis with fewer elements, which shrinks the table.
- **Approximate keys.** Instead of a fixed grid of bins, the invariant coordinates can be looked up by an approximate near neighbour index, for example with [locality-sensitive hashing](/locality-sensitive-hashing/), which removes the bin edges.

## When to use it

Use geometric hashing when many models must be found in many scenes, the models are known in advance, they are made of a modest number of distinctive points, and the scene points are accurate. The cost of the table is paid once, and recognition then needs few trials per scene. When there is only one model, the [alignment method](/alignment-recognition/) or [RANSAC](/ransac/) does the same work without the table. When the points are noisy, a vote in parameter space as in the [generalized Hough transform](/generalized-hough-transform/), or features with descriptors, are often more reliable. For the registration of two large scans, [4PCS](/four-points-congruent-sets/) uses a related invariant but builds the index from the scene at run time.

## Pitfalls

- **Bin size.** Bins smaller than the error in the coordinates split the votes of the true model. Bins much larger let many wrong entries share a bin, and the voting becomes slow and noisy.
- **Thin bases.** Three nearly collinear points or two very close points give large and unstable coordinates. Skip such bases, both in the table and in the scene.
- **Symmetric models.** A symmetric model gets votes for several bases. All of them can be correct; the verification must not reject them as conflicts.
- **Mirror images.** The affine group includes reflections. If a model must not match its mirror image, check the sign of the determinant of the fitted map.
- **Clutter.** Many stray points give many random votes. Set the vote threshold from the number of model points that you expect to see, and always verify.
- **Memory.** $m^4$ grows fast. Models of hundreds of points need subsampling, or bases of fewer points with a smaller group of maps.

## Implementations

## History

Lamdan and Wolfson presented geometric hashing at ICCV 1988 as a general scheme for model-based recognition, with an offline step that stores the models in a hash table under every basis and an online step that votes from bases of the scene. Grimson and Huttenlocher (1990) analysed its sensitivity and found that with a few pixels of error in the points, and with clutter, wrong models collect many votes, so the method degrades quickly. Wolfson and Rigoutsos (1997) surveyed the method, its forms for other groups of maps, and its uses.

## References
