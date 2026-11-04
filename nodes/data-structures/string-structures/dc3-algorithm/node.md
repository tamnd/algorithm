---
tag: 13MGBB
kind: algorithm
slug: dc3-algorithm
name: DC3 algorithm
aliases:
- skew algorithm
- Kärkkäinen-Sanders algorithm
area: data-structures/string-structures
level: advanced
summary: Linear-time suffix array construction by recursing on the suffixes at positions not divisible by three.
solves: [suffix-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
history:
  year: 2003
  people: [Juha Kärkkäinen, Peter Sanders]
  note: Kärkkäinen and Sanders gave the skew algorithm at ICALP 2003, and with Burkhardt generalized it to any difference cover in the journal version of 2006.
prereqs: [suffix-array, radix-sort, k-way-merge]
see_also: [dc3-skew-algorithm, suffix-array-construction, suffix-array, farach-algorithm, prefix-doubling, manber-myers-algorithm, external-memory-model, burrows-wheeler-transform]
sources:
  - paper: Juha Kärkkäinen and Peter Sanders, Simple linear work suffix array construction, ICALP 2003, LNCS 2719, doi:10.1007/3-540-45061-0_73
    locator: pages 943 to 955, the skew algorithm with the sample of positions 1 and 2 modulo 3
  - paper: Juha Kärkkäinen, Peter Sanders and Stefan Burkhardt, Linear work suffix array construction, Journal of the ACM 53(6), 2006, doi:10.1145/1217856.1217858
    locator: pages 918 to 936, the DC3 algorithm, its generalization DC-v to a difference cover modulo v, and the parallel and external memory versions
  - paper: Stefan Burkhardt and Juha Kärkkäinen, Fast lightweight suffix array construction and checking, CPM 2003, LNCS 2676, doi:10.1007/3-540-44888-8_5
    locator: pages 55 to 69, difference cover samples for suffix sorting in small extra space
---

The DC3 algorithm builds the [suffix array](/suffix-array/) of a text of length $n$ over an integer alphabet in $\Theta(n)$ time. It sorts the suffixes that start at positions $i$ with $i \bmod 3 \in \{1, 2\}$ by one recursive call on a string of length about $2n/3$, then sorts the other suffixes with one radix sort pass, and merges. The set $\{1, 2\}$ works because it is a *difference cover* modulo 3: any two positions $i$ and $j$ have an offset $\ell < 3$ for which both $i + \ell$ and $j + \ell$ fall in the sorted sample. This page describes the algorithm in that general form, DC-$v$ for a difference cover $D$ modulo $v$, with DC3 as the case $v = 3$. The page on the [skew algorithm](/dc3-skew-algorithm/) treats the classic three-way version with its two-way merge.

## In plain words

Sorting all suffixes of a text directly is slow, because two suffixes can share a long start. DC3 sorts two thirds of them first, the ones that start at positions 1, 2, 4, 5, 7, 8 and so on. It cuts the text into blocks of three letters, gives each block a number, and sorts the shorter string of block numbers by calling itself.

The rest, the positions 0, 3, 6 and so on, are easy once the first two thirds are known: such a suffix is one letter followed by a suffix that is already ranked. Last, the sorted groups are merged. Any two suffixes can be compared by looking at one or two letters and then at two ranks that are already known, so each comparison takes constant time.

## The problem

Given a text $t[0 \ldots n-1]$ over the integer alphabet $\{1, \ldots, K\}$, with $K \le n^{O(1)}$, compute the array $SA$ of the starting positions of its suffixes in increasing lexicographic order (the [suffix array construction](/suffix-array-construction/) problem). Positions at or after $n$ read as 0, which is smaller than every symbol.

## The algorithm

Fix $v$ and a difference cover $D \subseteq \{0, \ldots, v-1\}$: for every $r$ there are $a, b \in D$ with $a - b \equiv r \pmod v$. The covers used here are $\{1, 2\}$ for $v = 3$, $\{1, 2, 4\}$ for $v = 7$ and $\{1, 2, 4, 10\}$ for $v = 13$. The *class* of a position $i$ is $i \bmod v$.

```pseudo id=main
DC(t, n, v, D)
L1  S ← the positions i with 0 ≤ i ≤ n and i mod v ∈ D, listed class by class in the order of D and by increasing i within a class
L2  radix sort S by the v-tuples t[i ‥ i+v−1]; name each position by the rank of its tuple among the distinct tuples
L3  if two positions of S have the same name then
L4      R ← DC(the string of the names of S in the order of L1)          ▷ recursion on |S| ≈ |D| n / v symbols
L5      rank[i] ← 1 + the place of i's suffix in R, for each i in S     ▷ else rank[i] ← name[i]
L6  for each class c: ℓ_c ← the least ℓ with (c+ℓ) mod v ∈ D; radix sort the positions of class c by (t[i ‥ i+ℓ_c−1], rank[i+ℓ_c])
L7  for each pair of classes (a, b): off[a][b] ← the least ℓ < v with (a+ℓ) mod v ∈ D and (b+ℓ) mod v ∈ D
L8  merge the v sorted classes, comparing i and j by (t[i ‥ i+ℓ−1], rank[i+ℓ]) against (t[j ‥ j+ℓ−1], rank[j+ℓ]) with ℓ = off[i mod v][j mod v]
```

**The sample (L1 to L5).** Line L2 sorts the sample by its first $v$ letters. If all names differ, they already rank the sample suffixes. Otherwise line L4 writes, for each class of $D$, the names of its positions in increasing order, and sorts the suffixes of that string. The suffix of the name string at a position $i$ starts with the names of $i, i + v, i + 2v, \ldots$, whose tuples spell $t[i \ldots]$ in blocks of $v$ letters, so comparing name strings compares the text suffixes. The last position of each class is greater than $n - v$, so its tuple reaches past the end of the text, and two different sample suffixes differ before either name sequence leaves its class. Position $n$, if its class is in $D$, has the all-zero tuple and gets the least name.

**The other classes (L6).** For a position $i$ of class $c$, the position $i + \ell_c$ is in the sample, so the suffix at $i$ is the $\ell_c$ letters $t[i \ldots i+\ell_c-1]$ followed by a sample suffix of known rank. Radix sorting by these $\ell_c + 1$ keys sorts the class. For $c \in D$, $\ell_c = 0$ and the sort is by rank alone.

**The merge (L7, L8).** For two positions $i$ and $j$ in classes $a$ and $b$, the cover gives $x, y \in D$ with $x - y \equiv a - b$, and then $\ell = (x - a) \bmod v$ moves both $i$ and $j$ into the sample. The two suffixes compare like the pairs (first $\ell$ letters, rank at offset $\ell$), which costs $O(v)$. A heap merges the $v$ lists.

For $v = 3$ and $D = \{1, 2\}$, $\ell_0 = 1$ and the table of offsets is: $off[0][1] = 1$, $off[0][2] = 2$, and $off[a][b] = 0$ when $a, b \in \{1, 2\}$. The original skew algorithm merges the class 0 list with the sorted sample in one two-way merge, which is the same comparison.

## Example

The suffix array of abracadabra ($n = 11$), with a = 1, b = 2, c = 3, d = 4, r = 18 and $v = 3$.

| sample position | 1 | 4 | 7 | 10 | 2 | 5 | 8 | 11 |
|---|---|---|---|---|---|---|---|---|
| tuple | bra | cad | abr | a00 | rac | ada | bra | 000 |
| name | 5 | 6 | 3 | 2 | 7 | 4 | 5 | 1 |

The names are the ranks of the seven distinct tuples (000 < a00 < abr < ada < bra < cad < rac). Positions 1 and 8 share the name 5, so line L4 recurses on 5 6 3 2 7 4 5 1, whose suffix array is [7, 3, 2, 5, 6, 0, 1, 4]. Mapping back gives the ranks of the sample suffixes:

| position | 11 | 10 | 7 | 5 | 8 | 1 | 4 | 2 |
|---|---|---|---|---|---|---|---|---|
| rank | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |

The tie between 1 and 8 is broken by the next block: after bra, position 1 continues with cad and position 8 with a00, so 8 comes first. Line L6 sorts the three classes:

- class 0, by $(t[i], rank[i+1])$: 0 (a, 6), 3 (a, 7), 6 (d, 3), 9 (r, 2), so the order is 0, 3, 6, 9;
- class 1, by rank: 10, 7, 1, 4;
- class 2, by rank: 5, 8, 2.

The merge compares across classes. For 0 against 10, $off[0][1] = 1$: both start with a, and $rank[1] = 6$ is greater than $rank[11] = 1$, so 10 comes first. For 0 against 5, $off[0][2] = 2$: ab against ad differ at the second letter, so 0 comes first. The result is

$$SA = [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2].$$

## Correctness

The proof has three parts. Naming and recursion rank the sample suffixes correctly, because a name string suffix spells the text suffix in blocks and two different sample suffixes differ inside their name sequences. The class sorts are correct because a suffix outside the sample is a short string followed by a ranked sample suffix. The merge comparison is correct because the difference cover moves any two positions into the sample by the same offset. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

For a fixed $v$, each level of recursion does $O(n)$ work: the radix sorts of L2 and L6 make $O(v)$ passes over $O(n)$ items with $O(n)$ buckets each, and the merge makes $O(n \log v)$ comparisons of cost $O(v)$. The recursive call has $\lvert S \rvert \le \lvert D \rvert (n + 1)/v + \lvert D \rvert$ symbols, so for DC3

$$T(n) = T(2n/3 + O(1)) + O(n) = O(n).$$

The extra space is $O(n)$ words. A larger $v$ makes the recursion smaller ($3/7$ of the text for $v = 7$, $4/13$ for $v = 13$) at the cost of longer tuples and comparisons. Kärkkäinen, Sanders and Burkhardt note that covers of size $O(\sqrt v)$ exist for every $v$, so the sample can be made a small fraction of the text.

## Properties

- **Non-comparison.** The algorithm uses radix sorting on the integer symbols and names, so it works for any integer alphabet of polynomial size, not only bytes.
- **Recursive.** The depth is $O(\log n)$, since each level shrinks the text by a constant factor.
- **Simple data flow.** Every step is a scan, a radix sort or a merge. This is why the algorithm adapts well to the [external memory model](/external-memory-model/) and to parallel machines, which is the point of the journal version.

## Variants and improvements

- **DC3 as the skew algorithm.** The original presentation, on the page of the [skew algorithm](/dc3-skew-algorithm/), uses $D = \{1, 2\}$, pads the text with three zeros and merges the class 0 suffixes with the sample in one two-way merge.
- **Larger $v$.** DC7 and DC13 recurse on less of the text. In external memory, where the cost is the number of passes over the data, this reduces the I/O volume.
- **Lightweight sorting.** Burkhardt and Kärkkäinen used difference cover samples before DC3: sort only the sample suffixes, then sort all suffixes with comparisons that stop after at most $v$ letters and finish with two sample ranks. With $v$ growing with $n$, the sample and its ranks take sublinear space beyond the text and the suffix array.
- **Parallel and external versions.** The journal paper gives versions for the external memory model and for parallel models, with work linear in $n$.
- **Other linear algorithms.** [Farach's algorithm](/farach-algorithm/) also recurses on a fraction of the suffixes (the odd ones) but needs a harder merge. Induced sorting algorithms are usually faster in practice in internal memory.

## When to use it

Use DC3 when a simple linear-time suffix array construction is needed, for example in teaching or when an integer alphabet is large, and use a DC-$v$ variant when the text does not fit in memory or the construction runs in parallel. For a fast in-memory build on byte strings, induced sorting libraries are usually preferred; for short texts, [prefix doubling](/prefix-doubling/) or a plain sort is simpler.

## Pitfalls

- **The end of the text.** The tuples near the end must read zeros past the text, and the zero must be smaller than every symbol. Shifting byte values by one, as the implementation does, keeps 0 free.
- **The last sample position.** If the name sequence of a class could end with a tuple that lies wholly inside the text, two sample suffixes could compare equal in the recursive string while their text suffixes differ. Including the positions up to $n$, as in line L1, makes the last tuple of each class reach past the end; the skew algorithm achieves the same with a padding position when $n \bmod 3 = 1$.
- **Ranks versus names.** Line L8 needs the ranks of the sample suffixes, not the names of their tuples. Names are only ranks when they are all different.
- **Wrong offset table.** Using $\ell_c$ of one of the two positions in the merge comparison fails when it does not move the other position into the sample; the offset must work for both classes, which is what $off$ gives.
- **Bucket counts.** Each radix pass needs buckets for the largest name or rank, which can be close to $n$, not the size of the original alphabet.

## Implementations

The Python function takes $v \in \{3, 7, 13\}$ with the covers above and follows lines L1 to L8, with an LSD radix sort on lists of digits and a heap merge with the comparison of line L8. Texts of at most $2v$ symbols are sorted directly. The tests replay the example, check that each stored cover is a difference cover and that no smaller one exists, and compare 600 random texts against a naive sort of the suffixes.

## History

Manber and Myers introduced suffix arrays in 1990 with an $O(n \log n)$ construction. Farach (1997) built suffix trees in linear time for integer alphabets by recursing on the odd suffixes. Burkhardt and Kärkkäinen (CPM 2003) used difference cover samples for suffix sorting in small space. In the same year, Kärkkäinen and Sanders (ICALP 2003) gave the skew algorithm, the first direct linear-time suffix array construction, together with the linear algorithms of Kim, Sim, Park and Park and of Ko and Aluru published the same year. The journal version by Kärkkäinen, Sanders and Burkhardt (2006) presents the general DC-$v$ algorithm and its models of computation.

## References
