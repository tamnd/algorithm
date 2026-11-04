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
summary: The condition that holds when a procedure or loop stops, provided that its precondition held at the start. It relates the result to the input.
prereqs: [specification, precondition]
see_also: [hoare-triple, partial-correctness, total-correctness, weakest-precondition, design-by-contract, assertion, loop-invariant]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580, the notation P {Q} R and the rules of consequence (D1)
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32, the verification condition for an assignment operation
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Sections 4.2.2 to 4.2.4 (Hoare triples, partial and total correctness, program and logical variables)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1 (the assertion at the exit of Algorithm E)
---

A postcondition is a condition on the state at the end of a procedure, a loop or a statement. It holds whenever the code stops after a start in which the [precondition](/precondition/) held. It is the second half of a [specification](/specification/), and it usually relates the result to the input. A program is [correct](/correctness/) when every start that meets the precondition leads to a stop in a state that meets the postcondition.

## Definition

Let $S$ be a program text. A **postcondition** of $S$ is a predicate $Q$ on the states at the point where $S$ ends. In the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ it is $Q$. Under [partial correctness](/partial-correctness/), $Q$ must hold in each final state of a run that starts in $P$ and stops. Under [total correctness](/total-correctness/), $[P]\ S\ [Q]$, each such run must also stop.

A postcondition is evaluated in the final state, so a program variable in $Q$ means its final value. To speak of the start value of $x$, the specification uses a logical variable $x_0$ that $S$ does not mention: the precondition contains $x = x_0$, and $Q$ can use $x_0$. Because $S$ cannot change $x_0$, its value in the final state is still the start value of $x$. Huth and Ryan (Section 4.2.4) use this device. Languages for contracts give the same effect with a notation such as `old x`.

### Stronger and weaker

$Q_1$ is **stronger** than $Q_2$ when $Q_1 \Rightarrow Q_2$. A stronger postcondition says more about the result.

**Claim (weakening the postcondition).** If $\{P\}\ S\ \{Q_1\}$ holds and $Q_1 \Rightarrow Q_2$, then $\{P\}\ S\ \{Q_2\}$ holds. The same is true for $[P]\ S\ [Q]$.

*Proof.* Take $\sigma \models P$ and a run of $S$ from $\sigma$ that stops in $\sigma'$. By the first triple, $\sigma' \models Q_1$, so $\sigma' \models Q_2$. For the total triple, the first triple also gives that every run from $\sigma$ stops. $\square$

**Claim (conjunction).** If $\{P\}\ S\ \{Q_1\}$ and $\{P\}\ S\ \{Q_2\}$ hold, then $\{P\}\ S\ \{Q_1 \wedge Q_2\}$ holds.

*Proof.* Each final state of a run from a state of $P$ satisfies $Q_1$ by the first triple and $Q_2$ by the second. $\square$

So a postcondition can be proved one conjunct at a time. The analogue for disjunction fails for the same reason that $\mathrm{wp}$ is not disjunctive: see the page on the [weakest precondition](/weakest-precondition/).

### The strongest postcondition

For a fixed $P$ and $S$, the **strongest postcondition** $\mathrm{sp}(S, P)$ is the predicate that holds in exactly the final states of the runs of $S$ that start in a state of $P$ and stop.

**Claim.** $\{P\}\ S\ \{Q\}$ holds exactly when $\mathrm{sp}(S, P) \Rightarrow Q$.

*Proof.* If $\{P\}\ S\ \{Q\}$ holds, each state of $\mathrm{sp}(S, P)$ is the final state of a run from $P$, so it satisfies $Q$. Conversely, if $\mathrm{sp}(S, P) \Rightarrow Q$, each final state of a run from $P$ is in $\mathrm{sp}(S, P)$, so it satisfies $Q$. $\square$

So $\mathrm{sp}(S, P)$ is itself a valid postcondition, and every valid postcondition is implied by it. It is computed forwards through the program. For an assignment,

$$\mathrm{sp}(x \leftarrow E, \ P) = \exists x_0 : \ P[x_0/x] \ \wedge \ x = E[x_0/x],$$

where $x_0$ is the value of $x$ before the assignment. Floyd (1967) gave this rule for the assignment in a flowchart. The strongest postcondition belongs to partial correctness: it says what holds if the program stops, and it is dual to the weakest liberal precondition, $\mathrm{sp}(S, P) \Rightarrow Q$ exactly when $P \Rightarrow \mathrm{wlp}(S, Q)$, since both say $\{P\}\ S\ \{Q\}$.

### The postcondition of a loop

For $\textbf{while}\ B\ \textbf{do}\ S$ with [loop invariant](/loop-invariant/) $I$, the loop rule of [Hoare logic](/hoare-logic/) gives the postcondition $I \wedge \neg B$. The loop meets a desired postcondition $Q$ when $I \wedge \neg B \Rightarrow Q$. This implication is the exit step of an invariant proof.

## Examples and non-examples

### Integer square root

