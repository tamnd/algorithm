---
tag: NBXJ4P
kind: algorithm
slug: occupancy-grid-mapping
name: Occupancy grid mapping
aliases:
- log-odds occupancy update
- Moravec-Elfes mapping
area: robotics/localization-and-slam
level: core
summary: Builds an occupancy grid from known poses by adding the log odds of an inverse sensor model to each cell that a reading touches.
model: word-ram
complexity:
  vars: {g: the number of grid cells, b: the number of beams in one scan, T: the number of scans}
  time: {per_scan: O(g b), worst: O(T g b)}
  space: {extra: O(1), total: O(g)}
properties: {deterministic: true, exact: false, online: true, incremental: true}
history:
  year: 1985
  people: [Hans Moravec, Alberto Elfes]
  note: Moravec and Elfes built grids of occupancy probabilities from wide angle sonar readings in 1985, and Elfes described the grid as a random field updated by Bayes' rule in 1989.
prereqs: [bayes-theorem, bayes-filter, occupancy-grid-map]
see_also: [occupancy-grid-map, inverse-sensor-model, octree-occupancy-map, bayes-filter, grid-based-rbpf-slam, bresenham-line-algorithm, amanatides-woo-traversal, frontier-based-exploration]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 9, Section 9.2 (the algorithm of Table 9.1, the inverse range sensor model of Table 9.2 and the factorization over cells), Section 9.4 (maps with forward models), and Chapter 4, Section 4.2 (the binary Bayes filter with static state)"
  - paper: doi:10.1109/ROBOT.1985.1087316
    title: "Hans P. Moravec and Alberto Elfes, High resolution maps from wide angle sonar, Proceedings of the 1985 IEEE International Conference on Robotics and Automation, volume 2, pages 116 to 121"
    locator: the grid of cells with probabilities of empty and occupied space, built from many sonar cones
  - paper: doi:10.1109/2.30720
    title: "Alberto Elfes, Using occupancy grids for mobile robot perception and navigation, Computer 22(6), 1989, pages 46 to 57"
    locator: the occupancy grid as a random field of cell states, updated by Bayes' rule from sensor readings
---

Occupancy grid mapping builds a map of a robot's world from range readings taken at known poses. The map is an [occupancy grid map](/occupancy-grid-map/): each cell $m_i$ holds the probability that something occupies it, stored as log odds $l_i$. For each new scan, the algorithm asks an [inverse sensor model](/inverse-sensor-model/) how likely each cell is to be occupied given this scan alone, and adds the log odds of the answer to the cell, minus the log odds of the prior. Each cell is a separate [binary Bayes filter](/bayes-filter/) with a static state. The method is exact under one strong approximation, that the cells are independent of each other, and it costs $O(g)$ evaluations of the inverse model per scan for a grid of $g$ cells. The poses must be known; if they are not, the problem is SLAM, and a method such as [grid-based Rao-Blackwellized particle filter SLAM](/grid-based-rbpf-slam/) runs this algorithm once per particle.

## In plain words

Draw a grid of small squares over the floor. At first the robot does not know anything about any square, so each square says "maybe". The robot stands at a known place and sends out laser beams. A beam stops at a wall. Every square that the beam passes through is probably empty, so it moves a little towards "empty". The square where the beam stops is probably a wall, so it moves a little towards "full". Squares that no beam reaches do not change. The robot does this again and again from many places. A square that many beams pass through becomes very sure to be empty, and a square where many beams stop becomes very sure to be a wall. The robot does not multiply small numbers: it adds a score for "full" and subtracts a score for "empty", which is the same thing in a different unit.

## The problem

The input is a sequence of poses $x_{1:T}$ of the robot, each a planar pose $(x, y, \theta)$ in meters and radians, and a scan $z_t$ taken at each pose. A scan is a set of beams: beam $k$ has the bearing $\theta_k$ in the robot frame and the measured range $z_t^k$, at most the maximum range $z_{\max}$. The map $m$ is a grid of cells $m_1, \ldots, m_g$, and each cell is occupied ($m_i = 1$) or free ($m_i = 0$). The notation is the one of Thrun, Burgard and Fox (2005).

