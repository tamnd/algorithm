---
title: The linked list operations keep the chain and return the right result
proves: [correctness]
status: full
---

**Setting.** For a list $L$, the *chain* of $L$ is the sequence of nodes $v_0 = L.head$, $v_{k+1} = v_k.next$, up to the first NIL.

**Invariant (I).** The chain of $L$ has exactly $L.n$ nodes $v_0, \ldots, v_{n-1}$, they are distinct, and $v_{n-1}.next = $ NIL (or $L.head = $ NIL when $n = 0$). The list held is $(v_0.key, \ldots, v_{n-1}.key)$.

We show that each operation, started in a state where (I) holds and its precondition holds, ends with (I) for the list that the list type asks for. Write $\ell_k = v_k.key$ for the old keys. A new node made in line L1 or L4 is not in the old chain, because it did not exist before.

**PUSH-FRONT$(L, x)$.** Line L1 makes a new node $v$ with key $x$. Line L2 sets $v.next = v_0$ (or NIL if $n = 0$). Line L3 sets $L.head = v$ and the count to $n + 1$. The new chain is $v, v_0, \ldots, v_{n-1}$: these are $n + 1$ distinct nodes, because $v$ is new and the old nodes are distinct, and the old $next$ fields did not change, so the chain still ends at NIL after $v_{n-1}$. The list held is $(x, \ell_0, \ldots, \ell_{n-1})$.

**INSERT-AFTER$(L, p, x)$, $p = v_j$ for some $0 \le j < n$.** Line L4 makes a new node $v$. Line L5 sets $v.next$ to the old $v_j.next$, which is $v_{j+1}$, or NIL when $j = n - 1$. Line L6 then sets $v_j.next = v$. Only the $next$ field of $v_j$ and of $v$ are written. So the new chain is $v_0, \ldots, v_j, v, v_{j+1}, \ldots, v_{n-1}$, and it ends at NIL. These $n + 1$ nodes are distinct, and the count is $n + 1$. The list held is $(\ell_0, \ldots, \ell_j, x, \ell_{j+1}, \ldots, \ell_{n-1})$. Line L5 reads $p.next$ before line L6 changes it; that order is what makes $v.next$ the old successor.

**DELETE-FRONT$(L)$, $n \ge 1$.** Line L7 sets $v = v_0$. Line L8 sets $L.head = v_0.next = v_1$ (or NIL if $n = 1$) and the count to $n - 1$. No $next$ field changes, so the new chain is $v_1, \ldots, v_{n-1}$, with $n - 1$ distinct nodes, ending at NIL. Line L9 returns $\ell_0$, and the list held is $(\ell_1, \ldots, \ell_{n-1})$.

**DELETE-AFTER$(L, p)$, $p = v_j$ with $j \le n - 2$.** The precondition $p.next \ne$ NIL means $j \le n - 2$. Line L10 sets $v = v_{j+1}$. Line L11 sets $v_j.next = v_{j+1}.next$, which is $v_{j+2}$ or NIL, and the count to $n - 1$. Only the $next$ field of $v_j$ changes. The new chain is $v_0, \ldots, v_j, v_{j+2}, \ldots, v_{n-1}$: $n - 1$ distinct nodes ending at NIL. Line L12 returns $\ell_{j+1}$, and the list held is the old list without position $j + 1$.

**SEARCH$(L, x)$.** *Loop invariant:* at the test of line S2, $p = v_k$ for some $0 \le k \le n$ (with $v_n$ meaning NIL), and $\ell_t \ne x$ for every $t < k$. It holds with $k = 0$ after line S1. If the test passes, then $p \ne$ NIL and $\ell_k \ne x$, and line S3 moves to $v_{k+1}$, so the invariant holds for $k + 1$. The value $k$ grows by 1 in each iteration and cannot pass $n$, because at $k = n$ the test fails on $p = $ NIL; by (I) the chain has $n$ nodes and no cycle, so the loop ends after at most $n$ iterations. At exit, either $p = $ NIL and $k = n$, so no key equals $x$ and NIL is right, or $p = v_k$ with $\ell_k = x$ and no earlier key equal to $x$, so $p$ is the first node with key $x$.

**NODE-AT$(L, i)$, $0 \le i < n$.** After line S5 $p = v_0$, and each of the $i$ steps of line S6 moves from $v_k$ to $v_{k+1}$ for $k < i \le n - 1$, so no step reads NIL. Line S7 returns $v_i$. $\blacksquare$
