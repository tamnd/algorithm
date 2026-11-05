---
title: The monotonic deque over prefix sums finds a shortest subarray with sum at least K
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[0..n-1]$ and $K$, with $P[0] = 0$ and $P[t] = A[0] + \dots + A[t-1]$. A pair $(i, j)$ with $0 \le i < j \le n$ is valid if $P[j] - P[i] \ge K$, which says that $A[i..j)$ has sum at least $K$. Let $\ell^*$ be the smallest $j - i$ over valid pairs, or $\infty$ if there is none.

**Lemma 1 (order).** After line L7 of each step, the indices in $Q$ increase from front to back, and so do their prefix sums, strictly.

*Proof.* By induction on the steps. Pops keep the property. Line L7 pushes $j$, which is larger than every index in $Q$. After line L6 either $Q$ is empty or $P[\text{back}(Q)] < P[j]$, so the prefix sums still strictly increase. $\blacksquare$

**Lemma 2 (soundness).** Every pair recorded in line L5 is valid.

*Proof.* Line L5 runs only when the test of line L4 holds, that is $P[j] - P[i] \ge K$ for the popped front $i$. The index $i$ was pushed at an earlier step, so $i < j$. $\blacksquare$

So $best \ge \ell^*$ at the end, with $best = \infty$ if no pair is ever recorded.

**Lemma 3 (completeness).** If $\ell^* < \infty$, some pair of length $\ell^*$ is recorded.

*Proof.* Choose a valid pair $(i^*, j^*)$ with $j^* - i^* = \ell^*$. The index $i^*$ is pushed in step $i^*$. We show that it is still in $Q$ when step $j^*$ starts.

Suppose it is popped at the front in a step $t$ with $i^* < t < j^*$. Then $(i^*, t)$ is valid by Lemma 2 and $t - i^* < \ell^*$, a contradiction.

Suppose it is popped at the back in a step $t$ with $i^* < t < j^*$. Then $P[t] \le P[i^*]$, so $P[j^*] - P[t] \ge P[j^*] - P[i^*] \ge K$, and $(t, j^*)$ is valid with $j^* - t < \ell^*$, a contradiction.

So $i^*$ is in $Q$ at the start of step $j^*$. By Lemma 1, every index $i$ in front of $i^*$ has $P[i] < P[i^*] \le P[j^*] - K$, so it passes the test of line L4. Hence the loop of lines L4 and L5 pops all of them, then reaches $i^*$, which passes the test, and pops it with the pair $(i^*, j^*)$. At that point $best \ge \ell^*$, so $best$ becomes $\ell^*$ unless it is already $\ell^*$. $\blacksquare$

**Theorem.** SHORTEST-AT-LEAST returns $best = \ell^*$, and if $\ell^* < \infty$ it returns a valid pair $R$ of length $\ell^*$.

*Proof.* By Lemma 2, every value given to $best$ is the length of a valid pair, so $best \ge \ell^*$ always, and $R$ is valid whenever it is set. By Lemma 3, $best \le \ell^*$ at the end. The algorithm stops because each index is pushed once and popped at most once, so the loops of lines L4 and L6 run at most $n + 1$ times each in total. $\blacksquare$
