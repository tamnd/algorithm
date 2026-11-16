---
tag: D9FDCV
kind: problem
slug: k-sum
name: k-SUM
aliases:
- generalized subset sum over sorted lists
- k-SUM problem
area: complexity/fine-grained-complexity
level: core
summary: "Given n integers and a fixed k, decide whether k of them sum to zero. Meet in the middle takes about n^(k/2) time; a 2026 preprint beats n^ceil(k/2) for odd k."
prereqs: [3sum, meet-in-the-middle-attack, time-complexity]
see_also: [3sum, 3sum-conjecture, subset-sum-problem, horowitz-sahni-algorithm, schroeppel-shamir-algorithm, linear-decision-tree, parameterized-clique, fine-grained-reduction]
sources:
  - paper: "Jeff Erickson, Lower bounds for linear satisfiability problems, Chicago Journal of Theoretical Computer Science 1999, article 8 (conference version in SODA 1995, 388-395)"
    locator: the Omega(n^ceil(k/2)) bound for k-SUM in the k-linear decision tree model; the page relies on the journal version
  - paper: doi:10.1145/3285953
    title: "Daniel M. Kane, Shachar Lovett and Shay Moran, Near-optimal linear decision trees for k-SUM and related problems, Journal of the ACM 66(3), 2019, article 16 (conference version in STOC 2018)"
    locator: the abstract (O(n log^2 n) queries for every constant k, each query 2k-sparse with coefficients in {-1, 0, 1}); the page relies on the journal version
  - paper: doi:10.1137/1.9781611973075.86
    title: "Mihai Pătraşcu and Ryan Williams, On the possibility of faster SAT algorithms, SODA 2010, 1065-1075"
    locator: the abstract and the section on k-SUM (an n^o(k) algorithm for k-SUM would give a faster algorithm for k-SAT)
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on the 3SUM hypothesis and its generalization to k-SUM
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract (a randomized O(n^(ceil(k/2) - e_k)) algorithm for integer k-SUM for every odd constant k); not yet refereed
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the introduction (the 3SUM algorithm, and the remark that k-SUM for k at least 4 is not covered); not yet refereed
---

k-SUM asks whether $n$ given integers contain $k$ that sum to zero, where $k \ge 2$ is a fixed constant. The case $k = 3$ is [3SUM](/3sum/). The case $k = 2$ takes $O(n \log n)$ time by sorting. For larger $k$, the meet-in-the-middle method lists all sums of about $k/2$ elements and solves the problem in about $n^{\lceil k/2 \rceil}$ time. For decades no algorithm beat this exponent by a constant, and the $k$-SUM hypothesis said that none could.

The problem links fine-grained complexity with parameterized complexity. Erickson proved that $n^{\lceil k/2 \rceil}$ is optimal in a restricted decision tree model. Pătraşcu and Williams proved that an $n^{o(k)}$ algorithm would give faster algorithms for $k$-SAT. In October 2026, Chan, Itakura, Ma and Yu posted a preprint with a randomized algorithm that beats $n^{\lceil k/2 \rceil}$ by a polynomial factor for every odd $k$. For even $k \ge 4$ the exponent $k/2$ is still the best known.

This page is about the problem for general $k$. The special case is on [3SUM](/3sum/), and the hypothesis for $k = 3$ is on [3SUM conjecture](/3sum-conjecture/).

## In plain words

You have a list of whole numbers, some positive and some negative, and a small fixed count, such as 4 or 5. Can you pick that many different numbers from the list so that they cancel out to zero?

Trying every group is slow. A better way splits each group into two halves. First write down every possible half, with its total. Then look for two halves whose totals cancel out. This needs about as many steps as there are halves, which is much less than the number of full groups.

Experts believed that the halves trick was the best possible. A 2026 paper claims a faster method when the count is odd. When the count is even, the halves trick is still the best known.

## Definition

**k-SUM** (for a fixed integer $k \ge 2$)

- Instance: a set $S$ of $n$ integers, each in binary.
- Question: are there $k$ distinct elements of $S$ whose sum is $0$?

