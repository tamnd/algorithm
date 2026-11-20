---
tag: SJQJT4
kind: problem
slug: max-min-sinr-power-control
name: Max-min SINR power control
aliases:
- max-min fair power control
- SINR balancing
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Choose powers to make the smallest SINR of the links as large as possible. With a total power limit, the answer is the Perron eigenvalue and eigenvector of a positive matrix."
model: real-ram
complexity:
  vars: {K: the number of links, L: the number of bisection steps}
  time: {worst: O(K^3 L)}
prereqs: [foschini-miljanic-power-control, perron-frobenius-theorem]
see_also: [standard-interference-function, foschini-miljanic-power-control, geometric-programming-power-control, weighted-sum-rate-maximization, max-min-fairness, power-iteration, bisection-method, quasiconvex-function]
sources:
  - paper: doi:10.1109/25.120145
    title: "Jens Zander, Performance of optimum transmitter power control in cellular radio systems, IEEE Transactions on Vehicular Technology 41(1), 1992, pages 57 to 62"
    locator: "the noise-free model, the largest common SINR as the inverse of the largest eigenvalue of the normalized gain matrix, and the eigenvector as the optimal powers"
  - paper: doi:10.1109/TWC.2007.05960
    title: "Mung Chiang, Chee Wei Tan, Daniel P. Palomar, Daniel O'Neill and David Julian, Power control by geometric programming, IEEE Transactions on Wireless Communications 6(7), 2007, pages 2640 to 2651"
    locator: "the max-min SINR (and max-min weighted SINR) problem written as a geometric program"
  - paper: doi:10.1109/25.260747
    title: "Gerard J. Foschini and Zoran Miljanic, A simple distributed autonomous power control algorithm and its convergence, IEEE Transactions on Vehicular Technology 42(4), 1993, pages 641 to 646"
    locator: "the feasibility condition for a common SINR target with receiver noise"
---

Max-min SINR power control is the problem of choosing the transmit powers of $K$ links that share a band so that the worst SINR among them is as large as possible, under limits on the power. It is the fair counterpart of [Foschini-Miljanic power control](/foschini-miljanic-power-control/), which meets fixed targets with the least power: here the common target is not given but is pushed up until the power limit stops it. Without noise, Zander showed that the best common SINR is the inverse of the spectral radius of the normalized gain matrix; with noise and a total power limit, the same holds for a positive matrix that also contains the noise, so the answer comes from the [Perron-Frobenius theorem](/perron-frobenius-theorem/). The general case is quasiconvex and is solved by bisection or as a geometric program, the topic of [power control by geometric programming](/geometric-programming-power-control/). The fixed-point view of [standard interference functions](/standard-interference-function/) underlies both.

## In plain words

Several links share one channel, and each one disturbs the others. Each link gets some quality, the ratio of its wanted signal to everything else. We do not want a high total; we want the worst link to be as good as it can be. More power for the worst link helps it but hurts the others, so the best answer gives every link the same quality: if one link were better than the rest, it could give up a little power and lift the others. The question is how high that common quality can go with the power we have. The answer comes from a single number of a matrix built from the gains and the noise, and the best powers are the matching vector of that matrix. A simple search on the common quality also works for any set of power limits.

## Definition

**Input.** Gains $G_{ij} \ge 0$ from transmitter $j$ to receiver $i$, with $G_{ii} > 0$; noise powers $\sigma_i \ge 0$; weights $w_i > 0$ (all $1$ for plain max-min); and a power limit, either a total $\sum_i p_i \le P$ or per-link limits $p_i \le \bar p_i$. The SINR of link $i$ is

$$\mathrm{SINR}_i(p) = \frac{G_{ii}\, p_i}{\sum_{j \ne i} G_{ij}\, p_j + \sigma_i}.$$

**Problem.** Find $p \ge 0$ within the limit that maximizes

$$t(p) = \min_i \frac{\mathrm{SINR}_i(p)}{w_i}.$$

**Notation.** Let $Z_{ij} = w_i G_{ij} / G_{ii}$ for $j \ne i$, $Z_{ii} = 0$, and $v_i = w_i \sigma_i / G_{ii}$. Then $\mathrm{SINR}_i(p) \ge t\, w_i$ for all $i$ exactly when $p \ge t\,(Zp + v)$.

