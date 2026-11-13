---
tag: ZT81NP
kind: data-structure
slug: relaxed-planning-graph
name: Relaxed planning graph
aliases:
- relaxed graph
area: games-and-search/planning
level: advanced
summary: Planning graph built with delete effects ignored, used to extract relaxed plans.
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of ground actions, k: the number of layers}
  time: {build: O(k m n), extract: O(n (m + n))}
  space: {extra: O(m + n)}
prereqs: [strips, delete-relaxation, planning-graph]
see_also: [relaxed-plan-heuristic, fast-forward-planner, h-max-heuristic, h-add-heuristic, hsp-planner, enforced-hill-climbing, landmark-heuristic, graphplan]
sources:
  - paper: doi:10.1613/jair.855
    title: "Joerg Hoffmann and Bernhard Nebel, The FF planning system: fast plan generation through heuristic search, Journal of Artificial Intelligence Research 14 (2001)"
    locator: pp. 253 to 302; Section 4.1 and Propositions 1 and 2 (no mutexes and no backtracking on relaxed tasks), Section 4.2 (no-ops first, the difficulty of Equation 4, linearization), Section 4.3 and Figure 2 (layer memberships and relaxed plan extraction)
  - paper: doi:10.1016/S0004-3702(96)00047-1
    title: "Avrim L. Blum and Merrick L. Furst, Fast planning through planning graph analysis, Artificial Intelligence 90(1-2) (1997)"
    locator: Section 2 (the planning graph that the relaxed graph simplifies)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapter on classical planning heuristics (the delete relaxation, h_max, h_add and relaxed plans; general locator)
---

A relaxed planning graph is the [planning graph](/planning-graph/) of a [STRIPS](/strips/) task with every delete list removed, built from one state. Without deletes there are no [mutexes](/mutex-relation/), so the graph reduces to two numbers per element: the first fact level $\mathrm{level}(f)$ where a fact appears, and the first layer $\mathrm{level}(a)$ where an action becomes applicable. Fact level $i$ is the set of facts that the [delete relaxation](/delete-relaxation/) can reach in $i$ parallel steps, and $\mathrm{level}(f)$ equals the [$h^{\max}$](/h-max-heuristic/) value of $f$ with unit costs. Building stops when the goals all appear or when a level adds nothing, and the second case proves that the goal is unreachable even without deletes. A backward sweep then extracts a relaxed plan, a set of actions that reaches the goal when deletes are ignored, with no backtracking. Hoffmann and Nebel (2001) built this graph in every search state of the FF planner, and the length of the extracted plan is the [relaxed plan heuristic](/relaxed-plan-heuristic/).

## In plain words

Pretend that actions never undo anything. Then a fact, once true, stays true. Start from the facts of one state. In each round, fire every action whose needs are all met, and add what it makes. Write down the round in which each fact first shows up. Stop when all goals have shown up, or when a round adds nothing new.

Now walk back from the goals. For each goal, pick an action from the round just before the goal first showed up. Prefer actions whose needs showed up early. Its needs become new goals in earlier rounds. Skip a goal that an action already picked will make in time. The picked actions form a plan for the pretend world, and their number is a guess of the real distance.

## The abstract type

The input is a set $A$ of $m$ ground actions over $n$ facts, a state $s$ and a goal $G$. For the relaxed task, each action $a$ becomes $a^+$ with $\mathrm{pre}(a)$, $\mathrm{add}(a)$ and no deletes. A relaxed plan from $s$ is a sequence of actions $a_1, \ldots, a_r$ with $\mathrm{pre}(a_j) \subseteq s \cup \mathrm{add}(a_1) \cup \cdots \cup \mathrm{add}(a_{j-1})$ for every $j$ and $G \subseteq s \cup \bigcup_j \mathrm{add}(a_j)$. The length of a shortest relaxed plan is $h^+(s)$.

The structure offers:

- **build**$(A, s, G)$: the fact levels $F_0 \subseteq F_1 \subseteq \cdots \subseteq F_k$, the action layers $A_0, \ldots, A_{k-1}$, and the numbers $\mathrm{level}(f)$ and $\mathrm{level}(a)$; or the answer that $G$ is not relaxed reachable.
- **extract**: a relaxed plan for $G$, and the goal sets $G_1, \ldots, G_k$ that the sweep created.
- **helpful actions**: the actions applicable in $s$ that add a fact of $G_1$. The [Fast-Forward planner](/fast-forward-planner/) prunes its search to them.

## Representation

The graph needs no edges and no mutex sets. Hoffmann and Nebel (2001, Section 4.3) store only the layer membership of each fact and each action, plus one counter per action. When a fact gets its level, the counters of the actions that need it go up by one. An action whose counter reaches the size of its precondition enters the next layer, and its new add effects enter the next fact level. This is the same computation as the unit-cost $h^{\max}$ fixed point, done in rounds. Each layer here holds only the actions that are new at that layer, since an older action adds nothing new.

