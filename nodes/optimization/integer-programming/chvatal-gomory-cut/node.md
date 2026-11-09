---
tag: T2GZS5
kind: concept
slug: chvatal-gomory-cut
name: Chvátal-Gomory cut
aliases:
- Chvátal cut
- Gomory-Chvátal cut
- rank-one cut
- CG cut
- integer rounding cut
area: optimization/integer-programming
level: advanced
summary: Valid inequality from rounding a nonnegative combination of constraints with integer coefficients.
prereqs: [lp-relaxation, integer-hull]
see_also: [chvatal-closure, chvatal-gomory-finite-convergence, gomory-cutting-plane-algorithm, zero-half-cut, mixed-integer-rounding-inequality, gomory-mixed-integer-cut, cutting-plane-method-integer-programming, matching-polytope]
sources:
  - paper: "Vašek Chvátal, Edmonds polytopes and a hierarchy of combinatorial problems, Discrete Mathematics 4 (1973), 305 to 337"
    locator: the definition of the rounding operation and of the rank of an inequality
  - paper: doi:10.1090/S0002-9904-1958-10224-4
    title: Ralph E. Gomory, Outline of an algorithm for integer solutions to linear programs, Bulletin of the American Mathematical Society 64(5), 1958
    locator: the fractional cut from a row of the simplex tableau
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (Chvátal inequalities and the Chvátal closure)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 23 (cutting planes)
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part II, Chapter 1 (the Chvátal-Gomory procedure)
  - paper: "Friedrich Eisenbrand, On the membership problem for the elementary closure of a polyhedron, Combinatorica 19 (1999), 297 to 300"
    locator: NP-hardness of separating rank-one cuts
---

