---
tag: 5KDCPP
kind: problem
slug: entscheidungsproblem
name: Entscheidungsproblem
aliases:
- decision problem for first-order logic
area: complexity/computability
level: advanced
summary: Hilbert's question of whether an algorithm can decide if a first-order sentence is valid. Church and Turing showed in 1936 that no such algorithm exists.
prereqs: [halting-problem, church-turing-thesis]
see_also: [church-theorem, halting-problem, church-turing-thesis, godel-incompleteness-theorem, first-order-theorem-proving, wang-tiling-problem, presburger-arithmetic, sat]
sources:
  - title: David Hilbert and Wilhelm Ackermann, Grundzüge der theoretischen Logik, Springer, 1928
  - paper: doi:10.2307/2269326
    title: Alonzo Church, A note on the Entscheidungsproblem, Journal of Symbolic Logic 1(1) (1936)
    locator: pp. 40 to 41
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 11, Application to the Entscheidungsproblem
  - paper: doi:10.1007/BF01696781
    title: Kurt Gödel, Die Vollständigkeit der Axiome des logischen Funktionenkalküls, Monatshefte für Mathematik und Physik 37 (1930)
    locator: pp. 349 to 360
  - paper: doi:10.1073/pnas.48.3.365
    title: A. S. Kahr, Edward F. Moore and Hao Wang, Entscheidungsproblem reduced to the AEA case, Proceedings of the National Academy of Sciences 48(3) (1962)
    locator: pp. 365 to 377
  - book: isbn:9783540570738
    title: Egon Börger, Erich Grädel and Yuri Gurevich, The Classical Decision Problem, Perspectives in Mathematical Logic, Springer, 1997
    locator: the chapter The Classical Decision Problem
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, Modelling and Reasoning about Systems, second edition, Cambridge University Press, 2004
    locator: Section 2.5, Undecidability of predicate logic
---

The Entscheidungsproblem, German for "decision problem", asks for an algorithm that takes a sentence of first-order logic and decides whether it is valid, that is, true in every structure. David Hilbert and Wilhelm Ackermann stated it in their 1928 textbook and called it a main problem of mathematical logic. An algorithm of this kind would settle every mathematical question that can be written as "these axioms imply this statement". In 1936 Alonzo Church and Alan Turing, independently, showed that no such algorithm exists. To do so they first had to say exactly what an algorithm is, and the [Church-Turing thesis](/church-turing-thesis/) came out of this work. The theorem that answers the problem is [Church's theorem](/church-theorem/); this page is about the problem, its variants and the parts of it that are decidable.

## In plain words

Mathematicians write their claims in a precise language with "for all", "there exists", "and", "or" and "not". Hilbert asked for a mechanical method that reads any claim in this language and tells whether it follows from pure logic, true however its words are read.

Such a method would turn much of mathematics into calculation. To check whether some axioms imply a theorem, you would feed the statement "axioms imply theorem" to the method.

Church and Turing proved that the method cannot exist. Turing did it by first describing what any mechanical method can do, as a simple machine, and then showing that claims in logic can describe such machines. A method for logic would then predict whether any machine stops, which is impossible.

## Definition

**Instance.** A sentence $\varphi$ of first-order logic, over a finite vocabulary of constant, function and relation symbols.

**Question.** Is $\varphi$ valid, that is, true in every structure for its vocabulary?

The dual form asks whether $\varphi$ is *satisfiable*, true in some structure. A sentence is valid if and only if its negation is not satisfiable, so the two forms reduce to each other. Hilbert and Ackermann stated both.

**Answer.** No algorithm exists (Church 1936, Turing 1936). By Gödel's completeness theorem (1930), the valid sentences are the provable ones, so validity is computably enumerable (c.e.), and satisfiability is co-c.e. Validity is complete for the c.e. sets under many-one reductions. The proof by reduction from the Post correspondence problem is on the page [Church's theorem](/church-theorem/).

## Variants

