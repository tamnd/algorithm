---
tag: VGKM5B
kind: definition
slug: lexicographic-order
name: Lexicographic order
aliases:
- Lexicographic order on combinations
- alphabetical order
- dictionary order
- lex order
area: combinatorics/generating-permutations
level: intro
summary: Order sequences by their first differing element, used to list permutations in a canonical sequence.
prereqs: [total-order]
see_also: [colexicographic-order, total-order, lexicographic-permutation-successor, lexicographic-combinations, next-permutation, string-sorting, suffix-array, radix-sort]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (permutations in lexicographic order, Algorithm L) and Section 7.2.1.3 (combinations in lexicographic and colexicographic order)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (lexicographic order for subsets, k-subsets and permutations, with successor, rank and unrank)
---

Lexicographic order compares two sequences by their first position of difference, as a dictionary compares words: the sequence with the smaller item there comes first, and a proper prefix comes before every longer sequence that extends it. For each [total order](/total-order/) on the items, it gives a total order on the sequences. It is the standard order in which to list [permutations](/permutation/), combinations and other objects, because it is easy to define, to compare and to step through, with the [lexicographic successor](/lexicographic-permutation-successor/) as the step.

## Definition

Let $(\Sigma, <)$ be a totally ordered set, the *alphabet*, and let $a = a_1 \cdots a_m$ and $b = b_1 \cdots b_n$ be finite sequences over $\Sigma$.

**Lexicographic order.** $a <_{\text{lex}} b$ if one of these holds:

1. $a$ is a proper prefix of $b$: $m < n$ and $a_i = b_i$ for all $i \le m$;
2. there is an index $i \le \min(m, n)$ with $a_j = b_j$ for all $j < i$ and $a_i < b_i$.

For sequences of the same length only case 2 can occur.

**It is a total order.** For $a \ne b$, either one is a proper prefix of the other, or there is a first index $i$ with $a_i \ne b_i$, and then $a_i < b_i$ or $b_i < a_i$. So exactly one of $a <_{\text{lex}} b$, $a = b$, $b <_{\text{lex}} a$ holds. For transitivity, let $a <_{\text{lex}} b$ and $b <_{\text{lex}} c$, and let $p$ and $q$ be the positions where they first differ, with a missing item counted as smaller than every item of $\Sigma$. If $p < q$, then $a$ and $c$ first differ at $p$, where $a$ has the smaller item. If $q < p$, they first differ at $q$, again with $a$ smaller. If $p = q$, then $a_p < b_p < c_p$. In each case $a <_{\text{lex}} c$.

**Objects other than sequences.** A $k$-subset of $[n]$ is compared through the increasing sequence of its items; this is lexicographic order on combinations. A permutation is compared through its one-line form. For two ordered sets $A$ and $B$, the *lexicographic product* orders $A \times B$ by $(a, b) < (a', b')$ when $a < a'$, or $a = a'$ and $b < b'$.

## Examples and non-examples

**Words.** In the usual order of letters, car < card < care < cart < cat. Here car is a prefix of card, and card < care because d < e at the fourth letter.

**Permutations.** The permutations of $1\,2\,3$ in lexicographic order are 123, 132, 213, 231, 312, 321. The first is the increasing arrangement and the last is the decreasing one.

**Combinations.** The 2-subsets of $\{1, 2, 3, 4\}$ in lexicographic order are 12, 13, 14, 23, 24, 34.

**An infinite descending chain.** Over the alphabet $\{a, b\}$ with $a < b$, the infinite chain

$$b >_{\text{lex}} ab >_{\text{lex}} aab >_{\text{lex}} aaab >_{\text{lex}} \cdots$$

decreases forever. So lexicographic order on all finite words is a total order but not a well-order when the alphabet has at least two items. On words of one fixed length over a finite alphabet, the order is finite and so it is a well-order.

**Appending breaks the order.** A common prefix keeps the order: if $u <_{\text{lex}} v$ then $wu <_{\text{lex}} wv$. A common suffix need not: $a <_{\text{lex}} ab$, but $ac >_{\text{lex}} abc$, because $c > b$ at the second position.

**Non-examples.**

- *Colexicographic order* compares from the right end. The 2-subsets of $\{1, 2, 3, 4\}$ in [colexicographic order](/colexicographic-order/) are 12, 13, 23, 14, 24, 34, which differs from the list above at the third place.
- *Shortlex order* compares the lengths first and uses lexicographic order only for equal lengths. It puts b before ab, and it is a well-order on finite words over a finite alphabet.
- *Numeric order of decimal strings* is not lexicographic: as strings, $10 <_{\text{lex}} 9$, because $1 < 9$ at the first position. The two orders agree only for strings of equal length without a sign.
- *Character-code order* is lexicographic over the codes, not over the letters in the usual sense: in ASCII every uppercase letter comes before every lowercase letter, so Zebra comes before apple.

## Related definitions

- **[Total order](/total-order/).** The order on the alphabet. Lexicographic order needs it to be total to be total itself.
- **[Colexicographic order](/colexicographic-order/).** Lexicographic order on the reversed sequences. For $k$-subsets it lists all subsets of $[m]$ before any subset that contains $m + 1$.
- **[Lexicographic successor](/lexicographic-permutation-successor/).** The next arrangement in lexicographic order, computed by [next permutation](/next-permutation/).
- **[Lexicographic combinations](/lexicographic-combinations/).** The listing of $k$-subsets in lexicographic order.
- **[Permutation ranking](/permutation-ranking/).** The position of a permutation in lexicographic order, given by its [Lehmer code](/lehmer-code/).
- **[String sorting](/string-sorting/) and [suffix arrays](/suffix-array/).** A suffix array lists the suffixes of a string in lexicographic order. LSD [radix sort](/radix-sort/) sorts strings of equal length in lexicographic order.

## References
