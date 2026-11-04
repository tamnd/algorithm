---
tag: 0PTF6A
kind: definition
slug: hoare-triple
name: Hoare triple
aliases:
- Correctness triple
- Partial correctness assertion
area: foundations/correctness-and-invariants
level: intro
summary: 'The statement {P} S {Q}: if P holds before program S runs and S stops, then Q holds afterwards. The form [P] S [Q] adds that S stops.'
prereqs: [precondition, postcondition]
see_also: [hoare-logic, partial-correctness, total-correctness, weakest-precondition, floyd-inductive-assertions, assertion, loop-invariant]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580, the notation P {Q} R, the axiom of assignment (D0) and the rules D1 to D3
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Sections 4.2.2 and 4.2.3 (Hoare triples, partial and total correctness) and Section 4.3.1 (proof rules)
  - book: isbn:9781848827448
    title: Krzysztof R. Apt, Frank S. de Boer and Ernst-Rüdiger Olderog, Verification of Sequential and Concurrent Programs, third edition, Springer (2009)
    locator: Chapter 3, While programs (semantics, partial and total correctness, proof systems and their soundness)
---

A Hoare triple is a statement about a program text $S$ with two [assertions](/assertion/): a [precondition](/precondition/) $P$ and a [postcondition](/postcondition/) $Q$. The form $\{P\}\ S\ \{Q\}$ states [partial correctness](/partial-correctness/): each run of $S$ that starts in a state of $P$ and stops ends in a state of $Q$. The form $[P]\ S\ [Q]$ states [total correctness](/total-correctness/): each such run also stops. Triples are the statements of [Hoare logic](/hoare-logic/), which C. A. R. Hoare introduced in 1969 on the base of the flowchart method of R. W. Floyd (1967).

## Definition

### States and runs

A state $\sigma$ gives a value to each variable. An assertion is a formula over the variables, and $\sigma \models P$ means that $P$ is true in $\sigma$. A run of $S$ from $\sigma$ can do one of three things: stop in a final state $\sigma'$, run forever, or fail (for example on a division by zero). Write $S, \sigma \Downarrow \sigma'$ when some run of $S$ from $\sigma$ stops in $\sigma'$.

### The two triples

$$\{P\}\ S\ \{Q\} \iff \forall \sigma, \sigma' : \ \big( \sigma \models P \ \wedge \ S, \sigma \Downarrow \sigma' \big) \Rightarrow \sigma' \models Q$$

$$[P]\ S\ [Q] \iff \{P\}\ S\ \{Q\} \ \wedge \ \forall \sigma \models P : \text{ every run of } S \text{ from } \sigma \text{ stops}$$

A run that fails has no final state, so the partial triple ignores it in the same way as a run that never stops, and the total triple excludes it. For a deterministic program there is one run from each state, and the total triple is equivalent to

$$\forall \sigma : \ \sigma \models P \Rightarrow \exists \sigma' : \big( S, \sigma \Downarrow \sigma' \wedge \sigma' \models Q \big).$$

The page on [total correctness](/total-correctness/) proves this, and shows why the form with $\exists$ is too weak for a nondeterministic program.

A triple is a statement that is true or false. It is **valid** when it is true in the sense above; texts write $\models \{P\}\ S\ \{Q\}$. It is **derivable** when the rules of [Hoare logic](/hoare-logic/) prove it; texts write $\vdash \{P\}\ S\ \{Q\}$. The rules are sound: each derivable triple is valid.

### Notation

Hoare's 1969 paper wrote $P\ \{Q\}\ R$, with the braces around the program $Q$, and said: if the assertion $P$ is true before the start of $Q$, then $R$ is true on its completion. The braces later moved to the assertions, which is now the common form. Notation for total correctness varies: some texts write $[P]\ S\ [Q]$, some write $\langle P \rangle\ S\ \langle Q \rangle$, and some, such as Huth and Ryan, keep the braces and mark the relation as $\models_{\mathrm{par}}$ or $\models_{\mathrm{tot}}$. This site writes braces for partial and square brackets for total correctness.

### Three rules and why they are sound

Write $Q[E/x]$ for $Q$ with the expression $E$ in place of each free occurrence of $x$, and $\sigma[x \mapsto v]$ for the state $\sigma$ with the value of $x$ changed to $v$. The base fact is the **substitution lemma**: for an expression $E$ that is defined in $\sigma$ and has value $v$ there,

