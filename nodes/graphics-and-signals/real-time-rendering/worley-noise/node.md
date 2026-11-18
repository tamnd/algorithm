---
tag: KRW8CM
kind: algorithm
slug: worley-noise
name: Worley noise
aliases:
- cellular noise
- Voronoi noise
area: graphics-and-signals/real-time-rendering
level: core
summary: A procedural texture basis whose value is the distance to the nearest, or the k-th nearest, of random feature points scattered in cells.
model: real-ram
complexity:
  vars: {k: the order of the distance F_k, λ: the mean number of feature points per cell, q: the number of queries}
  time: {expected: O(q (1 + k/λ + (λ + k) k))}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false, online: true, in_place: false}
history:
  year: 1996
  people: [Steven Worley]
  note: Worley introduced the cellular texture basis functions F_1, F_2 and their combinations at SIGGRAPH 1996.
prereqs: [hash-function, nearest-neighbor-search, perlin-noise]
see_also: [perlin-noise, simplex-noise, fractal-noise, voronoi-diagram, nearest-neighbor-search, uniform-grid, spatial-hashing, k-means]
sources:
  - paper: doi:10.1145/237170.237267
    title: Steven Worley, A cellular texture basis function, SIGGRAPH 1996, pages 291 to 294
    locator: the whole paper (feature points with a Poisson count per cube, the functions F_n, and the search of the neighboring cubes)
  - book: isbn:9781558608481
    title: David S. Ebert, F. Kenton Musgrave, Darwyn Peachey, Ken Perlin and Steven Worley, Texturing and Modeling, A Procedural Approach, third edition, Morgan Kaufmann, 2003
    locator: the chapter by Worley on cellular texturing (general locator)
---

Worley noise is a procedural texture made from distances. Random feature points are scattered through space, a fixed set for each seed, and the value at a point $x$ is $F_k(x)$, the distance from $x$ to its $k$-th nearest feature point. $F_1$ looks like a field of round cells, $F_2 - F_1$ is zero on the edges of the [Voronoi diagram](/voronoi-diagram/) of the points and draws a web of cracks, and other combinations give stone, scales, foam and leather. [Perlin noise](/perlin-noise/) and [simplex noise](/simplex-noise/) are the other base noises. They blend random gradients on a lattice, and their features have no sharp edges. [Fractal noise](/fractal-noise/) sums octaves of any of these base noises.

## In plain words

Throw a handful of seeds on the floor at random. For each spot on the floor, measure the distance to the nearest seed. Paint near spots dark and far spots light. You get round blobs around the seeds, and the blobs meet in straight lines halfway between neighbors.

You cannot store infinitely many seeds, so the floor is cut into square tiles, and each tile makes its own seeds from a random number generator started with the tile number. The same tile always gets the same seeds. To find the nearest seed, look at your own tile, then at the ring of tiles around it, and so on, until no tile further out could hold a nearer seed.

## The problem

The input is a query point $x \in \mathbb{R}^2$, an order $k \ge 1$, a seed, a mean density $\lambda > 0$ and a distance (Euclidean, Manhattan or Chebyshev). The plane is cut into unit cells. Cell $b$ holds a Poisson number of points with mean $\lambda$, placed uniformly in the cell, all taken from a generator seeded by a [hash](/hash-function/) of the seed and $b$. The output is the sorted list $F_1(x) \le \dots \le F_k(x)$ of the distances from $x$ to its $k$ nearest feature points. The answer must be exact, not an estimate, so that the texture has no holes or seams.

## The algorithm

```pseudo id=main
WORLEY(x, k, seed)
L1  c ← ⌊x⌋; m ← the distance from x to the nearest side of the cell c
L2  best ← an empty sorted list
L3  for r ← 0, 1, 2, ... do
L4      for each cell b at Chebyshev distance exactly r from c do
L5          for each feature point p of b do      ▷ made from HASH(seed, b)
L6              insert δ(x, p) into best and keep the k smallest
L7      if best has k entries and best[k] ≤ r + m then
L8          return best
```

The cells at Chebyshev distance at most $r$ from $c$ form a square block. Every point outside the block is at a distance of at least $r + m$ from $x$. So when the $k$-th best distance is at most $r + m$, no further ring can change the answer.

## Example

Take $x = (0.5, 0.5)$, $k = 2$, seed 0 and $\lambda = 2$ in the code. Then $c = (0, 0)$ and $m = 0.5$.

| ring | feature points | distances | best after the ring | stop test |
|---|---|---|---|---|
| 0 | $(0.892, 0.591)$, $(0.773, 0.079)$ | $0.4024$, $0.5015$ | $(0.4024, 0.5015)$ | $0.5015 \le 0.5$ is false |
| 1 | 14 points in 8 cells | the smallest is $0.9153$ | $(0.4024, 0.5015)$ | $0.5015 \le 1.5$ is true |

So $F_1 = 0.4024$, $F_2 = 0.5015$ and $F_2 - F_1 = 0.0991$. The first test fails by a small margin: a point in the next ring could still be at a distance just over $0.5$, and the search must look. Ring 1 changes nothing here, but it must be searched.

