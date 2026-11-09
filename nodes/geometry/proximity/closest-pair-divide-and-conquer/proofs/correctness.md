---
title: The divide and conquer algorithm returns a closest pair
proves: [correctness, termination]
status: full
---

**Notation.** The items are positions in the input list, so two items can have equal coordinates. For a set $Q$ of at least two items let $\delta^2(Q) = \min\{\|p - q\|^2 : p, q \in Q,\ p \ne q\}$. "REC is correct on $(X, Y)$" means: $X$ and $Y$ hold the same set $Q$ of $m \ge 2$ items, $X$ is sorted by $(x, y)$, $Y$ by $(y, x)$, and REC returns $(\delta^2(Q), p, q)$ with $p \ne q \in Q$ and $\|p - q\|^2 = \delta^2(Q)$.

**Claim.** For $n \ge 2$, CLOSEST-PAIR returns two different items $p, q$ of $P$ with $\|p - q\|^2 = \delta^2(P)$. For $n < 2$ it returns none. Every call stops.

**Lemma 1 (the split).** Let $m \ge 4$, $h = \lfloor m/2 \rfloor$ and $x_m = X[h].x$. Then $X_L = X[0 \ldots h-1]$ and $X_R = X[h \ldots m-1]$ partition $Q$ into sets $L$ and $R$ of sizes $h \ge 2$ and $m - h \ge 2$; every item of $L$ has $x \le x_m$ and every item of $R$ has $x \ge x_m$; and $Y_L$, $Y_R$ hold the items of $L$ and $R$ in $(y, x)$-order.

*Proof.* $X$ is sorted by $(x, y)$, so $x$ is non-decreasing along $X$: items before position $h$ have $x \le x_m$ and items from $h$ on have $x \ge x_m$. Since $m \ge 4$, $h \ge 2$ and $m - h \ge 2$. The global rank of an item is its position in the global $x$-order, and $X$ is a contiguous run of that order (by induction on the calls: the top call has the whole order, and each call passes a prefix and a suffix of its run). So an item of $Q$ is in $X_L$ exactly when its rank is less than the rank of $X[h]$, which is the test of line L8. Line L8 keeps the order of $Y$, so $Y_L$ and $Y_R$ are sorted by $(y, x)$. $\square$

**Lemma 2 (crossing pairs are in the strip and close in the scan).** Let $\delta^2 = \min(\delta^2(L), \delta^2(R)) > 0$, and let $a \in L$, $b \in R$ with $\|a - b\|^2 < \delta^2$. Then both $a$ and $b$ are in $S$ (line L11), and if $a$ comes before $b$ in $S$ (otherwise swap the names), then the loop of line L14 started at $i = $ the index of $a$ reaches $j = $ the index of $b$.

*Proof.* $a.x \le x_m \le b.x$ by Lemma 1, so $(a.x - x_m)^2 \le (a.x - b.x)^2 \le \|a - b\|^2 < \delta^2$, and the same for $b$. So both pass the test of line L11. $S$ is sorted by $(y, x)$, so every item $c$ between $a$ and $b$ in $S$ has $a.y \le c.y \le b.y$, hence $(c.y - a.y)^2 \le (b.y - a.y)^2 \le \|a - b\|^2 < \delta^2$. So the test of line L14 is true at each $j$ from the index of $a$ plus one up to and including the index of $b$, and the loop reaches $b$. $\square$

**Lemma 3 (REC is correct).** By strong induction on $m$.

*Base, $m \le 3$.* Since $m \ge 2$, line L5 compares all pairs of $Q$ and returns a pair with the smallest squared distance.

*Step, $m \ge 4$.* By Lemma 1 both recursive calls in line L9 get valid arguments with $2 \le h,\ m - h < m$. By the induction hypothesis they return closest pairs of $L$ and of $R$, and line L9 keeps the better one, so after line L9 $best.d2 = \delta^2 = \min(\delta^2(L), \delta^2(R))$ and $best$ is a pair of $Q$.

If $\delta^2 = 0$, line L10 returns a pair at distance 0, which is the smallest possible value, so it is a closest pair of $Q$.

Otherwise, every pair of $Q$ is inside $L$, inside $R$, or crossing. Let $(a^*, b^*)$ be a closest pair of $Q$. If $\|a^* - b^*\|^2 = \delta^2$, $best$ already has the optimal value, and lines L12 to L16 only replace it by strictly smaller values of pairs of $Q$, of which there are none; so the returned value stays $\delta^2(Q)$. If $\|a^* - b^*\|^2 < \delta^2$, the pair is crossing, and by Lemma 2 line L15 evaluates it, so at the end $best.d2 \le \|a^* - b^*\|^2 = \delta^2(Q)$. Every value that line L15 stores is the squared distance of two different items of $Q$, so $best.d2 \ge \delta^2(Q)$. Hence REC returns a closest pair. $\square$

**Termination.** Each recursive call has a strictly smaller $m$ (Lemma 1), and each loop of lines L12 to L16 increases $i$ or $j$ by 1 up to $|S|$. So every call stops.

**Proof of the claim.** For $n < 2$ line L1 returns none. For $n \ge 2$, line L2 builds $X$ and $Y$ with the properties of the definition, and Lemma 3 applied to the top call gives the result. $\blacksquare$