**Output.** The optimal value $t^*$ and an optimal power vector $p^*$.

The problem is *quasiconvex*: for a fixed $t$, the set of feasible $p$ is given by linear inequalities, so it is convex, and it shrinks as $t$ grows. In log variables it is a [geometric program](/geometric-programming/).

## Variants

- **No noise.** With $\sigma = 0$ and no power limit, only the ratios of the powers matter. If $Z$ is irreducible, $t^* = 1 / \rho(Z)$, and $p^*$ is the Perron vector of $Z$ (Zander 1992). This is an upper bound for every noisy case with the same gains.
- **Total power.** With $\sigma > 0$ and $\sum_i p_i \le P$, put $A = Z + \frac{1}{P} v \mathbf{1}^T$. Then $t^* = 1 / \rho(A)$, and $p^*$ is the Perron vector of $A$ scaled to sum $P$. At the optimum all weighted SINRs are equal and the whole power is used.
- **Per-link limits.** With $p_i \le \bar p_i$, put $A_l = Z + \frac{1}{\bar p_l} v e_l^T$ for each link $l$, where $e_l$ is the $l$th unit vector. Then $t^* = \min_l 1/\rho(A_l)$, and the link that attains the minimum is the one at its limit.
- **Weighted.** Weights $w_i$ give each link its own share of quality, for example different rates; the weights only change $Z$ and $v$.
- **With beamforming.** If each link also has an antenna array, the problem becomes SINR balancing over powers and beamformers. For downlink beamforming to separate users it is still solved by eigenvalue methods and a power iteration. For multicast beamforming, where one beam serves a group, the max-min fair problem is NP-hard (Sidiropoulos, Davidson and Luo 2006), and semidefinite relaxation is used.
- **Max-min rate.** With equal weights, since each rate is an increasing function of the SINR, maximizing the smallest rate $\log_2(1 + \mathrm{SINR}_i)$ gives the same powers.

## Examples

**Two links with noise.** Let $G_{11} = G_{22} = 1$, $G_{12} = 0.5$, $G_{21} = 0.2$, $\sigma_1 = \sigma_2 = 0.1$, equal weights and a total power $P = 2$. With equal powers $p = (1, 1)$, the SINRs are $1/(0.5 + 0.1) = 1.667$ and $1/(0.2 + 0.1) = 3.333$, so the worst one is $1.667$. For the optimum,

$$Z = \begin{pmatrix} 0 & 0.5 \\ 0.2 & 0 \end{pmatrix}, \quad v = \begin{pmatrix} 0.1 \\ 0.1 \end{pmatrix}, \quad A = Z + \tfrac{1}{2} v \mathbf{1}^T = \begin{pmatrix} 0.05 & 0.55 \\ 0.25 & 0.05 \end{pmatrix}.$$

The eigenvalues of $A$ are $0.05 \pm \sqrt{0.55 \cdot 0.25}$, so $\rho(A) = 0.42081$ and $t^* = 2.3764$ (3.76 dB). The Perron vector, scaled to sum 2, is $p^* = (1.1946, 0.8054)$, and both SINRs are $2.3764$. The link with the stronger interference gets more power. Without noise the best common SINR would be $1/\sqrt{0.5 \cdot 0.2} = 3.1623$ (5.00 dB); the noise costs 1.24 dB at this power.

**The same links with per-link limits.** With $p_i \le 1.2$ instead of a total limit, $1/\rho(A_1) = 2.3790$ and $1/\rho(A_2) = 2.5923$, so $t^* = 2.3790$ and link 1 is at its limit. With $p_i \le 1$, $t^* = 2.2701$, again with link 1 at its limit. Bisection on $t$ with the linear test below gives the same values.

**Three links without noise.** For the three links of the example on the Foschini-Miljanic page, with gains $G_{ii} = 1$ and cross gains $0.1$ and $0.2$, $\rho(Z) = 0.26274$, so no power vector gives all three links a common SINR above $3.8061$ (5.81 dB). With noise, every common target below this value can be met with enough power, and none above it.

