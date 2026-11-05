---
title: The Galil-Park algorithm computes the furthest rows of the diagonals
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$. Let $C$ be the Sellers table and $L[d][e]$ the furthest row $i$ of diagonal $d$ with $C[i][i + d] \le e$, or $-\infty$. Write $\mathrm{LCE}(r, x)$ for the length of the longest common prefix of $P[r \ldots m)$ and $T[x \ldots n)$.

**Fact (Landau-Vishkin).** For $0 \le e \le k$ and $\max(-e, -m) \le d \le n$, let $r_0$ be the value of line L5 computed from the true values $L[d][e-1]$, $L[d-1][e-1]$ and $L[d+1][e-1]$. Then $L[d][e] = r_0 + \mathrm{LCE}(r_0, r_0 + d)$. For $d < -e$ or $d < -m$, $L[d][e] = -\infty$.

This is Lemma 4 of the [Landau-Vishkin correctness proof](/landau-vishkin-algorithm/), whose induction uses only these three values. The Galil-Park loop visits $c = 0, \ldots, n + k$ with $c = d + e$. For $c \ge 0$ and $0 \le e \le k$, $d = c - e \ge -e$, so the skipped entries are exactly those with $d > n$ (no cells) or $d < -m$. Entries with $c < 0$ have $d < -e$ and are $-\infty$. The inputs $L[d][e-1]$, $L[d-1][e-1]$ and $L[d+1][e-1]$ lie on the anti-diagonals $c - 1$, $c - 2$ and $c$, and the last one has the smaller error count $e - 1$, so all three are computed before $(d, e)$.

A triple $(q, y, f)$ is *maximal* when $T[q \ldots q + f) = P[y \ldots y + f)$ and ($q + f = n$ or $y + f = m$ or $T[q + f] \ne P[y + f]$). Equivalently, $\mathrm{LCE}(y, q) = f$.

**Lemma 1.** Assume that all triples in $R$ are maximal when an extension starts at line L6. Then the loop of lines L7 to L11 ends with $r - r_0 = \mathrm{LCE}(r_0, x_0)$, where $x_0 = r_0 + d$, and the triple $(x_0, r_0, r - r_0)$ is maximal.

*Proof.* The loop keeps the invariant $x - r = d$ and $P[r_0 \ldots r) = T[x_0 \ldots x)$. It holds at the start. We show that each step keeps it, and that each stop happens at a position where the extension cannot go on: $r = m$, $x = n$, or $P[r] \ne T[x]$, after the step's increment.

- Line L8 and line L11 compare $P[r]$ with $T[x]$. On equality both indices grow by 1 and the invariant holds. On inequality the loop stops with $P[r] \ne T[x]$.
- Line L9 uses a triple $(q, y, f)$ of $R$ with $q \le x < q + f$. Let $y' = y + x - q$ and $h = q + f - x \ge 1$. Maximality gives $T[x \ldots x + h) = P[y' \ldots y' + h)$. By definition, $g = PP[r][y']$ is the length of the longest common prefix of $P[r \ldots)$ and $P[y' \ldots)$.
  - If $g < h$: then $P[r \ldots r + g) = P[y' \ldots y' + g) = T[x \ldots x + g)$. Since $g < h \le m - y'$, the position $y' + g$ lies in $P$. So either $r + g = m$, or $P[r + g] \ne P[y' + g] = T[x + g]$. The loop stops with $r + g$ and $x + g$, at the end of $P$ or at a difference.
  - If $g > h$: then $P[r \ldots r + h) = P[y' \ldots y' + h) = T[x \ldots x + h)$, and $P[r + h] = P[y' + h]$ since $h < g$. If $y + f = m$, then $y' + h = m$ and $g \le m - y' = h$, a contradiction, so $y + f < m$. Maximality then gives $x + h = q + f = n$, or $T[x + h] \ne P[y' + h] = P[r + h]$. The loop stops with $r + h$ and $x + h$, at the end of $T$ or at a difference.
  - If $g = h$: the equal prefixes give $P[r \ldots r + g) = T[x \ldots x + g)$, and both indices grow by $g$. The invariant holds.
- The condition of line L7 stops the loop when $r = m$ or $x = n$.

Each step increases $r$ by at least 1 or stops, so the loop ends. At the end, the invariant and the stop condition give $r - r_0 = \mathrm{LCE}(r_0, x_0)$, and the same two facts say that $(x_0, r_0, r - r_0)$ is maximal. $\square$

**Lemma 2.** At every time, each triple in $R$ is maximal, and each stored value $L[d][e]$ is the true one.

*Proof.* Induct over the steps of line L4. At the start $R$ is empty. Consider the entry $(d, e)$, with all earlier entries true and all triples maximal. By the order shown above, line L5 reads true inputs, so $r_0$ is the value of the Fact. By Lemma 1, line L12 stores $r_0 + \mathrm{LCE}(r_0, r_0 + d) = L[d][e]$, and a new triple put into $R[e]$ is maximal. The arrays of three anti-diagonals keep the entries of $c - 1$ and $c - 2$ until $c$ is done, and skipped entries hold $-\infty$, so line L5 reads the right values. $\square$

**Theorem.** GALIL-PARK$(P, T, k)$ reports, in increasing order, exactly the positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$.

*Proof.* As in the Landau-Vishkin proof, $j$ is a match exactly when $L[j - m][k] = m$. By Lemma 2 the values stored for $e = k$ are true, and line L13 tests each diagonal $d = c - k$ with $-m \le d \le n$ once. The entries with $d < -m$ have no cells, and entries with $d > n - m$ cannot reach row $m$ because $r \le n - d < m$. Line L13 runs in increasing order of $c$, so in increasing order of $d$ and of $j = m + d$. $\blacksquare$
