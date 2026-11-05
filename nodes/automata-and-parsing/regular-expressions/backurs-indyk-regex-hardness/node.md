---
tag: ZSQ41N
kind: theorem
slug: backurs-indyk-regex-hardness
name: Backurs-Indyk regex matching lower bound
aliases:
- regex matching conditional lower bound
area: automata-and-parsing/regular-expressions
level: research
summary: Assuming SETH, regex matching has no O((mn)^(1-c)) algorithm for any constant c > 0, even for patterns of depth 2 or 3.
prereqs: [regex-matching, orthogonal-vectors-hypothesis]
see_also: [thompson-nfa-simulation, strong-exponential-time-hypothesis, orthogonal-vectors, seth-implies-ov-lower-bound, fine-grained-reduction, edit-distance-seth-lower-bound, lcs-seth-lower-bound, bit-parallel-regex-matching]
sources:
  - paper: doi:10.1109/FOCS.2016.56
    title: Arturs Backurs and Piotr Indyk, Which regular expression patterns are hard to match?, FOCS 2016
    locator: pp. 457 to 466
  - url: "https://arxiv.org/abs/1511.07070"
    title: Arturs Backurs and Piotr Indyk, Which regular expression patterns are hard to match?, arXiv version 2 (2016)
    locator: Tables 1 and 2 (the classification), Section 2 (the Orthogonal Vectors problem and homogeneous types), Section 3.1 Theorem 1 (type OR of concatenations of ORs), Section 3.3 Theorem 3 and Section 4.1 Theorem 8 (type concatenation of stars)
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3) (2005)
    locator: pp. 357 to 365
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2) (2001)
    locator: pp. 367 to 375
  - paper: doi:10.1109/FOCS.2015.15
    title: Karl Bringmann and Marvin Kuennemann, Quadratic conditional lower bounds for string problems and dynamic time warping, FOCS 2015
    locator: pp. 79 to 97 (the unbalanced Orthogonal Vectors problem, as used by Backurs and Indyk in their Section 2)
  - paper: doi:10.1109/FOCS.2017.36
    title: Karl Bringmann, Allan Gronlund and Kasper Green Larsen, A dichotomy for regular expression membership testing, FOCS 2017
    locator: pp. 307 to 318
  - paper: doi:10.1145/128749.128755
    title: Eugene W. Myers, A Four Russians algorithm for regular expression pattern matching, Journal of the ACM 39(2) (1992)
    locator: pp. 432 to 448
  - paper: doi:10.1007/978-3-642-02927-1_16
    title: Philip Bille and Mikkel Thorup, Faster regular expression matching, ICALP 2009, Lecture Notes in Computer Science 5555
    locator: pp. 171 to 182
---

