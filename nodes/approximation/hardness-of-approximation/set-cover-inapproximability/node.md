---
tag: H4FSRY
kind: theorem
slug: set-cover-inapproximability
name: Set cover inapproximability
aliases:
- Feige's set cover hardness
- ln n hardness of set cover
- Lund-Yannakakis set cover hardness
- Dinur-Steurer set cover hardness
area: approximation/hardness-of-approximation
level: advanced
summary: For each ε > 0, a ratio of (1 - ε) ln n for set cover is NP-hard (Dinur and Steurer 2014; Feige 1998 under a weaker assumption), so greedy is optimal. Proved here for every constant ratio.
prereqs: [set-cover, greedy-set-cover, label-cover, gap-problem, parallel-repetition-theorem]
see_also: [max-coverage-inapproximability, dominating-set-inapproximability, k-median-inapproximability, hitting-set, set-cover-conjecture, two-prover-one-round-game, gap-preserving-reduction, approximation-threshold]
sources:
  - paper: doi:10.1145/185675.306789
    title: Carsten Lund and Mihalis Yannakakis, On the hardness of approximating minimization problems, Journal of the ACM 41(5), 1994
    locator: Section 3 (set cover, the reduction from two-prover systems with set systems)
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: Sections 2 to 4 (multi-prover systems, partition systems and Theorem 4.4)
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the set cover corollary, (1 - α) ln n is NP-hard for every α > 0
  - paper: doi:10.4086/toc.2015.v011a007
    title: Dana Moshkovitz, The projection games conjecture and the NP-hardness of ln n-approximating set-cover, Theory of Computing 11, 2015
    locator: the reduction from projection games to set cover
  - paper: doi:10.1145/258533.258641
    title: Ran Raz and Shmuel Safra, A sub-constant error-probability low-degree test, and a sub-constant error-probability PCP characterization of NP, STOC 1997
    locator: the corollary c ln n for set cover unless P = NP
  - paper: "M. Bellare, S. Goldwasser, C. Lund and A. Russell, Efficient probabilistically checkable proofs and applications to approximation, Proceedings of the 25th ACM Symposium on Theory of Computing (STOC), 1993"
    locator: every constant ratio for set cover is NP-hard
  - paper: "M. Naor, L. J. Schulman and A. Srinivasan, Splitters and near-optimal derandomization, Proceedings of the 36th IEEE Symposium on Foundations of Computer Science (FOCS), 1995"
    locator: the deterministic construction of set systems used in the reduction
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 29, Section 29.7 (hardness of set cover, with set systems and label cover)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 16.5 (the reduction from label cover to set cover)
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: the greedy bound H_n
  - paper: "P. Slavík, A tight analysis of the greedy algorithm for set cover, Journal of Algorithms 25(2), 1997"
    locator: the bound ln n - ln ln n + O(1) for greedy
  - paper: "L. Trevisan, Non-approximability results for optimization problems on bounded degree instances, Proceedings of the 33rd ACM Symposium on Theory of Computing (STOC), 2001"
    locator: set cover with sets of size at most d, ratio ln d - O(ln ln d)
---

The set cover inapproximability theorem says that the [greedy algorithm](/greedy-set-cover/) for [set cover](/set-cover/) is optimal up to lower-order terms. Greedy uses at most $H_n \le \ln n + 1$ times the optimal number of sets, and for each $\varepsilon > 0$ no polynomial algorithm reaches $(1 - \varepsilon) \ln n$ unless P = NP. Feige (1998) proved this threshold under the assumption NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$, and Dinur and Steurer (2014) proved it under P $\ne$ NP. All proofs start from [label cover](/label-cover/) and replace each edge by a small set system that makes a short cover reveal a good labeling. This page proves that reduction in full for constant ratios and sketches the logarithmic and sharp versions.

## Statement

A set cover instance has a universe of $n$ elements and a family of $M$ sets whose union is the universe. $\mathrm{OPT}$ is the least number of sets in a cover. For this minimization problem, a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios below are absolute.

**Theorem.**

