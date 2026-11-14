---
tag: FXC7EF
kind: definition
slug: switching-activity
name: Switching activity
aliases:
- toggle rate
- activity factor
area: eda/power-reliability-and-manufacturability
level: intro
summary: The expected number of transitions of a signal per clock cycle, the main unknown in estimating the dynamic power of a circuit.
prereqs: [dynamic-power-dissipation]
see_also: [signal-probability-propagation, transition-density, glitch-power, bdd-switching-activity-estimation, monte-carlo-power-estimation, bus-invert-coding, gray-code, stationary-process]
sources:
  - paper: doi:10.1109/4.126534
    title: Anantha P. Chandrakasan, Samuel Sheng and Robert W. Brodersen, Low-power CMOS digital design, IEEE Journal of Solid-State Circuits 27(4), 473 to 484, April 1992
    locator: the section on the sources of power dissipation, with the activity factor of rising transitions and its dependence on signal statistics and logic style
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the definitions of signal probability and of transition activity, and the overview of the methods that estimate them
  - paper: doi:10.1109/DAC.1992.227826
    title: Abhijit Ghosh, Srinivas Devadas, Kurt Keutzer and Jacob White, Estimation of average switching activity in combinational and sequential circuits, Proceedings of the 29th ACM/IEEE Design Automation Conference, 253 to 259, 1992
    locator: the definition of the average switching activity of a gate over pairs of consecutive input vectors
---

The switching activity of a node in a synchronous digital circuit is the expected number of its transitions per clock cycle. It is the factor $\alpha$ of the [dynamic power](/dynamic-power-dissipation/) $\alpha C V_{DD}^2 f$, and the one factor that depends on what the circuit computes: capacitance, voltage and frequency are known from the design, while the activity depends on the input data and on the logic. Two conventions exist. The *rising activity* $\alpha_{0 \to 1}$ counts only transitions from 0 to 1, which are the ones that draw charge from the supply, and the *toggle rate* counts all transitions. Both include glitches, the extra transitions within a cycle, unless the zero-delay model is assumed. This page defines the measure; [signal probability propagation](/signal-probability-propagation/), [transition density](/transition-density/), [BDD-based estimation](/bdd-switching-activity-estimation/) and [Monte Carlo estimation](/monte-carlo-power-estimation/) are methods that compute or estimate it.

## Definition

Let $y$ be a node of a circuit clocked at frequency $f$, and let $R_k$ and $F_k$ be the numbers of rising and falling transitions of $y$ during clock cycle $k$, as random variables of the input data.

**Switching activity.** The rising activity and the toggle rate of $y$ are

$$ \alpha_{0 \to 1}(y) \;=\; \lim_{K \to \infty} \frac{1}{K} \sum_{k=1}^{K} E[R_k], \qquad \alpha(y) \;=\; \lim_{K \to \infty} \frac{1}{K} \sum_{k=1}^{K} E[R_k + F_k], $$

when the limits exist. They are numbers of transitions per cycle, not probabilities: a node with glitches can have $\alpha(y) > 1$.

**Zero-delay activity.** Under the zero-delay model each node takes one value per cycle, $y_k$, and changes at most once per cycle. If the sequence $(y_k)$ is [stationary](/stationary-process/), then

$$ \alpha(y) \;=\; P(y_k \ne y_{k+1}), \qquad \alpha_{0 \to 1}(y) \;=\; P(y_k = 0,\ y_{k+1} = 1). $$

**Fact 1 (rising is half of all).** For a stationary zero-delay sequence, $\alpha_{0 \to 1}(y) = \alpha_{1 \to 0}(y) = \alpha(y) / 2$.

*Proof.* Stationarity gives $P(y_{k+1} = 1) = P(y_k = 1)$. The left side is $P(y_k = 0, y_{k+1} = 1) + P(y_k = 1, y_{k+1} = 1)$ and the right side is $P(y_k = 1, y_{k+1} = 0) + P(y_k = 1, y_{k+1} = 1)$, so the two transition probabilities are equal, and each is half of $P(y_k \ne y_{k+1})$. $\square$

The same holds with glitches in the long run, since rising and falling transitions alternate. So $P_{\mathrm{dyn}} = \alpha_{0 \to 1} C V_{DD}^2 f = \frac{1}{2} \alpha\, C V_{DD}^2 f$, and the two conventions differ by a factor of 2.

