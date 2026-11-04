---
title: The position heap keeps its invariant, and SEARCH reports exactly the occurrences of the pattern
proves: [correctness, complexity]
status: full
---

We use the pseudocode, the notation and the invariant (H1) to (H3) of the page. Write $T_i = T[i \ldots n - 1]$ for the suffix at $i$, and $x_i$ for the node with $pos(x_i) = i$.

**Lemma 1 (PREPEND).** If the heap of $T$ satisfies (H1) to (H3), then after PREPEND(c) the heap satisfies them for $T' = c \cdot T$.

*Proof.* Each old node keeps its string and its suffix, which now starts at a position one larger; so (H2) still holds for the old nodes, and the old positions become $1, \ldots, n$. The walk of line L2 follows the symbols of $T'_0 = T'$ while the nodes exist. It stops at some depth $k < n + 1$: if it reached depth $n + 1$, the node of $T'$ itself would exist, and its holder $x$ would satisfy $\lvert str(x) \rvert = n + 1 > \lvert T'_{pos(x)} \rvert$, against (H2). So $T'[k]$ exists, and line L3 adds the node $y$ with $str(y) = T'[0 \ldots k]$, a prefix of $T'_0$, and $pos(y) = 0$. This gives (H1) and (H2) for $T'$. The new node is a leaf, and its parent is the root or an old node with position at least 1, so (H3) holds. $\square$

By induction, the heap built by $n$ calls of PREPEND satisfies (H1) to (H3). The trie has distinct symbols at the children of each node, so the walk along a string is unique, and for each string $s$ there is at most one node $x$ with $str(x) = s$; if such a node exists, so does the node of every prefix of $s$, its ancestor.

**Lemma 2 (where an occurrence is).** Let $P$ occur at $i$. Then either $str(x_i)$ is a proper prefix of $P$, or $P$ is a prefix of $str(x_i)$.

*Proof.* By (H2) $str(x_i)$ is a prefix of $T_i$, and $P$ is a prefix of $T_i$ since it occurs at $i$. Two prefixes of the same string are comparable under the prefix order. $\square$

**SEARCH is correct.** Let $u_0 = $ root, $u_1, \ldots, u_k$ be the nodes of the walk of line L4, with $str(u_j) = P[0 \ldots j - 1]$; the walk stops at $k = m$ or at a node with no child by $P[k]$.

*Every reported position is an occurrence.* Line L5 reports a position only after checking it. Line L6 runs only if $k = m$; then $str(u_m) = P$, and every node $y$ of the subtree of $u_m$ has $P$ as a prefix of $str(y)$, which is a prefix of $T_{pos(y)}$ by (H2), so $P$ occurs at $pos(y)$.

*Every occurrence is reported.* Let $P$ occur at $i$. By Lemma 2 there are two cases. If $str(x_i)$ is a proper prefix of $P$, of length $j < m$, then the node of $P[0 \ldots j - 1]$ is $x_i$, and since its ancestors exist the walk reaches it: $x_i = u_j$ with $j \le k$ and $j < m$. Line L5 checks $i$ and reports it. If $P$ is a prefix of $str(x_i)$, then the node of $P$ exists, as an ancestor of $x_i$ or $x_i$ itself, so the walk reaches depth $k = m$, $u_m$ is the node of $P$, and $x_i$ is in its subtree; line L6 reports $i$.

*No position is reported twice.* The nodes checked at line L5 have depth less than $m$ and the nodes of line L6 have depth at least $m$, and each node holds one position by (H1).

**Complexity.** The walk takes at most $m$ steps. Line L5 makes at most $m - 1$ checks of at most $m$ symbols each. Line L6 visits the subtree of $u_m$, and each of its nodes is an occurrence, so with $z$ occurrences it takes $O(z + 1)$ time. The total is $O(m^2 + z)$. By (H1) the heap has $n + 1$ nodes, so it takes $O(n)$ words. $\blacksquare$
