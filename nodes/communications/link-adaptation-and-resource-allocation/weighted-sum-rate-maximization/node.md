---
tag: J1XDTK
kind: problem
slug: weighted-sum-rate-maximization
name: Weighted sum rate maximization
aliases:
- WSR maximization
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Choose powers or precoders to maximize a weighted sum of user rates under interference. Nonconvex and NP-hard in general; WMMSE and successive convex methods find stationary points."
prereqs: [water-filling-power-allocation, np-hard]
see_also: [weighted-mmse-precoding, geometric-programming-power-control, energy-efficient-power-allocation, max-min-sinr-power-control, ofdma-resource-allocation, proportional-fair-scheduling, network-utility-maximization, interference-alignment]
sources:
  - paper: doi:10.1109/JSTSP.2007.914876
    title: "Zhi-Quan Luo and Shuzhong Zhang, Dynamic spectrum management: complexity and duality, IEEE Journal of Selected Topics in Signal Processing 2(1), 2008, pages 57 to 73"
    locator: "the complexity of sum rate maximization over the multiuser interference channel with many subcarriers (NP-hard for a fixed number of users, strongly NP-hard for one subcarrier and many users), and the dual method for many subcarriers"
  - paper: doi:10.1109/TSP.2011.2147784
    title: "Qingjiang Shi, Meisam Razaviyayn, Zhi-Quan Luo and Chen He, An iteratively weighted MMSE approach to distributed sum-utility maximization for a MIMO interfering broadcast channel, IEEE Transactions on Signal Processing 59(9), 2011, pages 4331 to 4340"
    locator: "the equivalence of weighted sum rate maximization and a weighted MSE minimization, and the block coordinate descent (WMMSE) that converges to a stationary point"
  - paper: doi:10.1109/TWC.2007.05960
    title: "Mung Chiang, Chee Wei Tan, Daniel P. Palomar, Daniel O'Neill and David Julian, Power control by geometric programming, IEEE Transactions on Wireless Communications 6(7), 2007, pages 2640 to 2651"
    locator: "sum rate power control as a geometric program at high SINR and by a series of geometric programs in general"
---

Weighted sum rate maximization (WSR) is the problem of choosing the transmit powers, and with antennas the beamformers, of interfering links so that $\sum_k w_k R_k$, a weighted sum of their Shannon rates, is as large as possible. With one link it is [water-filling](/water-filling-power-allocation/); with several links that treat each other as noise it is nonconvex and NP-hard, and practical methods find stationary points. The standard such method is the weighted MMSE iteration, which the page on [weighted MMSE precoding](/weighted-mmse-precoding/) describes for MIMO; the series of geometric programs in [power control by geometric programming](/geometric-programming-power-control/) is another. When the objective is bits per joule instead of bits per second, the problem becomes [energy-efficient power allocation](/energy-efficient-power-allocation/). WSR is also the inner step of a scheduler: [proportional fair scheduling](/proportional-fair-scheduling/) and [network utility maximization](/network-utility-maximization/) solve one WSR problem per slot, with weights from the past rates or the queue lengths.

## In plain words

Several transmitters send at the same time on the same band. Each one adds data for its own receiver and noise for all the others. Every user has a weight that says how much its data is worth now. We want to set the powers so that the total worth of the data sent is as large as possible. If the users barely disturb each other, everyone should transmit at full power. If they disturb each other a lot, it is often better that some stay silent. In between, the best answer can be a careful mix. Finding the true best answer for many users is very hard in general, so practical methods improve a guess step by step until no small change helps.

## Definition

**Input.** $K$ links, with power gains $G_{kj} \ge 0$ from transmitter $j$ to receiver $k$ and $G_{kk} > 0$, noise powers $\sigma_k > 0$, power limits $\bar p_k$ (or a total limit), and weights $w_k \ge 0$.

**Problem (single carrier).** Find $0 \le p_k \le \bar p_k$ that maximize

$$U(p) = \sum_{k=1}^K w_k \log_2\!\left(1 + \frac{G_{kk}\, p_k}{\sum_{j \ne k} G_{kj}\, p_j + \sigma_k}\right).$$

