---
tag: XZM37W
kind: algorithm
slug: octree-color-quantization
name: Octree color quantization
aliases:
- octree quantizer
area: graphics-and-signals/image-processing
level: advanced
summary: Insert each pixel color into an octree of the RGB cube and, whenever it has more than k leaves, merge a deepest node into one leaf; the leaf means are a palette of at most k colors.
solves: [color-quantization]
model: word-ram
complexity:
  vars: {n: the number of pixels, k: the palette size, b: the depth of the tree (one level per binary digit of a channel)}
  time: {worst: O(n b k), average: O(n b k), best: Θ(n b)}
  space: {extra: Θ(k b)}
properties: {deterministic: true, exact: false, heuristic: true, online: true, bounded_memory: true}
history:
  year: 1988
  people: [Michael Gervautz, Werner Purgathofer]
  note: Gervautz and Purgathofer presented octree quantization at Computer Graphics International 1988, as a palette method whose memory depends on the palette size and not on the number of colors of the image.
prereqs: [color-quantization, octree]
see_also: [median-cut, k-means, vector-quantization, floyd-steinberg-dithering, ordered-dithering, trie, k-means-problem, scalar-quantization]
sources:
  - paper: doi:10.1007/978-3-642-83492-9_20
    title: Michael Gervautz and Werner Purgathofer, A simple method for color quantization, octree quantization, in New Trends in Computer Graphics (Proceedings of CG International 1988), Springer, 1988, 219 to 231
    locator: the whole paper (the octree of the RGB cube, the insertion of colors, the reduction of the tree and the mapping of pixels)
  - paper: doi:10.1145/965145.801294
    title: Paul Heckbert, Color image quantization for frame buffer display, ACM SIGGRAPH Computer Graphics 16(3), 1982, 297 to 307
    locator: the statement of the color quantization problem and the median cut algorithm, which the octree method is compared with
  - paper: doi:10.1145/146443.146475
    title: Xiaolin Wu, Color quantization by dynamic programming and principal analysis, ACM Transactions on Graphics 11(4), 1992, 348 to 372
    locator: the review of earlier quantizers, including the octree method, and their errors
---

Octree color quantization makes a palette of at most $k$ colors for an image with an [octree](/octree/) of the RGB cube. The root is the whole cube, and each node splits its cube into 8 equal subcubes by the next binary digit of red, green and blue, so a path from the root is a prefix of the binary form of a color. The algorithm inserts the pixel colors one at a time, keeping a pixel count and a color sum in each leaf. Whenever the tree has more than $k$ leaves, it merges the children of a node at the deepest level into that node. The palette is the mean color of each leaf. The tree never holds more than about $k$ times the depth nodes, whatever the size of the image, but the palette can have fewer than $k$ colors, and the result is a heuristic for the [color quantization](/color-quantization/) problem.

## In plain words

Think of the color cube as a box. Cut it into 8 smaller boxes by halving red, green and blue, then cut each of those into 8, and so on, eight times for 8-bit colors. Each pixel color falls into one smallest box. Now read the image one pixel at a time and keep a tally in the boxes that have been used. If more boxes are in use than the palette can hold, take a group of small boxes with the same parent and pour their tallies into the parent box. The deepest and least used groups are merged first. At the end, each box in use gives one palette color, the average of the pixels in it. The work for one pixel is small, and the memory stays small for a huge image.

## The problem

The input is a list of $n$ colors, one per pixel, each a triple $c = (c_1, c_2, c_3)$ of red, green and blue integers in $[0, 2^b)$, usually with $b = 8$, and a palette size $k \ge 1$. The output is a palette of $k' \le k$ colors and an index for each pixel. The quality is the total squared error $\sum_i |c_i - p_{j(i)}|^2$, as on the [color quantization](/color-quantization/) page; the algorithm does not minimize it.

A node at level $\ell$ (the root is level 0) stands for the cube of colors whose first $\ell$ binary digits in each channel are fixed. Its child index for a color $c$ is

