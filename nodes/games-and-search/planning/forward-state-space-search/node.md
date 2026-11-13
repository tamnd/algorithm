---
tag: 3SHV74
kind: algorithm
slug: forward-state-space-search
name: Forward state-space search (progression)
aliases:
- progression planning
area: games-and-search/planning
level: core
summary: Searches from the initial state of a STRIPS task, applying applicable actions, until a state contains the goal. Breadth-first order gives a plan with the fewest actions.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of actions, r: the number of reachable states (at most 2^n)}
  time: {worst: O(r m n), best: O(n)}
  space: {extra: O(r n)}
properties: {deterministic: true}
prereqs: [state-space-planning, strips, breadth-first-search]
see_also: [backward-state-space-search, uniform-cost-search, a-star-search, hsp-planner, fast-forward-planner, duplicate-detection, optimal-planning, graph-reachability]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4, Section 4.2 (the Forward-search procedure, its soundness and completeness, and deterministic versions with breadth-first, depth-first and best-first order)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.2 (forward state-space search for planning) and Section 11.3 (heuristics for planning)
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (forward search with a domain-independent heuristic in HSP and HSP2)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapters on classical planning and on heuristic search planning (general locator)
---

Forward state-space search, or progression, solves a [STRIPS](/strips/) planning task by search in its state graph. It starts at the initial state $I$, applies every action whose preconditions hold, and goes on until it removes a state that contains the goal $G$. The actions on the path to that state are a plan. It is the forward direction of [state-space planning](/state-space-planning/); the backward direction is [backward state-space search](/backward-state-space-search/). With a table of reached states it stops on every finite task, and with breadth-first order it returns a plan with the fewest actions. Every node it visits is a real reachable state, which makes it simple to combine with any heuristic. Heuristic forward search is the base of most modern classical planners, such as [HSP](/hsp-planner/) and [FF](/fast-forward-planner/).

## In plain words

Think of a board game with a fixed goal position. You start from the opening position and list every legal move. Each move gives a new position. You write each new position in a notebook, so that you never look at the same position twice. Then you take the positions from the notebook, one at a time, in the order you wrote them, and list their moves too.

You stop when you take out a position that has everything the goal asks for. The moves that led there are your plan. Because you always look at the positions that are fewer moves away first, the plan you find has as few moves as possible. If the notebook runs out and you never saw the goal, no plan exists.

## The problem

The input is a ground STRIPS task $(F, A, I, G)$: a finite set $F$ of facts, a finite set $A$ of actions, an initial state $I \subseteq F$ and a goal $G \subseteq F$. Each action $a$ has a precondition $\mathit{pre}(a)$, an add list $\mathit{add}(a)$ and a delete list $\mathit{del}(a)$, all subsets of $F$, and a cost $c(a) \ge 0$. The action $a$ is applicable in a state $s \subseteq F$ when $\mathit{pre}(a) \subseteq s$, and then the next state is
$$ s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a). $$
A plan is a sequence $a_1, \ldots, a_k$ such that each $a_i$ is applicable in $s_{i-1}$, where $s_0 = I$ and $s_i = s_{i-1}[a_i]$, and $G \subseteq s_k$. The output is a plan, or *failure* when no plan exists. With breadth-first order the plan has the fewest actions; with the cost order of the variant below it has the least total cost. Write $n = |F|$, $m = |A|$, and $r$ for the number of states reachable from $I$, so $r \le 2^n$.

## The algorithm

```pseudo id=main
FORWARD-SEARCH(A, I, G)
L1  parent ← { I ↦ nil }
L2  Q ← a FIFO queue that holds I
L3  while Q is not empty do
L4      s ← Q.remove-first()
L5      if G ⊆ s then return PLAN(parent, s)
L6      for each a in A do
L7          if pre(a) ⊆ s then
L8              t ← (s \ del(a)) ∪ add(a)
L9              if t is not a key of parent then
L10                 parent[t] ← (s, a)
L11                 Q.add-last(t)
L12 return failure

PLAN(parent, s)
L13 π ← the empty sequence
L14 while parent[s] ≠ nil do
L15     (s, a) ← parent[s]
L16     put a at the front of π
L17 return π
```

The table `parent` is a [hash table](/hash-table/) keyed by states. It is the set of states the search has reached, and it holds for each one the state and action that reached it first. Line L9 is the [duplicate detection](/duplicate-detection/): a state enters the queue at most once. The goal test is at line L5, when a state leaves the queue. A test at line L9, when the state is generated, also gives a plan with the fewest actions in this breadth-first version and saves the last layer, but the cost-ordered variant below needs the test at removal.

With a stack in place of the FIFO queue, the same code searches in depth-first order. It still stops and still returns a valid plan, but the plan can be long. With a priority queue ordered by the path cost $g$, and a state put back when a cheaper path reaches it, it becomes [uniform-cost search](/uniform-cost-search/) on the state graph, which returns a cheapest plan. With $g + h$ it becomes [A*](/a-star-search/).

## Example

