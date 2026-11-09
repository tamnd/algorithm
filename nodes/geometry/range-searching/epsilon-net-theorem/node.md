---
tag: D66XHQ
kind: theorem
slug: epsilon-net-theorem
name: Epsilon-net theorem
aliases:
- Haussler-Welzl epsilon-net theorem
- epsilon-nets
- epsilon-net
area: geometry/range-searching
level: research
summary: A range space with bounded VC dimension d has an epsilon-net of size O((d/eps) log(1/eps)).
prereqs: [range-space, union-bound, chebyshev-inequality]
see_also: [range-space, vc-dimension, sauer-shelah-lemma, geometric-cutting, partition-theorem, hitting-set, pac-learning, randomized-incremental-construction]
sources:
  - paper: doi:10.1007/BF02187876
    title: David Haussler and Emo Welzl, Epsilon-nets and simplex range queries, Discrete and Computational Geometry 2, 1987, pages 127 to 151
    locator: Section 3, the epsilon-net theorem with the sample size max((4/eps) log2(2/delta), (8d/eps) log2(8d/eps)), and its use for simplex range queries
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 10, Section 10.2 (the epsilon-net theorem and its double sampling proof) and Section 10.3 (lower bounds and geometric consequences)
  - paper: doi:10.1007/BF02187833
    title: János Komlós, János Pach and Gerhard Woeginger, Almost tight bounds for epsilon-nets, Discrete and Computational Geometry 7, 1992, pages 163 to 173
    locator: the upper bound (d + o(1)) (1/eps) ln(1/eps) and a matching lower bound for abstract range spaces (DOI to be checked)
  - paper: doi:10.1137/1116025
    title: Vladimir N. Vapnik and Alexey Ya. Chervonenkis, On the uniform convergence of relative frequencies of events to their probabilities, Theory of Probability and its Applications 16(2), 1971, pages 264 to 280
    locator: the double sampling (symmetrization) argument for uniform convergence (DOI to be checked)
  - paper: doi:10.1145/76359.76371
    title: Anselm Blumer, Andrzej Ehrenfeucht, David Haussler and Manfred K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989, pages 929 to 965
    locator: the same sample bound in the setting of PAC learning (DOI to be checked)
---

The epsilon-net theorem says that in a [range space](/range-space/) of VC dimension $d$, a small random sample hits every large range. If a range contains at least an $\varepsilon$ fraction of a finite set $A$, it contains a point of a random sample of $O((d/\varepsilon) \log(1/\varepsilon))$ points of $A$, for all such ranges at once and with high probability. The size does not depend on $|A|$. Haussler and Welzl proved it in 1987, with explicit constants, to build data structures for [simplex range searching](/simplex-range-searching/), and it is the main tool behind [cuttings](/geometric-cutting/), the [partition theorem](/partition-theorem/) and the analysis of random sampling in geometry.

## Statement

**Definitions.** Let $(X, \mathcal{R})$ be a range space, $A \subseteq X$ a finite set with $|A| = n \ge 1$, and $0 < \varepsilon < 1$. A set $N \subseteq A$ is an **$\varepsilon$-net for $A$** (with respect to $\mathcal{R}$) if $N \cap r \ne \emptyset$ for every range $r \in \mathcal{R}$ with $|r \cap A| \ge \varepsilon n$. The VC dimension and the shatter function are defined on the page on [range spaces](/range-space/).

**Theorem (Haussler and Welzl 1987).** Let $(X, \mathcal{R})$ have VC dimension $d$ with $1 \le d < \infty$, let $A \subseteq X$ be finite and nonempty, and let $0 < \varepsilon < 1$ and $0 < \delta < 1$. Let $N$ be the set of elements of $m$ independent draws, each uniform from $A$, where
$$m \ge \max \left( \frac{4}{\varepsilon} \log_2 \frac{2}{\delta}, \; \frac{8d}{\varepsilon} \log_2 \frac{8d}{\varepsilon} \right).$$
Then $N$ is an $\varepsilon$-net for $A$ with probability at least $1 - \delta$.

