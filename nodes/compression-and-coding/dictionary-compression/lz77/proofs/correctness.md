---
title: LZ77 decoding inverts LZ77 encoding
proves: [correctness]
status: full
---

Let $T = T[1..n]$, $W \ge 1$ and $L_{\max} \ge 0$. Let $(d_1, \ell_1, c_1), \ldots, (d_t, \ell_t, c_t)$ be the triples that LZ77-ENCODE$(T, W, L_{\max})$ outputs, and let $i_s$ be the value of $i$ at line L2 when triple $s$ is made, so $i_1 = 1$ and $i_{s+1} = i_s + \ell_s + 1$.

**Lemma 1 (each triple is valid).** For each $s$, with $i = i_s$, $d = d_s$ and $\ell = \ell_s$:

1. $i + \ell \le n$, so $c_s = T[i + \ell]$ exists;
2. if $\ell = 0$ then $d = 0$; if $\ell \ge 1$ then $1 \le d \le \min(W, i - 1)$;
3. $T[i - d + k] = T[i + k]$ for $0 \le k < \ell$.

*Proof.* Line L3 sets $(d, \ell) = (0, 0)$, and only line L7 changes the pair, to $(i - j, k)$ with $k > \ell \ge 0$, for some $j$ with $\max(1, i - W) \le j \le i - 1$; so $1 \le i - j \le \min(W, i - 1)$, which gives (2). When line L7 runs with value $k$, the loop of line L6 has checked $T[j + k'] = T[i + k']$ for $0 \le k' < k$, which gives (3) with $d = i - j$. For (1): line L2 gives $i \le n$, so the loop of line L6 starts with $i + k = i \le n$, and it adds 1 to $k$ only when $i + k < n$. So $i + k \le n$ for every value of $k$, and in particular $i + \ell \le n$. $\square$

**Lemma 2 (the encoder ends and covers $T$).** The values $i_s$ strictly increase, $i_{t+1} = n + 1$, and the phrases $T[i_s .. i_s + \ell_s]$ for $s = 1, \ldots, t$ are consecutive and cover $T[1..n]$.

*Proof.* Line L9 adds $\ell_s + 1 \ge 1$ to $i$. By Lemma 1(1), $i_s + \ell_s \le n$, so $i_{s+1} \le n + 1$. The loop of line L2 ends when $i > n$, so at $i = n + 1$, after at most $n$ steps. Each phrase starts where the last one ended. $\square$

**Lemma 3 (the decoder).** Let $S_s$ be the value of $S$ after LZ77-DECODE has processed the first $s$ triples. Then $S_s = T[1 .. i_{s+1} - 1]$ for $s = 0, \ldots, t$.

*Proof.* By induction on $s$. For $s = 0$, $S_0$ is empty and $i_1 = 1$. Assume $S_{s-1} = T[1 .. i - 1]$ with $i = i_s$, and write $d = d_s$, $\ell = \ell_s$. Line L13 sets $start = i - 1 - d$.

We show by induction on $k$ that after $k$ rounds of line L14, $S = T[1 .. i - 1 + k]$. For $k = 0$ this is the assumption. Before round $k \ge 1$, $|S| = i - 2 + k$, and the round appends $S[start + k] = S[i - 1 - d + k]$. Since $\ell \ge k \ge 1$, Lemma 1(2) gives $d \ge 1$, so the index $i - 1 - d + k$ is at most $i - 2 + k = |S|$; and $d \le i - 1$ gives an index of at least $k \ge 1$. So the symbol exists and, by the inner assumption, equals $T[i - 1 - d + k]$. By Lemma 1(3) with $k - 1$ in place of $k$, $T[i - d + (k - 1)] = T[i + (k - 1)]$. So the round appends $T[i - 1 + k]$, as claimed.

After $\ell$ rounds, $S = T[1 .. i + \ell - 1]$, and line L15 appends $c_s = T[i + \ell]$. So $S_s = T[1 .. i + \ell] = T[1 .. i_{s+1} - 1]$. $\square$

**Theorem.** LZ77-DECODE(LZ77-ENCODE$(T, W, L_{\max})$) $= T$.

*Proof.* By Lemma 3 with $s = t$, the decoder returns $T[1 .. i_{t+1} - 1]$, and $i_{t+1} = n + 1$ by Lemma 2. $\square$

**Remark (greedy choice).** Line L4 visits every start $j$ in the window, and line L6 stops only at $L_{\max}$, at $n - i$, or at a mismatch. So $\ell_s$ is the length of the longest copy at $i_s$ that starts in the window, within the two limits, and line L7 keeps the first such $j$ in the order of line L4, which is the one with the smallest distance. Correct decoding does not depend on this choice; any $(d, \ell)$ that satisfies Lemma 1 decodes correctly.
