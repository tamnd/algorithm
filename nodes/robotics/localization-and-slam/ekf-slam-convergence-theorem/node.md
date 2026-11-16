---
tag: M4GQH4
kind: theorem
slug: ekf-slam-convergence-theorem
name: EKF SLAM convergence theorem
aliases:
- Dissanayake convergence theorem
area: robotics/localization-and-slam
level: advanced
summary: In linear Gaussian SLAM, landmark uncertainty never grows, and in the limit the landmarks become fully correlated with a floor set by the first pose.
prereqs: [ekf-slam, kalman-filter, positive-definite-matrix]
see_also: [ekf-slam, slam-problem, online-slam, extended-information-filter, covariance-matrix, determinant, observability, kalman-filter]
sources:
  - paper: "M. W. M. Gamini Dissanayake, Paul Newman, Steven Clark, Hugh F. Durrant-Whyte and M. Csorba, A solution to the simultaneous localization and map building (SLAM) problem, IEEE Transactions on Robotics and Automation 17(3), 2001, pages 229 to 241"
    locator: "Section III.A, Theorems 1 to 3 (the determinant of a submatrix of the map covariance, the full correlation of the landmarks in the limit, and the lower bound set by the initial vehicle covariance)"
  - paper: "Simon J. Julier and Jeffrey K. Uhlmann, A counter example to the theory of simultaneous localization and map building, Proceedings of the IEEE International Conference on Robotics and Automation, 2001"
    locator: the inconsistency of the nonlinear EKF SLAM for a stationary robot
  - paper: doi:10.1109/TRO.2007.903811
    title: "Shoudong Huang and Gamini Dissanayake, Convergence and consistency analysis for extended Kalman filter based SLAM, IEEE Transactions on Robotics 23(5), 2007, pages 1036 to 1049"
    locator: the analysis of the nonlinear planar EKF SLAM and the role of the Jacobians evaluated at different estimates
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10 (EKF SLAM and the correlations between the landmarks)"
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the history of the problem and the convergence of the joint estimate
---

The EKF SLAM convergence theorem of Dissanayake, Newman, Clark, Durrant-Whyte and Csorba (2001) describes what the Kalman filter for [SLAM](/slam-problem/) does to the map uncertainty when the models are linear and the noise is Gaussian. Three things hold. The uncertainty of the map never grows. The landmarks become fully correlated in the limit, so their relative positions become exact. And the uncertainty of each landmark never falls below the uncertainty of the robot at the time it first saw a landmark. The theorem is for the linear Gaussian case only, where the [Kalman filter](/kalman-filter/) is exact. For the nonlinear [EKF SLAM](/ekf-slam/) of a real robot it is a guide, not a guarantee: the nonlinear filter can become inconsistent.

## Statement

**Model.** A vehicle position $x_k \in \mathbb{R}^d$ and $n$ landmarks $p_1, \dots, p_n \in \mathbb{R}^d$ that do not move. The vehicle moves by $x_{k+1} = x_k + u_k + v_k$ with a known $u_k$ and $v_k \sim N(0, Q_k)$. A reading of landmark $i$ at step $k$ is $z_{ik} = p_i - x_k + w_{ik}$ with $w_{ik} \sim N(0, R)$, $R$ positive definite. All noises are independent. The prior on the first pose is $x_0 \sim N(\hat x_0, P_0)$, and a landmark has no prior information: it enters the filter at its first reading, as in EKF SLAM. Let $P_k$ be the covariance of the Kalman filter after step $k$, and $P_{ij}$ its block for landmarks $i$ and $j$. Inequalities between matrices are in the order of positive semidefinite matrices: $A \ge B$ means that $A - B$ is positive semidefinite.

Dissanayake et al. state and prove the three results for a linear SLAM model; the proof below is written for the model above, which is the simplest one of this kind.

**Theorem.**

