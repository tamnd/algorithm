---
tag: 3X02J1
kind: concept
slug: inversion-table
name: Inversion table
aliases:
- Knuth inversion table
area: sequences/inversions-and-permutations
level: core
summary: For each value, the count of larger elements to its left; this is a bijection with permutations.
prereqs: [permutation, inversion]
see_also: [lehmer-code, permutation-inverse, insertion-sort, bubble-sort, mahonian-numbers, expected-number-of-inversions, fenwick-tree, factorial-number-system]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (the inversion table b_1 ... b_n, its bijection with permutations, and its use in the analysis of sorting) and Section 5.2.2 (bubble sort and the inversion table)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (inversion tables and the generating function of inversions)
---

The inversion table of a [permutation](/permutation/) $a$ of $[n]$ is the sequence $b_1 b_2 \cdots b_n$ in which $b_j$ counts the values larger than $j$ that stand to the left of the value $j$. It is indexed by values, where the [Lehmer code](/lehmer-code/) is indexed by positions, and it is exactly the Lehmer code of the [inverse permutation](/permutation-inverse/). Each $b_j$ lies between $0$ and $n - j$, every such sequence is the table of exactly one permutation, and the entries add up to the number of [inversions](/inversion/). Knuth uses it to analyze [insertion sort](/insertion-sort/) and [bubble sort](/bubble-sort/), because $b_j$ is the number of places the value $j$ must move to the right.

## In plain words

Take a shuffled list of the numbers 1 to $n$. For the number 1, count how many numbers stand before it; all of them are bigger. For the number 2, count the bigger numbers before it, and so on. The last number $n$ always gets 0, since nothing is bigger.

The counts tell you how to rebuild the list. Start with the biggest number alone. Put the next biggest number into the list so that the right count of bigger numbers is in front of it. Keep going down to 1.

Each out-of-order pair is a bigger number in front of a smaller one, and it is counted once, at the smaller number. So the counts add up to the number of out-of-order pairs, and each count says how far that number is held back from its sorted place.

## The idea

**Definition.** For a permutation $a = a_1 \cdots a_n$ of $[n]$ and $1 \le j \le n$,
$$b_j = |\{\, i : a_i > j \text{ and } a_i \text{ is to the left of } j \,\}|.$$
Only the $n - j$ values $j + 1, \ldots, n$ can be counted, so $0 \le b_j \le n - j$. Each inversion, a larger value before a smaller value, is counted at its smaller value and nowhere else, so $b_1 + \cdots + b_n = \operatorname{inv}(a)$.

**Theorem.** The map $a \mapsto b$ is a bijection from $S_n$ onto $\{0, \ldots, n-1\} \times \{0, \ldots, n-2\} \times \cdots \times \{0\}$.

*Proof.* Both sets have $n!$ elements, so it is enough to rebuild $a$ from $b$. Build the list by inserting the values $n, n-1, \ldots, 1$ in this order. When $j$ is inserted, the values already in the list are exactly the values larger than $j$, in the same relative order as in $a$, and $j$ must have exactly $b_j$ of them to its left. That fixes the place of $j$: index $b_j$ of the current list, counted from 0. This insertion is possible because the list has $n - j \ge b_j$ items. At the end, the list is $a$. $\square$

**Relation to the Lehmer code.** A value $v > j$ stands to the left of $j$ in $a$ exactly when $a^{-1}(v) < a^{-1}(j)$. Read in the sequence $a^{-1}$, this says that position $v$ is to the right of position $j$ and holds a smaller entry. So $b_j$ counts the smaller entries to the right of position $j$ in $a^{-1}$:
$$b(a) = c(a^{-1}),$$
where $c$ is the Lehmer code. The two codes are exchanged by taking the inverse.

