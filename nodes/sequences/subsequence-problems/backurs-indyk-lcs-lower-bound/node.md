---
tag: 4HTN7N
kind: theorem
slug: backurs-indyk-lcs-lower-bound
name: Backurs-Indyk lower bound for edit distance and LCS
aliases:
- SETH hardness of LCS
area: sequences/subsequence-problems
level: research
summary: Under SETH, LCS of two length-n strings cannot be computed in strongly subquadratic time.
prereqs: [longest-common-subsequence, strong-exponential-time-hypothesis, orthogonal-vectors-hypothesis]
see_also: [lcs-seth-lower-bound, edit-distance-seth-lower-bound, orthogonal-vectors, seth-implies-ov-lower-bound, fine-grained-reduction, lcs-dynamic-programming, four-russians-method, edit-distance]
sources:
  - paper: "Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), Proceedings of the 47th ACM Symposium on Theory of Computing (STOC), 2015, 51-58"
    locator: the main theorem for edit distance and the reduction from orthogonal vectors with vector gadgets and an alignment of all pairs
  - paper: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS), 2015, 59-78"
    locator: the lower bound for LCS of two strings over a constant-size alphabet and for k strings, by coordinate gadgets, normalized vector gadgets and a combination of all pairs
  - paper: "Karl Bringmann and Marvin Künnemann, Quadratic conditional lower bounds for string problems and dynamic time warping, Proceedings of the 56th IEEE Symposium on Foundations of Computer Science (FOCS), 2015, 79-97"
    locator: the alignment gadget framework and the lower bound for LCS on binary strings
  - paper: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the split-and-list reduction from CNF satisfiability to orthogonal vectors
  - paper: "Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001, 367-375"
    locator: the exponential time hypotheses for k-SAT
  - paper: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma
  - paper: "William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980, 18-31"
    locator: the O(n^2 / log n) algorithm by the Four Russians method
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC), 2016, 375-388"
    locator: the circuit lower bounds that would follow from shaving all polylogarithmic factors from the quadratic time of edit distance and LCS
---

The Backurs-Indyk lower bound and its LCS form say that the length of a [longest common subsequence](/longest-common-subsequence/) of two strings of length $n$ cannot be computed in $O(n^{2 - \varepsilon})$ time for any $\varepsilon > 0$, unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) (SETH) is false. The bound holds already for a constant-size alphabet, and the same is true for the [edit distance](/edit-distance/). The proof is a [fine-grained reduction](/fine-grained-reduction/) from the [orthogonal vectors](/orthogonal-vectors/) problem. Backurs and Indyk proved the edit distance case in 2015; the LCS case is due to Abboud, Backurs and Vassilevska Williams, and independently Bringmann and Künnemann, in the same year.

## Statement

Let OV be the problem: given sets $A, B \subseteq \{0, 1\}^d$ of $n$ vectors each, decide if some $a \in A$ and $b \in B$ have $a \cdot b = \sum_{i} a_i b_i = 0$. The [Orthogonal Vectors Hypothesis](/orthogonal-vectors-hypothesis/) (OVH) says that for each $\varepsilon > 0$ there is a $c$ such that OV with $d = c \log n$ has no $O(n^{2 - \varepsilon})$ time algorithm.

**Theorem (LCS).** If for some $\varepsilon > 0$ there is an algorithm that computes $\mathrm{lcs}(X, Y)$ for strings $X, Y$ of length at most $n$ over a fixed alphabet in $O(n^{2 - \varepsilon})$ time, then OVH is false, and so SETH is false.

**Theorem (edit distance, Backurs and Indyk).** The same holds with the Levenshtein edit distance in place of $\mathrm{lcs}$.

Abboud, Backurs and Vassilevska Williams proved the LCS theorem over an alphabet of constant size; Bringmann and Künnemann proved it for binary strings.

## In plain words

The table method finds the longest common subsequence of two strings of length one thousand with about one million steps. For decades, nobody found a method that is faster by a real power, only by small factors.

This theorem says why that is likely. A much faster method for this problem would also give a much faster method for a famous puzzle: given many lists of on and off switches, find two lists that never have the same switch on. And that, in turn, would give a much faster way to solve logic formulas than anyone believes is possible. So the theorem does not prove that no fast method exists. It proves that finding one would overturn a widely held belief about hard problems.

## Proof

