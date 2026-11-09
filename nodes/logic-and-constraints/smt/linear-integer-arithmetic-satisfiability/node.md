---
tag: BPK53F
kind: problem
slug: linear-integer-arithmetic-satisfiability
name: Linear integer arithmetic satisfiability
aliases:
- linear integer arithmetic
- LIA
- QF_LIA
area: logic-and-constraints/smt
level: advanced
summary: Decide satisfiability of linear constraints over the integers.
prereqs: [linear-real-arithmetic-satisfiability, integer-feasibility, np-complete]
see_also: [omega-test, presburger-arithmetic, simplex-for-smt, difference-logic-satisfiability, lenstra-algorithm, gomory-cutting-plane-algorithm, bit-blasting, papadimitriou-pseudopolynomial-theorem]
sources:
  - paper: doi:10.1145/322276.322287
    title: Christos H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4), 1981
    locator: the bound n(ma)^(2m+1) on a smallest nonnegative integer solution of Ax = b
  - paper: "I. Borosh and L. B. Treybig, Bounds on positive integral solutions of linear Diophantine equations, Proceedings of the American Mathematical Society 55 (1976)"
    locator: an earlier bound of the same kind (page numbers not checked)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 17 (the size of solutions) and Chapter 18 (the complexity of integer linear programming, including Lenstra's algorithm)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 5, Linear Arithmetic (branch and bound, cutting planes and the Omega test)
  - paper: "Alberto Griggio, A practical approach to satisfiability modulo linear integer arithmetic, Journal on Satisfiability, Boolean Modeling and Computation 8 (2012)"
    locator: the integer layer of an SMT solver (branch and bound, cuts and the gcd test on top of the general simplex)
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: the main theorem
---

Linear integer arithmetic satisfiability is the problem of deciding whether a formula built from linear constraints over integer variables, such as $3x - 2y \le 5$, has an integer model. In SMT-LIB it is the logic QF_LIA when the formula has no quantifiers. Unlike the [real case](/linear-real-arithmetic-satisfiability/), it is [NP-complete](/np-complete/) even for a plain conjunction of constraints, because a conjunction is an [integer feasibility](/integer-feasibility/) problem. This page is about the quantifier-free problem; its full first-order theory is [Presburger arithmetic](/presburger-arithmetic/), and the [omega test](/omega-test/) is one exact algorithm for its conjunctions.

## In plain words

The unknowns must be whole numbers, and the rules say that a weighted sum is at most, at least or exactly some number. Rules can be joined with "and", "or" and "not". The question is whether whole numbers exist that make the whole formula true.

With fractions allowed, a fast method decides a list of such rules. With whole numbers, a region can contain many points with fractions but no whole-number point at all, for example a thin strip that passes between them. Even a plain list of rules can be hard, and no fast method is known for all cases. A useful fact helps: if a solution exists, a solution with numbers of limited size exists, so a correct guess can be checked quickly.

## Definition

An *atom* is $a \cdot x \bowtie b$ with integer (or rational) coefficients $a$, a constant $b$, integer variables $x = (x_1, \ldots, x_n)$, and $\bowtie \in \{\le, <, \ge, >, =\}$. A QF_LIA formula is a Boolean combination of atoms. The problem asks whether some $x \in \mathbb{Z}^n$ makes the formula true. The input size counts each integer in binary; $n$ is the number of variables and $m$ the number of atoms.

Over the integers, strict atoms need no special care: $a \cdot x < b$ is $a \cdot x \le b - 1$ when $a$ and $b$ are integers, and $\neg(a \cdot x \le b)$ is $a \cdot x \ge b + 1$. So the conjunctive case is a system $A x \le b$, which is the [integer feasibility](/integer-feasibility/) problem.

**How the three related pages differ.** This page is the quantifier-free decision problem. [Presburger arithmetic](/presburger-arithmetic/) is the first-order theory with quantifiers, which is decidable but much harder. The [omega test](/omega-test/) is an algorithm for the conjunctions of this problem, and it can also eliminate quantifiers.

## Variants

- **Conjunctions.** Integer feasibility of $A x \le b$; NP-complete.
- **Fixed number of variables.** For each fixed $n$, [Lenstra's algorithm](/lenstra-algorithm/) decides conjunctions in polynomial time (Lenstra 1983).
- **Difference logic.** Atoms $x - y \le c$ only. Conjunctions are in P by the negative-cycle test of [difference logic](/difference-logic-satisfiability/), since the constraint matrix is [totally unimodular](/total-unimodularity/).
- **Mixed variables.** Some variables real and some integer: QF_LIRA, the logic of [mixed integer programming](/mixed-integer-programming/).
- **Quantifiers.** The full first-order theory is [Presburger arithmetic](/presburger-arithmetic/).
- **Multiplication of variables.** With products of variables, satisfiability over the integers is undecidable, by the solution of [Hilbert's tenth problem](/hilberts-tenth-problem/) (Matiyasevich 1970); see [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/) for the contrast with the reals.
- **Bounded integers.** If each variable has known bounds, the problem can be [bit-blasted](/bit-blasting/) to SAT, in the style of [bit-vector](/bit-vector-satisfiability/) solvers.

## Examples

Each example was checked by a script with the [omega test](/omega-test/) implementation, and the bounded ones by brute force.

1. **Strict gaps.** $x < y < x + 1$ has real models but no integer model.
2. **A rational point only.** $3x + 2y = 7$ and $x - y = 1$ have the only solution $x = 9/5$, $y = 4/5$, so no integer solution.
3. **Parity.** $2x - 2y = 1$ has no integer solution, because the left side is even. The gcd test (the gcd of the coefficients must divide the constant) finds this at once.
4. **A thin strip.** $1 \le 3x - 3y \le 2$ has infinitely many real solutions and no integer solution, since $3(x - y)$ is a multiple of 3. Plain branch and bound on the real relaxation runs forever here: each branch $x \le k$ or $x \ge k + 1$ still has real solutions. Dividing by the gcd 3 and rounding gives $x - y \ge 1$ and $x - y \le 0$, which settles it.
5. **Coins.** $6a + 9b + 20c = 43$ with $a, b, c \ge 0$ has no solution, while $6a + 9b + 20c = 44$ has $a = 4$, $b = 0$, $c = 1$.
6. **SAT inside.** With $0 \le p, q \le 1$, the four atoms $p + q \ge 1$, $-p + q \ge 0$, $p - q \ge 0$ and $p + q \le 1$ encode the four clauses on $p$ and $q$, and have no solution. Without the last atom, $p = q = 1$ is a model.

## Known algorithms

| method | case | worst-case cost | notes |
|---|---|---|---|
| general simplex with branch and bound and cuts | conjunctions, inside [DPLL(T)](/dpll-t/) | exponential | the usual SMT method; see [general simplex](/simplex-for-smt/) and [Gomory cuts](/gomory-cutting-plane-algorithm/) |
| [omega test](/omega-test/) | conjunctions, projections | exponential | exact; gives integer projections |
| [Lenstra's algorithm](/lenstra-algorithm/) | conjunctions, fixed $n$ | polynomial for fixed $n$ | uses lattice basis reduction ([LLL](/lll-algorithm/)) |
| [Bellman-Ford](/bellman-ford/) | difference constraints | $O(n m)$ | see [difference logic](/difference-logic-satisfiability/) |
| [bit-blasting](/bit-blasting/) with the small-solution bound | full QF_LIA | exponential | a correct reduction to SAT; the bound makes the encoding large |

In SMT solvers, the integer layer sits on top of the real one: solve the relaxation with the general simplex, and if a variable that must be an integer has a fractional value $v$, either branch on $x \le \lfloor v \rfloor \vee x \ge \lceil v \rceil$ or add a cut that removes $v$. The gcd test of example 3 runs on the equalities first. Branch and bound alone does not always stop (example 4); it stops if each variable has a finite bound, and the bound below gives one. The fast running times of these solvers are measured results on benchmark sets, not proved bounds.

## Bounds

**Lemma (small solutions; Papadimitriou 1981).** Let $A$ be an integer $m \times n$ matrix and $b$ an integer vector, with all entries of absolute value at most $a$. If $A x = b$ has a solution $x \in \mathbb{Z}_{\ge 0}^n$, then it has one with each entry at most $n (m a)^{2m + 1}$.

The lemma is quoted from Papadimitriou (1981); Borosh and Treybig (1976) gave an earlier bound of the same kind. Its point is that the bit size of a smallest solution is polynomial in the bit size of the input.

**Theorem.** QF_LIA satisfiability is NP-complete, and it is already NP-complete for conjunctions of atoms.

*Proof.* *Membership.* For a conjunction $A x \le b$ over free integer variables, write $x = x^+ - x^-$ and add slack variables $s = b - A x$; this gives a system $A' y = b$ with $y \ge 0$ of polynomial size, whose nonnegative integer solutions map onto the integer solutions of $A x \le b$. By the lemma, if a solution exists, one exists whose entries have a number of binary digits polynomial in the input size. A nondeterministic machine guesses it and checks it. For a formula with Boolean structure, guess first the truth value of each atom, check the Boolean part, and then guess a small solution of the chosen literals; a false atom $a \cdot x \le b$ becomes $a \cdot x \ge b + 1$, so the chosen literals are again a conjunction of atoms.

*Hardness.* Reduce [3-SAT](/3-sat/): for each propositional variable $p$ take an integer variable with $0 \le x_p \le 1$, and for each clause, for example $p \vee \neg q \vee r$, the atom $x_p + (1 - x_q) + x_r \ge 1$. A truth assignment satisfies the clauses if and only if the 0-1 vector meets the atoms. The map is computable in polynomial time, and 3-SAT is NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/). $\square$

**Fixed dimension.** For each fixed $n$, conjunctions are in P (Lenstra 1983). So the hardness comes from the number of variables.

## Reductions

- **From 3-SAT.** As in the proof above: 0-1 variables and one atom per clause.
- **To SAT.** By the small-solution lemma, each variable can be bounded and written in binary with polynomially many bits; then [bit-blasting](/bit-blasting/) gives a CNF formula of polynomial size.
- **The real relaxation.** Each integer model is a real model, so an unsatisfiable [LRA](/linear-real-arithmetic-satisfiability/) relaxation proves unsatisfiability, and branch and bound and cuts refine the relaxation.
- **Into Presburger arithmetic.** A QF_LIA formula is satisfiable if and only if its existential closure is a true [Presburger](/presburger-arithmetic/) sentence (over $\mathbb{Z}$, or over $\mathbb{N}$ after writing each variable as a difference of two naturals).

## Applications

- Program verification and [symbolic execution](/symbolic-execution/), where loop counters, array indices and sizes are integers.
- Scheduling and planning with integer time steps and resources.
- Test generation, where a path condition over integer inputs must be solved.
- Dependence analysis of array accesses in compilers, where the [omega test](/omega-test/) was first used.

## References
