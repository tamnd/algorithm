---
tag: XCK7KW
kind: concept
slug: quadratic-time-hardness
name: Quadratic-time hardness
aliases:
- quadratic hardness
area: complexity/fine-grained-complexity
level: intro
summary: "Evidence that a problem has no O(n^(2-e)) algorithm: a fine-grained reduction from orthogonal vectors, and so from SETH, or from 3SUM. Edit distance, LCS and Fréchet distance are examples."
prereqs: [quadratic-barrier, conditional-lower-bound]
see_also: [orthogonal-vectors-hypothesis, 3sum-hardness, edit-distance-seth-lower-bound, lcs-seth-lower-bound, fine-grained-reduction, backurs-indyk-regex-hardness, frechet-distance, orthogonal-vectors]
sources:
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the lists of problems that are hard under SETH, OVH and the 3SUM conjecture
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the reduction from CNF-SAT to orthogonal vectors
  - paper: doi:10.1137/15M1053128
    title: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018 (conference version in STOC 2015)"
    locator: the vector gadgets and the reduction from orthogonal vectors to edit distance
  - paper: arxiv:1501.07053
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 59-78"
    locator: the lower bounds for LCS and dynamic time warping
  - paper: arxiv:1502.01063
    title: "Karl Bringmann and Marvin Künnemann, Quadratic conditional lower bounds for string problems and dynamic time warping, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 79-97"
    locator: the alignment gadget framework and the lower bounds for LCS on binary strings, edit distance on binary strings, longest palindromic subsequence and dynamic time warping
  - paper: "Karl Bringmann, Why walking the dog takes time: Fréchet distance has no strongly subquadratic algorithms unless SETH fails, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014), 661-670"
    locator: the reduction from orthogonal vectors to the continuous and the discrete Fréchet distance, also for approximation within a small constant factor
  - paper: doi:10.1109/FOCS.2016.56
    title: "Arturs Backurs and Piotr Indyk, Which regular expression patterns are hard to match?, Proceedings of the 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016), 457-466"
    locator: the classification of regular expression patterns of small depth by the time needed to match them
  - paper: doi:10.1145/2488608.2488673
    title: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 515-524"
    locator: the reduction from orthogonal vectors to telling diameter 2 from diameter 3 in sparse graphs
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995, 165-185"
    locator: the definition of 3SUM-hard problems and the reductions to collinear points and other problems in geometry
  - paper: doi:10.1142/S0218195995000064
    title: "Helmut Alt and Michael Godau, Computing the Fréchet distance between two polygonal curves, International Journal of Computational Geometry and Applications 5(1-2), 1995, 75-91"
    locator: the O(mn log(mn)) algorithm for the continuous Fréchet distance
---

Quadratic-time hardness is evidence that a problem has no algorithm with time $O(n^{2-\varepsilon})$ for any constant $\varepsilon > 0$. The evidence is a [fine-grained reduction](/fine-grained-reduction/) from a problem that is believed to need quadratic time: [orthogonal vectors](/orthogonal-vectors/), which is hard under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), or [3SUM](/3sum/). Such results now exist for edit distance, LCS, the Fréchet distance, regular expression matching, the diameter of sparse graphs and many problems of geometry.

The [quadratic barrier](/quadratic-barrier/) page is about the phenomenon and the ways around it. This page is about the statements, how they are proved, and which problems they cover.

## In plain words

Some tasks seem to need time that grows with the square of the input. Nobody can prove this outright. What researchers can show is that a clearly faster method for the task would also give a clearly faster method for one of two famous tasks. One asks whether two lists of yes-or-no vectors contain a pair with no common yes. The other asks whether three numbers in a list add up to zero.

For the first task there is extra support. A fast method for it would also solve a famous logic puzzle faster than anyone believes possible.

So "this task is quadratic-time hard" means: it is at least as hard as one of these famous tasks, up to small factors.

## The idea

### The statements

