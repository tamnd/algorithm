---
title: Shift-Or outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, SHIFT-OR$(T, P)$ stops after $n$ iterations and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, which is correct. Let $m \ge 1$, and write $D_j$ for digit $j$ of $D$, $0 \le j < m$.

**Masks.** After lines L3 and L4, digit $j$ of $B[c]$ is 0 exactly when $P[j] = c$: line L3 sets all digits to 1, and line L4 clears digit $j$ of $B[P[j]]$ for each $j$ and nothing else.

**Invariant.** After line L7 in the iteration for $i$:

> **(I)** for every $0 \le j < m$, $D_j = 0$ exactly when $j \le i$ and $P[0 \ldots j] = T[i - j \ldots i]$.

Set $D^{(-1)} = 1^m$, the value of line L5; it satisfies (I) for $i = -1$, since no $j \le -1$ exists.

**Step.** Let $D$ be the value before line L7 in iteration $i$, satisfying (I) for $i - 1$, and $D'$ the value after it. For $j \ge 1$, digit $j$ of $D \ll 1$ is $D_{j-1}$; digit 0 of $D \ll 1$ is 0. The AND with $1^m$ only removes digits $\ge m$. So

$$D'_0 = B[T[i]]_0, \qquad D'_j = D_{j-1} \mathbin{\mathrm{OR}} B[T[i]]_j \quad (1 \le j < m).$$

For $j = 0$: $D'_0 = 0$ exactly when $P[0] = T[i]$, which is (I) for $j = 0$. For $j \ge 1$: $D'_j = 0$ exactly when $D_{j-1} = 0$ and $P[j] = T[i]$, that is, by (I) for $i - 1$, when $j - 1 \le i - 1$, $P[0 \ldots j-1] = T[i - j \ldots i-1]$ and $P[j] = T[i]$, which is exactly $j \le i$ and $P[0 \ldots j] = T[i-j \ldots i]$. So (I) holds for $i$.

**Output.** By (I) with $j = m - 1$, line L8 outputs $i - m + 1$ exactly when $m - 1 \le i$ and $T[i - m + 1 \ldots i] = P$, that is, exactly when $s = i - m + 1$ is a valid shift with $0 \le s \le n - m$. Each valid shift $s$ is output in the iteration $i = s + m - 1$, and these iterations come in increasing order of $s$. The loop has $n$ iterations, each of constant work on a fixed number of words, so the algorithm stops. $\blacksquare$
