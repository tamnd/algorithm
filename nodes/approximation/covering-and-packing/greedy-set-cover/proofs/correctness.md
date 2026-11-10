---
title: Greedy set cover returns a cover of cost at most H_d times the optimum
proves: [correctness]
status: full
---

We use the notation of the page. The universe $U$ has $n$ elements, the sets are $S_1, \ldots, S_m$ with costs $c_j \ge 0$, and $d = \max_j |S_j|$. The family covers $U$. For a set $S$ of the family we write $c(S)$ for its cost.

**Lemma 1 (a cover, in at most $n$ rounds).** GREEDY-SET-COVER stops after at most $\min(n, m)$ rounds, and the sets in $C$ cover $U$.

*Proof.* At the start of a round, $R \ne \emptyset$. Each element of $R$ is in some set of the family, so line L3 finds a set $S_j$ with $S_j \cap R \neq \emptyset$. Line L5 removes $S_j \cap R$ from $R$, so $|R|$ drops by at least 1 in each round. So there are at most $n$ rounds. After line L5, $S_j \cap R = \emptyset$ for the new $R$, so line L3 never picks $j$ again; this gives at most $m$ rounds. The loop stops only when $R = \emptyset$. An element leaves $R$ only in line L5, when it is in the chosen set $S_j$. So each element of $U$ is in a set of $C$. $\square$

**Lemma 2 (the cost is the sum of the prices).** At the end, each element $e \in U$ has exactly one price, and $\sum_{j \in C} c_j = \sum_{e \in U} \text{price}(e)$.

*Proof.* Line L4 sets the price of $e$ in the round in which $e$ leaves $R$, and $e$ leaves $R$ exactly once. In the round that picks $j$, line L4 gives each of the $|S_j \cap R|$ new elements the price $c_j / |S_j \cap R|$, so the prices of this round add up to $c_j$. Sum over the rounds. $\square$

**Lemma 3 (the price bound of one set).** Let $S$ be any set of the family, with $s = |S| \ge 1$ elements. Then

$$\sum_{e \in S} \text{price}(e) \le c(S) \, H_s.$$

*Proof.* List the elements of $S$ in the order in which they leave $R$, as $e_1, e_2, \ldots, e_s$. Elements that leave $R$ in the same round are listed in any order. Fix $i$, and look at the round in which $e_i$ leaves $R$. At the start of this round, the elements $e_i, e_{i+1}, \ldots, e_s$ are all still in $R$, because none of them left $R$ in an earlier round. So $|S \cap R| \ge s - i + 1 \ge 1$, and $S$ was a candidate in line L3, with ratio $c(S) / |S \cap R| \le c(S)/(s - i + 1)$. Line L3 picks a set $S_j$ with the least ratio, so

$$\text{price}(e_i) = \frac{c_j}{|S_j \cap R|} \le \frac{c(S)}{|S \cap R|} \le \frac{c(S)}{s - i + 1}.$$

Sum over $i = 1, \ldots, s$: the right sides add up to $c(S)(1/s + 1/(s-1) + \cdots + 1/1) = c(S) H_s$. $\square$

**Theorem (Johnson 1974, Lovász 1975, Chvátal 1979).** GREEDY-SET-COVER returns a cover $C$ with

$$\sum_{j \in C} c_j \le H_d \cdot \text{LP}^* \le H_d \cdot \text{OPT},$$

where LP* is the optimum of the LP relaxation.

*Proof by dual fitting.* Define $y_e = \text{price}(e)/H_d$ for each $e \in U$. Then $y_e \ge 0$. For each set $S$ with $s = |S| \le d$, Lemma 3 gives $\sum_{e \in S} y_e \le c(S) H_s / H_d \le c(S)$, because $H_s \le H_d$. So $y$ is feasible for the dual LP

$$\max \sum_{e \in U} y_e \quad \text{subject to} \quad \sum_{e \in S_j} y_e \le c_j \text{ for each } j, \quad y \ge 0.$$

By weak duality, $\sum_e y_e \le \text{LP}^*$. By Lemma 2, the cost of $C$ is $\sum_e \text{price}(e) = H_d \sum_e y_e \le H_d \cdot \text{LP}^*$. Finally $\text{LP}^* \le \text{OPT}$, because an optimal cover gives a feasible 0-1 point of the LP. $\square$

*Proof by charging, without LP.* Let $O$ be an optimal cover. Each element of $U$ is in at least one set of $O$, and prices are non-negative, so by Lemma 2 and Lemma 3

$$\sum_{j \in C} c_j = \sum_{e \in U} \text{price}(e) \le \sum_{S \in O} \sum_{e \in S} \text{price}(e) \le \sum_{S \in O} c(S) H_{|S|} \le H_d \cdot \text{OPT}. \qquad \blacksquare$$

**Corollary (unit costs, a bound in $n$ and OPT).** With $c_j = 1$ for each $j$ and $k = \text{OPT}$, greedy uses at most $k \lceil \ln(n/k) \rceil + k$ sets when $n \ge k$.

*Proof.* Let $r_t$ be $|R|$ after $t$ rounds, so $r_0 = n$. The $k$ sets of an optimal cover cover the $r_t$ elements of $R$, so one of them holds at least $r_t / k$ of them. Greedy picks a set with at least as many new elements, so $r_{t+1} \le r_t (1 - 1/k)$. Then $r_t \le n (1 - 1/k)^t \le n e^{-t/k}$, because $1 - x \le e^{-x}$ for each real $x$. With $t = k \lceil \ln(n/k) \rceil$, $r_t \le n e^{-\ln(n/k)} = k$. Each later round removes at least one element, so at most $k$ more rounds follow. $\square$