1. *(Dinur and Steurer 2014.)* For each $\varepsilon > 0$, if a polynomial algorithm has ratio $(1 - \varepsilon) \ln n$ for set cover, then P = NP.
2. *(Feige 1998.)* For each $\varepsilon > 0$, if a polynomial algorithm has ratio $(1 - \varepsilon) \ln n$ for set cover, then NP $\subseteq$ DTIME$(n^{O(\log \log n)})$.
3. *(Constant ratios, proved below.)* For each constant $c \ge 1$, if a polynomial algorithm has ratio $c$ for set cover, then P = NP.
4. *(Logarithmic ratio, sketched below.)* There is a constant $c_0 > 0$ such that a polynomial algorithm with ratio $c_0 \ln n$ gives NP $\subseteq$ DTIME$(n^{O(\log \log n)})$.

Parts 1 and 2 are cited. The hard instances in all parts have $M$ polynomial in $n$, so the bounds hold also as functions of the input size.

## In plain words

Start from a hard puzzle: give each point of a two-sided network a label so that the label rules on the lines hold. It is hard to tell a network where all rules can hold from one where almost none can.

Turn each line into a group of items, and each possible label of each point into a group of items. Arrange the items with a special pattern so that a line's items are covered cheaply only when the two labels that cover them obey the rule. Then a network with a perfect labeling gives a cover with one group per point. A network where almost no rule can hold needs many more groups per point, because a short cover would show a good labeling. So no fast method can come close to the best cover.

## Proof

The proof of part 3 has five steps. It uses three facts about label cover; the first is proved on the [label cover](/label-cover/) page from the PCP theorem and the [parallel repetition theorem](/parallel-repetition-theorem/).

*Step 0: the source problem.* A label cover instance has left vertices $U$, right vertices $W$, edges $E$, alphabets $\Sigma_U$ and $\Sigma_W$ with $L = |\Sigma_W|$, and projections $\pi_e : \Sigma_U \to \Sigma_W$. For each constant $s > 0$, $\mathrm{GapLC}_{1, s}$, value 1 against value at most $s$, is NP-hard with constant alphabet sizes. The hard instances can be taken *biregular*, all left degrees equal and all right degrees equal: start from 3-SAT instances in which each variable is in exactly 5 clauses, which keep a constant gap (Feige 1998), and note that parallel repetition keeps biregularity.

*Step 1: equal sides.* From a biregular instance build a new one with $|W|$ copies $(u, i)$ of each left vertex and $|U|$ copies $(w, j)$ of each right vertex, and an edge $((u, i), (w, j))$ with projection $\pi_e$ for each edge $e = (u, w)$ and all $i, j$. Both sides have $N_0 = |U| \cdot |W|$ vertices, and every vertex has the same degree, because $\deg(u) \cdot |U| = |E| = \deg(w) \cdot |W|$. The value does not change. A labeling of the old instance, copied to all copies, satisfies the same fraction. In the other direction, take a labeling of the new instance, choose a copy $i(u)$ for each $u$ and $j(w)$ for each $w$ uniformly at random, and label $u$ and $w$ as these copies are labeled. Each new edge $((u, i), (w, j))$ is the chosen copy of its old edge with probability $1/(|U| |W|)$, so the expected fraction of satisfied old edges equals the fraction of satisfied new edges. Some choice reaches the expectation.

*Step 2: the partition system.* A set system $(B; C_1, \ldots, C_L)$ has *property $h$* if no family of at most $h$ sets, each of the form $C_b$ or its complement $\overline{C_b}$, covers $B$, unless the family contains both $C_b$ and $\overline{C_b}$ for some $b$. Such a system exists with $|B| = m$ for every $m > 2^h \, h \ln(2L)$. Choose each $C_b$ at random, each point in it with probability $\frac12$, independently. A family without a complementary pair uses at most $h$ distinct indices, and it suffices to look at families with exactly $\min(h, L)$ distinct indices, one sign each, because more sets cover more. For one such family, a point is missed with probability $2^{-h}$ or more, independently for each point, so the family covers $B$ with probability at most $(1 - 2^{-h})^m < e^{-m 2^{-h}}$. There are at most $(2L)^h$ families, so the probability that some family covers $B$ is less than $(2L)^h e^{-m 2^{-h}} \le 1$. For constant $h$ and $L$, the size $m$ is a constant, and a system with property $h$ is found by trying all systems, in constant time.

*Step 3: the construction.* Fix an integer $h \ge 2$ and a system $(B; C_1, \ldots, C_L)$ with property $h$. Given a label cover instance from step 1, build the universe $E \times B$, with $n = |E| \cdot m$ elements, and the sets

$$S_{w, b} = \{(e, x) : e \ni w, \ x \in C_b\}, \qquad S_{u, a} = \{(e, x) : e \ni u, \ x \in \overline{C_{\pi_e(a)}}\},$$

