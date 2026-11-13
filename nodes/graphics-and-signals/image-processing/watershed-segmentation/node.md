---
tag: P0M4PZ
kind: algorithm
slug: watershed-segmentation
name: Watershed segmentation
aliases:
- watershed transform
- watershed by immersion
- marker-controlled watershed
area: graphics-and-signals/image-processing
level: advanced
summary: Flood a gray image, usually a gradient, level by level from its minima or from markers, and draw watershed lines where water from two basins would meet.
solves: [image-segmentation]
model: word-ram
complexity:
  vars: {N: the number of pixels, G: the number of gray levels from the least value to the largest}
  time: {worst: O(N^2 + G), average: O(N^2 + G), best: O(N + G)}
  space: {extra: Θ(N)}
properties: {deterministic: true, exact_definition: true, draws_watershed_lines: true, one_basin_per_minimum: true, oversegments_without_markers: true}
history:
  year: 1979
  people: [Serge Beucher, Christian Lantuéjoul, Luc Vincent, Pierre Soille]
  note: Beucher and Lantuéjoul used watersheds for contour detection in 1979. Vincent and Soille defined the watershed by immersion and gave a fast queue-based algorithm in 1991.
prereqs: [image-segmentation, priority-queue, breadth-first-search]
see_also: [region-growing, distance-transform, mathematical-morphology, sobel-operator, prim, minimum-bottleneck-spanning-tree, connected-component-labeling, felzenszwalb-segmentation]
sources:
  - paper: doi:10.1109/34.87344
    title: Luc Vincent and Pierre Soille, Watersheds in digital spaces, an efficient algorithm based on immersion simulations, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(6), 583 to 598, 1991
    locator: the definition of the watershed by immersion with geodesic influence zones, and the algorithm that sorts the pixels and floods each level with a queue
  - paper: doi:10.3233/FI-2000-411207
    title: Jos B. T. M. Roerdink and Arnold Meijster, The watershed transform, definitions, algorithms and parallelization strategies, Fundamenta Informaticae 41(1-2), 187 to 228, 2000
    locator: Section 3.2.1 (Definition 3.2, the relabeling of watershed pixels, Fig. 3) and Section 4.1 (why the Vincent-Soille algorithm does not compute Definition 3.2, and the exact version with quadratic worst case)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation, the section on morphological watersheds and the use of markers
---

The watershed transform treats a gray image as a landscape, where the value of a pixel is its height. Water rises from the bottom of every valley. Where the water from two valleys would meet, a dam is built, and the dams are the watershed lines. Each valley with its water is a catchment basin, and the basins are the regions of the segmentation. The image that is flooded is usually a gradient magnitude, from a [Sobel operator](/sobel-operator/) for example, so that the valleys are the flat insides of objects and the ridges are their edges. Vincent and Soille gave the definition by immersion and a fast algorithm in 1991. Roerdink and Meijster showed in 2000 that this algorithm does not compute its own definition exactly. The implementation here follows the definition exactly, and it also gives the marker-based flood that most libraries use, because a raw gradient has many small valleys and gives far too many regions.

## In plain words

Think of the picture as a relief map, with bright pixels as hills and dark pixels as valleys. Make a small hole at the bottom of every valley and push the map slowly down into a lake. Water comes up through the holes and fills each valley. When the water from two valleys is about to mix, put up a thin wall. At the end, the walls cut the map into pieces, one piece for each valley. If you put the holes only where you choose, you get exactly one piece for each hole, and the walls follow the high ground between them.

## The problem

The input is a gray [digital image](/digital-image/) $f$ with $N$ pixels and integer values, and a neighborhood, 4 or 8 neighbors. For a level $h$, the threshold set $T_h$ is the set of pixels with $f(p) \le h$. Inside a set $A$ of pixels, the geodesic distance $d_A(p, q)$ is the length of the shortest path from $p$ to $q$ that stays in $A$. If $B_1, \ldots, B_k$ are disjoint sets inside $A$, the influence zone of $B_i$ is the set of pixels of $A$ that are strictly closer to $B_i$ than to every other $B_j$, and $IZ_A$ is the union of these zones. Pixels that are equally close to two or more sets are in no zone.

