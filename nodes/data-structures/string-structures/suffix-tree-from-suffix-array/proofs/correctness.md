---
title: The stack scan builds the suffix tree from the suffix array and the LCP array
proves: [correctness, complexity]
status: full
---

We use the pseudocode and notation of the page. The text $t$ has length $n$ and ends with a unique end marker, so no suffix is a prefix of another. Write $S_k$ for the suffix $t[SA[k] \ldots]$, so $S_0 < S_1 < \cdots < S_{n-1}$, and $lcp(x, y)$ for the length of the longest common prefix.

**Fact 1.** For $k < i$, $lcp(S_k, S_i) = \min(LCP[k+1], \ldots, LCP[i]) \le LCP[i]$. This is the standard property of sorted strings: the common prefix of $S_k$ and $S_i$ is a prefix of every string between them, and conversely the minimum over adjacent pairs is common to all of them.

Let $\mathcal{T}_i$ be the compacted trie of $S_0, \ldots, S_{i-1}$: the tree whose nodes are the root, one leaf for each of these suffixes, and one internal node for each string $w$ that is the longest common prefix of two of them and is followed in them by two different symbols, with the children of each node in increasing order of their next symbol. (Here every leaf is a suffix, since none is a prefix of another.) $\mathcal{T}_n$ is the suffix tree of $t$.

**Invariant.** Before iteration $i$ (for $i \ge 1$), the tree built is $\mathcal{T}_i$, each node has the right depth, a correct start and its children in order, and the stack holds, from bottom to top, the nodes of the path from the root to the leaf of $S_{i-1}$. For $i = 0$ the tree is the root alone and the stack is $[root]$.

*Iteration $i$.* Let $h = LCP[i]$ (for $i = 0$, $h = 0$, and the leaf of $S_0$ becomes the only child of the root, which gives $\mathcal{T}_1$ with the stack $[root, leaf]$). For $i \ge 1$, $\mathcal{T}_{i+1}$ differs from $\mathcal{T}_i$ as follows. Let $P$ be the point at depth $h$ on the path from the root to the leaf of $S_{i-1}$; it exists because $\lvert S_{i-1} \rvert > h$. By Fact 1, the prefix of length $h$ of $S_i$ is the string at $P$, and no earlier suffix shares more than $h$ symbols with $S_i$. So in $\mathcal{T}_{i+1}$, $S_i$ leaves the old tree at $P$: if $P$ is a node, the leaf of $S_i$ becomes a new child of it; if $P$ lies inside an edge, the edge is split by a new internal node at $P$, whose children are the lower part of the edge and the new leaf. In both cases the next symbol of $S_i$ after $P$ is larger than that of $S_{i-1}$, since $S_{i-1} < S_i$, and larger than the next symbol of every earlier suffix through $P$, since these suffixes are at most $S_{i-1}$ and share the string at $P$; so the new leaf is the last child of the node at $P$.

Line L3 pops exactly the nodes of the path with depth greater than $h$. If the new top has depth $h$, it is the node at $P$, and line L5 appends the leaf as its last child. Otherwise $P$ lies on the edge from the top, of depth below $h$, to $last$, the first popped node below it on the path, which is the last child of the top since the path is the rightmost one. Line L4 creates the node at $P$ with depth $h$, puts it in place of $last$, and makes $last$ its only child for now; its start is that of $last$, which is a suffix below $P$, so the labels of the two new edges are the two parts of the old label. Then line L5 appends the leaf. The depth of the leaf is $\lvert S_i \rvert = n - SA[i]$, and its start is $SA[i]$. The children stay in order, and the stack now holds the path from the root to the new leaf: the nodes below $P$ that were not popped, the node at $P$, and the leaf. So the invariant holds for $i + 1$.

After the last iteration, the tree is $\mathcal{T}_n$, the suffix tree of $t$. Every internal node other than the root has at least two children: it was created at line L4 with $last$ as a child, and the leaf of line L5 was appended right away.

**Time.** Each iteration pushes at most two nodes (lines L4 and L5), so at most $2n$ pushes happen in total, and each iteration of the loop in line L3 pops one of them. All other work is constant per iteration. So the scan takes $O(n)$ time, and it creates $n$ leaves and at most $n - 1$ internal nodes. $\blacksquare$
