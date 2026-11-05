---
title: The sparse Cole-Hariharan algorithm reports exactly the start positions of the approximate matches
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$, and $\mathrm{ed}$ is the Levenshtein distance with unit costs. A **start** is a position $s \in \{0, \ldots, n\}$ with $\mathrm{ed}(P, T[s \ldots j)) \le k$ for some $j$ with $s \le j \le n$. The claim is that COLE-HARIHARAN($P$, $T$, $k$), as given on the page and in the implementation, returns the sorted set of starts. Only the sparse case and the fallback of lines L2 and L3 are proved here; the mostly periodic procedure of the paper is not part of this program. The proof does not use that the breaks are aperiodic, only that they are disjoint substrings of $P$; aperiodicity matters for the running time.

## Reversal

Write $X^R$ for the reverse of a string $X$. Reversing an edit script of $P$ into $X$ gives one of the same cost of $P^R$ into $X^R$, so $\mathrm{ed}(P, X) = \mathrm{ed}(P^R, X^R)$. The reverse of $T[s \ldots j)$ is $T^R[n - j \ldots n - s)$. So $s$ is a start of $P$ in $T$ if and only if $n - s$ is an **end** of $P^R$ in $T^R$, that is, a position $j'$ with $\mathrm{ed}(P^R, T^R[h' \ldots j')) \le k$ for some $h' \le j'$.

## The Landau-Vishkin values

We use the [correctness proof of the Landau-Vishkin algorithm](/landau-vishkin-algorithm/), applied to $P^R$ and $T^R$. It defines the Sellers table $C$, the diagonals $d$ with $-m \le d \le n$, and the furthest row $L[d][e]$ of diagonal $d$ whose value is at most $e$, with $L[d][e] = -\infty$ when there is none. It shows the following.

- (F1) $L[d][e] = -\infty$ when $d < \max(-e, -m)$.
- (F2) If the three values $L[d-1][e-1]$, $L[d][e-1]$ and $L[d+1][e-1]$ are given correctly, with $-\infty$ for diagonals outside $[-m, n]$ or for $e - 1 = -1$, then the step that takes their candidates, clips to $\min(m, n - d)$ and extends by a longest common extension yields $L[d][e]$ (its Lemma 4, whose proof uses only these three values).
- (F3) A position $j'$ is an end if and only if $L[j' - m][k] = m$ (its theorem).

The program BAND-MATCHES($dlo$, $dhi$) runs the same step for $e = 0, \ldots, k$ on the diagonals $d$ with $\max(blo, -e) \le d \le bhi$, where $blo = \max(dlo - k, -m)$ and $bhi = \min(dhi + k, n)$, reads a neighbour outside $[blo, bhi]$ or below $-(e - 1)$ as $-\infty$ (the value NONE), and returns the $d \in [dlo, dhi]$ whose stored value at level $k$ is $m$.

## Lemma 1: the band

For $0 \le e \le k$, the stored value of every diagonal $d$ with $\max(dlo - k + e, -e, -m) \le d \le \min(dhi + k - e, n)$ is $L[d][e]$. Hence BAND-MATCHES($dlo$, $dhi$) returns exactly the $d \in [dlo, dhi]$ with $L[d][k] = m$.

*Proof.* Induct on $e$. Fix $d$ in the stated range for $e$; it lies in $[blo, bhi]$, so the program computes it. Consider a neighbour $d' \in \{d - 1, d, d + 1\}$ at level $e - 1$ (for $e = 0$ there is none, and the step uses only the first cell of the diagonal). We show that the program reads $L[d'][e - 1]$.

- If $-m \le d' \le n$ and $d' \ge -(e - 1)$, then $dlo - k + (e - 1) \le d' \le dhi + k - (e - 1)$, because $|d' - d| \le 1$. So $d'$ is in the range for $e - 1$, and its stored value is $L[d'][e - 1]$ by the induction hypothesis.
- If $d' < -(e - 1)$ or $d' < -m$, the true value is $-\infty$ by (F1) or because the diagonal has no cells. The program reads NONE: either $d' < blo$ and the neighbour is outside the array, or the entry was never written at level $e - 1$.
- If $d' > n$, then $d = n$ and $d' = n + 1 > bhi$, so the program reads NONE, and the diagonal has no cells.

By (F2), the stored value of $d$ is $L[d][e]$.

For the second sentence, let $d \in [dlo, dhi]$. If $-k \le d$ and $-m \le d \le n$, then $d$ is in the range for $e = k$, so its stored value at level $k$ is $L[d][k]$, and the program returns $d$ exactly when $L[d][k] = m$. Otherwise $L[d][k] \ne m$: for $d < -k$ or $d < -m$ it is $-\infty$, and for $d > n$ there is no cell. In that case the program does not return $d$, since the entry is NONE or $d$ lies outside $[blo, bhi]$, where the program does not look. $\square$

## Alignments

An **alignment** of $P$ and $A$ is a set of pairs $(i, u)$, with $i$ a position of $P$ and $u$ a position of $A$, in which no position occurs twice and $i < i'$ if and only if $u < u'$ for any two pairs. Its cost is the number of unpaired positions of $P$ and of $A$ plus the number of pairs with $P[i] \ne A[u]$, and the least cost is $\mathrm{ed}(P, A)$, as shown in the [proof of the edit distance hardness theorem](/edit-distance-hardness/) (its Lemma 1). If $i$ is paired, write $\pi(i)$ for its partner.

Let $\ell = k^2$. A break is a set $I_b = [o_b, o_b + \ell)$ of positions of $P$, for $b = 0, \ldots, 2k - 1$, and the sets are pairwise disjoint. A break is **clean** in an alignment if every $i \in I_b$ is paired with an equal symbol and $\pi(i + 1) = \pi(i) + 1$ whenever $i, i + 1 \in I_b$.

