---
title: The Bender-Farach-Colton RMQ returns the leftmost minimum in O(1) after O(n) preprocessing
proves: [correctness, complexity]
status: full
---

Let $A[0 \ldots n-1]$ with $n \ge 1$, and let $C$ be its Cartesian tree with leftmost minima: the root of the tree of a range $[a, b]$ is the least position $p \in [a, b]$ with $A[p] = \min A[a \ldots b]$, its left subtree is the tree of $[a, p - 1]$ and its right subtree the tree of $[p + 1, b]$. The subtree of each node $v$ is a range $[a_v, b_v]$ of positions with $v \in [a_v, b_v]$.

**Lemma 1 (stack build).** Line L1 builds $C$.

*Proof.* After step $i$ the stack holds the right spine of the Cartesian tree of $A[0 \ldots i]$, from the root down, with values non-decreasing and, for equal values, earlier positions higher. When $i$ arrives, the popped nodes are those with values greater than $A[i]$; they form the bottom of the spine, and they belong in the left subtree of $i$, since $i$ is the leftmost minimum of the range they and their left subtrees cover, together with $i$. The node left on top, if any, has a value at most $A[i]$, and it is earlier, so it is the parent of $i$ with $i$ as its right child. This gives the Cartesian tree of $A[0 \ldots i]$. Each position is pushed and popped at most once, so the build takes $O(n)$ time. $\square$

**Lemma 2 (RMQ to LCA).** For $l \le r$, the lowest common ancestor $w$ of $l$ and $r$ in $C$ is the leftmost minimum of $A[l \ldots r]$.

*Proof.* The nodes $l$ and $r$ are in the subtree of $w$, so $[l, r] \subseteq [a_w, b_w]$. If $w < l$, both $l$ and $r$ are in the right subtree of $w$, and if $w > r$ both are in the left subtree; either way a child of $w$ would be a common ancestor, which contradicts the choice of $w$. So $w \in [l, r]$. As $w$ is the leftmost minimum of $[a_w, b_w] \supseteq [l, r]$, it is a minimum of $A[l \ldots r]$, and no position of $[l, w)$ has an equal value, since such a position would be a minimum of $[a_w, b_w]$ further left. $\square$

**Lemma 3 (LCA to ±1 RMQ).** Let $E, D, F$ be the tour, the depths and the first indices of line L2, and let $x = \min(F[u], F[v])$ and $y = \max(F[u], F[v])$. Then $|D[k+1] - D[k]| = 1$ for all $k$, and the lowest common ancestor $w$ of $u$ and $v$ is the only node of least depth among $E[x \ldots y]$.

*Proof.* Consecutive tour entries are a parent and a child, so their depths differ by one. The walk enters the subtree of $w$ at $F[w] \le x$ and leaves it after all of its entries, so $E[x \ldots y]$ lies in the subtree of $w$, and every node there has depth at least $\mathrm{depth}(w)$. If $u = w$ or $v = w$, then $E[x] = w$. Otherwise $u$ and $v$ are in different child subtrees of $w$, and the walk returns to $w$ between finishing the first one and entering the second, so $w$ occurs in $E[x \ldots y]$. Every other node of the subtree is deeper. $\square$

**Lemma 4 (normalized blocks).** If two blocks $D[s \ldots s + t - 1]$ and $D[s' \ldots s' + t - 1]$ have the same length and the same signature, then $D[s + i] - D[s] = D[s' + i] - D[s']$ for all $i < t$, so for all $i \le k < t$ the leftmost minimum of the offsets $i \ldots k$ is the same in both. There are at most $2^{b-1}$ signatures of full blocks.

*Proof.* $D[s + i] - D[s]$ is the sum of the first $i$ steps, which the signature fixes. Adding a constant to all items does not change where the leftmost minimum is. A full block has $b - 1$ steps, each one bit. $\square$

**Theorem 1 (correctness).** QUERY$(l, r)$ returns the leftmost minimum of $A[l \ldots r]$.

*Proof.* By Lemmas 2 and 3 it is enough that $k$ is a position of least depth in $D[x \ldots y]$, because then $E[k] = w$. If $x$ and $y$ are in one block, line L9 reads the table of its signature, which by Lemma 4 holds the minimum of the offsets $x - jb \ldots y - jb$ of the block. Otherwise $[x, y]$ is the disjoint union of the end of block $bx$, the whole blocks $bx + 1, \ldots, by - 1$ and the start of block $by$. The two ends come from the tables, and the middle from the sparse table, whose two overlapping ranges have the minimum of all the middle blocks because the minimum is idempotent. The least of the candidates is a minimum of $D[x \ldots y]$. $\square$

**Theorem 2 (cost).** Preprocessing takes $O(n)$ time and words, and a query takes $O(1)$ time on the word RAM.

*Proof.* Lines L1 and L2 take $O(n)$ by Lemma 1 and because the tour has $m = 2n - 1$ entries. Line L4 reads each depth once. With $b = \max(1, \lfloor \frac12 \lg m \rfloor)$, the number of blocks is $B = \lceil m / b \rceil = O(m / \log m)$ for $m \ge 4$, so the sparse table of line L5 has $O(B \log B) = O(m)$ entries and takes as long to build. By Lemma 4 at most $2^{b-1} + 1 \le \sqrt m + 1$ tables are built at line L6, each of $b^2 = O(\log^2 m)$ entries in $O(b^2)$ time, which is $O(\sqrt m \log^2 m) = O(m)$. A query does a constant number of array reads, one division, one bit length of a word, and at most three comparisons. $\square$
