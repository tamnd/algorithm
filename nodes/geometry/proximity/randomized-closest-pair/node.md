---
tag: KQN34S
kind: algorithm
slug: randomized-closest-pair
name: Randomized closest pair
aliases:
- Rabin randomized closest pair
- grid-hashing closest pair
- incremental randomized closest pair
area: geometry/proximity
level: advanced
summary: Incremental randomized algorithm with grid hashing that finds the closest pair in expected O(n) time.
solves: [closest-pair-of-points]
model: word-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: O(n^2), expected: O(n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1976
  people: [Michael O. Rabin, Samir Khuller, Yossi Matias, Mordecai Golin, Rajeev Raman, Christian Schwarz, Michiel Smid]
  note: Rabin gave the first expected linear-time closest pair algorithm in 1976 using random sampling, the floor function and hashing; Khuller and Matias (1995) and Golin, Raman, Schwarz and Smid (1995) gave simpler versions, the latter including the incremental algorithm in random order.
prereqs: [closest-pair-of-points, randomized-algorithm, hash-table, floor-division, expected-running-time]
see_also: [closest-pair-divide-and-conquer, closest-pair-sweep-line, closest-pair-lower-bound, uniform-grid, spatial-hashing, randomized-incremental-construction, universal-hashing]
sources:
  - paper: "Michael O. Rabin, Probabilistic algorithms, in J. F. Traub (ed.), Algorithms and Complexity, New Directions and Recent Results, Academic Press, 1976, 21-39"
    locator: the randomized closest pair algorithm with random sampling, a grid built with the floor function, and expected linear time
  - paper: "Samir Khuller and Yossi Matias, A simple randomized sieve algorithm for the closest-pair problem, Information and Computation 118(1), 1995, 34-37"
    locator: the sieve that repeatedly samples a point, computes its nearest-neighbor distance and discards isolated points, in expected O(n) time
  - paper: "Mordecai Golin, Rajeev Raman, Christian Schwarz and Michiel Smid, Simple randomized algorithms for closest pair problems, Nordic Journal of Computing 2(1), 1995, 3-27"
    locator: the incremental algorithm in random order with a grid of cell size depending on the current minimum distance, and its backwards analysis
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 13, Section 13.7, Finding the closest pair of points, a randomized approach
  - paper: "Michiel Smid, Closest-point problems in computational geometry, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 877-935"
    locator: the survey sections on the closest pair in models with the floor function and on randomized algorithms
---

The randomized closest pair algorithm finds the [closest pair of points](/closest-pair-of-points/) in $O(n)$ expected time, which beats the $\Omega(n \log n)$ [lower bound](/closest-pair-lower-bound/) of the algebraic decision tree model. It inserts the points in random order into a grid whose cell side is about the current smallest distance $\delta$, so each new point is compared with the few points in nearby cells. When a new point gives a smaller $\delta$, the grid is rebuilt from scratch; a backwards analysis shows this happens at the insertion of the $i$-th point with probability at most $2/i$, so the rebuilds cost $O(n)$ in expectation. The algorithm needs the floor function to find cells and [hashing](/hash-table/) to store the non-empty cells, which is why the algebraic lower bound does not apply.

## In plain words

Shuffle the points and add them one at a time, always knowing the smallest gap among the points added so far.

Lay a grid of square boxes over the plane, with boxes about as wide as that gap, and remember which points are in which box. A new point can only be closer than the gap to points in its own box or in the boxes around it, and each box holds only a few points, so checking a new point is quick.

If the new point makes a smaller gap, the boxes are now too big, so rebuild the grid with smaller boxes from all points so far. That is expensive, but in a random order a new point is rarely part of the new closest pair, especially late in the run. On average the rebuilds cost a constant amount of work per point.

## The problem

**Input.** A list $P$ of $n$ points $p = (x, y)$ with integer coordinates (rational coordinates are first scaled by a common denominator, which multiplies every squared distance by the same factor). Duplicates and collinear points are allowed.

**Output.** For $n \ge 2$, two items $p \ne q$ with the smallest squared [Euclidean distance](/euclidean-distance/) $\delta^2(P)$, and that value. For $n < 2$ there is no pair.

**Model.** The grid cell of a point is $(\lfloor x/s \rfloor, \lfloor y/s \rfloor)$, which needs the floor function, and the non-empty cells are kept in a hash table, with $O(1)$ expected time per operation under [universal hashing](/universal-hashing/). On the [word RAM](/word-ram/) with integer input both are available. Classical statements use a [real RAM](/real-ram/) extended with floor. The cell side $s$ is chosen with $s \le \delta < 2s$; the implementation takes $s = 2^e$ with $4^e \le \delta^2 < 4^{e+1}$, read off the bit length of the integer $\delta^2$, so that no square root is taken and the floor is an arithmetic shift.

## The algorithm

```pseudo id=main
RANDOMIZED-CLOSEST-PAIR(P)
L1  if n < 2 then return none
L2  put P in uniformly random order P[0], …, P[n − 1]
L3  δ² ← ‖P[0] − P[1]‖²; best ← (P[0], P[1])
L4  if δ² = 0 then return (δ², best)
L5  choose s with s ≤ δ < 2s; G ← hash table of cells of side s holding P[0], P[1]
L6  for k ← 2 to n − 1 do
L7      (cx, cy) ← (⌊P[k].x / s⌋, ⌊P[k].y / s⌋)
L8      d² ← smallest ‖P[k] − q‖² over q in the cells (cx + a, cy + b), −2 ≤ a, b ≤ 2
L9      if d² < δ² then
L10         δ² ← d²; best ← (q, P[k]); if δ² = 0 then return (δ², best)
L11         choose s with s ≤ δ < 2s; G ← new grid of side s holding P[0], …, P[k]
L12     else insert P[k] into cell (cx, cy) of G
L13 return (δ², best)
```

Line L8 looks at a $5 \times 5$ block of cells. If $\|P[k] - q\| < \delta$ then $|P[k].x - q.x| < \delta < 2s$, and the cell indices differ by at most $2$ in each coordinate, so every point closer than $\delta$ is in the block. Cells that are not in $G$ are empty. Line L11 rebuilds the whole grid because all cell indices change with $s$.

## Example

Take the eight points of the [closest pair](/closest-pair-of-points/) page in the order $(8,8)$, $(0,0)$, $(9,5)$, $(3,6)$, $(7,0)$, $(5,3)$, $(1,9)$, $(4,2)$, as if line L2 had produced it. The cell side is the power of two $s$ with $s^2 \le \delta^2 < 4s^2$.

| step | new point | cell | points in the $5 \times 5$ block (squared distance) | $\delta^2$ after | $s$ after |
| --- | --- | --- | --- | --- | --- |
| start | $(8,8)$, $(0,0)$ | | | $128$ | $8$ |
| $k = 2$ | $(9,5)$ | $(1, 0)$ | $(0,0)$: 106; $(8,8)$: 10 | $10$, rebuild | $2$ |
| $k = 3$ | $(3,6)$ | $(1, 3)$ | none | $10$ | $2$ |
| $k = 4$ | $(7,0)$ | $(3, 0)$ | $(9,5)$: 29 | $10$ | $2$ |
| $k = 5$ | $(5,3)$ | $(2, 1)$ | $(0,0)$: 34; $(3,6)$: 13; $(7,0)$: 13; $(9,5)$: 20 | $10$ | $2$ |
| $k = 6$ | $(1,9)$ | $(0, 4)$ | $(3,6)$: 13 | $10$ | $2$ |
| $k = 7$ | $(4,2)$ | $(2, 1)$ | $(0,0)$: 20; $(3,6)$: 17; $(5,3)$: 2; $(7,0)$: 13; $(9,5)$: 34 | $2$, rebuild | $1$ |

At $k = 3$ the block of cells $x \in [-1, 3]$, $y \in [1, 5]$ is empty: $(8,8)$ is in cell $(4,4)$, $(9,5)$ in $(4,2)$ and $(0,0)$ in $(0,0)$, all outside it, and indeed all three are farther than $\sqrt{10}$ from $(3,6)$. The answer is $(4,2)$, $(5,3)$ with $\delta^2 = 2$. There were two rebuilds, at the steps where the new point belonged to the new closest pair.

## Correctness

The invariant is that before step $k$, $\delta^2$ is the smallest squared distance among $P[0], \ldots, P[k-1]$, and $G$ is the grid of side $s$ with $s \le \delta < 2s$ holding exactly those points. A point $q$ with $\|P[k] - q\|^2 < \delta^2$ has $|P[k].x - q.x| < 2s$ and $|P[k].y - q.y| < 2s$, so its cell is in the block of line L8, and line L8 finds the smallest such distance. If no such $q$ exists, the minimum over the first $k + 1$ points is still $\delta^2$, and line L12 adds $P[k]$ to $G$. Otherwise the new minimum is the value found, and line L11 restores the grid property. The randomness affects only the running time, never the answer. The full proof is in the correctness proof below.

## Complexity

- **Cost of a step without rebuild.** Points in one cell are at least $\delta$ apart, and a half-open square of side $s \le \delta$ contains at most $4$ points that are pairwise at least $\delta$ apart. So line L8 looks at at most $25 \cdot 4 = 100$ points, and each step costs $O(1)$ expected time with hashing.
- **Rebuilds, by backwards analysis.** Fix the set of the first $k + 1$ points; under a random order each of them is equally likely to be $P[k]$. Pick one closest pair $(a, b)$ of this set. If $P[k] \notin \{a, b\}$, both are among the first $k$ points and $\delta^2$ does not change. So step $k$ rebuilds with probability at most $2/(k + 1)$, at cost $O(k + 1)$, and the expected rebuild cost is $O(1)$ per step.
- **Total.** $O(n)$ expected time and $O(n)$ space, assuming $O(1)$ time per hash operation (expected, with universal hashing). The worst case over the random order is $O(n^2)$, when every step rebuilds.

The details are in the complexity proof below. The tests measure the total rebuild work on a fixed set of 400 points over 200 random orders; its average was about $1.92\,n$, below the bound $2n$ from the analysis.

## Properties

- **Las Vegas.** The answer is always correct; only the time is random.
- **Exact.** Distances are compared as squared integers, and cells use shifts; there is no square root.
- **Beats the algebraic lower bound.** The $\Omega(n \log n)$ bound holds for algebraic decision trees, where floor and hashing are not available. With them, the same grid idea also decides [element distinctness](/element-distinctness/) in $O(n)$ expected time.
- **Fixed dimension.** In $\mathbb{R}^d$ the block has $5^d$ cells and the analysis is the same, so the time is $O(n)$ expected for every fixed $d$, with a constant exponential in $d$.

## Variants and improvements

- **Rabin's sampling method.** Rabin (1976) samples a set of points, computes the closest pair distance of the sample recursively, builds a grid with that cell size, and compares points only within neighbouring cells; the analysis shows the expected number of comparisons is linear.
- **Khuller and Matias's sieve.** Repeatedly pick a random remaining point, compute its nearest-neighbor distance $d$ by brute force, put the points in a grid of side about $d/3$ and delete the points with no other point in their neighbourhood. When no point is left, the last $d$ approximates $\delta$ within a constant factor, and one final grid pass finds the exact closest pair. Expected $O(n)$ time.
- **Rebuild only when the cell side changes.** With power-of-two sides, a smaller $\delta^2$ often keeps the same $s$, and the rebuild of line L11 can be skipped; this changes only the constant.
- **Insertions.** Because the algorithm is incremental, it maintains the closest pair while points are inserted; Golin, Raman, Schwarz and Smid study this and related closest pair problems with the same grid idea.
- **Deterministic alternatives.** [Divide and conquer](/closest-pair-divide-and-conquer/) and the [sweep line](/closest-pair-sweep-line/) take $\Theta(n \log n)$ time without floor or hashing; Fortune and Hopcroft (1979) gave a deterministic $O(n \log \log n)$ algorithm that uses floor.

## When to use it

Use it for large inputs with integer or fixed-point coordinates, where a hash table is cheap and linear expected time matters. It is short to code and needs no sorting. Avoid it when a guaranteed worst-case bound is required, when the input may be chosen adversarially against a known hash function, or in models without floor. For a one-off query on modest input sizes, the [divide and conquer](/closest-pair-divide-and-conquer/) or [sweep](/closest-pair-sweep-line/) versions are just as fast in practice.

## Pitfalls

- **No random order.** Without line L2, an adversary can order the points so that every step lowers $\delta$, for example points on a line at shrinking gaps, and the rebuilds of line L11 cost $\Theta(n^2)$.
- **A cell side larger than $\delta$ with a $3 \times 3$ block.** With $s \ge \delta$ a $3 \times 3$ block suffices, but then a cell can hold many points when $s$ is much larger than $\delta$. The rule $s \le \delta < 2s$ of lines L5 and L11 keeps both the block ($5 \times 5$) and the cell load constant.
- **Floating-point cell side.** Computing $s = \sqrt{\delta^2}$ in floating point and then $\lfloor x/s \rfloor$ can round $s$ up past $\delta$ or put a point in the wrong cell near a cell border; with $|x|$ around $10^{16}$ the floor of a float quotient may be off by one. The power-of-two side and the shift in line L7 are exact.
- **Forgetting the zero case.** If two points are equal, $\delta^2 = 0$ and no positive $s$ satisfies $s \le \delta$; lines L4 and L10 stop at once.
- **Hash flooding.** With a fixed, known hash function an adversary can put all cells into one bucket. Use [universal hashing](/universal-hashing/) or a randomized seed for the expected bound to hold.

## Implementations

## History

Rabin presented the first randomized closest pair algorithm in 1976, in his paper on probabilistic algorithms, as an example where randomization and the floor function together give expected linear time, below the $n \log n$ of the deterministic methods. Fortune and Hopcroft (1979) showed that without randomization, but with floor, $O(n \log \log n)$ is possible. Khuller and Matias (1995) gave a simple sieve, and Golin, Raman, Schwarz and Smid (1995) gave the incremental algorithm in random order with its backwards analysis; this is the version presented by Kleinberg and Tardos.

## References
