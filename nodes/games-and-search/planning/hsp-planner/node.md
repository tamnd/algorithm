---
tag: WZK9NT
kind: algorithm
slug: hsp-planner
name: HSP planner
aliases:
- heuristic search planner
area: games-and-search/planning
level: advanced
summary: Forward state-space planner that evaluates each state by the additive heuristic h-add, computed anew from the delete relaxation, with hill climbing (HSP) or weighted A* (HSP2).
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of actions, r: the number of reachable states (at most 2^n)}
  time: {worst: O(r^2 m n + r m n log(m n)), best: O(m n log(m n))}
  space: {extra: O(r n + m n)}
properties: {deterministic: true}
prereqs: [forward-state-space-search, h-add-heuristic, weighted-a-star]
see_also: [h-max-heuristic, delete-relaxation, fast-forward-planner, hill-climbing, greedy-best-first-search, backward-state-space-search, sussman-anomaly, international-planning-competition]
sources:
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (the additive heuristic, the hill climbing planner HSP, the regression planner HSPr and the best first planner HSP2)
  - paper: doi:10.1609/aimag.v21i2.1506
    title: "Drew McDermott, The 1998 AI Planning Systems Competition, AI Magazine 21(2) (2000)"
    locator: the report on the competition at AIPS-98, in which HSP took part
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.3 (heuristics for planning)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on heuristic search planning (general locator)
---

HSP, the Heuristic Search Planner of Blai Bonet and Hector Geffner, solves [STRIPS](/strips/) tasks by [forward state-space search](/forward-state-space-search/) guided by a heuristic that it derives from the task itself. For each state it meets, it computes the additive heuristic [h-add](/h-add-heuristic/) in the [delete relaxation](/delete-relaxation/): each fact gets the cheapest cost of a relaxed derivation, and the estimate is the sum over the goal facts. No knowledge about the domain is needed. The first HSP used this estimate with [hill climbing](/hill-climbing/) and restarts; HSP2 uses it with [weighted A*](/weighted-a-star/), which keeps the search complete. HSP showed in 1998 that a plain forward search with a domain-independent heuristic can compete with the planning graph and SAT planners of that time, and the planners that followed, such as [FF](/fast-forward-planner/), kept the scheme and improved the heuristic and the search. The heuristic is not admissible, so the plans are not optimal in general.

## In plain words

HSP looks at the current state and asks: if actions never undid anything, how expensive would each goal be, priced one at a time? The sum of these prices is its guess of the distance to the goal. It makes this guess again for every new state.

Then it searches forward. It always looks first at the state with the best mix of "cost so far" and "guess of the cost still to go", and gives the guess more weight to get to a goal sooner. A state for which even the easy world has no plan is thrown away, because the real world has no plan from it either.

## The problem

The input is a ground STRIPS task $(F, A, I, G)$ with facts $F$, actions $A$, an initial state $I$ and a goal $G$, as on [forward state-space search](/forward-state-space-search/). Each action $a$ has a precondition, an add list, a delete list and a cost $c(a)$, here a nonnegative integer. An action is applicable in $s$ when $\mathit{pre}(a) \subseteq s$, and leads to $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. The output is a plan, a sequence of actions applicable from $I$ that ends in a state containing $G$, or *failure* when there is none. HSP does not promise a cheapest plan. Write $n = |F|$, $m = |A|$ and $r$ for the number of states reachable from $I$.

## The algorithm

HSP2 is weighted A* with the evaluation $f(s) = g(s) + W \cdot h_{\mathrm{add}}(s)$ for a weight $W \ge 1$. The value $g(s)$ is the cost of the best path to $s$ found so far, kept in the table `best`. H-ADD is the procedure of the [h-add](/h-add-heuristic/) page, with an index from facts to the actions that need them built once. Each state is evaluated once, and the value is kept with the state.

```pseudo id=main
HSP2(I, G, A, W)
L1  h ← the evaluator H-ADD(·, G, A), with its index of preconditions built once
L2  if h(I) = ∞ then return failure
L3  best(I) ← 0; parent(I) ← nil; OPEN ← a priority queue that holds I with key W · h(I)
L4  while OPEN is not empty do
L5      remove from OPEN an entry s with the least key; skip it if best(s) has dropped since it was inserted
L6      if G ⊆ s then return the actions on the parent links from I to s
L7      for each a in A with pre(a) ⊆ s do
L8          t ← (s \ del(a)) ∪ add(a)
L9          if best(s) + c(a) < best(t) then               ▷ best(t) = ∞ for a new state
L10             if h(t) = ∞ then continue                  ▷ a relaxed dead end: no plan leaves t
L11             best(t) ← best(s) + c(a); parent(t) ← (s, a)
L12             insert t into OPEN with key best(t) + W · h(t)
L13 return failure
```

