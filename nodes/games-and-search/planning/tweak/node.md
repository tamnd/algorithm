---
tag: SW1BEM
kind: algorithm
slug: tweak
name: TWEAK
aliases:
- Chapman's TWEAK
area: games-and-search/planning
level: advanced
summary: Chapman's lifted partial-order planner. It tests with the modal truth criterion whether each precondition is necessarily true and repairs it by establishment and declobbering.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the bound on the number of steps, s: the number of operator schemas, e: "the largest number of terms in the lists of one step, START and FINISH included"}
  time: {worst: O(((n + s) e)^(n^2 e^2) n^3 e^3)}
  space: {extra: O(n^4 e^4)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1987
  people: [David Chapman]
  note: Chapman stated the modal truth criterion, built TWEAK on it, proved the planner correct and complete, and showed that richer action representations make planning undecidable.
prereqs: [partial-order-plan, plan-space-planning]
see_also: [pop-partial-order-planning, snlp, ucpop, least-commitment-principle, sussman-anomaly, action-schema, robinson-unification, disjoint-set]
sources:
  - paper: doi:10.1016/0004-3702(87)90092-0
    title: "David Chapman, Planning for conjunctive goals, Artificial Intelligence 32(3) (1987)"
    locator: pp. 333 to 377 (the TWEAK representation, the modal truth criterion, the goal achievement procedure, its correctness and completeness; pp. 370 to 373 the undecidability results)
  - paper: doi:10.1016/0004-3702(94)00095-6
    title: "Subbarao Kambhampati and Dana S. Nau, On the nature and role of modal truth criteria in planning, Artificial Intelligence 82(1-2) (1996)"
    locator: pp. 129 to 155 (the criterion is correct for necessary truth and polynomial; possible truth is NP-hard; with finitely many constants necessary truth is co-NP-hard)
  - paper: "David McAllester and David Rosenblitt, Systematic nonlinear planning, Proceedings of AAAI-91"
    locator: pp. 634 to 639 (p. 637 the cost of the criterion, and why TWEAK is not systematic)
  - paper: doi:10.1016/0004-3702(94)00076-D
    title: "Subbarao Kambhampati, Craig A. Knoblock and Qiang Yang, Planning as refinement search: a unified framework for evaluating design tradeoffs in partial-order planning, Artificial Intelligence 76 (1995)"
    locator: pp. 167 to 238 (TWEAK as a refinement planner; general locator)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (plan-space planning with variable binding constraints; general locator)
---

TWEAK is the partial-order planner of Chapman (1987). A partial plan holds steps that are instances of operator [schemas](/action-schema/) with variables, ordering constraints, and constraints that two terms must or must not denote the same object, called codesignation and noncodesignation. TWEAK has no [causal links](/causal-link/). Instead it asks, for each precondition, whether it is *necessarily true*: true in every completion of the plan, every linearization with every value of the variables that meets the constraints. Chapman's modal truth criterion (MTC) answers this question in polynomial time from the constraints alone. When a precondition is not necessarily true, TWEAK makes it so: it picks a step that asserts it (establishment) and then defeats each step that could deny it in between (declobbering). When every precondition is necessarily true, every completion of the plan is a solution.

## In plain words

You keep a rough plan: some steps, some "this before that" rules, and blanks such as "move some block onto A" where you have not yet said which block. For each need of a step you ask: whatever order I pick, and however I fill the blanks, will this need hold? There is a quick test that answers this from the rules alone.

If the answer is no, you pick a step that gives the need, or add one. Then you look for steps that might take it away in between. For each one, you move it before the giver, or after the taker, or say that its blank must be a different object, or put another giver between it and the taker. You repeat until every need passes the test. If a choice leads nowhere, you go back and try another.

## The problem

The input is a planning task in the TWEAK representation: a set of operator schemas, each with parameters, a precondition list, an add list (the propositions it asserts), a delete list (the propositions it denies) and pairs of parameters that must differ; an initial state and a goal, both finite sets of ground propositions. A proposition is a predicate applied to terms, and a term is a constant or a variable. Chapman assumes infinitely many constants, so two variables can always differ unless a constraint says otherwise. We also assume that no schema can assert and deny the same proposition under values that meet its own constraints, which holds for the usual encodings such as the [blocks world](/blocks-world/).

A partial plan has START, which asserts the initial state, FINISH, which needs the goal, other steps, a strict partial order $\prec$, a set of codesignations $x \approx y$ closed under unification, and a set of noncodesignations $x \not\approx y$. A *completion* is a linearization of the steps together with a value for each variable, so that codesignated terms get the same constant and noncodesignated terms get different ones. A proposition $p$ is necessarily true before step $s$ if it holds before $s$ in every completion, when the effects of the steps are applied in order. The output is a plan whose every precondition is necessarily true, or failure.

## The algorithm

**The modal truth criterion.** For a step $s$ and a proposition $p$, $p$ is necessarily true before $s$ if and only if

1. some step $t$ with $t \prec s$, possibly START, asserts a proposition $q$ with $q \approx p$ necessarily (each argument pair is codesignated), and
2. for every step $c \ne s$ that is possibly before $s$ and denies some $q'$ that possibly codesignates with $p$, there is a *white knight*: a step $w$ with $c \prec w \prec s$ that asserts some $r$ such that $r \approx p$ follows from the constraints together with $q' \approx p$.

Each test is a reachability question in $\prec$ or a unification in the codesignation classes, so the criterion takes polynomial time. Kambhampati and Nau (1996) prove that it is exact for necessary truth in this representation.

The planner reads the criterion backwards. To make $p$ necessarily true before $s$, it picks an establisher for condition 1 and then makes condition 2 hold for every clobberer.

```pseudo id=main
TWEAK(I, G, schemas, N)
L1  for n ← 0, 1, ..., N do
L2      cut ← false
L3      Q ← REFINE(the plan START ≺ FINISH for I and G, n)
L4      if Q ≠ failure then return Q
L5      if cut = false then return failure          ▷ a larger n gives the same tree
L6  return failure
REFINE(P, n)
L7  if the MTC holds for every precondition of every step of P then return P
L8  (s, p) ← a precondition that is not necessarily true
L9  E ← for each step t not after s and each q ∈ add(t): P with t ≺ s and q ≈ p, if consistent
L10 if P has fewer than n steps then add to E, for each schema and each q in its add list, P with a new step t, t ≺ s and q ≈ p
L11 else if some schema asserts a proposition with the predicate of p then cut ← true
L12 for each P' in E, with its establisher t, do       ▷ choice point
L13     for each P'' in DECLOBBER(P', t, s, p) do      ▷ choice point
L14         Q ← REFINE(P'', n)
L15         if Q ≠ failure then return Q
L16 return failure
DECLOBBER(P, t, s, p)
L17 if no step c ∉ {t, s}, possibly between t and s, denies a q' that possibly codesignates with p and has no white knight then output P and stop
L18 take such a clobberer c and q'
L19 for each consistent P' in: P with c ≺ t (demotion); P with s ≺ c (promotion); P with x ≉ y for one argument pair (x, y) of q' and p (separation); P with c ≺ w ≺ s and r ≈ p for a step w and r ∈ add(w) (white knight) do
L20     output each plan of DECLOBBER(P', t, s, p)
```

Line L7 is the MTC, applied to every precondition, so a precondition that a later step has clobbered is chosen again. Line L9 may bind variables: establishing $\mathit{clear}(A)$ from a step $\mathit{move}(?b, ?x, ?y)$ that asserts $\mathit{clear}(?x)$ adds $?x \approx A$ and leaves $?b$ free. Lines L17 to L20 skip a clobberer that is necessarily before $t$, because $t$ itself is then a white knight. The codesignation classes are a [union-find](/disjoint-set/) structure in which two different constants never meet, and the test for possible codesignation is [unification](/robinson-unification/) that respects the noncodesignations. The search uses iterative deepening on the number of steps, with a bound $N$ given by the user: with infinitely many constants there is no finite state space to bound the plan length.

## Example

Take the [Sussman anomaly](/sussman-anomaly/) with three schemas: $\mathit{move\text{-}to\text{-}table}(?b, ?x)$, $\mathit{move\text{-}from\text{-}table}(?b, ?y)$ and $\mathit{move}(?b, ?x, ?y)$, with $\mathit{block}(?x)$ as a precondition wherever $?x$ must be a block and with $?b \not\approx ?x$, $?b \not\approx ?y$, $?x \not\approx ?y$. The initial state is $\mathit{on}(C, A)$, $\mathit{ontable}(A)$, $\mathit{ontable}(B)$, $\mathit{clear}(C)$, $\mathit{clear}(B)$ and $\mathit{block}$ of each block. The rounds $n = 0, 1, 2$ visit 1, 3 and 8 partial plans and fail. The round $n = 3$ goes straight to a plan in 7 nodes.

| step | precondition chosen | establishers | choice | declobbering |
|---|---|---|---|---|
| 1 | $\mathit{on}(A, B)$ at FINISH | 2 | new $S_A = \mathit{move\text{-}from\text{-}table}(?b_2, ?y_2)$, $?b_2 \approx A$, $?y_2 \approx B$ | none |
| 2 | $\mathit{on}(B, C)$ at FINISH | 2 | new $S_B = \mathit{move\text{-}from\text{-}table}(B, C)$ | none |
| 3 | $\mathit{clear}(A)$ at $S_A$ | 2 | new $S_C = \mathit{move\text{-}to\text{-}table}(?b_4, A)$, $?b_4$ free | none |
| 4 | $\mathit{clear}(B)$ at $S_B$ | 1 | START | $S_A$ denies $\mathit{clear}(B)$: promotion $S_B \prec S_A$ |
| 5 | $\mathit{on}(?b_4, A)$ at $S_C$ | 1 | START, which binds $?b_4 \approx C$ | none |
| 6 | $\mathit{clear}(C)$ at $S_C$ | 1 | START | $S_B$ denies $\mathit{clear}(C)$: promotion $S_C \prec S_B$ |

Many preconditions never need a step of their own. $\mathit{ontable}(A)$ at $S_A$ is necessarily true from the start, because START asserts it and no step can deny it. In step 3 the planner commits to moving *something* off $A$ before it knows what, and step 5 fills in the block. The result has the orderings $S_C \prec S_B \prec S_A$ and one completion: move $C$ to the table, $B$ onto $C$, $A$ onto $B$.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). It has five parts.

