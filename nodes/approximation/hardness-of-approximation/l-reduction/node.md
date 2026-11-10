---
tag: VK0B3P
kind: definition
slug: l-reduction
name: L-reduction
aliases:
- linear reduction
area: approximation/hardness-of-approximation
level: advanced
summary: The linear reduction of Papadimitriou and Yannakakis. Two constants bound the target optimum and the error transfer, so a PTAS for the target gives a PTAS for the source.
prereqs: [approximation-preserving-reduction]
see_also: [ptas-reduction, apx-completeness, apx-class, ptas, vertex-cover, maximum-independent-set, max-sat, transitivity-of-reductions]
sources:
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: pp. 425 to 440 (the definition of the L-reduction, its composition, PTAS preservation, and the MAX SNP-complete problems)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Section 16.2, Definition 16.4 and Theorems 16.5 and 16.6 (ratio transfer), Theorem 16.8 (MAX E3SAT to independent set) and Theorems 16.10 and 16.11 (bounded degree vertex cover)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 8, Approximation Preserving Reductions (L-reductions and their relation to AP-reductions)
  - paper: doi:10.1137/S0097539796304220
    title: Pierluigi Crescenzi, Viggo Kann, Riccardo Silvestri and Luca Trevisan, Structure in approximation classes, SIAM Journal on Computing 28(5), 1999
    locator: The comparison of L-reductions with AP-reductions and PTAS-reductions
---

An **L-reduction** ("linear reduction") from an optimization problem $A$ to an optimization problem $B$ is a pair of polynomial-time maps, instances forward and solutions back, with two constants: one bounds the optimum of the new instance by the old optimum, and one bounds the error of the mapped-back solution by the error in $B$. Papadimitriou and Yannakakis (1991) introduced it to define MAX SNP-completeness. Its key property is that it preserves approximation schemes: if $B$ has a PTAS, then so does $A$. It is the reduction that most textbook APX-hardness proofs use.

## Definition

**Notation.** $A$ and $B$ are [NPO](/npo-class/) problems. For an instance $x$ and a feasible solution $y$, $c_A(x, y)$ is the measure and $\mathrm{OPT}_A(x)$ the optimum; the same for $B$. The *error* of $y$ is $|\mathrm{OPT}(x) - c(x, y)|$, an absolute difference that works for min and max alike. Ratios follow the site convention: a minimization $\rho$-approximation has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$, and a maximization $\alpha$-approximation has $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$. To avoid a clash, the two L-reduction constants are written $a$ and $b$ (Williamson and Shmoys write them the same way).

**L-reduction.** $A \le_L B$ if there are polynomial-time maps $f$ and $g$ and constants $a, b > 0$ such that, for each instance $x$ of $A$, $f(x)$ is an instance of $B$, for each feasible solution $y$ of $f(x)$, $g(x, y)$ is a feasible solution of $x$, and

$$\text{(L1)}\quad \mathrm{OPT}_B(f(x)) \le a \cdot \mathrm{OPT}_A(x),$$

$$\text{(L2)}\quad |\mathrm{OPT}_A(x) - c_A(x, g(x, y))| \le b \cdot |\mathrm{OPT}_B(f(x)) - c_B(f(x), y)|.$$

(L1) says that $f$ does not inflate the optimum by more than a constant factor. (L2) says that $g$ does not inflate the error by more than a constant factor. Together they say that the *relative* error grows by at most the factor $ab$.

**Theorem 1 (an L-reduction preserves a PTAS).** If $A \le_L B$ with constants $a, b$ and $B$ has a PTAS, then $A$ has a PTAS.

*Proof.* Fix $\varepsilon > 0$ and set $\delta = \varepsilon/(ab)$. Run the scheme of $B$ with parameter $\delta$ on $f(x)$ and get $y$. If $B$ is a minimization problem, $c_B \le (1 + \delta)\,\mathrm{OPT}_B$; if it is a maximization problem, $c_B \ge (1 - \delta)\,\mathrm{OPT}_B$. In both cases

$$|\mathrm{OPT}_B(f(x)) - c_B(f(x), y)| \le \delta\,\mathrm{OPT}_B(f(x)).$$

By (L2) and then (L1),

$$|\mathrm{OPT}_A(x) - c_A(x, g(x, y))| \le b\,\delta\,\mathrm{OPT}_B(f(x)) \le a b \delta\,\mathrm{OPT}_A(x) = \varepsilon\,\mathrm{OPT}_A(x).$$

