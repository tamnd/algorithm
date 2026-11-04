---
title: The teaching version of the Brodal queue keeps the heap order and finds the minimum
proves: [correctness, termination]
status: full
---

This proof is about the teaching version on the page, the skew binomial queue with a pointer to the minimum, which is the code. The full Brodal queue is proved correct in Brodal's paper. We use the invariants of the page:

- **(O)** For each node $x$ with a parent $p$, $\mathrm{key}(p) \le \mathrm{key}(x)$.
- **(K)** Each child of a node $x$ has a rank smaller than $r(x)$; a node of rank 0 has no children; and a node of rank $r$ has at least $2^r$ nodes in its subtree.
- **(L)** The roots are sorted by rank, and only the first two may have the same rank.
- **(M)** If the queue is not empty, $\mathit{min}$ is a root, and no root has a smaller key; else $\mathit{min} = \mathrm{nil}$.
- **(I)** Each item in the queue is in exactly one node, $\mathrm{node}(e)$ is that node, and each node holds an item of the queue.

**Lemma 1.** If (O) and (M) hold, the item of $\mathit{min}$ has the minimum key.

*Proof.* By (O), keys do not decrease along each path down from a root, so each key is at least the key of its root, which is at least $\mathrm{key}(\mathit{min})$ by (M). $\square$

**Lemma 2.** LINK of two roots $s$ and $t$ of the same rank $r$ that satisfy (O) and (K) returns a root of rank $r + 1$ whose tree holds the nodes of both and satisfies (O) and (K).

*Proof.* After line L1, $\mathrm{key}(s) \le \mathrm{key}(t)$, so the new edge from $s$ to $t$ satisfies (O). The child $t$ has the rank $r < r + 1$, and the old children of $s$ have ranks below $r$. The tree has at least $2^r + 2^r = 2^{r + 1}$ nodes. $\square$

**Lemma 3.** Say that a node $x$ is *pending* if (O) holds on every edge except possibly the edge from the parent $p$ of $x$ to $x$, and $\mathrm{key}(p) \le \mathrm{key}(c)$ for every child $c$ of $x$. If $x$ is pending and $\mathrm{key}(x) < \mathrm{key}(p)$, then after the exchange of the items of $x$ and $p$, the node $p$ is pending, or (O) holds everywhere if $p$ is a root.

*Proof.* Let $a = \mathrm{key}(x) < b = \mathrm{key}(p)$ before the exchange; after it, $p$ holds $a$ and $x$ holds $b$. The edges from $x$ to its children hold, since each child has a key at least $b$. The edge from $p$ to $x$ holds, since $a < b$. The edges from $p$ to its other children hold, since these had keys at least $b > a$ by (O). The only edge that may fail is the one from the parent $g$ of $p$ to $p$. The children of $p$ now hold $b$, at $x$, and keys at least $b$, and $\mathrm{key}(g) \le b$ held by (O) before the exchange, so $p$ is pending. $\square$

## Insert

Let the roots before be $R$. Line L3 makes a node $x$ of rank 0 with no children, which satisfies (K).

*Case 1, line L4 is true.* The first two roots $s, t$ have the same rank $r$. Line L5 links them, which gives a root $u$ of rank $r + 1$ with (O) and (K), by Lemma 2. If $\mathit{min}$ was $s$ or $t$, then $\mathrm{key}(u) = \min(\mathrm{key}(s), \mathrm{key}(t)) = \mathrm{key}(\mathit{min})$, so $\mathit{min} \leftarrow u$ keeps (M) on the new root list. Line L6 makes $x$ a leaf child of $u$: its rank 0 is below $r + 1$, and the size of the tree only grows, so (K) holds. If $\mathrm{key}(x) < \mathrm{key}(u)$, line L7 exchanges the items; then $u$ holds a key smaller than its old key, which was at most every key of its tree, and the leaf $x$, which has no children, holds the old key of $u$, which is at least the new one. So (O) holds. By (L), the third root has a rank at least $r + 1$, and all later roots have distinct ranks larger than that of the third, so the new list $u$ and the rest is sorted, and only $u$ and the next root may share a rank: (L) holds.

*Case 2.* $x$ goes to the front. Its rank 0 is at most every rank, and the first two roots of $R$ had different ranks, or there were fewer than two, so the only pair of equal ranks is now at most $x$ and the next root: (L) holds.

In both cases, line L9 sets $\mathit{min}$ to the new front root if it has a smaller key, which keeps (M), since the new front root is the only root whose key is new. The item of $x$ is in exactly one node after the exchanges, and the exchange updates both handles, so (I) holds.

## Remove-root, delete-min and delete

REMOVE-ROOT$(m)$, for a root $m$. Line L12 makes the other roots and the children of $m$ into roots; each is a tree with (O) and (K), and the children lose their only parent, so they are roots. Line L13 processes the trees one by one and keeps the map $B$ with at most one tree per rank: while a tree of the same rank is in $B$, the two are linked by Lemma 2 into one tree of a rank one higher. Each link reduces the number of trees by one, so the inner loop ends, and at the end the trees of $B$ hold all nodes except $m$, with distinct ranks. Line L14 lists them by rank, which gives (L), and picks a root of smallest key, which gives (M). (I) holds for all items but the item of $m$, which leaves the queue.

DELETE-MIN removes $\mathit{min}$, whose item has the minimum key by Lemma 1, and returns that item.

DELETE$(e)$. Line L18 moves the item of $e$ to the root of its tree by exchanges with the parent. Give $e$ the symbolic key $-\infty$, smaller than every key. Then $\mathrm{node}(e)$ is pending, since its children have keys at least the old key of $e$, which is at least the key of its parent, and Lemma 3 applies to each exchange. When the loop stops, $e$ is at the root of its tree and (O) holds everywhere with the symbolic key. The symbolic key appears only on the edges from that root, which REMOVE-ROOT then removes, so (O) holds for the real keys on all the other edges. The item of $e$ leaves the queue, and the rest of the argument is that of REMOVE-ROOT.

## Decrease-key

Line L16 lowers the key of $x$ to $k$. Then (O) can fail only on the edge from the parent of $x$ to $x$: the children of $x$ had keys at least the old key, which is at least $k$. So $x$ is pending: its parent had a key at most the old key of $x$, which is at most the keys of its children. Each exchange of the loop is Lemma 3, so the only possible failure moves up one edge, and when the loop stops, either the edge above $x$ holds or $x$ is a root; in both cases (O) holds everywhere. The nodes and ranks do not change, so (K) and (L) hold. If $x$ is now a root, its key is the only root key that changed, and it went down, so line L17 restores (M); if $x$ is not a root, no root key changed. The exchanges keep the handles right, so (I) holds.

## Meld

MELD joins the two root lists as in line L13. As in REMOVE-ROOT, the result holds all nodes of both queues, with distinct ranks, (O) and (K). The smaller of the two minima has the smallest key among all roots: each root of the result is a root of one of the queues or a link of roots, and a linked root carries the smaller key of the two. So (M) holds.

## Termination

INSERT, FIND-MIN and the error checks do $O(1)$ steps. Each loop of exchanges moves up one level per iteration and stops at a root, so it ends, after at most $\lg n$ iterations by (K). Each iteration of the inner loop of line L13 removes one tree, so the loop ends. So every operation ends.

By (I) and Lemma 1, after each operation the queue holds exactly the items inserted and not yet removed, with their current keys, and FIND-MIN and DELETE-MIN return an item of minimum key. $\blacksquare$