Line L9 puts a state back into OPEN whenever a cheaper path to it is found, even if it was expanded before. This reopening is needed because h-add is not consistent. Line L10 prunes states from which the delete relaxation has no plan. Such a state has no real plan either, so pruning keeps every plan.

The first HSP used the same evaluator in a different search. From the current state, it moves to a child with the least $h_{\mathrm{add}}$, breaking ties at random and preferring children not yet visited in the current climb. It returns the plan when it reaches a goal state, and starts again from $I$ after too many moves that do not improve the best value. The implementation here has this search as `hsp1`.

## Example

Take the [Sussman anomaly](/sussman-anomaly/) in the [blocks world](/blocks-world/): C is on A, A and B are on the table, and the goal is $\{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$, with the four actions pickup, putdown, stack and unstack at cost 1. Then $h_{\mathrm{add}}(I) = 5$, while the shortest plan has 6 actions.

**Hill climbing is trapped.** Both children of $I$, after unstack(C,A) or after pickup(B), have the value 7. The climb goes to one of them; after unstack(C,A) the best child is putdown(C), with value 4. From there pickup(A) has value 4 and pickup(B) has value 5, so the climb picks up A and then stacks it on B, a state of value 3. This is a local minimum: its children, unstack(A,B) and pickup(C), have the values 4 and 6. The climb has achieved on(A,B) first, the order that the Sussman anomaly punishes, and must undo it. With a limit of 20 moves without improvement and 50 restarts, `hsp1` finds no plan for the seeds 0 to 4.

**HSP2 solves it.** With $W = 5$, HSP2 expands 10 states, evaluates 15 states, and returns unstack(C,A), putdown(C), pickup(B), stack(B,C), pickup(A), stack(A,B), a shortest plan. Along this plan the heuristic values are 5, 7, 4, 5, 2, 1, 0. The value 7 after the first action is above the true remaining cost 5, which shows that h-add is not admissible, and the rise from 4 to 5 shows that it is not monotone along a plan.

**Effect of the weight.** The table gives the length of the plan and the number of expanded states for $W = 1$ and $W = 5$ on small tasks with unit costs. The four-block task starts from the towers A under B and C under D and asks for the single tower D, C, B, A from the bottom. The logistics task has one truck at A, three connected places A, B, C, and three packages, each to move one place on.

| Task | Shortest plan | $W = 1$: length | $W = 1$: expanded | $W = 5$: length | $W = 5$: expanded |
| --- | --- | --- | --- | --- | --- |
| Sussman anomaly | 6 | 6 | 11 | 6 | 10 |
| Four blocks | 8 | 8 | 24 | 14 | 17 |
| Logistics, 3 packages | 9 | 9 | 14 | 11 | 11 |
| Tower of Hanoi, 4 disks | 15 | 15 | 35 | 15 | 24 |

A larger weight makes the search greedier: it expands fewer states, and the plans can get longer. Even $W = 1$ does not promise a shortest plan, because h-add can overestimate.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). For costs that are nonnegative integers, HSP2 is sound, terminates, and is complete. *Soundness*: the parent links always form a tree rooted at $I$, because a link is changed only when it lowers the value of `best` strictly, and following them from a state gives an applicable sequence of actions that ends in it. *Pruning is safe*: $h_{\mathrm{add}}(t) = \infty$ exactly when the relaxed task from $t$ has no plan, and every real plan is a relaxed plan, so no plan leaves $t$. *Termination*: each insertion of a state into OPEN lowers its value of `best`, an integer at least 0, so each state is inserted finitely often. *Completeness*: if a plan exists and OPEN became empty, follow the plan from $I$; each of its states is not a relaxed dead end, each is reached and expanded with its final value of `best`, so the last one, a goal state, would have been removed at line L5 and returned at line L6. There is no bound on the cost of the plan in terms of the optimal cost, because h-add is not admissible. The first HSP is sound but not complete, as the Sussman example shows.

## Complexity

**One evaluation.** H-ADD runs a generalized Dijkstra over facts and actions. The size of the task is $L = n + \sum_a (|\mathit{pre}(a)| + |\mathit{add}(a)|) = O(m n)$, and with a [binary heap](/binary-heap/) one evaluation takes $O(L \log L) = O(m n \log(m n))$ time. HSP2 evaluates each state at most once, so at most $r$ evaluations happen, which costs $O(r m n \log(m n))$.

**Search.** For unit costs, each value of `best` of a state is the length of a path from $I$ that visits no state twice, so it is at most $r - 1$. Each insertion lowers the value, so a state is inserted into OPEN at most $r$ times, and at most $r^2$ expansions happen. Each expansion tests $m$ actions and builds their successors in $O(m n)$ time, and each of its at most $m$ insertions into a heap of at most $r^2$ entries costs $O(\log r) = O(n)$, since $r \le 2^n$. This gives the worst case $O(r^2 m n + r m n \log(m n))$. For integer costs at most $C$, replace the bound $r$ on the number of insertions of a state by $C (r - 1) + 1$. In practice reopenings are rare, and the time is dominated by the evaluations. The best case is $G \subseteq I$ with one evaluation, $O(m n \log(m n))$.

