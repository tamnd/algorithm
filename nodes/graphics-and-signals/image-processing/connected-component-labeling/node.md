---
tag: FCV9GC
kind: algorithm
slug: connected-component-labeling
name: Connected component labeling
aliases:
- two-pass labeling
- blob labeling
- Rosenfeld-Pfaltz labeling
area: graphics-and-signals/image-processing
level: advanced
summary: Label the connected foreground regions of a binary image in two raster passes, recording label equivalences in a union-find forest, in O(N α(N)) time.
solves: [image-labeling]
model: word-ram
complexity:
  vars: {N: the number of pixels}
  time: {worst: O(N α(N)), average: O(N α(N)), best: Θ(N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, exact: true, raster_order: true, two_pass: true, uses_union_find: true}
history:
  year: 1966
  people: [Azriel Rosenfeld, John L. Pfaltz]
  note: Rosenfeld and Pfaltz described the sequential two-pass labeling of connected components, with equivalences between provisional labels recorded in the first pass and resolved before the second, in the Journal of the ACM in 1966.
prereqs: [image-labeling, disjoint-set]
see_also: [image-labeling, flood-fill, disjoint-set-forest, union-find-connectivity, connected-components, image-thresholding, image-moments, inverse-ackermann-function]
sources:
  - paper: doi:10.1145/321356.321357
    title: Azriel Rosenfeld and John L. Pfaltz, Sequential operations in digital picture processing, Journal of the ACM 13(4), 471 to 494, 1966
    locator: the sequential labeling of connected components (with the table of label equivalences), and the sequential distance computation
  - paper: doi:10.1145/321556.321570
    title: Azriel Rosenfeld, Connectivity in digital pictures, Journal of the ACM 17(1), 1970
    locator: the use of opposite connectivities for a set and its complement, and the results on surrounding and holes
  - paper: doi:10.1007/s10044-008-0109-y
    title: Kesheng Wu, Ekow Otoo and Kenji Suzuki, Optimizing two-pass connected-component labeling algorithms, Pattern Analysis and Applications 12(2), 117 to 135, 2009
    locator: the decision tree for the scan of the neighbors, and the array-based union-find
  - paper: doi:10.1016/j.patcog.2017.04.018
    title: Lifeng He, Xiwei Ren, Qihang Gao, Xiao Zhao, Bin Yao and Yuyan Chao, The connected-component labeling problem, a review of state-of-the-art algorithms, Pattern Recognition 70, 25 to 43, 2017
    locator: the survey of two-pass, run-based, contour-tracing and parallel labeling methods
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 19, Data structures for disjoint sets (union by rank, path compression, and the O(m α(n)) bound)
  - paper: doi:10.1145/62.2160
    title: Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2), 245 to 281, 1984
    locator: the bounds for linking by rank with path compression, path splitting and path halving
---

Connected component labeling gives each connected region of foreground pixels in a binary image its own number, and gives the background the number 0. The two-pass method reads the image twice in raster order. In the first pass each foreground pixel takes a provisional label from a neighbor that the scan has already visited, or a new label if it has none, and whenever two of those neighbors carry different labels, the method records that the two labels name the same region. Rosenfeld and Pfaltz kept these equivalences in a table; the standard modern form stores them in a [disjoint-set forest](/disjoint-set-forest/). Between the passes each class of equivalent labels gets one final number, and the second pass writes it into every pixel. With union by rank and path compression, the cost is $O(N \alpha(N))$ for $N$ pixels, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). The method solves the [image labeling](/image-labeling/) problem, and the choice of 4- or 8-connectivity is part of its input.

## In plain words

After thresholding, a picture is black and white, and the white pixels form blobs: letters, cells, coins. Labeling gives each blob its own number, so that later steps can count the blobs and measure each one. The method reads the picture row by row, like text. Each white pixel looks at its white neighbors that were already read (left and above). If there are none, it starts a new number. If there are some, it copies one of their numbers. Sometimes a pixel touches two blobs that were given different numbers, for example at the bottom of a letter U, whose two arms were numbered separately. The method writes down that the two numbers mean the same blob. In a second reading, it replaces every number by one chosen name for its group.

