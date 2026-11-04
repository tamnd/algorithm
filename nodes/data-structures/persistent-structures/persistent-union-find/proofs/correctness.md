---
title: The persistent union-find gives every version its own partition
proves: [correctness]
status: full
---

**Setting.** Each persistent array version $t$ has fixed contents $\text{cont}(t)$ in the abstract model: the first version holds its initial list, and SET$(t, i, v)$ returns a version whose contents are $\text{cont}(t)$ with slot $i$ set to $v$. A handle $h$ denotes the partition $P(h)$ whose blocks are the trees of the forest $\text{cont}(h.\text{parent})$.

**Lemma 1 (rerooting).** Let the diffs and the shared array $A$ of one family satisfy: the Arr version $t_*$ has $\text{cont}(t_*) = A$, and each $\text{Diff}(i, v, t')$ version $t$ has $\text{cont}(t) = \text{cont}(t')$ with slot $i$ set to $v$. Then after REROOT$(t)$ the same holds, $t$ is the Arr version, and no version has changed contents.

*Proof.* We also keep the fact that the Diff pointers form a tree whose root is the Arr version; it holds for a single version, SET puts a new root above the old one, and each step below reverses one edge of the path to the root, which keeps a tree with the new root. So the path $t_0, \ldots, t_m$ of line A1 ends at the Arr version. Consider the step for $j$ (lines A3 to A6). Before it, $t_{j+1}$ is Arr with $A = \text{cont}(t_{j+1})$, and $t_j = \text{Diff}(i, v_j, t_{j+1})$. After it, $A$ has slot $i$ set to $v_j$, which is $\text{cont}(t_j)$, and $t_j$ is Arr. The version $t_{j+1}$ becomes $\text{Diff}(i, a, t_j)$ with $a$ the old $A[i]$; since $\text{cont}(t_j)$ and $\text{cont}(t_{j+1})$ differ at most in slot $i$, the contents of $t_{j+1}$ equal $\text{cont}(t_j)$ with slot $i$ set to $a$. No other version changes. So the hypothesis holds after each step, and at the end $t = t_0$ is Arr. $\square$

**Corollary 2.** GET$(t, i)$ returns slot $i$ of $\text{cont}(t)$, and SET$(t, i, v)$ returns a version with the contents of the model, while no existing version changes contents.

*Proof.* GET reroots and reads $A = \text{cont}(t)$. SET reroots, makes $t'$ the Arr version, writes $v$ into $A$ so that $A = \text{cont}(t')$, and turns $t$ into $\text{Diff}(i, a, t')$ with $a$ the old value, which keeps the hypothesis of Lemma 1. (When $v$ equals the old value, the implementation returns $t$ itself, which has the right contents.) $\square$

By Corollary 2 we can reason about each handle as if its arrays were plain arrays with the contents $\text{cont}$, which no later operation changes, except where a line writes to a handle field.

**Invariant.** A handle is *good* if its forest $F = \text{cont}(h.\text{parent})$ and ranks $R = \text{cont}(h.\text{rank})$ satisfy: the roots of $F$ are its fixed points, and $R[F[x]] > R[x]$ for each non-root $x$.

**Lemma 3 (find).** On a good handle, FIND$(h, x)$ returns the root of the tree of $x$ in $F$, and afterwards $h$ is good and $P(h)$ is unchanged.

*Proof.* The walk of line L2 visits nodes of strictly growing rank, so it ends, at a fixed point $r$, which is the root of the tree of $x$. The loop of line L4 visits the same nodes $x = y_0, y_1, \ldots, y_k = r$ and sets the parent of each $y_j$ with $j < k$ to $r$. Each $y_j$ stays in the tree of $r$, every other node keeps its parent, and the subtrees below each $y_j$ move with it, so the trees, and hence the blocks, are the same. The ranks along the walk grow strictly, so $R[r] > R[y_j]$ for $j < k$, and the invariant holds for the new parent of each $y_j$. Line L5 stores the new parent array, so $h$ is good and $P(h)$ is unchanged. $\square$

**Lemma 4 (union).** On a good handle, UNION$(h, x, y)$ returns a good handle $h'$ with $P(h')$ equal to $P(h)$ with the blocks of $x$ and $y$ merged, and $P(h)$ is unchanged.

*Proof.* By Lemma 3, line L7 gives the roots $r_x$ and $r_y$ and leaves $P(h)$ as it was. If they are equal (line L8), $x$ and $y$ share a block and $h$ is the answer. Otherwise lines L10 to L12 set the parent of one root to the other root, which joins the two trees into one and leaves all other trees alone, so the blocks of $x$ and $y$ are merged. If the ranks differ, the new child has the smaller rank, so the invariant holds. If they are equal, the new parent's rank goes up by one, which keeps the invariant at the new child and at the old children of $r_x$. All writes are SET calls, which make new versions by Corollary 2, so $h$ keeps its contents. $\square$

**Theorem.** For every sequence of operations, every handle is good and denotes the partition that the abstract type gives to it, and FIND and SAME return answers that agree with that partition, on every version.

*Proof.* MAKE$(n)$ gives the forest of $n$ roots with rank 0, which is good and denotes the singletons. By Lemmas 3 and 4, by induction on the number of operations, every handle is good and denotes the right partition. The only write to an existing handle is line L5, which by Lemma 3 does not change the partition, so no later answer on any version changes. FIND returns a root of the tree of $x$; two elements share a root exactly when they share a tree, so SAME is correct. $\blacksquare$
