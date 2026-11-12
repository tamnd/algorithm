---
tag: W3D9YN
kind: problem
slug: nonlinear-real-arithmetic-satisfiability
name: Nonlinear real arithmetic satisfiability
aliases:
- nonlinear real arithmetic
- QF_NRA
- existential theory of the reals
area: logic-and-constraints/smt
level: advanced
summary: Decide polynomial constraints over the reals; decidable but expensive.
prereqs: [linear-real-arithmetic-satisfiability, real-closed-field, np-hard]
see_also: [tarski-decidability-theorem, cylindrical-algebraic-decomposition, delta-satisfiability, interval-constraint-propagation, hilberts-tenth-problem, groebner-basis, linear-integer-arithmetic-satisfiability, smt-problem]
sources:
  - paper: doi:10.1007/3-540-07407-4_17
    title: George E. Collins, Quantifier elimination for real closed fields by cylindrical algebraic decomposition, Automata Theory and Formal Languages, Lecture Notes in Computer Science 33 (1975), 134 to 183
    locator: the cylindrical algebraic decomposition and its doubly exponential bound
  - paper: "John Canny, Some algebraic and geometric computations in PSPACE, Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 1988, 460 to 467"
    locator: the existential theory of the reals is in PSPACE (page numbers to be checked)
  - paper: "Dejan Jovanović and Leonardo de Moura, Solving non-linear arithmetic, Automated Reasoning (IJCAR 2012), Lecture Notes in Computer Science 7364, Springer, 2012, 339 to 354"
    locator: the NLSAT procedure, a model-constructing search with CAD-based explanations (page numbers to be checked)
  - paper: "Yuri Matiyasevich, Enumerable sets are Diophantine, Soviet Mathematics Doklady 11 (1970), 354 to 357"
    locator: the main theorem, which makes polynomial constraints over the integers undecidable
  - paper: "Marcus Schaefer, Complexity of some geometric and topological problems, Graph Drawing (GD 2009), Lecture Notes in Computer Science 5849, Springer, 2010"
    locator: the complexity class of the existential theory of the reals and its complete problems
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 11 (cylindrical decomposition) and Chapter 13 (the existential theory of the reals)
---

