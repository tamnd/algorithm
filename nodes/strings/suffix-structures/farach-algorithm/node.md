---
tag: 5GVP55
kind: algorithm
slug: farach-algorithm
name: Farach's algorithm
aliases:
- Farach-Colton algorithm
area: strings/suffix-structures
level: research
summary: Linear-time suffix tree construction for integer alphabets, via a suffix array of odd positions.
solves: [suffix-tree-construction, suffix-array-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the alphabet size}
  time: {best: Θ(n), average: Θ(n), worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: true}
history:
  year: 1997
  people: [Martin Farach]
  note: Farach gave the algorithm at FOCS 1997; the journal version with Paolo Ferragina and S. Muthukrishnan, in the Journal of the ACM in 2000, extends it to external memory and parallel models.
prereqs: [suffix-tree, suffix-array, lowest-common-ancestor, radix-sort]
see_also: [dc3-skew-algorithm, suffix-tree-construction, ukkonen-algorithm, mccreight-algorithm, weiner-algorithm, sa-is, lcp-rmq-reduction, external-memory-model]
sources:
  - paper: doi:10.1109/SFCS.1997.646102
    title: Martin Farach, Optimal suffix tree construction with large alphabets, FOCS 1997
    locator: pages 137 to 143, the odd tree by recursion on character pairs, the even tree from the odd tree, and the merge by overmerging, d-links and unmerging
  - paper: doi:10.1145/355541.355547
    title: Martin Farach-Colton, Paolo Ferragina and S. Muthukrishnan, On the sorting-complexity of suffix tree construction, Journal of the ACM 47(6), 2000
    locator: pages 987 to 1011, the full version with the proofs of the merge, and the versions for external memory and parallel machines
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), the construction of suffix trees and suffix arrays for large alphabets
  - paper: doi:10.1145/1217856.1217858
    title: Juha Kärkkäinen, Peter Sanders and Stefan Burkhardt, Linear work suffix array construction, Journal of the ACM 53(6), 2006
    locator: pages 918 to 936, the introduction, which compares the skew algorithm with the odd and even recursion of Farach
---

Farach's algorithm builds the [suffix tree](/suffix-tree/) of a text of length $n$ over an integer alphabet in $\Theta(n)$ time. It was the first linear-time [suffix tree construction](/suffix-tree-construction/) for alphabets as large as $n$: the earlier algorithms of [Weiner](/weiner-algorithm/), [McCreight](/mccreight-algorithm/) and [Ukkonen](/ukkonen-algorithm/) take linear time only for a constant alphabet. It sorts the suffixes at odd positions by one recursive call on a string of half the length, derives the order of the even suffixes from them, and then merges the odd tree and the even tree. The merge is the hard part, and it is the reason for the later, simpler [DC3 algorithm](/dc3-skew-algorithm/).

## In plain words

Sorting the endings of a long text is slow when two endings share a long start. Farach's idea is to split the endings into two teams: those that start at an odd place and those that start at an even place.

To sort the odd team, glue the letters into pairs and give each different pair a number. The odd endings, read two letters at a time, are the endings of a text half as long, so the same method sorts them.

An even ending is one letter followed by an odd ending, so one quick sort by two keys puts the even team in order.

To merge the two teams, put both of their trees on top of each other. Where the trees are not sure that two branches agree, a chain of small lookups finds how many letters the two endings share.

## The problem

Given a text $T = T[0 \ldots n-1]$, compute its [suffix array](/suffix-array/), its LCP array and its suffix tree. Positions are 0-based.

**Alphabet.** The algorithm needs an integer alphabet: symbols $1, \ldots, \sigma$ with $\sigma \le n^{O(1)}$, so that [radix sort](/radix-sort/) sorts $n$ symbols in $O(n)$ time. A general ordered alphabet is first mapped to $1, \ldots, \sigma$ by sorting the distinct symbols, in $O(n \log \sigma)$ time. The [word RAM](/word-ram/) model is assumed.

