---
tag: 6ZZFCD
kind: algorithm
slug: interpolation-based-model-checking
name: Interpolation-based model checking
aliases:
- McMillan's interpolation model checking
- Interpolation-based model checking
- ITP
area: logic-and-constraints/model-checking
level: research
summary: Prove an invariant by growing an over-approximate reachable set with Craig interpolants taken from unsatisfiable BMC queries, and increasing the depth after a spurious hit.
solves: [invariant-checking]
model: word-ram
complexity:
  vars: {n: the number of latches, g: the number of gates of the circuit, k: the depth of the BMC query, p: the size of the resolution proof of one query}
  time: {queries: O(4^n), per_query: 2^O(k (g + n)), interpolant: O(p)}
  space: {interpolant: O(p)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 2003
  people: [Kenneth L. McMillan]
  note: McMillan showed at CAV 2003 how Craig interpolants from the resolution proofs of unsatisfiable BMC queries give a complete SAT-based model checker for finite systems.
prereqs: [sat-based-bounded-model-checking, inductive-invariant, invariant-checking, cdcl]
see_also: [ic3-pdr, k-induction, bounded-model-checking, lazy-abstraction, symbolic-reachability, binary-resolution, unsat-core, completeness-threshold]
sources:
  - paper: doi:10.1007/978-3-540-45069-6_1
    title: Kenneth L. McMillan, Interpolation and SAT-based model checking, CAV 2003, LNCS 2725
    locator: pages 1 to 13 (the interpolation system for resolution proofs, the fixed-point loop over interpolants, and the proofs of soundness and termination)
  - paper: doi:10.2307/2963594
    title: William Craig, Three uses of the Herbrand-Gentzen theorem in relating model theory and proof theory, Journal of Symbolic Logic 22(3), 1957
    locator: pages 269 to 285 (the interpolation theorem for first-order logic)
---

Interpolation-based model checking, introduced by Kenneth McMillan in 2003, proves that a property $P$ holds in every reachable state of a finite system with a SAT solver. It uses the [bounded model checking](/sat-based-bounded-model-checking/) query of depth $k$, split into two parts: $A$, one step from a set $R$ of states, and $B$, a path of $k - 1$ more steps that hits a bad state. When $A \wedge B$ is unsatisfiable, the resolution proof of the solver gives a *Craig interpolant* $J$: a formula over the state after the first step, implied by $A$ and inconsistent with $B$. So $J$ contains every successor of $R$, and no state of $J$ can reach a bad state in fewer than $k$ steps. The method adds $J$ to $R$ and repeats. If $J$ adds nothing new, $R$ is an [inductive invariant](/inductive-invariant/) and $P$ holds. If the query becomes satisfiable from the exact initial states, the bug is real. If it becomes satisfiable only from the over-approximation, the depth $k$ was too small, and the method starts again with $k + 1$.

## In plain words

Bounded model checking asks a SAT solver: is there a bad run of length $k$? When the answer is no, the solver can also explain why, in the form of a proof. From that proof we can read off a formula that describes a set of states that is reached after one step and that is safe for the next $k - 1$ steps.

This set is a little bigger than the true set of reachable states, so it is a good guess. We add it to the states we have, and ask again from the bigger set. If the set stops growing, we have found a closed region that contains the start and no bad state, and the property is proved. If the bigger set can reach a bad state, our guess was too coarse, and we try again with a longer look-ahead $k$.

## The problem

A finite system has state variables $s = (x_1, \ldots, x_n)$, initial states $I(s)$, and a transition relation $T(s, s')$, for example from a circuit with $g$ gates. The task is [invariant checking](/invariant-checking/): decide whether $P(s)$ holds in every reachable state.

The tool is Craig's interpolation theorem in its propositional form. If $A \wedge B$ is unsatisfiable, there is a formula $J$ that uses only the variables common to $A$ and $B$, such that $A \Rightarrow J$ and $J \wedge B$ is unsatisfiable. McMillan's system computes such a $J$ from a resolution refutation of $A \wedge B$ in time linear in the proof size. Each clause $C$ of the proof gets a partial interpolant $p(C)$:

- an input clause of $A$ gets the disjunction of its literals over shared variables;
- an input clause of $B$ gets $\mathit{true}$;
- a resolvent on the pivot $v$ of clauses $C_1$ and $C_2$ gets $p(C_1) \vee p(C_2)$ if $v$ occurs only in $A$, and $p(C_1) \wedge p(C_2)$ otherwise.

The partial interpolant of the empty clause is the interpolant. A [CDCL](/cdcl/) solver can compute these values during conflict analysis, since each learned clause is derived by a chain of resolution steps.

## The algorithm

```pseudo id=main
ITP-CHECK(I, T, P)
L1  if SAT(I ∧ ¬P) then return FAILS
L2  for k ← 1, 2, ... do
L3      R ← I; exact ← true
L4      loop
L5          A ← R(s_0) ∧ T(s_0, s_1); B ← T(s_1, s_2) ∧ ... ∧ T(s_k−1, s_k) ∧ (¬P(s_1) ∨ ... ∨ ¬P(s_k))
L6          if SAT(A ∧ B) then
L7              if exact then return FAILS, with the path read from the model
L8              break                                   ▷ maybe spurious: try a larger k
L9          J ← INTERPOLANT(A, B)                        ▷ over the variables of s_1, renamed to s
L10         if J ⇒ R then return HOLDS, with the invariant R
L11         R ← R ∨ J; exact ← false
```

The shared variables of $A$ and $B$ are the state variables of $s_1$, so $J$ is a formula over one state. The test of line L10 is one more SAT call, on $J \wedge \neg R$.

## Example

A shift register has three latches with $x'_0 = 0$, $x'_1 = x_0$, $x'_2 = x_1$, the initial state $(x_0, x_1, x_2) = (0, 0, 0)$, and the property $P = \neg x_2$. The only reachable state is $(0, 0, 0)$. A 1 in $x_0$ reaches $x_2$ in two steps, so the states with $x_0 = 1$ or $x_1 = 1$ are unreachable but can reach a bad state. The implementation gives this run.

- $k = 1$. $R = I$. The query is unsatisfiable, and the interpolant is $J = \neg x_2$, four states. It is not contained in $R$, so $R \leftarrow I \vee \neg x_2 = \neg x_2$. The next query is satisfiable from $(0, 1, 0)$, which is in $R$ but not initial. The hit may be spurious, so $k$ grows.
- $k = 2$. $R = I$. The interpolant is $J = \neg x_1 \wedge \neg x_2$, which still contains $(1, 0, 0)$. The next query from $R = I \vee J$ reaches $x_2 = 1$ in two steps from $(1, 0, 0)$, so $k$ grows again.
- $k = 3$. $R = I$. The interpolant is $J = \neg x_0 \wedge \neg x_1 \wedge \neg x_2$, which implies $R$. The method returns HOLDS with $R = I$, which is inductive here.

Each interpolant contains all successors of $R$ and excludes all states that reach $x_2 = 1$ in fewer than $k$ steps. Only at $k = 3$ does that exclude every state that can ever reach $x_2 = 1$.

## Correctness

At each point of the loop, $R$ contains $I$, every state of $R$ satisfies $P$, and every state of $R$ is either initial or can reach no bad state in fewer than $k$ steps. Each interpolant $J$ contains every successor of $R$, since $A \Rightarrow J$.

**HOLDS is sound.** If $J \Rightarrow R$, then every successor of $R$ is in $J$, hence in $R$. So $R$ is an inductive invariant. It contains $I$, and each part of it satisfies $P$: $I$ by line L1, and each $J$ because $B$ contains $\neg P(s_1)$. So $P$ holds in every reachable state.

**FAILS is sound.** When $R = I$, the model of line L6 is a path from an initial state to a bad state.

**Termination for finite systems.** For a fixed $k$, each pass of the loop that does not stop makes $R$ strictly larger, so there are at most $2^n$ passes. If $P$ fails, a counterexample of length $m$ makes the first query at $k = m$ satisfiable from $I$. If $P$ holds, let $b$ be the largest distance from a state to the bad states, over the states that can reach a bad state at all. Once $k > b$, no interpolant contains a state that can reach a bad state, so no query is satisfiable and the loop for that $k$ ends with HOLDS. As $b < 2^n$, the depth never exceeds $2^n$. The full proof is below.

## Complexity

All bounds here are worst-case bounds. There are at most $2^n$ depths and at most $2^n$ passes per depth, so at most $O(4^n)$ SAT queries. A query of depth $k$ has $O(k (g + n))$ variables, plus the size of $R$, and a SAT call takes time exponential in that in the worst case. The interpolant is computed in time linear in the size $p$ of the resolution proof, and it can be as large as the proof. So $R$, a disjunction of interpolants, can grow large; implementations simplify it, for example with AIG rewriting.

The real cost is set by the depth $k$ that the method needs, which is at most the backward distance $b + 1$ above and is often much smaller in practice. McMillan's paper reports experiments on hardware benchmarks that compare the method with BDD-based model checking and with $k$-induction. These are measured results on specific circuits, not bounds.

## Properties

- **Sound both ways.** HOLDS comes with an inductive invariant. FAILS comes with a real counterexample.
- **Complete for finite systems.** The needed depth is bounded by the backward depth of the bad states, which can be much smaller than the depth needed by $k$-induction without strengthening.
- **Over-approximate image.** The interpolant is an approximate image operator, computed without quantifier elimination, unlike the exact image of [symbolic reachability](/symbolic-reachability/).
- **Depends on the proof.** Different resolution proofs give different interpolants, so the run depends on the SAT solver.

## Variants and improvements

- **Interpolation sequences.** Vizel and Grumberg (FMCAD 2009) compute a sequence of interpolants from one BMC query, one for each step, and so reuse the work of BMC.
- **Other interpolation systems.** The system of Pudlák and of Huang, Krajíček and Pudlák gives interpolants of different strength from the same proof. Labelled systems by D'Silva and others let one tune the strength.
- **Lazy abstraction with interpolants.** McMillan (CAV 2006) uses interpolants along program paths to refine an abstract reachability tree. See [lazy abstraction](/lazy-abstraction/).
- **SMT theories.** Interpolants for linear arithmetic and other theories carry the method to software and infinite-state systems, where it is sound but not complete.

## When to use it

Use interpolation for safety properties of hardware when the property is not close to inductive, so $k$-induction needs a large depth, and when BDDs are too large. It is a standard engine in hardware model checkers, together with BMC, $k$-induction and [IC3](/ic3-pdr/). IC3 builds its invariant from many small one-step queries; interpolation builds it from a few large unrolled queries. Which one wins depends on the design, so tools often run both in parallel.

## Pitfalls

- **Treating every hit as real.** A satisfiable query from an over-approximate $R$ does not prove a bug. Only a hit from $R = I$ does.
- **Wrong partition.** All clauses of the first transition and of $R$ must be in $A$, and the bad states must be in $B$. If the property of $s_1$ is left out of $B$, the interpolant can contain bad states, and HOLDS becomes unsound.
- **Keeping $R$ when $k$ grows.** The old interpolants were only safe for the smaller depth, so a run that keeps them can hit the same spurious path again. McMillan's method restarts from $R = I$.
- **Growth of $R$.** Without simplification, the disjunction of interpolants can become very large, and each later query pays for it.

## Implementations

## History

Craig (1957) proved the interpolation theorem for first-order logic. Pudlák (1997) and Krajíček used interpolants from resolution proofs to prove lower bounds on proof size. McMillan (CAV 2003) turned these interpolants into an image operator for SAT-based model checking. The method is complete for finite systems without the diameter of BMC or the simple-path constraints of $k$-induction. Later work by McMillan and others used interpolants for software model checking and for abstraction refinement.

## References