The goal is the posterior $p(m \mid z_{1:t}, x_{1:t})$. It is a distribution over $2^g$ maps, which is far too large to store. The algorithm stores instead the $g$ marginals $p(m_i \mid z_{1:t}, x_{1:t})$ and uses them as if

$$p(m \mid z_{1:t}, x_{1:t}) = \prod_{i=1}^{g} p(m_i \mid z_{1:t}, x_{1:t}).$$

This independence of the cells is an approximation that makes the update tractable, not a property of real maps: two neighboring cells of one wall are clearly not independent. Each cell keeps its log odds

$$l_{t,i} = \log \frac{p(m_i \mid z_{1:t}, x_{1:t})}{1 - p(m_i \mid z_{1:t}, x_{1:t})}, \qquad l_0 = \log \frac{p(m_i)}{1 - p(m_i)},$$

where $p(m_i)$ is the prior probability of occupancy, often $0.5$, so that $l_0 = 0$.

## The algorithm

The first procedure is Thrun et al., Table 9.1. The second is the inverse range sensor model of Table 9.2, for a planar scanner with a beam width $\beta$ and an obstacle thickness $\alpha$.

```pseudo id=main
OCCUPANCY-GRID-MAPPING(l, x_t, z_t)           ▷ l_i = l_(t-1,i) for each cell m_i
L1  for each cell m_i do
L2      if m_i is in the perceptual field of z_t then
L3          l_i ← l_i + INVERSE-SENSOR-MODEL(m_i, x_t, z_t) - l_0
L4      else l_i stays the same
L5  return l

INVERSE-SENSOR-MODEL(m_i, x_t, z_t)           ▷ x_t = (x, y, theta)
L6  (x_i, y_i) ← the center of cell m_i
L7  r ← sqrt((x_i - x)^2 + (y_i - y)^2);  phi ← atan2(y_i - y, x_i - x) - theta
L8  k ← the beam j with the smallest |phi - theta_j|, angles wrapped to [-pi, pi)
L9  if r > min(z_max, z_t^k + alpha/2) or |phi - theta_k| > beta/2 then return l_0
L10 if z_t^k < z_max and |r - z_t^k| < alpha/2 then return l_occ
L11 if r ≤ z_t^k then return l_free
L12 return l_0
```

Line L7 gives the range and the bearing of the cell center as seen from the robot. Line L8 picks the beam that points closest to the cell. Line L9 returns the prior for a cell that is behind the reading or outside the beam: the scan says nothing about it. Line L10 marks a cell near the end point of the beam as occupied, except when the reading is a max range reading, which means that the beam hit nothing. Line L11 marks a cell in front of the end point as free. Line L12 is only reached on the boundary $r = z_t^k + \alpha/2$ when $|r - z_t^k| < \alpha/2$ fails; Table 9.2 has no line for this case, and the prior is the natural value.

The values are $l_{\mathrm{occ}} = \log(0.7/0.3) = 0.84730$ and $l_{\mathrm{free}} = \log(0.4/0.6) = -0.40547$ in the implementation below. These probabilities are rules of thumb, not values derived from the sensor; Thrun et al. (Section 9.3) show how to learn an inverse model from data instead.

The perceptual field test of line L2 needs no separate geometry: a cell outside the field gets $l_0$ from the inverse model, and line L3 would add zero. The implementation therefore calls the model for each cell within $z_{\max} + \alpha$ of the robot and skips the cells farther away, which the model would map to $l_0$ anyway.

## Example

The robot is at $(0, 0)$ with heading $\theta = 0$. Its scan has one beam at bearing $0$ with range $z = 1.0$ m, and $z_{\max} = 3$ m, $\alpha = 0.2$ m, $\beta = 0.1$ rad. The prior is $p(m_i) = 0.5$, so $l_0 = 0$.

| cell center (m) | $r$ (m) | rule | value |
|---|---|---|---|
| $(0.5, 0)$ | 0.5 | L11, in front of the end point | $l_{\mathrm{free}} = -0.40547$ |
| $(0.95, 0)$ | 0.95 | L10, $\lvert r - z \rvert = 0.05 < 0.1$ | $l_{\mathrm{occ}} = 0.84730$ |
| $(1.05, 0)$ | 1.05 | L10 | $l_{\mathrm{occ}} = 0.84730$ |
| $(1.2, 0)$ | 1.2 | L9, $r > z + \alpha/2 = 1.1$ | $l_0 = 0$ |
| $(0.5, 0.5)$ | 0.707 | L9, bearing $\pi/4 > \beta/2$ | $l_0 = 0$ |

