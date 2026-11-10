---
tag: YVSNYR
kind: definition
slug: gap-preserving-reduction
name: Gap-preserving reduction
aliases:
- gap-introducing reduction
area: approximation/hardness-of-approximation
level: advanced
summary: A polynomial-time map of instances that sends large optima to large optima and small optima to small optima, so an NP-hard gap for one problem becomes an NP-hard gap for another.
prereqs: [gap-problem, polynomial-time-reduction]
see_also: [gap-amplification, approximation-preserving-reduction, max-3sat-inapproximability, vertex-cover-inapproximability, clique-inapproximability, label-cover, gadget-reduction, transitivity-of-reductions]
sources:
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems, PWS Publishing, 1997
    locator: Chapter 10, Sanjeev Arora and Carsten Lund, Hardness of Approximations (the definition of gap-preserving reductions and their composition)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 29, Hardness of Approximation (gap-introducing and gap-preserving reductions)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Theorem 16.8 (MAX E3SAT to independent set) and Section 16.3 (reductions from PCPs)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11, Section 11.4, Hardness of approximation for vertex cover and independent set
---

A **gap-preserving reduction** is a polynomial-time map from instances of one optimization problem to instances of another that sends instances with a large optimum to instances with a large optimum and instances with a small optimum to instances with a small optimum. It is a reduction between two [gap problems](/gap-problem/), so it carries NP-hardness of a gap from one problem to the next. Unlike an [approximation-preserving reduction](/approximation-preserving-reduction/), it needs no map of solutions back, which makes it easier to build. When the source is a plain decision problem, the map *introduces* a gap, and the reduction is called gap-introducing.

## Definition

**Notation.** $\Pi$ and $\Pi'$ are [NPO](/npo-class/) problems with optima $\mathrm{OPT}$ and $\mathrm{OPT}'$. The thresholds $c, s, c', s'$ are functions of the instance size. For a maximization problem the gap $[c, s]$ has $c \ge s$, YES means $\mathrm{OPT} \ge c$ and NO means $\mathrm{OPT} < s$; for a minimization problem $c \le s$, YES means $\mathrm{OPT} \le c$ and NO means $\mathrm{OPT} > s$. Ratios follow the site convention: $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$ for minimization and $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$ for maximization.

**Gap-preserving reduction.** A map $f$ computable in polynomial time is a gap-preserving reduction from $\Pi$ with gap $[c, s]$ to $\Pi'$ with gap $[c', s']$ if, for each instance $x$ of $\Pi$,

1. (completeness) $x$ is a YES instance of gap-$\Pi[c, s]$ $\Rightarrow$ $f(x)$ is a YES instance of gap-$\Pi'[c', s']$;
2. (soundness) $x$ is a NO instance of gap-$\Pi[c, s]$ $\Rightarrow$ $f(x)$ is a NO instance of gap-$\Pi'[c', s']$.

For two maximization problems this reads: $\mathrm{OPT}(x) \ge c \Rightarrow \mathrm{OPT}'(f(x)) \ge c'$, and $\mathrm{OPT}(x) < s \Rightarrow \mathrm{OPT}'(f(x)) < s'$. Instances in the middle of the source gap may go anywhere. Arora and Lund write the same thing with a ratio: $\mathrm{OPT} \ge c \Rightarrow \mathrm{OPT}' \ge c'$ and $\mathrm{OPT} < c/g \Rightarrow \mathrm{OPT}' < c'/g'$.

**Gap-introducing reduction.** The source is a decision problem, for example [3SAT](/3-sat/) read as gap-MAX 3SAT$[m, m]$ (all $m$ clauses satisfiable or not), and the target gap has $s' < c'$ (maximization) or $s' > c'$ (minimization). The [PCP theorem](/pcp-theorem/) is a gap-introducing reduction from 3SAT to MAX 3SAT.

**Lemma 1 (transfer of hardness).** If gap-$\Pi[c, s]$ is NP-hard and $f$ is a gap-preserving reduction to gap-$\Pi'[c', s']$, then gap-$\Pi'[c', s']$ is NP-hard. If also $c', s'$ are computable in polynomial time, then $\Pi'$ has no approximation better than the ratio $s'/c'$ unless P = NP.

*Proof.* Let $h$ map 3SAT to gap-$\Pi[c, s]$. Then $f \circ h$ is polynomial, sends satisfiable formulas to YES instances of the target and unsatisfiable ones to NO instances. The ratio statement is the proposition on [gap problem](/gap-problem/). $\blacksquare$

**Lemma 2 (composition).** If $f_1$ is a gap-preserving reduction from gap-$\Pi[c, s]$ to gap-$\Pi'[c', s']$ and $f_2$ is one from gap-$\Pi'[c', s']$ to gap-$\Pi''[c'', s'']$, then $f_2 \circ f_1$ is a gap-preserving reduction from gap-$\Pi[c, s]$ to gap-$\Pi''[c'', s'']$.

*Proof.* The composition of two polynomial-time maps is polynomial, because the output of $f_1$ has polynomial length. If $x$ is YES, $f_1(x)$ is YES for $\Pi'$, so $f_2(f_1(x))$ is YES for $\Pi''$. The same chain holds for NO. The thresholds of $f_2$ must be stated as functions of the size of $f_1(x)$; since that size is polynomial in $|x|$, the composed thresholds are functions of $|x|$ as well. $\blacksquare$

Lemma 2 is why hardness proofs are written as chains: PCP to MAX 3SAT to independent set to vertex cover, each link proved once.

