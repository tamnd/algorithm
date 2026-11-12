---
tag: PY07JM
kind: definition
slug: catalan-numbers
name: Catalan numbers
aliases:
- Catalan sequence
- Catalan number
area: combinatorics/counting-algorithms
level: intro
summary: Count binary trees, Dyck paths and many other structures.
prereqs: [binomial-coefficient]
see_also: [dyck-word, binary-tree, balanced-parentheses, ballot-theorem, cycle-lemma, catalan-triangulation-theorem, counting-parenthesizations, stack-sortable-permutations]
sources:
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 1, Basic properties, and Chapter 2, Bijective exercises (the list of combinatorial interpretations)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5, Convolutions (the Catalan numbers from the generating function, and Raney's lemma)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.3.4.4, Enumeration of trees (the number of binary trees with n nodes)
---

The Catalan numbers $C_n = \frac{1}{n+1}\binom{2n}{n}$, for $n = 0, 1, 2, \ldots$, are $1, 1, 2, 5, 14, 42, 132, 429, \ldots$. They count the balanced strings of $n$ pairs of parentheses, the binary trees with $n$ nodes, the triangulations of a convex polygon with $n + 2$ sides, and more than two hundred other families of objects. They satisfy the recurrence $C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}$, which is the reason they appear whenever an object splits into a left part and a right part. They grow as $4^n/(n^{3/2}\sqrt{\pi})$.

## Definition

Notation: $\binom{a}{b}$ is the [binomial coefficient](/binomial-coefficient/). A **Dyck word** of semilength $n$ is a string of $n$ letters U and $n$ letters D in which every prefix has at least as many U as D. Drawn with U as a step $(1, 1)$ and D as a step $(1, -1)$, it is a **Dyck path**: a lattice path from $(0, 0)$ to $(2n, 0)$ that never goes below the horizontal axis. Written with "(" for U and ")" for D, it is a string of [balanced parentheses](/balanced-parentheses/); see [Dyck word](/dyck-word/).

**Definition.** The $n$-th **Catalan number** is
$$C_n = \frac{1}{n+1}\binom{2n}{n} = \binom{2n}{n} - \binom{2n}{n+1} = \frac{(2n)!}{n!\,(n+1)!}, \qquad n \ge 0.$$
The three expressions are equal, since $\binom{2n}{n+1} = \frac{n}{n+1}\binom{2n}{n}$.

**Theorem 1 (Dyck paths).** The number of Dyck words of semilength $n$ is $C_n$.

*Proof (reflection).* All strings with $n$ U and $n$ D number $\binom{2n}{n}$. Call a string bad if some prefix has more D than U, and let $t$ be the first step where the path reaches height $-1$. Swap U and D in the steps after $t$. The path after $t$ went from $-1$ to $0$, so the new path goes from $-1$ to $-2$, and the new string has $n - 1$ U and $n + 1$ D. Conversely, every string with $n - 1$ U and $n + 1$ D ends at height $-2$, so it reaches height $-1$, and the same swap after its first visit there gives a bad string back. The two maps are inverse, so the bad strings number $\binom{2n}{n+1}$, and the good ones $\binom{2n}{n} - \binom{2n}{n+1} = C_n$. This is the [reflection principle](/reflection-principle/). $\square$

**Theorem 2 (recurrence).** $C_0 = 1$ and $C_{n+1} = \sum_{i=0}^{n} C_i\,C_{n-i}$ for $n \ge 0$. Also $C_{n+1} = \frac{2(2n+1)}{n+2}\,C_n$.

*Proof.* A nonempty Dyck word $w$ of semilength $n + 1$ starts with U. Let the matching D be the first return of the path to height 0. Then $w = \mathrm{U}\,u\,\mathrm{D}\,v$, where $u$ and $v$ are Dyck words, of semilengths $i$ and $n - i$ for some $0 \le i \le n$. This first-return split is a bijection, so by the [rule of sum](/rule-of-sum/) and the [rule of product](/rule-of-product/) the count is $\sum_i C_i C_{n-i}$. The second form follows from the formula: $\frac{C_{n+1}}{C_n} = \frac{(2n+2)(2n+1)}{(n+1)(n+2)} = \frac{2(2n+1)}{n+2}$. $\square$

**Theorem 3 (generating function).** $C(x) = \sum_{n \ge 0} C_n x^n$ satisfies $C(x) = 1 + x\,C(x)^2$, so $C(x) = \frac{1 - \sqrt{1 - 4x}}{2x}$.

*Proof.* The recurrence says that the coefficient of $x^{n+1}$ in $x\,C(x)^2$ is $C_{n+1}$, and the constant terms agree. The quadratic has two roots, and only the one with the minus sign is a power series, since the other has a term $1/x$. $\square$

**Cost model.** $C_n$ has about $2n - \tfrac32\log_2 n$ bits, so exact values need big integers: $C_{36} < 2^{64} < C_{37}$, and $C_{100}$ has 190 bits (57 decimal digits). The ratio form computes $C_0, \ldots, C_n$ exactly in $n$ steps, each a multiplication and an exact division of a number of $O(n)$ bits by a small number. Modulo a prime $p > 2n$, a table of factorials gives $C_n \bmod p$ in $O(n)$ operations on residues; the convolution recurrence needs $O(n^2)$ operations but no division, so it works modulo any $m$. See [computing binomial coefficients](/binomial-coefficient-computation/).

## Examples and non-examples

