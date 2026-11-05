---
tag: X8KSF0
kind: concept
slug: lehmer-code
name: Lehmer code
aliases:
- inversion sequence
- inversion table code
- permutation code
area: sequences/inversions-and-permutations
level: core
summary: Encodes a permutation as a sequence where entry i counts smaller elements to its right.
prereqs: [permutation, inversion]
see_also: [inversion-table, factorial-number-system, permutation-rank-unrank, lexicographic-successor, expected-number-of-inversions, inversion-count-with-fenwick-tree, random-permutation, descents]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversion tables, the bijection with sequences 0 <= b_j <= n - j, and the generating function of inversions)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (generating all permutations, and permutations as mixed-radix numbers)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (inversion tables and the distribution of the number of inversions)
---

The Lehmer code of a [permutation](/permutation/) $a_1 a_2 \cdots a_n$ is the sequence $c_1 c_2 \cdots c_n$ in which $c_i$ counts the items to the right of position $i$ that are smaller than $a_i$. Each $c_i$ lies between $0$ and $n - i$, and every sequence in that range is the code of exactly one permutation, so the code is a bijection between $S_n$ and the numbers of the [factorial number system](/factorial-number-system/). The sum of the code is the number of [inversions](/inversion/), lexicographic order of permutations is numeric order of their codes, and the entries are independent for a random permutation. It is named after D. H. Lehmer, who used it to rank permutations.

## In plain words

Write down, for each item of a list, how many smaller items come after it. The last item gets 0, since nothing comes after it. The item before the last gets 0 or 1, and so on: the item in place $i$ from the left can have at most as many smaller items after it as there are places after it.

These numbers are a full description of the list. To rebuild it, look at the first number: if it says 2, the first item is the third smallest of all items, because exactly two smaller ones come later. Cross that item off and repeat with the next number and the items that are left.

The numbers also add up to the count of out-of-order pairs, since each such pair is counted once, at its left item.

## The idea

**Definition.** For a sequence $a = (a_1, \ldots, a_n)$ of distinct items, the Lehmer code is
$$c_i = |\{\, j > i : a_j < a_i \,\}|, \qquad 1 \le i \le n.$$
Each inversion $(i, j)$ is counted in $c_i$ and nowhere else, so $c_1 + \cdots + c_n = \operatorname{inv}(a)$. Since there are $n - i$ positions after $i$, $0 \le c_i \le n - i$.

**Theorem.** The map $a \mapsto c$ is a bijection from the permutations of $[n]$ onto
$$C_n = \{0, \ldots, n-1\} \times \{0, \ldots, n-2\} \times \cdots \times \{0, 1\} \times \{0\}.$$

*Proof.* Both sets have $n!$ elements, so it is enough to show that $c$ determines $a$. The items after position $i$ are exactly the items not among $a_1, \ldots, a_{i-1}$ other than $a_i$ itself. So $a_i$ is the item of $U_i = [n] \setminus \{a_1, \ldots, a_{i-1}\}$ with exactly $c_i$ smaller items of $U_i$, which is the $(c_i + 1)$-th smallest item of $U_i$. This fixes $a_1$, then $a_2$, and so on. $\square$

The proof is also the decoding algorithm:

```pseudo
DECODE(c[1 .. n])
1  U ← the sorted list 1, 2, .., n
2  for i ← 1 to n do
3      a[i] ← the item at index c[i] of U        ▷ indices start at 0
4      remove that item from U
5  return a
```

**Computing the code.** Directly from the definition the code takes $\Theta(n^2)$ time. Scanning from right to left with a [Fenwick tree](/fenwick-tree/) over the values gives each $c_i$ as a prefix count of the values already seen, in $O(n \log n)$ time in total, as in [inversion counting with a Fenwick tree](/inversion-count-with-fenwick-tree/). [Merge sort](/inversion-count-by-merge-sort/) gives all the $c_i$ in the same time, as counts of the smaller items that overtake each item. Decoding needs the $k$-th smallest remaining item, which a Fenwick tree with a binary descent or an [order-statistic tree](/order-statistic-tree/) finds in $O(\log n)$ time, so both directions take $O(n \log n)$ time.

**What the code shows.**

