---
tag: VFC544
kind: data-structure
slug: enhanced-suffix-array
name: Enhanced suffix array
aliases:
- ESA
area: strings/suffix-structures
level: research
summary: A suffix array with LCP array and child table, simulating every suffix tree operation.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-array, lcp-array, lcp-interval-tree]
see_also: [lcp-interval-tree, suffix-tree, compressed-suffix-tree, kasai-algorithm, suffix-array-search, maximal-repeats, lcp-rmq-reduction, suffix-link]
sources:
  - paper: doi:10.1016/S1570-8667(03)00065-0
    title: Mohamed Ibrahim Abouelhoda, Stefan Kurtz and Enno Ohlebusch, Replacing suffix trees with enhanced suffix arrays, Journal of Discrete Algorithms 2(1), 2004
    locator: pages 53 to 86, the child table with the fields up, down and nextlIndex, its construction with a stack, the child intervals of an lcp-interval and the top-down search
  - paper: doi:10.1007/3-540-45784-4_35
    title: Mohamed Ibrahim Abouelhoda, Stefan Kurtz and Enno Ohlebusch, The enhanced suffix array and its applications to genome analysis, Algorithms in Bioinformatics (WABI 2002), LNCS
    locator: pages 449 to 463, the enhanced suffix array and the bottom-up traversal for repeats
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the LCP array and the bottom-up traversal of the suffix tree simulated with it
---

The enhanced suffix array (ESA) of a text is its [suffix array](/suffix-array/) together with the [LCP array](/lcp-array/) and a small *child table*, and sometimes a suffix link table. Abouelhoda, Kurtz and Ohlebusch showed that these arrays support the same traversals as a [suffix tree](/suffix-tree/): bottom up, top down from the root, and along [suffix links](/suffix-link/). So an algorithm on the suffix tree can be replaced by one on the ESA with the same time bound, in much less space. The child table has three fields per rank, `up`, `down` and `next`, and two scans of the LCP array with a stack build it in $O(n)$ time.

## In plain words

A suffix tree is fast but large. A suffix array, the sorted list of all endings of a text, is small but has no tree to walk. The enhanced suffix array adds a few numbers to the suffix array so that you can walk it like a tree.

Endings that start with the same letters stand in one block of the sorted list, and each block is one branch of the tree. To go down from a branch, you must find where its sub-blocks start. The child table stores this. For each place in the list, it gives the next place where a sub-block of the same branch starts, and two more pointers that give the first such place.

With this, you can start at the top, pick the sub-block for each letter of a pattern, and so find all places where the pattern occurs.

## The abstract type

The structure is static. It is built from a text $T$ and supports, on the nodes of the suffix tree of $T\$$ given as rank ranges:

- `children(i, j)`: the child intervals of the node $[i..j]$, in rank order;
- `lcp_value(i, j)`: the string depth of the node;
- `child(i, j, c)`: the child whose edge starts with the symbol $c$;
- `find(P)`: the rank range of the suffixes that start with the pattern $P$, by a walk from the root;
- a bottom-up traversal of all internal nodes, with the stack of the [LCP interval tree](/lcp-interval-tree/).

## Representation

The text is $T = T[0 \ldots n-1]$ over a general ordered alphabet. A sentinel $\$$, smaller than every symbol and unique, is appended, so there are $N = n + 1$ suffixes of $T\$$, at ranks $0, \ldots, n$. Positions and ranks are 0-based, and rank 0 is the suffix $\$$.

- $SA[0 \ldots n]$: the suffix array of $T\$$.
- $L[0 \ldots N]$: the LCP array, with $L[0] = 0$, $L[r] = \mathrm{lcp}$ of the suffixes at ranks $r - 1$ and $r$ for $1 \le r \le n$, and $L[N] = -1$ as an end mark.
- The child table, three arrays over $0 \ldots N$, each entry a rank or nil:
  - $up[q] = \min \{ k < q : L[k] > L[q]$ and $L[r] \ge L[k]$ for all $k < r < q \}$;
  - $down[p] = \max \{ k > p : L[k] > L[p]$ and $L[r] > L[k]$ for all $p < r < k \}$;
  - $next[i] = \min \{ k > i : L[k] = L[i]$ and $L[r] > L[i]$ for all $i < r < k \}$.

