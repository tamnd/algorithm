---
tag: XB9YNH
kind: definition
slug: total-correctness
name: Total correctness
aliases:
- Total correctness of a program
area: foundations/correctness-and-invariants
level: intro
summary: A program is totally correct for a precondition and a postcondition when every run that starts in the precondition stops, and stops in the postcondition. It is partial correctness plus termination.
prereqs: [partial-correctness, hoare-triple]
see_also: [termination-proof, variant-function, well-founded-relation, loop-invariant, weakest-precondition, hoare-logic]
sources:
  - paper: doi:10.1007/BF00288637
    title: Zohar Manna and Amir Pnueli, Axiomatic approach to total correctness of programs, Acta Informatica 3 (1974)
    locator: pp. 243 to 263
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32, the proof of termination by a map into a well-ordered set
  - paper: doi:10.1145/360933.360975
    title: Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18(8) (1975)
    locator: pp. 453 to 457, the weakest pre-condition and the semantics of the repetitive construct
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Section 4.2.3 (partial and total correctness) and Section 4.4 (proof calculus for total correctness)
---

A program is totally correct with respect to a [precondition](/precondition/) $P$ and a [postcondition](/postcondition/) $Q$ when every run that starts in a state of $P$ stops, and its final state satisfies $Q$. Total correctness is [partial correctness](/partial-correctness/) plus termination. It is the notion that an algorithm needs, because an algorithm that does not stop gives no answer. It is written $[P]\ S\ [Q]$ in the [Hoare triple](/hoare-triple/) notation of this site.

## Definition

Let $S$ be a program and $(P, Q)$ a [specification](/specification/) on states. Write $\sigma \models P$ when the state $\sigma$ satisfies $P$, and $S, \sigma \Downarrow \sigma'$ when some run of $S$ from $\sigma$ stops in $\sigma'$. The program $S$ is **totally correct** for $(P, Q)$ when, for each $\sigma \models P$:

1. every run of $S$ from $\sigma$ stops, without a run-time error; and
2. every final state $\sigma'$ with $S, \sigma \Downarrow \sigma'$ satisfies $Q$.

Condition 2 for all $\sigma \models P$ is partial correctness, $\{P\}\ S\ \{Q\}$. Condition 1 for all $\sigma \models P$ is termination. So, by definition,

$$[P]\ S\ [Q] \iff \{P\}\ S\ \{Q\} \ \wedge \ \forall \sigma \models P : S \text{ stops from } \sigma.$$

### The deterministic form

A deterministic program has one run from each state. Then total correctness is equivalent to

$$\forall \sigma : \ \sigma \models P \Rightarrow \exists \sigma' : \ \big( S, \sigma \Downarrow \sigma' \ \wedge \ \sigma' \models Q \big).$$

*Proof.* Assume total correctness and take $\sigma \models P$. By condition 1 the run from $\sigma$ stops in some $\sigma'$, and by condition 2, $\sigma' \models Q$. Conversely, assume the formula and take $\sigma \models P$. It gives a $\sigma'$ with $S, \sigma \Downarrow \sigma'$ and $\sigma' \models Q$. The run from $\sigma$ is unique, so it is the run that stops in $\sigma'$: condition 1 holds. Any final state $\sigma''$ of a run from $\sigma$ is the final state of that unique run, so $\sigma'' = \sigma'$ and condition 2 holds. $\square$

For a nondeterministic program the form with $\exists$ is too weak. Let $S$ choose between $x \leftarrow 0$ and `while true do skip`. From each state, one run stops with $x = 0$, so the formula with $\exists$ holds for $(\mathrm{true}, \ x = 0)$. The other run never stops, so $S$ is not totally correct. The proof above fails at the step "the run from $\sigma$ is unique".

### Total correctness and wp

Let $\mathrm{wp}(S, Q)$ be the set of states from which $S$ is totally correct for $Q$, and $\mathrm{wlp}(S, Q)$ the set from which it is partially correct. Then

$$\mathrm{wp}(S, Q) = \mathrm{wlp}(S, Q) \wedge \mathrm{wp}(S, \mathrm{true}).$$

*Proof.* $\sigma \in \mathrm{wp}(S, \mathrm{true})$ says that every run from $\sigma$ stops, because $\mathrm{true}$ holds in each final state. $\sigma \in \mathrm{wlp}(S, Q)$ says that every run from $\sigma$ that stops ends in $Q$. Both together are conditions 1 and 2 at $\sigma$. $\square$

The identity holds for nondeterministic programs as well. It is the state-by-state form of "total = partial + termination". See [weakest precondition](/weakest-precondition/).

### Proving termination of a loop

A [variant function](/variant-function/) for a loop $\textbf{while}\ B\ \textbf{do}\ S$ with invariant $I$ is an integer expression $t$ such that

- $I \wedge B \Rightarrow t \ge 0$; and
- one pass of $S$ from a state of $I \wedge B$ with $t = z$ ends in a state with $t \le z - 1$.

**Claim.** If the loop starts in a state of $I$ where $t$ has the value $t_0$, it makes at most $\max(0, t_0 + 1)$ passes.

*Proof.* By induction on $k$, after $k$ passes $t \le t_0 - k$, and $I$ holds by the invariant. A pass $k + 1$ starts only if $B$ holds, so $t \ge 0$, which gives $t_0 - k \ge 0$, that is $k \le t_0$. So the passes are numbered at most $1, \ldots, t_0 + 1$. $\square$

