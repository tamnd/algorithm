---
tag: 40W505
kind: problem
slug: energy-efficient-power-allocation
name: Energy-efficient power allocation
aliases:
- energy efficiency maximization
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Choose powers to maximize bits per joule, rate over total consumed power including circuit power. A fractional program: Dinkelbach's method solves it exactly when the rate is concave."
prereqs: [water-filling-power-allocation, fractional-programming]
see_also: [dinkelbach-algorithm, fractional-programming, weighted-sum-rate-maximization, water-filling-power-allocation, geometric-programming-power-control, energy-per-bit-to-noise-density-ratio, spectral-efficiency, quasiconvex-function]
sources:
  - paper: doi:10.1561/0100000088
    title: "Alessio Zappone and Eduard Jorswieck, Energy efficiency in wireless networks via fractional programming theory, Foundations and Trends in Communications and Information Theory 11(3-4), 2015, pages 185 to 396"
    locator: "the definition of energy efficiency with circuit power, pseudoconcavity of a concave rate over an affine power, Dinkelbach's algorithm and its convergence, and the global, sum and minimum energy efficiency of interference networks solved by sequential fractional programming"
  - paper: doi:10.1287/mnsc.13.7.492
    title: "Werner Dinkelbach, On nonlinear fractional programming, Management Science 13(7), 1967, pages 492 to 498"
    locator: "the parametric problem max f(x) - q g(x), the root of its optimal value as the optimal ratio, and the iteration that updates q"
  - book: isbn:9780521833783
    title: "Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004"
    locator: "Section 3.4 (quasiconvex functions) and Section 4.2.5 (quasiconvex optimization by bisection)"
---

Energy-efficient power allocation is the problem of choosing transmit powers to maximize energy efficiency (EE): the number of bits delivered per joule of consumed energy, that is, a rate divided by a total power that includes a fixed circuit power. Unlike [weighted sum rate maximization](/weighted-sum-rate-maximization/), which spends all available power when interference is weak, EE maximization stops at the power where one more watt adds fewer bits than it costs, often well below the limit. The objective is a ratio, so the problem is a [fractional program](/fractional-programming/). For one link or for orthogonal channels, the rate is concave and the power affine, the ratio is pseudoconcave, and [Dinkelbach's algorithm](/dinkelbach-algorithm/) finds the global optimum by solving a short series of concave problems, each a form of [water-filling](/water-filling-power-allocation/). With interference between links, the problem is as hard as sum rate maximization, and the inner problems are solved by the successive convex methods of [power control by geometric programming](/geometric-programming-power-control/).

## In plain words

A radio uses energy in two ways: the power it sends into the air, and a fixed amount that its circuits need just to be on. Sending more power gives more bits each second, but each extra watt gives fewer extra bits than the one before. If we care about bits per unit of energy, sending with very little power is wasteful, because the fixed cost is paid while few bits go out. Sending at full power is also wasteful, because the last watts add almost nothing. The best choice is in between: increase the power while one more watt still pays for itself in bits, and stop there. The standard method guesses an efficiency, finds the best trade for that guess, updates the guess from the result, and is done in a few rounds.

## Definition

**Single link.** A link has bandwidth $B$, channel gain over noise $g > 0$ (the SNR per watt of transmit power), a power limit $\bar p$, a power amplifier efficiency $\eta \in (0, 1]$ and a circuit power $P_c > 0$. Maximize

$$\mathrm{EE}(p) = \frac{R(p)}{P(p)} = \frac{B \log_2(1 + g\, p)}{P_c + p/\eta} \quad \text{bits per joule}, \qquad 0 \le p \le \bar p.$$

**Many channels without interference.** Subcarriers or links $i = 1, \ldots, N$ with gains $g_i$: $R(p) = B \sum_i \log_2(1 + g_i p_i)$, $P(p) = P_c + \sum_i p_i / \eta$, subject to $\sum_i p_i \le \bar p$ and $p \ge 0$. The numerator is concave and the denominator affine.

**Interference networks.** $K$ links with SINRs as in [weighted sum rate maximization](/weighted-sum-rate-maximization/). Common objectives are the global energy efficiency (GEE) $\sum_k R_k / \sum_k P_k$, the sum of the links' own efficiencies $\sum_k R_k / P_k$, their weighted product, and the smallest efficiency $\min_k R_k / P_k$.

**Output.** The powers and the efficiency.

## Variants

- **Minimum rates.** Add $R_k \ge r_k$, so that energy is not saved by sending nothing; with the targets met, the problem trades the remaining power against efficiency.
- **Energy per bit.** Minimizing $P/R$, joules per bit, is the same problem. With $P_c = 0$ and $\eta = 1$, the infimum over $p$ is reached as $p \to 0$, and equals $\ln 2 / (B g)$ joules per bit, the limit $E_b / N_0 = \ln 2$ ($-1.59$ dB) of the [energy per bit](/energy-per-bit-to-noise-density-ratio/).
- **Trade-off with spectral efficiency.** Maximizing $R$ subject to $\mathrm{EE} \ge e$, or the reverse, traces the trade-off between [spectral efficiency](/spectral-efficiency/) and energy efficiency; for one link the curve rises up to the EE optimum and then falls.
- **Load-dependent circuit power.** Models where $P_c$ grows with the rate, or with the number of active antennas or subcarriers, keep the fractional form but may add integer choices.
- **Many antennas.** In massive MIMO, the number of antennas, users and the transmit power are chosen together; the circuit power per antenna then limits how many antennas pay off.

## Examples

**One link.** Let $B = 1$ MHz, $g = 10$ per watt, $\eta = 1$, $P_c = 1$ W and $\bar p = 10$ W. At full power the rate is $\log_2 101 = 6.658$ Mbit/s and $\mathrm{EE} = 6.658 / 11 = 0.605$ Mbit/J. Dinkelbach's method from $q_0 = 0$ (in Mbit/J):

| $n$ | $q_n$ | $p_n$ (W) | $F(q_n)$ |
|---|---|---|---|
| 0 | 0 | 10 | 6.6582 |
| 1 | 0.605292 | 2.28347 | 2.58753 |
| 2 | 1.393341 | 0.935422 | 0.67545 |
| 3 | 1.742332 | 0.728025 | 0.038882 |
| 4 | 1.764832 | 0.717469 | 0.000119 |
| 5 | 1.764902 | 0.717436 | 0 |

Here $p_n$ maximizes $R(p) - q_n P(p)$, which gives $p_n = \min\big(\bar p, \max(0, 1/(q_n \ln 2) - 1/g)\big)$ with rates in Mbit/s, and $F(q_n) = R(p_n) - q_n P(p_n)$. The optimum is $p^* = 0.7174$ W, with rate $3.031$ Mbit/s and $\mathrm{EE}^* = 1.7649$ Mbit/J: half the rate of full power at three times the efficiency. The convergence is superlinear: the value of $F$ drops by factors of 2.6, 3.8, 17 and 330.

**A closed form for one link.** With $\eta = 1$ and $g P_c > 1$, setting the derivative of $\mathrm{EE}$ to zero gives $\ln x = 1 + (g P_c - 1)/x$ for $x = 1 + g p$, whose root is $x = (g P_c - 1) / W\big((g P_c - 1)/e\big)$, with $W$ the Lambert W function. For the example, $W(9/e) = 1.1010$, $x = 8.1744$ and $p^* = 0.7174$ W, as found above. The optimum is $\min(\bar p, p^*)$, since $\mathrm{EE}$ is unimodal.

**Many subcarriers.** The inner problem of Dinkelbach's method, maximize $\sum_i \log_2(1 + g_i p_i) - q \sum_i p_i$, is water-filling with the fixed water level $\mu = 1/(q \ln 2)$: $p_i = \max(0, \mu - 1/g_i)$. If these powers sum to more than $\bar p$, the budget binds, and the inner answer is ordinary water-filling with the budget $\bar p$. When the budget does not bind, EE water-filling uses a lower level than rate water-filling, and turns off weak subcarriers sooner.

## Known algorithms

- **Dinkelbach's algorithm.** Let $F(q) = \max_p \{R(p) - q P(p)\}$. $F$ is convex and strictly decreasing in $q$, and its root is the optimal efficiency. Starting from $q_0 = 0$ or any feasible ratio, set $p_n = \arg\max_p \{R(p) - q_n P(p)\}$ and $q_{n+1} = R(p_n)/P(p_n)$. The ratios increase and converge superlinearly to the optimum. When $R$ is concave and $P$ is affine, each inner problem is concave. See [Dinkelbach's algorithm](/dinkelbach-algorithm/).
- **Bisection.** For each $q$, the condition $F(q) \ge 0$ says whether efficiency $q$ is reachable, so a [bisection](/bisection-method/) on $q$ also works, as for any quasiconcave problem; it converges linearly.
- **Charnes-Cooper transform.** With $R$ concave and $P$ affine, the substitution $t = 1/P(p)$, $x = t p$ turns the ratio into a concave problem in $(x, t)$, solved in one convex program.
- **Sequential fractional programming.** For interference networks, the rate is not concave. Zappone and Jorswieck combine Dinkelbach's method with successive lower bounds on the rate, so that each inner problem is concave; the method converges to a KKT point. Global optima need branch and bound or monotonic optimization, with a cost exponential in $K$.
- **Closed forms.** For one link, the Lambert W formula above; for orthogonal channels, EE water-filling with a search on the level.

