---
title: Frequency count is within twice the static optimum, but it is not competitive
proves: [correctness]
status: full
---

**Model.** A list holds $n$ distinct items. A request sequence $\sigma$ has $m$ requests. An access to the item at position $i$ costs $i$. After an access, the accessed item may move forward at no cost (free exchanges). Any other swap of two adjacent items costs $1$ (paid exchanges). Frequency count (FC) uses only free exchanges: after an access to $x$, it increments the count of $x$ (line L6) and moves $x$ forward past every item with a strictly smaller count (lines L7 and L8). For an item $x$, $f_x$ is the number of requests to $x$ in $\sigma$. $\mathrm{SOPT}(\sigma)$ is the cost of the best fixed list, without the cost of setting it up, and $\mathrm{OPT}(\sigma)$ is the cost of the best offline algorithm that starts from the same list and may use paid and free exchanges.

**Feasibility.** Each request is served by an access (lines L4 and L5), and lines L7 and L8 only swap adjacent items, so the list is always a permutation of the items.

**Lemma 1 (order invariant).** At every time, item $x$ is ahead of item $y$ if and only if the count of $x$ is larger than the count of $y$, or the two counts are equal to some $k$ and $x$ reached the count $k$ before $y$ did. For $k = 0$, "reached first" means "is ahead in the initial list".

*Proof.* By induction on the requests. The claim holds at the start, when all counts are $0$. Assume it holds before an access to $x$, whose count is $c$. By the claim, the items ahead of $x$ have counts at least $c$, and those with count exactly $c$ form a block just ahead of $x$, because the list is sorted by count. After line L6, $x$ has count $c + 1$ and is the last item to reach $c + 1$. Lines L7 and L8 move $x$ past exactly the items with count less than $c + 1$ that are ahead of it, which is the block with count $c$, and they stop behind the items with count at least $c + 1$. Then $x$ is behind every item with count at least $c + 1$, which is correct because the items with count $c + 1$ reached it earlier, and ahead of every item with count at most $c$. The relative order of the other items does not change, and their counts do not change. So the claim holds after the access. $\square$

**Lemma 2 (pairwise independence).** The relative order of two items $x$ and $y$ at any time depends only on the subsequence of $\sigma$ formed by the requests to $x$ and to $y$, and on their initial order.

*Proof.* By Lemma 1, the order of $x$ and $y$ depends only on their counts and on which of them reached a given count first, and these depend only on the requests to $x$ and $y$ and on their initial order. $\square$

**Cost by pairs.** An access to $z$ costs $1$ plus the number of items ahead of $z$. Summing over the requests,

$$\mathrm{FC}(\sigma) = m + \sum_{\{x, y\}} B(x, y),$$

where the sum is over all $\binom{n}{2}$ pairs of items and $B(x, y)$ is the number of requests to $x$ or $y$ at which the requested item is behind the other one. For a fixed list, the same sum shows that the cost is $m$ plus, for each pair, the number of requests to the item that is later in the list. That number is at least $\min(f_x, f_y)$, and sorting by decreasing frequency gives exactly $\min(f_x, f_y)$ for all pairs at once. So

$$\mathrm{SOPT}(\sigma) = m + \sum_{\{x, y\}} \min(f_x, f_y).$$

**Lemma 3 (pair bound).** If $f_x \ge f_y$, then $B(x, y) \le 2 f_y + 1$, and $B(x, y) \le 2 f_y$ if $f_x = f_y$.

*Proof.* Let $a$ and $b$ be the counts of $x$ and $y$ just before a request. By Lemma 1, a request to $y$ at which $y$ is behind has $b \le a$, and a request to $x$ at which $x$ is behind has $a \le b$. At most $f_y$ requests go to $y$. The requests to $x$ have distinct values of $a$, namely $0, 1, \ldots, f_x - 1$, and the requests at which $x$ is behind have $a \le b \le f_y$. So at most $\min(f_x, f_y + 1)$ of them are behind. Then $B(x, y) \le f_y + \min(f_x, f_y + 1)$, which is at most $2 f_y + 1$, and at most $2 f_y$ when $f_x = f_y$. $\square$

