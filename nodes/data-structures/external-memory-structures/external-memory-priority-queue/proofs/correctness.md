---
title: The buffer-tree priority queue returns the minimum and keeps its invariants
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Items are pairs $(k, s)$ with distinct insertion numbers $s$, compared by key and then by $s$, so all items are distinct and a smallest item has a smallest key, the earliest inserted among equal keys. Let $T$ be the multiset of items in the tree, in leaves and in buffers, and let $Q = \texttt{mem} \cup T$ be the content of the queue. We prove that, between operations,

- (P1) every item of `mem` is smaller than every item of $T$, and
- (P2) the tree satisfies the invariants (T1) to (T3) of the [buffer tree](/buffer-tree/) and no buffer is full, where the tree takes only inserts, so (D) of that page says: after all buffers are emptied, the leaves hold exactly $T$,

and that each call returns what the abstract priority queue returns.

**Base.** The empty queue has an empty `mem` and a tree with one empty leaf. Both hold.

**INSERT.** Let $k$ be the new item and $a = \max(\texttt{mem})$ if `mem` is not empty.

- If `mem` is empty or $k > a$ (line L1 fails), then $k$ goes to the tree in line L3. Every item of `mem` is at most $a < k$, so (P1) holds.
- If $k < a$, line L2 puts $k$ into `mem` in the place of $a$, and line L3 inserts $a$ into the tree. The new `mem` has all its items at most $a$; they are smaller than $a$ except $a$ itself, which has left. So all items of the new `mem` are smaller than $a$. By (P1) before the step, $a$ is smaller than every item of the old $T$. So the new `mem` is smaller than the new $T = T \cup \{a\}$, and (P1) holds.

In both cases $Q$ gains exactly $k$. Line L3 is the insert of the buffer tree, which keeps (P2) by the proof of that page. INSERT returns nothing and ends, since the buffer tree insert ends.

**DELETE-MIN, when `mem` is not empty.** By (P1), $\min(\texttt{mem})$ is smaller than every item of $T$ and is the smallest of `mem`, so it is the minimum of $Q$. Line L6 removes and returns it. Removing an item from `mem` keeps (P1), and the tree does not change.

**REFILL.** It is called when `mem` is empty.

*Line L7.* Each step finds the highest node $y$ on the leftmost path with a nonempty buffer, so the buffers of all ancestors of $y$ are empty, which is the condition under which EMPTY$(y)$ keeps (P2) by the proof of the buffer tree. EMPTY does not change $T$; it only moves items down or into leaves. The loop ends: each step moves the items of a buffer at least one level down or into the leaves, no item enters the tree during the loop, and the height can grow only by splits, which happen only when a bottom node gets more than $m$ leaves, so it is bounded by the number of items. When the loop ends, all buffers on the leftmost path are empty.

*Line L8 and L9.* Let $x$ be the leftmost bottom node, and let $I$ be the set of items in its leaves. Its buffer is empty, so all items of $T$ in the range of $x$ are in $I$, by (T2). Let $y$ be a node on the leftmost path, other than $x$, and $c_1$ its first child; the range of $c_1$ is the part of the range of $y$ below its first routing key $r$, and the routing is by `bisect_right`, so every item in the range of $c_1$ is smaller than $r$ and every item in the other children of $y$ is at least $r$. Going down the path, every item of $T$ that is not in $I$ is in a buffer on the path, which is empty, or in a subtree to the right of the path, at some node $y$ of the path, so it is at least the first routing key $r$ of $y$, while every item of $I$ is in the range of $c_1$ and so smaller than $r$. So every item of $T \setminus I$ is larger than every item of $I$. Line L9 moves $I$ to `mem`. The new `mem` is $I$, the new $T$ is $T \setminus I$, and (P1) holds.

*Line L10.* It removes $x$ and its leaves, then each ancestor left with no children, together with the routing key next to it. The remaining nodes keep their order, so the routing keys of each node stay increasing, and each remaining child has a range that contains its old range, so (T1) and (T2) still hold for all items in the remaining leaves and buffers. Whole subtrees go away, so all leaves remain at one depth. No buffer changes, so (T3) and the buffer sizes hold. If $x$ is the root, the tree becomes an empty bottom root, which is valid.

*Line L11.* Replacing a root that has one child by the child removes one level above all leaves at once, so the depths stay equal, and the child's range becomes all keys, which contains its old range. The root that is removed has an empty buffer, because it is on the leftmost path. So (P2) holds. The loop ends since each step lowers the height.

**DELETE-MIN, when `mem` is empty.** After REFILL, (P1) holds. If `mem` is still empty, then $I$ was empty, so the leftmost bottom node had no items. If the tree is a single bottom root, then $T$ was empty, and line L5 reports an empty queue correctly. Otherwise, a non-root bottom node with no items cannot exist in this code: a bottom node gets leaves only from EMPTY-BOTTOM, which makes at least one leaf per $B$ items, and items leave the tree only through L9, which removes the whole node; a bottom node made by a split gets at least one nonempty leaf. So in this case $T$ is empty, and the error is correct. If `mem` is not empty, line L6 returns its minimum, which is the minimum of $Q$ by the case above.

**Termination.** INSERT runs the buffer tree insert, which ends. REFILL runs loops that end, as shown, and DELETE-MIN calls REFILL at most once.

So every DELETE-MIN returns a smallest item of the queue, ties broken by insertion order, and every operation keeps (P1) and (P2). $\blacksquare$
