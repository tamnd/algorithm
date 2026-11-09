---
tag: S27DY0
kind: technique
slug: boolean-abstraction
name: Boolean abstraction
aliases:
- Boolean skeleton
- propositional abstraction
- propositional skeleton
- T2B
area: logic-and-constraints/smt
level: core
summary: Replace each theory atom of a formula by a propositional variable, and keep the map back. The result has a model whenever the formula has one, so it is a sound over-approximation for SAT.
prereqs: [smt-problem, sat, conjunctive-normal-form]
see_also: [lazy-smt, dpll-t, cdcl-t, eager-smt-encoding, tseitin-transformation, theory-conflict-explanation, hash-consing, cegar]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.2.1.4, Abstraction (the bijection T2B and its inverse B2T, and the elimination of ite terms); Section 33.4.3.1 (normalizing T-atoms), Section 33.4.3.6 (partial assignments) and Section 33.4.3.7 (pure-literal filtering)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 3, From Propositional to Quantifier-Free Theories (the propositional skeleton and the lazy algorithms that use it)
  - paper: doi:10.3233/sat190034
    title: Roberto Sebastiani, Lazy satisfiability modulo theories, Journal on Satisfiability, Boolean Modeling and Computation 3, 2007, pages 141 to 224
    locator: the Boolean abstraction and refinement functions, and the techniques of normalization, static learning and pure-literal filtering
---

The Boolean abstraction of a formula $\varphi$ replaces each theory atom, such as $x + y \le 3$ or $f(a) = b$, by a propositional variable, the same variable for each occurrence of the same atom. The result $\varphi^p$ is a propositional formula with the same Boolean structure, and a map $B$ from the new variables back to the atoms lets a solver read each propositional model as a set of theory literals. Every model of $\varphi$ gives a model of $\varphi^p$, so if a SAT solver finds $\varphi^p$ unsatisfiable, $\varphi$ is unsatisfiable in every theory. The converse fails, because $\varphi^p$ forgets what the atoms mean. The abstraction is the first step of every [lazy SMT](/lazy-smt/) solver, which then removes the wrong propositional models one by one, and of the per-constraint [eager encodings](/eager-smt-encoding/), which add the missing theory facts as clauses before the search.

## In plain words

A formula can say "x plus y is at most 3, or f of a equals b". A SAT solver cannot read such facts. It works only with switches that are on or off.

So give each fact a name, such as p1 and p2, and write the formula again with the names: "p1 or p2". Use the same name each time the same fact appears, and keep a table from each name back to its fact.

The SAT solver can now work on this formula. If it finds no way to set the switches, the first formula has no solution either. If it finds a way, the table turns the switches back into facts, and a theory solver checks whether these facts can hold together. Some settings fail this check, because the SAT solver does not know that x < 3 and x > 5 cannot both be true.

## When it applies

- The formula is quantifier-free, or its quantified subformulas can be treated as atoms, and the theory solver works on conjunctions of literals.
- A SAT solver is to do the Boolean search, as in [DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/), or the formula is to be sent to SAT after theory clauses are added.
- The atoms can be brought into a normal form, so that atoms that are equal in the theory get the same variable as often as possible.

## The template

The holes are the elimination of if-then-else terms, the normal form of atoms, and the conversion to CNF.

```pseudo id=main
ABSTRACT(φ)
L1  remove each term ite(ψ, t1, t2) of φ: put a fresh constant c in its place and add ite(ψ, c = t1, c = t2) as a conjunct   ▷ hole: ite elimination
L2  A ← an empty map from atoms to variables; B ← an empty map from variables to atoms
L3  for each atom α of φ
L4      (β, s) ← NORMALIZE(α), with α equivalent in T to β if s = + and to ¬β if s = −   ▷ hole: the normal form
L5      if β is not a key of A then p ← a fresh variable; A[β] ← p; B[p] ← β
L6      replace this occurrence of α by A[β], or by ¬A[β] if s = −
L7  φ^p ← the result; a propositional symbol of φ is its own abstraction
L8  return CNF(φ^p), A, B                                    ▷ hole: Tseitin or another CNF conversion
```

