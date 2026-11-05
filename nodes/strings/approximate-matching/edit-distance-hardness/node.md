---
tag: QCA6XN
kind: theorem
slug: edit-distance-hardness
name: Edit distance hardness under SETH
aliases:
- Backurs-Indyk theorem
area: strings/approximate-matching
level: research
summary: Edit distance has no strongly subquadratic algorithm unless the Strong Exponential Time Hypothesis fails.
prereqs: [edit-distance, wagner-fischer-algorithm, strong-exponential-time-hypothesis, orthogonal-vectors]
see_also: [edit-distance-seth-lower-bound, seth-implies-ov-lower-bound, orthogonal-vectors-hypothesis, lcs-seth-lower-bound, fine-grained-reduction, landau-vishkin-algorithm, sellers-algorithm, frechet-distance]
sources:
  - paper: doi:10.1137/15M1053128
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing, 2018
    locator: Section 3 (in the arXiv version 1412.0348v4, Theorems 1 and 2 on the vector gadgets, Theorem 3 on the pattern distance, Theorems 4 and 5 on the reduction to edit distance over seven symbols)
  - paper: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365"
    locator: the split of the variables of a CNF formula into two halves, which reduces satisfiability to a search for an orthogonal pair of vectors
  - paper: "Karl Bringmann and Marvin Künnemann, Quadratic conditional lower bounds for string problems and dynamic time warping, IEEE Symposium on Foundations of Computer Science (FOCS), 2015, 79-97"
    locator: the alignment gadgets and the lower bound for edit distance over a binary alphabet
  - paper: "Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001, 367-375"
    locator: the exponential time hypotheses for k-SAT, the source of SETH
  - paper: "Amir Abboud, Thomas Dueholm Hansen, Virginia Vassilevska Williams and Ryan Williams, Simulating branching programs with edit distance and friends, or: a polylog shaved is a lower bound made, ACM Symposium on Theory of Computing (STOC), 2016"
    locator: the reduction from the satisfiability of branching programs to edit distance and LCS
  - paper: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, Tight hardness results for LCS and other sequence similarity measures, IEEE Symposium on Foundations of Computer Science (FOCS), 2015, 59-78"
    locator: the quadratic lower bounds for LCS and related measures under SETH
  - paper: "Karl Bringmann, Why walking the dog takes time: Frechet distance has no strongly subquadratic algorithms unless SETH fails, IEEE Symposium on Foundations of Computer Science (FOCS), 2014, 661-670"
    locator: the first such bound for a distance between sequences, which posed the question for edit distance
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980
    locator: pages 18 to 31 (the O(n^2 / log n) algorithm for a finite alphabet)
  - paper: doi:10.1145/321921.321923
    title: C. K. Wong and Ashok K. Chandra, Bounds for the string editing problem, Journal of the ACM 23(1), 1976
    locator: pages 13 to 16 (the lower bound of order mn for algorithms that only test symbols for equality)
---

The edit distance hardness theorem states that if the [edit distance](/edit-distance/) of two strings of length $N$ can be computed in time $O(N^{2-\delta})$ for some constant $\delta > 0$, then the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) (SETH) is false. So the quadratic [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) is optimal up to factors of the form $N^{o(1)}$, unless CNF satisfiability has a much faster algorithm than any known one. Backurs and Indyk proved it in 2015, by a reduction from the [orthogonal vectors](/orthogonal-vectors/) problem.

## Statement

The edit model is Levenshtein: insertions, deletions and substitutions of single symbols, each of cost 1, with no transpositions. Write $\mathrm{ed}(x, y)$ for the distance. Strings are sequences of integers (the alphabet is part of the input), and the machine is the word RAM. A **strongly subquadratic** algorithm for edit distance runs in time $O(N^{2-\delta})$ on two strings of length at most $N$, for a constant $\delta > 0$.

**SETH.** For every $\varepsilon > 0$ there is an integer $k$ such that $k$-SAT on $\nu$ variables cannot be solved in time $O(2^{(1-\varepsilon) \nu})$.

**Orthogonal vectors (OV).** Given two lists $A$ and $B$ of $n$ vectors each in $\{0, 1\}^d$, decide whether some $a \in A$ and $b \in B$ have $a \cdot b = \sum_{\ell} a_\ell b_\ell = 0$.

**Theorem.**

1. For $n, d \ge 1$, an OV instance with $n$ vectors of dimension $d$ on each side can be turned, in time $O(nd)$, into two strings $X$ and $Y$ of length $O(nd)$ over an alphabet of $3d + 7$ symbols and an integer $\theta$, such that the instance has an orthogonal pair if and only if $\mathrm{ed}(X, Y) < \theta$.
2. If some algorithm computes the edit distance of any two strings of length at most $N$ over an alphabet of at most $N$ symbols in time $O(N^{2-\delta})$, for a constant $\delta > 0$, then SETH is false.

