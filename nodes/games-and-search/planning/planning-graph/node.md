---
tag: PJJTVQ
kind: data-structure
slug: planning-graph
name: Planning graph
aliases:
- layered planning graph
area: games-and-search/planning
level: core
summary: Layered graph of fact and action levels that over-approximates reachable states.
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of ground actions, k: the number of levels}
  time: {expand: O(n^2 (m + n)^2), build: O(k n^2 (m + n)^2)}
  space: {extra: O(k (m + n)^2)}
prereqs: [strips, classical-planning]
see_also: [mutex-relation, graphplan, relaxed-planning-graph, satplan, delete-relaxation, h-max-heuristic, invariant, blocks-world]
sources:
  - paper: doi:10.1016/S0004-3702(96)00047-1
    title: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Artificial Intelligence 90(1-2) (1997)"
    locator: pp. 281 to 300; Section 2 (planning graphs, no-ops and the mutual exclusion rules), Theorem 1 (the graph has polynomial size), Section 5.1 (the graph levels off)
  - paper: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Proceedings of IJCAI 1995"
    locator: pp. 1636 to 1642 (the first version of the planning graph and of Graphplan)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 6 (planning-graph techniques; the reachability tree, the planning graph, mutual exclusion and its properties)
---

A planning graph is a layered graph built from a [STRIPS](/strips/) task. Its levels alternate: fact level $P_0$, action level $A_0$, fact level $P_1$, action level $A_1$, and so on. $P_0$ is the initial state. $A_k$ holds every action whose preconditions are in $P_k$ and are pairwise not mutex, plus one no-op for each fact of $P_k$, and $P_{k+1}$ holds every add effect of $A_k$. Each level also stores [mutex](/mutex-relation/) pairs: two actions, or two facts, that cannot occur together at that level. The graph over-approximates reachability: every state reachable in at most $k$ parallel steps is a subset of $P_k$ with no mutex pair, but a set with no mutex pair need not be reachable. Each level has polynomial size, and the graph levels off after at most $n(n+1)/2 + 1$ levels for $n$ facts. Blum and Furst (1995, 1997) introduced it for [GRAPHPLAN](/graphplan/). Without the mutexes and the delete lists it becomes the [relaxed planning graph](/relaxed-planning-graph/) of heuristic planners.

## In plain words

Write the start facts in a column. Next to them, write every action that could run now, and after the actions, every fact that one of them could make true. A special do nothing action carries each old fact forward. Repeat column after column. You never choose between actions, so a column holds facts from many different possible worlds at once.

To keep some precision, you also mark pairs that cannot go together. Two actions clash if one destroys what the other needs or makes. Two facts clash if every way to make the first clashes with every way to make the second. A marked pair is truly impossible at that column. An unmarked pair may still be impossible. After a while the columns stop changing, and you can stop building.

## The abstract type

The input is a STRIPS task $(F, A, I, G)$: a set $F$ of $n$ facts, a set $A$ of $m$ ground actions, each with a precondition $\mathrm{pre}(a)$, an add list $\mathrm{add}(a)$ and a delete list $\mathrm{del}(a)$, an initial state $I \subseteq F$ and a goal $G \subseteq F$. An action is applicable in a state $s$ when $\mathrm{pre}(a) \subseteq s$, and its result is $(s \setminus \mathrm{del}(a)) \cup \mathrm{add}(a)$.

A parallel step is a set of actions that are applicable in $s$ and pairwise independent: no action deletes a precondition or an add effect of another. The result of the step is $(s \setminus \bigcup \mathrm{del}) \cup \bigcup \mathrm{add}$, and every order of the actions gives this state. A sequential plan of $k$ actions is a parallel plan of $k$ steps.

The structure offers these operations:

- **expand**: add the action level $A_k$ and the fact level $P_{k+1}$, with their mutexes.
- **holds**$(X, k)$: test whether $X \subseteq P_k$ and no two facts of $X$ are mutex at level $k$.
- **leveled-off**: test whether the last two fact levels have the same facts and the same mutexes.
- the achievers of a fact $f$ at level $k$: the actions of $A_{k-1}$ that add $f$. [GRAPHPLAN](/graphplan/) uses this for its backward search.

## Representation

The graph is a list of levels. Fact level $k$ is a set $P_k$ and a set $FM_k$ of unordered fact pairs. Action level $k$ is a list $A_k$ and a set $AM_k$ of unordered action pairs. The edges are implicit: an action of $A_k$ has precondition edges to its facts in $P_k$, add edges to $P_{k+1}$ and delete edges to $P_{k+1}$, and these come from the action itself. The no-op of a fact $f$ is an action with precondition $\{f\}$, add list $\{f\}$ and an empty delete list. It is what carries $f$ from $P_k$ to $P_{k+1}$, so $P_k \subseteq P_{k+1}$.

Two actions $a \ne b$ of $A_k$ are mutex when one of these holds:

- **inconsistent effects**: one deletes an add effect of the other;
- **interference**: one deletes a precondition of the other;
- **competing needs**: a precondition of $a$ and a precondition of $b$ are mutex in $FM_k$.

