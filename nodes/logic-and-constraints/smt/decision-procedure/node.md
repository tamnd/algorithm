---
tag: M686V8
kind: definition
slug: decision-procedure
name: Decision procedure
aliases:
- decision procedure for a theory
- satisfiability procedure
- T-solver
area: logic-and-constraints/smt
level: intro
summary: An algorithm that halts on every formula of a given class and answers correctly whether it is satisfiable (or valid) in a given theory. It must be sound, complete and terminating.
prereqs: [smt-problem, decidable-language]
see_also: [entscheidungsproblem, church-theorem, recursively-enumerable-language, hilberts-tenth-problem, congruence-closure, nelson-oppen, quantifier-elimination, delta-satisfiability]
sources:
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 1 (decision procedures, soundness and completeness, the theories of the book)
  - paper: doi:10.1007/978-3-540-74113-8
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Decision Procedures with Applications to Verification, Springer, 2007
    locator: Part II, decision procedures for quantifier-free fragments, and Chapter 10 on combinations
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.2 (theories and the ground T-satisfiability problem), Section 33.4.1 (features of theory solvers), Section 33.5 (theory solvers)
  - paper: doi:10.2307/2269326
    title: Alonzo Church, A note on the Entscheidungsproblem, Journal of Symbolic Logic 1(1), 1936, pages 40 to 41
    locator: there is no decision procedure for validity in first-order logic
---

A decision procedure answers a yes-or-no question about formulas. Given a theory $T$ and a class of formulas, such as the conjunctions of literals of linear real arithmetic, or all quantifier-free formulas of equality with uninterpreted functions, it takes any formula of the class, always halts, and says correctly whether the formula is satisfiable in $T$. In SMT, the decision procedures for conjunctions of literals are called *theory solvers*, and the SAT engine of [DPLL(T)](/dpll-t/) turns them into decision procedures for arbitrary quantifier-free formulas. Not every class has one: Church and Turing proved in 1936 that first-order validity has none, and nonlinear integer arithmetic has none by the solution of [Hilbert's tenth problem](/hilberts-tenth-problem/).

## Definition

Let $T$ be a theory and $\mathcal{F}$ a class of formulas, called the *fragment*. A **decision procedure for $\mathcal{F}$ modulo $T$** is an algorithm $D$ such that for every $\varphi \in \mathcal{F}$:

- **Termination.** $D(\varphi)$ halts.
- **Soundness.** If $D(\varphi)$ returns UNSAT, then $\varphi$ has no $T$-model.
- **Completeness.** If $\varphi$ has no $T$-model, then $D(\varphi)$ returns UNSAT.

Equivalently, $D$ answers SAT exactly on the $T$-satisfiable formulas of $\mathcal{F}$ and halts on all inputs. The fragment $\mathcal{F}$ is **decidable modulo $T$** if a decision procedure exists, that is, if the set of its $T$-satisfiable formulas is a [decidable language](/decidable-language/). Because $\varphi$ is $T$-valid exactly when $\neg \varphi$ is $T$-unsatisfiable, a decision procedure for satisfiability on a fragment closed under negation is also one for validity. Older texts often take the validity view.

Remarks on the definition.

- *Soundness and completeness are relative to the answer.* Some texts call a procedure sound when every SAT answer is correct, and complete when every UNSAT answer is correct. Read each source with its own convention. A decision procedure has both properties, whatever their names.
- *The fragment matters.* The same theory can be decidable on one fragment and not on another. Linear integer arithmetic is decidable with quantifiers ([Presburger arithmetic](/presburger-arithmetic/)), and so is the theory of real closed fields ([Tarski](/tarski-decidability-theorem/)). Equality with uninterpreted functions is decidable for ground formulas, but with quantifiers it is first-order logic, which is not.
- *Semi-decision procedures.* A procedure that halts with UNSAT on every unsatisfiable input, but may run forever on satisfiable ones, is a *semi-decision procedure*. Resolution for first-order logic is one: its unsatisfiable formulas form a [recursively enumerable](/recursively-enumerable-language/) set.
- *Incomplete procedures.* Real solvers also return a third answer, *unknown*, for fragments that are undecidable or too hard. Such a solver is not a decision procedure, even if it is sound.
- *Extra outputs.* For use inside SMT, a theory solver is expected to give more than the answer: a model when the answer is SAT, a small [conflict explanation](/theory-conflict-explanation/) when it is UNSAT, [theory propagations](/theory-propagation/), and incremental and backtrackable behaviour (Handbook, Section 33.4.1).

## Examples and non-examples

- **Equality with uninterpreted functions.** [Congruence closure](/congruence-closure/) decides conjunctions of ground equalities and disequalities in $O(n \log n)$ time. With a SAT engine on top, [DPLL(T)](/dpll-t/) decides all ground EUF formulas, see [EUF satisfiability](/euf-satisfiability/).
- **Difference logic.** [Bellman-Ford](/bellman-ford/) decides conjunctions of constraints $x - y \le c$: they are satisfiable exactly when the constraint graph has no negative cycle. See [difference logic satisfiability](/difference-logic-satisfiability/).
- **Linear real arithmetic.** The simplex method and [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) decide conjunctions of linear constraints over the reals. See [simplex for SMT](/simplex-for-smt/).
- **Linear integer arithmetic.** Branch and bound with cuts, the [Omega test](/omega-test/), and quantifier elimination for [Presburger arithmetic](/presburger-arithmetic/) are decision procedures.
- **Combinations.** [Nelson-Oppen](/nelson-oppen/) turns decision procedures for two signature-disjoint, [stably infinite](/stable-infiniteness/) theories into one for their union.
- **Non-example: first-order logic.** By [Church's theorem](/church-theorem/), no algorithm decides validity of first-order formulas, the [Entscheidungsproblem](/entscheidungsproblem/). Quantifier instantiation by [E-matching](/e-matching/) is therefore a heuristic, not a decision procedure.
- **Non-example: nonlinear integer arithmetic.** By the Matiyasevich-Robinson-Davis-Putnam theorem, the solvability of Diophantine equations is undecidable, so no decision procedure exists for QF_NIA.
- **Non-example: a SAT solver with a time limit.** A solver that gives up after one hour is sound, but it does not halt with a definite answer on all inputs.
- **A relaxed question.** [δ-satisfiability](/delta-satisfiability/) decides a weaker question about nonlinear real formulas with transcendental functions: it may answer "δ-SAT" for a formula that is unsatisfiable, but only if a small change of the constants makes it satisfiable. It is a decision procedure for that relaxed problem, not for the exact one.

## Related definitions

- [SMT problem](/smt-problem/): the problem of deciding $T$-satisfiability of quantifier-free formulas, for which the decision procedures of SMT solvers are built.
- [Decidable language](/decidable-language/) and [recursively enumerable language](/recursively-enumerable-language/): the computability notions behind decidable and semi-decidable fragments.
- [Quantifier elimination](/quantifier-elimination/): a method that gives decision procedures for full first-order theories, such as Presburger arithmetic and real closed fields, by reducing each formula to an equivalent quantifier-free one.
- [Convex theory](/convex-theory/) and [stable infiniteness](/stable-infiniteness/): properties of a theory that decide how its decision procedure can be combined with others.

## References
