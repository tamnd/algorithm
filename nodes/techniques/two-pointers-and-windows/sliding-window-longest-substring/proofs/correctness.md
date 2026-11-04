---
title: The sliding window returns the leftmost longest substring without repeated characters
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The string is $s = s_0 \cdots s_{n-1}$. A substring $s[i \ldots j]$ with $i \le j$ is *repeat-free* if its $j - i + 1$ characters are distinct. For $0 \le r \le n - 1$ let $L(r)$ be the smallest $i \le r$ such that $s[i \ldots r]$ is repeat-free; it exists since $s[r \ldots r]$ is repeat-free. Let $p(r)$ be the largest $j < r$ with $s_j = s_r$, or $-1$.

**Lemma 1 (closed under sub-intervals).** If $s[i \ldots j]$ is repeat-free and $i \le i' \le j' \le j$, then $s[i' \ldots j']$ is repeat-free. So for each $r$, $s[i \ldots r]$ is repeat-free if and only if $L(r) \le i \le r$.

*Proof.* The characters of $s[i' \ldots j']$ are a subset of those of $s[i \ldots j]$, at distinct positions. For the second part, if $s[L(r) \ldots r]$ is repeat-free, so is each $s[i \ldots r]$ with $i \ge L(r)$; and $s[i \ldots r]$ with $i < L(r)$ is not repeat-free by the choice of $L(r)$. $\blacksquare$

**Lemma 2.** $L(0) = 0$, and $L(r) = \max(L(r-1), p(r) + 1)$ for $r \ge 1$.

*Proof.* For $i \le r - 1$, the window $s[i \ldots r]$ is repeat-free if and only if $s[i \ldots r-1]$ is repeat-free and no $j$ with $i \le j \le r - 1$ has $s_j = s_r$. By Lemma 1 the first condition is $i \ge L(r-1)$. The second is $i > p(r)$, since $p(r)$ is the last earlier copy of $s_r$. The window $s[r \ldots r]$ is always repeat-free, and $\max(L(r-1), p(r) + 1) \le r$ because $L(r-1) \le r - 1$ and $p(r) \le r - 1$. So the smallest valid $i$ is $\max(L(r-1), p(r) + 1)$. $\blacksquare$

**Claim.** After step $r$ of the loop of line L2:

> **(U)** $l = L(r)$; $last[c]$ is the largest $j \le r$ with $s_j = c$, or $-1$ if there is none, for every character $c$; $best = \max_{r' \le r} (r' - L(r') + 1)$; and $start$ is the smallest $i$ such that $s[i \ldots i + best - 1]$ is repeat-free and $i + best - 1 \le r$.

On return, $best$ is the length of a longest repeat-free substring of $s$, and $start$ is the smallest start of one; for $n = 0$ the result is $(0, 0)$.

*Proof.* By induction on $r$. Before step 0, by line L1, $l = 0$, $best = 0$, $start = 0$ and $last[c] = -1$ for all $c$.

*Line L3.* Before line L4 of step $r$, $last[s_r]$ is the largest $j \le r - 1$ with $s_j = s_r$, which is $p(r)$ (for $r = 0$, it is $-1 = p(0)$). The value of $l$ before line L3 is $L(r-1)$ for $r \ge 1$, and 0 for $r = 0$. So line L3 sets $l$ to $\max(L(r-1), p(r) + 1) = L(r)$ by Lemma 2, and to $\max(0, 0) = 0 = L(0)$ for $r = 0$.

*Line L4.* It sets $last[s_r] = r$, the largest $j \le r$ with $s_j = s_r$. The other entries are unchanged and stay correct.

*Line L5.* The longest repeat-free substring that ends at $r$ is $s[L(r) \ldots r]$, by Lemma 1, of length $r - L(r) + 1$. If this is larger than $best$, line L5 sets $best$ to it and $start$ to $L(r)$. The new $best$ is $\max_{r' \le r}(r' - L(r') + 1)$. A repeat-free substring of the new length that ends at $r' \le r$ must have $r' = r$, since all earlier ones were shorter; and the only one that ends at $r$ with this length starts at $L(r)$. So $start$ is the smallest start. If the length is not larger, $best$ and $start$ stay. The new best substrings that end at $r$, if any, start at $L(r) = r - best + 1$, which is larger than the old $start$; so $start$ stays the smallest start.

*Result.* Every repeat-free substring $s[i \ldots j]$ has $i \ge L(j)$ by Lemma 1, so its length is at most $j - L(j) + 1 \le best$ after step $n - 1$. And $s[start \ldots start + best - 1]$ is repeat-free, by (U). For $n = 0$ the loop does not run and line L6 returns $(0, 0)$. $\blacksquare$

**No skipped answer.** The left end only increases, by Lemma 2 and line L3. A start $i < L(r)$ that the left end has passed gives a window $s[i \ldots r]$ with a repeat, and every window $s[i \ldots r']$ with $r' \ge r$ contains $s[i \ldots r]$, so it has the same repeat by Lemma 1. So no repeat-free window with start $i$ and end at or after $r$ exists, and passing $i$ loses no candidate.

**Termination and cost.** The loop of line L2 runs $n$ times, and each iteration does $O(1)$ table operations. Line L1 initializes a table of size $\sigma$. The total time is $\Theta(n + \sigma)$. $\blacksquare$
