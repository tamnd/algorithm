---
tag: 0D5R7R
kind: model
slug: inverse-sensor-model
name: Inverse sensor model
aliases:
- inverse measurement model
area: robotics/localization-and-slam
level: core
summary: "The probability that a map cell is occupied given one sensor reading and the pose, used by occupancy grid mapping."
history:
  year: 1985
  people: [Hans Moravec, Alberto Elfes]
  note: Moravec and Elfes turned each wide angle sonar reading into evidence that the cells inside its cone are empty and that the cells near its measured range are occupied, and combined this evidence in a grid of cells.
prereqs: [bayes-filter, occupancy-grid-map]
see_also: [occupancy-grid-mapping, occupancy-grid-map, octree-occupancy-map, beam-range-finder-model, bayes-theorem, logistic-regression, grid-based-rbpf-slam, frontier-based-exploration]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 9, Section 9.2 (the inverse range sensor model of Table 9.2 and its use in Table 9.1), Section 9.3 (learning inverse measurement models from forward models) and Section 9.4 (maximum a posteriori mapping with forward models)"
  - paper: doi:10.1109/ROBOT.1985.1087316
    title: "Hans P. Moravec and Alberto Elfes, High resolution maps from wide angle sonar, Proceedings of the 1985 IEEE International Conference on Robotics and Automation, volume 2, pages 116 to 121"
    locator: the grid of cells with probabilities of empty and occupied space, built from many sonar cones
  - paper: doi:10.1109/2.30720
    title: "Alberto Elfes, Using occupancy grids for mobile robot perception and navigation, Computer 22(6), 1989, pages 46 to 57"
    locator: the sensor model and the Bayesian update of the cell states of an occupancy grid
---

An inverse sensor model gives, for one cell of a map, the probability that the cell is occupied, given one sensor reading and the pose of the robot. It runs in the opposite direction of the usual measurement model. A forward model such as the [beam range finder model](/beam-range-finder-model/) says which readings to expect from a known world; the inverse model says what one reading tells about the world. For a range sensor the rule is simple: cells that the beam passed through are probably free, cells near the end of the beam are probably occupied, and the reading tells nothing about the other cells. [Occupancy grid mapping](/occupancy-grid-mapping/) adds the log odds of this probability to each cell of an [occupancy grid map](/occupancy-grid-map/). The model treats each cell on its own, which is an approximation. The notation is the one of Thrun, Burgard and Fox (2005).

## The machine

**State.** The pose $x_t = (x, y, \theta)$ of the robot, known, and a map of cells $m_1, \ldots, m_g$, each occupied ($m_i = 1$) or free ($m_i = 0$). Cell $i$ has its center at $(x_i, y_i)$.

**Measurement.** A scan $z_t$ of $K$ beams; beam $k$ has a bearing $\theta_k$ in the robot frame and a reading $z_t^k \le z_{\max}$.

**Output.** For each cell, $p(m_i = 1 \mid z_t, x_t)$, usually in log odds $\operatorname{logit} p = \log(p / (1 - p))$. The prior is $p(m_i = 1)$ with log odds $l_0$.

**The range sensor rule.** Thrun, Burgard and Fox (2005) give this inverse model for range finders. For cell $i$, let $r$ be its distance from the robot, $\phi = \operatorname{atan2}(y_i - y, x_i - x) - \theta$ its bearing, and $k$ the beam whose bearing $\theta_k$ is closest to $\phi$. Then the log odds is

- $l_0$ if $r > \min(z_{\max},\ z_t^k + \alpha/2)$ or $|\phi - \theta_k| > \beta/2$: the cell lies beyond the reading or outside every beam;
- $l_{\mathrm{occ}}$ if $z_t^k < z_{\max}$ and $|r - z_t^k| < \alpha/2$: the cell is at the end of a beam that hit something;
- $l_{\mathrm{free}}$ if $r \le z_t^k$: the beam passed through the cell.

The three tests are applied in this order. A reading at $z_{\max}$ marks no cell as occupied, because a max range reading means that the beam hit nothing.

**Parameters.** $\alpha$ is the assumed thickness of obstacles in meters, $\beta$ the width of a beam in radians, and $l_{\mathrm{occ}}$ and $l_{\mathrm{free}}$ the log odds for a hit and a pass. A common choice is the log odds of 0.7 and 0.4, $l_{\mathrm{occ}} = \log(0.7/0.3) \approx 0.84730$ and $l_{\mathrm{free}} = \log(0.4/0.6) \approx -0.40547$. These values are rules of thumb, not derived from the sensor. OctoMap uses the rounded values 0.85 and -0.4 in log odds (see [octree occupancy map](/octree-occupancy-map/)).

**Standing assumptions.** The pose is known. Each cell is judged on its own, given the reading, as if the cells were independent; this is an approximation. Readings at different times are independent given the map.

**Example.** The robot is at $(0, 0, 0)$, one beam has bearing 0 and reading $z = 2$ m, $\alpha = 0.2$ m, $z_{\max} = 6$ m, and the prior is 0.5, so $l_0 = 0$. Cells with centers on the beam get:

| distance $r$ of the cell (m) | 1.00 | 1.95 | 2.05 | 2.15 |
|---|---|---|---|---|
| log odds | $l_{\mathrm{free}}$ | $l_{\mathrm{occ}}$ | $l_{\mathrm{occ}}$ | $l_0$ |

The cell at $2.15$ lies beyond $z + \alpha/2 = 2.1$, so the reading says nothing about it. For a max range reading $z = 6$, a cell at $5.95$ gets $l_{\mathrm{free}}$ and a cell at $6.05$ gets $l_0$. A cell at bearing 0.5 rad with $\beta = 0.1$ is outside the beam and gets $l_0$.

## What it counts

The model assigns to each cell its occupancy probability given one scan. With the rule above, one cell costs $O(1)$ arithmetic plus the search for the nearest beam, which is $O(1)$ when the bearings are evenly spaced and $O(\log K)$ by binary search otherwise. Occupancy grid mapping evaluates it for the cells within $z_{\max}$ of the robot, so one scan costs $O(g)$ evaluations on a grid of $g$ cells in the worst case. Walking each beam through the grid with a line traversal instead visits $O(K (1 + z_{\max}/s))$ cells for a cell side $s$.

## Relation to other models

- **Forward models.** The [beam range finder model](/beam-range-finder-model/) gives $p(z_t \mid x_t, m)$ for a whole map. By [Bayes' theorem](/bayes-theorem/), $p(m_i \mid z_t, x_t) = \sum_{m: m_i} p(z_t \mid x_t, m)\, p(m) / p(z_t \mid x_t)$, a sum over all maps with the given value of $m_i$. So the inverse model of one cell is a marginal over all other cells, which no one computes exactly; the range sensor rule is a hand-made stand-in for it.
- **[Occupancy grid mapping](/occupancy-grid-mapping/).** The algorithm that uses this model, one binary [Bayes filter](/bayes-filter/) per cell. Its page has an implementation of the range sensor rule with tests.
- **[Octree occupancy map](/octree-occupancy-map/).** Uses the same model in 3D, with the beam walked through voxels and with clamping of the log odds.
- **Classifiers.** An inverse model is a classifier that predicts the label of a cell from the readings, so any probabilistic classifier, such as [logistic regression](/logistic-regression/), can serve as one if it is trained on labeled data.

## Known results in the model

- **Theorem (the log odds update).** Assume that $z_t$ is independent of $z_{1:t-1}$ given $m_i$ and the poses. Then $l_{t,i} = l_{t-1,i} + \operatorname{logit} p(m_i = 1 \mid z_t, x_t) - l_0$, where $l_{t,i}$ is the log odds of $p(m_i = 1 \mid z_{1:t}, x_{1:t})$. Proof: by Bayes' theorem and the assumption, $p(m_i \mid z_{1:t}) = p(z_t \mid m_i)\, p(m_i \mid z_{1:t-1}) / p(z_t \mid z_{1:t-1})$, and again by Bayes' theorem $p(z_t \mid m_i) = p(m_i \mid z_t)\, p(z_t) / p(m_i)$. Divide the expression for $m_i = 1$ by the one for $m_i = 0$: the terms $p(z_t)$ and $p(z_t \mid z_{1:t-1})$ cancel, and the log of the ratio is the sum above. The assumption is an approximation, since $z_t$ also depends on the other cells.
- **Theorem (the order of readings does not matter).** Without clamping, the log odds after $T$ readings is $l_0 + \sum_t (\operatorname{logit} p(m_i \mid z_t, x_t) - l_0)$, a sum, so it does not depend on the order of the readings. With the values 0.7 and 0.4, one hit outweighs one pass by $0.84730 / 0.40547 \approx 2.09$, so a cell seen as occupied once and as free twice ends at log odds $0.0364$, probability about $0.509$.
- **Approximation (cells judged one by one).** A wide beam, such as a sonar cone, says that some cell on the arc at range $z$ is occupied, not that every cell is. The inverse model gives each cell on the arc $l_{\mathrm{occ}}$, and readings from other places that pass through those cells push them back to free. With many conflicting readings the resulting map depends on the parameters more than on the data. Thrun, Burgard and Fox (2005) treat this in Section 9.4 by searching for the map of maximum posterior probability under the forward model, which keeps the dependence between cells.
- **Learning inverse models.** Section 9.3 of the same book learns an inverse model from a forward model: draw maps from a prior, simulate readings with the forward model, and train a function approximator to predict the occupancy of a cell from the readings near it. This replaces the hand-made rule with a fitted one, at the cost of a training set and a choice of features.
- **Heuristic (the parameters).** $\alpha$, $\beta$, $l_{\mathrm{occ}}$ and $l_{\mathrm{free}}$ are set by hand or tuned on maps with known ground truth. Larger $l_{\mathrm{occ}}$ makes the map react faster to new obstacles and also to noise; clamping the log odds, as OctoMap does, keeps the map able to change after many agreeing readings.

## References
