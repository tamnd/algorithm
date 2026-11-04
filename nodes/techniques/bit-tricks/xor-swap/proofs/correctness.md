---
title: The XOR swap exchanges two distinct cells and leaves one cell unchanged
proves: [correctness]
status: full
---

Fix a word size $w \ge 1$ and let $W = \{0,1\}^w$. For $a, b \in W$, $a \oplus b$ is the word whose bit $t$ is $a_t + b_t \bmod 2$, for $0 \le t < w$.

**Lemma (laws of XOR).** For all $a, b, c \in W$: (1) $(a \oplus b) \oplus c = a \oplus (b \oplus c)$; (2) $a \oplus b = b \oplus a$; (3) $a \oplus 0 = a$; (4) $a \oplus a = 0$.

*Proof.* Each law is an equation between two words, so it is enough to check it at each bit position $t$. At position $t$ the operation is addition modulo 2 on $\{0, 1\}$. Addition modulo 2 is associative and commutative, $a_t + 0 = a_t$, and $a_t + a_t = 2a_t \equiv 0 \pmod 2$. $\square$

The laws hold for any reading of the words, signed or unsigned, because they are about bit patterns.

**Theorem.** Let $A$ be a memory of $w$-bit cells. Let $x = A[i]$ and $y = A[j]$ before the call XOR-SWAP$(A, i, j)$. After the call, $A[i] = y$ and $A[j] = x$ when $i \ne j$, $A[i] = x$ when $i = j$, and no other cell changes.

*Proof.* Lines L2 to L4 write only to $A[i]$ and $A[j]$, and line L1 writes nothing, so no other cell changes.

*Case $i = j$.* Line L1 returns before any write, so $A[i] = x$.

*Case $i \ne j$.* Then $A[i]$ and $A[j]$ are different cells, and a write to one does not change the other. We follow the two cells.

1. Line L2 sets $A[i] = x \oplus y$. The cell $A[j]$ still holds $y$.
2. Line L3 sets $A[j] = (x \oplus y) \oplus y$. By (1), this is $x \oplus (y \oplus y)$; by (4), it is $x \oplus 0$; by (3), it is $x$. The cell $A[i]$ still holds $x \oplus y$.
3. Line L4 sets $A[i] = (x \oplus y) \oplus x$. By (2) and (1), this is $y \oplus (x \oplus x)$; by (4) and (3), it is $y$. The cell $A[j]$ still holds $x$.

So $A[i] = y$ and $A[j] = x$. $\square$

**Why line L1 is needed.** Remove line L1 and let $i = j$, with $A[i] = x$. Line L2 sets $A[i] = x \oplus x = 0$ by (4). Line L3 then sets $A[i] = 0 \oplus 0 = 0$, and line L4 does the same. So the cell ends with 0, and the result is wrong for each $x \ne 0$. For $x = 0$ the result happens to be right.

**Termination and cost.** There is no loop. The procedure runs at most one comparison and three XOR assignments, so it stops after a constant number of steps. $\blacksquare$
