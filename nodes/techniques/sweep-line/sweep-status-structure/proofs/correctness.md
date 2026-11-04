---
title: The sweep status keeps the active segments in their order along the sweep line
proves: [correctness]
status: full
---

We use the pseudocode of the page. $S$ is a finite set of segments, none vertical, no two overlapping (two distinct segments share at most one point). A segment $s$ has endpoints $(x_1(s), y_1(s))$ and $(x_2(s), y_2(s))$ with $x_1(s) < x_2(s)$, slope $m_s$, and $y_s(x)$ for $x \in [x_1(s), x_2(s)]$ as on the page. For a position $x$, the *active set* is $A(x) = \{ s \in S : x_1(s) \le x < x_2(s) \}$, and the key at $x$ is $\kappa_x(s) = (y_s(x), m_s)$, compared lexicographically.

**Lemma 1 (keys are distinct).** If $s \ne t$ are both in $A(x)$, then $\kappa_x(s) \ne \kappa_x(t)$.

*Proof.* If $y_s(x) = y_t(x)$ and $m_s = m_t$, both segments lie on the same line through $(x, y_s(x))$, and both contain the points of that line with abscissa in $[x, \min(x_2(s), x_2(t))]$, an interval of positive length since $x < x_2(s)$ and $x < x_2(t)$. So they share infinitely many points and overlap, a contradiction. $\square$

**Lemma 2 (the key order is the order just to the right).** Let $s, t \in A(x)$ with $s \ne t$. There is an $\varepsilon > 0$ such that $\kappa_x(s) < \kappa_x(t)$ if and only if $y_s(x') < y_t(x')$ for each $x' \in (x, x + \varepsilon)$.