Two facts $p \ne q$ of $P_{k+1}$ are mutex when every achiever of $p$ in $A_k$ is mutex with every achiever of $q$, and no single action adds both. Blum and Furst (1997, Section 2) group the first two rules under interference; Ghallab, Nau and Traverso (2004, Chapter 6) list them apart. The [mutex relation](/mutex-relation/) page gives the rules in more detail and compares them with [invariants](/invariant/) of the state space.

Practical planners store the graph in a more compact way. Each fact and action gets the index of the first level where it appears, and each mutex gets the last level where it holds, because facts and actions only appear and mutexes only disappear as $k$ grows (Lemma 1 of the proof). Then the whole graph takes the space of one level, plus one number per element.

## Operations

```pseudo id=main
EXPAND(A, P_k, FM_k)
L1  A_k ← {noop(f) : f ∈ P_k}
L2  for each action a ∈ A do
L3      if pre(a) ⊆ P_k and no pair of pre(a) is in FM_k then add a to A_k
L4  AM_k ← ∅
L5  for each pair a ≠ b in A_k do
L6      if a deletes a precondition or an add effect of b, or b of a, then add {a, b} to AM_k
L7      else if some p ∈ pre(a) and q ∈ pre(b) have {p, q} ∈ FM_k then add {a, b} to AM_k
L8  P_{k+1} ← the union of add(a) over a ∈ A_k
L9  FM_{k+1} ← ∅
L10 for each pair p ≠ q in P_{k+1} do
L11     if every achiever a of p and every achiever b of q in A_k have a ≠ b and {a, b} ∈ AM_k then
L12         add {p, q} to FM_{k+1}
L13 return A_k, AM_k, P_{k+1}, FM_{k+1}

BUILD(A, I, G)
L14 P_0 ← I ; FM_0 ← ∅ ; k ← 0
L15 while not HOLDS(G, k) and not (k ≥ 1 and P_k = P_{k-1} and FM_k = FM_{k-1}) do
L16     A_k, AM_k, P_{k+1}, FM_{k+1} ← EXPAND(A, P_k, FM_k) ; k ← k + 1
L17 return the levels 0 to k
```

Lines L1 to L3 build the action level. An action enters only if its preconditions are present and pairwise not mutex, because otherwise no reachable state can apply it. Lines L5 to L7 apply the three action rules: line L6 is interference and inconsistent effects together, and line L7 is competing needs. Line L8 builds the next fact level; with the no-ops it contains $P_k$. Lines L10 to L12 apply the fact rule. Line L15 stops when the goal holds at the last level or when the graph has leveled off. After a level off, every later level is the same, because level $k+1$ is a function of level $k$.

## Example

Take the blocks world with two blocks $A$ and $B$ on the table and the hand empty, with the goal $\mathit{on}(A, B)$.

- **Level 0.** $P_0$ has 5 facts: $\mathit{clear}(A)$, $\mathit{clear}(B)$, $\mathit{ontable}(A)$, $\mathit{ontable}(B)$ and $\mathit{handempty}$. There are no fact mutexes.
- **Actions 0.** $A_0$ has the 5 no-ops and $\mathit{pickup}(A)$, $\mathit{pickup}(B)$. There are 7 action mutexes: the two pickups delete $\mathit{handempty}$, a precondition of both, and each pickup deletes the facts carried by 3 no-ops ($\mathit{clear}$, $\mathit{ontable}$ and $\mathit{handempty}$).
- **Level 1.** $P_1$ adds $\mathit{holding}(A)$ and $\mathit{holding}(B)$, for 7 facts. There are 7 fact mutexes: $\mathit{holding}(A)$ with $\mathit{holding}(B)$, with $\mathit{handempty}$, with $\mathit{clear}(A)$ and with $\mathit{ontable}(A)$, and the same three for $B$. For example, the only achiever of $\mathit{holding}(A)$ is $\mathit{pickup}(A)$, the only achiever of $\mathit{handempty}$ is its no-op, and these two are mutex.
- **Actions 1.** $A_1$ has 7 no-ops and 6 actions: the two pickups, $\mathit{putdown}(A)$, $\mathit{putdown}(B)$, $\mathit{stack}(A, B)$ and $\mathit{stack}(B, A)$. The pair $\mathit{holding}(A)$, $\mathit{clear}(B)$ is not mutex, so $\mathit{stack}(A, B)$ enters. There are 54 action mutexes.
- **Level 2.** $P_2$ adds $\mathit{on}(A, B)$ and $\mathit{on}(B, A)$, for 9 facts, with 16 fact mutexes, for example $\mathit{on}(A, B)$ with $\mathit{on}(B, A)$ and $\mathit{on}(A, B)$ with $\mathit{ontable}(A)$.

The goal holds at level 2, and 2 is the length of the shortest plan, $\mathit{pickup}(A)$ then $\mathit{stack}(A, B)$. If we expand once more, $P_3 = P_2$ and $FM_3 = FM_2$, so the graph levels off at level 2. This task has 5 reachable states, and the 16 mutexes of level 2 are exactly the 16 pairs of facts that are never true together in any of them. With two blocks the mutexes are complete. The [mutex relation](/mutex-relation/) page shows a task where they are not.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness/). There are three results.

