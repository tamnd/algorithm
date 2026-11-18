---
title: FlatFAT keeps every node equal to the aggregate of its leaves, and its operations meet the stated bounds
proves: [correctness, time.worst, time.amortized, space.extra]
status: full
---

We use the line numbers of the pseudocode. The operator $\oplus$ is associative and has the identity $e$; it need not be commutative or invertible. The tree has $n = 2^L$ leaves for an integer $L \ge 0$, stored in the array $T[1..2n-1]$: the root is $T[1]$, the children of node $h$ are $2h$ and $2h + 1$, and leaf $i$ (for $0 \le i < n$) is $T[n + i]$. All leaves are at depth $L$. For a node $h$, let $\mathrm{lo}(h)$ and $\mathrm{hi}(h)$ be the positions of the leftmost and the rightmost leaf below $h$, so the leaves below $h$ are the contiguous block $a_{\mathrm{lo}(h)}, \dots, a_{\mathrm{hi}(h)}$, where $a_i$ is the value of leaf $i$. For $p \le q$ we write $a[p..q] = a_p \oplus a_{p+1} \oplus \cdots \oplus a_q$; by associativity the bracketing does not matter, but the order does.

**Invariant (I).** For every internal node $h$, $T[h] = a[\mathrm{lo}(h)..\mathrm{hi}(h)]$.

**Lemma 1 (new).** After lines L1 to L3, (I) holds, and the build makes exactly $n - 1$ calls of $\oplus$.

*Proof.* Line L2 visits the internal nodes in the order $n - 1, n - 2, \dots, 1$. The children $2h$ and $2h + 1$ of $h$ are larger than $h$, so they are leaves or nodes that were already set. By induction on this order, $T[2h] = a[\mathrm{lo}(h)..m]$ and $T[2h+1] = a[m+1..\mathrm{hi}(h)]$ with $m = \mathrm{hi}(2h)$, because the left block ends just before the right block starts. Line L3 sets $T[h]$ to their combination, which is $a[\mathrm{lo}(h)..\mathrm{hi}(h)]$ by associativity. There are $n - 1$ internal nodes and one call each. $\square$

**Lemma 2 (update).** Suppose (I) holds and an update writes $m \ge 1$ distinct leaves (lines L4 to L7). Then (I) holds after it, and the number of calls of $\oplus$ is at most $m r + m - 1 \le m(1 + r)$, where $r = \lceil \log_2(n / m) \rceil$.

*Proof.* Let $A$ be the set of the changed leaves. A node needs repair exactly when it is an ancestor of a leaf in $A$; every other node has the same leaves below it as before, so (I) still holds for it. We show by induction on the iterations of line L5 that the $k$-th iteration handles the set $D_k$ of all ancestors of $A$ at depth $L - k$, and that when it handles a node, both children are already correct. Line L4 puts into $D_1$ the parents of the changed leaves, which are all at depth $L - 1$, because all leaves are at depth $L$. The children of a node in $D_1$ are leaves, which hold their new values. Line L7 maps $D_k$ to the set of the parents of its nodes, which is $D_{k+1}$. A child of a node in $D_{k+1}$ is either in $D_k$, and so was repaired in iteration $k$, or not an ancestor of $A$, and so was already correct. Line L6 then sets each node of $D_{k+1}$ from its two correct children, as in Lemma 1. The loop stops after $D_L = \{1\}$, so every ancestor is repaired once.

For the cost, iteration $k$ makes $|D_k| \le \min(m, 2^{L-k})$ calls, because each changed leaf has one ancestor at each depth and depth $L - k$ has $2^{L-k}$ nodes. Let $c = \lceil \log_2 m \rceil$. The depths with $2^{L-k} \ge m$ are those with $L - k \ge c$; there are $L - c$ of them, and they give at most $m(L - c)$ calls. The other depths give at most $2^{c-1} + \cdots + 2 + 1 = 2^c - 1$ calls. If $m$ is a power of two, then $2^c = m$ and $L - c = r$, so the total is at most $m r + m - 1$. Otherwise $L - c = r - 1$ and $2^c < 2m$, so the total is less than $m(r - 1) + 2m - 1 = m r + m - 1$. $\square$

For $m = 1$ the bound is $L = \log_2 n$ calls. The bound is exact when $m$ is a power of two and the changed leaves are $0, n/m, 2n/m, \dots$, because then each depth below $c$ has $m$ distinct ancestors and the depths above it are full.

**Lemma 3 (prefix and suffix).** If (I) holds, PREFIX($i$) returns $a[0..i]$ and SUFFIX($j$) returns $a[j..n-1]$, each with at most $L$ calls of $\oplus$.