Each receiver treats interference as Gaussian noise, so the rates are those of the [Shannon-Hartley](/shannon-hartley-theorem/) formula with the interference added to the noise. Rates are in bits per channel use.

**Multicarrier form.** With $N$ subcarriers, gains $G_{kj}^{(n)}$ and powers $p_k^{(n)}$, maximize $\sum_k w_k \sum_n \log_2(1 + \mathrm{SINR}_k^{(n)})$ subject to $\sum_n p_k^{(n)} \le \bar p_k$ for each $k$.

**MIMO form.** Transmitter $j$ sends with precoders $V_j$, and the rate of link $k$ is $\log_2 \det(I + H_{kk} V_k V_k^H H_{kk}^H C_k^{-1})$ with the interference plus noise covariance $C_k$. The scalar case is $V_k = \sqrt{p_k}$.

**Output.** The powers (or precoders) and the value $U$.

## Variants

- **Sum rate.** All $w_k = 1$. This maximizes throughput and ignores fairness.
- **Weights from a scheduler.** With $w_k = 1/\bar R_k$, where $\bar R_k$ is a running average of the rate of user $k$, one WSR problem per slot is the step of proportional fair scheduling. With $w_k$ equal to queue lengths it is the max-weight rule, which keeps the queues stable whenever any policy can.
- **Treating interference as noise or not.** The definition fixes single-user decoding. With [successive interference cancellation](/successive-interference-cancellation/) or [dirty paper coding](/dirty-paper-coding/), the WSR over the capacity region of a broadcast channel is a convex problem, solved through the duality between the broadcast and the multiple-access channel.
- **Binary power control.** Each link transmits at $\bar p_k$ or stays silent. For two links and equal weights, the best powers are always of this form (Gjendemsjø et al. 2008), and for many links it is a good heuristic.
- **Minimum rates.** Add $R_k \ge r_k$, that is $\mathrm{SINR}_k \ge 2^{r_k} - 1$, which is a linear constraint in $p$.

## Examples

**Two links, equal weights.** Let $G_{11} = G_{22} = 1$, $\sigma_k = 0.1$ and $\bar p_k = 1$.

| Cross gains $(G_{12}, G_{21})$ | both on | only link 1 | only link 2 |
|---|---|---|---|
| $(0.1, 0.15)$ | $\log_2 6 + \log_2 5 = 4.907$ | $\log_2 11 = 3.459$ | $3.459$ |
| $(0.8, 0.9)$ | $\log_2 2.111 + \log_2 2 = 2.078$ | $3.459$ | $3.459$ |

With weak coupling both links should transmit at full power; with strong coupling one link should be silent. The second case also shows that $U$ is not concave: it takes the value $3.459$ at $(1, 0)$ and at $(0, 1)$, but only $2.078$ at $(1, 1)$, and only $\log_2(1 + 0.5/0.5) + \log_2(1 + 0.5/0.55) = 1.933$ at the midpoint $(0.5, 0.5)$.

**Weights change the answer.** For the strongly coupled pair with $w = (1, 3)$, the best choice is link 2 alone, $3 \log_2 11 = 10.378$, against $4.078$ with both on.

**An interior optimum.** Let $G = \begin{pmatrix} 1 & 0.2 \\ 0.05 & 1 \end{pmatrix}$, $\sigma_k = 0.4$, $\bar p_k = 1$ and $w = (1, 0.2)$. The three binary choices give $1.7526$ (both on), $1.8074$ (link 1 alone) and $0.3615$ (link 2 alone). The optimum is $p = (1, 0.17376)$ with $U = 1.81675$: link 2 sends with a little power, where its gain in rate still outweighs the harm to link 1. The WMMSE iteration from full power gives $p_2 = 0.745$, $0.561$, $0.435$ after 1, 2 and 3 steps, $0.197$ after 10 and $0.17376$ after 60, with $U$ rising at each step.

## Known algorithms