**Sentinel.** A sentinel $\$ = 0$ is appended, smaller than every symbol and unique. Let $T' = T\$$, $N = n + 1$ and $T'_p = T'[p \ldots N-1]$. The output lists all $N$ suffixes of $T'$, with the suffix $\$$ at rank 0. $LCP[0] = 0$ and $LCP[k]$ is the length of the longest common prefix of the suffixes at ranks $k - 1$ and $k$.

**Odd and even.** The *odd suffixes* start at the 0-based odd positions $1, 3, 5, \ldots$, and the *even suffixes* at $0, 2, 4, \ldots$. Farach numbers positions from 1, so his odd suffixes are the even ones of this page; the two choices are symmetric, and this page recurses on the 0-based odd positions so that the whole text is an even suffix built in the second step.

## The algorithm

The *odd tree* $\mathcal{T}_o$ is the compacted trie of the odd suffixes, and the *even tree* $\mathcal{T}_e$ the compacted trie of the even suffixes. Each tree is built from a sorted list and its LCP values with one stack scan, in linear time, as in the [LCP interval tree](/lcp-interval-tree/). For two suffixes $x$ and $y$, $\mathrm{lcp}(x, y)$ is the length of their longest common prefix.

```pseudo id=main
FARACH(T')                                  ▷ T'[0..N−1], symbols ≥ 1, T'[N−1] = $ = 0
L1  if N ≤ 4 then sort the suffixes directly and return (SA, LCP)
L2  name each pair (T'[p], T'[p+1]) with odd p by its rank, from 1 (pad with 0); R ← the names in order of p
L3  (SA_R, LCP_R) ← FARACH(R + [0])
L4  SA_o ← [2r + 1 for r in SA_R if r < |R|]; LCP_o[k] ← 2h + [T'[x+2h] = T'[y+2h]] with h = LCP_R[k+1]
L5  SA_e ← even positions sorted by the key (T'[p], rank of p + 1 in SA_o), with (0, −1) for p = N − 1
L6  LCP_e[k] ← 0 if the first symbols differ, else 1 + min LCP_o between the ranks of a + 1 and b + 1
L7  build 𝒯_o from (SA_o, LCP_o) and 𝒯_e from (SA_e, LCP_e)
L8  M ← OVERMERGE(𝒯_o, 𝒯_e); prepare constant-time LCA queries on M
L9  SA ← merge SA_o and SA_e, with x before y if T'[x+h] < T'[y+h], where h = LCP(x, y)
L10 LCP[k] ← LCP(SA[k−1], SA[k]) for k ≥ 1
L11 return (SA, LCP)

OVERMERGE(𝒯_o, 𝒯_e)
L12 create the root of M and push (root, root of 𝒯_o, root of 𝒯_e)
L13 pop (v, a point of 𝒯_o or none, a point of 𝒯_e or none); for each first symbol c of an edge below the points
L14     d ← the smaller depth of the targets of the edges with first symbol c; add a child of v at depth d
L15     push (the child, the point at depth d on each of these edges)

LCP(x, y) for x and y of different parity
L16 v ← LCA_M(x, y); if v is the root then return 0
L17 if ℓ(v) is known then return ℓ(v)
L18 ℓ(v) ← 1 + LCP(x + 1, y + 1), by a loop that follows the chain and fills ℓ on the way back
```

For $x$ and $y$ of the same parity, $\mathrm{LCP}(x, y)$ is the string depth of $\mathrm{LCA}_M(x, y)$. For a different parity it is $\ell(v)$ of lines L16 to L18.

**The odd suffixes (L2 to L4).** Read two symbols at a time, the odd suffix $T'_{2i+1}$ is the suffix of $R$ at index $i$, and the names keep the order of the pairs. So the suffix array of $R$ gives the order of the odd suffixes. The sentinel of $R$, at rank 0 of $SA_R$, is dropped. If two odd suffixes share $h$ pairs, they share $2h$ symbols, and one more when the next pairs agree in their first symbol. The pair that holds the sentinel of $T'$ is unique, so $x + 2h$ stays inside $T'$.

**The even suffixes (L5, L6).** $T'_p = T'[p]\,T'_{p+1}$ and $p + 1$ is odd, so the key $(T'[p], \text{rank of } p + 1)$ orders the even suffixes. With one radix sort pass over the sorted odd list, this takes $O(N)$ time. Two even suffixes with the same first symbol share $1 + \mathrm{lcp}(T'_{a+1}, T'_{b+1})$ symbols, which is a range minimum of $LCP_o$ by the [LCP-RMQ reduction](/lcp-rmq-reduction/).

