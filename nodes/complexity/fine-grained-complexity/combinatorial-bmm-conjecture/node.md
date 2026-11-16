---
tag: 6JQS28
kind: concept
slug: combinatorial-bmm-conjecture
name: Combinatorial Boolean matrix multiplication conjecture
aliases:
- BMM conjecture
- boolean matrix multiplication hypothesis
area: complexity/fine-grained-complexity
level: research
summary: "The conjecture that no combinatorial algorithm multiplies two n by n Boolean matrices in O(n^(3-e)) time. The term has no formal definition. It is still open in 2026."
prereqs: [boolean-matrix-multiplication, four-russians-method, conditional-lower-bound]
see_also: [triangle-detection-hypothesis, omv-conjecture, apsp-conjecture, valiant-lee-theorem, matrix-multiplication-exponent, dynamic-lower-bounds, fine-grained-reduction, min-weight-k-clique-hypothesis]
sources:
  - paper: doi:10.1109/FOCS.2014.53
    title: "Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, FOCS 2014, 434-443"
    locator: "Conjecture 5 (No truly subcubic combinatorial BMM), written with quotes, and footnote 2 (the notion of a combinatorial algorithm is not well defined); the summary of results (bounds for Pagh's problem from Conjecture 5)"
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the subcubic equivalence of Boolean matrix multiplication and triangle detection for combinatorial algorithms
  - paper: doi:10.1145/3618260.3649696
    title: "Amir Abboud, Nick Fischer, Zander Kelley, Shachar Lovett and Raghu Meka, New graph decompositions and combinatorial Boolean matrix multiplication algorithms, STOC 2024, 935-943 (arXiv:2311.09095)"
    locator: the abstract and the main theorem (combinatorial BMM in n^3 / 2^(Omega((log n)^(1/7))) time)
  - paper: doi:10.1145/505241.505242
    title: "Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1), 2002, 1-15"
    locator: the main theorem (a fast parser gives fast Boolean matrix multiplication)
  - paper: doi:10.1109/FOCS.2015.16
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, FOCS 2015, 98-117 (journal version in SIAM Journal on Computing 47(6), 2018, 2527-2555)"
    locator: the abstract (parsing lower bounds for combinatorial algorithms and for fast matrix multiplication, from k-clique)
  - paper: arxiv:1511.06773
    title: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015, 21-30"
    locator: Section 1.2 (OMv and combinatorial BMM, and the reading of combinatorial as not Strassen-like)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: "the paragraph Combinatorial algorithms in the introduction (the new algorithms are algebraic; no truly subcubic combinatorial BMM algorithm is known; the refuted hypotheses could be restated for combinatorial algorithms); not yet refereed"
---

The combinatorial BMM conjecture says that no combinatorial algorithm computes the product of two $n \times n$ [Boolean matrices](/boolean-matrix-multiplication/) in time $O(n^{3-\varepsilon})$ for any $\varepsilon > 0$. Algebraic algorithms are much faster: Boolean matrix multiplication takes time $O(n^{\omega})$ with $\omega < 2.371552$. So the conjecture is a statement about one kind of method, and "combinatorial" has no formal definition. Abboud and Vassilevska Williams wrote it as a "Conjecture" in quotes for this reason.

In October 2026, preprints refuted the 3SUM conjecture, the APSP conjecture, and the zero-weight and min-weight k-clique hypotheses. Their algorithms are algebraic. Alman and Vassilevska Williams state that no truly subcubic combinatorial algorithm for BMM is known, and they suggest that the refuted hypotheses could be restated for combinatorial algorithms. So in late 2026 the combinatorial BMM conjecture still stands, and it may become more important.

## In plain words

Take two square grids of yes and no marks. The product grid has a yes at a spot when some row of the first grid and some column of the second grid share a yes. The plain method checks every row, column and middle position, which is a cube of work.

Clever algebra does the job much faster, but it uses tricks with numbers that cancel each other. The conjecture is a bet that every method without such tricks, one that only looks at the marks and groups them, stays close to the cube.

Nobody can say exactly which methods count as "without tricks", so the bet is not a precise statement. It is still useful, because many reductions between problems use only simple steps of this kind.

## The idea

### Hypothesis (combinatorial BMM)

