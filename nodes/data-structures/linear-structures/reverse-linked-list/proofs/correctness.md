---
title: REVERSE returns the same nodes in reverse order
proves: [correctness, termination]
status: full
---

**Claim.** Let $head$ be the first node of an acyclic singly linked list with nodes $x_1, \dots, x_n$ ($n \ge 0$), so that $x_i.next = x_{i+1}$ for $1 \le i < n$ and $x_n.next = \text{nil}$, and $head = \text{nil}$ when $n = 0$. Then REVERSE$(head)$ stops after exactly $n$ iterations of the loop of line L3. It returns $x_n$ (nil when $n = 0$), and after the call $x_{i+1}.next = x_i$ for $1 \le i < n$ and $x_1.next = \text{nil}$. No other field of any node changes, and no node is created.

**Setup.** Write $x_0 = \text{nil}$ and $x_{n+1} = \text{nil}$. Count the iterations of the loop with $k$, so that $k = 0$ at the first test of line L3. The invariant at the test of line L3 after $k$ iterations is:

> **(R)** $0 \le k \le n$, $prev = x_k$, $curr = x_{k+1}$, $x_i.next = x_{i-1}$ for $1 \le i \le k$, and $x_i.next = x_{i+1}$ for $k < i \le n$.

The third part says that the list from $prev$ is $x_k \to x_{k-1} \to \dots \to x_1 \to \text{nil}$. The last part says that the list from $curr$ is $x_{k+1} \to \dots \to x_n \to \text{nil}$, with its old links.

**Step 1 (initialization).** Lines L1 and L2 set $prev = \text{nil} = x_0$ and $curr = head = x_1$ (both nil when $n = 0$). No link has changed, so $x_i.next = x_{i+1}$ for $0 < i \le n$, and the condition for $i \le 0$ is empty. So (R) holds with $k = 0$.

**Step 2 (maintenance).** Assume (R) for some $k$, and that the test of line L3 succeeds, so $curr \ne \text{nil}$. Since $curr = x_{k+1}$ and $x_{k+1}$ is nil only for $k = n$, we have $k < n$, and $curr$ is the real node $x_{k+1}$. By the last part of (R) with $i = k + 1$, line L4 sets $next = x_{k+1}.next = x_{k+2}$. Line L5 sets $x_{k+1}.next = prev = x_k$. This is the only write to a node field in the iteration, so the links of every other node stay as (R) states. Lines L6 and L7 set $prev = x_{k+1}$ and $curr = x_{k+2}$. Now $x_i.next = x_{i-1}$ holds for $1 \le i \le k + 1$, and $x_i.next = x_{i+1}$ holds for $k + 1 < i \le n$. So (R) holds for $k + 1$, and $k + 1 \le n$.

**Step 3 (termination).** By (R), $k \le n$ at each test of line L3, and each iteration increases $k$ by exactly 1. So the quantity $n - k$ is a non-negative integer that drops by exactly 1 in each iteration, and the loop runs at most $n$ times. The loop cannot stop while $k < n$, because then $curr = x_{k+1}$ is a node, not nil. So it stops exactly when $k = n$, after $n$ iterations.

**Step 4 (conclusion).** At exit, (R) holds with $k = n$: $prev = x_n$, and $x_i.next = x_{i-1}$ for $1 \le i \le n$, that is, $x_{i+1}.next = x_i$ for $1 \le i < n$ and $x_1.next = x_0 = \text{nil}$. Line L8 returns $prev = x_n$. The only writes to node fields are the $n$ writes of line L5, one to the next field of each node, and the algorithm creates no node. $\blacksquare$
