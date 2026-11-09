---
tag: S90VY0
kind: algorithm
slug: ic3-pdr
name: IC3 / property-directed reachability
aliases:
- IC3
- PDR
- Property-directed reachability
area: logic-and-constraints/model-checking
level: research
summary: Prove an invariant with a sequence of clause frames, each a bound on the states reachable in i steps, refined by one-step SAT queries until two frames are equal.
solves: [invariant-checking]
model: word-ram
complexity:
  vars: {n: the number of latches, g: the number of gates of the circuit, k: the number of frames}
  time: {queries: 2^O(n), per_query: 2^O(n + g)}
  space: {frames: 2^O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 2011
  people: [Aaron R. Bradley, Niklas Eén, Alan Mishchenko, Robert Brayton]
  note: Bradley presented IC3 at VMCAI 2011. Eén, Mishchenko and Brayton gave an efficient reimplementation at FMCAD 2011 and named it property-directed reachability.
prereqs: [inductive-invariant, invariant-checking, sat, incremental-sat]
see_also: [k-induction, interpolation-based-model-checking, sat-based-bounded-model-checking, bounded-model-checking, symbolic-reachability, counterexample-generation, unsat-core, safety-property]
sources:
  - paper: doi:10.1007/978-3-642-18275-4_7
    title: Aaron R. Bradley, SAT-based model checking without unrolling, VMCAI 2011, LNCS 6538
    locator: pages 70 to 87 (the frame invariants, the blocking of counterexamples to induction, the inductive generalization of clauses, the propagation phase, and the report on HWMCC 2010)
  - paper: "Niklas Eén, Alan Mishchenko and Robert Brayton, Efficient implementation of property directed reachability, FMCAD 2011, pages 125 to 134"
    title: Efficient implementation of property directed reachability
    locator: the name PDR, the priority queue of proof obligations, ternary simulation to enlarge cubes, and the implementation in ABC
---

IC3, also called property-directed reachability (PDR), proves that a property $P$ holds in every reachable state of a finite transition system, or finds a counterexample. Unlike [bounded model checking](/sat-based-bounded-model-checking/), [k-induction](/k-induction/) and [interpolation](/interpolation-based-model-checking/), it never unrolls the transition relation: every SAT query has one copy of $T$. It keeps a sequence of *frames* $F_0, F_1, \ldots, F_k$, sets of clauses where $F_i$ over-approximates the states reachable in at most $i$ steps. When a state in the last frame violates $P$, IC3 tries to show that the state cannot be reached in $k$ steps. It looks for predecessors one step at a time. Each time a predecessor does not exist, it learns a clause that excludes the state and its neighbours, and adds it to the frames. When two consecutive frames become equal, that frame is an [inductive invariant](/inductive-invariant/) that implies $P$. Aaron Bradley introduced the method in 2011, and Eén, Mishchenko and Brayton gave the name PDR to their implementation of it in the same year.

## In plain words

We want to show that a machine never reaches a bad state. IC3 keeps a list of guesses. Guess number $i$ is a set of states that contains every state the machine can reach in $i$ steps or fewer. Each guess is a list of facts, such as "latch 3 is off".

When the last guess still allows a bad state, IC3 asks the SAT solver: can this bad state come from the guess before it? If not, IC3 adds a fact that rules the state out. If yes, it tries to rule out that earlier state first, and so on back to the start. If the chain reaches the initial state, the bug is real.

IC3 also copies facts forward when they stay true after one step. When two guesses in a row are equal, nothing new can be reached, and the property is proved.

## The problem

A finite system has state variables $s = (x_1, \ldots, x_n)$, a set of initial states $I(s)$, and a transition relation $T(s, s')$, for example from a circuit with $g$ gates and $n$ latches. A property $P(s)$ is an invariant if it holds in every reachable state. This is the [invariant checking](/invariant-checking/) problem. A *cube* is a conjunction of literals, and a single state is a cube with $n$ literals. A cube $c$ is *inductive relative to* a formula $F$ if $F \wedge \neg c \wedge T \Rightarrow \neg c'$, that is, no state of $F$ outside $c$ has a successor in $c$.

IC3 keeps the frames $F_0, \ldots, F_k$, where $F_0 = I$ and each $F_i$ for $i \ge 1$ is a set of clauses. It maintains four invariants.

1. $I \Rightarrow F_i$ for all $i$.
2. $F_i \Rightarrow F_{i+1}$; in the clause view, every clause of $F_{i+1}$ is also in $F_i$.
3. $F_i \wedge T \Rightarrow F'_{i+1}$ for $0 \le i < k$.
4. $F_i \Rightarrow P$ for $0 \le i < k$.

Together they say that $F_i$ contains every state reachable in $i$ steps or fewer, and that no counterexample of length less than $k$ exists.

## The algorithm

```pseudo id=main
IC3(I, T, P)
L1  if SAT(I ∧ ¬P) then return FAILS
L2  F_0 ← I; F_1 ← ∅ (no clauses, so every state); k ← 1
L3  loop
L4      while SAT(F_k ∧ ¬P) gives a state s do
L5          if BLOCK(s, k) returns a path then return FAILS with that path
L6      F_k+1 ← ∅; k ← k + 1
L7      for i ← 1 to k − 1 do                                 ▷ propagation
L8          for each clause c in F_i but not in F_i+1 do
L9              if not SAT(F_i ∧ T ∧ ¬c') then add c to F_i+1
L10         if F_i = F_i+1 then return HOLDS, with the invariant F_i

BLOCK(s, k)
L11 Q ← a stack that holds the proof obligation (s, k)
L12 while Q is not empty do
L13     (t, i) ← the top of Q                                  ▷ t is a cube, i a frame index
L14     if not SAT(F_i−1 ∧ ¬t ∧ T ∧ t') then                   ▷ t is inductive relative to F_i−1
L15         g ← GENERALIZE(t, i)                               ▷ a subcube of t, disjoint from I, still relatively inductive
L16         add the clause ¬g to F_1, ..., F_i; pop (t, i)
L17     else u ← the predecessor state in the model
L18         if i − 1 = 0 or u ∈ I then return the path from u through the states of Q to s
L19         push (u, i − 1) on Q
L20 return NONE
```

GENERALIZE drops one literal of the cube at a time. It keeps the shorter cube when it still has no initial state and still passes the query of line L14. A shorter cube gives a shorter clause, which excludes more states. Real implementations use the UNSAT core of the query of line L14 first, and then a smarter search for a minimal subcube.

## Example

The system has two latches $x_0$ and $x_1$, an input $e$, the initial state $(x_0, x_1) = (0, 0)$, and the next-state functions $x'_0 = x_0$ and $x'_1 = x_1 \vee (x_0 \wedge e)$. The property is $P = \neg(x_0 \wedge x_1)$. Only $(0, 0)$ is reachable, so $P$ holds. $P$ is not inductive, because $(1, 0)$ goes to $(1, 1)$. Plain $k$-induction without the simple-path constraint never proves this property. IC3 proves it with 13 SAT queries.

- $k = 1$. The query of L4 gives $s = (1, 1)$. The query of L14 at $i = 1$ asks for a predecessor of $(1, 1)$ in $F_0 = I$. There is none. GENERALIZE drops $x_0$: the cube $x_1$ has no initial state, and $I$ has no successor with $x_1 = 1$. So the clause $\neg x_1$ goes into $F_1$. Now $F_1 \wedge \neg P$ is unsatisfiable. The frame $F_2$ is added, and the push of $\neg x_1$ to $F_2$ fails, because $(1, 0)$ goes to $(1, 1)$.
- $k = 2$. $F_2$ has no clauses, so L4 gives $s = (1, 1)$ again. Its predecessor in $F_1$ is $u = (1, 0)$ with $e = 1$. The obligation $((1, 0), 1)$ is pushed. $(1, 0)$ has no predecessor in $I$. GENERALIZE cannot drop $x_0$, since the cube $\neg x_1$ contains the initial state, but it drops $\neg x_1$. So $\neg x_0$ goes into $F_1$. Back at $((1, 1), 2)$: now $F_1 = \neg x_0 \wedge \neg x_1$, which holds only in $(0, 0)$, so there is no predecessor. The clause $\neg x_1$ goes into $F_1$ and $F_2$.
- $k = 3$. Propagation pushes $\neg x_0$ from $F_1$ to $F_2$, since $x_0$ never changes. Now $F_1 = F_2 = \{\neg x_0, \neg x_1\}$, and IC3 returns HOLDS with the invariant $\neg x_0 \wedge \neg x_1$.

The clause $\neg x_0$ is the strengthening that $P$ needs. IC3 found it from the counterexample to induction $(1, 0)$, without any unrolling.

## Correctness

The four frame invariants hold after each step. Line L16 adds a clause $\neg g$ where $g$ has no initial state and $F_{i-1} \wedge \neg g \wedge T \Rightarrow \neg g'$; since $\neg g$ is added to every frame $F_1, \ldots, F_i$, invariant 3 still holds. Line L9 adds a clause only when invariant 3 allows it. A new frame is added only when $F_k \wedge \neg P$ is unsatisfiable, which gives invariant 4 for the old $F_k$.

**HOLDS is sound.** If $F_i = F_{i+1}$, then $I \Rightarrow F_i$, $F_i \wedge T \Rightarrow F'_i$, and $F_i \Rightarrow P$. So $F_i$ is an inductive invariant that implies $P$.

**FAILS is sound.** Each obligation on the stack is a predecessor of the one below it, and the bottom one violates $P$. So the returned path is a real counterexample.

**Termination.** By induction on $i$, each obligation $(t, i)$ is popped with $t$ excluded from $F_i$, or a counterexample is found. Each predecessor found removes a state from $F_{i-1}$, so BLOCK terminates. After propagation, if no two frames are equal, then a clause of $F_i$ failed to move to $F_{i+1}$, so $F_{i+1}$ has a state that $F_i$ lacks. The frames $F_1 \subsetneq \cdots \subsetneq F_k$ then grow strictly as state sets, so $k \le 2^n$. The full proof is below.

## Complexity

All bounds here are worst-case bounds. Each obligation $(u, j)$ ends with $u$ removed from $F_j$, and frames only shrink. So each pair of a state and a frame index occurs at most once as an obligation, and there are at most $(2^n + 1) \cdot 2^n$ of them. Each obligation makes one query per predecessor found, one unsatisfiable query, and at most $n$ queries in GENERALIZE. Propagation makes at most one query per clause and frame. So the number of SAT queries is $2^{O(n)}$. Each query has one copy of $T$, so it has $O(n + g)$ variables, and a SAT call takes time $2^{O(n + g)}$ in the worst case. The frames can hold $2^{O(n)}$ clauses.

These bounds are far from what one sees in practice. The queries are small, and the solver runs incrementally. Bradley (2011) reports that his implementation placed third in the Hardware Model Checking Competition 2010. That is a measured result on one benchmark set, not a bound.

## Properties

- **No unrolling.** Each query contains $T$ once. Bounded model checking, $k$-induction and interpolation all use formulas with $k$ copies of $T$.
- **Many small queries.** IC3 makes many short incremental SAT calls instead of a few large ones.
- **Sound both ways.** HOLDS comes with an inductive invariant in CNF, which an independent checker can verify with three SAT calls. FAILS comes with a real counterexample, though not always a shortest one.
- **Complete for finite systems.** It terminates with the right answer, with at most about $2^n$ frames.
- **Property directed.** The learned clauses come only from states that lead to a violation of $P$.

## Variants and improvements

- **PDR** (Eén, Mishchenko and Brayton 2011) keeps the obligations in a priority queue by frame index, and enlarges cubes by ternary simulation before blocking them.
- **Better generalization.** Hassan, Bradley and Somenzi (FMCAD 2013) improve the search for small relatively inductive cubes, a step that strongly affects performance.
- **Software and infinite-state systems.** Later work lifts IC3 to SMT theories and to programs with control-flow graphs, for example in the tools Spacer and nuXmv. There the method is sound but in general not complete.
- **Liveness.** IC3 handles liveness through the [liveness-to-safety](/liveness-to-safety/) reduction, or with special variants for fair cycles.

## When to use it

IC3 is a default engine for proving safety properties of hardware. Use it when the property needs a strengthening that is not known in advance, and when the circuit is too large for BDD-based [symbolic reachability](/symbolic-reachability/). It also gives short counterexamples in many cases, but [BMC](/bounded-model-checking/) is usually faster at finding deep bugs. Hardware model checkers often run BMC, $k$-induction, interpolation and IC3 in parallel and take the first answer.

## Pitfalls

- **Generalizing into the initial states.** A generalized cube must still exclude $I$. Otherwise the learned clause cuts off initial states, and invariant 1 fails.
- **Adding a clause only to $F_i$.** The clause of line L16 must go into all of $F_1, \ldots, F_i$, or invariant 2 breaks, and the relative-induction argument for invariant 3 no longer applies.
- **Testing equality before propagation.** The test $F_i = F_{i+1}$ compares clause sets, not state sets. It can see a fixed point late, but the termination argument needs propagation to run first: only a failed push shows that $F_{i+1}$ has a state that $F_i$ lacks.
- **Forgetting the first check.** If $I \wedge \neg P$ is satisfiable, the main loop must not start.

## Implementations

## History

Bradley and Manna (FMCAD 2007) introduced inductive generalization of counterexamples to induction. Bradley then built IC3 on this idea. He presented it as "SAT-based model checking without unrolling" at VMCAI 2011, with a tool that had taken part in the Hardware Model Checking Competition 2010. Eén, Mishchenko and Brayton (FMCAD 2011) gave an efficient reimplementation in ABC and the name property-directed reachability. Many later papers extend the method to software, to SMT theories and to liveness.

## References