## In plain words

Comparing two strings symbol by symbol fills a table with one cell for each pair of positions, so the classic method takes time that grows with the square of the length. Decades of work found only small savings. This theorem explains why: a much faster method would also solve a famous hard problem faster.

The hard problem is to find, among two lists of short yes-or-no vectors, a pair that never says yes in the same place. The proof writes each vector as a short string, so that a good pair gives a cheaper match than a bad pair. It then glues all the strings of each list into one long string. Long blocks of a filler symbol force any cheap alignment to match the pieces one to one along a single shift. So the distance between the two long strings drops by one exactly when a good pair exists.

## Proof

The full proof, with each lemma, is in [the proof of the edit distance hardness theorem](proofs/main.md). Its steps:

- **Alignments.** An alignment of $x$ and $y$ pairs some positions of $x$ with positions of $y$ in increasing order. Its cost is the number of unpaired symbols plus the number of pairs with different symbols, and $\mathrm{ed}(x, y)$ is the least cost. If an alignment has $\pi$ pairs and $\mu$ of them join equal symbols, its cost is $|x| + |y| - (\pi + \mu)$. So a lower bound on the distance is an upper bound on the **gain** $\pi + \mu$.
- **SETH to OV.** Split the variables of a $k$-CNF formula with $\nu$ variables and $\kappa$ clauses into two halves. Each of the $2^{\nu/2}$ assignments of a half gives a vector with one coordinate for each clause, equal to 0 when the half assignment satisfies the clause. Two half assignments satisfy the formula exactly when their vectors are orthogonal. An OV algorithm in time $O(n^{2-\delta} d^{O(1)})$ then solves $k$-SAT in time $2^{(1-\delta/2)\nu} \mathrm{poly}(\nu)$ for each fixed $k$, which contradicts SETH.
- **Coordinate gadgets.** For $u, w \in \{0, 1\}^t$, let $L(u)$ have the symbol $\sigma_{\ell, u_\ell}$ at position $\ell$, and let $Q(w)$ have the block $\sigma_{\ell,0} \sigma_{\ell,1}$ at block $\ell$ when $w_\ell = 0$ and $\sigma_{\ell,0} \tau_\ell$ when $w_\ell = 1$. Then $\mathrm{ed}(L(u), Q(w)) = t + u \cdot w$.
- **A choice gadget.** Let $L$ and $R$ have length $p$, let $D$ have length $q$, and let none of them contain the symbols $\alpha$ and $\beta$. If $h \ge 2q$, then
$$ \mathrm{ed}(\alpha^h L \beta^h R \alpha^h,\ \beta^h D \beta^h) = 2h + p + \min(\mathrm{ed}(L, D), \mathrm{ed}(R, D)). $$
The run $\beta^h$ in the middle can be matched only if $D$ is aligned entirely under $L$ or entirely under $R$, and the proof counts the gain in each case.
- **Vector gadgets.** With $t = d + 1$, $h = 4t$, $\hat a = (0, a)$, $\hat b = (1, b)$ and $e_1 = (1, 0, \ldots, 0)$, set $G_1(a) = \alpha^h L(\hat a) \beta^h L(e_1) \alpha^h$ and $G_2(w) = \beta^h Q(w) \beta^h$. Then $\mathrm{ed}(G_1(a), G_2(\hat b)) = 10t + \min(a \cdot b, 1)$ and $\mathrm{ed}(G_1(a), G_2(1^t)) = 10t + \min(|a|, 1)$, where $|a|$ is the number of ones of $a$. So the cost is $E_s = 10t$ for an orthogonal pair and $E_u = 10t + 1$ for any other pair: it does not grow with the number of common ones. For $d = 1$ the gadgets have lengths 28 and 20, and the two costs are 20 and 21.
- **Pattern distance.** Let $H = E_u$ and let $\#$ be a new symbol. The pattern is $P = \#^H G_1(a_1) \#^{2H} G_1(a_2) \cdots \#^{2H} G_1(a_n) \#^H$. The text $T$ is the concatenation of $\#^H G_2(c) \#^H$ over the $3n - 2$ vectors $c = 1^t$ ($n - 1$ times), $\hat b_1, \ldots, \hat b_n$, $1^t$ ($n - 1$ times). If $a_i \cdot b_j = 0$, the window of $n$ text gadgets that puts $\hat b_j$ under $G_1(a_i)$ gives $\min_{T'} \mathrm{ed}(P, T') \le n E_u - 1$, where $T'$ ranges over the substrings of $T$. If no pair is orthogonal, a charging argument gives $\min_{T'} \mathrm{ed}(P, T') \ge n E_u$: each vector gadget of $P$ either sits under one text gadget that no other pattern gadget touches and pays at least $E_u$, or it forces at least $E_u$ units of cost from its own symbols or from a run of $\#$.
- **Padding.** For a new symbol $\&$, $\mathrm{ed}(\&^{|T|} P \&^{|T|}, T) = 2|T| + \min_{T'} \mathrm{ed}(P, T')$, because each $\&$ costs exactly 1 and can absorb any prefix or suffix of $T$.

