---
tag: RN3ZY8
kind: theorem
slug: lcs-seth-lower-bound
name: LCS SETH lower bound
aliases:
- Longest Common Subsequence lower bound
area: complexity/fine-grained-complexity
level: advanced
summary: "Conditional on SETH, the LCS of two strings of length N has no O(N^(2-e)) algorithm. Abboud, Backurs and Vassilevska Williams, and Bringmann and Künnemann proved it in 2015."
prereqs: [longest-common-subsequence, orthogonal-vectors-hypothesis, seth-implies-ov-lower-bound]
see_also: [backurs-indyk-lcs-lower-bound, edit-distance-seth-lower-bound, lcs-dynamic-programming, quadratic-time-hardness, fine-grained-reduction, four-russians-method, longest-palindromic-subsequence, orthogonal-vectors]
sources:
  - paper: arxiv:1501.07053
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 59-78"
    locator: the lower bounds for LCS of two strings over a constant-size alphabet and of k strings over an alphabet of size O(k), and for dynamic time warping; the coordinate gadgets, normalized vector gadgets and their combination
  - paper: arxiv:1502.01063
    title: "Karl Bringmann and Marvin Künnemann, Quadratic conditional lower bounds for string problems and dynamic time warping, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS 2015), 79-97"
    locator: the alignment gadget framework and the lower bounds for LCS on binary strings, longest palindromic subsequence, longest tandem subsequence and dynamic time warping
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the split-and-list reduction from CNF-SAT to orthogonal vectors
  - paper: doi:10.1137/15M1053128
    title: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018 (conference version in STOC 2015)"
    locator: the earlier bound for edit distance, whose method of vector gadgets and alignment of all pairs the LCS proofs adapt
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 375-388"
    locator: the reduction from satisfiability of branching programs to LCS and edit distance
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: "William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980, 18-31"
    locator: the O(n^2 / log n) method for a finite alphabet, which also applies to LCS
---

The LCS SETH lower bound says that, conditional on the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), no algorithm computes the length of a [longest common subsequence](/longest-common-subsequence/) of two strings of length $N$ in time $O(N^{2-\delta})$ for any $\delta > 0$. Two papers at FOCS 2015 proved it independently: Abboud, Backurs and Vassilevska Williams for a constant-size alphabet and for $k$ strings, and Bringmann and Künnemann for binary strings. Both reduce from [Orthogonal Vectors](/orthogonal-vectors/), so the bound also holds under the [OV hypothesis](/orthogonal-vectors-hypothesis/). The bound for edit distance, by Backurs and Indyk, is a different theorem; see [edit distance SETH lower bound](/edit-distance-seth-lower-bound/).

## Statement

The model is the [word RAM](/word-ram/) with words of $O(\log N)$ bits. $\mathrm{lcs}(X, Y)$ is the length of a longest string that is a subsequence of both $X$ and $Y$.

**Theorem (Abboud, Backurs and Vassilevska Williams 2015).** Conditional on SETH:

1. for every $\delta > 0$, there is no algorithm that computes $\mathrm{lcs}(X, Y)$ for two strings of length $N$ over an alphabet of constant size in time $O(N^{2-\delta})$;
2. for every $k \ge 2$ and $\delta > 0$, there is no algorithm that computes the LCS of $k$ strings of length $N$ over an alphabet of size $O(k)$ in time $O(N^{k-\delta})$.

**Theorem (Bringmann and Künnemann 2015).** Conditional on SETH, part 1 holds for binary strings.

**The reduction.** Part 1 comes from a deterministic [fine-grained reduction](/fine-grained-reduction/) from OV with $n$ vectors of dimension $d$ (time $n^2$) to one LCS computation (time $N^2$) with $N = n \cdot \mathrm{poly}(d)$, built in time $n \cdot \mathrm{poly}(d)$. So part 1 is also **conditional on OVH**. Part 2 reduces from $k$-OV in the same way.

The bound is for the exact value. It does not rule out $O(N^2 / \log^c N)$ algorithms.

## In plain words

The longest common subsequence of two texts is the longest list of symbols that appears in both, in order, with gaps allowed. The classic method fills a table with one cell for each pair of positions, so its work grows with the square of the length. No method is known that saves a fixed power of the length.

This result says why. Such a method would also find, among two lists of yes-or-no vectors, a pair with no common yes, much faster than by checking all pairs. That would break SETH.

The proof writes each vector as a short string, so that the common subsequence of two such strings is longer by one when the vectors have no common yes. Then it joins the short strings into two long strings, so that the longest common subsequence of the long strings detects the best pair.

## Proof

This is a sketch. The steps it leaves out are the normalization of the vector gadgets and the proof that the combination of all gadgets works (the analysis of the alignments of $X$ and $Y$). They are in the paper of Abboud, Backurs and Vassilevska Williams, and in the alignment gadget framework of Bringmann and Künnemann. The vector gadget lemma has a full proof on [the LCS lower bound page in the sequences area](/backurs-indyk-lcs-lower-bound/).

