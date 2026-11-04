---
title: Smoothsort sorts the array in place
proves: [correctness]
status: full
---

**Definitions.** A *Leonardo tree* of order $k$ at root index $r$ occupies $A[r - L(k) + 1 \ldots r]$. For $k \le 1$ it is the node $r$. For $k \ge 2$ its children are $c_2 = r - 1$, the root of a tree of order $k - 2$, and $c_1 = r - 1 - L(k-2)$, the root of a tree of order $k - 1$; the sizes add up, since $L(k-1) + L(k-2) + 1 = L(k)$. The tree is a *heap* when each node is at least each of its children. A *forest* is a list of trees whose segments are consecutive from index 0. We use two invariants for a forest:

- **(H)** each tree is a heap;
- **(R)** the roots are non-decreasing from left to right.

**Lemma 1 (SIFT-DOWN).** If both subtrees of a tree are heaps, SIFT-DOWN of its root makes the tree a heap and only permutes its segment.

*Proof.* This is the sift-down of [heapsort](/heapsort/), on a tree whose children are given by the formulas above. Each swap exchanges the root with its larger child when the root is smaller; then the old child position holds a value that is at least the other child and its own former subtree, except at the new position of the moving item, where the claim is applied again on a smaller tree. When the loop stops, the moving item is at least its children. $\square$

**Lemma 2 (RECTIFY).** Suppose the trees before tree $j$ satisfy (H) and (R), and the two subtrees of tree $j$ (if any) are heaps. Then after RECTIFY$(F, j)$, the trees up to tree $j$ satisfy (H) and (R).

*Proof.* Let $t$ be the current tree, starting with $t = j$, with root $x$ and, if the order is at least 2, children $c_1$ and $c_2$. Let $b$ be the largest of $x$, $c_1$ and $c_2$. The loop keeps this claim: the trees before $t$ satisfy (H) and (R); the subtrees of $t$ are heaps; and each tree after $t$, up to $j$, is a heap whose root is at least all items of the trees to its left and at least the roots before it. At the start there are no trees after $t$, so the claim holds.

If the root $p$ of tree $t - 1$ is greater than $b$, the loop swaps $p$ and $x$. Now the root of $t$ is $p$, which is greater than $c_1$ and $c_2$, so tree $t$ is a heap. Since $p$ was the largest item of the heap $t - 1$, and the roots before $t - 1$ are at most $p$ by (R), the new root $p$ of tree $t$ is at least all items to its left. Tree $t - 1$ now has root $x$ and subtrees that are heaps, so the claim holds with $t - 1$ as the current tree.

If $p \le b$, or $t$ is the first tree, the loop stops, and SIFT-DOWN makes tree $t$ a heap by Lemma 1. Its root is now $b$, the largest item of the tree, and $b \ge p$, so (R) holds between $t - 1$ and $t$. Between $t$ and $t + 1$: the root of $t + 1$ was set to a root that was larger than all items of tree $t$ at that time, and tree $t$ has the same items now. So (R) holds for all trees up to $j$. $\square$

**Lemma 3 (the build step).** If the forest of $A[0 \ldots i-1]$ satisfies (H) and (R), then after lines L3 to L5 the forest of $A[0 \ldots i]$ does.

*Proof.* If line L3 joins trees of orders $k + 1$ and $k$, they occupy $A[i - L(k+1) - L(k) \ldots i - 1]$, and with the root $i$ they form a tree of order $k + 2$ in the layout above, with heaps as subtrees. If line L4 adds a single node, it is a tree with no subtrees. In both cases the earlier trees are unchanged, so Lemma 2 applies with $j$ the last tree. $\square$

**Lemma 4 (the removal step).** If the forest of $A[0 \ldots i]$ satisfies (H) and (R), then $A[i]$ is the largest item of $A[0 \ldots i]$, and after lines L7 to L9 the forest of $A[0 \ldots i-1]$ satisfies (H) and (R).

*Proof.* By (H), each root is the largest item of its tree, and by (R) the last root is the largest root. The last root is at index $i$, the right end of the prefix. Removing it leaves either no new tree ($k \le 1$) or its two subtrees, which are heaps and occupy the end of the prefix in the order left, right. Lemma 2 applied to the left subtree, whose own subtrees are heaps, gives (H) and (R) up to it; then Lemma 2 applied to the right subtree gives them for the whole forest. $\square$

**Theorem.** After SMOOTHSORT$(A)$, the array is sorted, and it holds the input items.

*Proof.* All changes are swaps, so the multiset of items is unchanged. By Lemma 3 and induction on $i$, after the build the forest of $A[0 \ldots n-1]$ satisfies (H) and (R). By Lemma 4 and induction downwards on $i$, at each step of line L6 the item $A[i]$ is the largest of $A[0 \ldots i]$, and it is not moved again, because all later steps work inside $A[0 \ldots i-1]$. So for each $i \ge 1$, $A[i]$ is at least each item before it, and the array is sorted. $\blacksquare$