**The model.** The [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits. The integers are in $\{-n^{c}, \ldots, n^{c}\}$, where the constant $c$ may depend on $k$, so each number and each sum of $k$ numbers fits in $O(1)$ words. The real form uses the [real RAM](/real-ram/) or the [linear decision tree](/linear-decision-tree/) model. All time bounds below treat $k$ as a constant unless they say otherwise.

**Equivalent forms.** As for 3SUM, these forms are equivalent up to factors that depend only on $k$ and on $\log n$:

- *$k$ lists.* Given lists $A_1, \ldots, A_k$ of $n$ integers each, are there $a_1 \in A_1, \ldots, a_k \in A_k$ with $a_1 + \cdots + a_k = 0$? From one set to $k$ lists, give each element one of $k$ colors so that every $k$ distinct elements get $k$ different colors in at least one of the colorings, as in [3SUM](/3sum/). From $k$ lists to one set, add a different large offset to each list so that a zero sum must take one element from each list.
- *Target.* Sum $t$ instead of $0$: replace each $x$ by $kx - t$.

## Variants

- **Real k-SUM.** The input is $n$ real numbers.
- **Repetition allowed.** The $k$ elements need not be distinct. This changes only small details of the algorithms.
- **Subset sum.** [Subset sum](/subset-sum-problem/) with $m$ items reduces to $k$-SUM on lists of $2^{m/k}$ partial sums each: split the items into $k$ groups and list the sums of the subsets of each group. Meet in the middle then gives the [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/) for $k = 2$ and the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/) for $k = 4$.
- **k as part of the input.** If $k$ grows with $n$, the problem is NP-complete, as it contains subset sum. As a parameterized problem in $k$, it is W[1]-hard, by a reduction from [$k$-clique](/parameterized-clique/) to $O(k^2)$-SUM due to Downey and Fellows.

## Examples

**Meet in the middle for $k = 4$.** Let $T = \{-8, -3, 1, 4, 6, 10\}$. List the $\binom{6}{2} = 15$ sums of two distinct elements. Some sums repeat, and the 13 distinct values are

$$-11, -7, -4, -2, 1, 2, 3, 5, 7, 10, 11, 14, 16.$$

Look for two pair sums $s$ and $-s$ that use four different elements. The pairs $(-8, -3)$ and $(1, 10)$ give $-11$ and $11$. The same quadruple also splits as $(-8, 1)$ and $(-3, 10)$, with sums $-7$ and $7$, and as $(-8, 10)$ and $(-3, 1)$, with sums $2$ and $-2$. So the method finds $-8 + (-3) + 1 + 10 = 0$ three times, once for each split. A test of all $\binom{6}{4} = 15$ quadruples shows that this is the only solution.

**How much the split saves.** For $n = 1000$, there are $\binom{1000}{4} \approx 4.1 \times 10^{10}$ quadruples but only $\binom{1000}{2} \approx 5 \times 10^{5}$ pairs. For $k = 5$, there are $\binom{1000}{5} \approx 8.3 \times 10^{12}$ groups, and the bound $n^{\lceil 5/2 \rceil} = n^3$ is $10^9$.

## Known algorithms

- **Meet in the middle, even $k$.** List the $O(n^{k/2})$ sums of $k/2$ elements, sort them, and look for two sums $s$ and $-s$ with a two-pointer scan. This takes $O(n^{k/2} \log n)$ time, deterministic. With a [hash table](/hash-table/) in place of sorting, it takes $O(n^{k/2})$ expected time. The $k$-list form avoids the check that the two halves use different elements.
- **Meet in the middle, odd $k$.** Sort the list $L$ of sums of $(k-1)/2$ elements once. For each element $x$, scan $L$ from both ends for two sums that add to $-x$. This takes $O(n^{(k+1)/2})$ time, deterministic. For $k = 3$ it is the quadratic algorithm of [3SUM](/3sum/).
- **Small range.** If all numbers are in $[-U, U]$, the [fast Fourier transform](/fast-fourier-transform/) computes the $k$-fold sumset in $O(n + kU \log(kU))$ time.
- **Odd $k$, 2026.** Chan, Itakura, Ma and Yu (arXiv:2610.42012, not yet refereed) give a randomized algorithm for integer $k$-SUM with time $O(n^{\lceil k/2 \rceil - \varepsilon_k})$ for every odd constant $k$, where $\varepsilon_k > 0$ is a constant. For $k = 3$ their bound is $O(n^{1.965})$.

For $k = 3$, Alman and Vassilevska Williams (arXiv:2610.06783) also give a deterministic $O(n^{1.9992})$ algorithm. Their paper states that it does not handle $k \ge 4$.

