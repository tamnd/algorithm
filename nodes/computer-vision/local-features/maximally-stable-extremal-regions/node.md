---
tag: C7478H
kind: algorithm
slug: maximally-stable-extremal-regions
name: Maximally stable extremal regions
aliases:
- MSER
area: computer-vision/local-features
level: core
summary: Find connected regions of a thresholded image whose area changes least as the threshold moves, computed for all thresholds with a union-find sweep.
solves: [feature-detection]
model: word-ram
complexity:
  vars: {N: the number of pixels, M: the number of gray levels, T: the number of tracks (at most N)}
  time: {worst: O(N α(N) + M T), average: O(N α(N) + M T), best: O(N α(N) + M T)}
  space: {extra: O(N + M T)}
properties: {deterministic: true, exact: true, affine_covariant_regions: true, invariant_to_intensity_offset: true, heuristic: true}
history:
  year: 2002
  people: [Jiri Matas, Ondrej Chum, Martin Urban, Tomas Pajdla]
  note: Matas and others introduced MSER at BMVC 2002 for wide-baseline stereo, with the journal version in 2004. Nister and Stewenius gave a linear time algorithm in 2008.
prereqs: [disjoint-set-forest, connected-component-labeling]
see_also: [harris-affine-detector, invariant-local-features, detector-repeatability, watershed-segmentation, counting-sort, union-find-connectivity, image-segmentation, sift]
sources:
  - paper: doi:10.5244/C.16.36
    title: Jiri Matas, Ondrej Chum, Martin Urban and Tomas Pajdla, Robust wide baseline stereo from maximally stable extremal regions, Proceedings of the British Machine Vision Conference (BMVC 2002), 384-393, 2002
    locator: the section on maximally stable extremal regions (the definition of extremal regions, the stability measure and the enumeration algorithm)
  - paper: doi:10.1016/j.imavis.2004.02.006
    title: Jiri Matas, Ondrej Chum, Martin Urban and Tomas Pajdla, Robust wide-baseline stereo from maximally stable extremal regions, Image and Vision Computing 22(10), 761-767, 2004
    locator: the section on maximally stable extremal regions
  - paper: doi:10.1007/978-3-540-88688-4_14
    title: David Nister and Henrik Stewenius, Linear time maximally stable extremal regions, European Conference on Computer Vision (ECCV 2008), 2008
    locator: the description of the linear time algorithm
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the section on the MSER detector and the evaluation
---

Maximally stable extremal regions (MSER) solve [feature detection](/feature-detection/) by finding regions instead of points. Threshold a gray image at a level $g$: the pixels with $I \le g$ form connected components, the dark extremal regions, and the pixels with $I \ge g$ form the bright ones. As $g$ rises, dark regions appear, grow and merge. A region is maximally stable when its area changes least, relative to its size, as the threshold moves by $\pm\Delta$. These regions have sharp borders of high contrast, and a change of viewpoint that maps the scene by an affine map, or by any continuous map, carries each region to the corresponding region in the other view. One sweep over the levels with a [disjoint-set forest](/disjoint-set-forest/) finds the regions at all thresholds. With $N$ pixels, $M$ gray levels and $T$ tracks of nested regions, the cost is $O(N\alpha(N) + MT)$.

## In plain words

Think of the image as a landscape, where dark pixels are low and bright pixels are high. Fill it with water slowly. Lakes appear in the low places, grow, and join when the water passes over the ridges between them. Some lakes stay almost the same size while the water rises a lot, because steep walls hold them. Those lakes are the regions we want: their shape depends on the scene, not on the exact water level. The method notes the size of every lake at every water level in one pass, and then picks each lake at the level where its size changes most slowly. Doing the same with the image turned upside down gives the bright regions.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $N$ pixels and integer values in $0, \dots, M - 1$. A pixel has coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down. Two pixels are neighbours when they share a side (4-connectivity). The parameters are the step $\Delta \ge 1$, the smallest and largest area $a_{\min}$ and $a_{\max}$, and an optional largest variation $v_{\max}$.

A dark extremal region at level $g$ is a connected component of $\{I \le g\}$. Two such regions are either disjoint or nested, so they form a tree, the component tree. This page follows the regions along tracks. A track starts when a new component appears. When components merge at level $g$, the track whose region had the larger area at level $g - 1$ continues with the merged region, and the older track wins a tie; the other tracks end at $g - 1$. Let $a_T(g)$ be the area of the region of track $T$ at level $g$, with $a_T(g) = 0$ before the track starts, and let $A_T(g + \Delta)$ be the area of the region at level $g + \Delta$ that contains it. The stability of the region is

