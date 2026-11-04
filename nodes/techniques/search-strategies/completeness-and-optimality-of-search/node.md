---
tag: SH6XB8
kind: definition
slug: completeness-and-optimality-of-search
name: Completeness and optimality of search
aliases:
- search completeness
- search optimality
area: techniques/search-strategies
level: intro
summary: A search is complete if it finds a goal whenever one exists, and optimal if it returns a cheapest goal.
prereqs: [state-space-search, search-strategy, search-tree]
see_also: [uniform-cost-search, breadth-first-search, depth-first-search, iterative-deepening-search, a-star-optimality, optimal-efficiency-of-a-star, admissible-heuristic, total-correctness]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3.4 (completeness, cost optimality, time and space complexity) and Section 3.4.6 (the comparison of the uninformed strategies)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (completeness and admissibility of best-first search and A*)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (the use of "admissible" for a search that always finds an optimal solution)
---

A search algorithm is *complete* if it finds a solution whenever one exists, and *cost-optimal* if each solution it returns is a cheapest one. With time and space, these are the four measures that compare [search strategies](/search-strategy/). Both are properties of an algorithm on a class of problems, and both depend on conditions: a finite branching factor, a positive lower bound on the action costs, a finite state space, or the use of [graph search](/graph-search-vs-tree-search/). An older name for a search that always returns an optimal solution is *admissible*.

## Definition

