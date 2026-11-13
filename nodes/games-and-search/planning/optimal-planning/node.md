---
tag: ZB6GYE
kind: problem
slug: optimal-planning
name: Optimal planning
aliases:
- cost-optimal planning
area: games-and-search/planning
level: core
summary: Given a classical planning task with action costs, find a plan of minimum total cost, or report that no plan exists. With unit costs this is a plan with the fewest actions.
prereqs: [classical-planning, admissible-heuristic]
see_also: [a-star-search, h-max-heuristic, landmark-heuristic, pattern-database, delete-relaxation, satplan, bounded-plan-existence-np-complete, international-planning-competition]
sources:
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: Section 3.1 (PLANSAT is PSPACE-complete) and Section 4.1 (PLANMIN, with the NP-hardness of short plans for delete-free tasks)
  - paper: doi:10.1609/icaps.v19i1.13370
    title: "Malte Helmert and Carmel Domshlak, Landmarks, critical paths and abstractions: what's the difference anyway?, ICAPS 2009"
    locator: the LM-cut heuristic and its place between h-max and h+ (general locator)
  - paper: doi:10.1145/2559951
    title: "Malte Helmert, Patrik Haslum, Jörg Hoffmann and Raz Nissim, Merge-and-shrink abstraction: a method for generating lower bounds in factored state spaces, Journal of the ACM 61(3) (2014)"
    locator: the merge-and-shrink framework and its admissible heuristics (general locator)
  - paper: doi:10.1609/icaps.v24i1.13621
    title: "Florian Pommerening, Gabriele Röger, Malte Helmert and Blai Bonet, LP-based heuristics for cost-optimal planning, ICAPS 2014"
    locator: the operator-counting framework (general locator)
  - paper: doi:10.1007/978-3-642-04617-9_2
    title: "Christoph Betz and Malte Helmert, Planning with h+ in theory and practice, KI 2009, LNAI 5803"
    locator: pp. 9 to 16 (the complexity of computing h+ in standard benchmark domains)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2021
    locator: Chapter 11, Sections 11.2 and 11.3 (search and heuristics for classical planning)
---

Optimal planning asks for a cheapest plan of a [classical planning](/classical-planning/) task. Each action has a cost, the cost of a plan is the sum of the costs of its actions, and the answer is a plan of minimum cost, or the report that the task has no plan. A planner that only has to find some plan is called satisficing; an optimal planner must also prove that no cheaper plan exists. This proof is what makes the problem hard in practice: the planner must rule out every cheaper alternative, which in the worst case means a large part of the state space. Even deciding whether any plan exists is [PSPACE-complete](/strips-plan-existence-pspace-complete/), and finding a shortest plan is NP-hard already for tasks without deletes, by [bounded plan existence](/bounded-plan-existence-np-complete/). The standard method is [A*](/a-star-search/) with an [admissible heuristic](/admissible-heuristic/), and most research on optimal planning is research on such heuristics.

## In plain words

You have a list of moves, each with a price, and you want to get from the start to the goal. Any route that gets there is a plan. An optimal plan is a route with the lowest total price.

Finding one route is often easy. Finding the cheapest one is harder, because you must also be sure that no other route costs less. To do that without trying every route, planners use a lower estimate of the remaining price. If the estimate never says too much, a careful search that uses it finds the cheapest plan and can stop early.

## Definition

**Input.** A STRIPS task $T = (F, A, I, G)$ as on the [STRIPS](/strips/) page, with $n = |F|$ facts and $m = |A|$ actions, and a cost function $c : A \to \mathbb{R}_{\ge 0}$. For a plan $\pi = a_1, \ldots, a_k$, the cost is $c(\pi) = \sum_{i=1}^{k} c(a_i)$. Tasks in PDDL or in a multi-valued form such as SAS+ are first grounded to this form or to its multi-valued analogue.

**Output.** A plan $\pi^*$ with $c(\pi^*) = h^*(I)$, where $h^*(s)$ is the minimum cost of a plan from the state $s$, and $h^*(s) = \infty$ when no plan from $s$ exists. If $h^*(I) = \infty$, the output is "unsolvable".

**Decision version.** Given $T$, $c$ and a bound $K$, is there a plan of cost at most $K$? With unit costs and $K$ in unary this is PLANLEN, the problem of [bounded plan existence](/bounded-plan-existence-np-complete/).

**State graph view.** Let $\mathcal{S}$ be the graph whose vertices are the $2^n$ states and that has an edge from $s$ to $s[a]$ of weight $c(a)$ for each action $a$ applicable in $s$. A plan is a path from $I$ to a goal state, and an optimal plan is a shortest path from $I$ to the set of goal states. The graph is not given explicitly; it is described by $T$, which can be exponentially smaller.

