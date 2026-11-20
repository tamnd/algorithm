---
tag: C6KHMS
kind: problem
slug: house-allocation-problem
name: House allocation problem
aliases:
- assignment of indivisible objects
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Assign indivisible objects to agents with strict preferences, at most one object each and without money, so that the result is efficient, fair or hard to manipulate.
prereqs: [pareto-optimality, bipartite-matching]
see_also: [serial-dictatorship, random-serial-dictatorship, probabilistic-serial, popular-matching, shapley-scarf-housing-market, top-trading-cycles, school-choice-problem, assignment-problem]
sources:
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 6, Pareto optimal matchings (Section 6.2 on house allocation and Section 6.2.2 on ties); Chapter 7, Popular matchings
  - paper: doi:10.1007/978-3-540-30551-4_3
    title: David J. Abraham, Katarina Cechlarova, David F. Manlove and Kurt Mehlhorn, Pareto optimality in house allocation problems, ISAAC 2004, LNCS 3341, 3 to 15
    locator: the characterization of Pareto optimal matchings, the maximum Pareto optimal matching algorithm and the NP-hardness of the minimum one
  - paper: doi:10.2307/2998580
    title: Atila Abdulkadiroglu and Tayfun Sonmez, Random serial dictatorship and the core from random endowments in house allocation problems, Econometrica 66(3) (1998)
    locator: the model and the equivalence of random serial dictatorship with the core from random endowments
  - paper: doi:10.1006/jeth.2000.2710
    title: Anna Bogomolnaia and Herve Moulin, A new solution to the random assignment problem, Journal of Economic Theory 100(2), 295 to 328 (2001)
    locator: ordinal efficiency, envy-freeness in the stochastic dominance sense and the probabilistic serial rule
  - paper: doi:10.1007/s003550050160
    title: Lars-Gunnar Svensson, Strategy-proof allocation of indivisible goods, Social Choice and Welfare 16, 557 to 567 (1999)
    locator: the characterization of serial dictatorships by strategyproofness, nonbossiness and neutrality
---

The house allocation problem asks how to give indivisible objects, called houses, to agents who rank them, when each agent can get at most one object and no money changes hands. Nobody owns an object at the start. A solution is a matching of agents to objects, or a lottery over matchings, and the question is which matching to pick: one that is [Pareto optimal](/pareto-optimality/), one that is fair to agents with the same claim, one that no agent can improve by lying, or one that no other matching beats in a vote. Student housing, the assignment of courses, offices or shifts, and the first stage of [school choice](/school-choice-problem/) all have this form. When each agent owns one object at the start, the problem becomes the [Shapley-Scarf housing market](/shapley-scarf-housing-market/).

## In plain words

A group of people must share some rooms. Each person gets one room or none, and each room goes to one person or stays empty. Each person ranks the rooms they would accept. There are no prices and no payments.

Many answers are possible, so we need a reason to prefer one. An answer is wasteful if some other answer makes a person happier and nobody unhappier. A good rule never gives a wasteful answer, and it does not reward a person who lies about their ranking. If two people have the same claim, a fair rule gives them the same chances, so it often draws lots.

## Definition

**Input.** A set $N$ of $n$ agents and a set $O$ of $m$ objects. Each agent $i$ has a strict preference list $\succ_i$ over a subset $A_i \subseteq O$ of acceptable objects, best first. Agent $i$ prefers every acceptable object to having nothing, and having nothing to every object outside $A_i$. The pairs $(i, o)$ with $o \in A_i$ form the edge set $E$ of a [bipartite graph](/bipartite-graph/), so $|E| = \sum_i |A_i|$ is the total length of the lists.

**Output.** A matching $M$: each agent gets at most one acceptable object, and each object goes to at most one agent. $M(i)$ is the object of agent $i$, or nothing. A random solution is a lottery over matchings. Its *assignment matrix* $P$ has $P_{io}$ equal to the probability that $i$ gets $o$; with $n = m$ and complete lists, every lottery over perfect matchings gives a bistochastic matrix, and by the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) every bistochastic matrix comes from a lottery.

