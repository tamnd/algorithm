---
tag: N5YDRP
kind: concept
slug: apx-completeness
name: APX-completeness
aliases:
- APX-complete
- APX-hard
area: approximation/hardness-of-approximation
level: advanced
summary: A problem is APX-hard if every APX problem PTAS-reduces to it. MAX 3SAT, MAX CUT and vertex cover are APX-complete, so none of them has a PTAS unless P = NP.
prereqs: [apx-class, ptas-reduction, pcp-theorem]
see_also: [l-reduction, max-3sat-inapproximability, vertex-cover-inapproximability, npo-class, ptas, approximation-threshold, metric-tsp-inapproximability, steiner-tree-problem]
sources:
  - paper: doi:10.1137/S0097539795286612
    title: Sanjeev Khanna, Rajeev Motwani, Madhu Sudan and Umesh Vazirani, On syntactic versus computational views of approximability, SIAM Journal on Computing 28(1), 1998
    locator: Theorem 1 (closure of MAX SNP under E-reductions is APX-PB), the MAX SNP-completeness of MAX k-SAT under E-reductions, and Remark 5 (closure under PTAS-reductions is APX)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: pp. 425 to 440 (L-reductions, MAX SNP, and the MAX SNP-completeness of MAX 3SAT, MAX 2SAT, MAX CUT, and independent set and vertex cover of bounded degree)
  - paper: doi:10.1145/278298.278306
    title: Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 1998
    locator: The PCP theorem and its consequence that no MAX SNP-hard problem has a PTAS unless P = NP
  - paper: doi:10.1137/S0097539796304220
    title: Pierluigi Crescenzi, Viggo Kann, Riccardo Silvestri and Luca Trevisan, Structure in approximation classes, SIAM Journal on Computing 28(5), 1999
    locator: AP-reductions and APX-completeness under them; APX-intermediate problems
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 8, Approximation Preserving Reductions (APX-completeness of MAX 3SAT and its consequences)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Section 16.2, Reductions that preserve approximation (L-reductions from MAX E3SAT to independent set and vertex cover of bounded degree)
---

A problem is **APX-hard** when every problem of [APX](/apx-class/) reduces to it by a [PTAS-reduction](/ptas-reduction/), and **APX-complete** when it is also in APX. Khanna, Motwani, Sudan and Vazirani (1998) proved that MAX 3SAT is APX-complete, and earlier [L-reductions](/l-reduction/) of Papadimitriou and Yannakakis (1991) carry this to MAX CUT, vertex cover and many other problems. Since the [PCP theorem](/pcp-theorem/) shows that MAX 3SAT has no PTAS unless P = NP, no APX-hard problem has a PTAS unless P = NP. APX-completeness is to approximation schemes what NP-completeness is to exact algorithms.

## In plain words

Many hard optimization problems have fast algorithms that get within a fixed factor of the best answer. A natural question is whether the factor can be pushed as close to perfect as one likes. APX-complete problems are the ones for which this question has the same answer for all of them at once. Each problem with a fixed-factor algorithm can be translated into any APX-complete problem, and near-perfect answers translate back into near-perfect answers. So a scheme that gets arbitrarily close for one APX-complete problem gives such a scheme for all of them, including satisfiability with three literals per clause. The PCP theorem shows that this is impossible unless the famous hard problems are easy. To show that a new problem has no such scheme, it is enough to translate one APX-complete problem into it.

## The idea

**Notation.** Problems are in [NPO](/npo-class/). For an instance $x$ and a solution $y$, $R(x, y) = \max(m(x, y)/\mathrm{OPT}(x),\ \mathrm{OPT}(x)/m(x, y)) \ge 1$ is the performance ratio of Ausiello et al. On this site a minimization ratio is $\rho \ge 1$ with $\mathrm{ALG} \le \rho\,\mathrm{OPT}$, and a maximization ratio is $\alpha \le 1$ with $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$, so $R = \rho$ for min and $R = 1/\alpha$ for max. A PTAS is a family of polynomial-time algorithms, one for each $r > 1$, with $R \le r$.

