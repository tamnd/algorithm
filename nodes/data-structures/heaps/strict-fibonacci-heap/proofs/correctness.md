---
title: The strict Fibonacci heap operations keep heap order and the structure invariant I1
proves: [correctness]
status: full
---

We use the definitions of the page. Every key is treated as distinct (ties are broken by the order of insertion), and $-\infty$ is smaller than every key. We prove the following, for the operations of the pseudocode.

- (H) *Heap order.* Every node has a larger key than its parent.
- (B) *Bookkeeping.* The root is passive. Every active node has rank equal to its number of active children. The active children of every node come before its passive children. Every active root has loss 0.
- (C) *The rank condition.* For every active node $v$ and every $i$, the $i$-th rightmost active child $c$ of $v$ has $\mathrm{rank}(c) + \ell(c) \ge i - 1$.

(B) and (C) are the parts of I1 that the code keeps; the part of I1 that puts the linkable children of the root at its right end is only needed to find them in $O(1)$ time, and the code does not use it. The invariants I2 to I4 are proved in Section 5 of the paper and are not proved here.

**Lemma 1 (links).** A link of $x$ below $y$ with $\mathrm{key}(y) < \mathrm{key}(x)$ keeps (H), and it keeps the second half of (B): an active $x$ goes before all children of $y$, a passive $x$ after all of them.

*Proof.* The only new parent relation is $y$ above $x$, and $\mathrm{key}(y) < \mathrm{key}(x)$. The subtree of $x$ moves as a whole, so all other parent relations are unchanged. The placement is the definition of link. $\square$

Every link in the code is of this kind: the active root and the two-node loss reductions link the node of larger key below the one of smaller key; the root degree reduction links $z$ below $y$ below $x$ with $x < y < z$; and every other link puts a node below the root or below the new root of delete-min, which by the lemmas below has the smallest key in the heap.

**Lemma 2 (the effect of a lost child on (C)).** Suppose an active child $c$ is removed from an active node $v$, and then the rank of $v$ goes down by one and its loss goes up by one. Then (C) still holds at $v$, at the parent of $v$, and at every other node.

*Proof.* At $v$: the active children right of $c$ keep their index, and those left of $c$ get an index one smaller, so their condition gets weaker. At the parent of $v$: $\mathrm{rank}(v) + \ell(v)$ does not change, and the index of $v$ does not change. Nothing else changes. $\square$

If $v$ is an active root, only its rank goes down. Then (C) at $v$ holds by the first half of the proof, and no condition is on $v$ itself, because its parent is passive. If $v$ is passive, nothing is subtracted, and no condition is on $v$ or on its children's ranks at $v$.

**Lemma 3 (the transformations).** Each of the four transformations keeps (H), (B) and (C), and keeps the set of nodes.

*Proof.* (H) and the placement of children hold by Lemma 1. No node is created or deleted.

*Active root reduction.* Let $x$, $y$ be active roots of rank $r$. After the link, $y$ is an active child of the active $x$, so it is no longer an active root, which is allowed. The rank of $x$ becomes $r + 1$, which is its new number of active children. In $x$, $y$ is the $(r + 1)$-th rightmost active child, and $\mathrm{rank}(y) + \ell(y) = r + 0 \ge r$, so (C) holds. No other active child of $x$ changes its index. If the passive rightmost child $z$ of $x$ moves to the root, no active index changes. $x$ is still an active root with loss 0.

*Root degree reduction.* $x$, $y$, $z$ are linkable, so they have no active children. After the step, $y$ has no active child and $z$ is passive, so $\mathrm{rank}(y) = 0$ is right; $x$ has the one active child $y$, so $\mathrm{rank}(x) = 1$ is right, and the condition for $y$ is $0 + 0 \ge 0$. $x$ is a child of the passive root, so it is an active root, and its loss is 0. The rank of the root is not used, since the root is passive.

*One-node loss reduction.* $x$ has loss at least 2, so by (B) it is not an active root, so its parent $y$ is active. Removing $x$ and the update of $y$ are the case of Lemma 2, or of the remark after it if $y$ is an active root. Then $x$ is linked below the passive root with loss 0, which makes it an active root with loss 0, as (B) needs; no condition is on $x$.

