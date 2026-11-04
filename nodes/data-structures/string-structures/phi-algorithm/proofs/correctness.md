---
title: The PHI algorithm computes PLCP in text order and then the LCP array, in linear time
proves: [correctness, complexity]
status: full
---

We use the pseudocode and the notation of the page. Write $T_i = t[i \ldots n-1]$, with $T_n$ the empty string, and $<$ for the lexicographic order. All suffixes are distinct, so $SA$ is a strict order and $\Phi[i]$ is the suffix immediately before $T_i$ in it.

**Lemma 1 (the key fact).** For $0 \le i < n - 1$, if $\Phi[i] \ne -1$ and $PLCP[i] = h \ge 1$, then $\Phi[i+1] \ne -1$ and $PLCP[i + 1] \ge h - 1$.

*Proof.* Let $j = \Phi[i]$, so $T_j < T_i$ and they share their first $h \ge 1$ symbols. Removing the common first symbol keeps the order, so $T_{j+1} < T_{i+1}$, and they share $h - 1$ symbols. So $T_{i+1}$ has a predecessor in sorted order, $\Phi[i + 1] \ne -1$, and its predecessor $T_{\Phi[i+1]}$ satisfies $T_{j+1} \le T_{\Phi[i+1]} < T_{i+1}$. A string that lies between two strings in sorted order shares with the larger one at least their common prefix, so $lcp(T_{\Phi[i+1]}, T_{i+1}) \ge lcp(T_{j+1}, T_{i+1}) = h - 1$. $\square$

**Invariant of lines L3 to L5.** At the start of iteration $i$, $A[k] = PLCP[k]$ for $k < i$, $A[k] = \Phi[k]$ for $k \ge i$, and $h \le PLCP[i]$ (when $\Phi[i] \ne -1$).

At $i = 0$, line L1 has set $A = \Phi$ and $h = 0$. In iteration $i$, $A[i] = \Phi[i]$ is read before it is overwritten. If it is $-1$, then $PLCP[i] = 0$ by definition, which line L3 stores. Otherwise, by the invariant the first $h$ symbols of $T_i$ and $T_j$ agree, and the loop of line L4 extends $h$ while the next symbols agree and both suffixes continue, so it stops at $h = PLCP[i]$; line L5 stores it. For iteration $i + 1$: if $\Phi[i] = -1$, $h$ is reset to 0, a valid lower bound. If $PLCP[i] = 0$, $h$ stays 0. If $PLCP[i] \ge 1$, $h$ becomes $PLCP[i] - 1 \le PLCP[i + 1]$ by Lemma 1. The other entries are untouched, so the invariant holds.

After the loop, $A = PLCP$. Line L6 sets $LCP[r] = PLCP[SA[r]] = lcp(T_{\Phi[SA[r]]}, T_{SA[r]}) = lcp(T_{SA[r-1]}, T_{SA[r]})$ for $r \ge 1$, and $LCP[0] = PLCP[SA[0]] = 0$, which is the LCP array.

**Time.** Each iteration of line L4 increments $h$. Between iterations, $h$ decreases by at most 1, or is reset to 0, which happens only once (at $SA[0]$), from a value at most $n$. Since $h \le n$ always, the total number of increments is at most $n$ plus the total decrease, which is at most $n - 1$ from the decrements plus at most $n$ from the reset. So line L4 runs $O(n)$ times in total, and with the scans of lines L1, L3 and L6 the time is $\Theta(n)$. $\blacksquare$
