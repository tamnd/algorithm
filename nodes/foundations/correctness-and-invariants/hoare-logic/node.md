---
tag: V4RZ1G
kind: concept
slug: hoare-logic
name: Hoare logic
aliases:
- Floyd-Hoare logic
area: foundations/correctness-and-invariants
level: advanced
summary: A proof system for deriving Hoare triples from axioms and inference rules for each program construct.
prereqs: [hoare-triple, loop-invariant]
see_also: [weakest-precondition, total-correctness, partial-correctness, separation-logic, program-verification, rice-theorem, variant-function]
sources:
  - url: "https://en.wikipedia.org/wiki/Hoare_logic"
    locator: article Hoare logic, sections Rules and Total correctness
  - paper: "C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12 (1969)"
    locator: pages 576 to 580
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19 (1967)"
    locator: pages 19 to 32
  - paper: "Stephen A. Cook, Soundness and completeness of an axiom system for program verification, SIAM Journal on Computing 7 (1978)"
    locator: pages 70 to 90
  - paper: "Edmund M. Clarke, Programming language constructs for which it is impossible to obtain good Hoare axiom systems, Journal of the ACM 26 (1979)"
    locator: pages 129 to 147
  - paper: "Krzysztof R. Apt, Ten years of Hoare's logic: a survey, part I, ACM Transactions on Programming Languages and Systems 3 (1981)"
    locator: pages 431 to 483
  - paper: "Susan Owicki and David Gries, An axiomatic proof technique for parallel programs I, Acta Informatica 6 (1976)"
    locator: pages 319 to 340
  - book: isbn:9780387964805
    title: David Gries, The Science of Programming
    locator: Part II (the rules for each statement, and proof outlines)
---

## In plain words

A Hoare triple states that a piece of code, started in a good state, ends in a good state if it ends at all. Hoare logic is a set of rules for proving such statements. There is one rule for each kind of statement in the language: one for an assignment, one for two statements in sequence, one for an if statement and one for a loop. One more rule lets you make a precondition stronger or a postcondition weaker. A proof starts from the small statements and joins their facts until it reaches the whole program. The rule for a loop needs a loop invariant, and the person who writes the proof must find it. The rules give only true statements, and if every true fact about the conditions may be used, they can prove every true statement about a program. Without that help, no set of rules can.

## The idea

Hoare logic is the classic example of an *axiomatic semantics*: it gives a program its meaning by the rules that prove facts about it.

**The language.** Take a small language of statements over integer variables: $\mathbf{skip}$, the assignment $x \leftarrow E$, the sequence $S_1 ; S_2$, the conditional $\mathbf{if}\ B\ \mathbf{then}\ S_1\ \mathbf{else}\ S_2$, and the loop $\mathbf{while}\ B\ \mathbf{do}\ S$. Conditions $P$, $Q$ and $I$ are formulas of first-order arithmetic over the program variables. The notation is that of the [Hoare triple](/hoare-triple/) page: $\{P\}\ S\ \{Q\}$ states [partial correctness](/partial-correctness/), and $[P]\ S\ [Q]$ states [total correctness](/total-correctness/).

**The rules for partial correctness.** Each rule has premises above the line and a conclusion below it. A rule with no premises is an axiom.

$$ \frac{}{\{P\}\ \mathbf{skip}\ \{P\}} \qquad \frac{}{\{Q[E/x]\}\ x \leftarrow E\ \{Q\}} \qquad \frac{\{P\}\ S_1\ \{R\} \quad \{R\}\ S_2\ \{Q\}}{\{P\}\ S_1 ; S_2\ \{Q\}} $$

$$ \frac{\{P \wedge B\}\ S_1\ \{Q\} \quad \{P \wedge \neg B\}\ S_2\ \{Q\}}{\{P\}\ \mathbf{if}\ B\ \mathbf{then}\ S_1\ \mathbf{else}\ S_2\ \{Q\}} \qquad \frac{\{I \wedge B\}\ S\ \{I\}}{\{I\}\ \mathbf{while}\ B\ \mathbf{do}\ S\ \{I \wedge \neg B\}} $$

$$ \frac{P \implies P' \quad \{P'\}\ S\ \{Q'\} \quad Q' \implies Q}{\{P\}\ S\ \{Q\}} $$

The last rule is the rule of consequence. Its two implications are formulas of arithmetic, not triples, so a proof in Hoare logic has two parts: a derivation that uses the rules, and proofs of these side conditions in arithmetic. The second part is where the real work is.

**Three points about the rules.**

- *The assignment axiom goes backwards.* The precondition is the postcondition with $E$ in place of $x$. For example, $\{x + 1 > 3\}\ x \leftarrow x + 1\ \{x > 3\}$. The forward form $\{P\}\ x \leftarrow E\ \{P \wedge x = E\}$ is false: from $x = 2$, the command $x \leftarrow x + 1$ does not end with $x = x + 1$.
- *The loop rule needs an invariant.* The rule does not say how to find $I$. For a program with no loops, the derivation can be computed from the [weakest precondition](/weakest-precondition/) of each statement. What remains is one side condition, $P \implies \mathrm{wp}(S, Q)$, to prove in arithmetic. A program with loops needs one invariant for each loop. This is the only creative step, see [loop invariant](/loop-invariant/).
- *The loop rule says nothing about termination.* The conclusion is about runs that stop.