*Two-node loss reduction.* $x$ and $y$ have loss 1 and rank $r$, so neither is an active root, and the parent $z$ of $y$ is active. First $y$ is cut and linked below $x$, the rank of $x$ goes to $r + 1$, and both losses go to 0. In $x$, $y$ is the $(r + 1)$-th rightmost active child with $r + 0 \ge r$. At the parent of $x$, $\mathrm{rank}(x) + \ell(x)$ goes from $r + 1$ to $(r + 1) + 0$, so it does not change. Then the rank of $z$ goes down by one and, if $z$ is not an active root, its loss goes up by one; with the cut of $y$ this is the case of Lemma 2. If $z = x$, the net effect on $x$ is rank $r$ and loss 1, again with the sum $r + 1$, so the parent of $x$ still sees no change. $\square$

**Lemma 4 (the operations).** Insert, meld, decrease-key and delete-min keep (H), (B) and (C), and the root holds the smallest key.

*Proof.* By (H), the root of a tree has its smallest key. The transformations are covered by Lemma 3; it remains to check the other steps.

*Meld (lines L2 to L4).* All nodes of the smaller tree become passive, so no condition of (B) or (C) is on them, and the active nodes of the larger tree keep their children. The root $v$ of larger key is linked below the other root $u$, which keeps (H) by Lemma 1, and $v$ is passive. The active children of $v$ still have a passive parent. The root $u$ is passive. Insert is a meld.

*Decrease-key (lines L6 to L9).* Lowering $\mathrm{key}(x)$ keeps (H) between $x$ and its children. If the new key is below the key of the root, the items of $x$ and the root are swapped; then the root has a key smaller than all others, and $x$ has the old key of the root, which is smaller than all keys in the subtree of $x$, so (H) holds below $x$. In both cases the only relation that may break (H) is between $x$ and its parent $y$, and line L7 removes it by moving $x$ below the root, whose key is now the smallest. If $x$ is passive, no active index changes. If $x$ is an active root, the passive $y$ is not changed, and $x$ stays an active root. If $x$ and $y$ are active, line L8 is the case of Lemma 2 (or of the remark after it, if $y$ is an active root), and $x$ becomes an active root with loss 0.

*Delete-min (lines L10 to L14).* By (H) every node other than the root is in the subtree of a child of the root, so the child $x$ of smallest key has the smallest key of all the remaining items. Line L10 makes $x$ passive, so its active children become active roots, and they get loss 0. Line L11 puts the other children of the old root below $x$, which keeps (H) since $x$ has the smallest key; active nodes among them stay active roots. Line L12 moves only passive children, so no active index changes, and they go below $x$, which keeps (H). Line L13 and line L14 are transformations. $\square$

**Lemma 5 (termination).** The loop of line L14 ends after at most $2 \deg(\text{root}) + 3a$ rounds, where $a$ is the number of active roots when it starts.

*Proof.* Let $P = 2 \deg(\text{root}) + 3a$. An active root reduction removes one active root and adds at most one child to the root, so $P$ drops by at least $3 - 2 = 1$. A root degree reduction removes three children of the root, adds one, and adds one active root, so $P$ drops by $6 - 2 - 3 = 1$. Since $P \ge 0$, the loop ends. Each other operation does a fixed number of transformations. $\square$

**Theorem.** Every operation ends, the root always holds the smallest key, find-min returns it, delete-min removes and returns it and keeps all other items, and insert, meld, decrease-key and delete change the set of items as the abstract type says.

*Proof.* Termination is Lemma 5. By Lemma 4, (H) holds after every operation, so find-min returns the smallest key. Delete-min removes only the old root, whose key was the smallest; by Lemma 4 it keeps every other node, and the new root holds the smallest remaining key. Insert adds one node, meld takes the union of the two node sets, and decrease-key changes one key and moves nodes but removes none; the swap of items keeps the set of (item, key) pairs, and the handle of each item follows it to its new node. Delete is decrease-key to $-\infty$, after which the item is at the root, followed by delete-min. $\blacksquare$
