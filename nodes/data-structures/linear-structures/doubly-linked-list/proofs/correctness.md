---
title: The doubly linked list operations keep the ring and return the right result
proves: [correctness]
status: full
---

**Setting.** A list $L$ has a sentinel $L.nil$ and a count $L.n$. Write $n = L.n$, and let $v_0, \ldots, v_{n-1}$ be its item nodes from the front, with $v_{-1} = v_n = L.nil$.

**Invariant (I).** The nodes $L.nil, v_0, \ldots, v_{n-1}$ are distinct, $v_i.next = v_{i+1}$ for $-1 \le i \le n - 1$, and $v_i.prev = v_{i-1}$ for $0 \le i \le n$. The list held is $(v_0.key, \ldots, v_{n-1}.key)$.

Since $v_{-1}$ and $v_n$ are both $L.nil$, (I) says $L.nil.next = v_0$ and $L.nil.prev = v_{n-1}$, and for $n = 0$ both are $L.nil$. Write $\ell_i = v_i.key$. For each operation we assume (I) and the precondition, and show (I) for the list that the list type asks for.

**INSERT-AFTER$(L, p, x)$, $p = v_j$ with $-1 \le j \le n - 1$.** Line L1 makes a node $v$. It is new, so it is distinct from the nodes of the ring. By (I), $p.next = v_{j+1}$, which is $L.nil$ when $j = n - 1$. Line L2 sets $v.next = v_{j+1}$ and $v.prev = v_j$. Line L3 writes $v_{j+1}.prev = v$, and line L4 writes $v_j.next = v$ and sets the count to $n + 1$. When $j = n - 1$, the node $v_{j+1}$ is the sentinel, and when $j = -1$, the node $v_j$ is the sentinel; the lines are the same. Define the new sequence $w_{-1}, \ldots, w_n$ by $w_i = v_i$ for $i \le j$, $w_{j+1} = v$, and $w_i = v_{i-1}$ for $i \ge j + 2$, with $w_{n+1} = L.nil$. Its $n + 2$ nodes are distinct. Check the $next$ fields: for $i < j$ and for $i \ge j + 2$ the field was not written and keeps its old value, which is the old successor, and that is $w_{i+1}$; $w_j.next = v = w_{j+1}$ by line L4; $w_{j+1}.next = v_{j+1} = w_{j+2}$ by line L2. Check the $prev$ fields: $w_{j+1}.prev = v_j = w_j$ by line L2; $w_{j+2}.prev = v$ by line L3; the others were not written. So (I) holds for the list $(\ell_0, \ldots, \ell_j, x, \ell_{j+1}, \ldots, \ell_{n-1})$.

The order of the lines matters only in one place: line L2 reads $p.next$ before line L4 writes it, and line L3 reads $p.next$ (still $v_{j+1}$) before line L4. Both reads see the old value.

**DELETE$(L, v)$, $v = v_j$ with $0 \le j \le n - 1$.** By (I), $v.prev = v_{j-1}$ and $v.next = v_{j+1}$, where either can be the sentinel. Line L5 writes $v_{j-1}.next = v_{j+1}$, and line L6 writes $v_{j+1}.prev = v_{j-1}$ and sets the count to $n - 1$. Line L5 does not change $v.next$ or $v.prev$, so line L6 reads the old values. The new sequence $v_{-1}, \ldots, v_{j-1}, v_{j+1}, \ldots, v_n$ has $n + 1$ distinct nodes. The only changed fields are the $next$ field of the predecessor of $v_j$ and the $prev$ field of its successor, and both now skip $v_j$. All other fields keep their old values, which already match the new sequence. So (I) holds for $(\ell_0, \ldots, \ell_{j-1}, \ell_{j+1}, \ldots, \ell_{n-1})$, and line L7 returns $\ell_j$.

**SEARCH$(L, k)$.** Claim: each time line S2 tests the loop condition, $x = v_i$ for some $0 \le i \le n$ and $\ell_t \ne k$ for all $t < i$. At the first test, $x = L.nil.next = v_0$ and the claim holds with $i = 0$. If the loop body runs, then $x = v_i \ne L.nil$, so $i < n$, and $\ell_i \ne k$; line S3 sets $x = v_{i+1}$ by (I), and the claim holds for $i + 1$. Each pass increases $i$, and $i \le n$, so the loop stops after at most $n$ passes. When it stops, either $x = L.nil$, so $i = n$ and no item equals $k$, and line S4 returns NIL; or $x = v_i$ with $\ell_i = k$ and no earlier item equal to $k$, and line S4 returns the first node with key $k$. No field is written, so (I) still holds.

**End operations.** push_front, push_back and insert_before are INSERT-AFTER with $p = L.nil = v_{-1}$, $p = L.nil.prev = v_{n-1}$ and $p = q.prev$ for a node $q = v_j$, which is $v_{j-1}$. In each case $p$ is in the allowed range, and the new item lands at position $0$, $n$ and $j$. pop_front and pop_back are DELETE of $v_0$ and $v_{n-1}$, which are item nodes when $n \ge 1$. So all of them are correct by the two cases above. $\blacksquare$
