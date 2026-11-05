---
title: Two pointers with distinct counts finds the longest window with at most k values
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[0..n-1]$ and $k \ge 0$. For $0 \le i \le j \le n$ let $D(i, j)$ be the number of distinct values in $A[i..j)$, with $D(j, j) = 0$. Call $A[i..j)$ valid if $D(i, j) \le k$. For $0 \le j \le n$ let $L(j)$ be the smallest $i \le j$ such that $A[i..j)$ is valid. It exists because $A[j..j)$ is valid.

**Lemma 1 (monotone).** If $i \le i' \le j' \le j$ then $D(i', j') \le D(i, j)$. So a subarray of a valid subarray is valid, and $L(j) \le L(j + 1)$ for $0 \le j < n$.

*Proof.* The values of $A[i'..j')$ are among those of $A[i..j)$. If $i < L(j)$ then $A[i..j)$ is not valid, so neither is $A[i..j+1)$, which contains it. Hence $L(j + 1) \ge L(j)$. $\blacksquare$

**Invariant.** At the start of the step for $j$ (line L2), $i = L(j)$, the table $cnt$ maps each value of $A[i..j)$ to its positive count and holds no other key, and $d = D(i, j)$. After line L7 of the same step, the same holds with $j + 1$ in place of $j$.

*Proof.* For $j = 0$, line L1 gives $i = 0 = L(0)$, an empty table, and $d = 0$.

Assume the invariant at the start of the step for $j$. Lines L3 and L4 add one to the count of $A[j]$, and add a key and one to $d$ exactly when $A[j]$ is not in $A[i..j)$. So the table and $d = D(i, j + 1)$ are correct for the window $A[i..j+1)$. Now $i = L(j) \le L(j + 1)$ by Lemma 1.

Each run of lines L6 and L7 takes $A[i]$ out of the window: it lowers its count, deletes the key and lowers $d$ when the count reaches zero, which is when $A[i]$ is not in $A[i+1..j+1)$. So the table and $d$ stay correct for the window $A[i..j+1)$ with the new $i$. The loop runs while $d > k$, that is while the window is not valid. If $i < L(j + 1)$ the window is not valid by the definition of $L$, so the loop continues. At $i = L(j + 1)$ the window is valid and the loop stops. Since the loop starts with $i \le L(j + 1)$, it stops with $i = L(j + 1)$. $\blacksquare$

**Theorem.** DISTINCT-WINDOW returns $best = \max\{\, j - i : 0 \le i \le j \le n,\ D(i, j) \le k \,\}$ and a start $start$ with $D(start, start + best) \le k$.

*Proof.* For a fixed end $j' = j + 1$, the valid subarrays $A[i..j')$ are those with $i \ge L(j')$, by Lemma 1, and the longest of them has length $j' - L(j')$. By the invariant, line L8 tests exactly this length, $j + 1 - i$, for every $j' = 1, \dots, n$. The end $j' = 0$ gives only the empty subarray, with length $0$, which is the starting value of $best$ in line L1. So after the loop, $best$ is the maximum over all ends, and $start$ is the start of a window of that length that was valid when it was recorded. Each step moves $j$ once, and $i$ moves at most $n$ times in total because $i \le j + 1$, so the algorithm stops. $\blacksquare$
