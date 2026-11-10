---
tag: AY7Y25
kind: concept
slug: apx-class
name: APX (complexity class)
aliases:
- APX class
area: approximation/hardness-of-approximation
level: advanced
summary: APX seen from hardness. The class of NPO problems with a constant-factor approximation, its closure under AP-reductions, its complete problems, and the problems that are provably outside it.
prereqs: [npo-class, approximation-ratio]
see_also: [apx, apx-completeness, ptas, approximation-preserving-reduction, ptas-reduction, l-reduction, approximation-threshold, general-tsp-inapproximability]
sources:
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3, Approximation Classes (APX and the inclusions), and Chapter 8, Approximation Preserving Reductions (AP-reductions, closure and APX-completeness)
  - paper: doi:10.1137/S0097539795286612
    title: Sanjeev Khanna, Rajeev Motwani, Madhu Sudan and Umesh Vazirani, On syntactic versus computational views of approximability, SIAM Journal on Computing 28(1), 1998
    locator: Theorem 1 (the closure of MAX SNP under E-reductions is APX-PB) and Remark 5 (with PTAS-reductions the closure is APX)
  - paper: doi:10.1137/S0097539796304220
    title: Pierluigi Crescenzi, Viggo Kann, Riccardo Silvestri and Luca Trevisan, Structure in approximation classes, SIAM Journal on Computing 28(5), 1999
    locator: Abstract and the sections on AP-reductions (APX-intermediate problems exist if P is not NP)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Techniques in Proving the Hardness of Approximation, Section 16.2 (L-reductions and the class of problems with no PTAS)
---

APX is the class of [NPO](/npo-class/) problems that have a polynomial-time approximation algorithm with a constant ratio. This page looks at APX from the hardness side: which reductions keep a problem inside APX, which problems are hardest in APX, and how one proves that a problem is outside APX. For the definition with algorithmic examples, see the overview page [APX](/apx/).

## In plain words

Some hard optimization problems still let a fast algorithm get within a fixed factor of the best answer, for example "never more than twice the best". These problems form APX. Inside APX, some problems let you get as close as you like, and others stop at a fixed barrier. The hardest problems of APX are the ones that every other problem of APX translates into while the quality of answers is kept. If one hardest problem had arbitrarily good fast approximations, then every problem of APX would have them, and that would make the famous hard problems easy. Outside APX are problems where no fixed factor is possible at all, such as finding the largest clique in a graph.

## The idea

**Definition and notation.** Let $\Pi$ be an NPO problem with optimum $\mathrm{OPT}(x)$, and let an algorithm return a solution with value ALG. For a minimization problem, a $\rho$-approximation has $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$; for maximization, an $\alpha$-approximation has $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. With the performance ratio $R(x, y) = \max(m(x, y)/\mathrm{OPT}(x),\ \mathrm{OPT}(x)/m(x, y)) \ge 1$ of Ausiello et al., both cases read $R \le r$. Then

$$\mathrm{APX} = \{\, \Pi \in \mathrm{NPO} : \text{some polynomial-time algorithm has } R(x, A(x)) \le r \text{ for all } x, \text{ for a constant } r \,\}.$$

**APX-PB** is the part of APX with a measure bounded by a polynomial in $|x|$.

**The chain.** $\mathrm{PO} \subseteq \mathrm{FPTAS} \subseteq \mathrm{PTAS} \subseteq \mathrm{APX} \subseteq \mathrm{NPO}$. If P $\ne$ NP, each inclusion is strict. Two of these strict inclusions are at the APX boundary. (1) MAX 3SAT is in APX, because a random assignment satisfies $7/8$ of the clauses of width 3 in expectation and [conditional expectations](/method-of-conditional-expectations/) make this deterministic. It is not in PTAS unless P = NP, by the [PCP theorem](/pcp-theorem/); see [MAX 3SAT inapproximability](/max-3sat-inapproximability/). (2) General TSP is in NPO but not in APX unless P = NP; see [general TSP inapproximability](/general-tsp-inapproximability/). Maximum clique is another example, by [clique inapproximability](/clique-inapproximability/).

**Closure under AP-reductions.** An [AP-reduction](/approximation-preserving-reduction/) from $A$ to $B$ is a triple $(f, g, \alpha)$: $f(x, r)$ is an instance of $B$, $g(x, y, r)$ is a solution of $x$, both are polynomial-time for each fixed $r > 1$, and $\alpha \ge 1$ is a constant such that

$$R_B(f(x, r), y) \le r \implies R_A(x, g(x, y, r)) \le 1 + \alpha (r - 1).$$

