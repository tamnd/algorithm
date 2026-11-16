---
tag: PR79D6
kind: problem
slug: global-localization
name: Global localization
aliases:
- localization without initial pose
area: robotics/localization-and-slam
level: core
summary: Localization from an unknown initial pose, where the belief must start spread over the whole map and may keep several peaks until the data rule them out.
prereqs: [mobile-robot-localization]
see_also: [markov-localization, monte-carlo-localization, histogram-filter, kidnapped-robot-problem, topological-map, visibility-polygon, moore-machine, pomdp]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 7, Section 7.1 (local and global localization) and Section 7.2 (Markov localization), and Chapter 8, Section 8.2 (grid localization) and Section 8.3 (Monte Carlo localization)"
  - paper: "Dieter Fox, Wolfram Burgard and Sebastian Thrun, Markov localization for mobile robots in dynamic environments, Journal of Artificial Intelligence Research 11, 1999, pages 391 to 427"
    locator: global localization with a grid over all poses, starting from a uniform belief
  - paper: doi:10.1137/S0097539792233257
    title: "Leonidas J. Guibas, Rajeev Motwani and Prabhakar Raghavan, The robot localization problem, SIAM Journal on Computing 26(4), 1997, pages 1120 to 1138"
    locator: "the geometric problem: all points of a polygon whose visibility polygon matches the one that the robot sees, in O(mn) time per query without preprocessing"
  - paper: "Gregory Dudek, Kathleen Romanik and Sue Whitesides, Localizing a robot with minimum travel, SIAM Journal on Computing 27(2), 1998, pages 583 to 604"
    locator: the problem of the shortest route that localizes the robot, and its NP-hardness
---

Global localization is [mobile robot localization](/mobile-robot-localization/) when the robot does not know where it starts. The robot has a map, a motion model and a measurement model, but its prior belief over poses is uniform over the free space of the map. It must find its pose from its own motion and readings. This is harder than position tracking in two ways. First, the belief can have many peaks, one for each place that looks like the place where the robot is, so a single Gaussian cannot hold it. Second, the robot may never be sure: in a symmetric map some poses give the same readings forever. The standard methods are [Markov localization](/markov-localization/) on a grid and [Monte Carlo localization](/monte-carlo-localization/). A geometric version, with exact sensing and no motion, was solved by Guibas, Motwani and Raghavan (1997).

## In plain words

Someone leads you blindfolded into a large office and takes off the blindfold. You have a floor plan but you do not know where you are. At first every spot on the plan is possible. You look around and see a door on your left: now only the spots next to a door on the left are possible. You walk a few steps and see a window: fewer spots remain. You keep a list of all the places that still fit, and you walk until only one is left. In some buildings two places look exactly the same, and then you may never know which one you are in.

## Definition

**Input.** A map $m$, a motion model $p(x_t \mid u_t, x_{t-1}, m)$, a measurement model $p(z_t \mid x_t, m)$, and a stream of controls and readings, as in [mobile robot localization](/mobile-robot-localization/). The prior is uniform:

$$\mathrm{bel}(x_0) = \frac{1}{|X_{\text{free}}|} \quad \text{for every pose } x_0 \text{ in the free space } X_{\text{free}}.$$

**Output.** The belief $\mathrm{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t}, m)$ at each time $t$. The problem is solved at time $t$ when the belief is concentrated near the true pose, for example when one region of small size holds most of the probability.

**What makes it global.** The prior holds no information. A method that starts from a single guess, such as [EKF localization](/ekf-localization/), does not solve this problem, because its Gaussian cannot hold the many peaks of the early belief.

**The geometric version.** Guibas, Motwani and Raghavan (1997) state the problem without noise. The map is a simple polygon $P$ with $n$ vertices. The robot knows its heading and sees its [visibility polygon](/visibility-polygon/) $V$ with $m$ vertices. Output all points $p$ in $P$ whose visibility polygon is a translate of $V$.

## Variants

| variant | what changes |
|---|---|
| passive global localization | the robot moves for other reasons; the method only updates the belief |
| active global localization | the robot chooses its moves to make the belief concentrate fast or with little travel |
| geometric, one view | exact sensing, no motion; find all poses that match one view |
| geometric, minimum travel | exact sensing; find a route of least length that is sure to localize the robot |
| topological | the map is a [topological map](/topological-map/), and the belief is a set of places or a probability for each place |
| [kidnapped robot problem](/kidnapped-robot-problem/) | global localization that may start at an unknown time, after a confident belief became wrong |

## Examples

