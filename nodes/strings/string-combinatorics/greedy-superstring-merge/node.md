---
tag: HBAFAC
kind: algorithm
slug: greedy-superstring-merge
name: Greedy superstring merging
aliases:
- greedy shortest superstring
- greedy overlap merging
area: strings/string-combinatorics
level: core
summary: Repeatedly merges the pair of strings with the largest overlap, giving an approximation.
solves: [shortest-common-superstring]
model: word-ram
complexity:
  vars: {m: the number of strings, n: the total length of the strings}
  time: {worst: O(m·n + m^2·log m)}
  space: {extra: O(n + m^2)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [shortest-common-superstring, overlap-graph, prefix-function]
see_also: [greedy-shortest-common-superstring, shortest-common-superstring-np-hard, held-karp-algorithm, asymmetric-tsp, overlap-layout-consensus, approximation-ratio, greedy-algorithm, de-bruijn-assembly]
sources:
  - paper: doi:10.1016/0304-3975(88)90167-3
    title: Jorma Tarhio and Esko Ukkonen, A greedy approximation algorithm for constructing shortest common superstrings, Theoretical Computer Science 57(1), 1988, 131-145
    locator: the greedy merging algorithm, the bound of one half on its compression, the lower bound example of ratio 2 and the conjecture that 2 is the worst ratio
  - paper: doi:10.1016/0890-5401(89)90044-8
    title: Jonathan S. Turner, Approximation algorithms for the shortest common superstring problem, Information and Computation 83(1), 1989, 1-20
    locator: the greedy algorithm on the overlap graph and its compression bound of one half
  - paper: doi:10.1145/179812.179818
    title: Avrim Blum, Tao Jiang, Ming Li, John Tromp and Mihalis Yannakakis, Linear approximation of shortest superstrings, Journal of the ACM 41(4), 1994, 630-647
    locator: the overlap inequality for a pair with the largest overlap and the proof that greedy is within a factor 4 of the optimal length
  - paper: doi:10.1016/j.ipl.2004.09.012
    title: Haim Kaplan and Nira Shafrir, The greedy algorithm for shortest superstrings, Information Processing Letters 93(1), 2005, 13-17
    locator: the improved factor 3.5 for the greedy algorithm
  - paper: doi:10.1007/bf01840391
    title: Esko Ukkonen, A linear-time algorithm for finding approximate shortest common superstrings, Algorithmica 5(1-4), 1990, 313-323
    locator: an implementation of the greedy merging with the Aho-Corasick automaton in time linear in the total length
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 16, the shortest superstring problem (the greedy algorithm and the reduction to a substring-free set)
  - url: "https://arxiv.org/abs/2111.03968"
    title: Matthias Englert, Nicolaos Matsakis and Pavel Veselý, Improved approximation guarantees for shortest superstrings using cycle classification by overlap to length ratios, STOC 2022
    locator: the bound (13 + 57^(1/2))/6 for the greedy algorithm
---

Greedy superstring merging builds a short common superstring of a set of strings by repeatedly merging the two strings with the largest overlap, until one string is left. It is the standard heuristic for the NP-hard [shortest common superstring](/shortest-common-superstring/) problem: its output is at most 4 times longer than the optimum (Blum et al.), and it saves at least half of the letters that an optimal superstring saves (Tarhio and Ukkonen, Turner). Run on the [overlap graph](/overlap-graph/), it takes the edges in order of decreasing weight and keeps those that still extend a path, so it takes $O(m \cdot n + m^2 \log m)$ time for $m$ strings of total length $n$.

## In plain words

You have a pile of strips of text and want one short text that contains all of them. First throw away any strip that already appears inside another strip. Then look at every pair of strips and ask how much the end of one strip agrees with the start of the other. Glue together the pair that agrees the most, sharing the common part, and put the glued strip back in the pile. Repeat until one strip is left. Each glue step is the best local choice; it is not always the best overall, but it is never very bad.

## The problem

The input is a list of $m_0$ strings over an [alphabet](/alphabet/) $\Sigma$; only equality of letters is used. Indices are 0-based. The output is a string that contains each input string as a contiguous substring, and the aim is that it be short. For strings $x$ and $y$, the overlap $\mathrm{ov}(x, y)$ is the length of the longest suffix of $x$ that is also a prefix of $y$. The merge of $x$ and $y$ is $x \cdot y[\mathrm{ov}(x, y)..|y|-1]$.

A list is substring-free if no string occurs inside another one and there are no repeats. After the first step, the list $s_0, \ldots, s_{m-1}$ is substring-free, and $n = |s_0| + \cdots + |s_{m-1}|$. Then $\mathrm{ov}(s_i, s_j) < \min(|s_i|, |s_j|)$ for $i \ne j$, since an overlap of full length would put one string inside the other.

## The algorithm

The algorithm works on the overlap graph: the vertex $i$ is the string $s_i$, and the edge $(i, j)$ with $i \ne j$ has the weight $w(i, j) = \mathrm{ov}(s_i, s_j)$. It keeps a set of vertex-disjoint paths, called chains, starting from $m$ chains of one vertex each. For each chain it stores the head and the tail, so that $\mathit{head}[t]$ is the head of the chain whose tail is $t$.

```pseudo id=main
GREEDY-SUPERSTRING(S)
L1  remove repeats and the strings of S inside other strings; call the rest s[0 .. m − 1]
L2  for each pair i ≠ j do w(i, j) ← ov(s[i], s[j])
L3  sort the pairs (i, j) by decreasing w(i, j), ties by smaller i, then smaller j
L4  for each pair (i, j) in this order do
L5      if next[i] = nil and prev[j] = nil and head[i] ≠ j then
L6          next[i] ← j, prev[j] ← i, join the chain ending at i to the chain starting at j
L7  h ← the vertex with prev[h] = nil, R ← s[h]
L8  while next[h] ≠ nil do R ← R · s[next[h]][w(h, next[h]) ..], h ← next[h]
L9  return R
```

Line L5 accepts the edge $(i, j)$ when $i$ is the tail of a chain, $j$ is the head of a chain, and the two chains differ; for a tail $i$ and a head $j$, the test $\mathit{head}[i] \ne j$ says exactly that. Joining two chains in line L6 sets the head of the new tail and the tail of the new head, in $O(1)$ time. Lines L7 and L8 walk the final chain and spell the superstring. The overlaps of line L2 come from the [prefix function](/prefix-function/) of $s_j \,\#\, s_i$, where $\#$ is a separator that occurs in no string.

Taking edges in this order is the same as merging strings: after the merge of the chains ending at $i$ and starting at $j$, the overlap of the merged string with any other chain is the overlap that its tail $j$ already had, and the overlap of any chain with the merged string is the overlap with its head $i$ (see Correctness). So line L5 accepts, at each step, a pair of current strings with the largest overlap.

## Example

Let $S = ($`abb`, `bba`, `bbb`$)$, already substring-free, with indices 0, 1, 2. The overlaps are $w(0, 1) = 2$, $w(0, 2) = 2$, $w(2, 1) = 2$, $w(1, 0) = 1$, and $w(1, 2) = w(2, 0) = 0$.

| pair | $w$ | test of L5 | chains after the step |
|---|---|---|---|
| $(0, 1)$ | 2 | accept | `abb`$\to$`bba`, `bbb` |
| $(0, 2)$ | 2 | $\mathit{next}[0]$ is set | same |
| $(2, 1)$ | 2 | $\mathit{prev}[1]$ is set | same |
| $(1, 0)$ | 1 | $\mathit{head}[1] = 0$, same chain | same |
| $(1, 2)$ | 0 | accept | `abb`$\to$`bba`$\to$`bbb` |

The walk from the head 0 spells `abb` $\cdot$ `a` $\cdot$ `bbb` $=$ `abbabbb`, of length $9 - 2 - 0 = 7$. The shortest superstring is `abbba`, of length 5, from the order `abb`, `bbb`, `bba`. With the input order $($`abb`, `bbb`, `bba`$)$, the same tie rule takes the edge from `abb` to `bbb` first and finds `abbba`.

## Correctness

The output contains every input string, by two facts. First, a string removed in line L1 occurs inside some kept string: the relation "is a proper substring of" has no infinite chains, so following it from a removed string reaches a kept one. Second, after each step of line L8, $R$ ends with $s[h]$: the part appended is $s[\mathit{next}[h]]$ without its prefix of length $w(h, \mathit{next}[h])$, and that prefix is a suffix of $s[h]$, so of $R$. The chain covers all $m$ vertices, because line L5 accepts an edge between a tail and a head of different chains whenever one exists, and every such edge is tried. So $|R| = n - \sum w$ over the accepted edges. The proof file gives the details and the equivalence with merging strings.

## Complexity

- **Overlaps.** Each overlap $\mathrm{ov}(s_i, s_j)$ costs $O(|s_i| + |s_j|)$ with the prefix function, and the sum over the $m(m-1)$ ordered pairs is $2(m-1)n$. Line L1 tests each pair for an occurrence in the same way. Both are $O(m \cdot n)$.
- **Scan.** Sorting the $m(m-1)$ pairs takes $O(m^2 \log m)$ time; a counting sort by weight, which is at most $n$, takes $O(m^2 + n)$. Each test and join in lines L5 and L6 is $O(1)$, and lines L7 and L8 take $O(n)$.
- **Total.** $O(m \cdot n + m^2 \log m)$ time and $O(n + m^2)$ space. With all overlaps computed in $O(n + m^2)$ time by the method of Gusfield, Landau and Schieber, the time is $O(n + m^2)$, and Ukkonen showed how to run the whole greedy in time linear in $n$ with an Aho-Corasick automaton of the strings.

## Properties

- **Approximation of the length.** The output has length at most $4 \cdot \mathrm{OPT}$ (Blum et al.), and the factor was later lowered to 3.5 (Kaplan and Shafrir) and $(13 + \sqrt{57})/6 \approx 3.425$ (Englert, Matsakis and Veselý).
- **Approximation of the compression.** The compression of a superstring $R$ is $n - |R|$, the number of letters saved by the overlaps. Greedy reaches at least half of the optimal compression (Tarhio and Ukkonen; Turner).
- **The overlap inequality.** If $\mathrm{ov}(u, v) = k$ is at least $\mathrm{ov}(u, t) = a$ and $\mathrm{ov}(s, v) = b$, then $\mathrm{ov}(s, t) \ge a + b - k$. The prefix of $v$ of length $b$ and the suffix of $u$ of length $a$ both lie in the common part of length $k$ at the end of $u$, so they share $a + b - k$ letters, which form a suffix of $s$ and a prefix of $t$. This is the main tool of the bounds above: taking $(u, v)$ first loses at most what the two edges $(u, t)$ and $(s, v)$ would have given, minus $\mathrm{ov}(s, t)$.
- **Lower bound.** The list $a b^k$, $b^k a$, $b^{k+1}$ has the optimum $a b^{k+1} a$ of length $k + 3$, but greedy may first merge $ab^k$ with $b^k a$, since all three overlaps of size $k$ tie, and then output a string of length $2k + 3$. So no bound below 2 holds for every tie rule.
- **Deterministic.** With a fixed tie rule, the output depends only on the list and its order.

## Variants and improvements

- **String form.** Keep the current strings and merge two of them with the largest overlap, recomputing overlaps. It gives the same output as the graph form with matching ties, but costs much more time.
- **Cycle-cover algorithms.** Blum et al. compute a minimum-weight cycle cover of the distance graph and open each cycle, for a factor 3; later methods with more careful cycle handling reach about 2.47. These are better in theory, and greedy is usually as good in practice.
- **Exact solutions.** For small $m$, dynamic programming over subsets, the [Held-Karp algorithm](/held-karp-algorithm/) on the overlap graph, finds an optimal superstring in $O(m^2 2^m)$ time once the overlaps are known.
- **Genome assembly.** Early assemblers merged reads greedily by overlap; the [overlap-layout-consensus](/overlap-layout-consensus/) and [de Bruijn graph](/de-bruijn-assembly/) approaches replaced plain greedy merging for large data. The biology view of the same algorithm is the [greedy shortest common superstring](/greedy-shortest-common-superstring/).

## When to use it

Use it when you need a short superstring of many strings quickly and a factor of a few above the optimum is fine: data compression of string tables, packing many patterns into one buffer, or a first layout of reads. For a few strings, use an exact method instead. When the strings are reads with errors, an exact overlap is too strict; assemblers allow mismatches in the overlaps.

## Pitfalls

- **Skipping the substring removal.** If $s_i$ occurs inside $s_j$, the overlap can be as long as $s_i$, and a merge then copies $s_i$ next to $s_j$ instead of absorbing it. Remove such strings, and repeats, first.
- **Recomputing overlaps after each merge in the string form.** It is correct but costs a full recomputation per merge; the graph form computes each overlap once.
- **Accepting an edge inside one chain.** Without the test $\mathit{head}[i] \ne j$, the edge from the tail of a chain to its own head closes a cycle, and the walk of line L8 never ends or loses strings. In the example, the edge $(1, 0)$ would close `abb`$\to$`bba`$\to$`abb`.
- **Counting the overlap of a string with itself.** The pair $i = j$ must be skipped; $\mathrm{ov}(x, x)$ is the longest border of $x$, not a merge of two strings.
- **Relying on ties.** As the lower bound shows, ties decide whether greedy is optimal or twice the optimum. A fixed rule makes the output reproducible, not better.

## Implementations

## History

Gallant, Maier and Storer proved in 1980 that the shortest superstring problem is NP-hard. Tarhio and Ukkonen (1988) and Turner (1989) proved independently that greedy achieves at least half of the optimal compression; Tarhio and Ukkonen also gave the example of ratio 2 and conjectured that the length ratio is at most 2. Ukkonen gave a linear-time implementation in 1990. Blum, Jiang, Li, Tromp and Yannakakis proved the first constant factor for the length, 4, at STOC 1991 (journal version 1994). Kaplan and Shafrir lowered it to 3.5 in 2005, and Englert, Matsakis and Veselý to about 3.425 in 2022.

## References
