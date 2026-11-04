---
tag: PNS96R
kind: definition
slug: weakest-precondition
name: Weakest precondition
aliases:
- wp calculus
- Dijkstra's weakest precondition
area: foundations/correctness-and-invariants
level: advanced
summary: The least restrictive precondition that guarantees a postcondition after a command, computed backwards through the code.
prereqs: [hoare-triple, total-correctness]
see_also: [guarded-commands, hoare-logic, loop-invariant, variant-function, partial-correctness, refinement-calculus]
sources:
  - url: "https://en.wikipedia.org/wiki/Predicate_transformer_semantics"
    locator: article Predicate transformer semantics, sections Weakest preconditions and Properties
  - paper: "Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18 (1975)"
    locator: pages 453 to 457
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming
    locator: Chapters 3 and 4 (the characterization of semantics, and the semantic characterization of a programming language)
  - book: isbn:9780387964805
    title: David Gries, The Science of Programming
    locator: Chapters 7 to 11 (the predicate transformer wp, and the rules for assignment, sequence, alternation and iteration)
  - paper: "Stephen A. Cook, Soundness and completeness of an axiom system for program verification, SIAM Journal on Computing 7 (1978)"
    locator: pages 70 to 90
---

The weakest precondition $\mathrm{wp}(S, Q)$ of a command $S$ and a postcondition $Q$ is the set of all initial states from which $S$ is sure to stop in a state that satisfies $Q$. Every other precondition that gives this guarantee is stronger: it implies $\mathrm{wp}(S, Q)$. So to prove the [total correctness](/total-correctness/) triple $[P]\ S\ [Q]$, it is enough to compute $\mathrm{wp}(S, Q)$ and show $P \implies \mathrm{wp}(S, Q)$. The computation goes backwards through the code, one statement at a time. Dijkstra (1975) introduced the idea together with his [guarded commands](/guarded-commands/), and program verifiers still use it to turn code into formulas.

## Definition

Use the notation of the [Hoare triple](/hoare-triple/) page. A *state* $\sigma$ gives a value to each variable. A *predicate* is a condition on states, and $\sigma \models P$ means that $\sigma$ satisfies $P$. We identify a predicate with the set of states that satisfy it, so "$P$ implies $R$" means that each state in $P$ is also in $R$, and "weaker" means "a larger set".

**Definition.** Let $S$ be a command and $Q$ a predicate.

- $\mathrm{wp}(S, Q)$ is the set of states $\sigma$ such that every run of $S$ from $\sigma$ stops, and every final state satisfies $Q$.
- $\mathrm{wlp}(S, Q)$, the *weakest liberal precondition*, is the set of states $\sigma$ such that every run of $S$ from $\sigma$ that stops ends in a state that satisfies $Q$.

The word "every" matters when $S$ is nondeterministic. For a deterministic command there is one run from each state.

**The link with triples.** Directly from the definitions:
$$ [P]\ S\ [Q] \iff \bigl(P \implies \mathrm{wp}(S, Q)\bigr), \qquad \{P\}\ S\ \{Q\} \iff \bigl(P \implies \mathrm{wlp}(S, Q)\bigr). $$
So $\mathrm{wp}(S, Q)$ is itself a valid precondition, and it is the weakest one. The predicate $\mathrm{wp}(S, \mathit{true})$ is the set of states from which $S$ is sure to stop. For the commands below, $\mathrm{wp}(S, Q) = \mathrm{wlp}(S, Q) \wedge \mathrm{wp}(S, \mathit{true})$: total correctness is [partial correctness](/partial-correctness/) plus termination.

**Rules for each command.** The function $Q \mapsto \mathrm{wp}(S, Q)$ is a *predicate transformer*. For the guarded command language it is defined by one rule for each form of command.

