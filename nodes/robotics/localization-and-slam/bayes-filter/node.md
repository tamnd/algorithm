---
tag: V7B1QT
kind: algorithm
slug: bayes-filter
name: Bayes filter
aliases:
- recursive Bayesian estimation
- recursive state estimation
area: robotics/localization-and-slam
level: intro
summary: Updates a belief over the state by a prediction with the motion model and a correction by Bayes' rule with the measurement model.
solves: [filtering]
model: real-ram
complexity:
  vars: {g: the number of states of a finite state space, T: the number of time steps}
  time: {worst: O(T g^2)}
  space: {extra: O(g)}
properties: {deterministic: true, exact: true, online: true, recursive: true}
history:
  year: 1964
  people: [Yu-Chi Ho, Robert C. K. Lee]
  note: Ho and Lee wrote estimation as the step by step update of a conditional density by Bayes' rule, and derived the Kalman filter as the linear Gaussian case.
prereqs: [bayes-theorem, conditional-independence, filtering]
see_also: [kalman-filter, particle-filter, histogram-filter, markov-localization, forward-algorithm, odometry-motion-model, beam-range-finder-model, occupancy-grid-mapping]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 2, Section 2.4 (the Bayes filter algorithm of Table 2.1, the door example, the derivation and the Markov assumption)"
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 4 (probabilistic state space models and the Bayesian filtering equations)"
  - paper: "Yu-Chi Ho and Robert C. K. Lee, A Bayesian approach to problems in stochastic estimation and control, IEEE Transactions on Automatic Control 9(4), 1964, pages 333 to 339"
    locator: the recursive Bayesian update of the conditional density, and the Kalman filter derived from it
  - paper: "Dieter Fox, Wolfram Burgard and Sebastian Thrun, Markov localization for mobile robots in dynamic environments, Journal of Artificial Intelligence Research 11, 1999, pages 391 to 427"
    locator: the Bayes filter over a grid of robot poses for localization, and the Markov assumption in environments with people
---