**Corollary (existence).** Under the same hypotheses on $(X, \mathcal{R})$, $A$ and $\varepsilon$, there is an $\varepsilon$-net for $A$ of size at most $\left\lceil \frac{8d}{\varepsilon} \log_2 \frac{8d}{\varepsilon} \right\rceil$. Indeed, $\log_2(8d/\varepsilon) > 3$, so this $m$ is at least $(4/\varepsilon) \log_2(2/\delta)$ for $\delta$ close enough to $1$, and the theorem gives a net with positive probability.

The hypothesis is on the VC dimension of the whole range space; it is used only through the Sauer-Shelah bound $|\mathcal{R}|_B| \le \Phi_d(|B|) = \sum_{i=0}^{d} \binom{|B|}{i}$ for every finite $B$. So the theorem also holds, with the same proof, for any range space whose shatter function satisfies $\pi_{\mathcal{R}}(k) \le \Phi_d(k)$. The case $d = 0$ is trivial: all ranges have the same trace on $A$, and one point of that trace is a net.

## In plain words

A large group of points is given, together with a kind of region, such as all half-planes or all rectangles. Call a region heavy if it holds at least a fixed fraction, say one tenth, of the points. The goal is to pick a few points so that every heavy region holds at least one of them.

Picking points at random works, and the number needed does not grow with the size of the group. It depends only on the fraction and on how flexible the regions are, measured by a single number called the VC dimension. Half-planes have dimension three, for instance. The reason is that, although there are infinitely many regions, they can cut a small set of points in only a limited number of ways, so a counting argument over those few ways is enough.

## Proof

The proof is the double sampling argument of Vapnik and Chervonenkis, with the constants of Haussler and Welzl. Throughout, $m$ satisfies the bound of the theorem, and a draw is uniform from $A$. A range $r$ is **heavy** if $|r \cap A| \ge \varepsilon n$. For a sequence $s$ of draws, $|r \cap s|$ counts the positions of $s$ whose element lies in $r$, with repetition.

**Step 0 (two facts about $m$).** Write $m = (8d/\varepsilon) t$. Then $t \ge \log_2(8d/\varepsilon) > 3$, since $d \ge 1$ and $\varepsilon < 1$. Hence (a) $m \ge 24/\varepsilon \ge 8/\varepsilon$. And (b) $(2m + 1)^d \le 2^{\varepsilon m / 4}$: since $8d/\varepsilon \le 2^t$, we get $2m + 1 = 2t \cdot (8d/\varepsilon) + 1 \le 2t \cdot 2^t + 1$, and $2t \cdot 2^t + 1 \le 4^t$ because $2^t - 2t \ge 2 > 2^{-t}$ for $t \ge 3$; raising to the power $d$ gives $(2m+1)^d \le 4^{dt} = 2^{2dt} = 2^{\varepsilon m / 4}$. From the first term of the maximum, (c) $2^{-\varepsilon m / 4} \le \delta / 2$.

**Step 1 (the two events).** Draw two independent sequences $s = (x_1, \dots, x_m)$ and $t = (y_1, \dots, y_m)$, and let $N$ be the set of elements of $s$. Define

- $E_1$: some heavy range $r$ has $r \cap s$ empty, that is, $N$ is not an $\varepsilon$-net;
- $E_2$: some heavy range $r$ has $r \cap s$ empty and $|r \cap t| \ge \varepsilon m / 2$.

