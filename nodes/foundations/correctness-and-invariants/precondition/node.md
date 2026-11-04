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
summary: The condition that must hold when a procedure or loop starts. The caller must make it true, and the procedure may assume it.
prereqs: [specification]
see_also: [postcondition, hoare-triple, weakest-precondition, design-by-contract, assertion, loop-invariant]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580, the notation P {Q} R and the rules of consequence (D1)
  - paper: doi:10.1145/360933.360975
    title: Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18(8) (1975)
    locator: pp. 453 to 457, the weakest pre-condition wp(S, R)
  - paper: doi:10.1109/2.161279
    title: Bertrand Meyer, Applying "Design by Contract", IEEE Computer 25(10) (1992)
    locator: the table of the obligations and the benefits of the client and the supplier
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1 (the assertion at the start of Algorithm E)
---

A precondition is a condition on the inputs and on the state of a program that must hold when a procedure, a loop or a statement starts. It is the first half of a [specification](/specification/); the [postcondition](/postcondition/) is the second. The caller must make the precondition true, and the procedure may assume it. On a start that breaks the precondition, the specification promises nothing.

## Definition

Let $S$ be a program text, and let a state $\sigma$ give a value to each variable. A **precondition** of $S$ is a predicate $P$ on the states at the point where $S$ starts. Write $\sigma \models P$ when $\sigma$ satisfies $P$. In the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ the precondition is $P$. The triple states what $S$ guarantees on each start in a state that satisfies $P$. It states nothing about a start in any other state: there the program may return anything, fail, or run forever, and the triple is still true.

For an algorithm with inputs $x \in X$ and no other state, a precondition is a predicate on $X$, or a subset $P \subseteq X$, the set of legal inputs.

### Stronger and weaker

$P_1$ is **stronger** than $P_2$ when $P_1 \Rightarrow P_2$, that is, when each state that satisfies $P_1$ also satisfies $P_2$. A stronger precondition allows fewer starts. The predicate $\mathrm{false}$ is the strongest of all and $\mathrm{true}$ is the weakest.

**Claim (strengthening the precondition).** If $\{P_2\}\ S\ \{Q\}$ holds and $P_1 \Rightarrow P_2$, then $\{P_1\}\ S\ \{Q\}$ holds. The same is true for the total correctness triple $[P]\ S\ [Q]$.

*Proof.* Take $\sigma \models P_1$. Then $\sigma \models P_2$. Each run of $S$ from $\sigma$ that stops ends in a state that satisfies $Q$, by the first triple. This is the claim for $\{P_1\}\ S\ \{Q\}$. For the total triple, the first triple also gives that each run from $\sigma$ stops. $\square$

This is one half of Hoare's rules of consequence. A routine that is correct for a weak precondition is correct for each stronger one, so a weak precondition makes a routine more useful to its callers.

### The weakest precondition

For a fixed $S$ and $Q$, the valid preconditions form a set that is closed downward under implication, by the claim above. It has a weakest element, the predicate that holds in exactly the states from which $S$ meets $Q$:

- $\mathrm{wp}(S, Q)$, the [weakest precondition](/weakest-precondition/), holds in $\sigma$ when every run of $S$ from $\sigma$ stops in a state that satisfies $Q$. Then $[P]\ S\ [Q]$ holds exactly when $P \Rightarrow \mathrm{wp}(S, Q)$.
- $\mathrm{wlp}(S, Q)$, the weakest liberal precondition, holds in $\sigma$ when every run of $S$ from $\sigma$ that stops ends in $Q$. Then $\{P\}\ S\ \{Q\}$ holds exactly when $P \Rightarrow \mathrm{wlp}(S, Q)$.

*Proof of the first equivalence.* If $P \Rightarrow \mathrm{wp}(S, Q)$, then each $\sigma \models P$ is a state from which every run stops in $Q$, which is $[P]\ S\ [Q]$. Conversely, if $[P]\ S\ [Q]$ holds and $\sigma \models P$, then every run from $\sigma$ stops in $Q$, so $\sigma \models \mathrm{wp}(S, Q)$. The proof for $\mathrm{wlp}$ is the same with "that stops" added. $\square$

Dijkstra (1975) introduced $\mathrm{wp}$ and computes it backwards through the program text. For an assignment, $\mathrm{wp}(x \leftarrow E, Q) = Q[E/x]$, the postcondition with $E$ in place of $x$, when $E$ is defined in every state.

### Preconditions of loops and calls

- The precondition of a loop is the condition in the state before the first test. A [loop invariant](/loop-invariant/) must follow from it.
- At each call, and each recursive call, the caller must establish the precondition of the callee in the state at the call. A proof that skips this check is incomplete.
- In [design by contract](/design-by-contract/), Meyer calls the precondition an obligation of the client and a benefit of the supplier. If a precondition is broken, the bug is in the caller.

## Examples and non-examples

### Integer square root

For ISQRT on the page [correctness](/correctness/), the precondition is: $n$ is an integer and $n \ge 0$. The triple $[n \ge 0]\ \mathrm{ISQRT}\ [r^2 \le n < (r+1)^2]$ holds.

