---
tag: YD7XQN
kind: algorithm
slug: top-trading-cycles
name: Top trading cycles
aliases:
- TTC
- "Gale's top trading cycles"
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Each agent points to the owner of its favourite remaining house, and the agents on a cycle trade and leave. The result is the unique strict core allocation of a housing market.
solves: [house-allocation-problem]
model: word-ram
complexity:
  vars: {n: the number of agents, L: the total length of the preference lists}
  time: {worst: O(n + L)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1974
  people: [David Gale, Lloyd Shapley, Herbert Scarf]
  note: Shapley and Scarf published the algorithm in 1974 and gave it to David Gale. Roth and Postlewaite proved in 1977 that its result is the unique strict core allocation, and Roth proved in 1982 that it is strategyproof.
prereqs: [shapley-scarf-housing-market, functional-graph]
see_also: [roth-postlewaite-theorem, top-trading-cycles-and-chains, serial-dictatorship, random-serial-dictatorship, school-choice-problem, core-of-a-cooperative-game, individual-rationality, cycle-detection]
sources:
  - paper: doi:10.1016/0304-4068(74)90033-0
    title: Lloyd Shapley and Herbert Scarf, On cores and indivisibility, Journal of Mathematical Economics 1(1), 23 to 37 (1974)
    locator: the housing market model and the top trading cycle algorithm, which the paper attributes to David Gale
  - paper: doi:10.1016/0304-4068(77)90004-0
    title: Alvin E. Roth and Andrew Postlewaite, Weak versus strong domination in a market with indivisible goods, Journal of Mathematical Economics 4(2), 131 to 137 (1977)
    locator: the uniqueness of the strict core allocation for strict preferences
  - paper: doi:10.1016/0165-1765(82)90003-9
    title: Alvin E. Roth, Incentive compatibility in a market with indivisible goods, Economics Letters 9(2), 127 to 132 (1982)
    locator: the proof that truth-telling is a dominant strategy under top trading cycles
  - paper: doi:10.1016/0165-1765(84)90003-X
    title: Charles G. Bird, Group incentive compatibility in a market with indivisible goods, Economics Letters 14, 309 to 313 (1984)
    locator: group strategyproofness of the core rule
  - paper: "Jinpeng Ma, Strategy-proofness and the strict core in a market with indivisibilities, International Journal of Game Theory 23(1), 75 to 83 (1994)"
    title: Strategy-proofness and the strict core in a market with indivisibilities
    locator: the characterization of the core rule by individual rationality, Pareto efficiency and strategyproofness
  - paper: doi:10.2307/2998580
    title: Atila Abdulkadiroglu and Tayfun Sonmez, Random serial dictatorship and the core from random endowments in house allocation problems, Econometrica 66(3) (1998)
    locator: the equivalence of the core from random endowments and random serial dictatorship
---

Top trading cycles (TTC) finds the outcome of a [Shapley-Scarf housing market](/shapley-scarf-housing-market/), where each agent owns one house and ranks all houses. Each agent points to the owner of the house it likes best among the houses still in the market. Since every agent points somewhere, the pointers contain a cycle, and the agents on it trade along the cycle: each gets the house it points to. They leave with their houses, and the rest repeat. The result is the unique allocation in the strict core, as the [Roth-Postlewaite theorem](/roth-postlewaite-theorem/) states. It is [individually rational](/individual-rationality/), Pareto optimal, and no agent gains by a false ranking. With a walk that follows the pointers and never moves a list pointer back, it runs in $O(n + L)$ time, where $L$ is the total length of the lists, so $O(n^2)$ for complete lists.

## In plain words

Everyone owns a house and has a favourite. Each person points at the owner of the house they like best. Follow the arrows from anyone: since there are finitely many people, you come back to someone you saw, and that closes a loop. The people in the loop swap houses so that each gets the house they pointed at, and they go home. The others point again among the houses that are left, and the process repeats until everyone is gone.

People in a loop get their favourite house among those left, and nobody can do better by lying about what they like.

## The problem

There are $n$ agents $1, \dots, n$, and agent $i$ owns house $h_i$. Each agent has a strict ranking of the houses. A list may stop at the own house; the agent ranks the houses that it does not list below its own. The output is an allocation: a permutation $x$ with $x(i)$ the house of agent $i$.

## The algorithm

```pseudo id=main
TOP-TRADING-CYCLES(lists)
L1  for each agent i do ptr[i] ← 1
L2  for each agent i do x[i] ← NIL
L3  for each agent s that is still in the market, in any order do
L4      path ← (s)
L5      while path is not empty do
L6          i ← the last agent on path
L7          while house list[i][ptr[i]] has left the market do ptr[i] ← ptr[i] + 1
L8          j ← the owner of house list[i][ptr[i]]
L9          if j is on path then remove j, …, i from the end of path; each of them gets the house it points to, and all of them leave the market with their houses
L10         else append j to path
L11 return x
```

The path is a walk along the pointers. Line L7 moves the pointer of the last agent to its best house that is still in the market. Line L8 follows the pointer. If the owner is already on the path, the end of the path from $j$ to $i$ is a cycle, and line L9 makes it trade. After the trade the walk goes on from the agent that is now last, whose pointer may now point to a house that has left. Its own house is on its list and is still in the market, so line L7 always stops.

The textbook statement works in rounds: in each round all remaining agents point, and all cycles trade at once. The walk gives the same result, and it is faster because it does not rebuild the pointers in each round.

## Example

Five agents. Agent 1 ranks $h_3 \succ h_2 \succ h_1$, agent 2 ranks $h_1 \succ h_3 \succ h_2$, agent 3 ranks $h_2 \succ h_1 \succ h_3$, agent 4 ranks $h_1 \succ h_5 \succ h_4$, and agent 5 ranks $h_4 \succ h_1 \succ h_2 \succ h_3 \succ h_5$. The walk starts at agent 1.

| step | path | last agent points to | action |
|---|---|---|---|
| 1 | 1 | owner of $h_3$, agent 3 | append 3 |
| 2 | 1, 3 | owner of $h_2$, agent 2 | append 2 |
| 3 | 1, 3, 2 | owner of $h_1$, agent 1, on the path | cycle 1, 3, 2: agent 1 gets $h_3$, 3 gets $h_2$, 2 gets $h_1$ |
| 4 | (empty) | | start again at agent 4 |
| 5 | 4 | $h_1$ has left, so $h_5$, agent 5 | append 5 |
| 6 | 4, 5 | owner of $h_4$, agent 4, on the path | cycle 4, 5: agent 4 gets $h_5$, 5 gets $h_4$ |

The allocation is $x = (h_3, h_1, h_2, h_5, h_4)$. Agents 1, 2 and 3 get their first choices. Agents 4 and 5 both wanted $h_1$ or $h_4$, but $h_1$ went in the first cycle, so they trade with each other. A brute force check over all $120$ allocations and all coalitions shows that this is the only allocation that no coalition can weakly improve on.

**Edge cases.** An agent whose favourite house is its own forms a cycle of length one and keeps its house. If all agents rank their own house first, nobody trades. With one agent, the agent keeps its house.

## Correctness

Each agent on the path, except the last one, points to the next agent on the path, and that agent's house is its best house still in the market. This holds because houses only leave, so a best remaining house stays the best while it remains. So when line L9 finds a cycle, each agent on it points to the owner of its best remaining house: it is a cycle of the pointer graph, a [functional graph](/functional-graph/) in which every agent has one outgoing arc.

Any order of removing such cycles gives the same allocation, and it is the unique allocation in the strict core. In outline: the agents of the first cycle get their first choices, so any other allocation that changes their houses is weakly blocked by that cycle alone. Then the agents of the second cycle get their best houses outside the first cycle, and so on. Conversely, a coalition that tries to block the result must contain an agent that wants a house of an earlier cycle, but the agents of the earlier cycles in the coalition need all those houses for themselves. The proof file gives both directions in full, and also the proof that no agent gains by a false list.

## Complexity

The model is the [word RAM](/word-ram/). An agent is appended to the path at most once, because it stays on the path until it leaves the market, and an agent on the path is never appended again. Each pass of line L5 either appends an agent or removes at least one, so there are at most $2n$ passes. Line L7 only moves pointers forward, so its total cost is at most $L$, the total list length, and line L9 costs $O(1)$ per removed agent. The total time is $O(n + L)$, which is $O(n^2)$ for complete lists and linear in the input size. The extra space is $O(n)$ for the pointers, the path and the flags.

The round version recomputes all pointers and finds all cycles in each round. In a functional graph every cycle is a strongly connected component with more than one vertex or with a self-loop, so [Tarjan's algorithm](/tarjan-scc/) finds all cycles of a round in linear time, as does a simple walk with colours. A round costs $O(n)$ besides the pointer moves, and there can be $n$ rounds, so $O(n^2)$ besides the scans of the lists.

## Properties

- **Strict core, unique.** The result is the only allocation that no coalition can weakly improve on by trading its own houses (Roth and Postlewaite 1977). It is also the only competitive allocation.
- **Individually rational and Pareto optimal.** These follow from the strict core for the coalitions of one agent and of all agents.
- **Strategyproof.** No agent gets a better house by a false list (Roth 1982). The result is even group strategyproof: no group can misreport so that all its members are at least as well off and one is better off (Bird 1984).
- **Characterized.** Ma (1994) showed that TTC is the only rule on housing markets that is individually rational, Pareto optimal and strategyproof.
- **Independent of the order.** The walk can start at any agent and the cycles can trade in any order.

## Variants and improvements

- **House allocation with random owners.** Give the houses to the agents uniformly at random as endowments, then run TTC. Abdulkadiroglu and Sonmez (1998) proved that this gives the same lottery over matchings as [random serial dictatorship](/random-serial-dictatorship/).
- **Kidney exchange.** [Top trading cycles and chains](/top-trading-cycles-and-chains/) lets a patient-donor pair point to the waiting list for a deceased donor, and then also trades along chains that end at the list.
- **School choice.** In the TTC rule for the [school choice problem](/school-choice-problem/), students point to schools and schools point to the student with the highest priority, and the cycles trade seats.
- **Ties.** With indifferences the strict core can be empty, and a fixed tie-break inside TTC can lose Pareto optimality. Rules for ties first trade inside groups of equally good houses; they are more involved.

## When to use it

Use TTC when the agents already own the objects and must not lose by taking part: tenants who trade rooms, pairs in a kidney exchange, students with a seat that they keep unless they trade it. It is the only rule that is individually rational, efficient and strategyproof at once. When nobody owns the objects, use [serial dictatorship](/serial-dictatorship/) or a random order instead.

## Pitfalls

- **Pointing at houses instead of owners.** The graph has agents as nodes, and an arc goes to the owner of the wanted house. Each agent still owns the house it started with until its cycle trades.
- **Long cycles.** A cycle can contain every agent. In a kidney exchange all transplants of a cycle must take place at the same time, so long cycles are not practical, and a length bound turns the problem into the NP-hard [kidney exchange problem](/kidney-exchange-problem/).
- **Ties broken in a fixed way.** With indifferences, a fixed tie-break gives a strategyproof rule, but the result need not be Pareto optimal.
- **Rebuilding every round.** Recomputing all pointers each round wastes time; keep the pointers and move them forward only.

## Implementations

The Python version takes the lists as lists of house indices (agent $i$ owns house $i$), each containing the own house, and an optional start order for the walk. It returns $x$ with $x[i]$ the house of agent $i$. The tests compare the result with the strict core found by brute force over all allocations and coalitions, for every profile with three agents and random profiles with four, check strategyproofness over all false lists, and compare with the round version and other start orders.

## History

Shapley and Scarf (1974) defined the housing market and proved that its core is not empty by the top trading cycle algorithm, which they attributed to David Gale. Roth and Postlewaite (1977) showed that with strict preferences its result is the unique allocation in the strict core and the unique competitive allocation. Roth (1982) proved that it is strategyproof, Bird (1984) that it is group strategyproof, and Ma (1994) that it is the only individually rational, Pareto optimal and strategyproof rule. Abdulkadiroglu and Sonmez (1998) connected it with random serial dictatorship, and Roth, Sonmez and Unver (2004) extended it to kidney exchange.

## References
