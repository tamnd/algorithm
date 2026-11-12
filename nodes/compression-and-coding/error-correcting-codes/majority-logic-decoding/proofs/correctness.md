---
title: Reed's majority-logic decoder corrects every pattern of fewer than 2^(m - r - 1) errors in RM(r, m)
proves: [correctness]
status: full
---

**Setting.** Points of $\mathrm{GF}(2)^m$ index the $n = 2^m$ positions. For $S \subseteq \{1, \dots, m\}$ let $x_S = \prod_{i \in S} x_i$ and let $V_S = \mathrm{span}\{e_i : i \in S\}$, a subspace of dimension $|S|$. The cosets $b + V_S$, for $b$ with $b_i = 0$ for all $i \in S$, are $2^{m - |S|}$ pairwise disjoint sets of size $2^{|S|}$ that cover all points. For a word $z$ and a set $P$ of points write $z(P) = \sum_{p \in P} z_p$ over GF(2). The sent word is the table of $f = \sum_{|S| \le r} a_S x_S$, the error is $e$ with $\mathrm{wt}(e) \le t = 2^{m - r - 1} - 1$, and $y = f + e$.

**Lemma 1 (sums of monomials over cosets).** Let $|T| \le |S|$. Then $x_T(b + V_S) = 1$ if $T = S$, and $0$ otherwise.

*Proof.* $x_T(p) = 1$ exactly when $p_i = 1$ for all $i \in T$. On $b + V_S$ the coordinates in $S$ run over all $2^{|S|}$ values and the others are fixed to $b$. If $T \not\subseteq S$, some $i \in T \setminus S$ has $p_i = b_i = 0$ on the whole coset, so the sum is 0. If $T \subseteq S$, the points of the coset with $x_T = 1$ are those with $p_i = 1$ for $i \in T$, with the other coordinates of $S$ free: there are $2^{|S| - |T|}$ of them. This is odd only when $T = S$. $\square$

**Lemma 2 (check sums).** Let $g = \sum_{|T| \le \ell} c_T x_T$ have degree at most $\ell$ and let $|S| = \ell$. Then $g(b + V_S) = c_S$ for every coset $b + V_S$.

*Proof.* By linearity and Lemma 1, $g(b + V_S) = \sum_T c_T\, x_T(b + V_S) = c_S$. $\square$

**Lemma 3 (one vote).** Let $z = g + e$ with $g$ as in Lemma 2 and $\mathrm{wt}(e) \le t$, and let $\ell \le r$, $|S| = \ell$. Among the $2^{m - \ell}$ check sums $z(b + V_S)$, more than half equal $c_S$.

*Proof.* $z(b + V_S) = c_S + e(b + V_S)$ by Lemma 2. A check sum differs from $c_S$ only if its coset contains a position of $e$. The cosets are disjoint, so at most $\mathrm{wt}(e) \le t$ of them do. Now $t = 2^{m - r - 1} - 1 \le 2^{m - \ell - 1} - 1 < 2^{m - \ell}/2$, so fewer than half of the sums are wrong. $\square$

**Invariant.** At the start of the pass of line L2 for degree $\ell$:

> **(R)** $y = \sum_{|T| \le \ell} a_T x_T + e$, and $f = \{\, T : |T| > \ell, \; a_T = 1 \,\}$.

*Initialization.* Before the first pass, $\ell = r$, $y$ is the received word $\sum_{|T| \le r} a_T x_T + e$, and $f$ is empty (line L1). So (R) holds.

*Maintenance.* Fix the pass for $\ell$. For each $S$ of size $\ell$ (line L3), lines L4 to L6 count the cosets $b + V_S$ with $y(b + V_S) = 1$. By (R) and Lemma 3, with $g = \sum_{|T| \le \ell} a_T x_T$, more than half of the $2^{m - \ell}$ sums equal $a_S$. So the count exceeds $2^{m - \ell - 1}$ exactly when $a_S = 1$, and line L7 records $S$ exactly when $a_S = 1$. Line L7 reads only the current $y$, which line L8 changes after all $S$ of this degree are done, so each vote uses the same $y$. Line L8 adds $\sum_{|S| = \ell} a_S x_S$ to $y$, which leaves $y = \sum_{|T| \le \ell - 1} a_T x_T + e$. Line L9 adds the same sets to $f$. So (R) holds for $\ell - 1$.

*Termination.* The loop of line L2 runs for $\ell = r, r - 1, \dots, 0$. After the pass for $\ell = 0$, (R) with $\ell = -1$ gives $f = \{\, T : a_T = 1 \,\}$, the sent polynomial, and line L10 returns it.

**Tightness.** Let $c$ be the table of $x_1 x_2 \cdots x_r$, of weight $2^{m - r}$, and let $y$ be 1 on half of its support. Then $y$ is at distance $2^{m - r - 1}$ from both $0$ and $c$, so any decoder fails on one of these two patterns of weight $t + 1$. $\blacksquare$