**Measures.** The common goals are these.

- *Pareto optimality.* $M$ is Pareto optimal if no matching $M'$ is at least as good as $M$ for every agent and better for at least one.
- *Size.* Among the Pareto optimal matchings, find one with the most agents matched.
- *Popularity.* $M$ is [popular](/popular-matching/) if no matching $M'$ is preferred by more agents than prefer $M$.
- *Ordinal efficiency.* A lottery is ordinally efficient if no other lottery gives every agent a distribution that first-order stochastically dominates its own, with at least one strict.
- *Fairness.* Equal treatment of equals (agents with the same list get the same row of $P$) and envy-freeness in the stochastic dominance sense (each agent weakly prefers its own row to every other row, in that sense).
- *Strategyproofness.* No agent gets a better object, or a dominating lottery, by reporting a false list. This is a [dominant-strategy](/dominant-strategy-incentive-compatibility/) requirement.

## Variants

- **Ties.** Agents may be indifferent between objects. Pareto optimality then needs more care: a serial dictatorship with ties broken arbitrarily can give a matching that is not Pareto optimal, and Manlove (2013, Section 6.2.2) gives algorithms for this case.
- **Capacities.** An object can have several copies (a course with seats). The same rules apply with a copy count per object.
- **Existing tenants.** Some agents own an object at the start and must not be made worse off. With every agent an owner and $n = m$, this is the [Shapley-Scarf housing market](/shapley-scarf-housing-market/), solved by [top trading cycles](/top-trading-cycles/). The mixed case is house allocation with existing tenants (Abdulkadiroglu and Sonmez 1999).
- **Cardinal utilities.** Agents report values, not only rankings, and the goal is an efficient lottery in expected utility. The [Hylland-Zeckhauser mechanism](/hylland-zeckhauser-mechanism/) uses prices in fake money for this.
- **Two-sided preferences.** If objects also rank agents and stability is the goal, the problem becomes [stable matching](/stable-matching/) or [school choice](/school-choice-problem/).

## Examples

**Four agents, four objects.** Agents 1 and 2 rank $a \succ b \succ c \succ d$, and agents 3 and 4 rank $b \succ a \succ d \succ c$. This is the example of Bogomolnaia and Moulin (2001). Write a matching as the objects of agents 1 to 4 in order. There are $4! = 24$ perfect matchings and 209 matchings in all. A script that checks every pair of matchings finds exactly 12 Pareto optimal ones, all perfect.

| matching | Pareto optimal? | reason |
|---|---|---|
| $a, b, d, c$ | yes | serial dictatorship with the order 1, 2, 3, 4 gives it |
| $a, c, b, d$ | yes | the order 1, 3, 2, 4 gives it |
| $c, d, a, b$ | yes | the order 4, 3, 1, 2 gives it |
| $a, d, b, c$ | no | $a, c, b, d$ is better for agents 2 and 4 and the same for agents 1 and 3 |
| $c, b, a, d$ | no | $c, a, b, d$ is better for agents 2 and 3 and the same for agents 1 and 4 |

A perfect matching here fails to be Pareto optimal exactly when an agent of $\{1, 2\}$ holds $b$ while an agent of $\{3, 4\}$ holds $a$, or an agent of $\{1, 2\}$ holds $d$ while an agent of $\{3, 4\}$ holds $c$: the two agents gain by a swap. Each condition holds in 8 perfect matchings and both hold in 4, so $8 + 8 - 4 = 12$ perfect matchings are not Pareto optimal, and the other 12 are.

**Pareto optimal matchings of different sizes.** Agent 1 accepts $a$ and $b$, in this order, and agent 2 accepts only $a$. Both $\{1a\}$ and $\{1b, 2a\}$ are Pareto optimal: moving from the first to the second hurts agent 1. Abraham, Cechlarova, Manlove and Mehlhorn (2004) show that Pareto optimal matchings exist of every size between the smallest and the largest.

