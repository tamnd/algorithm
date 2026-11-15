---
tag: DBCEQ3
kind: definition
slug: disjunctive-logic-program
name: Disjunctive logic program
aliases:
- disjunctive answer set program
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: A program whose rule heads are disjunctions of atoms, with answer sets defined as minimal models of the reduct.
prereqs: [stable-model-semantics, gelfond-lifschitz-reduct]
see_also: [disjunctive-asp-sigma2-completeness, choice-rule, answer-set-programming, stable-model-np-completeness, circumscription, strongly-connected-components, logic-programming]
sources:
  - paper: doi:10.1007/bf03037169
    title: Michael Gelfond and Vladimir Lifschitz, Classical negation in logic programs and disjunctive databases, New Generation Computing 9(3-4), 365 to 385 (1991)
    locator: the definition of answer sets for disjunctive programs with classical negation, by the reduct and minimal models
  - paper: doi:10.1007/bf01530761
    title: Rachel Ben-Eliyahu and Rina Dechter, Propositional semantics for disjunctive logic programs, Annals of Mathematics and Artificial Intelligence 12(1-2), 53 to 87 (1994)
    locator: the definition of head-cycle-free programs and the proof that shifting preserves their answer sets
  - paper: doi:10.1007/bf01536399
    title: Thomas Eiter and Georg Gottlob, On the computational cost of disjunctive logic programming, propositional case, Annals of Mathematics and Artificial Intelligence 15(3-4), 289 to 323 (1995)
    locator: the complexity of answer sets of propositional disjunctive programs
  - paper: doi:10.1145/1149114.1149117
    title: Nicola Leone, Gerald Pfeifer, Wolfgang Faber, Thomas Eiter, Georg Gottlob, Simona Perri and Francesco Scarcello, The DLV system for knowledge representation and reasoning, ACM Transactions on Computational Logic 7(3) (2006)
    locator: the language of disjunctive programs supported by DLV
---

A disjunctive logic program allows rules such as $a \vee b \leftarrow c$, which say that when $c$ holds, at least one of $a$ and $b$ holds, without saying which. Gelfond and Lifschitz (1991) gave these programs a semantics that extends [stable models](/stable-model-semantics/): an answer set is a minimal model of the reduct. Disjunction expresses incomplete information directly, and it makes the existence of an answer set [$\Sigma_2^p$-complete](/disjunctive-asp-sigma2-completeness/), one level above normal programs.

## Definition

Let $A$ be a finite set of atoms. A *disjunctive rule* is an expression

$$a_1 \vee \cdots \vee a_k \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$$

with atoms $a_i, b_i, c_j \in A$, $k \geq 1$ and $m, n \geq 0$. The *head* is $H = \{a_1, \ldots, a_k\}$, and the body has the positive part $B^+ = \{b_1, \ldots, b_m\}$ and the negative part $B^- = \{c_1, \ldots, c_n\}$. A *disjunctive program* is a finite set of disjunctive rules. It is *normal* if every head has one atom and *positive* if every $B^-$ is empty.

A set $M \subseteq A$ is a *model* of a positive program $Q$ if for each rule of $Q$ with $B^+ \subseteq M$, the head meets $M$. A model is *minimal* if no proper subset of it is a model. A positive disjunctive program can have several minimal models, unlike a positive normal program, which has a least model.

For a disjunctive program $P$ and $M \subseteq A$, the *reduct* $P^M$ deletes every rule with $B^- \cap M \neq \emptyset$ and deletes the negative body of the other rules. $M$ is an *answer set* of $P$ if $M$ is a minimal model of $P^M$ (Gelfond and Lifschitz 1991). For a normal program, this is the stable model condition, since the least model is the only minimal model.

*Head cycles.* The positive dependency graph of $P$ has an edge from $b$ to $a$ for each rule with $a \in H$ and $b \in B^+$. $P$ is *head-cycle-free* if no rule has two distinct head atoms in the same [strongly connected component](/strongly-connected-components/) of this graph (Ben-Eliyahu and Dechter 1994). *Shifting* replaces each rule by the $k$ normal rules

$$a_i \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n, \mathit{not}\ a_1, \ldots, \mathit{not}\ a_{i-1}, \mathit{not}\ a_{i+1}, \ldots, \mathit{not}\ a_k.$$

For head-cycle-free programs, shifting preserves the answer sets.

## Examples and non-examples

- **One disjunction.** The program $a \vee b \leftarrow$ has the answer sets $\{a\}$ and $\{b\}$. The set $\{a, b\}$ is a model of the reduct but not a minimal one, so it is not an answer set.
- **Disjunction is not exclusive.** The program $a \vee b \leftarrow$, $a \leftarrow$, $b \leftarrow a$ has the single answer set $\{a, b\}$: both head atoms are true because other rules force them. Without the fact $a \leftarrow$, the program $a \vee b \leftarrow$, $b \leftarrow a$ has the single answer set $\{b\}$.
- **Disjunction with negation.** The program $a \vee b \leftarrow$, $a \leftarrow \mathit{not}\ b$ has the answer sets $\{a\}$ and $\{b\}$. For $M = \{b\}$ the reduct is $a \vee b \leftarrow$, whose minimal models are $\{a\}$ and $\{b\}$, and $M$ is one of them.
- **A head cycle.** The program $a \vee b \leftarrow$, $a \leftarrow b$, $b \leftarrow a$ has the single answer set $\{a, b\}$. The atoms $a$ and $b$ form a cycle and are both in the head of the first rule, so the program is not head-cycle-free. Its shifted program $a \leftarrow \mathit{not}\ b$, $b \leftarrow \mathit{not}\ a$, $a \leftarrow b$, $b \leftarrow a$ has no answer set.
- **Non-example: a choice rule.** The [choice rule](/choice-rule/) $\{a, b\} \leftarrow$ has the four answer sets $\emptyset, \{a\}, \{b\}, \{a, b\}$. A choice rule does not ask for minimality and is not a disjunctive rule.
- **Non-example: classical disjunction.** In classical logic, $a \vee b$ has the three models $\{a\}, \{b\}, \{a, b\}$. The answer set semantics keeps only the minimal ones, so $a \vee b \leftarrow$ does not entail $\neg(a \wedge b)$ classically but does make $a \wedge b$ false in every answer set.
- **Non-example: a constraint.** The rule $\leftarrow a, b$ has an empty head, so it is not a disjunctive rule with $k \geq 1$. It can be written $f \leftarrow a, b, \mathit{not}\ f$ with a new atom $f$.

## Related definitions

- **Normal program and stable model.** A disjunctive program with $k = 1$ in every rule is a normal program, and its answer sets are its [stable models](/stable-model-semantics/). Existence is NP-complete for normal programs ([Marek and Truszczyński](/stable-model-np-completeness/)) and $\Sigma_2^p$-complete for disjunctive programs.
- **Minimal models and circumscription.** For a positive disjunctive program, the answer sets are the minimal models. Reasoning over minimal models is also the propositional core of [circumscription](/circumscription/).
- **Extended disjunctive program.** Gelfond and Lifschitz (1991) also allow classical negation $\neg a$ in heads and bodies. For the consistent answer sets, treat $\neg a$ as a new atom $a'$ and add the constraint $\leftarrow a, a'$, so this extension adds no complexity.
- **Disjunctive solvers.** DLV (Leone et al. 2006) computes answer sets of disjunctive programs with a candidate search and a separate minimality check, which matches the two levels of the complexity.

## References