**Decoding from left to right.** Place the values $1, 2, \ldots, n$ in increasing order into $n$ empty slots. When $j$ is placed, every slot still empty will get a value larger than $j$, so $j$ goes into the $(b_j + 1)$-th empty slot from the left. With a [Fenwick tree](/fenwick-tree/) over the slots and a binary descent to find the $k$-th empty slot, decoding takes $O(n \log n)$ time. Encoding also takes $O(n \log n)$ time: scan $a$ from left to right and, for each value $j$, count the values larger than $j$ seen so far with a prefix sum.

**Sorting algorithms read off the table.**

- **Insertion sort.** Straight [insertion sort](/insertion-sort/) inserts each value past exactly the larger values to its left, so it moves the value $j$ over $b_j$ items, and the total number of moves is $\sum_j b_j = \operatorname{inv}(a)$.
- **Bubble sort.** One left-to-right pass of [bubble sort](/bubble-sort/) turns the table $b$ into $(\max(b_1 - 1, 0), \ldots, \max(b_n - 1, 0))$: a value with a larger value to its left has exactly one of the larger values carried past it in that pass. So the number of passes that make an exchange is $\max_j b_j$, and Knuth computes the distribution of the number of passes from this fact.
- **Random input.** For a uniform permutation, the $b_j$ are independent and $b_j$ is uniform on $\{0, \ldots, n - j\}$, by the bijection. This gives the [expected number of inversions](/expected-number-of-inversions/) and the generating function $\prod_{k=1}^{n} (1 + z + \cdots + z^{k-1})$ of the [Mahonian numbers](/mahonian-numbers/).

## Examples

**Encoding.** For $a = 3\,1\,4\,5\,2$: the value 1 has the 3 to its left, the value 2 has 3, 4 and 5, and the values 3, 4 and 5 have no larger value to their left. So
$$b = (1, 3, 0, 0, 0), \qquad \operatorname{inv}(a) = 4.$$
The Lehmer code of $a$ is $(2, 0, 1, 1, 0)$, a different sequence with the same sum. The inverse $a^{-1} = 2\,5\,1\,3\,4$ has Lehmer code $(1, 3, 0, 0, 0) = b$.

**Decoding by insertion.** From $b = (1, 3, 0, 0, 0)$: insert 5 to get $5$; insert 4 at index 0 to get $4\,5$; insert 3 at index 0 to get $3\,4\,5$; insert 2 at index 3 to get $3\,4\,5\,2$; insert 1 at index 1 to get $3\,1\,4\,5\,2$.

**Decoding into slots.** From the same table: 1 goes to the 2nd empty slot, slot 2; 2 goes to the 4th empty slot of $\{1, 3, 4, 5\}$, slot 5; then 3, 4 and 5 go to the first empty slots 1, 3 and 4. The result is again $3\,1\,4\,5\,2$.

**Bubble sort.** The table $(1, 3, 0, 0, 0)$ has maximum 3, so bubble sort makes exchanges in exactly 3 passes. After the first pass the list is $1\,3\,4\,2\,5$, with table $(0, 2, 0, 0, 0)$.

**A longer one.** $a = 5\,9\,1\,8\,2\,6\,4\,7\,3$ has the table $(2, 3, 6, 4, 0, 2, 2, 1, 0)$ and 20 inversions. The entry $b_3 = 6$ says that 3 has the six values 5, 9, 8, 6, 4, 7 before it, all larger.

## Where it is used

- **Analysis of sorting.** The table records how far each value must travel in insertion sort and how many passes bubble sort makes, and the independence of its entries gives exact average costs.
- **Encoding permutations.** Like the Lehmer code, the table is a mixed-radix number that names a permutation, so it can serve for [ranking](/permutation-rank-unrank/), with the [factorial number system](/factorial-number-system/) read in the order $b_1, \ldots, b_n$.
- **Combinatorics.** Statistics of permutations that are defined by values, such as the inversions at each value, become statistics of sequences in a product set.
- **Random generation.** Choosing each $b_j$ uniformly on $\{0, \ldots, n - j\}$ and decoding gives a uniform [random permutation](/random-permutation/), which is the idea of building a list by inserting items at random places.

## References