**A lottery.** In the four-agent example, [random serial dictatorship](/random-serial-dictatorship/) gives agent 1 the probabilities $5/12, 1/12, 5/12, 1/12$ for $a, b, c, d$, and [probabilistic serial](/probabilistic-serial/) gives $1/2, 0, 1/2, 0$. Agents 1 and 2 would both rather have the second, and so would agents 3 and 4, with $b$ and $d$ in place of $a$ and $c$.

## Known algorithms

- [Serial dictatorship](/serial-dictatorship/): agents pick in a fixed order. Pareto optimal and strategyproof, in $O(m + n^2)$ time. Every Pareto optimal matching is the result of serial dictatorship for some order (Abdulkadiroglu and Sonmez 1998); the serial dictatorship page proves this for incomplete lists too.
- [Random serial dictatorship](/random-serial-dictatorship/): serial dictatorship with a uniformly random order. Strategyproof, ex post Pareto optimal and fair in the sense of equal treatment of equals, but not ordinally efficient.
- [Probabilistic serial](/probabilistic-serial/): the eating algorithm. Ordinally efficient and envy-free in the stochastic dominance sense, but only weakly strategyproof.
- Maximum Pareto optimal matching: $O(n^{1/2} |E|)$ time for strict lists, by a maximum matching followed by phases based on top trading cycles that remove the inefficiencies (Abraham et al. 2004).
- [Popular matching](/popular-matching/): decide existence and find a largest popular matching in $O(n + m + |E|)$ time for strict lists.
- [Hylland-Zeckhauser mechanism](/hylland-zeckhauser-mechanism/): a market equilibrium in fake money for cardinal utilities; ex ante Pareto optimal and envy-free.

## Bounds

- Checking whether a given matching is Pareto optimal takes $O(n + m + |E|)$ time for strict lists (Abraham et al. 2004). Every algorithm must read the lists, so this is optimal.
- A maximum Pareto optimal matching takes $O(n^{1/2} |E|)$ time, the time of a maximum [bipartite matching](/bipartite-matching/) by [Hopcroft-Karp](/hopcroft-karp/). A minimum Pareto optimal matching is NP-hard to find, and every Pareto optimal matching has at least half the size of a largest one, because it is a maximal matching of the acceptability graph (Abraham et al. 2004).
- Computing the probabilities of random serial dictatorship is #P-complete (Aziz, Brandt and Brill 2013; Saban and Sethuraman 2015), so the exact lottery is hard to compute even though one draw is easy.
- Impossibility: with $n \ge 4$, no random assignment rule is ordinally efficient, strategyproof and treats equals equally (Bogomolnaia and Moulin 2001). With cardinal utilities, no rule is ex ante efficient, strategyproof and symmetric (Zhou 1990).
- Characterization: a deterministic rule is strategyproof, nonbossy and neutral exactly when it is a serial dictatorship (Svensson 1999).

## Reductions

- To [bipartite matching](/bipartite-matching/): the acceptable pairs form a bipartite graph, and every Pareto optimal matching is a maximal matching of it.
- From the housing market: a [Shapley-Scarf housing market](/shapley-scarf-housing-market/) is a house allocation problem with an initial matching that every agent may veto. Abdulkadiroglu and Sonmez (1998) show that drawing a random initial matching and taking the core gives the same lottery as random serial dictatorship.
- To weighted matching: maximizing a sum of utilities, or a lexicographic profile of ranks, is a [maximum weight matching](/maximum-weight-matching/) or [assignment problem](/assignment-problem/) with suitable weights, but such a rule is not strategyproof.

## Applications

Allocation of on-campus housing to students, of courses with capacities, of offices, of time slots and shifts, and of public housing. The kidney exchange programs start from the same model, with patient and donor pairs in place of tenants; see the [kidney exchange problem](/kidney-exchange-problem/).

## References
