---
tag: 0PTF6A
kind: definition
slug: hoare-triple
name: Hoare triple
aliases:
- Correctness triple
area: foundations/correctness-and-invariants
level: intro
summary: 'The notation {P} S {Q}: if P holds before program S runs and S terminates, Q holds afterwards.'
prereqs: [precondition, postcondition]
see_also: [hoare-logic, partial-correctness, total-correctness, weakest-precondition, floyd-inductive-assertions, assertion]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
---

A Hoare triple is a statement about a program $S$ with two assertions: a [precondition](/precondition/) $P$ and a [postcondition](/postcondition/) $Q$. The form $\{P\}\ S\ \{Q\}$ states [partial correctness](/partial-correctness/), and the form $[P]\ S\ [Q]$ states [total correctness](/total-correctness/). The notation comes from the logic of C. A. R. Hoare (1969), which builds on the work of R. W. Floyd (1967). The rules to prove triples are in [Hoare logic](/hoare-logic/).

## Definition

Fix a deterministic program $S$ and a set of states. Write $\sigma \models P$ when the state $\sigma$ satisfies the assertion $P$. Write $S, \sigma \Downarrow \sigma'$ when $S$ started in $\sigma$ stops in $\sigma'$.

$$\{P\}\ S\ \{Q\} \iff \forall \sigma, \sigma' : \ \big( \sigma \models P \ \wedge \ S, \sigma \Downarrow \sigma' \big) \Rightarrow \sigma' \models Q$$

$$[P]\ S\ [Q] \iff \forall \sigma : \ \sigma \models P \Rightarrow \exists \sigma' : \ \big( S, \sigma \Downarrow \sigma' \ \wedge \ \sigma' \models Q \big)$$

For a deterministic program, $[P]\ S\ [Q]$ holds exactly when $\{P\}\ S\ \{Q\}$ holds and $S$ stops from every state that satisfies $P$. The two forms differ only in the stop. Some texts use braces for both forms and say in words which one they mean. This site uses braces for partial correctness and square brackets for total correctness. Hoare's 1969 paper wrote the triple as $P \{S\} Q$.

A triple is a statement that is true or false. A triple that is true for a program is a fact about that program. A rule of Hoare logic derives true triples from other true triples. Two rules are used below. The assignment axiom: $\{Q[E/x]\}\ x \leftarrow E\ \{Q\}$, where $Q[E/x]$ is $Q$ with $E$ in place of each free $x$. The rule of consequence: if $P' \Rightarrow P$, $\{P\}\ S\ \{Q\}$ and $Q \Rightarrow Q'$, then $\{P'\}\ S\ \{Q'\}$.

## Examples and non-examples

In the examples, $x$ is a mathematical (unbounded) integer variable. With fixed-width machine integers, $\{x \ge 0\}\ x \leftarrow x + 1\ \{x \ge 1\}$ fails at the largest value.

- True: $\{x = 3\}\ x \leftarrow x + 1\ \{x = 4\}$. The only start state is $x = 3$, and it ends with $x = 4$.
- True: $\{x \ge 0\}\ x \leftarrow x + 1\ \{x \ge 1\}$. By the assignment axiom, $\{x + 1 \ge 1\}\ x \leftarrow x + 1\ \{x \ge 1\}$ holds, and $x \ge 0$ is the same as $x + 1 \ge 1$.
- True, from the assignment axiom: $\{x + 2 > 5\}\ x \leftarrow x + 2\ \{x > 5\}$. Since $x + 2 > 5 \iff x > 3$, also $\{x > 3\}\ x \leftarrow x + 2\ \{x > 5\}$.
- False: $\{\mathrm{true}\}\ x \leftarrow x + 1\ \{x > 0\}$. The state $x = -3$ satisfies the precondition and ends with $x = -2$. This state is a counterexample. Every integer $x \le -1$ is one, because it ends with $x + 1 \le 0$.
- True: $\{x > 0\}\ x \leftarrow x - 1\ \{x \ge 0\}$. False: $\{x \ge 0\}\ x \leftarrow x - 1\ \{x \ge 0\}$, because $x = 0$ ends with $x = -1$.
- True for each $S$ and each $Q$: $\{\mathrm{false}\}\ S\ \{Q\}$, because no state satisfies the precondition. Also $\{P\}\ S\ \{\mathrm{true}\}$ is true for each $P$ and $S$.
- Partial and not total: $\{\mathrm{true}\}\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ \{x = 0\}$ is true, because no run stops. $[\mathrm{true}]\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ [x = 0]$ is false. See [total correctness](/total-correctness/).
- With the running example (the program ISQRT of [correctness](/correctness/)): $[\,n \ge 0\,]\ \mathrm{ISQRT}\ [\,r^2 \le n < (r+1)^2\,]$ is true. The triple $\{\mathrm{true}\}\ \mathrm{ISQRT}\ \{r^2 \le n < (r+1)^2\}$ is false: for $n = -1$ the program stops with $r = 0$, and $0 \le -1$ is false.
- **Non-example: not a triple.** "$x \leftarrow x + 1$ is correct" has no precondition and no postcondition, so it is not a triple.
- **Non-example: a false triple.** $\{x = 3\}\ x \leftarrow x + 1\ \{x = x + 1\}$ is a triple, but it is false, because $x = x + 1$ is false in each state. To name the old value, use a logical variable that the program does not change: $\{x = x_0\}\ x \leftarrow x + 1\ \{x = x_0 + 1\}$ is true for each integer $x_0$.

## Related definitions

- [Partial correctness](/partial-correctness/) and [total correctness](/total-correctness/): the meaning of the braces and of the square brackets.
- [Hoare logic](/hoare-logic/): the proof system that derives true triples.
- [Weakest precondition](/weakest-precondition/): the weakest $P$ (in the order of implication) with $[P]\ S\ [Q]$ true. For $\{P\}\ S\ \{Q\}$ the weakest $P$ is the weakest liberal precondition.
- [Floyd's inductive assertions](/floyd-inductive-assertions/): the earlier method of Floyd, with assertions on the edges of a flowchart.
- [Assertion](/assertion/): the name for $P$ and $Q$ as logical statements.
- [Specification](/specification/): a triple for a whole program states that the program meets its specification.

## References