## Lemma 2: at least k clean breaks

In an alignment of cost $c$, at most $c$ breaks are not clean. So if $c \le k$, at least $k$ of the $2k$ breaks are clean.

*Proof.* We give each break that is not clean a unit of cost, with distinct units for distinct breaks.

- (a) If some $i \in I_b$ is unpaired or paired with an unequal symbol, the unit is the unpaired symbol $P[i]$ or the unequal pair of $i$.
- (b) Otherwise all $i \in I_b$ are paired with equal symbols, and $\pi(i + 1) \ne \pi(i) + 1$ for some $i, i + 1 \in I_b$. By the order condition $\pi(i + 1) \ge \pi(i) + 2$, and the position $u = \pi(i) + 1$ of $A$ lies strictly between the partners of $i$ and $i + 1$. A partner of $u$ would lie strictly between $i$ and $i + 1$, so $u$ is unpaired. The unit is the unpaired symbol $A[u]$.

Units of kind (a) involve a position of $P$ in $I_b$, and the breaks are disjoint, so they differ for different breaks. Units of kind (a) are symbols of $P$ or pairs, and units of kind (b) are unpaired symbols of $A$, so the two kinds differ. Let $b \ne b'$ both get units of kind (b), from $i, i + 1 \in I_b$ and $i', i' + 1 \in I_{b'}$, with $I_b$ before $I_{b'}$. Then $i + 1 \le i'$, and the unit of $b$ is below $\pi(i + 1) \le \pi(i')$, while the unit of $b'$ is above $\pi(i')$. So all units are distinct, and there are at most $c$ of them. $\square$

## Lemma 3: a clean break votes for the start

Let $A = T[s \ldots j)$ with an alignment of cost $c \le k$ to $P$, and let break $b$ be clean. Then $q = s + \pi(o_b)$ is an occurrence of $P[o_b \ldots o_b + \ell)$ in $T$, and $q - o_b - k \le s \le q - o_b + k$.

*Proof.* Cleanness gives $\pi(o_b + r) = \pi(o_b) + r$ and $A[\pi(o_b) + r] = P[o_b + r]$ for $0 \le r < \ell$, so $T[q + r] = P[o_b + r]$. Let $t$ be the number of pairs whose position of $P$ is below $o_b$; by the order condition these are also the pairs whose position of $A$ is below $\pi(o_b)$. Then $o_b = t + x$ and $\pi(o_b) = t + y$, where $x$ counts the unpaired positions of $P$ below $o_b$ and $y$ the unpaired positions of $A$ below $\pi(o_b)$. So $q - s - o_b = y - x$, and $x, y \ge 0$ with $x + y \le c \le k$ give $|q - s - o_b| \le k$. $\square$

## Lemma 4: the marks

If $s$ is a start and $k \ge 1$, then after line L5 the window $w = \lfloor s / k \rfloor$ has marks from at least $k$ distinct breaks, so line L6 keeps it.

*Proof.* Fix $j$ with $\mathrm{ed}(P, T[s \ldots j)) \le k$ and an alignment of least cost. By Lemma 2 at least $k$ breaks are clean. For a clean break $b$, Lemma 3 gives an occurrence $q$ of the string of $b$, which the Aho-Corasick search of line L4 reports (the implementation looks up each break by its string, so equal strings at different offsets share the list of occurrences, and each break uses its own offset). Line L5 sets $lo = \max(0, q - o_b - k)$ and $hi = \min(n, q - o_b + k)$. Since $0 \le s \le n$, Lemma 3 gives $lo \le s \le hi$, so $\lfloor lo/k \rfloor \le w \le \lfloor hi/k \rfloor$, and the window $w$ gets a mark from $b$. The stamp array counts break $b$ at most once per window, because line L5 handles the occurrences of one break before those of the next, and a window marked by $b$ is counted once for $b$. So the count of $w$ is the number of distinct breaks that mark it, which is at least $k$. $\square$

## Lemma 5: the check of a window

For a window $w$, with $s_0 = wk$ and $s_1 = \min(wk + k - 1, n)$, line L7 returns exactly the starts $s$ with $s_0 \le s \le s_1$.

*Proof.* The call is BAND-MATCHES($n - m - s_1$, $n - m - s_0$) on $P^R$ and $T^R$, and each returned diagonal $d$ is mapped to $s = n - (m + d)$. The map $d \mapsto n - m - d$ is a bijection from $[n - m - s_1, n - m - s_0]$ onto $[s_0, s_1]$. By Lemma 1, $d$ is returned if and only if $L[d][k] = m$, which by (F3) holds if and only if $m + d = n - s$ is an end of $P^R$ in $T^R$, which by the reversal holds if and only if $s$ is a start. $\square$

## The theorem

*Lines L2 and L3.* If $k = 0$, or the scan of line L1 finds fewer than $2k$ breaks, the program returns the images of BAND-MATCHES($-m$, $n - m$). By Lemma 1, (F3) and the reversal, these are the $s = n - m - d$ for the ends $m + d$ of $P^R$, which are all the starts, since every end lies in $[0, n]$ and so on a diagonal in $[-m, n - m]$. They are sorted before they are returned.

*Lines L4 to L8.* Otherwise $k \ge 1$ and there are $2k$ disjoint breaks of length $k^2$. Every returned value is a start by Lemma 5. Every start $s$ lies in a window that line L6 keeps, by Lemma 4, and Lemma 5 then returns it. The windows are disjoint, so no start is returned twice, and line L8 sorts the result. So the program returns the sorted set of starts. $\blacksquare$
