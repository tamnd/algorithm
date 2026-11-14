---
title: The pass computes the product-limit estimate, which is the nonparametric MLE and equals Efron's redistribute-to-the-right estimate
proves: [correctness]
status: full
---

Let the data be $(y_i, \delta_i)$ for $i = 1, \ldots, n$, with distinct event times $t_1 < \cdots < t_k$ (the distinct $y_i$ with $\delta_i = 1$), $n_j = \#\{i : y_i \ge t_j\}$ and $d_j = \#\{i : y_i = t_j, \delta_i = 1\}$. The product-limit estimate is $\hat S(t) = \prod_{j:\, t_j \le t}(1 - d_j/n_j)$.

**Claim 1 (the pass computes the product-limit estimate).** Every row $(t, r, d, S)$ that line L7 appends is $(t_j, n_j, d_j, \hat S(t_j))$ for some $j$, and each $j$ gives one row, in increasing order of $t_j$.

*Proof.* After line L1 the indices are in increasing order of $y$. The inner loop of line L6 reads exactly the indices whose time equals $t$, so the outer loop visits each distinct observed time $u_1 < u_2 < \cdots$ once, in order, and at time $u$ it sets $d$ and $c$ to the numbers of events and censorings at $u$.

Invariant: when the outer loop starts the group at time $u$, $r = \#\{i : y_i \ge u\}$ and $S = \hat S(u-) = \prod_{j:\, t_j < u}(1 - d_j/n_j)$. At the first group, $r = n$ and $S = 1$, and both sides are right because no $y_i$ is below the smallest time and the product is empty. Suppose the invariant holds at $u$. If $u = t_j$ is an event time, line L7 sets $S$ to $\hat S(u-)(1 - d_j/n_j) = \hat S(t_j)$; otherwise $S$ is unchanged and $\hat S(u) = \hat S(u-)$. Line L8 subtracts the $d + c$ subjects with $y_i = u$, so $r$ becomes $\#\{i : y_i > u\} = \#\{i : y_i \ge u'\}$ for the next distinct time $u'$, and $S = \hat S(u) = \hat S(u'-)$ because no event time lies in $(u, u')$. So the invariant holds at $u'$. At an event time the row appended has $r = n_j$, $d = d_j$ and $S = \hat S(t_j)$. $\square$

**Claim 2 (maximum likelihood).** Let $\mathcal F$ be the set of probability distributions on $(0, \infty]$, where mass at $\infty$ means that the event never happens. For $F \in \mathcal F$ write $p_F(u) = P_F(T = u)$ and $S_F(u) = P_F(T > u)$, and define

$$L(F) = \prod_{i:\, \delta_i = 1} p_F(y_i) \prod_{i:\, \delta_i = 0} S_F(y_i).$$

Assume at least one event. Then $L$ attains its maximum over $\mathcal F$, and $F$ is a maximizer if and only if $S_F(t) = \hat S(t)$ for all $t \le y_{(n)}$, the largest observed time.

This $L$ is the likelihood of the data as a function of $F$ when censoring is independent and noninformative: the full likelihood is $L(F)$ times a factor that depends only on the censoring distribution ([censoring](/censoring/) derives this factorization). So the claim says that the product-limit estimate is the nonparametric maximum likelihood estimate.

*Proof.* Put $t_0 = 0$ and $t_{k+1} = \infty$. Take $F$ with $L(F) > 0$; such an $F$ exists (put mass $1/(k+1)$ at each $t_j$ and at $\infty$). Then $p_F(t_j) > 0$ for every $j$.

*Step 1: the mass sits at the event times and beyond $y_{(n)}$.* Define $F^*$ by moving the mass of $F$ in each open interval $(t_{j-1}, t_j)$, for $j = 1, \ldots, k$, to the point $t_j$, and the mass in $(t_k, y_{(n)}]$ to $\infty$. Masses at the $t_j$ only grow, so $p_{F^*}(y_i) \ge p_F(y_i)$ for every event. For a censored $y_i$, every moved point goes to the right, so mass that was above $y_i$ stays above $y_i$, and $S_{F^*}(y_i) \ge S_F(y_i)$. Hence $L(F^*) \ge L(F)$. The inequality is strict if $F$ has mass in some $(t_{j-1}, t_j)$ with $j \le k$, because then $p_{F^*}(t_j) > p_F(t_j)$ and $d_j \ge 1$; it is also strict if $F$ has mass in $(t_k, y_{(n)}]$, because the subject with $y_i = y_{(n)}$ is then censored (an event at $y_{(n)}$ would make $y_{(n)} = t_k$) and $S_{F^*}(y_{(n)}) > S_F(y_{(n)})$.

