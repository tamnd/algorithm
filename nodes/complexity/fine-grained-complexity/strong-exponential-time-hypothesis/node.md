---
tag: W0X5VV
kind: concept
slug: strong-exponential-time-hypothesis
name: Strong Exponential Time Hypothesis
aliases:
- SETH
area: complexity/fine-grained-complexity
level: advanced
summary: "The hypothesis that for every e > 0 there is a k such that k-SAT on n variables has no O(2^((1-e)n)) algorithm. The page also states ETH and the sparsification lemma."
prereqs: [k-sat, conjunctive-normal-form, exact-exponential-algorithms]
see_also: [orthogonal-vectors-hypothesis, seth-implies-ov-lower-bound, conditional-lower-bound, set-cover-conjecture, gap-eth, ppsz-algorithm, schoning-algorithm, fine-grained-reduction]
sources:
  - paper: doi:10.1006/jcss.2000.1727
    title: "Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001, 367-375 (conference version in CCC 1999)"
    locator: the definition of s_k, the exponential time hypothesis s_3 > 0, and the theorem that under ETH s_k increases infinitely often; this page relies on the journal version
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530 (conference version in FOCS 1998)"
    locator: the sparsification lemma and the SERF-completeness of k-SAT
  - paper: doi:10.1007/978-3-642-11269-0_6
    title: "Chris Calabro, Russell Impagliazzo and Ramamohan Paturi, The complexity of satisfiability of small depth circuits, IWPEC 2009, Lecture Notes in Computer Science 5917, 75-85"
    locator: Section 1.1 (the definition of s_k with randomized algorithms, and the name Strong Exponential Time Hypothesis for s_infinity = 1)
  - paper: doi:10.1145/1066100.1066101
    title: "Ramamohan Paturi, Pavel Pudlák, Michael E. Saks and Francis Zane, An improved exponential-time algorithm for k-SAT, Journal of the ACM 52(3), 2005, 337-364"
    locator: the PPSZ algorithm and its bound 2^((1-mu_k/(k-1))n)
  - paper: doi:10.1137/120868177
    title: "Timon Hertli, 3-SAT faster and simpler: unique-SAT bounds for PPSZ hold in general, SIAM Journal on Computing 43(2), 2014, 718-729"
    locator: the main theorem (the PPSZ bounds for 3-SAT and 4-SAT without the unique solution condition)
  - paper: doi:10.1145/2840728.2840746
    title: "Marco L. Carmosino, Jiawei Gao, Russell Impagliazzo, Ivan Mihajlin, Ramamohan Paturi and Stefan Schneider, Nondeterministic extensions of the strong exponential time hypothesis and consequences for non-reducibility, ITCS 2016, 261-270"
    locator: the definition of NSETH and its consequences for deterministic fine-grained reductions
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: the section on cooperative subset queries and orthogonal vectors (the reduction from CNF-SAT)
  - paper: doi:10.1145/2925416
    title: "Marek Cygan, Holger Dell, Daniel Lokshtanov, Dániel Marx, Jesper Nederlof, Yoshio Okamoto, Ramamohan Paturi, Saket Saurabh and Magnus Wahlström, On problems as hard as CNF-SAT, ACM Transactions on Algorithms 12(3), 2016, article 41 (conference version in CCC 2012)"
    locator: the lower bounds under SETH for Hitting Set, Set Splitting and NAE-SAT, and the set cover conjecture
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the sections on SETH, the orthogonal vectors problem and the problems that are hard under SETH
  - paper: "Mihai Pătraşcu and Ryan Williams, On the possibility of faster SAT algorithms, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA 2010)"
    locator: the reduction from CNF-SAT to k-Dominating Set and the n^(k-e) lower bound under SETH
---

