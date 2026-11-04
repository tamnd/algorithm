---
tag: XB9YNH
kind: definition
slug: total-correctness
name: Total correctness
aliases:
- Total correctness of a program
area: foundations/correctness-and-invariants
level: intro
summary: Partial correctness plus a proof that the program terminates on every input satisfying the precondition.
prereqs: [partial-correctness, hoare-triple]
see_also: [termination-proof, variant-function, well-founded-relation, loop-invariant]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580 (notation and partial correctness only)
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - paper: Z. Manna and A. Pnueli, Axiomatic approach to total correctness of programs, Acta Informatica 3 (1974)
    locator: pp. 243 to 263
---

A program is totally correct with respect to a precondition $P$ and a postcondition $Q$ when, for each input that satisfies $P$, the program stops and its output satisfies $Q$. Total correctness is [partial correctness](/partial-correctness/) plus termination. It is the notion that an algorithm needs, because an algorithm that does not stop gives no answer. The statement is written $[P]\ S\ [Q]$ in the [Hoare triple](/hoare-triple/) notation.

## Definition

Let $S$ be a deterministic program and $(P, Q)$ a [specification](/specification/). Write $\sigma \models P$ when the state $\sigma$ satisfies $P$, and $S, \sigma \Downarrow \sigma'$ when $S$, started in $\sigma$, stops in $\sigma'$. The program $S$ is totally correct for $(P, Q)$ when

$$\forall \sigma : \ \sigma \models P \Rightarrow \exists \sigma' : \ \big( S, \sigma \Downarrow \sigma' \ \wedge \ \sigma' \models Q \big).$$

This is $[P]\ S\ [Q]$. It is equivalent to the conjunction of two statements:

1. Partial correctness: $\{P\}\ S\ \{Q\}$.
2. Termination: $\forall \sigma : \ \sigma \models P \Rightarrow \exists \sigma' : \ S, \sigma \Downarrow \sigma'$.

Proof of the equivalence. Assume $[P]\ S\ [Q]$. Termination is immediate. For partial correctness, take $\sigma \models P$ and $S, \sigma \Downarrow \sigma'$. By total correctness there is $\sigma''$ with $S, \sigma \Downarrow \sigma''$ and $\sigma'' \models Q$. The program is deterministic, so $\sigma' = \sigma''$, and $\sigma' \models Q$. Conversely, assume 1 and 2. Take $\sigma \models P$. By 2 there is $\sigma'$ with $S, \sigma \Downarrow \sigma'$, and by 1 we have $\sigma' \models Q$. ∎

For a nondeterministic program, total correctness requires that every execution from a state that satisfies $P$ stops, and that every final state satisfies $Q$. The form with $\exists$ above is then too weak, and the proof of the equivalence does not apply, because it uses $\sigma' = \sigma''$.

A proof of termination for a loop uses a [variant function](/variant-function/): an integer expression $v$ with $v \ge 0$ while the loop test holds, that drops by at least 1 at each step. See [termination proof](/termination-proof/). For recursion the same idea uses a [well-founded relation](/well-founded-relation/). The rule for the loop in total correctness is: if $[I \wedge B \wedge v = z]\ S\ [I \wedge v < z]$ and $I \wedge B \Rightarrow v \ge 0$, where $z$ is a fresh logical variable, then $[I]\ \textbf{while}\ B\ \textbf{do}\ S\ [I \wedge \neg B]$. The other rules are the same as in partial correctness.

## Examples and non-examples

The program ISQRT is on the page for [correctness](/correctness/). The precondition is $n \ge 0$ and the postcondition is $r^2 \le n < (r+1)^2$.

- ISQRT is totally correct. It is partially correct by the invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$. It stops because $v = hi - lo$ is an integer with $v \ge 2$ while the test holds, and each step gives a new $v$ of at most $v - 1$. For $n = 10$ the values of $v$ are $11, 5, 3, 2, 1$, and the loop stops after four steps.
- A loop that is partially correct and does not stop. Replace the test in L3 by `while hi − lo ≥ 1 do` and keep the other lines. Call the result ISQRT'.
- ISQRT' keeps the invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$. When $hi - lo \ge 1$, then $lo \le mid < hi$. If $mid^2 \le n$, then $lo \leftarrow mid$ keeps the invariant because $mid < hi$. Otherwise $mid^2 > n \ge lo^2$, so $mid > lo$, and $hi \leftarrow mid$ keeps it.
- ISQRT' never stops. The invariant contains $lo < hi$, so the test $hi - lo \ge 1$ holds at every check, and the loop never exits. When $hi = lo + 1$, then $mid = lo$ and L5 leaves $lo$ unchanged.
- Therefore $\{n \ge 0\}\ \mathrm{ISQRT'}\ \{r^2 \le n < (r+1)^2\}$ is true (and so is the same triple with the postcondition $1 = 2$), and $[n \ge 0]\ \mathrm{ISQRT'}\ [r^2 \le n < (r+1)^2]$ is false. The variant $hi - lo$ does not drop when $hi - lo = 1$, so the premise of the loop rule fails.
- Non-example: $[\mathrm{true}]\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ [Q]$ is false for each $Q$. The program stops from no state.
- Non-example: ISQRT with $hi \leftarrow n$ in L2 stops on every input, so it satisfies termination, and it is still not totally correct. It returns $0$ for $n = 1$. Termination alone is not correctness.

## Related definitions

- [Partial correctness](/partial-correctness/): the half of total correctness that does not need termination.
- [Hoare triple](/hoare-triple/): $[P]\ S\ [Q]$ is the triple for total correctness.
- [Termination proof](/termination-proof/) and [variant function](/variant-function/): how to prove that a loop stops.
- [Well-founded relation](/well-founded-relation/): the general base of termination arguments.
- [Weakest precondition](/weakest-precondition/): $\mathrm{wp}(S, Q)$ is defined with termination included. The weakest liberal precondition $\mathrm{wlp}(S, Q)$ is the counterpart for partial correctness. For deterministic $S$, $\mathrm{wp}(S, Q) = \mathrm{wlp}(S, Q) \wedge \mathrm{wp}(S, \mathrm{true})$.
- [Correctness](/correctness/): the concept that these definitions make exact.

## References
