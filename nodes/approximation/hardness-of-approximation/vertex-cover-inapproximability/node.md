---
tag: DAHD4S
kind: theorem
slug: vertex-cover-inapproximability
name: Vertex cover inapproximability
aliases:
- Dinur-Safra vertex cover hardness
area: approximation/hardness-of-approximation
level: advanced
summary: Vertex cover has no ratio below some constant above 1 unless P = NP. Known bounds are 7/6 (Håstad), 1.3606 (Dinur and Safra), √2 - ε (Khot, Minzer and Safra), and 2 - ε under UGC.
prereqs: [max-3sat-inapproximability, gap-preserving-reduction, vertex-cover]
see_also: [vertex-cover-2-approximation, unique-games-conjecture, clique-inapproximability, apx-completeness, l-reduction, label-cover, approximation-threshold, maximum-independent-set]
sources:
  - paper: doi:10.4007/annals.2005.162.439
    title: Irit Dinur and Samuel Safra, On the hardness of approximating minimum vertex cover, Annals of Mathematics 162(1), 2005
    locator: The main theorem, vertex cover has no 10√5 - 21 - ε approximation unless P = NP
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: The 7/6 - ε bound for vertex cover, from the hardness of MAX E3LIN2
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 - ε, Journal of Computer and System Sciences 74(3), 2008
    locator: The 2 - ε bound under the Unique Games Conjecture
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11, Section 11.4, Hardness of approximation for vertex cover and independent set (Theorem 11.15)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Theorem 16.8 (independent set) and Theorems 16.10 and 16.11 (vertex cover in bounded degree graphs), and Section 16.5 (unique games)
---

Minimum [vertex cover](/vertex-cover/) has a simple 2-approximation, but no polynomial-time algorithm can reach a ratio close to 1 unless P = NP. This page proves the first such bound in full: a constant $1 + \varepsilon$ from the gap for MAX 3SAT, carried through the independent set gap by the complement map, and $17/16 - \varepsilon$ when the gap is Håstad's. Stronger bounds are cited: $7/6 - \varepsilon$ by Håstad, $10\sqrt{5} - 21 - \varepsilon \approx 1.3606$ by Dinur and Safra, $\sqrt{2} - \varepsilon$ by Khot, Minzer and Safra, and $2 - \varepsilon$ under the [Unique Games Conjecture](/unique-games-conjecture/). The exact threshold under P $\ne$ NP is open.

## Statement

**Notation.** $G = (V, E)$ is a graph on $n$ vertices. $\tau(G)$ is the size of a minimum vertex cover, $\alpha(G)$ the size of a maximum independent set, and $\omega(G)$ the size of a maximum clique; $\bar G$ is the complement graph. Vertex cover is a minimization problem, so a $\rho$-approximation returns a cover with $\mathrm{ALG} \le \rho\,\tau(G)$, $\rho \ge 1$. For a formula, $m$ is the number of clauses and $\mathrm{OPT}$ the largest number of clauses that one assignment satisfies.

**Lemma 1 (the complement map; proved here).** For each graph $G$ on $n$ vertices, $\omega(G) + \tau(\bar G) = n$ and $\alpha(G) + \tau(G) = n$. A clique gap with $\omega(G) \ge cn$ versus $\omega(G) < sn$ becomes a vertex cover gap with $\tau(\bar G) \le (1 - c)n$ versus $\tau(\bar G) > (1 - s)n$; an independent set gap becomes a vertex cover gap in the same way on $G$ itself.

**Theorem 1 (a constant from the PCP theorem; proved here).** Let $\varepsilon_0 > 0$ be the constant of [MAX 3SAT inapproximability](/max-3sat-inapproximability/), Theorem 1. Unless P = NP, vertex cover has no polynomial-time $\rho$-approximation with $\rho < 1 + \varepsilon_0/2$.

