---
title: Kadane's algorithm returns a maximum-sum subarray
proves: [correctness]
status: full
---

We use the pseudocode of the page, on $A[1..n]$ with $n \ge 1$. For $1 \le j \le n$ let $E(j) = \max_{1 \le i \le j} \sum_{k=i}^{j} A[k]$, the largest sum of a subarray ending at $j$, and let $B(j) = \max_{1 \le i \le l \le j} \sum_{k=i}^{l} A[k]$, the largest sum of a subarray of $A[1..j]$. Write $S(i, l) = \sum_{k=i}^{l} A[k]$.

**Lemma 1.** $E(1) = A[1]$, and $E(j) = A[j] + \max(E(j-1), 0)$ for $j \ge 2$.

*Proof.* The subarrays ending at $j$ are $A[j..j]$, with sum $A[j]$, and $A[i..j]$ for $1 \le i \le j - 1$, with sum $S(i, j-1) + A[j]$. The largest of the second kind is $E(j-1) + A[j]$. So $E(j) = \max(A[j], E(j-1) + A[j]) = A[j] + \max(0, E(j-1))$. $\blacksquare$

**Lemma 2.** $B(1) = A[1]$, and $B(j) = \max(B(j-1), E(j))$ for $j \ge 2$.

*Proof.* A subarray of $A[1..j]$ either ends at $j$ or is a subarray of $A[1..j-1]$. $\blacksquare$

**Claim.** After step $j$ (after line L1 for $j = 1$, after line L5 for $j \ge 2$):

1. $cur = E(j)$, $1 \le c \le j$ and $S(c, j) = cur$;
2. $best = B(j)$, $1 \le bi \le bj \le j$ and $S(bi, bj) = best$.

*Proof.* By induction on $j$.

*Base, $j = 1$.* Line L1 sets $cur = A[1] = E(1)$ with $c = 1$, and $best = A[1] = B(1)$ with $(bi, bj) = (1, 1)$.

*Step, $j \ge 2$.* By induction, before line L3 we have $cur = E(j-1)$ and $S(c, j-1) = E(j-1)$.

If $E(j-1) < 0$, line L3 sets $cur = A[j]$ and $c = j$. Then $S(c, j) = A[j]$, and $A[j] = A[j] + \max(E(j-1), 0)$ since the max is $0$. If $E(j-1) \ge 0$, line L4 sets $cur = E(j-1) + A[j]$ and keeps $c$, and $S(c, j) = S(c, j-1) + A[j] = E(j-1) + A[j]$, with the max equal to $E(j-1)$. In both cases $cur = E(j)$ by Lemma 1, and $S(c, j) = cur$ with $1 \le c \le j$. Part 1 holds.

Before line L5, $best = B(j-1)$ with $S(bi, bj) = best$, by induction. If $cur > best$, line L5 sets $best = cur = E(j)$ and $(bi, bj) = (c, j)$, so $S(bi, bj) = E(j)$ by part 1. Otherwise $best = B(j-1) \ge E(j)$ is kept. In both cases $best = \max(B(j-1), E(j)) = B(j)$ by Lemma 2, and part 2 holds. $\blacksquare$

**Theorem.** Line L6 returns $(B(n), bi, bj)$ with $S(bi, bj) = B(n)$, the largest sum of a non-empty subarray of $A$.

*Proof.* The loop ends after step $n$ (or at once if $n = 1$). Apply the claim with $j = n$. The loop runs $n - 1$ times and each step does $O(1)$ work, so the algorithm stops after $\Theta(n)$ operations. $\blacksquare$
