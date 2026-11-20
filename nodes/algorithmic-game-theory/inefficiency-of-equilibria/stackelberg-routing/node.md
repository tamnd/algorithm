---
tag: ECM7BP
kind: problem
slug: stackelberg-routing
name: Stackelberg routing
aliases:
- Stackelberg scheduling of selfish traffic
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: A leader routes a fraction of the traffic centrally to steer the remaining selfish traffic toward a low-cost equilibrium.
prereqs: [selfish-routing-model, wardrop-equilibrium, system-optimal-flow]
see_also: [marginal-cost-tolls, price-of-anarchy, pigou-example, roughgarden-tardos-four-thirds-bound, braess-paradox-detection-hardness, stackelberg-equilibrium, security-game, np-hard]
sources:
  - paper: "Tim Roughgarden, Stackelberg scheduling strategies, SIAM Journal on Computing 33(2) (2004); STOC 2001"
    locator: "the model on parallel links, the strategies LLF and SCALE, the bounds 1/alpha and 4/(3 + alpha) for LLF, and the NP-hardness of computing an optimal strategy"
  - paper: "Yannis A. Korilis, Aurel A. Lazar and Ariel Orda, Achieving network optima using Stackelberg routing strategies, IEEE/ACM Transactions on Networking 5(1) (1997)"
    locator: conditions under which a network manager who controls part of the traffic can induce the optimal flow
  - paper: "V. S. Anil Kumar and Madhav V. Marathe, Improved results for Stackelberg scheduling strategies, ICALP 2002"
    locator: approximation schemes for the optimal strategy on parallel links
  - paper: "Chaitanya Swamy, The effectiveness of Stackelberg strategies and tolls for network congestion games, SODA 2007; ACM Transactions on Algorithms 8(4) (2012)"
    locator: bounds for Stackelberg strategies beyond parallel links
  - paper: "Vincenzo Bonifaci, Tobias Harks and Guido Schafer, Stackelberg routing in arbitrary networks, Mathematics of Operations Research 35(2) (2010)"
    locator: strategies and lower bounds in general networks
---

Stackelberg routing asks how a central authority that controls part of the traffic should route it, so that the selfish rest of the traffic settles into a good equilibrium. The leader moves first and commits to its routes; the followers then form a [Wardrop equilibrium](/wardrop-equilibrium/) on the network loaded by the leader. Here "Stackelberg" means only this leader-follower order in a routing game; it is a different use of the word from the two-player [Stackelberg equilibrium](/stackelberg-equilibrium/) and the [security games](/security-game/) built on it, where a leader commits to a mixed strategy against one rational follower. [Marginal cost tolls](/marginal-cost-tolls/) are the other main way to improve a selfish routing equilibrium: they change prices instead of controlling flow.

## In plain words

A city runs a fleet of buses and can choose their routes, but most cars are driven by people who pick the fastest route for themselves. The city wants low total travel time. If the buses take the same roads the cars like, the cars crowd those roads even more. A better plan is to send the buses on the roads that the cars would overuse, so those roads look slow to the cars, and the cars spread out. The question is how to choose the bus routes, how much this helps, and how hard the best choice is to compute.

## Definition

**Instance.** A [selfish routing](/selfish-routing-model/) instance $(G, r, \ell)$ with continuous nondecreasing latencies, and a number $\alpha \in [0, 1]$. The first and main case is a network of $m$ parallel links from $s$ to $t$; Roughgarden called the links machines and the problem Stackelberg scheduling.

**Leader.** The leader chooses a flow $s$ of rate $\alpha r$, a Stackelberg strategy.

**Followers.** The other $(1 - \alpha) r$ units of traffic are selfish and tiny. Given $s$, they form a flow $t$ of rate $(1 - \alpha) r$ that is a Wardrop equilibrium for the latencies $\tilde\ell_e(x) = \ell_e(s_e + x)$. This is a cost game with the Wardrop equilibrium as the equilibrium notion; an induced equilibrium $t$ always exists, and all of them have the same edge latencies.

**Goal.** Find $s$ that minimizes the total latency $C(s + t) = \sum_e (s_e + t_e)\, \ell_e(s_e + t_e)$.

The two extreme cases are known: for $\alpha = 0$ the answer is the ordinary Wardrop equilibrium, and for $\alpha = 1$ it is the [system optimal flow](/system-optimal-flow/). Let $f^*$ be an optimal flow and $\mathrm{OPT} = C(f^*)$.

## Variants

- **Parallel links or general networks.** Most results are for parallel links. In general networks, the leader's flow can create or remove a [Braess's paradox](/braess-paradox/), and the bounds are weaker.
- **Single or many commodities.** The leader may control a fraction $\alpha_i$ of each commodity.
- **Inducing the optimum.** Find the smallest $\alpha$ for which some strategy makes $s + t$ optimal. Korilis, Lazar and Orda (1997) gave conditions on parallel links, and Sharma and Williamson (2007) studied the smallest $\alpha$ for which the leader can improve the equilibrium at all.
- **Atomic followers.** The followers are players of an [atomic congestion game](/atomic-congestion-game/) instead of tiny users.