Let $B$ be a problem with a simple $O(n^2)$ algorithm, in the [word RAM](/word-ram/) model with words of $O(\log n)$ bits.

- $B$ is **OV-hard** if an $O(n^{2-\varepsilon})$ algorithm for $B$, for some $\varepsilon > 0$, gives an $O(n^{2-\delta})$ algorithm for OV with dimension $c \log n$ for every $c$, for some $\delta > 0$. Then $B$ has no $O(n^{2-\varepsilon})$ algorithm, conditional on the [OV hypothesis](/orthogonal-vectors-hypothesis/).
- $B$ is **SETH-hard** if such an algorithm for $B$ would refute SETH. Every OV-hard problem is SETH-hard, because SETH implies the OV hypothesis (Williams 2005). The converse is open, so "conditional on OVH" is the stronger form of the result.
- $B$ is **3SUM-hard** if an $O(n^{2-\varepsilon})$ algorithm for $B$ gives an $O(n^{2-\delta})$ algorithm for 3SUM. Then $B$ has no such algorithm, conditional on the [3SUM conjecture](/3sum-conjecture/). See [3SUM-hardness](/3sum-hardness/).

The 3SUM conjecture is not known to follow from SETH, and the OV hypothesis is not known to follow from the 3SUM conjecture, so the two kinds of hardness are separate pieces of evidence. If the hypothesis is stated for randomized algorithms, as SETH usually is, the bound for $B$ also holds for randomized algorithms, even when the reduction itself is randomized.

### How OV-hardness is proved

Most proofs for problems on sequences follow one pattern, from Backurs and Indyk (2015), made general by Bringmann and Künnemann (2015) as alignment gadgets:

1. **Coordinate gadgets.** Short strings for the values 0 and 1 of one coordinate, whose score is better when not both values are 1.
2. **Vector gadgets.** For each vector, join its coordinate gadgets, with separators that force coordinate $i$ to meet coordinate $i$. The score of two vector gadgets is one value for an orthogonal pair and a worse value for every other pair.
3. **Alignment of all pairs.** Join the gadgets of list $A$ into one long input and those of list $B$ into another, with padding, so that the best score of the whole instance is the best score over all pairs.
4. **Count.** The instance has size $n \cdot \mathrm{poly}(d)$, which is $n^{1+o(1)}$ when $d = c \log n$. So an $O(N^{2-\varepsilon})$ algorithm for $B$ decides OV in time $n^{2-\varepsilon+o(1)}$.

Step 4 is the reason for the care in steps 1 to 3: any blow-up of size $n^{1+\gamma}$ for a constant $\gamma > 0$ would weaken the bound to $N^{2/(1+\gamma)}$. For graph problems the gadgets are vertices and short paths, as in the example below.

### Problems with quadratic-time hardness

| Problem | Simple algorithm | Hard under | Source |
|---|---|---|---|
| [Orthogonal vectors](/orthogonal-vectors/), $d = c \log n$ | $O(n^2 d)$ | SETH | Williams 2005 |
| [Edit distance](/edit-distance-seth-lower-bound/) | $O(n^2)$ table | OVH, so SETH | Backurs and Indyk 2015 |
| [LCS](/lcs-seth-lower-bound/), also binary | $O(n^2)$ table | OVH, so SETH | Abboud, Backurs and Vassilevska Williams 2015; Bringmann and Künnemann 2015 |
| Dynamic time warping | $O(n^2)$ table | OVH, so SETH | the same two papers |
| [Longest palindromic subsequence](/longest-palindromic-subsequence/) | $O(n^2)$ table | OVH, so SETH | Bringmann and Künnemann 2015 |
| [Fréchet distance](/frechet-distance/), discrete and continuous | $O(n^2)$, $O(n^2 \log n)$ | OVH, so SETH | Bringmann 2014 |
| [Regular expression matching](/backurs-indyk-regex-hardness/), some patterns of depth 2 or 3 | $O(mn)$ | SETH | Backurs and Indyk 2016 |
| Diameter 2 or 3 in sparse graphs | $O(nm)$ | OVH, so SETH | Roditty and Vassilevska Williams 2013 |
| [3SUM](/3sum/) | $O(n^2)$ | 3SUM conjecture | the hypothesis itself |
| [Three collinear points](/collinear-points/) and other problems of geometry | $O(n^2)$ | 3SUM conjecture | Gajentaan and Overmars 1995 |

