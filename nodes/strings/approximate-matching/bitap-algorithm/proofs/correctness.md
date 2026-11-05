---
title: The bitap algorithm reports exactly the windows with at most k mismatches
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m \ge 1$, $|T| = n$, and $B = \lceil \log_2(k+1) \rceil + 1$, so $2^{B-1} \ge k + 1$. For a vector $V$ of $mB$ bits, $V_i$ is the value of field $i$, bits $iB$ to $iB + B - 1$. Each field of $H$ is $2^{B-1}$. Each field of $M[c]$ is $[P[i] \ne c]$, which is 0 or 1. For $0 \le i \le j$, $\mathrm{mm}(i, j) = |\{ q \le i : P[q] \ne T[j - i + q] \}|$.

**Lemma 1.** $\mathrm{mm}(0, j) = [P[0] \ne T[j]]$, and $\mathrm{mm}(i, j) = \mathrm{mm}(i-1, j-1) + [P[i] \ne T[j]]$ for $1 \le i \le j$.

*Proof.* The first claim is the definition with $i = 0$. For $i \ge 1$, split the positions $q \le i$ into $q \le i - 1$ and $q = i$. The positions $q \le i - 1$ compare $P[q]$ with $T[(j-1) - (i-1) + q]$, and they count $\mathrm{mm}(i-1, j-1)$. The position $q = i$ compares $P[i]$ with $T[j]$. $\square$

**Invariant.** After the loop body for index $j$, for each $i$ with $0 \le i \le m - 1$:

1. $S_i < 2^{B-1}$, and $O_i \in \{0, 2^{B-1}\}$;
2. if $i \le j$ and $O_i = 0$, then $S_i = \mathrm{mm}(i, j)$;
3. if $i \le j$ and $O_i = 2^{B-1}$, then $\mathrm{mm}(i, j) \ge 2^{B-1}$.

Before the loop, $S = O = 0$, so part 1 holds, and parts 2 and 3 are empty. Call this the state after step $-1$.

*Step.* Assume the invariant after step $j - 1$, and let $S'$, $O'$ be the vectors after step $j$.

No carry: in line L5, the shift moves each field $i - 1$ to field $i$ for $1 \le i \le m - 1$, puts 0 in field 0, and drops field $m - 1$ by the reduction mod $2^{mB}$. The shifted field is below $2^{B-1}$ by part 1, and $M[T[j]]_i \le 1$, so the sum of the two is at most $2^{B-1} \le 2^B - 1$. So the addition creates no carry between fields, and after line L5 the field $i$ is $u_i = S_{i-1} + [P[i] \ne T[j]]$ for $i \ge 1$, and $u_0 = [P[0] \ne T[j]]$. Each $u_i$ is at most $2^{B-1}$, so its top bit is set exactly when $u_i = 2^{B-1}$.

Line L6 gives $O'_i = O_{i-1} \vee (\text{top bit of } u_i)$ for $i \ge 1$ and $O'_0 = $ the top bit of $u_0$, where both sides are 0 or $2^{B-1}$ and the shift again moves whole fields. Line L7 gives $S'_i = u_i$ when $u_i < 2^{B-1}$ and $S'_i = 0$ when $u_i = 2^{B-1}$. So part 1 holds after step $j$.

Fix $i \le j$. Case $i = 0$: $u_0 = \mathrm{mm}(0, j) \le 1$ by Lemma 1. If $O'_0 = 0$, then $S'_0 = u_0 = \mathrm{mm}(0, j)$. If $O'_0 = 2^{B-1}$, then $u_0 = 2^{B-1}$, which needs $B = 1$, and then $\mathrm{mm}(0, j) = 1 = 2^{B-1}$. Case $i \ge 1$: then $i - 1 \le j - 1$, so the invariant applies to field $i - 1$ after step $j - 1$.

- If $O_{i-1} = 2^{B-1}$, then $\mathrm{mm}(i-1, j-1) \ge 2^{B-1}$ by part 3, so $\mathrm{mm}(i, j) \ge 2^{B-1}$ by Lemma 1. Also $O'_i = 2^{B-1}$. Part 3 holds, and part 2 is empty.
- If $O_{i-1} = 0$, then $S_{i-1} = \mathrm{mm}(i-1, j-1)$ by part 2, so $u_i = \mathrm{mm}(i, j)$ by Lemma 1. If $u_i < 2^{B-1}$, then $O'_i = 0$ and $S'_i = u_i = \mathrm{mm}(i, j)$, which is part 2. If $u_i = 2^{B-1}$, then $O'_i = 2^{B-1}$ and $\mathrm{mm}(i, j) = 2^{B-1}$, which is part 3.

So the invariant holds after each step. $\square$

**Theorem.** For $m \ge 1$, line L8 reports $i = j - m + 1$ exactly when $0 \le i \le n - m$ and $P$ and $T[i \ldots i + m)$ differ in at most $k$ positions.

*Proof.* Line L8 runs for $j = m - 1, \ldots, n - 1$, which gives exactly the starts $i = j - m + 1$ in $0, \ldots, n - m$. For such $j$, the field index $m - 1$ is at most $j$, and $\mathrm{mm}(m - 1, j)$ is the number of positions where $P$ and $T[j - m + 1 \ldots j]$ differ. By part 1 of the invariant, $S_{m-1} < 2^{B-1}$ and $O_{m-1}$ is 0 or $2^{B-1}$, so field $m - 1$ of $S \vee O$ is $S_{m-1} + O_{m-1}$. If $O_{m-1} = 0$, this value is $\mathrm{mm}(m-1, j)$ by part 2, and the test is the condition of the theorem. If $O_{m-1} = 2^{B-1}$, the value is at least $2^{B-1} \ge k + 1$, so the test fails, and $\mathrm{mm}(m-1, j) \ge 2^{B-1} > k$ by part 3, so the window is not a match either. $\blacksquare$
