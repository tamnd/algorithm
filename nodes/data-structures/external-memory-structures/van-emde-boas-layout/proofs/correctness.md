---
title: The van Emde Boas layout is a bijection with contiguous subtrees, and the search finds the predecessor
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A tree with $h \ge 1$ levels has the nodes $(d, p)$ with $0 \le d < h$ and $0 \le p < 2^d$; let $S(h) = 2^h - 1$ be their number. For $d \ge t$, the *first $t$ bits* of a $d$-bit path $p$ are $\lfloor p / 2^{d-t} \rfloor$ and the *last $d - t$ bits* are $p \bmod 2^{d-t}$.

**Lemma 1 (V1 and V2).** For every $h \ge 1$, the map $(d, p) \mapsto \mathrm{POS}(h, d, p)$ is a bijection from the nodes of the tree with $h$ levels onto $\{0, \ldots, S(h) - 1\}$. Moreover, in the recursion of POS, the nodes of the top tree map onto $\{0, \ldots, S(h_t) - 1\}$ and the nodes of bottom tree $j$ onto the range $\{S(h_t) + j S(h_b), \ldots, S(h_t) + (j+1) S(h_b) - 1\}$, so each recursive subtree occupies a contiguous range.

*Proof.* By induction on $h$. For $h = 1$ there is one node, and line L1 maps it to 0. Let $h \ge 2$, $h_t = \lfloor h/2 \rfloor \ge 1$ and $h_b = h - h_t \ge 1$; both are less than $h$. The nodes with $d < h_t$ form a tree with $h_t$ levels, whose node $(d, p)$ is the same pair, and line L3 maps them by $\mathrm{POS}(h_t, \cdot, \cdot)$, a bijection onto $\{0, \ldots, S(h_t) - 1\}$ by induction. The nodes with $d \ge h_t$ split by their first $h_t$ bits $j \in \{0, \ldots, 2^{h_t} - 1\}$ into $2^{h_t}$ trees; in tree $j$, the node $(d, p)$ corresponds to the node $(d - h_t, p \bmod 2^{d - h_t})$ of a tree with $h_b$ levels, and this correspondence is a bijection. Line L5 maps it to $S(h_t) + j S(h_b) + \mathrm{POS}(h_b, d - h_t, p \bmod 2^{d-h_t})$, which by induction runs over the range stated, bijectively. The ranges for $j = 0, \ldots, 2^{h_t} - 1$ are disjoint, follow each other, and follow the range of the top tree. Their union is $\{0, \ldots, S(h_t) + 2^{h_t} S(h_b) - 1\}$, and $S(h_t) + 2^{h_t}(2^{h_b} - 1) = 2^{h_t} - 1 + 2^h - 2^{h_t} = S(h)$. So POS is a bijection onto $\{0, \ldots, S(h) - 1\}$. The parts are contiguous at this level, and by induction inside each part. $\square$

POS ends: each call is on a tree with fewer levels.

**Lemma 2 (V3).** After BUILD, the node $(d, p)$ holds the key of in-order rank $r(d, p) = p \cdot 2^{h-d} + 2^{h-d-1} - 1$ in the padded list, and the tree is a binary search tree with these keys.

*Proof.* In a complete binary tree with $h$ levels, the subtree of $(d, p)$ has $2^{h-d} - 1$ nodes, and the subtrees of the $p$ nodes to its left at depth $d$, together with the ancestors between them, account for the first $p \cdot 2^{h-d}$ ranks; the left subtree of $(d, p)$ has $2^{h-d-1} - 1$ nodes. So its in-order rank is $r(d, p)$. Line L7 writes, by Lemma 1 at a distinct cell for each node, the padded key of that rank. Since the padded list is increasing, with $+\infty$ at the end, all keys in the left subtree of a node have smaller ranks, so they are smaller, and all keys in the right subtree are larger, with the convention that $+\infty$ is larger than every key and the cells of $+\infty$ are compared as $+\infty$. $\square$

**Lemma 3.** PREDECESSOR$(k)$ returns the largest key at most $k$, or none if there is none.

*Proof.* Let $P$ be the set of real keys at most $k$, and $\pi$ its largest element if $P$ is not empty. We keep the invariant: at the start of each pass of line L9, either $\pi$ is $best$, or $\pi$ is in the subtree of the current node $(d, p)$, or $P$ is empty and $best$ is none; and $best$ is none or a key at most $k$.

At the start, the current node is the root, whose subtree holds all keys, and $best$ is none.

Let $x$ be the key at the current node, read in line L10 at its position, which is right by Lemmas 1 and 2. If $x = k$, then $\pi = k$, and line L11 returns it. If $x < k$, then $x \in P$, all keys in the left subtree are smaller than $x$, so $\pi$ is $x$ or in the right subtree. Line L12 sets $best \leftarrow x$ and moves to the right child; if $\pi$ is in the right subtree the invariant holds by the second case, and otherwise $\pi = x = best$. If $x > k$ (including $x = +\infty$), every key in the right subtree is larger than $x$, so larger than $k$; so if $\pi$ was in the subtree of the current node, it is in the left subtree, and line L12 moves there. In all cases the invariant holds.

The loop ends after at most $h$ passes, since $d$ grows by one each time (line L13). When $d = h$, the current subtree is empty, so either $\pi = best$ or $P$ is empty and $best$ is none, and line L14 returns the right answer. And $best$ only ever takes values $x < k$ that are keys, by line L12. $\square$

By Lemma 3, `contains(k)` is right, since $k$ is in the set exactly when its predecessor is $k$. The I/O bound of a search follows from Lemma 1 (each recursive subtree is contiguous) by the argument on the [cache-oblivious model](/cache-oblivious-model/) page. $\blacksquare$
