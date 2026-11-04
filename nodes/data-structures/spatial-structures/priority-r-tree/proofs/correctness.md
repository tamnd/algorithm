---
title: BUILD makes an R-tree with every rectangle in one leaf, nodes of at most B entries and leaves at one depth, it stops, and SEARCH reports exactly the rectangles that meet the window
proves: [correctness, termination]
status: full
---

Let $B \ge 2$ and let $S$ be a finite set of items, each a non-empty closed rectangle with a payload. We prove three lemmas and the theorem. The query bound $O(\sqrt{N/B} + T/B)$ is proved in the paper of Arge, de Berg, Haverkort and Yi and is not repeated here.

**Lemma 1 (PSEUDO-PR-LEAVES partitions $S$).** PSEUDO-PR-LEAVES$(S, B, \text{depth})$ stops and returns a list of groups, each non-empty with at most $B$ items, such that every item of $S$ is in exactly one group. If $|S| > B$, there are at most $|S| - B + 1$ groups.

*Proof.* By strong induction on $|S|$. If $|S| \le B$ (line L1), the result is $[S]$ for non-empty $S$ and the empty list for empty $S$, which is correct. Otherwise lines L2 and L3 take out up to four groups of at most $B$ items each, and each taken group is non-empty, since the loop stops when nothing is left. The first group has exactly $B$ items, since $|S| > B$. Each item is taken out at most once, since it is removed from $S$. If $S'$ items are left, lines L4 and L5 sort them and split them into halves of sizes $\lfloor |S'|/2 \rfloor$ and $\lceil |S'|/2 \rceil$, which partition $S'$ and are smaller than $|S|$, so the induction applies to each half and gives groups that partition each half. Joining the lists gives a partition of $S$ into non-empty groups of at most $B$ items. The first group has $B$ items and every other group at least one, so there are at most $1 + (|S| - B) = |S| - B + 1$ groups. $\square$

**Lemma 2 (levels).** Let a level be a list of $L \ge 1$ nodes. Line L8 makes a new level of nodes, each with between 1 and $B$ entries, in which every node of the old level is the child of exactly one new node, and the entry rectangle of each child is its MBR. If $L \ge 2$, the new level has fewer than $L$ nodes.

*Proof.* Apply Lemma 1 to the $L$ items $(\operatorname{MBR}(u), u)$. Each group becomes a node whose entries are the items of the group, so each node of the old level appears in exactly one new node, with its MBR as the entry rectangle. If $2 \le L \le B$, there is one group, and $1 < L$. If $L > B$, there are at most $L - B + 1 \le L - 1$ groups, since $B \ge 2$. $\square$

**Lemma 3 (the R-tree invariant).** The tree that BUILD returns, for $N \ge 1$, has: every rectangle of $S$ in exactly one leaf entry; between 1 and $B$ entries in each node; every leaf at the same depth; and the rectangle of each internal entry equal to the MBR of its child.

*Proof.* Line L6 makes the leaves from the groups of Lemma 1 on $S$, so each rectangle is in exactly one leaf, and each leaf has between 1 and $B$ entries. By Lemma 2, the loop of lines L7 and L8 runs while the level has at least two nodes, and each pass makes the number of nodes strictly smaller, so the loop stops, with a single node, the root. Each pass adds one level above all nodes of the previous level, and every node of a level is the child of exactly one node of the next level, so by induction on the number of passes, every leaf is at depth equal to the number of passes. The entry rectangles are MBRs by Lemma 2. $\square$

**Lemma 4 (containment).** In the tree, every rectangle stored in a leaf below an internal entry lies inside the rectangle of that entry.

*Proof.* By induction on the height of the child. If the child is a leaf, its MBR contains each of its rectangles. Otherwise its MBR contains the rectangle of each of its entries, which by induction contains each stored rectangle below that entry. $\square$

**Theorem.** SEARCH(root, $q$) stops and reports exactly the payloads of the stored rectangles that meet $q$, each once.

*Proof.* SEARCH visits each node at most once, since every node has one parent, and the tree is finite, so it stops. A payload is reported only at line L10, when its rectangle meets $q$. Conversely, let $r$ meet $q$, stored in leaf $\lambda$. For every internal entry on the path from the root to $\lambda$, the rectangle of the entry contains $r$ by Lemma 4, so it meets $q$, and line L10 sends the search into the child at line L11. So the search reaches $\lambda$ and reports $r$ there. By Lemma 3, $r$ is in exactly one leaf entry, so it is reported once. For $N = 0$ there is no root, and the search reports nothing, which is correct. $\blacksquare$