## Bounds

- **Pseudoconcavity.** If $R$ is concave and differentiable and $P$ is affine and positive, $R/P$ is pseudoconcave: every stationary point is a global maximizer, and the superlevel sets are convex. So the single-link and orthogonal cases have no spurious local optima.
- **Unimodality.** For one link, $\mathrm{EE}(p)$ rises up to $p^*$ and then falls, so $\min(\bar p, p^*)$ is optimal.
- **The limit without circuit power.** With $P_c = 0$, $\mathrm{EE}(p) \le \eta B g / \ln 2$, reached only as $p \to 0$, where the rate also goes to $0$. A positive $P_c$ is what makes the problem well posed.
- **Interference.** With interference between links, the rate is not concave in the powers, the ratio is not pseudoconcave, and local optima that are not global can exist. Known global methods take time exponential in $K$.

## Reductions

- **To a parametric concave problem.** Dinkelbach's method reduces the ratio to the root of $F(q)$, each evaluation of which is a concave problem for concave $R$.
- **To water-filling.** For orthogonal channels, each evaluation of $F(q)$ is water-filling with a level fixed by $q$, as in the example.
- **To weighted sum rate.** For interference networks, each evaluation of $F(q)$ is a sum rate problem with a linear power penalty, so the methods for [weighted sum rate maximization](/weighted-sum-rate-maximization/) apply, including the series of geometric programs.

## Applications

- **Battery-powered devices.** Sensors and handsets choose the power that sends the most bits per joule when delay allows.
- **Base station design.** In networks where circuit and cooling power are a large part of the total, EE criteria decide how many antennas, carriers and cells are active at each load.
- **Green networks.** Operators report bits per joule as a measure of network efficiency, and EE-optimal schedulers switch off carriers at low load.
- **Link adaptation.** With [adaptive modulation](/adaptive-modulation/), the EE optimum tells which rate to use when the goal is battery life rather than throughput.

## References
