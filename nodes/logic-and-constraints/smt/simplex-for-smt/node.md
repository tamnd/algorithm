---
tag: W3SMMR
kind: algorithm
slug: simplex-for-smt
name: General simplex for linear arithmetic
aliases:
- Dutertre-de Moura simplex
- SMT simplex
- general simplex
area: logic-and-constraints/smt
level: advanced
summary: Incremental simplex with bounds that checks feasibility of linear constraints inside DPLL(T).
solves: [linear-real-arithmetic-satisfiability]
model: real-ram
complexity:
  vars: {n: the number of original variables, m: the number of slack variables (distinct linear forms)}
  time: {worst: O(6^(n+m) m n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, exact: true, incremental: true}
history:
  year: 2006
  people: [Bruno Dutertre, Leonardo de Moura]
  note: Published at CAV 2006 as the linear arithmetic solver of the Yices SMT solver.
prereqs: [linear-real-arithmetic-satisfiability, simplex-method, bland-rule, farkas-lemma, dpll-t]
see_also: [pivot-operation, theory-conflict-explanation, theory-propagation, incremental-solving, difference-logic-satisfiability, linear-integer-arithmetic-satisfiability, fourier-motzkin-elimination, unsat-core]
sources:
  - paper: doi:10.1007/11817963_11
    title: Bruno Dutertre and Leonardo de Moura, A Fast Linear-Arithmetic Solver for DPLL(T), CAV 2006, Lecture Notes in Computer Science 4144, 81 to 94
    locator: Section 3 (the general simplex, the procedures Check, AssertUpper, AssertLower and PivotAndUpdate, the explanations, and strict bounds with delta-rationals)
  - paper: "Bruno Dutertre and Leonardo de Moura, Integrating Simplex with DPLL(T), Technical Report SRI-CSL-06-01, SRI International, 2006"
    locator: the full version of the CAV paper, with the termination argument and the backtracking of bounds
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 5, Linear Arithmetic, the section on the general simplex
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 103 to 107 (1977)
    locator: the smallest-index rule and its proof of finiteness
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 33 (Barrett, Sebastiani, Seshia and Tinelli, Satisfiability Modulo Theories), pages 1267 to 1329, the section on linear arithmetic solvers
---

The general simplex of Dutertre and de Moura (2006) is the decision procedure that most SMT solvers use for conjunctions of linear constraints over the reals. It is a version of the [simplex method](/simplex-method/) with no objective: it keeps a fixed tableau, puts a lower and an upper bound on each variable, and pivots only to repair a bound that the current assignment breaks. Atoms of the input become bounds, so [DPLL(T)](/dpll-t/) can add and remove atoms by changing bounds, and it can backtrack at almost no cost. When the bounds cannot all hold, it returns a small conflict with its [Farkas](/farkas-lemma/) multipliers. This page is about the algorithm; the problem that it solves is [linear real arithmetic satisfiability](/linear-real-arithmetic-satisfiability/).

## In plain words

You have some unknown numbers and a list of rules such as "this sum is at least four" and "this number is at most one". Give each sum that the rules mention its own name, and write it as a formula of the unknowns. Now each rule only says "this name stays between these two limits".

Start with all numbers at zero. Look for a named sum that is outside its limits. Move it to the limit it broke, and pay for this by moving one of the plain numbers that still has room to move. Do this again. If a sum is outside its limits and every number it depends on is stuck at a limit, then the rules contradict each other, and the stuck limits are the reason. A solver can add or remove a limit at any time, and the numbers it already found stay useful.

## The problem

The input is a conjunction of atoms $a \cdot x \bowtie b$ over real variables $x_1, \ldots, x_n$, with rational $a$ and $b$ and $\bowtie \in \{\le, <, \ge, >, =\}$. The output is a rational model, or a set of atoms with no real model and a certificate for it. The atoms arrive one at a time from a SAT solver, which also takes them back on backtracking. This is the theory solver for the quantifier-free part of [linear real arithmetic](/linear-real-arithmetic-satisfiability/).

**Preprocessing.** Each linear form with two or more variables, such as $x + y$, gets one *slack* variable $s = x + y$. An atom $x + y \ge 4$ becomes the bound $s \ge 4$, and an atom $3x \le 6$ becomes $x \le 2$. After this step, the solver has $n$ original variables, $m$ slack variables, a set of $m$ equations $s_k = a_k \cdot x$ that never changes, and bounds that come and go.

**Strict bounds.** $x < c$ becomes $x \le c - \delta$, where $\delta$ is a positive infinitesimal. A value is a pair $(c, k)$ that stands for $c + k\delta$, and pairs compare lexicographically. At the end, a small rational $\delta_0$ replaces $\delta$.

## The algorithm

The state is a basis of $m$ basic variables, a tableau row $x_i = \sum_j a_{ij} x_j$ for each basic $x_i$ over the $n$ nonbasic variables, an assignment $\beta$, and the bounds $l_i \le x_i \le u_i$ (a missing bound is $-\infty$ or $+\infty$). At the start, the slacks are basic, the original variables are nonbasic, and $\beta = 0$. "Least index" in lines L2, L5 and L9 is [Bland's rule](/bland-rule/).

```pseudo id=main
CHECK()                                   ▷ decide the bounds now in force
L1  loop
L2      x_i ← the basic variable of least index with β(x_i) < l_i or β(x_i) > u_i
L3      if there is no such x_i then return SAT
L4      if β(x_i) < l_i then
L5          x_j ← the nonbasic of least index with (a_ij > 0 and β(x_j) < u_j) or (a_ij < 0 and β(x_j) > l_j)
L6          if there is no such x_j then return UNSAT with {x_i ≥ l_i} ∪ {x_j ≤ u_j : a_ij > 0} ∪ {x_j ≥ l_j : a_ij < 0}
L7          PIVOT-AND-UPDATE(x_i, x_j, l_i)
L8      else                              ▷ β(x_i) > u_i
L9          x_j ← the nonbasic of least index with (a_ij < 0 and β(x_j) < u_j) or (a_ij > 0 and β(x_j) > l_j)
L10         if there is no such x_j then return UNSAT with {x_i ≤ u_i} ∪ {x_j ≥ l_j : a_ij > 0} ∪ {x_j ≤ u_j : a_ij < 0}
L11         PIVOT-AND-UPDATE(x_i, x_j, u_i)

ASSERT-UPPER(x_i ≤ c)                     ▷ ASSERT-LOWER is the mirror image
L12 if c ≥ u_i then return OK             ▷ not tighter: nothing to do
L13 if c < l_i then return UNSAT with {x_i ≤ c, x_i ≥ l_i}
L14 u_i ← c                               ▷ and push the old u_i on the trail
L15 if x_i is nonbasic and β(x_i) > c then UPDATE(x_i, c)
L16 return OK

UPDATE(x_j, v)                            ▷ x_j is nonbasic
L17 for each basic x_k do β(x_k) ← β(x_k) + a_kj (v − β(x_j))
L18 β(x_j) ← v

PIVOT-AND-UPDATE(x_i, x_j, v)             ▷ x_i basic, x_j nonbasic, a_ij ≠ 0
L19 θ ← (v − β(x_i)) / a_ij
L20 β(x_i) ← v; β(x_j) ← β(x_j) + θ
L21 for each basic x_k ≠ x_i do β(x_k) ← β(x_k) + a_kj θ
L22 PIVOT(x_i, x_j)                       ▷ solve the row of x_i for x_j
```

CHECK looks for the first basic variable that breaks a bound (line L2). To push $x_i$ up to $l_i$, it needs a nonbasic $x_j$ that can move in the right direction: up if $a_{ij} > 0$, down if $a_{ij} < 0$, and not past its own bound (line L5). PIVOT-AND-UPDATE sets $x_i$ to exactly $l_i$, moves $x_j$ by the amount $\theta$ that this takes, and then swaps the roles of the two variables with a [pivot](/pivot-operation/). The new nonbasic $x_i$ sits on its bound, so each nonbasic variable stays inside its bounds. If no $x_j$ can move, the row of $x_i$ is at its largest possible value and still below $l_i$, and the bounds in line L6 are the conflict.

**Backtracking.** PUSH records the length of the bound trail, and POP restores the bounds above that point. The assignment and the tableau stay as they are: POP only makes bounds looser, so each nonbasic variable is still inside its bounds, and the assignment still meets each row. This is the reason why the method suits [DPLL(T)](/dpll-t/) and [incremental solving](/incremental-solving/): undoing a decision costs time linear in the number of undone bounds, with no pivot.

**The certificate.** Each bound in a conflict gets a multiplier: 1 for the bound of $x_i$, and $|a_{ij}|$ for the bound of $x_j$. The weighted sum of the bounds, with each slack replaced by its definition, has coefficient 0 on each variable and a constant that shows $0 < 0$ or $0 \le$ a negative number. This is a [Farkas](/farkas-lemma/) certificate, and the [theory conflict explanation](/theory-conflict-explanation/) that DPLL(T) turns into a learned clause.

## Example

Decide $x + y \ge 4$, $x - y \le 1$, $x \le 1$ and $y \le 2$. The slacks are $s_1 = x + y$ and $s_2 = x - y$, with the order $x, y, s_1, s_2$. The bounds are $s_1 \ge 4$, $s_2 \le 1$, $x \le 1$ and $y \le 2$. All four asserts find $\beta = 0$ inside the new bounds of the nonbasic $x$ and $y$, so they make no update.

| step | basis and rows | $\beta(x), \beta(y), \beta(s_1), \beta(s_2)$ | action |
|---|---|---|---|
| start | $s_1 = x + y$, $s_2 = x - y$ | 0, 0, 0, 0 | $s_1 = 0 < 4$; $x$ can go up |
| pivot 1 | $x = s_1 - y$, $s_2 = s_1 - 2y$ | 4, 0, 4, 4 | $x = 4 > 1$; $y$ (coefficient $-1$) can go up |
| pivot 2 | $y = s_1 - x$, $s_2 = 2x - s_1$ | 1, 3, 4, $-2$ | $y = 3 > 2$; $x$ is at $u_x$, $s_1$ is at $l_{s_1}$ |
| UNSAT | | | conflict $\{y \le 2, x \le 1, x + y \ge 4\}$ |

In the last row, $y = s_1 - x$ is above $u_y = 2$, but $y$ can only go down if $s_1$ goes down or $x$ goes up, and both are on a bound. The certificate is $(y - 2) + (x - 1) + (4 - (x + y)) = 1$: each term is at most 0 in a model, but the sum is 1. The atom $x - y \le 1$ is not in the conflict. Without $y \le 2$, the same two pivots stop at the model $x = 1$, $y = 3$.

## Correctness

The method keeps three invariants: the tableau is equivalent to the slack definitions, the assignment meets each row, and each nonbasic variable is inside its bounds. If CHECK returns SAT, all variables are inside their bounds, and a rational $\delta_0$ turns the pair values into a rational model. If it returns UNSAT, the conflict is a Farkas certificate, so no real model exists.

**Termination.** With the least-index choices of lines L2, L5 and L9, CHECK stops on each input. The proof is Bland's argument adapted to bounds: take the variable of largest index that enters and leaves the basis forever, compare the assignments at a pivot where it leaves and a later pivot where it enters, and the row of the variable that leaves at the second pivot gives a sum that must be both negative and positive. The full proof is below.

## Complexity

The costs are in the [real RAM](/real-ram/) with exact rational operations at unit cost.

- **One pivot.** PIVOT rewrites the $m$ rows, each with up to $n$ entries, so it takes $O(m n)$ operations. UPDATE and lines L19 to L21 take $O(m)$. Line L2 scans $m$ basic variables, and lines L5 and L9 scan one row of $n$ entries.
- **The number of pivots.** Inside one CHECK, each nonbasic variable holds its value from the start of the call or one of its two bounds, so a state is fixed by the basis and at most $3^{n+m}$ choices of values. No state repeats (otherwise the run would loop forever, which the termination proof excludes), so there are fewer than $\binom{n+m}{m} 3^{n+m} \le 6^{n+m}$ pivots, and the worst case is $O(6^{n+m} m n)$. This bound is crude. No polynomial bound on the pivots is known, and Avis and Chvátal (1978) gave linear programs on which the standard simplex method with Bland's rule makes exponentially many pivots.
- **Assert and backtrack.** ASSERT-UPPER takes $O(m)$ for its UPDATE. POP takes time linear in the number of bounds it restores.
- **Space.** The tableau has $m$ rows over $n$ columns: $\Theta(m n)$.

In practice the tableau is sparse, rows have few entries, and most checks need few pivots; these are measured observations, not bounds. A polynomial bound for the problem comes from other methods: [LP is in P](/lp-in-p/).

## Properties

- **Incremental.** New atoms only tighten bounds, and backtracking only loosens them. The tableau keeps the pivots of earlier checks, so a check after a small change usually starts close to a solution.
- **Exact.** All arithmetic is on rationals. Floating-point pivots give wrong answers on some inputs.
- **Small explanations.** A conflict holds the bounds of one row plus the violated bound, so it has at most $n + 1$ atoms.
- **No objective.** The method checks feasibility only. [Optimization modulo theories](/optimization-modulo-theories/) adds an objective on top of it.

## Variants and improvements

- **Theory propagation.** From a row and the current bounds, derive bounds on other variables, and tell the SAT solver which atoms are now implied. This is [theory propagation](/theory-propagation/).
- **Other pivot rules.** Solvers use faster rules to pick $x_i$ and $x_j$ in practice, and fall back to Bland's rule when the search seems to repeat, to keep the termination guarantee.
- **Integers.** For [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/), the same tableau is the relaxation inside branch and bound and [Gomory cuts](/gomory-cutting-plane-algorithm/).
- **Difference constraints.** For atoms $x - y \le c$ only, a graph method is faster: see [difference logic](/difference-logic-satisfiability/).

## When to use it

Use the general simplex as the theory solver for linear real arithmetic inside an SMT solver, when atoms arrive and leave in a stack order and conflicts must be small. For one large linear program with an objective, a standard LP solver (the [revised simplex method](/revised-simplex-method/) or an [interior point method](/interior-point-method/)) is faster. For a small system with few variables, [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) is simpler but can blow up. For pure difference constraints, use the [Bellman-Ford](/bellman-ford/) reduction.

## Pitfalls

- **Restoring the assignment on POP.** It is not needed and it costs time. Lines L14 and L15 only tighten bounds, and POP only loosens them, so the old assignment is still valid.
- **Dropping the least-index rule.** If line L2 or line L5 picks variables by another rule with no fallback, the method can cycle. Keep Bland's rule, or switch to it after a fixed number of pivots.
- **Rounding.** Do not use floating point in lines L19 to L21. A rounding error can turn a feasible system into a false conflict or the reverse.
- **Treating $x < c$ as $x \le c$.** The atoms $x < 1$ and $x > 1$ have no model, but $x \le 1$ and $x \ge 1$ do. Keep the $\delta$ part in each bound and compare pairs lexicographically.
- **Reporting all atoms as the conflict.** It is a correct conflict but a useless learned clause. Return only the bounds of line L6 or line L10.

## Implementations

## History

Dutertre and de Moura presented the method at CAV 2006 as the arithmetic solver of the Yices SMT solver. Its main ideas were the fixed tableau with bounds, the cheap backtracking, and strict bounds with an infinitesimal $\delta$. The termination argument goes back to Bland's least-index rule of 1977 for the standard simplex method.

## References