## Examples and non-examples

**MAX 3SAT to maximum independent set (proved here).** For a formula $\varphi$ with clauses $C_1, \ldots, C_m$, each of at most 3 literals, the graph $G_\varphi$ has one vertex $(j, \ell)$ for each occurrence of a literal $\ell$ in $C_j$. Two vertices are joined if they are in the same clause, or if their literals are $x_i$ and $\lnot x_i$.

*Claim.* $\alpha(G_\varphi) = \mathrm{OPT}(\varphi)$, the largest number of clauses that one assignment satisfies.

*Proof.* ($\ge$) Fix an assignment that satisfies $k$ clauses. In each satisfied clause pick one true literal. The picked vertices are in different clauses, and all picked literals are true, so no two are $x_i$ and $\lnot x_i$. This is an independent set of size $k$. ($\le$) Let $S$ be independent. It has at most one vertex per clause. It never contains both $x_i$ and $\lnot x_i$, so setting the literals of $S$ to true, and the other variables to false, is a consistent assignment. It satisfies each clause that has a vertex in $S$, so at least $|S|$ clauses. $\blacksquare$

So $f(\varphi) = G_\varphi$ maps gap-MAX 3SAT$[m, sm]$ to gap-MIS$[m, sm]$, with both completeness and soundness exact. With Håstad's theorem for MAX E3SAT (each clause has exactly 3 literals, gap $[m, (7/8 + \varepsilon)m]$), the graph has $N = 3m$ vertices, and independent set gets the gap $[N/3, (7/8 + \varepsilon)N/3]$: no $(7/8 + \varepsilon)$-approximation unless P = NP. This is Theorem 16.8 of Williamson and Shmoys. Stronger bounds for independent set use the graph products of [gap amplification](/gap-amplification/).

**Worked example.** Let $\varphi$ be the 8 clauses on $x_1, x_2, x_3$ with all 8 sign patterns, from $(x_1 \lor x_2 \lor x_3)$ to $(\lnot x_1 \lor \lnot x_2 \lor \lnot x_3)$. Each assignment falsifies exactly the one clause whose literals are all false, so $\mathrm{OPT} = 7$ and $\varphi$ is unsatisfiable. The graph has 24 vertices and 72 edges: 24 inside the 8 triangles, and 48 between complementary literals (each variable occurs 4 times positive and 4 times negative, which gives 16 pairs, for each of 3 variables). Its independence number is 7.

**Clique to vertex cover.** For a graph $G$ on $n$ vertices, let $f(G) = \bar G$, the complement graph. A set is a clique of $G$ exactly when it is independent in $\bar G$, and its complement is then a vertex cover of $\bar G$, so $\omega(G) + \tau(\bar G) = n$. A clique gap $[cn, sn]$ (YES: $\omega \ge cn$, NO: $\omega < sn$) becomes the vertex cover gap $[(1 - c)n, (1 - s)n]$ (YES: $\tau \le (1 - c)n$, NO: $\tau > (1 - s)n$), with ratio $(1 - s)/(1 - c)$. The [vertex cover inapproximability](/vertex-cover-inapproximability/) page uses this map.

**A gap-introducing reduction: Hamiltonian cycle to TSP.** For a graph $G$ on $n$ vertices, give the edges of $G$ weight 1 and the other pairs weight $rn$. The source is a decision problem; the target gap is $[n, rn]$ for minimization, of ratio $r$. See [general TSP inapproximability](/general-tsp-inapproximability/).

**Non-example: padding that closes the gap.** Map $\varphi$ with $m$ clauses to $\varphi$ plus $m^2$ clauses $(z_i \lor \lnot z_i)$ on new variables. Satisfiable formulas stay satisfiable, so this is a correct Karp reduction from 3SAT to itself. But if at most $sm$ clauses of $\varphi$ can be satisfied, the new formula still has a fraction at least $m^2/(m^2 + m)$ of its clauses satisfiable, which tends to 1. No fixed $s' < 1$ works, so the map does not preserve the gap $[1, s]$ in the fractional form.

**Non-example: a reduction through 2SAT.** No polynomial map can send gap-MAX 3SAT$[1, s]$ to gap-MAX 2SAT$[1, s']$ for $s' < 1$ unless P = NP, because the target is in P (satisfiability of 2CNF is decidable in linear time). The usual reductions to MAX 2SAT lose perfect completeness and map to a gap $[c', s']$ with $c' < 1$.

**Brute-force check.** The Python code of this page builds $G_\varphi$, lists all independent sets of small graphs, and checks on random formulas that $\alpha(G_\varphi) = \mathrm{OPT}(\varphi)$, that the two solution maps in the proof work, and that YES and NO instances of a gap stay on their side. It also checks the worked example: 24 vertices and independence number 7.

## Related definitions

- **[Gap problem](/gap-problem/).** The promise problems that a gap-preserving reduction connects.
- **[Gap amplification](/gap-amplification/).** A gap-preserving reduction from a problem to itself that makes the ratio of the gap more extreme.
- **[Approximation-preserving reduction](/approximation-preserving-reduction/).** Adds a map of solutions back, so it carries algorithms as well as hardness.
- **[Gadget reduction](/gadget-reduction/).** Replaces each constraint by a small fixed set of constraints; with the right weights it is gap-preserving.
- **[Label cover](/label-cover/).** The usual source of gap-preserving reductions for set cover and other problems with large gaps.

## References