**Lcp-intervals.** A node of the suffix tree is a rank range $[i..j]$. A leaf is a single rank $[r..r]$. An internal node with $i < j$ is an *$\ell$-interval*: all of $L[i+1 \ldots j]$ are at least $\ell$, at least one, an *$\ell$-index*, equals $\ell$, and $L[i] < \ell$ and $L[j+1] < \ell$. The root is $[0..n]$ with $\ell = 0$. If the $\ell$-indices are $k_1 < \cdots < k_r$, the children are $[i..k_1 - 1], [k_1..k_2 - 1], \ldots, [k_r..j]$; see the [LCP interval tree](/lcp-interval-tree/).

**What the fields give.** For an $\ell$-interval $[i..j]$ other than the root:

- $next$ links the $\ell$-indices: $next[k_t] = k_{t+1}$, and $next[k_r]$ is nil;
- the first $\ell$-index $k_1$ is $up[j + 1]$ if $i < up[j+1] \le j$, and $down[i]$ otherwise;
- for the root, $k_1 = next[0]$, since $L[0] = 0$ and the $0$-indices form the chain from 0.

The value $\ell$ is $L[k_1]$. So the child table replaces the explicit lists of children, at three numbers per rank.

## Operations

```pseudo id=main
ESA-CHILD-TABLE(L, N)            ▷ L[0] = 0 and L[N] = −1; all fields start as nil
L1  last ← nil; stack ← [0]
L2  for i ← 1 to N do
L3      while stack ≠ ∅ and L[i] < L[top] do
L4          last ← pop
L5          if stack ≠ ∅ and L[i] ≤ L[top] and L[top] ≠ L[last] then down[top] ← last
L6      if last ≠ nil then up[i] ← last; last ← nil
L7      push i
L8  stack ← [0]
L9  for i ← 1 to N do
L10     while stack ≠ ∅ and L[i] < L[top] do pop
L11     if stack ≠ ∅ and L[i] = L[top] then next[pop] ← i
L12     push i

ESA-CHILDREN(i, j)               ▷ an lcp-interval [i..j] with i < j
L13 if [i..j] is the root [0..n] then k ← next[0]
L14 else if i < up[j + 1] ≤ j then k ← up[j + 1] else k ← down[i]
L15 emit [i..k − 1]
L16 while next[k] ≠ nil do emit [k..next[k] − 1]; k ← next[k]
L17 emit [k..j]
```

**Up and down (L1 to L7).** The stack holds ranks whose $L$ values do not decrease from the bottom. At rank $i$, every rank on top with a larger value is popped (L3, L4). The last rank popped is the nearest rank before $i$ with a larger value whose run reaches $i$, so it becomes $up[i]$ (L6). When the stack top after a pop still has a value of at least $L[i]$ and differs from the popped value, the popped rank is the last rank after the top with a larger value and no smaller value in between, so it becomes $down[top]$ (L5).

**Next (L8 to L12).** The second scan keeps a stack of strictly increasing values. When $L[i]$ equals the value on top after the pops, the top is the previous rank with the same value and only larger values in between, so its $next$ is $i$ (L11).

**Children (L13 to L17).** The first $\ell$-index comes from $up$ or $down$ (L14), and the others from the $next$ chain (L16). Each child costs $O(1)$.

**Child by symbol.** `child(i, j, c)` scans the children and compares the symbol $T\$[SA[a] + \ell]$ of each child $[a..b]$ with $c$, which costs $O(\sigma)$.

**Find.** Start at the root with $d = 0$. While $d < m$: if the current node is a leaf, the suffix has ended, and $P$ does not occur. Otherwise take the child for $P[d]$; if there is none, $P$ does not occur. Compare $P[d+1 \ldots e-1]$ with the text at $SA[a] + d + 1$, where $e = \min(m, \ell)$ and $\ell$ is the string depth of the child, or the suffix length for a leaf, then set $d \gets e$. The answer is the rank range of the last node.

