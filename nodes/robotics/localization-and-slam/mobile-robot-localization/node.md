---
tag: HWNH9Z
kind: problem
slug: mobile-robot-localization
name: Mobile robot localization
aliases:
- robot localization
- map-based localization
area: robotics/localization-and-slam
level: intro
summary: Estimate the pose of a robot in a known map from its motion commands and sensor readings, as a probability distribution that is updated at each step.
prereqs: [state-estimation, bayes-theorem]
see_also: [markov-localization, ekf-localization, monte-carlo-localization, global-localization, kidnapped-robot-problem, slam-problem, dead-reckoning, filtering]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 7, Section 7.1 (a taxonomy of localization problems: local and global, static and dynamic environments, passive and active, single robot and multi-robot) and Section 7.2 (Markov localization), and Chapter 8 (grid and Monte Carlo localization)"
  - paper: "Dieter Fox, Wolfram Burgard and Sebastian Thrun, Markov localization for mobile robots in dynamic environments, Journal of Artificial Intelligence Research 11, 1999, pages 391 to 427"
    locator: the probabilistic formulation of localization as a Bayes filter over poses, and its use in dynamic environments
  - paper: doi:10.1109/70.88147
    title: "John J. Leonard and Hugh F. Durrant-Whyte, Mobile robot localization by tracking geometric beacons, IEEE Transactions on Robotics and Automation 7(3), 1991, pages 376 to 382"
    locator: localization as the tracking of the pose with an extended Kalman filter and a map of beacons
  - paper: doi:10.1137/S0097539792233257
    title: "Leonidas J. Guibas, Rajeev Motwani and Prabhakar Raghavan, The robot localization problem, SIAM Journal on Computing 26(4), 1997, pages 1120 to 1138"
    locator: the geometric version of localization from one visibility polygon in a polygonal map
---

Mobile robot localization is the problem of finding where a robot is in a map that it already has. The robot knows its commands and its sensor readings, but its wheels slip and its sensors are noisy, so its pose, the position and heading $(x, y, \theta)$ in the plane, cannot be read off directly. The standard formulation is probabilistic: the robot keeps a belief, a probability distribution over its poses, and updates it with each command and each reading. This is the [Bayes filter](/bayes-filter/) with a known map. Almost every task of a mobile robot needs the pose, so localization is a part of nearly every robot that uses a map. The problem splits into cases of very different difficulty: tracking a known start pose, [global localization](/global-localization/) from no knowledge, and recovery from a [kidnapping](/kidnapped-robot-problem/).

## In plain words

You walk through a building with a floor plan in your hand. You count your steps and look around. If you started at the main door, you only need to keep track: a few steps, a turn, and the corridor you see matches the plan. If you woke up somewhere unknown, you must look for clues: a long corridor, a staircase, a window. Several places on the plan may fit at first, and you walk on until only one fits. A robot does the same. It never knows its place for certain, so it keeps a list of how likely each place is, and it updates the list after each move and each look.

## Definition

**Input.** A map $m$ of the environment: for example an [occupancy grid](/occupancy-grid-map/), a list of landmarks, or a [topological map](/topological-map/). A motion model $p(x_t \mid u_t, x_{t-1}, m)$, such as the [odometry motion model](/odometry-motion-model/) or the [velocity motion model](/velocity-motion-model/). A measurement model $p(z_t \mid x_t, m)$, such as the [beam model](/beam-range-finder-model/), the [likelihood field](/likelihood-field-model/) or the [landmark model](/landmark-measurement-model/). A prior belief $p(x_0)$. A stream of controls $u_1, u_2, \dots$ and readings $z_1, z_2, \dots$.

**Output.** At each time $t$, the belief

$$\mathrm{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t}, m),$$

or a point estimate of $x_t$ taken from it.

**Assumption.** The state $x_t$ is complete: given $x_{t-1}$ and $u_t$, the pose $x_t$ does not depend on older data, and given $x_t$, the reading $z_t$ does not depend on anything else. Under this Markov assumption the belief obeys the recursion

$$\mathrm{bel}(x_t) = \eta\, p(z_t \mid x_t, m) \int p(x_t \mid u_t, x_{t-1}, m)\, \mathrm{bel}(x_{t-1})\, dx_{t-1}.$$

People who move, doors that open and wrong models break the assumption. Methods treat these effects as noise or filter them out.

**How it differs from SLAM.** Here the map is given. In the [SLAM problem](/slam-problem/), the robot must build the map while it localizes.

## Variants

Thrun et al. (Section 7.1) sort localization problems along four axes.

