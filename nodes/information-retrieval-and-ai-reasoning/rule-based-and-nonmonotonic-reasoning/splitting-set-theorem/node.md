---
tag: ED99PW
kind: theorem
slug: splitting-set-theorem
name: Splitting set theorem
aliases:
- Lifschitz-Turner splitting
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: If a set U of atoms contains every body atom of each rule whose head is in U, the stable models of a program are the stable models of its U part, each extended by the stable models of the rest.
prereqs: [stable-model-semantics, stratified-logic-program]
see_also: [strong-equivalence, answer-set-programming, gelfond-lifschitz-reduct, strongly-connected-components, topological-sort, answer-set-grounding, disjunctive-logic-program, fages-theorem]
sources:
  - paper: "Vladimir Lifschitz and Hudson Turner, Splitting a logic program, in Logic Programming: Proceedings of the Eleventh International Conference on Logic Programming, MIT Press, 23 to 37 (1994)"
    locator: the definitions of splitting sets and partial evaluation, the splitting set theorem and the splitting sequence theorem
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models and the result for stratified programs
  - book: isbn:9783030246570
    title: Vladimir Lifschitz, Answer Set Programming, Springer (2019)
    locator: the section on splitting and its use in generate and test programs
---

The splitting set theorem of Lifschitz and Turner (1994) breaks the computation of [stable models](/stable-model-semantics/) into parts. If a set $U$ of atoms is closed in one direction, so that the rules that define atoms of $U$ mention only atoms of $U$, then the program splits into a bottom part about $U$ and a top part about the rest. Each stable model of the whole program is a stable model of the bottom, extended by a stable model of the top in which the atoms of $U$ have been replaced by their values. The theorem is the general form of the layer-by-layer evaluation of [stratified programs](/stratified-logic-program/), and it is the standard tool to prove that an answer set program does what it should.

## Statement

Let $P$ be a ground normal program over the atoms $A$. For a rule $r = h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$, write $\mathrm{head}(r) = h$, $\mathrm{pos}(r) = \{b_1, \ldots, b_m\}$ and $\mathrm{neg}(r) = \{c_1, \ldots, c_k\}$.

- A set $U \subseteq A$ is a *splitting set* for $P$ if, for every rule $r$ of $P$ with $\mathrm{head}(r) \in U$, also $\mathrm{pos}(r) \cup \mathrm{neg}(r) \subseteq U$.
- The *bottom* $b_U(P)$ is the set of rules of $P$ whose head is in $U$, and the *top* is $t_U(P) = P \setminus b_U(P)$.
- For a set $X \subseteq U$, the *partial evaluation* $e_U(t_U(P), X)$ is obtained from the top as follows. Delete each rule $r$ with $\mathrm{pos}(r) \cap U \not\subseteq X$ or $\mathrm{neg}(r) \cap X \neq \emptyset$. From each remaining rule, delete all body literals whose atom is in $U$.

**Theorem** (Lifschitz and Turner 1994). Let $U$ be a splitting set for $P$. A set $M \subseteq A$ is a stable model of $P$ if and only if $M = X \cup Y$, where $X$ is a stable model of $b_U(P)$ and $Y$ is a stable model of $e_U(t_U(P), X)$.

Then $X = M \cap U$ and $Y = M \setminus U$, because the heads of the bottom are in $U$ and those of the top are not. Lifschitz and Turner proved the theorem for programs with disjunction and strong negation; there a splitting set must contain all atoms of a rule as soon as it contains one atom of its head. They also proved a splitting sequence theorem, for a monotone sequence of splitting sets, possibly transfinite.

## In plain words

Some parts of a program only feed others. The rules that decide which items are chosen may never look at the rules that check the choice, while the checks look at the choices. The theorem says that such a program can be solved in two rounds. First solve the part that does not look outside itself, and list its solutions. Then, for each solution, put its values into the rest, which becomes simpler, and solve that. Each combination of a first-round solution with a second-round solution is a solution of the whole program, and no solution is lost. The condition is that the first part really does not look at the second, not even through a negation.

## Proof

The proof is from Lifschitz and Turner (1994), here for normal programs. It uses the [reduct](/gelfond-lifschitz-reduct/) $P^M$ and its least model $\mathrm{lm}(P^M)$. Fix $M \subseteq A$, and let $X = M \cap U$, $Y = M \setminus U$, $B = b_U(P)$ and $E = e_U(t_U(P), X)$. Let $N = \mathrm{lm}(P^M)$.

**Lemma 1.** $N \cap U = \mathrm{lm}(B^X)$.

All atoms of the rules of $B$ are in $U$, so $B^M = B^X$, and $B^X \subseteq P^M$. Hence $\mathrm{lm}(B^X) \subseteq N$. Conversely, the set $\mathrm{lm}(B^X) \cup (A \setminus U)$ is closed under $P^M$: a rule with head in $U$ is in $B^X$ and has its body in $U$, so if its body is in the set, it is in $\mathrm{lm}(B^X)$ and so is its head; a rule with head outside $U$ puts its head in $A \setminus U$. So $N \subseteq \mathrm{lm}(B^X) \cup (A \setminus U)$, and $N \cap U \subseteq \mathrm{lm}(B^X)$.

**Lemma 2.** If $N \cap U = X$, then $N \setminus U = \mathrm{lm}(E^Y)$.

