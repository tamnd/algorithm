---
tag: PA7FJM
kind: algorithm
slug: zhang-suen-thinning
name: Zhang-Suen thinning
aliases:
- Zhang-Suen skeletonization
area: graphics-and-signals/image-processing
level: advanced
summary: Parallel thinning that peels the boundary of a binary shape in two subiterations, from 3 by 3 neighborhoods, until a curve one pixel wide is left.
solves: [image-skeletonization]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, T: "the number of iterations, at most n + 1", n: the number of foreground pixels}
  time: {worst: Θ(W H T)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: true, exact: true, linear: false, parallel: true}
prereqs: [image-skeletonization, digital-image, connected-components]
see_also: [hit-or-miss-transform, medial-axis, distance-transform, mathematical-morphology, connected-component-labeling, morphological-erosion]
sources:
  - paper: doi:10.1145/357994.358023
    title: T. Y. Zhang and C. Y. Suen, A fast parallel algorithm for thinning digital patterns, Communications of the ACM 27(3), 236 to 239, 1984
    locator: the whole paper (the two subiterations, the conditions on B and A, and the examples)
  - paper: doi:10.1145/5666.5670
    title: H. E. Lü and P. S. P. Wang, A comment on "A fast parallel algorithm for thinning digital patterns", Communications of the ACM 29(3), 239 to 242, 1986
    locator: the whole paper (the loss of diagonal lines two pixels thick, and the change of the lower bound on B to 3)
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 5, Hit-or-miss and Skeletons (thinning, simple points and homotopic skeletons)
---

Zhang-Suen thinning reduces a binary shape to a curve about one pixel wide near its middle. It deletes boundary pixels in parallel, in iterations of two subiterations: the first deletes pixels on the south and east sides and north-west corners, the second those on the north and west sides and south-east corners. Each test looks only at the 8 neighbors of a pixel, through two numbers: $B$, the count of foreground neighbors, and $A$, the count of background to foreground steps around them. Zhang and Suen published it in 1984. It is simple and fast, but it is not safe on every shape: a 2 by 2 square vanishes completely, and diagonal lines two pixels thick are destroyed.

## In plain words

Think of the white shape as a field of grass and burn it from the edges inward, one ring of pixels at a time, but never burn a pixel that holds the shape together. A pixel on the edge may go if its white neighbors form one unbroken group around it, if it has at least two white neighbors (so the ends of lines stay), and if it is not buried inside (at most six white neighbors).

To keep the result in the middle, each round has two halves. The first half burns only on the bottom and right sides, the second half only on the top and left sides. All pixels chosen in one half go at the same moment. Stop when a whole round burns nothing. What is left is a thin line that follows the middle of each part of the shape.

## The problem

The input is a binary image $X$ with $W$ columns and $H$ rows, the pixel centers at the integer points and $y$ growing downward; the pixels outside the image are background. The foreground uses 8-adjacency and the background 4-adjacency. The goal is the problem of [image skeletonization](/image-skeletonization/): a subset of $X$ that is thin (about one pixel wide), that keeps the shape's connected parts and holes, and that lies near the middle of the shape. Zhang-Suen meets the first goal and, on most shapes, the other two. The neighbors of a pixel $P_1$ are named clockwise from the north:

```text
P9  P2  P3
P8  P1  P4
P7  P6  P5
```

$B(P_1) = P_2 + P_3 + \dots + P_9$ counts the foreground neighbors. $A(P_1)$ counts the places where a 0 is followed by a 1 in the circular sequence $P_2, P_3, \dots, P_9, P_2$. $A = 1$ says that the foreground neighbors form a single unbroken arc around $P_1$.

## The algorithm

```pseudo id=main
ZHANG-SUEN(X, W, H)               ▷ COND(1): P2·P4·P6 = 0 and P4·P6·P8 = 0
                                   ▷ COND(2): P2·P4·P8 = 0 and P2·P6·P8 = 0
L1   repeat
L2       changed ← false
L3       for step ← 1 to 2 do
L4           M ← empty list
L5           for each foreground pixel P1 do
L6               B ← P2 + P3 + ... + P9;  A ← number of (0, 1) pairs in P2, P3, ..., P9, P2
L7               if 2 ≤ B ≤ 6 and A = 1 and COND(step) then append P1 to M
L8           for each P1 in M do X[P1] ← 0; changed ← true
L9   until not changed
L10  return X
```