**The overmerge (L12 to L15).** Walk down both trees at the same time from their roots. Below a pair of points, edges with different first symbols become different children. Two edges with the same first symbol $c$ are *merged* into one edge of $M$, and the walk goes on at the smaller of their two target depths. The merge is optimistic: two merged edges agree in their first symbol, but maybe not in the later ones. So $M$ can be too deep where an odd path and an even path really part. A node of $M$ can be a leaf of one tree and still have children from the other tree.

**The d-links (L16 to L18).** Let $v$ be a node of $M$ other than the root, with an odd leaf $x$ and an even leaf $y$ below it in different branches. They share their first symbol, so $\mathrm{lcp}(x, y) = 1 + \mathrm{lcp}(x + 1, y + 1)$, and $x + 1$ and $y + 1$ again have different parity. The link from $v$ to $\mathrm{LCA}_M(x + 1, y + 1)$ is Farach's *d-link*. The number $\ell(v)$ depends on $v$ only, not on the pair, so the d-links form a tree, and $\ell(v)$ is the depth of $v$ in it. Each $\ell(v)$ is computed once and stored.

**The merge (L9, L10).** With $h = \mathrm{LCP}(x, y)$, the suffixes differ at offset $h$, and the sentinel makes $T'[x + h] \ne T'[y + h]$. So one comparison of symbols orders $x$ and $y$, and a standard merge of two sorted lists gives $SA$. The suffix tree is then built from $SA$ and $LCP$ with one more stack scan.

## Example

The text is $T = \texttt{mississippi}$, $n = 11$, $N = 12$. The symbols map to $\texttt{i} = 1$, $\texttt{m} = 2$, $\texttt{p} = 3$, $\texttt{s} = 4$, so $T' = 2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0$.

**L2, L3.** The odd positions 1, 3, 5, 7, 9, 11 hold the pairs `is`, `si`, `ss`, `ip`, `pi` and `$` with a pad. Their names are $R = 3, 5, 6, 2, 4, 1$. All names are different, so the recursive call returns at once with $SA_R = [6, 5, 3, 0, 4, 1, 2]$ and all LCP values 0.

**L4 to L6.** The odd and even lists:

| list | positions | suffixes | LCP |
|---|---|---|---|
| odd | 11, 7, 1, 9, 3, 5 | `$`, `ippi$`, `ississippi$`, `pi$`, `sissippi$`, `ssippi$` | 0, 0, 1, 0, 0, 1 |
| even | 10, 4, 0, 8, 6, 2 | `i$`, `issippi$`, `mississippi$`, `ppi$`, `sippi$`, `ssissippi$` | 0, 1, 0, 0, 0, 1 |

The even keys are $(1, 0)$, $(1, 5)$, $(2, 2)$, $(3, 3)$, $(4, 1)$ and $(4, 4)$: for example, position 4 has the key $(\texttt{i}, \text{rank of } 5) = (1, 5)$. The LCP of 6 and 2 is 1, because `sippi$` and `ssissippi$` share `s` and their odd tails 7 and 3 have rank 1 and 4, with $\min LCP_o[2 \ldots 4] = 0$.

**L8.** In $M$, the node $v_i$ for `i` at depth 1 has three children, by the second symbol: the even leaf 10 for `$`, the odd leaf 7 for `p`, and an overmerged node for `s`. That node joins the odd leaf 1 (`ississippi$`, depth 11) and the even leaf 4 (`issippi$`, depth 8), so it lies at depth $\min(11, 8) = 8$. It is the leaf 4, and it has the leaf 1 as its child. In the same way, the odd leaf 3 and the even leaf 6 are overmerged at depth 6, and the odd leaf 5 and the even leaf 2 at depth 7.

**L16 to L18.** For the pair 1 and 4, the chain of d-links visits

