---
tag: FVGKKY
kind: definition
slug: postcondition
name: Postcondition
aliases:
- Post-condition
- Output guarantee
area: foundations/correctness-and-invariants
level: intro
summary: The condition guaranteed to hold when a procedure or loop terminates, given its precondition.
prereqs: [specification, precondition]
see_also: [hoare-triple, partial-correctness, total-correctness, design-by-contract, weakest-precondition, assertion]
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

A postcondition is a condition on the result of a procedure or loop, and on its relation to the input, that holds when it stops, provided that its [precondition](/precondition/) held at the start. It is the second half of a [specification](/specification/). A program is [correct](/correctness/) when, started in any state that meets the precondition, it establishes the postcondition.

## Definition

Let $S$ be a program. A postcondition is a predicate $Q$ on the states of the program at the point where $S$ ends. It may also mention the values that the variables had at the start. Write these start values as $x_0$, the "old" value of $x$. In a [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$, the formula $Q$ is the postcondition. In [partial correctness](/partial-correctness/) it holds after each stop that began in a state of $P$. In [total correctness](/total-correctness/) the stop is also guaranteed.

A postcondition $Q_1$ is stronger than $Q_2$ when $Q_1 \Rightarrow Q_2$. A stronger postcondition says more about the result. If $\{P\}\ S\ \{Q_1\}$ holds and $Q_1 \Rightarrow Q_2$, then $\{P\}\ S\ \{Q_2\}$ holds. This is the rule of consequence (Hoare 1969).

## Examples and non-examples

- For ISQRT (see [correctness](/correctness/)) the postcondition is $r^2 \le n < (r+1)^2$. It fixes $r$ to one value for each $n \ge 0$. For $n = 10$ it gives $r = 3$, because $3^2 = 9 \le 10 < 16 = 4^2$.
- For a [sort](/sorting-problem/) of an array $A$ into $B$, the postcondition is: $B$ is a permutation of $A_0$ (the start value of $A$) and $B$ is non-decreasing.
- For [binary search](/binary-search/) in a sorted array $A$ of length $m$: the result $i$ satisfies $0 \le i < m$ and $A[i] = key$, or $i = -1$ and $key$ is not in $A$; and $A = A_0$. The last part is a frame condition: it says what the program must not change. Without it, a program that overwrites $A$ could still meet the rest.
- For the statement $x \leftarrow x + 1$ the postcondition $x = x_0 + 1$ needs the old value $x_0$. Without it, the formula $x = x + 1$ is false, and says nothing about the program.
- For a loop, the invariant together with the negation of the loop test holds at exit. The loop meets its postcondition when this conjunction implies it. For the loop of ISQRT the conjunction is $0 \le lo < hi \wedge lo^2 \le n < hi^2 \wedge hi - lo \le 1$. Then $hi = lo + 1$, so it implies $r^2 \le n < (r+1)^2$ for $r = lo$.
- **Non-example: too weak.** $r^2 \le n$ is true for the result $r = 0$ and for each $n \ge 0$. A program that returns $0$ always meets it. For $n = 10$ each integer $r$ from $-3$ to $3$ meets it.
- **Non-example: the trivial one.** The postcondition "true" holds after every program. Every triple $\{P\}\ S\ \{\mathrm{true}\}$ is true, and it tells the reader nothing.
- **Non-example: too strong for the precondition.** $r^2 \le n < (r+1)^2$ after ISQRT is false when the precondition is "true", because $n = -1$ gives $r = 0$ and $0 \le -1$ is false. The postcondition cannot be established without $n \ge 0$.

## Related definitions

- [Specification](/specification/): a [precondition](/precondition/) and a postcondition together.
- [Hoare triple](/hoare-triple/): the notation $\{P\}\ S\ \{Q\}$.
- [Weakest precondition](/weakest-precondition/): given $S$ and $Q$, the weakest $P$ with $[P]\ S\ [Q]$ true. For $\{P\}\ S\ \{Q\}$ it is the weakest liberal precondition.
- Strongest postcondition: given $P$ and $S$, the strongest $Q$ with $\{P\}\ S\ \{Q\}$ true. Each valid postcondition is implied by it.
- [Design by contract](/design-by-contract/): the postcondition is the duty of the routine.
- [Assertion](/assertion/): a condition at a program point. An assertion at the end of a routine can check the postcondition at run time.
- [Loop invariant](/loop-invariant/): with the negated loop test it gives the postcondition of the loop.

## References
