---
tag: 763NVN
kind: algorithm
slug: webgraph-compression
name: WebGraph compression
aliases:
- Boldi-Vigna compression
area: graphs/graph-representation
level: research
summary: Compresses web graphs using locality, copying and gap encoding of adjacency lists.
solves: [graph-compression]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, W: the window size}
  time: {expected: O(W (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, lossless: true, sequential: true}
prereqs: [adjacency-list, elias-gamma-coding, delta-encoding, graph-compression]
see_also: [graph-compression, succinct-graph-representation, compressed-sparse-row, elias-gamma-coding, golomb-coding, delta-encoding, pagerank, reverse-cuthill-mckee]
sources:
  - paper: doi:10.1145/988672.988752
    title: Paolo Boldi and Sebastiano Vigna, The WebGraph framework I, compression techniques, WWW 2004
    locator: pages 595 to 602, the format of a successor list (outdegree, reference, copy blocks, intervals and residuals), the window and the maximum reference chain, and the measured bits per link
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: Chapter 9 (Graphs), the section on web graphs and the Boldi-Vigna representation
---

WebGraph compression, by Boldi and Vigna, stores a directed [graph](/graph/) as a bit stream of its successor lists, using two properties of web graphs when the pages are numbered in the lexicographic order of their URLs. **Locality**: most links go to pages with nearby numbers, so the successors of $x$ are close to $x$ and to each other, and their gaps are small. **Similarity**: pages of the same site, which have nearby numbers, often link to almost the same pages, so a list can be written as a copy of a recent list plus a few changes. Each list is coded as a reference to one of the previous $W$ lists, copy blocks that say which successors of the reference to keep, intervals of consecutive successors, and gap-coded residuals. The paper reports about three bits per link on large crawls, against more than twenty for a plain array of successors.

## In plain words

Number the web pages in alphabetical order of their addresses. Pages of one site are then neighbours, and their links point to nearby numbers. To store the links of page $x$, look back at the last few pages. If one of them has many of the same links, say "like page $x - r$, but keep only these parts of its list". For what is left, a run of consecutive numbers is written as its start and length. The other numbers are written as differences from the previous one, which are small and take few bits with a variable-length code.

## The problem

The input is a directed graph on $0, \ldots, n - 1$, given as sorted lists $S_0, \ldots, S_{n-1}$ of distinct successors, a window $W \ge 0$ and a minimum interval length $L_{\min} \ge 1$. The output is a bit string from which a decoder that knows $L_{\min}$ recovers every list exactly. The goal is to make the string short; the problem of [graph compression](/graph-compression/) asks the same with fast access.

## The algorithm

Every integer $k \ge 0$ is written with the [Elias gamma code](/elias-gamma-coding/) $\gamma(k)$ of $k + 1$. A value that may be negative is first mapped by $\nu(z) = 2z$ for $z \ge 0$ and $\nu(z) = 2|z| - 1$ for $z < 0$. The string starts with $\gamma(n)$.

```pseudo id=main
ENCODE(S_0, …, S_{n−1}, W, L_min)
L1  for x ← 0 to n − 1 do write γ(|S_x|); if S_x = ∅ then continue with the next x
L2      for r ← 1 to min(W, x) do gain(r) ← |S_{x−r} ∩ S_x|
L3      r* ← the r of largest gain, the smallest on ties; r* ← 0 if every gain is 0
L4      write γ(r*)
L5      if r* > 0 then write the copy blocks of S_{x−r*} against S_x
L6      E ← S_x minus the successors copied from S_{x−r*}
L7      split E into the maximal runs of consecutive integers of length ≥ L_min (intervals) and the rest (residuals)
L8      write the intervals
L9      for each residual y, in increasing order, do
L10         write γ(ν(y − x)) for the first y, and γ(y − y′ − 1) for the others, where y′ is the previous residual
L11 return the bits written
```

**Copy blocks (line L5).** Mark each successor of the reference list with 1 if it is in $S_x$ and 0 if not. Cut this mask into runs that alternate 1s and 0s, starting with a run of 1s, which may be empty. Write the number $b$ of runs without the last one, then the first run length as it is and the others minus 1, since only the first can be empty. The last run is implicit: it is the rest of the reference list.

**Intervals (line L8).** Write the number of intervals. For each interval $[a, a + \lambda)$ write the left end, as $\gamma(\nu(a - x))$ for the first one and as $\gamma(a - e - 1)$ for the others, where $e$ is the end of the previous interval, then $\gamma(\lambda - L_{\min})$.

**Residuals (lines L9 and L10).** The first one is coded relative to $x$, since by locality it is near $x$ but may be below it; the others by their gaps minus 1, which are $\ge 0$ because the list has no duplicates. The decoder knows how many residuals to read: $|S_x|$ minus the copied successors minus the interval lengths.

**Decoding** reads the same fields in the same order. For a reference $r^* > 0$ it needs the decoded list $x - r^*$, so it keeps the last $W$ lists.

## Example

Take $n = 5$, $W = 7$, $L_{\min} = 3$, and the lists

| $x$ | $S_x$ |
|---|---|
| 0 | 13, 15, 16, 17, 18, 19, 23, 24, 203 |
| 1 | 15, 16, 17, 22, 23, 24, 315, 316, 317, 3041 |
| 2, 3 | empty |
| 4 | 16, 17, 18, 19, 20, 21, 22, 23, 24, 203, 315, 1034 |

| $x$ | $r^*$ (gain) | copy blocks | intervals | residuals | bits |
|---|---|---|---|---|---|
| 0 | 0 (no window) | | $[15, 20)$ | 13, 23, 24, 203 | 55 |
| 1 | 1 (5) | $b = 5$: 0, 1, 3, 2, 2 | $[315, 318)$ | 22, 3041 | 83 |
| 2, 3 | | | | | 1 each |
| 4 | 4 (7) | $b = 2$: 0, 2 | $[20, 23)$ | 315, 1034 | 72 |

For $x = 1$ the mask of $S_0$ is $0\,1\,1\,1\,0\,0\,1\,1\,0$: an empty copy run, skip 13, copy 15 to 17, skip 18 and 19, copy 23 and 24, and the implicit last run skips 203. The rest is $\{22, 315, 316, 317, 3041\}$: the interval $315, 316, 317$, and the residuals 22, written as $\gamma(\nu(21)) = \gamma(42)$, 11 bits, and 3041, written as $\gamma(3018)$, 23 bits. For $x = 4$, the list $S_1$ at distance 3 shares 6 successors and $S_0$ at distance 4 shares 7, so $r^* = 4$. With $\gamma(5)$ for $n$, the total is $5 + 55 + 83 + 1 + 1 + 72 = 217$ bits for 31 arcs, against 372 bits for 12-bit successors.

## Correctness

**Claim.** DECODE(ENCODE$(S, W, L_{\min})$, $L_{\min}$) $= S$ for all sorted, duplicate-free lists. The key facts are that the gamma code is prefix-free and $\nu$ is a bijection, so each field is read back exactly; that the copied set, the intervals and the residuals partition $S_x$; and that every number written is $\ge 0$: interval gaps because the intervals are maximal runs, so two of them are separated by at least one missing integer, and residual gaps because the list has no duplicates. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/), with a hash set for each list.

- **Time.** For each $x$, line L2 tests the successors of up to $W$ previous lists against a hash set of $S_x$. Each list is tested by at most $W$ later lists, so the total is $O(W(n + m))$ expected. Lines L5 to L10 take $O(|S_{x-r^*}| + |S_x|)$, also within this bound. Decoding is $O(n + m)$ plus the copied lists, $O(W(n+m))$ in the worst case.
- **Space.** The encoder keeps all lists, $O(n + m)$ words; a streaming encoder needs only the last $W$.
- **Output.** A gap $g$ costs $2 \lfloor \log_2(g + 1) \rfloor + 1$ bits, so locality, small gaps, is what makes the code short. Without references and intervals, the method is gap coding of an [adjacency list](/adjacency-list/), a [delta encoding](/delta-encoding/) of each list.

## Properties

- **Lossless and deterministic.** The decoder recovers the lists exactly.
- **Sequential.** Decoding $S_x$ may need $S_{x - r^*}$, which may need its own reference, and so on. Random access needs an index of offsets and a bound on these chains.
- **Order dependent.** The same graph under another numbering of the vertices may take several times more bits.

## Variants and improvements

- **Codes.** WebGraph writes residuals with $\zeta_k$ codes, which suit the power-law distribution of the gaps, and other fields with gamma or unary codes; [Golomb codes](/golomb-coding/) are another choice.
- **Bounded reference chains.** WebGraph takes the parameter $R$, the maximum length of a chain of references, and never picks a reference that would exceed it, so a list is decoded with at most $R$ other lists. Small $R$ gives fast random access at some cost in size.
- **Choosing the reference by cost.** Instead of the largest overlap, try each $r$ in the window and keep the one with the fewest bits.
- **Orderings.** For graphs with no URLs, such as social networks, the numbering must be computed. Orders from clustering, such as layered label propagation, or by shingles bring back locality and similarity.
- **Random-access structures.** The $k^2$-tree and [succinct representations](/succinct-graph-representation/) give adjacency queries without sequential decoding, usually with more bits for web graphs.

## When to use it

Use it for very large, static, sparse directed graphs with locality: web crawls, citation graphs, software dependency graphs, and social networks after a good reordering. It suits algorithms that scan all lists in order, such as [PageRank](/pagerank/) or breadth-first search. When the graph changes, keep an [adjacency list](/adjacency-list/). When the numbering is random and cannot be changed, gap coding gives little and a plain [compressed sparse row](/compressed-sparse-row/) array is nearly as small.

## Pitfalls

- **A negative first gap.** The first residual may be below $x$. Writing $\gamma(y - x)$ at line L10 fails for $y < x$; write $\gamma(\nu(y - x))$. The same holds for the first interval at line L8.
- **Off-by-one in the copy blocks.** Writing every run length minus 1 at line L5 fails when the reference list starts with a successor that is not copied, because the first run is then empty. Write the first run as it is and only the later runs, which are never empty, minus 1.
- **Unbounded reference chains.** Picking the best reference at line L3 with no limit can build a chain through the whole graph, so that decoding one list decodes all the lists before it.
- **The vertex order.** Compressing a graph in a random order gives poor results. Sort by URL, or reorder, before line L1.

## Implementations

The Python module gives `encode` and `decode` on lists of sorted successors, with the window and $L_{\min}$ as parameters, plus the helpers `gamma`, `nu`, `copy_blocks` and `split_intervals`. It writes every field with the gamma code, picks the reference by overlap, and has no chain bound; the output is a string of `0` and `1`.

## History

The Connectivity Server and then the Link Database of Randall, Stata, Wiener and Wickremesinghe at Compaq, around 2001, already numbered pages by URL, gap-coded the lists, and wrote a list as a copy of a nearby one. Boldi and Vigna's WebGraph framework of 2004 added copy blocks, intervals, the window and the bound on reference chains, and new codes, and became the standard tool for storing and distributing web crawls. Later work moved the method to social networks by computing good vertex orders.

## References