## Operations

```pseudo id=main
BUILD(A, s, G)
L1  F_0 ← s ; level(f) ← 0 for f ∈ s ; i ← 0
L2  while G ⊄ F_i do
L3      A_i ← the actions a with pre(a) ⊆ F_i that are in no earlier layer
L4      new ← the union of add(a) over a ∈ A_i, minus F_i
L5      if new = ∅ then return "G is not relaxed reachable"
L6      level(a) ← i for a ∈ A_i ; level(f) ← i + 1 for f ∈ new ; F_{i+1} ← F_i ∪ new ; i ← i + 1
L7  return the levels F_0, ..., F_m and the layers A_0, ..., A_{m-1}, where m = i

EXTRACT(G)
L8  for each g ∈ G: put g into G_{level(g)} and set need(g) ← (m, 0)
L9  for i ← m down to 1 do
L10     for each g ∈ G_i, in a fixed order, do
L11         if a selected action at a position before need(g) adds g then skip g
L12         o ← an action of A_{i-1} that adds g with the least difficulty, the sum of level(p) over p ∈ pre(o)
L13         select o at the position (i - 1, j), where j actions of layer i - 1 were selected before it
L14         for each p ∈ pre(o) with level(p) ≥ 1 do
L15             put p into G_{level(p)} and set need(p) ← the smaller of need(p) and the position of o
L16 return the selected actions sorted by position
```

Lines L1 to L7 build the graph. An action enters at the first layer where its preconditions are all present, so $\mathrm{level}(a) = \max_{p \in \mathrm{pre}(a)} \mathrm{level}(p)$. Line L5 is the relaxed dead-end test: if a level adds no fact, no later level adds one either.

Lines L8 to L16 are the extraction of Hoffmann and Nebel (2001, Figure 2), with one change in how goals are marked as done. Each goal goes into the goal set of its first level. At level $i$, an achiever is taken from layer $i - 1$, which exists because $g$ first appears at level $i$. Line L12 is the difficulty rule of their Equation 4. A position $(i - 1, j)$ orders the selected actions by layer and then by the order of selection, and the plan is executed in this order. The value $\mathrm{need}(g)$ is the earliest position of an action that needs $g$; for a top goal it is $(m, 0)$, after every action.

Line L11 skips a goal only if an action that is placed before every user of the goal already adds it. Figure 2 of Hoffmann and Nebel instead marks each add effect of a selected action as true at levels $i - 1$ and $i$, and skips marked goals. Its note says this assumes that the actions of a layer are executed in the order of selection. But a goal can be marked by an action selected later in the same layer, so placed after the action that needs it. The example below shows that the literal rule can then return a set that is not a relaxed plan. With the need positions, the result is always a relaxed plan.

## Example

**A relaxed plan that is not optimal.** The state is empty and the goal is $\{g_1, g_2\}$. The actions are $p_P$ and $p_Q$, which add $P$ and $Q$ with no preconditions; $a_1$, which needs $P$ and adds $g_1$; $b$, which needs $Q$ and adds $g_2$; and $x$, which needs $P$ and $Q$ and adds both goals.

| level | facts | new actions in the layer |
|---|---|---|
| 0 | none | $p_P$, $p_Q$ |
| 1 | $P$, $Q$ | $a_1$, $b$, $x$ |
| 2 | $g_1$, $g_2$ | |

The difficulty of $a_1$ and $b$ is 1, and that of $x$ is 2. The sweep at level 2 takes $g_1$ first and selects $a_1$, and $P$ goes into $G_1$. Then $g_2$ is not added by $a_1$, so it selects $b$, and $Q$ goes into $G_1$. At level 1, it selects $p_P$ and $p_Q$. The relaxed plan is $p_P, p_Q, a_1, b$, of length 4. The plan $p_P, p_Q, x$ has length 3, so here $h^+ = 3$, and the real optimum $h^*$ is also 3. The difficulty rule prefers actions with early preconditions, and here it picks two actions where one would do.

**A literal reading of Figure 2 that fails.** The state is $\{r\}$ and the goal is $\{g_1, g_2\}$. The action $a_p$ needs $r$ and adds $p$, and $a_q$ needs $r$ and adds $q$. The action $b$ needs $p$ and adds $g_1$ and $q$; the action $c$ needs $q$ and adds $g_2$ and $p$. Both $p$ and $q$ are at level 1, and $b$ and $c$ are in layer 1. The sweep selects $b$ for $g_1$ and puts $p$ into $G_1$. With the literal marks, $b$ marks $q$ true at level 1, so $c$, selected next for $g_2$, does not put $q$ into $G_1$, and $c$ marks $p$ true at level 1. At level 1, $p$ is marked, so nothing is selected. The result $\{b, c\}$ has 2 actions, and neither is applicable in $\{r\}$. The need positions give $a_p, b, c$ instead: $p$ is needed by $b$ at position $(1, 0)$, and $c$ at position $(1, 1)$ comes too late to supply it. Its length 3 equals $h^+$.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness/). The results are these.

