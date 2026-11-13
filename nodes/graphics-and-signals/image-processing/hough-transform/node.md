---
tag: ZV0TVQ
kind: algorithm
slug: hough-transform
name: Hough transform
aliases:
- Hough line detection
area: graphics-and-signals/image-processing
level: advanced
summary: Detect straight lines in a set of edge points. Each point votes for every line through it in a grid over angle and distance, and the cells with many votes are the lines.
solves: [line-detection]
model: word-ram
complexity:
  vars: {N: number of edge points, T: number of angle bins, D: ceil of the image diagonal in pixels}
  time: {worst: Θ(N T + T D), best: Θ(N T + T D)}
  space: {extra: Θ(T D)}
properties: {deterministic: true, exact: false, linear: true, in_place: false}
history:
  year: 1962
  people: [Paul Hough, Richard Duda, Peter Hart]
  note: Hough patented the voting method in 1962 (US patent 3,069,654) to find particle tracks in bubble chamber photographs. Duda and Hart gave the normal form rho = x cos(theta) + y sin(theta) in 1972.
prereqs: [line-detection, edge-detection]
see_also: [collinear-points, line-arrangement, line-representation, point-to-line-distance, canny-edge-detector, non-maximum-suppression, linear-regression, random-sampling]
sources:
  - paper: doi:10.1145/361237.361242
    title: Richard O. Duda and Peter E. Hart, Use of the Hough transformation to detect lines and curves in pictures, Communications of the ACM 15(1), 11 to 15, 1972
    locator: the normal parameterization rho = x cos(theta) + y sin(theta), the sinusoidal curves in the parameter plane, and the quantized accumulator
  - paper: "Paul V. C. Hough, Method and means for recognizing complex patterns, US Patent 3,069,654, 1962"
    locator: the whole patent (each point of the picture is mapped to a line in a parameter plane of slope and intercept, and collinear points give lines that meet in one point)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the part on linking edge points, global processing using the Hough transform
  - paper: "John Illingworth and Josef Kittler, A survey of the Hough transform, Computer Vision, Graphics, and Image Processing 44(1), 87 to 116, 1988"
    locator: the whole survey (parameterizations, the accumulator, the detection of peaks, and the variants)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.4, Lines and vanishing points (the part on Hough transforms)
---

The Hough transform finds straight lines in a set of edge points. It describes each line by two numbers, an angle $\theta$ and a distance $\rho$ from the origin, and it puts a grid of cells over these two numbers, the *accumulator*. Each edge point votes once for each angle, in the cell of the one line through it at that angle. Points on a common line all vote for the same cell, so the lines of the image are the cells with many votes. Paul Hough patented the idea in 1962, and Richard Duda and Peter Hart gave the form with $\rho = x \cos\theta + y \sin\theta$ in 1972. For $N$ edge points and $T$ angles the voting costs $\Theta(N T)$ time. It is the classic method of [line detection](/line-detection/), and it is robust: points that are not on the line, and gaps in the line, change the peak only a little.

## In plain words

Each edge point could be on many lines, one for each direction through it. The method lets each point vote for all of them. It keeps a table with one box for each possible line, and each point adds a vote to the boxes of all the lines through it. A point that is noise votes for lines that nobody else votes for. But all the points of a real line vote for the box of that line, so that box gets many more votes than the others. At the end, the boxes with the most votes are the lines. A line with gaps still collects the votes of all its pieces.

## The problem

The input is a list of $N$ edge points of a $W \times H$ image, for example the output of the [Canny edge detector](/canny-edge-detector/). A point $(x, y)$ is the center of a pixel, with integer coordinates, $x$ to the right and $y$ downward. The output is the accumulator, an array of vote counts over a grid of lines, and the list of its peaks, each a line with its number of votes. This is the problem of [line detection](/line-detection/).

A line is the set of points with $x \cos\theta + y \sin\theta = \rho$, with $0 \le \theta < \pi$ and $-D \le \rho \le D$. Here $(\cos\theta, \sin\theta)$ is the unit normal of the line and $|\rho|$ is its distance from the origin, the pixel $(0, 0)$. Every line has exactly one such pair, except for the choice of the sign at $\theta = 0$, and the range of both numbers is bounded, which is not true of the slope and the intercept. See [line representation](/line-representation/) for the other forms. With $y$ downward, $\theta$ turns from the $x$ axis toward the bottom of the image.

## The algorithm

The angle bins are $\theta_k = k \pi / T$ for $k = 0, \ldots, T - 1$. Let $D = \lceil \sqrt{(W - 1)^2 + (H - 1)^2} \rceil$. The distance bins have width 1 and the centers $\rho_j = j$ for $j = -D, \ldots, D$, and a value $\rho$ goes to the bin of the nearest integer, with halves rounded up. For every point of the image $|\rho| \le D$, so every vote has a bin.

