---
tag: 8M5CJY
kind: algorithm
slug: omega-test
name: Omega test
aliases:
- Pugh's omega test
- omega test for integer programming
area: logic-and-constraints/smt
level: advanced
summary: Decision procedure for integer linear arithmetic built on Fourier-Motzkin with exact integer shadows.
solves: [linear-integer-arithmetic-satisfiability]
properties: {deterministic: true, exact: true, incremental: false}
history:
  year: 1991
  people: [William Pugh]
  note: Presented at Supercomputing 1991 as an exact test for array data dependences in compilers.
prereqs: [fourier-motzkin-elimination, linear-integer-arithmetic-satisfiability, linear-diophantine-equation, gcd-of-two-integers]
see_also: [presburger-arithmetic, simplex-for-smt, integer-feasibility, quantifier-elimination, lenstra-algorithm, hermite-normal-form, linear-real-arithmetic-satisfiability, branch-and-cut]
sources:
  - paper: "William Pugh, The Omega test: a fast and practical integer programming algorithm for dependence analysis, Proceedings of Supercomputing 1991, ACM, pages 4 to 13"
    locator: the equality elimination with the symmetric residue, the real and dark shadows, and the splinters (DOI and page numbers to be checked)
  - paper: "William Pugh, A practical algorithm for exact array dependence analysis, Communications of the ACM 35(8), 1992, pages 102 to 114"
    locator: the journal version, with the dark shadow lemma and the bound on the splinters (DOI and page numbers to be checked)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 5, Linear Arithmetic, the section on the Omega test
  - book: isbn:9783540741121
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Springer, 2007
    locator: Chapter 7, Quantified Linear Arithmetic (Fourier-Motzkin and Cooper's method, for comparison)
  - paper: "H. P. Williams, Fourier-Motzkin elimination extension to integer programming problems, Journal of Combinatorial Theory, Series A 21 (1976), 118 to 123"
    locator: an earlier integer version of Fourier-Motzkin elimination (to be checked)
---

The omega test of William Pugh (1991) decides whether a conjunction of linear equalities and inequalities has a solution in integers. It is [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) made exact for the integers: it removes equalities with a gcd-based substitution, and removes each other variable with two *shadows*, a real shadow that may contain too much and a dark shadow that may contain too little, plus a finite set of *splinters* that cover the gap. It decides the conjunctive case of [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), it returns a model, and it can also compute projections, which is why it is used for [Presburger](/presburger-arithmetic/) formulas and for dependence analysis in compilers.

## In plain words

You have whole-number unknowns and rules that say a weighted sum is at least some number, or equal to it. The plan is to remove the unknowns one at a time, until no unknown is left and the answer is plain.

To remove an unknown, compare each rule that pushes it up with each rule that pushes it down. With fractions, the unknown fits if the lowest top is above the highest bottom. With whole numbers, the gap can be too narrow to hold a whole number. So the test asks a stronger question first: is the gap wide enough that a whole number must fit? If yes, the answer is yes. If not, the only solutions left sit near a bottom rule, so the test tries each of the few values near it, one by one.

## The problem

The input is a finite system of constraints $\sum_i a_i x_i + c \ge 0$ and $\sum_i a_i x_i + c = 0$ with integer coefficients over integer variables $x_1, \ldots, x_n$; here $n$ is the number of variables and $m$ the number of constraints. The output is an integer solution, or the answer that none exists. This is the conjunctive case of [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), and it is [NP-complete](/np-complete/).

The notation used below:

- $a \operatorname{\widehat{mod}} m = a - m \lfloor a/m + 1/2 \rfloor$, the residue of $a$ modulo $m$ that lies in $[-m/2, m/2)$.
- For a variable $z$, each constraint that contains $z$ is a lower bound $b z \ge \beta$ or an upper bound $a z \le \alpha$, with $a, b > 0$ and $\alpha, \beta$ linear in the other variables. $a_{\max}$ is the largest $a$.
- The *real shadow* is the constraints without $z$ plus $b \alpha - a \beta \ge 0$ for each pair: this is Fourier-Motzkin.
- The *dark shadow* is the constraints without $z$ plus $b \alpha - a \beta \ge (a - 1)(b - 1)$ for each pair.

## The algorithm

```pseudo id=main
OMEGA(E, I)                       ▷ E: equalities, I: inequalities, integer variables
L1  while E is not empty do
L2      take e ∈ E; divide it by the gcd g of its coefficients; if g does not divide its constant then return UNSAT
L3      if e has a coefficient a_k = ±1 then solve e for x_k, and remove e from E
L4      else take a_k of least |a_k|, m ← |a_k| + 1, a new variable σ, and x_k ← −sign(a_k)·m·σ + Σ_{i≠k} sign(a_k)(a_i mod^ m) x_i + sign(a_k)(c mod^ m)
L5      substitute the value of x_k in E and I
L6  divide each inequality by the gcd of its coefficients and round its constant down; if some inequality is 0 ≥ c with c > 0 then return UNSAT
L7  if no inequality has a variable then return SAT
L8  choose a variable z to eliminate (prefer one with an exact elimination)
L9  if z has no lower bound or no upper bound then return OMEGA(∅, the inequalities without z)
L10 if every lower bound has b = 1 or every upper bound has a = 1 then return OMEGA(∅, real shadow)
L11 if OMEGA(∅, dark shadow) = SAT then return SAT
L12 for each lower bound b z ≥ β and each i = 0, 1, ..., ⌊(a_max b − a_max − b) / a_max⌋ do
L13     if OMEGA({b z = β + i}, I) = SAT then return SAT
L14 return UNSAT
```

**Equalities (lines L1 to L5).** An equality with a unit coefficient gives one variable as a linear function of the others, and substitution removes that variable. Without a unit coefficient, line L4 introduces a new variable $\sigma$. The value of $x_k$ in line L4 is an integer for each integer $\sigma$, and each integer solution of the equality has exactly one such $\sigma$, so no solution is lost or added. After the substitution the equality stays in $E$, but each coefficient other than the one of $\sigma$ is now strictly smaller in absolute value, so after a few rounds a coefficient $\pm 1$ appears. The gcd test of line L2 detects equalities such as $2x - 2y = 1$ with no integer solution.

**Inequalities (lines L6 to L14).** Line L6 is exact for integers: $3x \ge 2$ becomes $x \ge 1$. Line L9 drops a variable that is bounded only on one side, because it can always be chosen large or small enough. Line L10 is the case where Fourier-Motzkin is exact for integers: if every upper bound is $z \le \alpha$, then $z = \lfloor \alpha \rfloor$ works whenever the real shadow holds. Otherwise, the dark shadow is a sufficient condition (line L11): the interval for $z$ is wide enough to hold an integer. If the dark shadow has no solution, any remaining solution has $b z$ close to some lower bound $\beta$, and the splinters of lines L12 and L13 try each such value as an equality, which line L4 then removes.

**The model.** After a recursive call returns values for the other variables, $z$ gets $\max \lceil \beta/b \rceil$, and each solved variable gets its value from line L3 or line L4.

## Example

Decide $2 \le 3x - 2y \le 3$ and $1 \le y \le 4$ over the integers. Eliminating $x$ gives one pair, and eliminating $y$ gives four, so line L8 picks $x$. The bounds on $x$ are $3x \ge 2y + 2$ (so $b = 3$) and $3x \le 2y + 3$ (so $a = 3$), and the elimination is not exact.

| step | constraints | result |
|---|---|---|
| real shadow (for comparison) | $3(2y + 3) - 3(2y + 2) = 3 \ge 0$, $1 \le y \le 4$ | true for $y = 1, 2, 3, 4$ |
| dark shadow (line L11) | $3 \ge (3 - 1)(3 - 1) = 4$ | false: no solution |
| splinter $i = 0$ (line L13) | $3x - 2y - 2 = 0$ plus the old constraints | goes to line L4 |
| line L4, $a_k = -2$ on $y$, $m = 3$ | $y = 3\sigma - 1$; the equality becomes $3x - 6\sigma = 0$, so $x = 2\sigma$ | $1 \le 3\sigma - 1 \le 4$ gives $1 \le \sigma \le 1$ |
| model | $\sigma = 1$, $x = 2$, $y = 2$ | $3x - 2y = 2$ |

The real shadow says that real solutions exist for each $y$ from 1 to 4, but integer solutions exist only for $y = 2$ ($x = 2$) and $y = 3$ ($x = 3$). The dark shadow is empty, because the interval for $3x$ has length 1 and need not hold a multiple of 3. There are $\lfloor (9 - 3 - 3)/3 \rfloor + 1 = 2$ splinters: $3x = 2y + 2$ and $3x = 2y + 3$. With the extra constraint $y \le 1$, both splinters fail and the answer is UNSAT, although the real shadow is not empty. The tests check this example, and they check the inclusions of the shadows on random systems by brute force.

## Correctness

**Invariant.** Each step keeps the set of integer solutions, up to the new variables $\sigma$ and the variables that were solved: the gcd step and line L6 are exact for integers, and the substitution of line L4 is a bijection between the old solutions and the new ones. For the elimination of $z$, the integer projection $P$ of the solutions satisfies
$$\text{dark shadow} \subseteq P \subseteq \text{real shadow},$$
with equality on the right in the exact case, and each point of $P$ outside the dark shadow is the projection of a solution of some splinter. The left inclusion holds because $\lfloor \alpha/a \rfloor < \lceil \beta/b \rceil$ forces $b\alpha - a\beta \le (a - 1)(b - 1) - 1$. So the answer is SAT if and only if an integer solution exists.

**Termination.** In the equality phase, the sum of the absolute coefficients of the current equality decreases at each step of line L4, and line L3 removes the equality. Each recursive call of the inequality phase has one variable less after its equality phase. The [full proof](proofs/correctness.md) gives all the lemmas.

## Complexity

The costs count arithmetic operations on integers of any size, in the [real RAM](/real-ram/) style; the numbers can grow, so the bit cost is higher.

- **One equality step.** Substitution touches each constraint once: $O(m n)$ operations. One equality needs at most $W$ steps, where $W$ is the sum of its absolute coefficients, since each step of line L4 lowers $W$ by at least 1. This is a crude bound; the coefficients shrink by about a factor $m$ at each step.
- **One elimination.** With $p$ lower and $q$ upper bounds on $z$, each shadow has at most $p q$ new constraints, built in $O(p q n)$ time. Since $p + q \le m$, $p q \le m^2/4$, so after $k$ eliminations without splinters there are at most $m^{2^k}$ constraints. This doubly exponential growth is the weak point that the omega test shares with Fourier-Motzkin.
- **Splinters.** A lower bound with coefficient $b$ gives $\lfloor (a_{\max} b - a_{\max} - b)/a_{\max} \rfloor + 1 \le b - 1$ splinters, because $(a_{\max} b - a_{\max} - b)/a_{\max} < b - 1$. A lower bound with $b = 1$ gives none. Each splinter is a full recursive call.

No polynomial bound is possible unless P = NP, since the problem is NP-complete, and the proofs above give no useful closed form for the worst case. Pugh reported that the test was fast on the systems that arise in array dependence analysis, where most eliminations are exact; this is a measured result on those inputs, not a bound.

## Properties

- **Exact.** It decides integer feasibility with no rounding, and returns an integer model.
- **Projection.** Lines L9 to L13 compute the integer projection of a system as a union of systems, so the method can eliminate existential quantifiers from conjunctions. This is the basis for its use on [Presburger](/presburger-arithmetic/) formulas.
- **Not incremental.** Adding a constraint means running the eliminations again. This is one reason why SMT solvers prefer the [general simplex](/simplex-for-smt/) with branch and bound and cuts for linear integer arithmetic.
- **No short refutation.** An UNSAT answer comes with a tree of shadows and splinters, not with a single small certificate such as the Farkas multipliers of the real case.

## Variants and improvements

- **Real shadow first.** If the real shadow has no integer solution, neither does the system. Testing it before the dark shadow stops early on many unsatisfiable inputs.
- **Redundancy removal.** Removing constraints implied by others, and keeping only the tightest of parallel constraints, limits the growth of the shadows.
- **Projection for Presburger formulas.** For a formula with quantifiers, the method projects away the bound variables, with disjunctions at the splinters.
- **Real version.** Without the integer steps (L2, L4, L6, L11 to L13), the method is plain [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) for [linear real arithmetic](/linear-real-arithmetic-satisfiability/).

## When to use it

Use the omega test for small integer systems where an exact answer and a projection are needed, such as dependence tests between array subscripts in loops, or the conjunctive cases inside a Presburger decision procedure. In an SMT solver for large QF_LIA formulas, the [general simplex](/simplex-for-smt/) with branch and bound and [cutting planes](/gomory-cutting-plane-algorithm/) is the usual choice, since it is incremental and gives explanations. For a fixed number of variables, [Lenstra's algorithm](/lenstra-algorithm/) gives a polynomial bound, which the omega test does not.

## Pitfalls

- **Skipping the gcd division in line L2.** For $2x + 1 = 0$, line L4 then sets $x = -3\sigma + 1$ and gets the new equality $-6\sigma + 3 = 0$, with a larger coefficient, and the loop does not stop. Divide by the gcd and test divisibility first.
- **Using the real shadow when line L10 does not apply.** For $2 \le 3x - 2y \le 3$ and $y = 1$, the real shadow is true but no integer $x$ exists. Use line L10 only in the exact case, and use lines L11 to L13 otherwise.
- **Taking $a_{\max}$ from the lower bounds in line L12.** The bound on $i$ needs the largest coefficient of an upper bound. With the wrong value the splinters can miss solutions.
- **Rounding the constant up in line L6.** $3x \ge 2$ means $x \ge \lceil 2/3 \rceil = 1$; written as $3x - 2 \ge 0$ it becomes $x + \lfloor -2/3 \rfloor = x - 1 \ge 0$. Rounding the other way loses solutions.

## Implementations

## History

Fourier described the elimination of variables from linear inequalities in 1826, and Motzkin studied it again in 1936. Williams (1976) gave an extension of the elimination to integer problems. Pugh presented the omega test at Supercomputing 1991 as an exact and practical dependence test for parallelizing compilers, and gave a fuller version in Communications of the ACM in 1992. The test became part of the Omega library and of later work on polyhedral loop analysis.

## References
