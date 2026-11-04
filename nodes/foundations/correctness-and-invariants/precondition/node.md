---
tag: MF2XDP
kind: definition
slug: precondition
name: Precondition
aliases:
- Pre-condition
- Input assumption
area: foundations/correctness-and-invariants
level: intro
summary: The condition assumed to hold on entry to a procedure or loop.
prereqs: [specification]
see_also: [postcondition, hoare-triple, design-by-contract, weakest-precondition, assertion]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
---

A precondition is a condition on the inputs, and on the state of the program, that must hold when a procedure or loop starts. It is the first half of a [specification](/specification/). The caller must make it true, and the procedure may assume it. The [postcondition](/postcondition/) is the second half.

## Definition

Let $S$ be a program with inputs $x \in X$. A precondition is a predicate $P$ on $X$, or more generally on the states of the program at the point where $S$ starts. A [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ states what $S$ guarantees when it starts in a state that satisfies $P$. It states nothing about a start in a state that does not satisfy $P$. In that case the program may give any result, fail, or not stop.

A precondition $P_1$ is stronger than $P_2$ when $P_1 \Rightarrow P_2$. A stronger precondition allows fewer inputs and makes the work of the procedure easier. If $\{P_2\}\ S\ \{Q\}$ holds and $P_1 \Rightarrow P_2$, then $\{P_1\}\ S\ \{Q\}$ holds. This is the rule of consequence of Hoare logic (Hoare 1969). For a given $S$ and $Q$, the weakest $P$ is defined by the logical order of implication. If the triple means total correctness, $[P]\ S\ [Q]$, the weakest $P$ is the [weakest precondition](/weakest-precondition/) $\mathrm{wp}(S, Q)$. If the triple means partial correctness, $\{P\}\ S\ \{Q\}$, the weakest $P$ is the weakest liberal precondition $\mathrm{wlp}(S, Q)$.

## Examples and non-examples

- For ISQRT (see [correctness](/correctness/)) the precondition is $n \ge 0$ with $n$ an integer. The postcondition $r^2 \le n < (r+1)^2$ holds after ISQRT for each such $n$.
- A stronger precondition for the same program is $n \ge 1$. Every triple that holds with $n \ge 0$ also holds with $n \ge 1$.
- For [binary search](/binary-search/) in an array $A$ of length $m$, the precondition is that $A[0] \le A[1] \le \cdots \le A[m-1]$. If $A$ is not sorted, the search can return $-1$ for a key that is present. Example: $A = [3, 1, 2]$ and $key = 3$. The first probe is $A[1] = 1 < 3$, the search goes right, then probes $A[2] = 2 < 3$, and returns $-1$, though $3 = A[0]$.
- For a loop, the precondition is a predicate that holds in the state before the first test.
- At each recursive call, the caller must establish the precondition of the call. For a recursive binary search, the subarray that the call receives must still be sorted.
- For an in-place sort of an array $A$, the precondition can be $A = A_0$, where $A_0$ is a logical variable that names the start array and that the program does not change. The postcondition "$A$ is sorted and is a permutation of $A_0$" can then refer to the input. For the loop of ISQRT it is $lo = 0 \wedge hi = n + 1 \wedge n \ge 0$.
- **Non-example: the precondition cannot be dropped.** Use the precondition "true" with ISQRT. For $n = -1$ the loop test $hi - lo = 0 > 1$ is false, so the program stops with $r = 0$, and $0^2 \le -1$ is false. So $\{\mathrm{true}\}\ \mathrm{ISQRT}\ \{r^2 \le n < (r+1)^2\}$ is false, and the same happens for each $n < 0$.
- **Non-example: a check is not a precondition.** The line `if n < 0: raise ValueError` tests the input at run time. It does not say that callers may not pass $n < 0$. With the check, the procedure is a different one, with a larger set of legal inputs and a defined behavior on the others. A precondition is a part of the contract. The check is code that can enforce it, see [assertion](/assertion/).
- **Non-example: mentions the output.** "$r \ge 0$" is not a precondition of ISQRT, because $r$ does not exist before the program runs. It belongs in the postcondition.

## Related definitions

- [Specification](/specification/): the pair of a precondition and a [postcondition](/postcondition/).
- [Hoare triple](/hoare-triple/): the notation that puts the precondition in front of the program.
- [Weakest precondition](/weakest-precondition/): the weakest $P$ for which a given triple holds.
- [Design by contract](/design-by-contract/): the precondition is the duty of the caller, and the postcondition is the duty of the routine.
- [Assertion](/assertion/): a condition stated at a point of a program. A precondition is the assertion at the entry, and a run-time check can test it.
- [Loop invariant](/loop-invariant/): the invariant of a loop must follow from the precondition of the loop.

## References