**Total correctness.** All rules stay the same with $[\,]$ in place of $\{\}$, except the loop rule. The new loop rule uses a [variant function](/variant-function/) $t$, an integer expression, and a fresh logical variable $z$:

$$ \frac{[I \wedge B \wedge t = z]\ S\ [I \wedge t < z] \qquad I \wedge B \implies t \ge 0}{[I]\ \mathbf{while}\ B\ \mathbf{do}\ S\ [I \wedge \neg B]} $$

Each iteration makes $t$ smaller, and $t$ cannot go below $0$ while the loop runs, so the loop stops after at most $\max(0, t + 1)$ iterations, where $t$ is its value at the start.

**Soundness.** Every triple that the rules derive is true in the standard model of the integers. The proof is by induction on the derivation: each axiom is true, and each rule takes true premises to a true conclusion. For the loop rule, an induction on the number of iterations shows that $I$ holds each time the test is evaluated, and the loop exits only when $\neg B$ holds. Hoare (1969) gave the assignment axiom and the rules of consequence, sequence and iteration. The rule for the conditional was added in later presentations. Floyd (1967) gave the same method on flowcharts, with termination proved by a map into a well-ordered set.

**Completeness, and its limit.** The converse question is whether every true triple can be derived. Two results answer it.

- *No complete system exists.* The triple $\{\mathit{true}\}\ \mathbf{skip}\ \{P\}$ is true exactly when the formula $P$ is true in arithmetic. A proof system with a decidable set of proofs lists its derivable triples one by one. If it derived every true triple, it would list the true formulas of arithmetic. By Gödel's incompleteness theorem, no such list exists. So no proof system for triples over the integers derives every true triple.
- *Relative completeness.* Cook (1978) showed that the failure comes only from arithmetic. Suppose that the side conditions of the rule of consequence may use every true formula of the assertion language as an axiom, and that the language can express the strongest postcondition of each statement. Then the rules derive every true triple. The language of arithmetic with $+$ and $\times$ has this property for the language above. The proof uses the [weakest precondition](/weakest-precondition/): the invariant that the loop rule needs is $\mathrm{wlp}(\mathbf{while}\ B\ \mathbf{do}\ S, Q)$.
- *Constructs with no good system.* Clarke (1979) showed that some combinations of language features have no Hoare logic that is sound and relatively complete in this sense. One example is procedures that are passed as parameters, together with recursion, static scope, global variables and nested procedures. The reason is that, for such a language, it is undecidable whether a program halts even when the domain of values is finite. A sound and relatively complete system would make this question decidable for finite domains.

**Aliasing.** The assignment axiom assumes that the variable $x$ has one name. With an array $a$, the triple $\{a[j] = 5\}\ a[i] \leftarrow 3\ \{a[j] = 5\}$ looks true by the axiom, because $a[i]$ does not appear in the postcondition, but it is false when $i = j$. The usual fix treats the whole array as one variable that the assignment changes: $a[i] \leftarrow E$ means $a \leftarrow \mathrm{upd}(a, i, E)$, where $\mathrm{upd}(a, i, E)[j]$ is $E$ if $j = i$ and $a[j]$ otherwise. The axiom then gives the precondition $(i = j \wedge 3 = 5) \vee (i \ne j \wedge a[j] = 5)$, which is $i \ne j \wedge a[j] = 5$. For pointers and records the same problem is much worse, and [separation logic](/separation-logic/) was designed for it.

## Examples

**A derivation for ISQRT.** The program ISQRT on the [correctness](/correctness/) page computes the integer square root:

```
lo ← 0 ; hi ← n + 1 ;
while hi − lo > 1 do
    mid ← lo + ⌊(hi − lo)/2⌋ ;
    if mid · mid ≤ n then lo ← mid else hi ← mid ;
r ← lo
```

The goal is $\{n \ge 0\}\ \mathrm{ISQRT}\ \{r^2 \le n < (r+1)^2\}$. Let $I$ be $0 \le lo < hi \wedge lo^2 \le n < hi^2$ and $B$ be $hi - lo > 1$. The derivation goes from the inside out.