Line L5 reads the image as it was at the start of the subiteration: line L8 deletes only after the scan, so the order of the scan does not matter and the pixels of a subiteration can be tested in parallel. At line L7, $B \ge 2$ keeps the end pixels of lines, $B \le 6$ keeps pixels that would open a hole, and $A = 1$ keeps the pixels whose removal would cut the shape. COND(1) holds exactly when $P_4 = 0$ or $P_6 = 0$ or ($P_2 = 0$ and $P_8 = 0$): the east or south neighbor is background, or the pixel is a north-west corner. COND(2) holds exactly when $P_2 = 0$ or $P_8 = 0$ or ($P_4 = 0$ and $P_6 = 0$). Splitting the directions keeps a strip two pixels thick from losing both of its sides in the same subiteration.

## Example

A 7 by 4 block of 28 pixels in a 9 by 6 image:

```text
start                 iteration 1, step 1   iteration 1, step 2   iteration 2, step 1
. . . . . . . . .     . . . . . . . . .     . . . . . . . . .     . . . . . . . . .
. # # # # # # # .     . . # # # # # . .     . . . . . . . . .     . . . . . . . . .
. # # # # # # # .     . # # # # # # . .     . . # # # # # . .     . . . # # # . . .
. # # # # # # # .     . # # # # # # . .     . . # # # # . . .     . . . . . . . . .
. # # # # # # # .     . . . . . . . . .     . . . . . . . . .     . . . . . . . . .
. . . . . . . . .     . . . . . . . . .     . . . . . . . . .     . . . . . . . . .
```

The first subiteration deletes 11 pixels: the bottom row and the right column, where $P_6 = 0$ or $P_4 = 0$, and the north-west corner $(1, 1)$, where $P_2 = P_8 = 0$. Of the top row only the two end pixels go: $(1, 1)$ is the north-west corner and $(7, 1)$ has $P_4 = 0$. The pixel $(2, 1)$ has $P_4 = P_6 = P_8 = 1$, so its condition fails. The second subiteration deletes 8 pixels on the top and left and the new south-east corner. The second iteration deletes 6 more, and the third deletes nothing. The result is the 3-pixel line $(3, 2), (4, 2), (5, 2)$, in 3 iterations of which the last only confirms.

The 2 by 2 square shows the known defect. Each of its four pixels has $B = 3$ and $A = 1$, and each has $P_4 = 0$ or $P_6 = 0$, so all four are marked in the first subiteration and the square vanishes. A diagonal line two pixels thick loses almost all of its pixels in the same way; a staircase of 10 pixels from $(0, 0)$ to $(5, 4)$ ends as 2 pixels.

## Correctness

The proof below shows three things. The algorithm stops after at most $n + 1$ iterations, because each iteration but the last deletes a pixel. The output is a subset of the input and is a fixed point of both subiterations. And a pixel that passes the test of line L7 is simple: deleted alone, it changes neither the number of 8-connected components of the foreground nor the number of 4-connected components of the background, so it neither cuts the shape nor opens or closes a hole. The reason is that $A = 1$ and $2 \le B \le 6$ make the foreground neighbors one arc and the background neighbors one arc of length at least 2, which always holds a north, south, east or west neighbor.

The proof also shows the limit of that guarantee. The simplicity holds for one deletion at a time, but line L8 deletes many pixels at once. The 2 by 2 square is the counterexample: four pixels that are each simple are deleted together, and a component disappears.

## Complexity

- **Time per iteration.** Each subiteration reads the 8 neighbors of every foreground pixel: $\Theta(WH)$.
- **Number of iterations.** Each iteration but the last deletes at least one pixel, so $T \le n + 1$, which gives $O(WHn)$ in the worst case. On solid shapes each iteration peels about one layer from each side, so $T$ is about half of the largest thickness. For a $k \times k$ square with $k \ge 2$ the algorithm runs $\lfloor k/2 \rfloor + 1$ iterations, the last of which deletes nothing; it leaves one pixel for $k \ge 3$.
- **Space.** The list $M$ of marked pixels holds at most $n$ entries; with a second image instead of a list, $\Theta(WH)$.
- **Faster in practice.** The test at line L7 depends only on the 8 neighbors, so it is one lookup in a table of $2^8 = 256$ entries per step. Testing only the pixels next to a pixel deleted in the previous subiteration cuts the work of an iteration from $\Theta(WH)$ to the size of the current boundary.

## Properties

