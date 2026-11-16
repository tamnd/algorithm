---
tag: 1ZMBCJ
kind: algorithm
slug: correlative-scan-matching
name: Real-time correlative scan matching
aliases:
- Olson correlative scan matching
area: robotics/localization-and-slam
level: advanced
summary: Finds the pose of a laser scan in a window of poses with the best score on a rasterized lookup table, exactly, by a best-first branch and bound over a coarse and a fine table.
solves: [mobile-robot-localization]
model: real-ram
complexity:
  vars: {n: the number of scan points, A: the number of angles of the window, S: the number of shifts per axis, D: the block side in cells, E: the number of fine poses scored, G: the number of cells of the table}
  time: {tables: O(G D), bounds: O(A (S/D)^2 (n + log(A S^2 / D^2))), fine: O(E n), worst: O(A S^2 n)}
  space: {extra: O(G + A n + A S^2 / D^2)}
properties: {deterministic: true, exact: true, online: true, global_in_window: true}
history:
  year: 2009
  people: [Edwin B. Olson]
  note: Olson scored a dense window of poses on a rasterized table of the scan likelihood and made it fast with a coarse table of maxima and a best-first search, with the covariance of the match from the same scores.
prereqs: [mobile-robot-localization, likelihood-field-model]
see_also: [best-first-branch-and-bound, sliding-window-maximum, iterative-closest-point, normal-distributions-transform, lidar-odometry-and-mapping, loop-closure-detection, template-matching, cross-correlation]
sources:
  - paper: doi:10.1109/ROBOT.2009.5152375
    title: "Edwin B. Olson, Real-time correlative scan matching, Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), 2009, pages 4387 to 4393"
    locator: "the rasterized lookup table of log probabilities, the multi-resolution search with the low resolution table of maxima, and the covariance estimate of equation (3)"
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 6, the likelihood field model of range finders, which the lookup table discretizes"
---

Real-time correlative scan matching finds the rigid motion between a laser scan and a reference, a previous scan or a map, by scoring every pose of a search window on a grid. It does not start from a guess and descend to a local optimum, as [iterative closest point](/iterative-closest-point/) does; within the window and at the resolution of the grid, it returns a pose with the best score. Olson (2009) made this fast in two ways. First, the reference is rasterized once into a lookup table, in the spirit of the [likelihood field](/likelihood-field-model/), so that the score of a pose is a sum of $n$ table reads. Second, a coarse table holds the maxima of blocks of the fine table. A coarse score bounds the fine scores of a whole block of shifts, and a best-first [branch and bound](/best-first-branch-and-bound/) scores only the blocks that can still win. The same scores also give a covariance of the match.

## In plain words

The robot has a picture of the walls from before, drawn on squared paper, where squares near a wall get high marks. It takes a new scan and wants to know how it moved. For every candidate turn and shift, it lays the scan on the paper and adds the marks under the scan points. The best total wins. To avoid trying every shift, it first uses a rougher sheet where each square holds the best mark of a group of squares. If a group of shifts cannot beat the best total so far even on the rough sheet, the robot skips the whole group.

## The problem

The input is a set of reference points $P$ in the plane, a scan $Q = \{q_1, \dots, q_n\}$ of points in the frame of the robot, a prior guess $(x_0, y_0)$, a list of $A$ angles $\theta$, and a window of shifts $t = (t_x, t_y)$ with $t_x, t_y \in \{-w, \dots, w\}$ cells of size $r$, so $S = 2w + 1$ shifts per axis. A table $L$ on the grid of cell size $r$ scores each cell. The score of the pose $(\theta, t)$ is

$$s(\theta, t) = \sum_{i=1}^{n} L\big(c_i(\theta) + t\big),$$

where $c_i(\theta)$ is the cell of the point $(x_0, y_0) + R(\theta)\, q_i$. The output is a pose $(\theta^*, t^*)$ of the largest score in the window.

**The table.** Olson fills each cell with the log probability of a scan point there, as the maximum over the reference points of a radially symmetric kernel of the distance. Taking the maximum instead of the sum approximates the likelihood of a point by its nearest reference point. The code uses the integer score $\mathrm{round}(100\, e^{-d^2 / (2\sigma^2)})$ with $d$ the distance to the nearest reference point within $3\sigma$; any score that decreases with $d$ works for the search, and integers make the comparisons exact. The sum over the scan points treats the points as independent, which is an approximation; it is the reason why the scores of a long scan are very sharp.

## The algorithm

Let $D$ be the side of a block of shifts. The coarse table is

$$L_D(c) = \max_{0 \le a, b < D} L(c + (a, b)),$$

