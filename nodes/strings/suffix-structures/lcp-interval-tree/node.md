---
tag: GAWS4P
kind: data-structure
slug: lcp-interval-tree
name: LCP interval tree
aliases:
- enhanced suffix tree internal nodes
- suffix array tree
area: strings/suffix-structures
level: advanced
summary: The suffix tree topology obtained from the suffix array and LCP array alone.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [lcp-array, suffix-array, suffix-tree]
see_also: [enhanced-suffix-array, lcp-rmq-reduction, suffix-tree-from-suffix-array, kasai-algorithm, cartesian-tree, maximal-repeats, compressed-suffix-tree, longest-repeated-substring]
sources:
  - paper: doi:10.1016/S1570-8667(03)00065-0
    title: Mohamed Ibrahim Abouelhoda, Stefan Kurtz and Enno Ohlebusch, Replacing suffix trees with enhanced suffix arrays, Journal of Discrete Algorithms 2(1), 2004
    locator: pages 53 to 86, the definition of lcp-intervals, the lcp-interval tree, child intervals and the bottom-up traversal with a stack
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089
    locator: pages 181 to 192, the simulation of a bottom-up traversal of the suffix tree with the suffix array and the height array
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press, 2015
    locator: Chapter 8 (Classical indexes), the suffix tree simulated with the suffix array and the LCP array
---

An lcp-interval of a text is a maximal range of ranks of its [suffix array](/suffix-array/) in which all suffixes share a prefix of some length $\ell$, and some two neighbors share no more. The lcp-intervals, ordered by containment, form the LCP interval tree, which has the same shape as the internal nodes of the [suffix tree](/suffix-tree/): each interval is a node, and its value $\ell$ is the string depth. Abouelhoda, Kurtz and Ohlebusch defined it as the basis of the [enhanced suffix array](/enhanced-suffix-array/), and one left-to-right scan of the [LCP array](/lcp-array/) with a stack builds it, or visits it bottom up, in $O(n)$ time.

## In plain words

Sort all endings of a text. Endings that start with the same letters stand next to each other in the sorted list. So every shared start, such as "ssi" in "mississippi", owns one block of the list: the block of all endings that start with it.

Such blocks nest. The block of "s" contains the block of "ssi", just as the branch "s" of a suffix tree contains the branch "ssi". So the blocks form a tree with the same shape as the suffix tree, and you get it without building the suffix tree.

To find the blocks, read the list of shared lengths from top to bottom and keep a stack of open blocks. A larger number opens a new block. A smaller number closes the open blocks that are deeper than it.

## The abstract type

The structure is static. It is built from a text, or from its suffix array and LCP array, and supports:

- `intervals()`: all lcp-intervals, each as its value $\ell$ and its rank range $[lb, rb]$;
- `children(v)`: the child intervals of $v$ in rank order, with single ranks as leaves;
- `label(v)`: the shared prefix of length $\ell$ of the interval;
- `find(P)`: the rank range of the suffixes that start with $P$, by a walk from the root.

Most uses do not keep the tree: they run the build loop and process each interval when it is closed, a *bottom-up traversal*.

## Representation

Let $T = T[0 \ldots n-1]$ over a general ordered alphabet, with 0-based positions and ranks. No sentinel is appended; a suffix that is a proper prefix of another sorts first, so the end of the text acts as a symbol smaller than all others. $SA$ is the suffix array and $LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]})$ for $1 \le i < n$.

**Definition.** For the definition only, set $LCP[0] = LCP[n] = -1$. A range $[i, j]$ with $0 \le i < j < n$ is an *$\ell$-interval* if

1. $LCP[i] < \ell$,
2. $LCP[k] \ge \ell$ for all $i < k \le j$, and $LCP[k] = \ell$ for at least one of them, an *$\ell$-index*,
3. $LCP[j + 1] < \ell$.

The range $[0, n-1]$ is the root and has the value 0 by convention.

**Meaning.** An $\ell$-interval $[i, j]$ with $\ell > 0$ is the range of ranks of the suffixes that start with $u = T[SA[i] \ldots SA[i] + \ell - 1]$, and $u$ is followed by at least two different symbols in $T$, where the end of the text counts as a symbol. So the lcp-intervals other than the root are the internal nodes of the suffix tree of $T\$$, other than the root. The root can have a single child interval, when all suffixes start with the same symbol; the suffix tree of $T\$$ would add a leaf $\$$ there.

**Children.** If $[i, j]$ is an $\ell$-interval with the $\ell$-indices $k_1 < \cdots < k_r$, its children are $[i, k_1 - 1], [k_1, k_2 - 1], \ldots, [k_r, j]$. Each child is a single rank (a leaf) or an lcp-interval of a larger value. The intervals are nested or disjoint, and they form a tree.

