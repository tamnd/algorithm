---
title: Correctness of navigation on DFUDS
proves: [correctness]
status: full
---

Let $U = (\, \text{code}(v_0) \cdots \text{code}(v_{n-1})$ with $\text{code}(v) = (^{d(v)} )$ and the nodes in preorder. For a node $v$ let $s(v)$ be the start of its code and $T(v)$ the concatenation of the codes of the subtree of $v$, which is a contiguous segment of $U$ because preorder lists each subtree contiguously, starting at $s(v)$.

**Lemma 1.** $T(v)$ has one more `)` than `(`, every proper prefix of $T(v)$ has at least as many `(` as `)`, and so $(\,T(v)$ is balanced. By induction on the height. If $v$ is a leaf, $T(v) = )$. Otherwise $T(v) = (^{d} )\, T(c_1) \cdots T(c_d)$ for the children $c_1, \ldots, c_d$. After $(^{d} )$ the excess relative to the start is $d - 1$, and each $T(c_j)$ lowers it by exactly one without going below its starting value minus one, by induction. So the excess relative to the start goes $d - 1, d - 2, \ldots, -1$ at the ends of the $T(c_j)$, and is $\ge 0$ before the last symbol. With the leading `(`, $U = (\, T(v_0)$ is balanced.

**Lemma 2 (matching).** Let $v$ have children $c_1, \ldots, c_d$, $d \ge 1$, and let $e$ be the position of the `)` of $\text{code}(v)$, so that $s(c_1) = e + 1$ and $s(c_i)$ is one past the end of $T(c_{i-1})$. For $1 \le i \le d$, the `(` at $e - i$ matches the `)` at $s(c_i) - 1$.

Let $R(t)$ be the number of `(` minus the number of `)` in $U[e - i..t]$; the match of $e - i$ is the least $t > e - i$ with $R(t) = 0$. The positions $e - i, \ldots, e - 1$ are `(`, so $R \ge 1$ there, and $R(e) = i - 1$. If $i = 1$, the match is $e = s(c_1) - 1$. If $i > 1$, then by Lemma 1 each $T(c_j)$ lowers $R$ by exactly one and keeps it at or above its starting value inside, so $R = i - 1 - j$ at the end of $T(c_j)$ and $R \ge i - j$ before that end. For $j < i - 1$ all these values are at least 1, and at the end of $T(c_{i-1})$, which is $s(c_i) - 1$, $R$ is 0 for the first time.

Likewise the leading `(` at position 0 matches the last position of $U$, by Lemma 1, and $s(v_0) = 1$.

**DEGREE (L1).** There are $\text{rank}_)(s(v))$ codes before $v$, so the `)` ending $\text{code}(v)$ is the next one, at $e = \text{select}_)(\text{rank}_)(s(v)) + 1)$, and $\text{code}(v)$ has $e - s(v)$ symbols `(`.

**CHILD (L2-L4).** By Lemma 2, $\text{findclose}(e - i) = s(c_i) - 1$.

**PARENT (L5-L7).** For $v \ne v_0$ with parent $p$ and $v = c_i$, Lemma 2 says the `)` at $s(v) - 1$ is matched by the `(` at $e_p - i$, which lies in $\text{code}(p)$. The number of `)` before that position is the number of codes before $\text{code}(p)$, $\text{rank}_)(o)$, so $\text{code}(p)$ starts right after the $\text{rank}_)(o)$-th `)`, or at 1 if that number is 0, by the convention $\text{select}_)(0) = 0$.

**CHILD-RANK (L8-L9).** With $o = e_p - i$, the `)` ending $\text{code}(p)$ is $e_p = \text{select}_)(\text{rank}_)(o) + 1)$, so $i = e_p - o$.

**SUBTREE-SIZE (L10-L11).** $\text{fwdsearch}(s(v) - 1, -1)$ is the first position after $s(v) - 1$ where the excess falls one below its value at $s(v) - 1$. By Lemma 1, inside $T(v)$ the excess stays at or above its value at $s(v) - 1$ and falls one below it exactly at the last symbol of $T(v)$. So $end$ is the last position of $T(v)$, and since $T(v)$ has $s - 1$ `(` and $s$ `)` for a subtree of $s$ nodes, $end - s(v) + 1 = 2s - 1$.

**Space.** $|U| = 1 + \sum_v (d(v) + 1) = 1 + (n - 1) + n = 2n$. $\blacksquare$