**Example 1 (values).** $C_0, \ldots, C_{15}$ are $1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440, 9694845$ (OEIS A000108). Also $C_{20} = 6564120420$, $C_{30} = 3814986502092304$, and $C_{10^6} \bmod (10^9 + 7) = 70646122$.

**Example 2 (parentheses, $n = 3$).** The five Dyck words are `((()))`, `(()())`, `(())()`, `()(())` and `()()()`. Of the $\binom{6}{3} = 20$ strings with three of each symbol, $\binom{6}{4} = 15$ are bad, and $20 - 15 = 5$.

**Example 3 (binary trees).** The [binary trees](/binary-tree/) with $n$ nodes number $C_n$: a nonempty tree is a root with a left subtree of $i$ nodes and a right subtree of $n - 1 - i$ nodes, which is the recurrence of theorem 2. So there are 5 binary trees with 3 nodes, and $C_n$ shapes of a [binary search tree](/binary-search-tree/) on $n$ keys. Adding leaves to every free child slot gives the full binary trees with $n + 1$ leaves, also $C_n$ of them.

**Example 4 (products).** A product $x_0 x_1 \cdots x_n$ of $n + 1$ factors can be fully parenthesized in $C_n$ ways; for four factors: $((ab)c)d$, $(a(bc))d$, $(ab)(cd)$, $a((bc)d)$, $a(b(cd))$. This is why trying every order in [matrix chain multiplication](/matrix-chain-multiplication/) is exponential; see [counting parenthesizations](/counting-parenthesizations/).

**Example 5 (triangulations).** A convex polygon with $n + 2$ vertices has $C_n$ triangulations by diagonals that do not cross: 5 for a pentagon, 14 for a hexagon and 132 for an octagon. The edge from vertex 1 to vertex $n + 2$ lies in one triangle, whose third vertex splits the polygon into two smaller ones, which gives the recurrence; see the [triangulation theorem](/catalan-triangulation-theorem/).

**Example 6 (stack sorting).** The permutations of $[n]$ that one pass through a [stack](/stack/) can sort are those with no pattern $231$, and they number $C_n$; see [stack-sortable permutations](/stack-sortable-permutations/). For $n = 3$, all permutations except $231$ itself, so 5 of 6.

**Example 7 (parity and size).** $C_n$ is odd exactly when $n + 1$ is a power of 2: the odd values for $n \le 70$ are at $n = 0, 1, 3, 7, 15, 31, 63$. (By Kummer's theorem, the power of 2 in $C_n = \binom{2n+1}{n}/(2n+1)$ is the number of carries when $n$ and $n + 1$ are added in base 2, and there is no carry only when $n = 2^k - 1$.) The ratio $C_n\big/\bigl(4^n n^{-3/2}\pi^{-1/2}\bigr)$ is $0.898$ for $n = 10$ and $0.989$ for $n = 100$; it tends to 1 by [Stirling's approximation](/stirling-approximation/).

**Non-example 1 (all paths).** The central binomial coefficient $\binom{2n}{n}$ counts all paths with $n$ up and $n$ down steps, with no condition on the prefixes: $1, 2, 6, 20, 70$. It is $(n + 1)C_n$, not $C_n$.

**Non-example 2 (Bell numbers).** The [Bell numbers](/bell-numbers/) $1, 1, 2, 5, 15, 52$ agree with $C_0, \ldots, C_3$ and then differ: $15 \ne 14$. The partitions of $[n]$ with no crossing blocks are counted by $C_n$, and for $n = 4$ the only partition with a crossing is $\{1, 3\}, \{2, 4\}$.

**Non-example 3 (Motzkin numbers).** Paths from $(0, 0)$ to $(n, 0)$ with steps up, down and level that never go below the axis number $1, 1, 2, 4, 9, 21, 51$, the Motzkin numbers. Level steps break the U and D pairing of Dyck words.

**Non-example 4 (ternary trees).** Trees in which each node has a left, a middle and a right subtree number $\frac{1}{2n+1}\binom{3n}{n}$: $1, 1, 3, 12, 55, 273$. These are Fuss-Catalan numbers, not Catalan numbers.

## Related definitions

- **Cycle form.** $C_n = \frac{1}{2n+1}\binom{2n+1}{n}$: of the $2n + 1$ rotations of a string with $n + 1$ U and $n$ D, exactly one has every proper prefix with more U than D. This is the [cycle lemma](/cycle-lemma/), and its general form gives the Fuss-Catalan numbers $\frac{1}{(m-1)n+1}\binom{mn}{n}$ for $m$-ary trees.
- **Ballot numbers.** The paths that stay strictly above the axis after the start, with $a$ up and $b$ down steps, number $\frac{a - b}{a + b}\binom{a + b}{a}$ by the [ballot theorem](/ballot-theorem/); $C_n$ is the case $a = n + 1$, $b = n$. The ballot numbers $\frac{n - k + 1}{n + 1}\binom{n + k}{k}$ form Catalan's triangle, whose diagonal is $C_n$.
- **Narayana numbers.** $N(n, k) = \frac{1}{n}\binom{n}{k}\binom{n}{k-1}$ counts the Dyck words of semilength $n$ with $k$ peaks (a U followed by a D), and $\sum_k N(n, k) = C_n$; for $n = 4$ the values are $1, 6, 6, 1$.
- **Dyck language.** The set of all Dyck words is the [Dyck language](/dyck-language/), the standard example of a context-free language that is not regular.
- **Lattice paths.** Dyck paths are the monotone [lattice paths](/counting-lattice-paths/) from $(0, 0)$ to $(n, n)$ that stay on one side of the diagonal, after a rotation by 45 degrees.

## References
