---
title: The weak-heap operations keep weak-heap order
proves: [correctness]
status: full
---

The array $a[0..n-1]$ with bits $r[0..n-1]$ and $r[0] = 0$ defines a tree: the left child of $i$ is $2i + r[i]$ and the right child is $2i + 1 - r[i]$, where they exist, and node 0 has only the child 1. For a node $x$, $T(x)$ is the set of nodes of the subtree of $x$, and $L(x)$ and $R(x)$ are the sets of nodes of its left and right subtrees. Flipping $r[x]$ exchanges $L(x)$ and $R(x)$ and changes no other subtree as a set. Write $C(x)$ for the condition $a[x] \le a[y]$ for all $y \in R(x)$. The heap is in *weak-heap order* if $C(x)$ holds for every node $x$. A set $S$ of nodes is *ordered* if $C(x)$ holds for every $x \in S$. For a set $S$, write $a[i] \le S$ if $a[i] \le a[y]$ for every $y \in S$.

**Lemma 1 (distinguished ancestors).** For $j > 0$, let $d(j)$ be the value of D-ANCESTOR$(j)$. Then $j \in R(d(j))$, and for every node $x$, $j \in R(x)$ if and only if $x$ is one of $d(j), d(d(j)), \ldots$. If $j$ has a left child $y$, then $d(y) = d(j)$.

*Proof.* Line L1 goes up while the current node $c$ is a left child: $c$ is the left child of its parent exactly when $c \bmod 2 = r[\lfloor c/2 \rfloor]$. It stops at a node $c$ that is a right child, and $d(j)$ is its parent, so $j \in T(c) = R(d(j))$. Every ancestor $z$ of $j$ strictly between $d(j)$ and $j$ is on the walk, so $j$ is in $L(z)$, not in $R(z)$. So $d(j)$ is the lowest ancestor $x$ with $j \in R(x)$. If $j \in R(x)$ and $x \ne d(j)$, then $x$ is a proper ancestor of $d(j)$ and $d(j) \in R(x)$, and the claim follows by induction on depth. The converse holds because $R(d(z)) \supseteq T(z) \ni j$ for each $z$ on the chain. For the left child $y$ of $j$, the walk from $y$ first goes up to $j$, and then continues as the walk from $j$. $\square$

**Lemma 2 (join).** Let $i = d(j)$. Before JOIN$(i, j)$, assume that $T(j)$ is ordered and $a[i] \le L(j)$. After the join, $T(j)$ is ordered and $a[i] \le T(j)$. The join changes only $a[i]$, $a[j]$ and $r[j]$, and it does not increase $a[i]$.

*Proof.* If $a[j] \ge a[i]$, nothing changes, and $a[i] \le a[j] \le R(j)$ by $C(j)$, so $a[i] \le T(j)$.

Otherwise line L4 swaps the keys and flips $r[j]$. Let $u$ and $v$ be the old $a[i]$ and $a[j]$, with $v < u$. The new $a[i] = v$ is less than $u \le L(j)$, it is at most every key of the old $R(j)$ by the old $C(j)$, and it is less than the new $a[j] = u$. So the new $a[i] \le T(j)$. The new right subtree of $j$ is the old $L(j)$, and the new $a[j] = u \le$ the old $L(j)$, so $C(j)$ holds. For $x \in T(j)$ with $x \ne j$, the set $R(x)$ and its keys did not change, because $i \notin T(j)$, so $C(x)$ still holds. $\square$

**Theorem 1 (build).** After lines L5 and L6, the heap is in weak-heap order, with exactly $n - 1$ comparisons.

*Proof.* A join at $j$ changes only $a[d(j)]$, $a[j]$ and $r[j]$, and $d(j) < j$. So once $j$ has been processed, no later step (which has a smaller index) changes a key or a bit in $T(j)$: every node of $T(j)$ has an index at least $j$, and the later steps change only nodes with smaller indices. We prove by induction downward on $j$: when $j$ is processed, $T(j)$ is ordered and $a[d(j)] \le L(j)$.