**Theorem 2 (from Håstad's MAX E3SAT gap; proved here from the cited gap).** For each $\varepsilon > 0$, unless P = NP, vertex cover has no polynomial-time $(17/16 - \varepsilon)$-approximation.

**Theorem 3 (cited).** For each $\varepsilon > 0$, unless P = NP, vertex cover has no polynomial-time $\rho$-approximation with:

- $\rho = 7/6 - \varepsilon \approx 1.1667$ (Håstad 2001);
- $\rho = 10\sqrt{5} - 21 - \varepsilon \approx 1.3606$ (Dinur and Safra 2005);
- $\rho = \sqrt{2} - \varepsilon \approx 1.4142$ (Khot, Minzer and Safra, FOCS 2018, completing the 2-to-2 games theorem with Dinur and Kindler).

**Theorem 4 (Khot and Regev 2008; cited).** If the Unique Games Conjecture holds, then for each $\varepsilon > 0$ vertex cover has no polynomial-time $(2 - \varepsilon)$-approximation unless P = NP.

## In plain words

A vertex cover is a set of vertices that touches every edge, and the goal is to use as few as possible. Picking both ends of edges that share no vertex always gives a cover at most twice too large. The theorems on this page say that no fast method can promise to get much closer than that, unless every NP problem has a fast algorithm. The basic proof starts from a formula where it is hard to tell "all clauses satisfiable" from "a fixed fraction must fail". It turns the formula into a graph whose largest set of vertices with no edges between them counts the satisfied clauses. The vertices outside that set form the smallest cover, so a good cover would reveal which case holds. Stronger and more complex proofs push the barrier up, and an unproved conjecture would push it all the way to two.

## Proof

**Proof of Lemma 1.** A set $S \subseteq V$ is a clique of $G$ exactly when no two of its vertices are adjacent in $\bar G$, that is, when $S$ is independent in $\bar G$. A set $S$ is independent in a graph $H$ exactly when $V \setminus S$ is a vertex cover of $H$: an edge with both ends outside $V \setminus S$ would have both ends in $S$. So the complement of a maximum clique of $G$ is a minimum vertex cover of $\bar G$, which gives $\omega(G) + \tau(\bar G) = n$, and the same argument on $G$ gives $\alpha(G) + \tau(G) = n$. The gap statement follows: $\omega \ge cn$ gives $\tau(\bar G) = n - \omega \le (1 - c)n$, and $\omega < sn$ gives $\tau(\bar G) > (1 - s)n$. $\blacksquare$

The two maps take polynomial time and also map solutions both ways, so they are exact reductions. They are not approximation-preserving in general (see [approximation-preserving reduction](/approximation-preserving-reduction/)); they are used here only as [gap-preserving reductions](/gap-preserving-reduction/).

**The clause graph.** Let $\psi$ be a 3CNF formula with clauses $C_1, \ldots, C_m$. The graph $G_\psi$ has one vertex for each occurrence of a literal in a clause, so $n = \sum_j |C_j| \le 3m$ vertices. Two vertices are adjacent if they are in the same clause, or if their literals are $x_i$ and $\lnot x_i$. Then $\alpha(G_\psi) = \mathrm{OPT}(\psi)$: one true literal from each satisfied clause gives an independent set, and an independent set picks at most one literal per clause and never a complementary pair, so it extends to an assignment that satisfies at least $|S|$ clauses. The full proof is on [gap-preserving reduction](/gap-preserving-reduction/). By Lemma 1,

$$\tau(G_\psi) = n - \mathrm{OPT}(\psi).$$

**Proof of Theorem 1.** Apply the map of MAX 3SAT inapproximability, Theorem 1, to an instance $\varphi$ of SAT; it gives $\psi$ with $m$ clauses, each of width at most 3, with $\psi$ satisfiable if $\varphi$ is and $\mathrm{OPT}(\psi) \le (1 - \varepsilon_0)m$ if not. Build $G_\psi$ with $n \le 3m$ vertices.

- If $\varphi$ is satisfiable, $\mathrm{OPT}(\psi) = m$ and $\tau(G_\psi) = n - m$.
- If not, $\tau(G_\psi) \ge n - (1 - \varepsilon_0)m = (n - m) + \varepsilon_0 m$.

Each clause has at least one literal, so $n - m \ge 0$; and $n \le 3m$ gives $n - m \le 2m$. The ratio of the two cases is at least

$$\frac{(n - m) + \varepsilon_0 m}{n - m} = 1 + \frac{\varepsilon_0 m}{n - m} \ge 1 + \frac{\varepsilon_0}{2}.$$

(If $n = m$, all clauses have width 1, the first case gives $\tau = 0$ and the second $\tau > 0$, and any finite ratio separates them.) Let $\mathcal{A}$ be a $\rho$-approximation with $\rho < 1 + \varepsilon_0/2$. On a satisfiable $\varphi$ it returns a cover of size at most $\rho(n - m) < (n - m) + \varepsilon_0 m$; on an unsatisfiable one each cover has size at least $(n - m) + \varepsilon_0 m$. The test "$\mathcal{A}(G_\psi) < (n - m) + \varepsilon_0 m$?" decides SAT, so P = NP. $\blacksquare$

**Proof of Theorem 2.** Håstad's theorem (cited on [MAX 3SAT inapproximability](/max-3sat-inapproximability/)) gives, for each $\delta > 0$, an NP-hard gap for MAX E3SAT: each clause has exactly 3 literals, and either $\mathrm{OPT} = m$ or $\mathrm{OPT} \le (7/8 + \delta)m$. Now $n = 3m$, so $\tau(G_\psi) = 2m$ in the first case and $\tau(G_\psi) \ge 3m - (7/8 + \delta)m = (17/8 - \delta)m$ in the second. The ratio is $(17/8 - \delta)/2 = 17/16 - \delta/2$. Given $\varepsilon > 0$, take $\delta = \varepsilon$; a $(17/16 - \varepsilon)$-approximation returns at most $(17/8 - 2\varepsilon)m < (17/8 - \delta)m$ on YES instances and so separates the cases, as in Theorem 1. $\blacksquare$

**Worked example.** Let $\psi$ be the 8 clauses on $x_1, x_2, x_3$ with all 8 sign patterns. Each assignment falsifies exactly one clause, so $\mathrm{OPT} = 7$. The clause graph has $n = 24$ vertices, and $\tau(G_\psi) = 24 - 7 = 17$, one more than the value $2m = 16$ that a satisfiable formula with 8 clauses of width 3 would give.

**The cited theorems (not proved here).** Håstad's $7/6$ comes from his MAX E3LIN2 result with a gadget graph with one vertex for each satisfying pattern of each equation. Dinur and Safra start from a [label cover](/label-cover/) instance and use biased long codes and an analysis of intersecting families of sets. Khot, Minzer and Safra prove the 2-to-2 games conjecture with imperfect completeness through an expansion theorem for the Grassmann graph, and that conjecture gives $\sqrt{2} - \varepsilon$. Khot and Regev reduce a unique games instance to vertex cover with a long code construction and Fourier analysis.

**Brute-force check.** The Python code of this page computes $\tau$ by branch and bound and $\omega$ by brute force on small random graphs, and checks Lemma 1 with both solution maps, the gap transfer, the identity $\tau(G_\psi) = 3m - \mathrm{OPT}(\psi)$ for formulas with clauses of width 3, and the value 17 of the worked example.

## Consequences

- **No PTAS.** Vertex cover is not in [PTAS](/ptas/) unless P = NP. With the [2-approximation](/vertex-cover-2-approximation/) it is [APX-complete](/apx-completeness/), and the same holds for graphs of bounded degree (Williamson and Shmoys, Theorems 16.10 and 16.11).
- **Independent set.** By Lemma 1, $\alpha(G) = n - \tau(G)$, so the hardness of independent set and of vertex cover come from the same gaps. The ratios differ: a small relative change in $\tau$ can be a large relative change in $\alpha$. Independent set has no $n^{\varepsilon - 1}$-approximation unless P = NP, while vertex cover has ratio 2. See [clique inapproximability](/clique-inapproximability/).
- **Related covering problems.** Vertex cover is the special case of [set cover](/set-cover/) where each element is in two sets, so each hardness bound here also holds for set cover with sets of frequency 2.

## Tightness

The best algorithms reach ratio 2, and Karakostas (2009) gives $2 - \Theta(1/\sqrt{\log n})$. If the Unique Games Conjecture holds, Theorem 4 shows that $2$ is the threshold. Without it, the best hardness is $\sqrt{2} - \varepsilon$, so the threshold under P $\ne$ NP lies between $\sqrt{2}$ and $2$. Theorems 1 and 2, which this page proves, are far from tight; they show only that the threshold is above 1.

## History

Papadimitriou and Yannakakis (1991) showed that vertex cover in bounded degree graphs is MAX SNP-complete. The PCP theorem (Arora, Lund, Motwani, Sudan and Szegedy 1998) then gave a constant above 1, as in Theorem 1. Bellare, Goldreich and Sudan raised the constant, and Håstad (2001) proved $7/6 - \varepsilon$. Dinur and Safra (2005) proved $10\sqrt{5} - 21 - \varepsilon \approx 1.3606$, the first improvement on $7/6$. Khot and Regev (2008) proved $2 - \varepsilon$ under the Unique Games Conjecture. Khot, Minzer and Safra (2018), building on work with Dinur and Kindler, proved the 2-to-2 games theorem, which gives $\sqrt{2} - \varepsilon$ under P $\ne$ NP.

## References