The Bayes filter is the exact recursive solution of the [filtering](/filtering/) problem: at each time step it turns the belief $\mathrm{bel}(x_{t-1})$, a probability distribution over the state of a system, into $\mathrm{bel}(x_t)$ by a prediction with the motion model and a correction with the measurement model by [Bayes' theorem](/bayes-theorem/). It is correct when the state is Markov, so it is the filter of a [hidden Markov model](/hidden-markov-model/) or of a [state-space model](/state-space-model/) with controls. As written, it is a recursion of distributions, not a program: the [Kalman filter](/kalman-filter/) is its closed form in the linear Gaussian case, the [particle filter](/particle-filter/) is a Monte Carlo approximation, and the [histogram filter](/histogram-filter/) runs it on a grid. This page gives the recursion, its proof and the exact version for a finite state space, where it costs $O(g^2)$ time per step for $g$ states.

## In plain words

A robot does not know exactly where it is. It keeps a score for each place where it could be, and the scores add up to one. Two things happen again and again. First the robot moves. Its wheels slip, so the scores spread out: each place passes its score to the places the robot could reach from there. Then the robot looks at the world, for example it sees a door. Each place keeps its score times the chance of seeing a door from that place. Places with no door near them lose most of their score. At the end, the robot divides all scores by their total, so that they add up to one again. After a few moves and looks, most of the score sits on a few places, and often on one.

## The problem

The state $x_t$ of the robot (for example its pose $(x, y, \theta)$, or a cell of a map) changes at each time step $t = 1, 2, \ldots$ under a control $u_t$, and the robot gets a measurement $z_t$. The notation is the one of Thrun, Burgard and Fox (2005). The model has three parts:

- the initial belief $\mathrm{bel}(x_0) = p(x_0)$;
- the motion model $p(x_t \mid u_t, x_{t-1})$, for example the [odometry motion model](/odometry-motion-model/) or the [velocity motion model](/velocity-motion-model/);
- the measurement model $p(z_t \mid x_t)$, for example the [beam range finder model](/beam-range-finder-model/) or the [landmark measurement model](/landmark-measurement-model/). With a map $m$ it is $p(z_t \mid x_t, m)$; the map is fixed and known here.

Two conditional independence assumptions, together called the Markov assumption, make the state complete:

$$p(x_t \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(x_t \mid u_t, x_{t-1}), \qquad p(z_t \mid x_{0:t}, z_{1:t-1}, u_{1:t}) = p(z_t \mid x_t).$$

The output at each step is the posterior $\mathrm{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$. The prediction before the measurement is $\overline{\mathrm{bel}}(x_t) = p(x_t \mid z_{1:t-1}, u_{1:t})$.

## The algorithm

For a continuous state, read each sum as an integral.

```pseudo id=main
BAYES-FILTER(bel, u_t, z_t)              ▷ bel(x) = bel(x_{t-1}) for each state x
L1  for each state x_t do
L2      bel_bar(x_t) ← Σ_{x_{t-1}} p(x_t | u_t, x_{t-1}) bel(x_{t-1})    ▷ prediction
L3  bel'(x_t) ← p(z_t | x_t) bel_bar(x_t) for each state x_t             ▷ correction
L4  η ← 1 / Σ_{x_t} bel'(x_t)
L5  bel(x_t) ← η bel'(x_t) for each state x_t
L6  return bel
```

Line L2 is the law of total probability over the previous state. It is the Chapman-Kolmogorov equation of a [Markov chain](/markov-chain/) whose transition depends on the control. Line L3 is the numerator of Bayes' theorem, and lines L4 and L5 divide by the evidence $p(z_t \mid z_{1:t-1}, u_{1:t}) = 1/\eta$. The sequence of one prediction and one correction per step is the form of Thrun et al., Table 2.1. A step with no measurement skips lines L3 to L5, and a step with no motion skips lines L1 and L2.

The algorithm in this form needs a sum or an integral over the whole state space. It can run exactly in two cases only: a finite state space (this page, and the [forward algorithm](/forward-algorithm/) for hidden Markov models) and the linear Gaussian case (the Kalman filter). All other filters of robotics approximate one of the two lines L2 or L3.

## Example

**The door.** This is the example of Thrun et al. (Section 2.4). A robot faces a door that is open or closed. Its sensor says "open" with probability $0.6$ if the door is open and $0.2$ if it is closed. The robot can do nothing, or push. A push opens a closed door with probability $0.8$, and an open door stays open. The prior is $\mathrm{bel}(\text{open}) = 0.5$.

| step | control and measurement | $\overline{\mathrm{bel}}(\text{open})$ | $\mathrm{bel}'(\text{open}), \mathrm{bel}'(\text{closed})$ | $\mathrm{bel}(\text{open})$ |
|---|---|---|---|---|
| 1 | nothing, "open" | $1/2$ | $3/10, 1/10$ | $3/4 = 0.75$ |
| 2 | push, "open" | $3/4 + 0.8 \cdot 1/4 = 19/20$ | $57/100, 1/100$ | $57/58 \approx 0.983$ |

After two steps the robot is quite sure that the door is open, but not sure: the closed state keeps the probability $1/58$, because the sensor can be wrong.

**A corridor.** A robot moves in a ring of 6 cells, numbered 0 to 5. Cells 0, 1 and 3 have a door. The command "one cell forward" moves the robot by 0, 1 or 2 cells with probabilities $0.1$, $0.8$ and $0.1$. The door detector says "door" with probability $0.75$ at a door and $0.2$ elsewhere. The prior is uniform, and the robot moves and then senses "door", "door", "wall".

| after | cell 0 | cell 1 | cell 2 | cell 3 | cell 4 | cell 5 |
|---|---|---|---|---|---|---|
| move, "door" | 0.2632 | 0.2632 | 0.0702 | 0.2632 | 0.0702 | 0.0702 |
| move, "door" | 0.1514 | 0.4127 | 0.1101 | 0.1841 | 0.1013 | 0.0404 |
| move, "wall" | 0.0242 | 0.0699 | 0.4786 | 0.0620 | 0.2262 | 0.1391 |

The first belief is $5/19$ at each door and $4/57$ elsewhere. After the third step the most likely cell is 2, the only cell without a door that follows two cells with a door. The belief is exact: summing the joint probability over all $6^4 = 1296$ paths of states gives the same fractions.

## Correctness

Under the Markov assumption, and if each control $u_t$ is chosen from the past data $z_{1:t-1}, u_{1:t-1}$ and randomness that is independent of the state, the output of each step is exactly $p(x_t \mid z_{1:t}, u_{1:t})$. The proof is by induction on $t$. Line L2 is correct because the motion model does not depend on older states and older data, and because the new control carries no information about $x_{t-1}$. Line L3 is correct because the measurement depends only on $x_t$. The full proof is in [the correctness proof](proofs/correctness.md). Without the Markov assumption, the same lines still run, but the output is no longer the posterior.

## Complexity

Let $g$ be the number of states of a finite state space. These bounds are in the [real RAM](/real-ram/) model, with one operation per arithmetic step on a real number.

- Line L2 costs $O(g)$ for each of the $g$ states, so the prediction costs $O(g^2)$. If from each state only $b$ next states have a nonzero probability, it costs $O(g b)$. On a grid of poses, $b$ is the number of cells that one step of motion can reach, so a short time step keeps the prediction cheap.
- Lines L3 to L5 cost $O(g)$ plus $g$ evaluations of the measurement model.
- Over $T$ steps, the time is $O(T g^2)$ in the worst case, and the memory is $O(g)$: the filter keeps only the current belief.

For a continuous state, the exact filter is not finite. The Kalman filter keeps a mean and a covariance and costs $O(d^3)$ per step for a state of dimension $d$. A grid with a fixed resolution has a number of cells that grows exponentially with the dimension of the state, which is why grids are used for planar poses (3 dimensions) and rarely above.

## Properties

- **Exact for a finite state space.** With exact arithmetic, the output equals the posterior. The implementation below uses Python fractions for the tests.
- **Online and recursive.** Each step uses only the last belief, the new control and the new measurement. The past data are not stored.
- **Multimodal.** The belief can have several peaks, as in the corridor example. A Gaussian filter cannot represent this.
- **Normalization is optional until the end.** The unnormalized belief $\mathrm{bel}'$ gives the same posterior after one division at any later time; normalizing at each step only keeps the numbers in range.
- **Its normalizer is the likelihood.** For controls fixed in advance, the product of the evidences $1/\eta$ over all steps is the probability of the measurements $z_{1:T}$ under the controls $u_{1:T}$. This number can compare two models of the same data.

## Variants and improvements

- **[Kalman filter](/kalman-filter/).** Linear motion and measurement models with Gaussian noise keep the belief Gaussian, so the filter tracks only a mean $\mu$ and a covariance $\Sigma$. The [extended](/extended-kalman-filter/) and [unscented](/unscented-kalman-filter/) Kalman filters approximate a nonlinear model.
- **[Histogram filter](/histogram-filter/).** It splits a continuous state space into cells and runs this algorithm on the cells. For robot pose estimation with a map, this is grid [Markov localization](/markov-localization/).
- **[Particle filter](/particle-filter/).** It represents the belief by samples, draws line L2 from the motion model, weights by line L3, and [resamples](/resampling/). For localization it is [Monte Carlo localization](/monte-carlo-localization/).
- **Binary Bayes filter with a static state.** When the state does not change, the prediction is the identity, and the update of one binary variable is a sum of log odds. This is the cell update of [occupancy grid mapping](/occupancy-grid-mapping/).
- **Smoothing.** A backward pass after the filter gives $p(x_t \mid z_{1:T}, u_{1:T})$ for $t < T$; see [smoothing](/smoothing/).

## When to use it

Use the exact algorithm when the state space is small and finite: the position of a robot in a topological map, a door that is open or closed, or a fault mode of a machine. Use it as the template for every other estimator of the area: [mobile robot localization](/mobile-robot-localization/) and SLAM methods are Bayes filters with a chosen representation of the belief, and the choice decides what they can represent and what they cost.

## Pitfalls

- **Zero probabilities.** If the measurement model gives probability zero to the true state once, that state never comes back, because line L3 multiplies by zero. A wrong reading can then make the belief wrong forever, or empty it, in which case line L4 divides by zero. Real models add a small floor, such as the random term of the [beam range finder model](/beam-range-finder-model/).
- **Underflow.** Many sharp measurements make the products too small for floating point numbers. Normalize at each step, or work with logarithms.
- **Measurements that are not independent.** The Markov assumption says that the noise of two measurements is independent given the state. Neighboring beams of a laser scanner and repeated readings of the same object are not. The filter then counts the same evidence many times and becomes too confident. A common rule of thumb is to use only a subset of the beams, or to raise the likelihood to a power less than one; this is a heuristic, not a correction derived from the model.
- **An incomplete state.** People who walk near the robot, or a map that is out of date, break the Markov assumption, because they are part of the world but not of the state. Fox, Burgard and Thrun (1999) filter out readings that such effects explain.
- **The order of the two lines.** Some texts and programs correct first and predict second, so the belief at the end of a step is a prediction. Both orders are correct, but the result at time $t$ means a different thing.

## Implementations

## History

Ho and Lee (1964) wrote estimation as the update of the conditional density of the state, step by step, with Bayes' rule, and derived the Kalman filter as the case of linear models with Gaussian noise. The name "Bayes filter" and the form with a control in each step are those of the robotics literature, in particular of Thrun, Burgard and Fox (2005), who build the whole book on it. Grid versions of the filter were used for robot localization in the 1990s, for example by Fox, Burgard and Thrun (1999).

## References
