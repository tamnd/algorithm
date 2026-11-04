---
title: The skew binary random-access list implements a persistent list
proves: [correctness]
status: full
---

**Setting.** A version is a list of pairs $(w_1, t_1), \ldots, (w_m, t_m)$. For a complete tree $t$ let $\text{pre}(t)$ be its items in preorder, and let the items of the version be $\text{pre}(t_1) \cdots \text{pre}(t_m)$. The version is *good* if (I1) each $w_j = 2^{k_j} - 1$ with $k_j \ge 1$ and $t_j$ is a complete tree with $w_j$ nodes, (I2) $w_1 \le w_2 < w_3 < \cdots < w_m$, and (I3) $\sum_j w_j = n$.

**Lemma 1 (cons).** If $s$ is good with items $X$, then CONS$(x, s)$ is good with items $\langle x \rangle \cdot X$.

*Proof.* Case $m \ge 2$ and $w_1 = w_2 = w = 2^k - 1$ (lines L1 and L2). The new tree $\text{Node}(x, t_1, t_2)$ is complete with $1 + 2w = 2^{k+1} - 1$ nodes, and its preorder is $\langle x \rangle \cdot \text{pre}(t_1) \cdot \text{pre}(t_2)$, so the items are right. By (I2), $w_3 > w$, and $w_3$ is of the form $2^{k'} - 1$ with $k' > k$, so $w_3 \ge 2^{k+1} - 1$. If $w_3 = 2^{k+1} - 1$, the new list starts with two equal weights, which (I2) allows; any later weights are larger than $w_3$. So (I2) holds, and (I3) holds with $n + 1$. Otherwise (line L3), the new first weight is 1. If $m \ge 1$ and $w_1 = 1$, then $w_2 > 1$ (because the first case did not apply), so after the new weight 1 the sequence is $1, 1, w_2, \ldots$ with $w_2 > 1$, and (I2) holds. If $w_1 > 1$ or $m = 0$, (I2) is clear. The items are $\langle x \rangle \cdot X$. $\square$

**Lemma 2 (head and tail).** If $s$ is good and not empty, HEAD$(s)$ is its first item, and TAIL$(s)$ is good with the other items.

*Proof.* The first item is the first item of $\text{pre}(t_1)$, which is the root of $t_1$ (line L4). If $w_1 = 1$ (line L6), dropping $t_1$ removes exactly that item, and a suffix of a sequence that satisfies (I2) satisfies it. Otherwise $t_1 = \text{Node}(x, l, r)$ with $l$ and $r$ complete of weight $h = (w_1 - 1)/2 = 2^{k-1} - 1 \ge 1$ (line L7), and $\text{pre}(t_1) = \langle x \rangle \cdot \text{pre}(l) \cdot \text{pre}(r)$, so the new items are right. The new weights are $h, h, w_2, \ldots$; since $w_2 \ge w_1 > h$, (I2) holds. (I3) holds with $n - 1$. $\square$

**Lemma 3 (tree walk).** Let $t$ be complete with weight $w$ and $0 \le i < w$. The loop of lines L10 to L12 ends at the node that holds item $i$ of $\text{pre}(t)$.

*Proof.* By induction on $w$. If $i = 0$ the item is the root. Otherwise $t = \text{Node}(x, l, r)$ with $l$ and $r$ of weight $h = \lfloor w/2 \rfloor$. In preorder, positions $1, \ldots, h$ are the items of $l$, at positions $0, \ldots, h - 1$ of $\text{pre}(l)$, and positions $h + 1, \ldots, w - 1$ are the items of $r$, at positions $0, \ldots, h - 1$ of $\text{pre}(r)$. Line L12 goes to $l$ with $i - 1$ when $i \le h$, and to $r$ with $i - 1 - h$ otherwise, and both are in range for a tree of weight $h$. The claim follows by induction. $\square$

**Lemma 4 (lookup and update).** If $s$ is good and $0 \le i < n$, LOOKUP$(s, i)$ returns item $i$, and UPDATE$(s, i, y)$ returns a good version whose items are those of $s$ with item $i$ set to $y$, while $s$ is unchanged.

*Proof.* Line L8 keeps the item of the current index the same: skipping the tree $t_j$ removes its $w_j$ items from the front, and lowers $i$ by $w_j$. It stops at the first tree with $i < w_j$, which exists by (I3) because $i < n$. Lemma 3 finishes LOOKUP. UPDATE follows the same walk (line L14), makes a new node with item $y$ and the same children (line L15), and copies each node on the path with the new child in place of the old one (line L16). The new tree has the same shape, so it is complete of weight $w_j$, and its preorder differs from the old one only at item $i$. Line L17 rebuilds the cells in front with the same weights and trees. So the new version is good and has the right items. No line writes to an existing node or cell, so $s$ is unchanged. $\square$

**Theorem.** Every version made by the operations is good, every operation returns the result of the abstract persistent list on its argument, and no operation changes an existing version.

*Proof.* The empty list is good, with no items. By Lemmas 1, 2 and 4 and induction on the number of operations, every version is good and has the items of the abstract list. All operations build new cells and nodes that point to old ones and never write to existing memory, so each old version keeps its items. $\blacksquare$
