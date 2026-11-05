---
title: The Z-algorithm computes the Z array
proves: [correctness, termination]
status: full
---

**Claim.** For a string $S[0 \ldots N-1]$, Z-ARRAY$(S)$ stops and returns $Z$ with $Z[0] = N$ and, for $1 \le k < N$, $Z[k] = \operatorname{lcp}(S, S[k \ldots N-1])$, the length of the longest common prefix. Z-MATCH$(T, P)$ outputs exactly the valid shifts in increasing order.

**Termination.** The loop of line L2 runs $N - 1$ times. In the loop of lines L4 and L5, $k + Z[k]$ increases at each pass and is at most $N$, so the loop stops.

**Invariant.** At the start of the iteration for $k$:

> **(I)** $Z[j] = \operatorname{lcp}(S, S[j \ldots])$ for $1 \le j < k$; $r = \max(\{0\} \cup \{\, j + Z[j] : 1 \le j < k \,\})$; and if $r > 0$ then $1 \le l < k$, $r = l + Z[l]$.

It holds for $k = 1$ with $l = r = 0$. From (I) with $r > 0$, $S[l \ldots r-1] = S[0 \ldots r-l-1]$ by the definition of $Z[l]$.

**Lemma.** Let $z^* = \operatorname{lcp}(S, S[k \ldots])$ and let $z_0$ be the value set by line L3. Then $z_0 \le z^*$, and if $z_0 < r - k$ then $z_0 = z^*$.

*Proof.* If $k \ge r$, $z_0 = 0 \le z^*$, and the second part is empty since $r - k \le 0$. Let $k < r$, so $l < k < r$, and let $k' = k - l \ge 1$. The box gives $S[k \ldots r-1] = S[k' \ldots r-l-1]$, a string of length $r - k$.

First, $z_0 \le z^*$. Since $k' < k$, $Z[k'] = \operatorname{lcp}(S, S[k' \ldots])$ by (I). With $z_0 = \min(r - k, Z[k'])$, for $i < z_0$ we have $S[i] = S[k' + i]$ (as $i < Z[k']$) and $S[k' + i] = S[k + i]$ (as $i < r - k$, inside the box). So $S[0 \ldots z_0 - 1] = S[k \ldots k + z_0 - 1]$.

Second, assume $z_0 < r - k$, so $z_0 = Z[k'] < r - k$. Then $k' + Z[k'] < r - l \le N$, so the character $S[k' + Z[k']]$ exists, and it differs from $S[Z[k']]$ by maximality of $Z[k']$. Since $Z[k'] < r - k$, the box gives $S[k + Z[k']] = S[k' + Z[k']] \ne S[Z[k']]$. So the match at $k$ stops at $Z[k']$ and $z^* = z_0$. $\square$

**Step.** By the lemma, $z_0 \le z^*$, and $S[0 \ldots z_0 - 1] = S[k \ldots k + z_0 - 1]$. The loop of lines L4 and L5 keeps $S[0 \ldots Z[k]-1] = S[k \ldots k+Z[k]-1]$ and stops at the first $Z[k] \ge z_0$ where $k + Z[k] = N$ or $S[Z[k]] \ne S[k + Z[k]]$, which is $z^*$. Line L6 updates $r$ to $\max(r, k + Z[k])$ with $l = k$ when $r$ changes, so (I) holds for $k + 1$. At the end, (I) for $k = N$ gives every value, and $Z[0] = N$ by line L1.

**Matching.** Let $S = P \$ T$ with $|S| = m + 1 + n$ and $m \ge 1$, and let $0 \le s \le n - m$. Position $m + 1 + s$ holds $T[s]$. Because $\$$ equals no character of $P$ or $T$, the common prefix of $S$ and $S[m+1+s \ldots]$ cannot include $S[m] = \$$ matched against a character of $T$, so $Z[m+1+s] \le m$, and $Z[m+1+s] = m$ exactly when $T[s \ldots s+m-1] = P$. Line L11 visits the shifts in increasing order, and none when $m > n$. For $m = 0$, line L9 outputs all shifts $0, \ldots, n$, which are all valid. $\blacksquare$