- **The criterion is sufficient.** If the MTC holds for $p$ at $s$, take any completion and suppose $p$ is false before $s$. After $t$ it is true, so some step $c$ between $t$ and $s$ denies it last. That $c$ is possibly before $s$ and possibly denies $p$, so the MTC gives a white knight after $c$ that asserts $p$ in this completion, a contradiction.
- **Soundness.** If the MTC holds for every precondition, then in every completion every step finds its preconditions true, so applying the effects in order is a real execution, and the goal holds at the end.
- **Progress.** Each refinement adds a step, an ordering pair, a codesignation or a noncodesignation, and with at most $n$ steps there are finitely many of each, so each round terminates.
- **Completeness.** Fix a ground solution $\sigma$ with at most $n$ actions. Keep a map from the steps to positions of $\sigma$ and a value of each variable that grounds each step to its action. Establish $p$ from the last position before $s$ whose action asserts the value of $p$. A clobberer cannot lie between that position and $s$ with the same value, since $\sigma$ would then fail, so demotion, promotion or separation agrees with $\sigma$.
- **Fewest steps.** With the cut test and iterative deepening, the first round that succeeds is the length of a shortest solution.

The tests check these claims. On 3,000 random plans with up to 3 steps, 3 variables and 2 constants, the MTC agrees with a brute force over all completions, using the constants of the plan plus one fresh constant per variable. On 150 random tasks written as schemas, TWEAK finds a plan with at most 3 steps if and only if breadth-first search over the ground task finds one, with the same length, and every completion of the plan is a solution when it is run.

