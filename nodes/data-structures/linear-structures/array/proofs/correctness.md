---
title: The array operations keep the list and return the right result
proves: [correctness]
status: full
---

**Setting.** The array has capacity $N \ge 0$, a count $n$ and cells $A[0 \ldots N-1]$. The *list held by the array* is $L = (A[0], \ldots, A[n-1])$.

**Invariant (I).** $0 \le n \le N$.

We show that each operation, started in a state where (I) holds and its precondition holds, ends in a state where (I) holds, holds the list that the list type asks for, and returns the right value. We write $L = (\ell_0, \ldots, \ell_{n-1})$ for the list before the operation, so $\ell_k$ is the old value of $A[k]$.

**GET$(A, i)$, $0 \le i < n$.** Line L1 returns $A[i] = \ell_i$, the item at position $i$. Nothing is written, so $L$ and (I) do not change.

**SET$(A, i, x)$, $0 \le i < n$.** Line L2 writes only cell $i$, so the new list is $(\ell_0, \ldots, \ell_{i-1}, x, \ell_{i+1}, \ldots, \ell_{n-1})$, and $n$ does not change.

**INSERT$(A, i, x)$, $0 \le i \le n < N$.** The goal is the list $(\ell_0, \ldots, \ell_{i-1}, x, \ell_i, \ldots, \ell_{n-1})$ of length $n + 1$.

*Loop invariant (J).* At each test of line L3 with the current value $j$, where $i \le j \le n$: $A[k] = \ell_k$ for $0 \le k \le j - 1$, and $A[k] = \ell_{k-1}$ for $j + 1 \le k \le n$.

1. *Initialization.* Before the first test $j = n$. No cell has been written, so $A[k] = \ell_k$ for $k \le n - 1$, and the second range $n + 1 \le k \le n$ is empty. All indices used are less than $N$ because $n < N$.
2. *Maintenance.* Assume (J) at the test with value $j > i$. Line L4 sets $A[j] \leftarrow A[j-1]$. Since $j - 1 \le j - 1$, the first part of (J) gives $A[j-1] = \ell_{j-1}$, so now $A[j] = \ell_{j-1}$. No other cell changes. Then $j$ becomes $j' = j - 1$. For $k \le j' - 1 = j - 2$ the cell is unchanged and equals $\ell_k$. For $j' + 1 = j \le k \le n$: $A[j] = \ell_{j-1}$ was just written, and for $k \ge j + 1$ the cell is unchanged and equals $\ell_{k-1}$ by (J). So (J) holds for $j'$.
3. *Termination.* Each iteration decreases $j$ by exactly 1, from $n$, and the loop stops at the first test with $j = i$. So it runs exactly $n - i$ times. At exit, (J) with $j = i$ gives $A[k] = \ell_k$ for $k < i$ and $A[k] = \ell_{k-1}$ for $i + 1 \le k \le n$.

Line L5 writes $x$ to $A[i]$, which is the only index not covered by the two ranges. Line L6 sets the count to $n + 1 \le N$, so (I) holds. The cells $A[0 \ldots n]$ now read $\ell_0, \ldots, \ell_{i-1}, x, \ell_i, \ldots, \ell_{n-1}$, which is the goal.

**DELETE$(A, i)$, $0 \le i < n$.** The goal is to return $\ell_i$ and to leave the list $(\ell_0, \ldots, \ell_{i-1}, \ell_{i+1}, \ldots, \ell_{n-1})$ of length $n - 1$. Line L7 saves $x = \ell_i$ before any cell is written.

*Loop invariant (K).* At each test of line L8 with the current value $j$, where $i \le j \le n - 1$: $A[k] = \ell_k$ for $k < i$ and for $j \le k \le n - 1$, and $A[k] = \ell_{k+1}$ for $i \le k \le j - 1$.

1. *Initialization.* Before the first test $j = i$, no cell has been written, and the middle range is empty.
2. *Maintenance.* Assume (K) at the test with value $j \le n - 2$. Line L9 sets $A[j] \leftarrow A[j+1]$. Since $j + 1$ lies in $[j, n-1]$, (K) gives $A[j+1] = \ell_{j+1}$. So now $A[j] = \ell_{j+1}$, and the middle range grows to $[i, j]$. The cells from $j + 1$ to $n - 1$ are unchanged. So (K) holds for $j + 1$.
3. *Termination.* Each iteration increases $j$ by exactly 1, from $i$, and the loop stops at the first test with $j = n - 1$. So it runs exactly $n - 1 - i$ times. At exit, (K) with $j = n - 1$ gives $A[k] = \ell_{k+1}$ for $i \le k \le n - 2$ and $A[k] = \ell_k$ for $k < i$.

Line L10 sets the count to $n - 1 \ge 0$, so (I) holds, and the list $A[0 \ldots n-2]$ is the goal. Line L11 returns $x = \ell_i$.

**SEARCH$(A, x)$.** *Loop invariant:* at the test of line S1 with value $i$, no $\ell_k$ with $k < i$ equals $x$. It holds for $i = 0$, and line S2 keeps it, because it returns when $\ell_i = x$ and otherwise $\ell_i \ne x$. If line S2 returns $i$, then $\ell_i = x$ and no earlier item equals $x$, so $i$ is the first index of $x$. If the loop ends, then $i = n$ and no item equals $x$, so NIL is right. The loop runs at most $n$ times because $i$ increases by 1 each time. Nothing is written. $\blacksquare$