| pair | LCA in $M$ | string depth in $M$ | $\ell$ |
|---|---|---|---|
| 1, 4 | the merged node of 1 and 4 | 8 | 4 |
| 2, 5 | the merged node of 5 and 2 | 7 | 3 |
| 3, 6 | the merged node of 3 and 6 | 6 | 2 |
| 4, 7 | $v_i$ | 1 | 1 |
| 5, 8 | the root | 0 | 0 |

So $\mathrm{lcp}(\texttt{ississippi\$}, \texttt{issippi\$}) = 4$, the length of `issi`, while the depth in $M$ is 8. The values of the other three nodes on the chain are stored on the way back, and later queries that reach those nodes stop there.

**L9, L10.** The merge gives

$$SA = [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2], \qquad LCP = [0, 0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3].$$

## Correctness

The proof has five steps; the full proof is in the proof file of this page.

1. **Odd order.** Pair names keep the order of the pairs, so the suffixes of $R$ compare as the odd suffixes. The odd LCP values follow from the pairs.
2. **Even order.** $T'_p = T'[p]\,T'_{p+1}$ with $p + 1$ odd, so the key of L5 orders the even suffixes, and the LCP-RMQ reduction gives their LCP values.
3. **Same parity.** Every node of $\mathcal{T}_o$ is a node of $M$, and the children of a node of $M$ have different first symbols. So for two odd leaves, their LCA in $M$ is their LCA in $\mathcal{T}_o$, and its depth is their LCP. The same holds for the even leaves.
4. **Different parity.** For a node $v$ of $M$, let $P_o$ and $P_e$ be the strings that the odd tree and the even tree spell on the way to $v$. Every odd leaf below $v$ starts with $P_o$, and every even leaf with $P_e$. So $\mathrm{lcp}(x, y)$ for an odd $x$ and an even $y$ in different branches of $v$ is $\mathrm{lcp}(P_o, P_e)$, which depends on $v$ only. It is 0 at the root and at least 1 elsewhere, since the first symbols of merged edges agree. This gives the d-link rule.
5. **Merge.** With the right $h$, one symbol comparison orders two suffixes, and the merge of two sorted lists is sorted.

## Complexity

| case | time | extra space |
|---|---|---|
| integer alphabet, $\sigma \le n^{O(1)}$ | $\Theta(n)$ in every case | $\Theta(n)$ words |
| general ordered alphabet | $O(n \log \sigma)$ to rank the symbols, then $\Theta(n)$ | $\Theta(n)$ words |

**Time.** Without the recursive call, each step is linear: radix sort for the pair names and the even keys, a linear range minimum structure for $LCP_e$, stack scans for the trees, one walk for the overmerge, and a linear LCA structure on $M$. In the d-link step, each query costs $O(1)$ plus one step for each new value $\ell(v)$, and $M$ has $O(N)$ nodes, so all queries take $O(N)$ time. The recursive call is on $\lceil N/2 \rceil$ symbols, so $t(N) = t(N/2) + O(N)$, and $t(N) = O(N)$ by the [master theorem](/master-theorem/).

**Lower bound.** For an integer alphabet, $\Omega(n)$ time is needed to read the text. For a general ordered alphabet, building a suffix tree sorts the symbols, so $\Omega(n \log \sigma)$ comparisons are needed. Farach-Colton, Ferragina and Muthukrishnan show that suffix tree construction has the same complexity as sorting in the RAM, external memory and parallel models: the title of the journal paper.

**Space.** The text, the reduced string, the two lists and their LCP values, the two trees and $M$ take $O(N)$ words at the top level, and half as much at each lower level.

## Properties

- **Not adaptive.** The work is $\Theta(n)$ on every input; only the number of levels changes with the text.
- **Not comparison based.** Symbols are compared only when they are first ranked; after that, everything is radix sort, scans and tree walks.
- **Recursive.** One recursive call on a string half as long, with $O(\log n)$ levels.
- **Output.** The suffix tree, the suffix array and the LCP array all come out of the same run.
- **Deterministic.** With a deterministic linear LCA structure, the whole algorithm is deterministic.

## Variants and improvements