## Complexity

One MTC test checks $O(n e)$ possible clobbers and, for each, $O(n e)$ possible white knights, so it costs $O(n^2 e^2)$ steps of unification once the transitive closure of $\prec$ is known, and line L7 tests all $O(n e)$ preconditions, which gives $O(n^3 e^3)$ per node. A refinement adds one of $O(n^2 e^2)$ possible constraints, which bounds the depth, and a node has $O((n + s) e)$ children. This gives the time bound above. It is crude, and it is exponential, which is unavoidable: already the ground case contains STRIPS plan existence, which is [PSPACE-complete](/strips-plan-existence-pspace-complete/). Depth-first search keeps one plan of size $O(n^2 e^2)$ per level.

On the Sussman task the four rounds visit 19 partial plans in all. POP on the same task, with 18 ground actions, visits 29, and most of the difference is that TWEAK needs no step for preconditions that hold from the start.

## Properties

- **Lifted.** Variables stay open until a precondition forces a value, as in step 3 of the example. This is a form of [least commitment](/least-commitment-principle/).
- **No causal links.** The plan does not record why a step is there. A precondition that was true can become false when a later step is added, and the MTC finds it again.
- **Not systematic.** Different branches can reach the same plan, and different plans can share completions. McAllester and Rosenblitt point out that the choices inside the criterion do not split the space of plans into disjoint parts.
- **Sound and complete** within the step bound, for representations where the criterion is exact.
- **The criterion breaks with richer actions.** Chapman showed that when the effects of an action may depend on the state in which it runs, truth in a partial plan is no longer decided by a criterion of this form, and planning becomes undecidable.

