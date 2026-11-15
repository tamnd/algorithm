---
tag: S09RSH
kind: definition
slug: choice-rule
name: Choice rule
aliases:
- cardinality constraint rule
- weight constraint rule
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: An ASP rule whose head lets a solver include any subset of a set of atoms, within lower and upper bounds, when the body holds.
prereqs: [answer-set-programming, gelfond-lifschitz-reduct]
see_also: [stable-model-semantics, smodels-algorithm, answer-set-grounding, conflict-driven-answer-set-solving, disjunctive-logic-program, negation-as-failure]
sources:
  - paper: doi:10.1016/s0004-3702(02)00187-x
    title: Patrik Simons, Ilkka Niemelä and Timo Soininen, Extending and implementing the stable model semantics, Artificial Intelligence 138(1-2), 181 to 234 (2002)
    locator: the definitions of choice rules, cardinality constraints and weight constraints, and the reduct that defines their stable models
  - paper: doi:10.1023/a:1018930122475
    title: Ilkka Niemelä, Logic programs with stable model semantics as a constraint programming paradigm, Annals of Mathematics and Artificial Intelligence 25(3-4), 241 to 273 (1999)
    locator: the use of choice and cardinality constructs to encode NP search problems
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: the introduction of choice rules and cardinality constraints in the input language
---

A choice rule is the "guess" part of most [answer set programs](/answer-set-programming/). When its body holds, it lets an answer set contain any subset of its head atoms, and the optional bounds limit the size of that subset. It was introduced with the smodels system and its semantics is due to Simons, Niemelä and Soininen (2002). A choice rule can be rewritten as normal rules with new atoms, so it adds convenience but no expressive power over [normal programs](/stable-model-semantics/).

## Definition

Let $A$ be a set of atoms. A *choice rule* is an expression

$$\{a_1, \ldots, a_k\} \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$$

with atoms $a_i, b_i, c_j \in A$ and $k \geq 1$. Write $B^+ = \{b_1, \ldots, b_m\}$, $B^- = \{c_1, \ldots, c_n\}$ and $H = \{a_1, \ldots, a_k\}$. A *cardinality rule* with bounds is

$$l\ \{a_1, \ldots, a_k\}\ u \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$$

with integers $0 \leq l \leq u \leq k$. A missing $l$ means $0$ and a missing $u$ means $k$.

Let $P$ be a finite ground program of normal rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$, constraints and choice rules, and let $M \subseteq A$. The *reduct* $P^M$ is the positive program obtained as follows.

1. Delete every rule and constraint whose $B^-$ meets $M$.
2. In the other normal rules, delete the negative literals, as in the [Gelfond-Lifschitz reduct](/gelfond-lifschitz-reduct/).
3. Replace each remaining choice rule by the rules $a \leftarrow b_1, \ldots, b_m$, one for each $a \in H \cap M$.

$M$ is an *answer set* of $P$ if $M$ is the least model of the positive part of $P^M$ and $M$ violates no constraint. For a cardinality rule, $M$ must also satisfy $l \leq |H \cap M| \leq u$ whenever $B^+ \subseteq M$ and $B^- \cap M = \emptyset$.

*Normal translation.* The choice rule above has the same answer sets, restricted to $A$, as the $2k$ normal rules

$$a_i \leftarrow b_1, \ldots, b_m, \mathit{not}\ \bar{a}_i, \qquad \bar{a}_i \leftarrow \mathit{not}\ a_i \qquad (1 \leq i \leq k),$$

where the $\bar{a}_i$ are new atoms and $B$ is the body. The upper bound becomes one constraint $\leftarrow B, a_{i_1}, \ldots, a_{i_{u+1}}$ for each set of $u + 1$ head atoms, and the lower bound becomes one constraint $\leftarrow B, \mathit{not}\ a_{i_1}, \ldots, \mathit{not}\ a_{i_{k-l+1}}$ for each set of $k - l + 1$ head atoms. This direct translation has $\binom{k}{u+1} + \binom{k}{k-l+1}$ constraints, so solvers handle the bounds natively or use counter atoms of polynomial size instead.