- **Parallel.** All the tests of a subiteration read the same image, so they can run in any order or at the same time, on a GPU or with bit planes.
- **Ends of lines stay.** A pixel with $B = 1$ is never deleted, so a line one pixel wide keeps its length and the arms of a shape stay as branches. The arms of a thick shape can still shorten: the stem of a T shape three pixels wide loses two pixels at its free end.
- **Thin lines stay whole.** A line one pixel wide has $A = 2$ at its inner pixels, so the algorithm leaves it unchanged.
- **Subset and fixed point.** The output is part of the input, and running the algorithm on its own output changes nothing.
- **Not topology preserving in all cases.** The 2 by 2 square disappears, and two pixel thick diagonals break up. On larger shapes the result usually keeps the components and holes; a ring stays a closed curve.
- **Not minimal.** At a right-angle turn the output can keep the corner pixel, with its east and south neighbors in the curve and its south-east neighbor not. That pixel has $A = 2$, so it stays, although the curve would stay 8-connected without it. A thick square ring, thinned, keeps three of its four corners this way.
- **Not rotation invariant.** Step 1 favors the north-west and step 2 the south-east; turning the input by a quarter turn can change the output by a pixel.

## Variants and improvements

- **Lü and Wang (1986).** They report the destruction of diagonal lines two pixels thick and change the lower bound to $3 \le B \le 6$, which keeps such lines. The four pixels of the 2 by 2 square still have $B = 3$, so the change does not save the square.
- **Other two-subiteration algorithms.** Guo and Hall (1989) and later authors changed the conditions to control which sets of pixels a subiteration can delete together, so that the parallel deletions keep the connectivity that each single deletion keeps.
- **Sequential thinning.** Delete simple pixels one at a time, in a fixed order, as in the method of Hilditch. Topology is then always kept, by the simple pixel test of the proof, but the result depends on the scan order.
- **Thinning by hit-or-miss templates.** Repeat a thinning by the 8 turned templates of an edge and a corner, each with the [hit-or-miss transform](/hit-or-miss-transform/). This is a morphological thinning that can be made to keep the topology.
- **Skeletons from the distance transform.** Compute a [distance transform](/distance-transform/) and keep its ridges, the local maxima across the shape. These skeletons are closer to the [medial axis](/medial-axis/) and allow the shape to be rebuilt; see [image skeletonization](/image-skeletonization/).

## When to use it

Use Zhang-Suen to get a quick centerline of clean binary shapes such as handwritten characters, line drawings, road or vessel masks and fingerprints, when a few pixels of error are acceptable and the shapes have no parts two pixels thick. Smooth or open the mask first so that small spurs and holes do not become branches and loops. If the topology must be exact, for example for a graph of a road network, use an algorithm with a proven guarantee or check the result with [connected component labeling](/connected-component-labeling/). If the skeleton must be centered exactly or must allow reconstruction, use a skeleton from the distance transform.

## Pitfalls

- **Deleting during the scan.** If line L8 deletes each pixel as soon as it is marked, the later tests of the same subiteration see a changed image, and the result depends on the scan order. Mark first, delete after.
- **The order of the ring.** $P_2$ to $P_9$ go clockwise from the north. With $y$ growing upward, or counterclockwise names, COND(1) and COND(2) refer to other sides, and the result changes.
- **Counting $A$ without the wrap.** The sequence for $A$ ends with $P_2$ again. Without it, an arc that starts at $P_2$, such as $1, 1, 0, 0, 0, 0, 0, 0$, gives $A = 0$ instead of 1, and the pixel is never deleted.
- **Image border.** Treat the pixels outside the image as background, or pad the image by one pixel. A shape that touches the border is thinned as if it were cut there.
- **Thin parts two pixels wide.** They can vanish or break, as the 2 by 2 square shows. Upsample the image or use a variant if the input has such parts.
- **Noise.** Each bump on the boundary of the shape becomes a branch. Prune short branches after thinning, or smooth before.

## Implementations

## History

T. Y. Zhang and C. Y. Suen published the algorithm in the Communications of the ACM in March 1984 as a fast parallel method for thinning digital patterns such as characters. Two years later Lü and Wang showed that it destroys diagonal lines two pixels thick and proposed the change of the lower bound on $B$. The algorithm became one of the most used thinning methods because it is short, needs only the 3 by 3 neighborhood and runs in parallel, and later work on parallel thinning, such as Guo and Hall's, set out to keep its speed while fixing its defects.

## References
