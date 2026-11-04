---
title: Quadratic probing with triangular offsets finds each key and each free slot
proves: [correctness, termination]
status: full
---

Let $m = 2^p$ with $p \ge 0$. For a key $k$ and $i \ge 0$, write $p_i(k) = (h(k) + i(i+1)/2) \bmod m$. A slot is *full* when it holds a key, and *free* when it is EMPTY or DELETED.

**Lemma 1 (coverage).** The values $i(i+1)/2 \bmod m$ for $i = 0, 1, \ldots, m-1$ are pairwise different. So for each key $k$, the slots $p_0(k), \ldots, p_{m-1}(k)$ are the $m$ slots of the table, each one exactly once.

*Proof.* For $m = 1$ there is one value. Let $m \ge 2$ and assume that $0 \le i < j \le m-1$ and $i(i+1)/2 \equiv j(j+1)/2 \pmod{2^p}$. Then $2^p$ divides $\frac{j(j+1) - i(i+1)}{2} = \frac{(j-i)(j+i+1)}{2}$, so $2^{p+1}$ divides $(j-i)(j+i+1)$. The sum of the two factors is $2j + 1$, which is odd, so one factor is odd. An odd factor has no factor 2, so $2^{p+1}$ divides the other factor. But $0 < j - i \le m - 1 < 2^{p+1}$ and $0 < j + i + 1 \le (m-1) + (m-2) + 1 = 2^{p+1} - 2 < 2^{p+1}$. A positive integer less than $2^{p+1}$ is not a multiple of $2^{p+1}$. This is a contradiction. So the $m$ values are different, and as they lie in $\{0, \ldots, m-1\}$, they are all of its values. Adding $h(k)$ modulo $m$ is a bijection of $\{0, \ldots, m-1\}$, which gives the second claim. $\square$

**Lemma 2 (the variable $j$).** In QP-SEARCH and QP-INSERT, at the start of the iteration with counter $i$, $j = p_i(k)$.

*Proof.* By induction on $i$. For $i = 0$, line L1 or L7 sets $j = h(k) = p_0(k)$. If $j = p_i(k)$ at the start of iteration $i$ and the iteration does not return, line L5 or L10 sets $j$ to $(p_i(k) + i + 1) \bmod m = (h(k) + i(i+1)/2 + i + 1) \bmod m = (h(k) + (i+1)(i+2)/2) \bmod m = p_{i+1}(k)$. $\square$

**The invariant.** Consider a table built from an EMPTY table by calls of QP-INSERT (each with its precondition) and QP-DELETE.

> **(Q)** No key occurs in two slots. For each key $k$ in the table there is a $t$ with $0 \le t \le m-1$ such that $T[p_t(k)] = k$ and none of the slots $p_0(k), \ldots, p_{t-1}(k)$ is EMPTY.

**Lemma 3.** QP-SEARCH$(T, k)$ returns the slot of $k$ if $k$ is in $T$, and NIL otherwise, when (Q) holds. It does not change $T$.

*Proof.* QP-SEARCH writes nothing. It returns a slot $j$ only at line L4, where $T[j] = k$, so a returned slot holds $k$. If $k$ is not in $T$, no slot passes the test of line L4, so the result is NIL (line L3 or L6).

Let $k$ be in $T$, with $t$ as in (Q). By Lemma 2, iteration $i$ looks at $p_i(k)$. For $i < t$, the slot $p_i(k)$ is not EMPTY by (Q), so line L3 does not return. It does not hold $k$: by Lemma 1, $p_i(k) \ne p_t(k)$, and by (Q) $k$ is only at $p_t(k)$. So line L4 does not return either. In iteration $t \le m-1$ the slot $p_t(k)$ holds $k$, which is not EMPTY, and line L4 returns it. $\square$

**Lemma 4.** If $k$ is not in $T$ and (Q) holds, QP-INSERT$(T, k)$ either raises "the table is full", and then every slot is full and $T$ is not changed, or it writes $k$ into one free slot, and then (Q) holds again.

*Proof.* By Lemma 2, iteration $i$ tests slot $p_i(k)$, and by Lemma 1 the $m$ iterations test every slot once. If no slot is free, line L9 never writes and line L11 raises the error. Otherwise let $t$ be the first iteration at which $p_t(k)$ is free. Line L9 writes $k$ there. The slots $p_0(k), \ldots, p_{t-1}(k)$ were full at line L9, and they stay full, so none of them is EMPTY: (Q) holds for $k$. As $k$ was not in $T$, it now occurs once. For another key $k'$, its slot is not changed, because line L9 writes only to a free slot. The write turns one free slot into a full one, so the set of EMPTY slots does not grow, and (Q) stays true for $k'$. $\square$

**Lemma 5.** If (Q) holds, QP-DELETE$(T, k)$ removes $k$ when it is present, changes nothing else, and (Q) holds after it.

*Proof.* By Lemma 3, line L12 finds the only slot that holds $k$, or NIL. If NIL, nothing changes. Otherwise line L13 writes DELETED there, so $k$ is no longer in $T$. The set of EMPTY slots does not change, and no other key moves, so (Q) holds for each other key. $\square$

**Theorem.** Start from a table of EMPTY slots, and apply any sequence of QP-INSERT calls (each for a key that is not in the table) and QP-DELETE calls. After each call, the set of keys in $T$ is the set given by the sequence of operations, each QP-SEARCH answers correctly, and each QP-INSERT succeeds unless all $m$ slots are full. Each call ends after at most $m$ iterations of its loop.

*Proof.* The EMPTY table has no keys, so (Q) holds. By induction on the number of calls, with Lemmas 4 and 5 for the step, (Q) holds after each call, and each call changes the set of keys as its specification says. Lemma 3 then gives the answer of each search. The loops of lines L2 and L8 have exactly $m$ iterations at most, because the counter $i$ grows by 1 from 0 to $m-1$, and QP-DELETE makes one search and one write. $\blacksquare$
