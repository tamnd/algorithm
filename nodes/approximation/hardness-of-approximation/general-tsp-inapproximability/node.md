---
tag: BA61NJ
kind: theorem
slug: general-tsp-inapproximability
name: General TSP inapproximability
aliases:
- Inapproximability of general TSP
- Sahni-Gonzalez TSP hardness
- no constant-factor approximation for general TSP unless P = NP
- no polynomial ratio for TSP without the triangle inequality
area: approximation/hardness-of-approximation
level: intro
summary: Without the triangle inequality, TSP has no polynomial-time approximation with any ratio α(n) computable in polynomial time, unless P = NP. The proof is a gap reduction from Hamiltonian cycle.
prereqs: [traveling-salesman-problem, hamiltonian-cycle-problem, approximation-ratio, gap-problem]
see_also: [metric-tsp, metric-tsp-inapproximability, christofides-algorithm, asymmetric-tsp, gap-preserving-reduction, apx-class, hamiltonian-cycle-np-completeness, bottleneck-tsp]
sources:
  - paper: doi:10.1145/321958.321975
    title: "S. Sahni and T. Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 1976"
    locator: the result that a polynomial ε-approximate algorithm for the traveling salesperson problem implies P = NP (pp. 555-565 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.4 (the traveling salesman problem, the reduction from Hamiltonian cycle)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 3, Section 3.2 (metric TSP, and the hardness of TSP without the triangle inequality)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972"
    locator: the NP-completeness of the Hamiltonian circuit problem
---

The general TSP inapproximability theorem says that the [traveling salesman problem](/traveling-salesman-problem/) with arbitrary costs has no polynomial-time [approximation algorithm](/approximation-ratio/) with any ratio $\alpha(n)$ that is computable in polynomial time, unless P = NP. Sahni and Gonzalez proved it in 1976 with a [gap reduction](/gap-problem/) from [Hamiltonian cycle](/hamiltonian-cycle-problem/). The proof is short and complete below. The theorem explains why every useful TSP algorithm assumes the triangle inequality, as in [metric TSP](/metric-tsp/).

## Statement

An instance is a complete graph on $n \ge 3$ vertices with positive integer costs $c(u, v) = c(v, u)$, given as a list of numbers in binary. A tour visits each vertex once and returns to its start; its cost is the sum of its $n$ edge costs. $\mathrm{OPT}$ is the least cost of a tour, and $\mathrm{ALG}$ is the cost of the tour that an algorithm returns. The problem is a minimization problem, so a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance (an absolute, worst-case ratio).

**Theorem (Sahni and Gonzalez 1976).** Let $\alpha : \mathbb{N} \to [1, \infty)$ be a function such that $\lceil \alpha(n) \rceil$ can be computed in time polynomial in $n$. (Then $\lceil \alpha(n) \rceil < 2^{p(n)}$ for a polynomial $p$.) If a polynomial-time algorithm returns, on every instance with $n$ vertices, a tour of cost at most $\alpha(n) \cdot \mathrm{OPT}$, then P = NP.

In particular, for each constant $\rho \ge 1$, and also for $\alpha(n) = 2^n$, no polynomial $\alpha(n)$-approximation exists unless P = NP. The result holds already for instances with only two distinct costs.

## In plain words

Take a network of roads, and ask whether a single round trip can use only roads, visiting each town once. This question is hard. Now turn it into a travel cost problem. Each road costs one coin. Each pair of towns with no road gets a huge price, larger than any guarantee an approximate method could promise.

If a road-only round trip exists, the best trip costs as many coins as there are towns. If not, every trip pays the huge price at least once. A fast method with a fixed guarantee would return a cheap trip in the first case and could not in the second case. So it would answer the hard question. Since the price can be as large as we want, no guarantee helps.

## Proof

*The reduction.* Let $G = (V, E)$ be a graph with $n \ge 3$ vertices, an instance of Hamiltonian cycle, which is NP-complete (Karp 1972). Let $\rho = \lceil \alpha(n) \rceil$. Build the TSP instance $I(G)$ on the vertex set $V$ with

$$c(u, v) = \begin{cases} 1 & \text{if } \{u, v\} \in E, \\ \rho n + 1 & \text{if } \{u, v\} \notin E. \end{cases}$$

The instance has $\binom{n}{2}$ costs, and each has at most $\lceil \log_2(\rho n + 2) \rceil \le p(n) + \log_2 n + 2$ binary digits, so $I(G)$ is computed in polynomial time.

*Completeness.* If $G$ has a Hamiltonian cycle, that cycle is a tour whose $n$ edges all cost 1. Each tour has $n$ edges of cost at least 1, so $\mathrm{OPT}(I(G)) = n$.

*Soundness.* If $G$ has no Hamiltonian cycle, then each tour of $I(G)$ uses at least one pair $\{u, v\} \notin E$, because a tour with all its pairs in $E$ is a Hamiltonian cycle of $G$. The other $n - 1$ edges cost at least 1 each, so

$$\mathrm{OPT}(I(G)) \ge (n - 1) + \rho n + 1 = (\rho + 1) n > \rho n.$$

*The decision procedure.* Run the assumed algorithm $A$ on $I(G)$ and answer "Hamiltonian" exactly when $A(I(G)) \le \rho n$. If $G$ is Hamiltonian, $A(I(G)) \le \alpha(n) \cdot n \le \rho n$, so the answer is yes. If $G$ is not Hamiltonian, $A(I(G)) \ge \mathrm{OPT}(I(G)) > \rho n$, so the answer is no. The procedure runs in polynomial time, so Hamiltonian cycle is in P, and P = NP. $\blacksquare$

The proof shows more than the theorem: the [gap problem](/gap-problem/) that asks whether $\mathrm{OPT} \le n$ or $\mathrm{OPT} > \rho n$ is NP-hard. The gap is a factor of $\rho + 1$ between the two cases.

### Example

The cycle $C_5$ is Hamiltonian. With $\rho = 3$, the non-edges cost $3 \cdot 5 + 1 = 16$, and $\mathrm{OPT} = 5$. The star with center 0 and leaves 1 to 4 is not Hamiltonian. A tour passes the center once, so it uses at most 2 of the 4 star edges, and $\mathrm{OPT} = 2 + 3 \cdot 16 = 50 > 15 = \rho n$. The Petersen graph has 10 vertices, no Hamiltonian cycle, and a Hamiltonian path. With $\rho = 2$, the non-edges cost 21, and $\mathrm{OPT} = 9 + 21 = 30 > 20$.

## Consequences

- **General TSP is not in APX.** Unless P = NP, general TSP is outside the class [APX](/apx-class/) of problems with a constant-ratio approximation. So it has no [PTAS](/ptas/) and is not [APX-complete](/apx-completeness/) in the usual sense.
- **The triangle inequality is the whole difference.** The costs of $I(G)$ break the triangle inequality, since $1 + 1 < \rho n + 1$ as soon as $\rho n > 1$. With the triangle inequality, the [double tree algorithm](/double-tree-algorithm/) has ratio 2 and [Christofides' algorithm](/christofides-algorithm/) has ratio $3/2$. The metric problem is still hard to approximate within $123/122$; see [metric TSP inapproximability](/metric-tsp-inapproximability/).
- **Asymmetric costs.** A symmetric instance is a special case of the [asymmetric TSP](/asymmetric-tsp/), so the theorem holds there too. Asymmetric costs with the triangle inequality have an $O(\log n / \log\log n)$ algorithm and a constant-ratio algorithm; see the asymmetric TSP page.
- **Path versions.** The same reduction from Hamiltonian path rules out every ratio $\alpha(n)$ for the shortest Hamiltonian path with arbitrary costs.
- **Exact solution is not harder with a metric.** Adding a constant to every cost makes any instance metric and keeps the optimal tours, as the [metric TSP](/metric-tsp/) page shows. This map keeps optimality but not ratios, so it does not contradict the theorem.

## Tightness

The theorem cannot be extended to every function of the input. With positive integer costs, $\mathrm{OPT} \ge n$ and every tour costs at most $n \cdot c_{\max}$, where $c_{\max}$ is the largest cost. So any tour is a $c_{\max}$-approximation. The number $c_{\max}$ can be as large as $2^L$ for an input of $L$ binary digits, but it is not a function of $n$ alone, and the proof needs $\rho n + 1$ to fit in the cost field. For each ratio that depends only on $n$ and has polynomially many digits, the theorem applies.

The hypothesis on the costs matters in a second way. If zero costs are allowed, the same reduction with costs 0 on edges and 1 on non-edges gives $\mathrm{OPT} = 0$ exactly when $G$ is Hamiltonian. Then no algorithm with any finite ratio exists unless P = NP, since a ratio guarantee forces $\mathrm{ALG} = 0$ when $\mathrm{OPT} = 0$.

## History

Sahni and Gonzalez (1976) proved the theorem in a paper that also showed similar results for several other problems; they used the name P-complete for what is now called NP-complete. In the same year Christofides gave the $3/2$ algorithm for the metric case. Williamson and Shmoys (Section 2.4) and Vazirani (Chapter 3) give the proof above.

## References
