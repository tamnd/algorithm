---
tag: 9DV4RS
kind: problem
slug: conformant-planning
name: Conformant planning
aliases:
- planning without observation
area: games-and-search/planning
level: advanced
summary: Find one sequence of actions that reaches the goal from every possible initial state and for every outcome of the actions, with no sensing. It is a path search in the space of set beliefs.
prereqs: [belief-space, classical-planning]
see_also: [contingent-planning, pomdp-planning, planning-as-model-checking, forward-state-space-search, breadth-first-search, binary-decision-diagram, expspace, strips]
sources:
  - paper: "Blai Bonet and Hector Geffner, Planning with incomplete information as heuristic search in belief space, Proceedings of AIPS 2000"
    locator: pp. 52 to 61 (conformant planning as a shortest path problem over set beliefs, solved by heuristic search)
  - paper: doi:10.1613/jair.774
    title: Alessandro Cimatti and Marco Roveri, Conformant planning via symbolic model checking, Journal of Artificial Intelligence Research 13, 2000
    locator: pp. 305 to 338 (breadth-first search over beliefs represented by binary decision diagrams)
  - paper: doi:10.1613/jair.2708
    title: Hector Palacios and Hector Geffner, Compiling uncertainty away in conformant planning problems with bounded width, Journal of Artificial Intelligence Research 35, 2009
    locator: pp. 623 to 675 (translations into classical planning and the conformant width)
  - paper: doi:10.1007/10720246_24
    title: Patrik Haslum and Peter Jonsson, Some results on the complexity of planning with incomplete information, Recent Advances in AI Planning (ECP 1999), Lecture Notes in Computer Science 1809, 2000
    locator: pp. 308 to 318 (the complexity of conformant plan existence)
  - paper: doi:10.1016/S0004-3702(00)00043-6
    title: Chitta Baral, Vladik Kreinovich and Raul Trejo, Computational complexity of planning and approximate planning in the presence of incompleteness, Artificial Intelligence 122(1-2), 2000
    locator: pp. 241 to 267 (plans of polynomial length)
  - paper: "Jussi Rintanen, Complexity of planning with partial observability, Proceedings of ICAPS 2004"
    locator: pp. 345 to 354 (EXPSPACE-completeness of planning without observations)
  - book: isbn:9781608459698
    title: Hector Geffner and Blai Bonet, A Concise Introduction to Models and Methods for Automated Planning, Morgan and Claypool, 2013
    locator: Section 4.2 (planning with incomplete information and no sensing)
---

Conformant planning asks for a plan that works with no feedback. The initial state is only known to be in a set, the actions can have several outcomes, and the agent observes nothing while it acts. A conformant plan is one sequence of actions that is applicable at every step and ends in a goal state, whatever the initial state and the outcomes are. The agent always knows its [belief](/belief-space/), the set of the states that are still possible, and an action maps a belief to one new belief. So conformant planning is a path problem in the graph of set beliefs, and [breadth-first search](/breadth-first-search/) in that graph solves it. The graph has up to $2^{|S|}$ nodes, and for compact models the problem is EXPSPACE-complete.

## In plain words

You must give a robot a list of moves before it starts. The robot is blind, you do not know exactly where it starts, and some moves can go a little wrong. The list must bring the robot to the goal in every case.

The trick is to plan with the set of places the robot can be in. At the start the set is large. A good move makes the set smaller, for example a move into a wall, which puts the robot in the same place from many starts. The plan is done when every place in the set is a goal. Planning is then a search over sets of places, not over places, and there are many more sets than places.

## Definition

A conformant planning problem is a tuple $(S, I, G, A, F)$:

- $S$ is a finite set of states, $I \subseteq S$ is the set of the possible initial states, and $G \subseteq S$ is the set of the goal states.
- $A$ is a finite set of actions. $F(s, a) \subseteq S$ is the set of the possible next states of $a$ in $s$. The action $a$ is applicable in $s$ when $F(s, a) \ne \emptyset$.

There are no observations. For a belief $b \subseteq S$, the action $a$ is applicable in $b$ when it is applicable in every state of $b$, and then $b_a = \bigcup_{s \in b} F(s, a)$.

A sequence $\pi = a_1, \ldots, a_n$ is a **conformant plan** when the beliefs $b_0 = I$ and $b_k = (b_{k-1})_{a_k}$ are defined, so that each $a_k$ is applicable in $b_{k-1}$, and $b_n \subseteq G$. An equivalent definition follows the states: for every $s_0 \in I$ and every run $s_0, s_1, \ldots, s_n$ with $s_k \in F(s_{k-1}, a_k)$, each action is applicable and $s_n \in G$.

The **decision problem** asks whether a conformant plan exists. The **optimization problem** asks for a shortest one, or one of least total cost.

In the compact form, $S$ is the set of assignments to $m$ Boolean variables, $I$ and $G$ are formulas, and the actions are given by preconditions and conditional effects, as in [STRIPS](/strips/) or [PDDL](/pddl/) with uncertainty. Then $|S| = 2^m$ and there are up to $2^{2^m}$ beliefs.

## Variants

- **Deterministic conformant planning.** Each $F(s, a)$ has at most one state, and only the initial state is unknown. Many benchmarks are of this kind.
- **Bounded length.** Is there a conformant plan of at most $k$ steps, with $k$ given in unary?
- **Probabilistic conformant planning.** The initial state and the outcomes have probabilities, and the plan must reach the goal with probability at least $\theta$. This is a [POMDP](/pomdp-planning/) with no observations and a goal threshold.
- **Planning with sensing.** If the agent can observe, the plan may branch on what it sees. This is [contingent planning](/contingent-planning/).

