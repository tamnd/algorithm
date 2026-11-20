---
title: Correctness and properties of the Huntington-Hill method
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_n \ge 0$ be integers with $P = \sum_i p_i > 0$, and let $h \ge n$. The quota of state $i$ is $q_i = h p_i / P$. The greedy rule gives every state one seat and then gives the other $h - n$ seats one at a time; each goes to the state with the largest priority $p_i / \sqrt{a_i (a_i + 1)}$, where $a_i$ is its current number of seats, the smallest index among ties.

**Claim 1 (exact comparison).** The method of the page gives the same seats as the greedy rule, with no square roots.

*Proof.* Priorities are nonnegative, so $x \ge y$ exactly when $x^2 \ge y^2$. The heap compares the squares $p_i^2 / (a_i (a_i + 1))$ and $p_j^2 / (a_j (a_j + 1))$ by the integers $p_i^2 \, a_j (a_j + 1)$ and $p_j^2 \, a_i (a_i + 1)$, and breaks ties by the smaller index. After line L3 it holds the key of each state for $a_i = 1$, and lines L5 to L7 replace the key of the winner by its key for the new $a_i$. So line L5 removes the state that the greedy rule picks.

**Claim 2 (divisor form).** Let $\ell = \max_i p_i^2/(a_i (a_i + 1))$ and $u = \min_{i : a_i \ge 2} p_i^2/((a_i - 1) a_i)$ (or $u = \infty$ if no $a_i \ge 2$). Then $\ell \le u$. If $\ell < u$, then for every $M$ with $\ell < M < u$ and $\lambda = \sqrt{M}$, each $a_i$ is $p_i/\lambda$ rounded at the geometric mean: $\sqrt{(a_i - 1) a_i} < p_i/\lambda < \sqrt{a_i (a_i + 1)}$, where the left bound is 0 for $a_i = 1$. Conversely, every vector $b \ge 1$ with sum $h$ that comes from such a rounding for some $\lambda$ satisfies the same inequalities, so the output is the only Huntington-Hill apportionment when $\ell < u$.

*Proof.* The squared keys of the seats given after the first $n$ never increase, because a seat changes only the key of its winner, to a smaller value. So every such key is at least the largest key at the end, which is $\ell$. The last seat of a state with $a_i \ge 2$ had the key $p_i^2/((a_i - 1) a_i)$, so $u \ge \ell$. If $\ell < M < u$, then $p_i^2/M < a_i (a_i + 1)$ for every $i$ and $p_i^2/M > (a_i - 1) a_i$ when $a_i \ge 2$; take square roots. The uniqueness argument is the one of the [D'Hondt method](/dhondt-method/) with $\sqrt{(b - 1) b}$ and $\sqrt{b (b + 1)}$ in place of $b$ and $b + 1$: if $b \ne a$, some $b_i > a_i \ge 1$ and some $b_j < a_j$, and then $M_b \le p_i^2/((b_i - 1) b_i) \le p_i^2/(a_i (a_i + 1)) \le \ell$ and $M_b \ge p_j^2/(b_j (b_j + 1)) \ge p_j^2/((a_j - 1) a_j) \ge u$, which contradicts $\ell < u$.

**Claim 3 (Huntington's pairwise test).** For any two states $i \ne j$ with $a_i \ge 2$, moving one seat from $i$ to $j$ does not lower the relative difference of their representations. Here state $k$ has $r_k = a_k/p_k$ seats per person, and the relative difference of $x, y > 0$ is $\max(x, y)/\min(x, y) - 1$.

*Proof.* By Claim 2, $p_j^2/(a_j (a_j + 1)) \le \ell \le u \le p_i^2/((a_i - 1) a_i)$, that is,
$$\frac{(a_i - 1) a_i}{p_i^2} \le \frac{a_j (a_j + 1)}{p_j^2}. \tag{1}$$
Let $x = a_i/p_i$, $y = a_j/p_j$, $x' = (a_i - 1)/p_i < x$ and $y' = (a_j + 1)/p_j > y$. First, $y' \ge x'$: otherwise $x > x' > y' > y$, and multiplying $x x' > y' y$ contradicts (1). So after the move the ratio is $y'/x'$. If $x < y$, the ratio before is $y/x < y'/x'$. If $x \ge y$, the ratio before is $x/y$, and $y'/x' \ge x/y$ is $y y' \ge x x'$, which is (1).

**Claim 4 (house and population monotone).** The seats for $h + 1$ are those for $h$ plus one seat. If $p'_i \ge p_i$ and $p'_j \le p_j$, then $a'_i < a_i$ and $a'_j > a_j$ cannot both hold, unless one of the two apportionments has $\ell = u$.

*Proof.* The first part holds because the greedy rule for $h + 1$ repeats the steps for $h$. For the second, take $M \in [\ell, u]$ for $p$ and $M' \in [\ell', u']$ for $p'$. If $a'_i < a_i$ and $a'_j > a_j$, then $a_i \ge 2$ and $a'_j \ge 2$, and
$$M' \ge \frac{p'^2_i}{a'_i (a'_i + 1)} \ge \frac{p_i^2}{(a_i - 1) a_i} \ge M \ge \frac{p_j^2}{a_j (a_j + 1)} \ge \frac{p'^2_j}{(a'_j - 1) a'_j} \ge M',$$
so all are equal and $u \le \ell$ for $p$.

**Claim 5 (quota fails).** With $p = (18, 7, 2, 1)$ and $h = 8$, the method gives $(4, 2, 1, 1)$, while $q_1 = 36/7 \approx 5.14$, so state 1 gets less than its lower quota.

*Proof.* After one seat each, the squared keys are $324/2 = 162$, $49/2 = 24.5$, $4/2 = 2$ and $1/2$. The four other seats go to the keys $162$, $324/6 = 54$ and $324/12 = 27$ of state 1, and $24.5$ of state 2. The largest key left is $324/20 = 16.2$ and the smallest key used for a second or later seat is $24.5$, so $\ell < u$ and there is no tie.