## Correctness

The proof file shows four facts. First, the ring function lists each cell of ring $r$ once, so after ring $r$ the search has seen every point of the block of cells within Chebyshev distance $r$. Second, the list keeps the $k$ smallest distances seen. Third, a point outside the block differs from $x$ by at least $r + m$ in some coordinate, and all three distances are at least that difference. So when line L7 holds, no unseen point can be nearer than the $k$-th entry, and the answer is exact. Fourth, the loop stops by ring $\max(r_k, \lceil F_k \rceil)$, where $r_k$ is the ring of a $k$-th nearest point. The code test compares the result with a brute force search over all points of a block of $16 \times 16$ cells.

## Complexity

In the ideal model, where the counts are independent Poisson variables and the points are uniform, the points form a Poisson process of intensity $\lambda$. Then $E[F_k^2] = k / (\pi \lambda)$, and the search visits $O(1 + k / \lambda)$ cells and $O(\lambda + k)$ points on average. Each point costs $O(k)$ to insert. So a query costs $O(1 + k / \lambda + (\lambda + k) k)$ expected time, which is $O(1)$ for fixed $k$ and $\lambda$. These are proved bounds in the model. The worst case has no bound, because any number of cells can be empty. The extra space is $O(k)$, plus the points of one cell. No table is stored.

## Properties

- **Exact.** The ring search returns the true $F_k$. This is proved.
- **1-Lipschitz.** $|F_k(x) - F_k(y)| \le |x - y|$ for the Euclidean distance. So $F_k$ is continuous, but its gradient jumps on the edges of the Voronoi cells, which gives the sharp creases of the texture.
- **Zero at the feature points.** $F_1(p) = 0$ at each feature point.
- **Deterministic.** Each cell makes the same points for the same seed, so the texture is fixed on the object.
- **Not zero mean.** Unlike gradient noise, $F_k$ is positive and grows with $k$. Shift and scale it before you use it as a signed noise.

## Variants and improvements

- **One point per cell.** A jittered grid with exactly one point per cell is a common GPU form. It usually searches a fixed $3 \times 3$ block in 2D, or $3 \times 3 \times 3$ in 3D, for a fixed cost. This is still not exact in every case: for $x$ near a cell corner, the nine points of the block can all lie at a distance near $\sqrt2$, while a point two cells away lies at a distance just over 1. Its pattern is more regular than a Poisson pattern.
- **Combinations.** $F_2 - F_1$ for cracks and cell edges, $F_1 + F_2$, products, and the index of the nearest point as a cell ID for a flat color per cell.
- **Other distances.** The Manhattan and the Chebyshev distances give diamond and square cells. The ring search is exact for both.
- **Three and more dimensions.** The same search works with cubes in place of squares. The cost per ring grows with the dimension.
- **Fractal sums.** Summing octaves of $F_1$ gives rough rock and craters, as in [fractal noise](/fractal-noise/).

## When to use it

Use Worley noise for textures with cells or cracks: stone tiles, dry mud, scales, cells under a microscope, water caustics and foam. Use it as a source of cell IDs for a random color per cell. For smooth hills and clouds, use [Perlin noise](/perlin-noise/) or [simplex noise](/simplex-noise/). When the points are given data, not a procedural texture, use a [nearest neighbor search](/nearest-neighbor-search/) structure such as a [k-d tree](/kd-tree/) or a [uniform grid](/uniform-grid/).

## Pitfalls

- **The $3 \times 3$ shortcut with a random count.** With a Poisson count, the block can be empty, or a point outside it can be nearer. In the code, with $\lambda = 0.5$, the shortcut gives a wrong $F_1$ for 3.5 percent of 20000 random queries, and with $\lambda = 2$ for 1 query in 20000. These are measurements. The errors show as small seams on the cell borders.
- **Too few points for $F_2$ and higher.** A block that is large enough for $F_1$ may not be large enough for $F_3$ or $F_4$. The stop test of line L7 handles this, a fixed block does not.
- **A poor cell hash.** If the seeds of neighboring cells are correlated, the points line up. Use a well mixed hash of the cell index.
- **Precision far from the origin.** Far from the origin, $x - \lfloor x \rfloor$ loses bits in 32-bit floats, and the cells jitter.
- **Aliasing on the creases.** The gradient of $F_k$ jumps on the Voronoi edges, so $F_2 - F_1$ at a small scale aliases. Filter it or fade it out with the distance. See [aliasing](/aliasing/).

## Implementations

## History

Steven Worley published the cellular texture basis function at SIGGRAPH 1996. He scattered feature points through space with a Poisson count per cube, defined $F_n$ as the distance to the $n$-th nearest point, and showed textures made from linear combinations of $F_1$ to $F_4$. The idea complements Perlin noise, whose features are smooth and have no edges. Later GPU code often used one jittered point per cell and a fixed $3 \times 3$ block, which trades exactness and some randomness for a fixed cost.

## References