- $\mathrm{wp}(\mathbf{skip}, Q) = Q$.
- $\mathrm{wp}(\mathbf{abort}, Q) = \mathit{false}$. The command $\mathbf{abort}$ may fail or run forever, so nothing is guaranteed.
- *Assignment.* $\mathrm{wp}(x \leftarrow E, Q) = Q[E/x]$, the predicate $Q$ with each free $x$ replaced by $E$. This is the assignment axiom read backwards. If $E$ is not defined in each state, for example $E = a \operatorname{div} b$, the rule is $\mathrm{wp}(x \leftarrow E, Q) = \mathrm{def}(E) \wedge Q[E/x]$, here with $\mathrm{def}(E)$ being $b \ne 0$.
- *Sequence.* $\mathrm{wp}(S_1 ; S_2, Q) = \mathrm{wp}(S_1, \mathrm{wp}(S_2, Q))$. The rule for $S_2$ is applied first, because the computation goes backwards.
- *Alternation.* Let $\mathrm{IF}$ be $\mathbf{if}\ B_1 \to S_1 \mathbin{[\,]} \cdots \mathbin{[\,]} B_n \to S_n\ \mathbf{fi}$. It runs some $S_i$ whose guard $B_i$ is true, and it aborts when no guard is true. Then
$$ \mathrm{wp}(\mathrm{IF}, Q) = (B_1 \vee \cdots \vee B_n) \wedge \bigwedge_{i=1}^{n} \bigl(B_i \implies \mathrm{wp}(S_i, Q)\bigr). $$
If a guard can be undefined, add the conjunct $\mathrm{def}(B_1) \wedge \cdots \wedge \mathrm{def}(B_n)$, as in the rule for assignment.
- *Repetition.* Let $\mathrm{DO}$ be $\mathbf{do}\ B \to S\ \mathbf{od}$, which runs $S$ while $B$ is true. Let $H_0 = \neg B \wedge Q$, and $H_{k+1} = H_0 \vee \bigl(B \wedge \mathrm{wp}(S, H_k)\bigr)$. Then $H_k$ is the set of states from which the loop stops after at most $k$ iterations in a state that satisfies $Q$, and
$$ \mathrm{wp}(\mathrm{DO}, Q) = \exists k \ge 0 : H_k. $$
A loop with several guards is the same, with $B$ the disjunction of the guards and $S$ the alternation of the guarded commands.

The rule for $\mathrm{DO}$ is exact, but it is rarely used directly, because $H_k$ grows with $k$. Proofs use the loop theorem below.

**The loop theorem.** Let $P$ be a predicate, called the invariant, and $t$ an integer expression, called the [variant function](/variant-function/). Suppose that

1. $P \wedge B \implies \mathrm{wp}(S, P)$, so each iteration keeps $P$ true;
2. $P \wedge B \implies t > 0$, so the variant is positive while the loop runs;
3. $P \wedge B \wedge t = T \implies \mathrm{wp}(S, t < T)$ for each integer $T$, so each iteration makes $t$ smaller.

Then $P \implies \mathrm{wp}(\mathrm{DO}, P \wedge \neg B)$.

*Proof.* Let $Q = P \wedge \neg B$. Show by induction on $k \ge 0$ that $P \wedge t \le k \implies H_k$. Let $\sigma$ satisfy $P$ and $t \le k$. If $\neg B$ holds in $\sigma$, then $\sigma$ is in $H_0$, which is contained in $H_k$. This covers the base case $k = 0$, because there condition 2 rules out $B$. Otherwise $B$ holds, so by condition 2, $t > 0$ and $k \ge 1$. Let $T \le k$ be the value of $t$ in $\sigma$. By conditions 1 and 3 and conjunctivity (below), $\sigma$ is in $\mathrm{wp}(S, P \wedge t < T)$. Since $t$ is an integer, every final state satisfies $P \wedge t \le k - 1$, and by the induction hypothesis it is in $H_{k-1}$. By monotonicity (below), $\sigma$ is in $B \wedge \mathrm{wp}(S, H_{k-1})$, which is contained in $H_k$. Each state of $P$ has some value of $t$, and so it is in some $H_k$. $\square$

Condition 2 with $t \ge 0$ in place of $t > 0$ gives the same result, with the induction shifted by one. The theorem is how a [loop invariant](/loop-invariant/) and a variant prove total correctness of a loop.