```pseudo id=main
HOUGH(P, W, H, T)                           ▷ P is the list of edge points
L1  D ← ⌈√((W − 1)² + (H − 1)²)⌉
L2  acc[k][j] ← 0 for 0 ≤ k < T and −D ≤ j ≤ D
L3  for each point (x, y) in P do
L4      for k ← 0 to T − 1 do
L5          ρ ← x cos θ_k + y sin θ_k
L6          acc[k][round(ρ)] ← acc[k][round(ρ)] + 1    ▷ round half up
L7  return acc

PEAKS(acc, τ)                               ▷ τ is the least number of votes
L8  for each cell (k, j) in scan order do
L9      if acc[k][j] < τ then continue
L10     if a 3 × 3 neighbor has more votes, or the same votes and comes earlier in scan order, then continue
L11     report (acc[k][j], θ_k, j)
```

For a fixed point, the values of line L5 as a function of $\theta$ trace the curve $\rho = r \cos(\theta - \varphi)$, where $(r, \varphi)$ are the polar coordinates of the point. So each point votes along a sinusoid in the accumulator, and the sinusoids of collinear points cross in the cell of their common line. Line L10 is a [non-maximum suppression](/non-maximum-suppression/) in a $3 \times 3$ window, so a peak that spreads over two cells is reported once.

## Example

Take a $4 \times 4$ image with the 5 edge points $(0, 3)$, $(1, 2)$, $(2, 1)$, $(3, 0)$ and $(0, 0)$, and $T = 4$, so the angles are 0, 45, 90 and 135 degrees. Line L1 gives $D = \lceil \sqrt{18} \rceil = 5$, so there are 11 distance bins from $-5$ to 5. The values of $\rho$ are:

| point | $\theta = 0°$ | $45°$ | $90°$ | $135°$ |
|---|---|---|---|---|
| $(0, 3)$ | 0 | 2.12 | 3 | 2.12 |
| $(1, 2)$ | 1 | 2.12 | 2 | 0.71 |
| $(2, 1)$ | 2 | 2.12 | 1 | $-0.71$ |
| $(3, 0)$ | 3 | 2.12 | 0 | $-2.12$ |
| $(0, 0)$ | 0 | 0 | 0 | 0 |

At 45 degrees, the first four points all have $\rho = 3/\sqrt{2} \approx 2.12$, so the cell $(45°, 2)$ gets 4 votes. At 0 degrees, $(0, 3)$ and $(0, 0)$ share the cell $(0°, 0)$ with 2 votes, which is the line $x = 0$. At 90 degrees, $(3, 0)$ and $(0, 0)$ share the cell $(90°, 0)$, which is the line $y = 0$. At 135 degrees, all 5 points vote in different cells. With $\tau = 2$, PEAKS reports $(4, 45°, 2)$, then $(2, 0°, 0)$ and $(2, 90°, 0)$. The best line is $x \cos 45° + y \sin 45° = 2$, the cell nearest to the true line $x + y = 3$, which has $\rho = 2.12$.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, the accumulator counts, for each cell $(k, j)$, exactly the points whose line at the angle $\theta_k$ has its distance in $[j - \tfrac{1}{2}, j + \tfrac{1}{2})$, which is the definition by brute force over all pairs of a point and an angle. Second, if $m$ points lie on a line with the angle $\theta_k$ and a distance in the bin $j$, then the cell $(k, j)$ has at least $m$ votes. Third, for a line at an angle between two bins, the points of a segment of length $L$ have values of $\rho$ at the nearest angle bin that differ by at most $L \sin(\pi / (2T))$, so with $L \sin(\pi/(2T)) \le 1$ the votes of the segment at that angle fall in at most 2 adjacent cells, and one of them gets at least half of the votes. The tests check these facts against brute force voting over every pair of a point and an angle, and on lines with known parameters, where the top peak is within one bin of the true line.

## Complexity

Line L2 sets $T (2D + 1)$ counters, lines L3 to L6 do $N T$ votes of constant cost, and PEAKS reads each cell and its 8 neighbors. So the time is $\Theta(N T + T D)$ in the worst case and in the best case, and the accumulator takes $\Theta(T D)$ space. The $N T$ term of the votes is usually the larger one. A table of $\cos\theta_k$ and $\sin\theta_k$ makes each vote 2 multiplications, 1 addition and 1 rounding. To get a resolution of one pixel at the far end of a line of length $L$, the angle step must be about $1/L$, so $T$ grows with the size of the image, and the cost is then $\Theta(N \max(W, H))$.

