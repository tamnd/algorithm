---
title: The max-product scan returns the largest subarray product
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[0..n-1]$ with $n \ge 1$. For $i \le j$ let $\Pi(i, j) = A[i] \cdots A[j]$. For each $j$ let $X_j = \{\Pi(i, j) : 0 \le i \le j\}$, the products of the subarrays ending at $j$, and let $E^{+}(j) = \max X_j$, $E^{-}(j) = \min X_j$ and $B(j) = \max_{0 \le i \le l \le j} \Pi(i, l)$.

**Lemma 1.** For $j \ge 1$, $X_j = \{A[j]\} \cup \{x \cdot A[j] : x \in X_{j-1}\}$.

*Proof.* $\Pi(j, j) = A[j]$, and $\Pi(i, j) = \Pi(i, j-1) \cdot A[j]$ for $i < j$. $\blacksquare$

**Lemma 2.** For $j \ge 1$, let $(u, v) = (E^{+}(j-1), E^{-}(j-1))$ if $A[j] \ge 0$ and $(u, v) = (E^{-}(j-1), E^{+}(j-1))$ if $A[j] < 0$. Then $E^{+}(j) = \max(A[j], u A[j])$ and $E^{-}(j) = \min(A[j], v A[j])$.

*Proof.* Every $x \in X_{j-1}$ has $E^{-}(j-1) \le x \le E^{+}(j-1)$. If $A[j] \ge 0$, then $x A[j] \le E^{+}(j-1) A[j]$ and $x A[j] \ge E^{-}(j-1) A[j]$. If $A[j] < 0$, multiplying by $A[j]$ reverses the inequalities, so $x A[j] \le E^{-}(j-1) A[j]$ and $x A[j] \ge E^{+}(j-1) A[j]$. In both cases $u A[j]$ is the largest and $v A[j]$ the smallest element of $\{x A[j] : x \in X_{j-1}\}$, and both occur, since $E^{+}(j-1)$ and $E^{-}(j-1)$ are elements of $X_{j-1}$. Lemma 1 completes the proof. $\blacksquare$

**Claim.** After step $j$ (after line L1 for $j = 0$, after line L6 for $j \ge 1$), $hi = E^{+}(j)$, $lo = E^{-}(j)$ and $best = B(j)$.

*Proof.* By induction on $j$.

*Base.* $X_0 = \{A[0]\}$, so $E^{+}(0) = E^{-}(0) = B(0) = A[0]$, which line L1 sets.

*Step, $j \ge 1$.* Before line L3, $hi = E^{+}(j-1)$ and $lo = E^{-}(j-1)$ by induction. After line L3, $(hi, lo) = (u, v)$ as in Lemma 2. Line L4 sets $hi = \max(A[j], u A[j]) = E^{+}(j)$. Line L5 uses $lo = v$, which line L4 did not change, and sets $lo = \min(A[j], v A[j]) = E^{-}(j)$. A subarray of $A[0..j]$ either ends at $j$ or lies in $A[0..j-1]$, so $B(j) = \max(B(j-1), E^{+}(j))$, which line L6 computes from $best = B(j-1)$. $\blacksquare$

**Theorem.** MAX-PRODUCT returns $B(n-1)$, the largest product of a non-empty subarray of $A$.

*Proof.* Apply the claim with $j = n - 1$. The loop runs $n - 1$ times with $O(1)$ arithmetic operations each, so the algorithm stops. $\blacksquare$
