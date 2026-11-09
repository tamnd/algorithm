---
tag: EGKQSH
kind: problem
slug: combinations-with-repetition
name: Enumerating combinations with repetition
aliases:
- multisets of size k
- multiset combinations
- multicombinations
- k-multisets
area: combinatorics/generating-combinations
level: core
summary: List all multisets of size k drawn from an n-element set; there are C(n+k-1,k) of them.
complexity:
  vars: {n: the number of kinds, k: the size of each multiset, N: the number of multisets}
  time: {worst: Ω(N)}
prereqs: [k-subset-enumeration, stars-and-bars]
see_also: [stars-and-bars, k-subset-enumeration, lexicographic-combinations, integer-compositions, composition-generation, multiset-permutations, monomial, combinatorial-ranking-and-unranking]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (multicombinations, and their correspondence with combinations and with compositions)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.2, Sets and multisets (the number of k-multisets of an n-set)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Chapter 5, Binomial coefficients (choosing with repetitions)
---

The problem asks for a list of all multisets of size $k$ whose elements come from an $n$-element set, each exactly once. A multiset can hold an element more than once, and the order of its elements does not matter. There are $\left(\!\binom{n}{k}\!\right) = C(n + k - 1, k)$ of them. The map $b_i \mapsto b_i + i - 1$ turns them into the [k-subsets](/k-subset-enumeration/) of $[n + k - 1]$, so each generator of combinations also generates multisets, with the same cost.

## In plain words

A shop sells $n$ kinds of donuts, and you buy a box of $k$. You can take several donuts of one kind. Two boxes are the same if they hold the same number of each kind. You want to see every possible box once.

Write each box as a sorted list of kinds, for example $1, 1, 3$. Then go through these lists as a dictionary does. A second view is "stars and bars": draw one star for each donut and put a bar between two kinds. Each box is one row of $k$ stars and $n - 1$ bars, so the task is to choose where the bars go.

## Definition

Let $n \ge 1$ and $k \ge 0$. A $k$-multiset of $[n] = \{1, \ldots, n\}$ is a function $m : [n] \to \{0, 1, 2, \ldots\}$ with $m(1) + \cdots + m(n) = k$. The value $m(j)$ is the multiplicity of $j$. Let $N = C(n + k - 1, k)$.

**Input.** The integers $n$ and $k$.

**Output.** A sequence of all $N$ $k$-multisets of $[n]$, each exactly once.

**Representations.**

- *A weakly increasing list* $b_1 \le b_2 \le \cdots \le b_k$ with each $b_i \in [n]$.
- *A multiplicity vector* $(m_1, \ldots, m_n)$ of non-negative integers with sum $k$. This is a weak composition of $k$ into $n$ parts, see [integer compositions](/integer-compositions/).
- *A stars and bars string* of length $n + k - 1$ with $k$ stars and $n - 1$ bars: $m_1$ stars, a bar, $m_2$ stars, a bar, and so on. See [stars and bars](/stars-and-bars/).

**The count.** The stars and bars strings are the ways to choose the $k$ star positions among $n + k - 1$, so $N = C(n + k - 1, k) = C(n + k - 1, n - 1)$.

**Edge cases.** For $k = 0$ there is one multiset, the empty one. For $n = 0$ and $k \ge 1$ there is none.

## Variants

- **Lexicographic order.** List the increasing lists $b$ in lexicographic order. The successor finds the rightmost $b_i < n$, adds $1$ to it, and sets all entries to its right equal to the new $b_i$.
- **Order of the multiplicity vectors.** List the vectors $m$ in lexicographic or reverse lexicographic order. This is [composition generation](/composition-generation/) with parts of size $0$ allowed.
- **Gray codes.** Each step moves one copy from one kind to another, that is, $m_i$ goes down by $1$ and $m_j$ goes up by $1$. A revolving door order for the $k$-subsets of $[n + k - 1]$ gives such a list through the stars and bars string.
- **Bounded multiplicities.** Each $m_j$ is at most a given $u_j$. The count is no longer a single binomial, and the list is a subset of the multisets above.
- **All arrangements.** If the order of the elements matters, the objects are words, and the arrangements of one multiset are the [multiset permutations](/multiset-permutations/), counted by the [multinomial coefficient](/multinomial-coefficient/).

## Examples

**$n = 3$, $k = 2$.** There are $C(4, 2) = 6$ multisets.