**Space.** The tables `best`, `parent` and the stored heuristic values hold up to $r$ states of $O(n)$ bits each, and the index of preconditions takes $O(m n)$, so the space is $O(r n + m n)$.

**No polynomial bound.** Plan existence for STRIPS is [PSPACE-complete](/strips-plan-existence-pspace-complete/), and shortest plans can have exponential length, so no planner has a polynomial worst case. The heuristic reduces the number of expanded states in practice, not in the worst case.

## Properties

- **Domain independent.** The heuristic is computed from the actions alone, with no hand-written knowledge of the domain.
- **Sound, and complete in the HSP2 form** on every finite task with nonnegative integer costs. Rational costs can be scaled to integers.
- **Not optimal.** h-add is not admissible, so even $W = 1$ can return a plan that is longer or costlier than necessary.
- **Prunes relaxed dead ends.** A state with $h_{\mathrm{add}} = \infty$ is never put into OPEN.
- **Costly evaluations.** Most of the time goes into H-ADD, which is computed from scratch for every new state. A planner that evaluates fewer states, as with lazy evaluation or helpful actions, runs faster.
- **Deterministic.** HSP2 is deterministic; the first HSP breaks ties at random.

## Variants and improvements

- **HSP.** The original planner, hill climbing on h-add with random tie breaking and restarts. It is fast when it works and incomplete, as the Sussman example shows.
- **HSPr.** Search backward from the goal by [regression](/goal-regression/), and evaluate a set of subgoals $S$ by $\sum_{p \in S} g_I(p)$, with the fact costs $g_I$ computed once from the initial state. Each evaluation is then a sum of table entries. Regression reaches sets of facts that are not part of any reachable state, and HSPr removes some of them with mutex pairs; see [backward state-space search](/backward-state-space-search/).
- **HSP2 with other heuristics.** The same search with [h-max](/h-max-heuristic/) and $W = 1$ is A* with an admissible heuristic, which gives optimal plans. Haslum and Geffner (2000) used their admissible $h^m$ heuristics in the same way for optimal planning.
- **FF.** [FF](/fast-forward-planner/) replaces the sum by the cost of a [relaxed plan](/relaxed-plan-heuristic/) extracted from the [relaxed planning graph](/relaxed-planning-graph/), which counts shared work once, and replaces hill climbing by [enforced hill climbing](/enforced-hill-climbing/), which escapes plateaus by breadth-first search, with helpful actions to prune successors.
- **Greedy best first search.** Order OPEN by $h$ alone, the limit of very large $W$. This is the default of many later satisficing planners.

## When to use it

Use HSP2 as a simple and complete satisficing planner for STRIPS tasks when any plan is useful and the state space is too large for blind search, and as a baseline for heuristic search planners. Use it with h-max and $W = 1$, or better with a stronger admissible heuristic, when the plan must be optimal; see [optimal planning](/optimal-planning/). For speed on benchmark domains, prefer the relaxed plan heuristic of FF or later planners, which are better informed and evaluate fewer states. Use the hill climbing HSP only together with a complete fallback.

## Pitfalls

- **Expecting optimal plans.** h-add overestimates. With $W = 1$ HSP2 is still not A* with an admissible heuristic, and the plan can be longer than necessary.
- **Closing states for good.** Without reopening, the search stays complete on finite tasks, but it can keep a costly path to a state and so return a much costlier plan. Reopen as on line L9, or accept the loss.
- **Evaluating a state twice.** H-ADD is the main cost. Keep the value with the state, as the table of values does, and compute it only for new states.
- **Pruning on a finite but large value.** Only $h_{\mathrm{add}} = \infty$ proves a dead end. A large finite value can belong to the only state that leads to the goal.
- **Hill climbing without a fallback.** The first HSP can fail on small solvable tasks such as the Sussman anomaly. Add restarts, a complete second phase, or both.

## Implementations

## History

Bonet, Loerincs and Geffner (1997) used a heuristic computed from the delete relaxation in a real-time planner, ASP. Bonet and Geffner then built HSP, which searched forward by hill climbing on the additive heuristic and took part in the planning competition at AIPS-98, reported by McDermott (2000). HSPr, the regression form with fact costs computed once, appeared at the European Conference on Planning in 1999. Bonet and Geffner (2001) described HSP, HSPr and the best first planner HSP2 together, and showed that the additive heuristic with weighted A* solves many benchmark tasks. Haslum and Geffner (2000) gave the admissible $h^m$ heuristics for optimal planning. Hoffmann and Nebel's FF (2001) took the same forward search scheme with a better heuristic, and most later classical planners in the [International Planning Competition](/international-planning-competition/) follow it.

## References
