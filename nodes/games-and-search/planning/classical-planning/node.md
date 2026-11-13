---
tag: M1BM1K
kind: problem
slug: classical-planning
name: Classical planning
aliases:
- STRIPS planning
- propositional planning
area: games-and-search/planning
level: intro
summary: Find an action sequence from an initial state to a goal state in a deterministic, fully observable world.
prereqs: [state-space]
see_also: [strips, pddl, sas-plus, blocks-world, state-space-planning, optimal-planning, strips-plan-existence-pspace-complete, delete-relaxation]
sources:
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 1 (the restricted model and its assumptions); Chapter 2 (representations of classical planning problems); Chapter 3 (complexity)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11, Section 11.1 (definition of classical planning)
  - book: isbn:9783031004360
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: the chapters on classical planning and on heuristic search planning (general locator)
  - paper: doi:10.1016/0004-3702(71)90010-5
    title: "Richard E. Fikes and Nils J. Nilsson, STRIPS: A new approach to the application of theorem proving to problem solving, Artificial Intelligence 2(3-4) (1971)"
    locator: pp. 189 to 208
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: pp. 165 to 204
---

Classical planning is the problem of finding a sequence of actions that takes a world from a known initial state to a state that satisfies a goal, when the world is finite, fully observable, deterministic and changes only by the agent's actions. The task is given in a compact language such as [STRIPS](/strips/) or [PDDL](/pddl/), not as an explicit graph, so the [state space](/state-space/) is exponential in the size of the input. It is the base problem of automated planning: probabilistic, partially observable and temporal planning all relax one of its assumptions.

## In plain words

You know exactly how the world is now. You know what you want to be true at the end. You have a list of actions, and for each action you know when it can be used and what it changes. Nothing else changes the world, and no action has a surprise result. The job is to find a list of actions that gets you to the goal, or to say that no such list exists. A robot that must restack boxes, a truck fleet that must deliver parcels and a puzzle with sliding tiles all fit this frame. The hard part is size: a description of a few dozen lines can have more states than a computer can ever list.

## Definition

### The restricted model

Ghallab, Nau and Traverso list the assumptions that define classical planning. The world has finitely many states; it is fully observable; actions are deterministic; the world is static, so only actions change it; goals are sets of goal states; plans are finite sequences of actions; actions have no duration; and the planner works offline, with no change to the task during planning. Under these assumptions a plan is a path in a finite directed graph, and the planner never needs to observe the world while it executes the plan.

### The problem

