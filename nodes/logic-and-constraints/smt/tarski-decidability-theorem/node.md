---
tag: 89SMFE
kind: theorem
slug: tarski-decidability-theorem
name: Tarski's decidability theorem
aliases:
- Tarski-Seidenberg theorem
- decidability of real closed fields
- quantifier elimination for real closed fields
area: logic-and-constraints/smt
level: advanced
summary: The first-order theory of real closed fields, including real arithmetic, is decidable.
prereqs: [real-closed-field, quantifier-elimination, decidable-language]
see_also: [tarski-seidenberg-theorem, cylindrical-algebraic-decomposition, nonlinear-real-arithmetic-satisfiability, presburger-arithmetic, semialgebraic-set, sturm-theorem, hilberts-tenth-problem, delta-satisfiability]
sources:
  - paper: "Alfred Tarski, A Decision Method for Elementary Algebra and Geometry, RAND Corporation, 1948; second edition, University of California Press, 1951"
    locator: the main theorem (elimination of quantifiers for elementary algebra) and its consequences for geometry
  - paper: "A. Seidenberg, A new decision method for elementary algebra, Annals of Mathematics 60 (1954), 365 to 374"
    locator: the simpler proof of the elimination (page numbers to be checked)
  - paper: doi:10.1007/3-540-07407-4_17
    title: George E. Collins, Quantifier elimination for real closed fields by cylindrical algebraic decomposition, Automata Theory and Formal Languages, Lecture Notes in Computer Science 33 (1975), 134 to 183
    locator: the algorithm and its doubly exponential bound
  - paper: "James H. Davenport and Joos Heintz, Real quantifier elimination is doubly exponential, Journal of Symbolic Computation 5 (1988), 29 to 35"
    locator: the lower bound on the size of quantifier-free equivalents
  - paper: "Michael J. Fischer and Michael O. Rabin, Super-exponential complexity of Presburger arithmetic, Complexity of Computation, SIAM-AMS Proceedings 7 (1974), 27 to 41"
    locator: the exponential lower bound for the theory of the reals with addition
  - paper: "Michael Ben-Or, Dexter Kozen and John Reif, The complexity of elementary algebra and geometry, Journal of Computer and System Sciences 32 (1986), 251 to 264"
    locator: the decision of the theory in exponential space (to be checked)
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 2, Real Closed Fields (the Tarski-Seidenberg principle and quantifier elimination), and Chapter 11 (cylindrical decomposition)
  - book: isbn:9780387987606
    title: David Marker, Model Theory, An Introduction, Graduate Texts in Mathematics 217, Springer, 2002
    locator: Chapter 3, the section on real closed fields (quantifier elimination and completeness)
---

Tarski's decidability theorem states that the first-order theory of the real numbers with addition, multiplication and order is decidable. The reason is that this theory, the theory of [real closed fields](/real-closed-field/), admits [quantifier elimination](/quantifier-elimination/): each formula is equivalent to a computable formula without quantifiers. It makes satisfiability of polynomial constraints over the reals, [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/), decidable, in contrast with polynomial constraints over the integers. The geometric form of the same result, that projections of [semialgebraic sets](/semialgebraic-set/) are semialgebraic, has its own page, the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/).

## Statement

Let the language of ordered rings have the symbols $0, 1, +, -, \cdot, <$. A *real closed field* is an ordered field in which each positive element has a square root and each polynomial of odd degree has a root. RCF is the set of these axioms.

**Theorem (Tarski 1948; Seidenberg 1954).**

1. *Quantifier elimination.* For each first-order formula $\varphi(y_1, \ldots, y_k)$ of the language of ordered rings there is a quantifier-free formula $\psi(y_1, \ldots, y_k)$ such that $\mathrm{RCF} \vdash \forall y\, (\varphi \leftrightarrow \psi)$. Moreover, $\psi$ can be computed from $\varphi$.
2. *Completeness and decidability.* RCF is complete, and the set of sentences that it proves is decidable.
3. *The reals.* The set of first-order sentences true in $(\mathbb{R}, 0, 1, +, -, \cdot, <)$ is decidable, and it equals the set of sentences that RCF proves.

## In plain words

Take any question about real numbers that uses only plus, times, comparisons, "and", "or", "not", "for all" and "there exists". For example: "does every polynomial of degree three with these coefficients have a real root?" A computer can answer each such question correctly.

The method removes the "for all" and "there exists" parts one at a time. Each step replaces a question about some unknown number by a condition on the remaining numbers that uses no unknown. In the end only plain arithmetic on known numbers is left. The method is slow on large questions, but it always ends.

## Proof

Parts 2 and 3 follow from part 1 with a short argument. Part 1 is long, and we give a proof sketch, with a locator for the full proof.

**From 1 to 2 and 3.** Let $\varphi$ be a sentence and $\psi$ its quantifier-free equivalent from part 1. $\psi$ has no variables, so it is a Boolean combination of comparisons between terms built from $0$ and $1$. Each ordered field contains the rationals with their usual order, and such a term has the same rational value in each ordered field. So $\psi$ is true in all real closed fields or false in all of them, and we can compute which by evaluating it. Hence RCF proves $\varphi$ or proves $\neg \varphi$, so RCF is complete, and computing $\psi$ and then evaluating it decides $\varphi$. The field $\mathbb{R}$ is real closed, by the intermediate value theorem. So a sentence true in $\mathbb{R}$ is not refuted by RCF, and by completeness RCF proves it. $\square$