The Strong Exponential Time Hypothesis (SETH) says that satisfiability of [CNF formulas](/conjunctive-normal-form/) cannot be solved much faster than by trying all assignments: for every $\varepsilon > 0$ there is a clause width $k$ such that [$k$-SAT](/k-sat/) on $n$ variables has no algorithm with time $O(2^{(1-\varepsilon) n})$. It is a hypothesis, not a theorem, and it is much stronger than $\mathsf{P} \ne \mathsf{NP}$. This page also states the weaker Exponential Time Hypothesis (ETH), which has no page of its own, and the sparsification lemma that both of them use. Through the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/), SETH is the source of most [conditional lower bounds](/conditional-lower-bound/) for problems with quadratic algorithms.

## In plain words

To decide whether a logic formula of a simple kind can be made true, an algorithm can try every way to set the yes-or-no variables. The number of ways doubles with each new variable. Clever algorithms do better, but their savings shrink as the clauses get longer. SETH says that this is no accident: when the clauses are long enough, no algorithm saves even a small fixed fraction of the doubling.

ETH is the weaker claim that formulas with clauses of three items need time that grows exponentially, with some rate. SETH says the rate approaches the rate of brute force.

Nobody can prove either claim. Researchers use them as a fixed starting point. If a fast method for some other problem would also break SETH, then that problem probably has no fast method.

## The idea

### Model and notation

A $k$-CNF formula has $n$ variables and $m$ clauses, and each clause is an OR of at most $k$ literals. $k$-SAT asks whether such a formula has a satisfying assignment. Running times are on the [word RAM](/word-ram/) with words of $O(\log n)$ bits; the choice of a reasonable model changes only polynomial factors, which do not matter here. For a fixed $k$, a formula has at most $\sum_{w \le k} \binom{n}{w} 2^w$ distinct clauses, a polynomial in $n$, so a factor $\mathrm{poly}(m)$ in a running time is a factor $\mathrm{poly}(n)$, and it disappears when $\varepsilon$ is made a little smaller.

Impagliazzo and Paturi defined, for $k \ge 3$,

$$s_k = \inf\{\delta : k\text{-SAT has an algorithm with time } O(2^{\delta n})\}.$$

Calabro, Impagliazzo and Paturi use the same definition with randomized algorithms (bounded error, time $\mathrm{poly}(m)\, 2^{\delta n}$). A $k$-CNF formula is also a $(k+1)$-CNF formula, so $s_3 \le s_4 \le \cdots \le 1$, and the limit $s_\infty = \lim_{k \to \infty} s_k$ exists.

### Hypothesis (ETH)

$s_3 > 0$. In words: there is a constant $\delta > 0$ such that no algorithm decides 3-SAT on $n$ variables in time $O(2^{\delta n})$. The usual form also excludes randomized algorithms with bounded error.

ETH implies $\mathsf{P} \ne \mathsf{NP}$, and more: under ETH, 3-SAT has no algorithm with time $2^{o(n)}$. With the sparsification lemma below, it also has none with time $2^{o(m)}$, and so no $2^{o(n+m)}$ algorithm.

### Hypothesis (SETH)

$s_\infty = 1$. In words: for every $\varepsilon > 0$ there is an integer $k$ such that no algorithm decides $k$-SAT on $n$ variables in time $O(2^{(1-\varepsilon) n})$. In the form of Calabro, Impagliazzo and Paturi, which most later papers use, randomized algorithms with bounded error are excluded too.

The quantifiers matter. SETH does not say that 3-SAT needs time $2^{n}$; 3-SAT has much faster algorithms. It says that the exponent of the best algorithm goes to 1 as $k$ grows.

**Weaker form (CNF-SETH).** For every $\varepsilon > 0$, CNF-SAT on $n$ variables and $m$ clauses, with no bound on the clause width, has no algorithm with time $\mathrm{poly}(m)\, 2^{(1-\varepsilon) n}$. SETH implies CNF-SETH, because a $k$-CNF formula is a CNF formula and $m$ is polynomial in $n$. The converse is not known. Some reductions, such as the one in the [proof that SETH implies the OV lower bound](/seth-implies-ov-lower-bound/), need only CNF-SETH.