The input is a [STRIPS](/strips/) task $\Pi = (F, A, I, G)$: a set of facts $F$, a set of actions $A$, each with a precondition, an add list and a delete list, an initial state $I \subseteq F$ and a goal $G \subseteq F$. A state is a subset of $F$, action $a$ is applicable in $s$ when $\mathit{pre}(a) \subseteq s$, and its result is $(s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. A plan is a sequence of actions, each applicable in turn, that starts in $I$ and ends in a state that contains $G$.

- Plan generation: output a plan, or report that none exists.
- Plan existence: decide whether a plan exists. This is a [decision problem](/decision-problem/).
- Optimal planning: output a plan of least length, or of least total cost when actions have costs $c(a) \ge 0$. This is [optimal planning](/optimal-planning/).

A planner that returns any plan is satisficing; one that returns a plan of least cost is optimal. Unless a task states costs, every action costs 1 and the plan length is the measure. Plans are sequential: one action at each step.

### Size of the input

The input size is the length of the list of all the sets of $\Pi$. The state space has up to $2^{|F|}$ states. A lifted task in PDDL is more compact again: [grounding](/grounding/) a schema with $k$ parameters over $o$ objects gives up to $o^k$ actions, and a predicate of arity $k$ gives up to $o^k$ facts. So the state space is exponential in the size of the ground task, and can be doubly exponential in the size of the lifted task when the arities are part of the input.

## Variants

- Bounded plan existence: is there a plan with at most $k$ actions? See [bounded-plan-existence-np-complete](/bounded-plan-existence-np-complete/).
- Richer action languages: negative preconditions, disjunctive preconditions, quantifiers and [conditional effects](/conditional-effects/) (ADL, full PDDL). These keep the classical assumptions but make the description shorter.
- Finite-domain variables: the [SAS+](/sas-plus/) model replaces facts by variables with small domains. It describes the same tasks.
- Delete-free planning: no action has a delete list. Plan existence is then polynomial, and the problem is used as a relaxation; see [delete relaxation](/delete-relaxation/).
- Relaxing the assumptions gives other fields: an unknown initial state gives [conformant planning](/conformant-planning/), observations during execution give [contingent planning](/contingent-planning/), random action results give a [Markov decision process](/markov-decision-process/) or [stochastic shortest path](/stochastic-shortest-path/) problem, and actions with durations give [temporal planning](/temporal-planning/).
- Hierarchical planning: the goal is a set of tasks to perform, refined by methods, not a set of facts to make true; see [HTN planning](/htn-planning/).

## Examples

### The Sussman anomaly

Three blocks: $C$ is on $A$, and $A$ and $B$ are on the table. The goal is $\mathit{on}(A, B)$ and $\mathit{on}(B, C)$. With one operator $\mathit{move}(b, x, y)$ (move clear block $b$ from $x$ to $y$) the unique shortest plan has 3 actions: move $C$ to the table, move $B$ onto $C$, move $A$ onto $B$. With the four operators pickup, putdown, stack and unstack, each move becomes two actions and the shortest plan has 6. No sequence of 2 moves, or of 5 actions with four operators, reaches the goal. The goal is a partial description: it does not say where $C$ is, and any state with the two facts is a goal state. This instance is the [Sussman anomaly](/sussman-anomaly/), and it shows why the two goals cannot be solved one after the other.

### A delivery task

A truck is at $l_1$, package $p_1$ is at $l_1$, package $p_2$ is at $l_2$, and there is a road both ways between $l_1$ and $l_2$. The goal is $p_1$ at $l_2$ and $p_2$ at $l_1$. The actions drive, load and unload give 12 ground actions, and a shortest plan has 6: load $p_1$, drive to $l_2$, unload $p_1$, load $p_2$, drive to $l_1$, unload $p_2$.

### No plan

Two blocks on the table and the goal $\mathit{on}(A, B)$ and $\mathit{on}(B, A)$. The task has 3 reachable states, and none of them contains the goal, so the correct answer is "no plan". A planner proves this by exhausting the reachable states. Most real planners also use invariants, such as "a block is on at most one thing", to detect such goals faster.

### Goals that already hold

If $G \subseteq I$, the empty sequence is a plan, of length 0. A planner must test the goal before it expands the initial state.

## Known algorithms

The main families are listed here; their own pages give the details.

- [State-space planning](/state-space-planning/): [forward search](/forward-state-space-search/) from $I$, or [backward search](/backward-state-space-search/) from $G$ by [goal regression](/goal-regression/). With [breadth-first search](/breadth-first-search/) and unit costs the first plan found is shortest, because breadth-first search visits states in order of their distance from $I$.
- Heuristic search with domain-independent heuristics, such as the [delete relaxation](/delete-relaxation/) heuristics [h-max](/h-max-heuristic/) and [h-add](/h-add-heuristic/) in [HSP](/hsp-planner/), the [relaxed plan heuristic](/relaxed-plan-heuristic/) in [FF](/fast-forward-planner/), [landmarks](/landmark-heuristic/) and the [causal graph heuristic](/causal-graph-heuristic/).
- [Graphplan](/graphplan/): a [planning graph](/planning-graph/) with [mutex relations](/mutex-relation/), then a backward search for a parallel plan.
- [SATPLAN](/satplan/): encode a bounded plan as a [SAT](/sat/) formula and increase the bound.
- Plan-space planning: search over [partial-order plans](/partial-order-plan/) with [causal links](/causal-link/), as in [POP](/pop-partial-order-planning/).
- [Means-ends analysis](/means-ends-analysis/), the method of the original STRIPS system.
- [Planning as model checking](/planning-as-model-checking/): symbolic search over sets of states.

## Bounds

Plan existence for STRIPS is PSPACE-complete (Bylander 1994); the proof is on [strips-plan-existence-pspace-complete](/strips-plan-existence-pspace-complete/). The bounded version, with $k$ given in unary, is NP-complete; see [bounded-plan-existence-np-complete](/bounded-plan-existence-np-complete/). Shortest plans can have length exponential in $|F|$: an $n$-bit counter with $2n$ facts and $n$ actions needs $2^n - 1$ actions, as shown on the [STRIPS](/strips/) page. For a fixed domain the complexity can be much lower: in the [blocks world](/blocks-world/) a plan always exists between two arrangements and is easy to find, while a shortest plan is NP-hard to find.

## Reductions

- To graph search: the task is [graph reachability](/graph-reachability/) in its state space, and optimal planning is [shortest path](/shortest-path/) there. The graph is exponential in the input, so the reduction is not polynomial.
- To SAT: a plan with at most $k$ steps exists if and only if a formula with $k + 1$ copies of the facts is satisfiable. This is a polynomial reduction for $k$ in unary.
- To model checking: a plan is a witness for the formula "eventually $G$" in the transition system of the task; see [explicit-state model checking](/explicit-state-model-checking/) and [bounded model checking](/bounded-model-checking/).
- From PSPACE: any polynomial space [Turing machine](/turing-machine/) can be simulated by a STRIPS task whose facts describe the tape, the head and the control state, which gives the hardness result.

## Applications

- Robotics: the original STRIPS system planned the actions of the Shakey robot at SRI.
- Benchmarks: the [International Planning Competition](/international-planning-competition/) uses classical domains such as blocks world, logistics, gripper and many others to compare planners.
- As a subroutine: probabilistic and partially observable planners often solve a classical relaxation of their task, for example by making every action deterministic, and replan when the world differs from the plan; see [replanning](/replanning/).
- Other problems with a compact state space, such as puzzles, test generation and verification, can be stated as classical planning tasks and given to a general planner.

## References
