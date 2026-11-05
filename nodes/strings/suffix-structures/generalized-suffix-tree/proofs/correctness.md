---
title: The stack build gives the generalized suffix tree
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** The strings are $S_0, \ldots, S_{m-1}$, and $Z = S_0 \$_0 S_1 \$_1 \cdots S_{m-1} \$_{m-1}$ has length $N$. The separators are distinct, each occurs once in $Z$, and $\$_0 < \cdots < \$_{m-1}$ are smaller than all letters. Positions are 0-based. For a position $p$ that holds a letter, let $e(p)$ be the position of the first separator at or after $p$, and let $X_p = Z[p \ldots e(p)]$, the suffix of its string followed by its separator. The *generalized suffix tree* is the compacted trie of the set $\mathcal{X} = \{X_p\}$: a rooted tree whose edges are labeled with nonempty strings, where the labels of the edges out of a node start with different symbols, each internal node other than the root has at least two children, and the leaves are exactly the strings of $\mathcal{X}$.

**Lemma 1 (terminated suffixes).** Let $p \ne q$ be letter positions. Then $\mathrm{lcp}(Z_p, Z_q) < \min(|X_p|, |X_q|)$, and $Z_p < Z_q$ if and only if $X_p < X_q$. In particular, no string of $\mathcal{X}$ is a prefix of another.

*Proof.* Let $h = \mathrm{lcp}(Z_p, Z_q)$ and suppose $h \ge |X_p|$. Then $Z[p + |X_p| - 1] = Z[q + |X_p| - 1]$, and the left side is the separator at $e(p)$. A separator occurs once in $Z$, so $p = q$, a contradiction. The same holds for $q$. So the first difference of $Z_p$ and $Z_q$ is at an offset $h$ inside both $X_p$ and $X_q$, with the same two symbols, and the orders agree. If $X_p$ were a prefix of $X_q$, then $\mathrm{lcp}(Z_p, Z_q) \ge |X_p|$. $\square$

**Lemma 2 (ranks).** The ranks $0, \ldots, m-1$ of the suffix array of $Z$ hold the $m$ suffixes that start with a separator, and the ranks $m, \ldots, N-1$ hold the letter positions. For $i \ge m + 1$, $LCP[i] = \mathrm{lcp}(X_{SA[i-1]}, X_{SA[i]})$, and $LCP[m] = 0$.

*Proof.* A suffix that starts with a separator is smaller than each suffix that starts with a letter, because the separators are smaller than all letters. For $i \ge m + 1$ both suffixes start at letter positions, and Lemma 1 shows that their common prefix lies inside both terminated suffixes. The suffix of rank $m - 1$ starts with a separator and that of rank $m$ with a letter, so $LCP[m] = 0$. $\square$

So the letter positions in the order $SA[m], \ldots, SA[N-1]$ list $\mathcal{X}$ in increasing order, with the LCP of each adjacent pair. Write $x_t = X_{SA[m + t]}$ and $h_t = LCP[m + t]$ for $0 \le t < N - m$.

**Invariant.** After the loop of lines L3 to L10 has handled $x_0, \ldots, x_t$:

> **(G)** The tree is the compacted trie $C_t$ of $\{x_0, \ldots, x_t\}$, with the leaf of $x_s$ labeled by its string and offset. The stack holds, from bottom to top, the nodes of the path from the root to the leaf of $x_t$, in order of increasing string depth.

*Initialization.* Before the loop, the tree is the root alone and the stack is [root]. For $t = 0$, $h_0 = 0$: line L5 pops nothing, since the root has depth 0, line L6 fails, and lines L9 and L10 hang the leaf of $x_0$ below the root with the edge label $x_0$. This is $C_0$, and the stack is the path to the leaf.

*Maintenance.* Assume (G) for $t - 1$ and handle $x_t$ with $h = h_t$. Because the list is sorted, $x_t$ branches off the path to $x_{t-1}$ at string depth $h$: the common prefix of $x_t$ with each earlier $x_s$ has length at most $h$, by the sandwich property of sorted strings, $\mathrm{lcp}(x_s, x_t) = \min(h_{s+1}, \ldots, h_t) \le h$. So in $C_t$ the leaf of $x_t$ hangs from the point at depth $h$ on the path to $x_{t-1}$, and no other part of $C_{t-1}$ changes. By Lemma 1, $h < |x_{t-1}|$, the depth of the leaf on top of the stack. Line L5 pops the nodes of depth more than $h$; at least the leaf is popped, so $last$ is defined, and $last$ is the shallowest popped node, a child of the new top. If the new top has depth $h$, that node is the branch point. Otherwise its depth is less than $h$ and the point at depth $h$ lies inside the edge from the top to $last$; lines L7 and L8 split this edge with a new node $v$ of depth $h$. The key of $last$ below $v$ is the symbol at depth $h$ of its path label, and the key of $v$ below the top is the same as the old key of $last$, so the edge to $last$ is replaced. Lines L9 and L10 hang the leaf of $x_t$ below the branch point, with the key $x_t[h]$. This key differs from the key of the child on the path to $x_{t-1}$, because $h$ is the exact LCP. Each new internal node has two children, and the stack is the path to the new leaf. So (G) holds for $t$.

*Termination and result.* The loop runs $N - m$ times and each pop removes a node pushed earlier, so it ends. By (G) the result is the compacted trie of $\mathcal{X}$, which is the generalized suffix tree. Each suffix of each $S_k$ that is nonempty is one leaf. $\square$

**Lemma 3 (search).** For a nonempty pattern $P$ over the letters, the occurrences of $P$ in the strings are the labels of the leaves below the highest node whose path label starts with $P$.

*Proof.* $P$ occurs at offset $j$ of $S_k$ if and only if $P$ is a prefix of $X_p$ with $p$ the position of $S_k[j]$, because $P$ has no separator. The strings of $\mathcal{X}$ with prefix $P$ are the leaves below the locus of $P$ in the compacted trie. $\square$

**Theorem (time).** Given the suffix array and the LCP array of $Z$, lines L2 to L10 run in $O(N)$ time.

*Proof.* Each iteration pushes at most two nodes, so there are at most $2(N - m)$ pushes and so at most as many pops in total. The other lines take $O(1)$ time each, with the children of a node in a hash map keyed by a symbol, and the string of each position is found in $O(1)$ time from a table of the string of each position, or in $O(\log m)$ time by a binary search on the start positions. With a linear-time suffix array construction for an integer alphabet and Kasai's algorithm for the LCP array, the whole build is $O(N)$. $\blacksquare$
