---
title: The range operations of the compressed suffix tree return the right nodes
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** $T\$$ has $N = n + 1$ suffixes, $\$$ is unique and smallest, and ranks and positions are 0-based. $S_r$ is the suffix of rank $r$. $LCP[r] = \mathrm{lcp}(S_{r-1}, S_r)$ for $1 \le r \le n$, and $LCP[0] = LCP[N] = -1$. Since $\$$ is unique, no suffix is a prefix of another, so every suffix ends at its own leaf of the suffix tree, and for $r \ge 1$, $LCP[r] < \min(|S_{r-1}|, |S_r|)$.

**Fact (LCP-RMQ).** For $a < c$, $\mathrm{lcp}(S_a, S_c) = \min LCP[a+1 \ldots c]$. This is the lemma of the [LCP-RMQ reduction](/lcp-rmq-reduction/).

**Lemma 1 (nodes).** For a string $u$ that labels a node of the suffix tree, the set of ranks of the suffixes that start with $u$ is a range $[lb..rb]$. If the node is internal and $u \ne \varepsilon$, then $\ell = |u|$ satisfies $LCP[r] \ge \ell$ for $lb < r \le rb$, $LCP[r] = \ell$ for some such $r$, and $LCP[lb] < \ell$, $LCP[rb+1] < \ell$. Conversely, every range with these properties, for some $\ell \ge 1$, is the range of a node of depth $\ell$. The root is $[0..n]$, and a leaf is $[r..r]$.

*Proof.* The suffixes that start with $u$ are consecutive in sorted order. By the fact, $\min LCP[lb+1 \ldots rb] = \mathrm{lcp}(S_{lb}, S_{rb})$, which is at least $\ell$; it is exactly $\ell$ because $u$ is followed by at least two different symbols, and the smallest and the largest suffix in the range have the smallest and the largest of them. $S_{lb-1}$ and $S_{rb+1}$ do not start with $u$, so their lcp with the range is less than $\ell$. Conversely, the suffixes of such a range share their first $\ell$ symbols $u$, two of them differ at depth $\ell$, and the neighbors outside do not start with $u$; so $u$ is a node and the range is exactly its set. $\square$

**Lemma 2 (enclosing node).** Let $1 \le k \le n$ and $h = LCP[k] \ge 0$. The range $[\mathrm{PSV}(k)..\mathrm{NSV}(k) - 1]$ is the node of depth $h$ that contains the ranks $k - 1$ and $k$. Here $\mathrm{PSV}(k) \ge 0$ and $\mathrm{NSV}(k) \le N$ exist because $LCP[0] = LCP[N] = -1$.

*Proof.* Let $a = \mathrm{PSV}(k)$ and $c = \mathrm{NSV}(k)$. All values in $LCP[a+1 \ldots c-1]$ are at least $h$, the value $LCP[k] = h$ is among them, and $LCP[a] < h$, $LCP[c] < h$. If $h \ge 1$, Lemma 1 gives a node of depth $h$ with the range $[a..c-1]$, which contains $k - 1 \ge a$ and $k \le c - 1$. If $h = 0$, all values between are at least 0, which holds for all $1 \le r \le n$, so $a = 0$ and $c = N$, and the range is the root. $\square$

**Theorem 1 (depth).** CST-DEPTH returns the string depth.

*Proof.* A leaf $[r..r]$ has the label $S_r$, of length $N - SA[r]$. An internal node has depth $\min LCP[lb+1 \ldots rb]$ by Lemma 1, and RMQ returns a position of that minimum. $\square$

**Theorem 2 (parent).** For a node $v = [lb..rb]$ other than the root, CST-PARENT returns its parent.

*Proof.* Let $h = \max(LCP[lb], LCP[rb+1])$. Since $v$ is not the root, $lb \ge 1$ or $rb \le n - 1$, so $h \ge 0$. Let $k$ be the border with the value $h$. By Lemma 2, $p = [\mathrm{PSV}(k)..\mathrm{NSV}(k) - 1]$ is the node of depth $h$ that contains $k - 1$ and $k$, so it contains a rank of $v$ and a rank outside $v$; as nodes are nested or disjoint, $p$ strictly contains $v$. Every node that strictly contains $v$ is a larger range, so it contains $lb$ and $lb - 1$, or $rb$ and $rb + 1$. In the first case its depth is at most $\mathrm{lcp}(S_{lb-1}, S_{lb}) = LCP[lb] \le h$, and in the second at most $LCP[rb+1] \le h$. The nodes that contain $v$ form a chain, so $p$, which has the largest possible depth $h$, is the deepest of them: the parent. $\square$

**Theorem 3 (children).** For an internal node $v = [lb..rb]$ of depth $\ell$, with $\ell$-indices $k_1 < \cdots < k_t$, CST-FIRST-CHILD returns $[lb..k_1 - 1]$, and CST-NEXT-SIBLING maps $[k_i..k_{i+1} - 1]$ to the next child and returns nil for the last child $[k_t..rb]$.

