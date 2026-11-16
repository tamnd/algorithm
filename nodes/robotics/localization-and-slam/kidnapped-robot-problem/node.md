---
tag: B6V3H3
kind: problem
slug: kidnapped-robot-problem
name: Kidnapped robot problem
aliases:
- robot kidnapping
area: robotics/localization-and-slam
level: core
summary: Global localization after the robot is moved without being told, which tests whether a method can recover from a confident wrong belief.
prereqs: [global-localization]
see_also: [global-localization, monte-carlo-localization, markov-localization, mobile-robot-localization, kld-sampling, particle-filter, histogram-filter, likelihood-ratio-test]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 7, Section 7.1 (the kidnapped robot problem as a harder variant of global localization) and Chapter 8, Section 8.3.5 (Monte Carlo localization with random particles, and the averages w_slow and w_fast)"
  - paper: doi:10.1109/ROBOT.1992.220057
    title: "Sean P. Engelson and Drew V. McDermott, Error correction in mobile robot map learning, Proceedings of the IEEE International Conference on Robotics and Automation, 1992, pages 2555 to 2560"
    locator: the paper that Thrun et al. name as the origin of the kidnapped robot problem
  - paper: doi:10.1016/S0004-3702(01)00069-8
    title: "Sebastian Thrun, Dieter Fox, Wolfram Burgard and Frank Dellaert, Robust Monte Carlo localization for mobile robots, Artificial Intelligence 128(1-2), 2001, pages 99 to 141"
    locator: Mixture-MCL, which draws some particles from the measurement instead of the motion, and its tests with kidnapping
  - paper: "Jens-Steffen Gutmann and Dieter Fox, An experimental comparison of localization methods continued, Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems, 2002, pages 454 to 459"
    locator: measured comparison of localization methods, including their recovery after kidnapping
---

The kidnapped robot problem asks a localization method to recover after the robot is carried to another place without being told. Before the kidnapping, the method tracks the pose well and its belief is confident. After it, the belief is confident and wrong. The method must notice that its readings no longer fit, and then solve [global localization](/global-localization/) again. Thrun, Burgard and Fox describe it as more difficult than global localization, and they attribute it to Engelson and McDermott (1992). Real robots are seldom carried away, but the problem stands for every failure that leaves a confident wrong belief: a wheel slip, a bad reading, a jump in the software. A plain [particle filter](/particle-filter/) cannot recover, because it has no particles near the new pose. The usual fixes add random particles when the readings become unlikely, which is a heuristic.

## In plain words

You sleep in a train, sure that you are at home in your own bed. Someone moves you to a hotel room. When you wake up, you first think you are at home. Then the window is in the wrong place and the door has the wrong color. A sensible person notices that too many things do not fit, drops the old belief, and looks around from the start. A robot must do the same: notice that its sensor readings keep surprising it, and then start to search for its pose again. A robot that trusts its old belief too much will try to explain every reading from the wrong place.

## Definition

**Input.** As in [mobile robot localization](/mobile-robot-localization/): a map, a motion model, a measurement model, and a stream of controls and readings. The true poses follow the motion model, except at one unknown time $\tau$ or at several, when the pose jumps to a new pose that does not depend on the controls. The robot is not told $\tau$.

**Output.** A belief at each time $t$ that is near the true pose again within some time after each jump.

**Why it is harder than global localization.** In global localization the method knows that it knows nothing, and it starts with a uniform belief. Here the method does not know when it knows nothing. A method that solves it must keep some doubt at all times, or must detect the jump from the data.

**A model of the jump.** One way to state the problem as filtering is to add a jump to the motion model:

$$p(x_t \mid u_t, x_{t-1}) = (1 - \rho)\, p_{\text{motion}}(x_t \mid u_t, x_{t-1}) + \rho\, \frac{1}{|X_{\text{free}}|}.$$

With a small $\rho > 0$, the exact Bayes filter keeps a little probability at every pose, so it can recover. The approximate filters must copy this behavior.

## Variants

| variant | what changes |
|---|---|
| one kidnapping | a single jump at an unknown time; the classic test |
| repeated failures | jumps happen at random times, as in a model of slips and collisions |
| kidnapping to a similar place | the new place looks like the old one, and the jump may stay hidden for a long time |
| detection only | report the time of the jump, without finding the new pose |

## Examples

**A confident wrong particle set.** A robot runs [Monte Carlo localization](/monte-carlo-localization/) with 1000 particles, all within $0.5$ m of its pose in room A. It is carried to room B. Every particle now predicts readings that do not fit room B, so all weights are small. Resampling picks among these particles, and the motion noise moves them only a little at each step. No particle comes near room B, so the plain filter stays wrong. In the example on the Monte Carlo localization page, a robot on a ring of 30 cells with 300 particles is moved 13 cells ahead. In the 30 steps from step 41 to step 70, the most frequent cell of MCL with random particles is the true cell in 21 steps, and that of plain MCL in none. This is a measurement for one seed, not a general rate; with other seeds, plain MCL sometimes recovers by chance through its motion noise.

