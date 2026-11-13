---
tag: FN069M
kind: technique
slug: h-add-heuristic
name: h-add heuristic
aliases:
- additive heuristic
- hadd
area: games-and-search/planning
level: advanced
summary: Gives each fact the cost of its cheapest relaxed derivation, counting all preconditions, and sums over the goal. Informative but not admissible, and h+ is at most h-add.
prereqs: [delete-relaxation, h-max-heuristic]
see_also: [hsp-planner, relaxed-plan-heuristic, fast-forward-planner, greedy-best-first-search, weighted-a-star, relaxed-planning-graph, admissible-heuristic, set-cover]
sources:
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (the additive heuristic of HSP, its assumption of independent subgoals, and the planners HSP and HSPr)
  - paper: doi:10.1016/0020-0190(77)90002-3
    title: "Donald E. Knuth, A generalization of Dijkstra's algorithm, Information Processing Letters 6(1) (1977)"
    locator: the whole paper (shortest derivations in a grammar with superior cost functions; a sum of the arguments plus a constant is one)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.3 (heuristics for planning)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on heuristic search planning (the additive and max heuristics; general locator)
---

The h-add heuristic, also called the additive heuristic, estimates the distance from a state $s$ to the goal of a [STRIPS](/strips/) task in the [delete relaxation](/delete-relaxation/). Like [h-max](/h-max-heuristic/), it gives each fact $p$ a cost $g_s(p)$: zero if $p$ is true in $s$, and otherwise the cheapest way to make $p$ true. The difference is that an action costs its own cost plus the *sum* of the costs of its preconditions, and the state costs the sum over the goal facts, $h_{\mathrm{add}}(s) = \sum_{p \in G} g_s(p)$. The sum assumes that the subgoals are independent, so that no action helps two of them. When that is true the estimate is good, and when two subgoals share work it counts that work twice. So h-add is not [admissible](/admissible-heuristic/), but it is never below the optimal relaxed cost $h^+$, it detects the same dead ends, and it guides greedy search far better than h-max. It was the heuristic of the planner [HSP](/hsp-planner/) of Bonet and Geffner, and its best supporters give [relaxed plans](/relaxed-plan-heuristic/) like those of [FF](/fast-forward-planner/).

## In plain words

To guess how far a state is from the goal, forget that actions can undo things. A fact you already have costs nothing. Any other fact costs the price of the cheapest action that makes it, plus the prices of all the facts that action needs. The guess for the state is the sum of the prices of the goal facts.

This is like pricing each goal on its own and adding the bills. If two goals need the same trip, the trip is on both bills, so the guess can be too high. But it notices every goal and every need, so it tells a search well which states are closer to the goal.

## When it applies

- The task is a ground STRIPS task $(F, A, I, G)$ with nonnegative action costs $c(a)$, so the delete relaxation is defined. Negative preconditions must first be compiled into positive facts.
- The search does not need optimal plans: [greedy best first search](/greedy-best-first-search/), [weighted A*](/weighted-a-star/) or [hill climbing](/hill-climbing/) for satisficing planning. For optimal plans with [A*](/a-star-search/), use an admissible heuristic such as h-max or LM-cut.
- The subgoals are weakly coupled, as in logistics tasks with many packages. When many goals share a long chain of preconditions, h-add overestimates by a large factor.

## The template

A *relaxed derivation* of a fact $p$ from a state $s$ is a finite tree, as on the [h-max](/h-max-heuristic/) page: the single leaf $p$ when $p \in s$, or a root action $a$ with $p \in \mathit{add}(a)$ and one child derivation for each $q \in \mathit{pre}(a)$. Its *total weight* is the sum of the costs of all its action nodes, so that an action that occurs twice in the tree is counted twice. Define

$$g_s(p) = \min\{\text{total weight of } T : T \text{ is a relaxed derivation of } p \text{ from } s\}, \qquad h_{\mathrm{add}}(s) = \sum_{p \in G} g_s(p),$$

