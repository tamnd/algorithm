---
title: The persistent trie keeps every version and answers counts and maximum XOR correctly
proves: [correctness]
status: full
---

Fix $w \ge 1$. For a node $t$ and a depth $h$ with $0 \le h \le w$, call $t$ *well formed at depth* $h$ if either $h = w$ and $t.cnt \ge 0$, or $h < w$ and both children are well formed at depth $h + 1$ with $t.cnt = t.child[0].cnt + t.child[1].cnt$. The node $\varnothing$ is well formed at every depth, since its count is 0 and it is its own child. For $t$ well formed at depth $h$ and a string $s$ of $w - h$ bits, write $t[s]$ for the node reached by following $s$, and define the multiset $\text{ms}(t, h)$ in which each $s$ has multiplicity $t[s].cnt$. A version root is well formed at depth 0, and its multiset is read with $s$ the $w$ bits of a key, from bit $w - 1$ down.

**Lemma 1.** If $t$ is well formed at depth $h$, then $t.cnt = |\text{ms}(t, h)|$, the total multiplicity, and for a prefix $q$ of length $j$, $t[q].cnt$ is the number of elements of $\text{ms}(t, h)$ that start with $q$.

*Proof.* By induction on $w - h$, from the additivity of counts at each inner node. $\square$

**Lemma 2 (add).** Let $t$ be well formed at depth 0, $x$ a key, and $d$ an integer with $t[x].cnt + d \ge 0$. Then ADD$(t, x, d)$ returns a root $t'$ that is well formed at depth 0 with $\text{ms}(t') = \text{ms}(t)$ changed by $d$ copies of $x$. It makes exactly $w + 1$ nodes and writes only to nodes it made.

*Proof.* Let $t_0 = t, t_1, \ldots, t_w$ be the old nodes on the path of $x$, and $c_0, \ldots, c_w$ the new nodes made in lines L1 and L5, so $c_h$ starts with the children and the count of $t_h$, plus $d$. Line L6 sets $c_{h}.child[b_h] = c_{h+1}$, where $b_h$ is the bit used at depth $h$, and this is the only write. After the loop, $c_h$ has the child $c_{h+1}$ on the path side and the old child $t_h.child[1 - b_h]$ on the other side. By induction from $h = w$ up: $c_w$ is a leaf with count $t_w.cnt + d \ge 0$. For $h < w$, $c_h.cnt = t_h.cnt + d = t_h.child[b_h].cnt + t_h.child[1-b_h].cnt + d = c_{h+1}.cnt + t_h.child[1 - b_h].cnt$, so $c_h$ is well formed. A string $s$ that leaves the path at depth $h$ reaches the same node through $c_h$ as through $t_h$, so its multiplicity is unchanged; the string $x$ reaches $c_w$, whose count is the old one plus $d$. The nodes $c_h$ are made by this call, so no other version reaches them while they are written. $\square$

**Lemma 3 (no change).** After an operation returns, no node reachable from an existing root is written again.

*Proof.* By Lemma 2, ADD writes only to nodes that it made and that no root reached before it returned. COUNT and MAX-XOR do not write. $\square$

**Theorem 1.** After any sequence of operations, every version root is well formed at depth 0, and its multiset is the one that the abstract type gives to the version. COUNT returns the multiplicity of $x$ and REMOVE never makes a negative count.

*Proof.* By induction on the operations. Version 0 is $\varnothing$, which is well formed with the empty multiset. `insert` is ADD with $d = 1$, right by Lemma 2. REMOVE calls ADD with $d = -1$ only if COUNT is positive (line L9), so the precondition of Lemma 2 holds, and otherwise returns the old root, whose multiset has no $x$ to remove. COUNT follows the path of $x$ to its leaf and returns its count, the multiplicity by definition. By Lemma 3 no earlier version changes. $\square$

**Theorem 2 (maximum XOR).** Let $u$ and $v$ be version roots with $\text{ms}(v) \supseteq \text{ms}(u)$ as multisets, let $D = \text{ms}(v) - \text{ms}(u)$ be non-empty, and let $y$ be a key. Then MAX-XOR$(u, v, y)$ returns $\max_{x \in D} x \oplus y$.

*Proof.* By Lemma 1, for each prefix $q$, $v[q].cnt - u[q].cnt$ is the number of elements of $D$ that start with $q$. We claim that before the step for bit $i$, the nodes $u$ and $v$ are $u[q]$ and $v[q]$ for a prefix $q$ of length $w - 1 - i$ such that some element of $D$ starts with $q$, and $r$ is the value of the top $w - 1 - i$ bits of $q \oplus y$ (as a number), which equal the top bits of the optimum $M = \max_{x \in D} x \oplus y$. At the start $q$ is empty, $D$ is non-empty by line L12, and $r = 0$. In a step, let $b$ be bit $i$ of $y$. If some element of $D$ starts with $q(1 - b)$ (line L15), then such an $x$ has bit $i$ of $x \oplus y$ equal to 1, while all elements that start with $q$ agree with $M$ on the higher bits; since $2^i > \sum_{j < i} 2^j$, every optimum starts with $q(1 - b)$, so bit $i$ of $M$ is 1, and the step keeps the claim. Otherwise every element of $D$ that starts with $q$ continues with $b$, so bit $i$ of $M$ is 0, and line L16 keeps the claim. After the step for bit 0, $q$ has length $w$ and $r$ is $M$. $\blacksquare$
