---
title: Quick Search outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, QUICK-SEARCH$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, which is correct. Let $m \ge 1$. Since line L4 visits $k$ in increasing order, the last write for $c$ is its largest $k$, so after line L4

$$\mathrm{qs}[c] = \min\big(\{m + 1\} \cup \{\, m - k : 0 \le k \le m - 1,\ P[k] = c \,\}\big), \quad 1 \le \mathrm{qs}[c] \le m + 1.$$

**Lemma (safe shift).** Let $s < n - m$ and $c = T[s + m]$. No shift $s'$ with $s < s' < s + \mathrm{qs}[c]$ and $s' \le n - m$ is valid.

*Proof.* Let $s' = s + d$ with $1 \le d < \mathrm{qs}[c]$, so $d \le m$. The text position $s + m$ lies in the window at $s'$ and faces the pattern position $k = m - d$, with $0 \le k \le m - 1$. If $s'$ were valid, then $P[k] = c$, so $m - k = d$ is in the set defining $\mathrm{qs}[c]$, and $\mathrm{qs}[c] \le d$, a contradiction. $\square$

**Theorem.** The claim holds.

*Proof.* Invariant at line L6: the output is the increasing list of the valid shifts smaller than $s$. It holds for $s = 0$. In an iteration with $s \le n - m$, lines L7 and L8 end with $j = m$ exactly when the window equals $P$, so line L9 outputs $s$ exactly when it is valid, after all smaller ones. If $s = n - m$, line L10 stops, and every valid shift, being at most $n - m = s$, has been output. Otherwise $s + m < n$, line L11 reads an existing character, and by the lemma no valid shift lies strictly between $s$ and the new $s$, so the invariant holds. Each iteration increases $s$ by at least 1, so the loop ends after at most $n - m + 1$ iterations, either at line L10 or with $s > n - m$; in both cases all valid shifts have been output. $\blacksquare$