**Proof sketch of part 1 (the method of Cohen and Hörmander).** The full proof is in Basu, Pollack and Roy (2006), Chapter 2, and in Marker (2002), Chapter 3.

1. *One quantifier.* By induction on the formula, it is enough to remove $\exists x$ from $\exists x\, \chi$ with $\chi$ quantifier-free; $\forall x$ is $\neg \exists x \neg$. Write $\chi$ in disjunctive normal form, and move $\exists x$ inside the disjunction. Each atom is equivalent to $p(x, y) \mathrel{\sigma} 0$ with $\sigma \in \{<, =, >\}$ and $p$ a polynomial with integer coefficients. So the task is a conjunction of sign conditions on polynomials $p_1, \ldots, p_r$ in $x$, whose coefficients are polynomials in $y$.
2. *Fix the degrees.* Split into finitely many cases by the signs of the coefficients in $y$, a quantifier-free condition on $y$. In each case each $p_i$ has a known degree and a leading coefficient with a known sign.
3. *Sign tables.* For a list $P$ of polynomials in $x$, let the *sign table* be the list of sign vectors of $P$ at the real roots of the nonzero members of $P$, in increasing order, and on the open intervals between them and beyond them. The key lemma says that the sign table of $P$ is determined by the sign table of a list $P^*$ with a smaller sum of degrees: remove a member $p$ of largest degree, and add its derivative $p'$ and the remainders of $p$ by the other members and by $p'$ (with the leading coefficients known to be nonzero, so the division is defined). At a root $\xi$ of another member $q$, $p(\xi)$ equals the remainder of $p$ by $q$ at $\xi$. Between two consecutive points of the table of $P^*$, $p'$ has a constant sign, so $p$ is monotone there, and the intermediate value theorem for polynomials, which holds in each real closed field, tells from the signs at the two ends whether $p$ has a root inside. The sign of $p$ near $\pm\infty$ comes from its degree and leading coefficient.
4. *Induction.* By induction on the sum of degrees, the sign table of $P$ is a computable function of the signs of finitely many polynomials in $y$. For each of the finitely many sign assignments to these polynomials, the table, and so the truth of $\exists x$ (a conjunction of sign conditions), is fixed. The disjunction of the sign assignments that make it true is the quantifier-free equivalent. $\square$

## Consequences

- **Nonlinear real arithmetic is decidable.** Satisfiability of a quantifier-free formula of polynomial constraints is the truth of its existential closure, so [QF_NRA](/nonlinear-real-arithmetic-satisfiability/) is decidable, and so is the quantified version.
- **Elementary geometry.** Tarski's elementary Euclidean geometry translates into the theory of real closed fields with coordinates, so it is decidable too.
- **Projection.** A set defined by a formula with quantifiers is defined by one without, so projections of semialgebraic sets are semialgebraic: the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/) in its geometric form.
- **Transfer.** A first-order sentence true in $\mathbb{R}$ is true in every real closed field, for example the field of real algebraic numbers.
- **Algorithms.** [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) (Collins 1975) is the first practical method. For $m$ polynomials of degree at most $d$ in $n$ variables, its cost is bounded by $(m d)^{2^{O(n)}}$ times a polynomial in the coefficient sizes. The existential part, the existential theory of the reals, is in PSPACE (Canny 1988).

## Tightness

- **Doubly exponential elimination.** Davenport and Heintz (1988) gave formulas with $O(n)$ quantifiers whose quantifier-free equivalents need polynomials of degree doubly exponential in $n$. So each quantifier elimination method, CAD included, has a doubly exponential worst case in the output size.
- **Decision is at least exponential.** Fischer and Rabin (1974) proved that some sentences of length $n$ about $(\mathbb{R}, +, <)$ alone need nondeterministic time $2^{c n}$ for a constant $c > 0$. These sentences are also sentences of the full language, with the same truth value in $\mathbb{R}$, so the bound holds for the full theory. The best known upper bound for the decision problem, exponential space (Ben-Or, Kozen and Reif 1986), leaves a gap.
- **The hypothesis "real closed" is needed.** Over the integers, the same language gives an undecidable theory (Gödel, Church), and even its existential part is undecidable by [Hilbert's tenth problem](/hilberts-tenth-problem/). Over the rationals the theory is also undecidable (Julia Robinson 1949).
- **Adding sine breaks it.** With the function $\sin$, the integers are definable: $\pi$ is the least positive zero of $\sin$, and $\mathbb{Z} = \{x : \sin(\pi x) = 0\}$. So the theory of $(\mathbb{R}, +, \cdot, <, \sin)$ interprets the arithmetic of the integers and is undecidable. With the exponential function, decidability is known only under Schanuel's conjecture (Macintyre and Wilkie 1996). [δ-satisfiability](/delta-satisfiability/) is a weaker question that stays decidable for such functions on bounded domains.

## History

Tarski found the decision method around 1930 and published it in a RAND report in 1948, with a second edition in 1951. Seidenberg gave a simpler proof in 1954, and the proof was simplified again by Paul Cohen and by Hörmander. Tarski's original procedure is usually described as having no elementary bound on its running time. Collins introduced cylindrical algebraic decomposition in 1975, the first method with a doubly exponential bound, and it is the basis of many later tools.

## References
