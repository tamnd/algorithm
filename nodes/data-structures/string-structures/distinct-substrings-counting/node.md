---
tag: 6KAYAQ
kind: problem
slug: distinct-substrings-counting
name: Counting distinct substrings
area: data-structures/string-structures
level: core
summary: Count the number of distinct substrings of a string from its suffix structure.
prereqs: [suffix-tree, suffix-automaton, suffix-trie]
see_also: [count-distinct-substrings, suffix-automaton, suffix-tree, suffix-trie, blumer-algorithm, ukkonen-algorithm, kasai-algorithm, substring-queries]
sources:
  - paper: Anselm Blumer, Janet Blumer, David Haussler, Andrzej Ehrenfeucht, M. T. Chen and Joel Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985, doi:10.1016/0304-3975(85)90157-4
    locator: pages 31 to 55, the directed acyclic word graph, its states as end-position classes, and the bounds on its size
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Chapter 5 (Introduction to suffix trees) for the definitions of the suffix tree and its edge labels, and Chapter 7 (First applications of suffix trees)
  - paper: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, Combinatorial Pattern Matching (CPM 2001), LNCS 2089, doi:10.1007/3-540-48194-X_17
    locator: pages 181 to 192, the LCP array in linear time and its use on suffix tree problems
---

Counting distinct substrings asks for the number of different nonempty strings that occur as contiguous pieces of a string $T$ of length $n$. A string of length $n$ has $n(n+1)/2$ occurrences of nonempty substrings, but repeats make the number of different ones smaller. Every suffix structure of $T$ gives the count in $O(n)$ time once it is built: it is the number of nodes of the [suffix trie](/suffix-trie/) minus one, the total length of the edge labels of the [suffix tree](/suffix-tree/) without a terminator, and the sum of $len(v) - len(link(v))$ over the states of the [suffix automaton](/suffix-automaton/). The suffix array form, $n(n+1)/2$ minus the sum of the LCP array, is treated on [count distinct substrings](/count-distinct-substrings/); this page covers the tree and automaton views and the online version, where the count is kept for every prefix while $T$ is read.

## In plain words

Write down every piece of a word that you get by cutting it at two places, and throw away the copies. How many pieces are left? For "banana" there are 21 ways to cut, but "a" appears three times, "an" and "na" twice, and so on, and only 15 different pieces remain.

Listing the pieces would take too long for a long text, since there can be about $n^2/2$ of them. Instead, build a structure in which each different piece corresponds to exactly one spot, such as a node or a position along an edge, and count the spots. Suffix trees and suffix automata are such structures, and they have only about $2n$ nodes, so counting the spots takes linear time.

## Definition

**Input.** A string $T \in \Sigma^n$.

**Output.** The number $D(T) = \lvert \{ T[i .. j] : 0 \le i \le j < n \} \rvert$ of distinct nonempty substrings. Some texts count the empty string too, which adds 1.

**Online form.** Output $D(T[0 .. k-1])$ for each $k = 1, \ldots, n$, as the symbols of $T$ arrive one at a time.

The value satisfies $n \le D(T) \le n(n+1)/2$ for $n \ge 1$. The lower bound holds for $a^n$, whose distinct substrings are $a, aa, \ldots, a^n$. The upper bound holds when all symbols of $T$ are different.

## Variants

- **Fixed length.** Count the distinct substrings of each length $\ell$. In the suffix tree, the substrings of length $\ell$ are the points at string depth $\ell$, one on each edge that crosses depth $\ell$.
- **Repeated substrings.** Count the distinct substrings that occur at least twice. These are the points above the inner nodes of the suffix tree, or in the suffix automaton the substrings of states whose end-position set has at least two elements.
- **Range queries.** Count the distinct substrings of $T[i .. j]$ for many pairs $(i, j)$. This needs more than a single suffix structure and is a separate problem.
- **Total length or weighted count.** Sum the lengths of the distinct substrings, or weight each by a function of its length. The same decompositions give these sums by adding arithmetic series along edges or within states.
- **Several strings.** Count the distinct substrings of a set of strings with a [generalized suffix tree](/generalized-suffix-tree/) or a suffix automaton of the set.

## Examples

| $T$ | $n(n+1)/2$ | $D(T)$ |
|---|---|---|
| aaaa | 10 | 4 |
| abab | 10 | 7 |
| abcd | 10 | 10 |
| banana | 21 | 15 |
| mississippi | 66 | 53 |

**The online counts for banana.** Reading b, a, n, a, n, a, the counts of the prefixes are 1, 3, 6, 9, 12, 15. Each new symbol adds 1, 2, 3, 3, 3, 3 new substrings. When "ban" is extended to "bana", the new suffixes are bana, ana, na and a, but "a" already occurred, so 3 are new.

**The suffix automaton of banana.** It has 10 states. Write each state other than the initial one as (len, len of its suffix link target):

| state | substrings of the state | len | len of link | contribution |
|---|---|---|---|---|
| 1 | b | 1 | 0 | 1 |
| 5 | a | 1 | 0 | 1 |
| 2 | ba | 2 | 1 | 1 |
| 7 | an, n | 2 | 0 | 2 |
| 3 | ban | 3 | 2 | 1 |
| 9 | ana, na | 3 | 1 | 2 |
| 4 | bana | 4 | 3 | 1 |
| 6 | banan, anan, nan | 5 | 2 | 3 |
| 8 | banana, anana, nana | 6 | 3 | 3 |

