---
title: The stack with minimum returns the least item after each operation
proves: [correctness]
status: full
---

**Setting.** The structure is a stack $S$ of pairs. Write its state, from the bottom to the top, as $\langle (x_1, m_1), \ldots, (x_k, m_k) \rangle$ with $k \ge 0$. The stack that the user sees is $\langle x_1, \ldots, x_k \rangle$. The items come from a set with a total order.

**Invariant (M).** $m_j = \min\{x_1, \ldots, x_j\}$ for each $1 \le j \le k$.

We show that each operation keeps (M), that the stack of the $x_j$ changes as a stack must, and that each query returns the right value. The underlying stack of pairs meets the stack laws, so a push of a pair adds it at the top and a pop removes and returns the top pair.

**Initialization.** The new structure is empty, $k = 0$, and (M) holds with no index to check.

**PUSH$(S, x)$.** Line L1 sets $m = x$ if $k = 0$, and $m = \min(x, m_k)$ otherwise. Line L2 pushes $(x, m)$, so the new state has $x_{k+1} = x$ and $m_{k+1} = m$, and the pairs below are unchanged. For $j \le k$, (M) holds as before. For $j = k + 1$: if $k = 0$ then $m_1 = x_1 = \min\{x_1\}$. If $k \ge 1$ then, by (M) for $j = k$,

$$m_{k+1} = \min(x, m_k) = \min(x_{k+1}, \min\{x_1, \ldots, x_k\}) = \min\{x_1, \ldots, x_{k+1}\}.$$

The user's stack is $\langle x_1, \ldots, x_k, x \rangle$.

**POP$(S)$, $k \ge 1$.** Line L3 removes the top pair $(x_k, m_k)$, and line L4 returns $x_k$, the top item of the user's stack. The pairs $1, \ldots, k - 1$ are unchanged, so (M) holds for them, and the user's stack is $\langle x_1, \ldots, x_{k-1} \rangle$.

**TOP$(S)$, $k \ge 1$.** Line L5 returns $x_k$. Nothing changes.

**MIN$(S)$, $k \ge 1$.** Line L6 returns $m_k$, which by (M) is $\min\{x_1, \ldots, x_k\}$, the least item of the user's stack. Nothing changes.

**The lean variant.** The variant keeps the items in a stack $I = \langle x_1, \ldots, x_k \rangle$ and a second stack $Q$ that receives $x$ on a push exactly when $Q$ is empty or $x \le \text{top}(Q)$, and loses its top on a pop exactly when the popped item equals $\text{top}(Q)$. Its invariant is: $Q$ is the sequence of the *prefix minima with repeats*, that is, of the items $x_j$ with $x_j \le x_i$ for all $i < j$, in the order of $j$. A push of $x$ appends $x$ to this sequence exactly when $x \le \min\{x_1, \ldots, x_k\} = \text{top}(Q)$, which is the test. On a pop of $x_k$, the item $x_k$ is in the sequence exactly when $x_k \le$ every earlier item. In that case it is the last entry of $Q$ and equals $\text{top}(Q)$. If it is not in the sequence, then some earlier item is less than $x_k$, so $\text{top}(Q) < x_k$ and the test fails. So the test removes $x_k$ from $Q$ exactly when it is there, and $\text{top}(Q) = \min\{x_1, \ldots, x_k\}$ is kept, because the last prefix minimum is the minimum. With the strict test $x < \text{top}(Q)$ on push, a repeated minimum is not recorded, and the first pop of it removes the only copy from $Q$; this is the pitfall of the page. $\blacksquare$