The proof has three steps: SETH implies OVH; a vector gadget turns one pair of vectors into a pair of strings whose LCS reads off $a \cdot b$; and a combination puts all $n^2$ pairs into one pair of strings. Steps 1 and 2 are proved in full below. For step 3 we state the result of the papers and describe the idea; its proof is not given here, so this proof is partial.

**Step 1 (SETH implies OVH, Williams 2005).** Let $F$ be a $k$-CNF formula with $N$ variables and $M$ clauses. By the sparsification lemma of Impagliazzo, Paturi and Zane, for SETH it is enough to consider $M \le C_{k, \delta} N$ for each $\delta > 0$. Split the variables into two halves $V_1$, $V_2$ of size $N / 2$. For each of the $n = 2^{N/2}$ assignments $\alpha$ of $V_1$, let $a^\alpha \in \{0, 1\}^M$ have $a^\alpha_j = 0$ if and only if $\alpha$ satisfies clause $j$ (some literal of clause $j$ on $V_1$ is true under $\alpha$). Define $b^\beta$ for the assignments $\beta$ of $V_2$ in the same way. Then $a^\alpha \cdot b^\beta = 0$ if and only if each clause is satisfied by $\alpha$ or by $\beta$, that is, if and only if $\alpha \cup \beta$ satisfies $F$. The vectors have dimension $d = M = O(N) = O(\log n)$. An $O(n^{2 - \varepsilon} \mathrm{poly}(d))$ algorithm for OV would decide $F$ in $O(2^{(1 - \varepsilon / 2) N} \mathrm{poly}(N))$ time for all $k$, against SETH.

**Step 2 (vector gadget).** Use the alphabet $\{0, 1, 2\}$. The coordinate gadgets are

$$C_A(0) = 0, \quad C_A(1) = 1, \quad C_B(0) = 01, \quad C_B(1) = 0.$$

Then $\mathrm{lcs}(C_A(x), C_B(y)) = 1 - xy$ for $x, y \in \{0, 1\}$: the pairs $(0, 0)$, $(0, 1)$ and $(1, 0)$ share one letter, and 1 and 0 share none. For $a, b \in \{0, 1\}^d$ and $L = d + 1$, let

$$V_A(a) = 2^L C_A(a_1)\, 2^L C_A(a_2) \cdots 2^L C_A(a_d), \qquad V_B(b) = 2^L C_B(b_1) \cdots 2^L C_B(b_d),$$

where $2^L$ is the letter 2 written $L$ times.

**Lemma (vector gadget).** $\mathrm{lcs}(V_A(a), V_B(b)) = d (L + 1) - a \cdot b$. In particular, the value is $d (L + 1)$ if $a \perp b$ and at most $d (L + 1) - 1$ otherwise.

*Proof.* Call the $i$-th run of 2s of each string *block* $i$, and the letters after it *gadget* $i$. ($\ge$) Match block $i$ with block $i$ and gadget $i$ with gadget $i$ through a common subsequence of $C_A(a_i)$ and $C_B(b_i)$. This is order preserving and gives $dL + \sum_i (1 - a_i b_i)$.

($\le$) Take an optimal common subsequence, as a set of matched position pairs that do not cross. Let $s$ be the number of matched pairs of 2s and $t$ the number of other matched pairs. Gadget letters are not 2, so $t \le d$, the number of gadget letters of $V_A(a)$. Suppose a gadget letter of $V_A(a)$ in gadget $i$ is matched with a gadget letter of $V_B(b)$ in gadget $j$. Each matched pair of 2s lies before this pair in both strings or after it in both. Before it, $V_A(a)$ has $iL$ letters 2 and $V_B(b)$ has $jL$; after it, $(d - i) L$ and $(d - j) L$. So

$$s \le \min(i, j) L + \min(d - i, d - j) L = dL - |i - j| L.$$

If $i \ne j$, then $s + t \le dL - L + d < dL$, since $L > d$; but the matching of all blocks alone gives $dL$, so the subsequence is not optimal. Hence in an optimal one each gadget $i$ of $V_A(a)$ is matched only with gadget $i$ of $V_B(b)$, and these pairs form a common subsequence of $C_A(a_i)$ and $C_B(b_i)$. So $t \le \sum_i (1 - a_i b_i)$, and with $s \le dL$ the total is at most $dL + d - a \cdot b$. $\square$

The strings have length $O(d^2)$, which is polylogarithmic in $n$ when $d = O(\log n)$.

