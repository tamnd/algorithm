---
tag: 9CD50Z
kind: theorem
slug: disjunctive-asp-sigma2-completeness
name: Sigma2P-completeness of disjunctive answer sets
aliases:
- Eiter-Gottlob disjunctive complexity
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: research
summary: Deciding whether a propositional disjunctive logic program has an answer set is Sigma2P-complete.
prereqs: [disjunctive-logic-program, polynomial-hierarchy, qbf, stable-model-np-completeness]
see_also: [answer-set-programming, stable-model-semantics, gelfond-lifschitz-reduct, circumscription, default-logic-complexity, autoepistemic-logic, consistency-based-diagnosis, conflict-driven-answer-set-solving]
sources:
  - paper: doi:10.1007/bf01536399
    title: Thomas Eiter and Georg Gottlob, On the computational cost of disjunctive logic programming, propositional case, Annals of Mathematics and Artificial Intelligence 15(3-4), 289 to 323 (1995)
    locator: the results on the stable model semantics of propositional disjunctive programs, existence, brave and cautious reasoning, and model checking
  - paper: "Thomas Eiter and Georg Gottlob, Complexity results for disjunctive logic programming and application to nonmonotonic logics, in Dale Miller (ed.), Logic Programming: Proceedings of the 1993 International Symposium (ILPS 1993), MIT Press, 266 to 278 (1993)"
    locator: the conference version of the complexity results
  - paper: doi:10.1007/bf03037169
    title: Michael Gelfond and Vladimir Lifschitz, Classical negation in logic programs and disjunctive databases, New Generation Computing 9(3-4), 365 to 385 (1991)
    locator: the definition of answer sets for disjunctive programs as minimal models of the reduct
  - paper: doi:10.1007/bf01530761
    title: Rachel Ben-Eliyahu and Rina Dechter, Propositional semantics for disjunctive logic programs, Annals of Mathematics and Artificial Intelligence 12(1-2), 53 to 87 (1994)
    locator: head-cycle-free programs, their translation to normal programs, and the resulting NP bound
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: the survey of the complexity of disjunctive logic programming, in the propositional case and with variables
  - paper: doi:10.1145/1149114.1149117
    title: Nicola Leone, Gerald Pfeifer, Wolfgang Faber, Thomas Eiter, Georg Gottlob, Simona Perri and Francesco Scarcello, The DLV system for knowledge representation and reasoning, ACM Transactions on Computational Logic 7(3) (2006)
    locator: the solver for disjunctive programs and its check of answer set candidates
---

This theorem of Eiter and Gottlob (1993, 1995) shows that disjunction in rule heads makes answer set programming strictly more expressive than [normal programs](/stable-model-np-completeness/), unless the polynomial hierarchy collapses. For a [disjunctive logic program](/disjunctive-logic-program/), a candidate answer set must be a minimal model of its reduct, and this minimality test is itself a coNP problem. So the existence question sits at the second level, $\Sigma_2^p$, of the [polynomial hierarchy](/polynomial-hierarchy/), and it is complete there by a reduction from 2-[QBF](/qbf/). Disjunctive solvers such as DLV pay for this with a second, inner search.

## Statement

A *finite propositional disjunctive program* $P$ is a finite set of rules $a_1 \vee \cdots \vee a_k \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$ over a finite set $A$ of atoms, with $k \geq 1$ and $m, n \geq 0$. For $M \subseteq A$, the reduct $P^M$ deletes each rule with some $c_j \in M$ and deletes the negative literals of the other rules. $M$ is an *answer set* of $P$ if $M$ is a minimal model of the positive program $P^M$ (Gelfond and Lifschitz 1991). For $k = 1$ in every rule, this is the stable model of a normal program.

**Theorem** (Eiter and Gottlob 1995). For finite propositional disjunctive programs:

1. deciding whether $P$ has an answer set is $\Sigma_2^p$-complete;
2. deciding whether an atom is in some answer set (brave reasoning) is $\Sigma_2^p$-complete, and hardness holds already for programs without $\mathit{not}$;
3. deciding whether an atom is in every answer set (cautious reasoning) is $\Pi_2^p$-complete;
4. deciding whether a given set $M$ is an answer set (model checking) is coNP-complete.

