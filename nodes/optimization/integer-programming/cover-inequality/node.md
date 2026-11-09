---
tag: FR599Q
kind: concept
slug: cover-inequality
name: Cover inequality
aliases:
- knapsack cover inequality
- minimal cover inequality
- lifted cover inequality
area: optimization/integer-programming
level: advanced
summary: Valid inequality for a knapsack row, based on a set whose total weight exceeds the capacity.
prereqs: [binary-integer-programming, knapsack-problem, lp-relaxation]
see_also: [flow-cover-inequality, mixed-integer-rounding-inequality, knapsack-problem, branch-and-cut, cutting-plane-method-integer-programming, integer-hull, binary-integer-programming]
sources:
  - paper: "Harlan Crowder, Ellis L. Johnson and Manfred Padberg, Solving large-scale zero-one linear programming problems, Operations Research 31 (1983), 803 to 834"
    locator: lifted cover inequalities in a cutting plane code for pure 0-1 problems
  - paper: "Egon Balas, Facets of the knapsack polytope, Mathematical Programming 8 (1975), 146 to 164"
    locator: facets from minimal covers and extended covers
  - paper: "Laurence A. Wolsey, Faces for a linear inequality in 0-1 variables, Mathematical Programming 8 (1975), 165 to 178"
    locator: lifting of cover inequalities
  - paper: "Diego Klabjan, George L. Nemhauser and Craig Tovey, The complexity of cover inequality separation, Operations Research Letters 23 (1998), 35 to 40"
    locator: NP-hardness of separation
  - paper: "Zonghao Gu, George L. Nemhauser and Martin W. P. Savelsbergh, Lifted cover inequalities for 0-1 integer programs, INFORMS Journal on Computing 10 (1998), 427 to 437"
    locator: computational study of separation and lifting
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 9 (strong valid inequalities, knapsack covers and lifting)
---

A cover inequality is a valid inequality for a knapsack constraint in binary variables. A cover is a set of items whose total weight is larger than the capacity, so not all of them can be chosen, and the cover inequality says so. Cover inequalities, made stronger by lifting, were the first strong cuts used in general 0-1 programming codes, after Crowder, Johnson and Padberg (1983), and every MIP solver still separates them.

## In plain words

A truck can carry 14 tonnes. Three boxes weigh 7, 6 and 4 tonnes, so together they weigh 17 tonnes and cannot all go on the truck. So at most two of the three can go. That rule is a cover inequality.

The relaxed problem that a solver works with lets it take part of a box. It can take the first two boxes and a quarter of the third, which uses exactly 14 tonnes. The rule "at most two of these three" removes that answer, because $1 + 1 + 1/4$ is more than 2. Lifting then adds other boxes to the rule. A box of 8 tonnes is heavier than all three, so the rule "at most two of these four boxes" is also true, and it is stronger.

## The idea

**Covers.** Let $K = \{x \in \{0,1\}^n : \sum_{j=1}^n a_j x_j \le b\}$ with $0 < a_j \le b$. A set $C$ is a *cover* if $\sum_{j \in C} a_j > b$. The *cover inequality* is

$$\sum_{j \in C} x_j \le |C| - 1.$$

It is valid: a point with $x_j = 1$ for all $j \in C$ has weight more than $b$. The cover is *minimal* if each proper subset of $C$ fits, that is, $\sum_{j \in C} a_j - a_k \le b$ for every $k \in C$. A row $\sum a_j x_j \le b$ with some $a_j < 0$ becomes a knapsack row after the substitution $x_j \to 1 - x_j$, so the same theory applies to each row of a 0-1 program.

**Strength.** For a minimal cover $C$, the cover inequality defines a facet of $\operatorname{conv}\{x \in K : x_j = 0 \text{ for } j \notin C\}$: the $|C|$ points that take all items of $C$ but one are feasible, tight and affinely independent. In the full space it is usually not a facet. Two ways make it stronger.