- **Finite satisfiability.** Does $\varphi$ have a finite model? This is c.e., by listing finite structures, and Trakhtenbrot proved in 1950 that it is undecidable.
- **Prefix classes.** Restrict to prenex sentences with a given pattern of quantifiers. Without function symbols, satisfiability is decidable for the class $\exists^* \forall^*$ of Bernays and Schönfinkel, for Ackermann's class $\exists^* \forall \exists^*$, and for sentences with only unary relation symbols. It is undecidable for the class $\forall \exists \forall$ (Kahr, Moore and Wang 1962). Börger, Grädel and Gurevich give the full map of decidable and undecidable classes.
- **Theories.** Validity relative to a set of axioms, or truth in one structure. Some theories are decidable, such as [Presburger arithmetic](/presburger-arithmetic/) and the [theory of real closed fields](/tarski-decidability-theorem/). Others, such as the theory of $(\mathbb{N}, +, \times)$, are undecidable.
- **Propositional logic.** Without quantifiers the problem is [satisfiability](/sat/), which is decidable and NP-complete.
- **Higher-order logic.** Second-order validity is not even c.e., since second-order logic has no complete proof system.

## Examples

**A valid sentence.** $\forall x\, P(x) \to \exists x\, P(x)$ is valid, because structures in first-order logic have at least one element.

**A sentence that is not valid.** $\exists x\, P(x) \to \forall x\, P(x)$ fails in the structure with two elements $a$ and $b$ where $P$ holds of $a$ only.

**Satisfiable, but only in infinite structures.** The sentence
$$\forall x\, \neg R(x, x) \ \wedge\ \forall x\, \forall y\, \forall z\, \big(R(x, y) \wedge R(y, z) \to R(x, z)\big) \ \wedge\ \forall x\, \exists y\, R(x, y)$$
says that $R$ is a strict order with no largest element. The natural numbers with $<$ satisfy it. A finite strict order has a maximal element, so no finite structure satisfies it. A search through finite structures therefore cannot show that every satisfiable sentence is satisfiable.

**A sentence that codes a tile puzzle.** The PCP instance $[1 / 11]$, $[10 / 0]$ has the match $1, 2$: both rows spell $110$. Floyd's construction on the [Church's theorem](/church-theorem/) page turns it into a sentence with the parts
$$P\big(f_1(e),\, f_1(f_1(e))\big) \wedge P\big(f_0(f_1(e)),\, f_0(e)\big)$$
and
$$\forall v\, \forall w\, \big(P(v, w) \to P(f_1(v), f_1(f_1(w))) \wedge P(f_0(f_1(v)), f_0(w))\big),$$
which together imply $\exists z\, P(z, z)$. Since the instance has a match, this implication is valid.

## Known algorithms

- **Proof search.** List all proofs in a complete proof system and stop when one proves $\varphi$. It halts exactly on the valid sentences.
- **Resolution and tableaux.** Practical [first-order provers](/first-order-theorem-proving/) negate $\varphi$, put it in clause form by [Skolemization](/skolemization/), and search for a refutation. Resolution is refutation complete: if $\varphi$ is valid, the search finds a refutation of $\neg \varphi$. It need not halt otherwise.
- **Model search.** List finite structures and stop when one satisfies $\neg \varphi$. This halts on sentences that have a finite countermodel. Run alongside proof search, it settles every sentence that is valid or has a finite countermodel, but not those whose countermodels are all infinite.
- **Decision procedures for fragments.** The decidable prefix classes, the monadic class and decidable theories have their own algorithms, used in SMT solvers and description logics.

## Bounds

- **Undecidable** for full first-order logic, already with one binary relation symbol, and already for the prefix class $\forall \exists \forall$.
- **Semi-decidable.** Validity is c.e. and complete for the c.e. sets; satisfiability is not c.e.
- **Decidable fragments** can still be hard. Propositional satisfiability is NP-complete, and the decidable first-order classes have higher complexity; see Börger, Grädel and Gurevich.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **From halting.** Turing coded the run of a machine into a sentence that is valid if and only if the machine eventually prints a given symbol.
- **From PCP.** Floyd's construction maps an instance to a sentence that is valid if and only if the instance has a match; see [Church's theorem](/church-theorem/).
- **From tiling.** Kahr, Moore and Wang coded the origin-constrained [Wang tiling problem](/wang-tiling-problem/) into $\forall \exists \forall$ sentences: such a sentence is satisfiable if and only if the tiles cover a quarter of the plane.
- **To halting.** Map $\varphi$ to the program that searches for a proof of $\varphi$.

## Applications

- **Automated reasoning.** Provers for first-order logic are complete but cannot always halt. Their designers add time limits, and they use decidable fragments where termination matters.
- **Language design for logics.** Description logics, modal logics and other logics used in software are chosen to lie inside decidable fragments of first-order logic.
- **Foundations.** The negative answer ended the hope of reducing mathematics to calculation, and the tools built for it, Turing machines and the lambda calculus, became the base of computer science.

## References
