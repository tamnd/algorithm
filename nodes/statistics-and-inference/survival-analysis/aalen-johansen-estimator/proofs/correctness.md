---
title: The pass computes the cumulative incidences, which reduce to one minus Kaplan-Meier for one cause, add up with the survival to one, lie below one minus the cause-specific Kaplan-Meier, and equal the empirical proportions without censoring
proves: [correctness]
status: full
---

Let the data be $(y_i, c_i)$, $i = 1, \ldots, n$, with $c_i = 0$ for a censored subject and $c_i = k \in \{1, \ldots, K\}$ for an event of cause $k$ at $y_i$. Let $t_1 < \cdots < t_m$ be the distinct event times of any cause, $n_j = \#\{i : y_i \ge t_j\}$, $d_{kj}$ the number of events of cause $k$ at $t_j$ and $d_j = \sum_k d_{kj}$. The estimates are

$$\hat S(t) = \prod_{t_j \le t}\Bigl(1 - \frac{d_j}{n_j}\Bigr), \qquad \hat F_k(t) = \sum_{t_j \le t} \hat S(t_{j-1})\,\frac{d_{kj}}{n_j},$$

with $\hat S(t_0) = 1$. Here $\hat S(t_{j-1}) = \hat S(t_j-)$, the value just before $t_j$, because $\hat S$ only jumps at event times.

**Claim 1 (the pass computes the sums).** Every row that the pass appends is $(t_j, n_j, (d_{1j}, \ldots, d_{Kj}), \hat S(t_j), (\hat F_1(t_j), \ldots, \hat F_K(t_j)))$, one row for each $j$, in order.

*Proof.* After the sort of line L1, the inner loop of line L4 reads exactly the subjects at the current distinct time $u$ and counts the events of each cause. Invariant: at the start of the group at $u$, the variable `at_risk` is $\#\{i : y_i \ge u\}$, and $S$ and $F$ hold $\hat S$ and $\hat F_k$ just before $u$. It holds at the first group, with $n$ subjects at risk, $S = 1$ and $F = 0$. If $u = t_j$, line L6 adds $S\,d_{kj}/n_j$ to each $F_k$ while $S$ still holds $\hat S(t_j-)$, and line L7 then multiplies $S$ by $1 - d_j/n_j$. Line L8 removes all the subjects at $u$, events and censored alike, so `at_risk` becomes the count at the next distinct time. $\square$

The order of lines L6 and L7 matters: if $S$ were updated first, the increment would use $\hat S(t_j)$ and the sum of Claim 3 would fail.

**Claim 2 (one cause).** If $K = 1$, then $\hat F_1(t) = 1 - \hat S(t)$, where $\hat S$ is the [Kaplan-Meier estimator](/kaplan-meier-estimator/) of the event time.

*Proof.* With one cause, $d_{1j} = d_j$, and the increment of $\hat F_1$ at $t_j$ is $\hat S(t_{j-1})\,d_j/n_j = \hat S(t_{j-1}) - \hat S(t_{j-1})(1 - d_j/n_j) = \hat S(t_{j-1}) - \hat S(t_j)$. The sum telescopes to $\hat S(t_0) - \hat S(t) = 1 - \hat S(t)$. $\square$

**Claim 3 (the sum is one).** For every $t$, $\hat S(t) + \sum_{k=1}^K \hat F_k(t) = 1$.

*Proof.* Add the increments over $k$. The increment of $\sum_k \hat F_k$ at $t_j$ is $\hat S(t_{j-1})\,d_j/n_j = \hat S(t_{j-1}) - \hat S(t_j)$, as in Claim 2, so $\sum_k \hat F_k(t) = 1 - \hat S(t)$. $\square$

**Claim 4 (one minus the cause-specific Kaplan-Meier overstates).** Let $\hat S_k$ be the Kaplan-Meier estimator computed with the events of the other causes treated as censored. Then $1 - \hat S_k(t) \ge \hat F_k(t)$ for every $t$.

*Proof.* A subject with an event of another cause at $t_l$ is censored at $t_l$ in $\hat S_k$, and a censored subject is at risk at its own time and leaves after it. So the risk set of $\hat S_k$ at $t_j$ is the same set $\{i : y_i \ge t_j\}$, with $n_j$ members, and $\hat S_k(t) = \prod_{t_j \le t}(1 - d_{kj}/n_j)$. Each factor $1 - d_{kj}/n_j$ is at least $1 - d_j/n_j \ge 0$, so $\hat S_k(t) \ge \hat S(t)$ for every $t$. As in Claim 2, $1 - \hat S_k$ has the increment $\hat S_k(t_{j-1})\,d_{kj}/n_j$ at $t_j$, and $\hat F_k$ has the increment $\hat S(t_{j-1})\,d_{kj}/n_j$, which is not larger. Add the increments. $\square$

The inequality is strict at $t$ as soon as an event of another cause comes before an event of cause $k$ in $(0, t]$ while $\hat S$ is still positive. With the hand example of the page, $1 - \hat S_1(3) = 4/9$ and $\hat F_1(3) = 7/18$.

