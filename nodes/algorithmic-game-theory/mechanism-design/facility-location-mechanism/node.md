---
tag: N3EWMC
kind: problem
slug: facility-location-mechanism
name: Strategyproof facility location
aliases:
- approximate mechanism design without money
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "Place a facility from reported agent locations, without payments, so that no agent gains by lying, while approximating the total or the maximum distance."
prereqs: [approximation-ratio, dominant-strategy-incentive-compatibility]
see_also: [generalized-median-voter-rule, median-voter-theorem, single-peaked-preferences, facility-location-problem, k-median-problem, gibbard-satterthwaite-theorem, truthful-in-expectation, median]
sources:
  - paper: doi:10.1145/2542174.2542175
    title: "Ariel D. Procaccia and Moshe Tennenholtz, Approximate mechanism design without money, ACM Transactions on Economics and Computation 1(4) (2013), Article 18"
    locator: one facility on the line with the social cost and the maximum cost, the bounds 2 and 3/2, the left-right-middle mechanism, and two facilities
  - paper: doi:10.1145/1566374.1566401
    title: "Ariel D. Procaccia and Moshe Tennenholtz, Approximate mechanism design without money, Proceedings of the 10th ACM Conference on Electronic Commerce (EC 2009), 177-186"
    locator: the conference version
  - paper: "Herve Moulin, On strategy-proofness and single peakedness, Public Choice 35(4) (1980), 437-455"
    locator: the characterization of strategyproof rules on single-peaked preferences by medians with phantom voters
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 10, James Schummer and Rakesh V. Vohra, Mechanism design without money, the part on single-peaked preferences
  - paper: "Pinyan Lu, Xiaorui Sun, Yajun Wang and Zeyuan Allen Zhu, Asymptotically optimal strategy-proof mechanisms for two-facility games, Proceedings of the 11th ACM Conference on Electronic Commerce (EC 2010)"
    locator: bounds for two facilities on the line with the social cost
---

In strategyproof facility location, agents report their locations on a line, a mechanism places a facility, and each agent pays its distance to the facility as a cost. There is no money, so the rule itself must make truthful reports a dominant strategy, while keeping the total distance or the largest distance close to optimal. This page is about the approximation problem and its bounds. Its close page, the [generalized median voter rule](/generalized-median-voter-rule/), comes from social choice and characterizes the strategyproof rules for [single-peaked preferences](/single-peaked-preferences/), with no objective to approximate. The optimization problem without incentives is the [facility location problem](/facility-location-problem/).

## In plain words

A town will build one library on a long street. Each family says where it lives, and the town picks a spot. Every family wants the library as close to its own home as possible, and it may give a false address if that helps. The town wants a rule where an honest address is always the best answer. It also wants either a small total walking distance for all families, or a small walking distance for the family that lives farthest away. For the total distance, putting the library at the middle family's address is honest and best. For the farthest family, honest rules without chance can only promise twice the best distance, and rules with chance can promise one and a half times.

## Definition

There are $n$ agents. Agent $i$ has a private location $x_i \in \mathbb{R}$ and reports $x_i'$. A deterministic mechanism is a function $f : \mathbb{R}^n \to \mathbb{R}$ that places the facility at $y = f(x')$. The cost of agent $i$ is $|y - x_i|$. A randomized mechanism returns a probability distribution over $\mathbb{R}$, and the cost of agent $i$ is the expected distance $\mathbb{E}|y - x_i|$.

