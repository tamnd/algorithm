---
tag: C7JYMY
kind: concept
slug: 3sum-conjecture
name: 3SUM conjecture
aliases:
- 3SUM hypothesis
area: complexity/fine-grained-complexity
level: advanced
summary: "The hypothesis that 3SUM on n integers has no O(n^(2-e)) algorithm on the word RAM. Preprints from October 2026 refute it with an O(n^1.9992) algorithm."
prereqs: [3sum, word-ram, conditional-lower-bound]
see_also: [3sum, 3sum-hardness, k-sum, convolution-3sum, apsp-conjecture, orthogonal-vectors-hypothesis, zero-k-clique-hypothesis, dynamic-lower-bounds]
sources:
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry: Theory and Applications 5(3), 1995, 165-185"
    locator: the introduction, which poses the question whether 3SUM has a subquadratic algorithm, and the definition of 3SUM-hard problems
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on the 3SUM hypothesis, its integer and real forms, and the problems that are hard under it
  - paper: "Jeff Erickson, Lower bounds for linear satisfiability problems, Chicago Journal of Theoretical Computer Science 1999, article 8 (conference version in SODA 1995, 388-395)"
    locator: the Omega(n^2) bound for 3SUM in the 3-linear decision tree model
  - paper: doi:10.1145/3185378
    title: "Allan Grønlund and Seth Pettie, Threesomes, degenerates, and love triangles, Journal of the ACM 65(4), 2018, article 22 (conference version in FOCS 2014, 621-630)"
    locator: the abstract (the first subquadratic decision trees and the real RAM algorithms); the page relies on the journal version
  - paper: doi:10.1145/3285953
    title: "Daniel M. Kane, Shachar Lovett and Shay Moran, Near-optimal linear decision trees for k-SUM and related problems, Journal of the ACM 66(3), 2019, article 16 (conference version in STOC 2018)"
    locator: the abstract (O(n log^2 n) linear queries for 3SUM)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (the refutation of the 3SUM and APSP hypotheses, and the list of affected hypotheses); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract (a randomized O(n^1.965) integer algorithm and a deterministic truly subquadratic real algorithm); not yet refereed
  - paper: arxiv:2610.10153
    title: "Nick Fischer, Adam Polak and Jonas Schmidt, 3SUM is really hard: a real-to-integer reduction, arXiv preprint, October 2026, to appear in FOCS 2026"
    locator: the abstract (truly subquadratic integer 3SUM gives truly subquadratic real 3SUM)
---

The 3SUM conjecture, also called the 3SUM hypothesis, said that the [3SUM](/3sum/) problem has no algorithm that is faster than quadratic by a polynomial factor: for every $\varepsilon > 0$, there is no algorithm that decides whether $n$ integers contain three that sum to zero in time $O(n^{2-\varepsilon})$. Gajentaan and Overmars asked the question in 1995. Over the next thirty years it became one of the three main hypotheses of fine-grained complexity, beside [SETH](/strong-exponential-time-hypothesis/) and the [APSP conjecture](/apsp-conjecture/). Many [conditional lower bounds](/conditional-lower-bound/) used it, first in computational geometry and then for dynamic data structures, graph problems and strings.

In October 2026, Alman and Vassilevska Williams posted a preprint with a deterministic $O(n^{1.9992})$ algorithm for integer 3SUM and a randomized $O(n^{1.998})$ algorithm for real 3SUM. Later the same month, Chan, Itakura, Ma and Yu posted a simpler randomized $O(n^{1.965})$ algorithm for integers and a deterministic algorithm for reals. If these preprints are correct, the conjecture is false in both of its usual forms. This page states the conjecture as it was used, the evidence for it, and what the refutation changes.

The problem itself is on [3SUM](/3sum/). The problems that 3SUM reduces to are on [3SUM-hardness](/3sum-hardness/). The bounds proved from the conjecture stay valid as reductions; this page says what they now mean.

## In plain words

Picture a pile of whole numbers. Can three of them add up to zero? A simple method puts the numbers in order and then makes a number of steps that grows with the square of the pile size.

The conjecture was a bet that no method could beat the square by a real margin. Small savings did not count. A method that grows like the square divided by a slowly growing amount was fine. Only a method with a smaller power would break the bet.

Many people used the bet. They said: "if you could solve my problem fast, you could also solve this one fast, and we believe you cannot." In 2026, two research teams posted papers that claim to win against the bet by a very small power. So those other problems are no longer known to be hard.

## The idea

### Hypothesis (integer 3SUM)

