---
tag: 84D73X
kind: definition
slug: gelfond-lifschitz-reduct
name: Gelfond-Lifschitz reduct
aliases:
- GL reduct
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: The reduct of a normal program by a set of atoms M deletes the rules blocked by M and the negative literals in the rest. The result has no negation, so it has a least model.
prereqs: [negation-as-failure, logic-programming, horn-sat]
see_also: [stable-model-semantics, alternating-fixpoint, well-founded-semantics, strong-equivalence, horn-sat-forward-chaining, smodels-algorithm, disjunctive-logic-program, answer-set-programming]
sources:
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of the transformation of a program by a set of atoms
  - paper: doi:10.1016/0022-0000(93)90024-Q
    title: Allen Van Gelder, The alternating fixpoint of logic programs with negation, Journal of Computer and System Sciences 47(1), 185 to 221 (1993)
    locator: the antimonotone operator built from the reduct
  - book: isbn:9783030246570
    title: Vladimir Lifschitz, Answer Set Programming, Springer (2019)
    locator: the chapter on the reduct and stable models of propositional programs
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the linear-time computation of the least model of a Horn program
---

The Gelfond-Lifschitz reduct is the program transformation at the center of the [stable model semantics](/stable-model-semantics/). Given a ground normal program $P$ and a candidate set $M$ of true atoms, it fixes the meaning of every $\mathit{not}$ by $M$ and returns a program without negation. Gelfond and Lifschitz (1988) defined it, and called $M$ stable when the least model of the reduct is $M$ again. This page is about the transformation and its properties; the semantics built on it is on the stable model page, and the [alternating fixpoint](/alternating-fixpoint/) uses the same operator to compute the [well-founded model](/well-founded-semantics/).

## Definition

Let $P$ be a ground normal program and $M$ a set of atoms. The *reduct* $P^M$ is obtained from $P$ in two steps.

1. Delete each rule that has a negative literal $\mathit{not}\ c$ with $c \in M$.
2. Delete all negative literals from the remaining rules.

So a rule $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$ gives the rule $h \leftarrow b_1, \ldots, b_m$ in $P^M$ if no $c_j$ is in $M$, and nothing otherwise. The reduct is a definite program, so it has a least model $\mathrm{lm}(P^M)$, which forward chaining computes in time linear in the size of $P$ ([Horn satisfiability](/horn-sat-forward-chaining/), Dowling and Gallier 1984). Write $\Gamma_P(M) = \mathrm{lm}(P^M)$.

$M$ is a *stable model* of $P$ when $\Gamma_P(M) = M$.

For a non-ground program, the reduct is taken of its ground instance over the [Herbrand universe](/herbrand-universe/).

## Examples and non-examples

Take the program

```text
p ← not q.
q ← not p.
r ← p, not s.
```

| $M$ | $P^M$ | $\mathrm{lm}(P^M)$ | stable |
|---|---|---|---|
| $\emptyset$ | $p.\ q.\ r \leftarrow p.$ | $\{p, q, r\}$ | no |
| $\{p\}$ | $p.\ r \leftarrow p.$ | $\{p, r\}$ | no |
| $\{q\}$ | $q.\ r \leftarrow p.$ | $\{q\}$ | yes |
| $\{p, r\}$ | $p.\ r \leftarrow p.$ | $\{p, r\}$ | yes |
| $\{p, q\}$ | $r \leftarrow p.$ | $\emptyset$ | no |

The candidate $\{p\}$ is not stable: under it the rules also derive $r$, and $r \notin \{p\}$. The candidate $\{p, q\}$ blocks both rules for $p$ and $q$, so it supports nothing. The stable models are $\{q\}$ and $\{p, r\}$.

- **Definite program.** If $P$ has no negation, $P^M = P$ for every $M$, and the only stable model is the least model.
- **Self-blocking rule.** For $\{p \leftarrow \mathit{not}\ p\}$, $\Gamma(\emptyset) = \{p\}$ and $\Gamma(\{p\}) = \emptyset$. No set is a fixpoint.
- **Non-example.** Deleting only the negative literals, without first deleting the blocked rules, is not the reduct: on $\{p \leftarrow \mathit{not}\ p\}$ it would make $p$ a fact for every $M$.

## Related definitions

- **Antimonotonicity.** If $M \subseteq N$, then $P^N \subseteq P^M$, so $\Gamma_P(N) \subseteq \Gamma_P(M)$. Hence $\Gamma_P^2$ is monotone, and its least and greatest fixpoints give the true and the not-false atoms of the [well-founded model](/well-founded-semantics/) (Van Gelder 1993). This is the [alternating fixpoint](/alternating-fixpoint/).
- **Reduct of a formula.** For a [disjunctive program](/disjunctive-logic-program/), the same reduct gives a positive disjunctive program, and $M$ is an answer set when it is a minimal model of $P^M$. For arbitrary propositional formulas, Ferraris (2005) defined a reduct that replaces each maximal subformula false in $M$ by $\bot$.
- **SE-models.** The pairs $(X, Y)$ with $X \subseteq Y$, $Y \models P$ and $X \models P^Y$ characterize [strong equivalence](/strong-equivalence/).
- **Stability check.** Testing whether a given $M$ is stable takes linear time: build $P^M$ and compute its least model. To decide whether a stable model exists is [NP-complete](/stable-model-np-completeness/), because the candidate $M$ must be guessed.

## References