*Proof.* For $x'$ in both domains, $f(x') = y_s(x') - y_t(x') = (y_s(x) - y_t(x)) + (m_s - m_t)(x' - x)$. If $y_s(x) \ne y_t(x)$, then by continuity $f$ has the sign of $y_s(x) - y_t(x)$ on some interval $(x, x + \varepsilon)$, and that sign decides $\kappa$. If $y_s(x) = y_t(x)$, then $m_s \ne m_t$ by Lemma 1, and $f(x') = (m_s - m_t)(x' - x)$ has the sign of $m_s - m_t$ for each $x' > x$, which again decides $\kappa$. $\square$

**Lemma 3 (no crossing, no change of order).** Let $s, t$ be two segments that both span the closed interval $[u, v]$ with $u < v$, and that have no common point with abscissa in the open interval $(u, v)$. Then the sign of $y_s(x') - y_t(x')$ is the same nonzero value for each $x' \in (u, v)$, and the same sign, or zero, at $u$ and at $v$.

*Proof.* The function $f(x') = y_s(x') - y_t(x')$ is affine on $[u, v]$. It has no zero in $(u, v)$, since a zero is a common point. An affine function with a sign change on an interval has a zero inside it (it is continuous), so $f$ has one sign on $(u, v)$. By continuity, $f(u)$ and $f(v)$ have this sign or are $0$. $\square$

**The sweep.** The event positions are $x^{(1)} < x^{(2)} < \cdots < x^{(r)}$: the abscissas of all endpoints and of all points that two segments of $S$ share. At each event position $x$, the sweep does, in this order:

1. SET-X$(T, x)$;
2. DELETE$(T, s)$ for each stored $s$ with $x_2(s) = x$;
3. for each point $p$ with abscissa $x$ through which two or more stored segments pass, reverse the contiguous block of these segments (SWAP when there are two);
4. INSERT$(T, s)$ for each $s$ with $x_1(s) = x$.

**Claim.** After step 4 at the event position $x$, the list $T$ holds exactly $A(x)$, sorted by $\kappa_x$ in increasing order. Each ABOVE, BELOW and NEIGHBORS-OF-POINT made at this moment returns the neighbors in the order of $A(x)$ just to the right of $x$.

*Proof.* By induction on the events. Before the first event $T$ is empty, and the steps at $x^{(1)}$ are the step below with an empty list.

*Step.* Assume the claim after the event $u = x^{(j)}$, and let $v = x^{(j+1)}$. Between them no segment starts or ends and no two segments meet (each meeting point is an event), so each $s \in A(u)$ spans $[u, v]$, by $u < x_2(s)$ and the fact that $x_2(s)$ is an event position, so $x_2(s) \ge v$.

*SET-X.* Let $s, t$ be two consecutive entries of $T$, $s$ first. By the hypothesis $\kappa_u(s) < \kappa_u(t)$, so by Lemma 2 $y_s < y_t$ at some points of $(u, v)$. By Lemma 3, $y_s < y_t$ on all of $(u, v)$ and $y_s(v) \le y_t(v)$. So after line L1 the values $y_s(v)$ do not decrease along $T$ (*the y-order*), and the entries that tie at $v$ are consecutive. Two entries that tie at $v$ share the point $(v, y)$.

*LOCATE under the y-order.* Line L4 is a binary search for the first position whose value is at least $y_s(v)$; it is correct because the values do not decrease. All entries with the value $y_s(v)$ follow it contiguously, and $s$ is one of them, so the loop of lines L5 to L8 reaches $s$ and returns its position. It stops after at most $b$ iterations, where $b$ is the size of the block, because $i$ grows by 1 each time and the block ends.

*Step 2.* DELETE removes one entry; a sublist of a list with the y-order has the y-order. After step 2, $T$ holds the $s \in A(u)$ with $x_2(s) > v$.

*Step 3.* Let $p = (v, y)$ and $B$ the block of stored segments through $p$, $|B| \ge 2$. Each of them has $x_2 > v$ and $x_1 \le u < v$, so $p$ is interior to each. By the SET-X paragraph, the block is in increasing order of $y$ on $(u, v)$, so just to the left of $v$. For $x' < v$ close to $v$, $y_s(x') = y - m_s (v - x')$, so increasing order of $y$ just left of $v$ is decreasing order of slope. Reversing the block gives increasing order of slope, which is $\kappa_v$ order inside the block, since all have the same $y$. For two segments the reversal is line L14, and the precondition of SWAP holds: $t$ is directly above $s$ and they meet at $p$. Reversal moves entries only inside a block of equal values, so the y-order holds. After step 3, the list is sorted by $\kappa_v$: entries with different values are in y-order, and entries with equal values form one block through one point, now in slope order (a block of size 1 is sorted).

*Step 4.* Before each insert the list is sorted by $\kappa_v$ and its entries are in $A(v)$, so their keys are distinct by Lemma 1. Line L2 finds the first position with a larger key, so all entries before it have a key less than or equal to $\kappa_v(s)$, and by Lemma 1 (applied to $s$, which is in $A(v)$ since $x_1(s) = v < x_2(s)$) strictly less. Line L3 inserts $s$ there, and the list stays sorted by $\kappa_v$.

After step 4 the list holds the $s \in A(u)$ with $x_2(s) > v$, which are the segments of $A(v)$ with $x_1(s) < v$ (each of them has $x_1(s) \le u$ because no segment starts in $(u, v)$), together with the $s$ with $x_1(s) = v$. That is $A(v)$, sorted by $\kappa_v$.

*Queries.* ABOVE and BELOW read the entries next to the position that LOCATE returns, so they return the neighbors in $\kappa_v$ order, which by Lemma 2 is the order along the line just to the right of $v$. For NEIGHBORS-OF-POINT$(T, y)$, lines L15 and L16 are binary searches in the non-decreasing values: positions before $lo$ have value $< y$, positions from $hi$ on have value $> y$, and positions $lo$ to $hi - 1$ have value $y$. So $T[lo - 1]$ is the highest stored segment strictly below $(v, y)$ and $T[hi]$ the lowest one strictly above, or NIL when there is none. $\square$

**Between events.** The same argument with Lemma 3 shows that at each $x'$ strictly between two events, the list is strictly increasing in $y_s(x')$ and holds $A(x')$, so SET-X to such a position followed by queries also gives the order along the line. $\blacksquare$
