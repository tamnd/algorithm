---
tag: QH51FZ
kind: data-structure
slug: partial-order-plan
name: Partial-order plan
aliases:
- partially ordered plan
area: games-and-search/planning
level: core
summary: A plan given by steps, ordering constraints and causal links instead of a sequence. If it has no open precondition and no threat, every linearization of it is a valid plan.
model: word-ram
complexity:
  vars: {n: the number of steps with START and FINISH, e: the number of ordering pairs, l: the number of causal links}
  time: {worst: O(n + e)}
  space: {extra: O(n + e + l)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1975
  people: [Earl Sacerdoti, Austin Tate, David McAllester, David Rosenblitt]
  note: NOAH (1975) kept plans partially ordered, NONLIN (1977) recorded goal structure, and McAllester and Rosenblitt (1991) made causal links part of the plan.
prereqs: [strips, classical-planning, topological-sort]
see_also: [causal-link, plan-space-planning, pop-partial-order-planning, least-commitment-principle, sussman-anomaly, tweak, directed-acyclic-graph, counting-linear-extensions]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5, the definition of a partial plan as steps, orderings, bindings and causal links, flaws, and the proof that a solution plan has only valid linearizations
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (plans as steps, orderings, bindings and causal links; threats; the solution criterion)
  - paper: doi:10.1016/0004-3702(94)00076-D
    title: "Subbarao Kambhampati, Craig A. Knoblock and Qiang Yang, Planning as refinement search: a unified framework for evaluating design tradeoffs in partial-order planning, Artificial Intelligence 76 (1995)"
    locator: pp. 167 to 238 (partial plans as sets of constraints, and the candidate set of a partial plan, its linearizations)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (partial-order plans; general locator)
---

A partial-order plan describes a set of action sequences at once. It has a set of steps, each a copy of an action, ordering constraints between pairs of steps, and [causal links](/causal-link/) that record which step produces each precondition of each other step. A special step START produces the initial state and a special step FINISH needs the goal. A total order of the steps that respects the orderings is a linearization. The plan is consistent when the orderings have no cycle. It is a solution when it is consistent, every precondition has a link, and no step can fall between the two ends of a link whose fact it deletes. Then every linearization is a valid plan. This is the data structure that [plan-space planning](/plan-space-planning/) searches.

## In plain words

A recipe for a meal often does not fix the order of everything. You must boil the water before the pasta goes in, but you may chop the salad before, during or after that. A partial-order plan writes down only the orders that matter.

Each step says what it needs and what it gives. An arrow from one step to another says "this step gives that one what it needs". The arrow also says the first step comes first.

Danger comes when a third step could undo what an arrow carries, and the rules still let it run in the gap. If no step can do that and every need has an arrow, then any order the rules allow works. You can run the plan in any of those orders, or give unordered steps to different people.

## The abstract type

A partial-order plan over a ground [STRIPS](/strips/) task with initial state $I$ and goal $G$ is a tuple $P = (S, \prec, L)$:

- $S$ is a finite set of steps. Each step $s$ is labelled by an action with $\mathit{pre}(s)$, $\mathit{add}(s)$ and $\mathit{del}(s)$. The step START has $\mathit{add} = I$ and empty precondition; the step FINISH has $\mathit{pre} = G$ and no effects. Two steps can carry the same action.
- $\prec$ is a set of ordering pairs $i \prec j$. Every step other than START and FINISH is after START and before FINISH.
- $L$ is a set of causal links $i \xrightarrow{p} j$ with $p \in \mathit{add}(i)$ and $p \in \mathit{pre}(j)$. A link implies $i \prec j$.

A *linearization* is a sequence of all the steps in which $i$ comes before $j$ whenever $i \prec j$. The action sequence of a linearization drops START and FINISH. $P$ is *consistent* if it has a linearization, that is, if $\prec$ has no cycle. A flaw of $P$ is

- an *open condition* $(p, j)$: $p \in \mathit{pre}(j)$ and no link $i \xrightarrow{p} j$ is in $L$;
- a *threat* $(k, i \xrightarrow{p} j)$: $p \in \mathit{del}(k)$, $k \notin \{i, j\}$, and some linearization puts $k$ after $i$ and before $j$.

$P$ is a *solution* if it is consistent and has no flaw. The key law is: **every linearization of a solution is a plan for the task.** A lifted plan adds a fourth part, binding constraints that force two variables to be equal or different; [TWEAK](/tweak/) and [UCPOP](/ucpop/) use it. This page treats ground plans.

## Representation

Store the steps in an array, with START at index 0 and FINISH at index 1. Store the orderings as adjacency sets, $\mathit{after}[i]$ being the steps that $i$ directly precedes, so the orderings form a [directed graph](/directed-acyclic-graph/). Store the links as a set of triples. The orderings are kept as given, not transitively closed: the closure can have $\Theta(n^2)$ pairs, and planners add orderings one at a time. A reachability search answers "must $i$ come before $j$?" when needed.

## Operations

```pseudo id=main
ADD-STEP(P, a)
L1  i ← a new step labelled a; after[i] ← {FINISH}; add i to after[START]; return i
PRECEDES(P, i, j)                  ▷ does a chain of orderings lead from i to j?
L2  seen ← {i}; stack ← [i]
L3  while stack is not empty do
L4      for each k in after[pop(stack)] do
L5          if k = j then return true
L6          if k ∉ seen then add k to seen and push k on stack
L7  return false
ADD-ORDERING(P, i, j)
L8  if i = j or PRECEDES(P, j, i) then return false        ▷ the new pair would close a cycle
L9  add j to after[i]; return true
ADD-LINK(P, i, p, j)
L10 if p ∉ add(i) or p ∉ pre(j) then error
L11 if not ADD-ORDERING(P, i, j) then return false
L12 add i -p-> j to the links; return true
THREATS(P)
L13 for each link i -p-> j and each step k with p ∈ del(k) do
L14     if k ∉ {i, j} and not PRECEDES(P, k, i) and not PRECEDES(P, j, k) then report (k, i -p-> j)
OPEN-CONDITIONS(P)
L15 for each step j and each p ∈ pre(j) do
L16     if no link ends at j with the fact p then report (p, j)
IS-SOLUTION(P)
L17 return P has no cycle, OPEN-CONDITIONS(P) is empty and THREATS(P) is empty
```

Line L8 keeps the plan consistent: a new pair $i \prec j$ closes a cycle exactly when $j$ already precedes $i$. Line L14 is the threat test. It asks only for two reachability searches, because $k$ can fall between $i$ and $j$ in some linearization exactly when neither $k \prec i$ nor $j \prec k$ is forced. Line L17 tests for a cycle with [Kahn's algorithm](/kahns-algorithm/); a plan built only by ADD-ORDERING and ADD-LINK never has one. The linearizations are the [topological orders](/topological-sort/) of the ordering graph, and the implementation lists them by backtracking over the steps with no unplaced predecessor.

## Example

The [Sussman anomaly](/sussman-anomaly/) starts with $C$ on $A$ and $A$, $B$ on the table, and asks for $A$ on $B$ and $B$ on $C$. Take three steps: $S_C = \mathit{move}(C, A, \mathit{table})$ (step 2), $S_B = \mathit{move}(B, \mathit{table}, C)$ (step 3) and $S_A = \mathit{move}(A, \mathit{table}, B)$ (step 4), with 10 links:

| producer | fact | consumer |
|---|---|---|
| $S_A$ | $\mathit{on}(A, B)$ | FINISH |
| $S_B$ | $\mathit{on}(B, C)$ | FINISH |
| START | $\mathit{on}(C, A)$, $\mathit{clear}(C)$ | $S_C$ |
| START | $\mathit{ontable}(B)$, $\mathit{clear}(B)$, $\mathit{clear}(C)$ | $S_B$ |
| START | $\mathit{ontable}(A)$, $\mathit{clear}(B)$ | $S_A$ |
| $S_C$ | $\mathit{clear}(A)$ | $S_A$ |

No precondition is open. The only forced order among the three steps is $S_C \prec S_A$, from the link on $\mathit{clear}(A)$, so the plan has 3 linearizations. THREATS finds two threats. $S_B$ deletes $\mathit{clear}(C)$ and can fall between START and $S_C$. $S_A$ deletes $\mathit{clear}(B)$ and can fall between START and $S_B$. Of the 3 linearizations only $S_C, S_B, S_A$ is a valid plan: $S_B, S_C, S_A$ puts $B$ on $C$ first, and then $C$, with $B$ on top, cannot move, and $S_C, S_A, S_B$ covers $B$ before $B$ moves. Demotion is impossible for both threats, since nothing goes before START. Promotion adds $S_C \prec S_B$ and $S_B \prec S_A$. Now the plan has no flaw and one linearization, the valid one.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md).

- **PRECEDES** is a depth-first reachability search in the ordering graph, so it returns true exactly when a chain of orderings leads from $i$ to $j$.
- **Consistency.** A finite directed graph has a topological order if and only if it has no cycle. ADD-ORDERING adds $i \prec j$ only if no chain leads from $j$ to $i$; any new cycle would use the new pair and such a chain. So a plan built by these operations stays consistent.
- **The threat test.** If $k \prec i$ or $j \prec k$ is forced, no linearization puts $k$ between them. If neither is forced, adding $i \prec k$ and $k \prec j$ keeps the graph acyclic, and a topological order of the larger graph is a linearization with $k$ in the gap.
- **The solution law.** Take a solution and a linearization. For every step $j$ and $p \in \mathit{pre}(j)$, the link $i \xrightarrow{p} j$ puts $i$ before $j$, and $i$ adds $p$. A step between them that deleted $p$ would be a threat. So $p$ holds when $j$ starts, and for FINISH the goal holds at the end.
- **Converse.** Every plan $\sigma$ is a linearization of some solution: link each precondition to the last earlier step that adds it, or to START, and order each threatening step on the side where $\sigma$ puts it.

## Complexity

Let $n$ be the number of steps, $e$ the number of stored ordering pairs and $l$ the number of links. The time in the front matter is that of one ordering test or one new ordering or link.

| operation | time |
|---|---|
| ADD-STEP | $O(1)$ |
| PRECEDES, ADD-ORDERING, ADD-LINK | $O(n + e)$ |
| THREATS | $O(l n (n + e))$, or $O(n (n + e) + l n)$ with the transitive closure computed once |
| OPEN-CONDITIONS | $O(n p + l)$, for at most $p$ preconditions per step |
| consistency test | $O(n + e)$ |
| list the linearizations | $O(n + e)$ per linearization, up to $n!$ of them |

The space is $O(n + e + l)$. A plan with $m$ unordered actions stands for $m!$ sequences, which is the point of the structure. Counting the linearizations of a partial order exactly is #P-complete; see [counting linear extensions](/counting-linear-extensions/). Testing a solution does not need them: IS-SOLUTION is polynomial.

## Variants

- **Lifted plans.** Steps are copies of action schemas with variables, and a fourth component holds codesignation and noncodesignation constraints. A threat is then a step that *may* unify with the negation of the linked fact.
- **Plans without causal links.** [TWEAK](/tweak/) keeps only steps, orderings and bindings, and checks each precondition with the modal truth criterion.
- **Systematic plans.** [SNLP](/snlp/) also counts a step that adds the linked fact as a threat, so the linearizations of different complete plans are disjoint.
- **Conditional effects.** [UCPOP](/ucpop/) labels each link with the effect that supports it, and a threat can also be removed by a goal that keeps the threatening effect from firing.
- **Temporal plans.** Simple temporal networks replace the orderings by distance constraints between time points.
- **Hierarchical plans.** A [task network](/task-network/) has the same shape, but its nodes are tasks that may still be decomposed.

## When to use it

Use it as the search state of a plan-space planner, as the output of a planner when steps may run in parallel or by different agents, and as a post-processing target: a sequential plan can be turned into a partial-order plan by the converse construction above, which removes orderings that do not matter. It is also a good explanation of a plan, since every link says why a step is there.

## Pitfalls

- **Consistency is not enough.** A consistent plan with no open condition can still have threats, and then some linearizations fail, as in the example before promotion.
- **Transitive orderings.** The threat test must use chains of orderings, not just the stored pairs. A test on the stored pairs alone never misses a threat, but it reports false ones, so the planner adds useless orderings and may not see that a plan is already a solution.
- **A link is not just an order.** Two plans with the same steps and orderings but different links have different flaws. The links record which step supports a precondition, and the planner protects that choice.
- **Deleting a needed fact at the same step.** A step that deletes one of its own preconditions does not threaten its incoming link, since it is an end of that link.

## Implementations

## History

Sacerdoti's NOAH (1975) was the first planner to keep its plans partially ordered, in a structure called a procedural net. Tate's NONLIN (1977) recorded goal structure, the ancestor of causal links. Chapman (1987) gave a precise semantics in terms of the completions of a plan. McAllester and Rosenblitt (1991) put causal links into the plan as first-class constraints, and Weld (1994) and Kambhampati, Knoblock and Yang (1995) made the view of a partial plan as a set of constraints whose candidates are its linearizations the standard one.

## References
