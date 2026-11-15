---
tag: 9NTS8A
kind: definition
slug: well-founded-semantics
name: Well-founded semantics
aliases:
- Van Gelder-Ross-Schlipf semantics
- WFS
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: The well-founded semantics gives every normal program one three-valued model. Atoms are true when forced by the rules, false when only unfounded support exists, and undefined otherwise.
prereqs: [negation-as-failure, stratified-logic-program, fixed-point]
see_also: [alternating-fixpoint, slg-resolution, stable-model-semantics, gelfond-lifschitz-reduct, knaster-tarski-theorem, datalog, circuit-value-problem, clark-completion]
sources:
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: the definitions of unfounded sets, the greatest unfounded set and the operator W_P, and the relation to stratified programs and stable models
  - paper: doi:10.1016/0022-0000(93)90024-Q
    title: Allen Van Gelder, The alternating fixpoint of logic programs with negation, Journal of Computer and System Sciences 47(1), 185 to 221 (1993)
    locator: the characterization of the well-founded model by the alternating fixpoint
  - paper: doi:10.1145/227595.227597
    title: Weidong Chen and David S. Warren, Tabled evaluation with delaying for general logic programs, Journal of the ACM 43(1), 20 to 74 (1996)
    locator: the goal-directed computation of the well-founded model by SLG resolution
  - paper: "Krzysztof R. Apt and Roland N. Bol, Logic programming and negation: a survey, Journal of Logic Programming 19/20, 9 to 71 (1994)"
    locator: the section on the well-founded semantics
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: the complexity results for the well-founded semantics
---

The well-founded semantics assigns to every normal logic program a single three-valued model, the well-founded model. An atom is true if the rules force it, false if every way to derive it depends on atoms that are false or on itself, and undefined if neither holds. Van Gelder, Ross and Schlipf (1991) defined it with unfounded sets. It extends the standard model of [stratified programs](/stratified-logic-program/) to all programs, and it is more cautious than the [stable model semantics](/stable-model-semantics/): it never picks between alternatives. This page gives the definition and its properties. The two ways to compute it are on their own pages: the bottom-up [alternating fixpoint](/alternating-fixpoint/) and the goal-directed [SLG resolution](/slg-resolution/).

## Definition

Let $P$ be a ground normal program over the atoms $A$. A *partial interpretation* is a pair $(T, F)$ of disjoint sets of atoms, the true and the false ones; the other atoms are undefined. A positive literal $b$ is true in $(T, F)$ if $b \in T$ and false if $b \in F$; a literal $\mathit{not}\ c$ is true if $c \in F$ and false if $c \in T$. Pairs are ordered by $(T, F) \le (T', F')$ if $T \subseteq T'$ and $F \subseteq F'$.

A set $X \subseteq A$ is *unfounded* with respect to $(T, F)$ if each rule with its head in $X$ has

1. a body literal that is false in $(T, F)$, or
2. a positive body atom in $X$.

The union of unfounded sets is unfounded, so there is a *greatest unfounded set* $U_P(T, F)$. Let $T_P(T, F)$ be the set of heads of the rules whose body is true in $(T, F)$. The operator

$$W_P(T, F) = \big(T_P(T, F),\ U_P(T, F)\big)$$

is monotone, and the *well-founded model* is its least [fixed point](/fixed-point/), reached by iterating from $(\emptyset, \emptyset)$. The model is *total* if every atom is true or false. For programs with variables, $P$ is the ground instance and the iteration can be transfinite.

Van Gelder (1993) gave an equivalent form with the [reduct](/gelfond-lifschitz-reduct/). Let $\Gamma(M) = \mathrm{lm}(P^M)$. Since $\Gamma$ is antimonotone, $\Gamma^2$ is monotone. If $K$ is the least fixed point of $\Gamma^2$ and $U = \Gamma(K)$, then the true atoms are $K$ and the false atoms are $A \setminus U$.

## Examples and non-examples

Take the program

```text
a ← not b.     b ← not a.
c ← not c.
d ← not e.     e ← e.
f ← d, not c.
g ← a.
```

The iteration of $W_P$ from $(\emptyset, \emptyset)$ is

| step | true | false |
|---|---|---|
| 0 | $\emptyset$ | $\emptyset$ |
| 1 | $\emptyset$ | $\{e\}$ |
| 2 | $\{d\}$ | $\{e\}$ |
| 3 | $\{d\}$ | $\{e\}$ |

In step 1, $\{e\}$ is unfounded because its only rule needs $e$ itself. In step 2, $d$ is true since $\mathit{not}\ e$ is true. The atoms $a, b, c, f, g$ stay undefined: $a$ and $b$ block each other, $c$ blocks itself, and $f$ and $g$ depend on them. This program has no stable model, because of $c \leftarrow \mathit{not}\ c$, while its well-founded model exists and says something about $d$ and $e$.

- **Stratified program.** For $p \leftarrow \mathit{not}\ q$, the model is total: $p$ true, $q$ false. This is the standard model.
- **Positive loop.** $p \leftarrow p$ makes $p$ false, since $\{p\}$ is unfounded. The [completion](/clark-completion/) allows $p$ to be true.
- **Win game.** With $\mathit{win}(x) \leftarrow \mathit{move}(x, y), \mathit{not}\ \mathit{win}(y)$, a position is true if it is won, false if it is lost, and undefined if the play can be drawn by moving around a cycle.
- **Not the intersection of stable models.** For $a \leftarrow \mathit{not}\ b$, $b \leftarrow \mathit{not}\ a$, $c \leftarrow a$, $c \leftarrow b$, the atom $c$ is in both stable models but undefined in the well-founded model.

## Related definitions

- **Stable models.** Every atom true in the well-founded model is in every stable model, and every false atom is in none. If the well-founded model is total, it is the unique stable model (Van Gelder, Ross and Schlipf 1991). The converse fails: $\{p \leftarrow \mathit{not}\ p,\ p \leftarrow \mathit{not}\ q,\ q \leftarrow \mathit{not}\ p\}$ has the unique stable model $\{p\}$, but in its well-founded model $p$ and $q$ are undefined.
- **Three-valued stable models.** Przymusinski showed that the well-founded model is the least three-valued stable model, which links the two semantics in one framework.
- **Complexity.** The well-founded model of a finite ground program can be computed in polynomial time, in $O(n \cdot s)$ steps for $n$ atoms and program size $s$ by the [alternating fixpoint](/alternating-fixpoint/). For [Datalog](/datalog/) with negation under this semantics, the data complexity is P-complete, by a reduction from the [circuit value problem](/circuit-value-problem/).
- **Systems.** XSB Prolog computes the well-founded model goal by goal with [SLG resolution](/slg-resolution/), and answer set solvers use it to simplify a program before search.

## References