## Example

The text is $T = \texttt{mississippi}$, $n = 11$, so $T\$$ has $N = 12$ suffixes. The dash means nil.

| $r$ | $SA[r]$ | $L[r]$ | $up$ | $down$ | $next$ | suffix |
|---|---|---|---|---|---|---|
| 0 | 11 | 0 | - | - | 1 | `$` |
| 1 | 10 | 0 | - | 2 | 5 | `i$` |
| 2 | 7 | 1 | - | - | 3 | `ippi$` |
| 3 | 4 | 1 | - | 4 | - | `issippi$` |
| 4 | 1 | 4 | - | - | - | `ississippi$` |
| 5 | 0 | 0 | 2 | - | 6 | `mississippi$` |
| 6 | 9 | 0 | - | 7 | 8 | `pi$` |
| 7 | 8 | 1 | - | - | - | `ppi$` |
| 8 | 6 | 0 | 7 | 10 | - | `sippi$` |
| 9 | 3 | 2 | - | - | - | `sissippi$` |
| 10 | 5 | 1 | 9 | 11 | - | `ssippi$` |
| 11 | 2 | 3 | - | - | - | `ssissippi$` |
| 12 | | -1 | 0 | - | - | |

**Children of the root.** The chain from $next[0]$ is 1, 5, 6, 8, so the children are $[0..0]$ (`$`), $[1..4]$ (`i`), $[5..5]$ (`m...`), $[6..7]$ (`p`) and $[8..11]$ (`s`).

**Children of $[1..4]$.** Here $up[5] = 2$ and $1 < 2 \le 4$, so $k_1 = 2$ and $\ell = L[2] = 1$. Then $next[2] = 3$ and $next[3]$ is nil, so the children are $[1..1]$, $[2..2]$ and $[3..4]$.

**Children of $[8..11]$.** Here $up[12] = 0$ is not in the range, so $k_1 = down[8] = 10$ and $\ell = L[10] = 1$. $next[10]$ is nil, so the children are $[8..9]$ (`si`) and $[10..11]$ (`ssi`).

**Find `ssi`.** From the root, the child for `s` is $[8..11]$ with $\ell = 1$. Its child for the symbol `s` at depth 1 is $[10..11]$ with $\ell = L[11] = 3$, and the text at $SA[10] = 5$ reads `ssi`. The answer is the ranks 10 and 11, at the positions 5 and 2.

## Correctness

The full proof is in the proof file of this page. Its main steps:

1. **Up.** When rank $i$ is pushed in the first scan, the stack holds, from the bottom, the ranks before $i$ that have no smaller value after them before $i$. The ranks popped at $i$ are those of them with a value above $L[i]$, and the last one popped is the smallest such rank whose run of values at least its own reaches $i$, which is the definition of $up[i]$.
2. **Down.** A rank $p$ gets $down[p]$ set to the popped rank $k$ exactly when $L[k] > L[p]$, no value between them is at most $L[k]$, and no later rank can satisfy this, because a later candidate would have $k$ in between with a value that is not larger.
3. **Next.** In the second scan the stack holds strictly increasing values, and $L[i] = L[top]$ after the pops means that the top is the nearest earlier rank with the value $L[i]$ and only larger values in between.
4. **Children.** If $L[j+1] \ge L[i]$, then the nearest rank before $j + 1$ with a larger value and a run up to $j + 1$ is the first $\ell$-index, so $k_1 = up[j+1]$. Otherwise $L[i] > L[j+1]$, and $k_1 = down[i]$, since the $\ell$-indices are the minima of $L[i+1 \ldots j]$ and the first of them is the last rank after $i$ with only larger values before it.

## Complexity

