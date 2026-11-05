---
title: The positive-sum sliding window returns the shortest window
proves: [correctness]
status: full
---

We use the pseudocode of the page, on $A[0..n-1]$ with $A[i] \ge 0$ for all $i$ and $s > 0$. Write $S(i, j) = A[i] + \dots + A[j]$ for $i \le j$ and $S(i, i-1) = 0$. For $0 \le i \le n - 1$ let $e(i)$ be the smallest $j$ with $i \le j \le n - 1$ and $S(i, j) \ge s$, or $\infty$ if there is none. Let $D = \min_i (e(i) - i + 1)$, with $D = \infty$ if every $e(i)$ is $\infty$. The answer is $D$, or $0$ when $D = \infty$.

**Lemma 1 (monotone sums).** If $i \le i'$ and $j' \le j$, then $S(i', j') \le S(i, j)$.

*Proof.* $S(i, j) - S(i', j')$ is a sum of items, so it is not negative. $\blacksquare$

**Lemma 2 (inner loop).** Suppose that before line L4 of step $r$ we have $t = S(l, r)$ and $S(l, r - 1) < s$, with $l \le r$. Then the inner loop stops. Each time line L5 runs, $e(l) = r$ for the current $l$, and it records $r - l + 1 = e(l) - l + 1$. When the loop stops, $t = S(l, r) < s$ and $l \le r + 1$.

*Proof.* The loop keeps $t = S(l, r)$, since line L6 removes $A[l]$ and then moves $l$. When $l = r + 1$, $t = S(r + 1, r) = 0 < s$, so the loop runs at most $r - l + 1$ times. Each time the test $t \ge s$ passes with $l \le r$, we have $S(l, r) \ge s$. Also $S(l, r - 1) < s$: for the first pass this is the hypothesis, and for a later pass with a larger $l$ it follows from Lemma 1 and the hypothesis on the first $l$. So $r$ is the least end with sum at least $s$ from start $l$, that is, $e(l) = r$. $\blacksquare$

**Claim.** At the start of step $r$, for $0 \le r \le n$ (with step $n$ meaning the moment the outer loop ends):

1. $0 \le l \le r$ and $t = S(l, r - 1) < s$;
2. for every $i < l$, $e(i) \le r - 1$ and $best \le e(i) - i + 1$;
3. if $best < \infty$, then $best = e(i) - i + 1$ for some $i < l$.

*Proof.* By induction on $r$.

*Base, $r = 0$.* Line L1 sets $l = 0$, $t = 0 = S(0, -1) < s$ and $best = \infty$. Parts 2 and 3 hold, because there is no $i < 0$ and $best = \infty$.

*Step.* Assume the claim at the start of step $r < n$. Line L3 sets $t = S(l, r)$, and part 1 gives $S(l, r - 1) < s$. Let $l_0$ be $l$ at this moment and $l_1$ be $l$ after the inner loop. By Lemma 2 the inner loop stops with $t = S(l_1, r) < s$ and $l_1 \le r + 1$, so part 1 holds at the start of step $r + 1$.

The starts $i$ with $l_0 \le i < l_1$ are those that the inner loop drops. For each of them Lemma 2 gives $e(i) = r$, and line L5 makes $best \le r - i + 1 = e(i) - i + 1$. For $i < l_0$, part 2 gave $e(i) \le r - 1$ and $best \le e(i) - i + 1$, and $best$ only decreases. So part 2 holds for every $i < l_1$ at the start of step $r + 1$. Every value that line L5 writes is $e(i) - i + 1$ for a dropped start $i$, which gives part 3. $\blacksquare$

**Theorem.** MIN-WINDOW returns $D$ if $D < \infty$, and $0$ otherwise.

*Proof.* Apply the claim at $r = n$. For $i < l$, part 2 gives $best \le e(i) - i + 1$. For $i \ge l$, Lemma 1 and part 1 give $S(i, n - 1) \le S(l, n - 1) = t < s$, so $S(i, j) < s$ for every $j \ge i$ and $e(i) = \infty$. So $best \le D$. Part 3 gives $best \ge D$ when $best$ is finite, and if $best = \infty$ then no start has a finite $e(i)$, by part 2 applied to $i < l$, so $D = \infty$. So $best = D$, and lines L7 and L8 return the answer.

*Termination and cost.* The outer loop runs $n$ times. Line L6 increases $l$, and $l \le r + 1 \le n$ by part 1, so line L6 runs at most $n$ times in all, and line L4 fails exactly $n$ times. The algorithm stops after $O(n)$ operations. $\blacksquare$