1. *The two branches.* By the assignment axiom, $\{I[mid/lo]\}\ lo \leftarrow mid\ \{I\}$ and $\{I[mid/hi]\}\ hi \leftarrow mid\ \{I\}$. Here $I[mid/lo]$ is $0 \le mid < hi \wedge mid^2 \le n < hi^2$, and $I[mid/hi]$ is $0 \le lo < mid \wedge lo^2 \le n < mid^2$.
2. *The conditional.* Let $R$ be $I \wedge B \wedge lo < mid < hi$. Side conditions: $R \wedge mid^2 \le n$ implies $I[mid/lo]$, and $R \wedge \neg(mid^2 \le n)$ implies $I[mid/hi]$. Both follow by arithmetic: $R$ already gives $0 \le lo < mid < hi$, and the test of the branch gives the bound on $mid^2$. By consequence and the conditional rule, $\{R\}\ \mathbf{if} \cdots\ \{I\}$.
3. *The midpoint.* By the assignment axiom, $\{R[E/mid]\}\ mid \leftarrow E\ \{R\}$ with $E = lo + \lfloor (hi - lo)/2 \rfloor$. Side condition: $I \wedge B$ implies $R[E/mid]$, that is $lo < E < hi$. With $g = hi - lo \ge 2$, we have $E - lo = \lfloor g/2 \rfloor \ge 1$ and $hi - E = g - \lfloor g/2 \rfloor \ge 1$. By consequence and the sequence rule, $\{I \wedge B\}\ \text{body}\ \{I\}$.
4. *The loop.* The loop rule gives $\{I\}\ \mathbf{while} \cdots\ \{I \wedge \neg B\}$.
5. *The start.* By the assignment axiom twice and the sequence rule, $\{I[0/lo][n+1/hi]\}\ lo \leftarrow 0 ; hi \leftarrow n + 1\ \{I\}$, and the precondition is $0 < n + 1 \wedge 0 \le n < (n+1)^2$. Side condition: $n \ge 0$ implies it.
6. *The end.* By the assignment axiom, $\{lo^2 \le n < (lo+1)^2\}\ r \leftarrow lo\ \{r^2 \le n < (r+1)^2\}$. Side condition: $I \wedge \neg B$ implies $lo^2 \le n < (lo+1)^2$, because $lo < hi \le lo + 1$ gives $hi = lo + 1$.

The sequence rule joins steps 5, 4 and 6. For total correctness, use the variant $t = hi - lo$: step 3 shows $lo < mid < hi$, so each branch makes $hi - lo$ smaller, and $I \wedge B$ implies $t \ge 2 \ge 0$.

**A proof outline.** A full derivation is long, so proofs are usually written as a *proof outline*: the program with a condition between each two statements, so that each adjacent pair is an instance of a rule or a side condition. Gries (1981) uses this form throughout. The derivation above has this outline for the loop body:

```
{ I ∧ hi − lo > 1 }
mid ← lo + ⌊(hi − lo)/2⌋
{ I ∧ lo < mid < hi }
if mid · mid ≤ n then { 0 ≤ mid < hi ∧ mid² ≤ n < hi² } lo ← mid
                 else { 0 ≤ lo < mid ∧ lo² ≤ n < mid² } hi ← mid
{ I }
```

**A rule that is not sound.** Suppose a rule allowed $\{P\}\ x \leftarrow E\ \{P \wedge x = E\}$. Take $P$ to be $\mathit{true}$ and the command $x \leftarrow x + 1$. The rule gives $\{\mathit{true}\}\ x \leftarrow x + 1\ \{x = x + 1\}$, and by consequence $\{\mathit{true}\}\ x \leftarrow x + 1\ \{\mathit{false}\}$. But the command always stops, so this triple is false. A correct forward rule must name the old value: $\{P\}\ x \leftarrow E\ \{\exists x_0 : P[x_0/x] \wedge x = E[x_0/x]\}$.

**An invariant that is true but too weak.** For ISQRT, the condition $0 \le lo < hi$ is kept by the loop body. With it, the loop rule gives only $0 \le lo < hi \wedge hi - lo \le 1$ at exit, so the end step fails: nothing relates $lo$ to $n$. A useful invariant must be strong enough to give the postcondition at exit, and weak enough to hold at the start.

## Where it is used

- **Proofs by hand.** Textbook proofs of correctness, such as the loop invariant proofs in CLRS, are informal Hoare logic: the step is the premise of the loop rule, and the start and the exit are the side conditions of the rule of consequence around it. See [loop invariant](/loop-invariant/).
- **Program verifiers.** Tools such as Dafny, Why3, Boogie and Frama-C take a program with its pre- and postconditions and loop invariants. They compute the side conditions of the rules, by [weakest precondition](/weakest-precondition/) calculations, and send them to an automatic prover. See [program verification](/program-verification/).
- **Program derivation.** Dijkstra and Gries use the rules backwards, to build a program from its specification: choose the invariant first, then the guard and the body that keep it.
- **Extensions.** The same pattern of one rule for each construct is the base of later logics: [separation logic](/separation-logic/) for pointers, rules for concurrent programs (Owicki and Gries, 1976), and logics for probabilistic programs. Apt (1981) surveys the first decade of this work.
- **Limits.** By [Rice's theorem](/rice-theorem/), no algorithm decides whether a triple is true. Hoare logic moves the problem to the choice of invariants and to proofs in arithmetic, but it does not remove it.

## References