1. **Monotonicity.** $P_k \subseteq P_{k+1}$ and $A_k \subseteq A_{k+1}$. A pair that is not mutex at level $k$ is not mutex at level $k+1$.
2. **Soundness.** If a state $s$ is reachable from $I$ by at most $k$ parallel steps, then $s \subseteq P_k$ and no pair of facts of $s$ is in $FM_k$. Every parallel step that is applicable in such a state is a subset of $A_k$ with no pair in $AM_k$. So if the goal does not hold at level $k$, no plan has $k$ or fewer parallel steps.
3. **Level off.** The graph levels off after at most $n(n+1)/2 + 1$ expansions, and all later levels are equal.

Soundness is the induction on $k$ that each rule only marks pairs that no reachable state at level $k$ can contain. The converse fails: a pair with no mutex can be impossible, because the rules only look at pairs, and an impossibility can need three facts or more.

## Complexity

The input size is $n$ facts and $m$ ground actions. A grounded STRIPS task can have exponentially many actions in the size of its lifted [PDDL](/pddl/) description (see [grounding](/grounding/)), so all bounds here are in the ground size.

Each action level has at most $m + n$ actions (the actions and the no-ops), and each fact level at most $n$ facts. Line L7 checks at most $n^2$ precondition pairs for each of the $(m + n)^2$ action pairs, and line L11 checks at most $(m + n)^2$ achiever pairs for each of the $n^2$ fact pairs. So one expansion costs $O(n^2 (m + n)^2)$ time and $O((m + n)^2)$ space for the mutexes. This is the polynomial size of Blum and Furst (1997, Theorem 1). A graph of $k$ levels costs $k$ times this, and $k \le n(n+1)/2 + 1$ at the level off. These are proved upper bounds. Two actions that share no fact can only be mutex by competing needs, so an implementation indexes the actions by their facts and skips most pairs.

The graph says nothing for free about plan existence, which is [PSPACE-complete](/strips-plan-existence-pspace-complete/). The graph levels off in polynomially many levels, but a plan can need exponentially many steps, and the graph cannot tell the two cases apart by itself. [GRAPHPLAN](/graphplan/) needs its memoized search on top of the graph to decide the question.

## Variants

- **Without mutexes.** Drop lines L4 to L7 and L9 to L12. The levels then only record which facts can appear. The first level of a fact is its $h^{\max}$ value with unit costs (see [h-max heuristic](/h-max-heuristic/)).
- **Relaxed planning graph.** Ignore the delete lists as well. The [relaxed planning graph](/relaxed-planning-graph/) of the FF planner is this graph, built from the current state in each search node, and the relaxed plan extracted from it gives the [relaxed plan heuristic](/relaxed-plan-heuristic/).
- **Serial graph.** Make every pair of non-no-op actions mutex. Then a level is one sequential step, and the graph bounds sequential plan length instead of parallel steps.
- **Stronger mutexes.** Mutexes over three facts or more catch more impossible sets, at a higher cost per level: a level with $t$-fact mutexes has up to $n^t$ of them.
- **Planning graph as SAT.** The levels, the actions and the mutexes map directly to a propositional formula. Blackbox (Kautz and Selman 1999) builds the planning graph and hands this formula to a SAT solver; see [SATPLAN](/satplan/).

## When to use it

Use the graph as the search space of [GRAPHPLAN](/graphplan/), when short parallel plans matter, and as a fast test that rules out plans of fewer than $k$ steps. Use the mutexes as cheap state [invariants](/invariant/) for other planners, for example as extra clauses in a [SATPLAN](/satplan/) encoding. For heuristic forward search, the relaxed graph without mutexes is the better tool, because it is built once per state and must be cheap.

## Pitfalls

- **Forgetting the no-ops.** Without no-ops, $P_{k+1}$ loses facts that no action re-adds, and the soundness theorem fails.
- **Missing the same-action case.** Two facts added by one action are not mutex. If line L11 does not require $a \ne b$, the rule marks such pairs, and this is unsound.
- **Reading an unmarked pair as reachable.** Mutexes are sound, not complete. A goal that holds at level $k$ may still have no plan of $k$ steps, and may have no plan at all.
- **Comparing with the wrong step count.** The level of a goal bounds parallel steps, not the number of actions. A plan of 2 steps can have 4 actions.
- **Stopping at the first fact level off.** The graph has leveled off only when both the facts and the mutexes repeat. Facts usually stop changing first, and mutexes keep disappearing for a few more levels.

## Implementations

## History

Avrim Blum and Merrick Furst presented the planning graph and GRAPHPLAN at IJCAI 1995 and in the journal version of 1997. Their main point was that a compact graph that does not commit to an order of actions, together with the mutexes, cuts the search for short parallel plans. Later work used the graph in other ways: Kautz and Selman translated it to SAT in Blackbox (1999), and Hoffmann and Nebel (2001) built a relaxed version in each search state for the FF heuristic.

## References
