---
tag: EF89RD
kind: algorithm
slug: intelligent-scissors
name: Intelligent scissors
aliases:
- live wire
- Mortensen-Barrett live wire
area: computer-vision/segmentation-and-recognition
level: core
summary: "Trace an object boundary interactively. A least cost path on the pixel graph, from a seed point to the cursor, snaps to edges; the cost mixes Laplacian zero crossings, gradient size and direction."
solves: [interactive-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {worst: O(W H log(W H)), average: O(W H log(W H)), best: O(W H)}
  space: {extra: O(W H)}
properties: {deterministic: true, exact: true, interactive: true, nonnegative_costs: true}
history:
  year: 1995
  people: [Eric N. Mortensen, William A. Barrett]
  note: Mortensen and Barrett (SIGGRAPH 1995) computed least cost paths from a seed to all pixels so that the boundary follows the cursor in real time.
prereqs: [dijkstra, edge-detection, interactive-segmentation]
see_also: [bucket-queue, dial-algorithm, laplacian-of-gaussian, sobel-operator, active-contours, boykov-jolly-graph-cuts, random-walker-segmentation, single-source-shortest-paths]
sources:
  - paper: doi:10.1145/218380.218442
    title: "Eric N. Mortensen and William A. Barrett, Intelligent scissors for image composition, SIGGRAPH 95, 191-198, 1995"
    locator: "Section 3.1 (local costs, equations 1 to 5, weights), Section 3.2 (2D dynamic programming search and its pseudocode), Section 3.4 (path cooling), Section 3.5 (on-the-fly training)"
  - paper: doi:10.1006/gmip.1998.0480
    title: "Eric N. Mortensen and William A. Barrett, Interactive segmentation with intelligent scissors, Graphical Models and Image Processing 60(5), 349-384, 1998"
    locator: "The journal version, with more cost features and training"
  - book: isbn:978-1-84882-934-3
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 1st edition, Springer, 2011"
    locator: "Section 5.1.3, Scissors"
---

Intelligent scissors, also called live wire, is an interactive algorithm that traces the boundary of an object as a least cost path on the graph of pixels. The user clicks a seed point on the boundary. The algorithm then computes, with [Dijkstra's algorithm](/dijkstra/), the least cost path from the seed to every pixel. As the user moves the cursor, the path from the seed to the cursor is shown at once, and it snaps to nearby edges because the link costs are low on edges. Mortensen and Barrett (1995) defined the cost from the Laplacian zero crossings, the gradient magnitude and the gradient direction. The user fixes a piece of the path by clicking a new seed, and goes on around the object.

## In plain words

You want to cut a person out of a photo. Tracing the outline by hand needs a steady hand and a lot of time. With intelligent scissors you click once on the outline. Then, when you move the mouse near the outline, a wire appears from your click to the mouse, and it clings to the outline by itself. The wire is the cheapest route between the two points, where walking along a strong edge is cheap and walking across smooth areas is costly. When the wire looks right, you click again to fix that piece, and continue. A few clicks go around the whole object. The program computes the cheapest route to every pixel right after each click, so the wire can follow the mouse without delay.

## The problem

The input is a gray image $I$ of $W \times H$ pixels and a seed pixel $s$. The graph has one node per pixel and a directed link from each pixel $p$ to each of its 8 neighbors $q$, with a cost $l(p, q) \ge 0$. The output is, for each pixel $t$, the least total cost $g(t)$ of a path from $s$ to $t$, and back pointers that give such a path. The boundary piece shown to the user is the path from $s$ to the cursor. This is the [single-source shortest path](/single-source-shortest-paths/) problem on a grid graph with $n = WH$ nodes and at most $8n$ links.

The local cost of Mortensen and Barrett (1995, Section 3.1, equation 1) is
$$l(p, q) = \omega_Z f_Z(q) + \omega_G f_G(q) + \omega_D f_D(p, q),$$
with the weights printed in the paper: $\omega_Z = 0.43$, $\omega_G = 0.43$ and $\omega_D = 0.14$. The three features are:
- **Laplacian zero crossing** $f_Z(q)$: $0$ if $q$ lies on a zero crossing of the Laplacian of the image, else $1$. On the discrete grid the Laplacian rarely equals zero, so of two neighbors with opposite signs, the one closer to zero is the crossing.
- **Gradient magnitude** $f_G(q) = 1 - G(q)/\max G$ with $G = \sqrt{I_u^2 + I_v^2}$, so strong edges are cheap. It is scaled by $1$ when $q$ is a diagonal neighbor of $p$ and by $1/\sqrt 2$ when $q$ is a horizontal or vertical neighbor. This weights the cost by the length of the link and keeps the maximum at 1.
- **Gradient direction** $f_D(p, q) = \frac{2}{3\pi} \bigl(\arccos(D(p) \cdot L) + \arccos(L \cdot D(q))\bigr)$. Here $D(p) = (I_v(p), -I_u(p)) / G(p)$ is the unit vector along the edge, the gradient turned by 90 degrees. $L$ is the unit vector of the link from $p$ to $q$, or its negative, chosen so that $D(p) \cdot L \ge 0$. The cost is low when the link runs along the edge at both ends, and high at sharp turns.

The weights are design choices that the authors tuned. They are not derived from a model.

## The algorithm

The first block is the "live-wire 2D dynamic programming" search of Mortensen and Barrett (1995, Section 3.2). It is Dijkstra's algorithm. The active list $\mathcal L$ holds the pixels with a tentative cost, and $e(q)$ marks the expanded pixels.

```pseudo id=main
LIVE-WIRE(s, l)
L1  g(s) ← 0; 𝓛 ← {s}; e(q) ← false for every pixel q
L2  while 𝓛 is not empty do
L3      q ← the pixel in 𝓛 with the least g; remove q from 𝓛
L4      e(q) ← true
L5      for each neighbor r of q with e(r) = false do
L6          g_tmp ← g(q) + l(q, r)
L7          if r is in 𝓛 and g_tmp < g(r) then remove r from 𝓛
L8          if r is not in 𝓛 then g(r) ← g_tmp; ptr(r) ← q; insert r in 𝓛
L9  return g and ptr       ▷ the path to a free point t follows ptr from t to s
```

The second block computes the cost of one link before the search.

```pseudo id=cost
LOCAL-COST(p, q)
L10 f_Z(q) ← 0 if the Laplacian has a zero crossing at q, else 1
L11 f_G(q) ← (1 - G(q) / max G) · (1 if q is diagonal to p, else 1/√2)
L12 f_D(p, q) ← (2 / 3π) (arccos(D(p) · L) + arccos(L · D(q)))
L13 return 0.43 f_Z(q) + 0.43 f_G(q) + 0.14 f_D(p, q)
```

The search runs once per seed and gives paths to all pixels. Moving the cursor only follows pointers, which costs the length of the path. Mortensen and Barrett sort the active list with an $O(n)$ method: the costs are integers in a small range, so the list is a [bucket queue](/bucket-queue/), as in [Dial's algorithm](/dial-algorithm/).

## Example

Take this $5 \times 5$ image, with a dark area on the left, a bright area on the right and a step in the edge between rows 1 and 2:

| | u = 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| v = 0 | 10 | 10 | 10 | 90 | 90 |
| v = 1 | 10 | 10 | 10 | 90 | 90 |
| v = 2 | 10 | 10 | 90 | 90 | 90 |
| v = 3 | 10 | 10 | 90 | 90 | 90 |
| v = 4 | 10 | 10 | 90 | 90 | 90 |

The code uses central differences and the 4-neighbor Laplacian, with the border pixels repeated. The Laplacian changes sign across the edge, and column 2 holds a zero crossing in every row, so $f_Z = 0$ there. The largest gradient is $G = 40\sqrt 2 \approx 56.57$, at $(2, 1)$ and $(2, 2)$, where the edge turns.

Seed $s = (2, 0)$. The link down to $(2, 1)$ has $f_Z = 0$ and $f_G = 0$. At the seed the gradient is $(40, 0)$, so $D(s) = (0, -1)$, and $L = (0, -1)$ after the sign rule. At $(2, 1)$ the gradient is $(40, 40)$, so $D = (0.7071, -0.7071)$. Then $f_D = \frac{2}{3\pi}(\arccos 1 + \arccos 0.7071) = \frac{2}{3\pi} \cdot \frac{\pi}{4} = \frac16$, and $l = 0.14 / 6 \approx 0.0233$. The other links from the seed cost $0.8274$ to $(1, 0)$, $0.1824$ to $(3, 0)$, $0.9300$ to $(1, 1)$ and $0.1726$ to $(3, 1)$.

The search gives these least costs $g$ from the seed:

| | u = 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| v = 0 | 1.655 | 0.827 | 0 | 0.173 | 1.000 |
| v = 1 | 1.103 | 0.827 | 0.023 | 0.173 | 1.000 |
| v = 2 | 1.000 | 0.173 | 0.070 | 0.874 | 1.103 |
| v = 3 | 1.047 | 0.219 | 0.182 | 1.010 | 1.827 |
| v = 4 | 1.136 | 0.308 | 0.271 | 1.099 | 1.926 |

With the cursor at $(2, 4)$, the pointers give the path $(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)$ with the link costs $0.0233$, $0.0467$, $0.1124$, $0.0891$, total $0.2714$. The path runs along the zero crossings of the edge. The test file checks these numbers and compares the search with Bellman-Ford.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The facts that are proved:
- Every link cost is in $[0, 1]$. The three features are in $[0, 1]$ and the weights are nonnegative with sum 1. The sign rule for $L$ keeps the direction term at most 1.
- With nonnegative costs, a pixel taken from the active list at line L3 has its final least cost. This is the classical invariant of Dijkstra's algorithm. So line L9 gives least cost paths from the seed to every pixel.
- Removing and inserting again at lines L7 and L8 has the same effect as the lazy deletion in the code.
- With integer costs in $0, \dots, C$, a circular array of $C + 1$ buckets returns the pixels in the same order as a heap.

What is not proved: that the least cost path is the object boundary. The cost function is a heuristic, and its weights are tuned values.

## Complexity

The graph has $n = WH$ nodes and at most $8n$ links. In the [real-RAM](/real-ram/) model with a [binary heap](/binary-heap/), the search costs $O(n \log n) = O(WH \log(WH))$ time, as each link causes at most one insertion. The local costs take $O(WH)$ time before the search: a few filters and 8 costs per pixel. The best case $O(WH)$ in the front matter is for the bucket queue below with a fixed cost range.

With integer costs in $0, \dots, C$ (a word-RAM model), the bucket queue makes the search $O(n + D)$, where $D \le (n - 1) C$ is the largest path cost, since the scan over buckets never goes back. For a fixed $C$, such as costs scaled to 0 to 255, this is the $O(n)$ of the paper. The extra space is $O(WH)$ for $g$, the pointers, the expanded flags and the active list. After the search, each cursor move costs $O(k)$ for a path of $k$ pixels.

## Properties

- **Exact for its cost.** The path is a global least cost path, not a local optimum as in [active contours](/active-contours/).
- **Interactive.** One search per seed gives the path to every cursor position.
- **Directed costs.** $l(p, q)$ and $l(q, p)$ differ, because $f_Z$ and $f_G$ are evaluated at the end pixel. The graph is directed.
- **Invariant to brightness and contrast.** An affine change of intensity $I \to aI + b$ with $a \ne 0$ does not change $f_Z$, $f_G$ or $f_D$. A negative $a$ flips both $D(p)$ and the chosen $L$, so the dot products stay the same. The tests check it.
- **Short paths win.** The total cost grows with length, so the path can cut a corner across a weak region instead of following a long, faint boundary.

## Variants and improvements

- **Path cooling** (Section 3.4 of the 1995 paper). When a piece of the path near the seed stays the same for some time, the program fixes it and sets a new seed there, so the user needs fewer clicks. This is a heuristic.
- **On-the-fly training** (Section 3.5 of the 1995 paper). The gradient magnitude cost is replaced by a cost learned from the boundary piece just accepted, so the wire prefers edges like the last one and not simply the strongest edge nearby. This is a heuristic.
- **Other costs.** Color gradients, or a [Laplacian of Gaussian](/laplacian-of-gaussian/) at several scales, instead of the plain Laplacian.
- **Scissors with regions.** [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/) use seeds inside and outside instead of points on the boundary, and find the whole boundary at once.
- **Continuous paths.** Geodesic active contours and minimal path methods with fast marching compute least cost curves in the continuous plane. They are related methods, not the same algorithm.

## When to use it

Use intelligent scissors when the user can follow the boundary with the mouse, when the boundary has good edges in most places, and when the object is thin or has a long outline. It gives exact control of the boundary with few clicks. Use a region method such as [Boykov-Jolly graph cuts](/boykov-jolly-graph-cuts/) or the [random walker](/random-walker-segmentation/) when the object is large and its edges are weak or noisy, or when the data is 3D, where a boundary is a surface and a path does not suffice.

## Pitfalls

- **Weight order.** The paper prints $\omega_Z = 0.43$, $\omega_G = 0.43$ and $\omega_D = 0.14$. The small weight is on the gradient direction, not on the gradient magnitude.
- **Zero gradient.** $D(p)$ is undefined where the gradient is zero. The code uses the zero vector, which gives the arccosine $\pi/2$.
- **Flat regions and the Laplacian.** The Laplacian is zero in flat regions. Treating every zero as a crossing makes flat regions cheap. The code counts only sign changes.
- **Noise.** A raw Laplacian finds crossings in noise. Smooth the image first, for example with a [Gaussian filter](/gaussian-filter/).
- **Scale of the gradient cost.** $f_G$ divides by the largest gradient of the image. One very strong edge makes all other edges look weak.
- **Shortcut paths.** Without enough seeds, the wire jumps across a weak gap to a nearby strong edge. Add a seed before such a place.

## Implementations

The Python code in `impl/python/intelligent_scissors.py` computes the three cost features with central differences and the 4-neighbor Laplacian, runs the search of lines L1 to L9 with a binary heap and lazy deletion, and follows the pointers to a free point. It also has a bucket queue search for integer costs and Bellman-Ford as a reference. The tests check the example, that the costs lie in $[0, 1]$, that the search equals Bellman-Ford and that each path has the cost $g$, that the bucket queue gives the same costs as the heap, the invariance to affine intensity changes, and that the path follows a straight step edge.

## History

Least cost paths for boundary tracing are older than live wire: Montanari (1971) and Martelli (1976) traced curves with dynamic programming and heuristic graph search, but these methods needed a fixed start and end, or a search band. The name "live wire" and the search over all pixels appear first in a 1992 paper on cardiac images by Mortensen, Morse, Barrett and Udupa, which the 1995 paper cites. Mortensen and Barrett (1995) made it a general tool for image composition. They computed the paths from the seed to all pixels at once, so the end point could follow the cursor, and they added path cooling and on-the-fly training (Sections 3.4 and 3.5). The 1998 journal paper of Mortensen and Barrett gives a longer account.

## References
