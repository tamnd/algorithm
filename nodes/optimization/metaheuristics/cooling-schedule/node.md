---
tag: 4GG9EQ
kind: concept
slug: cooling-schedule
name: Cooling schedule
aliases:
- annealing schedule
- temperature schedule
area: optimization/metaheuristics
level: core
summary: The rule that sets the temperature of simulated annealing at each step. Logarithmic schedules carry the convergence theorem; geometric and adaptive schedules are fast but have no guarantee.
prereqs: [simulated-annealing, metropolis-criterion]
see_also: [simulated-annealing-convergence, threshold-accepting, great-deluge-algorithm, stationary-distribution, mixing-time, intensification-and-diversification]
sources:
  - paper: doi:10.1287/moor.13.2.311
    title: Bruce Hajek, Cooling schedules for optimal annealing, Mathematics of Operations Research 13(2), 1988
    locator: pages 311 to 329 (Theorem 1 and the logarithmic schedule)
  - paper: doi:10.1126/science.220.4598.671
    title: Scott Kirkpatrick, C. Daniel Gelatt and Mario P. Vecchi, Optimization by simulated annealing, Science 220(4598), 1983
    locator: pages 671 to 680 (the geometric schedule with a fixed number of steps at each temperature)
  - paper: doi:10.1287/opre.37.6.865
    title: David S. Johnson, Cecilia R. Aragon, Lyle A. McGeoch and Catherine Schevon, Optimization by simulated annealing, an experimental evaluation, part I, graph partitioning, Operations Research 37(6), 1989
    locator: pages 865 to 892 (the choice of the start temperature from an acceptance rate, the steps per temperature and the stopping rule)
  - book: doi:10.1007/978-94-015-7744-1
    title: Peter J. M. van Laarhoven and Emile H. L. Aarts, Simulated Annealing, Theory and Applications, Reidel, 1987
    locator: the chapter on cooling schedules (the schedule of Aarts and van Laarhoven and its parameters)
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 2, Section 2.4, Simulated annealing (the design of the cooling schedule)
---

