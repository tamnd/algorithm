---
tag: 599C1C
kind: algorithm
slug: markov-localization
name: Markov localization
aliases:
- Fox-Burgard-Thrun Markov localization
area: robotics/localization-and-slam
level: core
summary: Localization by a Bayes filter over all poses of the robot in a known map, under the Markov assumption. It can start with no knowledge of the pose.
solves: [mobile-robot-localization]
model: real-ram
complexity:
  vars: {g: the number of poses, b: the number of poses that one control can reach from a pose, D: the cost of one evaluation of the measurement model, T: the number of time steps}
  time: {per_step: O(g b + g D), worst: O(T g^2)}
  space: {extra: O(g)}
properties: {deterministic: true, exact: true, online: true, recursive: true}
history:
  year: 1999
  people: [Dieter Fox, Wolfram Burgard, Sebastian Thrun]
  note: Fox, Burgard and Thrun gave Markov localization on fine grids of poses, with filters that remove readings caused by people in the environment.
prereqs: [mobile-robot-localization, bayes-filter]
see_also: [histogram-filter, ekf-localization, monte-carlo-localization, global-localization, hidden-markov-model, forward-algorithm, beam-range-finder-model, pomdp]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 7, Sections 7.1 to 7.3 (the taxonomy of localization problems, the Markov localization algorithm and its illustration), and Chapter 8, Section 8.2 (grid localization)"
  - paper: "Dieter Fox, Wolfram Burgard and Sebastian Thrun, Markov localization for mobile robots in dynamic environments, Journal of Artificial Intelligence Research 11, 1999, pages 391 to 427"
    locator: the Bayes filter over a grid of poses, the selective update, and the entropy and distance filters for readings caused by people
  - paper: "Wolfram Burgard, Dieter Fox, Daniel Hennig and Timo Schmidt, Estimating the absolute position of a mobile robot using position probability grids, Proceedings of the Thirteenth National Conference on Artificial Intelligence (AAAI-96), 1996"
    locator: global localization with a grid over x, y and theta (general locator)
---

Markov localization estimates the pose of a robot in a known map by running the [Bayes filter](/bayes-filter/) over all poses. The state is the pose $x_t$, the map $m$ is fixed, and the belief $\mathrm{bel}(x_t)$ is a distribution over every pose the robot could have. Because the belief can have any shape, Markov localization handles [global localization](/global-localization/), where the robot starts with no idea of its pose, as well as tracking. The name comes from the Markov assumption that makes the filter exact: the current pose and the map explain each new reading. This page gives the algorithm on a finite set of poses, where it is exact, and shows a robot in a small maze that keeps four hypotheses until one turn decides between them.

## In plain words

The robot has a map but does not know where on it it is. It gives every place and every direction a score, and all scores add up to one. At the start all scores are equal. When the robot drives, each score moves to the places the robot could reach. When the robot measures, for example the distance to the wall in front of it, places where the map predicts that distance keep their score, and the others lose most of it. In a building with many similar corridors, several places keep a high score for a while. A later measurement that only one of them can explain removes the others.

## The problem

The input is a map $m$, a set of poses $X$ (cells of a grid over $(x, y, \theta)$, or the places of a [topological map](/topological-map/)), a motion model $p(x_t \mid u_t, x_{t-1}, m)$, a measurement model $p(z_t \mid x_t, m)$ and an initial belief. At each time $t$ the robot receives a control $u_t$ and a reading $z_t$. The output is the posterior

$$\mathrm{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t}, m)$$

for every $x_t \in X$. This is [mobile robot localization](/mobile-robot-localization/) with a belief that can have many peaks. For tracking, the initial belief is concentrated near a known pose; for global localization, it is uniform over the free space.

The map in the motion model expresses that the robot cannot drive through walls. Thrun et al. (Section 7.2) write both models with $m$, and the algorithm is the Bayes filter with $m$ as a fixed extra argument.

## The algorithm

```pseudo id=main
MARKOV-LOCALIZATION(bel, u_t, z_t, m)          ▷ bel(x) = bel(x_{t-1})
L1  bel_bar(x) ← 0 for all poses x
L2  for each pose x_{t-1} with bel(x_{t-1}) > 0 do
L3      for each pose x_t with p(x_t | u_t, x_{t-1}, m) > 0 do
L4          bel_bar(x_t) ← bel_bar(x_t) + p(x_t | u_t, x_{t-1}, m) bel(x_{t-1})
L5  bel'(x) ← p(z_t | x, m) bel_bar(x) for all poses x
L6  η ← 1 / Σ_x bel'(x)
L7  return η bel'
```

