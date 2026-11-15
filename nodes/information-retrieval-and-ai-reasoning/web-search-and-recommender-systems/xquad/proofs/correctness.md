---
title: The incremental xQuAD loop picks the document of Equation 5 at every step, and is greedy on a monotone submodular objective
proves: [correctness]
status: full
---

Let $R$ be a finite set of candidate ids with a total order, $\mathrm{rel}(d) = P(d \mid q)$ for $d \in R$, a finite set $Q$ of aspects with weights $w_i = P(q_i \mid q) \ge 0$, coverages $c_i(d) = P(d \mid q_i) \in [0, 1]$, taken as $0$ when not given, and $\lambda \in [0, 1]$. For a chosen set $S$ and $d \in R \setminus S$, Equation 5 of Santos, Macdonald and Ounis is

$$x_S(d) = (1 - \lambda)\, \mathrm{rel}(d) + \lambda \sum_{i \in Q} w_i\, c_i(d) \prod_{j \in S} \big(1 - c_i(j)\big).$$

The xQuAD list with the tie rule of this page is $s_1, \ldots, s_m$ with $m = \min(k, |R|)$, where $s_t$ is the smallest id among the maximizers of $x_{S_{t-1}}$ over $R \setminus S_{t-1}$, and $S_t = \{s_1, \ldots, s_t\}$.

**Lemma 1 (invariant).** At the start of each pass of the loop of line L3, with $S$ the set of ids chosen so far, $\mathrm{novel}[i] = \prod_{j \in S} (1 - c_i(j))$ for every aspect $i$.

*Proof.* Line L1 sets every value to $1$, the empty product. When $b$ is chosen, lines L7 and L8 multiply $\mathrm{novel}[i]$ by $1 - c_i(b)$ for each aspect that $b$ covers; for the other aspects $c_i(b) = 0$ and the factor is $1$. $\square$

**Theorem 2 (output).** The procedure returns $s_1, \ldots, s_m$, each with its score $x_{S_{t-1}}(s_t)$.

*Proof.* By Lemma 1, line L5 computes $x_S(d)$, where the sum skips the aspects with $c_i(d) = 0$, whose terms are $0$. The ids are scanned in increasing order and the best is replaced only on a strictly larger score, so line L6 records the smallest id among the maximizers, which is $s_t$. The loop runs while ids remain and fewer than $k$ are chosen, so it makes $m$ passes. $\square$

**Corollary 3 (lambda = 0).** For $\lambda = 0$ the output is the first $m$ ids in the order rel descending, then id ascending, the first ranking.

*Proof.* The score is $\mathrm{rel}(d)$ and does not depend on $S$. $\square$

**Theorem 4 (the set objective).** Define, for $S \subseteq R$,

$$F(S) = (1 - \lambda) \sum_{d \in S} \mathrm{rel}(d) + \lambda \sum_{i \in Q} w_i \Big(1 - \prod_{j \in S} \big(1 - c_i(j)\big)\Big).$$

Then $x_S(d) = F(S \cup \{d\}) - F(S)$ for $d \notin S$, so xQuAD is the greedy algorithm on $F$. If $\mathrm{rel}(d) \ge 0$ for every $d$, $F$ is monotone and submodular with $F(\emptyset) = 0$, and the list $S_m$ satisfies $F(S_m) \ge (1 - 1/e) \max_{|S| = m} F(S)$.

*Proof.* The first sum grows by $(1 - \lambda)\mathrm{rel}(d)$. In the second, the product of aspect $i$ gains the factor $1 - c_i(d)$, so its term grows by $w_i c_i(d) \prod_{j \in S}(1 - c_i(j))$. Together this is $x_S(d)$. The first sum is modular, so its marginal gain does not depend on $S$, and it is non-negative when rel is. The second is the objective of IA-Select with $P(c \mid q) = w_i$ and $V(d \mid q, c) = c_i(d)$, whose marginal gain is a product of numbers in $[0, 1]$ and can only shrink when $S$ grows. A non-negative combination of monotone submodular functions with value $0$ on the empty set has the same properties, and $F(\emptyset) = 0$ because the empty product is $1$. The theorem of Nemhauser, Wolsey and Fisher gives the bound for the greedy algorithm, since by Theorem 2 each pick maximizes the marginal gain. $\square$

Santos et al. do not state Theorem 4; they present Algorithm 1 as an instance of the greedy approximation and note that the general problem is NP-hard by a reduction from maximum coverage. The bound concerns $F$ under the model, and says nothing about measured effectiveness.

**Corollary 5 (lambda = 1).** For $\lambda = 1$, xQuAD and IA-Select with $P(c \mid q) = w_i$ and $V(d \mid q, c) = c_i(d)$ pick the same list under the same tie rule.

*Proof.* Both scores are the marginal gain of the same function, the second term of $F$. $\square$

**Cost.** Let $n = |R|$, $m_Q = |Q|$, and $e$ the number of pairs with $c_i(d) > 0$. Each of the at most $k$ passes computes $n$ scores in $O(n + e)$ total time and updates at most $m_Q$ values, so the procedure runs in $O(n \log n + k(n + e)) = O(n \log n + nk m_Q)$ time with $O(n + m_Q)$ extra space. The direct form, which recomputes each product over $S$, takes $O(nk^2 m_Q)$ time.

The test file checks Theorem 2 step by step against the direct form on random instances, half of them on a grid of values so that ties are frequent, and checks for $\lambda = 1$ that each score is the largest marginal gain of the coverage term.