| operation | time | space |
|---|---|---|
| child table, given $SA$ and $L$ | $O(n)$ | three arrays of $N + 1$ entries, plus a stack |
| build from the text | $O(n)$ for an integer alphabet with a linear suffix sort and [Kasai's algorithm](/kasai-algorithm/); the implementation sorts by prefix doubling | $\Theta(n)$ words |
| `children(i, j)`, `lcp_value(i, j)` | $O(\text{number of children})$ and $O(1)$ | |
| `child(i, j, c)` | $O(\sigma)$ | |
| `find(P)` | $O(m \sigma)$, which is $O(m)$ for a constant alphabet | |
| bottom-up traversal | $O(n)$ | a stack of $O(n)$ words |

Each rank is pushed once and popped at most once in each scan, so the child table takes $O(n)$ time. `find` visits at most $m + 1$ nodes, scans at most $\sigma$ children at each, and compares each symbol of $P$ once.

## Variants

- **One array.** Abouelhoda, Kurtz and Ohlebusch store the three fields in one array of $N$ entries, since the $up$ and $down$ values of a rank can share the place of an unused $next$ value.
- **Suffix links.** A suffix link table gives, for each lcp-interval $[i..j]$ with label $cu$, the interval of $u$. With it, the ESA supports the algorithms that follow suffix links, such as [matching statistics](/matching-statistics/).
- **Bottom-up only.** Many problems, such as [maximal repeats](/maximal-repeats/) and the [longest repeated substring](/longest-repeated-substring/), need only $SA$, $L$ and the bottom-up stack of the [LCP interval tree](/lcp-interval-tree/), and no child table.
- **Search without the child table.** The [suffix array search](/suffix-array-search/) of Manber and Myers finds a pattern in $O(m + \log n)$ time with extra LCP values for the binary search.
- **Compressed.** The [compressed suffix tree](/compressed-suffix-tree/) replaces $SA$ by a compressed suffix array and $L$ and the child table by compressed structures with range minimum and next smaller value queries.

## When to use it

Use the enhanced suffix array when you need suffix tree algorithms on a large text, such as a genome, and a pointer-based suffix tree does not fit in memory. It is a few integer arrays, it is easy to store on disk and to load, and its scans are friendly to the cache. Use a [suffix tree](/suffix-tree/) for an index that must grow online, and a [compressed suffix tree](/compressed-suffix-tree/) when even $\Theta(n)$ words are too many.

## Pitfalls

- **The end mark.** The scans need $L[N] = -1$, smaller than every value. With $L[N] = 0$, the last 0-index gets $next = N$, and the children of the root end with a wrong interval that starts at $N$.
- **The root.** For $[0..n]$, the rule with $up$ and $down$ does not apply: $up[N] = 0$ is outside the range, and $down[0]$ is not a 0-index. The first 0-index is $next[0]$.
- **Equal values.** The condition $L[top] \ne L[last]$ in line L5 matters: when equal values are popped one after the other, only the first of them gives a $down$ value.
- **Two scans.** The scans for $up$ and $down$ and for $next$ use different stacks: the first keeps equal values, the second replaces them. Merging them into one scan gives wrong $up$ values.
- **The sentinel.** Without $\$$, a suffix can be a prefix of another and end inside an interval, and the root can have one child; the definitions then need extra cases.

## Implementations

The Python class builds $SA$ of $T\$$ by prefix doubling, $L$ by Kasai's method and the child table with the two scans. The tests check $up$, $down$ and $next$ against their definitions, the children of every node against the suffix tree built from the branching substrings, and `find` against a scan of the suffix array, on random strings over alphabets of size 1, 2 and 4 and on $\texttt{a}^n$ and $(\texttt{ab})^n$.

## History

Kasai, Lee, Arimura, Arikawa and Park gave the linear-time LCP array in 2001 and showed how to simulate a bottom-up traversal of the suffix tree with it. Abouelhoda, Kurtz and Ohlebusch introduced the enhanced suffix array at WABI 2002, with applications to repeats in genomes, and in the 2004 journal paper added the child table and the suffix link table, which made top-down search and suffix link walks possible, and showed that every suffix tree algorithm can be run on the enhanced suffix array with the same time bound. The structure is used in tools for genome analysis such as Kurtz's Vmatch.

## References