For every constant $\varepsilon > 0$, no combinatorial algorithm computes the Boolean product $C = A B$ of two $n \times n$ Boolean matrices, with $C[i,k] = \bigvee_j (A[i,j] \wedge B[j,k])$, in expected time $O(n^{3-\varepsilon})$ (Abboud and Vassilevska Williams, FOCS 2014, "Conjecture" 5).

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits.
- The numbers are bits. The input is $2n^2$ bits and the output is $n^2$ bits.
- Randomized algorithms are excluded too: the bound is on the expected time.
- The algorithm must be combinatorial. This word has no formal definition (footnote 2 of the FOCS 2014 paper). It usually means an algorithm that does not use the algebraic structure of a ring, such as subtraction that cancels terms, as [Strassen's algorithm](/strassen-algorithm/) does. Henzinger, Krinninger, Nanongkai and Saranurak suggest one formal reading: "not Strassen-like" in the sense of Ballard et al.

### Without the restriction

Over the integers, $C[i,k] = 1$ exactly when the integer product has $(AB)[i,k] > 0$. So BMM takes time $O(n^{\omega})$ for every $\omega$ above the [matrix multiplication exponent](/matrix-multiplication-exponent/), and $O(n^{2.371552})$ is truly subcubic. This bound is unconditional. Without the word "combinatorial", the conjecture is false.

### Evidence

All bounds here are unconditional upper bounds for combinatorial algorithms.

- **Four Russians.** Arlazarov, Dinic, Kronrod and Faradzev (1970) split the matrices into blocks of about $\log n$ columns and precompute all the unions inside a block. On the word RAM this gives time $O(n^3 / \log^2 n)$. See [Four Russians method](/four-russians-method/).
- **Polylogarithmic savings.** Bansal and Williams (2009), Chan (2015) and Yu (2018) save further polylogarithmic factors, up to about $\log^4 n$.
- **More than any polylogarithm.** Abboud, Fischer, Kelley, Lovett and Meka (STOC 2024) give time $n^3 / 2^{\Omega((\log n)^{1/7})}$. This beats every polylogarithmic factor, but it is not $O(n^{3-\varepsilon})$ for any $\varepsilon > 0$, so it does not refute the conjecture.

### Equivalent and related forms

- **Triangle detection.** Vassilevska Williams and Williams (FOCS 2010) show that, for combinatorial algorithms, BMM and triangle detection in $n$-vertex graphs are subcubic equivalent: a truly subcubic combinatorial algorithm for one gives one for the other. One direction is easy: a graph with adjacency matrix $A$ has a triangle if and only if some edge $(k, i)$ has $(A A)[i,k] = 1$. So the conjecture is often stated as "combinatorial triangle detection needs $n^{3-o(1)}$ time". See [triangle detection hypothesis](/triangle-detection-hypothesis/).
- **Online matrix-vector multiplication.** An OMv algorithm with total time $T(n)$ gives a BMM algorithm with the same time: feed the columns of $B$ one at a time. So the combinatorial BMM conjecture implies the [OMv conjecture](/omv-conjecture/) for combinatorial algorithms. The OMv conjecture itself allows all algorithms.
- **Parsing.** Lee (2002) shows that a fast parser for context-free grammars gives fast BMM. Abboud, Backurs and Vassilevska Williams (FOCS 2015) prove lower bounds for parsing with a fixed grammar from the k-clique problem, for combinatorial algorithms and for algorithms with fast matrix multiplication. See [Valiant and Lee theorem](/valiant-lee-theorem/).

### Status in 2026

- **The conjecture: open.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) write that their new algorithms are algebraic and that no truly subcubic combinatorial algorithm for BMM is known. The best combinatorial bound is still that of Abboud et al. (2024).
- **Its role grows.** The 3SUM conjecture, the APSP conjecture and the zero-weight and min-weight k-clique hypotheses are refuted, if the preprints are correct. Alman and Vassilevska Williams note that most fine-grained reductions are combinatorial, so one could restate these hypotheses for combinatorial algorithms, as was done earlier for BMM. A bound proved from such a restated hypothesis holds only against combinatorial algorithms.
- **What else stands.** SETH and the plain OMv conjecture are not affected by the preprints. The triangle detection hypothesis for sparse graphs is not affected either.

### Pitfalls

- A bound "conditional on combinatorial BMM" holds only against combinatorial algorithms. It says nothing about algorithms that use fast matrix multiplication, and for many problems those are faster.
- Since the term is informal, a new algorithm can be called combinatorial by some authors and not by others. A paper that uses the conjecture should say which steps of its reduction are combinatorial.
- $n^3 / 2^{\Omega((\log n)^{1/7})}$ is $n^{3 - o(1)}$. Faster than every polylogarithmic saving is not the same as truly subcubic.

## Examples

**A small product.** Take

$$A = \begin{pmatrix} 1&0&1&0 \\ 0&0&0&0 \\ 0&1&0&0 \\ 1&0&0&1 \end{pmatrix}, \quad B = \begin{pmatrix} 0&1&0&0 \\ 0&0&1&1 \\ 0&0&0&0 \\ 1&0&0&0 \end{pmatrix}.$$

The Boolean product is

$$C = \begin{pmatrix} 0&1&0&0 \\ 0&0&0&0 \\ 0&0&1&1 \\ 1&1&0&0 \end{pmatrix}$$

with five 1 entries. Each 1 has one witness $j$: entry $(0,1)$ has $j = 0$, entries $(2,2)$ and $(2,3)$ have $j = 1$, entry $(3,0)$ has $j = 3$, and entry $(3,1)$ has $j = 0$. In the tripartite graph with $I$ to $J$ edges from $A$, $J$ to $K$ edges from $B$ and all $K$ to $I$ edges, each witness is a triangle $(i, j, k)$. This is the link between BMM and triangle detection.

**How large the savings are.** The Four Russians saving $\log^2 n$ is $400$ at $n = 2^{20}$ and $4096$ at $n = 2^{64}$. With the constant in $\Omega$ taken as 1, the saving $2^{(\log_2 n)^{1/7}}$ of Abboud et al. is only $2.90$ at $n = 2^{20}$ and $3.51$ at $n = 2^{64}$. It overtakes $\log_2^2 n$ only when $\log_2 n$ is about $5.2 \times 10^{13}$. The new bound is better in the limit, not in practice, and neither is a polynomial saving.

## Where it is used

- **[Dynamic lower bounds](/dynamic-lower-bounds/).** Abboud and Vassilevska Williams prove that, under the conjecture, any combinatorial algorithm for Pagh's problem needs $k^{3/2-o(1)}$ preprocessing time or $k^{1/2-o(1)}$ update or query time. Many such bounds were later proved from the OMv conjecture for all algorithms.
- **Graph problems.** Bounds for combinatorial algorithms for triangle detection and the problems that are equivalent to it on dense graphs (Vassilevska Williams and Williams 2010).
- **Parsing.** Lower bounds for combinatorial context-free parsers, through Lee (2002) and Abboud et al. (2015).
- **After 2026.** A possible base for restated forms of the refuted hypotheses, for combinatorial algorithms only.

## References
