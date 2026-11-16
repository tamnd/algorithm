---
tag: Z398RM
kind: algorithm
slug: vector-field-histogram
name: Vector field histogram
aliases:
- VFH
area: robotics/mobile-and-legged-robots
level: core
summary: Builds a polar histogram of obstacle density around the robot from a grid and steers through the valley closest to the goal.
model: real-ram
complexity:
  vars: {w: "the width of the active window in cells", n: "the number of sectors", l: "the half-width of the smoothing window in sectors"}
  time: {worst: O(w^2 + n l)}
  space: {extra: O(n)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 1991
  people: [Johann Borenstein, Yoram Koren]
  note: "Borenstein and Koren replaced the single force vector of their virtual force field method with a polar histogram, so that the robot could find and pass gaps between obstacles."
prereqs: [occupancy-grid-map, potential-field-method]
see_also: [dynamic-window-approach, velocity-obstacle, occupancy-grid-mapping, bug-algorithms, unicycle-model, pure-pursuit, configuration-space, motion-planning]
sources:
  - paper: doi:10.1109/70.88137
    title: "The vector field histogram, fast obstacle avoidance for mobile robots"
    locator: "Section 4 (eqs. 1 to 5 for the polar histogram and its smoothing, Section 4.2 for valleys and steering, Section 4.3 for the threshold, Section 4.4 and eqs. 8 to 10 for the speed)"
---

The vector field histogram (VFH) is a local obstacle avoidance method for a mobile robot with range sensors. It keeps a grid of certainty values around the robot, in the style of an [occupancy grid](/occupancy-grid-map/). At each cycle it reduces the cells near the robot to a polar histogram: for each angular sector, a number that grows with the certainty and the closeness of the cells in that direction. It smooths the histogram, marks the sectors below a threshold as free, and steers into the run of free sectors (a valley) that is closest to the direction of the goal. A second rule lowers the speed when an obstacle lies ahead or the robot turns fast. VFH followed the [potential field method](/potential-field-method/) and its weakness: summing all obstacle forces into one vector hides a gap between two obstacles, while a histogram keeps it.

## In plain words

Picture the robot in the middle of a clock face. For each hour mark, it asks: how much obstacle is in that direction, and how close? It draws a bar for each direction. Tall bars mean "blocked", short bars mean "open".

Then it looks for a run of open directions, like a gap between two tall bars. It picks the gap that is nearest to the direction of the goal. If the gap is narrow, the robot drives through its middle. If the gap is wide, the robot drives along its edge, at a safe angle from the obstacle beside it. When the bars straight ahead are tall, or when it has to turn hard, it slows down.

## The problem

**Input.** A histogram grid: a certainty value $c_{ij} \ge 0$ for each square cell (here 10 cm wide); the position of the robot; its heading; the direction to the target; and the parameters below. Arithmetic, square roots and arc tangents cost one step each, as in the [real RAM](/real-ram/).

**Output.** A steering direction $\theta$ inside a free sector, or "stop" if no sector is free, and a speed.

**How it differs from close pages.** A [potential field](/potential-field-method/) sums forces into one vector and can be pushed back from a gap that is wide enough to pass. The [dynamic window approach](/dynamic-window-approach/) searches over velocities and respects the accelerations of the robot, with a stopping test; VFH chooses a direction first and has no such test. [Bug algorithms](/bug-algorithms/) follow obstacle boundaries with a guarantee of reaching the goal in the plane, but need exact contact sensing. [Velocity obstacles](/velocity-obstacle/) handle moving obstacles.

## The algorithm

With $n$ sectors of width $\alpha = 360°/n$, a window of $w \times w$ cells, and positive constants $a$ and $b$ with $a - bd_{\max} = 0$, where $d_{\max}$ is the distance from the robot to the farthest cell of the window:

```pseudo id=main
VFH(grid c, position p, heading, target direction)
L1  h[0..n-1] ← 0
L2  for each cell (i, j) of the w × w window around p:  β ← direction from p to the cell;  d ← distance;  h[⌊β/α⌋] += c_ij² (a - b d)
L3  h′[k] ← Σ_{|j| ≤ l} (l + 1 - |j|) h[k + j] / (l + 1)²   (indices mod n)
L4  free[k] ← h′[k] < τ
L5  if no sector is free then return stop;  k_t ← the sector of the target;  if all are free then return k_t
L6  V ← the valley (maximal run of free sectors) that contains k_t, or else has a border nearest to k_t
L7  if V has more than s_max sectors then θ ← the sector of V nearest to k_t that is at least s_max/2 inside both borders, else θ ← the middle of V
L8  v ← V_max (1 - min(h′[current], h_m)/h_m) (1 - |Ω|/Ω_max) + V_min
```

Line L2 is eqs. 1 to 4 of Borenstein and Koren. The square of the certainty favors cells that many readings confirm; the term $a - bd$ is 0 at the farthest cell of the window and grows linearly for closer cells. Line L3 smooths the histogram, because the grid makes it ragged: in the Example below, one sector between two obstacle cells gets nothing. The paper's eq. 5 lists a triangular window with the middle weight $l$ and divides by $2l + 1$; that does not match the sum of its weights, so the code divides by the sum of the weights, which only rescales the threshold $\tau$.

Line L7 is the steering rule of Section 4.2. When the target lies outside the valley, let $k_n$ be the free sector nearest to it and $k_f = k_n \pm s_{\max}$; the robot steers at $(k_n + k_f)/2$, that is, $s_{\max}/2$ sectors from the obstacle. In a narrow valley, $k_f$ is the other border and the robot steers through the middle. The paper describes the rule for a target direction that is blocked. For a target inside a wide valley, the code steers straight at the target when it is at least $s_{\max}/2$ sectors inside both borders, and otherwise at the nearest sector that is; this agrees with the paper's rule at the borders. Line L8 is eqs. 8 to 10, where $h'_c$ is the smoothed density in the current direction of travel and $\Omega$ is the turn rate. The code returns the center of the chosen sector, so $\theta$ is quantized to $\alpha$.

The paper uses a window of $33 \times 33$ cells of 10 cm, $\alpha = 5°$ so $n = 72$, $l = 5$, $s_{\max} = 18$, $\Omega_{\max} = 120$ deg/s and $V_{\min} = 4$ cm/s.

## Example

The robot is at the center of cell $(0, 0)$. Five cells with certainty 3 form a short wall 1 m ahead, at cells $(10, -2)$ to $(10, 2)$. With $b = 1$ per meter, $a = d_{\max} = \sqrt2 \cdot 16 \cdot 0.1 = 2.263$ m. The middle cell is at 1 m, so it adds $9 \cdot (2.263 - 1) = 11.365$ to sector 0. The other cells lie at $\pm 5.7°$ and $\pm 11.3°$, so they go to sectors 1, 2, 70 and 69. Sector 71 gets nothing.

After smoothing, sector 0 has 6.90, sectors 1 and 71 have 6.58, and the values fall off on both sides to 0.31 at sectors 7 and 64. The target is straight ahead, at 0°.

| Threshold $\tau$ | Blocked sectors | Nearest free border | Steering direction |
|---|---|---|---|
| 5 | 69 to 2 | sector 3 | sector 12, 62.5° |
| 2 | 67 to 4 | sector 5 | sector 14, 72.5° |
| 1 | 66 to 5 | sector 6 | sector 15, 77.5° |

The valley on the other side of the wall is wide, so the robot steers $s_{\max}/2 = 9$ sectors beyond the near border: it turns left and leaves the wall on its right. A higher threshold makes the blocked range narrower, so the robot turns less.

## Correctness

VFH is a heuristic, with no guarantee of collision avoidance or of reaching the goal. The steering rule itself has a simple guarantee, which the [proof](proofs/correctness/) shows: when some sector is free, the returned direction lies in a free sector, and when the target sector is free with at least $s_{\max}/2$ free sectors on each side, the robot steers straight at it. The proof also shows that line L2 assigns each cell to exactly one sector, so the histogram sums all the magnitudes, and that rotating the grid by a multiple of $\alpha$ about the robot shifts the histogram by the same number of sectors. The tests check these facts on random grids and random histograms, the smoothing against its definition, and hand cases of the steering rule.

A collision can still happen: the threshold may hide an obstacle until the robot is close, the grid may be wrong, and the robot does not turn instantly. Measured in this code, with a point robot that turns at most 120 deg/s, a cycle of 0.16 s and a top speed of 0.6 m/s, through a gap of 1.2 m in a wall with a thin pole on the way: thresholds 2, 5, 10 and 20 reached the target in 80, 61, 64 and 57 cycles; threshold 1 blocked the gap and never reached it; threshold 40 reached it but passed 5.7 cm from the center of a wall cell.

## Complexity

- **Time.** Line L2 visits $w^2$ cells, line L3 costs $O(nl)$, and lines L4 to L7 scan the sectors a constant number of times, so one cycle costs $O(w^2 + nl)$. With the paper's values, that is 1089 cells and 792 products. Measured: one cycle takes about 2 to 5 ms in this pure Python code.
- **Space.** $O(n)$ for the two histograms, besides the grid.

## Properties

- **Keeps gaps visible.** Unlike one summed force vector, the histogram shows each gap between obstacles, so the robot can pass a door.
- **Insensitive threshold.** Borenstein and Koren report that raising or lowering the threshold by a factor of 3 or 4 changes only the width of the valleys. The table of the Example shows the same effect.
- **Smooth steering.** The averaging over many cells and the smoothing make the steering direction change only a little from one cycle to the next.
- **No dynamics.** The method does not model the accelerations or the shape of the robot; the speed rule and $s_{\max}$ make up for that only in part.
- **Local.** It can be trapped by a U-shaped obstacle, or swing between two valleys of the same quality.

## Variants and improvements

- **VFH+.** Ulrich and Borenstein enlarged obstacle cells by the robot radius, used a binary histogram with hysteresis, and masked the sectors that the robot cannot reach with its turning radius.
- **VFH\*.** Ulrich and Borenstein looked ahead with an A\*-style search over several steps of VFH+ to avoid dead ends.
- **Virtual force field (VFF).** The earlier method of the same authors: the same grid, with each cell pushing the robot by a force and the target pulling it.
- **Adaptive threshold.** The paper suggests a high-level planner that raises the threshold, and lowers the speed, to pass a narrow door.

## When to use it

Use VFH as a reactive layer on a robot with noisy range sensors, such as sonars, that must move without stopping among unknown obstacles. Its histogram grid is cheap to update from each reading. Pair it with a global planner for long routes. When the accelerations or the shape of the robot matter, the [dynamic window approach](/dynamic-window-approach/) or VFH+ is a better fit.

## Pitfalls

- **The threshold.** Far too high, and the robot sees an obstacle only when it is close and may hit it; far too low, and narrow passages disappear.
- **The ragged histogram.** Without smoothing, single empty sectors between obstacle cells look like gaps the robot can pass.
- **The sector of 360°.** Indices are circular. A valley can wrap around sector 0, and the nearest border must be found in both directions.
- **The window corner.** With $a - bd_{\max} = 0$, cells in the corners of the square window add almost nothing, while cells at the same distance in other directions are not even in the window. A circular window is more uniform, at a small cost.
- **The speed formula.** As written, eq. 10 adds $V_{\min}$ to the result, so the speed can reach $V_{\max} + V_{\min}$.

## Implementations

## History

Borenstein and Koren built the virtual force field method in the late 1980s for fast robots with ultrasonic sensors, on a histogram grid that increments one cell per reading. They found that summing all forces into one vector loses the shape of the obstacles, so the robot could not pass narrow openings. The vector field histogram, published in 1991, kept the intermediate polar histogram to solve that. Ulrich and Borenstein extended it to VFH+ in 1998 and to VFH\* in 2000.

## References