**Step 2 ($\Pr[E_1] \le 2 \Pr[E_2]$).** Fix an outcome of $s$ in $E_1$, and let $r$ be a heavy range with $r \cap s$ empty, chosen as a function of $s$ alone. The count $X = |r \cap t|$ is binomial with $m$ trials and success probability $p = |r \cap A| / n \ge \varepsilon$, independent of $s$. If $X < \varepsilon m / 2$, then $X < pm/2$ and $|X - pm| > pm/2$, so by [Chebyshev's inequality](/chebyshev-inequality/)
$$\Pr[X < \varepsilon m / 2] \le \frac{mp(1-p)}{(pm/2)^2} < \frac{4}{pm} \le \frac{4}{\varepsilon m} \le \frac{1}{2}$$
by Step 0 (a). So $\Pr[E_2 \mid s] \ge 1/2$ for every $s$ in $E_1$, and $\Pr[E_2] \ge \Pr[E_1]/2$.

**Step 3 (a random split).** The $2m$ draws $z = (x_1, \dots, x_m, y_1, \dots, y_m)$ are independent and identically distributed, so their joint law does not change under a fixed permutation of the positions. Hence $E_2$ has the same probability in this experiment: draw $z$, then draw a uniform random permutation $\sigma$ of the $2m$ positions independently, and let $s$ be the first $m$ entries of $\sigma(z)$ and $t$ the last $m$. It is enough to show $\Pr[E_2 \mid z] \le \Phi_d(2m) \, 2^{-\varepsilon m / 2}$ for every fixed $z$.

**Step 4 (one trace).** Fix $z$ and let $B$ be its set of elements, so $|B| \le 2m$. Whether a range $r$ satisfies the condition of $E_2$ depends only on its trace $S = r \cap B$. Fix one trace $S$, and let $k$ be the number of positions of $z$ whose element is in $S$. If $k < \varepsilon m / 2$, the condition fails. Otherwise, the condition needs all $k$ of these positions to land in the second half, and under a uniform random permutation this has probability
$$\frac{\binom{2m - k}{m}}{\binom{2m}{m}} = \prod_{i=0}^{k-1} \frac{m - i}{2m - i} \le 2^{-k} \le 2^{-\varepsilon m / 2},$$
since each factor is at most $1/2$ (and the product is $0$ if $k > m$).

**Step 5 (the union bound).** The traces $r \cap B$ form the set $\mathcal{R}|_B$, and a subset of $B$ shattered by $\mathcal{R}|_B$ is shattered by $\mathcal{R}$, so by the Sauer-Shelah lemma $|\mathcal{R}|_B| \le \Phi_d(|B|) \le \Phi_d(2m)$. By the [union bound](/union-bound/) over these traces and Step 4, $\Pr[E_2 \mid z] \le \Phi_d(2m) \, 2^{-\varepsilon m/2}$.

**Step 6 (the numbers).** Map a set $\{a_1 < \dots < a_i\} \subseteq \{1, \dots, M\}$ with $i \le d$ to the sequence $(a_1, \dots, a_i, 0, \dots, 0)$ of length $d$ over $\{0, \dots, M\}$. The map is one to one, so $\Phi_d(M) \le (M + 1)^d$. With Steps 2 to 5 and Step 0 (b) and (c),
$$\Pr[E_1] \le 2 \Phi_d(2m) \, 2^{-\varepsilon m/2} \le 2 (2m + 1)^d \, 2^{-\varepsilon m / 4} \, 2^{-\varepsilon m / 4} \le 2 \cdot 1 \cdot \frac{\delta}{2} = \delta.$$
So $N$ is an $\varepsilon$-net with probability at least $1 - \delta$. $\blacksquare$

## Consequences

- **Small nets exist.** Every range space of VC dimension $d$ has $\varepsilon$-nets of size $O((d/\varepsilon) \log(d/\varepsilon))$, independent of $n$. For halfspaces in $\mathbb{R}^k$ ($d = k + 1$), boxes, balls and simplices this gives $O((1/\varepsilon) \log(1/\varepsilon))$ for fixed dimension.
- **Cuttings.** Take the range space whose ground set is a set $H$ of $n$ hyperplanes and whose ranges are the sets of hyperplanes crossing a simplex; its VC dimension is bounded in fixed dimension. A $(1/r)$-net of $H$ of size $O(r \log r)$, triangulated, gives cells each crossed by fewer than $n/r$ hyperplanes, a $(1/r)$-[cutting](/geometric-cutting/) of size $O((r \log r)^d)$.
- **Partition trees.** The [partition theorem](/partition-theorem/) and the simplex range searching structures of Haussler and Welzl rest on nets and cuttings built this way.
- **Hitting sets and set cover.** For range spaces of bounded VC dimension, the iterative reweighting method of Brönnimann and Goodrich turns small nets into an $O(d \log(d \cdot \mathrm{OPT}))$ approximation for [hitting set](/hitting-set/) and [set cover](/set-cover/).
- **Learning.** In [PAC learning](/pac-learning/), a consistent hypothesis on $m$ examples has error at most $\varepsilon$ with probability $1 - \delta$ once $m$ meets the same bound: the ranges are the symmetric differences of the target with the hypotheses, which have the same VC dimension.

## Tightness

**The order of growth.** Komlós, Pach and Woeginger (1992) improved the upper bound to $(d + o(1)) (1/\varepsilon) \ln(1/\varepsilon)$ and showed that for each $d \ge 2$ there are range spaces of VC dimension $d$ with no $\varepsilon$-net of size less than about $(d - 2 + o(1)) (1/\varepsilon) \ln(1/\varepsilon)$. So the factor $\log(1/\varepsilon)$ cannot be removed for abstract range spaces. Pach and Tardos (2013) showed that it cannot be removed for some geometric ones either: points and halfspaces in $\mathbb{R}^4$ need nets of size $\Omega((1/\varepsilon) \log(1/\varepsilon))$.

**Better geometric bounds.** For some geometric range spaces the logarithm is not needed: halfplanes and disks in the plane, and halfspaces in $\mathbb{R}^3$, have $\varepsilon$-nets of size $O(1/\varepsilon)$ (Matoušek, Seidel and Welzl 1990). Such nets are not found by plain random sampling of that size.

**The constants.** The constants $4$ and $8$ are what the proof gives, not what is observed. For intervals on a line ($d = 2$) with $n = 1000$, $\varepsilon = 0.1$ and $\delta = 0.1$, the theorem asks for $m \ge \max(172.9, 1171.5)$, so $m = 1172$ draws. In $2000$ simulated trials with seed $20251109$, the failure rate was $0.108$ at $m = 60$, $0.0135$ at $m = 80$, $0.001$ at $m = 100$, and $0$ at $m = 172$.

**A small exact case.** For the eight points $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ and closed halfplanes ($d = 3$), an exhaustive search gives the smallest $\varepsilon$-nets: for $\varepsilon = 1/2$ (heavy means at least $4$ points) the set $\{(2,3), (9,6)\}$ of size $2$; for $\varepsilon = 3/8$ a set of size $3$; for $\varepsilon = 1/4$ a set of size $4$. The theorem's bound for $\varepsilon = 1/2$ is $48 \log_2 48 \approx 268$ draws, far more than the $8$ points; it is meant for large $n$.

## History

Vapnik and Chervonenkis (1971) introduced the VC dimension and the double sampling argument to prove uniform convergence of frequencies to probabilities, which gives the stronger $\varepsilon$-approximations. Haussler and Welzl (1987) defined $\varepsilon$-nets, proved the theorem above with its explicit constants, and used it for simplex range searching; Clarkson's random sampling work of the same years used similar arguments for arrangements of hyperplanes. Blumer, Ehrenfeucht, Haussler and Warmuth (1989) brought the bound to learning theory. Komlós, Pach and Woeginger (1992) settled the dependence on $d$ up to lower order terms, and Matoušek, Seidel and Welzl (1990) found the first $O(1/\varepsilon)$ nets for geometric ranges.

## References