Lines L1 to L4 compute the prediction $\overline{\mathrm{bel}}(x_t) = \sum_{x_{t-1}} p(x_t \mid u_t, x_{t-1}, m)\, \mathrm{bel}(x_{t-1})$. They loop over the source pose and push its probability to the poses it can reach, instead of looping over the target pose. The result is the same sum, but each pose has only a few successors, so the loop skips the zero terms. Lines L5 to L7 are the correction by Bayes' rule.

The code uses a grid map with four headings. A control is "F" (move one cell ahead), "L" or "R" (turn by 90 degrees). "F" succeeds with probability $p_{move}$, and the robot stays where it is otherwise or when a wall is ahead. The sensor measures the number $d$ of free cells ahead of the robot. The reading $z \in \{0, \ldots, z_{max}\}$ has probability $(1 - w_{rand}) K(z \mid d) + w_{rand} / (z_{max} + 1)$, where $K$ puts $3/5$ on $d$ and $1/5$ on each of $d - 1$ and $d + 1$. This is a small version of the [beam range finder model](/beam-range-finder-model/): a narrow peak at the expected range, plus a uniform term for random readings. The weights are chosen by hand here; on a real robot they are fitted to data.

## Example

The map has 14 free cells, so there are $14 \cdot 4 = 56$ poses. Rows and columns start at 0 in the top left corner, and the headings are N, E, S, W.

```
########
#......#
#.#.##.#
#...#..#
########
```

The parameters are $p_{move} = 4/5$, $z_{max} = 6$ and $w_{rand} = 1/10$. The robot starts at row 3, column 1, facing east, and does not know it. The prior is uniform. In this run, every move succeeds and every reading is the true range. The table gives, after each step, the number of poses with a belief above $0.05$ and the largest belief. The belief is computed in exact fractions.

| step | control | true pose | reading | poses above 0.05 | largest belief |
|---|---|---|---|---|---|
| 1 | none | (3, 1, E) | 2 | 10 | 0.0636 |
| 2 | F | (3, 2, E) | 1 | 10 | 0.0778 |
| 3 | F | (3, 3, E) | 0 | 10 | 0.0876 |
| 4 | L | (3, 3, N) | 2 | 4 | 0.2249 |
| 5 | F | (2, 3, N) | 1 | 4 | 0.2138 |
| 6 | F | (1, 3, N) | 0 | 4 | 0.2158 |
| 7 | R | (1, 3, E) | 3 | 1 | 0.9075 |

After step 1, ten poses see two free cells ahead and share most of the probability. Three steps later, four hypotheses remain: (1, 1, S), (1, 3, W), (3, 1, E) and (3, 3, N). For each of them, the robot saw ranges 2, 1, 0, then turned left and saw 2. They move in step and keep almost the same weight; after step 6, the true pose is in fact not the most likely one (0.2129 against 0.2158). The right turn at step 7 decides: only the true pose sees three free cells ahead. A filter with one Gaussian would have had to commit to one hypothesis at step 4 and would be wrong with probability about 3/4.

The test of the code checks this run, and checks the belief against a brute force sum over all paths of poses that the motion model allows.

## Correctness

Markov localization is the Bayes filter with the map as a fixed argument, so the proof of the Bayes filter applies: under the Markov assumption, the output is exactly $p(x_t \mid z_{1:t}, u_{1:t}, m)$ on a finite set of poses. Lines L1 to L4 compute the same sum as line L2 of the Bayes filter, term by term in another order. The full proof is in [the correctness proof](proofs/correctness.md).

On a grid over continuous poses, the result is exact for the model on the grid cells, and an approximation of the continuous posterior; see the [histogram filter](/histogram-filter/).

## Complexity

Let $g$ be the number of poses and $b$ the largest number of poses that one control can reach from a pose. The costs are in the [real RAM](/real-ram/) model.