## Examples

**The bomb in the toilet, with clogging.** There are $n$ packages, and exactly one of them holds an armed bomb. The action dunk($i$) puts package $i$ in the toilet: it disarms the bomb if the bomb is in package $i$, and it clogs the toilet. A clogged toilet does not accept a package. The action flush unclogs it. The goal is that the bomb is disarmed. The initial belief has $n$ states, one for each place of the bomb. The agent cannot see which package holds the bomb, so it must dunk all of them, and it must flush between two dunks. A shortest conformant plan is

$$\text{dunk}(1), \text{flush}, \text{dunk}(2), \text{flush}, \ldots, \text{dunk}(n),$$

with $2n - 1$ actions. Breadth-first search over beliefs, as in the implementation, finds it after expanding $2^{n+1} - 3$ beliefs, for $n = 1, \ldots, 6$. A belief is fixed by the set of the packages that are not yet dunked and by the state of the toilet, so the number of beliefs grows exponentially in $n$, while the number of states is only $4n$.

**A blind robot in a corridor.** The cells are $1, 2, 3, 4$, and the robot can be anywhere. The action left moves one cell to the left, and stays at 1. The plan left, left, left reaches cell 1 from every start, and the beliefs are $\{1, 2, 3\}$, $\{1, 2\}$ and $\{1\}$. The wall at cell 1 removes the uncertainty.

**Nondeterministic moves.** In the same corridor, let right move one or two cells, and stay at 4. From $I = \{1, 2\}$, the plan right, right, right reaches cell 4 for every outcome, with the beliefs $\{2, 3, 4\}$, $\{3, 4\}$ and $\{4\}$. No shorter plan exists.

**No conformant plan.** A treasure is behind door 1 or door 2, and opening the wrong door ends the game. No sequence of actions works in both cases. If a sensor can tell which door it is, a [contingent plan](/contingent-planning/) exists: look, then open the door that the sensor shows.

## Known algorithms

- **Breadth-first search in belief space.** Search the graph of set beliefs from $I$ and stop at the first belief inside $G$. This finds a shortest plan. The implementation does this with explicit sets.
- **Heuristic search in belief space.** Bonet and Geffner (2000) solve conformant problems as shortest path problems over beliefs with A* and heuristics from the relaxed problem with full observation.
- **Symbolic search.** Cimatti and Roveri (2000) represent beliefs and the transition relation with [binary decision diagrams](/binary-decision-diagram/) and search backward or forward over sets of beliefs. This is part of [planning as model checking](/planning-as-model-checking/).
- **Compilation to classical planning.** Palacios and Geffner (2009) translate a conformant problem into a classical problem whose fluents are literals such as "it is known that $x$ is true" and "$x$ is true if the initial state is $s$". Their translations are polynomial for a fixed bound on the conformant width, and complete for problems whose width is at most that bound. A classical planner then solves the result.
- **Planners with implicit beliefs.** Conformant-FF keeps the belief implicit as the start belief and the action sequence, and tests facts by satisfiability calls. Conformant Graphplan builds one planning graph for each initial state.
- **Bounded length by satisfiability.** For a fixed length $k$, the existence of a plan is a formula with a quantifier pattern "there is a plan such that for all initial states and outcomes", which a QBF or a two-level SAT method can decide.

## Bounds

- **Explicit states.** There are at most $2^{|S|} - 1$ nonempty beliefs. A shortest plan visits each belief at most once, so it has at most $2^{|S|} - 2$ actions. Breadth-first search takes $O(2^{|S|} \, |A| \, |S| \, d)$ time, where $d$ bounds $|F(s, a)|$.
- **Compact models.** The plan existence problem is EXPSPACE-complete (Haslum and Jonsson 1999; Rintanen 2004). Classical planning is [PSPACE-complete](/strips-plan-existence-pspace-complete/), so the lack of observations adds an exponential, unless PSPACE equals EXPSPACE.
- **Polynomial length.** If the length of the plan is bounded by a polynomial, the problem is $\Sigma_2^P$-complete (Baral, Kreinovich and Trejo 2000). The two quantifiers are "there is a plan" and "for every initial state and outcome it works". Classical planning with a polynomial bound is [NP-complete](/bounded-plan-existence-np-complete/).
- **One initial state and deterministic actions.** Then a belief is a single state, and the problem is classical planning.

## Reductions

- **From classical planning.** A classical problem is a conformant problem with $|I| = 1$ and deterministic actions.
- **To a shortest path problem.** The beliefs reachable from $I$ form a directed graph, and a shortest conformant plan is a shortest path from $I$ to a belief inside $G$.
- **To contingent planning.** A conformant problem is a [contingent](/contingent-planning/) problem with one observation that tells nothing.
- **To POMDP planning.** A conformant problem is a goal [POMDP](/pomdp-planning/) with no observations, in which the goal must hold with probability 1. Any probabilities with full support on $I$ and on each $F(s, a)$ give the same answer.
- **To classical planning.** The translations of Palacios and Geffner map conformant problems of bounded width to classical problems of polynomial size, so classical heuristics and planners apply.

## Applications

- Robots and machines with no sensors, or with sensors that are too slow or too costly, such as parts orienters that turn a part to one pose by a fixed series of pushes or tilts.
- Test sequences for circuits and protocols: a sequence of inputs that brings a finite automaton from any start to one given state is a conformant plan with $I = S$ and deterministic actions.
- Plans that must be fixed in advance, such as a recipe, a medical protocol or a startup sequence for a plant.
- Safe plans under uncertainty, where a plan that works only in the likely cases is not acceptable.

## References
