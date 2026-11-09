---
title: The Beyer-Hedetniemi successor lists every rooted tree once, in constant amortized time
proves: [correctness]
status: full
---

A *level sequence* of length $n \ge 1$ is a sequence $\ell = (\ell_1, \ldots, \ell_n)$ with $\ell_1 = 0$ and $1 \le \ell_{i+1} \le \ell_i + 1$; it is the list of depths, in preorder, of the nodes of an ordered rooted tree, and the parent of node $i \ge 2$ is the last $j < i$ with $\ell_j = \ell_i - 1$. The subtree of node $j$ occupies the positions from $j$ up to, but not including, the next position $k > j$ with $\ell_k \le \ell_j$. Call such a segment a *block at level* $\ell_j$: its first entry is $\ell_j$ and all its other entries are larger. Sequences are compared lexicographically, and a proper prefix is smaller than the longer sequence.

An ordered tree is *sorted* if, at every node, the blocks of its children are in non-increasing order from left to right. Let $\mathcal{C}_n$ be the set of level sequences of length $n$ that are the largest in their isomorphism class, the *canonical* sequences.

**Fact F.** Let $A$ and $B$ be blocks at the same level $c$ with $A < B$. Then the concatenation $BA$ is larger than $AB$.

*Proof.* If $A$ and $B$ differ at a position that both have, the first such position decides, and $B$ is larger there. Otherwise $A$ is a proper prefix of $B$. Then $AB$ continues after $A$ with the entry $c$, the start of $B$, while $BA$ continues with the next entry of $B$, which is larger than $c$. $\square$

**Lemma 1 (canonical means sorted).** Each isomorphism class of rooted trees with $n$ nodes contains exactly one sorted level sequence, and it is the largest sequence in the class. So $\mathcal{C}_n$ is the set of sorted level sequences, and it is in bijection with the unlabeled rooted trees with $n$ nodes.

*Proof.* Uniqueness, by induction on $n$. The class of a tree is given by the multiset of the classes of the root's subtrees. In a sorted sequence, each child block is itself sorted after subtracting $1$, so by induction it is the unique sorted sequence of its class; the blocks are then placed in non-increasing order, which fixes their order up to equal blocks. So the sorted sequence of a class is unique, and it exists, since sorting the children at every node gives one.

Maximality. Let $S$ be the largest sequence in a class. If $S$ is not sorted, some node has adjacent child blocks $A$, $B$ in this order with $A < B$. Exchanging the two subtrees gives a tree of the same class, whose sequence is $S$ with $AB$ replaced by $BA$ in place. By Fact F it is larger than $S$, a contradiction. So $S$ is sorted, and it is the unique sorted sequence. $\square$

**Lemma 2 (prefixes and level-one leaves).** Let $\ell \in \mathcal{C}_n$.

1. Every prefix $(\ell_1, \ldots, \ell_m)$ with $m \ge 1$ is canonical.
2. If $\ell_{i-1} = \ell_i = 1$ for some $i$, then $\ell_j = 1$ for all $j \ge i$.

*Proof.* (1) In the prefix, the child blocks of each node are blocks of $\ell$, except that the last one may be cut short, and some later ones may be missing. A cut block is a prefix of the original block, so it is not larger. The order stays non-increasing at every node, and the prefix is sorted. (2) Node $i - 1$ is a child of the root with no children, so its block is $(1)$. A block at level $1$ that is at most $(1)$ is $(1)$ itself, since $(1)$ is a proper prefix of every longer block at level $1$. So every later child of the root is a leaf, and every later entry is $1$. $\square$

**Lemma 3 (successor).** Let $\ell \in \mathcal{C}_n$ with $\ell_i \ge 2$ for some $i$. Let $p = \max\{i : \ell_i \ge 2\}$, let $q$ be the parent of $p$, let $d = p - q$ and $c = \ell_q = \ell_p - 1$, and define $s$ by $s_i = \ell_i$ for $i < p$ and $s_i = s_{i-d}$ for $i = p, \ldots, n$. Then $s \in \mathcal{C}_n$, $s < \ell$, and no $y \in \mathcal{C}_n$ satisfies $s < y < \ell$.

*Proof.* Since $\ell_i = 1$ for $i > p$, node $p$ is a leaf and it is the last node in the subtree of $q$. So $A = (\ell_q, \ldots, \ell_{p-1})$ is the subtree of $q$ without its last child $p$, and $s_p, \ldots, s_n$ is $A, A, \ldots$ cut to length $n - p + 1$. Let $g$ be the parent of $q$, with $\ell_g = c - 1$; it exists because $c \ge 1$.

