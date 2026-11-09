---
tag: XXNDEM
kind: concept
slug: zero-half-cut
name: Zero-half cut
aliases:
- zero-half inequality
- Caprara-Fischetti cut
- "{0, 1/2}-Chvátal-Gomory cut"
area: optimization/integer-programming
level: research
summary: Chvátal-Gomory cut with multiplier 1/2 applied to constraints with 0/1 combinations.
prereqs: [chvatal-gomory-cut, chvatal-closure]
see_also: [chvatal-gomory-cut, chvatal-closure, matching-polytope, independent-set, traveling-salesman-problem, cutting-plane-method-integer-programming, branch-and-cut, totally-dual-integrality]
sources:
  - paper: "Alberto Caprara and Matteo Fischetti, {0, 1/2}-Chvátal-Gomory cuts, Mathematical Programming 74 (1996), 221 to 235"
    locator: definition, NP-hardness of separation and the polynomial case with at most two odd entries per column
  - paper: "Alberto Caprara, Matteo Fischetti and Adam N. Letchford, On the separation of maximally violated mod-k cuts, Mathematical Programming 87 (2000), 37 to 56"
    locator: maximally violated cuts found by linear algebra over a finite field
  - paper: "Gabriele Andreello, Alberto Caprara and Matteo Fischetti, Embedding {0, 1/2}-cuts in a branch-and-cut framework: a computational study, INFORMS Journal on Computing 19 (2007), 229 to 238"
    locator: heuristic separation and computational results on MIPLIB
  - paper: "Arie M. C. A. Koster, Adrian Zymolka and Manuel Kutschka, Algorithms to separate {0, 1/2}-Chvátal-Gomory cuts, Algorithmica 55 (2009), 375 to 391"
    locator: preprocessing of the mod-2 system and separation heuristics
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (Chvátal-Gomory cuts and their separation)
---

A zero-half cut is a [Chvátal-Gomory cut](/chvatal-gomory-cut/) in which every multiplier is 0 or $\tfrac12$. One adds a set of constraints with integer coefficients so that every variable gets an even coefficient and the right side is odd, halves the sum, and rounds the right side down. Many classical cuts of combinatorial optimization have this form, among them the odd cycle inequalities for stable sets and the blossom inequalities for matching. Caprara and Fischetti (1996) defined the family, showed that separation is NP-hard in general, and found the cases where it is easy. MIP solvers separate zero-half cuts with heuristics.

## In plain words

Pick some of the rules of the problem and add them up. If every unknown appears an even number of times, the sum is twice some whole-number expression. If the total on the right side is odd, say 5, then twice that expression is at most 5, so the expression is at most $2.5$. It is a whole number, so it is at most 2. That last step, from $2.5$ to 2, is where the cut gains strength.

For example, on a cycle of five points, take the rules "at most one of these two neighbors". Each point is in two rules, and the right sides add up to 5. So twice the number of chosen points is at most 5, and at most 2 points can be chosen. A fractional answer that picks half of every point gives $2.5$, so the cut removes it.

## The idea

**Definition.** Let $P = \{x : Ax \le b\}$ with $A$ and $b$ integral, and assume the bounds $x \ge 0$ are among the rows or are known separately. For a set $S$ of rows, let $a_S = \sum_{i \in S} a_i$ and $\beta_S = \sum_{i \in S} b_i$. Let $\mathrm{odd}(S)$ be the set of columns $j$ where $a_{S,j}$ is odd. If $\beta_S$ is odd, then adding the bound rows $-x_j \le 0$ for $j \in \mathrm{odd}(S)$ makes every coefficient even, and halving gives

$$\frac12 \Big(a_S - \sum_{j \in \mathrm{odd}(S)} e_j\Big)^T x \le \frac{\beta_S - 1}{2},$$

the *zero-half cut* of $S$. It is the Chvátal-Gomory cut with multiplier $\tfrac12$ on the rows of $S$ and on the bounds of $\mathrm{odd}(S)$, so it is valid for $P \cap \mathbb{Z}^n$. Every zero-half cut is in the [Chvátal closure](/chvatal-closure/), and the zero-half closure lies between $P$ and $P'$.

**Violation.** Let $x^* \in P$ and let $s^* = b - Ax^* \ge 0$ be the slacks. The left side of the cut at $x^*$ is $\tfrac12(\beta_S - \sum_{i \in S} s^*_i - \sum_{j \in \mathrm{odd}(S)} x^*_j)$, so the violation is