1. **The map uncertainty never grows.** Neither a prediction nor an update increases the block of $P$ for the landmarks already in the map. Hence the determinant of every principal submatrix of the map covariance does not increase from step to step.
2. **Full correlation in the limit.** If landmarks $i$ and $j$ have been read together from the same pose at $k$ steps, then $\operatorname{Cov}(p_i - p_j) = P_{ii} + P_{jj} - P_{ij} - P_{ji} \le 2R / k$. So if they are read together infinitely often, the covariance of their difference tends to 0, and the landmark estimates become fully correlated.
3. **A floor set by the first pose.** At every step, $P_{ii} \ge P_0$ for every landmark $i$, and the covariance of the vehicle is also at least $P_0$. Here $P_0$ is the covariance of the vehicle when it first reads a landmark.

The paper says that the determinant of any submatrix "decreases monotonically"; the proof below gives "does not increase" for the principal submatrices, the ones that are covariances of a set of landmark coordinates.

## In plain words

Take a robot that drives around and looks at fixed marks, where all errors are simple bell curves. Three things then hold. First, every new look at the marks makes the map more certain or leaves it as it is; it never makes it worse. Second, the robot learns where the marks are relative to each other better and better, and in the end it knows their relative layout exactly. Third, it can never know where the whole layout sits in the world better than it knew its own start position, because every reading is about differences, from the robot to a mark or from one place to the next. The whole map can slide together by the error of the start, and no reading can see that.

## Proof

**The filter is the exact posterior.** In this model every quantity is a linear function of the Gaussian variables $x_0$, $v_k$ and $w_{ik}$, so the Kalman filter computes the exact conditional mean and covariance of the state given the data. A landmark with no prior information enters at its first reading $z$ with the mean $x_k + z$ and the covariance of $x_k + w$, which is the limit of the posterior under a Gaussian prior $N(0, \lambda I)$ on $p_i$ as $\lambda \to \infty$. Statements 1 and 2 are proved below for every finite $\lambda$, and they pass to the limit because they are non-strict inequalities between continuous functions of $\lambda$. Statement 3 is proved directly for the flat prior, whose posterior is a proper Gaussian once each landmark has a reading, with the limit mean and covariance.

**Lemma.** If $A \ge B \ge 0$ are symmetric, then $\det A \ge \det B$. If $B$ is singular, $\det B = 0 \le \det A$. Else $A = B^{1/2} (I + C) B^{1/2}$ with $C = B^{-1/2} (A - B) B^{-1/2} \ge 0$, so $\det A = \det B \cdot \det(I + C)$, and every eigenvalue of $I + C$ is at least 1.

**Proof of 1.** The prediction changes the vehicle and leaves the landmarks as they are, so the landmark block of $P$ is unchanged; only the vehicle block and the cross block change. An update with innovation covariance $S$ and gain $W$ gives $P^+ = P^- - W S W^\top$, and $W S W^\top \ge 0$ because $S > 0$. So $P^+ \le P^-$. For a set $I$ of landmark coordinates, the principal submatrices satisfy $P^+_{II} \le P^-_{II}$, since $y^\top (P^- - P^+) y \ge 0$ holds in particular for every $y$ that is zero outside $I$. Adding a new landmark appends rows and columns and leaves the old block unchanged. By the lemma, the determinant of every principal submatrix of the old landmarks does not increase. $\square$

**Proof of 2.** Let $k_1, \dots, k_k$ be the steps at which both $i$ and $j$ were read. Then $z_{i k_l} - z_{j k_l} = (p_i - p_j) + (w_{i k_l} - w_{j k_l})$: the vehicle position cancels. The estimate $g = \frac{1}{k} \sum_l (z_{i k_l} - z_{j k_l})$ has the error $g - (p_i - p_j) = \frac{1}{k} \sum_l (w_{i k_l} - w_{j k_l})$, which has mean 0 and covariance $2R / k$, whatever the state. The conditional mean is the estimate with the smallest error covariance among all functions of the data: for every fixed vector $b$, $\operatorname{E}[(b^\top (\delta - \operatorname{E}[\delta \mid D]))^2] \le \operatorname{E}[(b^\top (\delta - g))^2]$, where $\delta = p_i - p_j$ and $D$ is the data. In the linear Gaussian case, the conditional covariance of $\delta$ does not depend on the values of the data, so the left side is $b^\top \operatorname{Cov}(\delta \mid D) \, b$, and the right side is $b^\top (2R / k) \, b$. This holds for every $b$, so $\operatorname{Cov}(p_i - p_j) \le 2R / k$.

