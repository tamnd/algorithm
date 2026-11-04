---
title: The monotonic deque keeps the strict suffix minima and returns the minimum of the queue
proves: [correctness]
status: full
---

**Claim.** Start from NEW and apply any sequence of PUSH, POP and MIN, where POP and MIN are called only when $h < t$. Then before and after each operation, the invariant below holds, and each call of MIN returns $\min\{x_h, \ldots, x_{t-1}\}$. The total time of $n$ operations is $O(n)$.

**Notation.** $x_j$ is the item of the $j$-th PUSH, counting from 0. $Q = (x_h, \ldots, x_{t-1})$ is the queue. For $h \le j < t$, call $j$ a *strict suffix minimum* of $Q$ if $x_j < x_m$ for all $m$ with $j < m < t$. Let $M(h, t)$ be the set of these positions.

> **(I)** The positions of the pairs of $D$, from the front to the back, are the elements of $M(h, t)$ in increasing order, and the pair at position $j$ holds $x_j$.

**Fact 1.** Under (I), the items of $D$ strictly increase from the front to the back. *Proof.* If $j < j'$ are both in $M(h, t)$, then $j < j' < t$, so $x_j < x_{j'}$ by the definition for $j$. $\square$

**Fact 2.** If $h < t$, then $t - 1 \in M(h, t)$, so $D$ is not empty. *Proof.* For $j = t - 1$ there is no $m$ with $t - 1 < m < t$, so the condition holds. $\square$

**Step 1: NEW.** Line L1 sets $h = t = 0$ and $D$ empty. $M(0, 0)$ is empty, so (I) holds.

**Step 2: PUSH.** Assume (I) before PUSH$(x)$, and let $x_t = x$. After the call the counters are $h$ and $t + 1$. We show
$$M(h, t + 1) = \{\, j \in M(h, t) : x_j < x \,\} \cup \{t\}.$$
Take $j$ with $h \le j < t$. Then $j \in M(h, t + 1)$ exactly when $x_j < x_m$ for all $m$ with $j < m < t$ and also $x_j < x_t = x$, that is, when $j \in M(h, t)$ and $x_j < x$. And $t \in M(h, t + 1)$ by Fact 2.

By Fact 1, the pairs of $D$ with an item $\ge x$ form a suffix of $D$ (a back part): if a pair has item $\ge x$, every pair behind it has a larger item. The loop of lines L2 and L3 removes pairs from the back while the back item is $\ge x$, so it stops exactly when this suffix is gone, or when $D$ is empty. The remaining pairs are the positions $j \in M(h, t)$ with $x_j < x$, in increasing order. Line L4 appends $(t, x)$, and $t$ is larger than each remaining position. Line L5 sets the counter to $t + 1$. So (I) holds for $M(h, t + 1)$.

The loop ends: each round removes one pair, and $D$ has finitely many pairs.

**Step 3: POP.** Assume (I) and $h < t$. After the call the counters are $h + 1$ and $t$. For $j$ with $h + 1 \le j < t$, the condition for $j \in M$ does not depend on $h$, so $M(h + 1, t) = M(h, t) \setminus \{h\}$. By (I), the least position in $D$ is the front, and every position in $D$ is at least $h$. So $h \in M(h, t)$ exactly when the front has position $h$. Line L6 removes the front in exactly this case, and line L7 increases $h$. By Fact 2, $D$ is not empty, so line L6 can read the front. So (I) holds after POP.

**Step 4: MIN.** Assume (I) and $h < t$. Let $\mu = \min Q$, and let $j^\ast$ be the largest position in $\{h, \ldots, t - 1\}$ with $x_{j^\ast} = \mu$. Each $m$ with $j^\ast < m < t$ has $x_m \ge \mu$ and $x_m \ne \mu$, so $x_m > \mu$, and $j^\ast \in M(h, t)$. Let $f$ be the position of the front of $D$. By (I), $f \le j^\ast$. If $f < j^\ast$, then $x_f < x_{j^\ast} = \mu$ by the definition of $M$ for $f$, which is impossible because $\mu$ is the minimum of $Q$. So $f = j^\ast$, and line L8 returns $x_{j^\ast} = \mu$. MIN changes nothing, so (I) still holds.

**Step 5: the time.** Lines L1, L4 to L8 cost $O(1)$ for each call. Each round of the loop of lines L2 and L3 removes one pair, and each test that fails ends the loop, once per PUSH. A pair enters $D$ only at line L4, once per PUSH, and leaves at most once. So over $n$ operations, the loop runs at most $n$ rounds in total, and the total time is $O(n)$. In the terms of the potential $\Phi = |D| \ge 0$ with $\Phi = 0$ after NEW: a PUSH that removes $p$ pairs costs $p + 1$ units and changes $\Phi$ by $1 - p$, so its amortized cost is $2$; POP and MIN cost one unit and do not increase $\Phi$.

**Conclusion.** By induction on the number of operations, (I) holds after each operation, by Steps 1 to 4, and each MIN returns the minimum of the queue. The total time of $n$ operations is $O(n)$ by Step 5. $\blacksquare$
