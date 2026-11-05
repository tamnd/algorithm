---
title: Horspool outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, HORSPOOL$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, which is correct. Let $m \ge 1$. After lines L3 and L4, for every character $c$,

$$\mathrm{shift}[c] = \min\big(\{m\} \cup \{\, m - 1 - k : 0 \le k \le m - 2,\ P[k] = c \,\}\big),$$

because line L4 visits $k$ in increasing order and the last write for $c$ is its largest $k \le m - 2$, which gives the smallest value $m - 1 - k$. In particular $1 \le \mathrm{shift}[c] \le m$.

**Lemma (safe shift).** Let $s \le n - m$ and $c = T[s + m - 1]$. No shift $s'$ with $s < s' < s + \mathrm{shift}[c]$ is valid.

*Proof.* Let $s' = s + d$ with $1 \le d < \mathrm{shift}[c] \le m$ be valid. The text position $s + m - 1$ lies in the window at $s'$, because $s' \le s + m - 1 \le s' + m - 1$. It is aligned with the pattern position $k = m - 1 - d$, and $0 \le k \le m - 2$. Validity gives $P[k] = T[s + m - 1] = c$, so $m - 1 - k = d$ belongs to the set in the definition of $\mathrm{shift}[c]$, and $\mathrm{shift}[c] \le d$, a contradiction. $\square$

**Theorem.** The claim holds.

*Proof.* Invariant at line L6: the output is the increasing list of the valid shifts smaller than $s$. It holds for $s = 0$. In an iteration with $s \le n - m$, lines L7 and L8 end with $j < 0$ exactly when $P[i] = T[s+i]$ for all $0 \le i < m$, so line L9 outputs $s$ exactly when it is valid, after all smaller outputs. By the lemma, no valid shift lies strictly between $s$ and the new value $s + \mathrm{shift}[c]$, so the invariant holds again. Each iteration increases $s$ by at least 1, so the loop stops after at most $n - m + 1$ iterations, with $s > n - m$; then all valid shifts are smaller than $s$ and have been output. $\blacksquare$