## Properties

- **Robust to noise and gaps.** A point that is not on the line adds at most 1 vote to any cell of the line's angle. A gap in the line removes only the votes of the missing points.
- **Many lines at once.** All the lines are in the same accumulator, and the votes of one line do not move the peak of another, except where their sinusoids cross.
- **Linear in the points.** The accumulator of a union of point sets is the sum of their accumulators, so the votes can be split over threads or done in a stream.
- **Discrete.** The answer has the resolution of the grid. A finer grid splits the votes of a line that is not straight on the pixel grid, and a coarser grid merges near lines.
- **No endpoints.** A cell describes an infinite line. Segments need a second pass along each detected line.
- **Exact voting.** With the rounding of line L6 done exactly, the counts are the same as those of the brute force definition on every input.

## Variants and improvements

- **Votes along the gradient.** If each edge point also has a gradient direction, it can vote only for the angles near that direction. This divides the cost by $T$ up to a constant. O'Gorman and Clowes used this idea in 1976.
- **Probabilistic Hough transform.** Vote with a [random sample](/random-sampling/) of the points, and stop when a peak is clear. Kiryati, Eldar and Bruckstein analyzed this in 1991. The progressive version of Matas, Galambos and Kittler also removes the points of each line as it is found and returns segments.
- **Randomized Hough transform.** Pick 2 points at random and vote for the one line through both. This maps many points to few cells.
- **Circles and other curves.** For circles with center $(a, b)$ and radius $r$, each point votes in a 3D accumulator. With the gradient direction the vote reduces to a line in $(a, b)$ for each $r$.
- **Generalized Hough transform.** Dana Ballard in 1981 extended the method to any shape, with a table from the gradient direction to the offset of a reference point. This is close to [template matching](/template-matching/).
- **Peak refinement.** A least squares fit, as in [linear regression](/linear-regression/), to the points that voted for a peak gives a line with a precision finer than the grid.
- **Exact versions.** Without a grid, the problem of the line through the most points is the problem of [collinear points](/collinear-points/), solved in $O(N^2 \log N)$ time with the dual [line arrangement](/line-arrangement/).

## When to use it

Use the Hough transform when the edge map has several lines, with gaps, noise and other structures, and you know roughly the resolution you need. It is a good choice for lanes on roads, lines in documents, the edges of buildings and calibration patterns. If you have one line and few outliers, a least squares fit is simpler. If you have one line and many outliers, random sampling of pairs of points is often faster. If you need segments with exact endpoints, use the progressive probabilistic version or a detector of segments, see [line detection](/line-detection/).

## Pitfalls

- **Rounding with floor(rho + 0.5).** In floating point, $\lfloor \rho + 0.5 \rfloor$ rounds the largest number below $0.5$, which is $0.49999999999999994$, up to 1, because the sum $\rho + 0.5$ rounds to 1.0. The implementation takes $j = \lfloor \rho \rfloor$ and adds 1 if $\rho - j \ge 0.5$, which is exact. The difference is rare, but it makes the counts differ from a brute force check.
- **The size of the distance range.** With the origin at a corner, $\rho$ runs from about $-W$ to the diagonal. A range from 0 to the diagonal loses the lines with negative $\rho$.
- **The bin widths.** Too few angles spread the votes of a long line over several distance bins, too many split them over several angle bins. Choose the angle step near $1/L$ for the longest line $L$ you want to find.
- **Thick edges.** An edge map 3 pixels wide puts 3 parallel lines into the accumulator. Thin the edges first with [non-maximum suppression](/non-maximum-suppression/).
- **Double peaks at the wrap.** The angles $\theta$ near 0 and near $\pi$ describe the same lines with the opposite sign of $\rho$, so a line close to vertical can give peaks at both ends of the angle range.
- **The y axis.** With $y$ downward, an angle on the screen turns the other way from the usual mathematical angle. Draw the result with the same convention.

## Implementations

## History

Paul Hough filed a patent in 1960, granted in 1962 as US patent 3,069,654, "Method and means for recognizing complex patterns". It was for the tracks of particles in bubble chamber photographs, and it mapped each point to a line in a plane of slope and intercept. Slopes are not bounded, so the parameter plane was not either. Azriel Rosenfeld described the method in his book on picture processing of 1969. Richard Duda and Peter Hart wrote in 1972 that the normal form $\rho = x \cos\theta + y \sin\theta$ has bounded parameters, so each point maps to a sinusoid, and they extended the method to other curves. Dana Ballard generalized it to any shape in 1981. Illingworth and Kittler surveyed the many variants in 1988.

## References
