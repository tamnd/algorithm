---
title: The two-way algorithm outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an ordered alphabet, TWO-WAY$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, so let $m \ge 1$. A shift $s'$ is *valid* when $0 \le s' \le n - m$ and $T[s' \ldots s'+m-1] = P$. Write $\pi = \mathrm{per}(P)$ for the smallest period of $P$.

**Definitions.** For a cut $c$ with $0 \le c \le m$ (between $P[c-1]$ and $P[c]$), an integer $r \ge 1$ is a *repetition length* at $c$ when $P[k] = P[k + r]$ for every $k$ with $c - r \le k < c$, $k \ge 0$ and $k + r < m$. This is the definition of a repetition $w$ of length $r$ (with $w$ and the left part suffixes of one another, $w$ and the right part prefixes of one another) written position by position. The *local period* at $c$ is the smallest repetition length; $\pi$ is always a repetition length, and the cut is *critical* when the local period equals $\pi$.

**Facts about the factorization (Crochemore and Perrin).** Let $(\ell, p)$ be the result of CRITICAL-FACTORIZATION. Then (F1) the cut $c = \ell + 1$ is critical; (F2) $\ell + 1 < \pi$; (F3) if $P[0 \ldots \ell] \ne P[p \ldots p+\ell]$ then $\pi > \max(\ell + 1, m - \ell - 1)$. These are the critical factorization theorem for the cut before the later of the two maximal suffixes, and two lemmas of the same paper; the test `test_critical_factorization` checks all three on every word of length at most 7 over three letters. We also need:

(F4) if $P[0 \ldots \ell] = P[p \ldots p+\ell]$, then $p = \pi$. *Proof.* $p$ is the period of the suffix $P[\ell+1 \ldots m-1]$, so $P[k] = P[k+p]$ for $\ell + 1 \le k < m - p$, and the test gives it for $0 \le k \le \ell$. So $p$ is a period of $P$, $p \ge \pi$. Conversely $\pi$ is a period of the suffix, so $p \le \pi$. $\square$

So in the branch of line L4, $p = \pi$; in the branch of line L14, $q = \max(\ell+1, m-\ell-1) + 1 \le \pi$ by (F3).

**Lemma 1 (no occurrence close to a partial match).** Let $\ell + 1 \le j \le m$, and suppose $T[s+k] = P[k]$ for $\ell + 1 \le k \le j - 1$. Let $s + d$ be valid with $d \ge 1$.
(a) If $j = m$, or if $d \le j - \ell - 1$, then $d \ge \pi$.
(b) If $d \le j - \ell - 1$, then $\pi$ divides $d$.

*Proof.* Let $K$ be the set of $k \ge 0$ with $\ell + 1 \le k + d \le j - 1$. For $k \in K$, $P[k] = T[s+d+k]$ because $s + d$ is valid, and $T[s+d+k] = P[k+d]$ by the hypothesis; so $P[k] = P[k + d]$.

(a) The repetition condition for $d$ at $c = \ell + 1$ asks $P[k] = P[k+d]$ for $k \ge 0$ with $\ell + 1 - d \le k \le \ell$ and $k + d \le m - 1$. Such a $k$ has $k + d \ge \ell + 1$, and $k + d \le j - 1$: if $j = m$ this is the condition $k + d \le m - 1$, and if $d \le j - \ell - 1$ it follows from $k \le \ell$. So $k \in K$ and the condition holds. By (F1), $d \ge \pi$.

(b) Let $e_t = d - t\pi$ for $t = 0, 1, \ldots$ while $e_t \ge 0$. We show by induction on $t$ that $P[k] = P[k + e_t]$ for every $k \in K$. For $t = 0$ this is shown above. For the step, let $k \in K$ and $e_{t+1} \ge 0$: then $k + e_{t+1} \ge 0$ and $k + e_t \le k + d \le j - 1 \le m - 1$, so the period $\pi$ gives $P[k + e_{t+1}] = P[k + e_t] = P[k]$. Now if $e_t \ge 1$, the argument of (a) with $e_t$ in place of $d$ applies: for $k \ge 0$ with $\ell + 1 - e_t \le k \le \ell$, we have $k + d \ge k + e_t \ge \ell + 1$ and $k + d \le \ell + d \le j - 1$, so $k \in K$ and $P[k] = P[k+e_t]$. So $e_t$ is a repetition length at the critical cut and $e_t \ge \pi$, which means $e_{t+1} \ge 0$. The sequence decreases by $\pi$ and stays nonnegative, and it can only stop at a value $e_t$ that is not $\ge 1$, so it reaches 0: $\pi$ divides $d$. $\square$

**Lemma 2 (right-part mismatch).** If the scan of line L8 or L17 stops at $i < m$ with $T[s+i] \ne P[i]$, and $T[s+k] = P[k]$ for $\ell + 1 \le k \le i - 1$, then no shift $s + d$ with $1 \le d < i - \ell$ is valid.

*Proof.* Let $s + d$ be valid with $1 \le d \le i - \ell - 1$. Lemma 1(b) with $j = i$ gives $\pi \mid d$. Then $i - d \ge \ell + 1 \ge 0$, so $T[s+i] = P[i-d] = P[i]$ by the period $\pi$, a contradiction. $\square$

**Lemma 3 (full right part).** If $T[s+k] = P[k]$ for $\ell + 1 \le k \le m - 1$, then no shift $s + d$ with $1 \le d < \pi$ is valid.

*Proof.* Lemma 1(a) with $j = m$. $\square$

**The memory.** In the branch of line L4, the invariant is: at the start of each window $s$, $T[s+k] = P[k]$ for $0 \le k \le \mathit{mem}$. It holds with $\mathit{mem} = -1$ at the start and after line L13. After line L12, the previous window $s$ matched at least the positions $i + 1, \ldots, m - 1$ where $i \le \ell$ is where the left scan stopped (or $i \le \mathit{mem}$ and the window matched fully). The new window is $s + \pi$ and $\mathit{mem} = m - \pi - 1$; for $0 \le k \le m - \pi - 1$, the position $k + \pi$ satisfies $k + \pi \ge \pi > \ell \ge i$, so $T[s + \pi + k] = P[k + \pi] = P[k]$, using the period $\pi$.

With this invariant, the scans of lines L8 and L10 skip only positions known to match, so in both branches: the right scan establishes $T[s+k] = P[k]$ for $\ell + 1 \le k \le i - 1$ and either $i = m$ or a mismatch at $i$; and after a full right scan, the left scan ends with all of $P$ matched exactly when the window is valid (line L11 or L18 outputs $s$ exactly then).

**Proof of the claim.** At each window, $s$ is output exactly when it is valid. The shift is $i - \ell \ge 1$ after a right mismatch, safe by Lemma 2; after a full right scan it is $p = \pi$ or $q \le \pi$, safe by Lemma 3, and at least 1. So $s$ increases at every window, no valid shift is skipped, and the output is in increasing order. Each scan moves $i$ monotonically within $[-1, m]$, so each window takes finite time, and there are at most $n - m + 1$ windows. The procedure MAXIMAL-SUFFIX stops: line L25 strictly increases $ms$, which stays below $m$, so it runs fewer than $m + 1$ times; between two runs of line L25, each step of line L23 or L24 increases $j + k$ by exactly 1, and $j + k < m$ in the loop. $\blacksquare$