$T(j)$ is ordered: for every $x \in T(j)$ with $x \ne j$, the step at $x$ came earlier and left $T(x)$ ordered by Lemma 2, and $T(x)$ has not changed since. For $C(j)$: if $j$ has a right child $z$, then $d(z) = j$ by Lemma 1, so the step at $z$ gave $a[j] \le T(z) = R(j)$. After it, $T(z)$ did not change, and $a[j]$ changed only at steps $(j, z')$ for other $z' > j$, which do not increase it.

$a[d(j)] \le L(j)$: if $j$ has a left child $y$, then $d(y) = d(j)$ by Lemma 1, and the step at $y$ gave $a[d(j)] \le T(y) = L(j)$. Since then, $T(y)$ has not changed, and $a[d(j)]$ changed only as the first argument of joins, which do not increase it, because $d(j) < j$ and $d(j)$ is processed after $j$.

So Lemma 2 applies at every step. After the step at $j = 1$, $T(1)$ is ordered and $a[0] \le T(1) = R(0)$, so $C(0)$ also holds. Each of the $n - 1$ steps makes one comparison. $\square$

**Theorem 2 (sift-down).** Assume $C(x)$ holds for every $x \ne 0$ among the nodes $0, \ldots, m - 1$, with $m \ge 2$. After SIFT-DOWN$(m)$, the heap is in weak-heap order.

*Proof.* Line L8 finds the path $s_1 = 1, s_2, \ldots, s_k$, where $s_{t+1}$ is the left child of $s_t$ and $s_k$ has no left child. By Lemma 1, $d(s_t) = 0$ for every $t$. Lines L9 and L10 call JOIN$(0, s_k)$, then JOIN$(0, s_{k-1})$, up to JOIN$(0, s_1)$, because $\lfloor s_{t+1}/2 \rfloor = s_t$. We show by induction, for $t = k$ down to 1, that after JOIN$(0, s_t)$ the set $T(s_t)$ is ordered and $a[0] \le T(s_t)$.

For $t = k$: $T(s_k)$ is ordered by assumption, and $L(s_k)$ is empty, so Lemma 2 applies. For $t < k$: the earlier joins changed only $a[0]$ and nodes in $T(s_{t+1})$, and the bits there. So $C(s_t)$ still holds, because $R(s_t)$ and $a[s_t]$ have not changed, and the nodes of $R(s_t)$ are still ordered. With the induction hypothesis, $T(s_t) = \{s_t\} \cup R(s_t) \cup T(s_{t+1})$ is ordered, and $L(s_t) = T(s_{t+1})$, so $a[0] \le L(s_t)$. Lemma 2 applies again.

At the end, $T(1)$ is ordered and $a[0] \le T(1) = R(0)$, so every node satisfies $C$. $\square$

**Theorem 3 (delete-min).** DELETE-MIN returns a smallest key, and the remaining heap of $n - 1$ keys is in weak-heap order.

*Proof.* The root is a smallest key, because $R(0)$ holds all other nodes. Removing the last node, a leaf, removes one element from some sets $R(x)$ and keeps every $C(x)$. Moving its key to the root changes no $C(x)$ for $x \ne 0$, because node 0 is in no $R(x)$. With at least two nodes left, Theorem 2 gives the result; with one node, there is nothing to check. $\square$

**Theorem 4 (insert).** After INSERT$(k)$, the heap is in weak-heap order and holds the old keys and $k$.

*Proof.* Line L13 puts $k$ in the new leaf $j = n$. If $j$ is even, $j$ is the first child of its parent $p$, which was a leaf, so setting $r[p] = 0$ changes no subtree of the old tree and makes $j$ the left child of $p$.

We show that the loop keeps this invariant $I(j)$: for every node $x$ and every $y \in R(x)$ with $y \ne j$, $a[x] \le a[y]$. In words, the only possible violations are between $j$ and the nodes $x$ with $j \in R(x)$. After line L13, $I(j)$ holds, because the old heap was in weak-heap order and the new leaf has $R(j) = \emptyset$.

Let $i = d(j)$, and assume $I(j)$. If JOIN$(i, j)$ does not swap, then $a[i] \le a[j]$. By Lemma 1, every other $x$ with $j \in R(x)$ has $i \in R(x)$, so $a[x] \le a[i] \le a[j]$ by $I(j)$. Every $C(x)$ holds, and the loop stops.

If the join swaps, let $u$ and $v$ be the old $a[i]$ and $a[j]$, with $v < u$. We check $I(i)$.
- $x = j$: the new $R(j)$ is the old $L(j)$, which is part of $R(i)$ and does not contain $j$, so $u \le$ the old $L(j)$ by $I(j)$.
- $x = i$: $R(i)$ is the same set. Its keys other than $a[j]$ did not change and are at least $u > v$. The new $a[j] = u > v$.
- $x \in T(j)$, $x \ne j$: $R(x)$ and its keys did not change, and $j \notin R(x)$.
- $x$ with $i \in R(x)$: these $x$ are proper ancestors of $i$, so $j \in R(x)$ as well. The pair $(x, i)$ is the exception allowed by $I(i)$. For $y = j$, the new key is $u$, and $a[x] \le u$ held before, because $i \ne j$ and $i \in R(x)$.
- Every other $x$: if $R(x)$ meets $T(j)$, then $R(x) \supseteq T(j) \ni j$, and by Lemma 1 $x = i$ or $i \in R(x)$, which are the cases above. Otherwise $R(x)$ contains neither $i$ nor $j$ and did not change.

So $I(i)$ holds, and the loop continues with $j \leftarrow i$. Each step moves to a proper ancestor, so the loop ends: either at a join without a swap, which gives weak-heap order as shown, or with $j = 0$. Node 0 is in no $R(x)$, so $I(0)$ is the weak-heap order itself. Joins only exchange keys, so the multiset of keys is the old keys and $k$. $\blacksquare$
