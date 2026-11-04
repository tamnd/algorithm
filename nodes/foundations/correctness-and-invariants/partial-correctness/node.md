---
tag: 4X475Q
kind: definition
slug: partial-correctness
name: Partial correctness
aliases:
- Partial correctness of a program
area: foundations/correctness-and-invariants
level: intro
summary: A program is partially correct for a precondition and a postcondition when each run that starts in the precondition and stops ends in the postcondition. It says nothing about whether the run stops.
prereqs: [hoare-triple]
see_also: [total-correctness, termination-proof, loop-invariant, floyd-inductive-assertions, hoare-logic, weakest-precondition]
sources:
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580, the rules D0 to D3 and the discussion of termination
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Section 4.2.3 (partial and total correctness) and Section 4.3 (proof calculus for partial correctness)
  - book: isbn:9781848827448
    title: Krzysztof R. Apt, Frank S. de Boer and Ernst-Rüdiger Olderog, Verification of Sequential and Concurrent Programs, third edition, Springer (2009)
    locator: Chapter 3, While programs (the partial correctness semantics and its proof system)
---

A program is partially correct with respect to a [precondition](/precondition/) $P$ and a [postcondition](/postcondition/) $Q$ when every run that starts in a state of $P$ and stops ends in a state of $Q$. It makes no claim that the run stops. It is the statement of the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$, and its usual proof tool is the [loop invariant](/loop-invariant/). With a proof of termination it gives [total correctness](/total-correctness/).

## Definition

Let $S$ be a program and $(P, Q)$ a [specification](/specification/) on states. Write $\sigma \models P$ when the state $\sigma$ satisfies $P$, and $S, \sigma \Downarrow \sigma'$ when some run of $S$ from $\sigma$ stops in $\sigma'$. The program $S$ is **partially correct** for $(P, Q)$ when

$$\forall \sigma, \sigma' : \ \big( \sigma \models P \ \wedge \ S, \sigma \Downarrow \sigma' \big) \Rightarrow \sigma' \models Q.$$

This is the meaning of $\{P\}\ S\ \{Q\}$. The formula is an implication whose premise includes "stops". A run that never stops makes the premise false, so it cannot break partial correctness. A run that fails with an error (a division by zero, an index out of range) has no final state either, so in this standard definition it is treated like a run that never stops. Verification tools usually add separate proof obligations that rule out run-time errors.

For an algorithm with inputs $x \in X$ and a postcondition $Q(x, y)$ on the input and the output, the same statement reads $\forall x \in X : \big( P(x) \wedge A \text{ stops on } x \big) \Rightarrow Q(x, A(x))$.

### Properties

Each property below follows from the definition.

1. **Vacuous cases.** $\{\mathrm{false}\}\ S\ \{Q\}$ and $\{P\}\ S\ \{\mathrm{true}\}$ hold for each $P$, $S$ and $Q$. *Proof.* No state satisfies $\mathrm{false}$; each state satisfies $\mathrm{true}$.
2. **A program that never stops is partially correct for every specification.** *Proof.* If $S$ stops from no state of $P$, the premise is false for each $\sigma$ and $\sigma'$.
3. **Consequence.** If $P' \Rightarrow P$, $\{P\}\ S\ \{Q\}$ and $Q \Rightarrow Q'$, then $\{P'\}\ S\ \{Q'\}$. *Proof.* A start in $P'$ is a start in $P$; a final state then satisfies $Q$, and so $Q'$.
4. **Conjunction and disjunction.** From $\{P\}\ S\ \{Q_1\}$ and $\{P\}\ S\ \{Q_2\}$ follows $\{P\}\ S\ \{Q_1 \wedge Q_2\}$. From $\{P_1\}\ S\ \{Q\}$ and $\{P_2\}\ S\ \{Q\}$ follows $\{P_1 \vee P_2\}\ S\ \{Q\}$. *Proof.* In the first case each final state satisfies both postconditions. In the second, a start in $P_1 \vee P_2$ is a start in $P_1$ or in $P_2$, and either triple gives $Q$.
5. **The weakest liberal precondition.** Let $\mathrm{wlp}(S, Q)$ be the set of states from which every run that stops ends in $Q$. Then $\{P\}\ S\ \{Q\}$ holds exactly when $P \Rightarrow \mathrm{wlp}(S, Q)$. *Proof.* Both sides say that each state of $P$ has only final states in $Q$. See [weakest precondition](/weakest-precondition/).
6. **Total correctness splits.** For a deterministic program, $[P]\ S\ [Q]$ holds exactly when $\{P\}\ S\ \{Q\}$ holds and $S$ stops from each state of $P$. The page [total correctness](/total-correctness/) proves it.

### How it is proved

