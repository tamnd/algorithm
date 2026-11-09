---
tag: Z3GZFJ
kind: concept
slug: colexicographic-order
name: Colexicographic order
aliases:
- colex order
- reverse-lexicographic order on sorted sets
- co-lex order
area: combinatorics/generating-combinations
level: core
summary: Order k-subsets by comparing their largest elements first; the basis of the combinatorial number system.
prereqs: [lexicographic-order, k-subset-enumeration]
see_also: [combinatorial-number-system, lexicographic-combinations, next-same-popcount, gospers-hack, combinatorial-ranking-and-unranking, cool-lex-order, fixed-weight-binary-strings, k-subset-enumeration]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Algorithm L in the decreasing notation, the combinatorial number system, and Theorem K, the Kruskal-Katona theorem)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.3, k-element subsets (co-lex ordering, with successor, rank and unrank)
---

Colexicographic order, or colex order, compares two sets at their largest elements first. For two different sets $A$ and $B$ of integers, $A$ comes before $B$ when the largest element of the symmetric difference $A \triangle B$ is in $B$. On $k$-subsets it is the [lexicographic order](/lexicographic-order/) of the elements written in decreasing order. On subsets of $\{0, \ldots, n-1\}$ it is the increasing order of the bitmasks $\sum_{a \in A} 2^a$. Its main property is that the list does not depend on $n$: the first $C(m, k)$ sets are the $k$-subsets of $\{0, \ldots, m-1\}$.

## In plain words

To sort words in a dictionary, you compare the first letters, and you look at the second letters only when the first letters are equal. Colex order does the same thing from the other end. Write each set with its elements in increasing order. Compare the last elements, the largest ones. Look at the next largest elements only when the largest ones are equal.

So all sets whose largest element is $3$ come before all sets whose largest element is $4$. The list grows at its end when you allow larger numbers, and the start of the list never changes. This is why it is easy to give each set a number in this order.

## The idea

**Definition.** Let $A \ne B$ be finite sets of integers. Then $A <_{\text{colex}} B$ if and only if $\max(A \triangle B) \in B$. For two $k$-subsets written in decreasing order, $A = \{c_k > \cdots > c_1\}$ and $B = \{d_k > \cdots > d_1\}$, this is the same as: at the largest index $i$ with $c_i \ne d_i$, we have $c_i < d_i$. In other words, colex order is lexicographic order on the reversed sorted lists. Knuth's notation $c_k \cdots c_2 c_1$ writes the elements in this order, so his "lexicographic order of combinations" is colex order of the sets.

