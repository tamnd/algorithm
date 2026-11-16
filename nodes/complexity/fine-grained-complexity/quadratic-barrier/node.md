---
tag: 2ZQENN
kind: concept
slug: quadratic-barrier
name: Quadratic barrier
aliases:
- quadratic-time barrier
- n^2 barrier
area: complexity/fine-grained-complexity
level: intro
summary: "Many problems on pairs, such as edit distance, LCS and orthogonal vectors, have a simple O(n^2) algorithm and no known O(n^(2-e)) one. SETH and the 3SUM conjecture explain why."
prereqs: [time-complexity, asymptotic-notation]
see_also: [quadratic-time-hardness, conditional-lower-bound, orthogonal-vectors-hypothesis, 3sum-conjecture, edit-distance, longest-common-subsequence, frechet-distance, four-russians-method]
sources:
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the survey of quadratic problems that are hard under SETH, OVH and the 3SUM conjecture
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the reduction from CNF-SAT to orthogonal vectors
  - paper: doi:10.1137/15M1053128
    title: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018 (conference version in STOC 2015)"
    locator: the main theorem, the quadratic lower bound for edit distance under SETH
  - paper: "Karl Bringmann, Why walking the dog takes time: Fréchet distance has no strongly subquadratic algorithms unless SETH fails, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014), 661-670"
    locator: the quadratic lower bound for the Fréchet distance under SETH
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995, 165-185"
    locator: the class of 3SUM-hard problems in geometry
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: "William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980, 18-31"
    locator: the O(n^2 / log n) algorithm for edit distance over a finite alphabet
  - paper: "Pankaj K. Agarwal, Rinat Ben Avraham, Haim Kaplan and Micha Sharir, Computing the discrete Fréchet distance in subquadratic time, SIAM Journal on Computing 43(2), 2014, 429-449"
    locator: the O(mn log log n / log n) algorithm for the discrete Fréchet distance on the word RAM
  - paper: "Amir Abboud, Ryan Williams and Huacheng Yu, More applications of the polynomial method to algorithm design, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015), 218-230"
    locator: the algorithm for orthogonal vectors with dimension c log n in time n^(2 - 1/O(log c))
  - paper: doi:10.1145/2488608.2488673
    title: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515-524"
    locator: the near 3/2 approximation of the diameter in subquadratic time for sparse graphs, and the matching conditional lower bound
  - paper: doi:10.1145/321921.321923
    title: "C. K. Wong and Ashok K. Chandra, Bounds for the string editing problem, Journal of the ACM 23(1), 1976, 13-16"
    locator: the unconditional quadratic lower bound for edit distance when the algorithm only tests symbols for equality
---

The quadratic barrier is the observation that many basic problems on pairs have a simple algorithm with time $O(n^2)$, and that no algorithm with time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$ is known, after decades of work. Examples are [edit distance](/edit-distance/), the [longest common subsequence](/longest-common-subsequence/), the [Fréchet distance](/frechet-distance/), [orthogonal vectors](/orthogonal-vectors/) and [3SUM](/3sum/). Fine-grained complexity explains most of the barrier: conditional on SETH or on the 3SUM conjecture, these problems truly need time $n^{2-o(1)}$.

This page is about the barrier itself: where the $n^2$ comes from, what counts as breaking it, and which kinds of algorithms get around it. The proofs and the list of hard problems are on [quadratic-time hardness](/quadratic-time-hardness/).

## In plain words

Many tasks compare everything with everything. To compare two texts letter by letter, the classic method fills a table with one cell for each pair of positions. To find two matching items in two lists, it checks each pair. When the input doubles, the work grows four times.

For many such tasks, nobody has found a method that grows clearly slower than that, even though many people have tried for decades. Small savings are known, but not a real change in the growth.

Researchers now believe that this wall is real. A clearly faster method for any one of these tasks would also give a clearly faster method for a famous logic puzzle that has resisted all attempts. So the wall for many tasks is really one wall.

## The idea

### Where the square comes from

The simple algorithms have one of a few shapes:

- **All pairs.** Orthogonal vectors checks every pair of an $A$ vector and a $B$ vector. Closest pair problems in high dimension do the same.
- **A table over two sequences.** Edit distance, LCS, dynamic time warping and the discrete Fréchet distance fill an $n \times n$ table, one cell per pair of positions, in $O(1)$ time per cell.
- **One linear pass per element.** 3SUM sorts the numbers and, for each number, scans the rest with two pointers. The diameter of a graph with $n$ vertices and $m$ edges runs breadth-first search from every vertex, in time $O(nm)$, which is quadratic when $m = O(n)$.

### Truly subquadratic and log factors

An algorithm is **truly subquadratic** (or strongly subquadratic) if it runs in time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$. Saving a factor $\log n$ or $\log^2 n$ does not break the barrier, and the conditional lower bounds do not rule it out. The two kinds of saving differ a lot:

| $n$ | $n^2$ | $n^2 / \log_2 n$ | $n^{1.9}$ | $n^{1.5}$ |
|---|---|---|---|---|
| $10^3$ | $10^6$ | $1.0 \times 10^5$ | $5.0 \times 10^5$ | $3.2 \times 10^4$ |
| $10^6$ | $10^{12}$ | $5.0 \times 10^{10}$ | $2.5 \times 10^{11}$ | $10^9$ |