The map $B$ is the *refinement*. For a propositional assignment $\nu$ of the variables of $B$, the set $B(\nu) = \{B(p) : \nu(p) = \text{true}\} \cup \{\neg B(p) : \nu(p) = \text{false}\}$ is the set of theory literals that $\nu$ stands for. The Handbook calls the two maps T2B and B2T.

**Two facts.** Let $\varphi^p$ come from line L7 with a normal form that meets the rule of line L4.

1. *Soundness of UNSAT.* If $\varphi^p$ is unsatisfiable, then $\varphi$ is $T$-unsatisfiable. *Proof.* Let $\mathcal{A}$ be a $T$-model of $\varphi$. Set $\nu(p)$ to the truth value of $B(p)$ in $\mathcal{A}$. By line L4, each replaced occurrence has the truth value in $\nu$ that the original atom has in $\mathcal{A}$. The connectives are the same, so $\nu$ satisfies $\varphi^p$. $\square$
2. *Exactness with the theory check.* $\varphi$ is $T$-satisfiable if and only if $\varphi^p$ has a model $\nu$ for which $B(\nu)$ is $T$-satisfiable. *Proof.* If $\mathcal{A}$ is a $T$-model of $\varphi$, the $\nu$ of fact 1 satisfies $\varphi^p$, and $\mathcal{A}$ satisfies $B(\nu)$. Conversely, if $\mathcal{A}$ is a $T$-model of $B(\nu)$, each atom of $\varphi$ has in $\mathcal{A}$ the value that $\nu$ gives it, so $\mathcal{A}$ makes $\varphi$ true. $\square$

Fact 2 is the base of the lazy approach: search the models of $\varphi^p$, and check each with a theory solver. A CNF from the [Tseitin transformation](/tseitin-transformation/) adds new variables, but its models restricted to the variables of $\varphi^p$ are exactly the models of $\varphi^p$, so both facts still hold.

### A worked example

Take the EUF formula

$$\varphi = (a = b \vee a = c) \wedge (b = a \rightarrow f(a) \ne f(b)) \wedge (c = a \rightarrow f(a) \ne f(c)).$$

It is unsatisfiable: if $a = b$, the second conjunct needs $f(a) \ne f(b)$, which is false by congruence, and the same holds for $a = c$.

**Without a normal form**, each of the six atoms gets a variable: $p_1$ for $a = b$, $p_2$ for $a = c$, $p_3$ for $b = a$, $p_4$ for $f(a) = f(b)$, $p_5$ for $c = a$ and $p_6$ for $f(a) = f(c)$. Then $\varphi^p = (p_1 \vee p_2) \wedge (\neg p_3 \vee \neg p_4) \wedge (\neg p_5 \vee \neg p_6)$ has $3 \cdot 3 \cdot 3 = 27$ models.

**With a normal form** that orders the two sides of an equality, $b = a$ becomes $a = b$, and $c = a$ becomes $a = c$. Four variables are left, and $\varphi^p = (p_1 \vee p_2) \wedge (\neg p_1 \vee \neg p_3) \wedge (\neg p_2 \vee \neg p_4)$, with $p_3$ for $f(a) = f(b)$ and $p_4$ for $f(a) = f(c)$. It has 5 models.

In both cases none of the models has a $T$-consistent refinement, as fact 2 needs. A script that runs the offline lazy loop of the [lazy SMT](/lazy-smt/) page on both abstractions, with a SAT solver that returns the first model in a fixed order, gives these counts of SAT calls:

| abstraction | models of $\varphi^p$ | SAT calls, blocking the whole model | SAT calls, blocking a minimal conflict |
|---|---|---|---|
| six atoms | 27 | 28 | 5 |
| four atoms | 5 | 6 | 3 |

Without the normal form, the theory solver must also find the conflicts $\{a = b, b \ne a\}$ and $\{a = c, c \ne a\}$, which the SAT side cannot see because $p_1$ and $p_3$ are different variables to it.

## Classic examples