$$
i_\ell(c) = 4\,\mathrm{digit}_{b - 1 - \ell}(c_1) + 2\,\mathrm{digit}_{b - 1 - \ell}(c_2) + \mathrm{digit}_{b - 1 - \ell}(c_3),
$$

where $\mathrm{digit}_s(x) = \lfloor x / 2^s \rfloor \bmod 2$. Nodes at level $b$ are single colors.

## The algorithm

```pseudo id=main
OCTREE-QUANTIZE(c₁ … cₙ, k, b)
L1  for each pixel color c do
L2      v ← the root
L3      while v is not a leaf do
L4          v ← child i_level(v)(c) of v, created if missing (as a leaf at level b)
L5      count(v) ← count(v) + 1;  sum(v) ← sum(v) + c
L6      while the tree has more than k leaves do
L7          u ← a node with children at the deepest such level, with the fewest pixels below it
L8          count(u) ← the sum of the counts of its children;  sum(u) ← the sum of their sums
L9          delete the children of u and make u a leaf
L10 p ← sum(v) / count(v) for each leaf v
L11 for each pixel, descend from the root to its leaf v and give it the index of v
```

A node at the deepest level that has children has only leaves as children, so line L9 removes only leaves. A merge of a node with $m$ children lowers the number of leaves by $m - 1$, which is 0 when $m = 1$: such a merge only shortens a chain. Line L4 stops at a leaf that a merge made, so later colors in that cube go straight into it. The choice in line L7 among the nodes at the deepest level differs between implementations; the fewest pixels, with ties to the first node in child order, is the rule of the implementation here.

## Example

**Three far colors, k = 2.** Insert black $(0, 0, 0)$, red $(255, 0, 0)$ and green $(0, 255, 0)$. They differ in the first digit, so each has its own child of the root and a chain of single children down to level 8. After the third insertion there are 3 leaves. Lines L7 to L9 merge the 7 chain nodes of each color from level 7 up to level 1 (21 merges that do not lower the count), and then the root, which has 3 children. The tree is one leaf, and the palette is one color, $(85, 85, 0)$, with an error of $14450 + 36125 + 36125 = 86700$. The best palette of 2 colors puts two of the three together and has an error of $65025/2$. So the palette has fewer than $k$ colors.

**Neighbors across a digit, k = 2.** For the reds $0$, $127$ and $128$, the colors 127 and 128 differ in the first digit, so the root keeps them apart, and 0 and 127 share the child $0$ of the root and are merged. The palette is $(127/2, 0, 0)$ and $(128, 0, 0)$ with an error of $16129/2$, while the best palette, $\{0\}$ and $\{127, 128\}$, has an error of $1/2$. The ratio is $16129 = 127^2$; with $b$ levels and the reds $0$, $2^{b-1} - 1$, $2^{b-1}$, it is $(2^{b-1} - 1)^2$.

**A far outlier.** For the reds $0, 1, 2, 3, 100$ with $k = 2$, the color 100 differs from the others in the second digit (64), so it is in another cube from level 2 down, and the result is the best palette $(3/2, 0, 0)$ and $(100, 0, 0)$ with an error of 5, where [median cut](/median-cut/) has an error of 4234.

On 200 random images of 3 to 8 pixels with values in $[0, 16)$ and $k \in \{2, 3\}$, chosen with seed 8, the octree palette was strictly worse than the best palette on 166, and it had fewer than $\min(k, D)$ colors on 156, where $D$ is the number of distinct colors. For 5000 random colors in the full cube and $k = 16$, it gave 15 colors.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts. First, after each pass of lines L2 to L9, every leaf holds the number and the sum of exactly the inserted colors in its cube, and every inserted color reaches a leaf by descent. Second, after each pass the tree has at most $k$ leaves and at most $k(b + 1)$ nodes. Third, the palette has between 1 and $k$ colors, it has exactly the distinct colors with no error when there are at most $k$ of them, and each pixel maps to a mean that lies in the same cube as the pixel. Fourth, the error is at least that of the best palette, and the examples above show a palette with fewer than $k$ colors and a ratio of $(2^{b-1} - 1)^2$.

