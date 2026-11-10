---
tag: 7DN3DJ
kind: theorem
slug: max-coverage-inapproximability
name: Maximum coverage inapproximability
aliases:
- Feige max coverage hardness
- 1 - 1/e hardness of maximum coverage
area: approximation/hardness-of-approximation
level: advanced
summary: For each ε > 0, covering a 1 - 1/e + ε fraction of the optimum for maximum coverage is NP-hard (Feige 1998), so greedy is optimal. Proved here from the ln n hardness of set cover.
prereqs: [max-coverage, greedy-max-coverage, set-cover-inapproximability, approximation-ratio]
see_also: [set-cover-inapproximability, nemhauser-wolsey-fisher-theorem, submodular-function, k-median-inapproximability, dominating-set-inapproximability, label-cover, approximation-threshold]
sources:
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: Section 5 (maximum k-coverage, the bound 1 - 1/e + ε)
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the set cover corollary, (1 - α) ln n is NP-hard for every α > 0
  - paper: "G. L. Nemhauser and L. A. Wolsey, Best algorithms for approximating the maximum of a submodular set function, Mathematics of Operations Research 3(3), 1978"
    locator: the bound 1 - 1/e for algorithms that query a value oracle a polynomial number of times
  - paper: "G. L. Nemhauser, L. A. Wolsey and M. L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14, 1978"
    locator: the greedy bound 1 - (1 - 1/k)^k
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 3, Section 3.9 (maximum coverage and the greedy bound)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.5 (the greedy algorithm for maximum coverage)
---

The maximum coverage problem picks $k$ sets from a family to cover as many elements as possible. The [greedy algorithm](/greedy-max-coverage/) covers at least $1 - (1 - 1/k)^k > 1 - 1/e \approx 0.632$ times the optimum. Feige (1998) proved that for each $\varepsilon > 0$, a ratio of $1 - 1/e + \varepsilon$ is NP-hard, so greedy is the best polynomial algorithm up to $\varepsilon$. This page proves the bound from the $\ln n$ hardness of [set cover](/set-cover-inapproximability/): a better algorithm for maximum coverage, used in rounds, would give a cover with fewer than $(1 - \delta) \ln n$ times the optimal number of sets.

## Statement

An instance of [maximum coverage](/max-coverage/) has a universe of $n$ elements, a family of $M$ sets and a budget $k$. $\mathrm{OPT}$ is the largest number of elements covered by $k$ sets. For this maximization problem, a ratio $\alpha \le 1$ means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ on every instance.

**Theorem.** For each $\varepsilon > 0$, if a polynomial algorithm has ratio $1 - \frac1e + \varepsilon$ for maximum coverage, then P = NP.

Feige proved the theorem directly, and his proof gives a gap form: it is NP-hard to tell instances where $k$ disjoint sets cover all elements from instances where every $k$ sets cover at most a $1 - \frac1e + \varepsilon$ fraction. The proof below gives only the ratio form, from the set cover theorem.

## In plain words

Suppose you could always pick a few groups that cover a little more than 63 percent of what the best choice of the same number of groups covers. Then you could cover everything fast. Pick groups, take away what they cover, and pick again for the items that are left. If the best cover uses $k$ groups, the same $k$ groups also cover all items that are left, so each round covers more than 63 percent of the rest.

Each round leaves less than 37 percent. After a number of rounds that is a little less than the natural logarithm of the number of items, nothing is left. This gives a cover that is a little better than the logarithm bound. Covering everything that well is known to be hard. So the 63 percent rule cannot be improved.

## Proof

Let $\alpha = 1 - \frac1e + \varepsilon$ with $0 < \varepsilon < \frac1e$, and suppose an algorithm $A$ has ratio $\alpha$ for maximum coverage in polynomial time. We build a set cover algorithm.

*Rounds.* Take a set cover instance with universe $U$ of $n$ elements and sets $S_1, \ldots, S_M$, and let $k$ be a guess for its optimum $\mathrm{OPT}_{\mathrm{SC}}$. Set $R_0 = U$. In round $i$, run $A$ with budget $k$ on the sets restricted to $R_{i-1}$, add the $k$ sets it returns to the cover, and let $R_i$ be the elements of $R_{i-1}$ that they do not cover.

*Progress.* If $k \ge \mathrm{OPT}_{\mathrm{SC}}$, an optimal cover uses at most $k$ sets and covers all of $R_{i-1}$, so the maximum coverage optimum on $R_{i-1}$ is $|R_{i-1}|$. Then $A$ covers at least $\alpha |R_{i-1}|$ elements, and $|R_i| \le (1 - \alpha) |R_{i-1}|$. So $|R_t| \le (1 - \alpha)^t n$, and $R_t = \emptyset$ as soon as $(1 - \alpha)^t n < 1$, which holds for

$$t = \left\lfloor \frac{\ln n}{\ln (1/(1 - \alpha))} \right\rfloor + 1.$$