- **[DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/).** The SAT engine runs on $\varphi^p$, and the theory solver checks $B(\nu)$ for the partial assignment $\nu$ on the trail.
- **The offline loop of [lazy SMT](/lazy-smt/).** A SAT solver finds a model of $\varphi^p$, and if $B(\nu)$ has a conflict $\eta$, the clause $\neg \eta^p$ is added to $\varphi^p$.
- **Per-constraint [eager encoding](/eager-smt-encoding/).** The direct encoding of the Handbook, Section 33.3.3, first takes the Boolean abstraction and then adds a formula over the new variables, such as transitivity constraints, that rules out all $T$-inconsistent models at once.
- **[MaxSMT](/maxsmt/) and [optimization modulo theories](/optimization-modulo-theories/).** The soft constraints are abstracted like the hard ones, and a MaxSAT search runs on the abstraction.
- **[Unsat cores](/unsat-core/).** The core is computed on the abstraction plus the theory lemmas, and the map $B$ turns it back into input assertions.

## Variations

- **Normalization.** The Handbook lists rewrites that map $T$-equivalent atoms to the same atom: drop dual operators ($x_1 < x_2$ becomes $\neg (x_2 \le x_1)$ after ordering), flatten sums, sort the terms of a sum, and use facts of the theory, such as $x < 4$ to $x \le 3$ for an integer $x$. [Hash-consing](/hash-consing/) of terms makes the test of line L5 a pointer comparison.
- **Static learning.** Before the search, add small theory lemmas over the atoms of $\varphi$, such as $\neg (x = 0) \vee \neg (x = 1)$ or the congruence lemma $\neg (x_1 = y_1) \vee f(x_1) = f(y_1)$ when both atoms occur. These clauses make some theory facts visible to unit propagation.
- **Pure-literal filtering.** If an atom occurs only positively in $\varphi$, the theory solver need not get its negation when the SAT side sets it to false. This can make $B(\nu)$ consistent, and for disequalities in arithmetic it avoids a case split.
- **Partial assignments.** If a partial assignment already satisfies all clauses of $\varphi^p$, only its literals need a theory check. The other atoms can stay open.
- **Abstraction of quantified formulas.** Lazy solvers with quantifiers treat each quantified subformula $\forall x\, \psi$ as an atom. When it is set to true, [quantifier instantiation](/quantifier-instantiation/) adds instances of $\psi$.
- **Predicate abstraction in model checking.** [CEGAR](/cegar/) abstracts the states of a program by the truth values of chosen predicates. It is a different abstraction, of a transition system and not of one formula, but it uses the same idea of a Boolean view that is refined on demand.

## Pitfalls

- **A normal form that is not an equivalence.** The rewrite $x < 4$ to $x \le 3$ is right over the integers and wrong over the reals, where $x = 3.5$ makes the two atoms differ. Each rewrite of line L4 must be an equivalence in every model of $T$.
- **Atoms that are the same up to symmetry.** Without a normal form, $a = b$ and $b = a$ get different variables. The answer stays correct, but the SAT side can make them differ, and the theory solver must refute each such model. In the example this needs 5 SAT calls in place of 3.
- **Reading a propositional model as a theory model.** A model of $\varphi^p$ says nothing about the theory until $B(\nu)$ is checked. Returning SAT after the SAT call alone is wrong.
- **Terms with Boolean structure inside atoms.** An atom such as $f(\mathrm{ite}(\psi, a, b)) = c$ hides a case split. Line L1 must remove ite terms before abstraction, or the theory solver must handle them.
- **Losing the map.** Lemmas from the theory solver are over atoms, and learned clauses are over variables. Both directions of the map must be kept for the whole run, including atoms that were created later, for example by splitting on demand.

## Exercises

1. Show that fact 1 still holds if the normal form only gives $\alpha \models_T \beta$ for each positive occurrence of $\alpha$ and $\beta \models_T \alpha$ for each negative one. Hint: use the polarity of each occurrence.
2. For $\varphi = (x \le 1 \vee x \ge 3) \wedge x = 2$ over the integers, write $\varphi^p$, list its models, and find the conflict set of each.
3. Let $\varphi = (a = b) \wedge f(a) \ne f(b) \wedge \bigwedge_{i=1}^{k} (c_i = d_i \vee c_i = e_i)$. Count the models of $\varphi^p$, and show that one theory lemma of size 2 makes $\varphi^p$ unsatisfiable.

## References