Definition 3.2 of Roerdink and Meijster, which states the definition of Vincent and Soille as a recursion, is:

$$X_{h_{\min}} = T_{h_{\min}}, \qquad X_{h+1} = \min{}_{h+1} \cup IZ_{T_{h+1}}(X_h) \quad \text{for } h_{\min} \le h < h_{\max},$$

where $\min_{h+1}$ is the union of the regional minima at level $h+1$ (connected plateaus with no lower neighbor). The basins of $X_h$ are its connected parts, each one grown from one regional minimum. The watershed is the set of pixels not in $X_{h_{\max}}$. The output is a label image with one label per basin and a special label W for the watershed pixels. It is one way to solve the [image segmentation](/image-segmentation/) problem.

## The algorithm

```pseudo id=main
WATERSHED-BY-IMMERSION(f)
L1  group the pixels by gray value, each group in raster order;  W-set ← ∅
L2  for h ← h_min to h_max do
L3      P ← the pixels with f = h  ▷ skip h if P = ∅ and the last pass changed no label
L4      Q ← P ∪ W-set  ▷ every pixel of T_h that is not yet in a basin
L5      for each p ∈ Q next to a basin pixel do d(p) ← 1;  L(p) ← the basin labels of its neighbors
L6      breadth-first search in Q from these pixels: d(q) ← d + 1 and L(q) ← ∪ L(p) over neighbors p with d(p) = d
L7      for each reached p ∈ Q: if |L(p)| = 1 then label p with that basin else label p with W and keep it in W-set
L8      each connected part of the unreached pixels of P is a new minimum: give it a new label
L9  return the labels
```

Lines L5 and L6 compute, for every non-basin pixel of $T_h$, its geodesic distance to the nearest basins and the set of labels of the basins at that distance. A pixel with one label is in that basin's influence zone. A pixel with two or more is equally close to several basins and gets W. Line L8 handles the pixels that no basin reaches: they form plateaus at level $h$ with no lower neighbor, so they are the regional minima $\min_h$.

The important detail is line L4. A W pixel is not final. At a higher level the basins have grown, and the pixel can be closer to one of them, so every pass recomputes all W pixels, not only the new pixels. For the same reason, a level with no pixels is not always a no-op: the threshold set is the same, but the basins grew in the last pass, and the influence zones can grow again. Such a level is skipped only when the pass before it changed nothing, because then the next pass would return the same basins.

