---
tag: 1M0VSG
kind: concept
slug: conditional-lower-bound
name: Conditional lower bound
aliases:
- hardness under a hypothesis
area: complexity/fine-grained-complexity
level: core
summary: "A statement that a problem has no algorithm faster than some bound unless a stated hypothesis, such as SETH, the 3SUM conjecture or P != NP, fails. It is proved by a reduction."
prereqs: [lower-bound, reduction-lower-bound]
see_also: [fine-grained-reduction, strong-exponential-time-hypothesis, orthogonal-vectors-hypothesis, 3sum-conjecture, apsp-conjecture, omv-conjecture, quadratic-time-hardness, fine-grained-equivalence-class]
sources:
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the sections on the main hypotheses (SETH, 3SUM, APSP and others) and the problems that are hard under each
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010)"
    locator: the definition of subcubic reductions and the equivalence of APSP with negative triangle detection
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995, 165-185"
    locator: the definition of 3SUM-hard problems and the reductions between them
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the reduction from CNF-SAT to orthogonal vectors
  - paper: doi:10.1145/2488608.2488673
    title: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515-524"
    locator: the conditional lower bound for approximating the diameter of sparse graphs
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma and reductions that preserve subexponential time
  - paper: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, Proceedings of the 47th ACM Symposium on Theory of Computing (STOC 2015)"
    locator: the statement of the OMv conjecture and the conditional bounds for dynamic problems
  - paper: doi:10.1145/2840728.2840746
    title: "Marco L. Carmosino, Jiawei Gao, Russell Impagliazzo, Ivan Mihajlin, Ramamohan Paturi and Stefan Schneider, Nondeterministic extensions of the strong exponential time hypothesis and consequences for non-reducibility, ITCS 2016, 261-270"
    locator: NSETH and the limits of deterministic reductions from SAT
  - paper: doi:10.1145/321921.321923
    title: "C. K. Wong and Ashok K. Chandra, Bounds for the string editing problem, Journal of the ACM 23(1), 1976, 13-16"
    locator: the unconditional lower bound for edit distance with equality tests only
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract (integer 3SUM in deterministic O(n^1.9992) time), Theorem 2 (APSP in deterministic O(n^2.9995) time) and the introduction (the list of affected hypotheses; SETH, OV and plain OMv are not affected); not yet refereed
  - paper: arxiv:2610.42012
    title: "Timothy M. Chan, Reina Itakura, Zhiyuan Ma and Yuancheng Yu, 3SUM made simpler (without matrix multiplication), k-SUM hypothesis refuted for odd k, and real 3SUM/APSP derandomized, arXiv preprint, October 2026"
    locator: the abstract (a randomized O(n^1.965) integer 3SUM algorithm); not yet refereed
---

A conditional lower bound says that a problem has no algorithm faster than a given bound unless a stated hypothesis fails. The proof is a reduction: a fast algorithm for the problem would give a fast algorithm for the problem in the hypothesis, such as $k$-SAT in the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/). It does not prove that the problem needs that time. It proves that a faster algorithm would also break a hypothesis that many researchers have tried and failed to break.

This page is about the kind of statement and how to read it. The tool that proves it is a [fine-grained reduction](/fine-grained-reduction/). Reductions in both directions give a [fine-grained equivalence class](/fine-grained-equivalence-class/). The bounds of order $n^2$ are collected on [quadratic-time hardness](/quadratic-time-hardness/).

## In plain words

Proving that a problem truly needs a lot of time is very hard. For most everyday problems, nobody can prove that they need more time than it takes to read the input.

So researchers pick a few famous problems that nobody has solved quickly in decades, and they assume that these really are hard. Then they show that a fast method for a new problem would give a fast method for one of the famous ones. If you believe the famous problem is hard, you must believe the new one is hard too.

The oldest example is NP-hardness, which rests on the belief that P is not NP. Fine-grained complexity does the same for exact running times, such as square time or cube time.

## The idea

### The form of the statement

A conditional lower bound has three parts:

1. **A hypothesis** about a source problem $A$: no algorithm solves $A$ in time $O(a(n)^{1-\varepsilon})$ for any $\varepsilon > 0$, in a stated model.
2. **A reduction** from $A$ to the target problem $B$, which turns a $b(n)^{1-\delta}$ algorithm for $B$ into an $a(n)^{1-\varepsilon}$ algorithm for $A$.
3. **The conclusion:** conditional on the hypothesis, $B$ has no $O(b(n)^{1-\delta})$ algorithm for any $\delta > 0$.

For quadratic problems the conclusion reads "no $O(n^{2-\delta})$ algorithm for any $\delta > 0$". This is not "no $o(n^2)$ algorithm": savings by factors such as $\log n$ are allowed, and some quadratic problems have them. The model is the [word RAM](/word-ram/) with words of $O(\log n)$ bits unless the hypothesis names another model. Each statement must say whether randomized algorithms are excluded; this depends on whether the hypothesis excludes them and whether the reduction is randomized.

Every result on a page about fine-grained complexity is either **unconditional** (the reduction itself, an algorithm, a bound in a restricted model) or **conditional on** a named hypothesis.

### The main hypotheses

| Hypothesis | Source problem | Conjectured time | Typical targets |
|---|---|---|---|
| $\mathsf{P} \ne \mathsf{NP}$ | SAT | not polynomial | [NP-hard](/np-hard/) problems |
| ETH | 3-SAT on $n$ variables | $2^{\Omega(n)}$ | exact exponential algorithms, $n^{o(k)}$ bounds |
| [SETH](/strong-exponential-time-hypothesis/) | $k$-SAT for large $k$ | $2^{(1-o(1)) n}$ | [Hitting Set](/hitting-set/), dominating set, through OV |
| [OVH](/orthogonal-vectors-hypothesis/) | [Orthogonal Vectors](/orthogonal-vectors/) | $n^{2-o(1)}$ | [edit distance](/edit-distance-seth-lower-bound/), [LCS](/lcs-seth-lower-bound/), diameter |
| [3SUM conjecture](/3sum-conjecture/) | [3SUM](/3sum/) on $n$ integers | $n^{2-o(1)}$ | [collinear points](/collinear-points/), geometry |
| [APSP conjecture](/apsp-conjecture/) | [all-pairs shortest paths](/all-pairs-shortest-paths/) | $n^{3-o(1)}$ | [negative triangle](/negative-triangle/), min-plus product |
| [OMv conjecture](/omv-conjecture/) | online matrix-vector products | $n^{3-o(1)}$ in total | [dynamic problems](/dynamic-lower-bounds/) |
| [set cover conjecture](/set-cover-conjecture/) | Set Cover on $n$ elements | $2^{(1-o(1)) n}$ | Steiner tree, set partitioning |

Some links between them are proved: SETH implies OVH ([Williams 2005](/seth-implies-ov-lower-bound/)), and SETH implies ETH. Others are open: the 3SUM conjecture is not known to follow from SETH, and the APSP conjecture is not known to follow from SETH or from 3SUM. So a lower bound under one hypothesis says nothing about the others, and a problem that is hard under all three is more convincing.

**Status in late 2026.** In October 2026, two preprints, both not yet refereed, refuted two rows of this table. Alman and Vassilevska Williams (arXiv:2610.06783) give integer 3SUM in deterministic time $O(n^{1.9992})$ and APSP in deterministic time $O(n^{2.9995})$. Chan, Itakura, Ma and Yu (arXiv:2610.42012) give integer 3SUM in randomized time $O(n^{1.965})$. If these preprints are correct, the bounds conditional on the 3SUM conjecture or on the APSP conjecture, such as the cubic bound for negative triangle below, no longer hold, although the reductions themselves stay valid. Alman and Vassilevska Williams state that SETH, OVH and the plain OMv conjecture are not affected.

### Why not prove the bounds outright