**A corridor with three doors.** A ring corridor has 10 cells, with doors at the cells 2, 3 and 7. The sensor reports "door" with probability 0.8 at a door and 0.1 at a wall. Motion is exact. The robot starts with the belief 0.1 in every cell.

| step | belief at cells 2, 3, 7 | belief at cells 4, 8 | other cells |
|---|---|---|---|
| start | 0.1 each | 0.1 each | 0.1 each |
| sense "door" | 0.258 each | 0.032 each | 0.032 each |
| move one cell, sense "door" | cell 3: 0.634; cells 2, 7: 0.079 | 0.079 each | 0.010 each |

After the first reading the belief has three equal peaks, one at each door. After the move only the cell 3 has a door both before and after the move, so its peak grows. The values come from the Bayes rule; this is a measurement of the calculation, not a claim about real sensors. A Gaussian belief could not hold the three peaks of the second row.

**A symmetric room.** In an empty rectangular room, the pose $(x, y, \theta)$ and the pose turned by $180°$ about the center give the same readings for every motion. The belief keeps two peaks forever. Only a change in the map, such as a sign on one wall, can break the tie.

**A building with equal offices.** A row of equal offices along a corridor gives a peak in each office. The robot must leave the office and pass a place that is different, such as the end of the corridor, before one peak wins. A passive robot that stays in the office never localizes; an active robot drives out on purpose.

## Known algorithms

| method | how it holds the belief | notes |
|---|---|---|
| [Markov localization](/markov-localization/) on a grid, the [histogram filter](/histogram-filter/) | a probability for each cell of a grid over $(x, y, \theta)$ | exact up to the grid; the cost grows with the number of cells (Fox, Burgard and Thrun, 1999) |
| [Monte Carlo localization](/monte-carlo-localization/) | particles spread over the free space at the start | the particles gather at the peaks; few particles can lose the true peak |
| [KLD-sampling](/kld-sampling/) | particles, with a number that adapts to the spread | many particles at the start, few once the belief has one peak |
| multiple hypothesis tracking | a list of Gaussians, one for each candidate | Thrun et al. Section 7.6; needs a way to create the candidates |
| localization in a [topological map](/topological-map/) | a set of places | exact with exact sensing; the set never grows |
| the method of Guibas, Motwani and Raghavan | all matching points of a polygon | geometric version; exact sensing, one view |

Active methods choose the next move by an estimate of how much it will reduce the uncertainty, for example the expected [entropy](/shannon-entropy/) of the next belief. This is a heuristic. The exact problem of choosing moves under uncertainty is a [POMDP](/pomdp/).

## Bounds

- **Indistinguishable poses (a theorem).** If two poses give the same distribution of readings for every sequence of moves, then from a uniform prior the belief gives them equal weight at every time. No method can tell them apart, however long it runs.
- **One view (a theorem).** Guibas, Motwani and Raghavan (1997) find all points of a simple polygon with $n$ vertices that match a visibility polygon with $m$ vertices in $O(m n)$ time per query without preprocessing. They also give methods with preprocessing for faster queries.
- **Minimum travel (a theorem).** Dudek, Romanik and Whitesides (1998) show that finding a route of least length that localizes the robot in a polygon, with exact sensing, is [NP-hard](/np-hard/).
- **The cost of a grid (a theorem).** A grid with $g$ cells costs $\Theta(g)$ per measurement update. For a building of $100 \times 100$ m with cells of $0.1$ m and $5°$, $g = 1000 \cdot 1000 \cdot 72 = 7.2 \times 10^7$, which is why sampling methods are used for large maps.

## Reductions

- **To filtering with a uniform prior.** Global localization is the Bayes filter with a uniform prior. On a finite set of poses it is filtering in a hidden Markov model, and Markov localization solves it exactly.
- **To state identification in automata.** With exact sensing and exact actions on a finite map where every action is possible at every place, the map is a [Moore machine](/moore-machine/): the places are the states, the actions are the inputs and the signatures are the outputs. A sequence of actions that localizes the robot from every start place is a homing sequence of this machine.
- **To the kidnapped robot problem.** A method that solves the [kidnapped robot problem](/kidnapped-robot-problem/) must solve global localization each time a kidnapping happens.

## Applications

Global localization is needed when a robot is switched on at an unknown place, after a reset of its software, and after it has lost its pose. Service robots in offices and hospitals, warehouse robots and museum guides use it at start up. Self-driving cars usually avoid the hard case, because satellite positioning gives a coarse prior and only a local search remains.

## References