**Markers.** In practice the flood starts from markers, one labeled set of pixels per object wanted, instead of from all regional minima. `watershed_from_markers` in the implementation keeps a [priority queue](/priority-queue/) of unlabeled pixels next to labeled ones, with the key $\max(f(p), f(q))$ when the labeled pixel $p$ pushes $q$. It always labels the pixel with the least key, with the label of the pixel that pushed it, and ties go to the earlier entry. This is [Prim's algorithm](/prim/) for a minimum spanning forest rooted at the markers on the edge weights $\max(f(p), f(q))$. Every pixel goes to a marker that it can reach by a path whose highest value is as low as possible. This flood, due to Meyer, labels every pixel and draws no lines.

## Example

Take the $3 \times 3$ image of Roerdink and Meijster, with rows $(3, 2, 2)$, $(3, 1, 1)$ and $(0, 1, 0)$, and 4-connectivity. The two zeros are the regional minima, A at the bottom left and B at the bottom right. Rows are listed from top to bottom.

| level | row 1 | row 2 | row 3 |
|---|---|---|---|
| 0 | 3 2 2 | 3 1 1 | A 1 B |
| 1 | 3 2 2 | 3 W B | A W B |
| 2 | 3 B B | 3 B B | A W B |
| 3 | B B B | W B B | A W B |

At level 1, the bottom middle pixel touches both A and B, so it gets W. The center pixel is two steps from A (through the bottom middle pixel) and two steps from B (through the pixel to its right), so it also gets W. The right pixel of row 2 touches B. At level 2, the top right pixels join B, and the center is now one step from the top middle pixel of B, but still two steps from A, so it changes from W to B. At level 3, the top left pixel joins B, and the left pixel of row 2 touches A and the center pixel of B, so it is a watershed pixel. The Vincent-Soille algorithm keeps the center pixel as W, because it only floods the pixels of the current level.

**An empty level.** Take the image with rows $(0, 1, 0)$ and $(2, 2, 9)$, which has no pixels at levels 3 to 8. A is the top left zero and B the top right zero. At level 1, the top middle pixel touches both and gets W. At level 2, the bottom left pixel joins A, and the bottom middle pixel is two steps from A and two from B, so it gets W. Level 3 is empty, but A has grown: the bottom middle pixel is now one step from A and two from B, so it joins A. At level 9, the bottom right pixel touches A (the bottom middle pixel) and B (the pixel above it), so it is a watershed pixel. If the 9 is changed to a 3, there is no empty level, the bottom middle pixel is still W when the 3 is flooded, and the bottom right pixel is one step from B and two from A, so it joins B. The two images order their pixels in the same way, but the gap in the gray values gives them different watersheds.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that before each pass, the basin pixels are exactly $X_{h-1}$ and the W-set is exactly $T_{h-1} \setminus X_{h-1}$, so $Q$ at line L4 is $T_h \setminus X_{h-1}$. A shortest path from a pixel of $Q$ to the nearest basin passes only through pixels of $Q$ before its last step, so the search from the pixels next to a basin gives the true geodesic distance in $T_h$, and the label sets built layer by layer are exactly the sets of nearest basins. Basin pixels are at distance 0 from their own basin, so they stay. Pixels of $Q$ that no basin reaches are the regional minima at level $h$. Skipping a level with no pixels after a pass that changed nothing is safe, because the next pass would get the same input and return it again. The tests compare the implementation with a direct computation of Definition 3.2 over every integer level, with one breadth-first search per basin inside the whole threshold set, on random images with 4- and 8-connectivity, and with the figure of Roerdink and Meijster. For the marker flood, they check that each pixel's label is a marker with the least possible highest value on a path, which is the minimax property of a minimum spanning forest.

## Complexity

- Line L1 groups the pixels in $O(N + G)$ time.
- Line L2 runs over $G$ levels. A pass with no new pixels runs only if the last pass changed a label, and each such change moves a W pixel into a basin for good, so there are at most $2N$ passes that do work.
- A pass costs $O(|P| + |W\text{-set}|)$ for a fixed neighborhood.

If the W-set stays small, the total is $O(N + G)$. In the worst case the W-set has $\Theta(N)$ pixels and is recomputed at $\Theta(N)$ passes, which gives $O(N^2 + G)$. Roerdink and Meijster note this: the exact version is quadratic, the Vincent-Soille algorithm is linear, and in practice the number of W pixels is often small. The marker flood pushes each pixel at most once per neighbor, so it takes $O(N \log N)$ time with a binary heap, or $O(N + G)$ with one queue per gray level. Both use $\Theta(N)$ extra space.

## Properties

- **One basin per minimum.** Every regional minimum of $f$ starts exactly one basin, and every basin contains exactly one minimum. With markers, every region contains its marker.
- **Thick lines are possible.** A W pixel is any pixel equally far from two nearest basins. On plateaus, the lines can be two pixels wide or form small blobs, and they depend on the connectivity.
- **Oversegmentation.** Every small dip in the image starts its own basin. On a noisy gradient this gives hundreds of regions where a few are wanted. Markers fix this.
- **Lines can be missing.** Two basins can touch with no W pixel between them. In the row $(0, 1, 1, 0)$ each 1 is one step from its own zero and two from the other, so the result is A A B B: the meeting point falls between two pixels.
- **Minimax paths.** With markers, a pixel goes to a marker whose best path to it has the lowest possible highest point. This links the watershed with the [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/) and with single linkage clustering.

## Variants and improvements

- **Vincent and Soille.** Sort the pixels, and at each level flood only the new pixels with a FIFO queue, propagating basin and watershed labels. It is linear and widely used, but Roerdink and Meijster show that it does not compute Definition 3.2, and they could not find a recursion that it does compute.
- **Flooding from markers (Meyer).** A priority queue floods from given markers, as described above, with no watershed lines or with lines where two floods meet. This is the version in most libraries.
- **Topographical distance.** Another definition takes the basin of a minimum as the set of pixels closer to it than to any other minimum under a distance that integrates the slope of $f$. It is computed by shortest paths, as in [Dijkstra's algorithm](/dijkstra/), and does not always agree with the immersion definition.
- **Watershed on a graph.** Defined on a graph with edge weights, the watershed becomes a minimum spanning forest, and the flood is [Prim's algorithm](/prim/) or [Kruskal's algorithm](/kruskal/) with markers.
- **Marker choice.** Markers come from a user, from [thresholding](/image-thresholding/), from the regional maxima of a [distance transform](/distance-transform/) to separate touching round objects, or from minima that are deeper than a given height (h-minima).
- **Merging basins.** Build the region adjacency graph of the basins and merge the pair with the lowest saddle until the wanted number of regions is left.

## When to use it

Use the watershed when the objects are separated by ridges in some image, a gradient or a distance map, and you can supply one marker per object. The classical case is touching round objects such as cells or coins: threshold them, take the distance transform, put a marker at each peak, and flood the negated distance, which cuts the blob at its necks. With good markers, it gives closed boundaries that follow the ridges, in near-linear time. Without markers, use it only after strong smoothing or as a first step that is followed by merging. Use [region growing](/region-growing/) when the regions are uniform in value and the seeds are known, [Felzenszwalb segmentation](/felzenszwalb-segmentation/) when no markers are known, and [GrabCut](/grabcut/) when one object must be cut out with color models.

## Pitfalls

- **Raw gradients.** Flooding a noisy gradient without markers gives one region per noise dip. Smooth the image first, or use markers.
- **The definition and the common algorithm differ.** The Vincent-Soille algorithm and the definition can give different watershed lines, as in the example. If exact results matter, say which one you mean.
- **Gaps in the gray values.** The recursion runs over every integer level, and the extra passes at empty levels can move tie pixels into basins. Stretching the gray values can change the lines.
- **Plateaus.** On flat areas the distance inside the plateau decides, and the result depends on the connectivity and on the tie rule. Thick or odd lines are common.
- **Lines or no lines.** The marker flood gives a partition with no lines, and the immersion gives lines. Code that expects one format and gets the other miscounts the regions.
- **Floating-point images.** The recursion steps through integer levels. Quantize first, or use the marker flood, which only compares values.

## Implementations

## History

Serge Beucher and Christian Lantuéjoul introduced watersheds into image analysis in 1979, at a workshop in Rennes, as a tool for contour detection, using ideas from mathematical morphology at the École des Mines de Paris. Luc Vincent and Pierre Soille published the definition by immersion and their sorted-pixel, queue-based algorithm in 1991 in IEEE Transactions on Pattern Analysis and Machine Intelligence, and it became the standard implementation. Fernand Meyer and Beucher developed the use of markers to control the oversegmentation, and Meyer gave the priority-queue flood and the definition by topographical distance. In 2000 Jos Roerdink and Arnold Meijster surveyed the definitions and algorithms, showed that the Vincent-Soille algorithm does not compute its own recursion, and described how to change it to do so, at quadratic worst-case cost.

## References
