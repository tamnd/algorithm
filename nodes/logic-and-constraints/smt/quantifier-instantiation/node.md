---
tag: 952R67
kind: concept
slug: quantifier-instantiation
name: Quantifier instantiation
aliases:
- E-matching triggers
- instantiation of universal axioms
- instantiation-based quantifier reasoning
- ground instantiation
area: logic-and-constraints/smt
level: advanced
summary: SMT solvers handle a formula forall x. phi by adding ground instances phi[x/t] to the quantifier-free problem. The choice of the terms t decides whether a proof is found.
prereqs: [smt-problem, dpll-t]
see_also: [e-matching, model-based-theory-combination, smt-lib, church-theorem, cegis, syntax-guided-synthesis, euf-satisfiability, e-graph]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.7.2 (generalized literals, the rules for existential and universal instantiation, completeness of fair instantiation for universal theories, triggers and T-matching)
  - paper: doi:10.1145/1066100.1066102
    title: David Detlefs, Greg Nelson and James B. Saxe, Simplify, a theorem prover for program checking, Journal of the ACM 52(3), 2005, pages 365 to 473
    locator: instantiation by matching triggers in the E-graph, multi-triggers and matching loops
  - paper: doi:10.1007/978-3-642-02658-4_25
    title: Yeting Ge and Leonardo de Moura, Complete instantiation for quantified formulas in satisfiability modulo theories, CAV 2009, LNCS 5643, pages 306 to 320
    locator: model-based quantifier instantiation and the essentially uninterpreted fragment, on which it is complete
  - paper: doi:10.1109/fmcad.2014.6987613
    title: Andrew Reynolds, Cesare Tinelli and Leonardo de Moura, Finding conflicting instances of quantified formulas in SMT, FMCAD 2014, pages 195 to 202
    locator: conflict-based instantiation
  - paper: doi:10.1007/978-3-319-89963-3_7
    title: Andrew Reynolds, Haniel Barbosa and Pascal Fontaine, Revisiting enumerative instantiation, TACAS 2018, LNCS 10806, pages 112 to 131
    locator: enumerative instantiation of terms in a fixed order, as a complement to E-matching
  - paper: doi:10.1007/s10703-017-0290-y
    title: Andrew Reynolds, Tim King and Viktor Kuncak, Solving quantified linear arithmetic by counterexample-guided instantiation, Formal Methods in System Design 51(3), 2017, pages 500 to 532
    locator: counterexample-guided instantiation as a decision procedure for quantified linear real and integer arithmetic
  - url: https://smt-lib.org/papers/smt-lib-reference-v2.7-r2025-07-07.pdf
    title: Clark Barrett, Pascal Fontaine and Cesare Tinelli, The SMT-LIB Standard, Version 2.7, release of July 7, 2025
    locator: Section 3.6.5 (the :pattern attribute and footnote 7 on instantiation with the matching substitution)
---

