---
tag: 12PBRG
kind: algorithm
slug: green-filter
name: Green's filter
aliases:
- Green's 16-input sorting network
area: sorting/sorting-networks
level: advanced
summary: Green's 16-input sorting network with 60 comparators and depth 10, built from a hypercube filter of 32 comparators followed by 28 more.
solves: [sorting-problem]
model: sorting-network
complexity:
  vars: {n: the number of items, 16 for the network itself}
  time: {worst: Θ(n log² n), average: Θ(n log² n), best: Θ(n log² n)}
  space: {extra: O(1)}
  depth: {worst: Θ(log² n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1969
  people: [Milton W. Green]
  note: Green found the 60-comparator network for 16 inputs and published it in 1972.
prereqs: [sorting-network, zero-one-principle]
see_also: [minimum-size-sorting-network, odd-even-merge-sort, pairwise-sorting-network, depth-size-tradeoff, network-size, network-depth]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (Green's network for 16 elements)
  - paper: "M. W. Green, Some improvements in non-adaptive sorting algorithms, Proceedings of the Sixth Annual Princeton Conference on Information Sciences and Systems (1972)"
    locator: pp. 387 to 391
  - paper: "Igor S. Sergeev, Some comments on the structure of the best known networks sorting 16 elements, arXiv:1810.11262 (2018)"
    locator: Sections 2 and 3 (the cube order after the first four layers, and the sort of the middle layer by tetrads)
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the networks for 16 inputs (60 comparators in 10 layers, and 61 comparators in 9 layers)
---

Green's network is a [sorting network](/sorting-network/) on 16 wires with 60 [comparators](/comparator/) in 10 layers. Its first four layers, the *filter*, compare each wire $i$ with the wire $i \oplus 2^b$ for $b = 0, 1, 2, 3$; after them, the item on wire $w$ is at most the item on each wire whose binary digits include those of $w$. The other 28 comparators finish the sort with the help of this partial order. Since 1969 no network for 16 inputs with fewer comparators has been found; its depth 10 is one more than the optimal depth 9.

## In plain words

Number the 16 places from 0 to 15 and write each number with 4 binary digits. First compare the places that differ only in the last digit, then the places that differ only in the second digit, and so on, for all 4 digits. After these 4 rounds, place 0 holds the smallest item and place 15 the largest, and many other pairs of places are already in order: a place whose digits are part of the digits of another place holds the smaller item.

So much of the order is known, and only the items at places that are not related in this way still need work. Green found 28 more comparisons that sort the rest. The whole method uses 60 comparisons, fewer than any other known method for 16 items.

## The problem

The input is an array $A[0 \ldots 15]$ of items with a total order. The output is the same array in non-decreasing order, computed by a fixed sequence of compare-exchange steps. This is the [sorting problem](/sorting-problem/) for $n = 16$ in the [sorting network](/sorting-network/) model. Other values of $n$ are handled in [Variants and improvements](#variants-and-improvements).

## The algorithm

Each line from L5 to L10 is one layer, written as a list of comparators $[i{:}j]$ with disjoint wires.

```pseudo id=main
GREEN-16(A)                                ▷ sort A[0 .. 15]
L1  for each i with bit 0 of i equal to 0 do COMPARE(A, i, i + 1)    ▷ the filter
L2  for each i with bit 1 of i equal to 0 do COMPARE(A, i, i + 2)
L3  for each i with bit 2 of i equal to 0 do COMPARE(A, i, i + 4)
L4  for each i with bit 3 of i equal to 0 do COMPARE(A, i, i + 8)
L5  [1:2] [4:8] [7:11] [13:14] [3:12] [5:10] [6:9]
L6  [1:4] [2:8] [7:13] [11:14] [10:12] [3:5]
L7  [2:4] [11:13] [7:9] [6:8]
L8  [7:10] [9:12] [3:6] [5:8]
L9  [9:10] [5:6] [7:8] [11:12] [3:4]
L10 [6:7] [8:9]

COMPARE(A, i, j)                           ▷ a comparator [i:j], with i < j
L11 if A[i] > A[j] then exchange A[i] and A[j]
```

After the filter, group the wires by the number of one bits: $\{0\}$, the wires $I = \{1, 2, 4, 8\}$ with one bit, the wires $M = \{3, 5, 6, 9, 10, 12\}$ with two bits, the wires $III = \{7, 11, 13, 14\}$ with three bits, and $\{15\}$. Wires 0 and 15 already hold the smallest and the largest item.

- The comparators $[1{:}2], [4{:}8], [1{:}4], [2{:}8], [2{:}4]$ of lines L5 to L7 sort $I$ in the order $1, 2, 4, 8$, and $[7{:}11], [13{:}14], [7{:}13], [11{:}14], [11{:}13]$ sort $III$ in the order $7, 11, 13, 14$.
- Line L5 also compares the three pairs of $M$ whose bits are complements: $[3{:}12], [5{:}10], [6{:}9]$.
- The four wires $3, 5, 6, 8$, which hold the three smaller items of these pairs and the largest item of $I$, are sorted by $[3{:}5], [6{:}8], [3{:}6], [5{:}8], [5{:}6]$. The four wires $7, 9, 10, 12$, which hold the smallest item of $III$ and the three larger items of the pairs, are sorted by $[10{:}12], [7{:}9], [7{:}10], [9{:}12], [9{:}10]$.
- The last comparators $[3{:}4]$, $[11{:}12]$, $[7{:}8]$, $[6{:}7]$ and $[8{:}9]$ join these sorted groups.

The network has $4 \cdot 8 + 7 + 6 + 4 + 4 + 5 + 2 = 60$ comparators.

## Example

Sort $A = [3, 8, 13, 12, 10, 2, 7, 15, 6, 0, 4, 5, 11, 9, 1, 14]$. Each row is the array after the layer.

| layer | wires 0 to 15 |
|---|---|
| L1 | 3 8 12 13 2 10 7 15 0 6 4 5 9 11 1 14 |
| L2 | 3 8 12 13 2 10 7 15 0 5 4 6 1 11 9 14 |
| L3 | 2 8 7 13 3 10 12 15 0 5 4 6 1 11 9 14 |
| L4 | 0 5 4 6 1 10 9 14 2 8 7 13 3 11 12 15 |
| L5 | 0 4 5 3 1 7 8 13 2 9 10 14 6 11 12 15 |
| L6 | 0 1 2 3 4 7 8 11 5 9 6 12 10 13 14 15 |
| L7 | 0 1 2 3 4 7 5 9 8 11 6 12 10 13 14 15 |
| L8 | 0 1 2 3 4 7 5 6 8 10 9 12 11 13 14 15 |
| L9 | 0 1 2 3 4 5 7 6 8 9 10 11 12 13 14 15 |
| L10 | 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 |

After L4, wire 0 holds 0 and wire 15 holds 15. The wires of $I$ hold $5, 4, 1, 2$ and those of $III$ hold $14, 13, 11, 12$. Each layer from L5 to L10 makes at least one exchange on this input.

## Correctness

By the [zero-one principle](/zero-one-principle/) it is enough to consider inputs of zeros and ones. The filter makes the item on each wire $w$ at most the item on each wire $w'$ whose bits include those of $w$, because a layer for one bit keeps this order for the bits handled before. So, on 0-1 inputs, the zeros after the filter fill a down-set of the cube $\{0, 1\}^4$. The network is symmetric: the map that sends wire $w$ to $15 - w$ and each bit $x$ to $1 - x$ maps each layer to itself. So it is enough to handle inputs with at most 8 zeros. Then at most one wire of $III$ holds a zero, and a short case analysis on the number $z_1$ of zeros in $I$ and on the zeros of the three complementary pairs shows that the two sorted groups of four, the three sorted wires of $I$ that stay at the start, and the joining comparators put the zeros exactly on the first wires. The full proof is below.

## Complexity

The network itself has size 60 and depth 10, and it runs in $O(1)$ time and space for its 16 items. For comparison, on 16 inputs:

| network | size | depth |
|---|---|---|
| Green | 60 | 10 |
| [odd-even merge sort](/odd-even-merge-sort/) and the [pairwise network](/pairwise-sorting-network/) | 63 | 10 |
| [bitonic sort](/bitonic-sort/) | 80 | 10 |
| a 9-layer network from Dobbelaere's list | 61 | 9 |

The information bound gives at least $\lceil \lg 16! \rceil = 45$ comparators, and the smallest size for 16 inputs is not known. The smallest depth is 9 ([minimum-depth sorting network](/minimum-depth-sorting-network/)).

The Python code below also sorts other $n$, with Green's network as a base case. For $n > 16$ it makes $\Theta(n \log^2 n)$ comparisons in $\Theta(\log^2 n)$ layers, as odd-even merge sort does.

## Properties

- **Data oblivious, in place, not stable, not adaptive,** as each network of comparators.
- **The filter is a hypercube.** Each of the first four layers compares the wires that differ in one bit, so on a 4-dimensional hypercube each layer uses the links of one dimension.
- **Symmetric.** The network is mapped to itself by $w \mapsto 15 - w$ with min and max exchanged.
- **The cube order.** After the filter, the items are ordered by the bit sets of their wires: wire $w$ holds at most the item of wire $w'$ when $w \subseteq w'$. On 0-1 inputs, only 168 outputs of the filter are possible, the down-sets of $\{0, 1\}^4$, instead of $2^{16}$.

## Variants and improvements

- **Fewer than 16 wires.** Drop each comparator that touches a wire $j \ge n$. The missing wires act as $+\infty$, and a standard comparator on such a wire changes nothing. For $n = 9, \ldots, 15$ this gives $26, 31, 36, 40, 46, 51, 56$ comparators. For $n = 9$ to $13$ these counts are larger than the best known sizes $25, 29, 35, 39, 45$, and for $n = 14$ and $15$ they equal the best known sizes $51$ and $56$.
- **A base case for Batcher's merges.** For $n > 16$, sort each block of 16 wires with Green's network and merge the blocks with Batcher's odd-even merge. This saves 3 comparators per block compared with odd-even merge sort. The Python code below does this.

## When to use it

Use Green's network to sort 16 items with the fewest known comparators, for example in hardware or in branch-free code where each comparator costs an instruction pair. If the number of layers matters more, use a depth-9 network for 16 inputs. For other sizes, take a network from the tables of the best known networks, or use odd-even merge sort.

## Pitfalls

- **A wrong comparator.** The list is easy to copy wrong, and a single wrong comparator usually breaks the sort. Check a copied network on all $2^{16}$ inputs of zeros and ones, which takes well under a second with one bit per input.
- **Mixing two versions.** Books and web pages show isomorphic forms of Green's network with the wires numbered in another way. A layer of one form does not fit the filter of another.
- **Calling it optimal.** Green's network has the best known size for 16 inputs, but the optimal size is not proved, and its depth 10 is not optimal.

## Implementations

## History

M. W. Green found the network around 1969, and published it in 1972 in "Some improvements in non-adaptive sorting algorithms". Knuth describes it in Section 5.3.4 of *The Art of Computer Programming*. Sergeev explained its structure in 2018 in terms of the cube order after the filter.

## References