1. **Levels.** $F_i$ is the set of facts that $i$ relaxed parallel steps can reach from $s$, and $\mathrm{level}(f)$ is the unit-cost $h^{\max}$ value of $f$.
2. **Reachability.** BUILD stops after at most $n$ layers. It returns "not relaxed reachable" exactly when no relaxed plan exists, that is, when $h^+(s) = \infty$.
3. **Extraction.** EXTRACT returns a relaxed plan in which each action occurs once. So its length $h_{FF}$ satisfies $h^{\max} \le h^+ \le h_{FF}$, with the unit-cost $h^{\max}$ of the goal set, and $h_{FF} = 0$ exactly when $G \subseteq s$.

There is no upper bound of $h_{FF}$ in terms of $h^+$ that holds in general: the choice of achievers is greedy, and deciding whether $h^+ \le K$ is NP-complete (Bylander 1994; see [delete relaxation](/delete-relaxation/)).

## Complexity

Each layer adds at least one fact, so $k \le n$. In the plain form of lines L3 and L4, a layer scans the $m$ actions and their preconditions of up to $n$ facts, so BUILD costs $O(k m n)$ time. With the counters of the representation section, each precondition and each add effect is touched once, and BUILD costs time linear in the size of the task, $O(m n)$ at most. EXTRACT handles each fact at most once as a goal, scans its at most $m$ achievers, and adds at most $n$ preconditions, for $O(n (m + n))$ time. Both use $O(m + n)$ space beyond the task. These are proved upper bounds. In FF the graph is rebuilt in every evaluated state, so this cost is paid once per state.

## Variants

- **Planning graph.** Keep the deletes and the mutexes to get the [planning graph](/planning-graph/) of [GRAPHPLAN](/graphplan/).
- **Cost-based levels.** Replace the unit layers by the cost of reaching each fact under $h^{\max}$ or [$h^{\mathrm{add}}$](/h-add-heuristic/), and choose the best supporter of each fact by that cost. The relaxed plan then follows these supporters back from the goals. This is the form used in cost-aware planners.
- **Helpful actions.** The goal set $G_1$ gives the helpful actions of FF (Hoffmann and Nebel 2001, Equation 5), which cut the branching factor of [enforced hill climbing](/enforced-hill-climbing/).
- **Conditional effects.** Hoffmann and Nebel (2001, Section 7.2) extend the graph and the extraction to ADL actions with conditional effects.
- **Landmarks.** The same layered pass with one achiever set removed tests whether a fact is a landmark; see [landmark heuristic](/landmark-heuristic/).

## When to use it

Use the relaxed graph when a heuristic for forward search needs a relaxed plan, not only a number: for the FF heuristic, for helpful actions, and for landmark tests. When only a number is needed, [$h^{\mathrm{add}}$](/h-add-heuristic/) and [$h^{\max}$](/h-max-heuristic/) run the same fixed point without the extraction. When the deletes matter for the answer, as for an exact test that a plan of $k$ steps exists, use the full [planning graph](/planning-graph/).

## Pitfalls

- **Stopping only on the goal.** Without line L5, BUILD loops for ever on a state from which the goal is not relaxed reachable.
- **Marking add effects at the lower level.** As the example shows, a goal can be marked by an action placed after its user. Track where each goal is needed, or linearize so that suppliers come first.
- **Selecting an achiever from the wrong layer.** An achiever from layer $i - 2$ or below would have put $g$ at a lower level. An achiever from layer $i$ or above is not applicable yet.
- **Reading $h_{FF}$ as admissible.** $h_{FF}$ can exceed $h^*$, as the first example shows. For optimal search, use [$h^{\max}$](/h-max-heuristic/) or an [admissible](/admissible-heuristic/) landmark heuristic.
- **Ignoring the order of the plan.** The relaxed plan is a sequence. Its actions in the same layer may depend on each other, so the order of selection matters.

## Implementations

## History

Hoffmann and Nebel (2001) observed that GRAPHPLAN on a task without deletes builds a graph with no mutexes and finds a plan with no backtracking (their Propositions 1 and 2). This turned the planning graph into a fast way to compute relaxed plans in each search state. HSP of Bonet and Geffner, the planner that FF improved on, had used the same relaxation but summed the costs of the goals, which counts shared subgoals twice. At the AIPS 2000 planning competition, FF was named a Group A distinguished performance planning system (Hoffmann and Nebel 2001, Section 8.1), and relaxed plans became a standard tool for later planners such as Fast Downward and LAMA.

## References