A cooling schedule is the rule that gives the temperature $T_k$ that [simulated annealing](/simulated-annealing/) uses at step $k$ in the [Metropolis criterion](/metropolis-criterion/). It has four parts: the start temperature, the rule that lowers it, the number of steps at each temperature, and the stopping rule. Only the logarithmic schedule $T_k = c/\ln(k+1)$ with $c$ at least the depth of the deepest trap carries a convergence theorem, [Hajek's theorem](/simulated-annealing-convergence/), and it is far too slow for practice. The geometric and adaptive schedules that people use have no such guarantee.

## In plain words

Simulated annealing needs a temperature at each step. A high temperature lets the search accept bad moves and roam. A low one makes it accept only good moves and settle down. The schedule is the plan that says how hot to start, how fast to cool, and when to stop.

There is a trade-off. Cool slowly and the search has time to escape from poor valleys, but it uses many steps. Cool fast and it finishes early, but it can freeze in a poor valley. The plan with a proof behind it cools so slowly that nobody can wait for it, so in practice people pick a fast plan and tune it on their problem.

## The idea

**The four parts.**

1. *Start temperature $T_0$.* Pick it so that a fraction $\chi_0$ of the worse moves is accepted at the start, often $\chi_0 = 0.8$. With $\bar\Delta^+$ the mean increase of the worse moves in a short trial run, this gives about $T_0 = -\bar\Delta^+/\ln \chi_0$.
2. *Decrement rule.* How $T$ goes down, see the table below.
3. *Steps per temperature $L$.* Stay at each temperature for $L$ steps, often a small multiple of the size of a neighborhood, so that the walk comes close to the equilibrium distribution at that temperature.
4. *Stopping rule.* Stop when the fraction of accepted moves stays below a small value, for example 2 percent, for several temperatures in a row (the system is *frozen*), or when the budget of steps is used.

**Common decrement rules.**

| name | rule | guarantee |
|---|---|---|
| logarithmic | $T_k = c/\ln(k+1)$ | converges in probability to the global minima if and only if $c \ge d^*$ (Hajek 1988) |
| geometric | $T_{j+1} = \alpha T_j$, $0.8 \le \alpha \le 0.99$, $L$ steps at each $T_j$ | none |
| linear | $T_{j+1} = T_j - \eta$ | none |
| Lundy and Mees | $T_{j+1} = T_j/(1 + \beta T_j)$, so $1/T_j = 1/T_0 + \beta j$ | none for a fixed $\beta$ |
| Aarts and van Laarhoven | $T_{j+1} = T_j / \left(1 + T_j \ln(1 + \delta)/(3\sigma_j)\right)$, with $\sigma_j$ the standard deviation of $f$ observed at $T_j$ | none; designed to keep the walk near equilibrium |

Here $d^*$ is the largest depth of a local minimum that is not global: the smallest climb that leads from it to a lower state. The logarithmic rule is the only one with a theorem, and the theorem says nothing about a finite number of steps.

**Why the theory asks for so slow a schedule.** At a fixed temperature $T$, the walk is a [Markov chain](/markov-chain/) whose [stationary distribution](/stationary-distribution/) is the Boltzmann distribution $\pi_T(x) \propto e^{-f(x)/T}$, and as $T \to 0$ this distribution concentrates on the global minima. A schedule that lowers $T$ slowly keeps the walk close to $\pi_T$. But to leave a trap of depth $d$, the walk needs about $e^{d/T}$ steps at temperature $T$. A schedule that lowers $T$ faster than this rate can leave the walk in a trap forever. The border is exactly where $\sum_k e^{-d^*/T_k}$ diverges, and for the schedules $c/\ln(k+1)$ this is $c = d^*$.

**What fast schedules lose.** With a budget of $K$ steps, the logarithmic schedule never gets cold: after $10^9$ steps, $T = 4/\ln(10^9 + 1) = 0.193$. A geometric schedule reaches any temperature in a number of steps that grows only with $\ln(T_0/T)$. So for a finite budget, practice prefers fast schedules, and gives up the guarantee. Then the result must be reported as measured.

**Equivalent views.** Multiplying $f$ by $a > 0$ is the same as multiplying every temperature by $1/a$, so a schedule is only meaningful in the units of $f$. Rules that adapt $T$ to the observed spread $\sigma$ of $f$, as Aarts and van Laarhoven do, remove this unit.

## Examples

**The start temperature.** On the 8-state cycle of the [simulated annealing](/simulated-annealing/) page, with $f = (3, 1, 4, 2, 5, 0, 3, 6)$, the 8 uphill moves have increases $3, 2, 3, 2, 3, 5, 3, 3$, with mean $\bar\Delta^+ = 3$. For $\chi_0 = 0.8$, the rule gives $T_0 = -3/\ln 0.8 = 13.44$. For $\chi_0 = 0.5$ it gives $T_0 = 4.33$.

**How fast each schedule gets cold.**

| schedule | $T$ after $10^3$ steps | $T$ after $10^6$ steps | steps to reach $T = 0.5$ |
|---|---|---|---|
| $4/\ln(k+1)$ | 0.579 | 0.290 | $e^{8} - 1 \approx 2980$ |
| $5 \cdot 0.99^{k-1}$ | $2.2 \times 10^{-4}$ | far below any useful value | 231 |

The logarithmic schedule needs $e^{40} - 1 \approx 2.4 \times 10^{17}$ steps to reach $T = 0.1$, while the geometric one needs 391.

**Measured effect on the cycle.** From the start state 0, over 100 runs (seeds 0 to 99), the geometric schedule $5 \cdot 0.99^{k-1}$ with 1000 steps saw the global minimum in 99 runs, and the geometric schedule $2 \cdot 0.9^{k-1}$ with 60 steps in 8 runs. The theorem page gives the exact probabilities for the logarithmic schedules with $c = 1, 2, 4, 8$: with $c = 1$ and $c = 2$, below the depth $d^* = 4$, the probability of the global minimum stays near 0.04 and 0.14 forever.

**A non-example of a schedule.** A constant temperature is not a cooling schedule. At a fixed $T$ the walk samples $\pi_T$, which gives every state positive mass, so the probability that the current state is a global minimum tends to $\pi_T(S^*) < 1$ (on the cycle at $T = 1$, it is 0.613). The best state seen still improves over time.

## Where it is used

- **Simulated annealing** on placement, routing, the [traveling salesman problem](/traveling-salesman-problem/), [graph partitioning](/graph-partitioning-problem/) and timetabling, with a geometric or adaptive schedule.
- **[Threshold accepting](/threshold-accepting/)** uses a schedule of thresholds instead of temperatures, and the **[great deluge algorithm](/great-deluge-algorithm/)** a falling water level. The same trade-off between speed and quality holds.
- **Sampling.** Annealed importance sampling and parallel tempering use a ladder of temperatures to move between the modes of a distribution, see [Metropolis-Hastings](/metropolis-hastings/).
- **Exploration in other methods.** The temperature of a softmax choice, as in some bandit and reinforcement learning methods, is often lowered by a schedule of the same shapes. This is the balance of [intensification and diversification](/intensification-and-diversification/).

## References