**Step 3 (combination, quoted).** Abboud, Backurs and Vassilevska Williams, and Bringmann and Künnemann, show: there are strings $X$ and $Y$ over a constant-size alphabet (binary in the second paper), of length $n \cdot \mathrm{poly}(d)$, and a threshold $\tau$, all computable in $O(n \cdot \mathrm{poly}(d))$ time from $A$ and $B$, such that $\mathrm{lcs}(X, Y) \ge \tau$ if and only if $A$ and $B$ contain an orthogonal pair. The idea: first change the vector gadget into a *normalized* one, whose value is one fixed number for orthogonal pairs and one smaller fixed number for all other pairs. Then $X$ is the gadgets of $a_1, \ldots, a_n$ in a row, and $Y$ is the gadgets of $b_1, \ldots, b_n$ with dummy gadgets on both sides. Separators force an optimal alignment to match the $n$ gadgets of $X$ with $n$ consecutive gadgets of $Y$, and each pair $(a_i, b_j)$ meets in one of these shifts. The total is then at least $\tau$ if and only if one shift contains an orthogonal pair.

**Conclusion.** Let an algorithm compute $\mathrm{lcs}$ in $O(N^{2 - \varepsilon})$ time for strings of length $N$. On the strings of step 3, with $N = n \cdot \mathrm{poly}(d)$ and $d = c \log n$, it decides OV in $O(n^{2 - \varepsilon} \mathrm{polylog}(n))$ time, which is $O(n^{2 - \varepsilon / 2})$, for every $c$. This contradicts OVH, and by step 1 SETH. $\blacksquare$

**Example of the gadget.** With $d = 3$, $L = 4$, $a = (1, 0, 1)$ and $b = (0, 1, 1)$: $V_A(a) = 2222\,1\,2222\,0\,2222\,1$ and $V_B(b) = 2222\,01\,2222\,0\,2222\,0$. Here $a \cdot b = 1$, and the LCS has length $3 \cdot 5 - 1 = 14$: all twelve 2s, the 1 of the first gadget, and the 0 of the second; the third gadgets 1 and 0 share nothing. With $a = (1, 0, 0)$ in place of $a$, the vectors are orthogonal and the LCS is 15.

## Consequences

- **The table is close to optimal.** The $\Theta(mn)$ [LCS table](/lcs-dynamic-programming/), [Hirschberg's algorithm](/hirschberg-lcs/) and the [bit-parallel method](/bit-parallel-lcs/) are all quadratic up to factors of $\log n$ or $w$, and under SETH no algorithm improves the exponent 2.
- **Parameterized algorithms are the way out.** Methods whose time depends on other measures, such as the number $r$ of matching pairs in [Hunt-Szymanski](/hunt-szymanski/) or the distance $D$ in [Myers' algorithm](/myers-diff/), are fast on some inputs and quadratic on the hard ones. The theorem does not rule them out.
- **Related problems.** The [shortest common supersequence](/shortest-common-supersequence/) of two strings and the [shortest edit script](/shortest-edit-script/) have lengths $m + n - \mathrm{lcs}$ and $m + n - 2\,\mathrm{lcs}$, so they have the same conditional bound. The edit distance has it by the Backurs-Indyk theorem, and Bringmann and Künnemann give it for dynamic time warping.
- **More strings.** For $k$ strings, Abboud, Backurs and Vassilevska Williams show that the $O(n^k)$ table cannot be improved to $O(n^{k - \varepsilon})$ under SETH.

## Tightness

The exponent 2 is matched by the $O(n^2)$ table. Lower order factors can be removed: Masek and Paterson computed the edit distance in $O(n^2 / \log n)$ time over a constant alphabet with the [Four Russians method](/four-russians-method/), and the same idea applies to LCS. So the theorem cannot be raised to a bound of $\Omega(n^2)$ time. Abboud, Hansen, Vassilevska Williams and Williams (2016) showed that an algorithm faster than $n^2$ by every polylogarithmic factor would imply circuit lower bounds that are not known today.

## History

Impagliazzo and Paturi stated the exponential time hypotheses in 2001, and Williams reduced CNF satisfiability to orthogonal vectors in 2005. In 2015, Backurs and Indyk showed at STOC that edit distance has no strongly subquadratic algorithm unless SETH is false. At FOCS 2015, Abboud, Backurs and Vassilevska Williams proved the same for LCS, also for $k$ strings, and Bringmann and Künnemann gave a general framework of alignment gadgets with bounds for LCS on binary strings, edit distance and dynamic time warping. In 2016, Abboud, Hansen, Vassilevska Williams and Williams connected faster polylogarithmic improvements to circuit lower bounds.

## References