$$\sigma \models Q[E/x] \iff \sigma[x \mapsto v] \models Q.$$

Each free $x$ in $Q$ reads the value $v$ on the right, and on the left the same position holds $E$, whose value in $\sigma$ is $v$; the other variables have the same values in both states. A formal proof is an induction on the structure of $Q$, with care to rename bound variables so that no variable of $E$ is captured.

- **Assignment axiom** (Hoare's D0): $\{Q[E/x]\}\ x \leftarrow E\ \{Q\}$. *Soundness.* A run from $\sigma$ stops in $\sigma[x \mapsto v]$, where $v$ is the value of $E$ in $\sigma$. If $\sigma \models Q[E/x]$, the lemma gives $\sigma[x \mapsto v] \models Q$.
- **Rule of consequence** (D1): from $P' \Rightarrow P$, $\{P\}\ S\ \{Q\}$ and $Q \Rightarrow Q'$, infer $\{P'\}\ S\ \{Q'\}$. *Soundness.* A start in $P'$ is a start in $P$, so a final state satisfies $Q$ and therefore $Q'$.
- **Rule of composition** (D2): from $\{P\}\ S_1\ \{R\}$ and $\{R\}\ S_2\ \{Q\}$, infer $\{P\}\ S_1 ; S_2\ \{Q\}$. *Soundness.* A run of $S_1 ; S_2$ that stops is a run of $S_1$ from $\sigma$ to some $\tau$ and then a run of $S_2$ from $\tau$ to $\sigma'$. From $\sigma \models P$ the first triple gives $\tau \models R$, and the second gives $\sigma' \models Q$.

The rules for the conditional and the loop, and the loop rule for total correctness with a [variant function](/variant-function/), are on the page [Hoare logic](/hoare-logic/). The [weakest precondition](/weakest-precondition/) gives the best precondition for each statement: $[P]\ S\ [Q]$ holds exactly when $P \Rightarrow \mathrm{wp}(S, Q)$.

## Examples and non-examples

In these examples the variables are mathematical integers.

### Single assignments

- True: $\{x = 3\}\ x \leftarrow x + 1\ \{x = 4\}$. The only start has $x = 3$, and it ends with $x = 4$.
- True: $\{x \ge 0\}\ x \leftarrow x + 1\ \{x \ge 1\}$. The assignment axiom gives $\{x + 1 \ge 1\}\ x \leftarrow x + 1\ \{x \ge 1\}$, and $x \ge 0$ is the same predicate as $x + 1 \ge 1$.
- True: $\{x > 3\}\ x \leftarrow x + 2\ \{x > 5\}$. The axiom gives the precondition $x + 2 > 5$, which is $x > 3$.
- False: $\{\mathrm{true}\}\ x \leftarrow x + 1\ \{x > 0\}$. The start $x = -3$ ends with $x = -2$. Each start with $x \le -1$ is a counterexample.
- True: $\{x > 0\}\ x \leftarrow x - 1\ \{x \ge 0\}$. False: $\{x \ge 0\}\ x \leftarrow x - 1\ \{x \ge 0\}$, because the start $x = 0$ ends with $x = -1$.

### A derivation: swap with a temporary

Claim: $\{x = a \wedge y = b\}\ t \leftarrow x ;\ x \leftarrow y ;\ y \leftarrow t\ \{x = b \wedge y = a\}$, where $a$ and $b$ are logical variables. Apply the assignment axiom from the end backwards.

1. Through $y \leftarrow t$: the precondition of $x = b \wedge y = a$ is $x = b \wedge t = a$.
2. Through $x \leftarrow y$: the precondition of $x = b \wedge t = a$ is $y = b \wedge t = a$.
3. Through $t \leftarrow x$: the precondition of $y = b \wedge t = a$ is $y = b \wedge x = a$.

The last predicate is the given precondition. The rule of composition, used twice, gives the claim. Every statement stops, so the total triple holds as well.

### Triples that hold for every program

- $\{\mathrm{false}\}\ S\ \{Q\}$ is true for each $S$ and $Q$: no state satisfies the precondition.
- $\{P\}\ S\ \{\mathrm{true}\}$ is true for each $P$ and $S$: each final state satisfies $\mathrm{true}$.
- $[P]\ S\ [\mathrm{true}]$ is true exactly when $S$ stops from each state of $P$. So a total triple with postcondition $\mathrm{true}$ is a pure claim of termination.

### Partial and not total

$\{\mathrm{true}\}\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ \{x = 0\}$ is true, because no run stops. $[\mathrm{true}]\ \textbf{while}\ \mathrm{true}\ \textbf{do}\ \mathrm{skip}\ [x = 0]$ is false. The same holds with the postcondition $\mathrm{false}$.

### The running example

For the program ISQRT on the page [correctness](/correctness/), $[\,n \ge 0\,]\ \mathrm{ISQRT}\ [\,r^2 \le n < (r+1)^2\,]$ is true. The page [Hoare logic](/hoare-logic/) derives it rule by rule. The triple $\{\mathrm{true}\}\ \mathrm{ISQRT}\ \{r^2 \le n < (r+1)^2\}$ is false: for $n = -1$ the program stops with $r = 0$, and $0 \le -1$ is false.

### Non-examples

- **Not a triple.** "$x \leftarrow x + 1$ is correct" has no precondition and no postcondition. It is not a statement that can be true or false.
- **The old value without a name.** $\{x = 3\}\ x \leftarrow x + 1\ \{x = x + 1\}$ is a triple, and it is false: $x = x + 1$ is false in every state. The intended claim is $\{x = x_0\}\ x \leftarrow x + 1\ \{x = x_0 + 1\}$ with a logical variable $x_0$.
- **The forward form of the assignment axiom.** $\{P\}\ x \leftarrow E\ \{P \wedge x = E\}$ is not sound. With $P$ true and $x \leftarrow x + 1$ it gives $x = x + 1$, which is false. The sound forward form is the [strongest postcondition](/postcondition/) $\exists x_0 : P[x_0/x] \wedge x = E[x_0/x]$.
- **Aliasing.** $\{a[j] = 5\}\ a[i] \leftarrow 3\ \{a[j] = 5\}$ looks like an instance of the assignment axiom, because $a[i]$ does not occur in the postcondition. It is false when $i = j$. Treat the array as one variable: $a[i] \leftarrow 3$ assigns to $a$ the array that is $3$ at $i$ and equal to $a$ elsewhere. The axiom then gives the precondition $i \ne j \wedge a[j] = 5$.

### Pitfalls

- **Reading a partial triple as a promise of a result.** $\{P\}\ S\ \{Q\}$ holds for a program that never stops. If the result must exist, prove $[P]\ S\ [Q]$.
- **Machine integers.** With 64-bit integers that wrap around, $\{x \ge 0\}\ x \leftarrow x + 1\ \{x \ge 1\}$ fails at $x = 2^{63} - 1$, which ends with $x = -2^{63}$. The triple is true over mathematical integers only. In C, signed overflow is undefined, so the triple has no meaning there without the precondition $x < 2^{63} - 1$.
- **Expressions that can fail.** The axiom $\{Q[E/x]\}\ x \leftarrow E\ \{Q\}$ assumes that $E$ is defined. For $E = a \operatorname{div} b$, a total triple needs the precondition $b \ne 0 \wedge Q[E/x]$.
- **Validity is not derivability in a fixed system.** Over the integers no effective proof system derives every valid triple; the page [Hoare logic](/hoare-logic/) explains the limit and Cook's relative completeness.

## Related definitions

- [Partial correctness](/partial-correctness/) and [total correctness](/total-correctness/): the meaning of the braces and of the square brackets.
- [Hoare logic](/hoare-logic/): the proof system that derives triples, with one rule for each statement.
- [Weakest precondition](/weakest-precondition/): $[P]\ S\ [Q]$ holds exactly when $P \Rightarrow \mathrm{wp}(S, Q)$, and $\{P\}\ S\ \{Q\}$ exactly when $P \Rightarrow \mathrm{wlp}(S, Q)$.
- [Floyd's inductive assertions](/floyd-inductive-assertions/): the earlier method with assertions on the edges of a flowchart.
- [Loop invariant](/loop-invariant/): the assertion that the loop rule needs.
- [Specification](/specification/): a triple for a whole program states that it meets its specification.
- [Separation logic](/separation-logic/): an extension of triples to programs with pointers, which handles the aliasing problem above.

## References
