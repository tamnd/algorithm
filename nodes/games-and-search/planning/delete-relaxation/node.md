---
tag: JJ5Q8N
kind: technique
slug: delete-relaxation
name: Delete relaxation
aliases:
- relaxed planning problem
area: games-and-search/planning
level: core
summary: Drops every delete list of a STRIPS task. Relaxed plans exist exactly when a fixed point reaches the goal, and the optimal relaxed cost h+ is an admissible but NP-hard heuristic.
prereqs: [strips, classical-planning, relaxation-heuristic]
see_also: [h-max-heuristic, h-add-heuristic, relaxed-plan-heuristic, relaxed-planning-graph, hsp-planner, fast-forward-planner, landmark-heuristic, set-cover]
sources:
  - paper: doi:10.1016/S0004-3702(01)00108-4
    title: "Blai Bonet and Hector Geffner, Planning as heuristic search, Artificial Intelligence 129(1-2) (2001)"
    locator: pp. 5 to 33 (the relaxed problem without delete lists, and the heuristics h-add and h-max derived from it)
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: Section 4 (bounded plan existence; NP-completeness for operators with only positive postconditions, Corollary 4.3)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.3 (heuristics for planning, the ignore-delete-lists heuristic)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on heuristic search planning (delete relaxation; general locator)
---

The delete relaxation of a [STRIPS](/strips/) task keeps the facts, the initial state, the goal and the actions, but removes every delete list. In the relaxed task a fact, once true, stays true, so the state only grows. Two things follow. First, every real plan is also a relaxed plan, so the cost of an optimal relaxed plan, written $h^+$, is a lower bound on the real optimal cost $h^*$: an admissible heuristic. If the relaxed task has no plan, the real task has none either. Second, whether a relaxed plan exists can be decided in polynomial time by a simple fixed point. Finding an optimal relaxed plan is still NP-hard, so planners approximate $h^+$: [h-max](/h-max-heuristic/) from below, [h-add](/h-add-heuristic/) from above, and the [relaxed plan heuristic](/relaxed-plan-heuristic/) of FF by a plan that is not always optimal. Most heuristics of classical planning come from this one relaxation. The general idea of a heuristic from a relaxed problem is on [relaxation heuristic](/relaxation-heuristic/); this page is about the special case of deletes.

## In plain words

Imagine a world where nothing is ever used up. If you drive a truck from A to B, the truck is now at B, but it is also still at A. If you pick up a block, the block is in your hand, but it also stays on the table. In such a world planning is much easier, because no step can undo another one.

A plan for the real world still works in this easy world, so the easy world never needs more steps. That makes its cost a safe lower estimate. You can tell quickly whether the easy world has a plan: keep doing every step you can, until nothing new comes true. Finding the cheapest plan in the easy world is still hard.

## When it applies

- The task is a ground STRIPS task $(F, A, I, G)$ with nonnegative action costs, or a task that [grounding](/grounding/) makes into one. The relaxation needs preconditions and goals that are sets of positive facts; negative preconditions are first compiled into new positive facts.
- A planner needs an estimate of the distance from a state to the goal, for search ([HSP](/hsp-planner/), [FF](/fast-forward-planner/)) or for pruning: a state from which the relaxed task has no plan is a dead end.
- The relaxation is informative when actions mainly *produce* things, as in logistics, and weak when the plan must undo or consume, as in puzzles where every move is reversible. In the Tower of Hanoi, for example, the relaxed plan ignores that a disk leaves its peg, and with 4 disks $h^+ = 4$ while $h^* = 15$.

## The template

```pseudo id=main
RELAX(A)
L1  return { (pre(a), add(a), ∅, c(a)) : a ∈ A }

RELAXED-REACHABLE(s, A)                 ▷ the facts that some relaxed plan from s makes true
L2  R ← s
L3  repeat
L4      for each a in A do
L5          if pre(a) ⊆ R and add(a) ⊄ R then
L6              R ← R ∪ add(a)
L7  until a whole pass of lines L4 to L6 left R unchanged
L8  return R

RELAXED-SOLVABLE(s, G, A)
L9  return G ⊆ RELAXED-REACHABLE(s, A)
```

In the relaxed task, an action $a$ applies in $s$ when $\mathit{pre}(a) \subseteq s$, and the next state is $s \cup \mathit{add}(a)$. A relaxed plan from $s$ is a sequence that is applicable in this sense and ends in a state that contains $G$. Write $h^+(s)$ for the least cost of a relaxed plan from $s$, and $\infty$ if none exists.

