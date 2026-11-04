---
title: Finger search takes O(log d) time and updates at a finger take O(1) amortized rebalancing
proves: [complexity, amortized]
status: full
---

**Size measure.** For a non-root node $v$, let $c(v)$ be its number of children if $v$ is internal, and its number of keys plus 1 if $v$ is a bottom node. By (F1) of [the correctness proof](correctness.md), $2 \le c(v) \le 4$ in a valid tree. During an update, one node at a time can reach $c = 5$ (overfull, before its split) or $c = 1$ (underfull, before a share or merge).

**Lemma 1 (subtree size).** A node at height $i$ (bottom nodes have height 0) has at least $2^i$ keys below it, unless it is a bottom root.

*Proof.* A non-root bottom node has at least 1 key, and an internal node has at least 2 children. Induction on $i$. $\square$

So the height is at most $\lg n + 1$.

**Theorem 1 (finger search).** Let $d$ be the number of keys strictly between the range of the finger $f$ and $k$, that is, the keys in $(f.hi, k)$ if $k > f.hi$ and in $(k, f.lo]$ if $k \le f.lo$, and $d = 0$ if $f$ holds $k$. Then the climb of lines L1 to L5 goes up at most $\lg d + 1$ levels if $d \ge 1$, and no levels if $d = 0$; FINGER-SEARCH takes $O(\log d + 1)$ time.

*Proof.* Take $k > f.hi$; the other case is the mirror image. Suppose line L5 moves from a node $v$ at height $i$ to its parent. Then $v$ does not hold $k$ and, as $v$ is an ancestor of $f$, $v.hi \ge f.hi$, and $k > v.hi$ by Lemma 1 of the correctness proof (the ranges at one level are in order and $f$ is below $v$). The neighbour $w = v.next$ exists, since the last node of a level has range ending at $+\infty$, and $w.lo = v.hi < k$ while $w$ does not hold $k$, so $k > w.hi$. Every key below $w$ lies in $(v.hi, w.hi] \subseteq (f.hi, k)$, and there are at least $2^i$ of them by Lemma 1. So $d \ge 2^i$. If the climb reaches height $i \ge 1$, it left height $i - 1$, so $d \ge 2^{i-1}$ and $i \le \lg d + 1$. If $d = 0$, no move up happens. The descent from height $i$ takes $i$ rounds. Each round of the climb and of the descent looks at $O(1)$ nodes of at most 4 children, so the time is $O(i + 1) = O(\log d + 1)$. $\square$

**Theorem 2 (rebalancing).** Starting from any valid tree, a sequence of $m$ inserts and deletes, each given the bottom node found by the finger search, does at most $O(m)$ splits, merges and shares in total, plus 1 per increase of the height.

*Proof.* Let $\varphi(1) = 2$, $\varphi(2) = 1$, $\varphi(3) = 0$, $\varphi(4) = 2$, $\varphi(5) = 4$, and $\Phi = \sum_v \varphi(c(v))$ over the non-root nodes $v$. $\Phi \ge 0$ always. The changes of $\varphi$ when $c$ grows by 1 are $-1, -1, +2, +2$ (from $c = 1, 2, 3, 4$), and when $c$ drops by 1 they are $+1, +1, -2, -2$ (from $c = 2, 3, 4, 5$).

- *A key enters or leaves a bottom node:* $c$ changes by 1, so $\Phi$ grows by at most 2.
- *A split* of a node with $c = 5$ gives two nodes with $c = 3$ and $c = 2$ (internal) or $c = 3$ and $c = 3$ (bottom): $\Phi$ drops by at least $4 - 1 = 3$. The parent gains a child, which adds at most 2. So each split lowers $\Phi$ by at least 1, except a split of the root, where the two halves become non-root nodes and add at most 1 to $\Phi$; this happens once per increase of the height.
- *A merge* of a node with $c = 1$ and a sibling with $c = 2$ gives one node with $c = 3$ (internal: $1 + 2$ children) or $c = 2$ (bottom: $0 + 1$ keys): $\Phi$ drops by at least $3 - 1 = 2$. The parent loses a child, which adds at most 1. So each merge lowers $\Phi$ by at least 1. When the root loses its last but one child, the child becomes the root and leaves the sum, which does not increase $\Phi$.
- *A share* happens at most once per delete, since it ends the delete. The node with $c = 1$ goes to $c = 2$ (drop 1) and the sibling drops from $c \in \{3, 4\}$ by 1 (change at most $+1$), so $\Phi$ does not increase.

So each update raises $\Phi$ by at most 2 at its start and at most 2 at its last step, and each split or merge in between lowers it by at least 1, except root splits. Summing over the sequence, the number of splits and merges is at most $4m + \Phi_0 + (\text{the number of root splits})$, and $\Phi_0 \le 2N_0$ for the $N_0$ non-root nodes of the initial tree; from an empty tree $\Phi_0 = 0$. Each split, merge or share takes $O(1)$ time, including the change of the level links and of the ranges. $\blacksquare$

**Corollary.** An insert or a delete at a finger takes $O(\log d + 1)$ time for the finger search plus $O(1)$ amortized time for the rebalancing. In particular, building the tree from $n$ sorted keys, each inserted from the finger of the previous one, takes $O(n)$ time: the finger search has $d = 0$ each time, and the root splits number at most $\lg n + 1$.