with $g_s(p) = \infty$ when $p$ has no derivation. Splitting a derivation at its root gives the equations

$$g_s(p) = 0 \text{ if } p \in s, \qquad g_s(p) = \min_{a : p \in \mathit{add}(a)} \Big( c(a) + \sum_{q \in \mathit{pre}(a)} g_s(q) \Big) \text{ otherwise}.$$

H-ADD is the loop of H-MAX with a sum in place of the max. It also records a *best supporter* $\mathrm{sup}(p)$, the action whose entry fixed $p$. BEST-SUPPORTER-PLAN follows the supporters back from the goal and returns a relaxed plan.

```pseudo id=main
H-ADD(s, G, A)
L1  g(p) ← ∞ and sup(p) ← none for every fact p
L2  Q ← a priority queue that holds (p, 0, none) for every p ∈ s
L3  for each a in A do waiting(a) ← |pre(a)|
L4  for each a in A with pre(a) = ∅ do insert (r, c(a), a) into Q for every r ∈ add(a)
L5  while Q is not empty do
L6      (p, v, b) ← REMOVE-MIN(Q)
L7      if g(p) < ∞ then continue                      ▷ p is already fixed
L8      g(p) ← v; sup(p) ← b                            ▷ fix p, with supporter b
L9      for each a in A with p ∈ pre(a) do
L10         waiting(a) ← waiting(a) − 1
L11         if waiting(a) = 0 then                     ▷ a fires: all its preconditions are fixed
L12             w ← c(a) + Σ over q ∈ pre(a) of g(q)
L13             for each r ∈ add(a) with g(r) = ∞ do insert (r, w, a) into Q
L14 return Σ over p ∈ G of g(p)

BEST-SUPPORTER-PLAN(s, G, A)
L15 run lines L1 to L13; if g(p) = ∞ for some p ∈ G then return failure
L16 N ← the supporters reached from G: for each reached fact p with sup(p) ≠ none, add sup(p) to N and reach pre(sup(p))
L17 return the actions of N, each placed at the first time that it fixed a fact
```

**Removed keys never decrease.** When $a$ fires at line L11 because its last precondition $p$ was fixed with value $v$, the key $w = c(a) + \sum_q g(q) \ge g(p) = v$, because all terms are nonnegative. Every key already in $Q$ is at least $v$. So the keys that line L6 removes form a nondecreasing sequence.

**The loop computes $g_s$.** The argument is the one for H-MAX with sums. Each fixed value is the total weight of a derivation: the tree with root $\mathrm{sup}(p)$ over the derivations of its preconditions, which were fixed earlier, has total weight $c(a) + \sum_q g(q)$. Conversely, for a derivation $T$ of $p$ with root $a$ and total weight $w$, induction on the height gives $g(q) \le w_q$ for each child of total weight $w_q$, and $a$ fires with key $c(a) + \sum_q g(q) \le c(a) + \sum_q w_q = w$. If $p$ was fixed earlier, its value is at most that key, because removed keys never decrease; if not, the entry fixes $p$ at a value at most $w$. So $g(p) = g_s(p)$ for every fact, and line L14 returns $h_{\mathrm{add}}(s)$.

**Cost.** As for H-MAX: each action fires once, and with a [binary heap](/binary-heap/) the time is $O(L \log L)$ for $L = |F| + \sum_a (|\mathit{pre}(a)| + |\mathit{add}(a)|)$. Line L12 reads each precondition once, so it adds $O(L)$ in total. BEST-SUPPORTER-PLAN adds $O(L)$.

