---
tag: ECNM3R
kind: problem
slug: linear-real-arithmetic-satisfiability
name: Linear real arithmetic satisfiability
aliases:
- linear real arithmetic
- LRA
- QF_LRA
- linear rational arithmetic
area: logic-and-constraints/smt
level: advanced
summary: Decide satisfiability of linear constraints over the real numbers.
prereqs: [smt-problem, linear-feasibility, farkas-lemma]
see_also: [simplex-for-smt, difference-logic-satisfiability, linear-integer-arithmetic-satisfiability, fourier-motzkin-elimination, lp-in-p, dpll-t, quantifier-elimination, nonlinear-real-arithmetic-satisfiability]
sources:
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 5, Linear Arithmetic (the general simplex, Fourier-Motzkin elimination and strict inequalities)
  - book: isbn:9783540741121
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Springer, 2007
    locator: Chapter 8, Quantifier-Free Linear Arithmetic, and Chapter 7 for the quantified theory
  - paper: doi:10.1007/11817963_11
    title: Bruno Dutertre and Leonardo de Moura, A Fast Linear-Arithmetic Solver for DPLL(T), CAV 2006, Lecture Notes in Computer Science 4144, 81 to 94
    locator: Sections 2 and 3
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 7 (Farkas' lemma and its variants, including the version with strict inequalities), Chapter 10 (the size of solutions) and Chapter 13 (Khachiyan's method)
  - paper: "L. G. Khachiyan, A polynomial algorithm in linear programming, Soviet Mathematics Doklady 20 (1979), 191 to 194"
    locator: the main theorem (linear programming is in polynomial time)
  - paper: "Michael J. Fischer and Michael O. Rabin, Super-exponential complexity of Presburger arithmetic, Complexity of Computation, SIAM-AMS Proceedings 7 (1974), 27 to 41"
    locator: the lower bound for the first-order theory of the reals with addition
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 33 (Barrett, Sebastiani, Seshia and Tinelli, Satisfiability Modulo Theories), pages 1267 to 1329, the section on arithmetic theories
---

Linear real arithmetic satisfiability is the problem of deciding whether a formula built from linear constraints over the real numbers, such as $2x - 3y \le 5$, has a model. In SMT-LIB it is the logic QF_LRA when the formula has no quantifiers. A conjunction of constraints is a [linear feasibility](/linear-feasibility/) problem and can be decided in polynomial time, while a formula with arbitrary Boolean structure is [NP-complete](/np-complete/). In SMT solvers the standard method for the conjunctions is the [general simplex](/simplex-for-smt/), used inside [DPLL(T)](/dpll-t/).

## In plain words

You have some unknown quantities that can take any value, with fractions allowed. You also have rules that say a weighted sum of them is at most, at least, or exactly some number. Some rules can be joined with "or" and "not". The question is whether values exist that make the whole formula true.

If all rules must hold together, a fast method answers. If the rules are joined with "or", the solver must also choose which rules to make true, and this choice is the hard part. When no values exist, the solver can give a short proof: add some of the rules with positive weights, and the sum says that zero is more than zero.

## Definition

An *atom* is $a \cdot x \bowtie b$ with rational coefficients $a \in \mathbb{Q}^n$, a rational $b$, real variables $x = (x_1, \ldots, x_n)$, and $\bowtie \in \{\le, <, \ge, >, =\}$. A QF_LRA formula is a Boolean combination of atoms (with $\wedge$, $\vee$, $\neg$ and Boolean variables). The problem asks whether some $x \in \mathbb{R}^n$ makes the formula true. The input size is the number of symbols, with each rational written in binary.

The rationals and the reals give the same answers: if a formula has a real model, it has a rational one. This is why the logic is also called linear rational arithmetic.

**The conjunctive case.** The theory solver of [DPLL(T)](/dpll-t/) gets a conjunction of literals. The negation of an atom is again a conjunction of atoms or a disjunction of two of them: $\neg(a \cdot x \le b)$ is $a \cdot x > b$, and $\neg(a \cdot x = b)$ is $a \cdot x < b \vee a \cdot x > b$. So, after a choice for each negated equality, the conjunctive case is a system of non-strict and strict linear inequalities.

**Certificates.** By the version of [Farkas' lemma](/farkas-lemma/) for strict inequalities (Motzkin's transposition theorem), a system $A x \le b$, $C x < d$ has no real solution if and only if there are $\lambda, \mu \ge 0$ with $\lambda^{\top} A + \mu^{\top} C = 0$ and either $\lambda^{\top} b + \mu^{\top} d < 0$, or $\lambda^{\top} b + \mu^{\top} d = 0$ and $\mu \ne 0$. The multipliers are the explanation that an SMT solver turns into a learned clause.

## Variants

- **Quantified LRA.** The full first-order theory of $(\mathbb{R}, +, <, 0, 1)$ is decidable by [quantifier elimination](/quantifier-elimination/) ([Fourier-Motzkin](/fourier-motzkin-elimination/), or the methods of Ferrante and Rackoff (1975) and Loos and Weispfenning (1993)). Fischer and Rabin (1974) proved a lower bound for it: some formulas of length $\ell$ need nondeterministic time $2^{c\ell}$ for a constant $c > 0$.
- **Difference logic.** All atoms have the form $x - y \le c$. The conjunctive case reduces to negative cycles in a graph: see [difference logic](/difference-logic-satisfiability/).
- **Integers.** The same atoms over the integers give [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), which is NP-complete already for conjunctions. Mixed real and integer variables give QF_LIRA.
- **Optimization.** Add an objective to minimize: this is [optimization modulo theories](/optimization-modulo-theories/), and for conjunctions it is [linear programming](/linear-programming-problem/).
- **Nonlinear.** Products of variables give [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/).