For every $\varepsilon > 0$, no algorithm decides 3SUM on $n$ integers in $\{-n^{c}, \ldots, n^{c}\}$ in time $O(n^{2-\varepsilon})$.

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, so each input number fits in $O(1)$ words.
- The numbers are integers bounded by $n^{c}$ in absolute value for a constant $c$. Sources differ in the value of $c$. A smaller range is not hard: for numbers in $\{-U, \ldots, U\}$, the fast Fourier transform decides 3SUM in time $O(n + U \log U)$.
- Randomized algorithms with bounded error are excluded in the usual form, as in the survey of Vassilevska Williams (ICM 2018).

### Hypothesis (real 3SUM)

For every $\varepsilon > 0$, no algorithm decides 3SUM on $n$ real numbers in time $O(n^{2-\varepsilon})$.

- The model is the [real RAM](/real-ram/) with exact addition, subtraction, multiplication and comparison of reals at unit cost. Some statements use the [linear decision tree](/linear-decision-tree/) model, which counts only the sign tests of linear combinations of the inputs, and the decision tree results below show that the conjecture cannot hold in the general form of that model.
- Randomized algorithms are excluded too.

The two forms were not known to be related. An integer algorithm can use hashing and word packing, which a real RAM cannot do. Fischer, Polak and Schmidt (arXiv:2610.10153, to appear in FOCS 2026) showed that a truly subquadratic algorithm for integer 3SUM gives one for real 3SUM. This answered a question of Chan, Vassilevska Williams and Xu (STOC 2022).

### What counts as a refutation

The form "no $O(n^{2-\varepsilon})$ algorithm" is weaker than "no $o(n^2)$ algorithm". The conjecture allowed savings by any polylogarithmic factor, and indeed:

- Baran, Demaine and Pătraşcu (WADS 2005, Algorithmica 2008) gave a Las Vegas algorithm for integers on the word RAM in time $O(n^2 (\log \log n)^2 / \log^2 n)$.
- Grønlund and Pettie (FOCS 2014, JACM 2018) gave deterministic and randomized subquadratic algorithms for reals on the real RAM, with savings of a fractional power of $\log n$.
- Chan (SODA 2018, TALG 2020) gave a deterministic real RAM algorithm in time $(n^2 / \log^2 n)(\log \log n)^{O(1)}$.

None of these refuted the conjecture, since $n^2 / \log^2 n$ is not $O(n^{2-\varepsilon})$ for any $\varepsilon > 0$.

### Evidence before 2026

- **Failed attempts.** From 1995 to 2026, many groups tried to find a polynomial speedup and found only logarithmic ones.
- **Restricted lower bounds.** Erickson (SODA 1995, Chicago J. Theor. Comput. Sci. 1999) proved $\Omega(n^2)$ for linear decision trees in which each query tests the sign of an affine combination of at most 3 inputs. This is unconditional, but only for that model.
- **Decision trees beat the square.** Grønlund and Pettie gave linear decision trees of depth $O(n^{3/2} \sqrt{\log n})$, and Kane, Lovett and Moran gave linear decision trees with $O(n \log^2 n)$ queries, each with at most 6 nonzero coefficients in $\{-1, 0, 1\}$. So a quadratic lower bound could never be proved in the general linear decision tree model, and the conjecture was about uniform algorithms only. This was the first sign that the problem might be easier than it looked.

### Status in 2026

Alman and Vassilevska Williams (arXiv:2610.06783, 5 October 2026) give these results; the paper is not yet refereed:

- Integer 3SUM with numbers bounded by a polynomial in $n$, on the word RAM, in deterministic time $O(n^{1.9992})$. This is unconditional: it refutes the integer hypothesis, even in its deterministic form.
- Real 3SUM in expected time $O(n^{1.998})$, Las Vegas, with only comparisons, additions and subtractions on the reals. This refutes the real hypothesis.
- The core tool is a fast algorithm for the product of thin matrices when only a chosen set of entries is needed. It is a variant of Coppersmith's rectangular matrix multiplication. In graph terms, it finds the triangles through every edge of a sparse lopsided tripartite graph in truly subquadratic time.
- The same tool gives truly subcubic algorithms for APSP and for exact triangle, and so it also refutes the [APSP conjecture](/apsp-conjecture/) and the exact triangle and zero-weight $k$-clique hypotheses.

The paper states that Claude, an AI model made by Anthropic, discovered the algorithm, and that Claude also verified the main results in the Lean 4 proof assistant with the Mathlib library.

Chan, Itakura, Ma and Yu (arXiv:2610.42012, 30 October 2026) give a randomized $O(n^{1.965})$ algorithm for integer 3SUM that uses no fast matrix multiplication. It is based on variants of subset convolution and the zeta transform. They also derandomize real 3SUM and real APSP, and refute the [k-SUM](/k-sum/) hypothesis for every odd $k$. Karingula and Lovett (arXiv:2610.15663) give a simpler proof of a polynomial improvement with a weaker exponent.

What stays open:

- The true exponent of 3SUM. No lower bound of the form $n^{1 + \delta}$ is known in any general model.
- Most geometric problems that were [3SUM-hard](/3sum-hardness/). The reductions go from 3SUM to them, so a fast 3SUM algorithm does not make them fast. Alman and Vassilevska Williams write that it is now open whether three collinear points can be found in truly subquadratic time.
- $k$-SUM for even $k \ge 4$.

### Relation to the other hypotheses

- **SETH.** The 3SUM conjecture was not known to follow from [SETH](/strong-exponential-time-hypothesis/), and no reduction is known in either direction between 3SUM and [Orthogonal Vectors](/orthogonal-vectors/). The 2026 algorithms do not affect SETH or the [OV hypothesis](/orthogonal-vectors-hypothesis/).
- **APSP.** No reduction was known between 3SUM and APSP. Both reduce to the exact (zero-weight) triangle problem, so the hypothesis that exact triangle needs $n^{3 - o(1)}$ time was weaker than both; see [zero-k-clique hypothesis](/zero-k-clique-hypothesis/). The 2026 algorithm refutes all three.
- **Min-plus convolution.** A truly subquadratic algorithm for 3SUM gives one for the decision form of [min-plus convolution](/min-plus-convolution/) (Cygan, Mucha, Węgrzycki and Włodarczyk 2019). So the 3SUM conjecture was the stronger assumption of the two.
- **OMv.** The plain [OMv conjecture](/omv-conjecture/) is independent of 3SUM and is not affected.

### Pitfalls

- A conditional lower bound did not prove that a problem needs quadratic time. It said only that a fast algorithm would refute the conjecture. Now that the conjecture is refuted, the reduction still holds: a fast algorithm for the problem would give a fast 3SUM algorithm, which is no longer a contradiction.
- The refutation does not make the 3SUM-hard problems fast. It makes them no longer known to be hard.
- The integer and real forms are separate statements, and so is the range of the integers. Say which one a result uses.
- The 2026 results are preprints. Until they are refereed, name the preprint when you say that the conjecture is refuted.

## Examples

**How small the gain is.** The exponent $1.9992$ beats 2 by $0.0008$. For $n = 10^6$ the factor $n^{0.0008}$ is about $1.011$, and for $n = 10^9$ it is about $1.017$. It reaches 2 only at $n = 2^{1250}$. The $O(n^{1.965})$ algorithm saves $n^{0.035}$, about $1.62$ for $n = 10^6$ and about $2.07$ for $n = 10^9$, before the constant factors. These are results about the exponent, not about practical speed.

**Why log factors did not count.** Chan's bound saves a factor of about $\log^2 n$. A saving of $n^{0.1}$ is larger than a saving of $\log_2^2 n$ only when $n$ is above about $2^{143}$; at $n = 2^{64}$, $n^{0.1}$ is about 84 and $\log_2^2 n$ is 4096. So for every practical $n$, the log-factor algorithms save more than an $n^{0.1}$ algorithm would. The conjecture still allowed them, because in the limit any polynomial factor wins.

**What a conditional bound now says.** Gajentaan and Overmars showed that 3SUM reduces in linear time to deciding whether $n$ points in the plane contain three on a line, by $a \mapsto (a, a^3)$. Before 2026 this gave: three collinear points has no $O(n^{2-\varepsilon})$ algorithm, conditional on the 3SUM conjecture. Now the reduction gives only: an $O(n^{2-\varepsilon})$ algorithm for collinear points gives an $O(n^{2-\varepsilon})$ algorithm for 3SUM. Since 3SUM has an $O(n^{1.9992})$ algorithm, this tells nothing about collinear points, and its exponent is open. See [collinear points](/collinear-points/).

## Where it is used

- **[3SUM-hardness](/3sum-hardness/).** Gajentaan and Overmars defined the class of problems that 3SUM reduces to in subquadratic time. The geometric members include three collinear points, separating line segments by a line, and covering a triangle with triangles.
- **[Dynamic lower bounds](/dynamic-lower-bounds/).** Pătraşcu (STOC 2010) used the conjecture, through [Convolution 3SUM](/convolution-3sum/), to prove polynomial lower bounds for dynamic problems. Abboud and Vassilevska Williams (FOCS 2014) and Kopelowitz, Pettie and Porat (SODA 2016) proved more. These bounds now lose their base hypothesis, unless they also follow from the [OMv conjecture](/omv-conjecture/) or SETH.
- **[k-SUM](/k-sum/).** The $k$-SUM hypothesis generalizes the conjecture to $k$ terms. Its odd cases are refuted, and its even cases are open.
- **[Fine-grained equivalence classes](/fine-grained-equivalence-class/).** 3SUM and Convolution 3SUM are subquadratically equivalent, so the refutation covers both at once.

## References
