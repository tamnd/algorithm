---
tag: 7EP2KY
kind: algorithm
slug: pop-partial-order-planning
name: Partial-order planning (POP)
aliases:
- POP
area: games-and-search/planning
level: core
summary: Refines a partial-order plan by repairing its flaws, open preconditions and threatened causal links, until every linearization is a valid plan. Sound and complete for STRIPS.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the bound on the number of steps, a: the number of ground actions, p: the largest number of preconditions of an action or of the goal}
  time: {worst: O(n^2 (n + p) (n + a)^(n (n + p)))}
  space: {extra: O(n^2 (n + p)^2)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1991
  people: [David McAllester, David Rosenblitt, Daniel S. Weld]
  note: McAllester and Rosenblitt gave the causal-link planner that Weld (1994) simplified and named POP; causal links come from Tate's NONLIN (1977) and partial orders from Sacerdoti's NOAH (1975).
prereqs: [plan-space-planning, partial-order-plan, causal-link, strips]
see_also: [snlp, tweak, ucpop, least-commitment-principle, sussman-anomaly, state-space-planning, graphplan, htn-decomposition]
sources:
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (the POP algorithm, its flaws and resolvers, soundness and completeness, and the extension to UCPOP)
  - paper: "David McAllester and David Rosenblitt, Systematic nonlinear planning, Proceedings of AAAI-91"
    locator: pp. 634 to 639 (the causal-link planner, its soundness, completeness and systematicity)
  - paper: doi:10.1016/0004-3702(94)90012-4
    title: "Anthony Barrett and Daniel S. Weld, Partial-order planning: evaluating possible efficiency gains, Artificial Intelligence 67(1) (1994)"
    locator: pp. 71 to 112 (partial-order against total-order planners, and the role of goal interactions)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (plan-space planning; the PSP and PoP procedures, flaws, resolvers, soundness and completeness)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (partial-order planning; general locator)
---

Partial-order planning (POP) solves a [STRIPS](/strips/) task by search in the space of [partial-order plans](/partial-order-plan/). It starts from the plan with only a START step, whose effects are the initial state, and a FINISH step, whose preconditions are the goal. Then it repairs flaws one at a time. An open condition, a precondition with no support, is repaired by a [causal link](/causal-link/) from an existing or a new step. A threat, a step that may delete a linked fact between the two ends of the link, is repaired by an ordering constraint. When no flaw is left, every linearization of the plan is a valid plan. POP is the simplest sound and complete form of [plan-space planning](/plan-space-planning/).

## In plain words

You write down only the steps you need and why you need them. At first the plan says "start" and "finish", and the finish needs the goal. Each need with no answer yet is a flaw. To fix it, point to a step that gives the need, or add a new step that gives it, and draw an arrow from the giver to the taker. Each new step brings its own needs.

An arrow is a promise: what it carries must stay true between its two ends. If another step can undo it in that gap, that step is a threat, and you move it before the giver or after the taker. Steps that do not interfere stay unordered.

When no need is open and no arrow is threatened, every order that obeys your rules works. If a fix leads to a dead end, you go back and try another.

## The problem

The input is a ground STRIPS task: a finite set $F$ of facts, a finite set $A$ of actions, each with a precondition $\mathit{pre}(a)$, an add list $\mathit{add}(a)$ and a delete list $\mathit{del}(a)$, all subsets of $F$, an initial state $I \subseteq F$ and a goal $G \subseteq F$. An action $a$ applies in a state $s$ if $\mathit{pre}(a) \subseteq s$, and the next state is $(s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. The output is a partial-order plan whose every linearization is a plan, or the answer that no plan exists.

A partial plan $P$ has steps, which are copies of actions, an ordering relation $\prec$ on the steps, and a set of causal links $i \xrightarrow{p} j$. START adds $I$, FINISH needs $G$, and every other step is after START and before FINISH. The flaws of $P$ are:

- an **open condition** $(p, j)$: $p \in \mathit{pre}(j)$ and no link ends at $j$ with the fact $p$;
- a **threat** $(k, i \xrightarrow{p} j)$: $p \in \mathit{del}(k)$, $k \ne i, j$, and the orderings allow $i \prec k \prec j$, that is neither $k \prec i$ nor $j \prec k$ holds.

$P$ is complete when it has no flaw and its orderings are acyclic.

## The algorithm

The planner is a depth-first search over partial plans with a bound $n$ on the number of steps other than START and FINISH. The outer loop raises $n$ one at a time. This is [iterative deepening](/iterative-deepening-search/), and it returns a plan with the fewest steps.

```pseudo id=main
POP(I, G, A)
L1  for n ← 0, 1, ..., 2^|F| − 1 do
L2      cut ← false
L3      Q ← REFINE(the plan START ≺ FINISH for I and G, A, n)
L4      if Q ≠ failure then return Q
L5      if cut = false then return failure          ▷ a larger n gives the same tree
L6  return failure
REFINE(P, A, n)
L7  if P has no open condition and no threat then return P
L8  f ← a flaw of P with the fewest resolvers
L9  if f is a threat (k, i -p-> j) then
L10     R ← the orderings k ≺ i (demotion) and j ≺ k (promotion) that keep ≺ acyclic
L11 else f is an open condition (p, j):
L12     R ← a link i -p-> j for each step i with p ∈ add(i) and not j ≺ i
L13     if P has fewer than n steps then add to R a new step of each action a with p ∈ add(a), linked to j
L14     else if some action adds p then cut ← true
L15 for each r in R do                              ▷ the choice point
L16     Q ← REFINE(P with r, A, n)
L17     if Q ≠ failure then return Q
L18 return failure
```

Line L8 is the flaw selection. Any rule is correct, because every flaw must be repaired in the end. The rule "fewest resolvers first" fails fast: a flaw with no resolver ends the branch at once, and a flaw with one resolver costs no branching. Line L10 is the threat repair. A demotion before START or a promotion after FINISH is never consistent, so L10 drops it. Lines L12 and L13 are the two ways to support a precondition. Line L14 records that the bound removed an option. If a whole round runs without such a removal, line L5 stops: a larger bound gives the same search tree, so no plan exists. Line L1 stops at $2^{|F|} - 1$ steps, because a shortest plan never visits a state twice. Line L5 usually stops the loop much earlier.

The implementation also drops two kinds of useless actions before the search: an action whose precondition is not reachable even when delete lists are ignored, and an action whose add list is inside its precondition. The second kind only removes facts, so no shortest plan uses it.

## Example

Take the [Sussman anomaly](/sussman-anomaly/) in the move encoding of the [blocks world](/blocks-world/). The initial state is $\mathit{on}(C, A)$, $\mathit{ontable}(A)$, $\mathit{ontable}(B)$, $\mathit{clear}(C)$, $\mathit{clear}(B)$, and the goal is $\mathit{on}(A, B)$, $\mathit{on}(B, C)$. There are 18 ground move actions, and all of them pass the filter. The rounds $n = 0, 1, 2$ visit 1, 3 and 7 partial plans and fail. The round $n = 3$ visits 18 partial plans, and this is the path to the complete plan. The steps are $S_A = \mathit{move}(A, \mathit{table}, B)$, $S_B = \mathit{move}(B, \mathit{table}, C)$ and $S_C = \mathit{move}(C, A, \mathit{table})$.

| refinement | flaw chosen | resolvers | choice |
|---|---|---|---|
| 1 | open $\mathit{on}(A, B)$ at FINISH | 2 | new step $S_A$ |
| 2 | open $\mathit{on}(B, C)$ at FINISH | 2 | new step $S_B$ |
| 3 | open $\mathit{ontable}(A)$ at $S_A$ | 3 | link from START |
| 4 | open $\mathit{ontable}(B)$ at $S_B$ | 3 | link from START |
| 5 | open $\mathit{clear}(A)$ at $S_A$ | 4 | new step $S_C$ |
| 6 | open $\mathit{clear}(B)$ at $S_A$ | 1 | link from START |
| 7 | open $\mathit{clear}(B)$ at $S_B$ | 1 | link from START |
| 8 | threat: $S_A$ deletes $\mathit{clear}(B)$ of START $\to S_B$ | 1 | promotion $S_B \prec S_A$ |
| 9 | open $\mathit{clear}(C)$ at $S_B$ | 1 | link from START |
| 10 | open $\mathit{clear}(C)$ at $S_C$ | 1 | link from START |
| 11 | threat: $S_B$ deletes $\mathit{clear}(C)$ of START $\to S_C$ | 1 | promotion $S_C \prec S_B$ |
| 12 | open $\mathit{on}(C, A)$ at $S_C$ | 1 | link from START |

After refinement 5 the plan has 3 steps, so the bound $n = 3$ allows no new step, and each later open condition has one resolver. The threats in rows 8 and 11 have only promotion, because demotion would put a step before START. The result has 10 causal links and the orderings $S_C \prec S_B \prec S_A$, so it has one linearization: move $C$ to the table, $B$ onto $C$, $A$ onto $B$. This is the unique shortest plan. The planner never had to choose which goal to achieve first: it added both goal steps, and the threats fixed their order. This is why the anomaly, which defeats goal-by-goal planners, is easy here.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). There are four parts.

- **Soundness.** In a complete plan, take any linearization and any step $j$ with $p \in \mathit{pre}(j)$. The link $i \xrightarrow{p} j$ puts $i$ before $j$, and $i$ adds $p$. No step that deletes $p$ can lie between them, because such a step would be a threat. So $p$ holds when $j$ starts. For FINISH this says that the goal holds at the end.
- **Termination.** Each refinement adds a link or a new ordering pair, or a step. With at most $n$ steps there are finitely many of each, so each branch is finite.
- **Completeness.** Fix a plan $\sigma$ with at most $n$ actions. For an open condition $(p, j)$, choose the last position of $\sigma$ before $j$ whose action adds $p$, and use the step for that position, new or existing. For a threat, the threatening step is not between the ends of the link in $\sigma$, so demotion or promotion agrees with $\sigma$. These choices keep every ordering true in $\sigma$, so they never make a cycle, and a branch of the search reaches a complete plan.
- **Fewest steps.** A complete plan with $m$ steps gives a plan of $m$ actions, and a plan of $m$ actions gives a complete plan with at most $m$ steps in round $m$. So the first round that succeeds is the length of a shortest plan.

The tests check these claims. On 400 random tasks with 3 or 4 facts, POP finds a plan if and only if breadth-first search over all reachable states finds one, the number of steps equals the length of a shortest plan, and every linearization of each plan is valid when it is simulated.

## Complexity

Let $n$ be the bound, $a$ the number of actions and $p$ the largest number of preconditions. A plan has at most $n + 2$ steps, so at most $n (n + p)$ open conditions over its life and $O(n^2)$ ordering pairs. Each refinement adds one of them, so a branch has depth $O(n (n + p))$. A flaw has at most $n + a + 2$ resolvers. Each node costs $O(n^2 (n + p))$ to find the flaws and count their resolvers, with a reachability test for each pair. This gives the worst-case time bound above. Depth-first search keeps one plan for each level of the path, which is $O(n (n + p))$ plans of size $O(n (n + p))$.

The exponential bound is not an artifact of the analysis. Plan existence for STRIPS is PSPACE-complete ([plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/)), and the search tree of POP can be much larger than the state space, because many partial plans have the same set of linearizations. On a random task with 3 facts and no plan, a version of POP without the flaw rule, the filter and the cut test of line L5 needed 245,153 nodes at bound 7. With them, no task of the 400 random tasks of the tests needs more than 93 nodes over all rounds, and the mean is 4.2.

## Properties

- **Least commitment.** POP orders two steps only when a threat forces it, so one plan stands for many sequences. See the [least commitment principle](/least-commitment-principle/).
- **Sound and complete.** It returns only valid plans, and it finds one when one exists within the bound.
- **Not systematic.** Two branches can reach complete plans that share a linearization. On the task of the [SNLP](/snlp/) page, POP finds 4 complete plans with 16 linearizations but only 8 distinct action sequences. SNLP adds threats from steps that add the fact and removes the overlap.
- **Goal order does not matter.** The plan is not built in execution order, so the order in which goals are attacked does not limit the plans that can be found, as the Sussman example shows.
- **Ground actions.** This version has no variables. [TWEAK](/tweak/) and later planners keep variables and add binding constraints.

## Variants and improvements

- **SNLP.** McAllester and Rosenblitt (1991) treat a step that adds the linked fact as a threat too. Then no two complete plans share a linearization, and no partial plan is visited twice. See [SNLP](/snlp/).
- **TWEAK.** Chapman (1987) has no causal links. It checks with the modal truth criterion whether a precondition is necessarily true, and it keeps variables with codesignation constraints. See [TWEAK](/tweak/).
- **UCPOP.** Penberthy and Weld (1992) add conditional effects, universally quantified effects and goals, and a third threat resolver, confrontation. See [UCPOP](/ucpop/).
- **Flaw selection.** The choice of the next flaw changes the size of the search a lot. The implementation uses "fewest resolvers first". Other rules delay threats or prefer open conditions with one resolver.
- **Heuristic search.** Later causal-link planners replace depth-first search by a best-first search over partial plans, with an estimate of the work that remains, such as the number of open conditions.
- **Hierarchical planning.** [HTN decomposition](/htn-decomposition/) adds methods that expand abstract tasks, and many HTN planners keep partial orders and causal links.

## When to use it

Use POP to learn plan-space planning and to plan for tasks where the plan should stay flexible, for example when steps run in parallel or the order is chosen at execution time. A partial-order plan is also easy to explain, because each link says why a step is there. For finding a plan fast on standard benchmarks, use [forward state-space search](/forward-state-space-search/) with a heuristic, which is far faster on most tasks, or [Graphplan](/graphplan/). Use [UCPOP](/ucpop/) when actions have conditional effects, and a lifted planner such as [TWEAK](/tweak/) when grounding is too large.

## Pitfalls

- **No bound and depth-first search.** Without a step bound, depth-first search can add steps for ever on a task with no plan or with a long plan. Use iterative deepening, a bound, or a best-first search.
- **Testing threats against the closure.** "Possibly between" means that neither $k \prec i$ nor $j \prec k$ follows from the orderings by transitivity. Testing only the direct constraints misses threats and gives wrong plans.
- **Forgetting that a link orders its ends.** Adding $i \xrightarrow{p} j$ must also add $i \prec j$. Without it, a linearization can run $j$ before $i$.
- **Checking only one linearization.** A plan with open conditions or threats can still have one valid linearization. The unresolved Sussman plan on the [partial-order plan](/partial-order-plan/) page has 3 linearizations, and only 1 of them is valid.
- **Reading "complete" as "optimal".** POP is complete. It returns a shortest plan only with iterative deepening on the number of steps, as here.
- **Expecting systematicity.** POP can find the same sequence on several branches. Count distinct sequences, not plans, or use [SNLP](/snlp/).

## Implementations

## History

Sacerdoti's NOAH (1975) built plans as partial orders and repaired interactions between steps. Tate's NONLIN (1977) recorded for each precondition the step that achieves it, which is the idea of a causal link. Chapman's TWEAK (1987) gave the first clean proof of soundness and completeness for a partial-order planner, but it used the modal truth criterion in place of links. McAllester and Rosenblitt (1991) gave a simple causal-link planner that was sound, complete and systematic. Weld (1994) presented a simplified version as POP, together with its extension UCPOP of Penberthy and Weld (1992), and this form is the one in the textbooks. Barrett and Weld (1994) showed that partial-order planners beat total-order planners on tasks whose goals interact in some ways and not in others.

## References
