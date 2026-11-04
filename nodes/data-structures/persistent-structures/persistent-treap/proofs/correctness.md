---
title: The persistent treap keeps every version, and each version is a random treap
proves: [correctness]
status: full
---

A *treap* on a finite set $S$ of keys with priorities $p(k)$ is a binary tree whose nodes hold the keys of $S$, once each, in search-tree order (I1) and in heap order on priorities (I2). For a node $t$ write $\text{keys}(t)$ for the set of keys in its subtree, with $\text{keys}(\text{nil}) = \emptyset$. A tree whose size fields satisfy (I3) is called *sized*.

**Lemma 1 (no change).** No procedure writes a field of an existing node. Hence $\text{keys}(t)$ and the shape below $t$ never change once $t$ is made.

*Proof.* The procedures make nodes only by COPY and NEW-NODE, which write the fields of a node that did not exist before, and set the size from the children at that moment. CONTAINS only reads. $\square$

**Lemma 2 (split).** If $t$ is a sized treap, then SPLIT$(t, k)$ returns sized treaps $a$ and $b$ with $\text{keys}(a) = \{x \in \text{keys}(t) : x < k\}$ and $\text{keys}(b) = \{x \in \text{keys}(t) : x \ge k\}$, and every priority of $a$ or $b$ is the priority of the same key in $t$.

*Proof.* By induction on the size of $t$. For nil, line L1 is right. If $t.key < k$ (line L2), then all of $t.left$ and $t.key$ belong to the part below $k$, and by induction SPLIT$(t.right, k)$ splits the right subtree into $a$ and $b$. The copy of $t$ with right child $a$ has $t.key$ above all keys of $t.left$ and below all keys of $a \subseteq \text{keys}(t.right)$, so it is in search order; its priority $t.prio$ is at least each priority in $t.left$ and in $a$, because those are priorities of the subtree of $t$; so it is in heap order. Its size is set from its children. The tree $b$ is a treap by induction, and its keys are those of $t.right$ at least $k$, which are all the keys of $t$ at least $k$. Line L3 is the mirror case. $\square$

**Lemma 3 (merge).** If $a$ and $b$ are sized treaps with every key of $a$ less than every key of $b$, then MERGE$(a, b)$ returns a sized treap on $\text{keys}(a) \cup \text{keys}(b)$ with the same priorities.

*Proof.* By induction on $|a| + |b|$. Lines L4 and L5 are clear. If $a.prio > b.prio$ (line L6), then $a.prio$ is the highest priority of both trees, so $a.key$ may be the root. By induction MERGE$(a.right, b)$ is a treap on the keys of $a.right$ and $b$, all of which are above $a.key$, and with priorities at most $a.prio$. So the copy of $a$ with this right child is a treap. Line L7 is the mirror case, using $b.prio \ge a.prio$. $\square$

**Lemma 4 (insert).** If $t$ is a sized treap and $k \notin \text{keys}(t)$, then INS$(t, k, p)$ returns a sized treap on $\text{keys}(t) \cup \{k\}$, in which $k$ has priority $p$ and every other key has its old priority.

*Proof.* By induction on the size of $t$. In line L10, either $t$ is nil, or $p > t.prio$, so $p$ is higher than every priority of $t$ by heap order. By Lemma 2, SPLIT gives treaps $a$ and $b$ on the keys below and above $k$, and the new node with key $k$, priority $p$ and children $a$ and $b$ is in search order and heap order. Otherwise $t.prio \ge p$, and $k$ goes to the side given by the search order (lines L11 and L12). By induction the new subtree is a treap on the old keys of that side plus $k$, with priorities at most $t.prio$ (the old ones, and $p \le t.prio$). So the copy of $t$ with this child is a treap. $\square$

**Lemma 5 (delete).** If $t$ is a sized treap and $k \in \text{keys}(t)$, then DEL$(t, k)$ returns a sized treap on $\text{keys}(t) \setminus \{k\}$ with the old priorities.

*Proof.* By induction on the size of $t$. If $k = t.key$, line L17 merges $t.left$ and $t.right$, whose keys are separated by $k$; Lemma 3 applies. Otherwise $k$ lies in the subtree on the side chosen by line L15 or L16, which by induction is replaced by a treap on its keys minus $k$, with priorities at most $t.prio$; the copy of $t$ is a treap. $\square$

**Theorem 1 (persistence and correctness).** After any sequence of operations, every version is a sized treap on the set that the abstract ordered set gives to it, and every query returns the abstract answer on its version.

*Proof.* By induction on the operations. The empty set is nil. INSERT returns $t$ unchanged when $k$ is present (line L8) and otherwise is right by Lemma 4. DELETE returns $t$ when $k$ is absent (line L13) and otherwise is right by Lemma 5. `split` and `merge` are right by Lemmas 2 and 3; `merge` checks its precondition. CONTAINS follows the search order, so by (I1) it finds $k$ if and only if $k$ is present. By Lemma 1 the earlier versions do not change. $\square$

**Theorem 2 (shape of a version).** Suppose the sequence of operations, and the keys they use, is fixed in advance and does not depend on the priorities, and the priorities of new keys are independent and uniform on $[0, 1)$. Then for each version with key set $S$, the priorities of the keys of $S$ are independent and uniform, and the tree of the version is the unique treap on $S$ with these priorities. Hence the expected depth of the key of rank $i$ in a version of $n$ keys is $H_i + H_{n-i+1} - 1$.

*Proof.* A key in a version got its priority when it was inserted on the path of the version tree that leads to this version, and each priority is copied with its key and never changed (Lemmas 2 to 5 keep old priorities). Distinct keys of $S$ got their priorities in distinct calls of INSERT, so the priorities of $S$ are independent and uniform. With probability 1 they are distinct. A treap on a set with distinct priorities is unique: the key with the highest priority must be the root, and the two sides are treaps on the keys below and above it, unique by induction. So the version is the treap on $S$ with random priorities, which has the same distribution as an ephemeral treap on $S$, and the depth formula of Seidel and Aragon holds. $\blacksquare$