- **One link: water-filling.** For $K = 1$, the multicarrier problem is concave and [water-filling](/water-filling-power-allocation/) solves it in $O(N \log N)$ time.
- **WMMSE.** Shi, Razaviyayn, Luo and He showed that WSR is equivalent to minimizing a weighted sum of mean squared errors over the transmit filters, the receive filters and the MSE weights. Block coordinate descent over these three groups has a closed form for each block, raises $U$ at each step, and converges to a stationary point. For the scalar case the three steps are: $u_k = \sqrt{G_{kk}}\, v_k / (\sum_j G_{kj} v_j^2 + \sigma_k)$, $\omega_k = 1/(1 - u_k \sqrt{G_{kk}}\, v_k)$, and $v_k = \min\big(\sqrt{\bar p_k},\, w_k \omega_k u_k \sqrt{G_{kk}} / \sum_j w_j \omega_j u_j^2 G_{jk}\big)$, with $p_k = v_k^2$. See [weighted MMSE precoding](/weighted-mmse-precoding/).
- **Successive convex approximation.** Replace the nonconvex part by a convex bound that is tight at the current point, and repeat; the series of geometric programs of [power control by geometric programming](/geometric-programming-power-control/) is one such method, and the [fractional programming](/fractional-programming/) transforms give others. Each converges to a stationary point.
- **Dual methods for many subcarriers.** For the multicarrier form, Lagrangian relaxation of the power limits splits the problem into one small problem per subcarrier. The duality gap goes to zero as the subcarriers become many and narrow, so the dual method is close to optimal for OFDM systems with many subcarriers (Yu and Lui 2006; Luo and Zhang 2008).
- **Global methods.** $U$ is a difference of two increasing functions of $p$, so monotonic optimization with branch and bound (polyblock algorithms) finds the global optimum, at a cost that grows exponentially with $K$. These methods are used as benchmarks for small $K$.
- **Exhaustive search over on and off sets.** For small $K$, try all $2^K$ choices of active links at full power; for two links with equal weights this is exact.

## Bounds

**Complexity (Luo and Zhang 2008).** For the multicarrier form with treating interference as noise:

| Case | Sum rate |
|---|---|
| $K = 1$, any $N$ | concave, water-filling |
| fixed $K \ge 2$, $N$ part of the input | NP-hard |
| $N = 1$, $K$ part of the input | strongly NP-hard |

For one subcarrier, the max-min rate version is a linear program in the powers for each fixed target, and so is solved in polynomial time, which is the contrast with [max-min SINR power control](/max-min-sinr-power-control/). With a fixed number of subcarriers $N \ge 3$ and many users, the max-min version is also strongly NP-hard, and Liu (2017) extended this to $N = 2$. So no polynomial-time algorithm solves WSR in general unless P = NP.

**Upper bounds.** $U(p) \le \sum_k w_k \log_2(1 + G_{kk} \bar p_k / \sigma_k)$, the value without interference. A tighter bound comes from the dual function in the multicarrier form.

**Stationary points.** WMMSE and successive convex approximation reach stationary points, which can be far from optimal; the example in [power control by geometric programming](/geometric-programming-power-control/) has two stationary points with sum rates $2.8435$ and $2.8502$.

## Reductions

- **From hard combinatorial problems.** Luo and Zhang prove the hardness results by polynomial reductions from classical NP-complete problems; the hard instances force each link to choose between full power and silence, which is a combinatorial choice.
- **To weighted MSE.** WSR is equivalent to a weighted MMSE problem with extra variables, which is convex in each block (Shi et al. 2011).
- **To a geometric program.** At high SINR, $\log(1 + \mathrm{SINR}) \approx \log \mathrm{SINR}$, and WSR becomes a geometric program in log powers, solved to global optimality.
- **As a step of utility maximization.** For a concave utility $\sum_k u(\bar R_k)$ of long-run average rates, a gradient step solves WSR with $w_k = u'(\bar R_k)$ in each slot. This is how WSR solvers become schedulers.

## Applications

- **Coordinated multipoint and interference coordination.** Base stations that share channel state choose their powers and beams jointly by WSR, with the weights set by the scheduler.
- **Multicarrier digital subscriber lines.** Dynamic spectrum management in DSL is the multicarrier form of WSR, with crosstalk between the lines as the interference; the dual methods were developed there.
- **Cellular downlink scheduling.** With proportional fair weights, a WSR solver per slot decides which users are served and with which beams; see [OFDMA resource allocation](/ofdma-resource-allocation/) for the orthogonal case.
- **Benchmarks.** The WSR region traced by varying the weights shows the trade-off between the users' rates.

## References
