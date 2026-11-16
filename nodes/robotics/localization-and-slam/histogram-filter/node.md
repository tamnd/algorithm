---
tag: JZ7RY4
kind: algorithm
slug: histogram-filter
name: Histogram filter
aliases:
- discrete Bayes filter
- grid localization
area: robotics/localization-and-slam
level: core
summary: A Bayes filter over a fixed grid of cells that split a continuous state space. It can hold any belief shape, at a cost that grows with the number of cells.
solves: [filtering]
model: real-ram
complexity:
  vars: {g: the number of cells, b: the number of cells that one motion step can reach from a cell, T: the number of time steps}
  time: {worst: O(T g^2), banded: O(T g b)}
  space: {extra: O(g)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 1971
  people: [Richard S. Bucy, Kenneth D. Senne]
  note: Bucy and Senne ran the Bayes recursion for a nonlinear filter numerically on a grid of points, with an accuracy set by the grid.
prereqs: [bayes-filter]
see_also: [markov-localization, monte-carlo-localization, kalman-filter, particle-filter, forward-algorithm, occupancy-grid-map, convolution, fast-fourier-transform]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 4, Section 4.1 (the discrete Bayes filter and the histogram filter with its decomposition of a continuous space), and Chapter 8, Section 8.2 (grid localization)"
  - paper: doi:10.1016/0005-1098(71)90121-X
    title: "Richard S. Bucy and Kenneth D. Senne, Digital synthesis of non-linear filters, Automatica 7(3), 1971, pages 287 to 298"
    locator: the Bayes recursion of a nonlinear filter evaluated on a grid, with the convolution of the prediction done numerically
  - paper: "Stuart C. Kramer and Harold W. Sorenson, Recursive Bayesian estimation using piece-wise constant approximations, Automatica 24(6), 1988, pages 789 to 801"
    locator: the density held as a piecewise constant function on cells, and the analysis of how its error can grow
  - paper: "Wolfram Burgard, Dieter Fox, Daniel Hennig and Timo Schmidt, Estimating the absolute position of a mobile robot using position probability grids, Proceedings of the Thirteenth National Conference on Artificial Intelligence (AAAI-96), 1996"
    locator: a grid over the three pose coordinates of a robot, updated by the Bayes filter (general locator)
---

The histogram filter is the [Bayes filter](/bayes-filter/) run on a fixed partition of a continuous state space into $g$ cells. It keeps one probability per cell, so it can hold a belief of any shape: one peak, several peaks, or almost no information. It is exact for the discrete model that the partition defines, and an approximation of the continuous model, with an error that depends on the cell size. For a robot pose in a known map it is grid [Markov localization](/markov-localization/). One step costs $O(g^2)$ time, or $O(g b)$ when a motion step can reach only $b$ cells, and $O(g)$ memory.

## In plain words

Cut the world into small boxes of equal size and give each box a number: the chance that the robot is in that box. When the robot moves, each box hands its number to the boxes that the robot can reach from it, more to the box where the move should end and less to its neighbors. When the robot measures something, each box multiplies its number by how well the measurement fits a robot at the middle of the box. Then all numbers are divided by their total, so they add up to one again. Smaller boxes give a more exact answer but take more work.

## The problem

The state $x_t$ is continuous, for example the position of a robot on a line or its pose $(x, y, \theta)$ in a map. The model is the one of the Bayes filter: a motion model $p(x_t \mid u_t, x_{t-1})$, a measurement model $p(z_t \mid x_t)$ and a prior. The exact Bayes filter needs integrals over the state space, which have no closed form for most nonlinear models.

The histogram filter replaces the state space by $g$ cells $X_1, \ldots, X_g$ that cover it and do not overlap. Let $c_k$ be a representative point of cell $k$, usually its center. The belief is the list $p_{1,t}, \ldots, p_{g,t}$ of the probabilities of the cells. Two approximations turn the model into a model on the cells (Thrun et al., Section 4.1):

- the transition $P(k \mid u_t, i)$ is the probability that the motion model, started at $c_i$, ends in cell $k$; on a line with Gaussian noise it is a difference of two values of the normal distribution function;
- the likelihood of cell $k$ is $p(z_t \mid x_t = c_k)$, the density at the representative point.

The output is the posterior of the cells under this discrete model.

## The algorithm

```pseudo id=main
HISTOGRAM-FILTER(p, u_t, z_t)                 ▷ p_i = P(x_{t-1} in cell i)
L1  for k = 1 to g do
L2      p̄_k ← Σ_{i=1}^{g} P(k | u_t, i) p_i              ▷ prediction
L3  q_k ← p(z_t | x_t = c_k) p̄_k for k = 1, ..., g       ▷ correction
L4  η ← 1 / Σ_k q_k
L5  return the list with entries η q_k
```

The lines are those of the Bayes filter, with sums over cells. The work is in building the model on the cells. The code below handles a state on an interval $[a, b)$ cut into $g$ cells of width $h = (b - a)/g$, a motion $x_t = x_{t-1} + u_t + \varepsilon$ with $\varepsilon \sim N(0, \sigma^2)$, and any measurement density. The transition from cell $i$ to cell $k$ is $\Phi((r_k - c_i - u_t)/\sigma) - \Phi((l_k - c_i - u_t)/\sigma)$, where $l_k$ and $r_k$ are the edges of cell $k$ and $\Phi$ is the standard normal distribution function. The outer edges are $-\infty$ and $+\infty$: the mass that leaves the interval goes to the end cells, as if the robot stops at a wall. So each column of the transition matrix sums to one.

For a robot pose, the cells form a 3D grid over $x$, $y$ and $\theta$, and the transition comes from the [odometry motion model](/odometry-motion-model/) or the [velocity motion model](/velocity-motion-model/). Thrun et al. (Section 8.2) call this grid localization.

## Example

**A beacon on a line.** The state space is $[0, 10)$ m, cut into $g = 10$ cells of 1 m with centers $0.5, 1.5, \ldots, 9.5$. A beacon stands at $x = 5$. The sensor gives the distance to the beacon, but not the side: $z = |x - 5| + v$ with $v \sim N(0, 0.5^2)$. The likelihood of cell $k$ is $\exp(-\tfrac{1}{2}((z - |c_k - 5|)/0.5)^2)$; the constant factor cancels in L4. The prior is uniform. The robot is at $x = 3.2$.

Step 1 has no motion, and the sensor reads $z_1 = 2.0$. Cells 2, 3, 6 and 7 are at distance $1.5$ or $2.5$ from the beacon, so their likelihood is $e^{-1/2} = 0.6065$. Cells 1, 4, 5 and 8 get $e^{-9/2} = 0.0111$.

Step 2 moves the robot by $u_2 = 1$ m with $\sigma = 0.5$ m, to $x = 4.2$, and the sensor reads $z_2 = 0.8$. From the center of a cell, the move puts $0.6827$ of the mass in the cell one to the right, $0.1573$ in each of its two neighbors and $0.0013$ two cells further out on each side.

| cell | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $p_1$ | 0.0000 | 0.0045 | 0.2455 | 0.2455 | 0.0045 | 0.0045 | 0.2455 | 0.2455 | 0.0045 | 0.0000 |
| $\bar p_2$ | 0.0000 | 0.0010 | 0.0420 | 0.2069 | 0.2069 | 0.0431 | 0.0431 | 0.2069 | 0.2069 | 0.0431 |
| $p_2$ | 0.0000 | 0.0000 | 0.0004 | 0.2560 | 0.5697 | 0.1185 | 0.0533 | 0.0021 | 0.0000 | 0.0000 |

After step 1 the belief has two equal peaks, one on each side of the beacon. No Gaussian can hold this. The move shifts both peaks to the right. The left peak is now at about 1 m from the beacon, which fits $z_2 = 0.8$; the right peak is at about 3 m, which does not. After step 2, cells 0 to 4 hold $0.8261$ of the mass, cell 4 (which contains the true position 4.2) is the most likely cell, and the mean is $4.47$ m.

**Against the Kalman filter.** On a linear Gaussian model the exact posterior is known from the [Kalman filter](/kalman-filter/). The test of the code uses $[-20, 20)$, the prior $N(0, 2^2)$, six moves of $u = 1$ with $\sigma = 0.5$ and six measurements $z = x + N(0, 1)$ from a simulation with seed 7. The Kalman filter gives the mean $5.4167$ and the variance $0.3925$. The histogram filter, with the mass of each cell spread uniformly over the cell, gives:

| cells $g$ | width $h$ | mean | variance |
|---|---|---|---|
| 10 | 4 | 5.9779 | 1.4212 |
| 40 | 1 | 5.3532 | 0.5260 |
| 160 | 0.25 | 5.4125 | 0.4007 |
| 640 | 0.0625 | 5.4165 | 0.3930 |

These are measurements on one data set, not a bound. The error falls quickly with $h$ here because the posterior is smooth and much wider than a cell at $g = 640$.

## Correctness

The histogram filter is the Bayes filter of the discrete model whose states are the cells, whose transition is $P(k \mid u_t, i)$ and whose measurement probability is $p(z_t \mid c_k)$. Each column of the transition sums to one, so this is a valid model, and the proof of the Bayes filter applies line by line: the output is the exact posterior of the cells under the discrete model. The proof, with the condition that makes the end cells correct, is in [the correctness proof](proofs/correctness.md).

The output is not the posterior of the continuous model. The two differ because the motion from cell $i$ is computed from $c_i$ only, and because the likelihood is read at $c_k$ only. Both errors go to zero for smooth models as $h \to 0$, but the rate depends on the model, and a measurement model narrower than a cell can be badly wrong (see Pitfalls). Kramer and Sorenson (1988) analyze how such errors can grow over time.

## Complexity

Let $g$ be the number of cells. The costs are in the [real RAM](/real-ram/) model.

- **Prediction.** Line L2 costs $O(g)$ per cell, so $O(g^2)$ per step. If one motion step can reach only $b$ cells from any cell, the sum has $b$ nonzero terms, and the cost is $O(g b)$. For a pose grid with a short time step, $b$ is small.
- **Shift-invariant motion.** On a uniform grid, if the motion is the same everywhere (a shift plus noise that does not depend on the position), line L2 is a [convolution](/convolution/), and the [fast Fourier transform](/fast-fourier-transform/) computes it in $O(g \log g)$. Walls break the shift invariance near the edges.
- **Correction.** Lines L3 to L5 cost $O(g)$ plus $g$ evaluations of the measurement model. For a laser scan with many beams, these evaluations dominate.
- **Memory.** $O(g)$ for the belief. The transition matrix need not be stored; the code stores it only for the tests.
- **Dimension.** A grid with $s$ cells per axis in $d$ dimensions has $g = s^d$ cells. For a planar pose with 15 cm cells over a $30 \times 30$ m map and 5 degree steps in $\theta$, $g = 200 \cdot 200 \cdot 72 = 2\,880\,000$. This is why grids are used up to three dimensions and rarely above.

## Properties

- **Any shape.** The belief can have many peaks, long tails and flat parts. This is what [global localization](/global-localization/) needs.
- **Deterministic.** The same input gives the same output. A [particle filter](/particle-filter/) with the same number of cells gives a random answer.
- **Fixed resolution.** The cells do not move to where the probability is. Most cells hold almost no probability once the robot knows where it is, but they still cost time.
- **Mass is kept.** The prediction keeps the total probability at one, because the columns of the transition sum to one.
- **Exact on finite models.** When the state space is finite, as a set of doors, rooms or the places of a [topological map](/topological-map/), there is no discretization error, and the filter is the exact Bayes filter. In this case it is the [forward algorithm](/forward-algorithm/) with normalization at each step.

## Variants and improvements

- **Static and dynamic decomposition.** Thrun et al. (Section 4.1) describe grids with cells of different sizes, density trees and grids whose cells depend on the current belief. They save time, but the model on the cells must then be built for each layout.
- **Selective update.** Fox, Burgard and Thrun (1999) update only the cells whose probability is above a threshold. This is a heuristic: a cell below the threshold can hold the true pose.
- **Precomputed sensor model.** For a fixed map, the expected range of each beam from each cell can be computed once with [ray casting](/ray-casting/) and stored. This trades memory for time.
- **Point-mass filter.** Bucy and Senne (1971) put the mass on grid points instead of cells. The equations are the same with $P(k \mid u_t, i)$ taken as the density at $c_k$ times the cell volume.
- **Particle filter.** It puts its samples where the probability is, instead of on a fixed grid; for localization it is [Monte Carlo localization](/monte-carlo-localization/).

## When to use it

Use a histogram filter when the state has at most three dimensions, the belief can have several peaks, and a deterministic result matters, for example to localize a robot in a small map, to track a target on a road graph or to estimate a discrete mode. Use the [Kalman filter](/kalman-filter/) or the [EKF](/ekf-localization/) when the belief has one peak, and a particle filter when the space is large and most of it has almost no probability.

## Pitfalls

- **A sensor sharper than a cell.** If the measurement density is much narrower than a cell, the value at the center $c_k$ can be close to zero even when the cell contains states that fit the measurement well. The filter then removes the true cell. Thrun et al. (Section 8.2) discuss this effect for coarse grids. A common fix is to widen the sensor model to the cell size; this is a rule of thumb, and it makes the filter less certain than the model.
- **A motion smaller than a cell.** If the robot moves less than a cell per step and the transition is computed from the center only, the belief can stay in the same cell for ever, or jump by a whole cell. Spread the mass over the cells that the motion from the whole cell reaches, or keep the odometry between updates and apply it once it is larger than a cell.
- **Edges.** Decide what happens to mass that leaves the grid. The code puts it in the end cells, which models a wall. Dropping it and normalizing later makes the belief move away from the edge without evidence.
- **Underflow and zero cells.** A cell with probability zero never comes back. Add a small floor to the sensor model, or normalize in log space for many sharp measurements.
- **Angles.** On a pose grid, the $\theta$ axis wraps around: the cell before $-\pi$ is the cell before $\pi$. Treat it as a ring, not as an interval with walls.

## Implementations

## History

Bucy and Senne (1971) computed the Bayes recursion of a nonlinear filter on a grid of points, so that the accuracy is set by the program and not by a linearization. Kramer and Sorenson (1988) used densities that are constant on cells and studied the growth of the error. In robotics, Burgard, Fox, Hennig and Schmidt (1996) used position probability grids over the three pose coordinates for global localization, and Fox, Burgard and Thrun (1999) built Markov localization on such grids. Thrun, Burgard and Fox (2005) present the method as the histogram filter, and its use for robot pose as grid localization.

## References