The delivery task has one truck, one package and two places. The facts are $t_A$ and $t_B$ (the truck is at $A$ or at $B$) and $p_A$, $p_B$, $p_T$ (the package is at $A$, at $B$ or in the truck). The six actions are tried in this order.

| action | pre | add | del |
| --- | --- | --- | --- |
| drive(A,B) | $t_A$ | $t_B$ | $t_A$ |
| drive(B,A) | $t_B$ | $t_A$ | $t_B$ |
| load(A) | $t_A, p_A$ | $p_T$ | $p_A$ |
| load(B) | $t_B, p_B$ | $p_T$ | $p_B$ |
| unload(A) | $t_A, p_T$ | $p_A$ | $p_T$ |
| unload(B) | $t_B, p_T$ | $p_B$ | $p_T$ |

The initial state is $I = \{t_A, p_A\}$ and the goal is $G = \{p_B\}$. Breadth-first search runs as follows.

| step | state removed (L4) | applicable actions and next states | queue after the step |
| --- | --- | --- | --- |
| 1 | $\{t_A, p_A\}$ | drive(A,B) gives $\{t_B, p_A\}$, new; load(A) gives $\{t_A, p_T\}$, new | $\{t_B, p_A\}$, $\{t_A, p_T\}$ |
| 2 | $\{t_B, p_A\}$ | drive(B,A) gives $\{t_A, p_A\}$, seen | $\{t_A, p_T\}$ |
| 3 | $\{t_A, p_T\}$ | drive(A,B) gives $\{t_B, p_T\}$, new; unload(A) gives $\{t_A, p_A\}$, seen | $\{t_B, p_T\}$ |
| 4 | $\{t_B, p_T\}$ | drive(B,A) gives $\{t_A, p_T\}$, seen; unload(B) gives $\{t_B, p_B\}$, new | $\{t_B, p_B\}$ |
| 5 | $\{t_B, p_B\}$ | $G \subseteq s$: stop | |

The search expands 4 states and generates 7 successors. PLAN follows `parent` back from $\{t_B, p_B\}$ and returns load(A), drive(A,B), unload(B), a plan of 3 actions, the fewest possible. The task has 6 reachable states; the sixth, $\{t_A, p_B\}$, is never generated. With the goal $\{p_A, p_B\}$, which no state contains, the search expands all 6 states and returns failure. The depth-first version expands 3 states on the first goal: after $\{t_A, p_A\}$ it takes the last state pushed, $\{t_A, p_T\}$, and then $\{t_B, p_T\}$.

### Larger tasks

The table gives counts of the implementation on this page for the [blocks world](/blocks-world/) with the four operators pickup, putdown, stack and unstack, a logistics task with one truck, three places and 2 or 3 packages, and the [Tower of Hanoi](/tower-of-hanoi/). The Sussman task starts from C on A with B on the table and has the goal tower A on B on C; the 4-block task goes from the towers A, B and C, D (bottom first) to the tower D, C, B, A.

| task | actions | reachable states | BFS: plan, expanded, generated | DFS: plan, expanded |
| --- | --- | --- | --- | --- |
| Sussman, 3 blocks | 18 | 22 | 6, 21, 41 | 6, 9 |
| 4 blocks | 32 | 125 | 8, 104, 241 | 8, 11 |
| logistics, 2 packages | 18 | 48 | 6, 35, 109 | 10, 10 |
| logistics, 3 packages | 24 | 192 | 9, 168, 600 | 68, 82 |
| Hanoi, 3 disks | 38 | 27 | 7, 25, 73 | 15, 21 |
| Hanoi, 6 disks | 166 | 729 | 63, 675, 2024 | 287, 639 |