If $A$ is a minimization problem this reads $c_A \le (1 + \varepsilon)\,\mathrm{OPT}_A$; if it is a maximization problem it reads $c_A \ge (1 - \varepsilon)\,\mathrm{OPT}_A$. The time is that of $f$, of the scheme for the fixed $\delta$, and of $g$, which is polynomial for each fixed $\varepsilon$. $\blacksquare$

**Theorem 2 (ratio transfer).** Let $A \le_L B$ with constants $a, b$, and let $\mathcal{B}$ have performance ratio $R_B \le r$ on $B$ (so $\rho = r$ if $B$ is a minimization problem and $\alpha = 1/r$ if it is a maximization problem).

1. If $A$ is a minimization problem, $g \circ \mathcal{B} \circ f$ has ratio $\rho_A \le 1 + ab(r - 1)$.
2. If $A$ and $B$ are maximization problems and $\mathcal{B}$ is an $\alpha$-approximation, $g \circ \mathcal{B} \circ f$ is a $(1 - ab(1 - \alpha))$-approximation, which is useful when $ab(1 - \alpha) < 1$.

*Proof.* If $B$ is a minimization problem, the error of $y$ is at most $(r - 1)\,\mathrm{OPT}_B$. If $B$ is a maximization problem, it is at most $(1 - 1/r)\,\mathrm{OPT}_B \le (r - 1)\,\mathrm{OPT}_B$. By (L2) and (L1) the error of $g(x, y)$ is at most $ab(r - 1)\,\mathrm{OPT}_A$, which gives part 1. For part 2, the error in $B$ is at most $(1 - \alpha)\,\mathrm{OPT}_B$, so $c_A \ge \mathrm{OPT}_A - ab(1 - \alpha)\,\mathrm{OPT}_A$. $\blacksquare$

Part 1 shows that L-reductions to any problem in [APX](/apx-class/) keep a minimization problem $A$ in APX. For a maximization $A$ the bound of part 2 is void when $ab(1 - \alpha) \ge 1$, so this argument does not show that APX is preserved. Williamson and Shmoys state both directions as Theorems 16.5 and 16.6.

**Theorem 3 (an L-reduction is a PTAS-reduction).** If $A \le_L B$ with constants $a, b$, then $(f, g, c)$ with $c(r) = 1 + (1 - 1/r)/(ab)$ is a [PTAS-reduction](/ptas-reduction/).

*Proof.* Let $\delta = (1 - 1/r)/(ab)$ and suppose $R_B(f(x), y) \le 1 + \delta$. As in Theorem 1, the error of $y$ is at most $\delta\,\mathrm{OPT}_B$ (for a maximization $B$, $\mathrm{OPT}_B - c_B \le \frac{\delta}{1 + \delta}\mathrm{OPT}_B \le \delta\,\mathrm{OPT}_B$). So the error of $g(x, y)$ is at most $ab\delta\,\mathrm{OPT}_A = (1 - 1/r)\,\mathrm{OPT}_A$. For a maximization $A$, $c_A \ge \mathrm{OPT}_A / r$. For a minimization $A$, $c_A \le (2 - 1/r)\,\mathrm{OPT}_A \le r\,\mathrm{OPT}_A$, because $r^2 - 2r + 1 \ge 0$. In both cases $R_A \le r$. $\blacksquare$

**Theorem 4 (composition).** If $A \le_L B$ with $(f_1, g_1, a_1, b_1)$ and $B \le_L C$ with $(f_2, g_2, a_2, b_2)$, then $A \le_L C$ with $f(x) = f_2(f_1(x))$, $g(x, z) = g_1(x, g_2(f_1(x), z))$ and constants $(a_1 a_2,\ b_1 b_2)$.

*Proof.* (L1): $\mathrm{OPT}_C(f(x)) \le a_2\,\mathrm{OPT}_B(f_1(x)) \le a_2 a_1\,\mathrm{OPT}_A(x)$. (L2): the error of $g(x, z)$ in $A$ is at most $b_1$ times the error of $g_2(f_1(x), z)$ in $B$, which is at most $b_1 b_2$ times the error of $z$ in $C$. $\blacksquare$

## Examples and non-examples