A rule $r$ of the top gives a rule of $P^M$ when $\mathrm{neg}(r) \cap M = \emptyset$, that is, when $\mathrm{neg}(r) \cap X = \emptyset$ and $\mathrm{neg}(r) \cap Y = \emptyset$. It gives a rule of $E^Y$ when, in addition, $\mathrm{pos}(r) \cap U \subseteq X$, and that rule is $\mathrm{head}(r) \leftarrow \mathrm{pos}(r) \setminus U$. First, $X \cup \mathrm{lm}(E^Y)$ is closed under $P^M$. The bottom rules of $P^M$ are the rules of $B^X$, and $X = \mathrm{lm}(B^X)$ by Lemma 1, so they keep inside $X$. A top rule of $P^M$ with its body in $X \cup \mathrm{lm}(E^Y)$ has $\mathrm{pos}(r) \cap U \subseteq X$, so it gives a rule of $E^Y$ with body in $\mathrm{lm}(E^Y)$, and its head is in $\mathrm{lm}(E^Y)$. So $N \setminus U \subseteq \mathrm{lm}(E^Y)$. Second, $N \setminus U$ is closed under $E^Y$. If a rule of $E^Y$ from $r$ has $\mathrm{pos}(r) \setminus U \subseteq N$, then $\mathrm{pos}(r) \subseteq N$, because $\mathrm{pos}(r) \cap U \subseteq X \subseteq N$. The rule $\mathrm{head}(r) \leftarrow \mathrm{pos}(r)$ is in $P^M$, so its head is in $N \setminus U$. So $\mathrm{lm}(E^Y) \subseteq N \setminus U$.

**The theorem.** If $M$ is stable, then $N = M$. By Lemma 1, $X = \mathrm{lm}(B^X)$, so $X$ is a stable model of $B$. Then Lemma 2 applies and gives $Y = \mathrm{lm}(E^Y)$, so $Y$ is a stable model of $E$. Conversely, let $X$ be a stable model of $B$ and $Y$ one of $E$, and $M = X \cup Y$. By Lemma 1, $N \cap U = \mathrm{lm}(B^X) = X$. By Lemma 2, $N \setminus U = \mathrm{lm}(E^Y) = Y$. So $N = M$, and $M$ is stable.

**A check by hand.** Take

```text
a ← not b.    b ← not a.    c ← a.    d ← not c.
```

and $U = \{a, b\}$. The rules for $a$ and $b$ mention only $a$ and $b$, so $U$ is a splitting set. The bottom $\{a \leftarrow \mathit{not}\ b,\ b \leftarrow \mathit{not}\ a\}$ has the stable models $\{a\}$ and $\{b\}$. For $X = \{a\}$, the partial evaluation of the top is $\{c,\ d \leftarrow \mathit{not}\ c\}$, with the stable model $\{c\}$. For $X = \{b\}$, the rule $c \leftarrow a$ is deleted and the evaluation is $\{d \leftarrow \mathit{not}\ c\}$, with the stable model $\{d\}$. So the stable models of the program are $\{a, c\}$ and $\{b, d\}$.

## Consequences

- **Stratified programs.** The strata of a [stratified program](/stratified-logic-program/) form a chain of splitting sets. Each layer, after partial evaluation, is a definite program, so by the splitting sequence theorem the program has exactly one stable model, its standard model.
- **Generate, define and test.** An answer set program usually has a part that generates candidates, a part that defines auxiliary atoms and constraints that test. When the atoms of the generating part form a splitting set, the stable models are the candidates for which the rest has a stable model. Constraints in the top only remove candidates. This is how correctness proofs of [answer set programs](/answer-set-programming/) are usually written.
- **Evaluation by components.** In the dependency graph with positive and negative edges, a set of atoms that contains every atom its atoms depend on is a splitting set. So a [topological order](/topological-sort/) of the [strongly connected components](/strongly-connected-components/), with each component after the components it depends on, gives a splitting sequence. Grounders and solvers use this order to evaluate the stratified part of a program completely before search.
- **Adding a top part.** If new rules have heads outside $U$ and the old rules mention only $U$, every stable model of the new program agrees on $U$ with a stable model of the old one. If the new rules are definite, each old stable model extends to exactly one new one.

## Tightness

The condition on $U$ cannot be dropped. Take $P = \{a \leftarrow \mathit{not}\ b,\ b \leftarrow \mathit{not}\ a\}$ and $U = \{a\}$, which is not a splitting set, since the rule for $a$ mentions $b \notin U$. The rules with head in $U$ are $\{a \leftarrow \mathit{not}\ b\}$; $b$ has no rule there, so the only stable model of this part is $\{a\}$. Then the rule $b \leftarrow \mathit{not}\ a$ is deleted, and the procedure gives only $\{a\}$. The stable model $\{b\}$ of $P$ is lost.

The condition is one-sided. Rules of the top can mention atoms of $U$ in any way, positively or negatively; only the bottom must not look up. Every program has the trivial splitting sets $\emptyset$ and $A$, and the theorem is useful only when a proper splitting set exists. A program whose atoms all depend on each other, such as $\{a \leftarrow \mathit{not}\ b,\ b \leftarrow \mathit{not}\ a\}$, has no proper splitting set.

## History

Lifschitz and Turner presented the splitting set theorem and the splitting sequence theorem at the International Conference on Logic Programming in 1994. Their setting includes disjunctive programs with strong negation. The theorem became a basic tool in the theory of answer set programming, and later work extended it to arbitrary propositional theories and first-order programs, and to modules that depend on each other in both directions.

## References