Quantifier instantiation is how SMT solvers reason about quantified formulas. The theory solvers of an SMT solver work only on ground literals, without variables. So a universally quantified formula $\forall x.\, \varphi(x)$ is used through its *instances* $\varphi(t)$, for ground terms $t$, which the solver adds to the ground problem. An existential $\exists x.\, \varphi(x)$ is replaced once by $\varphi(a)$ for a fresh constant $a$, which is Skolemization. Each instance is a logical consequence, so adding instances is always sound: if the ground problem with the instances is unsatisfiable, so is the original formula. The hard part is the choice of the terms. First-order logic is undecidable ([Church's theorem](/church-theorem/)), so no choice works in all cases. Fair enumeration of all ground terms finds every refutation in pure first-order logic with equality, but it is slow and never shows satisfiability. Practical methods, such as [E-matching](/e-matching/) with *triggers*, choose terms that already appear in the problem. They are fast but incomplete. Other methods are complete on exact fragments, which this page states.

## In plain words

A rule such as "every number plus one is bigger than the number" is about infinitely many numbers. A solver cannot look at all of them at once.

So it copies the rule for some numbers that it actually meets in the problem: "a plus one is bigger than a", "b plus one is bigger than b". Each copy is a plain fact that the solver already knows how to handle.

If the copies lead to a contradiction, the problem has no solution. If they do not, the solver may simply have chosen the wrong copies. Choosing good copies is the whole difficulty, and different solvers choose in different ways.

## The idea

**The rules.** The Handbook (Section 33.7.2) extends the abstract DPLL(T) framework with *generalized literals*: a literal can also be a closed quantified formula, whose Boolean value the SAT engine decides. Two rules then add clauses:

- **Existential instantiation.** If $\exists \bar x.\, \varphi$ is true on the trail, add the clause $\neg \exists \bar x.\, \varphi \vee \varphi[\bar x / \bar a]$ with fresh constants $\bar a$. This is needed once per formula.
- **Universal instantiation.** If $\forall \bar x.\, \varphi$ is true on the trail, add the clause $\neg \forall \bar x.\, \varphi \vee \varphi[\bar x / \bar s]$ for ground terms $\bar s$. This may be needed many times, with different terms.

Termination can only come from a limit on the use of the second rule. A strategy for it is the instantiation method of the solver.

**Why it can work.** Herbrand's theorem gives the basis. Let $\Phi$ be a set of formulas $\forall \bar x.\, C$, with $C$ quantifier-free, over a signature with function symbols and equality and no other theory. Then $\Phi$ is unsatisfiable exactly when some finite set of ground instances, with terms built from the symbols of $\Phi$ (and one extra constant if there is none), is unsatisfiable in [EUF](/euf-satisfiability/). So a *fair* strategy, one that makes every ground instance at some point, refutes every unsatisfiable input. The Handbook states that completeness of this kind holds for exhaustive and fair instantiation for some background theories, such as universal theories. Such a strategy is still not a decision procedure. On a satisfiable input it runs forever, unless the set of useful instances is finite.

**The main strategies.**

| method | how it chooses the terms | complete on |
|---|---|---|
| [E-matching](/e-matching/) (Simplify, Z3, cvc5) | match the triggers of the formula against the terms of the [e-graph](/e-graph/), modulo the known equalities | no fragment in general: the instances depend on the triggers |
| conflict-based (Reynolds, Tinelli and de Moura, 2014) | look for one instance that is false in the current e-graph, so that it gives a conflict at once | no fragment in general; it is used before E-matching |
| model-based (Ge and de Moura, 2009) | build a candidate model of the ground part, check each quantified formula in it, and instantiate with a counterexample | the essentially uninterpreted fragment (see below) |
| enumerative (Reynolds, Barbosa and Fontaine, 2018) | try the ground terms of the problem in a fixed order | refutationally complete for EUF when the enumeration is fair over all terms |
| counterexample-guided, for arithmetic (Reynolds, King and Kuncak, 2017) | find a model of the negated body, and choose terms from bounds in it | quantified linear real and linear integer arithmetic, where it terminates |

**The complete fragments, stated exactly.**

- **Pure first-order logic with equality.** Universal formulas over uninterpreted symbols: fair instantiation over the Herbrand universe is *refutationally* complete. It finds every refutation, but it is only a semi-decision procedure.
- **The Bernays-Schönfinkel class (EPR).** Formulas $\exists \bar x\, \forall \bar y.\, \varphi$, where $\varphi$ is quantifier-free and uses only predicate symbols, equality and constants, with no function symbol of arity 1 or more. Skolemization adds only constants, so the Herbrand universe is the finite set of constants. Instantiating $\bar y$ with all tuples of constants gives an equisatisfiable ground formula. So instantiation *decides* this class.
- **The essentially uninterpreted fragment.** Ge and de Moura call a formula essentially uninterpreted when every quantified variable occurs only as an argument of uninterpreted function or predicate symbols, never under an interpreted symbol such as $+$ or $\le$. For such formulas they compute, for each variable, a set of ground terms, such that the formula is satisfiable exactly when its instances over these sets are satisfiable. When the sets are finite, model-based instantiation decides the formula; otherwise it is refutationally complete. They extend the fragment with some arithmetic literals on variables.
- **Quantified linear arithmetic.** Reynolds, King and Kuncak give instantiation strategies, guided by models of the negated body, that terminate on linear real and linear integer arithmetic. These are decision procedures, much like [quantifier elimination](/quantifier-elimination/) done lazily.

**E-matching is incomplete.** The facts $g(a) = g(b)$ and $a \ne b$ with the axiom $\forall x.\, f(g(x)) = x$ are unsatisfiable. With the trigger $f(g(x))$, E-matching makes no instance, because the problem has no term with $f$, so the solver can only answer "unknown". The trigger $g(x)$ finds the refutation. Even in EPR, a trigger that does not fit the ground terms can miss instances. And with a trigger such as $f(x)$ for $\forall x.\, f(x) = f(g(x))$, each instance creates a new match, which is a *matching loop*. The SMT-LIB standard treats patterns only as "heuristic information" for solvers (Section 3.6.5).

## Examples

**A refutation with one instance.** Take $\forall x.\, f(x) > x$ with the ground fact $f(a) \le a$, over integer arithmetic with an uninterpreted $f$. The instance for $a$ is $f(a) > a$, and the ground problem $f(a) > a \wedge f(a) \le a$ is unsatisfiable. With the trigger $f(x)$, E-matching finds this instance at once, because $f(a)$ is in the e-graph.

**EPR decided by instantiation.** Take $\forall y.\, P(y) \rightarrow Q(y)$, $P(c)$ and $\neg Q(d)$. The constants are $c$ and $d$, so the instances are $P(c) \rightarrow Q(c)$ and $P(d) \rightarrow Q(d)$. The ground problem is satisfiable, with $P(c)$, $Q(c)$, $\neg P(d)$ and $\neg Q(d)$, and because the formula is in EPR this proves that the original formula is satisfiable. If $\neg Q(c)$ is added, the first instance gives a conflict.

**Satisfiable, but E-matching cannot say so.** Take $\forall x.\, f(x) > 0$ with $f(a) = b$. The trigger $f(x)$ gives the instance $f(a) > 0$, and then E-matching has nothing new to try. The ground problem is satisfiable, but this does not show that the quantified formula is, because other instances were never tried. Model-based instantiation builds a candidate model, for example $b = 1$ and $f$ equal to 1 everywhere, checks $\forall x.\, f(x) > 0$ in it, finds no counterexample, and answers SAT.

**Triggers in SMT-LIB.** The standard writes triggers as `:pattern` attributes on the body of a quantified formula, for example `(forall ((x Int)) (! (> (f x) x) :pattern ((f x))))`. A solver that uses E-matching instantiates the body with the terms that a match assigns to the variables (footnote 7 of Section 3.6.5).

## Where it is used

- **Program verification.** Verifiers such as Boogie, Dafny and F* produce verification conditions with many quantified axioms, for heaps, sequences, sets and user-defined functions. They rely on E-matching, and the authors of the axioms write triggers to control it.
- **SMT-LIB logics with quantifiers.** Logics such as UFLIA and AUFLIRA, without the QF_ prefix, allow quantifiers. Solvers combine several strategies: conflict-based first, then E-matching, then model-based or enumerative instantiation.
- **Synthesis.** Counterexample-guided instantiation for arithmetic is the core of the approach of cvc5 to [syntax-guided synthesis](/syntax-guided-synthesis/) for some problem classes, and it follows the same loop as [CEGIS](/cegis/).
- **Theory combination.** [Model-based theory combination](/model-based-theory-combination/) uses the same idea as model-based instantiation: build a candidate model, check it, and learn from the failure.

## References