**Stored fields.** For each interval $v$: $value(v)$, $lb(v)$, $rb(v)$ and the list $kids(v)$ of its child intervals in rank order; leaves are not stored. Together with $SA$, $LCP$ and $T$ this is $\Theta(n)$ words, since there are fewer than $n$ intervals.

## Operations

```pseudo id=main
LIT-BUILD(SA, LCP, n)                    ▷ ranks 0 .. n − 1; returns the root
L1  stack ← [interval(value 0, lb 0)]
L2  for i ← 1 to n do
L3      h ← LCP[i] if i < n else 0; lb ← i − 1; last ← nil
L4      while h < value(top) do
L5          rb(top) ← i − 1; last ← pop; lb ← lb(last)
L6          if h ≤ value(top) then add last as the last child of top; last ← nil
L7      if h > value(top) then
L8          push interval(value h, lb), with last as its first child if last ≠ nil
L9  rb(root) ← n − 1
L10 return root
```

**Build.** The stack holds the open intervals, with strictly increasing values from the bottom. At rank $i$, the value $h = LCP[i]$ closes every open interval of a larger value at $rb = i - 1$ (L4, L5). A closed interval is a child of the interval below it if that one has value at least $h$ (L6); otherwise the new interval of value $h$ starts at the same $lb$ and takes it as its first child (L7, L8). The final value $h = 0$ at $i = n$ closes all but the root. Each closed interval is reported at line L5, children before parents, which gives the bottom-up traversal.

**Children.** `children(v)` lists the single ranks between the stored child intervals, in rank order. With the child table of the [enhanced suffix array](/enhanced-suffix-array/), the same list is found from $LCP$ and three small arrays, without the lists.

**Find.** Start at the root, with depth $d = 0$. At an interval of value $\ell$, compare $P[d \ldots \ell - 1]$ with the text at $SA[lb]$; then pick the child whose suffix at $SA[lb]$ has the symbol $P[\ell]$ at depth $\ell$ and go on. A leaf $[r, r]$ is compared to the end of its suffix. The answer is the rank range of the last interval or leaf reached.

## Example

The text is $T = \texttt{mississippi}$, $n = 11$, with $SA = [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]$ and $LCP = [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3]$.

| $i$ | $h$ | action | stack after (value-[lb..]) |
|---|---|---|---|
| 1 | 1 | push 1-[0..] | 0-[0..] 1-[0..] |
| 2 | 1 | none | 0-[0..] 1-[0..] |
| 3 | 4 | push 4-[2..] | 0-[0..] 1-[0..] 4-[2..] |
| 4 | 0 | close 4-[2..3], close 1-[0..3] | 0-[0..] |
| 5 | 0 | none | 0-[0..] |
| 6 | 1 | push 1-[5..] | 0-[0..] 1-[5..] |
| 7 | 0 | close 1-[5..6] | 0-[0..] |
| 8 | 2 | push 2-[7..] | 0-[0..] 2-[7..] |
| 9 | 1 | close 2-[7..8]; push 1-[7..] with it as first child | 0-[0..] 1-[7..] |
| 10 | 3 | push 3-[9..] | 0-[0..] 1-[7..] 3-[9..] |
| 11 | 0 | close 3-[9..10], close 1-[7..10] | 0-[0..] |

At $i = 9$, the value 1 is smaller than 2 and larger than 0, so the closed interval 2-[7..8] cannot go to the root: line L8 opens 1-[7..] at $lb = 7$ and gives it 2-[7..8] as its first child.

| interval | label | children |
|---|---|---|
| 0-[0..10] | the empty string | [0..3], [4], [5..6], [7..10] |
| 1-[0..3] | i | [0], [1], [2..3] |
| 4-[2..3] | issi | [2], [3] |
| 1-[5..6] | p | [5], [6] |
| 1-[7..10] | s | [7..8], [9..10] |
| 2-[7..8] | si | [7], [8] |
| 3-[9..10] | ssi | [9], [10] |

The six intervals below the root are the six internal nodes `i`, `issi`, `p`, `s`, `si` and `ssi` of the suffix tree of `mississippi$`. The deepest one, 4-[2..3], gives the [longest repeated substring](/longest-repeated-substring/) `issi`. `find("ssi")` goes from the root to [7..10] (symbol `s`), then to [9..10] (symbol `s` at depth 1), and returns the ranks 9 and 10, the suffixes at positions 5 and 2.

## Correctness

The full proof is in the proof file of this page. Its main steps:

1. **Intervals are nodes.** By the [LCP-RMQ reduction](/lcp-rmq-reduction/), $\mathrm{lcp}$ of the suffixes at ranks $a < b$ is $\min LCP[a+1 \ldots b]$. So the suffixes of an $\ell$-interval share exactly $\ell$ symbols, the suffixes just outside share fewer, and two of them differ at depth $\ell$: the label is a branching substring and the interval is the set of all its suffixes. The converse also holds.
2. **Stack invariant.** Before rank $i$, the stack holds, from the bottom, the intervals that contain both $i - 1$ and, if they continue, $i$, with their left ends, and their values strictly increase. Each pop happens exactly when $LCP[i]$ is smaller than the value, which is condition 3 for $rb = i - 1$; each push happens when $LCP[i]$ is larger than the value of the top, which starts an interval whose left end is the $lb$ of the last closed interval, or $i - 1$.
3. **Children.** A closed interval is attached to the next interval that contains it: the top if its value is at least $h$, or else the interval pushed at this step.

## Complexity

| operation | time | space |
|---|---|---|
| build or bottom-up traversal, given $SA$ and $LCP$ | $O(n)$ | $O(n)$ words for the stack and the tree |
| build from the text | $O(n)$ for an integer alphabet with a linear suffix sort and [Kasai's algorithm](/kasai-algorithm/); the implementation sorts by prefix doubling in $O(n \log^2 n)$ | $\Theta(n)$ words |
| `children(v)` | $O(\text{number of children})$ | |
| `find(P)` | $O(m \sigma)$ by scanning the children, $O(m \log \sigma)$ by binary search on them | |

Each rank pushes at most one interval and each interval is popped once, so the loop does $O(n)$ work in total. There are at most $n - 1$ intervals below the root, as in a suffix tree with $n$ leaves.

## Variants

- **Bottom-up traversal without a tree.** Kasai et al. simulate the bottom-up traversal of the suffix tree with the stack alone; this solves the [longest repeated substring](/longest-repeated-substring/), [maximal repeats](/maximal-repeats/) and many other problems in $O(n)$ time and little extra space.
- **Child table.** The [enhanced suffix array](/enhanced-suffix-array/) stores, for each rank, the `up`, `down` and `next` $\ell$-index values, which give the children of any interval in constant time per child and allow top-down search.
- **Suffix tree from the suffix array.** Adding the leaves and edge labels to the intervals gives the full suffix tree; see [suffix tree from suffix array](/suffix-tree-from-suffix-array/).
- **Cartesian tree.** The LCP interval tree is the [Cartesian tree](/cartesian-tree/) of $LCP[1 \ldots n-1]$ with each run of equal values on a path merged into one node.
- **Compressed form.** The [compressed suffix tree](/compressed-suffix-tree/) represents the same intervals with range minimum and next smaller value queries on a compressed LCP array and a balanced parentheses tree.

## When to use it

Use the LCP interval tree, or just its bottom-up traversal, whenever a suffix tree algorithm visits the internal nodes and needs only their string depths and leaf ranges: repeats, counting, statistics over all substrings, and the [generalized suffix tree](/generalized-suffix-tree/) of several strings. It needs far less memory than a pointer-based suffix tree. For algorithms that follow [suffix links](/suffix-link/) or need fast child access by symbol, add the child table and the suffix link structure of the enhanced suffix array, or use a real suffix tree.

## Pitfalls

- **No sentinel.** Without $\$$, all suffixes may start with one symbol, and the root has one child interval. The root must still be the 0-interval $[0, n-1]$, or the tree loses its top.
- **The final value.** The loop must run to $i = n$ with $h = 0$ (or $-1$) so that the last open intervals are closed.
- **The carried child.** When a closed interval has a value larger than $h$ but the interval below it has a value smaller than $h$, it belongs to the new interval pushed at this rank. Dropping it, or attaching it to the top, gives a wrong tree.
- **Equal values.** A value equal to the top's value opens nothing; it is an $\ell$-index of the open interval. Pushing a second interval with the same value splits one node into two.

## Implementations

The Python class builds $SA$ by prefix doubling and $LCP$ by Kasai's method, then the tree with the stack loop. The tests compare the intervals with the definition on all pairs of ranks, the labels with the branching substrings of the text, and `find` with a scan of the suffix array, on random strings over alphabets of size 1, 2 and 4 and on $\texttt{a}^n$ and $(\texttt{ab})^n$.

## History

In 2001, Kasai, Lee, Arimura, Arikawa and Park showed how to simulate the bottom-up traversal of a suffix tree with the suffix array and the LCP array, as an application of their LCP algorithm. Abouelhoda, Kurtz and Ohlebusch gave the lcp-intervals a name and a tree, the lcp-interval tree, in their work on the enhanced suffix array, first at WABI 2002 and in full in the Journal of Discrete Algorithms in 2004, where they added the child table and showed that every suffix tree algorithm can be replaced by one on the enhanced suffix array with the same time bound.

## References
