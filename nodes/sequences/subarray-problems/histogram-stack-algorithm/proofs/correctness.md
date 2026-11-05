---
title: The histogram stack algorithm returns the largest rectangle
proves: [correctness]
status: full
---

We use the pseudocode of the page on heights $h[0..n-1] \ge 0$, and we set $h[n] = 0$, the value that line L3 uses at $i = n$. For $0 \le a \le b \le n - 1$ let $\text{area}(a, b) = (b - a + 1) \min_{a \le l \le b} h[l]$, and let $A^*$ be the largest such area, or $0$ if $n = 0$. Write the stack from the bottom as $S = [s_1, \dots, s_t]$ and set $s_0 = -1$.

**Lemma 1 (invariants).** At the start of each step $i$ ($0 \le i \le n$):

1. $s_1 < \dots < s_t \le i - 1$ and $h[s_1] < \dots < h[s_t]$;
2. for $1 \le q \le t$, every $l$ with $s_{q-1} < l < s_q$ has $h[l] \ge h[s_q]$;
3. if $i \ge 1$, then $t \ge 1$ and $s_t = i - 1$.

*Proof.* At $i = 0$ the stack is empty. Suppose the lemma holds at the start of step $i \le n$ and look at the stack just before line L8 of that step, $[s_1, \dots, s_u]$ with $u \le t$. The pops removed exactly $s_{u+1}, \dots, s_t$, and they all have $h \ge x = h[i]$, while $h[s_u] < h[i]$ if $u \ge 1$, since the loop stopped. Line L8 pushes $i$. Part 1 holds for the new stack, since $h[s_u] < h[i]$. For part 2 with the new top $i$, the bars $l$ with $s_u < l < i$ are the popped $s_{u+1}, \dots, s_t$, each with $h \ge h[i]$, and the bars between them, each at least as high as the popped bar above it by part 2; so all have $h[l] \ge h[i]$. The other parts of part 2 do not change. Part 3 holds since $i$ is on top. $\blacksquare$

**Lemma 2 (each recorded area is real).** When line L7 runs for $k$ at step $i$ with $left$ from line L6, every bar $l$ with $left < l < i$ has $h[l] \ge h[k]$. So $h[k] (i - left - 1) = \text{area}(left + 1, i - 1)$ if $i \le n$, and $left + 1 \le k \le i - 1$.

*Proof.* At the pop, $k = s_q$ and $left = s_{q-1}$ for the stack at that moment, which is a prefix of the stack at the start of step $i$, so Lemma 1 applies to it. Bars with $left < l < k$ have $h[l] \ge h[k]$ by part 2. Bars with $k < l < i$ are the stack items above $k$ at the start of the step, which are higher than $h[k]$ by part 1, and the bars between them, which are at least as high as some such item by part 2, with the last item $s_t = i - 1$ by part 3. The lowest bar of $left + 1..i - 1$ is then $k$ itself. $\blacksquare$

**Lemma 3 (when a bar is popped).** Bar $k \le n - 1$ is popped at step $i_k$, the least $i$ with $k < i \le n$ and $h[i] \le h[k]$, and at that moment $left = L_k$, the largest $l < k$ with $h[l] < h[k]$, or $-1$.

*Proof.* Bar $k$ is pushed at step $k$. At a later step $i$ with $h[i] > h[k]$, the pops stop at $k$ or above it, because every item above $k$ is higher than $h[k]$ and the loop stops at the first item lower than $h[i]$; so $k$ stays. At the first step $i$ with $h[i] \le h[k]$, every item above $k$ is higher than $h[k] \ge h[i]$, so all of them and then $k$ are popped. Now $left = s_{q-1}$ has $h[left] < h[k]$ by part 1, and every bar between $left$ and $k$ has $h \ge h[k]$ by part 2, so $left = L_k$. $\blacksquare$

At $i = n$ the value $x = 0 \le h[k]$ for every $k$, so $i_k \le n$ always exists.

**Theorem.** LARGEST-RECTANGLE returns $A^*$.

*Proof.* By Lemma 2, every value that line L7 compares is the area of a real rectangle, so $best \le A^*$; and $best \ge 0 = A^*$ if $n = 0$. Let $n \ge 1$, and let $\text{area}(a, b) = A^*$. Let $k$ be the largest index in $a..b$ with $h[k] = \min_{a \le l \le b} h[l]$. Bars $k + 1..b$ are higher than $h[k]$, so $i_k > b$ by Lemma 3. Bars $a..k-1$ are at least $h[k]$, so $L_k < a$. Line L7 for $k$ records $h[k](i_k - L_k - 1) \ge h[k](b - a + 1) = A^*$. So $best \ge A^*$ at the end.

*Cost.* Each of the indices $0..n$ is pushed once and popped at most once, so the loop of line L4 runs at most $n + 1$ times in all, and the algorithm stops after $\Theta(n)$ steps. $\blacksquare$
