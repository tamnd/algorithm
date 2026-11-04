---
title: The persistent stack meets the stack laws and never changes an old version
proves: [correctness]
status: full
---

Write $\text{seq}(s)$ for the sequence of items of the stack $s$, from the top down: $\text{seq}(\text{nil}) = \langle \rangle$, and $\text{seq}(s) = \langle s.item \rangle \cdot \text{seq}(s.next)$ for a node $s$. Write $|s|$ for the length of $\text{seq}(s)$.

**Lemma 1 (the invariant holds).** At each moment, every node satisfies (I1) its fields have not changed since it was made, (I2) $s.size = 1 + |s.next|$ where $|\text{nil}| = 0$, and (I3) the chain $s, s.next, s.next.next, \ldots$ reaches nil.

*Proof.* By induction on the number of operations done. Before the first operation there is no node. POP, TOP, IS-EMPTY and SIZE write no field and make no node, so they keep all three statements. PUSH$(s, x)$ at line L1 makes one node $r$ with $r.item = x$, $r.next = s$ and $r.size = 1 + \text{SIZE}(s)$, and writes no other field, so (I1) holds for the old nodes. The chain from $r$ is $r$ followed by the chain from $s$, which reaches nil by the hypothesis, so (I3) holds for $r$. SIZE$(s)$ returns $s.size$, which is $|s|$ by (I2) and (I3) for $s$ (induction along the finite chain), or 0 for nil. So $r.size = 1 + |s| = 1 + |r.next|$, which is (I2) for $r$. $\square$

By (I3), $\text{seq}(s)$ is a finite sequence for each stack $s$, and by (I1), $\text{seq}(s)$ depends only on fields that never change.

**Lemma 2 (old versions are unchanged).** If a stack value $v$ exists at some moment, then $\text{seq}(v)$ is the same at every later moment.

*Proof.* $\text{seq}(v)$ is determined by the fields $item$ and $next$ of the nodes on the chain from $v$, and by Lemma 1 no field of an existing node changes. A node made later is not on this chain, because the chain consists of nodes that existed when $v$ existed, and $next$ fields do not change. $\square$

**Theorem (the stack laws).** For each stack $s$ and item $x$:

1. PUSH$(s, x)$ returns a stack $r$ with $\text{seq}(r) = \langle x \rangle \cdot \text{seq}(s)$, and $\text{seq}(s)$ is unchanged.
2. If $s \ne \text{nil}$ and $\text{seq}(s) = \langle y \rangle \cdot w$, then POP$(s)$ returns $(y, t)$ with $\text{seq}(t) = w$, and TOP$(s)$ returns $y$.
3. If $s = \text{nil}$, POP$(s)$ and TOP$(s)$ report underflow.
4. IS-EMPTY$(s)$ is true exactly when $\text{seq}(s) = \langle \rangle$, and SIZE$(s) = |s|$.

*Proof.* (1) Line L1 makes $r$ with $r.item = x$ and $r.next = s$, so $\text{seq}(r) = \langle x \rangle \cdot \text{seq}(s)$ by the definition of seq. Lemma 2 gives that $\text{seq}(s)$ is unchanged. (2) If $s \ne \text{nil}$, line L2 does not stop, and line L3 returns $s.item = y$ and $t = s.next$, with $\text{seq}(t) = w$ by the definition of seq. Lines L4 and L5 return $s.item = y$ in the same way. (3) Lines L2 and L4 test exactly $s = \text{nil}$. (4) $\text{seq}(s) = \langle \rangle$ exactly when $s = \text{nil}$, because a node contributes its item. SIZE returns $|s|$ by (I2) and (I3), as in the proof of Lemma 1. $\square$

**Corollary (full persistence).** Let $v_0, v_1, \ldots, v_m$ be the versions made by any sequence of operations, where each update takes any earlier version as input. Then at the end, $\text{seq}(v_i)$ is the sequence that the stack laws give for the chain of updates that made $v_i$ from the empty stack.

*Proof.* By induction on $i$. The version $v_0$ is nil. The version $v_i$ was made by PUSH or POP from some $v_j$ with $j < i$. At that moment, $\text{seq}(v_j)$ was, by the hypothesis, the right sequence, so by the theorem $\text{seq}(v_i)$ was the right sequence for $v_i$. By Lemma 2 it is still the same at the end. $\blacksquare$

**Append.** Lines A1 to A4 push the items of $s$ onto $t$ from the bottom item of $s$ up to the top item. By part 1 of the theorem and induction on the number of pushes, after the pushes of the bottom $j$ items of $s$ the sequence of $r$ is those $j$ items, in the order they have in $s$, followed by $\text{seq}(t)$. With $j = k$ this is $\text{seq}(s) \cdot \text{seq}(t)$. Each push makes one node, so APPEND makes $k$ nodes.
