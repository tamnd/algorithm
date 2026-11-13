---
tag: 9M4E8C
kind: algorithm
slug: ucpop
name: UCPOP
aliases:
- Universal Conditional Partial Order Planner
area: games-and-search/planning
level: advanced
summary: A causal-link planner for actions with conditional effects, negative goals and quantifiers. It adds confrontation, which blocks a threatening effect by making its condition false.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the bound on the number of steps, a: the number of effects of all ground actions together, f: the number of facts}
  time: {worst: O(n^2 f a (n a)^(n (n + f)))}
  space: {extra: O(n^2 (n + f)^2)}
properties: {deterministic: true, online: false, exact: true, recursive: true}
history:
  year: 1992
  people: [J. Scott Penberthy, Daniel S. Weld]
  note: Penberthy and Weld extended the causal-link planner of McAllester and Rosenblitt to Pednault's ADL, with conditional and universally quantified effects, and proved it sound and complete.
prereqs: [pop-partial-order-planning, conditional-effects]
see_also: [snlp, tweak, causal-link, partial-order-plan, closed-world-assumption, pddl, graphplan, sussman-anomaly]
sources:
  - paper: "J. Scott Penberthy and Daniel S. Weld, UCPOP: a sound, complete, partial order planner for ADL, Proceedings of KR-92, Morgan Kaufmann, isbn 1558602623"
    locator: pp. 103 to 114 (the planner, conditional and universally quantified effects, confrontation, soundness and completeness)
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (POP, its extension to conditional effects and quantification, confrontation, the briefcase example; general locator)
  - paper: "David McAllester and David Rosenblitt, Systematic nonlinear planning, Proceedings of AAAI-91"
    locator: pp. 634 to 639 (the causal-link planner that UCPOP extends)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (plan-space planning and its extensions to more expressive actions; general locator)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (partial-order planning and extended action languages; general locator)
---

UCPOP is a causal-link planner in the style of [POP](/pop-partial-order-planning/) for actions with [conditional effects](/conditional-effects/). An effect of an action happens only if its condition holds in the state where the action runs, so a step can achieve a fact in one context and destroy it in another. UCPOP links an open goal to one effect of a step and adds the condition of that effect as new goals of the step. A threat comes from an effect that may make a linked literal false, and besides demotion and promotion UCPOP can resolve it by **confrontation**: it adds the goal that the condition of the threatening effect is false when the step runs. Goals may be negative literals, read under the [closed world assumption](/closed-world-assumption/). Penberthy and Weld (1992) also handle variables and universally quantified goals and effects; over a finite set of objects these expand into the ground conditional effects treated here.

## In plain words

Some actions do different things in different situations. Driving the car to work moves everything that is in the car, so whether your bag ends up at work depends on whether it was in the car.

The planner works like POP. To get a need met, it points to one effect of a step, and then that step also needs the effect's condition: the bag must be in the car when you drive. A threat is an effect that could undo a promise between giver and taker. You can still move the threatening step out of the way. But there is now a third fix: make sure its harmful effect does not happen, by adding the need that its condition is false. If you must drive but your wallet must stay home, take the wallet out of the car first.

## The problem

The input is a ground task with conditional effects. A literal is a fact $f$ or its negation $\neg f$. An action $a$ has a precondition $\mathit{pre}(a)$, a set of literals, and a list of effects; each effect $e$ has a condition $\mathit{cond}(e)$, a set of literals, an add list and a delete list. In a state $s$, $a$ applies if $\mathit{pre}(a)$ holds, and every effect whose condition holds in $s$ fires: the next state is $s$ minus the deletes of the fired effects, plus their adds. We require that two effects that can fire together never add and delete the same fact. The initial state $I$ is a set of facts, every other fact is false, and the goal $G$ is a set of literals. The output is a partial-order plan whose every linearization is a solution, or failure.

A partial plan has steps, an acyclic ordering $\prec$, a set of goals $(\ell, j)$, and causal links $i \xrightarrow{e,\ell} j$: effect $e$ of step $i$ makes $\ell$ true, that is it adds $f$ if $\ell = f$ and deletes $f$ if $\ell = \neg f$. START makes every literal true in the closed world of $I$. The goals of a step are its precondition, the conditions of its effects that some link uses, and the confrontation goals. The flaws are:

- an **open goal** $(\ell, j)$: a goal with no link into it;
- a **threat** $(k, e', i \xrightarrow{e,\ell} j)$: effect $e'$ of a step $k \ne i, j$ makes $\neg \ell$ true, $k$ may lie between $i$ and $j$, and no goal $(\neg c, k)$ with $c \in \mathit{cond}(e')$ has been posted yet.

## The algorithm

```pseudo id=main
UCPOP(I, G, A)
L1  for n ← 0, 1, ..., 2^|F| − 1 do
L2      cut ← false
L3      Q ← REFINE(the plan START ≺ FINISH for I and G, A, n)
L4      if Q ≠ failure then return Q
L5      if cut = false then return failure          ▷ a larger n gives the same tree
L6  return failure
REFINE(P, A, n)
L7  if P has no open goal and no threat then return P
L8  f ← a flaw of P with the fewest resolvers
L9  if f is a threat (k, e', i -ℓ-> j) then
L10     R ← the orderings k ≺ i (demotion) and j ≺ k (promotion) that keep ≺ acyclic
L11     add to R the goal (¬c, k) for each c ∈ cond(e')    ▷ confrontation
L12 else f is an open goal (ℓ, j):
L13     R ← a link i -e,ℓ-> j for each step i not after j and each effect e of i that makes ℓ; the link adds the goals (c, i) for c ∈ cond(e)
L14     if P has fewer than n steps then add to R a new step for each action a and effect e of a that makes ℓ, linked to j, with the goals pre(a)
L15     else if some effect of some action makes ℓ then cut ← true
L16 for each r in R do                              ▷ the choice point
L17     Q ← REFINE(P with r, A, n)
L18     if Q ≠ failure then return Q
L19 return failure
```

Line L13 is the main change from POP: a link chooses an effect, and the effect's condition becomes a goal of the producer, so the effect is sure to fire. Line L11 is confrontation. It does not order anything: it asks that one literal of the condition of $e'$ be false before $k$, and that goal is then linked and protected like any other. A threat stops counting as soon as such a goal exists, since in a complete plan that goal holds and $e'$ cannot fire. Negative goals are linked from START when the fact is absent from $I$, or from an effect that deletes the fact.

## Example

The briefcase task is due to Pednault. The briefcase $B$, the paycheck $P$ and the dictionary $D$ are at home, and the paycheck is in the briefcase. The goal is $\mathit{at}(B, \mathit{office})$, $\mathit{at}(D, \mathit{office})$ and $\mathit{at}(P, \mathit{home})$. The action $\mathit{move\text{-}b}(l_1, l_2)$ moves the briefcase and has one conditional effect for each object $x$: if $\mathit{in}(x)$, then $x$ moves too. This is the ground form of the universally quantified effect "every object in the briefcase moves". The actions $\mathit{take\text{-}out}(x)$ and $\mathit{put\text{-}in}(x, l)$ change $\mathit{in}(x)$. There are 8 ground actions. The rounds $n = 0, 1, 2$ visit 1, 4 and 10 partial plans and fail; the round $n = 3$ reaches a complete plan in 12 nodes, with no backtracking.

| refinement | flaw chosen | resolvers | choice |
|---|---|---|---|
| 1 | open $\mathit{at}(B, \mathit{office})$ at FINISH | 1 | new step $M = \mathit{move\text{-}b}(\mathit{home}, \mathit{office})$, its unconditional effect |
| 2 | open $\mathit{at}(B, \mathit{home})$ at $M$ | 2 | link from START |
| 3 | open $\mathit{at}(D, \mathit{office})$ at FINISH | 2 | link from the effect "if $\mathit{in}(D)$, $D$ moves" of $M$, which posts the goal $\mathit{in}(D)$ at $M$ |
| 4 | open $\mathit{at}(P, \mathit{home})$ at FINISH | 2 | link from START |
| 5 | threat: the effect "if $\mathit{in}(P)$, $P$ moves" of $M$ against START $\to$ FINISH on $\mathit{at}(P, \mathit{home})$ | 1 | confrontation: goal $\neg \mathit{in}(P)$ at $M$ |
| 6 | open $\neg \mathit{in}(P)$ at $M$ | 1 | new step $\mathit{take\text{-}out}(P)$ |
| 7 | open $\mathit{in}(D)$ at $M$ | 2 | new step $\mathit{put\text{-}in}(D, \mathit{home})$ |
| 8 to 11 | the preconditions of the two new steps | 1 each | links from START |

In row 5, demotion would put $M$ before START and promotion would put it after FINISH, so confrontation is the only way out. Without it the paycheck could not stay at home, since nothing can order the move outside the protected interval from START to FINISH. The result has two linearizations: take out $P$ and put in $D$ in either order, then move the briefcase. Breadth-first search on the same task also finds 3 steps.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). There are four parts.

- **Soundness.** In a linearization of a complete plan, show by induction along the order that every goal of every step holds before the step. For a link $i \xrightarrow{e,\ell} j$, the condition of $e$ is a goal of $i$, so $e$ fires and makes $\ell$ true. An effect $e'$ of a step between $i$ and $j$ that would make $\ell$ false has a confrontation goal $\neg c$, which holds before that step, so $e'$ does not fire.
- **Termination.** Each refinement adds a step, a link, a new ordering pair or a new goal, and with at most $n$ steps there are finitely many of each.
- **Completeness.** Fix a solution $\sigma$ with at most $n$ actions. For an open goal $(\ell, j)$, link from the last position of $\sigma$ before $j$ where a fired effect makes $\ell$ true, or from START if there is none. For a threat whose step lies between the ends in $\sigma$, its effect did not fire there, so some literal of its condition was false, and confrontation with that literal agrees with $\sigma$. Otherwise demotion or promotion agrees with $\sigma$.
- **Fewest steps.** As for POP, iterative deepening returns a plan with as few steps as a shortest solution.

The tests compile each task into STRIPS with negative preconditions, one action for each way its effects can fire, and check that breadth-first search gives the same length on the compiled and on the original task, for 300 random tasks. On 300 more random tasks, UCPOP finds a plan if and only if a plan exists, with the same length, and every linearization of the plan is a solution. Every complete plan of a bounded search over 150 random tasks is a solution, and the briefcase plan contains the confrontation goal $\neg \mathit{in}(P)$ at the move step.

## Complexity

A plan has at most $n + 2$ steps, each with at most $2 f$ goals, so there are $O(n f)$ goals and links over the life of a branch, and $O(n^2)$ ordering pairs. Each refinement adds one of them, so a branch has depth $O(n (n + f))$. A flaw has $O(n a)$ resolvers. Finding the threats checks each link against each effect of each step, $O(n^2 f a)$ tests with a precomputed closure. This gives the bound above. It is exponential, as it must be, since the task contains STRIPS planning, whose plan existence problem is [PSPACE-complete](/strips-plan-existence-pspace-complete/). Depth-first search keeps one plan per level.

Conditional effects do not raise the worst case by much, but they make the search wider in practice. The STRIPS compilation of the tests turns an action with $c$ conditional effects into one action for each way the effects can fire or fail, which is at least $2^c$ when the conditions are independent, while UCPOP keeps one action and decides about each effect only when a link or a threat forces it.

## Properties

- **Sound and complete** within the step bound, like POP.
- **Least commitment about effects.** UCPOP does not decide which effects of a step fire until a link needs one or a threat must be blocked. See the [least commitment principle](/least-commitment-principle/).
- **Closed world.** Negative goals are true in the initial state unless the fact is listed, which matches [STRIPS](/strips/) and [PDDL](/pddl/).
- **Not systematic.** Like POP it counts only harmful effects as threats, so two complete plans can share a linearization. A systematic version follows [SNLP](/snlp/) and also counts effects that make $\ell$ true.
- **One action, many outcomes.** A step is one action, but different links can use different effects of it, each with its own condition.

## Variants and improvements

- **Lifted UCPOP.** The original works with variables and codesignation constraints, as in [TWEAK](/tweak/) and lifted SNLP, so it never grounds the actions.
- **Universal quantification.** Penberthy and Weld allow goals and effects quantified over the objects of a type. With a finite set of objects, a universal goal is a conjunction and a universal effect is one conditional effect per object, which is how the briefcase is encoded here.
- **Disjunctive preconditions.** ADL also allows disjunctive goals, which a planner handles by a choice among the disjuncts.
- **Better search control.** Later causal-link planners in this line replaced depth-first search by best-first search with estimates of the remaining work, which made partial-order planning competitive again on some benchmarks.
- **STRIPS compilation.** Conditional effects can also be compiled away, as in the tests, at the price of many more actions; [Graphplan](/graphplan/) and state-space planners often handle them directly instead.

## When to use it

Use UCPOP when actions have effects that depend on the state, such as a move that carries the contents of a container, and a flexible partial-order plan is wanted. It is the standard textbook planner for ADL-style actions and a good base for teaching plan-space planning beyond STRIPS. For speed on large tasks, use a state-space planner with a heuristic that supports conditional effects.

## Pitfalls

- **Forgetting the effect condition.** A link from a conditional effect must add the condition as a goal of the producer. Otherwise the plan relies on an effect that may not fire.
- **Confrontation is a new goal, not a check.** The negated condition must be linked and protected like any goal. Treating the threat as resolved without that goal is unsound.
- **One literal at a time.** To stop an effect it suffices that one literal of its condition be false, so each literal is a separate resolver. Requiring all of them to be false is incomplete.
- **Effects that conflict.** If two effects of one action can fire together and one adds what the other deletes, the outcome depends on the convention. The implementation rejects such actions.
- **Negative goals and the initial state.** Under the closed world assumption, START makes $\neg f$ for every fact $f$ not in $I$, and links from START can support negative goals.

## Implementations

## History

Pednault (1989) defined ADL, an action language between STRIPS and the situation calculus with conditional effects and quantifiers, and showed how to regress goals through such actions with secondary preconditions, the conditions that make an effect fire or not fire. Penberthy and Weld (1992) combined this with the causal-link planner of McAllester and Rosenblitt (1991) and proved the result sound and complete; confrontation is the plan-space form of a secondary precondition. Weld's tutorial (1994) presented POP and UCPOP side by side, with the briefcase as the standard example, and the planner became a common base for research on partial-order planning in the 1990s. ADL features such as conditional effects and quantifiers later entered [PDDL](/pddl/).

## References
