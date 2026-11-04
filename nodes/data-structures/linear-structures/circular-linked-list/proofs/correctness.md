---
title: The circular linked list operations keep the ring and return the right result
proves: [correctness]
status: full
---

**Invariant (I).** If $L.n = 0$, then $L.last = $ NIL. If $n = L.n \ge 1$, the items are held in distinct nodes $v_0, \ldots, v_{n-1}$ with $v_i.next = v_{i+1}$ for $0 \le i < n - 1$, $v_{n-1}.next = v_0$, and $L.last = v_{n-1}$. The list held is $(\ell_0, \ldots, \ell_{n-1})$ with $\ell_i = v_i.key$.

For each operation we assume (I) and the precondition, and show (I) for the list that the type asks for. Each push adds 1 to the count and each pop subtracts 1, so we only check the nodes and pointers.

**PUSH-FRONT$(L, x)$.** Line L1 makes a new node $v$, distinct from the old nodes. If $n = 0$, line L2 sets $v.next = v$ and $L.last = v$: this is (I) for $n = 1$ with $v_0 = v$, and the list $(x)$. If $n \ge 1$, line L3 first sets $v.next = L.last.next = v_{n-1}.next = v_0$, then sets $v_{n-1}.next = v$. Define $w_0 = v$ and $w_i = v_{i-1}$ for $1 \le i \le n$. Then $w_0.next = v_0 = w_1$; $w_i.next = v_i = w_{i+1}$ for $1 \le i \le n - 1$, since those fields are unchanged; and $w_n.next = v_{n-1}.next = v = w_0$. The nodes are distinct and $L.last = v_{n-1} = w_n$. So (I) holds for $(x, \ell_0, \ldots, \ell_{n-1})$.

**PUSH-BACK$(L, x)$.** After line L4, (I) holds for $(x, \ell_0, \ldots, \ell_{n-1})$ with nodes $w_0 = v, w_1, \ldots, w_n$ and $L.last = w_n$. Line L5 sets $L.last = w_n.next = w_0 = v$. Read the same ring from $L.last.next = w_1$: define $u_i = w_{i+1}$ for $0 \le i \le n - 1$ and $u_n = w_0$. Then $u_i.next = u_{i+1}$ for $i < n$, $u_n.next = w_1 = u_0$, and $L.last = u_n$. So (I) holds for $(\ell_0, \ldots, \ell_{n-1}, x)$. When $n = 0$ the ring is the single node $v$ and $L.last = v.next = v$, which is (I) for $(x)$.

**POP-FRONT$(L)$, $n \ge 1$.** Line L6 sets $v = v_{n-1}.next = v_0$. If $n = 1$, then $v_0 = v_{n-1} = L.last$, line L7 sets $L.last = $ NIL, and (I) holds for the empty list. If $n \ge 2$, then $v \ne L.last$, and line L7 sets $v_{n-1}.next = v_0.next = v_1$. The nodes $v_1, \ldots, v_{n-1}$ are distinct, $v_i.next = v_{i+1}$ for $1 \le i < n - 1$ (unchanged), $v_{n-1}.next = v_1$, and $L.last = v_{n-1}$. So (I) holds for $(\ell_1, \ldots, \ell_{n-1})$, and line L8 returns $\ell_0$.

**ROTATE$(L)$, $n \ge 1$.** Line L9 sets $L.last = v_{n-1}.next = v_0$. No $next$ field changes. Define $u_i = v_{i+1}$ for $0 \le i \le n - 2$ and $u_{n-1} = v_0$. Then $u_i.next = u_{i+1}$ for $i < n - 1$, $u_{n-1}.next = v_1 = u_0$ (or $v_0 = u_0$ when $n = 1$), and $L.last = u_{n-1}$. So (I) holds for $(\ell_1, \ldots, \ell_{n-1}, \ell_0)$, which is the list with its front moved to the back. $\blacksquare$