*Proof.* For PREFIX, we claim that at the test of line L10, $a$ holds $a[\mathrm{lo}(h)..i]$. At line L9, $h$ is the leaf $i$ and $a = a_i$. If $h$ is odd, it is a right child, its sibling $h - 1$ covers the block that ends just before $\mathrm{lo}(h)$, and $\mathrm{lo}(\lfloor h/2 \rfloor) = \mathrm{lo}(h - 1)$; line L11 puts $T[h-1]$ on the left of $a$, so the claim holds for the parent. If $h$ is even, it is a left child and $\mathrm{lo}(\lfloor h/2 \rfloor) = \mathrm{lo}(h)$, so the claim holds without a call. At the root, $\mathrm{lo}(1) = 0$. The loop climbs $L$ levels and makes at most one call per level. SUFFIX is the mirror image: a left child $h$ adds its right sibling $h + 1$ on the right of $a$ (line L13), and $\mathrm{hi}(1) = n - 1$. $\square$

## The FIFO window

The window keeps $F$, the slot of the oldest value, $B$, the slot for the next value, and the count $c$. The window holds the values in the slots $F, F + 1, \dots, F + c - 1$, taken modulo $n$, oldest first.

**Invariant (W).** The window values are in these $c$ slots in this order, every other leaf holds $e$, and (I) holds.

**Lemma 4.** INSERT and EVICT keep (W), and a resize keeps (W) with $F = 0$.

*Proof.* A resize (lines L14 and L17) reads the $c$ values oldest first, builds a new tree with them in the leaves $0, \dots, c - 1$ and $e$ elsewhere (Lemma 1), and sets $F = 0$ and $B = c \bmod n$. INSERT first makes room if $c = n$; then slot $B$ is free and holds $e$. Line L15 writes the new value there with an update (Lemma 2) and advances $B$, so the new value is the youngest. EVICT (line L16) writes $e$ into slot $F$, which is the oldest value, and advances $F$. $\square$

**Theorem 1 (query).** Under (W), QUERY returns $v_1 \oplus v_2 \oplus \cdots \oplus v_c$, where $v_1, \dots, v_c$ are the window values oldest first.

*Proof.* If $c = 0$ the result is $e$. If $c > 0$ and $F < B$, the values fill the slots $F, \dots, B - 1$; if $B = 0$, they fill the slots $F, \dots, n - 1$. In both cases they are in order from left to right, and every other leaf holds $e$. By (I) the root is the combination of all leaves in order, and the identities drop out, so line L18 is correct. Otherwise $c > 0$, $B > 0$ and $F \ge B$ (with $F = B$ only when $c = n$). Then the window wraps: its values are the leaves $F, \dots, n - 1$ followed by the leaves $0, \dots, B - 1$, and the leaves between hold $e$. By Lemma 3 and associativity, line L19 returns $a[F..n-1] \oplus a[0..B-1]$, which is the window in order. $\blacksquare$

## Costs

**Theorem 2 (worst case).** Without a resize, INSERT and EVICT make at most $L = \log_2 n$ calls of $\oplus$, and QUERY at most $2L + 1$. A resize to $n'$ leaves makes $n' - 1$ calls.

*Proof.* INSERT and EVICT are updates with $m = 1$ (Lemma 2). QUERY makes no call on line L18 and two climbs and one combine on line L19 (Lemma 3). A resize is one build (Lemma 1). $\square$

**Theorem 3 (amortized resizing).** Start from an empty window with $n = 1$. Over any sequence of $N$ inserts and evicts, the resizes make at most $4N$ calls of $\oplus$ in total, so $O(1)$ amortized calls per operation.

*Proof.* Right after each resize the tree is at most half full: a doubling from $n$ to $2n$ happens at $c = n$, and a halving from $n$ to $n/2$ happens at $c < n/4$, so $c < (n/2)/2$. Charge each resize to the operations since the previous one. A doubling from $n$ to $2n$ costs $2n - 1$ calls, and it needs $c$ to grow from at most $n/2$ to $n$, so at least $n/2$ inserts paid for it; this is at most 4 calls per operation. For a halving from $n$ to $n/2$, consider the state right after the previous resize to $n$. It was a doubling from $n/2$, which left $c = n/2$, or a halving from $2n$, which left $c = n/2 - 1$ (that halving happened at the first evict that took $c$ below $2n/4$, so $c$ went from $n/2$ to $n/2 - 1$). Now $c \le n/4 - 1$, so at least $n/4$ evicts happened, and the halving costs $n/2 - 1$ calls, at most 2 per operation. The first doubling, from $n = 1$, costs one call and follows one insert. $\square$

**Space.** The array has $2n$ entries. A halving from $n$ happens as soon as $c < n/4$, so after every operation $c \ge \lfloor n/4 \rfloor$. This gives $n \le 4c + 3$, and the extra space is $O(W + 1)$ for a window of $W$ values.
