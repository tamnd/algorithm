---
tag: 9886BS
kind: algorithm
slug: seam-carving
name: Seam carving
aliases:
- liquid rescaling
area: graphics-and-signals/image-processing
level: advanced
summary: Narrow an image by removing, one at a time, a connected top-to-bottom path of pixels with the least energy, found by dynamic programming.
solves: [content-aware-resizing]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, k: the number of seams removed}
  time: {worst: Θ(k W H), average: Θ(k W H), best: Θ(k W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, optimal_single_seam: true, greedy_over_seams: true, heuristic: true}
history:
  year: 2007
  people: [Shai Avidan, Ariel Shamir]
  note: Avidan and Shamir introduced seams, the dynamic program for the cheapest seam, seam insertion and the transport map for the order of seams at SIGGRAPH 2007.
prereqs: [dag-dynamic-programming, digital-image, traceback]
see_also: [content-aware-resizing, image-resampling, dp-on-dag, directed-acyclic-graph, sobel-operator, poisson-image-editing, image-inpainting, image-segmentation-graph-cuts]
sources:
  - paper: doi:10.1145/1276377.1276390
    title: Shai Avidan and Ariel Shamir, Seam carving for content-aware image resizing, ACM Transactions on Graphics 26(3), article 10, 2007 (SIGGRAPH 2007)
    locator: Section 3, The Operator (seam definition, equation (1) for e1 and the recurrence for M); Section 4.2 (optimal order by the transport map T); Section 4.3 (image enlarging); Section 4.6 (object removal)
  - paper: doi:10.1145/1360612.1360615
    title: Michael Rubinstein, Ariel Shamir and Shai Avidan, Improved seam carving for video retargeting, ACM Transactions on Graphics 27(3), article 16, 2008 (SIGGRAPH 2008)
    locator: the section on forward energy, and the graph cut form for video
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Image processing (image warping and resizing)
---

Seam carving is a method for [content-aware resizing](/content-aware-resizing/) that makes an image one pixel narrower by removing a vertical seam: a path of pixels from the top row to the bottom row, one pixel per row, where each pixel is in the same column as the one above it or in a column next to it. The method gives each pixel an energy, usually the size of the local gradient, and removes the seam whose total energy is least. That seam is a shortest path in a [directed acyclic graph](/directed-acyclic-graph/), so a row-by-row [dynamic program](/dag-dynamic-programming/) finds it exactly in $\Theta(WH)$ time for a $W \times H$ image. To remove $k$ columns, the method removes $k$ seams one at a time and computes the energy again after each one, for $\Theta(kWH)$ time. Each seam is optimal for the image it is cut from, but the sequence of seams is greedy, so the result as a whole is a heuristic. Horizontal seams, which make the image lower, are the same method on the transposed image.

## In plain words

To make a photo narrower, scaling squeezes everything, and cropping cuts off the sides. Seam carving instead takes out a thin crooked line of pixels that runs from the top of the photo to the bottom. The line goes through the dullest part of the picture: sky, a smooth wall, still water. Pixels where the color changes fast, such as edges of faces and buildings, cost a lot, and the line avoids them. In each row the line can move at most one step left or right, so the two sides join again without a visible break. The cheapest line is found row by row: for each pixel, remember the cheapest way to reach it from the top. Then follow the cheapest path back up. Remove the line, and repeat until the photo is narrow enough.

## The problem

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels, with $I(x, y)$ the sample at column $x \in \{0, \ldots, W-1\}$ and row $y \in \{0, \ldots, H-1\}$, and a number $k$ with $0 \le k < W$. The pixel centers are at integer coordinates. The values are real numbers in any range; the method compares only energies, so gamma encoded and linear values both work, but they give different seams. A color image uses the sum of the energies of its channels. Each pixel gets an energy $e(x, y) \ge 0$. This page uses the $e_1$ energy of Avidan and Shamir with central differences and a clamp-to-edge border rule:

$$e(x, y) = |I(x+1, y) - I(x-1, y)| + |I(x, y+1) - I(x, y-1)|,$$

where an index outside the image is replaced by the nearest index inside. Other energies (a [Sobel](/sobel-operator/) magnitude, a saliency map, a mask that protects a face) plug into the same algorithm.

A vertical seam is a sequence $s = (s_0, \ldots, s_{H-1})$ of columns with $|s_y - s_{y-1}| \le 1$ for $y \ge 1$. It is 8-connected: each pixel touches the one above it by a side or a corner. Its energy is $E(s) = \sum_y e(s_y, y)$. Removing it deletes pixel $(s_y, y)$ from row $y$ and moves the pixels on its right one place left, so the result is a $(W-1) \times H$ image. The single-seam problem asks for a seam of least $E(s)$. The number of seams grows like $3^H$, so listing them is not practical: a $5 \times 4$ image has 95 seams, and a $5 \times 6$ image has 707.

## The algorithm

```pseudo id=main
SEAM-CARVE(I, k)                               ▷ remove k vertical seams
L1  repeat k times
L2      e ← ENERGY(I)                           ▷ e1 energy of the current image
L3      s ← MIN-VERTICAL-SEAM(e)
L4      I ← REMOVE-SEAM(I, s)                   ▷ width drops by one
L5  return I

MIN-VERTICAL-SEAM(e)                           ▷ e is W × H
L6  for x ← 0 to W − 1 do M[0][x] ← e[0][x]
L7  for y ← 1 to H − 1 do
L8      for x ← 0 to W − 1 do
L9          b ← the x' in {x − 1, x, x + 1} ∩ [0, W − 1] with least M[y − 1][x'], leftmost on a tie
L10         M[y][x] ← e[y][x] + M[y − 1][b];  P[y][x] ← b
L11 s[H − 1] ← the leftmost x with least M[H − 1][x]
L12 for y ← H − 1 down to 1 do s[y − 1] ← P[y][s[y]]
L13 return s
```

$M[y][x]$ is the least energy of a connected partial seam that starts in row 0 and ends at pixel $(x, y)$. Line L6 sets the first row, where a partial seam is one pixel. Lines L7 to L10 fill the rows from top to bottom: a partial seam that ends at $(x, y)$ passes through one of the at most three pixels above it, so the best one extends the best partial seam to one of them. $P$ stores that choice. Line L11 picks the cheapest end in the last row, and line L12 follows $P$ back to row 0, which is a [traceback](/traceback/). This is the shortest path problem in the graph whose nodes are pixels and whose edges go from each pixel to the up to three pixels below it, with weights on the nodes; rows give a topological order, so no priority queue is needed (see [DP on a DAG](/dp-on-dag/)).

The tie rule at lines L9 and L11 makes the output deterministic. Any other fixed rule also gives a seam of least energy.

## Example

Take this energy table, with $W = 5$ and $H = 4$ (row $y = 0$ on top):

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 2 | 4 | 3 | 5 | 1 |
| 1 | 3 | 2 | 5 | 2 | 3 |
| 2 | 5 | 2 | 4 | 2 | 1 |
| 3 | 2 | 3 | 1 | 9 | 9 |

Lines L6 to L10 give the cumulative table $M$:

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 2 | 4 | 3 | 5 | 1 |
| 1 | 5 | 4 | 8 | 3 | 4 |
| 2 | 9 | 6 | 7 | 5 | 4 |
| 3 | 8 | 9 | 6 | 13 | 13 |

For example $M[1][3] = 2 + \min(3, 5, 1) = 3$, with $P[1][3] = 4$, and $M[3][2] = 1 + \min(6, 7, 5) = 6$, with $P[3][2] = 3$. Line L11 finds the least value of the last row, 6 at $x = 2$. Line L12 follows $P$: $P[3][2] = 3$, $P[2][3] = 3$, $P[1][3] = 4$. The seam is $s = (4, 3, 3, 2)$ with energy $1 + 2 + 2 + 1 = 6$. It is the only seam of energy 6 among the 95 seams of this table.

A greedy walk that starts at the cheapest pixel of the top row and then steps to the cheapest of the pixels below does worse: it goes $(4, 3, 4, 3)$, because in row 3 it can only reach columns 3 and 4, and it pays $1 + 2 + 1 + 9 = 13$. The dynamic program sees the expensive bottom right corner before it chooses the path.

For a full step, take the $5 \times 4$ image with rows $(9, 9, 0, 9, 9)$, $(9, 1, 9, 8, 9)$, $(9, 9, 9, 9, 0)$ and $(9, 9, 9, 0, 9)$. Its $e_1$ energy has rows $(0, 17, 9, 10, 0)$, $(8, 0, 16, 0, 10)$, $(0, 8, 0, 17, 9)$ and $(0, 0, 9, 9, 18)$. The least seam is $(0, 1, 0, 0)$ with energy 0, and removing it leaves the $4 \times 4$ image with rows $(9, 0, 9, 9)$, $(9, 9, 8, 9)$, $(9, 9, 9, 0)$ and $(9, 9, 0, 9)$. The dark pixels 0, 1 and 8 that carry the structure all stay.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). By induction on $y$, after line L10 has run for row $y$, $M[y][x]$ is the least energy of a connected partial seam from row 0 to $(x, y)$, and $P[y][x]$ is the column above it on one such partial seam. The base case is line L6. For the step, a partial seam to $(x, y)$ is a partial seam to some $(x', y-1)$ with $|x' - x| \le 1$ followed by $(x, y)$, so its least energy is $e(x, y)$ plus the least $M[y-1][x']$ over those $x'$, which line L9 selects. Then line L11 picks a seam end of least total, and line L12 rebuilds a seam with that total, because each step of the traceback goes to a column that realizes the minimum. Every step of the traceback moves by at most one column, so the seam is connected.

The proof covers one seam. For $k \ge 2$ the loop of line L1 is greedy, and it does not in general remove the $k$ seams of least total energy. The proof file gives a $4 \times 3$ table, with the energies kept fixed on the pixels, where two greedy steps cost 10 and the best pair of steps costs 8.

## Complexity

Let $W$ be the width and $H$ the height at the start of one call.

- Line L2 reads at most five pixels per output pixel: $\Theta(WH)$.
- Lines L6 to L10 do a constant amount of work per pixel, at most three comparisons at line L9: $\Theta(WH)$ time and $\Theta(WH)$ space for $M$ and $P$.
- Lines L11 and L12 take $\Theta(W + H)$.
- Line L4 copies the image: $\Theta(WH)$.

One seam costs $\Theta(WH)$ in each case, and each pixel must be read, so this is optimal for one seam. The $k$ seams of the loop of line L1 cost $\sum_{i=0}^{k-1} \Theta((W - i)H)$, which is between $kWH/2$ and $kWH$ times a constant because $k < W$, so $\Theta(kWH)$. The extra space is $\Theta(WH)$. $M$ can keep only two rows if $P$ is stored, and $P$ needs $\log_2 3$ bits per pixel in principle (one of three moves), but the image itself is $\Theta(WH)$ anyway.

Recomputing the full energy after each removal is not needed: only the pixels next to the removed seam change their energy, but the dynamic program still reads the whole table, so the order of the cost stays $\Theta(kWH)$.

## Properties

- **Exact for one seam.** The seam is a true minimum of $E(s)$ over all connected seams, not an approximation.
- **Greedy over many seams.** Removing $k$ seams one by one is not optimal for the $k$ seams as a whole. Avidan and Shamir call the result content-aware, not optimal.
- **Local change.** Only the pixels on the right of the seam move, by one place, and only in their own row. Far from the seam, the image is unchanged.
- **Shape is kept.** Each row loses exactly one pixel, so the output is a rectangle. Removing the cheapest pixels of the whole image would not keep the rectangle, and removing the cheapest pixel of each row on its own would make a zigzag.
- **Deterministic.** With a fixed tie rule, the same input gives the same output.
- **Not a resampling.** No new pixel value is made by removal; each output pixel is an input pixel. Seam insertion averages, so it does make new values.

## Variants and improvements

- **Horizontal seams.** Transpose, carve vertical seams, transpose back.
- **Both directions.** To change the size from $W \times H$ to $W' \times H'$, Avidan and Shamir fill a transport map $T(r, c)$, the cost of reaching $r$ fewer rows and $c$ fewer columns, by a second dynamic program over the order of horizontal and vertical seams. Each entry keeps the image of the better predecessor, so this is also a heuristic, and it costs one seam computation per entry.
- **Seam insertion.** To widen by $k$, find the first $k$ seams that removal would take, then duplicate each of them in the original image, with the new pixel set to the average of its left and right neighbors. Inserting the single best seam $k$ times would choose the same seam again and stretch it.
- **Object removal.** Give the pixels of an object a large negative energy and remove seams until the object is gone, then insert seams to get the size back. Give a large positive energy to protect a region.
- **Forward energy.** Rubinstein, Shamir and Avidan charge each step by the new gradients that the removal creates between pixels that become neighbors, instead of the energy of the removed pixels. This gives fewer jagged artifacts. The dynamic program has the same shape, with the step cost depending on the move.
- **Video.** For a video, a seam is a surface in the $x, y, t$ volume. The same paper finds it with a minimum cut (see [graph cuts](/image-segmentation-graph-cuts/)), because the dynamic program does not extend to two dimensions.
- **Multi-size images.** Store, for each pixel, the step at which it is removed. A viewer can then show any width up to the stored range by keeping the pixels with a large enough index, in $\Theta(WH)$ time per size and with no new seam search.

## When to use it

Use seam carving to change the aspect ratio of a photo with a lot of low-detail background, such as sky, sea, sand or a plain wall, when the objects must keep their shape. It is also a simple tool to remove an object that a mask marks. Do not use it when the image has straight lines or regular structure everywhere, such as buildings, text or a face close up: every seam then crosses something and the lines bend or break. Do not use it to make an image much smaller: once the background is gone, the seams go through objects. Scale or crop for that (see [image resampling](/image-resampling/)), or mix the operators, which is what most practical retargeting tools do.

## Pitfalls

- **Not recomputing the energy.** After a removal, the pixels on the two sides of the seam become neighbors, and their gradients change. Using the old energy table for the next seam can pick a seam through a new edge. Line L2 is inside the loop for this reason.
- **Wrong window at the image border.** At $x = 0$ only columns 0 and 1 are above, and at $x = W - 1$ only $W - 2$ and $W - 1$. Reading $M[y-1][-1]$ in a language that wraps negative indices picks the last column, and the seam can jump from one side of the image to the other.
- **Choosing the seam greedily.** Starting at the cheapest top pixel and stepping to the cheapest pixel below is not the same as the dynamic program; the Example shows a case where it costs 13 instead of 6.
- **Integer overflow.** $M$ can reach $H$ times the largest energy. With 8-bit data and the $e_1$ energy, a pixel energy is at most 510, so a 16-bit $M$ overflows for tall images. Use 32-bit or wider sums.
- **Inserting the same seam again.** Inserting the cheapest seam, then the cheapest seam of the new image, inserts the same place again and again. Choose all $k$ seams for insertion from the removal order first.
- **Color by one channel.** Computing the energy on one channel, or on the luma only, can miss an edge between two colors with the same brightness. Sum the energy over the channels.

## Implementations

## History

Shai Avidan and Ariel Shamir presented seam carving at SIGGRAPH 2007, in a paper that defined seams, the $e_1$ energy and other energies, the dynamic program for the best seam, the transport map for the order of horizontal and vertical seams, seam insertion, object removal and multi-size images. Image editors added it soon after, for example as the Liquid Rescale plug-in for GIMP. In 2008 Rubinstein, Shamir and Avidan replaced the backward energy with forward energy and moved to video, where a seam becomes a surface found by a graph cut. Later retargeting work combined seams with scaling and cropping and with warping methods.

## References
