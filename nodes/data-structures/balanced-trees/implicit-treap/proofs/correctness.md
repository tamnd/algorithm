---
title: Split and merge on positions keep the represented sequence
proves: [correctness]
status: full
---

Write $s \cdot s'$ for the concatenation of sequences, $\overline{s}$ for the reverse of $s$, and $|s|$ for the length. The sequence that a subtree $t$ *represents* is defined, with the lazy flag, by

$$\text{seq}(\text{nil}) = \langle\rangle, \qquad \text{seq}(t) = \begin{cases} \text{seq}(t.left) \cdot \langle t.value \rangle \cdot \text{seq}(t.right) & \text{if } t.rev = \text{false},\\ \overline{\text{seq}(t.left) \cdot \langle t.value \rangle \cdot \text{seq}(t.right)} & \text{if } t.rev = \text{true}. \end{cases}$$

So toggling the flag of $t$ replaces $\text{seq}(t)$ by its reverse, because $\overline{\overline{s}} = s$. A subtree is *valid* when:

1. (H) each node has a priority at least as large as the priorities of its children;
2. (S) each node $t$ has $t.size = |\text{seq}(t)|$ and $t.total$ equal to the sum of the items of $\text{seq}(t)$.

Reversal does not change the length or the sum of a sequence, so (S) can be checked without regard to the flags: $|\text{seq}(t)| = |\text{seq}(t.left)| + 1 + |\text{seq}(t.right)|$ in both cases, and the same for the sum. That is what UPDATE computes.

**Lemma 1 (PUSH).** If $t$ is valid, then after PUSH$(t)$ the subtree is valid, $\text{seq}(t)$ is the same, and $t.rev$ is false.

*Proof.* If $t.rev$ is false, nothing changes. Otherwise let $l$, $r$ be the children and $v$ the value. Before, $\text{seq}(t) = \overline{\text{seq}(l) \cdot \langle v \rangle \cdot \text{seq}(r)} = \overline{\text{seq}(r)} \cdot \langle v \rangle \cdot \overline{\text{seq}(l)}$. PUSH makes $r$ the left child and $l$ the right child, toggles both of their flags, which makes their sequences $\overline{\text{seq}(r)}$ and $\overline{\text{seq}(l)}$, and clears $t.rev$. So the new $\text{seq}(t)$ is the same. Each node has the same children as a set, so (H) holds, and no length or sum changes, so (S) holds. $\square$

**Lemma 2 (SPLIT).** Let $t$ be valid and $i \ge 0$. SPLIT$(t, i)$ returns valid subtrees $A$ and $B$, made of the nodes of $t$, with $\text{seq}(A)$ the first $\min(i, |\text{seq}(t)|)$ items of $\text{seq}(t)$ and $\text{seq}(B)$ the rest.

*Proof.* By induction on the size of $t$. If $t$ is nil, line L1 returns two empty trees. Otherwise, by Lemma 1, after line L2, $\text{seq}(t) = \text{seq}(l) \cdot \langle v \rangle \cdot \text{seq}(r)$ with $l$, $r$ the children, and $t.rev$ is false. Let $s = |\text{seq}(l)| = size(l)$.

If $s < i$ (line L3), the first $i$ items are all of $\text{seq}(l)$, then $v$, then the first $i - s - 1$ items of $\text{seq}(r)$. By the induction hypothesis the call on $r$ returns $A'$ with those $i - s - 1$ items and $B'$ with the rest. Setting $t.right = A'$ gives $\text{seq}(t) = \text{seq}(l) \cdot \langle v \rangle \cdot \text{seq}(A')$, which is the first part, and $B'$ is the rest. The nodes of $A'$ come from $r$, so their priorities are at most that of $t$, and (H) holds at $t$; UPDATE makes (S) hold at $t$.

If $i \le s$ (line L4), the first $i$ items all lie in $\text{seq}(l)$, and the case is the mirror image, with $t.left = B'$. $\square$

**Lemma 3 (MERGE).** Let $a$ and $b$ be valid, with disjoint nodes. MERGE$(a, b)$ returns a valid subtree, made of the nodes of $a$ and $b$, with sequence $\text{seq}(a) \cdot \text{seq}(b)$.

*Proof.* By induction on the total size. If one of them is nil, line L5 returns the other. Let $a.prio > b.prio$ (line L6). After PUSH$(a)$, $\text{seq}(a) = \text{seq}(a.left) \cdot \langle a.value \rangle \cdot \text{seq}(a.right)$. By the induction hypothesis, MERGE$(a.right, b)$ is valid with sequence $\text{seq}(a.right) \cdot \text{seq}(b)$, so the new $\text{seq}(a)$ is $\text{seq}(a) \cdot \text{seq}(b)$ for the old $a$. The root of the merged subtree is a node of $a.right$ or of $b$. The first have priority at most $a.prio$ by (H) in $a$, and the second at most $b.prio < a.prio$ by (H) in $b$. So (H) holds at $a$, and UPDATE gives (S). The case $a.prio \le b.prio$ (line L7) is the mirror image, with $b$ as the root. $\square$

**The operations.** Let the whole tree be valid and represent the list $L$.

- INSERT$(i, x)$ (line L8): by Lemma 2 the split gives $L[0..i)$ and $L[i..n)$, and a new node is a valid tree for $\langle x \rangle$. By Lemma 3 the two merges give $L[0..i) \cdot \langle x \rangle \cdot L[i..n)$.
- DELETE$(i)$ (line L9): the two splits give $L[0..i)$, the one-node tree $M$ for $\langle L[i] \rangle$ and $L[i+1..n)$. The merge gives the list without $L[i]$, and the value of $M$ is returned.
- REVERSE$(lo, hi)$ (lines L10 and L11): the splits give $L[0..lo)$, $M$ for $L[lo..hi)$ and $L[hi..n)$. Toggling the flag of $M$ makes $\text{seq}(M)$ the reverse of $L[lo..hi)$; it changes no priority, length or sum, so $M$ stays valid. The merges give the list with that range reversed.
- RANGE-SUM$(lo, hi)$ (line L12): the same splits give $M$ for $L[lo..hi)$, and by (S) its total is the sum asked for. Merging back restores the tree for $L$.
- GET$(i)$: at each node, after PUSH, $\text{seq}(t) = \text{seq}(l) \cdot \langle v \rangle \cdot \text{seq}(r)$, so the item of index $i$ is in $l$ when $i < size(l)$, is $v$ when $i = size(l)$, and is item $i - size(l) - 1$ of $\text{seq}(r)$ otherwise.

**Theorem.** Starting from the empty list, after any sequence of operations the tree is valid, represents the list that the same operations give on a plain array, and every query returns the right answer.

*Proof.* The empty tree is valid and represents the empty list, and each operation keeps this by the cases above. $\blacksquare$
