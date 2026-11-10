---
title: The 3-opt moves, and the O(√n) bound for 3-optimal tours
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 5$, are symmetric, non-negative and satisfy the triangle inequality. Write the tour as an array $T[0], \ldots, T[n-1]$. For positions $0 \le i < j < k \le n - 1$, let $a = T[i]$, $X = T[i+1..j]$, $Y = T[j+1..k]$, and $f = T[(k+1) \bmod n]$. A 3-opt move removes the edges $\{a, X_{\text{first}}\}$, $\{X_{\text{last}}, Y_{\text{first}}\}$ and $\{Y_{\text{last}}, f\}$, and puts the two segments back between $a$ and $f$ in another order or direction.

**Lemma 1 (the reconnections).** Let $X$ and $Y$ both have at least two cities, and let the three removed edges be pairwise disjoint. Then there are exactly 7 other ways to put $X$ and $Y$ back into one tour with $a$ before them and $f$ after them. Three of them keep one of the removed edges; they are 2-opt moves. Four of them use three new edges; they are the pure 3-opt moves.

*Proof.* The tour after the move is $a$, then the two segments in some order, each in one of two directions, then $f$ and the rest. That gives $2 \cdot 2 \cdot 2 = 8$ ways, and $X\,Y$ is the old tour. Write $\bar X$ for $X$ reversed. The new edges of each way are:

| way | edges at the three joints | old edge kept |
|---|---|---|
| $\bar X\, Y$ | $a X_{\text{last}}$, $X_{\text{first}} Y_{\text{first}}$, $Y_{\text{last}} f$ | $Y_{\text{last}} f$ |
| $X\, \bar Y$ | $a X_{\text{first}}$, $X_{\text{last}} Y_{\text{last}}$, $Y_{\text{first}} f$ | $a X_{\text{first}}$ |
| $\bar Y\, \bar X$ | $a Y_{\text{last}}$, $Y_{\text{first}} X_{\text{last}}$, $X_{\text{first}} f$ | $X_{\text{last}} Y_{\text{first}}$ |
| $\bar X\, \bar Y$ | $a X_{\text{last}}$, $X_{\text{first}} Y_{\text{last}}$, $Y_{\text{first}} f$ | none |
| $Y\, X$ | $a Y_{\text{first}}$, $Y_{\text{last}} X_{\text{first}}$, $X_{\text{last}} f$ | none |
| $Y\, \bar X$ | $a Y_{\text{first}}$, $Y_{\text{last}} X_{\text{last}}$, $X_{\text{first}} f$ | none |
| $\bar Y\, X$ | $a Y_{\text{last}}$, $Y_{\text{first}} X_{\text{first}}$, $X_{\text{last}} f$ | none |

Because each segment has two different ends and the removed edges are disjoint, the edges in the last four rows are all different from the three removed edges. In the first three rows exactly one removed edge comes back. $\square$

If a segment has one city, it is equal to its reverse, and some rows give the same tour. The implementation tries all 7 rows in each case; the gain formula is still exact, since it counts the three joints.

**Lemma 2 (every 2-opt move is a 3-opt move).** A tour that no 3-opt move improves is 2-optimal.

*Proof.* A 2-opt move on the positions $i < j$ removes the edges after $T[i]$ and after $T[j]$, and reverses $T[i+1..j]$. If $j \le n - 2$, it is the row $\bar X\, Y$ with the triple $(i, j, j+1)$: the third joint is the old edge $\{T[j+1], T[j+2]\}$, which is kept. If $j = n - 1$, then $i \ge 1$, and the move is the row $X\, \bar Y$ with the triple $(0, i, n - 1)$: then $X = T[1..i]$, $Y = T[i+1..n-1]$, and $f = T[0]$, and the row keeps $\{T[0], T[1]\}$ and replaces $\{T[i], T[i+1]\}$ and $\{T[n-1], T[0]\}$ by $\{T[i], T[n-1]\}$ and $\{T[i+1], T[0]\}$, which is the 2-opt move. So a 2-opt move that gains is a 3-opt move that gains. $\square$

**Theorem.** The 3-opt search stops, and for metric costs the tour it returns satisfies

$$\text{ALG} \le 2\sqrt{2} \sum_{i=1}^{n} \frac{1}{\sqrt{i}} \cdot \text{OPT} < 4\sqrt{2}\,\sqrt{n} \cdot \text{OPT}.$$

*Proof.* Each move makes the tour strictly shorter, and there are finitely many tours, so the search stops at a tour that no move improves. By Lemma 2 this tour is 2-optimal. The bound for 2-optimal tours is proved in full on the [2-opt](/two-opt/) page. $\blacksquare$

**Remarks.**

- The bound uses only the 2-opt moves inside the 3-opt neighborhood. Chandra, Karloff and Tovey (1999) proved that for each fixed $k$ there are metric instances with $k$-optimal tours of ratio $\frac{1}{4} n^{1/(2k)}$, which is $\frac{1}{4} n^{1/6}$ for $k = 3$. So 3-optimal tours have no constant ratio. This lower bound is quoted, not proved, here, and the gap between $n^{1/6}$ and $\sqrt{n}$ is not closed by this page.
- The row $Y\,X$ moves the segment $Y$ before $X$ without turning either one. When $Y$ has at most 3 cities, this is an [Or-opt](/or-opt/) move.
