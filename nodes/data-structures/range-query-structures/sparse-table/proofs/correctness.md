---
title: The sparse table holds the power-of-two aggregates and its queries return the range product
proves: [correctness, termination]
status: full
---

Let $(S, \oplus)$ be a semigroup, so $\oplus$ is associative, and let $n \ge 1$. For $0 \le a \le b \le n - 1$ write $\Pi(a, b) = A[a] \oplus \cdots \oplus A[b]$. By associativity this does not depend on the brackets, and for $a \le m < b$,

$$\Pi(a, b) = \Pi(a, m) \oplus \Pi(m + 1, b). \tag{1}$$

Let $K = \lfloor \lg n \rfloor$. All loops of the procedures run over finite integer ranges that do not change inside the loop, and the loop of line L9 also runs over $K + 1$ values, so every procedure ends.

**Lemma 1 (the log table).** After line L1, $LG[m] = \lfloor \lg m \rfloor$ for $1 \le m \le n$.

*Proof.* By strong induction on $m$. $LG[1] = 0 = \lfloor \lg 1 \rfloor$. For $m \ge 2$, let $j = \lfloor \lg m \rfloor \ge 1$, so $2^j \le m < 2^{j+1}$. Then $2^{j-1} \le m/2 < 2^j$, and since $2^{j-1}$ is an integer, also $2^{j-1} \le \lfloor m/2 \rfloor < 2^j$. So $\lfloor \lg \lfloor m/2 \rfloor \rfloor = j - 1$. The loop sets $LG[\lfloor m/2 \rfloor]$ before $LG[m]$, because $\lfloor m/2 \rfloor < m$, and by the hypothesis $LG[m] = (j - 1) + 1 = j$. $\square$

**Lemma 2 (build).** After BUILD, for each $0 \le k \le K$ and $0 \le i \le n - 2^k$: $ST[k][i] = \Pi(i, i + 2^k - 1)$.

*Proof.* By induction on $k$. Line L2 gives $ST[0][i] = A[i] = \Pi(i, i)$. Let $1 \le k \le K$ and assume the claim for $k - 1$. Line L3 runs to $LG[n] = K$ by Lemma 1. For $0 \le i \le n - 2^k$, the cells read by line L5 exist: $i \le n - 2^{k-1}$, and $i + 2^{k-1} \le n - 2^{k-1}$ because $i \le n - 2^k$. By the hypothesis they are $\Pi(i, i + 2^{k-1} - 1)$ and $\Pi(i + 2^{k-1}, i + 2^k - 1)$, and by (1) with $m = i + 2^{k-1} - 1$ their product is $\Pi(i, i + 2^k - 1)$. Row $k$ is written only after row $k - 1$ is complete, and row $k - 1$ is not written again. $\square$

**Lemma 3 (fast query).** Assume that $\oplus$ is also idempotent: $x \oplus x = x$ for each $x \in S$. For $0 \le l \le r \le n - 1$, QUERY$(l, r)$ returns $\Pi(l, r)$.

*Proof.* Let $L = r - l + 1 \le n$. By Lemma 1, line L6 sets $k = \lfloor \lg L \rfloor$, so $2^k \le L < 2^{k+1}$, and $k \le K$. Let $a = r - 2^k + 1$ and $b = l + 2^k - 1$. Then $a \ge l$ and $b \le r$, because $2^k \le L$. So both cells exist ($0 \le l \le n - 2^k$ and $0 \le a \le n - 2^k$), and by Lemma 2 line L7 returns $\Pi(l, b) \oplus \Pi(a, r)$. Also $a \le b + 1$, because $a - b - 1 = L - 2^{k+1} < 0$, so $a \le b$.

So $l \le a \le b \le r$. Write $\Pi(l, b) = X \oplus M$ and $\Pi(a, r) = M \oplus Y$, where $M = \Pi(a, b)$, $X = \Pi(l, a - 1)$ when $l < a$, and $Y = \Pi(b + 1, r)$ when $b < r$; by (1), each part that exists may be split off this way. If $l < a$ and $b < r$, associativity and idempotence give

$$\Pi(l, b) \oplus \Pi(a, r) = X \oplus (M \oplus M) \oplus Y = X \oplus M \oplus Y = \Pi(l, r),$$

the last step by (1) twice. If $l = a$, then $\Pi(l, b) = M$ and the same computation without $X$ gives $M \oplus M \oplus Y = M \oplus Y = \Pi(l, r)$, or $M \oplus M = M = \Pi(l, r)$ when also $b = r$. The case $b = r$ with $l < a$ is the mirror image. No step exchanges two factors, so commutativity is not used. $\square$

**Lemma 4 (query-any).** For $0 \le l \le r \le n - 1$, QUERY-ANY$(l, r)$ returns $\Pi(l, r)$, for any associative $\oplus$.

*Proof.* Write $l_0$ for the first argument and $l$ for the variable that line L10 moves. We use the invariant, at the start of the iteration for $k$ in line L9:

> **(Q)** $l_0 \le l \le r + 1$, $r - l + 1 < 2^{k+1}$, and $res$ is $\Pi(l_0, l - 1)$, where $res = e$ stands for the empty product when $l = l_0$.

At the start, $k = K$, $l = l_0$, and $r - l + 1 \le n < 2^{K+1}$, so (Q) holds. In the iteration for $k$: if $l + 2^k - 1 \le r$, then the cell $ST[k][l]$ exists, since $l + 2^k - 1 \le r \le n - 1$, and by Lemma 2 it is $\Pi(l, l + 2^k - 1)$. Line L10 makes $res = \Pi(l_0, l - 1) \oplus \Pi(l, l + 2^k - 1) = \Pi(l_0, l + 2^k - 1)$ by (1), or just $\Pi(l, l + 2^k - 1)$ when $res$ was empty, and moves $l$ to $l + 2^k$. The new length $r - l + 1$ is the old one minus $2^k$, which is less than $2^{k+1} - 2^k = 2^k$. If the test fails, then $r - l + 1 < 2^k$ already. In both cases (Q) holds for $k - 1$. After the iteration for $k = 0$, (Q) gives $r - l + 1 < 1$, so $l = r + 1$, and $res = \Pi(l_0, r)$. This product is not empty, because $l$ moved from $l_0 \le r$ to $r + 1$. $\square$

**Theorem.** After BUILD on $A[0 \ldots n - 1]$, QUERY-ANY$(l, r)$ returns $A[l] \oplus \cdots \oplus A[r]$ for every associative $\oplus$, and QUERY$(l, r)$ returns the same value for every associative and idempotent $\oplus$, for all $0 \le l \le r \le n - 1$.

*Proof.* Lemmas 2, 3 and 4, together with the termination shown at the start. $\blacksquare$