The same inequality holds in the population. With cause-specific hazards $h_k$, $H_k(t) = \int_0^t h_k$ and $H = \sum_k H_k$, we have $F_k(t) = \int_0^t e^{-H(u)} h_k(u)\,du$ and $1 - e^{-H_k(t)} = \int_0^t e^{-H_k(u)} h_k(u)\,du$, and $e^{-H(u)} \le e^{-H_k(u)}$.

**Claim 5 (no censoring).** If no subject is censored, then $\hat F_k(t) = \#\{i : y_i \le t,\ c_i = k\}/n$ and $\hat S(t) = \#\{i : y_i > t\}/n$.

*Proof.* Without censoring, every subject that leaves the risk set before $t_j$ has an event, so $n_j = n - \sum_{l < j} d_l$, and $\hat S(t_{j-1}) = \prod_{l < j}(n_l - d_l)/n_l = n_j/n$ because the product telescopes ($n_{l+1} = n_l - d_l$). The increment of $\hat F_k$ at $t_j$ is $(n_j/n)(d_{kj}/n_j) = d_{kj}/n$. Add the increments. $\square$

**Claim 6 (the product integral).** Let $P(t) = \prod_{t_j \le t}(I + d\hat A(t_j))$, with $d\hat A_{gh}(t_j) = N_{gh}(t_j)/Y_g(t_j)$ for $g \ne h$ and $d\hat A_{gg}(t_j) = -\sum_{h \ne g} d\hat A_{gh}(t_j)$, where $N_{gh}(t_j)$ counts the transitions from $g$ to $h$ at $t_j$ and $Y_g(t_j)$ counts the subjects in state $g$ just before $t_j$ that are under observation at $t_j$. Then:

1. every row of $P(t)$ sums to $1$ and every entry is in $[0, 1]$;
2. for the competing risks data (state $0$ alive, state $k$ dead of cause $k$), $P_{00}(t) = \hat S(t)$ and $P_{0k}(t) = \hat F_k(t)$;
3. if every subject starts in state $0$ and is followed until it reaches an absorbing state, $P_{0h}(t)$ is the proportion of subjects in state $h$ at time $t$.

*Proof.* (1) Each row of $d\hat A$ sums to $0$, so each row of $I + d\hat A$ sums to $1$. The off-diagonal entries are at least $0$, and the diagonal entry $1 - \sum_{h \ne g} N_{gh}/Y_g$ is at least $0$ because the subjects that leave $g$ at $t_j$ are among the $Y_g$ subjects in $g$ just before $t_j$. A product of matrices with entries at least $0$ and row sums $1$ has the same two properties, and then each entry is at most its row sum $1$.

(2) For competing risks, $Y_0(t_j) = n_j$ and $N_{0k}(t_j) = d_{kj}$, and the states $k \ge 1$ are absorbing, so their rows of $I + d\hat A$ are rows of $I$. Row $0$ of $I + d\hat A(t_j)$ is $(1 - d_j/n_j, d_{1j}/n_j, \ldots, d_{Kj}/n_j)$. Row $0$ of the product obeys $P_{00}(t_j) = P_{00}(t_{j-1})(1 - d_j/n_j)$ and $P_{0k}(t_j) = P_{0k}(t_{j-1}) + P_{00}(t_{j-1})\,d_{kj}/n_j$, which are lines L7 and L6.

(3) Let $p_h(t)$ be the proportion of subjects in state $h$ at $t$, and $Y'_h(t_j)$ the number of subjects in $h$ just before $t_j$, so that $p_h(t_j-) = Y'_h(t_j)/n$. Assume $P_{0h}(t_j-) = p_h(t_j-)$ for every $h$, which holds before the first transition. Row $0$ of $P(t_j) = P(t_j-)(I + d\hat A(t_j))$ is

$$P_{0h}(t_j) = p_h(t_j-) - p_h(t_j-) \sum_{h' \ne h} \frac{N_{hh'}}{Y_h} + \sum_{g \ne h} p_g(t_j-) \frac{N_{gh}}{Y_g}.$$

A state $g$ with transitions out of it is not absorbing, and without censoring every subject in a state that is not absorbing is still under observation, so $Y_g = Y'_g$ and $p_g(t_j-)/Y_g = 1/n$. So $P_{0h}(t_j) = (Y'_h - \sum_{h'} N_{hh'} + \sum_g N_{gh})/n$, which is the number of subjects in $h$ just after $t_j$ divided by $n$. Induction over the transition times completes the proof. $\square$

**What is not proved here.** Under independent censoring, $\hat F_k$ and $P$ are uniformly consistent, and $\sqrt n$ times the error converges to a Gaussian process (Aalen and Johansen 1978; Andersen, Borgan, Gill and Keiding 1993). We cite these results. The tests of the page check them only by simulation at a few time points.

**Cost.** One sort, $\Theta(n \log n)$, and one pass with $O(K)$ work at each of the $m$ event times, $O(n + mK)$ in total. The general product integral costs $O(n \log n)$ to sort the transitions and $O(s)$ for each pair $(g, h)$ that has a transition at $t_j$, because only the columns $g$ and $h$ of $P$ change.