The minimum exists when a plan exists. A cheapest plan never visits a state twice when all costs are positive, so it is a shortest simple path in a finite graph. With costs of zero, a cheapest plan with no repeated state still exists, since removing a cycle never makes a plan more expensive.

## Variants

- **Step-optimal planning.** All actions cost 1, so the goal is a plan with the fewest actions. Many early benchmark domains had no action costs, so this was the usual measure of early optimal planners.
- **Cost-optimal planning.** General nonnegative action costs, as defined above. A step-optimal plan can be far from cost-optimal; see the examples.
- **Parallel-step optimal planning.** Independent actions may run in the same step, and the measure is the number of steps. [Graphplan](/graphplan/) and the plans of a fixed horizon in [SATPLAN](/satplan/) are optimal in this sense, which differs from both measures above.
- **Makespan.** For actions with durations the measure is the end time of the plan; see [temporal planning](/temporal-planning/).
- **Bounded-suboptimal planning.** Find a plan of cost at most $w \cdot h^*(I)$ for a given $w \ge 1$. [Weighted A*](/weighted-a-star/) with an admissible heuristic gives this guarantee.
- **Soft goals and net benefit.** Some goals have rewards, and the planner maximizes the reward of the reached goals minus the cost of the plan. This is also called oversubscription planning.
- **Optimal delete-free planning.** Find a cheapest plan of the [delete relaxation](/delete-relaxation/) of a task. Its value is the heuristic $h^+$, which is a lower bound for the original task.

## Examples

**Cost and length differ.** A package is at location A and must go to C. A truck and a plane are at A. The truck can go from A to B and from B to C, each at cost 1; the plane can fly from A to C at cost 10. Loading and unloading cost 1. The plan "load into plane, fly, unload" has 3 actions and cost 12. The plan "load into truck, drive to B, drive to C, unload" has 4 actions and cost 4. So the step-optimal plan has cost 12 and the cost-optimal plan has 4 actions. On this task $h_{\max}(I) = 3$ and $h_{\mathrm{add}}(I) = h^*(I) = 4$, both computed with the costs above by the code of the [h-max](/h-max-heuristic/) and [h-add](/h-add-heuristic/) pages.

**The Sussman anomaly.** In the [Sussman anomaly](/sussman-anomaly/), with the four actions pick up, put down, stack and unstack at unit cost, the optimal plan has 6 actions. In the initial state $h_{\max} = 3$, $h^+ = 5$ and $h_{\mathrm{add}} = 5$. The admissible values 3 and 5 are below 6, and A* with either of them returns a plan of 6 actions.

**Long optimal plans.** The [Tower of Hanoi](/tower-of-hanoi/) with $d$ disks needs $2^d - 1$ moves, and every plan has at least that many actions. With 4 disks the optimal plan has 15 actions, and $h_{\max}(I) = h^+(I) = 4$ in the standard encoding of the h-add page. A weak lower bound means that A* expands many states with $f$ below 15.

**Delete-free and still hard.** A delete-free task whose actions have no preconditions is a [set cover](/set-cover/) problem: the goal facts are the elements, and each action covers the goal facts that it adds. A cheapest plan is a cheapest cover.

## Known algorithms

Every algorithm for this problem is a search that returns a plan together with a proof that no cheaper plan exists. They differ in what they search and in what lower bounds they use.

| method | what it does | guarantee |
| --- | --- | --- |
| Breadth-first search, [uniform-cost search](/uniform-cost-search/), [Dijkstra](/dijkstra/) | blind search of the state graph | optimal; time and space up to the number of reachable states |
| [A*](/a-star-search/) with an admissible heuristic | best-first search on $g + h$ | optimal if $h$ is admissible and duplicates are reopened, or if $h$ is consistent |
| [IDA*](/iterative-deepening-a-star/) | depth-first search with a growing bound on $g + h$ | optimal with an admissible $h$; memory linear in the depth |
| [h-max](/h-max-heuristic/) (Bonet and Geffner 2001) | the cost of the most expensive goal in the delete relaxation | admissible and consistent; often weak |
| LM-cut (Helmert and Domshlak 2009) | repeated cuts of the h-max justification graph give disjunctive action landmarks with a cost partitioning | admissible; between $h_{\max}$ and $h^+$ |
| [Landmark heuristics](/landmark-heuristic/) with cost partitioning | facts or actions that every plan needs, with their costs shared out | admissible when the costs are partitioned |
| [Pattern databases](/pattern-database/) | exact costs in a projection onto some variables, stored in a table | admissible and consistent; sums are admissible for additive patterns |
| Merge-and-shrink (Helmert, Haslum, Hoffmann and Nissim 2014) | abstractions built by merging variables and shrinking the product | admissible and consistent; exact with bisimulation shrinking |
| Operator counting (Pommerening, Röger, Helmert and Bonet 2014) | a linear program over how often each action is used, with constraints from landmarks, the state equation and abstractions | the LP optimum is admissible |
| Symbolic search with [BDDs](/binary-decision-diagram/) | breadth-first or cost-layered search on sets of states | optimal; works on sets, not single states |
| [SATPLAN](/satplan/) and [Graphplan](/graphplan/) | encodings of a fixed horizon | optimal in parallel steps, not in cost |