**SETH implies ETH.** Suppose ETH fails, so $s_3 = 0$. A $k$-CNF formula with $m$ clauses turns into an equivalent 3-CNF formula with $n + O(m)$ variables by splitting each long clause with new variables. After sparsification each part has $m = O(n)$ clauses, so every $s_k$ is 0 and $s_\infty = 0 < 1$. So SETH fails too.

### The sparsification lemma

**Lemma (Impagliazzo, Paturi and Zane 2001).** For every $k$ and every $\varepsilon > 0$ there is a constant $C = C(k, \varepsilon)$ such that the following holds. Every $k$-CNF formula $F$ on $n$ variables is equivalent to an OR $F_1 \lor \cdots \lor F_t$ of $t \le 2^{\varepsilon n}$ formulas, each a $k$-CNF formula on the same variables with at most $Cn$ clauses. The list $F_1, \ldots, F_t$ can be computed in time $\mathrm{poly}(n)\, 2^{\varepsilon n}$.

So for questions about exponential time, a $k$-SAT instance can be assumed to have a linear number of clauses: an algorithm with time $2^{\delta n}$ on sparse formulas gives one with time $\mathrm{poly}(n)\, 2^{(\delta + \varepsilon) n}$ on all formulas. The lemma is the reason why the orthogonal vectors hypothesis can use dimension $d = c \log n$; see [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/).

### What is known about $s_k$

- Unconditional upper bounds: [Schöning's algorithm](/schoning-algorithm/) gives $s_k \le \log_2(2 - 2/k)$, randomized. The [PPSZ algorithm](/ppsz-algorithm/) gives $s_k \le 1 - \mu_k/(k-1)$, randomized, where $\mu_k = \sum_{j \ge 1} \frac{1}{j(j + 1/(k-1))}$ tends to $\pi^2/6$. For $k \ge 5$ this is in the 2005 paper; for $k = 3$ and $4$ the general case is due to Hertli (2014). Both bounds have the form $1 - \Theta(1/k)$, so they tend to 1. This is the main evidence for SETH.
- Unconditional, for CNF-SAT with $m = cn$ clauses: time $2^{(1 - 1/O(\log c)) n}$ (Calabro, Impagliazzo and Paturi 2006, as cited in their 2009 paper). The saving vanishes as the density $c$ grows.
- Conditional on ETH: $s_k$ increases infinitely often (Impagliazzo and Paturi 2001). So the hierarchy of $k$-SAT problems does not collapse to one exponent.

### How strong are the hypotheses

ETH is widely believed. SETH is less widely believed, because it fixes the exact constant in the exponent, and a better algorithm for large $k$ would refute it. Its consequences are still useful: a conditional lower bound under SETH says that a faster algorithm for the target problem would also be a breakthrough for CNF-SAT.

**NSETH.** Carmosino, Gao, Impagliazzo, Mihajlin, Paturi and Schneider (2016) proposed a nondeterministic form: for every $\varepsilon > 0$ there is $k$ such that the set of unsatisfiable $k$-CNF formulas (equivalently, $k$-DNF tautologies) has no nondeterministic algorithm with time $O(2^{(1-\varepsilon) n})$. Under NSETH, some problems cannot be shown SETH-hard by deterministic fine-grained reductions, because they have fast nondeterministic algorithms for both answers.

### Relation to the other hypotheses

- SETH implies the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/) (Williams 2005, proved on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/)). It is not known whether OVH implies SETH.
- The [3SUM conjecture](/3sum-conjecture/) is not known to follow from SETH, and the [APSP conjecture](/apsp-conjecture/) is not known to follow from SETH or from 3SUM.
- [Gap-ETH](/gap-eth/) is a stronger form of ETH about approximate 3-SAT, used for hardness of approximation.
- The [set cover conjecture](/set-cover-conjecture/) is a similar hypothesis for Set Cover. It is open whether SETH implies it.