## Known algorithms

- **Bisection on the target.** For a fixed $t$, the least vector with $p \ge t(Zp + v)$ is $p(t) = t\,(I - tZ)^{-1} v$ if $t\,\rho(Z) < 1$, and none exists otherwise. Check whether $p(t)$ meets the power limit, and halve the interval of $t$. Each step solves one linear system in $O(K^3)$ time, so $L$ steps cost $O(K^3 L)$. This works for any limit that is monotone in $p$. See the [bisection method](/bisection-method/).
- **Eigenvalue.** For the total power limit, compute $\rho(A)$ and its Perron vector, by a dense eigenvalue routine in $O(K^3)$ time or by the [power iteration](/power-iteration/) $p \leftarrow P\, A p / \mathbf{1}^T A p$, which converges because $A$ is positive.
- **Normalized fixed-point iteration.** Each link sets $q_i = w_i\, p_i / \mathrm{SINR}_i(p)$, the power it would need for the weighted SINR 1 if the others stayed put, as in [Foschini-Miljanic](/foschini-miljanic-power-control/). Then all powers are scaled by one common factor, $p = P q / \mathbf{1}^T q$. When $\mathbf{1}^T p = P$, $q = Zp + v = Ap$, so this is the power iteration on $A$ written per link. Only the common factor needs a central step.
- **Geometric programming.** Maximize $t$ subject to $t\, w_i (\sum_{j \ne i} G_{ij} p_j + \sigma_i) / (G_{ii} p_i) \le 1$ and the power limits. The constraints are posynomial, so in log variables the problem is convex and an interior-point method solves it (Chiang et al. 2007). This form also takes other constraints, such as a mix of max-min and fixed targets.

## Bounds

- **Upper bound by the noise-free case.** For every power limit, $t^* < 1/\rho(Z)$ when $\sigma > 0$ and $Z$ is irreducible, and $t^* \to 1/\rho(Z)$ as the power limit grows.
- **Upper bound by noise alone.** $t^* \le \min_i G_{ii} \bar p_i / (w_i \sigma_i)$ with per-link limits, and $t^* \le P / \sum_i v_i$ with a total limit, since interference only lowers the SINR.
- **Equal SINRs at the optimum.** If $Z$ is irreducible, every optimal $p$ has all weighted SINRs equal to $t^*$. Otherwise a link above $t^*$ could lower its power a little. This raises the SINR of each link it disturbs, and by irreducibility a chain of such steps raises the smallest SINR.
- **Exactness.** The eigenvalue and the bisection answers are exact up to the accuracy of the arithmetic; $L$ bisection steps give $t^*$ to within $2^{-L}$ times the start interval.

## Reductions

- **To fixed targets.** For a fixed $t$, deciding whether $t$ is reachable is the feasibility question of [Foschini-Miljanic power control](/foschini-miljanic-power-control/) with targets $t w_i$, plus a check of the least powers against the limit. So max-min is a one-parameter search over fixed-target problems.
- **To an eigenvalue problem.** With a total power limit, it reduces to the spectral radius of the positive matrix $A$, a [Perron-Frobenius](/perron-frobenius-theorem/) problem.
- **To a geometric program.** In the variables $\log p_i$ and $\log t$, it is a [geometric program](/geometric-programming/), hence a convex problem.
- **Relation to sum rate.** The max-min problem is solved in polynomial time, while [weighted sum rate maximization](/weighted-sum-rate-maximization/) on the same model is NP-hard in general.

## Applications

- **Fixed-rate services.** When all users get the same rate, for example voice in early CDMA systems, the best common SINR sets the largest rate that the cell can give to everyone, and the matching powers set the operating point.
- **Fairness.** Max-min fairness is the most egalitarian of the [fairness](/max-min-fairness/) criteria; it is used when no user may be left behind, at the cost of total throughput.
- **Admission control.** If $t^*$ is below the required target, no power allocation can serve all links, and some link must be dropped.
- **Cell planning.** $1/\rho(Z)$ is a quick measure of how much interference a frequency reuse pattern allows.

## References