**The best supporter plan is a relaxed plan.** If $\mathrm{sup}(p) = b \neq$ none, then $b$ fired before $p$ was fixed, so every precondition of $b$ was fixed before $p$. If $\mathrm{sup}(p) =$ none, then $p \in s$. Let $b \in N$ be placed at the first fact $p$ that it fixed, and let $q \in \mathit{pre}(b)$ with supporter $b' \in N$. Then $q$ was fixed before $p$, so $b'$ fixed a fact no later than $q$, and $b'$ is placed before $b$. So in the order of line L17, each precondition of each action is in $s$ or added by an earlier action, and every goal fact is in $s$ or added by its supporter. The list is a relaxed plan from $s$.

**$h^+ \le h_{\mathrm{add}}$.** For a fixed fact $p$, unfold the supporters into the derivation $T_p$: the leaf $p$ if $\mathrm{sup}(p) =$ none, and otherwise the root $\mathrm{sup}(p)$ over the trees $T_q$ for its preconditions. By induction in the order of fixing, the total weight of $T_p$ is $g(p)$. The actions of $N$ are exactly the action nodes of the trees $T_p$ for $p \in G$, and each of them occurs at least once there. So the cost of the best supporter plan, which uses each action of $N$ once, is at most $\sum_{p \in G} g(p) = h_{\mathrm{add}}(s)$. That plan is a relaxed plan, so $h^+(s) \le \mathrm{cost}(N) \le h_{\mathrm{add}}(s)$. With h-max: $h_{\max}(s) \le h^+(s) \le h_{\mathrm{add}}(s)$, and all three are infinite exactly when the relaxed task from $s$ has no plan.

**h-add is not admissible, and not consistent.** Take one action with no precondition that adds both goal facts $g_1$ and $g_2$ at cost 1. Then $g_s(g_1) = g_s(g_2) = 1$ and $h_{\mathrm{add}} = 2$, while $h^* = 1$. A heuristic that is consistent and is 0 on goal states is admissible, and h-add is 0 on goal states, so it cannot be consistent either.

**The overestimate has no constant bound.** Take a chain $k_0 \to k_1 \to \cdots \to k_L$ of unit actions, with $k_0 \in s$, and $n$ goal facts $g_1, \ldots, g_n$, each added by a unit action with the precondition $k_L$. Each goal fact has $g_s(g_i) = L + 1$, so $h_{\mathrm{add}} = n (L + 1)$, while $h^+ = h^* = L + n$. With $L = n$ the ratio is $(n + 1)/2$.

## Classic examples

The table compares the heuristics on the initial states of small tasks with unit costs. The tasks are those of the [delete relaxation](/delete-relaxation/) page, and the logistics task has one truck at A, three places that are all connected, a package p0 from A to B and a package p1 from B to C.

| Task | $h_{\max}$ | $h_{\mathrm{add}}$ | $h^+$ | $h^*$ |
| --- | --- | --- | --- | --- |
| One truck, one package from A to B | 2 | 3 | 3 | 3 |
| One truck, two packages from A to B | 2 | 6 | 5 | 5 |
| Logistics with two packages | 3 | 7 | 6 | 6 |
| Sussman task | 3 | 5 | 5 | 6 |
| Tower of Hanoi, 4 disks | 4 | 4 | 4 | 15 |
| Chain with $L = 4$ and $n = 5$ goals | 5 | 25 | 9 | 9 |

### One truck, one package

From $\{t_A, p_A\}$, drive(A,B) gives $t_B$ the value 1, and load(A) gives the package in the truck, $p_T$, the value 1. Unload(B) needs both, so $p_B$ gets $1 + 1 + 1 = 3$, and $h_{\mathrm{add}} = 3 = h^*$. Here the sum is exact, because the drive and the load are separate work. h-max gives 2 on the same task.

### Two packages

With two packages, $p_1@B$ and $p_2@B$ each get the value 3, so $h_{\mathrm{add}} = 6$, while $h^* = 5$. The drive to B is on the bill of both packages. The best supporters are drive(A,B), load(p1,A), load(p2,A), unload(p1,B) and unload(p2,B), and BEST-SUPPORTER-PLAN puts the drive once, so its plan costs 5.

### The Sussman task