| axis | the easier case | the harder case |
|---|---|---|
| initial knowledge | **position tracking**: the start pose is known, and the error stays small | **global localization**: the start pose is unknown; the **kidnapped robot problem**: the robot can be moved without being told |
| environment | **static**: only the robot moves | **dynamic**: people, doors and furniture change the readings |
| control of the robot | **passive**: the robot moves for other reasons, and localization only watches | **active**: the robot chooses its moves to reduce its uncertainty |
| number of robots | **single robot** | **multi-robot**: robots that see one another can share information |

Other variants change the map or the data: landmarks with unknown identities need [data association](/data-association-slam/); a map without coordinates gives topological localization; and the geometric problem of Guibas, Motwani and Raghavan asks for all points of a polygon whose visibility polygon matches a given one, with no noise and no motion.

## Examples

- **Tracking in a corridor.** A robot starts at a known door and drives along a corridor. Odometry alone drifts, and the error grows with the distance. Each doorway that the laser sees corrects the position along the corridor, and the walls correct the position across it. A Gaussian belief is enough.
- **Waking up in an office.** The robot is switched on at an unknown place. Many offices look alike, so the belief has many peaks. Only after the robot drives through a distinctive area, such as a corridor junction, does one peak remain.
- **A symmetric hall.** In a rectangular hall with no features, the poses $(x, y, \theta)$ and the pose rotated by $180°$ about the center give the same readings. No method can tell them apart; the belief keeps two peaks forever.
- **A museum with visitors.** People surround the robot and block its laser. A method that does not filter readings caused by people can lose its pose. Fox, Burgard and Thrun (1999) used filters for such readings in the Bayes filter.

## Known algorithms

| method | belief | global localization | cost per step |
|---|---|---|---|
| [EKF localization](/ekf-localization/) | one Gaussian | no | $O(1)$ per reading with known landmarks |
| multi-hypothesis tracking | a mixture of Gaussians | with a few hypotheses | grows with the number of hypotheses |
| [Markov localization](/markov-localization/) on a grid, the [histogram filter](/histogram-filter/) | a histogram over poses | yes | grows with the number of grid cells |
| [Monte Carlo localization](/monte-carlo-localization/) | particles | yes | $O(N)$ evaluations of the models |
| [KLD-sampling](/kld-sampling/) | particles, adaptive number | yes | adapts to the spread of the belief |
| [correlative scan matching](/correlative-scan-matching/) | the best pose in a window, with a covariance | within the window | grows with the window |

The methods differ in how they represent the belief, and so in what they can do. A Gaussian is cheap but has one peak. A grid or a particle set can hold many peaks, at a cost that grows with the size of the space. Thrun et al. (Chapters 7 and 8) compare them.

## Bounds

- **The exact belief (a theorem).** For a finite set of $g$ poses, one step of the Bayes filter costs $O(g^2)$ in general and $O(g b)$ when each control reaches at most $b$ poses. For continuous poses the integral has no closed form except in special cases, such as linear Gaussian models, where the [Kalman filter](/kalman-filter/) is exact. All practical methods approximate.
- **Indistinguishable poses (a theorem).** If two poses give the same distribution of readings for every sequence of moves, as in a symmetric hall, then the belief gives them equal weight for every equal prior, so no method can tell them apart. This bound is about information, not computation.
- **The geometric version (a theorem).** Guibas, Motwani and Raghavan (1997) find all points of a simple polygon with $n$ vertices whose visibility polygon, with $m$ vertices, matches a given one, in $O(m n)$ time for a single query without preprocessing.
- **Active localization (a theorem).** Choosing a route of least length that is sure to localize the robot is NP-hard (Dudek, Romanik and Whitesides, 1998); see [global localization](/global-localization/).

## Reductions

- **To filtering.** Localization with a finite set of poses is filtering in a [hidden Markov model](/hidden-markov-model/): the poses are the hidden states, the motion model is the transition matrix and the measurement model gives the emissions. The [forward algorithm](/forward-algorithm/) is Markov localization.
- **From SLAM.** If the map is known, the [SLAM problem](/slam-problem/) becomes localization. In a [Rao-Blackwellized particle filter](/rao-blackwellized-particle-filter/) for SLAM, each particle samples the path of the robot as Monte Carlo localization does, and builds its own map from that path.
- **Global localization and kidnapping.** Tracking is localization with a narrow prior. Global localization is localization with a uniform prior. The kidnapped robot problem is global localization at an unknown time, during tracking.

## Applications

Localization is a part of every mobile robot that uses a map: delivery robots in hospitals and warehouses, museum guides, cleaning robots, and self-driving cars, which localize against a prior map of the road. Its output feeds path planning, obstacle avoidance and the mapping of new areas. Methods from localization, such as particle filters and scan matching, are also the building blocks of SLAM.

## References
