---
tag: RD7TS9
kind: algorithm
slug: graphplan
name: GRAPHPLAN
aliases:
- Blum-Furst GRAPHPLAN
area: games-and-search/planning
level: advanced
summary: Expands a planning graph level by level and searches it backward for a valid plan.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of ground actions, k: the number of graph levels}
  time: {graph: O(k n^2 (m + n)^2), stage: O(k n^2 2^n (m + n)^n)}
  space: {extra: O(k (m + n)^2 + k n 2^n)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1995
  people: [Avrim L. Blum, Merrick L. Furst]
  note: Blum and Furst presented the planning graph and its backward search at IJCAI 1995, and gave the memoized search and the termination test for unsolvable tasks in the journal version of 1997.
prereqs: [strips, planning-graph, mutex-relation]
see_also: [satplan, backward-state-space-search, relaxed-planning-graph, partial-order-plan, temporal-planning, bounded-plan-existence-np-complete, constraint-satisfaction-problem, blocks-world]
sources:
  - paper: doi:10.1016/S0004-3702(96)00047-1
    title: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Artificial Intelligence 90(1-2) (1997)"
    locator: pp. 281 to 300; Section 3.2 (the backward search and forward checking), Section 3.2.1 (memoization), Section 3.2.3 and Theorem 2 (minimal action sets), Section 5.3 and Theorem 3 (the termination test)
  - paper: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Proceedings of IJCAI 1995"
    locator: pp. 1636 to 1642 (the first version of Graphplan)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 6 (the Graphplan algorithm, its nogood table and its termination)
  - paper: doi:10.1613/jair.655
    title: "Subbarao Kambhampati, Planning graph as a (dynamic) CSP: exploiting EBL, DDB and other CSP search techniques in Graphplan, Journal of Artificial Intelligence Research 12 (2000)"
    locator: pp. 1 to 34 (the backward search as dynamic constraint satisfaction; explanation-based learning and dependency-directed backtracking)
  - paper: "Henry Kautz and Bart Selman, Unifying SAT-based and graph-based planning, Proceedings of IJCAI 1999"
    locator: pp. 318 to 325 (Blackbox, which translates the planning graph to SAT)
  - paper: "Alfonso Gerevini, Alessandro Saetti and Ivan Serina, Planning through stochastic local search and temporal action graphs in LPG, Journal of Artificial Intelligence Research 20 (2003)"
    locator: pp. 239 to 290 (local search over subgraphs of the planning graph)
---

GRAPHPLAN is a planner for [STRIPS](/strips/) tasks that alternates two phases. It grows a [planning graph](/planning-graph/) from the initial state until all goals appear at the last level with no [mutex](/mutex-relation/) pair. Then it searches backward from the goals at that level: it picks a set of pairwise non-mutex actions that add the goals, takes their preconditions as the goals one level down, and repeats until level 0. If the search fails, it adds one level and searches again. Goal sets that failed at a level are stored, so no failure is explored twice, and the same store gives a test that stops on unsolvable tasks. Blum and Furst (1995, 1997) proved that GRAPHPLAN returns a plan with the fewest parallel steps, and says "no plan" exactly when the task has no plan. The plan need not have the fewest actions.

## In plain words

First build the layered map of what might be possible, step by step, until the goals all show up together. Then work back from the goals. For each goal, pick something that makes it true at the last step, and only pick things that do not clash. What those picks need becomes the list of goals one step earlier. Keep going until you reach the start. If you get stuck, try other picks.

If nothing works, the plan needs more steps: add a step to the map and try again. Write down every list of goals that failed at a step, so you never try it twice. Once the map stops changing and no new failed lists appear, there is no plan at all.

## The problem

The input is a STRIPS task $(F, A, I, G)$ with $n$ facts and $m$ ground actions. A parallel plan of $k$ steps is a sequence $S_1, \ldots, S_k$ of sets of actions. Each $S_j$ is applicable in the state $s_{j-1}$ (with $s_0 = I$), and no action of $S_j$ deletes a precondition or an add effect of another action of $S_j$. Then $s_j = (s_{j-1} \setminus \bigcup_{a \in S_j} \mathrm{del}(a)) \cup \bigcup_{a \in S_j} \mathrm{add}(a)$, and the plan solves the task when $G \subseteq s_k$. Every order of the actions inside a step gives the same state, so a parallel plan is a set of sequential plans. The output is a parallel plan with the fewest steps, or "no plan".

## The algorithm

```pseudo id=main
GRAPHPLAN(A, I, G)
L1  build the planning graph from I until G holds at the last level k or the graph levels off
L2  if G does not hold at level k then return no plan
L3  nogood ← an empty table of goal sets per level
L4  loop
L5      π ← EXTRACT(G, k)
L6      if π ≠ failure then return π
L7      if the graph leveled off at a level n < k and this stage added no goal set to nogood at level n then return no plan
L8      expand the graph by one level ; k ← k + 1

EXTRACT(g, i)
L9  if i = 0 then return the empty plan
L10 if g ∈ nogood at level i then return failure
L11 for each set S yielded by ASSIGN(g, i, ∅) do
L12     π ← EXTRACT(the union of pre(a) over a ∈ S, i - 1)
L13     if π ≠ failure then return π followed by the step S without its no-ops
L14 add g to nogood at level i ; return failure

ASSIGN(g, i, S)
L15 if every fact of g is added by some action of S then yield S and return
L16 f ← the first fact of g that no action of S adds
L17 for each achiever a of f in the action level A_{i-1}, no-ops first, do
L18     if a is not mutex at level i - 1 with any action of S then ASSIGN(g, i, S ∪ {a})
```

Line L1 is the BUILD loop of the [planning graph](/planning-graph/). It stops at the first level where every goal is present and no two goals are mutex, because by the soundness of the graph no plan has fewer steps. Line L2 is the quick test of Blum and Furst (1997, Section 5.2): if the graph has leveled off and the goals still do not hold, they never will.

The search is the stage loop of lines L4 to L8. Stage $k$ asks whether a plan of at most $k$ steps exists. EXTRACT works one level at a time. ASSIGN picks, for each goal not yet covered, one achiever at the level below, and keeps only achievers that are not mutex with those already picked. The preconditions of the picked set are a goal set one level down (line L12). No-ops come first, so a goal that already holds is carried down before an action is tried for it.

Line L14 is the memo of Blum and Furst (1997, Section 3.2.1). A goal set $g$ at level $i$ goes into nogood only after every set of achievers for it has failed. The graph below level $i$ never changes when the graph grows, so the entry stays valid for all later stages. Line L10 uses it to cut the search.

Line L7 is the termination test of Blum and Furst (1997, Section 5.3). After the graph has leveled off at level $n$, the stages are like shifted copies of each other above level $n$. If a full stage adds nothing new to nogood at level $n$, then the failed goal sets at level $n$ are closed under regression, and none of them can ever be reached. The test is checked only when $n < k$: the stage must search through level $n$ from above.

## Example

**A logistics task.** A truck is at $l_1$ with packages $p_1$ and $p_2$. The goal is both packages at $l_2$. The actions are $\mathit{load}(p, l)$, $\mathit{unload}(p, l)$ and $\mathit{drive}(l, l')$. The goals first hold at level 3, and stage 3 succeeds at once. The search visits one goal set per level:

| level | goal set |
|---|---|
| 3 | $\mathit{at}(p_1, l_2)$, $\mathit{at}(p_2, l_2)$ |
| 2 | $\mathit{in}(p_1)$, $\mathit{in}(p_2)$, $\mathit{truck}(l_2)$ |
| 1 | $\mathit{in}(p_1)$, $\mathit{in}(p_2)$, $\mathit{truck}(l_1)$ |
| 0 | $\mathit{at}(p_1, l_1)$, $\mathit{at}(p_2, l_1)$, $\mathit{truck}(l_1)$ |

At level 3 the two unloads are not mutex: they share the precondition $\mathit{truck}(l_2)$ and neither deletes it. At level 2 the goal $\mathit{truck}(l_2)$ is added by $\mathit{drive}(l_1, l_2)$, and the packages stay inside by no-ops. The plan is $\{\mathit{load}(p_1, l_1), \mathit{load}(p_2, l_1)\}$, $\{\mathit{drive}(l_1, l_2)\}$, $\{\mathit{unload}(p_1, l_2), \mathit{unload}(p_2, l_2)\}$: 3 steps and 5 actions. A sequential planner needs 5 levels of depth for the same plan.

**An unsolvable task that the graph cannot see.** Two tokens $t_1, t_2$ can each be put on one slot $x$, $y$ or $z$. The action $\mathit{make}_u$ needs $x$ and $y$ and adds $u$, and $\mathit{make}_v$ needs $z$ and adds $v$. The goal $\{u, v\}$ needs three tokens, so there is no plan. But the graph has no fact mutexes at all (see [mutex relation](/mutex-relation/)). The goals hold at level 2, and the graph levels off at $n = 2$. The sizes of the nogood table per stage are:

| stage $k$ | level 1 | level 2 | level 3 | level 4 | level 5 |
|---|---|---|---|---|---|
| 2 | 1 | 1 | | | |
| 3 | 10 | 4 | 1 | | |
| 4 | 10 | 20 | 4 | 1 | |
| 5 | 10 | 20 | 20 | 4 | 1 |

Stage 5 adds nothing at level 2, so line L7 reports no plan after stage 5. The table shows the shift: above the level off, each stage repeats the counts of the stage before, one level higher.

**Fewest steps against fewest actions.** Let $a_1, a_2, a_3$ add $p$, $q$, $r$ with no preconditions, and let $b$ need $p, q, r$ and add $g$. A second route is $c_1$ adds $s$, $c_2$ needs $s$ and adds $t$, $c_3$ needs $t$ and adds $g$. GRAPHPLAN returns $\{a_1, a_2, a_3\}, \{b\}$: 2 steps and 4 actions. The plan $c_1, c_2, c_3$ has 3 actions but 3 steps, and GRAPHPLAN never returns it.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness/). The results are these.

1. **Soundness.** A returned plan is a valid parallel plan. Each step is pairwise non-mutex, so it is a parallel step, and every goal of a level is added by a picked action and deleted by none of the others.
2. **Completeness at a level.** If a goal set $g$ can be reached in $i$ parallel steps, then EXTRACT$(g, i)$ returns a plan. The proof takes the last step of a real plan, adds no-ops for the goals that it does not add, and shows that ASSIGN yields a subset of it. The soundness of the [planning graph](/planning-graph/) makes this set pairwise non-mutex. So every nogood entry is truly unsolvable at its level.
3. **Step optimality.** Stage $k$ succeeds exactly when a plan of at most $k$ steps exists. Stages run for $k = k_0, k_0 + 1, \ldots$, and no plan has fewer than $k_0$ steps. So the first success has the fewest steps.
4. **Termination.** If no plan exists, the nogood table at the level off $n$ grows in each stage until the test of line L7 fires, and it has at most $2^n$ entries. The test fires only when no plan exists (Blum and Furst 1997, Theorem 3). The proof here describes each failed stage by a regression closure and shows that the shift above level $n$ makes the failed sets at level $n$ closed under regression.

## Complexity

The graph costs $O(n^2 (m + n)^2)$ time per level, as on the [planning graph](/planning-graph/) page. The search is exponential in the worst case. In one stage, each pair (goal set, level) is explored at most once, thanks to the memo, and there are at most $2^n$ goal sets per level. One exploration tries at most $(m + n)^n$ achiever choices, one per open goal, and each choice costs $O(n^2)$ mutex tests and set operations. So a stage of $k$ levels costs $O(k n^2 2^n (m + n)^n)$ time. The nogood table holds at most $k 2^n$ sets of up to $n$ facts. These are crude proved upper bounds, not measured counts.

The worst case is no surprise: with a bound $k$ on the plan length that is polynomial in the input, deciding whether a plan exists is [NP-complete](/bounded-plan-existence-np-complete/), and deciding whether any plan exists is [PSPACE-complete](/strips-plan-existence-pspace-complete/). GRAPHPLAN decides the second question, so no polynomial bound on its running time is expected. The number of stages after the level off is at most $2^n$, the number of possible entries at level $n$, plus one.

In practice the cost is in the search, and the graph is cheap. Blum and Furst (1997, Section 4) report that graph building took a large share of the time only on easy problems.

## Properties

- **Step optimal.** The plan has the fewest parallel steps among all plans whose steps have no interfering actions.
- **Not action optimal.** A plan with fewer steps can have more actions, as in the example above.
- **Complete.** It returns a plan when one exists and says "no plan" otherwise.
- **Deterministic.** The order of the goals and of the achievers fixes the search. With the minimal action set rule of Blum and Furst (1997, Theorem 2), the goal sets it visits at a level do not depend on the goal order when the stage fails.
- **Level by level.** It searches one whole level before it goes down, which gives the mutexes their full effect, and it resembles iterative deepening on the number of steps.

## Variants and improvements

- **Forward checking.** After each pick, check that every goal still open has an achiever that is not mutex with the picks so far, and back up at once if not. Blum and Furst (1997, Section 3.2) use it.
- **Minimal action sets.** Recurse only on sets of achievers from which no action can be removed. Blum and Furst (1997, Section 3.2.3) prove that the visited goal sets are then the preconditions of exactly the minimal sets, in any goal order. The implementation here yields some non-minimal sets too, which is still sound and complete.
- **EBL and DDB.** Kambhampati (2000) treats the backward search as a dynamic constraint satisfaction problem (see [constraint satisfaction](/constraint-satisfaction-problem/)). With explanation-based learning, a nogood stores only the subset of goals that caused the failure, and dependency-directed backtracking jumps back to the pick that caused it. Smaller nogoods match more often.
- **Planning graph to SAT.** Blackbox (Kautz and Selman 1999) builds the graph and hands it to a SAT solver as a formula of $k$ steps. This is the graph encoding of [SATPLAN](/satplan/).
- **Local search on the graph.** LPG (Gerevini, Saetti and Serina 2003) searches over subgraphs of the planning graph that are partial plans, and repairs flaws by local moves.
- **Durative actions.** TGP (Smith and Weld 1999) extends the graph and its mutexes to actions with durations, a form of [temporal planning](/temporal-planning/).
- **Heuristics from the graph.** Without mutexes and deletes, the graph becomes the [relaxed planning graph](/relaxed-planning-graph/), and a relaxed plan extracted from it is the [relaxed plan heuristic](/relaxed-plan-heuristic/) of FF.

## When to use it

Use GRAPHPLAN when the shortest parallel plan matters, when the plans are short, and when the actions are mostly independent, as in logistics. There the graph is small and the mutexes cut most of the search. For long sequential plans, or when only some plan is needed fast, a heuristic forward planner such as the [Fast-Forward planner](/fast-forward-planner/) is much faster. For optimal parallel plans on hard tasks, a SAT encoding with a modern solver ([SATPLAN](/satplan/)) is usually stronger, and it can reuse the graph and its mutexes.

## Pitfalls

- **Stopping at the first level where the goals hold.** That level is only a lower bound. The search can fail there, and the graph must then grow.
- **A nogood check at the wrong level.** A goal set that fails at level $i$ can succeed at level $i + 1$. Store the level with the set.
- **Testing termination too early.** The test of line L7 needs $n < k$. In a stage at or below the level off, the table at level $n$ is empty or new, and an equal count says nothing.
- **Mutex achievers for one goal.** Two picks for different goals may be the same action. ASSIGN skips a goal that a picked action already adds, so the same action is never compared with itself.
- **Reading the plan as sequential.** The plan is a list of steps. Any order inside a step works, but actions from different steps must keep their order.
- **Empty steps.** A step of only no-ops does not occur in the result, because a shorter plan would then exist, but an implementation that allows empty steps should drop them before it counts actions.

## Implementations

## History

Blum and Furst presented GRAPHPLAN at IJCAI 1995, and the journal version of 1997 added the memo and the termination test. It was much faster than the partial-order planners of the time, such as [UCPOP](/ucpop/), on many benchmarks, and it changed the direction of the field. In the first [planning competition](/international-planning-competition/), in 1998, several entries were based on planning graphs, among them IPP, STAN and Blackbox. Kambhampati (2000) linked the search to constraint satisfaction. After 2000, heuristic forward search took over most of the field, but the planning graph lived on in the heuristics of FF and in SAT encodings.

## References
