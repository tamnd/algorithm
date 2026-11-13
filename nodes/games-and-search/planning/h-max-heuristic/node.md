---
tag: 7HHW76
kind: technique
slug: h-max-heuristic
name: h-max heuristic
aliases:
- hmax
area: games-and-search/planning
level: advanced
summary: Gives each fact the cost of its cheapest relaxed derivation, where an action costs its own cost plus its most expensive precondition, and takes the max over the goal. Admissible and consistent.
prereqs: [delete-relaxation, dijkstra]
see_also: [h-add-heuristic, hsp-planner, relaxed-planning-graph, landmark-heuristic, admissible-heuristic, consistent-heuristic, bellman-ford, a-star-search]
sources:
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (the fact costs of the relaxed problem; the max form of the heuristic and its admissibility)
  - paper: doi:10.1016/0020-0190(77)90002-3
    title: "Donald E. Knuth, A generalization of Dijkstra's algorithm, Information Processing Letters 6(1) (1977)"
    locator: the whole paper (shortest derivations in a grammar with superior cost functions; max plus a constant is one)
  - paper: doi:10.1609/icaps.v19i1.13370
    title: "Malte Helmert and Carmel Domshlak, Landmarks, critical paths and abstractions: What's the difference anyway?, ICAPS 2009"
    locator: the definition of the h-max values and of LM-cut, which is built on them
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.3 (heuristics for planning)
---

