---
title: Backward DAWG matching outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, BACKWARD-DAWG-MATCHING$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, so let $m \ge 1$. A shift $s'$ is *valid* when $0 \le s' \le n - m$ and $T[s' \ldots s'+m-1] = P$.

**The automaton.** We use the defining property of the suffix automaton $\mathcal{A}$ of $P^R$: for every string $x$, $\delta(q_0, x)$ is defined exactly when $x$ is a factor of $P^R$, and then it lies in $F$ exactly when $x$ is a suffix of $P^R$. Since reversal maps factors to factors and suffixes of $P^R$ to prefixes of $P$, for $y = T[s+j \ldots s+m-1]$ and $x = y^R$: $\delta(q_0, x)$ is defined iff $y$ is a factor of $P$, and it is in $F$ iff $y$ is a prefix of $P$.

**Lemma 1 (the scan).** At window $s$, after line L8 has run with the new value $j$, $q = \delta(q_0, (T[s+j \ldots s+m-1])^R)$, or nil if that string is not a factor of $P^R$.

*Proof.* By induction on the number of steps: the characters are fed in the order $T[s+m-1], T[s+m-2], \ldots, T[s+j]$, which spells $(T[s+j \ldots s+m-1])^R$, and once $q$ is nil the loop stops. $\square$

Let $j^*$ be the value of $j$ when the loop of line L7 ends. Either $j^* = 0$ and $q \ne$ nil, or $q = $ nil and $T[s+j^* \ldots s+m-1]$ is not a factor of $P$.

**Lemma 2 (occurrence).** Line L10 outputs $s$ if and only if $s$ is valid.

*Proof.* Line L10 outputs $s$ when $j = 0$ and $q \in F$, that is, by Lemma 1, when $T[s \ldots s+m-1]$ is a prefix of $P$; since its length is $m$, this means it equals $P$. Conversely, if $s$ is valid, every $T[s+j \ldots s+m-1]$ is a suffix of $P$ and hence a factor, so the scan never meets nil, reaches $j = 0$, and the whole window $P$ is a prefix of $P$, so $q \in F$ and $s$ is output. $\square$

**Lemma 3 (safe shift).** At line L11, $1 \le \mathit{shift} \le m$, and no shift $s + d$ with $0 < d < \mathit{shift}$ is valid.

*Proof.* $\mathit{shift}$ starts at $m$ and is only set to values $j > 0$, so $1 \le \mathit{shift} \le m$. Moreover, at the end, $\mathit{shift}$ is the smallest $j$ with $j^* \le j$, $0 < j < m$ and $T[s+j \ldots s+m-1]$ a prefix of $P$, or $m$ if there is none, because line L10 runs for each such $j$ in decreasing order.

Let $s + d$ be valid with $0 < d < \mathit{shift} \le m$. Then $T[s+d \ldots s+m-1] = P[0 \ldots m-d-1]$ is a prefix of $P$.

- If $d \ge j^*$, the scan read position $s + d$, the string $T[s+d \ldots s+m-1]$ is a prefix of $P$, and $0 < d < m$, so line L10 set $\mathit{shift}$ to at most $d$, a contradiction.
- If $d < j^*$, then $j^* > 0$, so the scan stopped with $q = $ nil and $T[s+j^* \ldots s+m-1]$ is not a factor of $P$. But the occurrence at $s + d$ covers the text positions $s + d$ to $s + d + m - 1 \ge s + m - 1$, and $d < j^*$, so $T[s+j^* \ldots s+m-1] = P[j^* - d \ldots m - 1 - d]$ is a factor of $P$, a contradiction. $\square$

**Proof of the claim.** By Lemma 2, each tested window is output exactly when it is valid. By Lemma 3, $s$ increases by at least 1 at each iteration and no valid shift is skipped, so every valid shift $\le n - m$ is tested, and the output is in increasing order. The inner loop runs at most $m$ times per window and the outer loop at most $n - m + 1$ times, so the algorithm stops. $\blacksquare$