## Complexity

- **Insertion.** Lines L2 to L5 visit at most $b + 1$ nodes, so all insertions cost $\Theta(n b)$ in the [word RAM](/word-ram/), where a child index takes $O(1)$ word operations.
- **Merges.** Each merge deletes at least one node, and each insertion creates at most $b$ nodes, so there are at most $n b$ merges over the whole run. Keep a list of the nodes with children for each level. Then a merge that takes any node of the deepest list costs $O(1)$, and the total time is $\Theta(n b)$. Choosing the node with the fewest pixels scans a list of at most $k + 1$ nodes, so the worst case is $O(n b k)$; a heap per level brings it to $O(n b \log k)$.
- **Mapping.** Line L11 costs $O(b)$ per pixel, with no search over the palette.
- **Space.** By the second fact, the tree has at most $k(b + 1)$ nodes after each insertion, so the extra space is $\Theta(k b)$, which does not grow with $n$ or with the number of distinct colors. The implementation here finds the deepest nodes by a walk of the tree, which costs $O(k b)$ per merge instead.

## Properties

- **Bounded memory.** The tree has $O(k b)$ nodes at all times, so the method can read an image as a stream.
- **One pass.** Each pixel is read once to build the palette and once to map it.
- **Fixed cells.** The cells are the cubes of the octree, fixed in advance, so two near colors on the two sides of a large cube boundary stay apart, as in the example with 127 and 128.
- **At most k colors.** The palette can be smaller than $k$, because one merge can remove up to 7 leaves.
- **Order dependent.** The online merges depend on the order of the pixels, so two orders of the same image can give two palettes.

## Variants and improvements

- **Fill the palette.** After the last merge, split back the most populous leaves, or merge nodes with fewer children first, so that the palette has close to $k$ colors.
- **Offline reduction.** Insert all colors first and reduce at the end, which removes the dependence on the order at the cost of memory for all distinct colors.
- **Choice of the merged node.** Merge the node whose merge adds the least squared error, instead of the one with the fewest pixels; the error of a merge follows from the counts and sums, with a sum of squares per node.
- **Shallower tree.** Limit the depth to 5 or 6 levels, which is a uniform [scalar quantization](/scalar-quantization/) of each channel before the octree, as in histogram-based quantizers.
- **Refinement.** Use the octree palette as the start of [k-means](/k-means/) iterations, and map pixels to the nearest palette color instead of their leaf.
- **Dithering.** Combine with [Floyd-Steinberg dithering](/floyd-steinberg-dithering/), using the octree palette and a nearest-color search, since the diffused error moves colors out of their cells.

## When to use it

Use octree quantization when the image is large or comes as a stream and memory must stay bounded, or when a palette is needed in one pass with a cost of a few operations per pixel. Its mapping by descent is also fast. Use [median cut](/median-cut/) when the palette must have exactly $k$ colors and the colors fit in memory, and refine either with k-means when the error matters more than the time.

## Pitfalls

- **Fewer than k colors.** A merge of a node with many children can drop the leaf count well below $k$; do not assume that the palette has $k$ entries.
- **Chains of single children.** A merge of a node with one child does not lower the count of leaves; a loop that expects every merge to make progress in the count can stop too early or not at all if it skips them.
- **Mapping after dithering.** A color changed by error diffusion may descend to a missing child. Use a nearest-color search, or stop at the last existing node and take any leaf below it.
- **Bit order.** The child index must use the most significant digit at the root. Using the least significant first gives cells that are not cubes of near colors.
- **Integer means.** Rounding the leaf means can make two palette colors equal.

## Implementations

## History

Gervautz and Purgathofer presented octree quantization at Computer Graphics International in 1988, with the proceedings published by Springer as New Trends in Computer Graphics. The method took the subdivision of the RGB cube from the octree and bounded the memory by the palette size, in contrast to [median cut](/median-cut/) (Heckbert 1982), which works on a histogram of all colors. A shorter description of the same method by the same authors appeared in the first Graphics Gems book in 1990.

## References