For head-cycle-free programs (Ben-Eliyahu and Dechter 1994), items 1 and 2 drop to NP and item 3 to coNP, as for normal programs.

## In plain words

For an ordinary program you can check a proposed answer by following the rules forward once. With rules that say "one of these atoms is true", that is no longer enough. You must also be sure that no smaller set of atoms would satisfy the rules too, and to be sure of that you must in effect search through all smaller sets. So the problem has two nested searches. The outer search guesses an answer. The inner search tries to find a smaller set that defeats it. Problems of this shape, "is there a choice such that every counter-choice fails?", form their own class, one level above the problems with a single search. This theorem says that disjunctive programs reach exactly that level and no higher.

## Proof

*Membership.* For item 1, guess $M \subseteq A$. Check that $M$ satisfies $P^M$ in polynomial time. Then check with one call to an NP oracle that no $N \subsetneq M$ is a model of $P^M$; a model $N$ is a polynomial certificate that $M$ is not minimal. So the problem is in $\mathrm{NP}^{\mathrm{NP}} = \Sigma_2^p$. Brave reasoning adds the test $a \in M$. Cautious reasoning for $a$ fails exactly when $P \cup \{\leftarrow a\}$ has an answer set, where the constraint is written $z \leftarrow a, \mathit{not}\ z$ with a new atom $z$, so it is in $\Pi_2^p$. Model checking is the minimality test alone, so it is in coNP.

*Hardness.* The problem "given a DNF formula $\varphi$ over disjoint sets $X$ and $Y$ of variables, is $\exists X\, \forall Y\, \varphi$ true?" is $\Sigma_2^p$-complete. For a literal $l$, let $\sigma(l)$ be the atom $x$ if $l = x$ and $x'$ if $l = \neg x$, and the same for the variables in $Y$. The program $P_\varphi$ has the atoms $x, x'$ for $x \in X$, $y, y'$ for $y \in Y$, and $w$, and the rules

$$x \vee x' \leftarrow \quad (x \in X), \qquad y \vee y' \leftarrow, \quad y \leftarrow w, \quad y' \leftarrow w \quad (y \in Y),$$

$$w \leftarrow \sigma(l_1), \ldots, \sigma(l_r) \quad \text{for each term } l_1 \wedge \cdots \wedge l_r \text{ of } \varphi, \qquad w \leftarrow \mathit{not}\ w.$$

The construction is linear. The proof follows Eiter and Gottlob (1995).

(a) *Every answer set contains $w$.* If $w \notin M$, the reduct contains the fact $w \leftarrow$, so $M$ is not a model of $P^M$.