## The problem

The input is a binary [digital image](/digital-image/) $B$ of $W \times H$ pixels, $N = WH$, with $B(x, y) \in \{0, 1\}$, and a connectivity $c \in \{4, 8\}$. Two foreground pixels are adjacent if they share a side ($c = 4$) or a side or a corner ($c = 8$). A component is a maximal set of foreground pixels in which any two are joined by a path of adjacent foreground pixels; these are the [connected components](/connected-components/) of the graph whose nodes are the foreground pixels. The output is a label image $\ell$ with $\ell(p) = 0$ on the background and $\ell(p) \in \{1, \ldots, K\}$ on the foreground, such that two foreground pixels have the same label if and only if they are in the same component, and $K$ is the number of components. This implementation numbers the components in the raster order of their first pixel, which makes the output unique. Outside the image everything counts as background.

## The algorithm

```pseudo id=main
TWO-PASS-LABEL(B, c)                            ▷ c ∈ {4, 8}
L1  F ← an empty disjoint-set forest
L2  for y ← 0 to H − 1 do
L3      for x ← 0 to W − 1 do
L4          if B[y][x] = 0 then continue        ▷ lab[y][x] stays 0
L5          S ← labels of the foreground pixels among the scanned neighbors
                ▷ W and N if c = 4;  W, NW, N and NE if c = 8
L6          if S is empty then
L7              lab[y][x] ← MAKE-SET(F)         ▷ a new provisional label
L8          else
L9              lab[y][x] ← the first label of S
L10             for each b in S do UNION(F, lab[y][x], b)
L11 for each (x, y) with lab[y][x] ≠ 0, in raster order do
L12     r ← FIND(F, lab[y][x])
L13     if r has no final number then give r the next number, from 1
L14     lab[y][x] ← the final number of r
L15 return lab and the count of final numbers
```

The scanned neighbors at line L5 are exactly the neighbors of $(x, y)$ that come before it in raster order: the west neighbor and, in the row above, the north neighbor, plus the north-west and north-east neighbors for 8-connectivity. Every adjacent pair of foreground pixels is therefore looked at once, from its later pixel. Lines L1 to L10 are the first pass, and lines L11 to L15 are the second pass. The forest $F$ is a [disjoint-set](/disjoint-set/) structure with union by rank and path halving (a form of path compression).

## Example

Take the $6 \times 4$ image (row 0 on top):

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 | 1 | 0 |
| 2 | 1 | 1 | 1 | 1 | 1 | 0 |
| 3 | 0 | 0 | 0 | 0 | 0 | 1 |

With $c = 4$, row 0 has three foreground pixels with no scanned foreground neighbors, so they get the new labels 1, 2 and 3. Row 1 copies them from above. In row 2, the pixel at $x = 0$ takes 1 from above, and the pixels at $x = 1$ to $4$ take 1 from the west. At $x = 2$ the scanned neighbors carry 1 (west) and 2 (north), so line L10 calls UNION(1, 2), and at $x = 4$ it calls UNION(1, 3). The pixel at $(5, 3)$ has no scanned foreground neighbor in the 4-connected sense, so it gets the new label 4. The provisional labels are:

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 0 | 1 | . | 2 | . | 3 | . |
| 1 | 1 | . | 2 | . | 3 | . |
| 2 | 1 | 1 | 1 | 1 | 1 | . |
| 3 | . | . | . | . | . | 4 |

The forest holds the classes $\{1, 2, 3\}$ and $\{4\}$. The second pass writes 1 for the first class and 2 for the second, so the comb of 11 pixels is component 1 and the corner pixel is component 2, with $K = 2$.