$$q_T(g) = \frac{A_T(g + \Delta) - a_T(g - \Delta)}{a_T(g)}.$$

This is the measure $\lvert Q_{g + \Delta} \setminus Q_{g - \Delta} \rvert / \lvert Q_g \rvert$ of Matas and others, applied along a track. The output is each region where $q_T$ has a strict local minimum along its track, with $a_{\min} \le a_T(g) \le a_{\max}$ and $q_T(g) \le v_{\max}$; a run of equal values that is lower than both neighbours counts once, at its first level. Each region is reported as its level and a seed pixel, the first pixel of its track. The bright regions are the dark regions of $M - 1 - I$.

## The algorithm

```pseudo id=main
MSER(I, Δ, a_min, a_max, v_max)         ▷ I has N pixels with values in 0, …, M - 1
L1  sort the pixels by gray level with counting sort
L2  for g ← 0 to M - 1 do
L3      for each pixel p with I(p) = g, in index order do
L4          make p a set of its own;  R ← the distinct sets of its 4-neighbours that are already added
L5          if R is empty then start a new track with seed p and birth g
L6          else join p and all sets of R; the track with the largest a(g - 1) continues (the older on ties) and the others end at g - 1
L7      for each live track T do a_T(g) ← the size of its set
L8  for each track T and each g from its birth to min(its end, M - 1 - Δ) do q_T(g) ← (A_T(g + Δ) - a_T(g - Δ)) / a_T(g)
L9  for each run of equal values of q_T with larger values on both sides do report (first level of the run, seed of T) if a_min ≤ a_T ≤ a_max and q_T ≤ v_max
L10 do the same for M - 1 - I to get the bright regions, and return all regions
```

Line L1 is a [counting sort](/counting-sort/), $O(N + M)$. Lines L3 to L6 are the union-find form of [connected component labeling](/connected-component-labeling/), run once while the threshold rises: each pixel is added once and joined with its neighbours. A track that ended at level $e$ was absorbed by another track, so $A_T(g + \Delta)$ follows these links until it reaches the track that is live at $g + \Delta$. Line L9 compares exact fractions. The region of a reported pair $(g, p)$ is the component of $\{I \le g\}$ that contains $p$; any flood fill gets its pixels.

## Example

Take a $10 \times 10$ image with background $200$, a $6 \times 6$ square of $120$ at $2 \le u, v \le 7$, a $3 \times 3$ square of $40$ inside it at $3 \le u, v \le 5$, the pixel $(4, 4)$ set to $30$, and two lone pixels, $90$ at $(8, 6)$ and $150$ at $(1, 8)$. Take $\Delta = 10$. The track that starts at $(4, 4)$ has the area $1$ for $30 \le g \le 39$, $9$ for $40 \le g \le 119$, $37$ for $120 \le g \le 199$ (the square of side 6 and the lone $90$ pixel next to it), and $100$ from $200$ on. Its stability is:

| $g$ | 30 to 39 | 40 to 49 | 50 to 109 | 110 to 119 | 120 to 129 | 130 to 189 | 190 to 199 | 200 to 209 | 210 to 245 |
|---|---|---|---|---|---|---|---|---|---|
| $q(g)$ | 9 | 8/9 | **0** | 28/9 | 28/37 | **0** | 63/37 | 63/100 | 0 |

The two runs of $0$ with larger values on both sides give the dark regions at $g = 50$, the $3 \times 3$ square with area $9$, and at $g = 130$, the $37$ pixels of the large square and the $90$ pixel. The last run reaches the top of the range of $q$, so it has no larger value on its right and gives no region. The lone pixels give the dark regions $(8, 6)$ at $g = 100$ and $(1, 8)$ at $g = 160$, each with area $1$. The bright regions, of $\{I \ge g\}$, have the areas $91$, $90$, $63$ and $62$, at $g = 80$, $110$, $140$ and $190$. With $a_{\min} = 4$ and $a_{\max} = 50$ only the two squares remain.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that after level $g$ the sets of the forest are exactly the connected components of $\{I \le g\}$, that each live track holds one of them and contains its seed, and that the recorded areas and the values of $q$ are the ones of the definition. The selection of line L9 then reports exactly the strict local minima along each track. Two invariance facts follow from the definition. The set of extremal regions does not change under a strictly increasing change of the gray values; adding a constant to the image shifts every level and leaves the result the same. And a continuous one-to-one map of the image plane maps connected components to connected components and keeps the order of inclusion, so a region in one view maps to the corresponding region in the other view. The areas change by the same factor under an affine map, so $q$ and the selection do not change.

