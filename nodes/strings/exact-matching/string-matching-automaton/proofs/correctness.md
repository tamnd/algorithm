---
title: The string-matching automaton reports exactly the occurrences
proves: [correctness, termination]
status: full
---

**Claim.** If $\delta[q][c] = \sigma_P(P[0 \ldots q-1]\,c)$ for every state $0 \le q \le m$ and every character $c$, then AUTOMATON-SEARCH$(T, \delta, m)$ stops after $n = |T|$ steps and outputs exactly the shifts $s$ with $T[s \ldots s+m-1] = P$, in increasing order. That the construction produces this table is proved on the page of [the construction](/string-matching-automaton-construction/).

Here $\sigma_P(w)$ is the length of the longest prefix of $P$ that is a suffix of $w$. It is at most $m$ and at most $|w|$.

**Lemma 1.** For any string $w$ and character $c$, $\sigma_P(wc) \le \sigma_P(w) + 1$.

*Proof.* Let $r = \sigma_P(wc)$. If $r = 0$ there is nothing to show. Otherwise $P[0 \ldots r-1]$ is a suffix of $wc$, so $P[0 \ldots r-2]$ is a suffix of $w$, and $r - 1 \le \sigma_P(w)$. $\square$

**Lemma 2.** If $q = \sigma_P(w)$, then $\sigma_P(wc) = \sigma_P(P[0 \ldots q-1]\,c)$.

*Proof.* Let $x = P[0 \ldots q-1]$, a suffix of $w$, so $xc$ is a suffix of $wc$. Any prefix of $P$ that is a suffix of $xc$ is then a suffix of $wc$, so $\sigma_P(xc) \le \sigma_P(wc)$. Conversely, let $r = \sigma_P(wc)$. By Lemma 1, $r \le q + 1 = |xc|$. The strings $P[0 \ldots r-1]$ and $xc$ are both suffixes of $wc$, and the first is not longer, so it is a suffix of $xc$. So $r \le \sigma_P(xc)$. $\square$

**Theorem.** The claim holds.

*Proof.* Assume $m \ge 1$; for $m = 0$, line L2 outputs all shifts $0, \ldots, n$, and each is valid because the empty string occurs everywhere. We show by induction on $i$ that after line L5 in the iteration for $i$, $q = \sigma_P(T[0 \ldots i])$. Before the loop, $q = 0 = \sigma_P$ of the empty string. If $q = \sigma_P(T[0 \ldots i-1])$ before line L5, then line L5 sets $q = \delta[q][T[i]] = \sigma_P(P[0 \ldots q-1]\,T[i]) = \sigma_P(T[0 \ldots i])$ by Lemma 2.

Now $\sigma_P(T[0 \ldots i]) = m$ exactly when $P$ is a suffix of $T[0 \ldots i]$, that is, when $T[i-m+1 \ldots i] = P$. So line L7 outputs the shift $s = i - m + 1$ exactly when it is valid. Each valid shift $s$ is output in the iteration $i = s + m - 1$, and the shifts are output in increasing order of $i$, hence of $s$. When $m > n$, the state never reaches $m$, because $\sigma_P(w) \le |w| < m$. The loop has $n$ iterations of constant work, so the algorithm stops. $\blacksquare$