Nonlinear real arithmetic satisfiability is the problem of deciding whether a Boolean combination of polynomial constraints, such as $x^2 + y^2 \le 1 \wedge x y > 0$, has a model in the real numbers. In SMT-LIB it is the logic QF_NRA, and as a decision problem on conjunctions it is the *existential theory of the reals*. It is decidable by [Tarski's theorem](/tarski-decidability-theorem/), it is [NP-hard](/np-hard/), and it is in PSPACE; the classic complete method, [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/), is doubly exponential in the number of variables. The same constraints over the integers are undecidable.

## In plain words

The unknowns are real numbers, and the rules may multiply unknowns together, as in "x times y is more than 1" or "x squared plus y squared is at most 1". The question is whether some real numbers make all the rules true.

A computer can always answer this question. The difficulty is that the shapes these rules describe can be curved, split into many pieces, and touch only at single points, and a solution may need a number such as the square root of 2 that has no exact decimal form. Correct methods are known, but they slow down very quickly as the number of unknowns grows. With whole numbers instead of real numbers, no correct method exists at all.

## Definition

A *polynomial atom* is $p(x_1, \ldots, x_n) \bowtie 0$, where $p$ has integer (or rational) coefficients and $\bowtie \in \{<, \le, =, \ne, \ge, >\}$. A QF_NRA formula is a Boolean combination of polynomial atoms. The problem asks whether some $x \in \mathbb{R}^n$ makes the formula true. The input size counts the coefficients in binary and the polynomials in dense or sparse form; the analysis below uses $n$ variables, $m$ polynomials and a maximum degree $d$.

A model can need irrational values: the only models of $x^2 = 2$ are $\pm\sqrt{2}$. Solvers report such a value as a *real algebraic number*, a polynomial with integer coefficients together with an isolating interval with rational ends, for example $(x^2 - 2, [1, 2])$. Each satisfiable QF_NRA formula has a model whose coordinates are real algebraic numbers, because the field of real algebraic numbers is real closed and Tarski's theorem transfers the existential sentence to it.

**How this page relates to its neighbours.** [Tarski's theorem](/tarski-decidability-theorem/) is the decidability result for the full first-order theory, with quantifiers. This page is its quantifier-free part, as an SMT problem. [δ-satisfiability](/delta-satisfiability/) is a relaxed question that also allows functions such as $\sin$ and $\exp$. [Linear real arithmetic](/linear-real-arithmetic-satisfiability/) is the special case of degree 1, which is much easier.

## Variants

- **Linear atoms only.** [Linear real arithmetic](/linear-real-arithmetic-satisfiability/): conjunctions are in P.
- **Quantified formulas.** The full theory of real closed fields; decidable by [Tarski's theorem](/tarski-decidability-theorem/), with a doubly exponential cost for quantifier elimination.
- **Integer variables (QF_NIA).** Undecidable: a Diophantine equation $p(x) = 0$ over the integers is a QF_NIA formula, and [Hilbert's tenth problem](/hilberts-tenth-problem/) has no algorithm (Matiyasevich 1970). Solvers handle it with bounds and [bit-blasting](/bit-blasting/), linearization, or branch and bound on top of an NRA solver, and they may answer "unknown".
- **Transcendental functions.** With $\exp$, $\sin$ or $\cos$, the exact problem is undecidable in general (for $\sin$, see [Richardson's theorem](/richardson-theorem/)). [δ-satisfiability](/delta-satisfiability/) is the usual decidable relaxation on bounded domains.
- **One variable.** Decidable in polynomial time, by isolating the real roots with [Sturm sequences](/sturm-sequence/) or Descartes' rule and checking the sign conditions between the roots.

## Examples

Each example was checked by a script, with exact rational arithmetic where the claim is about exact values.

1. **No real model.** $x^2 < 0$ is unsatisfiable, since each square is nonnegative.
2. **An irrational model only.** $x^2 = 2$ is satisfiable over the reals with $x = \sqrt{2}$. It has no rational model and no integer model; the script found no rational $p/q$ with $q < 300$ and $p^2 = 2q^2$, and the classic proof shows that none exists.
3. **A curved region with no linear certificate.** $x^2 + y^2 \le 1 \wedge x + y \ge 2$ is unsatisfiable. From the identity $(x - y)^2 + (x + y)^2 = 2(x^2 + y^2)$ (checked on 1000 random rational points), $x + y \ge 2$ gives $2(x^2 + y^2) \ge 4$, so $x^2 + y^2 \ge 2 > 1$. The largest value of $x + y$ on the disk is $\sqrt{2}$.
4. **A one-variable decomposition.** For $x^2 - 2 < 0 \wedge x - 1 > 0$, the roots $-\sqrt{2}$, $1$ and $\sqrt{2}$ split the real line into seven cells, and the signs are constant on each cell:

| cell | $(-\infty, -\sqrt{2})$ | $-\sqrt{2}$ | $(-\sqrt{2}, 1)$ | $1$ | $(1, \sqrt{2})$ | $\sqrt{2}$ | $(\sqrt{2}, \infty)$ |
|---|---|---|---|---|---|---|---|
| sign of $x^2 - 2$ | $+$ | $0$ | $-$ | $-$ | $-$ | $0$ | $+$ |
| sign of $x - 1$ | $-$ | $-$ | $-$ | $0$ | $+$ | $+$ | $+$ |

Only the cell $(1, \sqrt{2})$ meets both conditions, and its sample point $x = 6/5$ is a model. CAD does the same in $n$ variables, one variable at a time.

5. **SAT inside.** With the atoms $x_p (x_p - 1) = 0$, each real variable is $0$ or $1$. A clause such as $p \vee q$ becomes $(1 - x_p)(1 - x_q) = 0$, and $\neg p \vee q$ becomes $x_p (1 - x_q) = 0$. The four clauses on $p$ and $q$ give an unsatisfiable system; without the clause $\neg p \vee \neg q$ the only model is $x_p = x_q = 1$.

## Known algorithms

| method | complete? | worst-case cost | notes |
|---|---|---|---|
| [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) (Collins 1975) | yes | $(m d)^{2^{O(n)}}$ | the standard complete method; it also does quantifier elimination |
| NLSAT, also called MCSat (Jovanović and de Moura 2012) | yes | doubly exponential | builds a model one variable at a time inside a [CDCL](/cdcl/) search, and explains conflicts with single CAD cells; used in Z3 and Yices |
| virtual substitution (Weispfenning) | yes, for low degree | exponential | eliminates a variable that has degree at most 2 (or 3) by a finite set of test terms |
| critical point methods (Canny; Basu, Pollack and Roy) | yes | $(m d)^{O(n)}$ for conjunctions | the best bounds in theory; little used in solvers |
| incremental linearization | no | iterative | refines a [linear](/linear-real-arithmetic-satisfiability/) abstraction with tangent and monotonicity lemmas; good on easy satisfiable cases |
| [interval constraint propagation](/interval-constraint-propagation/) | δ-complete only | exponential in precision | branch and prune on boxes; the basis of [δ-satisfiability](/delta-satisfiability/) solvers such as dReal |
| [Gröbner bases](/groebner-basis/) | for equalities with no complex solution | doubly exponential | proves unsatisfiability by the [Nullstellensatz](/hilbert-nullstellensatz/) when the equations have no common complex solution |

Gröbner bases decide whether equations have a common complex solution. Since $x^2 + 1 = 0$ has the complex solutions $\pm i$, a Gröbner basis alone does not refute it over the reals; real reasoning, such as sums of squares or CAD, is necessary for that.

## Bounds

**Theorem.** Satisfiability of QF_NRA formulas is decidable, NP-hard, and in PSPACE.

*Proof.* *Decidable.* A QF_NRA formula $\varphi(x)$ is satisfiable over $\mathbb{R}$ if and only if the sentence $\exists x\, \varphi(x)$ is true in $\mathbb{R}$, and this is decidable by [Tarski's theorem](/tarski-decidability-theorem/).

*NP-hard.* Reduce [3-SAT](/3-sat/). For each propositional variable $p$, take a real variable $x_p$ and the atom $x_p (x_p - 1) = 0$, so $x_p \in \{0, 1\}$. For each clause, take the product of the factors $(1 - x_p)$ for a positive literal $p$ and $x_q$ for a negative literal $\neg q$, and require that the product equals $0$. On 0-1 values, the product is $0$ exactly when some factor is $0$, that is, when some literal is true. So the system is satisfiable if and only if the clauses are, and the map is computable in polynomial time.

*In PSPACE.* This is Canny's theorem (1988), quoted here: the existential theory of the reals can be decided in polynomial space. $\square$

- **The class ∃R.** Many geometric problems, such as the recognition of segment intersection graphs and the stretchability of pseudoline arrangements, are polynomial-time equivalent to the existential theory of the reals (Schaefer 2009). So $\mathrm{NP} \subseteq \exists\mathbb{R} \subseteq \mathrm{PSPACE}$, and neither inclusion is known to be strict.
- **One polynomial suffices.** A conjunction $p_1 = 0 \wedge \cdots \wedge p_k = 0$ is equivalent to $\sum_i p_i^2 = 0$, so the problem for equations reduces to the real zeros of a single polynomial.
- **Cost of CAD.** For $m$ polynomials of degree at most $d$ in $n$ variables, CAD produces up to $(2d)^{2^{O(n)}} m^{2^{O(n)}}$ cells. The doubly exponential growth in $n$ cannot be avoided by any quantifier elimination method (Davenport and Heintz 1988), but the existential problem alone does not need full elimination, which is why it is in PSPACE.
- **Over the integers.** QF_NIA is undecidable, already for one equation of fixed degree in a fixed number of variables (Matiyasevich 1970 and later refinements).

## Reductions

- **From 3-SAT.** As in the proof above.
- **From LRA.** A [linear real arithmetic](/linear-real-arithmetic-satisfiability/) formula is a QF_NRA formula of degree 1.
- **To Tarski's theorem.** Existential closure, as in the proof above.
- **To δ-satisfiability.** On a bounded box, a QF_NRA formula is a special case of the formulas of [δ-satisfiability](/delta-satisfiability/); a δ-solver then answers "unsatisfiable" correctly, or "δ-satisfiable" with no guarantee of an exact model.
- **From nonlinear integer arithmetic, partially.** Integer constraints relax to real ones: an unsatisfiable real relaxation proves that the integer problem is unsatisfiable, but not the other way round ($x^2 = 2$ is a counterexample).

## Applications

- Verification of hybrid and cyber-physical systems, where the dynamics and safety conditions are polynomial; see [hybrid automata](/hybrid-automata/).
- Proofs of invariants and termination for programs with nonlinear arithmetic, for example polynomial [loop invariants](/loop-invariant/).
- Geometry theorem proving, robot motion planning and the analysis of polynomial systems in control theory.
- Program analysis with [symbolic execution](/symbolic-execution/), when path conditions multiply inputs; in practice these are often over bit-vectors or floats instead of reals.

## References
