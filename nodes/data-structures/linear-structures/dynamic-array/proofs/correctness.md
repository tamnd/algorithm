---
title: The dynamic array keeps its list and its size bound
proves: [correctness]
status: full
---

**Invariant.** (I1) $0 \le n \le cap$, and the list held is $(A[0], \ldots, A[n-1])$. (I2) $cap = 2^e$ for some integer $e \ge 0$, and $cap < 4 \max(n, 1)$.

At the start $n = 0$ and $cap = 1 = 2^0 < 4$, so both parts hold for the empty list.

**Lemma (RESIZE).** If $n \le c$, then RESIZE$(D, c)$ leaves $n$ unchanged, sets $cap = c$, and leaves the list $(A[0], \ldots, A[n-1])$ unchanged.

*Proof.* Line L8 makes a block $B$ of $c$ cells. The loop of lines L9 and L10 keeps the invariant "$B[k] = A[k]$ for $0 \le k < i$" at its test with value $i$: it holds for $i = 0$, and line L10 extends it to $i + 1$. It runs for $i = 0, \ldots, n - 1$, and each index is less than $c$ because $n \le c$. At exit $B[0 \ldots n-1] = A[0 \ldots n-1]$. Line L11 makes $B$ the block and sets $cap = c$. $\square$

**APPEND$(D, x)$.** Let $(\ell_0, \ldots, \ell_{n-1})$ be the list before the call, and assume (I1) and (I2).

- If $n < cap$, line L1 does nothing. Line L2 writes $x$ to cell $n < cap$, and line L3 sets the count to $n + 1 \le cap$. The list is $(\ell_0, \ldots, \ell_{n-1}, x)$. The capacity is the same power of two, and $cap < 4\max(n, 1) \le 4(n + 1)$.
- If $n = cap$, line L1 calls RESIZE$(D, 2 cap)$, with $n \le 2 cap$, so by the lemma the list is unchanged and $cap$ becomes $2n = 2^{e+1}$. Now $n < cap$ because $n = cap/2$ and $cap \ge 2$. Lines L2 and L3 append $x$ as in the first case. After the call, $n + 1 \le 2n = cap$ because $n = 2^e \ge 1$, and $cap = 2n < 4(n + 1)$.

In both cases (I1) and (I2) hold for the list with $x$ appended.

**POP$(D)$, $n \ge 1$.** Let $(\ell_0, \ldots, \ell_{n-1})$ be the list. Line L4 sets the count to $n' = n - 1$, and line L5 reads $x = A[n'] = \ell_{n-1}$, which is in range because $n' < n \le cap$. The list $A[0 \ldots n'-1]$ is $(\ell_0, \ldots, \ell_{n-2})$, and (I1) holds. Line L7 returns $\ell_{n-1}$, the last item. It remains to show (I2) after line L6. Before the call, $cap < 4\max(n, 1) = 4n = 4n' + 4$.

- *Case $n' = 0$.* Line L6 does nothing. Then $cap < 4 = 4\max(n', 1)$.
- *Case $n' \ge 1$ and $4n' = cap$.* Line L6 calls RESIZE$(D, cap/2)$. Here $cap = 4n' \ge 4$, so $cap/2 = 2^{e-1}$ is a power of two and is at least $2n' \ge n'$. By the lemma the list is unchanged, and the new capacity is $2n' < 4n'$.
- *Case $n' \ge 1$ and $4n' \ne cap$.* Line L6 does nothing. If $cap \le 3$, then $cap < 4 \le 4n'$. If $cap \ge 4$, then $cap$ is a multiple of 4, and $cap < 4n' + 4$ gives $cap \le 4n'$; with $cap \ne 4n'$ this gives $cap < 4n'$.

In all cases (I2) holds with $n'$.

**GET and SET.** These read or write $A[i]$ for $0 \le i < n$, as in an array, and change neither $n$ nor $cap$. $\blacksquare$