The decrease must be by at least a fixed amount on a set with no infinite descending chain. A real-valued quantity that halves at each pass, such as $1, 1/2, 1/4, \ldots$, decreases forever. This is the loop rule for total correctness in [Hoare logic](/hoare-logic/): from $[I \wedge B \wedge t = z]\ S\ [I \wedge t < z]$ and $I \wedge B \Rightarrow t \ge 0$, with $z$ a fresh logical variable, infer $[I]\ \textbf{while}\ B\ \textbf{do}\ S\ [I \wedge \neg B]$. Floyd (1967) proved termination by a map into a well-ordered set that decreases along each loop of the flowchart. Manna and Pnueli (1974) gave an axiomatic system that proves partial correctness and termination in one formalism.

For recursion, and for loops whose natural measure is not one integer, the variant takes values in a set with a [well-founded relation](/well-founded-relation/), such as pairs of natural numbers in lexicographic order. See [termination proof](/termination-proof/).

## Examples and non-examples

The program ISQRT is on the page [correctness](/correctness/). Its precondition is $n \ge 0$ and its postcondition is $r^2 \le n < (r+1)^2$.

### Examples

- **ISQRT is totally correct.** The invariant $I$: $0 \le lo < hi \wedge lo^2 \le n < hi^2$ gives partial correctness. The variant is $t = hi - lo$. Under $I \wedge B$, $t \ge 2 \ge 0$. A pass replaces $t = g$ by $\lfloor g/2 \rfloor$ or $\lceil g/2 \rceil$, both at most $g - 1$ for $g \ge 2$. For $n = 10$ the values of $t$ at the tests are $11, 5, 3, 2, 1$: four passes. The claim above bounds the passes by $t_0 + 1 = n + 2$. The halving gives the sharper bound $\lceil \lg(n+1) \rceil$, which is $4$ for $n = 10$.
- **Euclid's algorithm.** `while b ≠ 0: (a, b) ← (b, a mod b)` with $a, b \ge 0$ stops: the variant $b$ is non-negative, and for $b > 0$ the new value $a \bmod b$ is at most $b - 1$. See [Euclidean algorithm](/euclidean-algorithm/).
- **A recursion with a lexicographic variant.** The Ackermann function $A(0, n) = n + 1$, $A(m, 0) = A(m-1, 1)$, $A(m, n) = A(m-1, A(m, n-1))$ is total on $\mathbb{N}^2$. Each call on $(m, n)$ calls itself only on pairs that are smaller in the lexicographic order: $(m-1, \cdot)$, or $(m, n-1)$. This order on $\mathbb{N}^2$ is well-founded, so no infinite chain of calls exists. $A(2, 3) = 9$, computed with 44 calls.

### Non-examples

- **Partially correct, never stops.** Replace the test of ISQRT by `while hi − lo ≥ 1 do`. The invariant still holds after each pass. It contains $lo < hi$, so the test never fails. When $hi = lo + 1$, $mid = lo$ and the body sets $lo \leftarrow lo$. So $\{n \ge 0\}\ \mathrm{ISQRT'}\ \{r^2 \le n < (r+1)^2\}$ is true, and $[n \ge 0]\ \mathrm{ISQRT'}\ [r^2 \le n < (r+1)^2]$ is false. The variant $hi - lo$ does not decrease when it is $1$, so the premise of the loop rule fails exactly there.
- **Termination depends on the precondition.** The loop `i, s ← 0, 0; while i ≠ n do (i ← i + 1; s ← s + i)` stops for each $n \ge 0$ with $s = n(n+1)/2$; for $n = 10$, $s = 55$. For $n = -1$, $i$ passes over $n$ and the loop never stops. So $[n \ge 0]\ S\ [s = n(n+1)/2]$ is true, $[\mathrm{true}]\ S\ [s = n(n+1)/2]$ is false, and $\{\mathrm{true}\}\ S\ \{s = n(n+1)/2\}$ is true.
- **Unknown.** For the Collatz loop, $\{n \ge 1\}\ S\ \{n = 1\}$ is true at once, and $[n \ge 1]\ S\ [n = 1]$ is the open Collatz conjecture.
- **No state.** $[\mathrm{true}]\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ [Q]$ is false for each $Q$, including $Q = \mathrm{true}$.
- **Stops with the wrong output.** ISQRT with $hi \leftarrow n$ in line L2 stops on every $n \ge 0$, and it is not totally correct: it returns $0$ for $n = 1$. Termination alone is not correctness.

### Pitfalls

- **A quantity that decreases but not by a fixed amount.** "$hi - lo$ gets smaller" is not enough over the reals or the rationals. Show that an integer drops by at least 1, or that the values lie in a well-founded set.
- **A variant that is bounded only inside the loop.** The condition is $I \wedge B \Rightarrow t \ge 0$. Outside the loop $t$ may be negative; inside it must not be.
- **Forgetting that the variant depends on the precondition.** In the summation loop, $n - i$ is a variant only under $i \le n$, which needs $n \ge 0$ at the start.
- **Recursion through a data structure.** A recursive call on "a smaller list" terminates only if the list has no cycle. The precondition must exclude cycles.
- **Errors count.** A run that fails with a division by zero breaks total correctness, even though it stops.

## Related definitions

- [Partial correctness](/partial-correctness/): the half of total correctness that does not need termination.
- [Hoare triple](/hoare-triple/): $[P]\ S\ [Q]$ is the triple for total correctness.
- [Termination proof](/termination-proof/) and [variant function](/variant-function/): how to prove that a loop or a recursion stops.
- [Well-founded relation](/well-founded-relation/): the general base of termination arguments.
- [Weakest precondition](/weakest-precondition/): $\mathrm{wp}(S, Q)$ is the weakest precondition for total correctness.
- [Hoare logic](/hoare-logic/): its loop rule with a variant derives total correctness triples.
- [Correctness](/correctness/): the concept that these definitions make exact.

## References
