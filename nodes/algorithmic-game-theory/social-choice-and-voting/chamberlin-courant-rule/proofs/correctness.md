---
title: The dynamic program is exact on single-peaked profiles, and greedy reaches 1 - (1 - 1/k)^k of the optimal satisfaction
proves: [correctness]
status: full
---

A profile $P = (\succ_1, \ldots, \succ_n)$ ranks the candidates $0, \ldots, m - 1$. For a voter $i$ and a candidate $c$, $r_i(c)$ is the position of $c$ in $\succ_i$, with $0$ for the top. The misrepresentation of a committee $W$ is $\rho(W) = \sum_i \min_{c \in W} r_i(c)$, and its satisfaction is $f(W) = \sum_i \max_{c \in W} (m - 1 - r_i(c))$, with $f(\emptyset) = 0$. For $|W| \ge 1$, $f(W) = n(m - 1) - \rho(W)$, so the committees of size $k$ with the least $\rho$ are those with the largest $f$.

## The exact search

`chamberlin_courant` computes $\rho(W)$ for every $W$ of size $k$, in the lexicographic order of sorted tuples, and keeps a new committee only when its value is strictly smaller. So it returns the lexicographically first committee with the least misrepresentation.

## The dynamic program on single-peaked profiles

Let the profile be single-peaked on the axis $a_0 \lhd a_1 \lhd \cdots \lhd a_{m-1}$. We work with places on the axis: $c(t) = a_t$, $q_i$ is the place of the peak of voter $i$, and $\kappa_i(t) = r_i(a_t)$.

**Lemma 1.** If $s < t \le q_i$, then $\kappa_i(t) < \kappa_i(s)$. If $q_i \le t < s$, then $\kappa_i(t) < \kappa_i(s)$.

*Proof.* If $t = q_i$, $a_t$ is the top of voter $i$. Otherwise $a_s, a_t, a_{q_i}$ lie in this order on the axis (or in the reverse order), and a single-peaked ranking has no valley at $a_t$, so $a_t \succ_i a_s$ because $a_{q_i} \succ_i a_t$ already. $\square$

**Lemma 2.** Let the committee have the places $t_1 < t_2 < \cdots < t_k$. Voter $i$ is best represented by $a_{t_1}$ if $q_i < t_1$, by $a_{t_k}$ if $q_i \ge t_k$, and otherwise by the better of $a_{t_j}$ and $a_{t_{j+1}}$, where $t_j \le q_i < t_{j+1}$.

*Proof.* By Lemma 1, among the members at places at most $q_i$ the one with the largest place is best, and among those at places above $q_i$ the one with the smallest place is best. If $q_i < t_1$ there are no members on the left, and if $q_i \ge t_k$ none on the right. $\square$

For places $s < t$, line L1 and line L2 compute

$$\mathrm{head}(t) = \sum_{i : q_i < t} \kappa_i(t), \qquad \mathrm{tail}(t) = \sum_{i : q_i \ge t} \kappa_i(t), \qquad \mathrm{seg}(s, t) = \sum_{i : s \le q_i < t} \min(\kappa_i(s), \kappa_i(t)).$$

The intervals $q < t_1$, $t_1 \le q < t_2$, ..., $t_{k-1} \le q < t_k$ and $q \ge t_k$ split the voters, so Lemma 2 gives

$$\rho(\{a_{t_1}, \ldots, a_{t_k}\}) = \mathrm{head}(t_1) + \sum_{j=1}^{k-1} \mathrm{seg}(t_j, t_{j+1}) + \mathrm{tail}(t_k). \tag{1}$$

**Claim.** After lines L3 to L6, $F[j][t]$ is the least value of $\mathrm{head}(t_1) + \sum_{l=1}^{j-1} \mathrm{seg}(t_l, t_{l+1})$ over all places $t_1 < \cdots < t_j = t$, for $1 \le j \le k$ and $j - 1 \le t \le m - 1$.

*Proof.* By induction on $j$. For $j = 1$ the only choice is $t_1 = t$, and line L3 sets $F[1][t] = \mathrm{head}(t)$. For $j \ge 2$, a choice $t_1 < \cdots < t_{j-1} < t_j = t$ has $t_{j-1} = s$ with $j - 2 \le s < t$, and its value is the value of the first $j - 1$ places plus $\mathrm{seg}(s, t)$. For a fixed $s$, the least value of the first part is $F[j-1][s]$ by induction, and line L6 takes the minimum over all $s$. $\square$

By (1) and the claim, the value of line L7, $\min_t F[k][t] + \mathrm{tail}(t)$, is the least misrepresentation of a committee of size $k$. Line L6 records the $s$ that gives each minimum, so line L8 follows these records back from the best $t$ and reads $k$ places $t_k > t_{k-1} > \cdots > t_1$ whose value in (1) is this minimum. The test `test_dp_matches_exact_search_on_random_single_peaked_profiles` checks the value against the exact search for every $k$ on random single-peaked profiles.

**Running time.** Lines L1 take $O(mn)$ time. Line L2 adds, for each voter, one term to $\mathrm{seg}(s, t)$ for each $s \le q_i < t$, at most $m^2/4$ terms, so $O(m^2 n)$ time in all. Lines L4 to L6 take $O(k m^2)$ time. The total is $O(m^2 (n + k))$ time and $O(m^2 + mn)$ space.

## The greedy algorithm

The function $f$ is monotone: adding a candidate never lowers any voter's best score. It is submodular: for $X \subseteq Y$ and a candidate $c$, the gain $f(X \cup \{c\}) - f(X) = \sum_i \max(0, s_i(c) - \max_{X} s_i)$, with $s_i(c) = m - 1 - r_i(c)$ and the maximum over the empty set equal to $0$, is at least the gain for $Y$, because each term is nonincreasing in the best score so far.

Let $O$ be an optimal committee of size $k$, $\mathrm{OPT} = f(O)$, and $W_j$ the greedy committee after $j$ steps. Each step picks a candidate of largest gain; candidates already in $W_j$ have gain $0$, so the step has a gain at least as large as every candidate of $O$. By monotonicity and submodularity,

$$\mathrm{OPT} \le f(W_j \cup O) \le f(W_j) + \sum_{o \in O} \bigl(f(W_j \cup \{o\}) - f(W_j)\bigr) \le f(W_j) + k \bigl(f(W_{j+1}) - f(W_j)\bigr).$$

So $\mathrm{OPT} - f(W_{j+1}) \le (1 - 1/k)(\mathrm{OPT} - f(W_j))$, and after $k$ steps $\mathrm{OPT} - f(W_k) \le (1 - 1/k)^k \, \mathrm{OPT}$, since $f(W_0) = 0$. This gives $f(W_k) \ge (1 - (1 - 1/k)^k)\,\mathrm{OPT} > (1 - 1/e)\,\mathrm{OPT}$. This is the bound of Nemhauser, Wolsey and Fisher (1978) for monotone submodular functions. The test `test_greedy_guarantee` checks it exactly in `Fraction` against the exact search.

The bound is for satisfaction. It says nothing about the ratio of misrepresentations: in the example on the page the greedy committee has misrepresentation $4$ and the optimum $3$.
