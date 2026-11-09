---
tag: 3CT6YF
kind: concept
slug: backbone
name: Backbone of a formula
aliases:
- backbone variables
- backbone literals
- implied literals
area: logic-and-constraints/sat-solving
level: advanced
summary: The literals that are true in every model of a satisfiable formula; testing one literal is coNP-complete, and the whole backbone needs at most n + 1 SAT calls.
prereqs: [sat, literal, conjunctive-normal-form]
see_also: [failed-literal-probing, incremental-sat, autarky, satisfiability-threshold, model-counting, unsat-core]
sources:
  - paper: doi:10.3233/AIC-140640
    title: Mikoláš Janota, Inês Lynce and Joao Marques-Silva, Algorithms for computing backbones of propositional formulae, AI Communications 28(2), 2015, 161-177
    locator: the iterative algorithm with model filtering, its bound of n + 1 SAT calls, chunking and core-based variants, and their experiments
  - paper: doi:10.1038/22055
    title: Rémi Monasson, Riccardo Zecchina, Scott Kirkpatrick, Bart Selman and Lidror Troyansky, Determining computational complexity from characteristic 'phase transitions', Nature 400, 1999, 133-137
    locator: the backbone of random 3-SAT and of the 2+p-SAT model, and its jump at the threshold
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), failed literals and units; the chapters on random satisfiability and on incremental use of solvers
---

The backbone of a satisfiable [CNF](/conjunctive-normal-form/) formula $F$ is the set of literals that are true in every model of $F$. A variable whose literal is in the backbone is a backbone variable: it has the same value in all solutions. A literal $l$ is in the backbone exactly when $F \wedge \neg l$ is unsatisfiable, so testing one literal is coNP-complete, and the whole backbone can be found with at most $n + 1$ calls of a SAT solver. Backbones tell a user which choices are forced, for example in product configuration. They also simplify a formula, because backbone literals can be added as unit clauses without losing any model. In random 3-SAT, the size of the backbone jumps at the [satisfiability threshold](/satisfiability-threshold/), as found by Monasson and co-authors in 1999.

## In plain words

A formula can have many solutions. Some variables take different values in different solutions, while others have the same value in every one of them. Those fixed values form the backbone.

To test whether a value is fixed, ask a solver for a solution with the opposite value. If there is none, the value is fixed. Each solution the solver finds also shows that many other values are not fixed, namely all values that this solution does not share with the first one. So you never need more questions than variables plus one.

## The idea

Notation: $F$ has $n$ variables and $m$ clauses; $|F|$ is its size. $\mathrm{Mod}(F)$ is its set of models. For satisfiable $F$,
$$\mathrm{BB}(F) = \{\, l : \alpha(l) = 1 \text{ for every } \alpha \in \mathrm{Mod}(F) \,\}.$$
For unsatisfiable $F$ the backbone is not defined; some authors take all literals by convention.

**Basic facts.**

- $l \in \mathrm{BB}(F)$ if and only if $F$ is satisfiable and $F \wedge \neg l$ is unsatisfiable. So deciding $l \in \mathrm{BB}(F)$ for a satisfiable $F$ is coNP-complete: it is in coNP, and unsatisfiability of a CNF $G$ reduces to it. Add a fresh variable $y$ to every clause of $G$ to get $F$. Then $F$ is satisfiable (set $y = 1$), and $y \in \mathrm{BB}(F)$ if and only if $F \wedge \neg y$, which is $G$ with $y = 0$, is unsatisfiable.
- $F$ and $F \wedge \bigwedge_{l \in \mathrm{BB}(F)} l$ have the same models. So backbone literals are safe units.
- Every unit found by [unit propagation](/unit-propagation/) or by [failed-literal probing](/failed-literal-probing/) on a satisfiable $F$ is in the backbone. The converse fails: the backbone can contain literals that no cheap method finds.

**Computing the backbone with model filtering.** The algorithm keeps a set of candidates, which starts as the literals of one model, and removes candidates with each new model.