If the robot takes the same scan three times, a cell at $(0.5, 0)$ ends at $l = 3 \cdot (-0.40547) = -1.21640$, which is the probability $(0.4/0.6)^3 / (1 + (0.4/0.6)^3) = 8/35 = 0.2286$. A cell at $(1.0, 0)$ ends at $l = 2.54189$, which is $0.343 / 0.370 = 0.9270$. A cell that is seen as free once and as occupied once ends at $l = 0.44183$, which is $0.6087$: one hit outweighs one miss, because $0.84730 > 0.40547$.

The term $-l_0$ matters when the prior is not $0.5$. With $p(m_i) = 0.3$, the prior is $l_0 = -0.84730$. Two hits must give $l = l_0 + 2 (0.84730 - l_0) = 2.54189$, which is $0.9270$, the same value as above. A program that forgets $-l_0$ gets $l_0 + 2 \cdot 0.84730 = 0.84730$, which is $0.7$, and so it counts the prior twice too often.

The tests also map a room of 4 m by 3 m with walls through the cell centers, from three poses and 120 beams per scan, on a grid of 51 by 41 cells of 0.1 m. All wall cells away from the corners end with $l > 0$, all interior cells with $l < 0$, and every cell 0.2 m or more behind a wall keeps exactly $l_0$.

## Correctness

Fix one cell $m_i$. Assume that, given $m_i$ and the poses, the scan $z_t$ is independent of the earlier scans, and that the inverse model returns the log odds of $p(m_i \mid z_t, x_t)$. Then Bayes' rule, written in odds, gives

$$l_{t,i} = l_{t-1,i} + \log \frac{p(m_i \mid z_t, x_t)}{1 - p(m_i \mid z_t, x_t)} - l_0,$$

because the evidence $p(z_t \mid z_{1:t-1}, x_{1:t})$ cancels in the ratio of the two posteriors for $m_i = 1$ and $m_i = 0$, and $p(z_t \mid m_i, x_t)$ is turned into $p(m_i \mid z_t, x_t)$ by Bayes' rule once more, which brings in the prior. Line L3 is this equation. By induction, $l_{T,i} = l_0 + \sum_t (\mathrm{ism}_t(m_i) - l_0)$, and the order of the scans does not matter. The assumption is the approximation of independent cells in another form: the readings depend on the other cells too, so the result is the posterior of the cell only under that assumption. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $g$ be the number of cells, $b$ the number of beams in a scan and $T$ the number of scans. The bounds are in the [word RAM](/word-ram/) model, with one step for each arithmetic operation on a log odds value, which is a floating-point number in one word.

- One call of the inverse model costs $O(b)$ for the search of line L8, and $O(1)$ for the rest. If the beams are evenly spaced, the index $k$ is a rounding of $(\phi - \theta_1) / \Delta\theta$, and the call costs $O(1)$.
- One scan costs $O(g b)$ in the worst case, and $O(g)$ with evenly spaced beams. Only cells within $z_{\max} + \alpha$ of the robot can change, so with a cell side $s$ the number of cells visited is at most about $\pi (z_{\max} + \alpha)^2 / s^2$, whatever the size of the grid.
- $T$ scans cost $O(T g b)$ time. The memory is the grid, $O(g)$, and the update needs $O(1)$ extra memory, since it changes the grid in place.

The variant that traces each beam through the grid instead of testing each cell costs $O(b\, z_{\max} / s)$ per scan: each beam crosses at most about $z_{\max} / s$ cells.

## Properties

- **Additive and commutative.** The map after $T$ scans is $l_0$ plus a sum of terms, one per scan. Scans can be added in any order, and a scan can be removed by subtracting its term.
- **Incremental and online.** Each scan updates the grid in place, and old scans are not stored.
- **No normalization and no products.** Log odds turn the product of likelihood ratios into a sum, so the update cannot underflow and needs no division. Probabilities come back by $p = 1 - 1 / (1 + e^{l})$ when they are needed.
- **Unbounded certainty.** Without clamping, $l_i$ grows linearly with the number of consistent readings, so a cell seen 100 times as free has $l = -40.5$ and needs 48 hits to get back above $l_0$ with the values above.
- **Not exact for the joint map.** The output is the product of the per-cell posteriors under the independence approximation. It is not the marginal of the true joint posterior over maps.