**Step 1: SETH to OV.** By [Williams' split and list](/seth-implies-ov-lower-bound/), an $O(n^{2-\delta}\mathrm{poly}(d))$ algorithm for OV refutes SETH.

**Step 2: coordinate gadgets.** Over the alphabet $\{0, 1, 2\}$, let $C_A(0) = 0$, $C_A(1) = 1$, $C_B(0) = 01$ and $C_B(1) = 0$. Then $\mathrm{lcs}(C_A(x), C_B(y)) = 1 - xy$: three of the four pairs share one symbol, and $1$ and $0$ share none.

**Step 3: vector gadgets.** For $a, b \in \{0,1\}^d$ and a run length $L$, let $V_A(a) = 2^L C_A(a_1)\, 2^L C_A(a_2) \cdots 2^L C_A(a_d)$, and $V_B(b)$ the same with $C_B$. With $L = d + 1$,

$$\mathrm{lcs}(V_A(a), V_B(b)) = d(L + 1) - a \cdot b.$$

The runs of 2s force an optimal subsequence to match gadget $i$ only with gadget $i$; an alignment that shifts by one gadget loses $L$ symbols 2 and can gain at most $d$ gadget symbols.

**Step 4: normalization.** The value in step 3 falls with $a \cdot b$, so a pair with many common ones costs more than a pair with one. Abboud, Backurs and Vassilevska Williams change the gadgets so that the value is one fixed number $E_s$ for an orthogonal pair and one fixed smaller number $E_u$ for every other pair. *(Left out.)*

**Step 5: combination.** $X$ is the normalized gadgets of $a_1, \ldots, a_n$ in a row, and $Y$ is the gadgets of $b_1, \ldots, b_n$ with dummy gadgets on both sides, all separated by long runs of a separator symbol. The separators force an optimal common subsequence to match the $n$ gadgets of $X$ with $n$ consecutive gadgets of $Y$, and every pair $(a_i, b_j)$ meets in some shift. So $\mathrm{lcs}(X, Y)$ is at least a threshold $\tau$ if and only if some pair is orthogonal. The strings have length $n \cdot \mathrm{poly}(d)$. *(The proof of this is left out.)*

**Counting.** With $d = c \log n$, an $O(N^{2-\delta})$ LCS algorithm decides OV in time $O((n\, \mathrm{polylog}\, n)^{2-\delta}) = O(n^{2-\delta/2})$ for every $c$, which contradicts OVH, and so SETH. $\blacksquare$

**A worked example of step 3.** Take $d = 3$ and $L = 4$. For $a = 101$ and $b = 011$,

$$V_A(a) = 2222\,1\,2222\,0\,2222\,1, \qquad V_B(b) = 2222\,01\,2222\,0\,2222\,0,$$

and the LCS table gives $\mathrm{lcs} = 14 = 3 \cdot 5 - 1$, since $a \cdot b = 1$. For $b = 010$ the vectors are orthogonal and the value is $15$. Over all 64 pairs $(a, b) \in \{0,1\}^3 \times \{0,1\}^3$, the formula $d(L+1) - a \cdot b$ holds for $L = 1, 2, 3, 4$. Without the runs, with $L = 0$, it fails for 10 of the 64 pairs, because gadgets then match across positions. The proof uses $L = d + 1$ because it needs a bound that works for all $d$.

## Consequences

- **The LCS table is near optimal.** Conditional on SETH, the $O(N^2)$ [dynamic program](/lcs-dynamic-programming/) cannot be improved by a factor $N^{\delta}$. Log-factor savings, such as the [Four Russians method](/four-russians-method/) with time $O(N^2 / \log N)$ for a fixed alphabet, remain possible.
- **Several strings.** The $O(N^k)$ table for $k$ strings is optimal up to $N^{o(1)}$ factors, conditional on SETH, when the alphabet has size $O(k)$.
- **Related problems.** Bringmann and Künnemann give the same quadratic bound for the [longest palindromic subsequence](/longest-palindromic-subsequence/), the longest tandem subsequence and dynamic time warping on one-dimensional sequences. The shortest common supersequence of two strings has length $|X| + |Y| - \mathrm{lcs}(X, Y)$, so it has the same bound.
- **Weaker hypotheses.** Abboud, Hansen, Vassilevska Williams and Williams (2016) reduced satisfiability of branching programs to LCS, so the bound holds under a hypothesis weaker than SETH.

## Tightness

- **Upper bound.** The table computes the LCS in $O(N^2)$ time, so the exponent 2 is tight. The bound is of the form "no $O(N^{2-\delta})$", and "no $o(N^2)$" would be false, by the $O(N^2/\log N)$ method.
- **Alphabet.** Binary strings suffice (Bringmann and Künnemann). For a one-symbol alphabet, the LCS is the shorter length.
- **Input measures.** The hard instances have many matching pairs and a large LCS. Algorithms whose time depends on the number of matching pairs or on the distance are fast on other inputs, and the theorem does not exclude them.

## History

Backurs and Indyk proved the SETH bound for edit distance at STOC 2015. At FOCS 2015, two papers proved the bound for LCS. Abboud, Backurs and Vassilevska Williams adapted the vector gadgets and the alignment of all pairs to LCS, with a normalization step, and added the bounds for $k$ strings and dynamic time warping. Bringmann and Künnemann gave a general framework, alignment gadgets, that yields the bounds for LCS on binary strings, edit distance, dynamic time warping and several other problems. The credit for LCS goes to these two papers, not to Backurs and Indyk.

## References
