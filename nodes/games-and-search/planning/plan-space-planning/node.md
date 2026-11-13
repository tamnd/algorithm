---
tag: A9JNM8
kind: technique
slug: plan-space-planning
name: Plan-space planning
aliases:
- partial-order planning search
area: games-and-search/planning
level: core
summary: Planning by search in the space of partial plans. A node is a plan with open preconditions and threats as flaws, and an edge adds a step, a causal link, an ordering or a binding that repairs one flaw.
prereqs: [partial-order-plan, causal-link, strips]
see_also: [pop-partial-order-planning, snlp, tweak, ucpop, state-space-planning, least-commitment-principle, sussman-anomaly, htn-decomposition]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (plan-space planning; the PSP procedure, flaws and resolvers, its soundness and completeness, and the PoP variant)
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (the search in plan space, POP and UCPOP, and the role of flaw selection)
  - paper: doi:10.1016/0004-3702(94)00076-D
    title: "Subbarao Kambhampati, Craig A. Knoblock and Qiang Yang, Planning as refinement search: a unified framework for evaluating design tradeoffs in partial-order planning, Artificial Intelligence 76 (1995)"
    locator: pp. 167 to 238 (refinement search, candidate sets, and the design choices that separate the plan-space planners; general locator)
  - paper: "Earl D. Sacerdoti, The nonlinear nature of plans, Proceedings of IJCAI-75"
    locator: pp. 206 to 214 (NOAH and its procedural nets, the first partially ordered plans)
  - paper: "Austin Tate, Generating project networks, Proceedings of IJCAI-77"
    locator: pp. 888 to 893 (NONLIN, goal structure and the protection of conditions)
---

Plan-space planning solves a planning task by search in a graph whose nodes are partial plans, not world states. A node is a [partial-order plan](/partial-order-plan/): a set of steps with ordering constraints, [causal links](/causal-link/) and, for actions with variables, binding constraints. The start node holds only a START step, whose effects are the initial state, and a FINISH step, whose preconditions are the goal. Every node lists its flaws: open preconditions, which no link supports, and threats, steps that may undo a link. An edge picks one flaw and adds a resolver, which is a new step, a new link, an ordering or a binding. A node without flaws is a solution: all of its linearizations are valid plans. The general method is the template below. [POP](/pop-partial-order-planning/), [SNLP](/snlp/), [TWEAK](/tweak/) and [UCPOP](/ucpop/) fill its holes in different ways. It differs from [state-space planning](/state-space-planning/), whose nodes are states or goal descriptions.

## In plain words

Instead of building a plan from the first action to the last, you sketch it. At first the sketch says only "start" and "finish", and the finish needs the goal.

Then you fix what is wrong with the sketch, one thing at a time. A need with no supplier is fixed by naming a step that supplies it, old or new. A step that could spoil a supply is fixed by moving it before the supplier or after the user.

Each fix adds a little to the sketch and never takes anything away. Some fixes lead to a dead end, and then you go back and try another fix.

When nothing is wrong, the sketch is done. It may leave some steps unordered, and any order it allows works.

## When it applies

- The task is a [classical planning](/classical-planning/) task in a STRIPS-like language: actions with preconditions and effects, an initial state and a goal. The template also works with variables in actions, with conditional effects and quantifiers, and with time constraints, provided the language comes with a list of flaw types and resolvers.
- The goals interact in ways that a planner that works on one goal at a time gets wrong, or the output should be flexible: a partial order that a scheduler or several agents can execute in any allowed order.
- An explanation is wanted: every causal link says why its step is in the plan.
- It is less suited to large tasks without a good heuristic for partial plans. Partial plans have no current state, so the strong state-based heuristics of forward search do not apply directly.

## The template