## Examples

**Pigou's network with $\alpha = 1/4$** ([Pigou example](/pigou-example/)). Link 1 has latency 1, link 2 has latency $x$, and $r = 1$. With no leader, all traffic takes link 2, with cost 1. The optimum splits $1/2, 1/2$, with cost $3/4$. Let the leader put $s_1$ on link 1 and $1/4 - s_1$ on link 2. The followers then see link 2 at latency at most 1, so they all take link 2, and the cost is $s_1 \cdot 1 + (1 - s_1)^2$. For $s_1 \le 1/4$ this is smallest at $s_1 = 1/4$, so the best strategy puts all its flow on link 1, with cost

$$\frac{1}{4} + \left(\frac{3}{4}\right)^2 = \frac{13}{16}.$$

The ratio to the optimum is $13/12$.

**Three links.** Let $\ell_1(x) = x$ and $\ell_2(x) = \ell_3(x) = x + 1$, with $r = 1$ and $\alpha = 1/6$. The marginal costs are $2x$ and $2x + 1$, and they are equal at $f^* = (2/3, 1/6, 1/6)$, so $\mathrm{OPT} = 4/9 + 2 \cdot \frac{1}{6} \cdot \frac{7}{6} = 5/6$. With no leader, all traffic takes link 1, with cost 1.

| leader flow $s$ | follower flow $t$ | cost |
|---|---|---|
| $(0, 0, 1/6)$ | $(5/6, 0, 0)$ | $25/36 + 7/36 = 8/9$ |
| $(0, 1/12, 1/12)$ | $(5/6, 0, 0)$ | $25/36 + 2 \cdot \frac{1}{12} \cdot \frac{13}{12} = 7/8$ |

In both rows the followers see latency $5/6$ on link 1 and at least 1 on the other links, so they all take link 1. The first row is what the LLF strategy below can do when it fills one of the two tied links; the second row splits the leader's flow and is better. It is the optimal strategy here, since the cost $25/36 + s_2(1 + s_2) + s_3(1 + s_3)$ with $s_2 + s_3 = 1/6$ is smallest at $s_2 = s_3$.

## Known algorithms

**LLF (largest latency first), Roughgarden 2001.** Compute $f^*$. Sort the links by their latency $\ell_i(f^*_i)$ at the optimum, largest first. Fill the links in this order, putting $f^*_i$ on each, until the leader's flow $\alpha r$ is used up. The idea is that the followers would underuse the slow links of the optimum, so the leader should take those. LLF runs in polynomial time once $f^*$ is known, which is a convex program.

**SCALE.** Route $s = \alpha f^*$, a scaled copy of the optimal flow. It is simple and works in any network, but it ignores which links the followers would overuse.

**Optimal strategy.** Computing an optimal Stackelberg strategy is [NP-hard](/np-hard/), even on parallel links with linear latencies (Roughgarden 2001). Kumar and Marathe (2002) gave approximation schemes for the optimal strategy on parallel links.

## Bounds

Each item is a theorem (Roughgarden 2001, for parallel links).

- For any continuous nondecreasing latencies, LLF gives $C(s + t) \le \frac{1}{\alpha}\, \mathrm{OPT}$.
- For linear latencies $\ell_i(x) = a_i x + b_i$, LLF gives $C(s + t) \le \frac{4}{3 + \alpha}\, \mathrm{OPT}$.
- Both bounds are tight.

For $\alpha = 0$ the second bound is the $4/3$ of the [Roughgarden-Tardos bound](/roughgarden-tardos-four-thirds-bound/), and for $\alpha = 1$ it is 1. In the Pigou example above, $4/(3 + 1/4) = 16/13 > 13/12$. The bound $1/\alpha$ does not depend on the latencies, while the [price of anarchy](/price-of-anarchy/) with no leader is unbounded for arbitrary latencies.

Beyond parallel links, Swamy (2007) and Bonifaci, Harks and Schafer (2010) studied LLF and SCALE beyond parallel links, where the bounds also depend on the shape of the network and on the class of latencies.

## Reductions

- With $\alpha = 1$ the problem is the computation of the [system optimal flow](/system-optimal-flow/), a convex program.
- With $\alpha = 0$ it is the computation of a [Wardrop equilibrium](/wardrop-equilibrium/), a convex program for the [Beckmann potential](/beckmann-potential/).
- For a fixed strategy $s$, computing the induced equilibrium is again a convex program, on the latencies $\ell_e(s_e + x)$. The hardness is in the choice of $s$.

## Applications

The model fits networks in which an operator controls some of the traffic: a network manager that routes its own flows among selfish users (the setting of Korilis, Lazar and Orda), a transport authority with a fleet of vehicles, or a cloud operator that places part of the jobs on servers that users also choose themselves. It is also a way to measure how much control is needed: the bounds above say how far a fraction $\alpha$ of controlled traffic moves the cost from the selfish equilibrium toward the optimum.

## References