*Step 2: maximize over distributions on $\{t_1, \ldots, t_k, \infty\}$.* Write such a distribution through its discrete hazards $h_j = P(T = t_j \mid T \ge t_j) \in [0, 1]$, which give $p(t_j) = h_j \prod_{l < j}(1 - h_l)$ and $P(T > t) = \prod_{l:\, t_l \le t}(1 - h_l)$. Every vector $h \in [0, 1]^k$ comes from exactly one such distribution, with the remaining mass $\prod_{l \le k}(1 - h_l)$ at $\infty$, and every such distribution has a vector $h$ (if $P(T \ge t_j) = 0$, set $h_j = 1$; then $L = 0$ anyway). Substitute: the event of subject $i$ at $t_j$ contributes $h_j \prod_{l < j}(1 - h_l)$, and a censored subject with $t_j \le y_i < t_{j+1}$ contributes $\prod_{l \le j}(1 - h_l)$. Collect the factors. $h_j$ appears once for each event at $t_j$, so $d_j$ times. $(1 - h_l)$ appears once for each event at a time $t_j > t_l$ and once for each censored subject with $y_i \ge t_l$, that is, once for each subject with $y_i \ge t_l$ except the $d_l$ events at $t_l$. That count is $n_l - d_l$. So

$$L = \prod_{j=1}^{k} h_j^{d_j}(1 - h_j)^{n_j - d_j}.$$

The factors depend on separate variables. For $d \ge 1$ and $n \ge d$, the function $h \mapsto h^d (1 - h)^{n - d}$ on $[0, 1]$ has the unique maximizer $h = d/n$: its logarithm $d \log h + (n - d)\log(1 - h)$ is strictly concave on $(0, 1)$ with derivative $d/h - (n - d)/(1 - h)$, which vanishes only at $h = d/n$ (if $n = d$, the function $h^d$ is increasing and the maximizer is $h = 1 = d/n$). So the unique maximizer has $h_j = d_j / n_j$, and its survival function is $\prod_{t_j \le t}(1 - d_j/n_j) = \hat S(t)$.

Combining the steps: every $F$ has $L(F) \le L(F^*) \le L(\hat F)$, where $\hat F$ is the distribution of Step 2. Equality throughout forces $F$ to have no mass in any $(t_{j-1}, t_j)$ or in $(t_k, y_{(n)}]$ (Step 1) and to have the hazards $d_j/n_j$ at the $t_j$ (Step 2), which together fix $S_F$ on $[0, y_{(n)}]$ to be $\hat S$. Beyond $y_{(n)}$, when the largest observation is censored, $L$ does not depend on where the mass $\hat S(y_{(n)})$ lies, so $S$ is not identified there. $\square$

**Claim 3 (redistribute to the right).** Order the subjects by time, with events before censorings at equal times, as positions $1, \ldots, n$. Give each subject mass $1/n$. Go through the positions in order; at a censored subject at position $p < n$, split its current mass equally among the subjects at positions $p + 1, \ldots, n$ and set its own mass to $0$. Let $\tilde S(t) = 1 - (\text{total final mass of events with } y_i \le t)$. Then $\tilde S(t_j) = \hat S(t_j)$ for every $j$.

*Proof.* Event subjects never pass mass on, and redistribution keeps the total mass equal to $1$. Call the subjects at positions $p, \ldots, n$ the tail at $p$.

Invariant: when the pass reaches position $p$, all subjects in the tail at $p$ hold the same mass $m$, and the tail holds total mass $1 - (\text{mass of events at positions} < p)$. At $p = 1$ this holds with $m = 1/n$. If position $p$ is an event, nothing moves, and the tail at $p + 1$ still has equal masses and total $1 - (\text{event mass at positions} < p + 1)$. If position $p$ is censored and $p < n$, it gives $m/(n - p)$ to each of the $n - p$ later subjects, which all held $m$; they now hold $m(n - p + 1)/(n - p)$ each, equal again, and their total is $(n - p + 1)m$, the old total of the tail at $p$. Censored subjects keep no mass, so the second part also holds.

Now take an event time $t_j$ and let $p$ be the first position with $y = t_j$. By the ordering, the tail at $p$ is exactly the $n_j$ subjects with $y_i \ge t_j$, and its first $d_j$ positions are the events at $t_j$. By the invariant the $n_j$ subjects hold equal mass $m_j$ and total $n_j m_j = 1 - (\text{event mass at times} < t_j) = \tilde S(t_j -)$. The $d_j$ events at $t_j$ come next, so nothing changes their mass before they are passed, and they keep $m_j$ each to the end. So

$$\tilde S(t_j) = \tilde S(t_j -) - d_j m_j = \tilde S(t_j -)\left(1 - \frac{d_j}{n_j}\right).$$

Since $\tilde S$ is constant between event times and $\tilde S(t_1 -) = 1$, induction on $j$ gives $\tilde S(t_j) = \prod_{l \le j}(1 - d_l/n_l) = \hat S(t_j)$. $\square$

**Cost.** Line L1 sorts $n$ keys in $\Theta(n \log n)$ comparisons. Each iteration of the inner loop of line L6 advances $i$, so lines L4 to L8 run $n$ inner steps and at most $n$ outer steps, each with $O(1)$ arithmetic. The total is $\Theta(n \log n)$ in the worst case.