The heuristics relate as follows on every state: $h_{\max} \le h^{\mathrm{LM\text{-}cut}} \le h^+ \le h^*$. Pattern databases and merge-and-shrink are not bounded by $h^+$, since they keep some of the deletes. A heuristic that needs more time per state can still pay off when it cuts the number of expanded states enough; which choice is best depends on the domain.

## Bounds

- **Decision.** Deciding whether a plan exists is PSPACE-complete ([Bylander 1994](/strips-plan-existence-pspace-complete/)), so optimal planning is PSPACE-hard. Deciding whether a plan of cost at most $K$ exists is NP-complete for unit costs and $K$ polynomial in the input, and PSPACE-complete for $K$ in binary ([bounded plan existence](/bounded-plan-existence-np-complete/)).
- **Delete-free tasks.** For delete-free tasks a plan exists or not in polynomial time, but a cheapest plan is NP-hard to find, so $h^+$ is NP-hard to compute. Through the set cover example, the minimum number of actions of a delete-free task without preconditions is the minimum size of a set cover, so no polynomial algorithm approximates it within a factor $(1 - \varepsilon) \ln |G|$ unless P = NP, by the [inapproximability of set cover](/set-cover-inapproximability/).
- **Domains.** Betz and Helmert (2009) classify standard benchmark domains into ones where $h^+$ is computable in polynomial time and ones where it is NP-hard. Optimal planning in the [blocks world](/blocks-world/) is NP-hard, although a plan of at most twice the optimal length is easy to find.
- **Output.** Some tasks with $n$ facts have only plans of $2^n - 1$ actions (the binary counter of the plan existence page), so writing an optimal plan can take time exponential in $n$.
- **Upper bound.** A blind search of the state graph with a binary heap runs in time $O(r \, m \, (n + \log m))$ for $r \le 2^n$ reachable states, using a hash table on states and at most $r m$ heap entries, which is exponential in $n$ in the worst case.

## Reductions

- **To shortest paths.** By the state graph view, optimal planning is a single-source shortest path problem to a set of targets, on a graph of up to $2^n$ vertices given implicitly. Every method in the table is a way to avoid building this graph.
- **To the decision version.** With integer costs at most $C$, a binary search over $K$ in $[0, C (2^n - 1)]$ finds $h^*(I)$ with $O(n + \log C)$ calls to the decision version.
- **To satisfiability and integer programs.** For a fixed horizon, the plans form the models of a propositional formula, and minimizing cost becomes a [MAX-SAT](/max-sat/) problem or an [integer program](/integer-programming/). The horizon must be large enough to contain an optimal plan, which can need $2^n - 1$ steps.
- **From SAT.** The reduction on the bounded plan existence page turns a CNF formula into a delete-free task whose shortest plan has $2m + r$ actions exactly when the formula is satisfiable, so any algorithm for optimal planning solves SAT.
- **From set cover.** The example above is an approximation-preserving reduction from set cover to optimal delete-free planning.

## Applications

- **Benchmarks for search and heuristics.** The optimal tracks of the International Planning Competition compare optimal planners on shared PDDL domains. The measure is the number of tasks solved within a time and memory limit, since every returned plan has the same cost.
- **Lower bounds for satisficing planners.** The optimal cost, or a proved lower bound, shows how far a satisficing plan is from the best one.
- **Puzzles.** Shortest solutions of puzzles such as the [sliding tile puzzle](/sliding-tile-puzzle/) are optimal planning problems with unit costs, and the techniques of pattern databases were first developed for them.
- **Logistics, scheduling and resource use.** When actions have real prices, such as fuel, time or money, a cost-optimal plan is the cheapest way to reach the goal under the model.
- **Verification.** Model checkers that look for a shortest counterexample solve the same shortest path problem on an implicit state graph.

## References