For ISQRT on the page [correctness](/correctness/), the postcondition is $r^2 \le n < (r+1)^2$. For $n \ge 0$ it fixes $r = \lfloor \sqrt n \rfloor$; for $n = 10$ it fixes $r = 3$, because $9 \le 10 < 16$.

The loop of ISQRT has the invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$ and the test $hi - lo > 1$. At exit, $I \wedge \neg B$ gives $lo < hi \le lo + 1$, so $hi = lo + 1$ and $lo^2 \le n < (lo + 1)^2$. The final assignment $r \leftarrow lo$ turns this into the postcondition.

### Strongest postconditions of assignments

- $\mathrm{sp}(x \leftarrow x + 1, \ x \ge 0) = \exists x_0 : x_0 \ge 0 \wedge x = x_0 + 1$, which is $x \ge 1$ over the integers.
- $\mathrm{sp}(x \leftarrow 2x, \ 1 \le x \le 3) = \exists x_0 : 1 \le x_0 \le 3 \wedge x = 2 x_0$, which is $x \in \{2, 4, 6\}$. The postcondition $2 \le x \le 6$ is valid and weaker, because it also allows $3$ and $5$.
- $\mathrm{sp}(x \leftarrow 0, \ P) = (\exists x_0 : P[x_0/x]) \wedge x = 0$. The assignment keeps what $P$ says about the other variables and forgets what $P$ says about $x$. From $P$: $x = y \wedge y > 5$ it gives $y > 5 \wedge x = 0$.

### Sorting and searching

- For a [sort](/sorting-problem/) of an array $A$ in place, the postcondition is: $A$ is a permutation of $A_0$, and $A[0] \le A[1] \le \cdots \le A[m-1]$, where $A_0$ is the start value. Without the permutation part, the program that sets every entry to $0$ meets the rest.
- For [binary search](/binary-search/) of $k$ in a sorted array $A$ of length $m$: the result $i$ satisfies $0 \le i < m$ and $A[i] = k$, or $i = -1$ and $k$ does not occur in $A$; and $A = A_0$. The last conjunct is a **frame condition**: it says what the routine must not change. Without it, a routine that writes $k$ into $A[0]$ and returns $0$ meets the rest.

### Non-examples

- **Too weak.** $r^2 \le n$ alone holds for $r = 0$ and each $n \ge 0$, so a routine that always returns $0$ meets it. For $n = 10$, each of the seven integers $-3$ to $3$ meets it.
- **Trivial.** $\mathrm{true}$ holds after every run. The triple $\{P\}\ S\ \{\mathrm{true}\}$ is true for each $P$ and $S$, and it says nothing.
- **Without a frame on the input.** The ISQRT postcondition $r^2 \le n < (r+1)^2$ mentions the final value of $n$. The program `n ← 0; r ← 0` meets it from every start, because $0 \le 0 < 1$. The right postcondition is $n = n_0 \wedge r^2 \le n_0 < (r+1)^2$, with $n = n_0$ in the precondition.
- **The old value without a name.** $x = x + 1$ as the postcondition of $x \leftarrow x + 1$ is false in every state, so the triple $\{x = 3\}\ x \leftarrow x + 1\ \{x = x + 1\}$ is false. The intended statement is $\{x = x_0\}\ x \leftarrow x + 1\ \{x = x_0 + 1\}$.
- **Not reachable from the precondition.** With the precondition $\mathrm{true}$, the postcondition $r^2 \le n < (r+1)^2$ fails after ISQRT: for $n = -1$ the program stops with $r = 0$, and $0 \le -1$ is false. A postcondition is a claim relative to a precondition.

### Pitfalls

- **Forgetting the permutation or the frame.** Most weak postconditions in practice describe the shape of the output and forget that it must come from the input.
- **The error path.** If a routine can fail or return early, its postcondition must say what holds in that case, for example "$i = -1$ and $k$ does not occur in $A$". A postcondition that covers only the success path is false on the other one.
- **A postcondition as a promise of termination.** $\{P\}\ S\ \{Q\}$ holds for a program that never stops. If the result must exist, the claim is $[P]\ S\ [Q]$.
- **A postcondition that cannot be checked.** "The output is the shortest path" can be stated, but a run-time check costs as much as the algorithm. A [certifying algorithm](/certifying-algorithms/) returns a witness that makes the check cheap.

## Related definitions

- [Specification](/specification/): a [precondition](/precondition/) and a postcondition together.
- [Hoare triple](/hoare-triple/): the notation $\{P\}\ S\ \{Q\}$ and $[P]\ S\ [Q]$.
- [Weakest precondition](/weakest-precondition/): for a given $S$ and $Q$, the weakest $P$; it is the backward counterpart of the strongest postcondition.
- [Loop invariant](/loop-invariant/): with the negated test it gives the postcondition of the loop.
- [Assertion](/assertion/): an assertion at the end of a routine can check the postcondition at run time.
- [Design by contract](/design-by-contract/): the postcondition is the duty of the routine to its caller.
- [Symbolic execution](/symbolic-execution/): runs a program forwards on symbolic values, which computes strongest postconditions path by path.

## References
