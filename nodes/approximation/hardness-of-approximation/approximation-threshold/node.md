---
tag: XW4ZHJ
kind: concept
slug: approximation-threshold
name: Approximation threshold
aliases:
- inapproximability ratio
- hardness threshold
area: approximation/hardness-of-approximation
level: advanced
summary: The best ratio that a polynomial-time algorithm can guarantee for a problem unless P = NP, or under another stated assumption. A table of known thresholds and their assumptions.
prereqs: [approximation-ratio, gap-problem]
see_also: [apx-class, apx-completeness, gap-preserving-reduction, max-3sat-inapproximability, vertex-cover-inapproximability, set-cover-inapproximability, unique-games-conjecture, k-center-inapproximability]
sources:
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 13, Approximability (the approximation threshold as the infimum of the relative errors that polynomial-time algorithms achieve)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Techniques in Proving the Hardness of Approximation (Theorem 16.22 for MAX E3SAT and the label cover and unique games sections)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: The results for MAX E3SAT, MAX E3LIN2 and the gadget bound for MAX CUT
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: The ln n bound for set cover and the 1 - 1/e bound for maximum coverage
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: The corollary that set cover has no (1 - ε) ln n approximation unless P = NP
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of max clique and chromatic number, Theory of Computing 3, 2007
    locator: The n to the power 1 - ε bounds for clique and chromatic number unless P = NP
---

The **approximation threshold** of an optimization problem is the best ratio that a polynomial-time algorithm can guarantee for it, under a stated assumption such as P $\ne$ NP. An upper bound on the threshold is an algorithm; a lower bound is a hardness result, usually an NP-hard [gap problem](/gap-problem/). The threshold is *known* when the two bounds meet, as for MAX E3SAT at $7/8$ and set cover at $\ln n$. For many problems, such as vertex cover and metric TSP, a gap remains or the matching lower bound needs a conjecture.

## In plain words

For a hard optimization problem, ask how close to the best answer a fast algorithm can promise to get. One side of the answer is an algorithm with a proven guarantee. The other side is a proof that a better guarantee would make an NP-complete problem easy. If the two sides agree, that number is the threshold of the problem: the exact limit of fast approximation, as long as the famous hard problems stay hard. Some thresholds are fixed numbers, some grow with the size of the input, and some are only known between two values. A few are known to match only if an unproved conjecture holds, so each threshold must be read together with the assumption that it uses.

## The idea

**Notation and conventions.** For a minimization problem a $\rho$-approximation returns $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$; for a maximization problem an $\alpha$-approximation returns $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. Ratios may depend on the input size $n$. With an assumption $H$ (for example P $\ne$ NP), the threshold is

$$\rho^*_H = \inf\{\rho : \text{a polynomial-time } \rho\text{-approximation exists, assuming } H\}$$

for minimization, and $\alpha^*_H = \sup\{\alpha : \ldots\}$ for maximization. Papadimitriou (Chapter 13) defines the threshold through the relative error $|\mathrm{ALG} - \mathrm{OPT}|/\max(\mathrm{ALG}, \mathrm{OPT})$; in that scale a threshold of 0 means arbitrarily good approximation and a threshold of 1 means no constant ratio. With $R = \max(\mathrm{ALG}/\mathrm{OPT},\ \mathrm{OPT}/\mathrm{ALG})$ the two scales are linked by error $= 1 - 1/R$.

**From a gap to a lower bound (proved here).** Let $\Pi$ be a maximization problem and suppose the gap problem gap-$\Pi[c, s]$ is NP-hard: given $x$ with the promise that $\mathrm{OPT}(x) \ge c(x)$ or $\mathrm{OPT}(x) < s(x)$, decide which. Let $\mathcal{A}$ be an $\alpha$-approximation with $\alpha > s/c$. On a yes instance, $\mathrm{ALG} \ge \alpha c > s$. On a no instance, $\mathrm{ALG} \le \mathrm{OPT} < s$. So the test "$\mathrm{ALG} \ge s$?" decides the gap problem in polynomial time, and P = NP. Hence $\alpha^* \le s/c$ if P $\ne$ NP. For a minimization problem with gap $[c, s]$, where yes means $\mathrm{OPT} \le c$ and no means $\mathrm{OPT} > s$, the same argument gives $\rho^* \ge s/c$. [Gap-preserving reductions](/gap-preserving-reduction/) carry such gaps from one problem to another.

**When the bound is not attained.** The infimum or supremum need not be attained. For MAX E3SAT the threshold $7/8$ is attained by a random assignment, and each $7/8 + \varepsilon$ is NP-hard. For set cover the algorithm gives $H_n \le \ln n + 1$ and the hardness is $(1 - \varepsilon)\ln n$, so the threshold is $\ln n$ up to lower order terms.