A search problem $P$ has an initial state $s_0$, a finite set of actions in each state, a transition model, action costs $c(s, a, s') \ge 0$ and a goal test. A *solution* is a finite sequence of actions that leads from $s_0$ to a goal state. Its cost is the sum of its action costs. Let $\mathcal{S}(P)$ be the set of solutions. When $\mathcal{S}(P) \neq \emptyset$, let

$$ C^*(P) = \inf \{\, \mathrm{cost}(\sigma) : \sigma \in \mathcal{S}(P) \,\}. $$

Let $\mathcal{A}$ be a search algorithm and $\mathcal{P}$ a class of search problems.

- $\mathcal{A}$ is **complete** on $\mathcal{P}$ if, for each $P \in \mathcal{P}$ with $\mathcal{S}(P) \neq \emptyset$, the run of $\mathcal{A}$ on $P$ stops after finitely many steps and returns some $\sigma \in \mathcal{S}(P)$.
- $\mathcal{A}$ is **complete with failure detection** on $\mathcal{P}$ if, in addition, for each $P \in \mathcal{P}$ with $\mathcal{S}(P) = \emptyset$, the run stops after finitely many steps and reports failure. Russell and Norvig use "complete" in this stronger sense.
- $\mathcal{A}$ is **cost-optimal** on $\mathcal{P}$ if, for each $P \in \mathcal{P}$, each solution $\sigma$ that $\mathcal{A}$ returns has $\mathrm{cost}(\sigma) = C^*(P)$. In particular, the infimum is then attained.
- $\mathcal{A}$ is **admissible** on $\mathcal{P}$ if it is complete and cost-optimal on $\mathcal{P}$: whenever a solution exists, it returns an optimal one. This is the sense of Pearl and of Korf's title.

An algorithm that is cost-optimal but not complete can run for ever without an answer, and then it is cost-optimal for an empty reason. So a claim of optimality is useful only with a claim of completeness under the same conditions.

The standard conditions are about the [search tree](/search-tree/). Let $b$ be the branching factor, $d$ the depth of a shallowest goal and $\epsilon$ a lower bound on the action costs.

- **Finite branching factor.** Each state has finitely many actions, so each level of the tree is finite.
- **Costs bounded away from zero.** Each action cost is at least some $\epsilon > 0$. Then a path of cost at most $C$ has at most $\lfloor C/\epsilon \rfloor$ actions, and with a finite branching factor there are finitely many of them.

**Fact 1.** If $b$ is finite, each action cost is at least $\epsilon > 0$, and $\mathcal{S}(P) \neq \emptyset$, then $P$ has a solution of cost exactly $C^*(P)$.

*Proof.* Let $\sigma_0$ be a solution and $C = \mathrm{cost}(\sigma_0)$. Each solution of cost at most $C$ has at most $\lfloor C/\epsilon \rfloor$ actions. With a finite branching factor, the number of action sequences of at most this length is finite. So the set of solutions with cost at most $C$ is finite and not empty, and it has a cheapest element. Each other solution costs more than $C$. So this element has cost $C^*(P)$. $\square$

**Fact 2.** Breadth-first search with a finite branching factor is complete. It is complete with failure detection on finite state spaces when it uses graph search.

*Proof.* Breadth-first search expands all nodes of depth $i$ before any node of depth $i + 1$. A shallowest goal has depth $d$, and the levels $0$ to $d$ are finite, so the search generates a goal node after finitely many steps. On a finite space with graph search, each state enters the frontier at most once, so the frontier becomes empty after finitely many steps when no goal is reachable. $\square$

**Fact 3.** No search algorithm is complete with failure detection on the class of all search problems whose states, actions and goal test are given by programs.

*Proof.* Take a [Turing machine](/turing-machine/) $M$. Let the states be the configurations of $M$ on the empty input, the one action of a configuration lead to the next configuration, and the goal test accept the halting configurations. A solution exists if and only if $M$ halts. An algorithm that always stops and decides whether a solution exists would decide the [halting problem](/halting-problem/). $\square$

So on infinite spaces, completeness in the weaker sense is the best that a general search can give: it finds a solution when one exists, and it may run for ever when none exists.

## Examples and non-examples

All examples use the graph with the directed edges S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3, start S and goal G. Its solutions cost 12 (S-G), 4 (S-A-C-G), 6 (S-A-C-D-G) and 11 (S-A-B-D-G), so $C^* = 4$.

- **Complete, not cost-optimal.** Breadth-first search returns S-G, the solution with the fewest actions, with cost 12. It is complete by Fact 2. It is cost-optimal only on the problems in which all actions have the same cost.
- **Complete and cost-optimal.** [Uniform-cost search](/uniform-cost-search/) with the goal test at expansion returns S-A-C-G with cost 4. It is complete and cost-optimal when $b$ is finite and each action cost is at least $\epsilon > 0$.
- **Cost-optimal on unit costs, with little memory.** [Iterative deepening search](/iterative-deepening-search/) is complete for finite $b$ and returns a shallowest goal, so it is cost-optimal when all actions cost the same.
- **Not complete: an infinite branch.** Let the root have two children: a left child that starts an infinite chain of states with no goal, and a right child that is a goal. Depth-first search that takes the left child first never returns. Depth-first search is complete on a finite space only with graph search or a check for cycles.
- **Not complete: costs that tend to zero.** Let S have the action S→G with cost 1, and an infinite chain $S = x_0 \to x_1 \to x_2 \to \cdots$ where the action $x_{i-1} \to x_i$ costs $2^{-i}$. Each cost is positive, but no positive lower bound exists. The node $x_i$ has path cost $1 - 2^{-i} < 1$, so uniform-cost search expands the whole chain before the goal and never returns. This is why its completeness needs $\epsilon > 0$, not only positive costs.
- **No optimal solution.** Let S have, for each $i \ge 1$, an action to a goal $G_i$ with cost $1 + 2^{-i}$. This needs an infinite branching factor. Then $C^* = 1$, but no solution costs 1. No algorithm can be cost-optimal here, and Fact 1 shows that a finite branching factor rules this out when the costs are bounded away from zero.
- **Not cost-optimal: an early goal test.** Uniform-cost search that tests a node for the goal when it generates the node finds S-G at the first expansion and returns cost 12. Optimality needs the test when the node is selected for expansion.
- **Not cost-optimal: greedy best-first search.** [Greedy best-first search](/greedy-best-first-search/) orders the frontier by an estimate of the remaining cost only. With $h(G) = 0$ and $h(A) \ge 1$, it selects S-G right after S and returns cost 12.

## Related definitions

- **Soundness.** Each answer that the search returns is a solution. All the searches on this site are sound, so the definitions above assume it. With [partial correctness](/partial-correctness/) and termination it gives [total correctness](/total-correctness/), and completeness is the termination part for the instances that have a solution.
- **Systematic search.** A search that visits each node of the search tree, or each state, at most once in a fixed order and does not lose any. Breadth-first, uniform-cost and iterative deepening search are systematic. Local search, such as [hill climbing](/hill-climbing/), is not, and it is not complete in general.
- **Admissible heuristic.** A different use of the same word: a heuristic $h$ is [admissible](/admissible-heuristic/) when it never overestimates the cost to a goal. A* with an admissible heuristic is an admissible search on the problems with finite $b$ and costs at least $\epsilon > 0$, see [A* optimality](/a-star-optimality/).
- **Optimal efficiency.** A different notion: among the algorithms that use the same information, an algorithm is optimally efficient if no other expands fewer nodes. A* with a consistent heuristic is optimally efficient in a precise sense, see [optimal efficiency of A*](/optimal-efficiency-of-a-star/).
- **Probabilistic completeness.** A randomized search is probabilistically complete if the probability that it has found a solution, when one exists, tends to 1 as the number of steps grows. Random restarts of a local search and sampling-based motion planners have this weaker property.
- **Resolution completeness.** A search over a grid or a fixed discretization is complete relative to that grid: it finds a solution when one exists on the grid.

## References
