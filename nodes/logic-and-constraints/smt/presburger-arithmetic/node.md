---
tag: XNEW3K
kind: definition
slug: presburger-arithmetic
name: Presburger arithmetic
aliases:
- Presburger logic
- linear integer arithmetic with quantifiers
- first-order theory of the integers with addition
area: logic-and-constraints/smt
level: advanced
summary: First-order theory of the natural numbers with addition, decidable by quantifier elimination.
prereqs: [linear-integer-arithmetic-satisfiability, quantifier-elimination]
see_also: [omega-test, tarski-decidability-theorem, hilberts-tenth-problem, linear-real-arithmetic-satisfiability, decision-procedure, quantifier-instantiation, buchi-automaton, nexptime]
sources:
  - paper: "Mojżesz Presburger, Über die Vollständigkeit eines gewissen Systems der Arithmetik ganzer Zahlen, in welchem die Addition als einzige Operation hervortritt, Comptes Rendus du I Congrès de Mathématiciens des Pays Slaves, Warsaw, 1929 (published 1930)"
    locator: the quantifier elimination and the completeness of the theory (page numbers not checked)
  - paper: "D. C. Cooper, Theorem proving in arithmetic without multiplication, Machine Intelligence 7, Edinburgh University Press, 1972, pages 91 to 99"
    locator: the elimination of one existential quantifier with a finite set of test points (page numbers to be checked)
  - paper: "Michael J. Fischer and Michael O. Rabin, Super-exponential complexity of Presburger arithmetic, Complexity of Computation, SIAM-AMS Proceedings 7 (1974), 27 to 41"
    locator: the doubly exponential lower bound, for nondeterministic machines
  - paper: "Derek C. Oppen, A 2^2^2^pn upper bound on the complexity of Presburger arithmetic, Journal of Computer and System Sciences 16(3) (1978), 323 to 332"
    locator: the analysis of Cooper's procedure
  - paper: "Leonard Berman, The complexity of logical theories, Theoretical Computer Science 11 (1980)"
    locator: the exact complexity in terms of alternating machines (to be checked)
  - paper: "Seymour Ginsburg and Edwin H. Spanier, Semigroups, Presburger formulas, and languages, Pacific Journal of Mathematics 16 (1966)"
    locator: the definable sets are the semilinear sets
  - book: isbn:9783540741121
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Springer, 2007
    locator: Chapter 7, Quantified Linear Arithmetic (Cooper's method, with the proof of its main step)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 9, Quantified Formulas
---

Presburger arithmetic is the first-order theory of the natural numbers (or of the integers) with addition and order, but without multiplication of variables. Presburger proved in 1929 that it is decidable, by [quantifier elimination](/quantifier-elimination/), in contrast with arithmetic with multiplication, which is undecidable. Its decision problem is very hard: Fischer and Rabin (1974) proved a doubly exponential lower bound. Its quantifier-free and existential part is [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), which is only NP-complete, and the [omega test](/omega-test/) and Cooper's method are classic algorithms for it.

## Definition

**Language.** The constants $0$ and $1$, the function $+$, the relations $=$ and $<$, the connectives, and the quantifiers $\forall$ and $\exists$. Multiplication by a fixed numeral is an abbreviation: $3x$ is $x + x + x$. A product of two variables, such as $x \cdot y$, is not in the language.

**Presburger arithmetic** is the set of sentences of this language that are true in $(\mathbb{N}, 0, 1, +, <)$. The version over $(\mathbb{Z}, 0, 1, +, <)$ has the same decidability and complexity results; the two interpret each other, since a natural number is an integer $x \ge 0$ and an integer is a difference of two naturals.

**Quantifier elimination needs divisibility.** The formula $\exists y\, (x = y + y)$ says that $x$ is even, and no quantifier-free formula in the language above says it. So the elimination works in the language extended with the predicates $k \mid t$ ("$k$ divides $t$") for each fixed numeral $k \ge 1$. With them, each formula is equivalent to a quantifier-free one (Presburger 1929). Since a quantifier-free sentence has no variables and can be evaluated, the theory is decidable.

**Cooper's step (Cooper 1972).** Let $\varphi(x)$ be a quantifier-free formula over $\mathbb{Z}$ in negation normal form, where each literal that contains $x$ has one of the forms $x < t$, $t < x$, $k \mid x + t$ or $\neg(k \mid x + t)$, with $t$ free of $x$. (Equalities become two inequalities, a negated $x < t$ becomes $t - 1 < x$, and a coefficient $h$ on $x$ is removed by multiplying all literals up to the least common multiple $\ell$ of the coefficients, renaming $\ell x$ to $x$, and adding $\ell \mid x$.) Let $\delta$ be the least common multiple of the $k$ in the divisibility literals, $B$ the set of terms $t$ in the literals $t < x$, and $\varphi_{-\infty}$ the formula $\varphi$ with each $x < t$ replaced by true and each $t < x$ by false. Then
$$\exists x\, \varphi(x) \iff \bigvee_{j=1}^{\delta} \varphi_{-\infty}(j) \;\vee\; \bigvee_{j=1}^{\delta} \bigvee_{t \in B} \varphi(t + j).$$

*Proof.* For $x$ below all terms $t$, $\varphi(x)$ and $\varphi_{-\infty}(x)$ agree, and $\varphi_{-\infty}$ has period $\delta$ in $x$, so a true $\varphi_{-\infty}(j)$ gives a model $x = j - N\delta$ for a large $N$. A true $\varphi(t + j)$ is a model. Conversely, let $\varphi(x_0)$ hold and suppose no $\varphi(t + j)$ holds. Each literal true at $x_0$ stays true at $x_0 - \delta$: this is clear for $x < t$ and for divisibility, and if $t < x_0$ but not $t < x_0 - \delta$, then $x_0 = t + j$ with $1 \le j \le \delta$, which we excluded. As $\varphi$ is in negation normal form, $\varphi(x_0 - \delta)$ holds, and so does $\varphi(x_0 - N\delta)$ for each $N$. For large $N$ this is $\varphi_{-\infty}(x_0 - N\delta) = \varphi_{-\infty}(j)$ with $j \equiv x_0 \pmod \delta$, $1 \le j \le \delta$. $\square$

Applying the step to the innermost quantifier, and $\forall x$ as $\neg \exists x \neg$, removes all quantifiers.

**Complexity.** Let $n$ be the length of a sentence.

- **Lower bound (Fischer and Rabin 1974).** There is a constant $c > 0$ such that each decision procedure for Presburger arithmetic, even a nondeterministic one, needs more than $2^{2^{c n}}$ steps on some sentences of length $n$, for all large $n$.
- **Upper bound (Oppen 1978).** Cooper's procedure decides a sentence of length $n$ in deterministic time $2^{2^{2^{p n}}}$ for a constant $p$.
- **Exact class.** Berman (1980) showed that the theory is complete for a class of alternating machines with doubly exponential time and a linear number of alternations; this placement is quoted, not proved here.
- **Fragments.** The existential fragment is equivalent to QF_LIA satisfiability and so is NP-complete. Bounding the number of quantifier alternations lowers the complexity.

## Examples and non-examples

- **True sentences.** $\forall x\, \exists y\, (x = 2y \vee x = 2y + 1)$: each number is even or odd. Over $\mathbb{N}$, $\forall x\, (x \ge 12 \to \exists a\, \exists b\, (x = 4a + 5b))$: each number from 12 on is a sum of fours and fives, while 11 is not (a script checked all $x < 200$; the numbers that are not sums are 1, 2, 3, 6, 7 and 11).
- **A false sentence.** Over $\mathbb{N}$, $\forall x\, \forall y\, (x < y \to \exists z\, (x < z \wedge z < y))$: it fails for $y = x + 1$. Over the rationals the same sentence is true, which shows that the domain matters.
- **Cooper's step on an example.** $\exists x\, (3 \mid x + 1 \wedge y < x \wedge x < z)$. Here $\delta = 3$, $B = \{y\}$, and $\varphi_{-\infty}$ is false, so the formula is equivalent to $\bigvee_{j=1}^{3} (3 \mid y + j + 1 \wedge y + j < z)$. A script checked this equivalence for all $y, z$ in $[-6, 6]$.
- **Defined sets.** The sets of tuples definable in Presburger arithmetic are exactly the semilinear sets, finite unions of sets $\{v_0 + k_1 v_1 + \cdots + k_r v_r : k_i \in \mathbb{N}\}$ (Ginsburg and Spanier 1966).
- **Non-example: multiplication.** With $\cdot$ in the language, the theory of $(\mathbb{N}, +, \cdot)$ is undecidable, and so is its existential part, by the solution of [Hilbert's tenth problem](/hilberts-tenth-problem/) (Matiyasevich 1970).
- **Non-example: the reals.** The theory of $(\mathbb{R}, +, <)$, or of $(\mathbb{R}, +, \cdot, <)$, is a different theory. It is decidable by [Tarski's theorem](/tarski-decidability-theorem/), and it needs no divisibility predicates.

## Related definitions

- [Linear integer arithmetic](/linear-integer-arithmetic-satisfiability/) is the quantifier-free fragment, as an SMT decision problem. It is NP-complete, much easier than the full theory.
- The [omega test](/omega-test/) decides conjunctions of linear constraints over the integers, and its projections eliminate existential quantifiers, so it can serve as a Presburger procedure.
- [Quantifier elimination](/quantifier-elimination/) is the general method; Cooper's step above is the version for this theory.
- Automata give another decision procedure: write numbers in binary, and each formula defines a regular language of tuples, built from automata for addition and closed under the Boolean operations and projection. The idea goes back to Büchi's work on [automata](/buchi-automaton/) and weak monadic logic.
- In SMT solvers, quantified LIA formulas are often handled by [quantifier instantiation](/quantifier-instantiation/) instead of full elimination.

## References