**MAX 3SAT to maximum independent set, with $a = b = 1$.** For clauses $C_1, \ldots, C_m$, $f$ builds the graph with one vertex per literal occurrence, edges inside each clause, and edges between complementary occurrences. The map $g$ sets the literals of an independent set $S$ to true and the other variables to false. Then $\alpha(G) = \mathrm{OPT}_A$, which is (L1) with $a = 1$, and $|S| \le c_A(g(S)) \le \mathrm{OPT}_A$, so $\mathrm{OPT}_A - c_A(g(S)) \le \alpha(G) - |S|$, which is (L2) with $b = 1$. This is Theorem 16.8 of Williamson and Shmoys.

**Bounded degree independent set to vertex cover, with $a = B$, $b = 1$.** Let $G$ have $n$ vertices and maximum degree $B$. Take $f$ the identity and $g(C) = V \setminus C$. The greedy algorithm (pick a vertex, delete it and its at most $B$ neighbours) gives $\alpha(G) \ge n/(B + 1)$, so $\tau(G) = n - \alpha(G) \le B\,\alpha(G)$: (L1) with $a = B$. For each cover $C$, $\alpha(G) - |V \setminus C| = |C| - \tau(G)$: (L2) with $b = 1$. The complete graph $K_{B+1}$ has $\alpha = 1$ and $\tau = B$, so $a = B$ is the least constant that works for all such graphs.

**Bounded degree vertex cover to independent set, with $a = B$, $b = 1$.** Now let $G$ have maximum degree $B$ and no isolated vertex, and again take complements. Let $I$ be a maximum independent set, so $V \setminus I$ is a minimum cover. Each vertex of $I$ has a neighbour, which lies in $V \setminus I$, and each vertex of $V \setminus I$ has at most $B$ neighbours in $I$. Counting the edges between the two sides gives $\alpha(G) \le B\,\tau(G)$: (L1) with $a = B$. (L2) holds with $b = 1$ as before. The star $K_{1,B}$ has $\tau = 1$ and $\alpha = B$, so $a = B$ is again the least constant. A perfect matching has $\alpha = \tau$, so it needs only $a = 1$.

**Non-example: vertex cover to independent set on all graphs.** The same maps fail (L1) when the degree is not bounded. The star $K_{1,k}$ has $\tau = 1$ and $\alpha = k$, so no constant $a$ works for all $k$. This is consistent with the facts that vertex cover is in APX and independent set is not (unless P = NP).

**Non-example: a reduction that shifts the optimum.** Map an instance of MAX 3SAT with $m$ clauses to the same formula with $m^2$ new clauses $(z_j \lor \lnot z_j)$ that are always true, and let $g$ forget the $z_j$. The errors are the same, so (L2) holds with $b = 1$. But $\mathrm{OPT}_B = \mathrm{OPT}_A + m^2$ and $\mathrm{OPT}_A \le m$, so $\mathrm{OPT}_B / \mathrm{OPT}_A \ge m$ grows without bound, and (L1) fails. The new instance is easy to approximate within a factor close to 1, which says nothing about the old one.

**Brute-force check of the constants.** The Python code of this page takes small instances, lists all feasible solutions, and returns the least constants $a$ and $b$ that each instance needs. Its tests run it on the three reductions above: MAX 3SAT to independent set gives $a = 1$ and $b \le 1$; the complement maps in graphs of degree at most $B$ give $a \le B$ and $b \le 1$; $K_{B+1}$ and the star $K_{1,B}$ reach $a = B$.

## Related definitions

- **[Approximation-preserving reduction](/approximation-preserving-reduction/).** The umbrella page, with the strict, E-, AP- and gap-preserving kinds and a table of the classes each kind preserves.
- **[PTAS-reduction](/ptas-reduction/).** Theorem 3 shows that each L-reduction is one. The PTAS-reduction allows the maps to depend on the target ratio, so it is more general.
- **E-reduction.** Khanna, Motwani, Sudan and Vazirani replace (L1) by a polynomial bound and (L2) by a bound on the relative error; this kind also preserves FPTAS.
- **[APX-completeness](/apx-completeness/).** Papadimitriou and Yannakakis used L-reductions to prove MAX SNP-completeness of MAX 3SAT, MAX 2SAT, MAX CUT, and bounded degree independent set and vertex cover. With the PCP theorem these problems have no PTAS unless P = NP.

## References