**Healthiness properties.** For every command of the language and all predicates $Q$ and $R$:

- *Excluded miracle:* $\mathrm{wp}(S, \mathit{false}) = \mathit{false}$. No command can stop in a state that does not exist.
- *Monotonicity:* if $Q \implies R$, then $\mathrm{wp}(S, Q) \implies \mathrm{wp}(S, R)$.
- *Conjunctivity:* $\mathrm{wp}(S, Q \wedge R) = \mathrm{wp}(S, Q) \wedge \mathrm{wp}(S, R)$.
- *Disjunctivity* holds in one direction only: $\mathrm{wp}(S, Q) \vee \mathrm{wp}(S, R) \implies \mathrm{wp}(S, Q \vee R)$. The two sides are equal when $S$ is deterministic.

The rule for $\mathrm{DO}$ with a union over $k \in \mathbb{N}$ assumes that each command has finitely many possible results in each state. Dijkstra calls this bounded nondeterminism. A command such as "set $x$ to any natural number" has unboundedly many results. With it, a loop can be sure to stop although no bound $k$ holds, and the union must go over the ordinals.

## Examples and non-examples

**Examples.**

- *One assignment.* $\mathrm{wp}(x \leftarrow x + 1,\ x > 3) = (x + 1 > 3) = (x > 2)$ over the integers.
- *A sequence.* Take $S$ to be $y \leftarrow 2x ;\ x \leftarrow y - 1$ and $Q$ to be $x > 3$. First $\mathrm{wp}(x \leftarrow y - 1,\ x > 3) = (y > 4)$. Then $\mathrm{wp}(y \leftarrow 2x,\ y > 4) = (2x > 4) = (x > 2)$. So $[x > 2]\ S\ [x > 3]$ holds, and no weaker precondition gives the same guarantee.
- *Swap without a temporary.* Take $S$ to be $x \leftarrow x + y ;\ y \leftarrow x - y ;\ x \leftarrow x - y$ and $Q$ to be $x = b \wedge y = a$. Through the third assignment, $\mathrm{wp}(x \leftarrow x - y, Q) = (x - y = b \wedge y = a)$. Through the second, $x - (x - y) = b \wedge x - y = a$, that is $y = b \wedge x - y = a$. Through the first, $y = b \wedge (x + y) - y = a$, that is $y = b \wedge x = a$. So $\mathrm{wp}(S, Q) = (x = a \wedge y = b)$, and $S$ swaps $x$ and $y$ in exact integer arithmetic.
- *An alternation with overlapping guards.* Take $\mathrm{IF}$ to be $\mathbf{if}\ x \ge 0 \to y \leftarrow x \mathbin{[\,]} x \le 0 \to y \leftarrow -x\ \mathbf{fi}$ and $Q$ to be $y \ge 3$. The guards cover every integer, and both are true at $x = 0$. The rule gives $(x \ge 0 \vee x \le 0) \wedge (x \ge 0 \implies x \ge 3) \wedge (x \le 0 \implies -x \ge 3)$, which is $x \ge 3 \vee x \le -3$.
- *A loop where wp and wlp differ.* Take the program
$$ i, s \leftarrow 0, 0 ;\ \mathbf{do}\ i \ne n \to i \leftarrow i + 1 ;\ s \leftarrow s + i\ \mathbf{od} $$
with $Q$ being $s = n(n+1)/2$. Use the invariant $P$: $s = i(i+1)/2 \wedge 0 \le i \le n$ and the variant $t = n - i$. For condition 1, $\mathrm{wp}(i \leftarrow i + 1 ; s \leftarrow s + i,\ P)$ is $s + i + 1 = (i+1)(i+2)/2 \wedge 0 \le i + 1 \le n$, and this follows from $P \wedge i \ne n$. Conditions 2 and 3 hold because $i < n$ inside the loop and each iteration makes $n - i$ one smaller. At exit $i = n$, so $P \wedge \neg B$ implies $Q$. The initial assignment gives $P[0/i, 0/s] = (0 \le n)$. So $\mathrm{wp} = (n \ge 0)$. If $n < 0$, then $i$ passes over $n$ and the loop never stops. But the conjunct $s = i(i+1)/2$ alone is kept by every iteration, and it holds after the initial assignment for every $n$. So a run that stops has $i = n$ and $s = n(n+1)/2$, and $\mathrm{wlp} = \mathit{true}$.
- *Nondeterminism and disjunctivity.* Let $S$ be $\mathbf{if}\ \mathit{true} \to x \leftarrow 0 \mathbin{[\,]} \mathit{true} \to x \leftarrow 1\ \mathbf{fi}$. Then $\mathrm{wp}(S, x = 0 \vee x = 1) = \mathit{true}$, but $\mathrm{wp}(S, x = 0) = \mathrm{wp}(S, x = 1) = \mathit{false}$, because each run can end with the other value. So the disjunction rule fails in the direction from right to left.

