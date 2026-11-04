---
title: Mo's algorithm makes O(n sqrt q) moves
proves: [complexity]
status: full
---

Let $1 \le B \le n$ be the block size, $k = \lceil n / B \rceil$ the number of blocks, and let the queries be sorted by the key $(\lfloor l / B \rfloor, r)$. Let $(l_1, r_1), \ldots, (l_q, r_q)$ be the queries in this order and $(l_0, r_0) = (0, 0)$. A round makes exactly $|l_t - l_{t-1}| + |r_t - r_{t-1}|$ calls of ADD and REMOVE, because each loop moves one end one step towards its target. So the total cost is

$$ C = \sum_{t=1}^{q} |l_t - l_{t-1}| + \sum_{t=1}^{q} |r_t - r_{t-1}|. $$

**Lemma 1 (the right end).** $\sum_t |r_t - r_{t-1}| \le 2 n k$.

*Proof.* Group the rounds by the block $b_t = \lfloor l_t / B \rfloor$; at most $k$ groups are non-empty. Inside a group the $r_t$ are non-decreasing, so the moves inside the group add up to at most $n$. The first round of each group moves $R$ by at most $n$. Over at most $k$ groups the sum is at most $2 n k$. $\square$

**Lemma 2 (the left end).** $\sum_t |l_t - l_{t-1}| \le q B + 2 n + 2 B$.

*Proof.* If $b_t = b_{t-1}$, both left ends lie in the same block of $B$ positions, so $|l_t - l_{t-1}| < B$, and these rounds add up to less than $q B$. Otherwise $b_t > b_{t-1}$ (with $b_0 = 0$ for the start), and $0 < l_t - l_{t-1} < (b_t - b_{t-1} + 1) B$. The blocks increase along these rounds, so the sum of $b_t - b_{t-1}$ over them is at most $k - 1$, and there are at most $k$ such rounds. They add up to less than $(k - 1 + k) B < 2 k B < 2(n + B)$, because $k B < n + B$. $\square$

**Theorem.** With $B = \max(1, \min(n, \lceil n / \sqrt q \rceil))$ and $1 \le q \le n^2$, the algorithm makes $O(n \sqrt q)$ calls of ADD and REMOVE, and with an $O(1)$ cost per call it runs in $O(n \sqrt q + q \log q)$ time.

*Proof.* By Lemmas 1 and 2, $C \le 2 n \lceil n / B \rceil + q B + 4n$. With $B \ge n / \sqrt q$, $n \lceil n / B \rceil \le n (\sqrt q + 1)$. With $B \le n / \sqrt q + 1$, $q B \le n \sqrt q + q \le 2 n \sqrt q$ because $q \le n^2$ gives $\sqrt q \le n$. So $C = O(n \sqrt q + n) = O(n \sqrt q)$. Sorting the keys takes $O(q \log q)$ time, and the other lines of the loop take $O(q)$. $\square$

**The bound of Lemma 1 is tight.** For each block $b$, take the two queries $(bB, bB + 1)$ and $(bB, n)$. In sorted order, $R$ climbs to $n$ in each block and falls back to $(b + 1) B + 1$ at the start of the next one, so $\sum_t |r_t - r_{t-1}| \ge \sum_{b=0}^{k-2} (n - (b + 1) B - 1)$, which is about $n k / 2$.
