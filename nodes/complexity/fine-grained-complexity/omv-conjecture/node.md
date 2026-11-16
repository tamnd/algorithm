---
tag: 1DFYN5
kind: concept
slug: omv-conjecture
name: Online Matrix-Vector multiplication conjecture
aliases:
- OMv conjecture
area: complexity/fine-grained-complexity
level: research
summary: "The conjecture that online Boolean matrix-vector multiplication has no O(n^(3-e)) algorithm, even randomized. It gives tight dynamic lower bounds and is still open in 2026."
prereqs: [online-matrix-vector-multiplication, conditional-lower-bound, boolean-matrix-multiplication]
see_also: [online-matrix-vector-multiplication, dynamic-lower-bounds, combinatorial-bmm-conjecture, strong-exponential-time-hypothesis, 3sum-conjecture, apsp-conjecture, update-query-tradeoff, fine-grained-equivalence-class]
sources:
  - paper: arxiv:1511.06773
    title: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015, 21-30"
    locator: Conjecture 1.1, Section 1.2 (OMv and combinatorial BMM), Theorem 2.7, Corollary 2.8, Lemmas 2.10 and 2.11 and Theorem 2.12 of the arXiv version, which the page relies on
  - paper: arxiv:1605.01695
    title: "Kasper Green Larsen and R. Ryan Williams, Faster online matrix-vector multiplication, SODA 2017, 2182-2189"
    locator: the abstract (total time n^3/2^Omega(sqrt(log n)), and the cell probe upper bound)
  - paper: arxiv:1905.05067
    title: "Jan van den Brand, Danupon Nanongkai and Thatchaphol Saranurak, Dynamic matrix inverse: improved algorithms and matching conditional lower bounds, FOCS 2019"
    locator: the abstract and the section on the variants of the OMv conjecture used for the lower bounds
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the introduction (three hinted OMv conjectures refuted; plain OMv not affected; the affected dynamic bounds are at the end of the trade-off curves with the fastest queries); not yet refereed
---

The OMv conjecture says that [online matrix-vector multiplication](/online-matrix-vector-multiplication/) over the Boolean semiring has no truly subcubic algorithm: for every $\varepsilon > 0$, no algorithm, even a randomized one with error probability at most $1/3$, can multiply a fixed $n \times n$ Boolean matrix with $n$ vectors that arrive one at a time in total time $O(n^{3-\varepsilon})$. Henzinger, Krinninger, Nanongkai and Saranurak stated it in 2015. They showed that it gives tight, or better than before, lower bounds for a long list of dynamic problems, often by short reductions. It replaced several older hypotheses for this purpose.

In October 2026, preprints refuted the 3SUM conjecture, the APSP conjecture, and three hinted variants of the OMv conjecture. Alman and Vassilevska Williams state that plain OMv is not affected. So in late 2026, the OMv conjecture, together with SETH, is the main base for polynomial lower bounds on dynamic problems.

## In plain words

You get a big fixed grid of yes and no marks, and then a series of questions, each a list of marks. For each list, you must say which rows of the grid share a marked spot with it, before you see the next list.

The conjecture is a bet that no method can do this much faster than checking each row against each list, even if it first studies the grid for a long time and even if it may make a small error.

Many questions about networks that change over time contain this problem. If the bet is right, those questions cannot be answered fast either. In 2026, related bets fell, but this one still stands.

## The idea

### Hypothesis (OMv)

For every constant $\varepsilon > 0$, there is no $O(n^{3-\varepsilon})$-time algorithm that solves OMv with an error probability of at most $1/3$ (Henzinger et al., Conjecture 1.1).

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits.
- The numbers are bits: $M$ and the vectors are Boolean, and the product is over the Boolean semiring.
- Randomized algorithms with error probability at most $1/3$ are excluded too, so a bound proved from the conjecture holds against them.
- The time counts the preprocessing of $M$ and all $n$ rounds.

### Forms that follow from it

All of these are conditional on the hypothesis, and each is proved in Henzinger et al. by a deterministic reduction that extends to randomized algorithms:

- **Polynomial preprocessing.** No algorithm with polynomial preprocessing time and total time $\tilde{o}(n_1 n_2 n_3)$ for the rounds solves $\gamma$-OuMv, the form with an $n_1 \times n_2$ matrix, $n_1 = n_2^{\gamma}$, $n_3$ rounds, and one bit $u^{T} M v$ per round (Theorem 2.7). So studying the matrix for a long time does not help.
- **One query.** For uMv, the case $n_3 = 1$, no algorithm with polynomial preprocessing answers the one query in time $\tilde{o}(n_1 n_2)$ (Corollary 2.8).
- **Graph queries.** OuMv is equivalent to three query problems: independent set queries, 2-CNF queries and edge queries (Theorem 2.12). The matrix may also be taken symmetric (Theorem 2.13).

### Evidence