**The reduction.** A PTAS-reduction from $A$ to $B$ is a triple $(f, g, c)$ with $c : (1, \infty) \to (1, \infty)$ such that, for each $r > 1$, $f(x, r)$ and $g(x, y, r)$ are computable in polynomial time and

$$R_B(f(x, r), y) \le c(r) \implies R_A(x, g(x, y, r)) \le r.$$

**Definitions.** $B$ is APX-hard if $A \le_{PTAS} B$ for each $A \in$ APX. $B$ is APX-complete if it is APX-hard and $B \in$ APX. Some authors use AP-reductions instead (Crescenzi et al. 1999); an AP-reduction is a PTAS-reduction with $c(r) = 1 + (r - 1)/\alpha$, so APX-hardness under AP-reductions implies APX-hardness under PTAS-reductions.

**Proposition (proved here).** If $B$ is APX-hard and $B$ has a PTAS, then P = NP.

*Proof.* MAX 3SAT is in APX, so $\mathrm{MAX\ 3SAT} \le_{PTAS} B$ by a triple $(f, g, c)$. Fix $r > 1$. Run the scheme of $B$ with ratio $c(r)$ on $f(x, r)$, which takes polynomial time for this fixed $r$, and map the answer back with $g$. The result is a solution of $x$ with $R \le r$. So MAX 3SAT has a PTAS. The [MAX 3SAT inapproximability](/max-3sat-inapproximability/) theorem, which follows from the PCP theorem, gives a constant $\varepsilon_0 > 0$ such that a $(1 - \varepsilon_0)$-approximation for MAX 3SAT decides SAT. Take $r < 1/(1 - \varepsilon_0)$; then SAT is in P, so P = NP. $\blacksquare$

**Theorem (Khanna, Motwani, Sudan and Vazirani 1998; cited).** MAX 3SAT is APX-complete under PTAS-reductions.

*Proof sketch (sketch only; the full proof is in the paper and in Ausiello et al., Chapter 8).* Membership: a random assignment satisfies at least half of all clauses, and $7/8$ of the clauses of width exactly 3, in expectation. For hardness, first reduce each minimization problem of APX to a maximization problem of APX; this step is in the cited sources. Let $A$ be a maximization problem with an algorithm $M$ of ratio $r_0$. On input $x$, let $t = m(x, M(x))$, so $t \le \mathrm{OPT}(x) \le r_0 t$. Cut $[t, r_0 t]$ at the points $t(1 + \eta)^i$ for $i = 0, \ldots, k - 1$, with $k = \lceil \log_{1+\eta} r_0 \rceil$, a constant for fixed $\eta$. Each question "is $\mathrm{OPT}(x) \ge t(1+\eta)^i$?" is in NP. The PCP theorem and the map of [MAX 3SAT inapproximability](/max-3sat-inapproximability/) turn it into a 3CNF formula $\varphi_i$ with a constant gap: satisfiable if the answer is yes, and at most a $1 - \delta$ fraction satisfiable if it is no. Make all $\varphi_i$ the same size and put them on disjoint variables; $f(x, r)$ is their conjunction $\psi$. An assignment of $\psi$ with ratio close enough to 1, where "close enough" depends on $k$, $\delta$ and $r$, must satisfy more than a $1 - \delta$ fraction of $\varphi_i$ for each yes index $i$. The proof then decodes, from such an assignment, a solution of $x$ of value at least $t(1 + \eta)^{i^* - 1}$, where $i^*$ is the largest yes index; this decoding step uses a property of the PCP construction that this sketch does not prove. With $(1 + \eta)^2 \le r$, the ratio of the decoded solution is at most $r$.

**Spreading hardness.** Once one problem is APX-complete, others follow by reductions. An L-reduction with constants $(\alpha, \beta)$ is a PTAS-reduction with $c(r) = 1 + (1 - 1/r)/(\alpha\beta)$ (see [L-reduction](/l-reduction/)), and reductions compose. So to prove that $B$ is APX-hard, it is enough to L-reduce MAX 3SAT, or any problem already known to be APX-hard, to $B$.