The precondition $n \ge 0$ is the weakest one for this program and this postcondition: $\mathrm{wp}(\mathrm{ISQRT}, \ r^2 \le n < (r+1)^2) = (n \ge 0)$. Proof. The triple above gives $n \ge 0 \Rightarrow \mathrm{wp}$. For the converse, take $n < 0$. Then $hi = n + 1 \le 0 = lo$, so $hi - lo \le 0$, the loop does not run, and the program stops with $r = 0$. The postcondition needs $0 \le n$, which is false. So no state with $n < 0$ is in $\mathrm{wp}$. $\square$ No program that leaves $n$ unchanged can do better for this postcondition: $r^2 \le n$ forces $n \ge 0$.

- $n \ge 1$ is a stronger precondition. Each triple that holds with $n \ge 0$ holds with $n \ge 1$, by the claim above.
- The loop of ISQRT has the precondition $lo = 0 \wedge hi = n + 1 \wedge n \ge 0$, which implies the invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$.

### Assignments

Over the integers, $\mathrm{wp}(x \leftarrow x + 1, \ x > 3) = (x + 1 > 3) = (x > 2)$. Both $x > 2$ and $x > 5$ are valid preconditions for this statement and postcondition, and $x > 2$ is the weakest. The start $x = 3$ reaches $x = 4 > 3$ and does not satisfy $x > 5$, so $x > 5$ is valid but not the weakest.

For integer division, $\mathrm{wp}(q \leftarrow a \operatorname{div} b, \ \mathrm{true}) = (b \ne 0)$: the statement fails when $b = 0$. Each division in a program adds a conjunct $b \ne 0$ to the precondition at that point.

### Binary search

For [binary search](/binary-search/) in an array $A$ of length $m$, the precondition is $A[0] \le A[1] \le \cdots \le A[m-1]$. If it fails, the search can miss a key that is present. With $A = [3, 1, 2]$ and the key $3$, the search of this site probes $A[1] = 1 < 3$ and sets $lo = 2$, then probes $A[2] = 2 < 3$ and sets $lo = 3$. The range is empty, and it returns NIL, though $A[0] = 3$. A recursive version must also show that each subarray it passes down is sorted, which holds because a subarray of a sorted array is sorted.

### Logical variables in a precondition

For an in-place sort, the precondition $A = A_0$ names the start array with a logical variable $A_0$ that the program does not change. The postcondition "$A$ is non-decreasing and is a permutation of $A_0$" can then refer to the input. The conjunct $A = A_0$ restricts nothing, since every state satisfies it for one value of $A_0$; it only gives the start value a name.

### Non-examples

- **Dropping the precondition.** With the precondition $\mathrm{true}$, the triple $\{\mathrm{true}\}\ \mathrm{ISQRT}\ \{r^2 \le n < (r+1)^2\}$ is false: for $n = -1$ the program stops with $r = 0$, and $0 \le -1$ is false. Each $n < 0$ is a counterexample.
- **Mentioning the output.** "$r \ge 0$" is not a precondition of ISQRT, because $r$ has no value before the program runs. It belongs in the postcondition.
- **A check is not a precondition.** The line `if n < 0: raise ValueError` makes a different routine. Its precondition is $\mathrm{true}$, and its postcondition has a second case: if $n < 0$, the routine raises an error. A precondition is a promise by the caller; a check is code that handles a broken promise. See [assertion](/assertion/).

### Pitfalls

- **A check that costs more than the routine.** Testing the precondition "$A$ is sorted" takes $\Theta(m)$ time, and binary search takes $O(\log m)$ time. A run-time check of this precondition destroys the reason to use binary search. Check it in tests, or prove it at the call.
- **A precondition that the caller cannot check.** "The input has no cycle" or "the hash function is uniform" are hard or impossible for a caller to test. Prefer preconditions that the caller can establish.
- **Hidden preconditions.** Non-zero divisors, non-empty arrays, indices in range and no overflow are preconditions even when nobody writes them. A proof must list them.
- **The precondition of the wrong point.** In a sequence $S_1 ; S_2$, the precondition of $S_2$ is about the state after $S_1$, not about the input.
- **Too strong to be useful.** $\mathrm{false}$ is a valid precondition for every program and postcondition, and it allows no input. A precondition must be as weak as the task allows.

## Related definitions

- [Specification](/specification/): the pair of a precondition and a [postcondition](/postcondition/).
- [Hoare triple](/hoare-triple/): the notation that puts the precondition before the program text.
- [Weakest precondition](/weakest-precondition/): the weakest $P$ for which a given $S$ meets a given $Q$.
- [Loop invariant](/loop-invariant/): it must follow from the precondition of its loop.
- [Assertion](/assertion/): a precondition is the assertion at the entry of a routine, and a run-time check can test it.
- [Design by contract](/design-by-contract/): the precondition is the duty of the caller, and the postcondition is the duty of the routine.
- [Hoare logic](/hoare-logic/): the rule of consequence strengthens preconditions and weakens postconditions.

## References