- **Unmerging the tree.** Farach does not merge the two sorted lists. After the d-link depths are known, he walks over $M$ and splits each overmerged edge at the depth $\ell(v)$, which gives the suffix tree directly. Merging the lists, as on this page, gives the same suffix array and LCP array, and the tree follows from them.
- **External memory and parallel.** Farach-Colton, Ferragina and Muthukrishnan replace each step with sorting and scanning, so suffix tree construction costs as much as sorting in the [external memory model](/external-memory-model/) and on the PRAM.
- **DC3.** The [DC3 algorithm](/dc3-skew-algorithm/) recurses on the positions not divisible by 3. For any two positions $i$ and $j$, some offset $k < 3$ puts both $i + k$ and $j + k$ in that set, so the merge needs no d-links: two symbols and one rank compare any two suffixes. With odd and even positions this is impossible, which is why Farach needs the overmerge.
- **Suffix arrays first.** [SA-IS](/sa-is/) and DC3 build the suffix array directly in linear time, and the suffix tree follows from the suffix array and the LCP array. This route has replaced Farach's merge in practice.

## When to use it

Use Farach's algorithm as the theoretical answer for suffix trees over large integer alphabets, and as the model for its external memory and parallel versions. For a program, build the suffix array with [SA-IS](/sa-is/) or [DC3](/dc3-skew-algorithm/), the LCP array with [Kasai's algorithm](/kasai-algorithm/), and the tree from both. For a small constant alphabet, [Ukkonen's algorithm](/ukkonen-algorithm/) is simpler and online.

## Pitfalls

- **The depth of an overmerged node.** It is the smaller of the two target depths, and both edges must be followed to that depth. Using the larger depth, or stopping only at nodes of both trees, loses nodes of one tree, and then the LCA of two leaves of the same parity is wrong.
- **Leaves with children.** A leaf of one tree can lie on an edge of the other tree, so a node of $M$ can be a leaf and have children. Code that assumes leaves have no children drops suffixes.
- **The depth of a node of $M$ is not an LCP.** For a pair of different parity, the depth of the LCA in $M$ is only an upper bound; in the example it is 8 for an LCP of 4. Only the d-links give the true value.
- **Long d-link chains.** A chain of d-links can be as long as $n$. Recursion on it overflows the stack; follow the chain with a loop and fill in the stored values on the way back.
- **The shift in $LCP_R$.** The sentinel of $R$ is at rank 0 of $SA_R$, so the LCP of the odd suffixes at ranks $k - 1$ and $k$ is $LCP_R[k + 1]$.
- **The last pair.** The pair at the last odd position must be padded with 0. It is the only pair that contains the sentinel, so its name is unique, and the odd LCP never runs past the end of $T'$.

## Implementations

The Python module maps the symbols to $1, \ldots, \sigma$, appends the sentinel 0 and calls the recursive core, whose depth is $O(\log n)$. It sorts with Python's sort in place of radix sort, and answers range minimum and LCA queries with [sparse tables](/sparse-table/) over an [Euler tour](/euler-tour-technique/), so it runs in $O(n \log n)$ time; a linear LCA structure would make it $O(n)$. The overmerge walk, the Euler tour and the d-link chains use loops with explicit stacks. The tests compare the suffix array and the LCP array with sorting all suffixes, check $\ell$ against the true LCP for every pair of an odd and an even suffix, and compare the suffix tree with its definition, on random strings over alphabets of size 1, 2 and 4, on the empty string, on $\texttt{a}^n$ and on $(\texttt{ab})^n$.

## History

Linear-time suffix tree construction goes back to Weiner in 1973, McCreight in 1976 and Ukkonen in 1995, but all three spend $O(\log \sigma)$ time to choose a child at each node, so they take $\Theta(n \log \sigma)$ time on a large alphabet. In 1997, Martin Farach (later Martin Farach-Colton) presented "Optimal suffix tree construction with large alphabets" at FOCS, and closed this gap for integer alphabets with the odd and even recursion. The journal version, "On the sorting-complexity of suffix tree construction", with Paolo Ferragina and S. Muthukrishnan, appeared in the Journal of the ACM in 2000. The odd and even recursion led to the linear suffix array constructions of 2003, among them the skew algorithm of Kärkkäinen and Sanders, which chose two thirds of the positions so that the merge becomes simple.

## References