With $c = 8$ the first three rows get the same provisional labels, and row 2 makes more union calls because the north-west and north-east neighbors are also scanned. At $(1, 2)$ the scanned labels are 1 (west), 1 (north-west) and 2 (north-east). The pixel at $(5, 3)$ now sees its north-west neighbor $(4, 2)$ with label 1 and copies it, so the whole image is one component, $K = 1$, of 12 pixels.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key fact is that after the first pass, two foreground pixels have provisional labels in the same class of $F$ if and only if they are in the same component. In one direction, every class of $F$ is built by unions of labels of adjacent pixels (line L10) and by copies from adjacent pixels (line L9), so by induction the pixels of one class form a connected set. In the other direction, for each adjacent pair of foreground pixels, the later one in raster order sees the earlier one at line L5, because the scanned neighbors are exactly the earlier neighbors, so the two labels end in one class after line L10. Along a path inside a component this links every pixel to every other. The second pass then gives one number to each class, which is one number per component, and the numbers are in the raster order of the first pixel of each component because the pass visits pixels in that order.

## Complexity

- The first pass reads each pixel once and at most four neighbors per pixel, so it makes at most $N$ MAKE-SET calls and at most $4N$ UNION calls, each of which does two FIND calls.
- The second pass makes one FIND per foreground pixel.

So there are $O(N)$ operations on a forest of at most $N$ elements. With union by rank and path compression or path halving, $m$ operations on $n$ elements take $O(m\, \alpha(n))$ time (Chapter 19 of CLRS proves it for path compression, and Tarjan and van Leeuwen for path halving), so the total is $O(N \alpha(N))$. The function $\alpha$ is at most 4 for any $N$ that fits in memory, so in practice the method is linear. On an all-background image it takes $\Theta(N)$. The label image and the forest take $\Theta(N)$ space. The number of provisional labels is at most $\lceil W/2 \rceil$ per row, because a new label needs a background pixel on the west, so the forest can be allocated with $\lceil W/2 \rceil H$ entries. A [flood fill](/flood-fill/) by breadth-first search gives the same labels in $\Theta(N)$ time without the $\alpha$ factor, but it jumps around in memory, and the two-pass method is usually faster on large images because it reads them sequentially.

## Properties

- **Exact.** The output is the unique labeling that the problem defines, with the stated numbering. It is not a heuristic.
- **Raster access.** Each pass reads the image in memory order, and the first pass needs only the current and the previous row of labels besides the forest, which suits hardware and streaming.
- **Connectivity is a parameter.** The same image can have different components under 4- and 8-connectivity, as the example shows.
- **Dual connectivity.** Use 8-connectivity for the foreground with 4-connectivity for the background, or 4 with 8. Then a simple closed curve of foreground pixels separates the background into exactly an inside and an outside, which is the digital form of the Jordan curve theorem, and the holes of a component are the background components that do not touch the border (Rosenfeld 1970). With the same connectivity for both, the four pixels around a single background pixel break this: under 4 and 4 they are four separate objects that still enclose a hole, and under 8 and 8 they form a closed ring whose inside leaks out through the corners.
- **Euler number.** With the dual pairs, the number of objects minus the number of holes equals the Euler number, which a count of $2 \times 2$ patterns of the zero-padded image gives: $(n_1 - n_3 - 2 n_d)/4$ for an 8-connected foreground and $(n_1 - n_3 + 2 n_d)/4$ for a 4-connected one, where $n_1$ and $n_3$ count the $2 \times 2$ windows with one and three foreground pixels and $n_d$ counts the windows with two foreground pixels on a diagonal.
- **Statistics on the fly.** Area, bounding box, sums for [moments](/image-moments/) and other additive features can be kept per provisional label and added together at each union, so the second pass is not needed when only the features are wanted.

## Variants and improvements