$$\frac12 \Big(1 - \sum_{i \in S} s^*_i - \sum_{j \in \mathrm{odd}(S)} x^*_j\Big).$$

So the cut of $S$ is violated if and only if the weight $w(S) = \sum_{i \in S} s^*_i + \sum_{j \in \mathrm{odd}(S)} x^*_j$ is less than 1, and no zero-half cut is violated by more than $\tfrac12$.

**Separation as a parity problem.** Work over $\mathrm{GF}(2)$, with $\bar A = A \bmod 2$ and $\bar b = b \bmod 2$. A set $S$ is a 0/1 vector $z$, and the problem is

$$\min\ \sum_i s^*_i z_i + \sum_j x^*_j\, [ (z^T \bar A)_j = 1 ] \quad \text{subject to} \quad z^T \bar b = 1.$$

- *In general it is NP-hard* (Caprara and Fischetti, 1996).
- *Two odd entries per column.* If each column of $\bar A$ has at most two ones, the rows can be seen as the nodes of a graph and the columns as its edges. Caprara and Fischetti reduce the problem to a minimum weight odd cycle problem in a graph built from this one, which is solvable in polynomial time. This covers the edge-node incidence systems of matching and stable set problems.
- *Maximally violated cuts.* A cut with violation exactly $\tfrac12$ has $w(S) = 0$. It uses only tight rows and puts odd columns only where $x^*_j = 0$. Finding such an $S$ is a system of linear equations over $\mathrm{GF}(2)$ in the tight rows, which Gaussian elimination solves in polynomial time (Caprara, Fischetti and Letchford, 2000).

Solvers first reduce the mod-2 system: they drop columns with $x^*_j = 0$, rows with slack at least 1, and duplicate or zero columns. Then they search with Gaussian elimination and greedy rules for sets $S$ of small weight (Koster, Zymolka and Kutschka, 2009).

## Examples

**Odd cycles in stable sets.** On the cycle $C_5$ with edge constraints $x_u + x_v \le 1$, take $S$ as all five edges. Every variable appears twice, so $\mathrm{odd}(S) = \emptyset$, and $\beta_S = 5$. The cut is $\sum_{v} x_v \le 2$. The point $x^* = (\tfrac12, \ldots, \tfrac12)$ has all slacks 0, so $w(S) = 0$ and the violation is $\tfrac12$: the left side is $5/2$. The largest stable set of $C_5$ has 2 nodes, so the cut is tight. The same argument for any odd cycle of length $2k+1$ gives the odd cycle inequality $\sum_{v \in C} x_v \le k$ for [independent sets](/independent-set/).

**Blossoms in matching.** For a node set $U$ of odd size in a graph, take the degree rows $x(\delta(v)) \le 1$ for $v \in U$. An edge inside $U$ appears twice and an edge in the cut $\delta(U)$ appears once, so $\mathrm{odd}(S) = \delta(U)$ and $\beta_S = |U|$. The zero-half cut is $x(E(U)) \le (|U| - 1)/2$, the blossom inequality of the [matching polytope](/matching-polytope/). For a triangle with $x_e = \tfrac12$ on its edges and $x_e = 0$ on the cut edges, the weight is 0 and the cut removes the point.

**Parity infeasibility.** The equation $2x_1 + 2x_2 = 1$ is the pair of rows $2x_1 + 2x_2 \le 1$ and $-2x_1 - 2x_2 \le -1$. Each row alone gives a zero-half cut with $S$ a single row: $x_1 + x_2 \le 0$ and $-x_1 - x_2 \le -1$. Their sum is $0 \le -1$, so the system has no integer solution.

## Where it is used

- **MIP solvers.** Zero-half separators run in several solvers, with heuristic separation on the reduced mod-2 system. Andreello, Caprara and Fischetti (2007) showed that they close a useful part of the gap on many MIPLIB instances.
- **Combinatorial polytopes.** Odd cycle inequalities for stable sets, blossom inequalities for matching and $b$-matching, and the comb inequalities of the [traveling salesman problem](/traveling-salesman-problem/) can all be obtained as $\{0, \tfrac12\}$ combinations of simple rows. Zero-half separation gives a generic way to find them without problem-specific code.
- **Mod-$k$ cuts.** The same idea with multipliers in $\{0, \tfrac1k, \ldots, \tfrac{k-1}{k}\}$ gives mod-$k$ cuts, studied by Caprara, Fischetti and Letchford (2000).

## References
