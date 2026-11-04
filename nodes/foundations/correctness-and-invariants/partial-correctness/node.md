---
tag: 4X475Q
kind: definition
slug: partial-correctness
name: Partial correctness
aliases:
- Partial correctness of a program
area: foundations/correctness-and-invariants
level: intro
summary: If the program terminates on input x, its output satisfies the postcondition.
prereqs: [hoare-triple]
see_also: [total-correctness, termination-proof, loop-invariant, floyd-inductive-assertions]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
---

A program is partially correct with respect to a precondition $P$ and a postcondition $Q$ when, for each input that satisfies $P$, the output satisfies $Q$ whenever the program stops. Partial correctness says nothing about whether the program stops. For a program with loops, the proof usually uses a [loop invariant](/loop-invariant/) or [Floyd's inductive assertions](/floyd-inductive-assertions/). The Hoare triple $\{P\}\ S\ \{Q\}$ states it.

## Definition

Let $S$ be a program and $(P, Q)$ a [specification](/specification/). The program $S$ is partially correct for $(P, Q)$ when

$$\forall \sigma, \sigma' : \ \big( \sigma \models P \ \wedge \ S, \sigma \Downarrow \sigma' \big) \Rightarrow \sigma' \models Q.$$

Here $S, \sigma \Downarrow \sigma'$ means that $S$ started in $\sigma$ stops in $\sigma'$. This is the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$. The condition is an implication whose premise includes "stops". A run that does not stop makes the premise false, so it can never break partial correctness. A run that aborts with an error (a division by zero, an index out of range) has no final state $\sigma'$, so under this definition it is treated like a run that does not stop. Some logics count an abort as a failure of the triple instead.

Two consequences follow. A program that never stops on any input is partially correct for every pair $(P, Q)$. And partial correctness cannot show that the program gives any output at all. For this you need [total correctness](/total-correctness/).

## Examples and non-examples

- ISQRT of the page on [correctness](/correctness/) is partially correct for $P: n \ge 0$ and $Q: r^2 \le n < (r+1)^2$. The loop invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$ gives it. No termination argument is used.
- The loop `while true do skip` is partially correct for any $P$ and any $Q$, for example $Q$: $1 = 2$. It never stops, so no run ends in a state that breaks $Q$.
- A modified ISQRT with the test $hi - lo \ge 1$ in place of $hi - lo > 1$ is partially correct for $n \ge 0$ and the same $Q$. It never stops: when $hi = lo + 1$, then $mid = lo$ and L5 leaves $lo$ unchanged (see [total correctness](/total-correctness/)).
- Non-example: the variant of ISQRT with $hi \leftarrow n$ in L2 is not partially correct for $(n \ge 0, \ r^2 \le n < (r+1)^2)$. For $n = 1$ it stops with $r = 0$, and $1 < 1^2$ is false. This is a run that stops with a wrong output.
- Non-example: the program `x ← 1` is not partially correct for $(\mathrm{true}, \ x = 2)$. It stops in every run, and the final state breaks $Q$. A program that stops with the wrong output is the main thing that partial correctness excludes.
- Non-example: "the program stops and gives the right output" is not partial correctness. It adds the stop. That claim is total correctness.

## Related definitions

- [Total correctness](/total-correctness/): partial correctness plus termination.
- [Hoare triple](/hoare-triple/): $\{P\}\ S\ \{Q\}$ is the statement of partial correctness.
- [Loop invariant](/loop-invariant/): the usual tool for a proof of partial correctness of a loop.
- [Termination proof](/termination-proof/) and [variant function](/variant-function/): the tools for the other half.
- [Precondition](/precondition/) and [postcondition](/postcondition/): the two predicates $P$ and $Q$.
- [Hoare logic](/hoare-logic/): the proof system for partial correctness.
- [Weakest precondition](/weakest-precondition/): $\{P\}\ S\ \{Q\}$ holds exactly when $P \Rightarrow \mathrm{wlp}(S, Q)$, where $\mathrm{wlp}$ is the weakest liberal precondition. The weakest precondition $\mathrm{wp}(S, Q)$ gives total correctness.

## References
