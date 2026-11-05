---
title: Galil-Seiferas outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$, a pattern $P[0 \ldots m-1]$ over any alphabet with equality tests, and an integer $k \ge 3$, GALIL-SEIFERAS$(T, P)$ stops and outputs exactly the shifts $p$, $0 \le p \le n - m$, with $T[p \ldots p+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, so let $m \ge 1$. Throughout, $v = P[s \ldots m-1]$ for the current value of $s$.

**Definitions and facts.** For a string $w$, $\mathrm{per}(w)$ is its smallest period. For $1 \le p \le |v|$, $\mathrm{reach}(p)$ is the length of the longest prefix of $v$ with period $p$; so $\mathrm{reach}(p) \ge p$, and if $\mathrm{reach}(p) < |v|$ then $v[\mathrm{reach}(p)] \ne v[\mathrm{reach}(p) - p]$. A length $p$ is a *prefix period* if $v[0 \ldots p-1]$ is primitive and $\mathrm{reach}(p) \ge kp$, and *good* if $\mathrm{reach}(p) \ge kp$ or $\mathrm{reach}(p) = |v|$. We use three standard facts.

(F1) If $\pi = \mathrm{per}(w)$ then $w[0 \ldots \pi-1]$ is primitive: if it were $y^r$ with $r \ge 2$, then $w$, a prefix of $y^\infty$, would have the smaller period $|y|$.

(F2) Fine and Wilf: if $w$ has periods $a$ and $b$ and $|w| \ge a + b - \gcd(a, b)$, it has period $\gcd(a, b)$.

(F3) If $z = v[0 \ldots p-1]$ is primitive, a prefix $w$ of $v$ with period $p$ and $|w| \ge p$ has no period $g < p$ dividing $p$; with (F2), if $w$ also has a period $d$ and $|w| \ge p + d$, then $p$ divides $d$. Indeed $z$ would have period $g \mid p$, $g < p$, making it a power.

(F4) If $v[0 \ldots L-1]$ has period $d$ and $L \ge kd$, then $\pi = \mathrm{per}(v[0 \ldots L-1]) \le d$ is a prefix period, by (F1) and $\mathrm{reach}(\pi) \ge L \ge k\pi$.

**The properties of the factorization.** We show that whenever FACTORIZE returns $(s, p_1, q_1)$:
(S1) every prefix period of $v$ equals $p_1$;
(S2) $p_1 + q_1 = \mathrm{reach}(p_1)$;
(S3) $p_1 = \mathrm{per}(v[0 \ldots p_1 + q_1 - 1])$.

Write $R = p_1 + q_1$. The invariant of lines L11 to L15 and of the loop of lines L24 to L29, at the start of lines L12 and L25, is

(G) no $p < p_1$ is good for $v$;

and after line L12 or L25 has run, $R = \mathrm{reach}(p_1)$, because $q_1$ was 0 or already $\mathrm{reach}(p_1) - p_1$ when the loop started, and the loop stops at the end of $v$ or at the first mismatch.

**Lemma 1 (skip).** Assume (G), $R = \mathrm{reach}(p_1) < k p_1$ and $R < |v|$. Then no $p$ with $p_1 < p \le p_1 + \lfloor q_1/k \rfloor$ is good, so (G) holds after line L15 or L28.

*Proof.* Suppose $p = p_1 + \delta$ is good, $1 \le \delta \le q_1/k$. Then $\mathrm{reach}(p) \ge R$: either $\mathrm{reach}(p) \ge kp > kp_1 > R$, or $\mathrm{reach}(p) = |v| > R$. For $0 \le i < q_1 - \delta$, we have $i + p < R$, so $v[i] = v[i + p]$, and $i + \delta + p_1 < R$, so $v[i + p] = v[(i + \delta) + p_1] = v[i + \delta]$. So $v[0 \ldots q_1 - 1]$ has period $\delta$ and length $q_1 \ge k\delta$. By (F4) it has a prefix period $\pi \le \delta \le q_1/k$, and $q_1 = R - p_1 < (k-1)p_1$ gives $\pi < p_1$; a prefix period is good, against (G). $\square$

**Lemma 2 (the shortest prefix period).** Assume (G) and $R = \mathrm{reach}(p_1) \ge kp_1$. Then $p_1$ is a prefix period and $p_1 = \mathrm{per}(v[0 \ldots R-1])$.

*Proof.* Let $\pi = \mathrm{per}(v[0 \ldots R-1]) \le p_1$. By (F1) $v[0 \ldots \pi-1]$ is primitive and $\mathrm{reach}(\pi) \ge R \ge kp_1 \ge k\pi$, so $\pi$ is good, and (G) gives $\pi = p_1$. $\square$

**Lemma 3 (drop).** Assume (G), $R = \mathrm{reach}(p_1) \ge kp_1$, and let line L26 move $s$ by $tp_1$, $t \ge 1$, to obtain $v' = v[tp_1 \ldots]$ and $R' = R - tp_1$, with $(k-1)p_1 \le R' < kp_1$. Then $\mathrm{reach}_{v'}(p_1) = R'$ and (G) holds for $v'$.