As $k \to \infty$, $P_{ii} + P_{jj} - P_{ij} - P_{ji} \to 0$. In one dimension, write $\rho = P_{ij} / \sqrt{P_{ii} P_{jj}}$. Then $P_{ii} + P_{jj} - 2 P_{ij} = (\sqrt{P_{ii}} - \sqrt{P_{jj}})^2 + 2 \sqrt{P_{ii} P_{jj}} \, (1 - \rho)$, a sum of two nonnegative terms. By statement 3, $\sqrt{P_{ii} P_{jj}} \ge P_0 > 0$, so $\rho \to 1$: the two estimates become fully correlated. In several dimensions, the same holds along each direction $b$. $\square$

**Proof of 3.** Write $y = x_0$ and describe every other variable relative to it: $r_k = x_k - x_0$ and $s_i = p_i - x_0$. Then $r_0 = 0$, $r_{k+1} = r_k + u_k + v_k$ and $z_{ik} = s_i - r_k + w_{ik}$. So the data depend on the relative variables $(r, s)$ and on the noise, and not on $y$. In the prior, $y \sim N(\hat x_0, P_0)$ is independent of the $v_k$, so it is independent of the $r_k$, and the flat prior on the landmarks makes the $s_i$ flat and independent of $y$ too. Hence the posterior density factors as $p(y) \, p(r, s \mid D)$: given the data, $y$ is still $N(\hat x_0, P_0)$ and independent of $(r, s)$. So $\operatorname{Cov}(p_i \mid D) = \operatorname{Cov}(y + s_i \mid D) = P_0 + \operatorname{Cov}(s_i \mid D) \ge P_0$, and in the same way $\operatorname{Cov}(x_k \mid D) = P_0 + \operatorname{Cov}(r_k \mid D) \ge P_0$. If the robot moved before its first reading of a landmark, take that time as step 0; the data before it carry no information about any landmark. $\square$

## Consequences

- **The correlations must be kept.** The exact posterior has landmarks that become fully correlated, so a filter that drops the cross covariances, for example to save time, throws away the information that makes the map converge, and it reports a wrong uncertainty. This is why EKF SLAM keeps the full covariance and pays $O(m^2)$ per update for $m$ landmarks.
- **Relative accuracy is unlimited, absolute accuracy is not.** The layout of the map becomes exact, but its place in the world is only as good as the robot's knowledge of its start. With the map frame fixed at the first pose, $P_0 = 0$, and the map converges completely.
- **The map covariance becomes singular in the limit.** In the example below its determinant goes to 0. In practice this means that the information form, the inverse of $P$, has entries that grow without bound, and a filter must take care with rounding.
- **An exact filter never reports less than the floor.** A nonlinear filter that reports a landmark or a vehicle covariance below $P_0$ is overconfident. This gives a simple check of consistency in simulation.

## Tightness

**A 1D example, by hand.** A robot stands still on a line, with $u_k = 0$ and $Q_k = 0$. Its position has the prior variance $P_0 = 1$. At each step it reads two landmarks with $R = 1$. After $k$ steps, by the proof of statement 3, the position is still $N(\hat x_0, 1)$, independent of the relative positions $s_1, s_2$, and each $s_i$ is known from the mean of its $k$ readings with variance $1 / k$. So