*$s$ is a level sequence, and $s < \ell$.* Inside a copy of $A$ the steps are steps of $\ell$. A new copy starts with $c$, and the entry before it is at least $c$, so the step is allowed. The two sequences agree before $p$ and $s_p = c < \ell_p$.

*$s$ is sorted.* The copies of $A$ that start at $p, p + d, \ldots$ are children of $g$, because all entries between $g$ and them are at least $c$. Consider the nodes of $s$.

- Nodes inside a copy of $A$. In $\ell$, the children of $q$ are sorted, and dropping the last child $p$ keeps them sorted; the other nodes of $A$ are unchanged. So $A$ is sorted, every full copy is sorted, and the last, possibly cut, copy is sorted by Lemma 2.
- The node $g$. In $\ell$ its children are $Y_1 \ge \cdots \ge Y_t \ge Q$, where $Q = (\ell_q, \ldots, \ell_p)$ is the subtree of $q$, possibly followed by leaves at level $1$ if $g$ is the root. In $s$ they are $Y_1, \ldots, Y_t, A, A, \ldots, A'$ with $A'$ a prefix of $A$. Here $Y_t \ge Q > A$, since $A$ is a proper prefix of $Q$, and $A \ge A'$. So they are sorted.
- An ancestor $h \ne g$ of $q$. Its last child block $E$ in $\ell$ contains $q$ and ends at $p$, followed only by leaves at level $1$ if $h$ is the root. In $s$ this block runs to position $n$, agrees with $E$ before $p$, and is smaller at $p$. So it is smaller than $E$, hence not larger than the block before it, and the order stays non-increasing.
- All other nodes have the same subtree in $s$ as in $\ell$.

By Lemma 1, $s \in \mathcal{C}_n$.

*No canonical sequence lies between.* Let $y \in \mathcal{C}_n$ with $y < \ell$, and let $k$ be the first index with $y_k \ne \ell_k$, so $y_k < \ell_k$. If $k > p$, then $\ell_k = 1$ and $y_k \ge 1$, which is impossible. If $k < p$, then $y_k < \ell_k = s_k$, so $y < s$. If $k = p$ and $y_p < c$, then $y < s$. It remains the case $y_p = c$, where $y$ and $s$ agree on $1, \ldots, p$. In $y$, the subtree of $q$ is then exactly $A$, and $p$ starts a later child of $g$. Write $y_p \cdots y_n = B_1 B_2 \cdots B_m R$, where $B_1, \ldots, B_m$ are the blocks of the children of $g$ that start at or after $p$, and $R$ is empty or starts with an entry less than $c$. Since $y$ is sorted, $A \ge B_1 \ge \cdots \ge B_m$. Compare $y_p \cdots y_n$ with $s_p \cdots s_n = AA\cdots$ block by block. While $B_j = A$, the two agree on that copy. At the first $B_j \ne A$: $A$ is not a proper prefix of $B_j$, since then $B_j > A$. If $B_j$ and $A$ differ at a position that both have, $y$ is smaller there. If $B_j$ is a proper prefix of $A$, then the next entry of $y$, if there is one, is $c$ or less than $c$, while the next entry of $s$ is an inner entry of $A$, larger than $c$. If all blocks equal $A$ and $R$ is not empty, the first entry of $R$ is less than $c$, while $s$ starts a new copy with $c$. In every case $y \le s$. $\square$

The path $(0, 1, \ldots, n - 1)$ is the largest level sequence of length $n$, since $\ell_i \le i - 1$, and the star $(0, 1, \ldots, 1)$ is the smallest, since $\ell_i \ge 1$ for $i \ge 2$. Both are sorted. The star is the only canonical sequence for which Lemma 3 does not apply.

**Lemma 4 (the implementation).** At the start of each call of NEXT, after the current tree is visited:

1. $L[1..n]$ is a canonical sequence $\ell$;
2. $\mathit{par}[i]$ is the parent of $i$ in $\ell$, for $2 \le i \le n$;
3. $1 \le p \le n$ and $L[i] = 1$ for $p < i \le n$.

Each call either returns LAST, when $\ell$ is the star, or changes $L$ into the sequence $s$ of Lemma 3.

