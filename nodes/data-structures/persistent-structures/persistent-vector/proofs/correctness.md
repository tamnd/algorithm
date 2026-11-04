---
title: The persistent vector keeps every version and implements an immutable dynamic array
proves: [correctness]
status: full
---

Fix $B \ge 1$ and $M = 2^B$. For $n \ge 0$ let $T(n) = \text{tailoff}(n)$, which is 0 if $n < M$ and $M \lfloor (n-1)/M \rfloor$ otherwise. Then $T(n)$ is a multiple of $M$, and $1 \le n - T(n) \le M$ when $n \ge 1$. Write $L(n) = T(n)/M$ for the number of leaves in the trie.

**Shape.** For a shift $s$ (a positive multiple of $B$) and a count $\lambda$ with $0 \le \lambda \le 2^s$, the *packed trie* of height $s$ with $\lambda$ leaves is the tree in which the leaf with number $q$, for $0 \le q < \lambda$, is reached from the root by the base-$M$ digits of $q$ written with $s/B$ digits, most significant first, and in which an inner node exists exactly when some leaf is below it. Its slots are in use from slot 0 in each node, because leaf numbers are an initial segment $\{0, \ldots, \lambda - 1\}$. A vector $v$ is *valid* if its trie is the packed trie of height $s$ with $L(n)$ leaves, each leaf full, its tail has $n - T(n)$ items, and (I4) holds: $L(n) \le 2^s$, and $L(n) > 2^{s - B}$ if $s > B$. Its sequence $\text{items}(v)$ is the leaves in order of number, then the tail.

Leaf $q$ holds items $qM$ to $qM + M - 1$, so item $i < T(n)$ is in leaf $\lfloor i/M \rfloor$ at slot $i \bmod M$, and the digits of $\lfloor i/M \rfloor$ in base $M$ are $\text{digit}_\ell(i)$ for $\ell = s, s - B, \ldots, B$. Since $\lfloor i/M \rfloor < L(n) \le 2^s$, the digit at level $s$ is the top digit, and no higher digit is lost.

**Lemma 1 (no change).** No procedure writes a node that existed before the call.

*Proof.* SET-PATH, PUSH-TAIL and POP-TAIL write only to the copy $c$ they made; NEW-PATH and NODE make new nodes; the tail is replaced by a new array in SET, PUSH and POP. $\square$

**Lemma 2 (get).** If $v$ is valid and $0 \le i < n$, GET$(v, i)$ returns item $i$ of $\text{items}(v)$.

*Proof.* If $i \ge T(n)$ the item is at position $i - T(n)$ of the tail (L1). Otherwise L2 follows the digits of $\lfloor i/M \rfloor$, which by the remark above reach leaf $\lfloor i/M \rfloor$, and L3 reads slot $i \bmod M$. $\square$

**Lemma 3 (set).** If $v$ is valid, SET$(v, i, x)$ returns a valid vector whose sequence is $\text{items}(v)$ with item $i$ replaced by $x$.

*Proof.* The tail case (L4) is clear. Otherwise SET-PATH copies each node on the path to leaf $\lfloor i/M \rfloor$, sets one child pointer of each copy to the copy below it, and changes slot $i \bmod M$ of the leaf copy. The new trie has the same shape and the same leaves except that one leaf has one changed slot. $\square$

**Lemma 4 (push).** If $v$ is valid with $n$ items, PUSH$(v, x)$ returns a valid vector with $n + 1$ items whose sequence is $\text{items}(v) \cdot \langle x \rangle$.

*Proof.* If $n - T(n) < M$ (line L9), then $T(n + 1) = T(n)$. For $n < M$, $T(n) = 0$, and $T(n + 1) = 0$ too: either $n + 1 < M$, or $n + 1 = M$ and $T(n + 1) = M \lfloor (M - 1)/M \rfloor = 0$. For $n \ge M$, $n - T(n) < M$ means $n < M \lfloor (n-1)/M \rfloor + M$, so $\lfloor n/M \rfloor = \lfloor (n-1)/M \rfloor$. So the trie is unchanged and the tail grows by one, to at most $M$ items. Otherwise the tail is full, $n = T(n) + M$, and $T(n + 1) = n$, so the tail must become leaf number $L(n)$ and the new tail is $\langle x \rangle$. If $L(n) + 1 \le 2^s$, the leaf number $L(n)$ has $s/B$ digits, which are $\text{digit}_\ell(n - 1)$ since $n - 1$ is the last index of that leaf, and PUSH-TAIL (L11, L13 to L16) copies the nodes on the path that exist and makes the missing part with NEW-PATH; the result is the packed trie with $L(n) + 1$ leaves. Else $L(n) = 2^s$, which is the test $n/M = L(n) + 1 > 2^s$ of line L10, and the new root of height $s + B$ has the old trie, which is complete, as child 0 and a path to the new leaf as child 1; its leaf numbers are $0, \ldots, 2^s$, so it is the packed trie with $2^s + 1$ leaves, and (I4) holds since $2^s + 1 > 2^{(s + B) - B}$. In the first case, (I4) holds since $L$ only grew and did not exceed $2^s$. $\square$

**Lemma 5 (pop).** If $v$ is valid with $n \ge 1$ items, POP$(v)$ returns a valid vector with $n - 1$ items whose sequence is $\text{items}(v)$ without its last item.

*Proof.* For $n = 1$ the result is empty (L17). If the tail has at least two items (L18), $T(n - 1) = T(n)$ by the computation in Lemma 4, and dropping the last tail item is right. Otherwise the tail has one item, $n - 1 = T(n)$, and $T(n - 1) = T(n) - M$ when $n - 1 \ge M$, so the last leaf, number $L(n) - 1$, which holds item $n - 2$, becomes the tail (L19, by Lemma 2's path). POP-TAIL removes this leaf from the trie: along the path of the digits of $n - 2$, it keeps slots $0$ to $j - 1$ of each node, and slot $j$ only if the subtree below still has a leaf, which happens unless every digit below is 0 (the case $c = \text{nil}$ with $j = 0$). This is the packed trie with $L(n) - 1$ leaves, or the empty trie. If now $s > B$ and the root has one child, then $L(n) - 1 \le 2^{s - B}$, and the child is the packed trie of height $s - B$ (L21); otherwise the root has two children and $L(n) - 1 > 2^{s - B}$. Either way (I4) holds. $\square$

**Theorem.** Every version made by the operations is valid, and its sequence is the one that the abstract immutable dynamic array gives to it; GET returns the right item; and no version changes once made.

*Proof.* The empty vector is valid. By induction over the operations, Lemmas 3 to 5 keep validity and give the right sequences, and Lemma 2 gives the reads. By Lemma 1 no node of an existing version is written, so the sequence of each version is fixed. $\blacksquare$