$$P_{11} = P_{22} = 1 + \frac{1}{k}, \qquad P_{12} = 1, \qquad \rho = \frac{1}{1 + 1/k}, \qquad \det \begin{pmatrix} P_{11} & P_{12} \\ P_{12} & P_{22} \end{pmatrix} = \frac{2}{k} + \frac{1}{k^2}.$$

After one step the variance of each landmark is $2 = P_0 + R$, as in the EKF initialization. The determinant goes $3, 1.25, 0.778, 0.5625$ for $k = 1, 2, 3, 4$, down, as statement 1 says. $\operatorname{Var}(p_1 - p_2) = 2/k$, which is exactly the bound $2R/k$ of statement 2. And $P_{ii} \to 1 = P_0$, the floor of statement 3, which is reached in the limit and not before. So the bounds of statements 2 and 3 cannot be improved in general. This short script runs the Kalman filter on the example and prints $P_{11}$, $P_{12}$, the determinant and $\operatorname{Var}(p_1 - p_2)$:

```python
def update(mu, P, i, z, R=1.0):  # the state is (x, p1, p2); the reading is z = p_i - x + w
    h = [-1.0, 0.0, 0.0]
    h[i] = 1.0
    Ph = [sum(P[r][c] * h[c] for c in range(3)) for r in range(3)]
    S = sum(h[r] * Ph[r] for r in range(3)) + R
    nu = z - sum(h[r] * mu[r] for r in range(3))
    mu = [mu[r] + Ph[r] * nu / S for r in range(3)]
    P = [[P[r][c] - Ph[r] * Ph[c] / S for c in range(3)] for r in range(3)]
    return mu, P

big = 1e9  # no prior information on the landmarks
mu, P = [0.0, 0.0, 0.0], [[1.0, 0, 0], [0, big, 0], [0, 0, big]]
for k in range(1, 5):
    mu, P = update(mu, P, 1, 2.0)
    mu, P = update(mu, P, 2, 3.0)
    det = P[1][1] * P[2][2] - P[1][2] ** 2
    print(k, round(P[1][1], 6), round(P[1][2], 6), round(det, 6), round(P[1][1] + P[2][2] - 2 * P[1][2], 6))
# 1 2.0 1.0 3.0 2.0
# 2 1.5 1.0 1.25 1.0
# 3 1.333333 1.0 0.777778 0.666667
# 4 1.25 1.0 0.5625 0.5
```

**The hypotheses matter.**

- **Linearity.** For a nonlinear model, such as a planar robot with a heading and range and bearing readings, the EKF linearizes at the current estimate, and the statements are no longer theorems about it. Julier and Uhlmann (2001) showed with a stationary robot that the nonlinear EKF SLAM becomes inconsistent: its covariance becomes smaller than its true error. Huang and Dissanayake (2007) analyzed the nonlinear planar case and related the inconsistency to Jacobians evaluated at different estimates.
- **Relative readings.** Statement 3 needs readings and motions that see only differences. A sensor that measures absolute position, such as satellite positioning, breaks the floor, as it should.
- **Static landmarks.** If the landmarks move, the prediction adds noise to the map block, and statement 1 fails.
- **Repeated joint readings.** Statement 2 needs the two landmarks to be read together from the same pose again and again. Landmarks that are never seen together are still correlated through the path, but the bound $2R / k$ does not apply directly.

## History

Smith, Self and Cheeseman introduced the stochastic map in the late 1980s: one state vector and one covariance for the robot and all the objects, with the correlations between them. Durrant-Whyte and Bailey (2006) recall that many researchers at first expected the errors of such a map to grow without bound, and that the key step was to see that the joint problem of localization and mapping converges. Dissanayake, Newman, Clark, Durrant-Whyte and Csorba proved the three results above for the linear case in the IEEE Transactions on Robotics and Automation in 2001, and showed the filter at work on a vehicle with a millimeter wave radar. The same year, Julier and Uhlmann gave a counterexample for the nonlinear filter. Later work, such as Huang and Dissanayake (2007), studied when the nonlinear EKF SLAM is consistent.

## References