## Bounds

- **Unconditional, $k$-linear decision trees.** Erickson (SODA 1995, Chicago J. Theor. Comput. Sci. 1999) proved $\Omega(n^{\lceil k/2 \rceil})$ depth for linear decision trees in which each query is the sign of an affine combination of at most $k$ inputs. So in that model meet in the middle is optimal.
- **Unconditional, general linear decision trees.** Kane, Lovett and Moran (STOC 2018, JACM 2019) solve $k$-SUM for every constant $k$ with $O(n \log^2 n)$ linear queries, each of which compares the sums of two $k$-element subsets. So no bound above $n \log^2 n$ can be proved in that model, and Erickson's bound depends on the limit of $k$ inputs per query.
- **Conditional on ETH, for growing $k$.** Pătraşcu and Williams (SODA 2010) showed that an $n^{o(k)}$ algorithm for $k$-SUM would refute the exponential time hypothesis, which says that 3-SAT on $N$ variables has no $2^{o(N)}$ algorithm. This bound is about the dependence on $k$ and allows any constant in the exponent. It is not affected by the 2026 algorithms, which save only a constant $\varepsilon_k$ in the exponent. See [k-SAT](/k-sat/) and [SETH](/strong-exponential-time-hypothesis/).
- **Conditional, fixed $k$.** The $k$-SUM hypothesis below is refuted for odd $k$ and open for even $k \ge 4$.

### Hypothesis (k-SUM)

For every $k \ge 3$ and every $\varepsilon > 0$, $k$-SUM on $n$ integers in $\{-n^{c}, \ldots, n^{c}\}$ has no $O(n^{\lceil k/2 \rceil - \varepsilon})$ algorithm on the word RAM. The constant $c$ depends on $k$, and sources differ in its value. Randomized algorithms are excluded.

Status: refuted for every odd $k$ by Chan, Itakura, Ma and Yu (arXiv:2610.42012), with a randomized algorithm, if the preprint is correct. Open for every even $k \ge 4$.

## Reductions

- **From $k$-SUM to $(k+1)$-SUM.** Deterministic, one call of size $n + 1$, linear time. Let $M > (k+1) \max |x|$. Add $M$ to every element and put $-kM$ into the set. A sum of $k+1$ distinct elements without $-kM$ is at least $(k+1)M - (k+1)\max|x| > 0$. A sum with $-kM$ and $k$ other elements is $kM + (x_1 + \cdots + x_k) - kM$, which is zero exactly when the $k$ original elements sum to zero. With $a(n) = n^{\lceil k/2 \rceil}$ and $b(n) = n^{\lceil (k+1)/2 \rceil}$, this transfers a saving only when the two exponents are equal, that is, from odd $k$ to $k + 1$. So a refutation for even $k+1$ would also refute odd $k$, but not the other way.
- **From $k$-SAT to $k$-SUM** (Pătraşcu and Williams 2010). Deterministic. The variables are split into groups, and each group gives a list of numbers that encode its partial assignments, so the number of numbers is exponential in the number of variables over the number of groups. It is not a fine-grained reduction for a fixed $k$: it gives the ETH bound above, about the growth in $k$.
- **From $k$-clique to $k$-SUM with $O(k^2)$ terms** (Downey and Fellows). Deterministic and polynomial. It shows W[1]-hardness, not a fine-grained bound for a fixed $k$.
- **From 3SUM to many problems.** See [3SUM-hardness](/3sum-hardness/).

## Applications

- **Cryptanalysis and subset sum.** The $k$-list form with large $k$ is the generalized birthday problem. Meet-in-the-middle methods for $k$-SUM give the [Horowitz-Sahni](/horowitz-sahni-algorithm/) and [Schroeppel-Shamir](/schroeppel-shamir-algorithm/) algorithms, and the same idea underlies the [meet-in-the-middle attack](/meet-in-the-middle-attack/).
- **Fine-grained hardness.** The $k$-SUM hypothesis was used for conditional lower bounds in the same way as the [3SUM conjecture](/3sum-conjecture/). After 2026, the bounds that used odd $k$ lose their base, and the bounds that used even $k$ stand.
- **Parameterized complexity.** $k$-SUM is a standard W[1]-hard problem, and the ETH bound of Pătraşcu and Williams is a standard source of $n^{\Omega(k)}$ lower bounds.

## References
