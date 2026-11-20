---
tag: ATPZWG
kind: model
slug: shapley-scarf-housing-market
name: Shapley-Scarf housing market
aliases:
- housing market
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Each agent owns one house, ranks all houses, and houses are traded without money. With strict rankings, top trading cycles gives the unique strict core allocation.
prereqs: [core-of-a-cooperative-game, pareto-optimality]
see_also: [top-trading-cycles, roth-postlewaite-theorem, house-allocation-problem, top-trading-cycles-and-chains, kidney-exchange-problem, competitive-equilibrium, assignment-game, individual-rationality]
sources:
  - paper: doi:10.1016/0304-4068(74)90033-0
    title: Lloyd Shapley and Herbert Scarf, On cores and indivisibility, Journal of Mathematical Economics 1(1), 23 to 37 (1974)
    locator: the model, the nonempty core, competitive prices, and the top trading cycle algorithm of David Gale
  - paper: doi:10.1016/0304-4068(77)90004-0
    title: Alvin E. Roth and Andrew Postlewaite, Weak versus strong domination in a market with indivisible goods, Journal of Mathematical Economics 4(2), 131 to 137 (1977)
    locator: weak and strong domination, and the uniqueness of the strict core allocation for strict preferences
  - paper: doi:10.1016/0165-1765(82)90003-9
    title: Alvin E. Roth, Incentive compatibility in a market with indivisible goods, Economics Letters 9(2), 127 to 132 (1982)
    locator: the core rule is strategyproof
  - paper: "Jinpeng Ma, Strategy-proofness and the strict core in a market with indivisibilities, International Journal of Game Theory 23(1), 75 to 83 (1994)"
    title: Strategy-proofness and the strict core in a market with indivisibilities
    locator: the characterization of the core rule by individual rationality, Pareto efficiency and strategyproofness
---

The Shapley-Scarf housing market is the simplest model of trade without money. There are $n$ agents, each owns one indivisible object (a house), and each ranks all the houses. Agents can only swap houses; nobody can buy a house or pay to keep one. Shapley and Scarf (1974) used the model to show that a market with indivisible goods can have a nonempty [core](/core-of-a-cooperative-game/), even though such a market is not a convex economy. Their proof is the [top trading cycles](/top-trading-cycles/) algorithm of David Gale. With strict rankings, the result of that algorithm is the only allocation in the strict core and the only competitive allocation, which is the [Roth-Postlewaite theorem](/roth-postlewaite-theorem/).

## The machine

**Agents and houses.** There are agents $N = \{1, \dots, n\}$, and agent $i$ owns house $h_i$ at the start. Each agent $i$ has a ranking $\succeq_i$ of all $n$ houses. In the main case the rankings are strict, written $\succ_i$; the general model allows ties.

**Allocations.** An allocation is a permutation $x$ of the houses: $x(i)$ is the house that agent $i$ gets. Every agent gets exactly one house. An agent that does not trade keeps its own house, so an agent never ends up with nothing.

**Blocking.** A coalition $S \subseteq N$ can trade only among its own houses. A trade of $S$ is a permutation $y$ of $\{h_j : j \in S\}$ among the agents of $S$.

- $S$ *strongly blocks* $x$ if some trade $y$ of $S$ gives $y(i) \succ_i x(i)$ for every $i \in S$.
- $S$ *weakly blocks* $x$ if some trade $y$ of $S$ gives $y(i) \succeq_i x(i)$ for every $i \in S$, with strict preference for at least one agent of $S$.

**Core and strict core.** The *core* is the set of allocations that no coalition strongly blocks. The *strict core* is the set of allocations that no coalition weakly blocks. The strict core is a subset of the core.

**Competitive equilibrium.** A price vector $p$ assigns a price to each house. Agent $i$ can afford the houses $h$ with $p(h) \le p(h_i)$, since it can only pay by selling its own house. A pair $(x, p)$ is a [competitive equilibrium](/competitive-equilibrium/) if each agent $i$ gets a house $x(i)$ that it ranks highest among the houses it can afford. Since $x$ is a permutation, the market clears.

## What it counts

The model asks which allocations are stable against trade by groups, and how to compute them.