For a program with no loops and no recursion, the rules of [Hoare logic](/hoare-logic/) reduce $\{P\}\ S\ \{Q\}$ to one implication of predicates, $P \Rightarrow \mathrm{wlp}(S, Q)$. Each loop needs an invariant $I$ with three checks: the precondition of the loop implies $I$; one pass of the body from $I \wedge B$ gives $I$ again; and $I \wedge \neg B$ implies the postcondition of the loop. An induction on the number of passes shows that $I$ holds at each test, so a run that leaves the loop leaves it in $I \wedge \neg B$. [Floyd's inductive assertions](/floyd-inductive-assertions/) do the same on a flowchart, with one assertion on each loop. Recursion needs an induction on the depth of the calls that stop, with the hypothesis that the inner calls meet their specification.

### Undecidability

No algorithm decides, for each program and specification, whether the program is partially correct. The set of true claims is not even recursively enumerable. *Proof.* For a program $M$ and an input $w$, let $H_w$ be the program that ignores its input and runs $M$ on $w$. Then $\{\mathrm{true}\}\ H_w\ \{\mathrm{false}\}$ holds exactly when $M$ does not stop on $w$. The set of pairs $(M, w)$ on which $M$ does not stop is not recursively enumerable, because its complement, the [halting problem](/halting-problem/), is recursively enumerable and not decidable. A procedure that listed all true partial correctness triples would list this set. $\square$ So each proof of partial correctness depends on invariants that a person or a tool must find.

## Examples and non-examples

### Examples

- **ISQRT.** The program ISQRT on the page [correctness](/correctness/) is partially correct for $P$: $n \ge 0$ and $Q$: $r^2 \le n < (r+1)^2$. The invariant $0 \le lo < hi \wedge lo^2 \le n < hi^2$ gives it, with no argument about termination. For $n = 10$ the run stops with $r = 3$, and $9 \le 10 < 16$.
- **A loop that never stops.** `while true do skip` is partially correct for each $P$ and $Q$, for example for $(\mathrm{true}, \ 1 = 2)$, by property 2.
- **A modified ISQRT.** With the test `hi − lo ≥ 1` in place of `hi − lo > 1`, the program keeps the same invariant and is partially correct for the same $P$ and $Q$. It never stops: the invariant contains $lo < hi$, so the test is always true, and when $hi = lo + 1$ the body sets $lo \leftarrow mid = lo$ and the state stays the same. The page [total correctness](/total-correctness/) gives the details.
- **The Collatz loop.** The program `while n ≠ 1 do if n is even then n ← n / 2 else n ← 3n + 1` is partially correct for $(n \ge 1, \ n = 1)$, because the loop exits only when $n = 1$. Whether it is totally correct for this specification is the Collatz conjecture, which is open. From $n = 27$ the run stops after 111 passes. Here the partial correctness proof is one line, and the termination proof is unknown.
- **A run that fails.** $\{\mathrm{true}\}\ q \leftarrow 10 \operatorname{div} x\ \{x \ne 0\}$ is partially correct in the standard definition: a start with $x = 0$ fails and has no final state, and each start with $x \ne 0$ ends with $x \ne 0$. It is not totally correct.

### Non-examples

- **A wrong result.** The variant of ISQRT with $hi \leftarrow n$ in line L2 is not partially correct for $(n \ge 0, \ r^2 \le n < (r+1)^2)$. For $n = 1$ it stops with $r = 0$, and $1 < 1^2$ is false. A run that stops with a wrong output is exactly what partial correctness excludes.
- **A single statement.** `x ← 1` is not partially correct for $(\mathrm{true}, \ x = 2)$: it stops from every state with $x = 1$.
- **A stronger claim.** "The program stops and gives the right output" is not partial correctness. It is total correctness.

### Pitfalls

- **Calling a partially correct program correct.** A routine whose loop has a wrong exit test can keep every invariant and never return. The invariant proof does not detect this; only a [termination proof](/termination-proof/) does.
- **Proving partial correctness of an unsatisfiable specification.** A program that never stops is partially correct for a specification that no program can meet, such as $(\mathrm{true}, \ \mathrm{false})$. A partial correctness proof does not show that the specification makes sense.
- **Ignoring run-time errors.** Because a failing run counts like a run that never stops, a partial correctness proof says nothing about divisions by zero or indices out of range. Prove their absence as a separate obligation, or use total correctness.

## Related definitions

- [Total correctness](/total-correctness/): partial correctness plus termination.
- [Hoare triple](/hoare-triple/): $\{P\}\ S\ \{Q\}$ is the statement of partial correctness.
- [Loop invariant](/loop-invariant/): the usual tool for a proof of partial correctness of a loop.
- [Termination proof](/termination-proof/), [variant function](/variant-function/) and [well-founded relation](/well-founded-relation/): the tools for the other half.
- [Precondition](/precondition/) and [postcondition](/postcondition/): the two predicates $P$ and $Q$.
- [Hoare logic](/hoare-logic/): the proof system whose loop rule gives partial correctness.
- [Weakest precondition](/weakest-precondition/): $\mathrm{wlp}(S, Q)$ is the weakest precondition for partial correctness, and $\mathrm{wp}(S, Q)$ for total correctness.
- [Correctness](/correctness/): the concept that these definitions make exact.

## References
