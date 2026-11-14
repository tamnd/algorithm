---
title: The Mann-Whitney test computes the exact conditional null law of U, and each p-value is valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $N = m + n$, let $v_1, \ldots, v_N$ be the pooled values with the $x$ values first, and let $r_1, \ldots, r_N$ be their doubled midranks (line L1).

**Claim 1 (U from ranks).** $2U = \sum_{i=1}^m r_i - m(m+1)$, as line L2 computes.

*Proof.* The midrank of $x_i$ is $1 + \#\{\text{pooled values} < x_i\} + \frac{1}{2}(\#\{\text{pooled values} = x_i\} - 1)$. Sum over $i$ and split the pooled values into $x$ values and $y$ values. The $x$ part gives $\sum_i [\#\{x_l < x_i\} + \frac{1}{2}\#\{l \ne i : x_l = x_i\}] = \binom{m}{2}$, because each unordered pair of $x$ values contributes exactly 1 (either one is smaller, or both get $\frac{1}{2}$). The $y$ part gives $\sum_{i, j} [\mathbf{1}\{y_j < x_i\} + \frac{1}{2}\mathbf{1}\{y_j = x_i\}] = U$. So $\sum_i R_i = m + \binom{m}{2} + U = m(m+1)/2 + U$. $\square$

**Claim 2 (the null law).** Under $H_0$, conditional on the multiset of pooled values, the set $S$ of positions (in the sorted pooled order) taken by the $x$ values is uniform over the $\binom{N}{m}$ subsets of size $m$, and $2U = \sum_{i \in S} r_i - m(m + 1)$.

*Proof.* Under $H_0$ the $N$ variables are independent with the same law, so their joint law is invariant under permutations: the vector is exchangeable. Given the multiset of values, every assignment of the values to the $N$ slots that is consistent with it has the same conditional probability, so the set of slots holding the first $m$ variables is uniform. Midranks are functions of the multiset, so Claim 1 gives the formula. $\square$

**Claim 3 (the table).** After line L5 has processed the values $1, \ldots, i$, $c[j][s]$ is the number of $j$-element sets $J \subseteq \{1, \ldots, i\}$ with $\sum_{l \in J} r_l = s$, for $0 \le j \le k$ and $0 \le s \le top$.

*Proof.* Induction on $i$. At the start only the empty set exists, so $c[0][0] = 1$ and every other entry is 0. A $j$-set inside $\{1, \ldots, i\}$ either leaves out $i$ (counted by the old $c[j][s]$) or is $J' \cup \{i\}$ for a $(j-1)$-set $J'$ with sum $s - r_i$ (counted by the old $c[j - 1][s - r_i]$). Line L5 runs $j$ downward, so $c[j - 1]$ is still the old row when $c[j]$ is updated; row $0$ never changes, which is correct because only the empty set has size 0. Every sum of $k$ doubled ranks is at most $top$, so no count is lost. $\square$

**Claim 4 (the conversion).** Line L6 gives the number $c(u)$ of size-$m$ sets $S$ with $2U = u$.

*Proof.* If $k = m$, apply Claim 2 directly to $c[m][s]$. If $k = n < m$, the complement $T = \{1, \ldots, N\} \setminus S$ is an $n$-set, and $S \mapsto T$ is a bijection. The pairs $(x_i, y_j)$ split into $x > y$, $x < y$ and $x = y$, so $U_x + U_y = mn$, and Claim 1 for the $y$ sample gives $2U_y = \sum_{l \in T} r_l - n(n+1)$. So $2U_x = 2mn - (s - n(n+1))$ with $s = \sum_{l \in T} r_l$. $\square$

**Claim 5 (validity).** Lines L7 and L8 return $P_{hi}$, $P_{lo}$ and the doubled smaller tail of the conditional null law, and for every $\alpha$, $P_{H_0}(p \le \alpha) \le \alpha$.

*Proof.* By Claims 2 to 4, $A / \binom{N}{m}$ and $B / \binom{N}{m}$ are the exact conditional tails. For a one-sided p-value, the rejection set $\{u : P(2U \ge u) \le \alpha\}$ is empty or an upper set with least element $u^*$, and its conditional probability is $P(2U \ge u^*) \le \alpha$; the lower tail is the same. For the two-sided p-value, $p \le \alpha$ forces one tail to be at most $\alpha/2$, and each such event has conditional probability at most $\alpha/2$. This needs no symmetry, so it holds with ties. Averaging over the multiset of pooled values gives the unconditional bound. $\square$

**Claim 6 (symmetry without ties).** If the values are distinct, $c(u) = c(2mn - u)$.

*Proof.* Without ties $r_l = 2l$. The map $S \mapsto \{N + 1 - l : l \in S\}$ is a bijection on $m$-sets and sends the doubled rank sum $s$ to $2m(N + 1) - s$, hence $2U = s - m(m+1)$ to $2m(N+1) - s - m(m+1) = 2mn - 2U$. $\square$

With ties the reflection changes the tie pattern, and the law can be asymmetric; the tests give an example with ranks $1, 2.5, 2.5, 4, 5$.

**Moments.** Under the uniform law of $S$, $E \sum_{i \in S} R_i = m (N+1)/2$, so $E U = mn/2$. Sampling $m$ of $N$ values without replacement, $\operatorname{Var} \sum_{i \in S} R_i = \frac{m n}{N(N - 1)} \sum_{l} (R_l - \bar R)^2$. Without ties $\sum_l (R_l - \bar R)^2 = (N^3 - N)/12$, and a tie group of size $t$ lowers it by $(t^3 - t)/12$. This gives the variance on the page; the tests check it in exact fractions.

**Cost.** With $k = \min(m, n)$, $top = k(2N - k + 1)$. Line L5 does at most $top$ additions for each pair $(i, j)$ with $1 \le i \le N$ and $1 \le j \le k$, so $O(N k \cdot kN) = O(m^2 n^2)$, because $k N \le 2 m n$. For distinct values the inner range has length $top - r_i + 1 \ge top - 2N + 1$, which is $\Theta(kN)$ when $k \ge 2$, so the bound is tight. The table has $(k+1)(top+1) = \Theta(m n \min(m, n))$ entries. $\square$
