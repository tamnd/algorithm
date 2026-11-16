---
tag: AWXN3M
kind: theorem
slug: edit-distance-seth-lower-bound
name: Edit distance SETH lower bound
aliases: []
area: complexity/fine-grained-complexity
level: advanced
summary: "Conditional on SETH, the edit distance of two strings of length N has no O(N^(2-e)) algorithm (Backurs and Indyk 2015), even for binary strings (Bringmann and Künnemann 2015)."
prereqs: [edit-distance, orthogonal-vectors-hypothesis, seth-implies-ov-lower-bound]
see_also: [edit-distance-hardness, lcs-seth-lower-bound, wagner-fischer-algorithm, quadratic-time-hardness, fine-grained-reduction, frechet-distance, four-russians-method, landau-vishkin-algorithm]
sources:
  - paper: doi:10.1137/15M1053128
    title: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018 (conference version in STOC 2015, 51-58)"
    locator: Section 3 (the vector gadgets, the pattern distance and the reduction to edit distance over seven symbols; Theorems 1 to 5 in the arXiv version 1412.0348v4); this page relies on the journal version
  - paper: arxiv:1502.01063
    title: "Karl Bringmann and Marvin Künnemann, Quadratic conditional lower bounds for string problems and dynamic time warping, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 79-97"
    locator: the alignment gadget framework and the lower bound for edit distance on binary strings and with general fixed costs
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the split-and-list reduction from CNF-SAT to orthogonal vectors
  - paper: "Karl Bringmann, Why walking the dog takes time: Frechet distance has no strongly subquadratic algorithms unless SETH fails, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014), 661-670"
    locator: the lower bound for the Fréchet distance and the question for edit distance
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 375-388"
    locator: the reduction from satisfiability of branching programs to edit distance, and the circuit lower bounds that would follow from shaving enough logarithmic factors
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: "William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980, 18-31"
    locator: the O(n^2 / log n) algorithm for a finite alphabet
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on sequence problems that are hard under SETH
  - paper: doi:10.1145/321921.321923
    title: "C. K. Wong and Ashok K. Chandra, Bounds for the string editing problem, Journal of the ACM 23(1), 1976, 13-16"
    locator: the lower bound of order mn for algorithms that only test symbols for equality
---

The edit distance SETH lower bound says that, conditional on the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), no algorithm computes the [edit distance](/edit-distance/) of two strings of length $N$ in time $O(N^{2-\delta})$ for any $\delta > 0$. Backurs and Indyk proved it in 2015 with a reduction from [Orthogonal Vectors](/orthogonal-vectors/), so the bound also holds under the weaker [OV hypothesis](/orthogonal-vectors-hypothesis/). It shows that the quadratic [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) is optimal up to factors $N^{o(1)}$, unless SETH fails.

This page states the result and its place among the fine-grained bounds, with a proof sketch. The full proof, with every lemma, is on [edit distance hardness](/edit-distance-hardness/) in the strings area.

## Statement

The model is the [word RAM](/word-ram/) with words of $O(\log N)$ bits. The distance is the Levenshtein distance: insertions, deletions and substitutions of single symbols, each of cost 1. The input is two strings of length at most $N$ over an alphabet $\Sigma$.

**Theorem (Backurs and Indyk 2015).** Conditional on SETH: for every $\delta > 0$, there is no algorithm that computes the edit distance of two strings of length $N$ over an alphabet of seven symbols in time $O(N^{2-\delta})$.

**Theorem (Bringmann and Künnemann 2015).** Conditional on SETH, the same holds for binary strings, $|\Sigma| = 2$.

**The reduction.** Both bounds come from a deterministic [fine-grained reduction](/fine-grained-reduction/) from OV with $n$ vectors of dimension $d$ (time $n^2$) to one edit distance computation (time $N^2$) on strings of length $N = n \cdot d^{O(1)}$, computed in time $n \cdot d^{O(1)}$. An $O(N^{2-\delta})$ algorithm for edit distance then decides OV in time $O(n^{2-\delta} d^{O(1)})$. So the bound is **conditional on OVH** too, and on SETH through [SETH implies OV lower bound](/seth-implies-ov-lower-bound/).

The bound rules out a polynomial saving. It does not rule out $O(N^2 / \log^c N)$ algorithms, and it says nothing about approximation.

## In plain words

Comparing two strings by the edit distance fills a table with one cell for each pair of positions. So the work grows with the square of the length. After fifty years, the best methods still save only small factors.

This result explains the lack of progress. A method that saved a fixed power of the length would also find a pair of yes-or-no vectors with no common yes much faster than by checking all pairs. That, in turn, would solve hard logic formulas faster than anyone expects to be possible.

The proof writes each vector as a short string, so that a good pair is one step cheaper to match than a bad pair. Then it joins the short strings of each list into one long string, so that the cheapest match of the long strings uses the best pair.

## Proof

This is a sketch. It follows the version of Backurs and Indyk as written out on [edit distance hardness](/edit-distance-hardness/), which uses $3d + 7$ symbols instead of seven. The steps it leaves out are the proof of the choice gadget lemma (a case analysis of the alignments of the gadgets) and the charging argument for the no-case of the pattern distance; both are given in full on that page.

