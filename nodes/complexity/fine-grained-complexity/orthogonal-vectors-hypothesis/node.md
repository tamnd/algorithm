---
tag: VRNB8T
kind: concept
slug: orthogonal-vectors-hypothesis
name: Orthogonal Vectors Hypothesis
aliases:
- OV hypothesis
- OV conjecture
area: complexity/fine-grained-complexity
level: advanced
summary: "The hypothesis that for every e > 0 there is a c such that Orthogonal Vectors with n vectors of dimension c log n has no O(n^(2-e)) algorithm. SETH implies it."
prereqs: [strong-exponential-time-hypothesis, orthogonal-vectors]
see_also: [seth-implies-ov-lower-bound, quadratic-time-hardness, conditional-lower-bound, fine-grained-reduction, edit-distance-seth-lower-bound, lcs-seth-lower-bound, 3sum-conjecture, apsp-conjecture]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: the section on cooperative subset queries and orthogonal vectors (CNF-SAT in time 2^((1-e/2)n) from a k^(2-e) algorithm for the subset query problem)
  - paper: "Amir Abboud, Ryan Williams and Huacheng Yu, More applications of the polynomial method to algorithm design, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015), 218-230"
    locator: the randomized algorithm for orthogonal vectors with d = c log n in time n^(2 - 1/O(log c))
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma, which gives the low-dimension form
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the statement of the OV hypothesis, its relation to SETH, and the problems that are hard under it
  - paper: arxiv:1501.07053
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 59-78"
    locator: the lower bounds for LCS and dynamic time warping, stated from orthogonal vectors
---

The Orthogonal Vectors Hypothesis (OVH) says that the [Orthogonal Vectors](/orthogonal-vectors/) problem needs essentially quadratic time once the dimension is a large enough multiple of $\log n$. It follows from the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) (SETH), but it is not known to imply SETH, so it is a weaker and safer assumption. Most quadratic [conditional lower bounds](/conditional-lower-bound/) are proved by a reduction from OV, and so they hold under OVH and not only under SETH.

The problem itself, with its algorithms, is on [orthogonal vectors](/orthogonal-vectors/). The proof that SETH implies OVH is on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).

## In plain words

Take two long lists of yes-or-no answer sheets. You want a pair, one sheet from each list, with no question where both sheets say yes. Checking all pairs works. The hypothesis says that nothing works much better, as long as each sheet has a moderate number of questions.

The number of questions must be large enough. With very few questions, a table of all possible sheets gives a fast method. So the claim is only for sheets with more questions than a fixed multiple of the number of digits in the list size.

If someone found a much faster method, they would also break SETH, and with it a long line of failed attempts to solve logic formulas faster.

## The idea

### Hypothesis (OVH, low-dimension form)

For every $\varepsilon > 0$ there is a constant $c$ such that no algorithm decides OV with $n$ vectors per list and dimension $d = c \log n$ in time $O(n^{2-\varepsilon})$.

- The model is the [word RAM](/word-ram/) with words of $O(\log n)$ bits.
- The numbers: $n$ is the number of vectors in each list, and $d$ is their dimension. The vectors are 0-1 vectors, so the input has $\Theta(n \log n)$ bits.
- Randomized algorithms with bounded error are excluded too, in the usual form. That form follows from the randomized form of SETH.

### Hypothesis (OVH, moderate-dimension form)

For every $\varepsilon > 0$, no algorithm decides OV with $n$ vectors per list and dimension $d$ in time $O(n^{2-\varepsilon}\,\mathrm{poly}(d))$.

The low-dimension form implies this one: an $O(n^{2-\varepsilon} d^{t})$ algorithm runs in time $O(n^{2 - \varepsilon/2})$ when $d = c \log n$, for every constant $c$. Both forms follow from SETH. The moderate form follows even from the weaker CNF-SETH, by Williams' reduction without sparsification. The low-dimension form needs the sparsification lemma, which makes the number of clauses, and so the dimension, linear in the number of variables.

### Why the dimension must grow

The constant $c$ depends on $\varepsilon$. It cannot be fixed in advance:

- The [sum over subsets](/sum-over-subsets/) table solves OV in time $O(2^d d + nd)$. For $d = c \log_2 n$ with $c < 2$, this is $O(n^{c} \log n)$, which is subquadratic.
- For every fixed $c$, Abboud, Williams and Yu (2015) solve OV with $d = c \log n$ in time $n^{2 - 1/O(\log c)}$, randomized.

So for every fixed $c$ the exponent is below 2, and a bound of the form "no $O(n^{2-\varepsilon})$ algorithm for every $\varepsilon > 0$" can hold only when $d = \omega(\log n)$. OVH says that this is the only obstacle: as $c$ grows, the saving tends to 0.

### Relation to the other hypotheses

- **SETH implies OVH** (Williams 2005). Split the $N$ variables of a CNF formula into two halves, and make one vector for each assignment of each half, with one coordinate per clause. A pair is orthogonal if and only if the two half assignments together satisfy every clause. An $O(n^{2-\varepsilon})$ algorithm for OV, with $n = 2^{N/2}$, would decide CNF-SAT in time $2^{(1-\varepsilon/2) N} \mathrm{poly}(N)$. The full proof is on [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).
- **The converse is open.** No reduction from $k$-SAT to OV in the other direction is known. A fast OV algorithm would refute SETH, but SETH could fail while OVH still holds.
- **Other hypotheses.** OVH is not known to imply, or to follow from, the [3SUM conjecture](/3sum-conjecture/) or the [APSP conjecture](/apsp-conjecture/). The three are the main independent sources of [fine-grained equivalence classes](/fine-grained-equivalence-class/) and conditional bounds.

## Examples

**Where the easy range ends.** Take $n = 2^{20}$ vectors per list. All pairs cost about $n^2 d$ basic steps, and the subset table about $2^d d + nd$:

| $d$ | $c = d / \log_2 n$ | subset table $2^d d + nd$ | all pairs $n^2 d$ |
|---|---|---|---|
| 20 | 1 | 41,943,040 | 21,990,232,555,520 |
| 40 | 2 | 43,980,507,054,080 | 43,980,465,111,040 |
| 60 | 3 | 69,175,290,276,473,733,120 | 65,970,697,666,560 |

At $c = 1$ the table wins by a factor of about 500,000. At $c = 2$ the two are about equal. At $c = 3$ the table is a million times worse. OVH is a claim about the rows below $c = 2$ and beyond: there, no method is known that gains a polynomial factor for all $c$.

**What a refutation would give.** Suppose OV with $d = c \log n$ had an $O(n^{1.9})$ algorithm for every constant $c$. Then CNF-SAT with $N$ variables and $O(N)$ clauses would be solvable in time $2^{0.95 N} \mathrm{poly}(N)$, by the split into halves. With sparsification, $k$-SAT would then have an algorithm with time $2^{0.96 N} \mathrm{poly}(N)$ for every $k$ (sparsify with $\varepsilon = 0.01$ and solve each of the $2^{0.01 N}$ parts), and SETH would fail.

**A conditional bound that uses only OVH.** The reduction from OV to edit distance in [edit distance SETH lower bound](/edit-distance-seth-lower-bound/) takes time $O(nd)$ and makes strings of length $O(nd)$. With $d = c \log n$, an edit distance algorithm with time $O(N^{2-\delta})$ would solve OV in time $O((n \log n)^{2-\delta})$, which is $O(n^{2 - \delta/2})$, for every $c$. So the edit distance bound holds under OVH alone.

## Where it is used

- As the source hypothesis of the quadratic lower bounds for [edit distance](/edit-distance-seth-lower-bound/), [LCS](/lcs-seth-lower-bound/), [Fréchet distance](/frechet-distance/), [regular expression matching](/backurs-indyk-regex-hardness/), approximate graph diameter and many more; see [quadratic-time hardness](/quadratic-time-hardness/). Papers often state these bounds "under SETH", but the proofs go through OV.
- For bounds on [dynamic problems](/dynamic-lower-bounds/) and on data structures, through unbalanced forms of OV.
- As a test for new algorithmic ideas: a method that solves OV in time $n^{2-\varepsilon}$ for $d = \omega(\log n)$ would be a major result, so such claims need very careful checking.

## References