In the [blocks world](/blocks-world/), from C on A with A and B on the table and the goal $\{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$, the values are 1 for clear(A), holding(B) and holding(C), 2 for holding(A), on(B,C), on(C,B) and ontable(C), and 3 for on(A,B), on(A,C) and on(B,A). So $h_{\mathrm{add}} = 3 + 2 = 5 = h^+$, while $h^* = 6$. The best supporter plan is pickup(B), unstack(C,A), stack(B,C), pickup(A), stack(A,B), a relaxed plan of cost 5 that is not applicable in the real task: it unstacks C while the hand holds B.

### Shared chains

In the chain task above with $L = 4$ and $n = 5$, every goal fact costs 5, so $h_{\mathrm{add}} = 25$, while the plan that walks the chain once and then makes the five goals has 9 actions. The best supporter plan finds those 9 actions, so its cost is a much better estimate than the sum, which is the main idea of the relaxed plan heuristic.

## Variations

- **Relaxed plan heuristics.** Take the cost of the best supporter plan, or of a relaxed plan extracted from the [relaxed planning graph](/relaxed-planning-graph/), instead of the sum. Each action is then counted once, the estimate is between $h^+$ and $h_{\mathrm{add}}$, and it still costs about one run of H-ADD. FF chooses supporters by the layers of the relaxed planning graph, which are the h-max values for unit costs. Choosing them by the h-add values, as BEST-SUPPORTER-PLAN does, takes the action costs into account.
- **Set-additive heuristic.** Keyder and Geffner propagate, for each fact, a set of actions that achieves it, and take the cost of the union of the sets of the goal facts. This counts each action once at the cost of larger labels.
- **Regression form.** HSPr computes $g_I$ once from the initial state and evaluates a subgoal $S$ of a [backward search](/backward-state-space-search/) by $\sum_{p \in S} g_I(p)$, which saves a run of H-ADD for each state.
- **Bellman-Ford form.** Repeat the update of the equations over all actions until nothing changes. The first HSP computed its values in this style. The result is the same, by the argument given for h-max.
- **Weighted sums.** Since h-add already overestimates, it is usually used with greedy best first search. Used with A*, it gives no guarantee on the cost of the plan.

## Pitfalls

- **Using h-add with A* for optimal plans.** It overestimates, so A* with h-add can return plans that are not optimal, as the action that adds two goals shows.
- **Firing an action before all its preconditions are fixed.** Line L12 needs the final value of every precondition. The waiting counter makes the action wait for the last of them; the key is then a sum of final values.
- **Counting the supporter plan as h-add.** The best supporter plan uses each action once, so its cost can be far below $h_{\mathrm{add}}$, as in the chain task. Keep the two numbers apart, and do not claim admissibility for either.
- **Ties between supporters.** When two actions give the same key, the supporter depends on the order of the queue. The value of $g$ does not, but the supporter plan, and its cost, can.
- **Treating a finite value as solvable.** $h_{\mathrm{add}}(s) < \infty$ only says that the relaxed task is solvable. The real task can still be a dead end.

## Exercises

1. Give a task with unit costs and two goal facts where $h_{\mathrm{add}}(s) = h^*(s)$, and one where $h_{\mathrm{add}}(s) = 2 h^*(s)$.
2. Show that $h_{\max}(s) \le h_{\mathrm{add}}(s) \le |G| \cdot \max_{p \in G} g_s(p)$, where $g_s$ is the h-add fact cost.
3. Show that when every action has a positive cost, $h_{\mathrm{add}}(s) = 0$ exactly when $G \subseteq s$. Give a task with a cost 0 action where this fails.
4. On the two-package task, list the facts in the order in which H-ADD fixes them, with their supporters, and check that line L17 gives a relaxed plan of cost 5.
5. Show that $h_{\max} = h_{\mathrm{add}} = h^+$ when the goal has one fact and every action has at most one precondition.

## References