**Every plan is a relaxed plan.** Let $a_1, \ldots, a_k$ be a plan from $s$, with real states $s_i = (s_{i-1} \setminus \mathit{del}(a_i)) \cup \mathit{add}(a_i)$ and relaxed states $r_i = r_{i-1} \cup \mathit{add}(a_i)$, $s_0 = r_0 = s$. By induction $s_i \subseteq r_i$: if $s_{i-1} \subseteq r_{i-1}$, then $\mathit{pre}(a_i) \subseteq s_{i-1} \subseteq r_{i-1}$, so $a_i$ applies in the relaxed task, and $s_i \subseteq s_{i-1} \cup \mathit{add}(a_i) \subseteq r_i$. So $G \subseteq s_k \subseteq r_k$. Hence $h^+(s) \le h^*(s)$, and $h^+(s) = \infty$ implies $h^*(s) = \infty$.

**The fixed point is exact.** Let $R^*$ be the set that RELAXED-REACHABLE returns. The actions in the order in which line L6 fires them form a relaxed plan that ends in $R^*$, so every fact of $R^*$ is reachable. Conversely, along any relaxed plan $a_1, \ldots, a_k$ from $s$, every relaxed state is a subset of $R^*$, by induction: $r_0 = s \subseteq R^*$, and if $r_{i-1} \subseteq R^*$ then $\mathit{pre}(a_i) \subseteq R^*$, so $\mathit{add}(a_i) \subseteq R^*$, or the last pass of the loop would have changed $R$. So a relaxed plan exists exactly when $G \subseteq R^*$.

**Cost of the fixed point.** Each pass except the last adds at least one fact, so there are at most $n + 1$ passes for $n = |F|$, and a pass costs $O(m n)$ for $m = |A|$. That is $O(m n^2)$. With a counter of unmet preconditions for each action and a queue of new facts, the same set is computed in time linear in the total size of the task.

**Properties of $h^+$.** It is admissible by the first argument. It is consistent: for an action $a$ that applies in $s$, a relaxed plan from $s[a]$ preceded by $a$ is a relaxed plan from $s$, because $s \cup \mathit{add}(a) \supseteq s[a]$ and relaxed plans only gain from more facts; so $h^+(s) \le c(a) + h^+(s[a])$. An optimal relaxed plan never uses an action twice, since the second use adds nothing, and each of its actions adds a new fact, so it has at most $\min(n, m)$ actions.

**$h^+$ is NP-hard.** Take a [set cover](/set-cover/) instance: a universe $U$ and sets $S_1, \ldots, S_q \subseteq U$. Build the task with $F = U$, $I = \emptyset$, $G = U$, and one action $\mathrm{take}_j$ with no precondition, $\mathit{add} = S_j$, no deletes and cost 1. The task is already delete free, and a relaxed plan is a sequence of takes whose sets cover $U$. So $h^+(I)$ is the size of a smallest cover, and deciding $h^+(I) \le K$ is NP-hard. It is in NP, because a relaxed plan has at most $n$ actions and can be checked in polynomial time. The reduction keeps costs exactly, so any approximation guarantee for $h^+$ in polynomial time gives the same guarantee for set cover, which is NP-hard to approximate within a factor $c \ln |U|$ for some $c > 0$.

## Classic examples

### Two packages and one truck

A truck and two packages are at A, and both packages must go to B. The actions are drive, load and unload, each of cost 1. The fixed point from $I = \{t_A, p_1@A, p_2@A\}$ adds $t_B$, $p_1@T$ and $p_2@T$ in the first pass and $p_1@B$, $p_2@B$ in the second. An optimal relaxed plan is drive(A,B), load(p1,A), unload(p1,B), load(p2,A), unload(p2,B), of cost 5. It loads at A after the truck has left A: in the relaxed task the truck is at both places. Here $h^+ = h^* = 5$, because the real plan load, load, drive, unload, unload also has 5 actions.

### The Sussman task