A mechanism is **strategyproof** if for every agent $i$, every profile $x$ and every report $x_i'$,
$$\text{cost}_i\bigl(f(x), x_i\bigr) \;\le\; \text{cost}_i\bigl(f(x_i', x_{-i}), x_i\bigr).$$
For a randomized mechanism this is strategyproofness in expectation, the analog of [truthful in expectation](/truthful-in-expectation/) without payments.

The two objectives are
$$\text{SC}(y, x) = \sum_{i=1}^n |y - x_i| \quad \text{(social cost)}, \qquad \text{MC}(y, x) = \max_i |y - x_i| \quad \text{(maximum cost)}.$$
A mechanism has [approximation ratio](/approximation-ratio/) $\rho$ for an objective if its cost, or expected cost, is at most $\rho$ times the optimal cost on every profile. The problem is to find strategyproof mechanisms with the smallest ratio and to prove matching lower bounds.

Agents with cost $|y - x_i|$ have single-peaked preferences with peak $x_i$, so strategyproof facility location on the line is a special case of strategyproof voting on single-peaked preferences.

## Variants

- **Several facilities.** Two or $k$ facilities, each agent using the nearest one. This is the strategic form of the [k-median problem](/k-median-problem/).
- **Other spaces.** Trees, cycles, general graphs and the plane. In $\mathbb{R}^d$, the coordinatewise median is strategyproof.
- **Group strategyproofness.** No coalition can misreport so that all its members gain.
- **Obnoxious facilities.** Agents want the facility far away, as for a landfill.
- **Agents with several locations, weights or capacities.** Each changes the bounds.

## Examples

A small example. Four agents are at $0, 2, 3, 10$.

- **Median.** With the left median for even $n$, the facility goes to $2$. The social cost is $2 + 0 + 1 + 8 = 11$, which is optimal, since every point of $[2, 3]$ has cost 11. The agent at 10 cannot help itself: a larger report leaves the median at 2, and a report below 2 moves it farther away.
- **Maximum cost.** The optimal location is the midpoint $5$, with maximum cost 5. The median 2 has maximum cost 8.
- **Leftmost agent.** The facility goes to $0$, with maximum cost $10 = 2 \cdot 5$.
- **Left-right-middle (LRM).** Place the facility at the leftmost location $0$ with probability $1/4$, at the rightmost $10$ with probability $1/4$, and at the midpoint $5$ with probability $1/2$. The expected maximum cost is $\frac14 \cdot 10 + \frac14 \cdot 10 + \frac12 \cdot 5 = 7.5 = \frac32 \cdot 5$.

## Known algorithms

- **Median.** Place the facility at a median of the reports. It is strategyproof, even group strategyproof. An agent left of the median can change the median only by reporting a point to the right of it, and that moves the median to the right, away from the agent. The case of an agent right of the median is symmetric. Its social cost is optimal.
- **Generalized medians.** Moulin (1980) showed that the strategyproof, anonymous rules that depend only on the peaks are the medians of the $n$ reports and $n + 1$ fixed *phantom* points, and that Pareto efficiency reduces the phantoms to $n - 1$. See [generalized median voter rule](/generalized-median-voter-rule/) and the [median voter theorem](/median-voter-theorem/).
- **Leftmost agent.** Place the facility at the smallest report. Only an agent who reports left of everyone can move it, and that moves it away from that agent, so the rule is strategyproof. Its maximum cost is the width $R - L$ of the profile, and the optimum is $(R - L)/2$, so the ratio is 2.
- **LRM.** The randomized mechanism of the example, due to Procaccia and Tennenholtz. It is strategyproof in expectation, and its expected maximum cost is $\frac14 (R - L) + \frac14 (R - L) + \frac12 \cdot \frac{R - L}{2} = \frac34 (R - L)$, which is $\frac32$ times the optimum.
- **Two facilities.** Procaccia and Tennenholtz analyzed the mechanism that places the two facilities at the leftmost and rightmost reports. For the social cost its ratio is $n - 2$. Lu, Sun, Wang and Zhu (2010) showed that deterministic strategyproof mechanisms for two facilities cannot get a ratio that stays bounded as $n$ grows, and gave a randomized mechanism with constant ratio.

## Bounds

For one facility on the line:

| Objective | Deterministic | Randomized |
| --- | --- | --- |
| Social cost | 1 (median) | 1 |
| Maximum cost | 2, tight | $3/2$, tight |

**Deterministic lower bound 2 for the maximum cost.** Suppose a strategyproof $f$ has ratio below 2. On the profile $(0, 1)$, the optimum is $1/2$. If $f(0, 1) \notin (0, 1)$, the maximum cost is at least 1, so $y = f(0, 1)$ lies strictly between 0 and 1. Now take the profile $(0, y)$. The agent at $y$ could report 1 and get the facility at its own location, with cost 0. Strategyproofness forces $f(0, y) = y$. On this profile the maximum cost is $y$ and the optimum is $y/2$, which gives ratio 2, a contradiction.

**Randomized lower bound 3/2 for the maximum cost.** Let $P$ be the distribution on the profile $(0, 1)$. Since $\mathbb{E}_P|y| + \mathbb{E}_P|1 - y| \ge 1$, one agent has expected cost at least $1/2$; by symmetry let it be the agent at 1. Take the profile $(0, 2)$ with distribution $P'$. An agent at 1 could report 2 and get $P'$, so strategyproofness at $(0, 1)$ gives $\mathbb{E}_{P'}|1 - y| \ge \mathbb{E}_P|1 - y| \ge \frac12$. On $(0, 2)$ the maximum cost of a point $y$ is $\max(|y|, |2 - y|) = 1 + |1 - y|$, so the expected maximum cost is at least $\frac32$, while the optimum is 1.

For two facilities, Procaccia and Tennenholtz proved a deterministic lower bound of $3/2$ for the social cost, and the later work cited above showed that the deterministic ratio must grow with $n$.

## Reductions

- **From single-peaked voting.** Distance costs on a line are single-peaked, so every strategyproof rule for single-peaked preferences gives a strategyproof facility location mechanism. The converse direction is the content of Moulin's characterization.
- **Escaping Gibbard-Satterthwaite.** On all preference orders, the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/) leaves only dictatorships. The single-peaked structure of facility location is what allows the median and other good rules.
- **Approximation as a replacement for money.** With money, [VCG](/vcg-mechanism/) would place the facility optimally for the social cost. Without money, the designer gives up some of the objective instead, as with the maximum cost, where the optimal midpoint is not strategyproof.

## Applications

- **Public facilities.** Locating a library, school or bus stop from residents' reports.
- **Choosing a number.** A committee picks a budget level, a temperature or a date, each member has an ideal value, and the median is used.
- **Robust estimation from strategic data.** When data points come from agents who want the estimate close to their own point, median-like estimators are strategyproof.

## References