The h-max heuristic estimates the distance from a state $s$ to the goal of a [STRIPS](/strips/) task in the [delete relaxation](/delete-relaxation/). It gives each fact $p$ a cost $g_s(p)$: zero if $p$ is true in $s$, and otherwise the cheapest way to make $p$ true, where an action costs its own cost plus the cost of its *most expensive* precondition. The value of the state is the cost of its most expensive goal fact, $h_{\max}(s) = \max_{p \in G} g_s(p)$. Taking the maximum and not the sum means that h-max never counts the same work twice, so it is [admissible](/admissible-heuristic/) and [consistent](/consistent-heuristic/), and $h_{\max} \le h^+ \le h^*$. The fact costs come from a variant of [Dijkstra's algorithm](/dijkstra/) in time close to linear in the size of the task. The price is weak guidance: h-max sees only the longest chain of the plan and ignores all the work beside it. Bonet and Geffner defined it next to the sum form used by their planner [HSP](/hsp-planner/). The sum form, which is more informative but not admissible, is [h-add](/h-add-heuristic/).

## In plain words

To guess how far a state is from the goal, forget that actions can undo things. Then ask, for each fact you need, how soon you could have it. A fact you already have costs nothing. Any other fact costs the price of the cheapest action that makes it, plus the price of that action's most expensive need, because you must wait for its slowest need.

The guess for the state is the price of the most expensive goal fact. The real plan must make that fact too, and it cannot do it more cheaply, so the guess is never too high. It is often much too low, because it only follows one chain of needs and ignores the other goals.

## When it applies

- The task is a ground STRIPS task $(F, A, I, G)$ with nonnegative action costs $c(a)$, so a [delete relaxation](/delete-relaxation/) is defined. Negative preconditions must first be compiled into positive facts.
- The search needs an admissible heuristic, for example [A*](/a-star-search/) for optimal planning, or a fast test for dead ends: $h_{\max}(s) = \infty$ exactly when the relaxed task from $s$ has no plan.
- h-max is a building block more often than a heuristic on its own. LM-cut, h-add and the relaxed plans of [FF](/fast-forward-planner/) all start from the same kind of fact costs.

## The template

A *relaxed derivation* of a fact $p$ from a state $s$ is a finite tree. Either it is the single leaf $p$, which is allowed when $p \in s$, or its root is an action $a$ with $p \in \mathit{add}(a)$, and it has one child derivation for each $q \in \mathit{pre}(a)$. The *weight* of a root to leaf path is the sum of the costs of the actions on it, and the *weight* of the derivation is the largest weight of its paths. Define

$$g_s(p) = \min\{\text{weight of } T : T \text{ is a relaxed derivation of } p \text{ from } s\}, \qquad h_{\max}(s) = \max_{p \in G} g_s(p),$$

with $g_s(p) = \infty$ when $p$ has no derivation and $h_{\max}(s) = 0$ when $G = \emptyset$. Splitting a derivation at its root gives the equations

$$g_s(p) = 0 \text{ if } p \in s, \qquad g_s(p) = \min_{a : p \in \mathit{add}(a)} \Big( c(a) + \max_{q \in \mathit{pre}(a)} g_s(q) \Big) \text{ otherwise},$$

where the max over an empty set is 0. H-MAX computes $g_s$ as Knuth's generalization of Dijkstra's algorithm. A fact is *fixed* when its value is final, and an action *fires* when the last of its preconditions is fixed.

```pseudo id=main
H-MAX(s, G, A)
L1  g(p) ← ∞ for every fact p                         ▷ no fact is fixed yet
L2  Q ← a priority queue that holds (p, 0) for every p ∈ s
L3  for each a in A do waiting(a) ← |pre(a)|
L4  for each a in A with pre(a) = ∅ do insert (r, c(a)) into Q for every r ∈ add(a)
L5  while Q is not empty do
L6      (p, v) ← REMOVE-MIN(Q)
L7      if g(p) < ∞ then continue                      ▷ p is already fixed
L8      g(p) ← v                                       ▷ fix p
L9      for each a in A with p ∈ pre(a) do
L10         waiting(a) ← waiting(a) − 1
L11         if waiting(a) = 0 then                     ▷ a fires: p is its last precondition
L12             for each r ∈ add(a) with g(r) = ∞ do insert (r, v + c(a)) into Q
L13 return max over p ∈ G of g(p), or 0 if G = ∅
```

**Removed keys never decrease.** Every key inserted at line L12 is $v + c(a) \ge v$, where $v$ is the key just removed, and every key already in $Q$ is at least $v$ because $v$ was the minimum. So the keys that line L6 removes form a nondecreasing sequence. In particular, when an action fires at line L11, all its preconditions are fixed and $v$ is the largest of their values, so $v + c(a) = c(a) + \max_{q \in \mathit{pre}(a)} g(q)$.

**Every fixed value is the weight of a derivation.** By induction on the order in which facts are fixed. A fact fixed with an entry from line L2 is in $s$ and has the derivation that is a leaf, of weight 0. An entry from line L4 for $r$ gives the derivation with root $a$ and no children, of weight $c(a)$. An entry from line L12 for $r$ has key $c(a) + \max_q g(q)$ over the preconditions of $a$, which were fixed earlier; by the induction hypothesis each $g(q)$ is the weight of a derivation of $q$, and these derivations under the root $a$ form a derivation of $r$ of weight $c(a) + \max_q g(q)$. So $g(p) \ge g_s(p)$ for every fixed $p$.

**Every derivable fact is fixed at its least weight.** Let $T$ be a derivation of $p$ of weight $w$. We show by induction on the height of $T$ that $p$ is fixed with $g(p) \le w$. If $T$ is a leaf, $(p, 0)$ is inserted at line L2. Otherwise let $a$ be the root. If $\mathit{pre}(a) = \emptyset$, then $(p, c(a))$ is inserted at line L4 and $w \ge c(a)$. Otherwise, by the induction hypothesis every precondition $q$ is fixed with $g(q) \le w - c(a)$, so $a$ fires when the last of them is fixed, with $v = \max_q g(q) \le w - c(a)$. If $p$ was fixed before that moment, then $g(p) \le v \le w$, because removed keys never decrease. If not, line L12 inserts $(p, v + c(a))$ with $v + c(a) \le w$. The loop runs until $Q$ is empty, so this entry is removed at some time, and the entry for $p$ that is removed first, which fixes $p$, comes no later and has a key no larger. So $g(p) \le w$ in every case. With the previous paragraph, $g(p) = g_s(p)$ for every fact, and a fact that is never fixed has no derivation, so $g(p) = g_s(p) = \infty$. Line L13 then returns $h_{\max}(s)$.

**Cost.** Each action fires at most once, because $\mathit{waiting}(a)$ reaches 0 once, so $Q$ receives at most $|s| + \sum_a |\mathit{add}(a)|$ entries, and lines L9 and L10 run $\sum_a |\mathit{pre}(a)|$ times in total. With a [binary heap](/binary-heap/) and $L = |F| + \sum_a (|\mathit{pre}(a)| + |\mathit{add}(a)|)$, the time is $O(L \log L)$ and the space is $O(L)$. With unit costs, a bucket queue makes it $O(L)$.

**h-max is admissible.** Let $a_1, \ldots, a_k$ be a relaxed plan from $s$, with relaxed states $r_0 = s$ and $r_i = r_{i-1} \cup \mathit{add}(a_i)$, and let $C_i = c(a_1) + \cdots + c(a_i)$. By induction on $i$, every $p \in r_i$ has $g_s(p) \le C_i$: facts of $s$ have value 0, and a fact added by $a_i$ has $g_s(p) \le c(a_i) + \max_{q \in \mathit{pre}(a_i)} g_s(q) \le c(a_i) + C_{i-1} = C_i$, by the equations and because $\mathit{pre}(a_i) \subseteq r_{i-1}$. The goal is in $r_k$, so $h_{\max}(s) \le C_k$. This holds for every relaxed plan, so $h_{\max}(s) \le h^+(s) \le h^*(s)$.

**h-max detects exactly the relaxed dead ends.** If $g_s(p) < \infty$, the actions of a derivation of $p$, listed so that each comes after the actions of its subtrees, form a relaxed plan that makes $p$ true. Concatenate such plans for all goal facts. So $h_{\max}(s) < \infty$ exactly when $h^+(s) < \infty$.

**h-max is consistent.** Let $a$ apply in $s$ and let $s' = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. Take a derivation $T'$ of $p$ from $s'$. Each leaf $q$ of $T'$ is in $s'$, so either $q \in s$, and the leaf is also allowed from $s$, or $q \in \mathit{add}(a)$, and we replace the leaf by the node $a$ with the leaves $\mathit{pre}(a) \subseteq s$ below it. The result is a derivation of $p$ from $s$, and each path gains at most $c(a)$. So $g_s(p) \le c(a) + g_{s'}(p)$ for every $p$, and taking the max over $G$ gives $h_{\max}(s) \le c(a) + h_{\max}(s')$. Also $h_{\max}(s) = 0$ when $G \subseteq s$.

**The values by rounds of updates.** A [Bellman-Ford](/bellman-ford/) style loop that starts with 0 on $s$ and $\infty$ elsewhere, and in each round applies the equation to every fact, reaches $g_s$ after at most $|F|$ rounds plus one round that changes nothing. If a fact repeats on a path of a derivation, the lower subtree can replace the upper one without making any path heavier, because costs are nonnegative. So some least weight derivation has no repeated fact on a path and has height at most $|F|$, and after round $k$ every fact with a least weight derivation of height at most $k$ has its final value. The total time is $O(|F| \cdot L)$, worse than H-MAX, but the loop is simpler and it is how h-max is often first explained.

**Unit costs give the layers of the relaxed planning graph.** When every action costs 1, the weight of a derivation is its height, and a fact is in layer $k$ of the [relaxed planning graph](/relaxed-planning-graph/) exactly when it has a derivation of height at most $k$. So $g_s(p)$ is the index of the first layer that contains $p$, and $h_{\max}(s)$ is the index of the first layer that contains the whole goal.

## Classic examples

### One truck, one package

The truck and the package are at A, and the package must go to B. From $\{t_A, p_A\}$, H-MAX fixes $t_A$ and $p_A$ at 0. Then drive(A,B) and load(A) fire and give $t_B$ and $p_T$ (the package in the truck) the value 1. Then unload(B), whose preconditions $t_B$ and $p_T$ both have value 1, gives $p_B$ the value $1 + \max(1, 1) = 2$. So $h_{\max} = 2$, while the real plan load, drive, unload has 3 actions. The maximum treats the drive and the load as if they happened at the same time.

### Two packages

With two packages that must both go from A to B, the values are 0 for $t_A$, $p_1@A$ and $p_2@A$, 1 for $t_B$, $p_1@T$ and $p_2@T$, and 2 for $p_1@B$ and $p_2@B$. So $h_{\max} = 2$, while $h^+ = h^* = 5$. A second package does not change h-max at all.

### The Sussman task

Start from C on A with A and B on the table and the hand empty, with the goal $\{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$ and the four [blocks world](/blocks-world/) actions at cost 1. The facts of the initial state have value 0. Unstack(C,A) and pickup(B) give the value 1 to clear(A), holding(C) and holding(B). Then pickup(A), stack(B,C), stack(B,A), stack(C,B) and putdown(C) give the value 2 to holding(A), on(B,C), on(B,A), on(C,B) and ontable(C). Last, stack(A,B) and stack(A,C) give on(A,B) and on(A,C) the value 3. So $h_{\max} = \max(3, 2) = 3$, while $h^+ = 5$ and $h^* = 6$.

### Independent goals

Take $n$ goal facts $g_1, \ldots, g_n$, each made by its own action with no precondition and cost 1. Then every $g_s(g_i) = 1$ and $h_{\max} = 1$, while $h^+ = h^* = n$. The ratio $h^*/h_{\max}$ can be as large as the number of goals, which is why h-max alone guides search poorly.

### The Tower of Hanoi

With $n$ disks and the goal of the whole tower on the third peg, h-max is $n$, the same as $h^+$, while $h^* = 2^n - 1$. For $n = 1, 2, 3, 4$ the values are 1, 2, 3, 4 against 1, 3, 7, 15. Here the error comes from the relaxation, not from the maximum: each disk needs only one relaxed move.

## Variations

- **h-add.** Replace the max over preconditions and goals by a sum. [h-add](/h-add-heuristic/) is much more informative and is the heuristic of HSP, but it counts shared work more than once and is not admissible. The same Dijkstra loop computes it, with an action firing at its last precondition and the sum of the precondition values taken at that point.
- **The $h^m$ family.** Haslum and Geffner (2000) define $h^m$ by the same kind of equations over sets of at most $m$ facts: a set costs as much as its most expensive subset of size $m$. h-max is $h^1$. $h^2$ notices pairs of facts that cannot hold together, close to the mutex relations of [Graphplan](/graphplan/). For a fixed $m$ the values are still computed in polynomial time, because there are $O(|F|^m)$ fact sets.
- **LM-cut.** Compute h-max, take for each action a precondition with the largest value, and cut the graph of these supporters in front of the goal. The cut is a disjunctive action landmark. Subtract its least cost from its actions and repeat until h-max is 0. The sum of the cut costs is an admissible heuristic between $h_{\max}$ and $h^+$, and it is one of the strongest [landmark heuristics](/landmark-heuristic/).
- **Regression form.** HSPr evaluates states of a [backward search](/backward-state-space-search/) by one table of fact costs computed once from the initial state: the estimate of a subgoal $S$ is $\max_{p \in S} g_I(p)$. This saves the Dijkstra run for each state.
- **Bellman-Ford form.** The rounds of updates above need no priority queue and are easy to run with many actions in parallel, at a higher sequential cost.

## Pitfalls

- **Reading "max" as "the cost of the most expensive action".** The max is over preconditions and over goals, inside a recursion. A fact can have a large value even when every action is cheap, because a long chain of preconditions adds up.
- **Firing an action before all its preconditions are fixed.** If the queue gets $c(a) + g(q)$ as soon as one precondition $q$ is fixed, the value of the added fact can be too low. The waiting counter of line L10 makes the action wait for its last precondition, which then carries the largest value.
- **Negative costs.** The proof that removed keys never decrease needs $c(a) \ge 0$. With negative costs, use rounds of updates, and note that a negative cycle of derivations makes the values undefined.
- **Expecting good guidance.** h-max is admissible and cheap, but on tasks with many independent goals it is close to 1 everywhere. Greedy best first search with h-max alone is usually poor.
- **Treating a finite value as solvable.** $h_{\max}(s) < \infty$ only says that the relaxed task is solvable. The real task can still be a dead end.

## Exercises

1. Run H-MAX on the two-package task and list the order in which the facts are fixed. Which actions fire, and in which iteration of line L5?
2. Give a task with unit costs where $h_{\max}(s) = 1$ and $h^*(s) = 10$, and one where $h_{\max}(s) = h^*(s) = 10$.
3. Show that $s \supseteq s'$ implies $h_{\max}(s) \le h_{\max}(s')$.
4. Modify line L12 so that it inserts $c(a) + \sum_{q \in \mathit{pre}(a)} g(q)$. Show that the result is h-add, and find the step of the correctness argument that changes.
5. With unit costs, show that $h_{\max}(s) = k$ exactly when the goal first appears in layer $k$ of the relaxed planning graph built from $s$.

## References
