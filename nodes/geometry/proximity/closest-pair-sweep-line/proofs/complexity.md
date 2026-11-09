---
title: The plane sweep compares each point with at most 8 others and takes O(n log n) time
proves: [time.worst, space.extra]
status: full
---

**Packing lemma.** In step $k$ with $\delta^2 = D_k$ finite at line L8, lines L10 and L14 together compute at most $8$ distances.

*Proof.* Let $\delta = \sqrt{D_k} > 0$ (if $D_k = 0$, both walks stop before their first comparison, since no square is less than $0$). Every $q$ compared in lines L10 or L14 is in $T$ and satisfies $(q.y - P[k].y)^2 < \delta^2$ with the current $\delta^2 \le D_k$, and $(P[k].x - q.x)^2 < D_k$ because $q$ survived line L6, with $q.x \le P[k].x$. So $q$ lies in the rectangle

$$R = (P[k].x - \delta,\ P[k].x] \times (P[k].y - \delta,\ P[k].y + \delta).$$

The compared items have indices less than $k$, so any two of them are at squared distance at least $D_k$, at distance at least $\delta$. Cut the closure of $R$ into the $2 \times 4$ grid of closed squares of side $\delta / 2$. Two points in one square are at distance at most $\delta/\sqrt{2} < \delta$, so each square holds at most one compared item (assign a point on a shared side to any one square). Hence at most $8$ items are compared. $\square$

**Step cost.** Each walk makes one first call (line L8 or L12), then one more call (line L11 or L15) after each comparison, and stops after a failed test or when no element is left. So step $k$ makes at most $8 + 2 = 10$ successor or predecessor calls and at most $10$ tests in lines L9 and L13 that do not lead to a comparison. With $D_k = \infty$ (only for $k \le 1$), $T$ has at most one element and the step makes at most one comparison.

**Total time.** Line L2 sorts in $O(n \log n)$ time. Over the whole run, line L16 runs $n$ times and line L7 at most $n$ times, since each item is deleted once; the loop test of line L6 fails once per step. With a balanced search tree, or the Fenwick tree over the precomputed $y$-ranks used in the implementation, insert, delete, successor and predecessor take $O(\log n)$ time. So the time is

$$O(n \log n) + n \cdot O(1) \cdot O(\log n) + 2n \cdot O(\log n) = O(n \log n).$$

The sort in line L2 makes $\Omega(n \log n)$ comparisons in the worst case for any comparison sort, so the worst-case time is $\Theta(n \log n)$.

**Space.** The sorted array, the ranks and the tree hold $O(1)$ words per item, so the extra space is $\Theta(n)$. There is no recursion. $\blacksquare$
