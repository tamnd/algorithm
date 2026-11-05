---
title: Naive string matching outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ with $n, m \ge 0$, NAIVE-STRING-MATCHING$(T, P)$ stops, and it outputs exactly the shifts $s$ with $0 \le s \le n - m$ and $T[s \ldots s+m-1] = P$, each one time, in increasing order.

**Setup.** Fix one iteration of line L2, with shift $s$, $0 \le s \le n - m$. So $s + m \le n$, and each index $s + j$ with $0 \le j < m$ is a valid index of $T$.

**Lemma (inner loop).** Each time line L4 tests its condition, the invariant

> **(I)** $0 \le j \le m$ and $T[s + i] = P[i]$ for each $0 \le i < j$

is true.

*Proof.* 1. *Initialization.* Line L3 sets $j = 0$. Then $0 \le j \le m$ because $m \ge 0$, and the second part is about no index, so it is true.

2. *Maintenance.* Assume (I) and that the test of line L4 is true. Then $j < m$ and $T[s + j] = P[j]$. Line L5 sets $j' = j + 1 \le m$. The equality for $i = j$ holds by the test, and the equalities for $i < j$ hold by (I). So (I) holds for $j'$.

3. *Termination.* Each pass of the loop increases $j$ by exactly 1, and (I) gives $j \le m$. So the loop makes at most $m$ passes and stops. $\square$

**Lemma (one shift).** Line L6 outputs $s$ if and only if $T[s \ldots s+m-1] = P$.

*Proof.* When the loop of line L4 stops, (I) holds and the test is false, so $j = m$ or $T[s + j] \ne P[j]$ with $j < m$.

- If $j = m$, then (I) gives $T[s + i] = P[i]$ for each $i < m$, so $s$ is a valid shift, and line L6 outputs it.
- If $j < m$, then $T[s + j] \ne P[j]$, so $s$ is not a valid shift, and line L6 outputs nothing.

The test $j < m$ is evaluated first, so the loop never reads $P[m]$ or $T[s + m]$. $\square$

**Theorem.** The claim holds.

*Proof.* If $m > n$, then $n - m < 0$, line L2 makes no iteration, and the output is empty. This is correct, because no $s$ satisfies $0 \le s \le n - m$. Otherwise, line L2 runs the body for $s = 0, 1, \ldots, n - m$, each value one time and in increasing order, and each body stops by the first lemma. By the second lemma, the body for $s$ outputs $s$ exactly when $s$ is a valid shift. So the output is the list of valid shifts in increasing order, and the algorithm stops after $n - m + 1$ iterations of line L2. If $m = 0$, the loop of line L4 stops at once with $j = 0 = m$, so each $s$ from $0$ to $n$ is output, as the definition requires. $\blacksquare$
