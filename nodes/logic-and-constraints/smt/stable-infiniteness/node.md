---
tag: TGJ8QB
kind: definition
slug: stable-infiniteness
name: Stable infiniteness
aliases:
- stably infinite theory
- stably infinite
area: logic-and-constraints/smt
level: advanced
summary: A theory is stably infinite if every quantifier-free formula that is satisfiable in it is also satisfiable in one of its models with an infinite domain. Nelson-Oppen needs it for completeness.
prereqs: [smt-problem]
see_also: [nelson-oppen, convex-theory, model-based-theory-combination, shostak-combination, bit-vector-satisfiability, euf-satisfiability, decision-procedure]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.6.1, Definition 33.6.1 (stably infinite theory), Proposition 33.6.2, and the text after it on the error in the 1979 completeness proof and on non-stably infinite theories
  - paper: doi:10.1016/0304-3975(80)90059-6
    title: Derek C. Oppen, Complexity, convexity and combinations of theories, Theoretical Computer Science 12(3), 1980, pages 291 to 302
    locator: the first correct proof of the combination result, under the condition of stable infiniteness
  - paper: doi:10.1007/s10817-005-5204-9
    title: Cesare Tinelli and Calogero G. Zarba, Combining nonstably infinite theories, Journal of Automated Reasoning 34(3), 2005, pages 209 to 238
    locator: an example showing that Nelson-Oppen is incomplete without stable infiniteness, and a method that combines a non-stably infinite theory with a shiny one
  - paper: doi:10.1007/3-540-45988-x_11
    title: Clark W. Barrett, David L. Dill and Aaron Stump, A generalization of Shostak's method for combining decision procedures, FroCoS 2002, LNAI 2309, pages 132 to 146
    locator: a convex theory with no trivial models is stably infinite
  - paper: doi:10.1007/11559306_3
    title: Silvio Ranise, Christophe Ringeissen and Calogero G. Zarba, Combining data structures with nonstably infinite theories using many-sorted logic, FroCoS 2005, LNAI 3717, pages 48 to 64
    locator: polite theories, and stable infiniteness for each sort
  - paper: doi:10.1007/978-3-642-16242-8_29
    title: Dejan Jovanović and Clark Barrett, Polite theories revisited, LPAR 2010, LNCS 6397, pages 402 to 416
    locator: strong politeness, a corrected condition for polite combination
---

Stable infiniteness is the condition on the component theories under which the [Nelson-Oppen](/nelson-oppen/) combination method is complete. A theory is stably infinite when no quantifier-free formula can force its models to be finite: whenever such a formula is satisfiable in the theory, it is also satisfiable in a model with infinitely many elements. Equality with uninterpreted functions and linear arithmetic over the integers or the reals have this property. Theories with a bound on the size of their models, such as fixed-width bit-vectors, do not. The 1979 completeness proof of Nelson and Oppen tacitly assumed it, and Oppen made the condition explicit in 1980.

## Definition

Let $\Sigma$ be a signature and $C$ an infinite set of constants not in $\Sigma$. A $\Sigma$-theory $T$ is **stably infinite** if every $T$-satisfiable ground formula of signature $\Sigma \cup C$ is satisfiable in a model of $T$ with an infinite universe (Handbook, Definition 33.6.1).

Remarks on the definition.

- *Ground formulas only.* The constants of $C$ play the role of the free variables of a quantifier-free formula. Quantified formulas are not part of the condition: the theory may contain axioms that are true only in finite models of some formulas with quantifiers, as long as no ground formula can force a finite model.
- *Some infinite model, not all.* The condition asks for one infinite model of the formula. It does not say that all models are infinite, and it does not say that there are models of every infinite size. For a countable signature, the downward Löwenheim-Skolem theorem gives a countably infinite model whenever there is an infinite one, so "infinite" can be read as "countably infinite".
- *Conjunctions suffice.* A ground formula is satisfiable exactly when one disjunct of its disjunctive normal form is, so it is enough to check conjunctions of literals.
- *Many sorts.* In a many-sorted logic, as in SMT-LIB, the condition is stated for each sort: a theory is stably infinite with respect to a set of sorts if every satisfiable quantifier-free formula has a model in which these sorts are infinite.

**Why Nelson-Oppen needs it.** The combination method guesses an *arrangement* of the shared variables, an equivalence relation on them, and asks each solver whether its part of the formula is satisfiable together with the arrangement. If both say yes, the two models agree on the number of distinct shared values, but they may still differ in the size of their universes. When both models can be taken infinite and countable, they have the same size, and a bijection glues them into one model of the combined theory. If one theory forces a finite universe, no such bijection may exist, and the method can answer "satisfiable" for an unsatisfiable formula. The [Nelson-Oppen](/nelson-oppen/) page gives the proof and a counterexample.

## Examples and non-examples

- **EUF is stably infinite.** The theory of equality with uninterpreted functions has no axioms besides those of equality. Take any model $M$ of a ground formula $\varphi$, add infinitely many new elements, and define each function on the new arguments in any way. The values of the ground terms of $\varphi$ do not change, so $\varphi$ is still true, and the model is infinite.
- **Linear arithmetic is stably infinite.** Every model of the theory of the integers, or of the reals, is infinite, so every satisfiable formula has an infinite model.
- **A theory with at most two elements is not.** The theory $T_{\le 2}$ with the axiom $\forall x\, y\, z.\ x = y \vee x = z \vee y = z$ has only models with one or two elements. The formula $a = a$ is satisfiable in it but has no infinite model.
- **Fixed-width bit-vectors are not.** For a fixed width $w$, the bit-vector theory has one model per sort, with $2^w$ elements. The Handbook notes that the theory of any single finite model is not stably infinite, and gives bit-vectors and strings of bounded size as examples.
- **A theory with infinite models can still fail.** Let $\Sigma = \{P\}$ with a unary predicate $P$, and let $T$ have the axiom $\forall w\, x\, y\, z.\ \neg P(w) \vee x = y \vee x = z \vee y = z$. The structure on the natural numbers with $P$ empty is an infinite model. But the ground formula $P(c)$ is satisfiable only in models with at most two elements. So $T$ has infinite models, but it is not stably infinite.
- **Convex theories.** A [convex](/convex-theory/) theory with no model of size one is stably infinite (Barrett, Dill and Stump, 2002). The [convex theory](/convex-theory/) page gives the proof. This covers EUF and linear real arithmetic, but not linear integer arithmetic, which is not convex and is stably infinite for the simpler reason above.

## Related definitions

- [Convex theory](/convex-theory/): a theory in which a conjunction that entails a disjunction of equalities entails one of them. Convexity makes Nelson-Oppen deterministic; stable infiniteness makes it complete.
- [Nelson-Oppen](/nelson-oppen/): the combination method whose completeness depends on this property. [Model-based theory combination](/model-based-theory-combination/) and [Shostak's method](/shostak-combination/) make the same assumption for the theories that they combine.
- **Shiny theories** (Tinelli and Zarba): theories in which the possible sizes of the models of each formula can be computed. A shiny theory can be combined with an arbitrary theory, at the cost of exchanging cardinality constraints in addition to equalities.
- **Polite and strongly polite theories** (Ranise, Ringeissen and Zarba; Jovanović and Barrett): a many-sorted condition that is easier to check for data structure theories such as lists and arrays. A polite theory can be combined with any theory, if the method also guesses equalities among some extra terms. Jovanović and Barrett found that the first definition was too weak for the proof, and gave strong politeness.
- [Decision procedure](/decision-procedure/): Nelson-Oppen turns decision procedures for two stably infinite theories into one for their union.

## References
