---
title: With the exact change of rate, sticky sampling is in the ideal state, meets the guarantee, and keeps at most 2t entries in expectation
proves: [correctness]
status: full
---

Let $t = (1/\varepsilon) \ln(1/(s\delta))$ with $0 < \varepsilon < s < 1$ and $0 < \delta < 1$. After $N$ items, let $r$ be the current rate. By line L2, $N \le 2rt$, and if $r \ge 2$, the rate became $r$ when $N$ first exceeded $2(r/2)t = rt$, so $rt < N$.

**The ideal state.** Fix an item $x$ with $k$ occurrences so far. Give its occurrences independent uniform numbers $U_1, U_2, \ldots$ in $[0, 1)$. The *ideal state at rate $r$* is: $x$ has an entry if some $U_j < 1/r$ with $j \le k$, and then its count is $k - L + 1$, where $L$ is the first such $j$. So with $q = 1/r$,
$$ \Pr[L = l] = (1 - q)^{l-1} q \quad (1 \le l \le k), \qquad \Pr[\text{no entry}] = (1 - q)^k . $$
For the whole table, the items are independent. The algorithm uses separate coins for separate items, so it is enough to follow one item.

**Lemma 1 (a new occurrence).** If the entry of $x$ is in the ideal state at rate $r$ for $k$ occurrences, then after lines L4 and L5 for occurrence $k + 1$ at the same rate, it is in the ideal state for $k + 1$ occurrences.

*Proof.* If $x$ has an entry, then $L \le k$, and in the ideal state the count grows by 1, as in line L4. If $x$ has no entry, then $U_1, \ldots, U_k \ge q$, and in the ideal state $x$ gets the entry with count 1 exactly when $U_{k+1} < q$, which has probability $q$, independently of the past. This is line L5. $\square$

**Lemma 2 (a change of rate).** If the entry of $x$ is in the ideal state at rate $r$ for $k$ occurrences, then after ADJUST$(S, 2r)$ it is in the ideal state at rate $r' = 2r$.

*Proof.* Use the same numbers $U_j$. Let $L$ be the first $j \le k$ with $U_j < 1/r$, and let $L'$ be the first $j \le k$ with $U_j < 1/r'$, where "none" means there is no such $j$. Since $1/r' < 1/r$, $L' \ge L$, and $L$ = none implies $L'$ = none. Condition on $L = l \le k$. This event depends only on $U_1, \ldots, U_l$: it says $U_1, \ldots, U_{l-1} \ge 1/r$ and $U_l < 1/r$. So given it,

- $U_l$ is uniform in $[0, 1/r)$, and $U_l < 1/r'$ with probability $1/2$;
- $U_{l+1}, \ldots, U_k$ are still independent and uniform in $[0, 1)$, so each is below $1/r'$ with probability $1/r'$, independently.

Hence, given $L = l$: $L' = l$ with probability $1/2$; otherwise $L' = l + 1 + G$, where $G$ is the number of failures before the first success in independent trials with success $1/r'$, and $L'$ = none if $l + 1 + G > k$. In terms of the count $c = k - l + 1$: the new count is $c$ with probability $1/2$, and otherwise $c - 1 - G$, or 0 if $G \ge c - 1$. This is lines L7 to L9, with $G$ cut at $c - 1$. So ADJUST produces the conditional law of $L'$ given $L$, and $L'$ is the start of the ideal state at rate $r'$. $\square$

**Theorem 1 (ideal state).** At every time, the table of the algorithm has the same distribution as the ideal state at the current rate $r$.

*Proof.* By induction on the steps, with Lemma 1 for each item and Lemma 2 for each change of rate. At the start the table is empty and $r = 1$, which is the ideal state. $\square$

**Theorem 2 (guarantee).** At each time, $S[x] \le f_x$ for every $x$, and with probability at least $1 - \delta$, every item with $f_x \ge sN$ has $S[x] \ge f_x - \varepsilon N$. On this event, STICKY-REPORT returns every item with $f_x \ge sN$ and no item with $f_x < (s - \varepsilon) N$.

*Proof.* An entry counts occurrences from its start, so $S[x] \le f_x$ always. Fix $x$ with $f_x \ge sN$. Then $f_x > \varepsilon N$, so $f_x \ge \lfloor \varepsilon N \rfloor + 1$. The estimate is low by more than $\varepsilon N$ exactly when $L - 1 > \varepsilon N$ or there is no entry, that is, when the first $\lfloor \varepsilon N \rfloor + 1$ occurrences are not sampled. By Theorem 1, this has probability $(1 - 1/r)^{\lfloor \varepsilon N \rfloor + 1}$. If $r = 1$, this is 0. If $r \ge 2$, then $N > rt$, and with $1 - u \le e^{-u}$,
$$ \left(1 - \frac{1}{r}\right)^{\lfloor \varepsilon N \rfloor + 1} \le e^{-\varepsilon N / r} < e^{-\varepsilon t} = s\delta . $$
At most $1/s$ items have $f_x \ge sN$, because their counts add up to at most $N$. By the union bound, the probability that one of them is low by more than $\varepsilon N$ is less than $(1/s) \cdot s\delta = \delta$. On the other event, each such $x$ has $S[x] \ge f_x - \varepsilon N \ge (s - \varepsilon) N$ and is reported, and an item with $f_x < (s - \varepsilon) N$ has $S[x] \le f_x < (s - \varepsilon) N$ and is not reported. $\square$

**Theorem 3 (space).** At each time, $\mathbb{E}[|S|] \le N/r \le 2t$.

*Proof.* By Theorem 1, item $x$ has an entry with probability $1 - (1 - 1/r)^{f_x}$. By Bernoulli's inequality, $(1 - 1/r)^{f_x} \ge 1 - f_x / r$, so this probability is at most $f_x / r$. By linearity of expectation, $\mathbb{E}[|S|] \le \sum_x f_x / r = N / r$, and $N \le 2rt$ by line L2. $\blacksquare$

**Remark (the fair-coin rule).** The rule of the paper replaces lines L7 and L8 by: subtract 1 for each tails of a fair coin before the first heads. Its advance $A$ of the start has $\Pr[A \ge a] = 2^{-a}$. The advance of Lemma 2 has $\Pr[A \ge a] = \frac{1}{2}(1 - 1/r')^{a-1} \ge 2^{-a}$ for $a \ge 1$, since $1 - 1/r' \ge 1/2$. So the fair-coin rule moves the start by a stochastically smaller amount, and its counts are stochastically no smaller than in the ideal state; the bound of Theorem 2 then also holds for it. But Lemma 2 fails for it from the second change on. For an item with 3 occurrences in the first phase, the fair-coin rule gives the start distribution $(1/4, 1/4, 3/16)$ and no entry with probability $5/16$ at rate 4, while the ideal state gives $(1/4, 3/16, 9/64)$ and $27/64$. Theorem 3 uses Theorem 1, so it does not cover the fair-coin rule.