*Proof.* The children of an lcp-interval are the ranges between its $\ell$-indices, as on the [LCP interval tree](/lcp-interval-tree/) page. The minimum of $LCP[lb+1 \ldots rb]$ is $\ell$, and the leftmost position with it is $k_1$, which gives L5. For a child $w = [x..y]$, the parent of $w$ has the depth $\max(LCP[x], LCP[y+1])$ by Theorem 2. If $w$ is not the last child, then $y + 1$ is an $\ell$-index, so $LCP[y+1] = \ell \ge LCP[x]$, and the test of L6 fails. The next child starts at $y + 1$ and ends just before the next $\ell$-index or at $rb$, that is, just before the first $r > y + 1$ with $LCP[r] \le \ell$, because inside $v$ all values are at least $\ell$ and $LCP[rb+1] < \ell$. If $w$ is the last child, then $w = [k_t..rb]$, since an internal node has at least two children, so $LCP[x] = \ell > LCP[rb+1]$ and L6 returns nil. For the root, L6 returns nil at once. $\square$

**Theorem 4 (LCA).** For nodes $u$ and $v$ with $rb(u) < lb(v)$, CST-LCA returns their lowest common ancestor.

*Proof.* Let $k$ be the leftmost minimum of $LCP[rb(u)+1 \ldots lb(v)]$ and $h = LCP[k]$. The values inside $u$ are at least the depth of $u$, which is larger than $LCP[rb(u)+1] \ge h$ when $u$ is internal, and the same holds for $v$; so $h = \min LCP[lb(u)+1 \ldots rb(v)]$, the lcp of every suffix of $u$ with every suffix of $v$ that are the farthest apart. By Lemma 2, $[\mathrm{PSV}(k)..\mathrm{NSV}(k) - 1]$ is the node of depth $h$ around $k$; it contains $[lb(u)..rb(v)]$ because no value in that range is below $h$. A common ancestor contains $rb(u)$ and $lb(v)$, so its depth is at most $\mathrm{lcp}(S_{rb(u)}, S_{lb(v)}) = h$. So this node is the deepest common ancestor. $\square$

**Theorem 5 (suffix link).** For an internal node $v = [lb..rb]$ with label $cu$, CST-SUFFIX-LINK returns the node of $u$.

*Proof.* $S_{lb}$ and $S_{rb}$ start with $cu$, and they differ at depth $|cu|$ (Lemma 1 with the fact). $\Psi$ maps them to the suffixes one position later, which start with $u$ and differ at depth $|u|$. So the LCA of the leaves $\Psi(lb)$ and $\Psi(rb)$ has depth $|u|$ by Theorem 4 and its proof, and its label is $u$. Since $\Psi$ keeps the order of suffixes with the same first symbol, $\Psi(lb) < \Psi(rb)$ and the leaves are disjoint, so Theorem 4 applies. A leaf $S_r = c\,S'$ with $c \ne \$$ links to the leaf of $S'$, which has the rank $\Psi(r)$; the leaf $\$$ links to the root, whose label is empty. $\square$

**Lemma 3 (H).** $PLCP[p+1] \ge PLCP[p] - 1$ for $0 \le p < n$. Hence the numbers $PLCP[p] + 2p$ strictly increase with $p$, and the one of $H$ with index $p$, counting from 0, is at $PLCP[p] + 2p$.

*Proof.* If $PLCP[p] = h \ge 1$, the suffix at $p$ has a previous suffix $q$ in sorted order that shares $h$ symbols. Then the suffix at $q + 1$ is smaller than the suffix at $p + 1$ and shares $h - 1$ symbols with it, and by the fact every suffix between them in sorted order, in particular the previous suffix of $p + 1$, shares at least $h - 1$ symbols. So $PLCP[p+1] \ge h - 1$, which also holds when $h = 0$. Then $PLCP[p+1] + 2(p+1) \ge PLCP[p] + 2p + 1$. $\square$

**Letter and find.** By Lemma 1, all suffixes of $v$ share the label of $v$, so the symbol at depth $d$ is $T\$[SA[lb] + d]$, the first symbol of the suffix of rank $SA^{-1}[SA[lb] + d]$. Find walks the tree as in a suffix tree: at each node it picks the unique child whose edge starts with the next symbol, and compares the edge with the pattern.

**Time and termination.** Every scan in a block, every walk in the tree of minima, every select and every chain of $\Psi$ steps is bounded: by $b$, by $2 \log_2$ of the number of blocks, by the distance between two sampled ones of $H$, and by $s$. PSV and NSV always find an answer for $h \ge 0$, because of the border values $-1$. So each operation ends, in the times given on the page. $\blacksquare$
