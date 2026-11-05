---
title: Prefix sum hash counting counts the subarrays with sum k
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[0..n-1]$ and a target $k$. Let $P_0 = 0$ and $P_m = A[0] + \dots + A[m-1]$ for $1 \le m \le n$, so that the subarray $A[i..j]$ has sum $P_{j+1} - P_i$. Treat the hash table $C$ as a map from values to counts, where an absent key has count $0$. For $0 \le j \le n$ let $N_j$ be the number of pairs $(i, l)$ with $0 \le i \le l < j$ and $P_{l+1} - P_i = k$.

**Claim.** At the start of step $j$ (and, for $j = n$, when the loop ends):

1. $p = P_j$;
2. for every value $v$, $C[v] = \#\{m : 0 \le m \le j,\ P_m = v\}$;
3. $count = N_j$.

*Proof.* By induction on $j$.

*Base, $j = 0$.* Line L1 sets $p = 0 = P_0$, $C[0] = 1$ and every other count to $0$, which matches the one value $P_0 = 0$, and $count = 0 = N_0$, because there is no pair with $l < 0$.

*Step.* Assume the claim at the start of step $j < n$. Line L3 sets $p = P_j + A[j] = P_{j+1}$. The pairs counted by $N_{j+1}$ but not by $N_j$ are those with $l = j$, that is, the starts $i$ with $0 \le i \le j$ and $P_i = P_{j+1} - k$. By part 2, line L4 adds exactly their number, $C[P_{j+1} - k]$, so $count = N_{j+1}$. Line L5 then adds one to $C[P_{j+1}]$, so part 2 holds with $j + 1$ in place of $j$. $\blacksquare$

**Theorem.** COUNT-SUM-K returns the number of subarrays of $A$ with sum $k$.

*Proof.* By the claim with $j = n$, line L6 returns $N_n$, the number of pairs $0 \le i \le l \le n - 1$ with $A[i] + \dots + A[l] = k$. The loop runs $n$ times with one lookup and one update of $C$, so the algorithm stops. $\blacksquare$

**Remark (order of lines L4 and L5).** If line L5 came before line L4, part 2 would include $m = j + 1$ at the lookup, and for $k = 0$ line L4 would also count the pair $i = j + 1$, which is the empty subarray $A[j+1..j]$. So the order of the two lines is needed for $k = 0$, and does no harm for $k \ne 0$.