## Examples

APX-complete problems. The reductions are cited unless the text says otherwise.

| Problem | Ratio in APX | Hardness proof |
| --- | --- | --- |
| [MAX 3SAT](/max-sat/), MAX E3SAT | $7/8$ for E3SAT | Khanna et al. 1998 |
| [MAX 2SAT](/max-2-sat/) | constant | L-reduction from MAX 3SAT (Papadimitriou and Yannakakis 1991) |
| [MAX CUT](/maximum-cut/) | $0.878$ | L-reduction from MAX 2SAT or NAE-3SAT (Papadimitriou and Yannakakis 1991) |
| Maximum [independent set](/maximum-independent-set/) in graphs of degree at most $B$ | $1/(B+1)$ by [greedy](/greedy-independent-set/) | L-reduction from MAX 3SAT (Papadimitriou and Yannakakis 1991; Williamson and Shmoys, Section 16.2) |
| [Vertex cover](/vertex-cover/) of degree at most $B$, and in general | $2$ | L-reduction from bounded degree independent set |
| TSP with weights 1 and 2, and [metric TSP](/metric-tsp/) | $3/2$ or better | Papadimitriou and Yannakakis 1993; see [metric TSP inapproximability](/metric-tsp-inapproximability/) |
| [Steiner tree](/steiner-tree-problem/) | constant | Bern and Plassmann 1989 |

**Vertex cover, in a few lines.** In a graph $G$ on $n$ vertices of maximum degree $B$, the complement of a vertex cover is an independent set and $\tau(G) + \alpha(G) = n$. The greedy algorithm gives $\alpha(G) \ge n/(B+1)$. The map "same graph, complement the solution" from independent set to vertex cover has $\tau(G) = n - \alpha(G) \le B\,\alpha(G)$, so (L1) holds with $\alpha_L = B$, and the error is the same on both sides, so (L2) holds with $\beta_L = 1$. Bounded degree vertex cover is APX-hard, and so is general vertex cover, which contains it. The 2-approximation by [maximal matching](/vertex-cover-2-approximation/) puts both in APX. The constants are checked by brute force in the code of [L-reduction](/l-reduction/).

**Not APX-complete, or not known to be.** [Knapsack](/knapsack-fptas/) is in FPTAS, so it is not APX-hard unless P = NP. [Bin packing](/bin-packing/) is in APX and has no PTAS unless P = NP, but its [asymptotic PTAS](/asymptotic-ptas/) shows that its hardness comes only from instances with a small optimum. [Set cover](/set-cover/) and [maximum clique](/maximum-clique/) are APX-hard but not in APX unless P = NP (see [set cover inapproximability](/set-cover-inapproximability/) and [clique inapproximability](/clique-inapproximability/)). Crescenzi et al. (1999) show that, if P $\ne$ NP, some problems of APX are neither in PTAS nor APX-complete under AP-reductions.

## Where it is used

- **No PTAS results.** A single L-reduction from an APX-hard problem shows that a new problem has no PTAS unless P = NP. Williamson and Shmoys, Section 16.2, do this for independent set and vertex cover of bounded degree.
- **A starting point for constants.** APX-hardness gives only "some constant". Specific constants come from [gap-preserving reductions](/gap-preserving-reduction/) out of strong PCPs such as [Håstad's 3-bit PCP](/hastad-3bit-pcp/); see [approximation threshold](/approximation-threshold/).
- **Class structure.** The completeness of MAX 3SAT under E-reductions for MAX SNP, and the closure results of Khanna et al., connect the syntactic class MAX SNP with the computational class APX.
- **Guidance for algorithm design.** For an APX-complete problem, the useful work is to improve the constant, not to look for a PTAS. Special inputs can escape: planar graphs and dense graphs often admit a PTAS (for example [dense MAX CUT](/dense-max-cut-ptas/)).

## References
