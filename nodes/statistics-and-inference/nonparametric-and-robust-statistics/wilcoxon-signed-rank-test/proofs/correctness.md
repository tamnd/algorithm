---
title: The signed-rank test computes the exact conditional null law, and each p-value is valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. $D_1, \ldots, D_N$ are independent, and under $H_0$ each $D_i$ has the same law as $-D_i$. Let $Z = \{i : D_i \ne 0\}$, $n = \lvert Z \rvert$, and $A = (\lvert D_i \rvert)_{i \in Z}$.

**Claim 1 (the signs given the sizes).** Under $H_0$, conditional on $Z$ and $A$, the signs $\varepsilon_i = \mathbf{1}\{D_i > 0\}$, $i \in Z$, are independent and each equals 1 with probability $1/2$.

*Proof.* Write $D_i = \sigma_i \lvert D_i \rvert$ with $\sigma_i \in \{-1, 0, 1\}$. Symmetry gives $(\sigma_i, \lvert D_i \rvert) \overset{d}{=} (-\sigma_i, \lvert D_i \rvert)$, so for every Borel set $B \subseteq (0, \infty)$, $P(\sigma_i = 1, \lvert D_i \rvert \in B) = P(\sigma_i = -1, \lvert D_i \rvert \in B)$. Hence, given $\lvert D_i \rvert$ and $D_i \ne 0$, $\sigma_i$ is $\pm 1$ with probability $1/2$ each. The pairs $(\sigma_i, \lvert D_i \rvert)$ are independent over $i$, so these conditional laws are independent. $\square$

**Claim 2 (the null law).** Let $r_1, \ldots, r_n$ be the doubled midranks of $A$, which line L2 computes and which depend only on $A$. Conditional on $Z$ and $A$, $2W^+ = \sum_{i} \varepsilon_i r_i$, and each of the $2^n$ vectors $\varepsilon \in \{0, 1\}^n$ has probability $2^{-n}$. So $P(2W^+ = s \mid Z, A) = c(s)/2^n$, where $c(s)$ is the number of subsets of the multiset $\{r_1, \ldots, r_n\}$ (subsets of indices) with sum $s$.

*Proof.* Immediate from Claim 1, because the ranks are functions of $A$. $\square$

**Claim 3 (the dynamic program).** After the iteration $i$ of line L5, $c[s]$ is the number of index sets $J \subseteq \{1, \ldots, i\}$ with $\sum_{j \in J} r_j = s$, for every $0 \le s \le T$.

*Proof.* Induction on $i$. Before the loop, $c[0] = 1$ (the empty set) and $c[s] = 0$ for $s > 0$. In iteration $i$, a set $J \subseteq \{1, \ldots, i\}$ with sum $s$ either leaves out $i$, and is counted by the old $c[s]$, or contains $i$, and then $J \setminus \{i\}$ has sum $s - r_i$ and is counted by the old $c[s - r_i]$. Line L6 visits $s$ in decreasing order, so when it reads $c[s - r_i]$ with $r_i \ge 1$, that entry has not yet been updated in this iteration and still holds the old value. Entries with $s < r_i$ are not changed, which is correct because no set containing $i$ has such a sum. $\square$

**Claim 4 (the returned values).** Line L3 gives $w = 2W^+$. By Claims 2 and 3, line L7 gives $U = 2^n P(W^+ \ge W^+_{obs} \mid Z, A)$ and $L = 2^n P(W^+ \le W^+_{obs} \mid Z, A)$, and line L8 returns the three p-values of the page exactly.

**Claim 5 (validity).** For every $\alpha \in [0, 1]$, $P_{H_0}(p \le \alpha) \le \alpha$ for each p-value.

*Proof.* Condition on $Z$ and $A$, so that the null law of $W^+$ is the discrete law of Claim 2. For the "greater" p-value, the set $\{v : P(W^+ \ge v) \le \alpha\}$ is empty or has a least element $v^*$, and the conditional probability of rejection is $P(W^+ \ge v^*) \le \alpha$. The "less" case is the same in the other direction. For the two-sided p-value, rejection forces one of the two one-sided p-values to be at most $\alpha/2$, and each event has conditional probability at most $\alpha/2$. Averaging over $(Z, A)$ keeps the bound. $\square$

**Claim 6 (symmetry and the two-sided rule).** $c(s) = c(T - s)$, so the conditional law of $W^+$ is symmetric about $T/4 = E(W^+ \mid Z, A)$, and $2 \min(P_{lo}, P_{hi})$, capped at 1, equals $P(\lvert W^+ - T/4 \rvert \ge \lvert w/2 - T/4 \rvert)$.

*Proof.* Taking complements, $J \mapsto \{1, \ldots, n\} \setminus J$, is a bijection from the sets with sum $s$ to the sets with sum $T - s$. Take $w/2 \le T/4$; the other case is symmetric. The event $\lvert W^+ - T/4 \rvert \ge T/4 - w/2$ is the union of $W^+ \le w/2$ and $W^+ \ge T/2 - w/2$, which by symmetry have the same probability $P_{lo}$. If $w/2 < T/4$ the two events are disjoint and the union has probability $2 P_{lo}$; also $P_{lo} \le P_{hi}$ there. If $w/2 = T/4$ the event is certain, and $2 \min(P_{lo}, P_{hi}) \ge 1$, so the cap gives 1. $\square$

**Moments.** Given $A$, $W^+ = \sum_i \varepsilon_i R_i$ with $R_i = r_i/2$, so $E W^+ = \frac{1}{2} \sum_i R_i = n(n+1)/4$, because midranks keep the sum $n(n+1)/2$. $\operatorname{Var} W^+ = \frac{1}{4} \sum_i R_i^2$. A tie group of size $t$ that covers the ranks $a + 1, \ldots, a + t$ has midrank $m = a + (t + 1)/2$, and replacing the ranks by $m$ lowers the sum of squares by $\sum_{k=1}^{t} (a + k - m)^2 = (t^3 - t)/12$. So $\operatorname{Var} W^+ = n(n+1)(2n+1)/24 - \sum_j (t_j^3 - t_j)/48$. The tests check both formulas in exact fractions.

**Cost.** Line L2 sorts in $O(n \log n)$. $T = \sum_i r_i = n(n+1)$, so line L6 does at most $T$ additions for each of the $n$ values of $i$: $\Theta(n^3)$ additions in total, and the array has $T + 1 = \Theta(n^2)$ entries. Line L7 costs $O(n^2)$. $\square$