The continuous Fréchet distance of curves with $m$ and $n$ segments takes $O(mn \log(mn))$ time by the method of Alt and Godau (1995). Bringmann's bound also covers approximation within a small constant factor. For the diameter, the gap between 2 and 3 means that a $(3/2 - \varepsilon)$-approximation in time $O(m^{2-\delta})$ would refute SETH.

### What a result rules out

- It rules out a saving of a fixed power, $n^{2-\varepsilon}$. It does not rule out savings of $\log$ factors, which exist for edit distance, LCS and 3SUM.
- It speaks about the hard instances that the reduction builds. Algorithms that are fast when a parameter is small, such as the edit distance itself, are not excluded.
- It speaks about the exact problem or about the gap it builds. Edit distance has no exact truly subquadratic algorithm under SETH, but the result says nothing about approximation within large factors.

## Examples

**Diameter from orthogonal vectors.** Take $A = \{1100, 0110, 1011, 0101\}$ and $B = \{0011, 1110, 0111, 1101\}$, with $d = 4$. Build a graph with a vertex for each vector, a vertex $c_j$ for each coordinate, and two vertices $x$ and $y$. Join each vector to the $c_j$ where it has a 1, $x$ to all of $A$ and all $c_j$, $y$ to all of $B$ and all $c_j$, and $x$ to $y$.

The graph has 14 vertices and 37 edges. The dot products of the pairs, with rows for $A$ and columns for $B$, are

$$\begin{pmatrix} 0 & 2 & 1 & 2 \\ 1 & 2 & 2 & 1 \\ 2 & 2 & 2 & 2 \\ 1 & 1 & 2 & 2 \end{pmatrix}, \qquad \text{and the distances are} \qquad \begin{pmatrix} 3 & 2 & 2 & 2 \\ 2 & 2 & 2 & 2 \\ 2 & 2 & 2 & 2 \\ 2 & 2 & 2 & 2 \end{pmatrix}.$$

The only orthogonal pair, $1100$ and $0011$, is the only pair at distance 3: the two vectors have no common coordinate, so no path of length 2 joins them, and the path through $x$ and $y$ has length 3. Breadth-first search from every vertex gives diameter 3. With $0111$ in place of $0011$, no pair is orthogonal, the graph has 38 edges, and the diameter is 2.

In general the graph has $2n + d + 2$ vertices and $O(nd)$ edges. With $d = c \log n$, an algorithm that tells diameter 2 from diameter 3 in time $O(m^{2-\varepsilon})$ decides OV in time $n^{2-\varepsilon+o(1)}$, which refutes the OV hypothesis, and so SETH.

**Collinear points from 3SUM.** The map $s \mapsto (s, s^3)$ turns three integers with sum 0 into three points on a line. A worked instance is on [fine-grained reduction](/fine-grained-reduction/).

## Where it is used

- **Choosing what to look for.** A hardness result redirects work to log-factor savings, approximation, parameters and special inputs; see the [quadratic barrier](/quadratic-barrier/).
- **Explaining algorithms that are "only" quadratic.** Dynamic programming over two sequences, as in [edit distance](/edit-distance/) and [LCS](/longest-common-subsequence/), is near optimal, conditional on SETH.
- **Families of reductions.** Once one problem is OV-hard with linear size, problems that it reduces to with linear size inherit the bound. The same holds for 3SUM-hard problems in geometry.

## References