**Fact 2 (activity, probability and correlation).** For a stationary zero-delay sequence with $p = P(y_k = 1) \in (0, 1)$ and lag-one correlation coefficient $\rho$ between $y_k$ and $y_{k+1}$,

$$ \alpha(y) \;=\; 2\, p\, (1 - p)\, (1 - \rho). $$

*Proof.* For 0-1 values, $[y_k \ne y_{k+1}] = (y_k - y_{k+1})^2$. Its expectation is $\mathrm{Var}(y_k) + \mathrm{Var}(y_{k+1}) - 2\, \mathrm{Cov}(y_k, y_{k+1}) = 2 p (1 - p) - 2 \rho\, p (1 - p)$, using that the two means are equal. $\square$

So the activity depends on the signal probability $p$ and also on how the signal is correlated in time. For temporally independent values ($\rho = 0$) it is $2 p (1 - p)$, at most $1/2$. A signal that alternates every cycle has $\rho = -1$ and $\alpha = 1$; a constant signal or one that changes very rarely has $\rho$ near 1 and $\alpha$ near 0.

## Examples and non-examples

**A random bit.** A fresh fair bit each cycle has $p = 1/2$ and $\rho = 0$, so $\alpha = 1/2$ and $\alpha_{0 \to 1} = 1/4$.

**An AND gate.** With two fresh fair inputs, $P(y = 1) = 1/4$, and values in different cycles are independent, so $\alpha = 2 \cdot \frac{1}{4} \cdot \frac{3}{4} = 3/8$ and $\alpha_{0 \to 1} = 3/16$. The gate is less active than its inputs because its output is mostly 0.

**A binary counter.** Bit $k$ of a counter that increments every cycle toggles once every $2^k$ cycles, so $\alpha = 2^{-k}$ and $\alpha_{0 \to 1} = 2^{-(k+1)}$. The bits together toggle $\sum_{k=0}^{m-1} 2^{-k} < 2$ times per cycle. A [Gray code](/gray-code/) counter toggles exactly one bit per step, so its total activity is 1. Here the activity of each bit is far from $2 p (1 - p)$: bit 0 has $p = 1/2$ and $\alpha = 1$, because it alternates.

**A clock.** A clock rises and falls once per cycle, so $\alpha = 2$ and $\alpha_{0 \to 1} = 1$. It is the most active net of a design, and clock power is often a large part of the total.

**A glitch.** For $y = \mathrm{AND}(a, \bar a)$ with a delay on the inverter, $y$ is always 0 under zero delay, so its zero-delay activity is 0. With the delay, each rising edge of $a$ makes a short pulse on $y$, two transitions, so the true activity is that of the rising edges of $a$. Glitches are part of the activity and of the power; see [glitch power](/glitch-power/).

**Non-example: signal probability.** $P(y = 1)$ alone does not fix the activity. A node with $P(y = 1) = 1/2$ can switch every cycle ($\rho = -1$, $\alpha = 1$) or almost never ($\rho$ near 1).

**Non-example: toggle coverage.** In verification, toggle coverage records whether each bit went from 0 to 1 and back at least once in a test. It is a yes or no measure of test quality, not a rate, and says nothing about power.

**Non-example: transition density.** The [transition density](/transition-density/) of a signal is its mean number of transitions per second, a rate in continuous time. In a synchronous circuit it is the activity times the clock frequency, but it is defined also for signals without a clock.

## Related definitions

- **Signal probability.** $P(y = 1)$, the fraction of cycles in which the node is 1; [signal probability propagation](/signal-probability-propagation/) computes it. With temporally independent inputs and zero delay it gives the activity by Fact 2.
- **Transition density.** The continuous-time rate of transitions, with Najm's propagation rule; see [transition density](/transition-density/).
- **Glitch activity.** The part of $\alpha$ beyond the zero-delay activity; see [glitch power](/glitch-power/).
- **Hamming distance.** For a bus, the number of bits that change between consecutive words is the [Hamming distance](/hamming-distance/) between them, and its mean is the sum of the bit activities. [Bus-invert coding](/bus-invert-coding/) lowers it.
- **Effective capacitance.** $\sum_y \alpha_{0 \to 1}(y) C_y$, the switched capacitance per cycle, which multiplied by $V_{DD}^2 f$ gives the dynamic power.

## References