- **Rank.** Reading $c$ as a number in the factorial base gives the position of $a$ in lexicographic order, counted from 0:
$$\operatorname{rank}(a) = \sum_{i=1}^{n} c_i\,(n-i)!.$$
Of the permutations that agree with $a$ before position $i$, the ones with a smaller item at position $i$ number $c_i \cdot (n-i)!$, since there are $c_i$ smaller choices and $(n-i)!$ ways to finish each. See [permutation rank and unrank](/permutation-rank-unrank/).
- **Lexicographic order.** For permutations $a \ne b$, $a < b$ in lexicographic order exactly when $c(a) < c(b)$ in lexicographic order, since the first position where the codes differ is the first position where the permutations differ. The [lexicographic successor](/lexicographic-successor/) adds 1 to the code with carries.
- **Descents.** $a_i > a_{i+1}$ exactly when $c_i > c_{i+1}$. If $a_i > a_{i+1}$, then $a_{i+1}$ and every item smaller than $a_{i+1}$ to its right are counted in $c_i$, so $c_i \ge c_{i+1} + 1$. If $a_i < a_{i+1}$, every item counted in $c_i$ is to the right of $i + 1$ and smaller than $a_{i+1}$, so $c_i \le c_{i+1}$. So the [descents](/descents/) of $a$ are the descents of its code.
- **Right-to-left minima.** $c_i = 0$ exactly when $a_i$ is smaller than every item to its right.
- **Random permutations.** A uniform permutation has a uniform code in the product set $C_n$, so $c_1, \ldots, c_n$ are independent and $c_i$ is uniform on $\{0, \ldots, n - i\}$. This gives the mean $n(n-1)/4$ and the variance of the inversion count in [expected number of inversions](/expected-number-of-inversions/), and the generating function $\prod_{k=1}^{n} (1 + z + \cdots + z^{k-1})$ of the [Mahonian numbers](/mahonian-numbers/). Choosing the $c_i$ independently and decoding is a way to build a [random permutation](/random-permutation/).
- **The inverse.** The Lehmer code of $a^{-1}$ is Knuth's [inversion table](/inversion-table/) of $a$, which counts for each value the larger values to its left.

**Conventions.** Some books count smaller items to the left, larger items to the right, or index the code from the right end, and some call the Lehmer code the inversion table or the inversion sequence. All these versions are bijections with $C_n$ or its reverse and carry the same information. This page uses smaller items to the right, which makes the rank formula above hold.

## Examples

**Encoding.** For $a = 3\,1\,4\,5\,2$: the 3 has the smaller items 1 and 2 after it, the 1 has none, the 4 has the 2, the 5 has the 2, and the last item has none. So
$$c = (2, 0, 1, 1, 0), \qquad \operatorname{inv}(a) = 4, \qquad \operatorname{rank}(a) = 2 \cdot 24 + 0 \cdot 6 + 1 \cdot 2 + 1 \cdot 1 + 0 = 51.$$

**Decoding.** From $c = (2, 0, 1, 1, 0)$ and $U = \{1, 2, 3, 4, 5\}$: index 2 of $U$ is 3, leaving $\{1, 2, 4, 5\}$; index 0 is 1, leaving $\{2, 4, 5\}$; index 1 is 4, leaving $\{2, 5\}$; index 1 is 5, leaving $\{2\}$; index 0 is 2. The result is $3\,1\,4\,5\,2$.

**Descents in the code.** $a = 3\,1\,6\,2\,5\,4$ has code $(2, 0, 3, 0, 1, 0)$ and 6 inversions. The descents of $a$ are at positions 1, 3 and 5, and so are the descents of the code: $2 > 0$, $3 > 0$, $1 > 0$.

**The extremes.** The identity has code $(0, \ldots, 0)$ and rank 0. The reversal $n \cdots 2\,1$ has code $(n-1, n-2, \ldots, 0)$, the largest in $C_n$, with $\binom n2$ inversions and rank $n! - 1$.

**All of $S_3$.** In lexicographic order, $123, 132, 213, 231, 312, 321$ have the codes $000, 010, 100, 110, 200, 210$, which are $0, 1, \ldots, 5$ in the factorial base with digit weights $2, 1, 1$.

## Where it is used

- **[Ranking and unranking](/permutation-rank-unrank/).** The code turns a permutation into its index among all $n!$ permutations and back, which is used to store a permutation as one integer, to index tables by permutations, and to sample.
- **Counting inversions.** The sum of the code is the inversion count, and the per-item counts are the answer to "count the smaller items after each item".
- **Analysis of sorting.** [Insertion sort](/insertion-sort/) run from the right moves each item past exactly $c_i$ smaller items, and the independence of the $c_i$ gives its exact average cost. Knuth uses the equivalent inversion table for the same purpose.
- **Combinatorics of permutations.** The code transports statistics such as inversions, descents and right-to-left minima to sequences in $C_n$, where they are easier to count.
- **Search and puzzles.** Programs that store the states of a permutation puzzle in an array index each state by its rank, computed from the code.

## References