## Examples and non-examples

- **Free choice.** The program $\{a, b, c\} \leftarrow$ has $8$ answer sets, all subsets of $\{a, b, c\}$. For $M = \{a, c\}$, the reduct is $a \leftarrow$, $c \leftarrow$, whose least model is $M$.
- **Bounds.** The program $1\ \{a, b, c\}\ 2 \leftarrow$ has $6$ answer sets: $\{a\}, \{b\}, \{c\}, \{a, b\}, \{a, c\}, \{b, c\}$. The same answer sets come from $\{a, b, c\} \leftarrow$ with the constraints $\leftarrow a, b, c$ and $\leftarrow \mathit{not}\ a, \mathit{not}\ b, \mathit{not}\ c$.
- **Conditional choice.** The program $\{p\} \leftarrow q$, $q \leftarrow \mathit{not}\ r$ has the answer sets $\{q\}$ and $\{p, q\}$. For $M = \{p, q\}$, the reduct is $q \leftarrow$, $p \leftarrow q$, whose least model is $\{p, q\}$. The atom $p$ is never chosen without $q$.
- **Choice gives support to a cycle.** The program $\{a\} \leftarrow$, $b \leftarrow a$, $a \leftarrow b$ has the answer sets $\emptyset$ and $\{a, b\}$. Without the choice rule, the positive cycle alone gives only $\emptyset$, because nothing outside the cycle supports it.
- **Non-example: disjunction.** The disjunctive rule $a \vee b \leftarrow$ is not a choice rule. Its answer sets are $\{a\}$ and $\{b\}$, because a [disjunctive answer set](/disjunctive-logic-program/) must be a minimal model, while $\{a, b\} \leftarrow$ has the four answer sets $\emptyset, \{a\}, \{b\}, \{a, b\}$, and $1\ \{a, b\}\ 1 \leftarrow$ has $\{a\}$ and $\{b\}$.
- **Non-example: a choice is not a fact.** The rule $\{a\} \leftarrow$ does not make $a$ true. If no other rule mentions $a$, the answer sets with and without $a$ both exist. A program that needs $a$ in every answer set uses the fact $a \leftarrow$.
- **Non-example: unsupported atoms.** An atom in $M$ that is in the head of a choice rule whose body is false in $M$ is not justified by that rule. For example, $\{p\} \leftarrow q$ with no rule for $q$ has only the answer set $\emptyset$.

## Related definitions

- **Weight rule.** A weight constraint $l\ [a_1 = w_1, \ldots, a_k = w_k, \mathit{not}\ c_1 = v_1, \ldots]\ u$ counts the weights of the true literals instead of their number, and may contain negative literals. A cardinality constraint is the special case with all weights $1$. Simons, Niemelä and Soininen (2002) define the stable models of programs with weight constraints in heads and bodies with one reduct. A weight rule is more general than a choice rule, so the alias "weight constraint rule" names a larger class than this page.
- **Cardinality constraint in a body.** The literal $l\ \{a_1, \ldots, a_k\}\ u$ in a rule body is true in $M$ when $l \leq |\{a_1, \ldots, a_k\} \cap M| \leq u$. Unlike the head form, it only tests and never chooses.
- **Constraint.** A rule $\leftarrow B$ with an empty head removes every candidate in which $B$ holds. Choice rules generate and constraints test, which is the generate-and-test pattern of ASP.
- **Disjunctive rule.** A head $a_1 \vee \cdots \vee a_k$ asks for a minimal set of true head atoms. It raises the complexity of existence to $\Sigma_2^p$ ([Eiter and Gottlob](/disjunctive-asp-sigma2-completeness/)), while choice rules keep it in NP.

## References