(b) *The answer sets are the sets $M_I = I \cup \{y, y' : y \in Y\} \cup \{w\}$, where $I$ contains exactly one of $x, x'$ for each $x \in X$ and the corresponding assignment of $X$ makes $\forall Y\, \varphi$ true.* By (a), $w \in M$, so the rule $w \leftarrow \mathit{not}\ w$ is deleted, and the rules $y \leftarrow w$ and $y' \leftarrow w$ force all of $y, y'$ into $M$. Any model $N \subsetneq M$ of $P^M$ that keeps $w$ must keep all of $Y$ and $Y'$, so $M$ can be minimal only if it contains exactly one of $x, x'$ for each $x$. A model $N \subsetneq M$ that drops $w$ keeps $I$, picks at least one of $y, y'$ for each $y$, and makes no term body true. A choice of exactly one of $y, y'$ for each $y$ is such a model exactly when the assignment of $Y$ it gives makes every term false under $I$. So $M_I$ is minimal exactly when no assignment of $Y$ falsifies $\varphi$ under $I$, that is, when $\forall Y\, \varphi$ holds under $I$.

By (b), $P_\varphi$ has an answer set if and only if $\exists X\, \forall Y\, \varphi$ is true. Remove the rule $w \leftarrow \mathit{not}\ w$ to get a positive program $P^+_\varphi$. Its answer sets are its minimal models, the sets $M_I$ of (b) together with the minimal models without $w$, and so $w$ is in some answer set of $P^+_\varphi$ if and only if the formula is true. This gives item 2 for positive programs. Item 3 follows from item 1: with a new atom $z$ that occurs in no rule, $z$ is in every answer set of $P$ exactly when $P$ has none. Item 4 is coNP-hard by a similar reduction from the validity of a DNF formula, with $X$ empty: $M = Y \cup Y' \cup \{w\}$ is an answer set of $P_\varphi$ exactly when $\forall Y\, \varphi$ is true. $\square$

*Examples.* For $\exists x\, \forall y\, ((x \wedge y) \vee (x \wedge \neg y))$, which is true, $P_\varphi$ has exactly one answer set, $\{w, x, y, y'\}$, and $P^+_\varphi$ has the three answer sets $\{w, x, y, y'\}$, $\{x', y\}$ and $\{x', y'\}$. For $\exists x\, \forall y\, ((x \wedge y) \vee (\neg x \wedge \neg y))$, which is false, $P_\varphi$ has no answer set, and $P^+_\varphi$ has the two answer sets $\{x, y'\}$ and $\{x', y\}$, neither of which contains $w$.

## Consequences

- **Disjunction adds expressive power.** Unless the polynomial hierarchy collapses to its first level, disjunctive programs cannot be translated into normal programs in polynomial time with the same answer sets on the original atoms. In particular, the translation that replaces $a \vee b \leftarrow B$ by $a \leftarrow B, \mathit{not}\ b$ and $b \leftarrow B, \mathit{not}\ a$ (shifting) must fail on some programs.
- **Solvers need two searches.** A disjunctive solver generates candidates with an NP-style search and checks the minimality of each candidate with a second search, usually a SAT call. DLV (Leone et al. 2006) is built this way.
- **Problems at the second level.** Every problem in $\Sigma_2^p$ has a polynomial encoding as a disjunctive program, through 2-QBF and the construction above. Normal programs have no such encoding unless the hierarchy collapses.
- **Link to other nonmonotonic logics.** The main reasoning tasks of [circumscription](/circumscription/), [default logic](/default-logic-complexity/) and [autoepistemic logic](/autoepistemic-logic/) are also at the second level. The 1993 paper of Eiter and Gottlob applies the disjunctive results to these logics.

## Tightness

- **Negation is needed for item 1.** A positive disjunctive program always has an answer set, because every finite model contains a minimal one and the set of all atoms is a model. So the hardness of existence uses $\mathit{not}$ or constraints. The single rule $w \leftarrow \mathit{not}\ w$ is enough.
- **Head cycles are needed.** If no rule has two head atoms on a common cycle of the positive dependency graph, shifting is correct and the program becomes a normal program of the same size, so existence is in NP. With a head cycle, shifting can lose answer sets. A small example is $a \vee b \leftarrow$, $a \leftarrow b$, $b \leftarrow a$: it has the answer set $\{a, b\}$, and its shifted version has none.
- **Model checking.** For normal programs model checking is polynomial; for disjunctive programs it is coNP-complete, so the gap already shows in the inner test.
- **Variables.** For disjunctive programs with variables and no function symbols, the problem is complete for $\mathrm{NEXPTIME}^{\mathrm{NP}}$ when the program is part of the input and $\Sigma_2^p$-complete when the program is fixed (Dantsin, Eiter, Gottlob and Voronkov 2001).

## History

Gelfond and Lifschitz (1991) extended stable models to disjunctive programs with classical negation, and called them answer sets. Eiter and Gottlob presented the complexity of disjunctive logic programming at ILPS 1993 and published the full propositional study in 1995, which covered the stable, minimal model and other semantics. Ben-Eliyahu and Dechter (1994) identified head-cycle-free programs as the class where disjunction does not raise the complexity. The DLV system (Leone et al. 2006) was designed for the full $\Sigma_2^p$ case.

## References