the maximum of $L$ over the $D \times D$ cells whose lowest corner is $c$. For a block $B$ of shifts with the lowest corner $b$, every shift $t \in B$ is $b + (a, b')$ with $0 \le a, b' < D$, so $L(c_i(\theta) + t) \le L_D(c_i(\theta) + b)$ for each point, and

$$U(\theta, B) = \sum_{i} L_D\big(c_i(\theta) + b\big) \ \ge\ \max_{t \in B} s(\theta, t).$$

```pseudo id=main
CORRELATIVE-SCAN-MATCH(P, Q, (x0, y0), angles, w, r, D)
L1  L ← the lookup table of P on the grid of cell size r
L2  L_D ← the window maximum of L over D × D cells
L3  for each angle θ do                         ▷ the cells c_i(θ) of the scan
L4      for each block B of D × D shifts of the window, with the lowest corner b do
L5          push (U = Σ_i L_D(c_i(θ) + b), θ, B) on a max-heap H
L6  best ← -∞
L7  while H is not empty do
L8      pop (U, θ, B) with the largest U from H
L9      if U ≤ best then break
L10     for each shift t in B within the window do
L11         s ← Σ_i L(c_i(θ) + t);  if s > best then best ← s, pose ← (θ, t)
L12 return pose, best
```

The cells $c_i(\theta)$ of each angle are computed once. A shift then only adds an integer offset to each cell, so the score of a pose is $n$ table reads and additions. Line L2 is a 2D [sliding window maximum](/sliding-window-maximum/): first along one axis, then along the other.

**The coarse table must be a window maximum.** Olson describes the low resolution table as a table whose cells hold the maximum of the high resolution cells they cover, for example 30 cm cells over 3 cm cells. If the coarse cells form a fixed partition of the grid, a scan point and its shifts do not in general stay in one coarse cell, because the points $c_i(\theta)$ do not lie on the corners of the coarse grid. The code therefore uses the window maximum $L_D$, defined at every fine cell, which bounds every shift of the block for every point. The cost is a table of the size of $L$ instead of a table $D^2$ times smaller.

## Example

**The room.** The reference is the walls of a 4 m by 3 m room with a 1 m by 0.5 m box, 340 points spaced 5 cm. The table has cells of $r = 5$ cm, $\sigma = 5$ cm, and $105 \times 85$ cells. The window has 13 angles from $-0.12$ to $0.12$ rad in steps of $0.02$, and shifts of $\pm 8$ cells ($\pm 0.4$ m) around the guess $(1.2, 1.5)$, so $13 \times 17^2 = 3757$ poses. With $D = 4$, there are $5 \times 5$ blocks per angle, so 325 coarse scores.

The scans are about a quarter of the room points, seen from a random true pose with 2 cm noise per coordinate. For four scans, the measured results are:

| true pose $(x, y, \theta)$ | found pose | best score | fine poses scored |
|---|---|---|---|
| (1.043, 1.527, -0.026) | (1.05, 1.55, -0.04) | 6852 | 96 |
| (1.349, 1.555, -0.071) | (1.35, 1.55, -0.08) | 8247 | 112 |
| (1.105, 1.587, -0.044) | (1.10, 1.60, -0.04) | 8239 | 96 |
| (1.299, 1.264, 0.080) | (1.30, 1.25, 0.10) | 6742 | 96 |

In each case the search of all 3757 poses gives the same best score and the same pose. The branch and bound scored 325 coarse bounds and at most 112 fine poses, about 9 times fewer score evaluations. The found pose is within one cell and one angle step of the truth, which is the resolution of the window. Refine it with a finer window around the result, or with a local method such as [ICP](/iterative-closest-point/).

**A corridor.** The reference is two parallel walls 1 m apart, and the scan sees 2 m of both walls. The covariance from the scores of the window, with the weights $e^{0.05\,(s - s_{\max})}$, has the standard deviation $0.187$ m along the corridor, which is the spread of a uniform weight over the whole window of $\pm 0.3$ m. Across the corridor it is below 1 mm, and in the heading it is $0.016$ rad. The scan does not fix the position along the corridor, and the covariance shows it.

## Correctness

The [correctness proof](proofs/correctness.md) shows that the algorithm returns a pose with the largest score of the window. It uses two facts. The coarse score $U(\theta, B)$ is at least the score of every pose of the block, by the bound above. The blocks leave the heap in the order of decreasing $U$, so when line L9 stops, every block left in the heap has $U \le$ best, and none of its poses can have a larger score. Every pose of the window lies in exactly one block, and every block that is popped before the stop is scored in full.

The search is exact for the discrete problem: the best pose on the grid of angles and shifts, with the given table. It is not exact for the continuous problem. The grid limits the accuracy to about a cell and an angle step, and the table is a model whose kernel width is set by hand.

## Complexity

Let $G$ be the number of cells of the table and $E$ the number of fine poses that line L11 scores.

- Tables: $O(|P| (\sigma / r)^2)$ to stamp the kernels, and $O(G D)$ for the window maximum with running maxima of length $D$ along each axis. A monotone queue makes it $O(G)$. The tables are built once per reference and shared by all scans matched to it.
- Rotations: $O(A n)$.
- Bounds and heap: $A \lceil S / D \rceil^2$ coarse scores of $O(n)$ each, and as many heap operations.
- Fine scores: $O(E n)$, with $E \le A S^2$.

In the worst case, for example in a corridor where many poses score alike, the bound prunes little and the cost is that of the full search, $O(A S^2 n)$. In the room above, $E$ was about 100 out of 3757. Olson reports that the method runs in real time for windows of the size that odometry errors need; that is a measurement on his data.

## Properties

- **Global within the window.** It cannot be trapped by a local optimum inside the window, unlike ICP. It can fail only if the true pose is outside the window or the best score belongs to a wrong pose, as in a symmetric room.
- **Exact for the discrete problem and deterministic.** The result does not depend on the order of the heap, except for which of several equal best poses it returns.
- **The covariance comes free.** Olson's equation (3) gives the covariance from the scores that the search computes, $\Sigma = K/s - u u^\top / s^2$ with $K = \sum_j w_j x_j x_j^\top$, $u = \sum_j w_j x_j$ and $s = \sum_j w_j$, over the poses $x_j$ with the weights $w_j$ of their likelihoods. It shows ambiguity, such as in a corridor, which a single best pose hides. The pruned search does not score every pose, so the code computes the covariance from a full scan of the window.
- **Resolution bound.** The accuracy is that of the grid.

## Variants and improvements

- **More levels.** Use a pyramid of window maximum tables with the sides $D, D^2, \dots$, and branch from coarse to fine. This is the precomputed grid scheme used for loop closure in Google's Cartographer.
- **Depth-first search.** Explore the most promising block first and keep the best score as a bound, as in [depth-first branch and bound](/depth-first-branch-and-bound/). It needs less memory than a heap of all blocks.
- **Refinement.** Run a fine window, or a local optimizer, around the result to get below the cell size.
- **Probabilistic tables.** Fill the table with log probabilities, as Olson does, so that the scores and the covariance have a probabilistic meaning; the integer table of the code is a scaled and rounded version.
- **Loop closure.** With a large window around the guess, the same search checks a loop closure candidate; see [loop closure detection](/loop-closure-detection/).

## When to use it

Use correlative scan matching for 2D laser odometry and for loop closure, when the error of the prior guess is larger than the basin of convergence of ICP, and when a covariance of the match is needed for a [pose graph](/pose-graph-optimization/). Use ICP or the [normal distributions transform](/normal-distributions-transform/) when the guess is good and sub-cell accuracy is needed quickly. For 3D scans, the dense window becomes too large; use local methods or feature matching.

## Pitfalls

- **A coarse table of fixed blocks.** A table whose coarse cells partition the grid is not an upper bound for scan points off the coarse corners. The branch and bound can then prune the best block and return a worse pose without a sign of error. Use the window maximum, or align the shifts so that the bound holds.
- **The window too small.** The result is the best pose in the window. If the true pose is outside, the search returns a wrong pose with a confident score. Size the window from the odometry error.
- **The kernel too narrow.** With $\sigma$ below the cell size, a small error gives no score, and the scores of most poses are 0, which leaves nothing to rank them. With $\sigma$ too large, nearby poses score alike and the match is blurred.
- **Overconfident covariance.** The sum over independent points makes the likelihood far too sharp. Scale the scores down before the covariance, as the test does with the factor $0.05$, and choose the factor by checks on real data.
- **Symmetric places.** In a corridor or a symmetric room, several poses score alike. Look at the covariance, or at the second best score, before trusting a match.

## Implementations

## History

Correlation of scans on a grid of poses is an old idea in robotics and in image [template matching](/template-matching/), but a dense search was long thought too slow for real time. Olson (2009) showed that a rasterized lookup table, a coarse table of maxima and a best-first search make it fast enough for laser odometry and loop closure. Hess, Kohler, Rapp and Andor (2016) used a related branch and bound over precomputed grids for loop closure in Cartographer.

## References