Breadth-first search expands most of the reachable states before it finds the goal, because the goal is far from $I$. Depth-first search is sometimes much faster, but on logistics with 3 packages it returns 68 actions where 9 are enough. For $n = 1$ to $6$ disks, breadth-first search on Hanoi returns $2^n - 1$ moves and reaches all $3^n$ states.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). Each state that is a key of `parent` is reachable from $I$, and PLAN returns the actions of a path from $I$ to it, so a returned sequence is a plan (soundness). Each state enters the queue at most once and there are at most $r$ reachable states, so the loop stops. If the search returns failure, every reachable state was a key of `parent`, because along any path from $I$ the first state that never entered the table would have entered it when its predecessor was expanded; so no reachable state contains $G$ (completeness). In breadth-first order the states leave the queue in order of their distance from $I$, and the first state found for each distance is reached by a shortest path, so the plan has the fewest actions. The uniform-cost variant returns a cheapest plan for nonnegative costs by the argument of [Dijkstra's algorithm](/dijkstra/).

## Complexity

**Time.** At most $r$ states are expanded. Expanding one tests $m$ preconditions and builds up to $m$ successors, each in $O(n)$ time with sets of facts held as bit vectors or sorted lists, and each hash lookup costs $O(n)$ to hash a state. So the time is $O(r m n)$ in the worst case, and $O(2^n m n)$ since $r \le 2^n$. The best case is $G \subseteq I$, decided by one test in $O(n)$ time.

**Space.** The table holds up to $r$ states of $O(n)$ bits each, so the space is $O(r n)$. Breadth-first search needs this memory in the worst case, because the queue can hold a whole layer of the state graph.

**Why no polynomial bound.** The bound is exponential in $n$, and it cannot be made polynomial in general. Shortest plans can have $2^{\Omega(n)}$ actions, as in the Tower of Hanoi with $n$ disks and $O(n^2)$ facts, and plan existence is PSPACE-complete ([plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/)). A heuristic changes the number of states expanded, not the worst case.

## Properties

- **Sound.** Every returned sequence is a plan, in every order of the queue.
- **Complete on finite tasks.** Duplicate detection makes it stop on every task, with a plan when one exists and failure when none does. Without duplicate detection it loops on any task with an action that can be undone, such as drive(A,B) and drive(B,A).
- **Step optimal in breadth-first order.** It returns a plan with the fewest actions. This is the cheapest plan only when all costs are equal.
- **Cost optimal with uniform-cost order** and nonnegative costs.
- **Visits only reachable states.** Unlike regression, every node is a real state, so state constraints such as "the truck is at one place" hold in every node, and a heuristic can be computed from a complete state.
- **Deterministic.** The result depends on the order of the actions only through ties.

## Variants and improvements

- **Uniform-cost search.** For action costs, order the queue by $g$ and test the goal at removal; see [uniform-cost search](/uniform-cost-search/) and [optimal planning](/optimal-planning/).
- **A* with an admissible heuristic.** [h-max](/h-max-heuristic/) and the other admissible heuristics of [optimal planning](/optimal-planning/) keep the plan cost optimal and expand fewer states.
- **Greedy and weighted search with an inadmissible heuristic.** [HSP](/hsp-planner/) uses the additive heuristic [h-add](/h-add-heuristic/) with hill climbing (HSP) or with [weighted A*](/weighted-a-star/) (HSP2). [FF](/fast-forward-planner/) uses the [relaxed plan heuristic](/relaxed-plan-heuristic/) with [enforced hill climbing](/enforced-hill-climbing/) and helpful actions, which prune the successors to the actions that a relaxed plan suggests. These planners find plans for much larger tasks but give up optimality.
- **Lazy evaluation.** Compute the heuristic of a state only when it is removed from the queue, with the value of its parent as the key; this saves heuristic calls when the branching factor is large.
- **Pruning of equivalent successors.** Partial order reduction and symmetry reduction remove successors that lead to the same states in another order or to symmetric copies.
- **Depth-first and iterative deepening order.** [Iterative deepening search](/iterative-deepening-search/) gives plans with the fewest actions in memory linear in the plan length, at the cost of repeated states.

## When to use it

Use breadth-first forward search as the reference planner for small tasks, for example to test other planners, and when a plan with the fewest actions is needed and the state space fits in memory. Use the uniform-cost variant when actions have costs. For larger tasks, use forward search with a heuristic: A* with an admissible heuristic when the plan must be optimal, and greedy or weighted search with h-add or the relaxed plan heuristic when any good plan will do. Prefer forward search to backward search when the task has state constraints that regression does not know, as in most benchmark domains.

## Pitfalls

- **Testing equality with the goal.** The goal is a partial description. Test $G \subseteq s$, not $G = s$; in the delivery task no state equals $\{p_B\}$.
- **Applying effects in the wrong order.** The next state is $(s \setminus \mathit{del}) \cup \mathit{add}$. An action that deletes and adds the same fact keeps it under this rule; applying the add list first would remove it. Most formalisms assume that the two lists are disjoint.
- **Testing the goal at generation in a cost order.** With uniform-cost search or A*, a goal state generated by an expensive action can come before a cheaper plan. Test the goal when a state is removed.
- **No duplicate detection.** A forward search without a reached table loops on reversible actions and can repeat a state an exponential number of times even on tasks without cycles.
- **Expecting a short plan from depth-first order.** On logistics with 3 packages, depth-first search returns 68 actions against 9.
- **Hashing mutable sets.** States must be immutable values, such as frozen sets or bit vectors, or the table loses them when they change.

## Implementations

## History

The STRIPS system of Fikes and Nilsson (1971) did not search forward from the initial state: it used a goal-directed method in the style of [means-ends analysis](/means-ends-analysis/), and for many years forward search was thought to be hopeless for planning because of its large branching factor. Ghallab, Nau and Traverso (2004) present forward search as the basic state-space planner and prove it sound and complete. The view changed with heuristic search planning. Bonet, Loerincs and Geffner (1997) computed a domain-independent heuristic from the delete relaxation of the task, and the HSP planner of Bonet and Geffner searched forward with it at the planning competition at AIPS-98. Hoffmann and Nebel's FF planner (2001) added the relaxed plan heuristic and enforced hill climbing. Since then most planners of the [International Planning Competition](/international-planning-competition/) are forward search planners with heuristics.

## References
