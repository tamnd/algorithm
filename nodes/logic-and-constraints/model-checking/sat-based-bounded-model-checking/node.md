---
tag: 3TYGHB
kind: algorithm
slug: sat-based-bounded-model-checking
name: SAT-based bounded model checking
aliases:
- BMC
- BMC encoding
- Unrolling to SAT
area: logic-and-constraints/model-checking
level: advanced
summary: Unroll the transition relation k times into one formula, add the negated property (with a loop condition for liveness), convert to CNF and ask a SAT solver; a model is a counterexample.
solves: [invariant-checking, ltl-model-checking]
model: word-ram
complexity:
  vars: {k: the bound, g: the number of gates of the circuit, n: the number of latches}
  time: {build: O(k^2 · g), solve: 2^O(k g)}
  space: {formula: O(k · g)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1999
  people: [Armin Biere, Alessandro Cimatti, Edmund M. Clarke, Yunshan Zhu]
  note: Biere, Cimatti, Clarke and Zhu translated bounded LTL model checking into propositional satisfiability, with the loop conditions for infinite paths, at TACAS 1999.
prereqs: [bounded-model-checking, sat, tseitin-transformation, cdcl, kripke-structure]
see_also: [completeness-threshold, k-induction, interpolation-based-model-checking, ic3-pdr, incremental-sat, counterexample-generation, linear-temporal-logic, symbolic-reachability]
sources:
  - paper: doi:10.1007/3-540-49059-0_14
    title: Armin Biere, Alessandro Cimatti, Edmund M. Clarke and Yunshan Zhu, Symbolic model checking without BDDs, TACAS 1999, LNCS 1579
    locator: pages 193 to 207 (the bounded semantics of LTL, the unrolling, the loop condition L_k and the translation of LTL into propositional formulas)
  - paper: doi:10.1016/S0065-2458(03)58003-2
    title: Armin Biere, Alessandro Cimatti, Edmund M. Clarke, Ofer Strichman and Yunshan Zhu, Bounded model checking, Advances in Computers 58, 2003
    locator: pages 117 to 148 (the translation, its correctness, the diameter bounds and the experiments)
  - paper: "Niklas Eén and Niklas Sörensson, Temporal induction by incremental SAT solving, Electronic Notes in Theoretical Computer Science 89(4), 2003"
    title: Temporal induction by incremental SAT solving
    locator: the incremental use of one SAT solver over growing unrollings, with assumptions
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: the chapter Bounded Model Checking, by Armin Biere (the encodings, the loop conditions and the completeness thresholds)
---

SAT-based bounded model checking (BMC) is the concrete algorithm behind the method of [bounded model checking](/bounded-model-checking/). For a bound $k$, it builds one propositional formula that is satisfiable exactly when the system has a counterexample of length $k$. The formula is the *unrolling* $I(s_0) \wedge T(s_0, s_1) \wedge \cdots \wedge T(s_{k-1}, s_k)$, with a fresh copy $s_i$ of the state variables for each time step, and a part that says the property fails on this path. For a safety property this part is $\neg P(s_k)$. For a liveness property it also needs a *loop condition* $T(s_k, s_l)$, which closes the path into a lasso. The [Tseitin transformation](/tseitin-transformation/) turns the formula into CNF of size linear in $k$ times the circuit, and a [CDCL](/cdcl/) solver decides it. A model is a real counterexample. An unsatisfiable formula only says that no counterexample of that length exists.

## In plain words

Take a circuit and make $k + 1$ copies of its state, one copy for each clock tick. Wire the copies together so that copy $i + 1$ is what the circuit computes from copy $i$. Fix copy 0 to the start state. Then ask: can the last copy be a bad state?

A SAT solver answers this question. If it says yes, its answer gives the value of each wire at each tick: this is a run of the circuit that ends in a bad state. If it says no, there is no bad run of exactly this length. Try $k = 0, 1, 2, \ldots$ in turn, and the first yes gives a shortest bad run.

## The problem

A system has $n$ state variables $s = (x_1, \ldots, x_n)$, inputs $w$, an initial condition $I(s)$, and a transition relation $T(s, s')$. For a circuit with $g$ gates, $T(s, s') = \exists w.\, \bigwedge_j (x'_j \leftrightarrow f_j(s, w))$. Given a property and a bound $k$, decide whether the system has a counterexample of length $k$:

- **Safety, $\mathbf{G}\, P$.** A path $s_0, \ldots, s_k$ with $I(s_0)$ and $\neg P(s_k)$. This is the [invariant checking](/invariant-checking/) problem, bounded to depth $k$.
- **Liveness, $\mathbf{F}\, q$.** An infinite path on which $q$ never holds. In a finite system it can be taken as a *lasso*: a path $s_0, \ldots, s_k$ with $T(s_k, s_l)$ for some $l \le k$, and $\neg q(s_i)$ for all $i$.

## The algorithm

For safety, write $\llbracket M \rrbracket_k = I(s_0) \wedge \bigwedge_{i=0}^{k-1} T(s_i, s_{i+1})$. For liveness, write ${}_l L_k = T(s_k, s_l)$ for "there is a step from $s_k$ back to $s_l$", and $L_k = \bigvee_{l=0}^{k} {}_l L_k$.

```pseudo id=main
BMC-SAFETY(I, T, P, kmax)
L1  for k ← 0 to kmax do
L2      φ ← ⟦M⟧_k                              ▷ fresh variables s_0 .. s_k and inputs w_0 .. w_k−1
L3      φ ← φ ∧ ¬P(s_k)
L4      if SAT(CNF(φ)) then
L5          return the path s_0 .. s_k read from the model
L6  return NONE                                ▷ no counterexample of length ≤ kmax

BMC-LASSO(I, T, q, kmax)                       ▷ counterexample to F q
L7  for k ← 0 to kmax do
L8      φ ← ⟦M⟧_k ∧ T(s_k, s_back)             ▷ s_back: one more fresh copy, the state after s_k
L9      φ ← φ ∧ ¬q(s_0) ∧ ... ∧ ¬q(s_k)
L10     for l ← 0 to k do add e_l → (s_back = s_l) with a fresh selector e_l
L11     φ ← φ ∧ (e_0 ∨ ... ∨ e_k)              ▷ the loop condition L_k
L12     if SAT(CNF(φ)) then
L13         return the lasso s_0 .. s_k, back to s_l for an l with e_l true
L14 return NONE
```

The CNF in lines L4 and L12 comes from the Tseitin transformation. Each AND or OR gate at each step gets a fresh variable and 3 clauses; an XOR gate gets 4 clauses. Each latch at each step adds 2 clauses for $x'_j \leftrightarrow f_j$. So the CNF of $\llbracket M \rrbracket_k$ has $O(k g)$ variables and clauses. Constants fold away: the initial values are unit clauses, and gates with a constant input need no variable.

Line L10 writes the equality $s_{\mathrm{back}} = s_l$ as $2n$ clauses $\neg e_l \vee \neg a \vee b$ and $\neg e_l \vee a \vee \neg b$ for each pair $(a, b)$ of matching variables. So $e_l$ true forces ${}_l L_k$, and line L11 forces some $e_l$. This uses $O(k n)$ clauses for the loop condition, instead of $k + 1$ copies of $T$.

## Example

A 3-bit counter $x_2 x_1 x_0$ starts at 0, and counts up by one in each step where the input $e$ is 1. The property is $P = \neg(x_0 \wedge x_1 \wedge x_2)$: the counter is never 7.

The next-state functions are $x'_0 = x_0 \oplus e$, $x'_1 = x_1 \oplus (x_0 \wedge e)$ and $x'_2 = x_2 \oplus (x_0 \wedge x_1 \wedge e)$. Each step has 4 variables (three latches, one input) and 6 gates (three XOR, three AND). For $k = 7$ the unrolling has $8 \cdot 4 + 7 \cdot 6 = 74$ variables, and $3 + 7 \cdot (12 + 9 + 6) = 192$ clauses: 3 unit clauses for $I$, and in each step 12 clauses for the XOR gates, 9 for the AND gates and 6 for the latch equalities.

For $k = 0, 1, \ldots, 6$ the formula with $\neg P(s_k)$ is unsatisfiable: in $k$ steps the counter is at most $k$. For $k = 7$ it is satisfiable, and the model has $e_0 = \cdots = e_6 = 1$ and the states $0, 1, \ldots, 7$. This is a shortest counterexample.

For the liveness property $\mathbf{F}\, x_2$ ("the counter reaches 4 or more"), BMC-LASSO succeeds already at $k = 0$: the state 0 with input $e = 0$ steps back to itself, so $e_0$ holds, and $x_2$ is false on this lasso forever.

## Correctness

Each model of the formula gives a real path, because the clauses force $s_0$ to be initial and each $s_{i+1}$ to be a successor of $s_i$. So a counterexample that BMC returns is always real. Conversely, each counterexample of length $k$ gives a model, so the search finds one when one exists within the bound, and the loop over $k$ in increasing order returns one of least length. For liveness, an infinite path with $q$ always false exists in a finite system if and only if a lasso with at most $2^n$ distinct states exists, so BMC-LASSO is complete for $\mathbf{F}\, q$ with $k_{\max} = 2^n - 1$. For safety, the bound that makes BMC complete is the [completeness threshold](/completeness-threshold/). The full proofs are below.

## Complexity

Building the formula for bound $k$ takes $O(k g)$ time, so a loop from 0 to $k$ that rebuilds it each time takes $O(k^2 g)$. An [incremental SAT](/incremental-sat/) solver adds only one new step per bound and keeps its learned clauses, so the building cost drops to $O(k g)$ in total.

Each SAT call is on a formula with $O(k g)$ variables, so the worst case is exponential in $k g$; SAT is NP-complete, and the bounded problem for safety is NP-complete too when $k$ is given in unary. In practice CDCL solvers handle unrollings with millions of clauses. The cost grows fast with $k$, so BMC finds shallow bugs in very large designs, but it rarely reaches the full depth of a large design.

## Properties

- **Sound for counterexamples.** A satisfiable formula always gives a real counterexample.
- **Incomplete by itself.** An unsatisfiable formula for all $k \le k_{\max}$ proves nothing about longer paths, unless $k_{\max}$ reaches a completeness threshold.
- **Shortest counterexamples.** Trying $k$ in increasing order gives a counterexample of least length.
- **No canonical forms.** Unlike BDDs, the CNF does not depend on a variable order, and its size is linear in $k$ times the circuit, so it never blows up in the encoding step.

## Variants and improvements

- **Full LTL.** Biere, Cimatti, Clarke and Zhu (1999) translate any LTL formula $f$ into $\llbracket M, f \rrbracket_k = \llbracket M \rrbracket_k \wedge \big( (\neg L_k \wedge \llbracket f \rrbracket_k^0) \vee \bigvee_{l=0}^{k} ({}_l L_k \wedge {}_l\llbracket f \rrbracket_k^0) \big)$, which looks for a path that satisfies $f$, that is, a counterexample to $\neg f$. The part without a loop uses a bounded semantics in which $\mathbf{G}$ can never hold on a finite prefix. The original translation has one copy of the formula for each loop position $l$, so it grows faster than linearly in $k$. The linear encoding of Biere, Heljanko, Junttila, Latvala and Schuppan (2006) grows only linearly in $k$ and in $|f|$.
- **Incremental BMC.** One solver instance for all $k$, with the property added under an assumption literal, as in Eén and Sörensson (2003).
- **Any-step check.** Ask for $\neg P$ at any step $0..k$ in one call, with a disjunction. This finds a counterexample of length at most $k$ in one SAT call, but not a shortest one.
- **Software BMC.** Unroll the loops of a program $k$ times and encode the program in bit-vector logic, as CBMC does, or in SMT.
- **Proofs from BMC.** [k-induction](/k-induction/) adds an inductive step to the same unrolling, and [interpolation](/interpolation-based-model-checking/) takes interpolants of an unsatisfiable BMC formula. Both turn BMC into a complete method.

## When to use it

Use BMC first when you look for bugs: it finds shallow counterexamples in designs too large for BDDs, and its results are concrete traces. It is the standard first engine in hardware model checkers and in bounded software checkers. To prove a property, combine it with [k-induction](/k-induction/), [IC3](/ic3-pdr/) or [interpolation](/interpolation-based-model-checking/), or run it up to a known [completeness threshold](/completeness-threshold/).

## Pitfalls

- **Reading UNSAT as a proof.** "No counterexample up to $k$" is not "the property holds". Report the bound with the result.
- **Missing loop condition.** A path of length $k$ on which $q$ is false is not a counterexample to $\mathbf{F}\, q$; the path must close into a loop. Without $L_k$, the result is unsound for liveness.
- **Deadlocks.** The lasso argument assumes every state has a successor. With dead states, either make the relation total or treat finite maximal paths explicitly.
- **Inputs at the last step.** The loop step $T(s_k, s_{\mathrm{back}})$ needs its own input copy $w_k$; sharing it with an earlier step changes the meaning.

## Implementations

## History

Biere, Cimatti, Clarke and Zhu proposed SAT-based bounded model checking at TACAS 1999, under the title "Symbolic model checking without BDDs", together with a DAC 1999 paper with Fujita on the same idea. They gave the unrolling, the loop conditions and the translation of LTL. The method spread fast in industry, as SAT solvers such as GRASP and Chaff became much faster in the same years. Sheeran, Singh and Stålmarck (2000) added induction, Eén and Sörensson (2003) made the method incremental, and McMillan (2003) used the unsatisfiable BMC formulas to compute interpolants.

## References