**Bitmasks.** For subsets of $\{0, \ldots, n-1\}$, let $\mathrm{mask}(A) = \sum_{a \in A} 2^a$. The largest element of $A \triangle B$ is the highest bit where the two masks differ. So $A <_{\text{colex}} B$ if and only if $\mathrm{mask}(A) < \mathrm{mask}(B)$. On all subsets, colex order is binary counting order. On $k$-subsets, it is the order of the integers with $k$ one bits, which [Gosper's hack](/gospers-hack/) and the [next same popcount](/next-same-popcount/) step produce.

**No dependence on $n$.** If $\max B \le m - 1 < \max A$, then $B$ comes before $A$. So the $k$-subsets of $\{0, \ldots, m-1\}$ form an initial segment of the colex order of the $k$-subsets of $\{0, \ldots, n-1\}$ for each $n \ge m$. There is one infinite colex list of all finite $k$-subsets of $\{0, 1, 2, \ldots\}$, and each set has a finite position in it. Lexicographic order does not have this property: among the $2$-subsets of $\{0, \ldots, n-1\}$ in lexicographic order, the set $\{1, 2\}$ comes after the $n - 1$ sets $\{0, x\}$, so its position depends on $n$.

**The rank.** Write $A = \{c_1 < c_2 < \cdots < c_k\}$ with $c_1 \ge 0$. The number of $k$-subsets that come before $A$ in colex order is
$$\mathrm{rank}(A) = \binom{c_k}{k} + \binom{c_{k-1}}{k-1} + \cdots + \binom{c_1}{1}.$$
The term $\binom{c_k}{k}$ counts the sets with a largest element less than $c_k$. The other terms count, in the same way, the sets with the same largest element and a smaller rest. This formula is the [combinatorial number system](/combinatorial-number-system/): each integer $N \ge 0$ has exactly one such form, so rank is a bijection from the $k$-subsets of $\{0, 1, 2, \ldots\}$ to the integers $N \ge 0$.

**Relation to lexicographic order.** For $k$-subsets of $\{1, \ldots, n\}$, the map $a \mapsto n + 1 - a$ reverses the order of the elements. It maps colex order to the reverse of lexicographic order. So the lexicographic rank of $A$ is $C(n, k) - 1$ minus the colex rank of its mirror image. See [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).

**Shadows.** The *shadow* of a family $\mathcal{F}$ of $k$-sets is the family of $(k-1)$-sets that are contained in some member of $\mathcal{F}$. The Kruskal-Katona theorem says that among all families of $m$ $k$-sets, the first $m$ sets in colex order have the smallest shadow. Knuth gives it as Theorem K in Section 7.2.1.3, with credit to J. B. Kruskal (1963) and G. Katona (1968).

## Examples

**The $3$-subsets of $\{0, 1, 2, 3, 4\}$.** The table gives each set, its mask and its rank by the formula.

| colex rank | set $c_3 c_2 c_1$ | mask | $\binom{c_3}{3} + \binom{c_2}{2} + \binom{c_1}{1}$ |
| --- | --- | --- | --- |
| 0 | $210$ | $00111$ | $0 + 0 + 0$ |
| 1 | $310$ | $01011$ | $1 + 0 + 0$ |
| 2 | $320$ | $01101$ | $1 + 1 + 0$ |
| 3 | $321$ | $01110$ | $1 + 1 + 1$ |
| 4 | $410$ | $10011$ | $4 + 0 + 0$ |
| 5 | $420$ | $10101$ | $4 + 1 + 0$ |
| 6 | $421$ | $10110$ | $4 + 1 + 1$ |
| 7 | $430$ | $11001$ | $4 + 3 + 0$ |
| 8 | $431$ | $11010$ | $4 + 3 + 1$ |
| 9 | $432$ | $11100$ | $4 + 3 + 2$ |

The masks increase from top to bottom: $7, 11, 13, 14, 19, 21, 22, 25, 26, 28$. The first $4 = C(4, 3)$ rows are the $3$-subsets of $\{0, 1, 2, 3\}$.

**Lexicographic and colex order side by side.** The $2$-subsets of $\{1, 2, 3, 4\}$ are $12, 13, 14, 23, 24, 34$ in lexicographic order and $12, 13, 23, 14, 24, 34$ in colex order. The set $14$ comes before $23$ in lexicographic order, because $1 < 2$, and after it in colex order, because $4 > 3$.

**A shadow.** The first $5$ sets in the colex order of $3$-sets are $210, 310, 320, 321, 410$. Their shadow is $\{01, 02, 12, 03, 13, 23, 04, 14\}$, with $8$ pairs. The family $\{012, 013, 014, 015, 016\}$ also has $5$ sets, but its shadow has $11$ pairs.

## Where it is used

- **Ranking and indexing.** The rank formula above is the [combinatorial number system](/combinatorial-number-system/). It stores a $k$-subset as one integer, with no dependence on $n$. Compressed bit vectors such as the [RRR bit vector](/rrr-bitvector/) use this kind of index.
- **Bit tricks.** Colex order of $k$-subsets is the increasing order of the masks with $k$ one bits, so a loop with [Gosper's hack](/gospers-hack/) visits them in colex order in $O(1)$ word operations for each set.
- **Generation.** Knuth's Algorithm L and Algorithm T list combinations in this order, see [lexicographic combinations](/lexicographic-combinations/). [Cool-lex order](/cool-lex-order/) is a different order that also has the property that the start of the list does not depend on $n$.
- **Extremal set theory.** The Kruskal-Katona theorem and its use in the study of shadows, of antichains and of the face numbers of simplicial complexes rest on colex order.
- **Dynamic programming over subsets.** A loop over masks in increasing order visits each subset after all of its proper subsets, because a proper subset has a smaller mask. [Bitmask DP](/bitmask-dp/) uses this.

## References
