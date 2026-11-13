---
tag: 33TKWV
kind: concept
slug: least-commitment-principle
name: Least commitment principle
area: games-and-search/planning
level: advanced
summary: The planning heuristic of making a decision, such as an order between steps or a value for a variable, only when a flaw forces it. One partial plan then stands for many sequences.
prereqs: [partial-order-plan]
see_also: [plan-space-planning, pop-partial-order-planning, tweak, causal-link, state-space-planning, least-constraining-value, constraint-propagation, sussman-anomaly]
sources:
  - paper: doi:10.1609/aimag.v15i4.1109
    title: "Daniel S. Weld, An introduction to least commitment planning, AI Magazine 15(4) (1994)"
    locator: pp. 27 to 61 (least commitment in orderings and bindings, and the planners built on it)
  - paper: doi:10.1016/0004-3702(94)90012-4
    title: "Anthony Barrett and Daniel S. Weld, Partial-order planning: evaluating possible efficiency gains, Artificial Intelligence 67(1) (1994)"
    locator: pp. 71 to 112 (when delaying orderings pays, with serializable and laboriously serializable goals; general locator)
  - paper: doi:10.1016/0004-3702(94)00076-D
    title: "Subbarao Kambhampati, Craig A. Knoblock and Qiang Yang, Planning as refinement search: a unified framework for evaluating design tradeoffs in partial-order planning, Artificial Intelligence 76 (1995)"
    locator: pp. 167 to 238 (commitment, redundancy and the cost of the consistency test as design choices of refinement planners; general locator)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 5 (the least commitment principle in plan-space planning)
---

The least commitment principle says that a planner should not make a choice until it has to. A planner that searches over sequences must decide, at every step, which action comes next, and so it fixes the relative order of every pair of actions. A planner that follows the principle adds an ordering only to resolve a threat, and binds a variable of an action only when a precondition or a threat requires it. A [partial-order plan](/partial-order-plan/) with few orderings and few bindings stands for every sequence and every value that its constraints allow. A wrong commitment is never made, so it never has to be undone by backtracking. The principle is a heuristic, not a theorem. Fewer commitments mean larger sets of candidates per plan, but also weaker information for search control and costlier consistency tests.

## In plain words

If you do not know yet in what order to do two jobs, do not pick one. Write both down and leave the order open. Pick an order only when something forces it, for example when one job would undo what the other needs.

The same goes for details. If a step needs "some free block", do not name the block yet. Wait until another part of the plan says which block it must be.

A guess made too early can be wrong, and then you have to go back and undo work that depended on it. A choice made late is made with more information.

But waiting has a price. A vague plan is harder to check, and it tells you less about what to try next.

## The idea

A planner refines a partial plan by adding constraints. Each partial plan $P$ has a candidate set: the action sequences that satisfy all of its constraints, in the sense of refinement planning. For a [partial-order plan](/partial-order-plan/) the candidates of a ground plan are its linearizations; for a lifted plan they are also its ground instances. A refinement shrinks the candidate set, and a search that commits less shrinks it more slowly.

There are three kinds of commitment.

- **Ordering.** A forward [state-space planner](/state-space-planning/) commits to the full order at once. A plan-space planner such as [POP](/pop-partial-order-planning/) adds $k \prec i$ or $j \prec k$ only to resolve a threat to a [causal link](/causal-link/).
- **Binding.** A lifted planner such as [TWEAK](/tweak/) or [UCPOP](/ucpop/) adds a step $\mathit{move}(x, y, z)$ with free variables and adds $x = A$ or $x \ne A$ only when a precondition or a threat needs it. Ground planners commit to every value when they add a step.
- **Support.** A planner with causal links commits to the step that supplies each precondition. TWEAK delays even this choice, and lets the modal truth criterion decide, for each completion, which step makes a fact true.

The gain: a planner with ordering commitment must also choose, at each step, which goal to work on, and a wrong choice can force it to backtrack over the order of goals. In the [Sussman anomaly](/sussman-anomaly/) every fixed order of the two goals fails for a planner that achieves goals one at a time. A plan-space planner adds both goal steps unordered and lets the threats between them decide the order.

The costs:

- **Weaker information.** A forward state-space planner knows the current state, so it can compute a heuristic estimate from it. A partial plan has no single current state, and good heuristics for it are harder to get.
- **Costlier tests.** With fewer constraints, a test such as "is $p$ true before step $j$ in every completion?" quantifies over more completions. For TWEAK's language it is polynomial. Chapman showed that with conditional effects it becomes NP-hard. Causal-link planners such as UCPOP never ask it: they commit to a producer for each precondition and check threats instead.
- **Redundant work.** A planner that delays choices can reach the same candidate sequences through several plans. SNLP adds a commitment, systematic causal links, exactly to avoid this.

So the right amount of commitment depends on the domain. Barrett and Weld found that delaying orderings pays when goals interact, and Kambhampati, Knoblock and Yang analysed commitment as one of several tradeoffs that make one refinement planner faster than another.

## Examples

**Independent jobs.** Two goals each need a chain of 3 actions, and the chains do not interact. A partial-order plan for them has 6 steps, two chains of orderings, and no ordering between the chains. It stands for $\binom{6}{3} = 20$ sequences, all valid, and the planner never had to choose one. It can hand the two chains to two agents that work in parallel.

**A late binding.** In the [blocks world](/blocks-world/) the goal $\mathit{clear}(A)$ with $C$ on $A$ is supported by a step $\mathit{move}(x, y, z)$ that adds $\mathit{clear}(y)$. Unification with the goal binds $y = A$. The precondition $\mathit{on}(x, A)$ is supported by the initial state, which binds $x = C$. The destination $z$ stays free until a precondition $\mathit{clear}(z)$ or a threat fixes it. A ground planner would have tried one step for each destination.

**Too little commitment.** Suppose a partial plan has $t$ threats, each with two resolutions, and a dead end that shows only when a certain precondition is examined. If that precondition is examined last, the planner can try up to $2^t$ combinations of resolutions before it gives up the branch. A forward planner with a fixed sequence knows the state at each step and would see the dead end as soon as it reached it. Here commitment gives better search control, and the remedy in plan-space planners is a good flaw order, such as "fewest resolvers first".

## Where it is used

- **Plan-space planning.** NOAH used partial orders, and Weld's survey made "least commitment planning" the name of the family that includes [POP](/pop-partial-order-planning/), [SNLP](/snlp/), [TWEAK](/tweak/) and [UCPOP](/ucpop/); see [plan-space planning](/plan-space-planning/).
- **Constraint posting.** Stefik's MOLGEN planner added constraints on variables instead of choosing values, the same idea for bindings. Modern constraint-based planners and schedulers keep start times and resources as variables with constraints and decide them late.
- **Temporal planning and scheduling.** Plans with time windows keep a network of distance constraints, so that the start times can be chosen at execution time.
- **Constraint satisfaction.** The [least constraining value](/least-constraining-value/) heuristic and [constraint propagation](/constraint-propagation/) express a related idea: prefer the choices that rule out the fewest options, and deduce what is forced before guessing.
- **HTN planning.** Decomposition planners can leave the method of a task open until its subtasks interact, though SHOP-style planners commit early to know the current state.

## References