So $X = \&^{|T|} P \&^{|T|}$, $Y = T$ and $\theta = 2|T| + n E_u$ prove part 1. The strings have length $O(nt) = O(nd)$, and the symbols are $\sigma_{\ell,0}, \sigma_{\ell,1}, \tau_\ell$ for $\ell \le t$ and $\alpha, \beta, \#, \&$, which is $3t + 4 = 3d + 7$. For part 2, chain the two reductions: a $k$-CNF on $\nu$ variables has at most $(2\nu + 1)^k$ distinct clauses, so the strings have length $2^{\nu/2} \mathrm{poly}(\nu)$, and an $O(N^{2-\delta})$ edit distance algorithm decides the formula in time $O(2^{(1-\delta/4) \nu})$ for every fixed $k$.

## Consequences

- **Wagner-Fischer is near optimal.** Under SETH, no algorithm beats the $O(N^2)$ dynamic program of [Wagner and Fischer](/wagner-fischer-algorithm/) by a polynomial factor. Savings of logarithmic factors, such as the [Four Russians method](/four-russians-method/) of Masek and Paterson, remain possible.
- **Approximate string matching.** The pattern distance $\min_{T'} \mathrm{ed}(P, T')$ in the proof is the smallest value that [Sellers' algorithm](/sellers-algorithm/) reports over all end positions. So the [approximate string matching](/approximate-string-matching/) problem with $k = \Theta(m)$ and $m = \Theta(n)$ also has no $O((mn)^{1 - \delta})$ algorithm under SETH.
- **Small distances stay easy.** The hard strings have distance $\Theta(N)$. For a distance $k$, the diagonal methods with [longest common extension](/longest-common-extension-query/) queries, as in the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/), compute it in $O(N + k^2)$ time, so the theorem says nothing against fast algorithms when $k \le N^{1 - \delta}$.
- **Weighted and related measures.** Weighted edit distance with unit weights contains the plain case, so it is at least as hard. Reductions from OV of the same kind give quadratic lower bounds for the [longest common subsequence](/longest-common-subsequence/) (see [LCS lower bound under SETH](/lcs-seth-lower-bound/)) and for the [Fréchet distance](/frechet-distance/).
- **Through OV.** Part 1 shows more than part 2: an $O(N^{2-\delta})$ algorithm for edit distance gives an $O(n^{2-\delta} \mathrm{poly}(d))$ algorithm for OV, so the bound also holds under the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/), which SETH implies.

## Tightness

- **Upper bound.** The Wagner-Fischer algorithm computes the edit distance in $O(N^2)$ time, so the exponent 2 cannot be lowered in the theorem. The theorem rules out $N^{2-\delta}$, not $N^2 / \log^{c} N$, and Abboud, Hansen, Vassilevska Williams and Williams relate savings of more than a polylogarithmic factor to circuit lower bounds.
- **Alphabet size.** The proof here uses $3d + 7$ symbols, which is polylogarithmic in $N$ when the vectors come from a $k$-CNF formula. Backurs and Indyk use seven symbols, and Bringmann and Künnemann prove the same bound for binary strings. With one symbol, $\mathrm{ed}(x, y) = \bigl| |x| - |y| \bigr|$, so the bound needs at least two symbols.
- **Unconditional bounds.** Wong and Chandra proved an $\Omega(N^2)$ lower bound for algorithms that can only test two symbols for equality. On the word RAM, which can use the symbols as numbers, no unconditional bound above linear is known.
- **Exactness.** The proof needs the exact distance, since the two cases differ by 1 in a value of order $N$. The reduction says nothing about approximation of the edit distance within a constant factor.

## History

Bringmann showed in 2014 that the Fréchet distance has no strongly subquadratic algorithm unless SETH fails, and listed edit distance as an open problem. Backurs and Indyk answered it at STOC 2015, with a reduction from orthogonal vectors over seven symbols, and the journal version appeared in the SIAM Journal on Computing in 2018. Their key idea is the gadget with two alignment options, which caps the cost of a pair of vectors at a fixed value. The step from SETH to orthogonal vectors is due to Williams (2005), and SETH itself to Impagliazzo and Paturi (2001). In 2015, Bringmann and Künnemann extended the bound to binary strings with their alignment gadgets, and Abboud, Backurs and Vassilevska Williams proved the matching results for LCS. In 2016, Abboud, Hansen, Vassilevska Williams and Williams based the bound on a weaker hypothesis about branching programs. The quadratic lower bound of Wong and Chandra (1976) holds only for algorithms that compare symbols for equality.

## References