## Variants and improvements

- **Ray casting of each beam.** Trace each beam from the robot to its end point with the [Bresenham line algorithm](/bresenham-line-algorithm/) or the [Amanatides-Woo traversal](/amanatides-woo-traversal/), update the cells it crosses as free and the end cell as occupied. This visits only the cells that change and is the usual form for laser scanners.
- **Clamping.** Keep each $l_i$ between two bounds, so that the map can adapt when the world changes. The [octree occupancy map](/octree-occupancy-map/) (OctoMap) uses clamping thresholds and then merges identical children of the tree.
- **Learned inverse models.** Thrun et al. (Section 9.3) learn the inverse model by sampling maps and readings from the forward model, instead of using fixed values such as 0.7 and 0.4.
- **Forward models and MAP maps.** Thrun et al. (Section 9.4) search for the most likely map under the forward [beam range finder model](/beam-range-finder-model/), which keeps the dependencies between cells that the inverse model ignores. It is a batch method, and it needs a search over maps.
- **Several sensors.** With sonar and laser on one robot, Thrun et al. (Section 9.2) keep one grid per sensor and combine the grids per cell, for example by the maximum, because the sensors see different obstacles.
- **Unknown poses.** When the poses are estimated, the algorithm runs inside SLAM: once per particle in [grid-based Rao-Blackwellized particle filter SLAM](/grid-based-rbpf-slam/), or once after a [pose graph optimization](/pose-graph-optimization/) with the corrected poses.

## When to use it

Use it when the poses are known or estimated well, and the robot needs a dense map of free and occupied space for planning, exploration or localization. It is simple, each scan touches only the cells near the robot, and it fuses noisy readings over time. For 3D maps, a dense grid of cells uses too much memory; use an [octree occupancy map](/octree-occupancy-map/). For maps of point landmarks, use a feature map and the [landmark measurement model](/landmark-measurement-model/) instead.

## Pitfalls

- **Forgetting the prior term.** The update is $l + \mathrm{ism} - l_0$. With a prior of $0.5$ the term is zero and the mistake is invisible, but with any other prior it counts the prior once for every scan.
- **Wrong angle differences.** The difference $\phi - \theta_k$ must be wrapped to $[-\pi, \pi)$. Without wrapping, a cell behind the robot at a bearing of $\pi - 0.01$ and a beam at $-\pi + 0.01$ look $2\pi$ apart, and the cell is never updated.
- **Max range readings.** A reading at $z_{\max}$ usually means that the beam hit nothing. Marking its end as occupied puts a ring of false obstacles at the maximum range. Many implementations also skip the free update for such beams, because the reading may come from a glass surface or a failed return.
- **Too much confidence.** Neighboring beams and repeated scans from the same pose are not independent, so the sum counts the same evidence many times. The resulting probabilities are too close to 0 and 1. Clamping limits the effect; it does not remove it.
- **Beam width and cell size.** If $\beta$ is less than the angle between two beams, cells between the beams far from the robot are never updated, and the map has radial gaps. If $\alpha$ is less than the cell side, some walls fall between cell centers and get no hit.
- **Moving objects and wrong poses.** People who walk by leave traces, and a pose error of a few degrees smears the walls. The algorithm assumes a static world and known poses, and it cannot correct either.

## Implementations

## History

Moravec and Elfes (1985) built maps from many readings of wide angle sonar sensors on a mobile robot. Each reading told something about a cone of space: probably empty inside, probably occupied near the arc at the measured range. They kept these probabilities in a grid of cells. Elfes (1989) presented the occupancy grid as a random field of cell states, estimated by Bayes' rule, and used it for navigation. The log odds form with an inverse sensor model, and its derivation as a binary Bayes filter for each cell, are the ones of Thrun, Burgard and Fox (2005), Chapter 9, which also describes the limits of the independence assumption.

## References