*Proof.* By Lemma 2, $z = v[0 \ldots p_1 - 1]$ is primitive. $v'[0 \ldots R'-1] = v[tp_1 \ldots R-1]$ is a factor of the $p_1$-periodic prefix that starts at a multiple of $p_1$, so it equals $v[0 \ldots R'-1]$, and the mismatch (or end) at $R$ in $v$ is at $R'$ in $v'$; so $\mathrm{reach}_{v'}(p_1) = R'$. Suppose $\delta < p_1$ is good for $v'$, and let $L = \min(\mathrm{reach}_{v'}(\delta), R')$; then $v'[0 \ldots L-1]$ has periods $\delta$ and $p_1$. If $L \ge \delta + p_1$, (F3) applied to $v'$ (which starts with $z$) says $p_1 \mid \delta$, impossible for $0 < \delta < p_1$. Otherwise $L < \delta + p_1 < 2p_1 \le (k-1)p_1 \le R'$, using $k \ge 3$, so $L = \mathrm{reach}_{v'}(\delta) < R' \le |v'|$, and goodness gives $\mathrm{reach}_{v'}(\delta) \ge k\delta$. Since $v$ and $v'$ agree on their first $R'$ characters and $\mathrm{reach}_{v'}(\delta) < R'$, the mismatch that ends the $\delta$-periodic prefix of $v'$ is also one in $v$, so $\mathrm{reach}_v(\delta) = \mathrm{reach}_{v'}(\delta) \ge k\delta$, and $\delta$ is good for $v$, against (G). $\square$

**Lines L11 to L15.** (G) holds at the first entry, with $p_1 = 1$, vacuously. If line L14 returns, $R = |v| < kp_1$: by (G) no $p < p_1$ is a prefix period or a period of $v$; $p_1$ is not a prefix period; and $p > p_1$ has $\mathrm{reach}(p) \le |v| < kp$. So $v$ has no prefix period and $p_1 = \mathrm{per}(v)$: (S1) to (S3) hold. If line L15 runs, Lemma 1 keeps (G). If line L16 is reached, Lemma 2 applies.

**Lines L17 to L23.** Here $p_1$ is a prefix period with $R \ge kp_1$, $z = v[0 \ldots p_1-1]$ is primitive and $p_1 = \mathrm{per}(v[0 \ldots R-1])$ (Lemma 2). The invariant at the start of line L19 is:
(H1) no prefix period $p$ with $p_1 < p < p_2$;
(H2) $p_2 + q_2 \le |v|$ and $v[0 \ldots q_2 - 1] = v[p_2 \ldots p_2 + q_2 - 1]$.

*Start.* $p_2 = q_1 = R - p_1 \ge (k-1)p_1 > p_1$ and $q_2 = 0$. If $p_1 < p < q_1$ were a prefix period, then $\mathrm{reach}(p) \ge kp \ge p + p_1$ and $R = p_1 + q_1 > p + p_1$, so $v[0 \ldots p + p_1 - 1]$ has periods $p$ and $p_1$, and (F3) for the primitive prefix of length $p$ gives $p \mid p_1$, impossible as $p > p_1$.

*Exits.* Line L19 keeps (H2). If line L20 exits, $p_2$ is used only as a bound in lines L24 to L29, where (G) is what matters, and (G) holds there because it held at line L12 and $v$, $p_1$ have not changed since. If line L21 returns, $|v| = p_2 + q_2 < kp_2$, so no $p \ge p_2$ is a prefix period; with (H1) and (G), every prefix period equals $p_1$, and with Lemma 2 this gives (S1) to (S3).

*Line L22,* $q_2 = R$. The loop stopped at a mismatch $v[q_2] \ne v[p_2 + q_2]$ with $p_2 + q_2 < kp_2$, so $\mathrm{reach}(p_2) = p_2 + q_2 < kp_2$ and $p_2$ is not a prefix period. Let $p = p_2 + \delta$, $1 \le \delta < p_1$, be a prefix period. Then $\mathrm{reach}(p) \ge kp > p_2 + q_2$, so for $0 \le i < R - \delta$, $v[i] = v[i + p]$ and, by (H2), $v[i + p] = v[p_2 + (i + \delta)] = v[i + \delta]$; so $v[0 \ldots R-1]$ has period $\delta < p_1$, against Lemma 2. So (H1) holds for $p_2 + p_1$. For (H2), for $i < q_1$: $v[p_2 + p_1 + i] = v[p_1 + i] = v[i]$, by (H2) and the period $p_1$ of $v[0 \ldots R-1]$.

*Line L23,* $q_2 \ne R$. As above $p_2$ is not a prefix period. Let $p = p_2 + \delta$, $1 \le \delta \le q_2/k$, be one. Then $\mathrm{reach}(p) \ge kp > p_2 + q_2$, and for $0 \le i < q_2 - \delta$, $v[i] = v[i + p] = v[p_2 + i + \delta] = v[i + \delta]$ by (H2): $v[0 \ldots q_2-1]$ has period $\delta$ and length $q_2 \ge k\delta$. By (F4) it has a prefix period $\pi \le \delta \le q_2/k < p_2$, which is $p_1$ by (H1) and (G). So $v[0 \ldots q_2 - 1]$ has period $p_1$, hence $q_2 \le R$, and so $q_2 < R$ and $v[0 \ldots q_2]$ has period $p_1$. Also $q_2 \ge k\delta \ge \delta + p_1$ (as $\delta \ge \pi = p_1$), so (F3) gives $p_1 \mid \delta$. Now $p \le p_2 + q_2 < \mathrm{reach}(p)$, so $v[p_2 + q_2] = v[p_2 + q_2 - p] = v[q_2 - \delta] = v[q_2]$, against the mismatch. (H2) holds with $q_2 = 0$, and $p_2 + \lfloor q_2/k \rfloor + 1 \le p_2 + q_2 + 1 \le |v|$ since $p_2 + q_2 < |v|$.

**Lines L24 to L29.** (G) holds at the first entry. After line L25, if $R \ge kp_1$, line L26 drops copies and Lemma 3 gives (G) for the new $v$ with $\mathrm{reach}(p_1) = R' < kp_1$; this does not change $s + p_1 + q_1$. If line L27 returns, $\mathrm{reach}(p_1) = |v| < kp_1$, and (S1) to (S3) follow exactly as for line L14. Otherwise Lemma 1 applies to line L28.

**Lemma 4 (the search).** Assume (S1) to (S3), $R = p_1 + q_1$. At the start of each window $p$ of line L5, $T[p+s \ldots p+s+q-1] = v[0 \ldots q-1]$; line L7 outputs $p$ exactly when $p$ is valid; and no shift $p'$ with $p < p' < p_{\mathrm{next}}$ is valid.

*Proof.* The invariant holds with $q = 0$; line L6 keeps it and stops at $q = |v|$ or at a real mismatch $T[p+s+q] \ne v[q]$ (the position is inside $T$ because $p \le n - m$). Line L7 outputs $p$ exactly when $v$ and $u$ both match, that is, when $p$ is valid. After line L8, for $i < q - p_1 = q_1$, $T[p + p_1 + s + i] = v[p_1 + i] = v[i]$ by the period $p_1$ of $v[0 \ldots R-1]$; after line L9 the invariant is empty. For the shifts: $p'$ valid implies $v$ occurs at $p' + s$; let $d = p' - p \ge 1$. For $d \le i < q$, $T[p+s+i] = v[i]$ and $T[p+s+i] = v[i - d]$, so $v[0 \ldots q-1]$ has period $d$.

- Line L8, $q = R$, $d < p_1$: $v[0 \ldots R-1]$ has period $d < p_1$, against (S3).
- Line L9, $q \ne R$, $d \le q/k$: $v[0 \ldots q-1]$ has period $d$ and length $q \ge kd$, so by (F4) it has a prefix period $\pi \le d$, and $\pi = p_1$ by (S1). Then $v[0 \ldots q-1]$ has period $p_1$, so $q \le R$ by (S2), and $q < R \le |v|$: the scan stopped at a real mismatch, and $v[0 \ldots q]$ has period $p_1$. As $q \ge kd \ge d + p_1$, (F3) gives $p_1 \mid d$. The occurrence gives $T[p+s+q] = v[q - d] = v[q]$, against the mismatch. $\square$

**Termination.** In lines L11 to L15 and L24 to L29, $p_1$ strictly increases at lines L15 and L28, and line L26 only runs while $p_1 + q_1 \ge kp_1$, which bounds the number of drops. These lines keep $p_1 + q_1 \le |v| \le m$: lines L15 and L28 run only when $s + p_1 + q_1 < m$, and then $p_1 + \lfloor q_1/k \rfloor + 1 \le p_1 + q_1 + 1 \le |v|$. Lines L17 to L23 strictly increase $p_2$ at each step and keep $p_2 \le p_2 + q_2 \le |v|$ by (H2), so they stop. The loop of lines L24 to L29 ends with $p_1 \ge p_2 > p_1^{\mathrm{old}}$, so each return to line L12 has a larger $p_1$, and since $p_1 \le m$ FACTORIZE returns. In the search, each shift is at least 1 and each window does at most $m$ steps of line L6, so the search stops after at most $n - m + 1$ windows.

**Proof of the claim.** FACTORIZE returns with (S1) to (S3). By Lemma 4, every window is output exactly when it is valid, the shifts skip no valid shift, and $p$ increases, so every valid shift is output once, in increasing order. $\blacksquare$