```pseudo id=main
BACKBONE(F)
L1  μ ← SAT(F); if F is unsatisfiable then return UNSAT
L2  Cand ← the literals true in μ;  B ← ∅
L3  while Cand is not empty do
L4      l ← remove a literal from Cand
L5      if SAT(F ∧ B ∧ ¬l) returns a model μ' then
L6          Cand ← the literals of Cand that are true in μ'
L7      else B ← B ∪ {l}                       ▷ F ∧ ¬l is unsatisfiable
L8  return B
```

**Theorem.** BACKBONE returns $\mathrm{BB}(F)$ and makes at most $n + 1$ SAT calls.

*Proof.* Invariant: $B \subseteq \mathrm{BB}(F)$, and every literal of $\mathrm{BB}(F)$ is in $B$ or in Cand. At line L2 it holds, because every backbone literal is true in $\mu$. At line L5 the units $B$ are implied by $F$, so $F \wedge B \wedge \neg l$ is satisfiable exactly when $F \wedge \neg l$ is. If it has a model $\mu'$, then $l \notin \mathrm{BB}(F)$, and line L6 removes only literals false in the model $\mu'$ of $F$, which are not in the backbone. Otherwise $l \in \mathrm{BB}(F)$ and line L7 adds it. Each round removes $l$ from Cand, and Cand starts with $n$ literals, so there are at most $n$ rounds after the first call. When Cand is empty, the invariant gives $B = \mathrm{BB}(F)$. $\blacksquare$

Each SAT call can be an [incremental](/incremental-sat/) call with $B$ and $\neg l$ as assumptions, so the solver keeps its learned clauses between calls.

## Examples

**A small formula.** Let
$$F = (x_1 \vee x_2) \wedge (\neg x_1 \vee x_2) \wedge (\neg x_2 \vee x_3 \vee x_4) \wedge (\neg x_3 \vee \neg x_4) \wedge (x_3 \vee x_5).$$
The first two clauses force $x_2 = 1$ in every model. The rest has models with $x_3 = 1, x_4 = 0$ and with $x_3 = 0, x_4 = 1, x_5 = 1$, and $x_1$ is free. So $\mathrm{BB}(F) = \{x_2\}$. Unit propagation alone does not find $x_2$, but probing $\neg x_2$ fails at once, so failed-literal probing does.

**Unique model.** If $F$ has exactly one model $\alpha$, the backbone is the set of all $n$ literals of $\alpha$.

**No backbone.** If for each variable some model sets it true and some model sets it false, the backbone is empty. A formula with no clauses is such a case.

**A backbone that probing misses.** Take the 7 clauses with three literals over $x_1, x_2, x_3$ other than $(\neg x_1 \vee \neg x_2 \vee \neg x_3)$. Each clause excludes one assignment, so the only model is $x_1 = x_2 = x_3 = 1$, and the backbone is $\{x_1, x_2, x_3\}$. Setting $\neg x_1$ leaves all four binary clauses over $x_2, x_3$, and setting $x_1$ leaves three of them; neither has a unit, so no literal fails and nothing is lifted. Failed-literal probing finds none of the backbone, while BACKBONE finds all of it with 4 SAT calls.

## Where it is used

- **Product configuration and interactive design.** A configurator shows which options are forced by the choices so far; these are the backbone literals of the constraints together with the choices.
- **Simplification.** Adding backbone literals as units removes variables and clauses before model counting, enumeration or optimization, without losing models.
- **Random SAT.** Monasson and co-authors studied the fraction of backbone variables in random $k$-SAT with methods from statistical physics. In their analysis the fraction for 3-SAT jumps from zero to a positive value at the threshold, while for 2-SAT it grows continuously; they linked this jump to the high cost of the search near the threshold. See [satisfiability threshold](/satisfiability-threshold/).
- **Fault localization and debugging.** In SAT-based diagnosis, the backbone of the diagnosis formula gives the components that are faulty in every explanation.
- **Variants of the algorithm.** Janota, Lynce and Marques-Silva compare the plain iterative test, model filtering, testing chunks of $k$ candidates with one clause $(\neg l_1 \vee \cdots \vee \neg l_k)$, and core-based methods that read several backbone literals from one unsatisfiable core.

## References