## Examples

Each example below was checked by a script with exact rational arithmetic.

1. **Unsatisfiable conjunction.** $x + y \ge 4$, $x - y \le 1$, $x \le 1$, $y \le 2$. With multipliers $1, 1, 1$ on $x \le 1$, $y \le 2$ and $x + y \ge 4$ (as $4 - x - y \le 0$), the sum is $(x - 1) + (y - 2) + (4 - x - y) = 1 \le 0$, which is false. The atom $x - y \le 1$ is not needed, so the small conflict is $\{x + y \ge 4, x \le 1, y \le 2\}$. The [general simplex](/simplex-for-smt/) page traces how it finds this conflict.
2. **Strict inequalities.** $x < y$ and $y < x + 1$ has the real model $x = 0$, $y = 1/2$, but no integer model, because no integer lies strictly between $x$ and $x + 1$.
3. **A unique rational point.** $3x + 2y = 7$ and $x - y = 1$ have the only solution $x = 9/5$, $y = 4/5$. Over the integers the system has no solution, because $5x = 9$.
4. **Boolean structure.** $(x + y \le 2 \vee x - y \ge 3) \wedge x \ge 2 \wedge y \ge 1$. The first branch is unsatisfiable, with the conflict $\{x + y \le 2, x \ge 2, y \ge 1\}$. The second branch has the model $x = 4$, $y = 1$. A [DPLL(T)](/dpll-t/) solver learns the clause $\neg(x + y \le 2) \vee \neg(x \ge 2) \vee \neg(y \ge 1)$ from the first conflict and then finds the second branch.

## Known algorithms

| method | input | worst-case cost | notes |
|---|---|---|---|
| [general simplex](/simplex-for-smt/) | conjunctions | exponential (no polynomial bound known) | incremental, cheap backtracking, Farkas explanations; the standard in SMT solvers |
| [ellipsoid method](/ellipsoid-method/), [interior point methods](/interior-point-method/) | conjunctions | polynomial | proves membership in P; not incremental |
| [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) | conjunctions, quantifiers | doubly exponential growth of the system | simple; useful for few variables and for projection |
| [Bellman-Ford](/bellman-ford/) | difference constraints | $O(n m)$ | see [difference logic](/difference-logic-satisfiability/) |
| [DPLL(T)](/dpll-t/) with a theory solver | full QF_LRA | exponential | the method of practical SMT solvers |

## Bounds

**Theorem (conjunctions are in P).** A conjunction of $m$ atoms over $n$ real variables can be decided in time polynomial in its size.

*Proof.* Replace each equality by two non-strict inequalities, so the system is $A x \le b$, $C x < d$. Add a new variable $t$ and solve the linear program: maximize $t$ subject to $A x \le b$, $C x + t \mathbf{1} \le d$ and $t \le 1$. If the system has a solution $x$, then $t = \min(1, \min_k (d_k - C_k x)) > 0$ is feasible, so the optimum is positive. If the optimum is some $t > 0$ at a point $x$, then $x$ meets $C x < d$. If the program is infeasible or its optimum is at most 0, the system has no solution. The program has polynomial size, and [linear programming is in P](/lp-in-p/) (Khachiyan 1979). $\square$

The same argument gives a rational model of polynomial bit size, since an optimal vertex of a linear program has this size (Schrijver 1986, Chapter 10).

**Theorem (QF_LRA is NP-complete).** Satisfiability of QF_LRA formulas is NP-complete.

*Proof.* Membership: guess a truth value for each atom and Boolean variable, and for each false equality guess which side holds. Check in polynomial time that the guess makes the formula true, and check that the chosen literals have a common real model with the theorem above. Hardness: map each propositional variable $p$ of a CNF formula to a new real variable $x_p$ and the atom $x_p > 0$. The atoms use different variables, so each truth assignment of them is realizable, and the CNF formula is satisfiable if and only if its image is. [SAT](/sat/) is NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/). $\square$

No polynomial bound is known on the number of pivots of any simplex pivot rule. So the polynomial bound for conjunctions comes from the ellipsoid or interior point methods, not from the general simplex that solvers use. The fast running times of simplex-based SMT solvers are measured results, not proved bounds.

## Reductions

- **To linear programming.** The conjunctive case reduces to one linear program, as in the proof above.
- **From SAT.** The hardness proof above maps a CNF formula to QF_LRA with one atom per variable.
- **From difference logic.** Difference logic is a fragment of LRA, and it can be solved faster with a graph method.
- **Relaxation of LIA.** Each model over the integers is a model over the reals, so LRA is the relaxation inside [branch and cut](/branch-and-cut/) for [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/). If the relaxation is unsatisfiable, so is the integer problem.
- **Theory combination.** LRA is a [convex theory](/convex-theory/) and [stably infinite](/stable-infiniteness/), so it meets the hypotheses of [Nelson-Oppen](/nelson-oppen/) combination with other such theories.

## Applications

- Verification of programs and systems with rational or real quantities, in [bounded model checking](/bounded-model-checking/) and in invariant checking.
- The analysis of [timed automata](/timed-automata/) and [hybrid automata](/hybrid-automata/), where the constraints on clocks are often difference constraints.
- Scheduling and planning with real time windows.
- The relaxation step of integer and mixed-integer solvers.

## References