**A complete small case: $k$-center.** The threshold of the [$k$-center problem](/k-center-problem/) in metric spaces is exactly 2, assuming P $\ne$ NP. The [Gonzalez algorithm](/gonzalez-k-center/) gives 2. For the lower bound, take a graph $G$ and $k$, and define the metric $d(u, v) = 1$ for edges and $d(u, v) = 2$ for other pairs of distinct vertices; the triangle inequality holds because each distance is 1 or 2. If $G$ has a [dominating set](/dominating-set/) of size $k$, those centers give radius 1. If not, some vertex is at distance 2 from each set of $k$ centers, so the radius is 2. A ratio $\rho < 2$ returns radius 1 on yes instances, so it decides dominating set, which is NP-complete. See [k-center inapproximability](/k-center-inapproximability/).

## Examples

The ratio column uses the convention above. "Proved" means the bound is proved on the linked page; the others are cited there.

| Problem | Goal | Best algorithm | Hardness | Assumption |
| --- | --- | --- | --- | --- |
| MAX E3SAT | max | $7/8$ ([random assignment](/random-assignment-max-3-sat/)) | $7/8 + \varepsilon$ ([Håstad](/max-3sat-inapproximability/)) | P $\ne$ NP |
| MAX E3LIN2 | max | $1/2$ (random assignment) | $1/2 + \varepsilon$ (Håstad) | P $\ne$ NP |
| [Set cover](/set-cover/) | min | $\ln n + 1$ ([greedy](/greedy-set-cover/)) | $(1 - \varepsilon)\ln n$ (Dinur and Steurer 2014) | P $\ne$ NP |
| [Max coverage](/max-coverage/) | max | $1 - 1/e$ ([greedy](/greedy-max-coverage/)) | $1 - 1/e + \varepsilon$ (Feige 1998) | P $\ne$ NP |
| [Vertex cover](/vertex-cover/) | min | $2$ | $\sqrt{2} - \varepsilon$ (Khot, Minzer and Safra) | P $\ne$ NP |
| Vertex cover | min | $2$ | $2 - \varepsilon$ (Khot and Regev 2008) | UGC |
| [MAX CUT](/maximum-cut/) | max | $0.878$ (Goemans and Williamson) | $16/17 + \varepsilon$ (Håstad; Trevisan, Sorkin, Sudan and Williamson) | P $\ne$ NP |
| MAX CUT | max | $0.878$ | $0.878 + \varepsilon$ ([Khot, Kindler, Mossel and O'Donnell 2007](/max-cut-ugc-hardness/)) | UGC |
| [Maximum clique](/maximum-clique/) | max | $\mathrm{polylog}\,n / n$ | $n^{-(1 - \varepsilon)}$ ([Zuckerman 2007](/clique-inapproximability/)) | P $\ne$ NP |
| [Chromatic number](/chromatic-number/) | min | $n / \mathrm{polylog}\,n$ | $n^{1 - \varepsilon}$ ([Zuckerman 2007](/graph-coloring-inapproximability/)) | P $\ne$ NP |
| [$k$-center](/k-center-problem/) | min | $2$ | $2 - \varepsilon$ (proved above) | P $\ne$ NP |
| [Metric TSP](/metric-tsp/) | min | $3/2 - 10^{-36}$ ([Karlin, Klein and Oveis Gharan](/karlin-klein-oveis-gharan-algorithm/)) | $123/122$ (Karpinski, Lampis and Schmied) | P $\ne$ NP |
| [Bin packing](/bin-packing/), absolute ratio | min | $3/2$ | $3/2 - \varepsilon$ (from [partition](/partition-problem/)) | P $\ne$ NP |
| [Unrelated machines](/unrelated-machine-scheduling/) makespan | min | $2$ ([Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/)) | $3/2 - \varepsilon$ (same paper) | P $\ne$ NP |
| [Knapsack](/knapsack-fptas/) | max | $1 - \varepsilon$ for each $\varepsilon$ (FPTAS) | none, threshold 1 | none |

**Reading the table.** Thresholds known exactly under P $\ne$ NP: MAX E3SAT, MAX E3LIN2, set cover, max coverage, $k$-center, bin packing (absolute), and knapsack. Thresholds known only under the [Unique Games Conjecture](/unique-games-conjecture/): vertex cover and MAX CUT. Open even under UGC: metric TSP and unrelated machines. For clique and chromatic number the threshold is $n^{1 - o(1)}$; the exact lower order term is open.

## Where it is used

- **Stopping rules for algorithm design.** When the threshold is known, an algorithm that reaches it is optimal, and research moves to running time or special cases.
- **Choosing the assumption.** A threshold is only meaningful with its assumption. Some results need NP $\ne$ ZPP or NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$ in their first proofs, and later work removed them; for example Feige's $\ln n$ for set cover first used the second assumption.
- **Gap reductions.** The usual route to a lower bound is: an NP-hard gap from the [PCP theorem](/pcp-theorem/) or from [label cover](/label-cover/), then a chain of [gap-preserving reductions](/gap-preserving-reduction/).
- **Classification.** The threshold decides the class of the problem: threshold 1 with an efficient scheme means PTAS, a constant above 1 means [APX-hard](/apx-completeness/) inside [APX](/apx-class/), and a growing threshold means the problem is outside APX.

## References
