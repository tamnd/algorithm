---
title: The circular buffer operations keep the queue in the right cells
proves: [correctness]
status: full
---

**Setting.** A buffer $B$ has an array $A[0..N-1]$ with $N \ge 1$, an index $h$ and a count $n$. For $0 \le i < N$, write $c_i = (h + i) \bmod N$.

**Lemma.** For a fixed $h$, the cells $c_0, \ldots, c_{N-1}$ are distinct, so they are all $N$ cells.

*Proof.* If $c_i = c_j$ with $0 \le i < j < N$, then $N$ divides $j - i$, which is between 1 and $N - 1$. That is impossible. $\square$

**Invariant (I).** $0 \le h < N$, $0 \le n \le N$, and the queue held is $Q = \langle A[c_0], \ldots, A[c_{n-1}] \rangle$.

(I) holds for a new buffer with $h = 0$ and $n = 0$. For each operation, assume (I) and the precondition, and write $Q = \langle q_0, \ldots, q_{n-1} \rangle$ with $q_i = A[c_i]$.

**ENQUEUE$(B, x)$.** If $n = N$, line L1 stops with an error and nothing changes. Otherwise $n < N$. Line L2 writes $x$ into cell $c_n$. By the lemma, $c_n$ differs from $c_0, \ldots, c_{n-1}$, so the items $q_0, \ldots, q_{n-1}$ stay in their cells. Line L3 sets the count to $n + 1 \le N$, and $h$ does not change. So the new queue is $\langle q_0, \ldots, q_{n-1}, x \rangle$, and (I) holds.

**DEQUEUE$(B)$.** If $n = 0$, line L4 stops with an error. Otherwise line L5 reads $x = A[c_0] = q_0$. Line L6 sets $h' = (h + 1) \bmod N$, which is in $[0, N)$, and $n' = n - 1 \ge 0$. No cell is written. The new cells are $c'_i = (h' + i) \bmod N = (h + 1 + i) \bmod N = c_{i+1}$. So the new queue is $\langle A[c_1], \ldots, A[c_{n-1}] \rangle = \langle q_1, \ldots, q_{n-1} \rangle$, and line L7 returns $q_0$.

**PUSH-FRONT$(B, x)$, $n < N$.** Line L8 sets $h' = (h - 1) \bmod N$, taken in $[0, N)$, writes $x$ into $A[h']$ and sets $n' = n + 1$. The new cells are $c'_0 = h'$ and $c'_i = (h - 1 + i) \bmod N = c_{i-1}$ for $i \ge 1$. The cell $h' = c_{N-1}$ is not one of $c_0, \ldots, c_{n-1}$ because $n \le N - 1$, by the lemma. So the write does not touch an item, and the new queue is $\langle x, q_0, \ldots, q_{n-1} \rangle$.

**POP-BACK$(B)$, $n \ge 1$.** Line L9 sets $n' = n - 1$, and line L10 returns $A[(h + n') \bmod N] = A[c_{n-1}] = q_{n-1}$. No cell is written and $h$ does not change, so the new queue is $\langle q_0, \ldots, q_{n-2} \rangle$.

**GET$(B, i)$, $0 \le i < n$.** Line L11 returns $A[c_i] = q_i$, and nothing changes. $\blacksquare$