*Claim.* If $A \le_{AP} B$ and $B \in$ APX, then $A \in$ APX. *Proof.* Let $\mathcal{B}$ be an algorithm for $B$ with ratio $r_B$. On input $x$, compute $x' = f(x, r_B)$, then $y = \mathcal{B}(x')$, then $g(x, y, r_B)$. Each step is polynomial, because $r_B$ is a fixed constant. Since $R_B(x', y) \le r_B$, the output has ratio at most $1 + \alpha(r_B - 1)$, a constant. $\blacksquare$ The same argument with $r \to 1$ shows that AP-reductions preserve membership in PTAS: to get ratio $1 + \varepsilon$ for $A$, run the scheme of $B$ with $r = 1 + \varepsilon/\alpha$.

**Which reductions keep APX.** The [L-reduction](/l-reduction/) of Papadimitriou and Yannakakis preserves APX when $A$ is a minimization problem, and it always preserves PTAS. The [PTAS-reduction](/ptas-reduction/) of Crescenzi and Trevisan only promises that $R_B \le c(r)$ implies $R_A \le r$ for some function $c$; if $c$ stays below the ratio $r_B$ of the known algorithm for $B$, the reduction gives no constant ratio for $A$. So PTAS-reductions preserve PTAS but not APX. This is why APX-hardness is usually stated with PTAS-reductions: it is the weakest reduction that still rules out a PTAS.

**APX-completeness.** A problem is APX-hard if each problem of APX reduces to it, and APX-complete if it is also in APX. Khanna, Motwani, Sudan and Vazirani show that the closure of MAX SNP under E-reductions is APX-PB (their Theorem 1), and under PTAS-reductions the closure is all of APX (their Remark 5). So MAX 3SAT is APX-complete. If any APX-hard problem had a PTAS, then MAX 3SAT would have one, and the PCP theorem would give P = NP. See [APX-completeness](/apx-completeness/) for the list of complete problems and the proof sketch.

**Structure inside APX.** Crescenzi, Kann, Silvestri and Trevisan (1999) show that, if P $\ne$ NP, APX contains problems that are neither in PTAS nor APX-complete under AP-reductions. Such problems are called APX-intermediate. Their paper also gives what its abstract calls the first natural APX-intermediate problems.

## Examples

What is proved on this page: the closure of APX and PTAS under AP-reductions. The other facts below are cited and proved on the linked pages.

| Problem | Best known ratio | Hardness | Status |
| --- | --- | --- | --- |
| MAX 3SAT | $7/8$ | no $7/8 + \varepsilon$ unless P = NP | APX-complete |
| [Minimum vertex cover](/vertex-cover/) | $2$ | no $\sqrt{2} - \varepsilon$ unless P = NP | APX-complete |
| [Maximum cut](/maximum-cut/) | $0.878$ | no $16/17 + \varepsilon$ unless P = NP | APX-complete |
| Metric TSP | $3/2$ (slightly below) | no $123/122$ unless P = NP | APX-complete |
| [Bin packing](/bin-packing/) | $3/2$ (absolute) | no $3/2 - \varepsilon$ unless P = NP | in APX, has an [asymptotic PTAS](/asymptotic-ptas/) |
| [Knapsack](/knapsack-fptas/) | $1 - \varepsilon$ for each $\varepsilon$ | none | in FPTAS |
| [Set cover](/set-cover/) | $\ln n$ | no $(1 - \varepsilon)\ln n$ unless P = NP | not in APX |
| [Maximum clique](/maximum-clique/) | $n/\mathrm{polylog}\, n$ | no $n^{1 - \varepsilon}$ unless P = NP | not in APX |
| General TSP | none | no ratio $2^{p(n)}$, $p$ a polynomial | not in APX |

The vertex cover entry uses the theorem of Khot, Minzer and Safra (see [vertex cover inapproximability](/vertex-cover-inapproximability/)). The MAX CUT entry uses Håstad's gadget result, and under the [Unique Games Conjecture](/unique-games-conjecture/) the threshold for MAX CUT is the Goemans and Williamson ratio (see [MAX CUT under UGC](/max-cut-ugc-hardness/)). Bin packing is in APX but not in PTAS, and the reason is a gap of [partition](/partition-problem/) at the value 2; see [bin packing inapproximability](/bin-packing-inapproximability/). Its asymptotic scheme shows that the hard instances of bin packing all have a small optimum.

**A problem outside APX, in one paragraph.** General TSP asks for a shortest tour in a complete graph with arbitrary positive integer weights. Given a graph $G$ on $n$ vertices, give weight 1 to the edges of $G$ and weight $rn$ to the other pairs. If $G$ has a [Hamiltonian cycle](/hamiltonian-cycle/), the optimum is $n$. If not, each tour uses a heavy edge, so the optimum is more than $rn$. An $r$-approximation would tell the two cases apart, so it exists only if P = NP. The weights have $O(\log n + \log r)$ bits, so the argument works for each ratio $r \le 2^{p(n)}$ with $p$ a polynomial.

## Where it is used

- **Ruling out a PTAS.** To show that a problem has no PTAS unless P = NP, one gives an L-reduction or a PTAS-reduction from an APX-hard problem such as MAX 3SAT or [vertex cover](/vertex-cover/) in bounded degree graphs. Williamson and Shmoys, Section 16.2, use this route.
- **Locating a problem in the hierarchy.** Constant-ratio algorithms put a problem in APX; a gap reduction (see [gap problem](/gap-problem/)) at a growing ratio puts it outside. The classes log-APX and poly-APX of Ausiello et al. sit above APX and hold set cover and maximum clique.
- **Sorting problems by threshold.** Inside APX, the [approximation threshold](/approximation-threshold/) of each complete problem is a separate question. APX-completeness says only that the threshold is above 1.
- **Syntactic classes.** MAX SNP of Papadimitriou and Yannakakis is defined by the shape of a logical formula. The theorem of Khanna et al. connects it to the computational class APX, so a syntactic reduction gives a computational result.

## References