- **Prediction.** Lines L2 to L4 cost $O(g b)$. In the code $b \le 2$. A pose grid with a fine resolution and a long time step has a large $b$; in the worst case the prediction costs $O(g^2)$.
- **Correction.** Line L5 evaluates the measurement model once per pose. If one evaluation costs $D$, for example a ray cast through the map, the correction costs $O(g D)$. The expected ranges depend only on the pose and the map, so they can be computed once and stored, which makes $D$ the number of beams.
- **Memory.** $O(g)$ for the belief, plus $O(g)$ times the number of beams if the expected ranges are stored.

The number of poses is the problem. A $40 \times 40$ m building at 10 cm and 2 degree resolution has $400 \cdot 400 \cdot 180 = 28.8$ million poses. Fox, Burgard and Thrun (1999) update only the poses whose belief is above a threshold; this selective update is a heuristic.

## Properties

- **Exact on a finite set of poses.** With exact arithmetic the output equals the posterior; the test uses fractions.
- **Global.** A uniform prior gives global localization with no special case.
- **Multimodal.** The belief keeps all hypotheses that fit the data, with the right weights, as in the example.
- **Symmetry is not resolved.** If the map looks the same from two poses for every reading, for example in a room with a rotation symmetry, their beliefs stay equal for ever. This is a property of the data, and no filter can do better.
- **Deterministic.** The same input gives the same belief, unlike [Monte Carlo localization](/monte-carlo-localization/).

## Variants and improvements

- **Grid Markov localization.** The poses are cells of a 3D grid; this is the [histogram filter](/histogram-filter/) applied to pose estimation (Thrun et al., Section 8.2).
- **Topological Markov localization.** The poses are places of a topological map, or places with a few headings. This is how the method started (Simmons and Koenig 1995, Nourbakhsh, Powers and Birchfield 1995), and the state space is small.
- **EKF localization.** A Gaussian belief instead of a table; it is much cheaper but cannot localize globally. See [EKF localization](/ekf-localization/).
- **Monte Carlo localization.** Samples instead of a grid; see [Monte Carlo localization](/monte-carlo-localization/).
- **Dynamic environments.** Fox, Burgard and Thrun (1999) add filters that drop readings that are shorter than expected and that people probably caused. The filtered readings break the strict Markov assumption less, but the filter itself is a heuristic.
- **Active localization.** The robot chooses controls that reduce the expected entropy of the belief. This is a [POMDP](/pomdp/) problem in general. Fox, Burgard and Thrun also studied an active version that picks the next action by a greedy one-step rule, which is a heuristic.

## When to use it

Use Markov localization when the robot may not know its pose, the set of poses is small enough to hold in memory (a topological map, or a 2D map with a coarse grid), and a deterministic answer is useful. For a large map at fine resolution, use Monte Carlo localization; for tracking with a good initial pose and identified landmarks, use EKF localization.

## Pitfalls

- **Readings that are not independent.** The filter assumes that the readings of the beams of one scan are independent given the pose. They are not: one person in front of the robot shortens many beams at once. The filter then becomes too sure, too fast, and can remove the true pose. Using a subset of beams, or a sensor model with a wider peak, is a common rule of thumb.
- **A map that is wrong.** Doors that are open in the map and closed in reality, or furniture that moved, give readings that the model says are almost impossible. Keep the random term $w_{rand}$ above zero, so that the true pose never gets probability zero.
- **Probability zero.** If the motion model forbids a move that happened (for example, the robot was pushed), the true pose can get probability zero and never come back. This is the [kidnapped robot problem](/kidnapped-robot-problem/). Add a small probability of a random jump, which is a heuristic.
- **Heading resolution.** With coarse heading cells, a long range reading moves far from where the model expects when the heading is a little wrong. The sensor model must be wide enough for the cell size.
- **Cost of the sensor model.** A ray cast per beam per pose per step is too slow for large grids. Precompute the expected ranges, or use the [likelihood field model](/likelihood-field-model/), which needs no ray cast.

## Implementations

## History

Markov localization grew out of work in the mid 1990s that applied hidden Markov models and POMDPs to robot navigation on topological maps: Simmons and Koenig (1995) and Nourbakhsh, Powers and Birchfield (1995) kept a probability for each place of a graph of the office. Burgard, Fox, Hennig and Schmidt (1996) used a fine grid over the full pose $(x, y, \theta)$ and localized the robot globally. Fox, Burgard and Thrun (1999) gave the general method under the name Markov localization, with the selective update and the filters for people around the robot. Thrun, Burgard and Fox (2005) present it in Chapter 7 as the basis of all localization filters in the book.

## References