**Step 1: SETH to OV.** By [Williams' split and list](/seth-implies-ov-lower-bound/), a $k$-CNF formula on $\nu$ variables becomes an OV instance with $n = 2^{\nu/2}$ vectors per list and $d = \mathrm{poly}(\nu)$, and an $O(n^{2-\delta} d^{O(1)})$ algorithm for OV refutes SETH.

**Step 2: vector gadgets.** Use $t = d + 1$ coordinate positions, $\hat a = (0, a)$ and $\hat b = (1, b)$. The gadgets $G_1(a)$ of length $14t$ and $G_2(\hat b)$ of length $10t$ are built from coordinate gadgets with $\mathrm{ed}(L(u), Q(w)) = t + u \cdot w$, and from long runs of two filler symbols that force each alignment into one of two options. One option pays for $\hat a \cdot \hat b$, the other pays a fixed 1. So

$$\mathrm{ed}(G_1(a), G_2(\hat b)) = \begin{cases} E_s = 10t & \text{if } a \cdot b = 0, \\ E_u = 10t + 1 & \text{otherwise.} \end{cases}$$

The cap at $E_u$ matters: the cost of a bad pair does not grow with the number of common ones, so one good pair is visible in a sum over $n$ pairs.

**Step 3: all pairs at once.** The pattern $P$ is the gadgets $G_1(a_1), \ldots, G_1(a_n)$ separated by runs of a new symbol $\#$. The text $T$ is the gadgets $G_2(\hat b_1), \ldots, G_2(\hat b_n)$, with $n - 1$ dummy gadgets $G_2(1^t)$ on each side, also separated by runs of $\#$. A dummy costs $E_u$ against every $G_1(a)$. Sliding $P$ along $T$ puts every $b_j$ under every $a_i$ in some window. So the smallest distance from $P$ to a substring of $T$ is at most $n E_u - 1$ if some pair is orthogonal, and at least $n E_u$ otherwise.

**Step 4: padding.** With a new symbol $\&$, $X = \&^{|T|} P \&^{|T|}$ and $Y = T$ satisfy $\mathrm{ed}(X, Y) = 2|T| + \min_{T'} \mathrm{ed}(P, T')$. With $\theta = 2|T| + n E_u$, the OV instance has an orthogonal pair if and only if $\mathrm{ed}(X, Y) < \theta$. Both strings have length $O(nd)$.

**Counting.** From $\nu$ variables, the strings have length $N = 2^{\nu/2} \mathrm{poly}(\nu)$. An $O(N^{2-\delta})$ algorithm would decide $k$-SAT in time $2^{(1-\delta/2)\nu} \mathrm{poly}(\nu)$ for every $k$, which contradicts SETH. $\blacksquare$

**A worked example.** Take $n = 2$ and $d = 2$, so $t = 3$, $E_u = 31$, $|P| = 208$, $|T| = 368$, $|X| = 944$, $\theta = 798$, and 13 symbols. For $A = \{10, 01\}$ and $B = \{11, 10\}$, the pair $(01, 10)$ is orthogonal, and the Wagner-Fischer table gives $\mathrm{ed}(X, Y) = 797 < \theta$. For $A = B = \{11, 10\}$, no pair is orthogonal, and $\mathrm{ed}(X, Y) = 798 = \theta$. The answer of OV is one unit of edit distance in a value near 800.

## Consequences

- **Wagner-Fischer is near optimal.** Conditional on SETH, no algorithm beats the $O(N^2)$ dynamic program by a factor $N^{\delta}$. Log-factor savings, such as the [Four Russians method](/four-russians-method/) of Masek and Paterson with time $O(N^2 / \log N)$ for a fixed alphabet, are allowed by the bound.
- **A polylog shaved is a lower bound made.** Abboud, Hansen, Vassilevska Williams and Williams (2016) reduced satisfiability of branching programs, a problem believed harder than CNF-SAT, to edit distance. So the bound holds under a weaker hypothesis than SETH. They also showed that an algorithm with time $N^2 / \log^{c} N$ for every constant $c$ would give new circuit lower bounds.
- **Related measures.** The same method, with other gadgets, gives quadratic bounds conditional on SETH for the [longest common subsequence](/lcs-seth-lower-bound/), dynamic time warping, the [Fréchet distance](/frechet-distance/) and [approximate string matching](/approximate-string-matching/) with a pattern of linear length. See [quadratic-time hardness](/quadratic-time-hardness/).
- **Where to look for algorithms.** The hard strings have edit distance $\Theta(N)$. When the distance $k$ is small, the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) runs in time $O(N + k^2)$, which is subquadratic for $k \le N^{1-\delta}$. Approximation is also open to faster methods, since the reduction needs the exact value.

## Tightness

- **Upper bound.** The Wagner-Fischer algorithm runs in $O(N^2)$ time, and Masek and Paterson's in $O(N^2 / \log N)$ for a fixed alphabet. So the exponent 2 is tight.
- **Alphabet.** The bound holds for two symbols (Bringmann and Künnemann). With one symbol, the edit distance is the difference of the lengths, computed in $O(N)$ time.
- **Form of the bound.** The form "no $O(N^{2-\delta})$ for any $\delta > 0$" is the strongest form the reduction gives. A bound of the form "no $o(N^2)$" would be false, by Masek and Paterson.
- **Unconditional.** On the word RAM, no lower bound above linear is known. The $\Omega(N^2)$ bound of Wong and Chandra (1976) holds only for algorithms that compare symbols for equality, and it is unconditional in that model.

## History

Bringmann proved the SETH bound for the Fréchet distance in 2014 and asked about edit distance. Backurs and Indyk answered at STOC 2015 with seven symbols, and the journal version appeared in the SIAM Journal on Computing in 2018. In the same year, Bringmann and Künnemann gave alignment gadgets, a general framework that covers binary edit distance, LCS and dynamic time warping, and Abboud, Backurs and Vassilevska Williams proved the bounds for LCS. In 2016, Abboud, Hansen, Vassilevska Williams and Williams based the bound on branching programs. The survey of Vassilevska Williams (ICM 2018) places the result among the other SETH-hard sequence problems.

## References