**Existence.** Shapley and Scarf proved that the core is never empty, also with ties, and that a competitive allocation always exists. With strict rankings the top trading cycles algorithm gives one directly. It removes cycles $C_1, C_2, \dots, C_r$ in order. Give each house of $C_k$ the price $r - k + 1$. An agent of $C_k$ can afford exactly the houses of $C_k, \dots, C_r$, and its house from the algorithm is its best house among these. So the result, with these prices, is a competitive equilibrium.

**Uniqueness with strict rankings.** Roth and Postlewaite (1977) proved that with strict rankings the strict core has exactly one allocation, the result of top trading cycles, and that it is also the only competitive allocation. The core under strong blocking can be larger. For three agents, let agent 1 rank $h_2 \succ h_1 \succ h_3$, agent 2 rank $h_1 \succ h_3 \succ h_2$, and agent 3 rank $h_1 \succ h_2 \succ h_3$. Top trading cycles gives $(h_2, h_1, h_3)$: agents 1 and 2 swap. The allocation $(h_2, h_3, h_1)$ is also in the core, because no coalition can make all its members strictly better off. It is not in the strict core: the coalition $\{1, 2\}$ swaps, agent 1 keeps $h_2$, and agent 2 gets $h_1$ in place of $h_3$. A brute force check over the six allocations confirms that the core has exactly these two allocations and the strict core has only the first.

**Ties.** With ties, the strict core can be empty or have several allocations. If agent 1 is indifferent between all houses, and agents 2 and 3 both rank $h_1$ first and are indifferent between $h_2$ and $h_3$, then every allocation is weakly blocked, while all six are in the core. If agents 1 and 2 are indifferent between all houses and agent 3 ranks $h_3$ first, the strict core has two allocations: nobody trades, or agents 1 and 2 swap.

**Incentives.** The mechanism that returns the top trading cycles allocation is strategyproof: no agent gets a better house by a false ranking (Roth 1982). Ma (1994) showed that it is the only mechanism on this model that is [individually rational](/individual-rationality/), Pareto optimal and strategyproof.

**Computation.** With strict rankings, top trading cycles finds the strict core allocation in $O(n^2)$ time, linear in the input. In contrast, a brute force search over coalitions and allocations takes exponential time.

## Relation to other models

- **House allocation.** The [house allocation problem](/house-allocation-problem/) has the same objects but no owners, so individual rationality does not apply. Giving the houses to the agents at random and then running top trading cycles gives the same lottery as [random serial dictatorship](/random-serial-dictatorship/) (Abdulkadiroglu and Sonmez 1998).
- **Mixed markets.** In house allocation with existing tenants, some agents own a house and others do not, and some houses are vacant. Rules for it combine serial dictatorship with top trading cycles.
- **Kidney exchange.** A patient with a willing but incompatible donor is an agent that owns a kidney. The [kidney exchange problem](/kidney-exchange-problem/) uses this view, with two changes: a cycle must be short, because its operations take place at the same time, and a pair may also trade with the waiting list, as in [top trading cycles and chains](/top-trading-cycles-and-chains/).
- **The assignment game.** In the [assignment game](/assignment-game/) of Shapley and Shubik, houses are sold for money between buyers and sellers. With money the core is the set of optimal dual solutions of an LP, while without money the core is found by the combinatorial cycle argument.
- **Two-sided matching.** In [stable matching](/stable-matching/), both sides have preferences and nobody owns the other side. The housing market is one-sided: only the agents have preferences.

## Known results in the model

| question | answer | source |
|---|---|---|
| Is the core nonempty? | Yes, with or without ties | Shapley and Scarf 1974 |
| Is there a competitive allocation? | Yes | Shapley and Scarf 1974 |
| Size of the strict core, strict rankings | Exactly one allocation, the TTC one | Roth and Postlewaite 1977 |
| Competitive allocations, strict rankings | Exactly the TTC allocation | Roth and Postlewaite 1977 |
| Size of the core, strict rankings | Can be larger than one | the example above |
| Is the core rule strategyproof? | Yes, for strict rankings | Roth 1982 |
| Rules that are IR, Pareto optimal and strategyproof | Only the core rule | Ma 1994 |
| Strict core with ties | Can be empty or have several allocations | the examples above |
| Time to compute the strict core allocation | $O(n^2)$, linear in the input | top trading cycles |

## References