At these sizes a saving of $\log_2 n$ beats a saving of $n^{0.1}$. For $n = 2^t$ the power saving wins only when $0.1\, t > \log_2 t$, which first holds at $t = 59$, that is, $n \approx 5.8 \times 10^{17}$. So the barrier is a statement about growth, not about practical speed. It still matters: a saving of $n^{0.5}$ would cut $10^{12}$ steps to $10^9$.

### What gets around the barrier

None of the following contradicts the hypotheses, and each is a real way to solve large instances.

- **Log factors.** The Four Russians method computes edit distance over a finite alphabet in time $O(n^2 / \log n)$ (Masek and Paterson 1980); see [Four Russians method](/four-russians-method/). The discrete Fréchet distance of curves with $m$ and $n$ points takes $O(mn \log \log n / \log n)$ time on the word RAM (Agarwal, Ben Avraham, Kaplan and Sharir 2014). 3SUM has similar savings; see the [3SUM conjecture](/3sum-conjecture/).
- **Small dimension.** Orthogonal vectors with dimension $d = c \log n$ takes time $n^{2 - 1/O(\log c)}$ (Abboud, Williams and Yu 2015). That is truly subquadratic for each fixed $c$, but the saving shrinks as $c$ grows, which is why the [OV hypothesis](/orthogonal-vectors-hypothesis/) quantifies over all $c$. With $d$ below $\log_2 n$ by a constant factor, a table over all $2^d$ vectors is faster still.
- **Small answers.** If the edit distance is at most $k$, only the cells within distance $k$ of the diagonal of the table matter, so $O(nk)$ cells suffice. The [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) uses the same idea for approximate matching.
- **Approximation.** Roditty and Vassilevska Williams (2013) estimate the diameter of a graph within a factor of about $3/2$ in time $\tilde{O}(m \sqrt{n})$, which is subquadratic for sparse graphs. Conditional on SETH, a factor below $3/2$ needs $m^{2-o(1)}$ time, so this is where the barrier moves.
- **Restricted models in the other direction.** In some models the barrier is a theorem: Wong and Chandra (1976) proved that edit distance needs $\Omega(n^2)$ equality tests when the algorithm may only test symbols for equality. Algorithms that look up tables, as the Four Russians method does, are outside that model.

### Why the hypotheses explain it

Each problem above has a fine-grained reduction from a problem that is believed hard. Williams (2005) reduced CNF-SAT to orthogonal vectors, so the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) implies the OV hypothesis. From OV there are reductions to edit distance (Backurs and Indyk 2015), to LCS and dynamic time warping (two papers of 2015; see the [LCS SETH lower bound](/lcs-seth-lower-bound/)), to the Fréchet distance (Bringmann 2014) and to the diameter of sparse graphs. For geometry, Gajentaan and Overmars (1995) reduced 3SUM to many problems, such as three collinear points. So a truly subquadratic algorithm for edit distance would give one for OV, then a $2^{(1-\delta) N}$ algorithm for CNF-SAT, which would refute SETH.

The 3SUM barrier and the OV barrier are separate: 3SUM is not known to follow from SETH, and OV is not known to follow from 3SUM. A problem may sit behind one barrier, the other, or both.

### What the barrier is not

- It is not a proved lower bound on the word RAM. For none of these problems is an unconditional bound of the form $n^{1+\varepsilon}$ known there.
- It does not say "no $o(n^2)$ algorithm". Log-factor savings exist.
- It is not NP-hardness. All these problems are in polynomial time; the question is the exponent.

## Examples

**A table over two strings.** Two DNA strings of lengths 2000 and 2004, the second made from the first by 30 random substitutions, insertions and deletions, have edit distance 25. The full table of the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) computes it in $2000 \times 2004 = 4{,}008{,}000$ cells. With the promise that the distance is at most $k = 50$, the band of cells within 50 of the diagonal gives the same answer in 199,644 cells, about 20 times fewer. With $k = 10$, the band uses 41,924 cells and reports that the distance is more than 10. The band works because the distance is small. For two random strings the distance grows with $n$, the band must cover the whole table, and the barrier is back.

**One barrier for many problems.** Suppose someone finds an edit distance algorithm with time $O(n^{1.99})$. Through the reduction of Backurs and Indyk, OV with $n$ vectors in dimension $c \log n$ would take time $n^{1.99 + o(1)}$ for every $c$. Through Williams' reduction, CNF-SAT on $N$ variables would take time about $2^{0.995 N}$ for every clause width, which would refute SETH. The same chain applies to LCS, Fréchet distance and the other OV-hard problems.

## Where it is used

- **Algorithm design.** When a problem is shown to be OV-hard or 3SUM-hard, the search for a truly subquadratic exact algorithm stops, and work turns to log-factor savings, parameters such as the distance, approximation and special inputs.
- **Sequence comparison in practice.** A program that compares long texts or genomes uses a band, a bound on the distance or a heuristic, since the exact full table is the only known method for hard inputs.
- **Teaching.** The barrier shows that many problems with very different stories share one cause, and that a lower bound can be proved relative to a hypothesis when no unconditional proof is in sight.

## References