The Backurs-Indyk theorem says that [regular expression matching](/regex-matching/) cannot be solved in time $O((mn)^{1-\delta})$ for any constant $\delta > 0$, for a pattern of size $m$ and a text of length $n$, unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails. The hardness holds already for patterns of depth 2 or 3 of a fixed shape, such as an OR of concatenations of ORs of symbols. So the $O(mn)$ bound of [Thompson's simulation](/thompson-nfa-simulation/), improved since 1968 only by logarithmic factors, is optimal up to factors smaller than any power.

## Statement

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. Backurs and Indyk also use the plus, $r^+ = r r^*$. Every pattern on this page is a regular expression in the strict sense; no feature beyond regular languages is used.

**Problems.** A pattern $p$ has size $m$, the number of symbols and operators in it, and a text $t$ has length $n$. *Pattern matching* asks whether some substring of $t$ is in $L(p)$. *Membership* asks whether $t \in L(p)$.

**Types.** Read a pattern as a tree whose inner nodes are $\mid$, concatenation, ${}^*$ or ${}^+$, with any number of children, and whose leaves are symbols. The pattern is *homogeneous* of type $o_1 o_2 \cdots o_k$ if all inner nodes at depth $i$ carry the operator $o_i$. For example, $0(0 \mid 1)0 \mid (0 \mid 1)00$ has type "$\mid\,\cdot\,\mid$": an OR of concatenations, whose factors are symbols or ORs of symbols. Type "$\cdot\,{}^*$" is a concatenation of symbols and stars of symbols, such as $y y^* x x x x^*$.

**Orthogonal Vectors.** Given sets $A, B \subseteq \{0, 1\}^d$ of $N$ vectors each, the [Orthogonal Vectors](/orthogonal-vectors/) problem asks whether some $a \in A$ and $b \in B$ have $a \cdot b = \sum_j a_j b_j = 0$. The [Orthogonal Vectors hypothesis](/orthogonal-vectors-hypothesis/) (OVH) says that for every $\varepsilon > 0$ there is a $c$ such that the problem with $d = c \log N$ has no $O(N^{2 - \varepsilon})$ algorithm. Williams (2005) showed that SETH implies OVH ([proof](/seth-implies-ov-lower-bound/)).

**Theorem (Backurs and Indyk, 2016).** Assume OVH, and so in particular assume SETH. For every constant $\delta > 0$:

1. Pattern matching has no $O((mn)^{1-\delta})$ algorithm for patterns of type "$\mid\,\cdot\,\mid$" over the alphabet $\{0, 1\}$ and texts over $\{0, 1, 2\}$, even on instances with $m = \Theta(n)$.
2. The same holds for pattern matching and for membership with patterns of type "$\cdot\,{}^*$".

The proof below is for part 1, which is Theorem 1 of the paper. Part 2 is Theorems 3 and 8 of the paper; its reduction is longer, and only its main gadget is shown here.

## In plain words

Matching a pattern against a text by the textbook method takes time about the size of the pattern times the length of the text. For decades, nobody has found a method that is faster by more than a small factor.

This theorem explains why. It takes a problem that is believed to need about the square of its input size, namely finding two lists of yes and no answers that never say yes at the same place, and turns it into a matching problem of about the same size. A much faster matcher would then solve the list problem much faster too, and that would break a widely believed assumption about how hard logic puzzles are.

The patterns that the translation needs are very simple: a choice between plain words in which some letters are a choice of two letters.

## Proof

Let $A = \{a^1, \dots, a^N\}$ and $B = \{b^1, \dots, b^N\}$ be an instance of Orthogonal Vectors in dimension $d$.

**Construction.** For a coordinate value $v \in \{0, 1\}$ let
$$\mathrm{CG}(0) = (0 \mid 1), \qquad \mathrm{CG}(1) = 0,$$
and for a vector $a$ let $\mathrm{VG}(a) = \mathrm{CG}(a_1)\, \mathrm{CG}(a_2) \cdots \mathrm{CG}(a_d)$. The pattern and the text are
$$p = \mathrm{VG}(a^1) \mid \mathrm{VG}(a^2) \mid \cdots \mid \mathrm{VG}(a^N), \qquad t = b^1\, 2\, b^2\, 2 \cdots 2\, b^N,$$
where each $b^j$ is written as the word $b^j_1 b^j_2 \cdots b^j_d$ over $\{0, 1\}$. The pattern has type "$\mid\,\cdot\,\mid$", size $m = O(Nd)$, and the text has length $n = (d + 1) N - 1$. Both are built in $O(Nd)$ time.

**Lemma 1.** For $a, b \in \{0, 1\}^d$, the word $b_1 \cdots b_d$ is in $L(\mathrm{VG}(a))$ if and only if $a \cdot b = 0$.

*Proof.* $L(\mathrm{CG}(0)) = \{0, 1\}$ and $L(\mathrm{CG}(1)) = \{0\}$, so every word of $L(\mathrm{VG}(a))$ has length $d$, and a word $w_1 \cdots w_d$ is in it exactly when $w_j \in L(\mathrm{CG}(a_j))$ for every $j$. For $w = b$ this says: for every $j$, $a_j = 0$ or $b_j = 0$, that is, $a_j b_j = 0$. The terms $a_j b_j$ are $0$ or $1$, so all of them are $0$ exactly when their sum $a \cdot b$ is $0$. $\square$

**Lemma 2.** Some substring of $t$ is in $L(p)$ if and only if some $a^i \in A$ and $b^j \in B$ have $a^i \cdot b^j = 0$.

*Proof.* If $a^i \cdot b^j = 0$, the substring $b^j$ of $t$ is in $L(\mathrm{VG}(a^i)) \subseteq L(p)$ by Lemma 1. Conversely, let a substring $w$ of $t$ be in $L(p)$. Then $w \in L(\mathrm{VG}(a^i))$ for some $i$, so $w$ has length $d$ and no symbol $2$. In $t$ the symbols $2$ cut the text into blocks of exactly $d$ symbols over $\{0, 1\}$, so a substring of length $d$ with no $2$ is one whole block $b^j$. By Lemma 1, $a^i \cdot b^j = 0$. $\square$

**The time bound.** Suppose an algorithm solves pattern matching for type "$\mid\,\cdot\,\mid$" in time $O((mn)^{1-\delta})$. Take the $c$ that OVH gives for $\varepsilon = \delta$, and let $d = c \log N$. By Lemma 2, building $p$ and $t$ and running the algorithm decides Orthogonal Vectors in time
$$O(Nd) + O\big((Nd \cdot Nd)^{1-\delta}\big) = O\big(N^{2 - 2\delta} \log^2 N\big) = O(N^{2 - \delta}),$$
which OVH rules out. Here $m$ and $n$ are both $\Theta(Nd)$, so the instances have $m = \Theta(n)$. This proves part 1. $\square$

**The gadget of part 2.** For type "$\cdot\,{}^*$" the pattern cannot choose, so Backurs and Indyk encode a coordinate by a run length. A coordinate at an odd index $j$ becomes $y y^*$ (at least one $y$) for $a_j = 0$ and $y y y y^*$ (at least three) for $a_j = 1$ in the pattern, and $y y y$ for $b_j = 0$ and $y$ for $b_j = 1$ in the text; even indices use $x$ in the same way. Since the letters alternate, a text vector gadget is derived from a pattern vector gadget if and only if the vectors are orthogonal. The rest of the proof, in Sections 3.3 and 4.1 of the paper, chains the $N$ pattern gadgets with separators and a gadget $(y^* x^*)^{d+10} y^*$ that absorbs one text vector, so that the whole pattern fits into the text only if one pair of aligned gadgets uses an orthogonal pair.

## Consequences

- **Thompson's bound is optimal.** Pattern matching and membership are solved in $O(mn)$ time by [simulating the Thompson NFA](/thompson-nfa-simulation/). Myers (1992) improved this to $O(mn / \log n)$, and Bille and Thorup (2009) to roughly $O(mn / \log^{1.5} n)$, as Backurs and Indyk summarize. Under SETH, no algorithm improves the exponent: an $O((mn)^{1-\delta})$ algorithm for general patterns would refute SETH, because general patterns include the patterns of the theorem.
- **Hardness depends on the shape, not only the size.** Backurs and Indyk classify every homogeneous type of depth 2 and 3. At depth 2, only "$\cdot\,{}^*$" is hard; the other types are near-linear, for example "$\mid\,\cdot$", which is dictionary matching and is solved by [Aho-Corasick](/aho-corasick/), and "$\cdot\,{}^+$", for which they give an $O(n \log^2 m)$ algorithm. At depth 3, every type that starts with concatenation is hard for both problems, and every type that starts with ${}^*$ is easy for pattern matching.
- **Membership at every depth.** Bringmann, Gronlund and Larsen (2017) extend the classification of membership to homogeneous types of any constant depth: every type is near-linear or quadratic under SETH, except Word Break.
- **Other hard string problems.** The proof follows the pattern of [conditional lower bounds](/conditional-lower-bound/) for [edit distance](/edit-distance-seth-lower-bound/) and [longest common subsequence](/lcs-seth-lower-bound/): an OV instance is written as a concatenation of vector gadgets. The [fine-grained reduction](/fine-grained-reduction/) keeps the size linear in $Nd$, which is what turns a quadratic bound for OV into one for matching.
- **Unbalanced sizes.** With the unbalanced form of OVH, in which $|A| = \Theta(|B|^\alpha)$, the same constructions give the bound for instances with $m$ about $n^\alpha$, for every constant $\alpha \in (0, 1]$; Backurs and Indyk use this form, which Bringmann and Kuennemann (2015) derived from SETH.

## Tightness

- **The exponent is tight.** The $O(mn)$ algorithm meets the bound up to factors that are smaller than every power $(mn)^\delta$. The theorem says nothing about factors such as $\log n$, which is where all known improvements lie.
- **The restriction to types is needed.** Without a restriction on the shape, the theorem would be false for some classes: patterns that are single words, of type "$\cdot$", are matched in $O(m + n)$ time by [Knuth-Morris-Pratt](/knuth-morris-pratt/), and the types listed as near-linear in the classification above are not hard.
- **Word Break is in between.** Membership for type "${}^*\,\mid\,\cdot$", such as $(a \mid ab \mid bc)^*$, is the Word Break problem. Backurs and Indyk give a roughly $O(n m^{1/2 - 1/18})$ algorithm, which is subquadratic, and Bringmann, Gronlund and Larsen give an $\tilde O(n m^{1/3} + m)$ algorithm with a matching lower bound for combinatorial algorithms. So for this type the quadratic bound is false.
- **The hypothesis.** The bound is conditional. It does not hold if SETH or OVH fails, and it says nothing about engines with features beyond regular languages: with [backreferences](/backreference-matching/), matching is NP-hard, which is a stronger reason to expect slow worst cases.
- **Small example.** For $A = \{101\}$ the pattern is $0(0 \mid 1)0$. The text for $B = \{011, 010\}$ is $0112010$, and its substring $010$ matches, as $101 \cdot 010 = 0$. The text for $B = \{011, 110\}$ is $0112110$, which has no matching substring, and indeed $101 \cdot 011 = 101 \cdot 110 = 1$.

## History

Backurs and Indyk posted the paper on arXiv in November 2015 and presented it at FOCS 2016. They cite the existence of a faster general algorithm as an open problem listed by Galil in 1985. They note that the reduction for type "$\mid\,\cdot\,\mid$" was found independently by Kasper Larsen and Raphael Clifford. The work belongs to a series of SETH-based quadratic lower bounds for sequence problems, including edit distance (Backurs and Indyk, 2015) and longest common subsequence (Abboud, Backurs and Vassilevska Williams, and Bringmann and Kuennemann, 2015), all through Orthogonal Vectors, whose hardness under SETH goes back to Williams (2005). Bringmann, Gronlund and Larsen completed the classification for membership in 2017.

## References