On the word RAM, no unconditional lower bound of the form $n^{1+\varepsilon}$ is known for OV, 3SUM, edit distance or APSP. Unconditional bounds exist only in restricted models: $\Omega(n \log n)$ comparisons for sorting, or the $\Omega(n^2)$ bound of Wong and Chandra for edit distance with equality tests only. A [lower bound by reduction](/reduction-lower-bound/) inside such a model is unconditional. A conditional lower bound trades the restriction on the model for an assumption.

There is also evidence that some hypotheses cannot be derived from others by simple reductions. Under NSETH, a nondeterministic form of SETH, 3SUM and APSP cannot be shown SETH-hard by deterministic fine-grained reductions (Carmosino et al. 2016).

### How to read one

- Check the **direction**: the reduction goes from the hard source problem to the target, not the other way.
- Check the **size blow-up**. A reduction from OV with $n$ vectors to a graph with $n^{1+o(1)}$ edges transfers an $n^{2}$ bound. A reduction to a graph with $n^2$ edges transfers nothing useful about quadratic time in the number of edges.
- Check the **quantifiers**. "For every $\varepsilon > 0$ there is a $c$" in OVH is not "for some fixed $c$".
- Check the **model**. A 3SUM bound for the real RAM does not transfer to the word RAM, and the reverse.
- Check the **parameter**. A bound for dense inputs says nothing about sparse inputs, and a bound for large distances says nothing about small ones.

## Examples

**Diameter, conditional on SETH.** From an OV instance with lists $A$ and $B$ of $n$ vectors in $\{0,1\}^d$, build a graph with a vertex for each vector, a vertex for each coordinate, and two vertices $x$ and $y$. Join a vector to the coordinates where it has a 1, join $x$ to all of $A$ and all coordinates, $y$ to all of $B$ and all coordinates, and $x$ to $y$. Then a vector of $A$ and a vector of $B$ are at distance 3 if they are orthogonal and 2 otherwise, and every other pair is at distance at most 2. For $A = \{10110, 01101, 11010\}$ and $B = \{01001, 10101, 00111\}$, the graph has 13 vertices and 34 edges, and breadth-first search from every vertex gives diameter 3, from the orthogonal pair $(10110, 01001)$. With $01011$ in place of $01001$, no pair is orthogonal, and the diameter is 2. The graph has $O(nd)$ edges, so an algorithm that tells diameter 2 from 3 in time $O(m^{2-\delta})$ on graphs with $m$ edges would refute OVH, and so SETH. In particular, no algorithm approximates the diameter of sparse graphs within a factor below $3/2$ in that time, conditional on SETH (Roditty and Vassilevska Williams 2013).

**Collinear points, conditional on 3SUM.** Map each integer $a$ to the point $(a, a^3)$. Three distinct integers sum to 0 if and only if their points lie on a line, so an $O(n^{2-\delta})$ algorithm for [three collinear points](/collinear-points/) refutes the 3SUM conjecture (Gajentaan and Overmars 1995). See [3SUM-hardness](/3sum-hardness/).

**Negative triangle, conditional on APSP.** Vassilevska Williams and Williams proved that APSP has a truly subcubic algorithm if and only if detecting a negative-weight triangle has one. So the APSP conjecture gives a cubic bound for [negative triangle](/negative-triangle/), and the reduction in the other direction shows the two are in one [equivalence class](/apsp-negative-triangle-equivalence/).

**Exponential bounds, conditional on ETH.** Standard reductions from 3-SAT to 3-coloring create $O(n + m)$ vertices. With the sparsification lemma, $m = O(n)$, so 3-coloring of a graph with $N$ vertices has no $2^{o(N)}$ algorithm, conditional on ETH.

## Where it is used

- To stop the search for an algorithm that probably does not exist, and to point to what is still open: approximation, special inputs, parameters such as a small distance or a small treewidth.
- To group problems: problems reduce to each other with small overhead and share a fate. See [fine-grained equivalence class](/fine-grained-equivalence-class/).
- To compare models: a conditional bound on the word RAM next to an unconditional bound in a restricted model shows which tricks a faster algorithm would need.
- In data structures and dynamic algorithms, where the OMv and 3SUM conjectures give bounds on update and query time; see [dynamic lower bounds](/dynamic-lower-bounds/).

## References