The contributions sum to 15. The state numbers are the order of creation in the standard online construction, where state 5 is a clone made when the second "a" arrived, and states 7 and 9 are clones made at the second "n" and the third "a".

## Known algorithms

| method | time | extra space | online |
|---|---|---|---|
| put all substrings in a hash set | $O(n^2)$ substrings, $O(n^3)$ symbol work | $\Theta(n^2)$ strings | no |
| [suffix trie](/suffix-trie/): count nodes, minus the root | $O(n^2)$ | $\Theta(n^2)$ nodes | yes |
| [suffix tree](/suffix-tree/): sum of edge lengths | $O(n)$ after an $O(n)$ build | $O(n)$ words | with [Ukkonen's algorithm](/ukkonen-algorithm/) |
| [suffix automaton](/suffix-automaton/): sum of $len(v) - len(link(v))$ | $O(n)$ for a constant alphabet | $O(n)$ words | yes |
| suffix array and LCP array | $O(n)$ after the build | $O(n)$ words | no |

**Suffix trie.** Each node other than the root is the end of exactly one distinct nonempty substring: the string on its path from the root. So $D(T)$ is the number of nodes minus one. This is correct but can use $\Theta(n^2)$ nodes.

**Suffix tree.** The suffix tree compresses the suffix trie by merging chains of nodes with one child into edges. Each point of the trie, a node or a position inside an edge, still stands for one distinct substring. So $D(T)$ is the total length of all edge labels of the suffix tree of $T$ without a terminator, where suffixes that are prefixes of other suffixes end inside edges. With a terminator \$ not in $\Sigma$, each of the $n + 1$ leaf edges has one extra symbol \$, and $D(T)$ is the total edge length minus $n + 1$.

**Suffix automaton.** Each state $v$ of the suffix automaton stands for a set of substrings that have the same set of end positions in $T$. These substrings are the suffixes of the longest one, of lengths $len(link(v)) + 1$ up to $len(v)$, where $link(v)$ is the suffix link (Blumer et al. 1985). The sets of different states are disjoint and cover all nonempty substrings, so $D(T) = \sum_{v \ne \text{init}} (len(v) - len(link(v)))$.

**Online count.** The online construction of the suffix automaton adds one state $cur$ for the whole new prefix in each step, with $len(cur) = k$. The substrings that end at the new last position and are new are exactly those of the state $cur$, since every older substring already belonged to a state. So the step adds $len(cur) - len(link(cur))$ to the count, and cloning a state does not change the total: a clone takes a range of lengths away from the state it copies. The same idea works with Ukkonen's construction of the suffix tree, where the count of new substrings in phase $k$ is $k$ minus the length of the active point at the end of the phase, which is the length of the longest suffix of the prefix that also occurs earlier.

## Bounds

**Linear time.** For a constant alphabet, the suffix automaton and the suffix tree are built in $O(n)$ time, so $D(T)$ takes $\Theta(n)$ time. For an integer alphabet of size polynomial in $n$, the suffix tree can be built in $O(n)$ time with [Farach's algorithm](/farach-algorithm/) and the suffix array in $O(n)$ time, so the bound stays $\Theta(n)$. Each symbol of $T$ must be read, since changing one symbol can change $D(T)$.

**Size of the structures.** The suffix automaton of a string of length $n \ge 2$ has at most $2n - 1$ states and at most $3n - 4$ transitions (Blumer et al. 1985), and the suffix tree has at most $2n$ nodes with a terminator. So the sums above have $O(n)$ terms, while $D(T)$ itself can be $\Theta(n^2)$; the count fits in $O(\log n)$ bits.

**Comparison model.** If symbols can only be compared, building any of these structures needs $\Omega(n \log \sigma)$ comparisons in the worst case for alphabets of size $\sigma$ up to $n$, as for sorting the symbols. Counting itself has the same bound for general alphabets in that model, since $D(T) = n(n+1)/2$ decides whether all symbols are different, which is element distinctness.

## Reductions

- **To the LCP array.** $D(T) = n(n+1)/2 - \sum_{r=1}^{n-1} LCP[r]$, where $LCP[r]$ is the length of the longest common prefix of the suffixes of ranks $r - 1$ and $r$. Each suffix $T[SA[r] ..]$ contributes its prefixes longer than $LCP[r]$ as new strings. See [count distinct substrings](/count-distinct-substrings/) and the [Kasai algorithm](/kasai-algorithm/).
- **From element distinctness.** As in Bounds, $D(T) = n(n+1)/2$ if and only if the symbols of $T$ are pairwise distinct.
- **Distinct substrings of a set.** Join the strings with distinct separators and subtract the substrings that contain a separator, or build a generalized structure directly.

## Applications

- **Repetitiveness measures.** The number of distinct substrings of each length, called the substring complexity, measures how repetitive a string is, and is used to bound the size of compressed indexes.
- **Test data and puzzles.** The counts are a standard check of suffix tree and suffix automaton implementations, since a brute force count is easy to compare against.
- **Sequence analysis.** In genomics, the number of distinct substrings of length $k$ (the distinct k-mers) of a read set is used to estimate genome size and to set parameters of assemblers.
- **Combinatorics on words.** Strings with many distinct substrings, such as [de Bruijn sequences](/de-bruijn-sequence/), which contain each string of length $k$ once, are the extreme cases of the problem.

## References
