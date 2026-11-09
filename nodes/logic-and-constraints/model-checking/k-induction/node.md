---
tag: ZHFE5T
kind: algorithm
slug: k-induction
name: k-induction
aliases:
- Induction-based model checking
- Temporal induction
- SAT-based induction
area: logic-and-constraints/model-checking
level: advanced
summary: Prove an invariant with two SAT checks per depth k, a BMC base case and an induction step over any k + 1 good states; simple-path constraints make it complete for finite systems.
solves: [invariant-checking]
model: word-ram
complexity:
  vars: {k: the depth reached, g: the number of gates of the circuit, n: the number of latches}
  time: {build: O(k^2 · (g + k n)), solve: 2^O(k (g + k n))}
  space: {formula: O(k g + k^2 n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 2000
  people: [Mary Sheeran, Satnam Singh, Gunnar Stålmarck]
  note: Sheeran, Singh and Stålmarck proved safety properties with SAT by induction over paths of growing length, and made the method complete with loop-free paths, at FMCAD 2000.
prereqs: [sat-based-bounded-model-checking, inductive-invariant, invariant-checking]
see_also: [bounded-model-checking, ic3-pdr, interpolation-based-model-checking, completeness-threshold, incremental-sat, safety-property, loop-invariant, cdcl]
sources:
  - paper: doi:10.1007/3-540-40922-X_8
    title: Mary Sheeran, Satnam Singh and Gunnar Stålmarck, Checking safety properties using induction and a SAT-solver, FMCAD 2000, LNCS 1954
    locator: pages 108 to 125 (the base case and the induction step, the loop-free path constraints, and the proof that the method is complete for finite systems)
  - paper: "Niklas Eén and Niklas Sörensson, Temporal induction by incremental SAT solving, Electronic Notes in Theoretical Computer Science 89(4), 2003"
    title: Temporal induction by incremental SAT solving
    locator: the incremental formulation of the base and step cases, and the lazy addition of the simple-path constraints
  - paper: "Leonardo de Moura, Harald Rueß and Maria Sorea, Bounded model checking and induction, from refutation to verification, CAV 2003, LNCS 2725"
    title: Leonardo de Moura, Harald Rueß and Maria Sorea, Bounded model checking and induction, from refutation to verification, CAV 2003, LNCS 2725
    locator: k-induction for infinite-state systems with decision procedures, and the strengthening of the induction step
---

$k$-induction proves that a property $P$ holds in every reachable state of a system, with SAT calls on unrolled formulas. At depth $k$ it makes two checks. The *base case* is a [bounded model checking](/sat-based-bounded-model-checking/) query: no path of $k$ steps from an initial state ends in a state where $P$ fails. The *step case* forgets the initial states: every path of $k + 1$ states that all satisfy $P$ extends only to states that satisfy $P$. If both hold, then $P$ is an invariant, by induction on the length of paths. If the step case fails, $k$ grows by one. Plain $k$-induction can fail at every $k$, because a path that loops in good but unreachable states is a counterexample to every step. With the *simple-path constraint*, that all states on the path are distinct, the step case holds for some $k \le 2^n - 1$ in every finite system where $P$ is an invariant. So the method is complete for finite systems, but the needed $k$ can be very large.

## In plain words

Bounded model checking only looks for bad runs up to a given length. To prove that no bad run exists at all, we use a proof by induction, as in school mathematics.

The base: no run of up to $k$ steps from the start reaches a bad state. The step: any $k + 1$ good states in a row, from anywhere, are followed by a good state. If both are true, a run can never become bad. A SAT solver checks each part. If the step fails, we try a longer chain. Requiring the chain to visit no state twice makes sure that the step holds for some length in a system with finitely many states.

## The problem

A finite system has state variables $s = (x_1, \ldots, x_n)$, initial states $I(s)$ and a transition relation $T(s, s')$, for example from a circuit with $g$ gates. A property $P(s)$ is an invariant if it holds in every reachable state. This is the [invariant checking](/invariant-checking/) problem. For $k \ge 0$, $P$ is *$(k+1)$-inductive* if
$$P(s_0) \wedge T(s_0, s_1) \wedge P(s_1) \wedge \cdots \wedge P(s_k) \wedge T(s_k, s_{k+1}) \;\Rightarrow\; P(s_{k+1})$$
is valid. For $k = 0$ this says that $P$ is an [inductive invariant](/inductive-invariant/): $P \wedge T \Rightarrow P'$.

## The algorithm

```pseudo id=main
K-INDUCTION(I, T, P, kmax)
L1  for k ← 0 to kmax do
L2      if SAT(I(s_0) ∧ T(s_0, s_1) ∧ ... ∧ T(s_k−1, s_k) ∧ ¬P(s_k)) then     ▷ base case
L3          return FAILS, with the path read from the model
L4      φ ← P(s_0) ∧ T(s_0, s_1) ∧ ... ∧ P(s_k) ∧ T(s_k, s_k+1) ∧ ¬P(s_k+1)    ▷ step case, no I
L5      φ ← φ ∧ ⋀ { s_i ≠ s_j : 0 ≤ i < j ≤ k + 1 }                         ▷ simple-path constraint
L6      if not SAT(φ) then
L7          return HOLDS                                                   ▷ P is (k + 1)-inductive on simple paths
L8  return UNKNOWN
```

Each $s_i \ne s_j$ is the clause $\bigvee_t (x_t^{(i)} \oplus x_t^{(j)})$, with one Tseitin variable per XOR. The base case at depth $k$ only checks paths of exactly $k$ steps: the shorter ones were checked in earlier rounds. So when the base case fails, the path it returns is a shortest counterexample.

## Example

A system has two latches $x_0$ and $x_1$, an input $e$, the initial state $(x_0, x_1) = (0, 0)$, and the next-state functions $x'_0 = x_0$ and $x'_1 = x_1 \vee (x_0 \wedge e)$. The property is $P = \neg(x_0 \wedge x_1)$. Only $(0, 0)$ is reachable, as $x_0$ stays 0, so $P$ holds.

- $k = 0$. The base case is unsatisfiable: $(0, 0)$ satisfies $P$. The step case is satisfiable: $s_0 = (1, 0)$ with $e = 1$ goes to $s_1 = (1, 1)$. So $P$ is not inductive.
- $k = 1$, without the simple-path constraint. The step case is satisfiable: $(1, 0) \to (1, 0) \to (1, 1)$, with $e = 0$ and then $e = 1$. The same trick with more copies of $(1, 0)$ works for every $k$, so plain $k$-induction never terminates here. The implementation returns UNKNOWN for $k_{\max} = 6$.
- $k = 1$, with the simple-path constraint. A path $s_0, s_1, s_2$ needs $s_2 = (1, 1)$. Its predecessor $s_1$ must satisfy $P$ and have $x_0 = 1$, so $s_1 = (1, 0)$. The only predecessor of $(1, 0)$ is $(1, 0)$ itself, since $x_0$ never changes and $x_1$ never goes from 1 to 0. So $s_0 = s_1$, which the constraint forbids. The step case is unsatisfiable, and the method returns HOLDS at $k = 1$.

## Correctness

If the base cases for all depths up to $k$ and the step case at $k$ hold, take a shortest path from $I$ to a state where $P$ fails, of length $m$. The base cases give $m > k$. A shortest such path visits no state twice, and $P$ holds on all its states but the last. Its last $k + 2$ states then form a simple path that the step case excludes, a contradiction. So HOLDS is sound, with or without the simple-path constraint. FAILS is sound because the base case is BMC. For completeness: if $P$ is an invariant, no base case fails, and a simple path has at most $2^n$ states, so the step case with the constraint is unsatisfiable at $k = 2^n - 1$ at the latest. The full proof is below.

## Complexity

Round $k$ makes two SAT calls. The base case has $O(k g)$ variables and clauses. The step case has $O(k g)$ for the unrolling and $O(k^2 n)$ for the simple-path constraint, since there are $\binom{k+2}{2}$ pairs of states with $n$ XOR gates each. So the formulas up to depth $k$ take $O(k^2 (g + k n))$ time to build, or less with [incremental SAT](/incremental-sat/), and each SAT call is exponential in the formula size in the worst case.

The depth $k$ that the method needs is the real cost. It is at most the length of the longest simple path in the states that satisfy $P$, which can be close to $2^n$. A system with an unreachable chain of $2^n - 2$ good states that ends in a bad state needs about that depth. In such cases one strengthens $P$ by hand or by an invariant generator, or uses [IC3](/ic3-pdr/), which finds the strengthening by itself.

## Properties

- **Sound both ways.** FAILS comes with a real, shortest counterexample, and HOLDS is a proof.
- **Complete for finite systems** with the simple-path constraint, with $k \le 2^n - 1$. Without the constraint it is incomplete.
- **Strength grows with $k$.** If $P$ is $j$-inductive, it is also $(j+1)$-inductive. So the step case, once unsatisfiable, stays unsatisfiable for larger $k$.
- **A by-product of BMC.** The base case is exactly BMC, so $k$-induction finds the same bugs as BMC at the same depth.

## Variants and improvements

- **Incremental $k$-induction.** Eén and Sörensson (2003) keep one solver for the base cases and one for the step cases, and add the simple-path constraints lazily, only between states that the solver made equal.
- **Strengthening with invariants.** Add known invariants, from another engine or from a template-based generator, to every state of the step case. This often brings the needed $k$ down to 1 or 2.
- **Infinite-state systems.** De Moura, Rueß and Sorea (2003) use the same scheme with SMT solvers for systems over integers and reals. There the method is sound but not complete.
- **Software verification.** $k$-induction for loops of C programs, as in tools such as ESBMC and 2LS, unrolls each loop and checks the step case with nondeterministic values for the variables at the loop head.
- **Parallel $k$-induction.** Run the base cases and the step cases for several $k$ at the same time, as in the Kind model checker for Lustre programs.

## When to use it

Use $k$-induction when the property is inductive or close to inductive, for example when it already holds with a few extra invariants. It is simple, and it reuses a BMC engine. It is a standard engine in hardware model checkers, often run in parallel with BMC and IC3. When the property needs a deep or complex strengthening, IC3 or [interpolation](/interpolation-based-model-checking/) usually do better, because they build the strengthening themselves.

## Pitfalls

- **Forgetting the base cases for smaller $k$.** The step case at $k$ needs the base cases at all depths from 0 to $k$. If one keeps only depth $k$, a short counterexample can be missed.
- **No simple-path constraint.** Without it, a self-loop in a good unreachable state defeats the step case at every $k$, as in the example.
- **Assuming $P$ only at the last state.** The step case must assume $P$ in each of $s_0, \ldots, s_k$; that is what makes it stronger than plain induction.
- **Infinite-state systems.** There the simple-path constraint does not give completeness, since simple paths can be arbitrarily long.

## Implementations

## History

Sheeran, Singh and Stålmarck (FMCAD 2000) introduced the method for hardware, with Stålmarck's SAT procedure. They showed that the restriction to loop-free paths makes it complete for finite systems. Eén and Sörensson (2003) made it incremental with the MiniSat solver. De Moura, Rueß and Sorea (2003) carried it to infinite-state systems with decision procedures, and later work brought it to Lustre programs (the Kind model checker) and to C programs.

## References