In the [blocks world](/blocks-world/) with pickup, putdown, stack and unstack, start from C on A with A and B on the table, and take the goal $\{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$. An optimal relaxed plan is pickup(B), stack(B,C), unstack(C,A), pickup(A), stack(A,B), of cost 5. It unstacks C after B was stacked on it, because the relaxation keeps clear(C), and it picks up A while the hand still holds C. So $h^+ = 5$ and $h^* = 6$. With the full goal, which also asks for C on the table and A clear, $h^+ = h^* = 6$.

### A relaxed plan without a real plan

Take one fact *key* in $I$, the goal $\{g_1, g_2\}$, and two actions use1 and use2, each with the precondition *key*, adding $g_1$ or $g_2$ and deleting *key*. In the relaxed task the key is never used up, so use1, use2 is a relaxed plan and $h^+ = 2$. The real task has no plan: after one use the key is gone. So $h^+ < \infty = h^*$, and a dead end can look solvable to every heuristic based on this relaxation.

### Set cover

With $U = \{1, \ldots, 6\}$ and the sets $\{1,2,3\}$, $\{4,5,6\}$, $\{1,4\}$, $\{2,5\}$, $\{3,6\}$, the task of the reduction has $h^+ = 2$, the cover by the first two sets. With the sets $\{1,2,3,4\}$, $\{1,2,5\}$, $\{3,4,6\}$, the greedy rule that takes the set with the most new elements first takes $\{1,2,3,4\}$ and then needs both other sets, 3 actions, while $h^+ = 2$. A relaxed plan built greedily, as in FF, can therefore cost more than $h^+$.

## Variations

- **Approximations of $h^+$.** [h-max](/h-max-heuristic/) takes the cost of the most expensive goal fact and is admissible, $h_{\max} \le h^+$. [h-add](/h-add-heuristic/) adds the costs of the goal facts and can overestimate, $h^+ \le h_{\mathrm{add}}$. The [relaxed plan heuristic](/relaxed-plan-heuristic/) of FF extracts an actual relaxed plan from the [relaxed planning graph](/relaxed-planning-graph/) and takes its cost, which is at least $h^+$.
- **Landmarks and cuts.** The [landmark heuristics](/landmark-heuristic/), and LM-cut in particular, find sets of actions of which every relaxed plan must use one. LM-cut builds such sets from the h-max costs and gives an admissible estimate with $h_{\max} \le h_{\text{LM-cut}} \le h^+$.
- **Partial delete relaxation.** Keep some of the deletes, for example by compiling chosen conjunctions of facts into new facts, so that the relaxation of the compiled task notices that two facts cannot hold together. With enough conjunctions the estimate becomes exact, at a growing cost. The $h^m$ heuristics are a related idea that reasons about sets of up to $m$ facts.
- **Red-black planning.** Relax only some state variables of a [SAS+](/sas-plus/) task ("red", which keep every value they had) and keep the others exact ("black").
- **Delete-free tasks.** When a task has no deletes in the first place, plan existence is easy but optimal planning is still NP-hard, by the same set cover reduction.

## Pitfalls

- **Treating $h^+$ as easy.** Relaxed plan existence is polynomial, but the optimal relaxed cost is NP-hard. A greedy relaxed plan is an upper bound on $h^+$, not $h^+$ itself, and it is not admissible.
- **Expecting dead ends to be detected.** A state with $h^+ < \infty$ can still be a dead end, as the key task shows. Only $h^+ = \infty$ proves that a state is a dead end.
- **Negative preconditions.** If an action needs a fact to be false, dropping the deletes is not a relaxation unless the negative fact is first made a positive fact with its own adds and deletes. Otherwise the "relaxed" task can lose plans.
- **Counting an action twice.** In a relaxed plan an action is useful at most once. A plan that repeats it is never optimal.
- **Confusing the relaxed state with a real state.** Facts such as "the truck is at A" and "the truck is at B" hold together in a relaxed state. Do not use a relaxed state to check state constraints.

## Exercises

1. Compute the relaxed reachable set of the delivery task with one truck, one package and the places A and B, from $\{t_A, p_A\}$. How many passes does RELAXED-REACHABLE make?
2. Show that $h^+(s) \le h^+(s')$ whenever $s \supseteq s'$.
3. In the Tower of Hanoi with $n$ disks, show that $h^+ = n$ for the goal of the whole tower on the third peg, while $h^* = 2^n - 1$. (For $n = 4$ the values are 4 and 15.)
4. Show that an optimal relaxed plan from $s$ has at most $|F \setminus s|$ actions, and give a task where it needs all of them.
5. The Sussman relaxed plan above is not applicable in the real task. Find its first action that does not apply in the real task, and say which deleted fact it needs.

## References