- *Extended cover.* Let $E(C) = C \cup \{j : a_j \ge \max_{i \in C} a_i\}$. Then $\sum_{j \in E(C)} x_j \le |C| - 1$ is valid, because $|C|$ items of $E(C)$ weigh at least as much as $C$.
- *Lifting.* Add the variables $x_k$, $k \notin C$, one at a time, with the largest coefficient $\alpha_k$ that keeps the inequality valid. If $\sum_{j \in S} \alpha_j x_j \le |C| - 1$ is valid so far, then
$$\alpha_k = |C| - 1 - \max\Big\{\sum_{j \in S} \alpha_j x_j : \sum_{j \in S} a_j x_j \le b - a_k,\ x \in \{0,1\}^S\Big\}.$$
Lifting all variables of a minimal cover gives a facet of $\operatorname{conv}(K)$ (Balas 1975, Wolsey 1975). The result depends on the order. Each step is a small knapsack problem, and sequence-independent lifting with superadditive functions avoids the dependence on the order at some loss of strength.

**Separation.** Given an LP point $x^*$, a cover inequality is violated if and only if $\sum_{j \in C} (1 - x^*_j) < 1$. So the most violated cover comes from the knapsack problem

$$\min\Big\{\sum_j (1 - x^*_j) z_j : \sum_j a_j z_j \ge b + 1,\ z \in \{0,1\}^n\Big\}$$

for integral $a$ and $b$. Separation of cover inequalities is NP-hard (Klabjan, Nemhauser and Tovey, 1998). Solvers use a greedy rule that takes items in increasing order of $(1 - x^*_j)/a_j$, or dynamic programming when $b$ is small, then make the cover minimal and lift it.

## Examples

Take the knapsack row $8x_1 + 7x_2 + 6x_3 + 4x_4 + 2x_5 \le 14$ with $x \in \{0,1\}^5$.

- **Minimal covers.** They are $\{1,2\}$, $\{1,3,4\}$, $\{1,3,5\}$, $\{2,3,4\}$ and $\{2,3,5\}$. The set $\{1,2,3\}$ is a cover but not minimal, since $\{1,2\}$ is already a cover.
- **A violated cover.** The point $x^* = (0, 1, 1, \tfrac14, 0)$ has weight 14, so it is in the LP relaxation. The separation problem gives $C = \{2,3,4\}$ with $\sum_{j \in C}(1 - x^*_j) = 3/4 < 1$, and indeed $x_2 + x_3 + x_4 \le 2$ fails at $x^*$, where the left side is $9/4$.
- **The face is small.** The feasible 0-1 points where $x_2 + x_3 + x_4 = 2$ span a face of dimension only 3 of the 5-dimensional knapsack polytope.
- **Lifting.** Lift $x_1$ first: with $x_1 = 1$, the capacity left is 6, and at most one of items 2, 3, 4 fits, so $\alpha_1 = 2 - 1 = 1$. Then lift $x_5$: with capacity $12$, the best value of $x_1 + x_2 + x_3 + x_4$ is 2 (items 3 and 4), so $\alpha_5 = 0$. The result, $x_1 + x_2 + x_3 + x_4 \le 2$, is here also the extended cover inequality. It has five affinely independent tight points, so it defines a facet of the knapsack polytope.

## Where it is used

- **General 0-1 programs.** Crowder, Johnson and Padberg (1983) solved large 0-1 problems that were out of reach before by adding lifted cover inequalities for each row, together with preprocessing. This work started the use of strong cuts in commercial codes.
- **Branch and cut.** Every MIP solver separates lifted cover inequalities on rows that are knapsacks after complementing, often with extra conditions from set packing rows (GUB covers).
- **Knapsack-structured models.** Capacity rows in [facility location](/facility-location-problem/), bin packing, scheduling and [multiple knapsack](/knapsack-problem/) models give covers that close much of the [integrality gap](/integrality-gap/).
- **Mixed-integer versions.** [Flow cover inequalities](/flow-cover-inequality/) extend the idea to rows with continuous flows and binary switches.

## References