- **Algorithms.** The best algorithms save little. Williams (SODA 2007) gives $O(n^3 / \log^2 n)$ in total. Larsen and Williams (SODA 2017) give $n^3 / 2^{\Omega(\sqrt{\log n})}$, randomized. Neither is $O(n^{3-\varepsilon})$.
- **Combinatorial BMM.** Any OMv algorithm gives a [Boolean matrix multiplication](/boolean-matrix-multiplication/) algorithm with the same time: feed the columns of the second matrix one at a time. So the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/) implies the OMv conjecture for combinatorial algorithms. Henzinger et al. argue that it implies the full conjecture if "combinatorial" is read as "not Strassen-like" in the sense of Ballard et al., a class that contains all known fast matrix multiplication algorithms. Fast matrix multiplication does not obviously help, because the vectors come one at a time.
- **Algebraic lower bound.** Henzinger et al. cite an algebraic lower bound of Bläser as support.

### What it does not follow from, and what does not follow from it

- The OMv conjecture does not replace SETH. Henzinger et al. state that it can replace all the other conjectures used for dynamic bounds, but the bounds from SETH still need SETH. They do not reduce 3SUM or APSP to OMv either: for dynamic problems, OMv gives the same or better bounds by a separate reduction.
- The cell probe model cannot prove the conjecture: Larsen and Williams answer each vector with $O(n^{7/4} / \sqrt{w})$ cell probes. So an unconditional proof would need a model closer to the word RAM.

### Status in 2026

- **Plain OMv: open.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) state that their algorithm does not affect it.
- **Hinted OMv: refuted, if the preprint is correct.** Van den Brand, Nanongkai and Saranurak (FOCS 2019) used variants of OMv in which some information about the queries is given in advance, as a hint, to prove matching lower bounds for dynamic matrix inverse and related problems. Alman and Vassilevska Williams refute three of these hinted conjectures. They write that the affected dynamic bounds are those at the end of the update and query trade-off curves with the fastest queries.
- **Dynamic bounds.** Henzinger et al. showed that, for most earlier dynamic bounds from 3SUM, combinatorial BMM, triangle detection and the multiphase problem, the OMv conjecture gives the same or a stronger bound on the amortized time. So most of those bounds survive the fall of the 3SUM conjecture. See [dynamic lower bounds](/dynamic-lower-bounds/).

### Pitfalls

- OMv is about total time. A bound per operation from it is amortized unless the reduction says otherwise.
- The conjecture counts the preprocessing time, but Theorem 2.7 removes that limit. A bound stated "with polynomial preprocessing" is the stronger form, and a reduction must say which form it uses.
- "Hinted OMv" and "OMv" are different statements. Only the hinted forms are refuted.

## Examples

**Why $2^{\sqrt{\log n}}$ is not a polynomial saving.** Larsen and Williams save a factor $2^{\Omega(\sqrt{\log n})}$. For $\log_2 n = 64$, $2^{\sqrt{64}} = 256$, while $n^{0.01} = 2^{0.64} \approx 1.56$. For $\log_2 n = 100$, $2^{10} = 1024$ against $n^{0.01} = 2$. The two meet at $\log_2 n = 10000$, and beyond that $n^{0.01}$ is larger. In general $2^{\sqrt{\log_2 n}} = n^{\varepsilon}$ at $\log_2 n = 1/\varepsilon^2$. So the algorithm is fast in practice but does not refute the conjecture.

**Listing the witnesses.** The bound for OMv follows from the bound for OuMv because one OuMv bit per query is enough to find all of $M v$. Ask $u^{T} M v$ with $u$ the indicator of a set of rows, and halve the set while the answer is 1. Henzinger et al. (Lemma 2.10) list all $w$ rows with $(M v)_r = 1$ in $1 + O(w \log n)$ queries. For an $8 \times 8$ example with 4 such rows, the search uses 16 queries; see [online matrix-vector multiplication](/online-matrix-vector-multiplication/) for the matrix.

**A tight bound.** In subgraph connectivity, nodes are turned on and off, and a query asks whether $s$ and $t$ are connected through nodes that are on. From the conjecture, Henzinger et al. show that no algorithm has polynomial preprocessing, amortized update time $m^{\alpha - \varepsilon}$ and amortized query time $m^{1 - \alpha - \varepsilon}$, for any $0 \le \alpha \le 1$. With $\alpha = 2/3$ this matches the known algorithm with $\tilde{O}(m^{2/3})$ update and $\tilde{O}(m^{1/3})$ query time. This bound is conditional.

## Where it is used

- **[Dynamic lower bounds](/dynamic-lower-bounds/).** Reachability, shortest paths, subgraph connectivity, decremental single-source shortest paths, Pagh's problem, approximate diameter, densest subgraph, and more. Henzinger et al. state that OMv and SETH together give all the dynamic lower bounds known in 2015 with polynomial preprocessing.
- **Limits of techniques.** The conjecture shows that some approaches to minimum Steiner tree and minimum cut cannot be made faster.
- **[Update and query trade-offs](/update-query-tradeoff/).** Most OMv bounds are trade-offs: a faster update forces a slower query.
- **[Fine-grained equivalence classes](/fine-grained-equivalence-class/).** OMv, OuMv and the query problems of Theorem 2.12 form one class.

## References
