---
title: Apostolico-Giancarlo outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, APOSTOLICO-GIANCARLO$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, which is correct, so let $m \ge 1$. We take as given the tables of the page: $\mathrm{suff}[i]$ is the largest $h \le i + 1$ with $P[i-h+1 \ldots i] = P[m-h \ldots m-1]$, $\lambda(c)$ is the last position of $c$ in $P$ or $-1$, and $\mathrm{gs}$ is the strong good-suffix table. That GOOD-SUFFIX computes $\mathrm{gs}$, that $\mathrm{gs}[0]$ is the smallest period of $P$, and that the shift of lines L13 and L14 skips no valid shift, is proved on the page of Boyer-Moore (its Lemma 2), for a mismatch at a position $i$ with $P[i] \ne T[s+i]$ and $P[i+1 \ldots m-1] = T[s+i+1 \ldots s+m-1]$.

For a text position $t$, let $\mathrm{ms}(t)$ be the largest $k \le \min(m, t + 1)$ with $T[t-k+1 \ldots t] = P[m-k \ldots m-1]$: the length of the longest suffix of $P$ that ends at $t$.

**Invariant (I).** At the start of each window $s$, every entry $\mathrm{skip}[t]$ with $s \le t \le s + m - 1$ is either 0 or equal to $\mathrm{ms}(t)$, and in the second case $\mathrm{ms}(t) > 0$. (With the array indexed by $t \bmod m$, this is the statement about the entry read for $t$.)

Initially all entries are 0. Entries are written only at line L13 or L14 for $t = s + m - 1$; entries for positions that leave the window are cleared at line L15 before a new position with the same residue enters, because the positions entering, $s + m, \ldots, s + \mathit{shift} + m - 1$, have the same residues as the cleared $s, \ldots, s + \min(\mathit{shift}, m) - 1$ (all residues if $\mathit{shift} \ge m$). So (I) holds if each written value equals $\mathrm{ms}(s + m - 1)$ and is positive or 0; we prove this in Lemma 2.

**Lemma 1 (the scan).** Assume (I) at window $s$. The loop of lines L7 to L12 keeps the invariant $T[s+i+1 \ldots s+m-1] = P[i+1 \ldots m-1]$ and ends either with $i = -1$, when $s$ is valid, or with $0 \le i < m$ and $T[s+i] \ne P[i]$.

*Proof.* The invariant holds at $i = m - 1$. Consider one step at position $i$, with $k = \mathrm{skip}[s+i]$ and $h = \mathrm{suff}[i]$.

If $k = 0$, line L12 compares $P[i]$ with $T[s+i]$ and either extends the invariant by one position or ends with a mismatch at $i$.

If $k > 0$, then $k = \mathrm{ms}(s+i)$ by (I), so $T[s+i-k+1 \ldots s+i] = P[m-k \ldots m-1]$, and if $k < m$ and $s + i - k \ge 0$, then $T[s+i-k] \ne P[m-1-k]$ by maximality. Also $P[i-h+1 \ldots i] = P[m-h \ldots m-1]$, and if $h \le i$ then $P[i-h] \ne P[m-1-h]$ by maximality.

- Case $k > h$, $h = i + 1$. Then $T[s \ldots s+i] = P[m-1-i \ldots m-1]$, because $k \ge i + 2 > i + 1$ and the suffixes of length $i + 1 = h$ agree, and $P[m-1-i \ldots m-1] = P[0 \ldots i]$ because $h = i + 1$. With the invariant, the window is an occurrence, and line L10 sets $i = -1$.
- Case $k > h$, $h \le i$. The text and $P[0 \ldots i]$ both end with the suffix of $P$ of length $h$, so $T[s+i-h+1 \ldots s+i] = P[i-h+1 \ldots i]$. At position $i - h$: since $k > h$, $T[s+i-h] = P[m-1-h]$, while $P[i-h] \ne P[m-1-h]$. So the invariant holds down to $i - h + 1$, and $i - h$ is a mismatch.
- Case $k < h$. Both end with the suffix of length $k$, so the text matches $P[i-k+1 \ldots i]$. At position $i - k \ge 0$ (since $k < h \le i + 1$): since $h > k$, $P[i-k] = P[m-1-k]$; and $k < h \le m$ with $s + i - k \ge 0$, so $T[s+i-k] \ne P[m-1-k]$. So $i - k$ is a mismatch.
- Case $k = h$. The text matches $P[i-k+1 \ldots i]$, and line L11 sets $i \leftarrow i - k$ and goes on, which keeps the invariant.

Each step decreases $i$ or ends the loop, so the loop stops. $\square$

**Lemma 2 (the note).** The value written at line L13 or L14 is $\mathrm{ms}(s + m - 1)$.

*Proof.* At line L13 the window is an occurrence, so $\mathrm{ms}(s+m-1) = m$. At line L14, by Lemma 1, $T[s+i+1 \ldots s+m-1] = P[i+1 \ldots m-1]$ and $T[s+i] \ne P[i]$, so the longest suffix of $P$ ending at $s + m - 1$ has length exactly $m - 1 - i$. $\square$

**Proof of the claim.** By Lemma 2, (I) holds at every window. By Lemma 1, line L13 outputs $s$ exactly when $s$ is valid, and otherwise line L14 runs with a true mismatch at $i$ and the text matching $P[i+1 \ldots m-1]$, which is the situation of Boyer-Moore; its shift, and the shift $\mathrm{gs}[0]$ after an occurrence, are at least 1 and skip no valid shift. So $s$ increases at each window, every valid shift is tested, and only valid shifts are output, in increasing order. The loop stops once $s > n - m$, after at most $n - m + 1$ windows. $\blacksquare$