A Chvátal-Gomory cut is an inequality obtained from a system $Ax \le b$ by two steps: take a nonnegative combination $u^T A x \le u^T b$ whose left side has integer coefficients, then round the right side down. Every integer point of $P = \{x : Ax \le b\}$ satisfies the result, but fractional points of $P$ may not. These cuts are the basic cutting planes of integer programming. The fractional cuts of [Gomory's algorithm](/gomory-cutting-plane-algorithm/) are of this kind, and repeated rounds of them reach the [integer hull](/integer-hull/), by the [finite convergence theorem](/chvatal-gomory-finite-convergence/).

## In plain words

Suppose that whole numbers $x$ and $y$ satisfy $2x + 2y \le 3$. Divide by 2: $x + y \le 1.5$. The left side is a whole number, so it cannot be 1.5. It must be at most 1. That is the whole trick: combine the rules so that the left side is a whole number for every whole-number answer, and then round the right side down.

The new rule keeps every whole-number answer, but it can cut away fractional points, such as $x = y = 0.75$. A solver that adds such rules makes the relaxed problem tighter, and its answer moves toward a whole-number one.

## The idea

**The cut.** Let $P = \{x \in \mathbb{R}^n : Ax \le b\}$ with $A$, $b$ rational. Let $u \ge 0$ be a vector with $u^T A \in \mathbb{Z}^n$. Then

$$(u^T A)\, x \le \lfloor u^T b \rfloor$$

is valid for every $x \in P \cap \mathbb{Z}^n$.

*Proof.* For $x \in P$, $u \ge 0$ gives $u^T A x \le u^T b$. If $x$ is also integral, $u^T A x$ is an integer, and an integer that is at most $u^T b$ is at most $\lfloor u^T b \rfloor$. $\square$

When $P$ includes $x \ge 0$, the integrality condition on $u^T A$ can be dropped: for $P = \{x \ge 0 : Ax \le b\}$ and each $u \ge 0$,

$$\sum_j \lfloor u^T A_j \rfloor\, x_j \le \lfloor u^T b \rfloor$$

is valid, where $A_j$ is column $j$. Rounding the coefficients down only makes the left side smaller when $x \ge 0$, and then the argument above applies. This is the same cut as before, with multipliers on the rows $-x_j \le 0$.

**The cut can be useless or strong.** If $u^T b$ is an integer, the cut is implied by $Ax \le b$. It can cut off a point $\bar x \in P$ only when $u^T b$ is fractional and $u^T A \bar x > \lfloor u^T b \rfloor$. The *rank* of an inequality valid for $P_I$ is the least number of rounds of CG cuts needed to derive it, and rank-one cuts are those obtained in one round from the original system.

**Only fractional multipliers matter.** If $u$ is replaced by $u - \lfloor u \rfloor$, componentwise, the cut changes by $\lfloor u \rfloor^T (Ax \le b)$, which is implied by the original system. So for a fixed $P$, all rank-one cuts come from $0 \le u < 1$, and since the cuts that matter are those whose $u^T A$ lies in a bounded set, there are finitely many of them up to dominance. This is why the [Chvátal closure](/chvatal-closure/) is a polyhedron.

**Proofs with cuts.** Chvátal (1973) viewed a sequence of CG cuts as a proof: each line is a nonnegative combination of earlier lines with rounding. Every valid inequality for the integer points of a rational polytope has such a proof, and an empty integer set has a proof of $0 \le -1$. The length of such proofs can be exponential: Pudlák (1997) proved exponential lower bounds for CG proofs of the clique-coloring tautologies.

**Separation is hard.** Given $\bar x \in P$, deciding whether some rank-one CG cut cuts off $\bar x$ is NP-hard (Eisenbrand 1999). Even the special case of [zero-half cuts](/zero-half-cut/), where $u \in \{0, 1/2\}^m$, is NP-hard to separate (Caprara and Fischetti, 1996). Solvers therefore use heuristics: cuts read from the simplex tableau, as in [Gomory's algorithm](/gomory-cutting-plane-algorithm/), aggregation heuristics, and small integer programs for $u$.

## Examples

**The running example.** Let $P = \{x \ge 0 : 3x_1 + 2x_2 \le 6,\ -3x_1 + 2x_2 \le 0\}$, whose LP maximum of $x_2$ is at the vertex $(1, 3/2)$. The integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$.

| $u$ | $u^T A$ | $u^T b$ | cut | value at $(1, 3/2)$ |
|---|---|---|---|---|
| $(1/4,\ 1/4)$ | $(0,\ 1)$ | $3/2$ | $x_2 \le 1$ | $3/2$, cut off |
| $(1/12,\ 5/12)$ | $(-1,\ 1)$ | $1/2$ | $-x_1 + x_2 \le 0$ | $1/2$, cut off |
| $(9/20,\ 1/10)$ | $(21/20,\ 11/10)$ | $27/10$ | $x_1 + x_2 \le 2$ | $5/2$, cut off |
| $(1/2,\ 0)$ | $(3/2,\ 1)$ | $3$ | $x_1 + x_2 \le 3$ | $5/2$, valid but weak |

The third row uses $x \ge 0$ to round the coefficients down. The cuts $-x_1 + x_2 \le 0$ and $x_1 + x_2 \le 2$, with $x_2 \ge 0$, describe $P_I = \operatorname{conv}\{(0,0), (2,0), (1,1)\}$, so all facets of $P_I$ have rank at most one. The last row has an integral $u^T b$, and its cut is implied by $P$.

**Odd set inequalities.** In a triangle with edges $x_{12}$, $x_{13}$, $x_{23}$, add the three degree constraints $x(\delta(v)) \le 1$ with $u_v = 1/2$:

$$x_{12} + x_{13} + x_{23} \le \lfloor 3/2 \rfloor = 1.$$

This cuts off $(1/2, 1/2, 1/2)$. In general, for an odd vertex set $S$, half the sum of the degree constraints of $S$, with the coefficients of the edges that leave $S$ rounded down using $x \ge 0$, gives $x(E(S)) \le \lfloor |S|/2 \rfloor$. These are Edmonds' odd set inequalities, so the [matching polytope](/matching-polytope/) is the first Chvátal closure of the degree polytope.

**Odd cycles in stable sets.** For an [independent set](/independent-set/) problem with edge constraints $x_u + x_v \le 1$, sum them around an odd cycle $C$ with $u_e = 1/2$. Each vertex of $C$ gets the coefficient 1, and the cut is $\sum_{v \in C} x_v \le \lfloor |C|/2 \rfloor$.

**Infeasibility by parity.** The system $2x_1 + 2x_2 \le 1$, $-2x_1 - 2x_2 \le -1$ has real solutions but no integer ones. With $u = 1/2$, the two cuts are $x_1 + x_2 \le 0$ and $-x_1 - x_2 \le -1$. Their sum is $0 \le -1$, a CG proof that the integer set is empty.

**A non-example.** For $P = \{x \in \mathbb{R} : 2x \le -1\}$, without $x \ge 0$, the multiplier $u = 1/4$ gives $\tfrac12 x \le -\tfrac14$. Rounding the coefficient $1/2$ down to 0 gives $0 \le -1$, which would declare the integer set empty, but $x = -1$ is a feasible integer point. Without $x \ge 0$, the coefficients $u^T A$ must already be integers. The correct cut, with $u = 1/2$, is $x \le \lfloor -1/2 \rfloor = -1$.

## Where it is used

- **[Gomory's algorithm](/gomory-cutting-plane-algorithm/).** The fractional cut of a tableau row is a CG cut, and with the lexicographic rule the algorithm is finite.
- **[Branch and cut](/branch-and-cut/).** Solvers separate CG cuts heuristically, together with [zero-half cuts](/zero-half-cut/), [Gomory mixed-integer cuts](/gomory-mixed-integer-cut/) and [MIR inequalities](/mixed-integer-rounding-inequality/), which extend the rounding idea to continuous variables.
- **Polyhedral combinatorics.** Many facet classes of combinatorial polytopes, such as odd set, odd cycle, blossom and comb inequalities, are CG cuts of low rank.
- **Proof complexity.** Cutting plane proofs are a proof system for propositional logic, stronger than resolution, and lower bounds on their length are studied in complexity theory.
- **Theory of the closure.** The [Chvátal closure](/chvatal-closure/) and its rank measure how far a formulation is from its integer hull.

## References