## Examples

**Known exponents against SETH.** The table gives the exponent $\delta$ in $2^{\delta n}$, and the base $2^{\delta}$, for the two classic randomized algorithms. The values come from the formulas above, with $\mu_k$ summed to $2 \cdot 10^6$ terms.

| $k$ | Schöning base $2 - 2/k$ | Schöning exponent | PPSZ exponent | PPSZ base |
|---|---|---|---|---|
| 3 | 1.3333 | 0.4150 | 0.3863 | 1.3070 |
| 4 | 1.5 | 0.5850 | 0.5548 | 1.4690 |
| 5 | 1.6 | 0.6781 | 0.6502 | 1.5694 |
| 10 | 1.8 | 0.8480 | 0.8307 | 1.7786 |
| 20 | 1.9 | 0.9260 | 0.9166 | 1.8877 |
| 100 | 1.98 | 0.9855 | 0.9835 | 1.9773 |

For $k = 3$, $\mu_3 / 2 = 2 - 2 \ln 2 \approx 0.61371$, so the PPSZ exponent is $2 \ln 2 - 1 \approx 0.3863$ and the base is $2^{2 \ln 2 - 1} \approx 1.30703$. The saving $1 - \delta$ of PPSZ, times $k$, goes from 1.841 at $k = 3$ down to 1.649 at $k = 100$, toward $\pi^2/6 \approx 1.6449$. So the saving behaves like $1.64/k$, and it tends to 0. SETH says that no algorithm does better in this limit.

**The number of clauses is polynomial.** Over $n = 100$ variables there are $\binom{100}{3} \cdot 8 = 1{,}293{,}600$ distinct clauses of width exactly 3, and 1,313,600 of width at most 3. A 3-CNF formula without repeated clauses has at most that many, so $m$ is $O(n^3)$, and $\mathrm{poly}(m)$ factors are $\mathrm{poly}(n)$.

**What a fast quadratic algorithm would do.** The reduction of Williams turns a CNF formula on $N$ variables into an [orthogonal vectors](/orthogonal-vectors/) instance with $2^{N/2}$ vectors on each side. For $N = 60$ this is $2^{30} = 1{,}073{,}741{,}824$ vectors per side. An OV algorithm with time $n^{2 - \varepsilon}$ would then decide CNF-SAT in time about $2^{(1 - \varepsilon/2) N}$; for $\varepsilon = 0.1$, the exponent is $0.95 N$, which would refute SETH.

## Where it is used

- Quadratic lower bounds, conditional on SETH, through OV: [edit distance](/edit-distance-seth-lower-bound/), [longest common subsequence](/lcs-seth-lower-bound/), [Fréchet distance](/frechet-distance/), [regular expression matching](/backurs-indyk-regex-hardness/), and approximate graph diameter. See [quadratic-time hardness](/quadratic-time-hardness/).
- Exponential lower bounds, conditional on SETH: Cygan et al. (2016) show that [Hitting Set](/hitting-set/) on $n$ elements, Set Splitting and NAE-SAT on $n$ variables have no $O(2^{(1-\varepsilon) n})$ algorithm.
- Parameterized lower bounds: under SETH, [$k$-Dominating Set](/parameterized-dominating-set/) has no $O(n^{k - \varepsilon})$ algorithm for $k \ge 3$ (Pătraşcu and Williams 2010), and dynamic programs over a [tree decomposition](/treewidth/) are optimal in the base of the exponent for several problems.
- Lower bounds conditional on ETH: no $2^{o(n)}$ algorithm for 3-coloring, Hamiltonian cycle and many other NP-hard problems, through linear-size reductions from sparse 3-SAT.
- [Fine-grained reductions](/fine-grained-reduction/) use SETH as the source problem of the largest class of conditional bounds.

## References