one for each $w \in W$, $b \in \Sigma_W$, $u \in U$ and $a \in \Sigma_U$. There are $M = N_0 (|\Sigma_U| + L)$ sets, so the map takes polynomial time.

*Step 4: completeness.* Let a labeling $(\ell_U, \ell_W)$ satisfy every edge. Take $S_{u, \ell_U(u)}$ for each $u$ and $S_{w, \ell_W(w)}$ for each $w$, which is $2 N_0$ sets. For an edge $e = (u, w)$, the block $\{e\} \times B$ is covered by $C_b \cup \overline{C_{\pi_e(\ell_U(u))}} = C_b \cup \overline{C_b} = B$ with $b = \ell_W(w)$. So $\mathrm{OPT} \le 2 N_0$.

*Step 5: soundness.* Let $\mathcal{C}$ be a cover with $|\mathcal{C}| \le \frac{h}{2} N_0$ sets. For a vertex $v$, let $L(v)$ be the set of labels $a$ with $S_{v, a} \in \mathcal{C}$. The block of the edge $e = (u, w)$ is covered only by the sets $S_{w, b}$ with $b \in L(w)$, which give $C_b$ on the block, and $S_{u, a}$ with $a \in L(u)$, which give $\overline{C_{\pi_e(a)}}$. Call $e$ *good* if $|L(u)| + |L(w)| \le h$. Then at most $h$ sets of the system cover $B$, so by property $h$ there are $a \in L(u)$ and $b \in L(w)$ with $\pi_e(a) = b$.

All degrees are equal and both sides have $N_0$ vertices, so a uniform random edge has a uniform random left end and a uniform random right end. Hence the average of $|L(u)| + |L(w)|$ over the edges is $\sum_{v} |L(v)| / N_0 = |\mathcal{C}| / N_0 \le \frac{h}{2}$. By Markov's inequality, fewer than half of the edges have $|L(u)| + |L(w)| > h$, so at least half are good.

Now give each vertex a label chosen uniformly from $L(v)$, or any label if $L(v)$ is empty. A good edge has $|L(u)|, |L(w)| \le h$ and a matching pair, so it is satisfied with probability at least $1/h^2$. The expected fraction of satisfied edges is at least $\frac{1}{2h^2}$, so the value is at least $\frac{1}{2h^2}$.

*Conclusion.* Take $s < \frac{1}{2 h^2}$. On instances of value 1, $\mathrm{OPT} \le 2 N_0$. On instances of value at most $s$, step 5 shows $\mathrm{OPT} > \frac{h}{2} N_0$. The ratio of the two bounds is $\frac{h}{4}$. Given $c$, choose $h > 4c$. An algorithm with ratio $c$ returns at most $2 c N_0 < \frac{h}{2} N_0$ sets on the first kind of instance, and more than $\frac{h}{2} N_0$ on the second, so it decides $\mathrm{GapLC}_{1, s}$, and P = NP. This proves part 3. $\blacksquare$

*Part 4 (sketch).* Choose $h = \Theta(\log |E|)$. Step 0 then needs soundness $s < 1/(2h^2)$, which is $1/\Theta(\log^2 |E|)$. Raz's theorem gives it with $k = \Theta(\log \log n)$ repetitions, so the label cover has size $n^{O(\log \log n)}$ and $L = 2^k$ is polylogarithmic. Step 2 needs $m \approx 2^h h \ln(2L)$, which is polynomial, and a deterministic construction (Naor, Schulman and Srinivasan 1995). With $2^h \ge |E| \cdot h \ln(2L)$, the universe has $n \le 2^{2h + O(1)}$ elements, so the gap $\frac{h}{4}$ is at least $c_0 \ln n$ with $c_0 = \frac{1}{8 \ln 2} - o(1)$. The steps not proved here are the two cited constructions.

*Parts 1 and 2 (sketch).* The loss in step 5 comes from the two-sided count: each block is covered by sets from both sides, and Markov's inequality costs a constant factor. Feige replaces the two-prover game by a game with $k$ provers and replaces the system by a *partition system*: $L$ partitions of $B$ into $k$ parts each, such that no $d = (1 - \varepsilon) k \ln m$ parts from distinct partitions cover $B$. In the yes case each block is covered by the $k$ parts of one partition. In the no case most blocks need about $k \ln m$ sets, by the same decoding argument. This gives the sharp constant $1 - \varepsilon$ in front of $\ln n$, with size $n^{O(\log \log n)}$ from the repetition. Moshkovitz (2015) showed that two provers suffice if the label cover has low soundness and small alphabets, and Dinur and Steurer (2014) built such label cover instances in polynomial time from a new bound on the parallel repetition of projection games, which gives part 1. These two arguments are cited, not proved.