```pseudo id=main
PLAN-SPACE-PLAN(I, G, A, frontier)
L1  P0 ← the plan START ≺ FINISH, where START adds I and FINISH needs G
L2  frontier.insert(P0)
L3  while frontier is not empty do
L4      P ← frontier.remove()                           ▷ hole: the search strategy
L5      if P has no flaw then return P
L6      f ← a flaw of P                                 ▷ hole: flaw selection, not a choice point
L7      for each resolver r of f do                     ▷ hole: the flaws and resolvers of the language
L8          P′ ← P with the constraints of r added
L9          if P′ is consistent then frontier.insert(P′)
L10 return failure
```

**The holes.**

- *Line L4, the strategy.* A stack with a bound on the number of steps gives depth-first search, and raising the bound gives [iterative deepening](/iterative-deepening-search/), as on the POP page. A priority queue gives best-first search; common estimates are the number of steps plus the number of open preconditions, or a reachability estimate of the cost to close the open preconditions.
- *Line L6, flaw selection.* Every flaw must be repaired in the end, so the choice of flaw is not a backtracking point: any rule keeps the search complete. The rule changes the size of the search a lot. Choosing the flaw with the fewest resolvers first fails fast, and resolving threats early keeps plans small.
- *Line L7, the language.* For ground STRIPS, an open precondition $(p, j)$ is resolved by a link from an existing step that adds $p$ and may come before $j$, or by a new step that adds $p$. A threat $(k, i \xrightarrow{p} j)$ is resolved by demotion, $k \prec i$, or promotion, $j \prec k$. Variables add separation, a binding that keeps the threatening fact from unifying with $p$. Conditional effects add confrontation, a new goal that keeps the threatening effect from firing. [SNLP](/snlp/) also counts a step that adds $p$ as a threat, for systematicity.
- *Line L9, consistency.* The orderings must stay acyclic, and the bindings must have a model. Both tests are cheap for ground plans; see the [partial-order plan](/partial-order-plan/) page.

**Why the template is sound.** A plan without flaws has a causal link for every precondition and no step that can fall between the ends of a link whose fact it deletes, so every linearization is a valid plan. This is the solution law, proved on the [partial-order plan](/partial-order-plan/) page.

**Why it is complete.** Think of each partial plan as the set of action sequences that are consistent with it, its candidates. A set of resolvers is complete for a flaw if every solution that is a candidate of $P$ is also a candidate of some child. With complete resolvers, a solution present at the root stays present along some branch. A complete strategy, such as iterative deepening on the number of steps, or best-first search with a cost that grows along every branch, then reaches a flawless plan. The proofs for each planner are on their pages.

**Cost.** With at most $n$ steps, $a$ ground actions and at most $p$ preconditions per step, a branch adds at most $n$ steps, $n (n + p)$ links and $O(n^2)$ orderings, and each node has at most $n + a$ children, so the search tree has $(n + a)^{O(n (n + p))}$ nodes; the POP page gives the exact bound. The worst case cannot be avoided: [STRIPS plan existence is PSPACE-complete](/strips-plan-existence-pspace-complete/), and a shortest plan can be exponentially long.

## Classic examples

### The Sussman anomaly

In the [Sussman anomaly](/sussman-anomaly/), C is on A, A and B are on the table, and the goal is A on B and B on C. A planner that achieves one goal completely and then the other fails with either order. A plan-space planner adds a step for each goal, $\mathit{move}(A, \mathit{table}, B)$ and $\mathit{move}(B, \mathit{table}, C)$, without ordering them. The step that clears A, $\mathit{move}(C, A, \mathit{table})$, comes in for an open precondition. Then two threats appear: moving B onto C deletes $\mathit{clear}(C)$, which the move of C needs, and moving A onto B deletes $\mathit{clear}(B)$, which the move of B needs. Each has only one resolver, promotion, and the two promotions give the unique shortest plan: C to the table, B onto C, A onto B. The goals were never ordered by a guess.

The planners on the pages of this family give these counts on the task, with iterative deepening on the number of steps:

| planner | plan language | partial plans visited, all rounds |
|---|---|---|
| [POP](/pop-partial-order-planning/) | 18 ground move actions | 29 (rounds of 1, 3, 7 and 18) |
| [TWEAK](/tweak/) | 3 move schemas with variables | 19 (rounds of 1, 3, 8 and 7) |

### Independent goals

Pednault's briefcase task, with the conditional effects of [UCPOP](/ucpop/), asks for the dictionary and the briefcase at the office and the paycheck at home. UCPOP returns a plan in which taking the paycheck out and putting the dictionary in are unordered, and both come before the move of the briefcase. A state-space planner would return one of the two orders. The plan-space plan keeps both, and an executor may choose either.

### Redundant and systematic search

Take actions $A$, which adds $p$; $R$, which needs $p$ and adds $r$; and $S$, which needs $p$ and adds $s$, with an empty initial state and the goal $\{p, r, s\}$. Enumerating all complete plans with at most 4 steps gives 4 plans in both POP and SNLP. Under POP's threat rule they have 16 linearizations but only 8 distinct sequences, and one sequence belongs to 3 of the plans. Under SNLP's rule, where a step that adds $p$ also threatens a link for $p$, they have 6 linearizations, all distinct. The table is on the [SNLP](/snlp/) page.

## Variations

- **POP.** Ground STRIPS, causal links, demotion and promotion; the simplest sound and complete form. See [POP](/pop-partial-order-planning/).
- **SNLP.** Adds the systematic threat, so that no candidate sequence is reached through two complete plans. See [SNLP](/snlp/).
- **TWEAK.** No causal links; each precondition is checked with the modal truth criterion, and repaired by establishment and declobbering, which includes white knights. See [TWEAK](/tweak/).
- **UCPOP.** Conditional effects, negative goals and quantifiers, with confrontation as a third threat resolver. See [UCPOP](/ucpop/).
- **Hierarchical plan-space planning.** NOAH, NONLIN, SIPE, O-Plan and UMCP add a third flaw type, a compound task that is not yet decomposed, and its resolvers are the methods of the task. See [hierarchical task network](/hierarchical-task-network/).
- **Heuristic plan-space planning.** Later causal-link planners, such as RePOP and VHPOP, use best-first search with reachability heuristics computed from a relaxed planning graph and became far faster than the planners of the early 1990s.
- **Temporal plan-space planning.** The orderings become a network of time constraints between the start and end points of durative actions.

## Pitfalls

- **Backtracking over the flaw choice.** The flaw at line L6 is not a choice point. A planner that also backtracks over it explores the same plans many times and gains nothing.
- **Unbounded depth-first search.** A planner can add a new step for the same open precondition again and again. Depth-first search needs a bound, or the strategy must be complete in another way.
- **Threat tests on stored pairs only.** Whether $k$ can fall between $i$ and $j$ depends on chains of orderings. Testing only the stored pairs reports false threats and adds useless orderings.
- **Reading a solution as a sequence.** A solution with unordered steps is a set of sequences. Executing two unordered steps at the same time is safe only if the action model says so; a partial order of STRIPS steps promises only that every sequence works.
- **Expecting a shortest plan from best-first search.** Iterative deepening on the number of steps gives a plan with the fewest steps. Best-first search with an inadmissible estimate gives no such guarantee.

## Exercises

1. Give a task with two goals that a goal-at-a-time planner solves in one order but not in the other, and show the partial plan that a plan-space planner returns for it.
2. Prove that the template stays complete for any flaw selection rule at line L6, when the resolvers of every flaw are complete and the strategy is iterative deepening on the number of steps.
3. In a ground plan with $n$ steps, how many threats can there be, and what is the cost of listing them?
4. Show that two different branches of POP's search tree can end in complete plans that share a linearization, and that SNLP's threat rule makes this impossible.
5. Extend the template with variables. What flaws does a binding constraint create, and what is separation?

## References
