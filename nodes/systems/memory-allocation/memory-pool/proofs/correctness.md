---
title: A memory pool never hands out a live block and fails only when all blocks are live
proves: [correctness, termination]
status: full
---

**Setting.** The pool has $n$ blocks with addresses $0, b, 2b, \ldots, (n - 1) b$. The program calls POOL-ALLOC and POOL-FREE, and it calls POOL-FREE$(p)$ only for a block $p$ that it holds: a block that an earlier POOL-ALLOC returned and that it has not freed since. Let $V$ be the set of *live* blocks, the blocks that the program holds. Let $\Lambda$ be the sequence of addresses $p_1 = $ HEAD, $p_2 = $ MEM$[p_1]$, and so on, up to the first NIL. Let $R = \{ i b : \text{FRESH} \le i < n \}$ be the *fresh* blocks.

**Invariant (I).**

1. $\Lambda$ is finite, and its addresses are distinct;
2. the set of addresses of $\Lambda$, the set $V$ and the set $R$ are pairwise disjoint, and their union is the set of all $n$ blocks;
3. $0 \le \text{FRESH} \le n$.

**Lemma 1.** (I) holds after the creation of the pool.

*Proof.* HEAD = NIL, so $\Lambda$ is empty. $V$ is empty. FRESH = 0, so $R$ holds all $n$ blocks. $\square$

**Lemma 2.** If (I) holds before POOL-ALLOC, then (I) holds after it, and a returned address was not in $V$ before the call.

*Proof.* *Case L1*, HEAD $\ne$ NIL. Then $p = p_1$, the first element of $\Lambda$, and HEAD becomes MEM$[p_1] = p_2$, or NIL if $\Lambda$ had one element. So the new list is $p_2, p_3, \ldots$, which is finite and has distinct addresses. The block $p_1$ leaves the list and joins $V$. By (I.2), $p_1$ was not in $V$ or $R$ before, so the three sets stay disjoint, and their union does not change. No word of MEM changes, so the links of the other listed blocks are intact.

*Case L2*, HEAD = NIL and FRESH $< n$. Then $p = \text{FRESH} \cdot b$ is in $R$, and the step FRESH $\leftarrow$ FRESH + 1 removes exactly $p$ from $R$. The block joins $V$. By (I.2) it was not in $V$, and the list did not change. FRESH stays at most $n$.

*Case L3*, HEAD = NIL and FRESH = $n$. Nothing changes. $\square$

**Lemma 3.** If (I) holds before POOL-FREE$(p)$ with $p \in V$, then (I) holds after it.

*Proof.* Line L4 writes HEAD into MEM$[p]$, and line L5 sets HEAD to $p$. The block $p$ is live, so by (I.2) it is not on the list. So the write of line L4 does not change the link of any listed block, and the new list is $p, p_1, p_2, \ldots$. It is finite, and its addresses are distinct because $p$ was not among $p_1, p_2, \ldots$. The block $p$ moves from $V$ to the list, so (I.2) holds. $\square$

**Theorem.** If the program frees only blocks that it holds, then:

1. POOL-ALLOC never returns a block that the program holds, so two live blocks never share a word;
2. POOL-ALLOC returns FAIL exactly when all $n$ blocks are live;
3. each call ends after a constant number of steps.

*Proof.* By Lemmas 1, 2 and 3 and induction on the number of calls, (I) holds before each call. (1) is Lemma 2. Distinct block addresses are multiples of $b$ that differ by at least $b$, so their blocks do not overlap. (2): POOL-ALLOC fails exactly when HEAD = NIL and FRESH = $n$, that is, when the list and $R$ are both empty. By (I.2) this happens exactly when $V$ holds all $n$ blocks. (3): no line has a loop. $\blacksquare$

**Remark (double free).** If the program calls POOL-FREE$(p)$ for a block that is already on the list, line L4 overwrites the link of a listed block. If $p = p_1$, the list becomes the cycle $p, p, p, \ldots$, and every later POOL-ALLOC returns $p$ again. So the precondition $p \in V$ is necessary.