*Proof.* At the start, $L$ is the path, $\mathit{par}[i] = i - 1$ and $p = n$. Assume the invariant. By part 3, line L1 stops at the largest index with $L[p] \ne 1$. If $p = 1$, every other entry is $1$, $\ell$ is the star, and line L2 returns. Otherwise $L[p] \ge 2$, and $p$ is the $p$ of Lemma 3.

*Line L3 is true.* Then $L[p] = 2$ and $L[p - 1] = 1$, so $q = p - 1$, $A = (1)$ and $s$ is $\ell$ with $s_p = 1$, since the later entries are already $1$. Line L4 makes this change. Node $p$ is now at level $1$, so its parent is the root, which is $\mathit{par}[p - 1]$. The invariant holds with the same $p$, because now $L[i] = 1$ for all $i \ge p$.

*Line L3 is false.* Line L6 sets $d = p - \mathit{par}[p] = p - q$, and lines L7 and L8 compute $s_i = s_{i-d}$ for $i = p, \ldots, n$, in this order. For the parents: the sequence $s$ is $A$ followed by copies of $A$ from position $q$ on. If node $i - d$ is the first node of its copy, then node $i$ is the first node of the next copy, and its parent is $g$. Then $\mathit{par}[i - d] = g < q$, so $d + \mathit{par}[i - d] < p$, and line L9 sets $\mathit{par}[i] = g$. Otherwise the parent of $i - d$ lies in the same copy, at or after its first node, which is at least $q$; so $d + \mathit{par}[i - d] \ge p$, and line L9 sets $\mathit{par}[i]$ to the same node shifted by one copy, which is the parent of $i$. Here $\mathit{par}[i - d]$ is already correct for $s$, either because $i - d < p$ or by induction on $i$. Line L10 sets $p = n$, and part 3 holds. $\square$

**Lemma 5 (cost).** If NEXT is called $N$ times, where $N = |\mathcal{C}_n|$, the loop of line L1 decrements $p$ at most $2N$ times in total, and the loop of line L7 makes at most $3N$ passes in total.

*Proof.* First, each call decrements $p$ at most twice. In the first call, $L$ is the path and at most one decrement happens, for $n = 2$. After a call that took line L4 at position $p$, we have $L[p] = L[p - 1] = 1$; the old sequence had $L[p] = 2$ after $L[p - 1] = 1$, so by Lemma 2 part 2 the entry $L[p - 2]$ is not $1$, or $p - 2 = 1$ and $L[1] = 0$. So the next call decrements exactly twice. After a call that took line L5, $p = n$, and $L[n - 1]$ and $L[n]$ are not both $1$. Indeed, the new entries at positions $q, \ldots, n$ are $A$ followed by copies of $A$, and in each copy only the first entry can be $1$. If $d \ge 2$, two copy starts are $d \ge 2$ apart, so two adjacent positions in $q, \ldots, n$ are never both $1$; and $n - 1 \ge p - 1 \ge q + 1$, so this covers the positions $n - 1$ and $n$. If $d = 1$, then $q = p - 1$ and $A = (c)$. Here $c = 1$ would mean $L[p] = 2$ and $L[p - 1] = 1$ before the call, which is the case of line L3; so $c \ge 2$, and all entries from $q$ on equal $c$. So the next call decrements at most once.

Second, $p$ starts at $n$, ends at a value at least $1$, and changes only by the decrements of line L1 and the resets of line L10, which raise it by $n - p$. So the total increase is at most the total decrease, which is at most $2N$. A call through line L5 makes $n - p + 1$ passes of line L7, that is, the increase it causes plus one. The total is at most $2N + N = 3N$. $\square$

**Theorem.** For $n \ge 1$, the generator visits every unlabeled rooted tree with $n$ nodes exactly once, as its canonical level sequence, in decreasing lexicographic order, starting with the path and ending with the star. It keeps the parent array correct at each visit, and the total time is $O(n + N)$, where $N$ is the number of trees, so the time per tree is $O(1)$ amortized.

*Proof.* The first sequence is the path, the largest element of $\mathcal{C}_n$. By Lemma 4, each call replaces the current sequence by the sequence $s$ of Lemma 3, which by Lemma 3 is the next smaller element of $\mathcal{C}_n$, until the star, the smallest element, is visited, after which the call returns LAST. So every element of $\mathcal{C}_n$ is visited once, in decreasing order, and by Lemma 1 these are the rooted trees, each once. The setup takes $O(n)$ time. Each call does $O(1)$ work apart from the loops of lines L1 and L7, and by Lemma 5 these loops make $O(N)$ steps in total. $\blacksquare$