## Complexity

The model is the word RAM, with gray levels that fit in a word.

- Line L1 is $O(N + M)$.
- Lines L3 to L6 make $N$ additions and at most $4N$ find operations with union by size and path compression, $O(N\alpha(N))$ in total. Choosing the continuing track is $O(1)$ per neighbour.
- Line L7 runs once per level for each live track. A track is live for at most $M$ levels, so this is $O(MT)$.
- Lines L8 and L9 do $O(1)$ work per recorded area, plus the links followed for $A_T$, which is $O(MT)$ over all tracks.

The total is $O(N\alpha(N) + MT)$, with $O(N + MT)$ space for the forest and the areas. For 8-bit images $M = 256$. Recording areas only at the levels where a track changes, as most implementations do, removes the factor $M$. Nister and Stewenius give an algorithm in linear time that processes the pixels in the order of a flood fill and needs only one stack of components.

## Properties

- **Regions, not points.** Each MSER is a set of pixels of any shape. For matching, an ellipse with the same second moments is fitted, and a descriptor is computed on the normalized ellipse.
- **Affine covariance.** The regions follow any continuous one-to-one change of the image plane, so in particular affine maps. No iteration is needed, unlike the [Harris-affine detector](/harris-affine-detector/).
- **Intensity.** The extremal regions are the same under any strictly increasing change of the gray values. The selection depends on $\Delta$ in gray levels, so an offset does not change it and a change of contrast can.
- **Nested results.** Regions from one track or from nested tracks can be nested or almost equal. Many implementations remove regions that are too similar to their parent.
- **Exact.** For a given image and parameters, the result follows from the definition without any approximation, since all values are integers and fractions.

## Variants and improvements

- **Linear time MSER.** Nister and Stewenius flood the image from one pixel and keep a stack of growing components, so the time is linear in $N$ and the memory is small.
- **Diversity filter.** Drop a region when its parent region has almost the same area. This removes most duplicates.
- **Color MSER.** Grow regions on a color image by joining neighbours in the order of their color distance, instead of the gray value.
- **Ellipse fit.** Report the mean and covariance of the pixels of each region, which give an affine frame for a descriptor.
- **Other stability measures.** Use only the change above, $(A_T(g + \Delta) - a_T(g)) / a_T(g)$, as several libraries do. This changes which levels are chosen but not the set of extremal regions.

## When to use it

Use it for matching images of flat or almost flat objects under large changes of viewpoint, such as buildings, signs and documents, and for finding text, where letters are often stable dark or bright regions. It is fast, needs no smoothing and gives few, distinct regions. On images of natural scenes with soft texture and blur, the regions are less stable, and corner or blob detectors such as [SIFT](/sift/) find more useful points.

## Pitfalls

- **Only one polarity.** Dark and bright regions need two sweeps, on $I$ and on $M - 1 - I$.
- **Connectivity.** 4-connectivity and 8-connectivity give different regions. Use the same one in all views.
- **Blur.** A blurred border makes the area grow steadily with $g$, and no level is stable. Small or blurred structures are lost.
- **Too small a $\Delta$.** With few gray levels between neighbour regions, the stability is undefined or noisy. With $M = 256$, values from 5 to 10 are common.
- **Huge regions.** The background and its big parts are stable too. Set $a_{\max}$, for example to a fraction of the image.
- **Plateaus.** Many levels can have the same $q$. Report one region per run of equal values, or the same region comes out many times.

## Implementations

## History

Jiri Matas, Ondrej Chum, Martin Urban and Tomas Pajdla introduced maximally stable extremal regions at BMVC 2002, to find correspondences in wide-baseline stereo, and published the journal version in 2004. They enumerate the extremal regions with a union-find structure over the pixels sorted by gray level, as in the flooding view of the [watershed transform](/watershed-segmentation/). In the 2005 comparison of affine region detectors by Mikolajczyk and others, MSER was one of the six detectors studied. David Nister and Henrik Stewenius gave a linear time algorithm in 2008.

## References