The cover has at most $k t$ sets. Run this for each $k = 1, 2, \ldots, M$, stop each run after $t$ rounds, and return the smallest cover found. The run with $k = \mathrm{OPT}_{\mathrm{SC}}$ succeeds, so the result has at most $\mathrm{OPT}_{\mathrm{SC}} \cdot t$ sets, after $O(M t)$ calls to $A$.

*The ratio.* Write $\lambda = \ln \frac{1}{1 - \alpha}$. Since $1 - \alpha = \frac1e - \varepsilon = \frac1e (1 - e \varepsilon)$, we have $\lambda = 1 - \ln(1 - e \varepsilon) > 1 + e \varepsilon$. So

$$t \le \frac{\ln n}{\lambda} + 1 < \frac{\ln n}{1 + e \varepsilon} + 1.$$

Let $\delta = \frac{e \varepsilon}{2(1 + e \varepsilon)}$, so that $\frac{1}{1 + e \varepsilon} = 1 - 2\delta$. If $\ln n \ge 1/\delta$, then $t < (1 - 2\delta) \ln n + \delta \ln n = (1 - \delta) \ln n$. Instances with $\ln n < 1/\delta$ have fewer than $n_0 = e^{1/\delta}$ elements, a constant. Their optimum is at most $n_0$, so trying all families of at most $n_0$ sets solves them exactly in time $O(M^{n_0})$, which is polynomial.

So set cover has a polynomial algorithm with ratio $(1 - \delta) \ln n$. By the theorem of Dinur and Steurer (see [set cover inapproximability](/set-cover-inapproximability/)), P = NP. $\blacksquare$

*Remark.* The same argument with Feige's set cover theorem gives the conclusion NP $\subseteq$ DTIME$(n^{O(\log \log n)})$. Feige's own proof for maximum coverage needs only P $\ne$ NP, because he reduces from a gap version of [label cover](/label-cover/) with constant soundness and a partition system of constant size. The step from the ratio form to the gap form, with disjoint sets in the yes case, is cited and not proved here.

### Example

Take $n = 10^6$, so $\ln n \approx 13.82$. With $\varepsilon = 0.05$, $\alpha \approx 0.682$ and $\lambda = 1 - \ln(1 - 0.05 e) \approx 1.146$, so $t = \lfloor 13.82 / 1.146 \rfloor + 1 = 13$ rounds suffice, and the cover has at most $13 \cdot \mathrm{OPT}_{\mathrm{SC}}$ sets. With $\alpha = 1 - \frac1e$ exactly, $\lambda = 1$ and $t = 14$, which is the greedy set cover bound $\ln n + 1$ again. So each constant gained over $1 - \frac1e$ becomes a constant factor gained over $\ln n$. The code for this page checks the round argument by brute force on small instances, with greedy as the algorithm $A$ and $\alpha = 1 - (1 - 1/k)^k$.

## Consequences

- **Greedy is optimal.** Greedy reaches $1 - (1 - 1/k)^k$, which is more than $1 - \frac1e$ for each $k$ and tends to it. The theorem shows that no polynomial algorithm reaches $1 - \frac1e + \varepsilon$ on all instances, unless P = NP.
- **Monotone submodular maximization.** Coverage is a [submodular function](/submodular-function/), so the bound applies to maximizing monotone submodular functions under a cardinality constraint, where the [Nemhauser, Wolsey and Fisher](/nemhauser-wolsey-fisher-theorem/) bound is $1 - \frac1e$. For functions given by a value oracle, Nemhauser and Wolsey (1978) showed that $1 - \frac1e + \varepsilon$ needs exponentially many queries, with no complexity assumption. The theorem here is the matching statement for functions given explicitly.
- **Related problems.** The gap form, with disjoint sets in the yes case, is the starting point for the $1 + \frac{2}{e}$ bound for [$k$-median](/k-median-inapproximability/), the $1.463$ bound for metric facility location, and bounds for welfare maximization with coverage valuations.
- **Budgeted and matroid versions.** These contain maximum coverage, so the bound $1 - \frac1e$ holds for them too, and it is reached for both (see [max coverage](/max-coverage/)).

## Tightness

The constant $1 - \frac1e$ is tight: greedy reaches it, and the theorem rules out every larger constant. For a fixed budget $k$ the problem is solved exactly in time $O(M^k n)$ by trying all choices, so the hard instances have $k$ growing with $n$. The greedy bound $1 - (1 - 1/k)^k$ is tight for greedy itself for each $k$.

## History

Hochbaum and Pathria (1998) and the survey of Hochbaum (1997, Chapter 3) analysed greedy for maximum coverage, following Nemhauser, Wolsey and Fisher (1978) for submodular functions. Feige (1998) proved the bound $1 - \frac1e + \varepsilon$ in the same paper as the $\ln n$ threshold for set cover. Unlike the set cover threshold, which needed a quasi-polynomial assumption until Dinur and Steurer (2014), the maximum coverage bound was proved under P $\ne$ NP from the start.

## References