- **Fewer neighbor reads.** For 8-connectivity, if the north neighbor is foreground, every other scanned foreground neighbor is adjacent to it (west at a corner, north-west and north-east at a side), and their labels were already united with its label when the later pixel of each pair was scanned. So the pixel can copy the north label with no union and no further reads. Wu, Otoo and Suzuki turn such cases into a decision tree over the neighbors, and pair it with an array-based union-find.
- **Run-based labeling.** Label runs of consecutive foreground pixels in a row instead of single pixels, and union runs that overlap runs of the previous row. The number of union calls drops from the number of pixels to the number of runs.
- **Block-based labeling.** Treat $2 \times 2$ blocks as units for 8-connectivity. All foreground pixels of a block are 8-adjacent to each other, so one label per block suffices, and fewer provisional labels and unions are needed.
- **Contour tracing.** Follow the outer and inner boundaries of each component when they are first met, and fill the interior in the same scan. This also gives the boundaries and the holes.
- **Flood fill.** A [breadth-first search](/breadth-first-search/) or a stack-based [flood fill](/flood-fill/) from each unlabeled pixel is the simplest correct method and runs in $\Theta(N)$; it is the reference used by the tests.
- **Parallel labeling.** On GPUs, label propagation and union-find with atomic operations on tiles replace the sequential scan.
- **Gray and color images.** Label maximal connected sets of pixels with equal value (flat zones), or with a value difference below a bound, by changing the test at line L5.
- **Volumes.** In 3D the scanned neighbors are the earlier ones of the 6-, 18- or 26-neighborhood, and the same two passes work. The consistent pairs there are 6 with 26 and 26 with 6.

## When to use it

Use two-pass labeling to number the objects of a binary image before counting or measuring them: cells, particles, characters, defects. It is the right choice for large images, for hardware and for streams, because it reads the image in order. Use a flood fill when you need only the component of one seed pixel, or when the image is small and simplicity matters. Choose the connectivity on purpose: 8-connectivity keeps thin diagonal strokes in one piece, and 4-connectivity keeps two objects that touch only at a corner apart. Label the background with the other connectivity if holes matter.

## Pitfalls

- **Missing the north-east neighbor.** For 8-connectivity the scan must read the north-east pixel too. Without it, a stroke that goes down and to the left, like the image of "/", splits into many components.
- **Forgetting the union.** Copying the label of one neighbor without uniting the labels of the others is the classic bug. A U shape then gets two labels.
- **Wrong border handling.** Reading $x - 1$ at $x = 0$ or the row above at $y = 0$ wraps around in languages with negative indexing. Treat the outside as background.
- **Same connectivity for objects and holes.** Using 8 with 8 or 4 with 4 makes hole counts and Euler numbers inconsistent, as the ring of four diagonal pixels shows.
- **Too few labels.** The number of provisional labels can be much larger than the number of components (each tooth of a comb gets one), so size the forest by the bound $\lceil W/2 \rceil H$, not by a guess of the number of objects.
- **Deep recursion.** A recursive flood fill on a large component overflows the call stack. Use an explicit stack or queue, or the two-pass method.
- **Unstable numbering.** Libraries number components in different orders (raster order of the first pixel, or of the root label). Do not compare label values across libraries; compare the partitions.

## Implementations

## History

Azriel Rosenfeld and John Pfaltz described sequential operations on digital pictures in the Journal of the ACM in 1966, among them the labeling of connected components with two raster scans: the first pass assigns provisional labels and records which of them are equivalent, and the equivalences are resolved before the second pass relabels the picture. The same paper gave the sequential distance transform. Rosenfeld's 1970 paper on connectivity in digital pictures set out the rule of opposite connectivities for a set and its complement. The union-find structure for the equivalences, with the near-linear bound of Tarjan, became the standard way to store them. Later work reduced the number of neighbor reads with decision trees (Wu, Otoo and Suzuki), and labeled runs, blocks and contours instead of single pixels; He and coauthors surveyed these methods in 2017.

## References
