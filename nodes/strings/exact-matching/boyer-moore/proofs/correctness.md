---
title: Boyer-Moore outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, BOYER-MOORE$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

We take as given the two tables: $\lambda(c)$ is the largest $k$ with $P[k] = c$, or $-1$; and $\mathrm{gs}[j]$, for $0 \le j < m$, is the smallest $d \ge 1$ such that (G1) $P[i-d] = P[i]$ for all $i$ with $j < i < m$ and $i \ge d$, and (G2) $j - d < 0$ or $P[j-d] \ne P[j]$. That lines L13 to L23 compute these values is the procedure described on the page of the [good-suffix rule](/good-suffix-rule/). For $m = 0$, line L2 outputs every shift, which is correct, so let $m \ge 1$.

**Lemma 1 (the period).** $\mathrm{gs}[0]$ is the smallest period $p$ of $P$, the smallest $d \ge 1$ with $P[i - d] = P[i]$ for all $d \le i < m$.

*Proof.* For $j = 0$, (G2) always holds because $0 - d < 0$, and (G1) asks $P[i-d] = P[i]$ for $\max(1, d) \le i < m$, which is the same as $d \le i < m$ since $d \ge 1$. $\square$

**Lemma 2 (safe shifts).** Let $s$ be a shift tested by the loop of line L5, and let $\Delta$ be the amount added to $s$ by line L11 or L12. Then $\Delta \ge 1$, and no shift $s'$ with $s < s' < s + \Delta$ is valid.

*Proof.* If the window matched (line L11), $\Delta = p \ge 1$. A valid shift $s' = s + d$ with $1 \le d < p$ would give $P[i - d] = T[s + i] = P[i]$ for all $d \le i < m$, since both $P$ at $s$ and $P$ at $s + d$ equal the text there; so $d$ would be a period smaller than $p$, a contradiction.

Otherwise, lines L7 and L8 stopped at $j \ge 0$ with $P[i] = T[s+i]$ for $j < i < m$ and $P[j] \ne T[s+j] = c$, and $\Delta = \max(\mathrm{gs}[j], j - \lambda(c)) \ge \mathrm{gs}[j] \ge 1$. Let $s' = s + d$ be valid with $1 \le d < \Delta$, so $T[s + d + k] = P[k]$ for $0 \le k < m$, and $s + d + m \le n$.

- If $d < \mathrm{gs}[j]$, then (G1) or (G2) fails for $d$. For $j < i < m$ with $i \ge d$, the text position $s + i$ lies in both windows, so $P[i - d] = T[s+i] = P[i]$: (G1) holds. So (G2) fails: $j - d \ge 0$ and $P[j - d] = P[j]$. But the text position $s + j$ is in the window at $s'$, so $P[j - d] = T[s + j] = c \ne P[j]$, a contradiction.
- If $d < j - \lambda(c)$, then $j - d > \lambda(c) \ge -1$, so $0 \le j - d < j < m$ and $P[j-d] = T[s+j] = c$. That is an occurrence of $c$ at the position $j - d > \lambda(c)$, which contradicts the definition of $\lambda$.

In both cases $s'$ is not valid. $\square$

**Theorem.** The claim holds.

*Proof.* We show the invariant: at line L5, the output is the increasing list of the valid shifts smaller than $s$. It holds for $s = 0$. In one iteration, the window at $s$ is tested by lines L6 to L8, which stop with $j < 0$ exactly when $P[i] = T[s+i]$ for all $0 \le i < m$; then $s$ is output, and it is larger than every earlier output. By Lemma 2, no shift strictly between $s$ and $s + \Delta$ is valid, so the invariant holds for $s + \Delta$. Each iteration increases $s$ by at least 1, so the loop stops after at most $n - m + 2$ iterations, with $s > n - m$; the inner loop runs at most $m$ times. At that point every valid shift, being at most $n - m$, is smaller than $s$, so the output is complete. $\blacksquare$
