---
title: The strip holds at most 8 points per box, so the algorithm takes O(n log n) time
proves: [time.worst, space.extra]
status: full
---

**Packing lemma.** In a call of REC with $\delta^2 > 0$ after line L10, fix an index $i$ of $S$. The number of indices $j > i$ for which line L15 runs is at most $7$.

*Proof.* Let $s = S[i]$. Line L15 runs for $j$ only while $(S[j].y - s.y)^2 < \delta^2$, and $S$ is sorted by $y$, so every such $S[j]$ satisfies $s.y \le S[j].y < s.y + \delta$. Every item of $S$ satisfies $|x - x_m| < \delta$. So every such $S[j]$, and $s$ itself, lies in the closed rectangle

$$B = [x_m - \delta,\ x_m + \delta] \times [s.y,\ s.y + \delta].$$

Split $B$ into the left square $B_L = [x_m - \delta, x_m] \times [s.y, s.y + \delta]$ and the right square $B_R = [x_m, x_m + \delta] \times [s.y, s.y + \delta]$. Each item of $L$ in $B$ has $x \le x_m$, so it is in $B_L$; each item of $R$ in $B$ is in $B_R$.

Cut $B_L$ into four closed squares of side $\delta/2$. Two points of one small square are at distance at most its diagonal, $\delta/\sqrt{2} < \delta$. Two different items of $L$ are at squared distance at least $\delta^2(L) \ge \delta^2$, so at distance at least $\delta$. Hence each small square holds at most one item of $L$, and $B_L$ holds at most $4$ items of $L$. (An item on a common side of two small squares is counted in one of them; this only lowers the count.) In the same way $B_R$ holds at most $4$ items of $R$. So $B$ holds at most $8$ items of $Q$, one of which is $s$. The indices $j > i$ for which line L15 runs are different items in $B$ other than $s$, so there are at most $7$ of them. $\square$

The test of line L14 is evaluated at most $8$ times for each $i$: at most $7$ times true and once false (or the loop ends at $j = |S|$).

**Cost of one call.** Let $m = |X|$. Line L5 costs $O(1)$ when $m \le 3$. For $m \ge 4$, lines L6 and L7 cost $O(m)$ (copying the two halves), line L8 is one pass over $Y$ with $O(1)$ work per item using the precomputed ranks, line L11 is one pass over $Y$, and the loop of lines L12 to L16 costs $O(|S|) \subseteq O(m)$ by the packing lemma. So the work of a call outside its two recursive calls is at most $c\,m$ for a constant $c$, and at least $m$ because line L8 reads every item of $Y$.

**Recurrence.** Let $T(m)$ be the worst-case time of REC on $m$ items. Then $T(m) \le c$ for $m \le 3$ and

$$T(m) \le T(\lfloor m/2 \rfloor) + T(\lceil m/2 \rceil) + c\,m \qquad (m \ge 4).$$

We show $T(m) \le c\,m \lceil \lg m \rceil + c\,m$ for $m \ge 2$ by strong induction. For $2 \le m \le 3$, $T(m) \le c \le c\,m$. For $m \ge 4$ let $m_1 = \lfloor m/2 \rfloor$ and $m_2 = \lceil m/2 \rceil$, both at least 2. If $2^{k-1} < m \le 2^k$ then $2^{k-2} < \lceil m/2 \rceil \le 2^{k-1}$, so $\lceil \lg m_2 \rceil = \lceil \lg m \rceil - 1$, and $\lceil \lg m_1 \rceil \le \lceil \lg m_2 \rceil$ because $m_1 \le m_2$. Applying the hypothesis to both halves,

$$T(m) \le c\,(m_1 + m_2)(\lceil \lg m \rceil - 1) + c\,(m_1 + m_2) + c\,m = c\,m \lceil \lg m \rceil + c\,m .$$

So $T(n) = O(n \log n)$. Adding the $O(n \log n)$ presort of line L2 gives $O(n \log n)$ for CLOSEST-PAIR on the real RAM. For a lower bound on this algorithm, when no two items are equal, line L10 never returns early, every call with $m \ge 4$ does at least $m$ steps in line L8, and the calls of one recursion level partition the items. There are $\lfloor \lg (n/3) \rfloor$ or more levels with all calls of size at least 4, so the time is $\Omega(n \log n)$; and the presort with a comparison sort is $\Omega(n \log n)$ in the worst case by the [comparison sort lower bound](/comparison-sort-lower-bound/). Hence $\Theta(n \log n)$.

**Space.** $X$, $Y$ and the ranks take $\Theta(n)$. A call allocates $O(m)$ for $X_L$, $X_R$, $Y_L$, $Y_R$ and $S$, and the calls on one root-to-leaf path have sizes $n, \lceil n/2 \rceil, \ldots$, which sum to at most $2n + O(\log n)$. So the extra space is $\Theta(n)$, with a recursion depth of $\lceil \lg n \rceil$. $\blacksquare$
