---
tag: C5Y5FZ
kind: model
slug: hybrid-automata
name: Hybrid automata
aliases:
- Hybrid automaton
- Hybrid system
area: logic-and-constraints/model-checking
level: research
summary: Automata whose real variables follow differential conditions in each mode and jump on mode switches. Reachability is undecidable even for linear flows and decidable for initialized rectangular ones.
prereqs: [timed-automata, labelled-transition-system, reachability-problem]
see_also: [region-graph, difference-bound-matrix, undecidability, halting-problem, polyhedron, bounded-model-checking, symbolic-reachability, ode-initial-value-problem]
sources:
  - paper: "Rajeev Alur, Costas Courcoubetis, Nicolas Halbwachs, Thomas A. Henzinger, Pei-Hsin Ho, Xavier Nicollin, Alfredo Olivero, Joseph Sifakis and Sergio Yovine, The algorithmic analysis of hybrid systems, Theoretical Computer Science 138(1), 1995, pages 3 to 34"
    title: The algorithmic analysis of hybrid systems
    locator: the definition of hybrid automata and linear hybrid automata, the symbolic reachability procedure with polyhedra, and the undecidability of reachability for linear hybrid automata
  - paper: "Thomas A. Henzinger, The theory of hybrid automata, 11th IEEE Symposium on Logic in Computer Science (LICS 1996), pages 278 to 292"
    title: The theory of hybrid automata
    locator: the survey of the subclasses, their semantics, and the borders between decidable and undecidable verification problems
  - paper: "Thomas A. Henzinger, Peter W. Kopke, Anuj Puri and Pravin Varaiya, What's decidable about hybrid automata?, Journal of Computer and System Sciences 57(1), 1998, pages 94 to 124"
    title: What's decidable about hybrid automata?
    locator: the decidability and PSPACE-completeness of reachability for initialized rectangular automata by reduction to timed automata, and the undecidability results that follow when the restrictions are relaxed
  - paper: "Thomas A. Henzinger, Pei-Hsin Ho and Howard Wong-Toi, HyTech: a model checker for hybrid systems, International Journal on Software Tools for Technology Transfer 1(1-2), 1997, pages 110 to 122"
    title: "HyTech: a model checker for hybrid systems"
    locator: the semi-algorithm for linear hybrid automata with polyhedral state sets
  - paper: doi:10.1016/0304-3975(94)90010-8
    title: Rajeev Alur and David L. Dill, A theory of timed automata, Theoretical Computer Science 126(2), 1994, pages 183 to 235
    locator: timed automata and regions, the decidable base case that initialized rectangular automata reduce to
---

A *hybrid automaton* models a system with both discrete and continuous behaviour, such as a digital controller that drives a physical plant. It has finitely many *modes*, called locations, and a vector of real variables. In each mode the variables change continuously, following a *flow* condition such as a differential equation, while an *invariant* holds. A *jump* switches the mode when its *guard* holds, and it can change the variables in a step. Alur, Courcoubetis, Henzinger, Ho and others defined the model in the early 1990s. A [timed automaton](/timed-automata/) is the special case where every variable is a clock with derivative 1. That small case is decidable through the [region graph](/region-graph/). Almost every extension is not: location reachability is undecidable already for *linear* hybrid automata, where the derivatives are constants or lie in polyhedra. The main decidable class with more than clocks is the *initialized rectangular automata* of Henzinger, Kopke, Puri and Varaiya (1998), which reduce to timed automata. Tools therefore use semi-algorithms with polyhedra or over-approximations, or they bound time and the number of jumps.

## The machine

**Syntax.** A hybrid automaton $H$ with $n$ real variables $X = (x_1, \ldots, x_n)$ consists of:

- a finite set $L$ of *locations* (modes), with initial conditions $\mathrm{Init}(\ell) \subseteq \mathbb{R}^n$;
- for each location, a *flow* condition $\mathrm{Flow}(\ell)$ on $X$ and its derivative $\dot X$, such as $\dot X = f_\ell(X)$ or $\dot X \in P_\ell$ for a set $P_\ell$;
- for each location, an *invariant* $\mathrm{Inv}(\ell) \subseteq \mathbb{R}^n$;
- a finite set of *jumps* $(\ell, a, \mathrm{Jump}, \ell')$, where $\mathrm{Jump} \subseteq \mathbb{R}^n \times \mathbb{R}^n$ relates the values before and after. It combines a guard and an update.

**Semantics.** States are pairs $(\ell, v)$ with $v \in \mathrm{Inv}(\ell)$. A *flow step* $(\ell, v) \xrightarrow{t} (\ell, v')$ exists when some differentiable function $\phi : [0, t] \to \mathbb{R}^n$ has $\phi(0) = v$, $\phi(t) = v'$, satisfies $\mathrm{Flow}(\ell)$ at every point, and stays in $\mathrm{Inv}(\ell)$ throughout. A *jump step* $(\ell, v) \xrightarrow{a} (\ell', v')$ exists when $(v, v') \in \mathrm{Jump}$ and $v' \in \mathrm{Inv}(\ell')$. A run alternates the two. The *reachable set* is the set of states on runs from initial states.

**Subclasses.** The classes differ in what the flows, invariants and jumps may say.

| Class | Flows | Guards, invariants, updates |
|---|---|---|
| Timed automata | $\dot x = 1$ for every variable | Compare with integer constants; reset to 0 |
| Stopwatch automata | $\dot x \in \{0, 1\}$, chosen per location | As for timed automata |
| Multirate automata | $\dot x = k_{\ell, x}$, a constant per location | As for timed automata |
| Rectangular automata | $\dot x \in [a_{\ell, x}, b_{\ell, x}]$, separately for each variable | Rectangles, that is, products of intervals; reset to an interval |
| Linear hybrid automata | $\dot X$ in a convex polyhedron | Linear constraints over $X$; linear updates |
| Affine and nonlinear | $\dot X = A X + b$, or $\dot X = f(X)$ | General |

A rectangular automaton is *initialized* when every jump that changes the flow interval of a variable also resets that variable.

**Example.** A thermostat has one variable, the temperature $x$, and two locations:

- In $\mathit{on}$, the flow is $\dot x \in [1, 2]$ and the invariant is $x \le 22$. The jump to $\mathit{off}$ has the guard $x \ge 21$.
- In $\mathit{off}$, the flow is $\dot x \in [-2, -1]$ and the invariant is $x \ge 18$. The jump to $\mathit{on}$ has the guard $x \le 19$.

The automaton starts in $\mathit{on}$ with $x = 20$. A symbolic search keeps one interval per location:

1. Flow in $\mathit{on}$ from $x = 20$ gives $[20, 22]$.
2. The jump with $x \ge 21$ gives $\mathit{off}$ with $[21, 22]$, and flow there gives $[18, 22]$.
3. The jump with $x \le 19$ gives $\mathit{on}$ with $[18, 19]$, and flow gives $[18, 22]$.
4. The next jump adds nothing new, and the search stops.

The reachable temperatures are $[18, 22]$ in both locations. This automaton is rectangular but not initialized: the jumps change the flow interval of $x$ without a reset. The search still ends here because there is one variable. In general such a search need not end.

## What it counts

The model asks questions about the reachable set and the runs:

- **Location or state reachability:** can a bad location, or a bad region of $\mathbb{R}^n$, be reached? Most [safety properties](/safety-property/) reduce to this.
- **Bounded reachability:** the same question for at most $k$ jumps, or for time at most $T$.
- **Temporal logic model checking**, and controller synthesis, which is a game version.

The input size is the size of the description: the number of locations, jumps and variables, and the rational constants. For nonlinear flows, the question also depends on how the dynamics are given and on what precision is accepted, as in $\delta$-decision procedures that may answer with a robustness margin.

## Relation to other models

- **Timed automata.** A [timed automaton](/timed-automata/) is a hybrid automaton with clock flows and integer comparisons. Its region equivalence is a finite time-abstract [bisimulation](/bisimulation/). For general hybrid automata no finite bisimulation exists, and this is the root of undecidability.
- **Initialized rectangular automata.** These reduce to timed automata. Henzinger, Kopke, Puri and Varaiya first reduce a rectangular variable with rates in $[a, b]$ to two variables that track its lower and upper bound. Initialization means that each bound restarts when its rate changes. A rescaling then turns variables with constant rates into clocks. The size grows by a polynomial factor in the number of variables, so reachability stays in PSPACE.
- **Two-counter machines.** A stopwatch can hold a value while time passes, and a variable with rate 2 can double a difference. These operations are enough to store the two counters of a Minsky machine in real variables and to increment, decrement and test them. Since the [halting problem](/halting-problem/) for these machines is undecidable, so is reachability.
- **Linear arithmetic.** For linear hybrid automata, one flow or jump step maps a polyhedron to a polyhedron. The flow step uses a projection, which is the time-elapse operator of HyTech. So the states reachable in $k$ jumps form a finite union of polyhedra, computed with [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) or similar methods. This is a semi-algorithm for the full reachable set. Bounded reachability can also be encoded as a formula of linear real arithmetic for an [SMT solver](/smt-problem/), as in [bounded model checking](/bounded-model-checking/).
- **Control and numerical analysis.** For affine flows $\dot X = A X + b$, reachable sets are over-approximated with zonotopes or [support functions](/support-function/). For nonlinear flows, tools use Taylor models or validated [ODE](/ode-initial-value-problem/) solvers with [interval arithmetic](/interval-arithmetic/).
- **Polyhedral abstract domains.** The polyhedra used for linear hybrid automata are the same as the polyhedral domain of [abstract interpretation](/abstract-interpretation/). Widening can force termination at the cost of precision.

## Known results in the model

| Problem | Status | Source |
|---|---|---|
| Reachability, timed automata | PSPACE-complete | Alur and Dill 1994 |
| Reachability, initialized rectangular automata | PSPACE-complete | Henzinger, Kopke, Puri and Varaiya 1998 |
| Reachability, rectangular automata without initialization | Undecidable | Henzinger, Kopke, Puri and Varaiya 1998 |
| Reachability, stopwatch automata | Undecidable | Alur et al. 1995; Henzinger 1996 |
| Reachability, linear hybrid automata | Undecidable; semi-decided by symbolic search with polyhedra | Alur et al. 1995 |
| Reachability in at most $k$ jumps, linear hybrid automata | Decidable, by linear real arithmetic | Follows from the polyhedral step of Alur et al. 1995 |
| Reachability, nonlinear flows | Undecidable in general; $\delta$-decidable in bounded time for some function classes | Henzinger 1996; Gao, Kong and Clarke 2013 |

**Why the border is sharp.** Initialized rectangular automata are at the limit of decidability. Henzinger, Kopke, Puri and Varaiya show that small relaxations already give undecidability, for example dropping initialization. Stopwatch automata differ from timed automata only by letting clocks stop, and linear hybrid automata contain stopwatch automata. So reachability is undecidable even for linear hybrid automata. Any analysis of a general model is therefore a semi-algorithm or an approximation. It can prove safety when it finds an inductive invariant, and it can find counterexamples by bounded search, but it cannot always decide.

**Practice.** HyTech (Henzinger, Ho and Wong-Toi) computed reachable sets of linear hybrid automata with exact polyhedra. Later tools, such as PHAVer, SpaceEx and Flow*, use approximation by polyhedra, support functions and Taylor models, and dReach uses $\delta$-complete SMT solving. Abstraction refinement in the style of [CEGAR](/cegar/) and invariant synthesis in the style of [IC3](/ic3-pdr/) have been adapted to hybrid systems.

## References
