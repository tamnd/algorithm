---
tag: 9AF70E
kind: definition
slug: stable-model-semantics
name: Stable model semantics
aliases:
- Gelfond-Lifschitz semantics
- answer set semantics
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: A set of atoms is a stable model of a normal program when it equals the least model of the program's reduct by that set. A program can have no, one or many stable models.
prereqs: [gelfond-lifschitz-reduct, negation-as-failure]
see_also: [answer-set-programming, well-founded-semantics, fages-theorem, loop-formulas, splitting-set-theorem, strong-equivalence, stable-model-np-completeness, smodels-algorithm]
sources:
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models and the result for stratified programs
  - paper: "V. Wiktor Marek and Mirosław Truszczyński, Autoepistemic logic, Journal of the ACM 38(3), 588 to 619 (1991)"
    locator: the NP-completeness of the existence of a stable model
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: the relation between the well-founded model and the stable models, and the characterization by unfounded sets
  - book: isbn:9783030246570
    title: Vladimir Lifschitz, Answer Set Programming, Springer (2019)
    locator: the chapters on stable models of propositional programs and their properties
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: the chapter on the stable model semantics and the characterization by completion and loop formulas
---

The stable model semantics gives a normal logic program a set of intended models, the stable models. A candidate set $M$ of true atoms is stable when the program, with each $\mathit{not}\ c$ read as "$c \notin M$", derives exactly $M$. Gelfond and Lifschitz (1988) proposed it as a reading of [negation as failure](/negation-as-failure/) close to autoepistemic logic, and it became the basis of [answer set programming](/answer-set-programming/). The transformation it uses is defined on the [Gelfond-Lifschitz reduct](/gelfond-lifschitz-reduct/) page. This page gives the semantics, its main properties and its relation to the other readings of negation.

## Definition

Let $P$ be a ground normal program, with rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$. For a set $M$ of atoms, the reduct $P^M$ deletes each rule with some $c_j \in M$ and then deletes all negative literals. A set $M$ is a *stable model* (or *answer set*) of $P$ if

$$M = \mathrm{lm}(P^M),$$

where $\mathrm{lm}$ is the least model of a definite program. A program with variables has the stable models of its ground instance. A *constraint* $\leftarrow L_1, \ldots, L_k$ is written as $f \leftarrow L_1, \ldots, L_k, \mathit{not}\ f$ with a new atom $f$; it removes the stable models in which its body is true.

An equivalent form uses unfounded sets. A set $X$ is *unfounded* for $M$ if each rule with its head in $X$ has a positive body atom outside $M$ or in $X$, or a negative body literal $\mathit{not}\ c$ with $c \in M$. Then $M$ is stable if and only if $M$ is a model of $P$ and no nonempty subset of $M$ is unfounded for $M$. The atoms of a stable model are true for a reason that does not lean on themselves.

## Examples and non-examples

- **Two models.** $p \leftarrow \mathit{not}\ q$, $q \leftarrow \mathit{not}\ p$, $r \leftarrow p, \mathit{not}\ s$ has the stable models $\{q\}$ and $\{p, r\}$. The reduct by $\{p\}$ is $\{p,\ r \leftarrow p\}$, with least model $\{p, r\} \ne \{p\}$, so $\{p\}$ is not stable.
- **A constraint selects.** $p \leftarrow \mathit{not}\ q$, $q \leftarrow \mathit{not}\ p$, $f \leftarrow p, \mathit{not}\ f$ has the single stable model $\{q\}$. For $M = \{p\}$, the reduct contains $f \leftarrow p$, so $f$ is derived; for $M = \{p, f\}$, the rule for $f$ is deleted and $f$ is not derived.
- **No model.** $p \leftarrow \mathit{not}\ p$ has no stable model.
- **Self support is rejected.** $p \leftarrow p$ has the stable model $\emptyset$ only, although $\{p\}$ is a model of its [completion](/clark-completion/).
- **Not classical.** $p \leftarrow \mathit{not}\ q$ has the one stable model $\{p\}$, although the classical formula $q \vee p$ also has the minimal model $\{q\}$.
- **Graph coloring.** For each vertex $v$ and colors $1, 2, 3$, rules $c_i(v) \leftarrow \mathit{not}\ c_j(v), \mathit{not}\ c_k(v)$ with $\{i, j, k\} = \{1, 2, 3\}$, and a constraint $\leftarrow c_i(u), c_i(v)$ for each edge $uv$ and color $i$. The stable models are the proper 3-colorings.

## Related definitions

- **Properties.** Every stable model is a minimal model of $P$ and a supported model ($M = T_P(M)$, a model of the completion). No stable model is a proper subset of another. Adding a fact can remove stable models and create new ones, so the semantics is nonmonotonic.
- **Stratified programs.** A [stratified program](/stratified-logic-program/) has exactly one stable model, its standard model (Gelfond and Lifschitz 1988).
- **Well-founded semantics.** The atoms true in the [well-founded model](/well-founded-semantics/) are in every stable model, and the false ones are in none. The well-founded model can be weaker: for $a \leftarrow \mathit{not}\ b$, $b \leftarrow \mathit{not}\ a$, $c \leftarrow a$, $c \leftarrow b$, the atom $c$ is in both stable models but undefined in the well-founded model. If the well-founded model is total, it is the unique stable model.
- **Completion and loops.** For tight programs the stable models are the models of the completion ([Fages' theorem](/fages-theorem/)). In general they are the models of the completion that satisfy every [loop formula](/loop-formulas/) (Lin and Zhao).
- **Modularity.** The [splitting set theorem](/splitting-set-theorem/) computes stable models layer by layer, and [strong equivalence](/strong-equivalence/) says when one part of a program can be replaced by another.
- **Complexity.** To decide whether a finite ground program has a stable model is [NP-complete](/stable-model-np-completeness/) (Marek and Truszczyński 1991). Solvers such as [Smodels](/smodels-algorithm/) and [clasp](/conflict-driven-answer-set-solving/) search for them.
- **Extensions.** [Disjunctive programs](/disjunctive-logic-program/) use minimal models of the reduct, and [choice rules](/choice-rule/) and strong negation are part of the answer set language.

## References