## Variants and improvements

- **Causal links.** [POP](/pop-partial-order-planning/) and [SNLP](/snlp/) replace the criterion by links and threats. They need no global truth test at each node, and SNLP is systematic.
- **New white knights.** Chapman's procedure may also add a new step as a white knight. The completeness proof does not need it, so the implementation only uses existing steps.
- **Finite domains.** With finitely many constants the criterion stays sufficient, since every finite completion is also a completion over infinitely many constants, but it is no longer necessary: two noncodesignations can exhaust the domain. Exact necessary truth is then co-NP-hard (Kambhampati and Nau 1996).
- **Possible truth.** Deciding whether a proposition is true in *some* completion is NP-hard (Kambhampati and Nau 1996), so planners that reason about possible truth pay more.
- **Refinement search.** Kambhampati, Knoblock and Yang (1995) describe TWEAK and the causal-link planners in one framework, as different ways to split the set of candidate plans.

## When to use it

Use TWEAK to understand necessary truth in partial plans, lifted planning, and the cost of reasoning without causal links. It also suits small domains with many objects, where grounding every action is too costly and late binding pays. For practical planning use a causal-link planner such as [UCPOP](/ucpop/), which also handles conditional effects, or state-space search with a heuristic.

## Pitfalls

- **Possible and necessary.** The clobberer test uses possible codesignation and possible ordering; the establisher and the white knight need necessary ones. Mixing them up makes the criterion unsound.
- **Codesignation is not just equality of names.** $?x \approx ?y$ and $?y \approx A$ give $?x \approx A$. Use union-find with constants as roots, and check the noncodesignations after each merge.
- **Unification leaves state behind.** A failed unification must not change the bindings. Work on a copy.
- **Finite domains.** The criterion assumes infinitely many constants. With a finite domain, a precondition can be necessarily true and still fail the criterion, which costs extra search, and noncodesignations can leave a variable with no legal value, so that the plan has no completion at all. Add type preconditions such as $\mathit{block}(?x)$, as in the example, so that every variable is bound to a constant from the initial state.
- **A step that asserts and denies the same thing.** The criterion assumes that no step asserts and denies codesignating propositions. Check the schemas.
- **No bound.** Without a step bound the search may add steps for ever. Plan existence in this setting has no general decision procedure.

## Implementations

## History

Sacerdoti's NOAH (1975) and Tate's NONLIN (1977) built partial-order plans, but their correctness was unclear. Chapman (1987) gave the first rigorous treatment. He defined necessary and possible truth in a partial plan, stated the modal truth criterion, built TWEAK as a nondeterministic procedure that reads the criterion as a list of ways to make a precondition true, and proved TWEAK correct and complete. He also proved that planning is undecidable for slightly richer representations, a result that set limits for the field. McAllester and Rosenblitt (1991) avoided the criterion with causal links. Kambhampati and Nau (1996) showed that the criterion is exact for necessary truth in TWEAK's representation and polynomial, argued that a complete planner does not need it, and settled the complexity of necessary and possible truth.

## References