**Random particles by the averages of the weights.** Augmented MCL keeps two averages of the mean weight $w_{\text{avg}}$ of the particles, a slow one and a fast one:

$$w_{\text{slow}} \leftarrow w_{\text{slow}} + \alpha_{\text{slow}} (w_{\text{avg}} - w_{\text{slow}}), \qquad w_{\text{fast}} \leftarrow w_{\text{fast}} + \alpha_{\text{fast}} (w_{\text{avg}} - w_{\text{fast}}),$$

and replaces each particle by a random pose with probability $\max(0, 1 - w_{\text{fast}} / w_{\text{slow}})$. Take $\alpha_{\text{slow}} = 0.05$, $\alpha_{\text{fast}} = 0.5$, and a long run with $w_{\text{avg}} = 0.8$, so both averages are $0.8$. Then the robot is kidnapped, and $w_{\text{avg}}$ falls to $0.2$.

| step after the jump | $w_{\text{slow}}$ | $w_{\text{fast}}$ | probability of a random particle |
|---|---|---|---|
| 0 | 0.800 | 0.800 | 0 |
| 1 | 0.770 | 0.500 | 0.351 |
| 2 | 0.742 | 0.350 | 0.528 |
| 3 | 0.714 | 0.275 | 0.615 |

The fast average follows the drop at once and the slow one remembers the old level, so the ratio falls and more random particles enter. Once the filter has found the new pose, $w_{\text{avg}}$ rises again, the fast average passes the slow one, and the injection stops.

**A hidden kidnapping.** A robot in one of two equal offices is carried to the other one and put at the same pose in that office. Its readings do not change, so no method can see the jump until the robot leaves the office.

## Known algorithms

| method | how it recovers | kind of claim |
|---|---|---|
| [Markov localization](/markov-localization/) on a grid with a small uniform term $\rho$ in the motion model | every cell keeps a probability of at least $\rho / g$ after each prediction, so the true cell can grow again | exact for the jump model above |
| augmented MCL, with random particles (Thrun et al. Section 8.3.5) | adds random particles when $w_{\text{fast}}$ falls below $w_{\text{slow}}$ | heuristic |
| MCL with a fixed rate of random particles | always replaces a small fraction of the particles by random poses | heuristic; costs accuracy while tracking |
| Mixture-MCL (Thrun, Fox, Burgard and Dellaert, 2001) | draws some particles from the poses that fit the current reading, and weights them by the predicted belief | heuristic with a sound weighting; needs a way to sample poses from a reading |
| [KLD-sampling](/kld-sampling/) with random particles | adds random particles and lets the number of particles grow when the belief spreads | heuristic |
| multiple hypothesis tracking | starts new hypotheses when the readings fit none of the old ones | heuristic |

Gutmann and Fox (2002) compared several localization methods, including their recovery after kidnapping. Their results are measurements on their data.

## Bounds

- **Hidden jumps (a theorem).** If the robot is moved to a pose whose readings have the same distribution as the old pose for every motion it makes, then the data after the jump have the same distribution with or without the jump. No method can detect such a jump, however it is built.
- **Recovery needs doubt (a theorem).** If an approximate filter gives zero probability to a region and never adds probability there except by the motion model, then the filter cannot place the true pose in that region after a jump to it, unless the motion moves probability there. A plain particle filter with bounded motion noise is of this kind. Random particles, a uniform term in the motion model and Mixture-MCL break this.
- **The cost of doubt (a heuristic).** Each random particle is a particle that does not track the pose. A fixed rate of random particles makes tracking less accurate for the same number of particles. The averages $w_{\text{slow}}$ and $w_{\text{fast}}$ reduce this cost because they add particles only after the readings become unlikely, but a short burst of bad readings, such as a person in front of the laser, also triggers them.

## Reductions

- **To global localization.** After a jump is detected, the problem is global localization with the readings that come after the jump.
- **To change detection.** Detecting the jump is a test of whether the recent readings fit the current belief. The averages $w_{\text{fast}}$ and $w_{\text{slow}}$ are a simple heuristic test of this kind. A [likelihood ratio test](/likelihood-ratio-test/) between the hypotheses "no jump" and "a jump at time $\tau$" is the classical form.
- **To filtering with a jump model.** With the uniform term $\rho$ in the motion model, the problem becomes ordinary localization, and an exact Bayes filter solves it.

## Applications

The kidnapped robot problem is used as a test of robustness for localization methods. Recovery from a wrong belief matters for robots that are carried by people, such as cleaning robots and delivery robots that are lifted or pushed, for robots in crowds, where people block the sensors for a long time, and for long missions, where a rare failure is sure to happen at some point.

## References