**Non-examples.**

- *A precondition that is not the weakest.* $x > 5$ is a valid precondition of $x \leftarrow x + 1$ for $x > 3$, but it is not the weakest. The state $x = 3$ is left out, and from it the command also ends with $x > 3$.
- *Assignment applied forwards.* The rule $\mathrm{wp}(x \leftarrow E, Q) = Q[E/x]$ does not work forwards. From the precondition $x = 2$, the command $x \leftarrow x + 1$ does not give the postcondition $x + 1 = 2$. Forward reasoning needs the strongest postcondition, below.
- *Abort and liberal preconditions.* $\mathrm{wlp}(\mathbf{abort}, Q) = \mathit{true}$ but $\mathrm{wp}(\mathbf{abort}, Q) = \mathit{false}$. A liberal precondition says nothing about termination, so it is not a precondition for total correctness.
- *A miracle.* A command $\mathbf{magic}$ with $\mathrm{wp}(\mathbf{magic}, Q) = \mathit{true}$ for every $Q$, including $\mathit{false}$, breaks the law of the excluded miracle. No program can run it, so it is not in Dijkstra's language. The [refinement calculus](/refinement-calculus/) adds it on purpose as a specification statement.

## Related definitions

- **Strongest postcondition.** The *strongest postcondition* $\mathrm{sp}(S, P)$ is the set of final states of runs of $S$ that start in $P$ and stop. It computes forwards. For assignment, $\mathrm{sp}(x \leftarrow E, P) = \exists x_0 : P[x_0/x] \wedge x = E[x_0/x]$, where $x_0$ is the old value of $x$. It is dual to the liberal precondition: $\{P\}\ S\ \{Q\}$ holds exactly when $\mathrm{sp}(S, P) \implies Q$, and exactly when $P \implies \mathrm{wlp}(S, Q)$.
- **Predicate transformer semantics.** Dijkstra's approach defines the meaning of a command as its predicate transformer, $Q \mapsto \mathrm{wp}(S, Q)$, instead of as a relation between states. The two views give the same information for the language above.
- **Hoare logic.** The rules of [Hoare logic](/hoare-logic/) derive triples, and wp computes the best precondition. Cook (1978) proved that Hoare logic is complete relative to the truth of formulas in the assertion language, when that language can express the strongest postcondition $\mathrm{sp}(S, P)$ for each $S$ and $P$. This is Cook's notion of expressiveness, and an equivalent condition is that the language can express $\mathrm{wlp}(S, Q)$.
- **Verification conditions.** Program verifiers such as Boogie and Why3 compute a weakest precondition of the code against its specification, with the loop invariants that the user gives, and send the formula $P \implies \mathrm{wp}(S, Q)$ to an automatic prover. The program is correct when the prover proves the formula.
- **Derivation of programs.** Dijkstra and Gries use wp to design a program from its specification. To make an assignment establish $Q$, choose the expression $E$ so that the current state satisfies $Q[E/x]$. To design a loop, choose the invariant first and the guard so that $P \wedge \neg B \implies Q$.

## References