### Example

Take one edge $e = (u, w)$, $\Sigma_U = \{0, 1, 2\}$, $\Sigma_W = \{0, 1\}$ and $\pi_e = (0, 1, 1)$. Use the hypercube system $B = \{0, 1\}^2$ with $C_b$ the points whose bit $b$ is 1; it has property $h$ for every $h$. A family without a complementary pair misses the point whose bit $b$ is 0 when $C_b$ is in the family and 1 when $\overline{C_b}$ is in it. Write points as numbers 0 to 3. Then $S_{w, 0} = \{1, 3\}$, $S_{w, 1} = \{2, 3\}$, $S_{u, 0} = \overline{C_0} = \{0, 2\}$ and $S_{u, 1} = S_{u, 2} = \overline{C_1} = \{0, 1\}$. The cover $\{S_{u, 0}, S_{w, 0}\}$ comes from the satisfying labeling $(0, 0)$. The family $\{S_{w, 0}, S_{w, 1}\}$ misses the point 0, as property $h$ says. For small instances with the hypercube system, brute force confirms that $\mathrm{OPT}$ equals the number of non-isolated vertices exactly when the value is 1, and is larger otherwise.

## Consequences

- **Greedy is optimal.** The greedy bound $H_n \le \ln n + 1$ and part 1 fix the approximation threshold of set cover at $\ln n$, up to lower-order terms. The same holds for weighted set cover and for [hitting set](/hitting-set/), which is the same problem with the roles of sets and elements exchanged.
- **Problems with the same threshold.** [Dominating set](/dominating-set-inapproximability/) is equivalent to set cover under reductions that keep the optimum. [Maximum coverage](/max-coverage-inapproximability/) cannot be approximated better than $1 - 1/e$, which also follows from part 1. Each of these transfers the bound without loss.
- **Problems with a constant bound.** The structure of the instances, sets against elements, gives the $1 + 2/e$ bound for [$k$-median](/k-median-inapproximability/) and the $1.463$ bound for facility location.
- **Bounded set size.** If every set has at most $d$ elements, greedy gives $H_d$, and the ratio $\ln d - O(\ln \ln d)$ is NP-hard (Trevisan 2001). For element frequency at most $f$, the bounds are on the [set cover](/set-cover/) page.
- **Exact and parameterized forms.** The [set cover conjecture](/set-cover-conjecture/) is about exact algorithms. For the parameter $k = \mathrm{OPT}$, see [parameterized inapproximability](/parameterized-inapproximability/).

## Tightness

The constant 1 in front of $\ln n$ is tight: greedy reaches $H_n$, and Slavík (1997) showed that greedy has ratio $\ln n - \ln \ln n + \Theta(1)$. The lower-order term of the threshold is not known.

The gap of part 3 is as large as the reduction allows. On the instances, $\mathrm{OPT}$ is between $2 N_0$ and $\frac{h}{2} N_0$ only, and the system needs $m > 2^h$ points, so $n > 2^h$ and the gap $\frac{h}{4}$ is at most $O(\ln n)$. Feige's partition systems remove the factor lost to Markov's inequality and to the two-sided count, which is why they reach $(1 - \varepsilon) \ln n$.

## History

Johnson (1974), Lovász (1975) and Chvátal (1979) analysed the greedy algorithm. Lund and Yannakakis (1994) gave the first logarithmic hardness: ratio $c \log_2 n$ for each $c < \frac14$ unless NP has quasi-polynomial algorithms, by the two-prover reduction of this page with set systems. Bellare, Goldwasser, Lund and Russell (1993) showed that every constant ratio is NP-hard. Raz and Safra (1997) and Arora and Sudan (1997) obtained $c \ln n$ for some $c > 0$ unless P = NP, from PCPs with sub-constant error. Feige (1998) found the sharp constant with partition systems and $k$-prover games. Moshkovitz (2015) reduced the question to a conjecture on projection games, and Dinur and Steurer (2014) proved enough of it to show the sharp threshold under P $\ne$ NP.

## References