| $b$ | multiplicities $m$ | stars and bars | $\{b_i + i - 1\}$ |
| --- | --- | --- | --- |
| $1, 1$ | $(2, 0, 0)$ | $\star \star \mid \mid$ | $\{1, 2\}$ |
| $1, 2$ | $(1, 1, 0)$ | $\star \mid \star \mid$ | $\{1, 3\}$ |
| $1, 3$ | $(1, 0, 1)$ | $\star \mid \mid \star$ | $\{1, 4\}$ |
| $2, 2$ | $(0, 2, 0)$ | $\mid \star \star \mid$ | $\{2, 3\}$ |
| $2, 3$ | $(0, 1, 1)$ | $\mid \star \mid \star$ | $\{2, 4\}$ |
| $3, 3$ | $(0, 0, 2)$ | $\mid \mid \star \star$ | $\{3, 4\}$ |

The last column lists the $2$-subsets of $[4]$ in lexicographic order, in the same order as the first column.

**$n = 3$, $k = 3$.** The $C(5, 3) = 10$ multisets in lexicographic order are $111, 112, 113, 122, 123, 133, 222, 223, 233, 333$.

**Sizes.** A box of $12$ donuts from $5$ kinds is one of $C(16, 12) = 1820$ boxes. A roll of $3$ dice with $6$ faces, when the dice are not told apart, has $C(8, 3) = 56$ outcomes.

## Known algorithms

| algorithm | representation | time for each multiset | page |
| --- | --- | --- | --- |
| lexicographic successor on $b$ | increasing list | $O(1 + k/n)$ amortized | this page |
| any $k$-subset generator on $[n + k - 1]$, then $c_i \mapsto c_i - i + 1$ | increasing list | same as the generator | [k-subset enumeration](/k-subset-enumeration/) |
| a loopless $k$-subset generator on the stars and bars string | bit string | $O(1)$ worst case | [cool-lex order](/cool-lex-order/) |
| composition generators with zero parts | multiplicity vector | $O(1)$ amortized | [composition generation](/composition-generation/) |
| unrank each rank | any ranked order | $O(n + k)$ arithmetic operations | [ranking and unranking combinations](/combinatorial-ranking-and-unranking/) |

**The cost of the successor.** The scan from the right passes over the trailing entries equal to $n$. The multisets whose last $d$ entries equal $n$ are the $(k - d)$-multisets of $[n]$ followed by $d$ copies of $n$, so there are $C(n + k - d - 1, k - d)$ of them. Summed over $d = 1, \ldots, k$, the [hockey stick identity](/hockey-stick-identity/) gives $C(n + k - 1, k - 1)$ scan steps in total. This is $N \cdot k/n$, so the successor takes $O(1 + k/n)$ amortized time for each multiset. It is CAT when $k = O(n)$. When $k$ is much larger than $n$, generate the multiplicity vectors instead.

## Bounds

- **Lower bound.** Each algorithm takes $\Omega(N)$ time, because there are $N$ outputs.
- **Changes.** Two different $k$-multisets differ in at least two multiplicities, one up and one down. A Gray code that moves one copy at each step meets this bound, so loopless generation in $O(1)$ worst-case time for each multiset is possible through the stars and bars string.

## Reductions

- **To $k$-subsets.** The map $b \mapsto \{b_1, b_2 + 1, \ldots, b_k + k - 1\}$ is a bijection from the $k$-multisets of $[n]$ to the $k$-subsets of $[n + k - 1]$. It keeps lexicographic and colexicographic order, so it also gives rank and unrank.
- **To fixed-weight strings.** The stars and bars string is a [fixed-weight binary string](/fixed-weight-binary-strings/) of length $n + k - 1$ with $k$ ones.
- **To compositions.** The multiplicity vector is a weak composition of $k$ into $n$ parts. Adding $1$ to each part gives a composition of $n + k$ into $n$ positive parts.
- **To lattice paths.** The stars and bars string is a monotone lattice path with $k$ steps of one kind and $n - 1$ of the other. See [counting lattice paths](/counting-lattice-paths/).

## Applications

- **Monomials.** The monomials of degree $k$ in $n$ variables, $x_1^{m_1} \cdots x_n^{m_n}$ with $\sum m_j = k$, are the $k$-multisets of $[n]$. Polynomial algebra and polynomial regression list them, see [monomial](/monomial/).
- **Integer solutions.** The solutions of $x_1 + \cdots + x_n = k$ in non-negative integers are the multiplicity vectors.
- **Occupancy.** The ways to put $k$ identical balls into $n$ boxes are the $k$-multisets of $[n]$. In physics this count gives the Bose-Einstein statistics.
- **Unordered outcomes.** The outcomes of $k$ identical dice, or of $k$ draws with replacement when the order does not matter.

## References
