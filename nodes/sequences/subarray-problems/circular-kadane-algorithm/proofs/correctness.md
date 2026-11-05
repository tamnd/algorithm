---
title: The circular Kadane algorithm returns the best circular subarray sum
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[0..n-1]$ with $n \ge 1$. Write $S(i, j) = A[i] + \dots + A[j]$ for $i \le j$, and $S(i, i - 1) = 0$. Let $T = S(0, n - 1)$. A *plain* subarray is a pair $(i, j)$ with $0 \le i \le j \le n - 1$, with sum $S(i, j)$. A *wrapping* subarray is a pair $(i, j)$ with $0 \le j < i \le n - 1$, with sum $W(i, j) = S(i, n - 1) + S(0, j)$. Let $S^*_{\max}$ and $S^*_{\min}$ be the largest and smallest plain sums, and $C^*$ the largest sum over plain and wrapping subarrays.

**Lemma 1 (the scans).** After the loop, $best = S^*_{\max}$, $worst = S^*_{\min}$ and $T = S(0, n - 1)$.

*Proof.* Line L3 is the recurrence $E(j) = A[j] + \max(E(j-1), 0)$ of Kadane's algorithm together with the running maximum of $E$, so the invariant of that algorithm gives $best = S^*_{\max}$. Line L4 is the same recurrence for $B = -A$, with every value negated: if $hi'$ and $best'$ are the values of line L3 on $B$, then $lo = -hi'$ and $worst = -best'$ at each step, by induction on $j$, because $-(B[j] + \max(x, 0)) = A[j] + \min(-x, 0)$. So $worst = -\max(\text{plain sums of } B) = S^*_{\min}$. Line L5 adds each item once. $\blacksquare$

**Lemma 2 (complement).** For a wrapping subarray $(i, j)$, $W(i, j) = T - S(j + 1, i - 1)$. The map $(i, j) \mapsto (j + 1, i - 1)$ is a bijection from wrapping subarrays to the blocks $(a, b)$ with $1 \le a \le b + 1 \le n - 1$, that is, to the plain subarrays that contain neither $A[0]$ nor $A[n-1]$, together with the empty blocks $(a, a - 1)$ for $1 \le a \le n - 1$.

*Proof.* The items $0..n-1$ split into $0..j$, $j+1..i-1$ and $i..n-1$, so $T = S(0, j) + S(j + 1, i - 1) + S(i, n - 1)$. The inverse map is $(a, b) \mapsto (b + 1, a - 1)$, and the conditions $0 \le j < i \le n - 1$ match $1 \le a \le b + 1 \le n - 1$. $\blacksquare$

**Lemma 3.** Every wrapping sum is at most $\max(T - S^*_{\min}, T)$, and $T \le S^*_{\max}$. Also, if $S^*_{\min}$ is reached by a plain block $(a, b)$ other than the whole array, then some circular subarray has sum $T - S^*_{\min}$.

*Proof.* By Lemma 2 a wrapping sum is $T - S(a, b)$ for a block that is either a plain subarray, so $S(a, b) \ge S^*_{\min}$, or empty, so the sum is $T$. And $T = S(0, n - 1) \le S^*_{\max}$. For the second part, let $(a, b) \ne (0, n - 1)$ reach $S^*_{\min}$. If $1 \le a$ and $b \le n - 2$, Lemma 2 gives a wrapping subarray with sum $T - S(a, b)$. If $a = 0$, then $b \le n - 2$ and the plain subarray $(b + 1, n - 1)$ has sum $T - S(0, b)$. If $b = n - 1$, then $a \ge 1$ and the plain subarray $(0, a - 1)$ has sum $T - S(a, n - 1)$. $\blacksquare$

**Theorem.** CIRCULAR-KADANE returns $C^*$.

*Proof.* By Lemma 1, $best = S^*_{\max}$ and $worst = S^*_{\min}$.

*Case $best < 0$.* Every item is negative, because a single item is a plain subarray. A circular subarray contains some item $A[k]$, and its other items are negative, so its sum is at most $A[k] \le S^*_{\max}$. Plain subarrays reach $S^*_{\max}$, so $C^* = S^*_{\max}$, which line L6 returns.

*Case $best \ge 0$.* By Lemma 3 every wrapping sum is at most $\max(T - S^*_{\min}, S^*_{\max})$, and every plain sum is at most $S^*_{\max}$. So $C^* \le \max(S^*_{\max}, T - S^*_{\min})$. For the other direction, $S^*_{\max}$ is reached by a plain subarray. If $S^*_{\min}$ is reached by a block other than the whole array, Lemma 3 gives a circular subarray with sum $T - S^*_{\min}$. Otherwise $S^*_{\min} = T$ and $T - S^*_{\min} = 0 \le best$. In both cases $\max(S^*_{\max}, T - S^*_{\min}) \le C^*$. So line L7 returns $C^*$.

*Termination.* The loop runs $n - 1$ times with $O(1)$ work per step. $\blacksquare$