**Theorem 4 (static bound).** For every sequence $\sigma$ of $m$ requests on a list of $n$ items,

$$\mathrm{FC}(\sigma) \le 2\, \mathrm{SOPT}(\sigma) - m + \binom{n}{2}.$$

*Proof.* By Lemma 3, $B(x, y) \le 2 \min(f_x, f_y) + 1$ for every pair. Then $\mathrm{FC}(\sigma) \le m + 2 \sum \min(f_x, f_y) + \binom{n}{2} = 2\, \mathrm{SOPT}(\sigma) - m + \binom{n}{2}$. $\square$

The factor $2$ is tight. On the list $y, x$, the sequence $x, (y, y, x, x)^f$ makes every access cost $2$, so $\mathrm{FC} = 2m$, while $\mathrm{SOPT} = m + (m - 1)/2$. Here $B(x, y) = 4f + 1 = 2 \min(f_x, f_y) + 1$, so Lemma 3 is tight.

**Theorem 5 (not competitive).** Let $n \ge 2$, start from the list $x_1, \ldots, x_n$, and let a phase be the requests

$$A = x_1^{\,n}\, x_2^{\,n-1} \cdots x_n^{\,1}, \qquad B = x_1^{\,1}\, x_2^{\,2} \cdots x_n^{\,n},$$

where $x^j$ means $j$ requests to $x$ in a row. For the sequence of $k$ phases, $\mathrm{FC} = k\, n (n + 1)^2 / 2$ and $\mathrm{OPT} \le k (3 n^2 - n)$. Hence FC is not $c$-competitive for any constant $c$.

*Proof.* Each item is requested $n + 1$ times in a phase. Assume that a phase starts with the list $x_1, \ldots, x_n$ and all counts equal to some $C$, which is true for the first phase with $C = 0$. During $A$, every count of $x_i$ after an access is at most $C + n - i + 1$, while $x_{i-1}$ already has count $C + n - i + 2$. During $B$, the count of $x_i$ rises to at most $C + n + 1$, while $x_{i-1}$ already has count $C + n + 1$. In both cases the item just ahead does not have a strictly smaller count, so line L7 never moves anything. The phase ends with the same list and all counts equal to $C + n + 1$, so every phase behaves the same way. The cost of one phase is $\sum_i i\,(n + 1) = n (n + 1)^2 / 2$.

For the upper bound on OPT, consider the offline algorithm that runs move-to-front during the phase and then uses paid exchanges to restore $x_1, \ldots, x_n$. In $A$, the first request to $x_i$ finds it at position $i$, and the other $n - i$ requests cost $1$, so $A$ costs $n^2$ and leaves the list $x_n, \ldots, x_1$. In $B$, the first request to $x_i$ finds it at position $n$, and the other $i - 1$ requests cost $1$, so $B$ costs $n^2 + n(n - 1)/2$ and leaves the list $x_n, \ldots, x_1$ again. Restoring the start costs $n(n - 1)/2$ paid exchanges. The total per phase is $3n^2 - n$, so $\mathrm{OPT} \le k (3 n^2 - n)$.

Now fix constants $c$ and $b$. Choose $n \ge 6c$; then $(n + 1)^2 > 6cn > c(6n - 2)$, so $n(n + 1)^2/2 > c (3n^2 - n)$. For $k$ large enough, $k\, n (n + 1)^2/2 > c\, k (3n^2 - n) + b$, so $\mathrm{FC} > c \cdot \mathrm{OPT} + b$. $\square$

**Theorem 6 (trivial upper bound).** On a list of $n$ items, $\mathrm{FC}(\sigma) \le n \cdot \mathrm{OPT}(\sigma)$.

*Proof.* Each access costs at most $n$, so $\mathrm{FC} \le n m$, and every algorithm pays at least $1$ per request, so $\mathrm{OPT} \ge m$. $\square$

So the competitive ratio of FC on lists of $n$ items lies between $(n + 1)^2/(6n - 2)$ and $n$, and it grows linearly in $n$.
