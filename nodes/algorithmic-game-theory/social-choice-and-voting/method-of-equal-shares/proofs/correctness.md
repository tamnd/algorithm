---
title: The price rho is computed exactly, budgets are never overspent, and the committee satisfies extended justified representation
proves: [correctness]
status: full
---

An approval profile has ballots $A_1, \ldots, A_n \subseteq \{0, \ldots, m - 1\}$ with $n \ge 1$, and $N(c) = \{i : c \in A_i\}$. Each candidate $c$ has a cost $\mathrm{cost}(c) > 0$, and the total budget is $B$. For committees, every cost is $1$ and $B = k$. Each voter starts with $x_i = B / n$.

In a round, a candidate $c$ that is not yet bought is affordable if $\sum_{i \in N(c)} x_i \ge \mathrm{cost}(c)$. Its price is the least $\rho$ with

$$f_c(\rho) = \sum_{i \in N(c)} \min(\rho, x_i) = \mathrm{cost}(c).$$

The round buys the affordable candidate with the least price, ties to the smallest index, and each supporter $i$ pays $\min(\rho, x_i)$. Phase 1 ends when no candidate is affordable. For committees, phase 2 runs sequential Phragmen from the loads $y_i = -x_i$ until there are $k$ members.

## Computing the price

The function $f_c$ is continuous and nondecreasing, with $f_c(0) = 0$ and $f_c(\rho) = \sum_{i \in N(c)} x_i$ for $\rho \ge \max_i x_i$. So a price exists exactly when $c$ is affordable.

`rho` sorts the budgets $b_0 \le b_1 \le \cdots \le b_{s-1}$ and keeps $R_j = \mathrm{cost}(c) - \sum_{j' < j} b_{j'}$. At step $j$ it tests $b_j (s - j) \ge R_j$.

- If the test fails at every step, the failed test at step $s - 1$ gives $b_{s-1} < R_{s-1}$, so $\sum b < \mathrm{cost}(c)$, and `rho` returns None. Conversely, if $\sum b \ge \mathrm{cost}(c)$, the test at step $s - 1$ holds if no earlier test holds.
- If the test first holds at step $j$, let $r = R_j / (s - j)$. Then $r \le b_j \le b_{j+1} \le \cdots$. If $j > 0$, the failed test at step $j - 1$ says $b_{j-1}(s - j + 1) < R_{j-1} = R_j + b_{j-1}$, so $b_{j-1} (s - j) < R_j$ and $b_{j-1} < r$. Hence the voters $0, \ldots, j - 1$ pay their whole budgets, the others pay $r$, and $f_c(r) = \sum_{j' < j} b_{j'} + (s - j) r = \mathrm{cost}(c)$. For $\rho < r$, the $s - j \ge 1$ voters with $b \ge r$ pay $\rho < r$, so $f_c(\rho) < f_c(r)$. So $r$ is the least price.

## Budgets

Each payment $\min(\rho, x_i)$ is at most $x_i$, so no budget becomes negative, and the payments for $c$ add up to $f_c(\rho) = \mathrm{cost}(c)$. So after phase 1, the total cost of the bought candidates plus the leftover budgets equals $B$. For committees, phase 1 buys at most $k$ candidates, because each costs $1$ and the budgets add up to $k$.

Budgets only decrease, so each $f_c$ only decreases, and the price of each candidate only increases. Hence the prices of the bought candidates do not decrease from round to round.

## Extended justified representation

A committee $W$ satisfies extended justified representation (EJR) if for every $\ell$ with $1 \le \ell \le k$ and every nonempty group $S$ of voters with $|S| \ge \ell n / k$ and $|\bigcap_{i \in S} A_i| \ge \ell$, some voter $i \in S$ has $|A_i \cap W| \ge \ell$.

**Theorem.** For committees (all costs $1$, $B = k$), the set $W_1$ bought in phase 1 satisfies EJR. So does every committee that contains $W_1$, in particular the completed committee.

*Proof.* Suppose $\ell$ and $S$ violate EJR for $W_1$: every voter of $S$ approves at most $\ell - 1$ members of $W_1$. Let $s = |S|$. The common set $T = \bigcap_{i \in S} A_i$ has at least $\ell$ candidates, and a voter of $S$ approves at most $\ell - 1$ members of $W_1$, so some $c \in T$ is not in $W_1$. This $c$ is never bought, so it is a candidate in every round.

Consider the rounds of phase 1 in order, and let round $r$ be the first round that either buys a candidate with price greater than $1/s$ or finds no affordable candidate. Such a round exists, because phase 1 ends with a round that finds no affordable candidate. Before round $r$, every price was at most $1/s$, so every payment was at most $1/s$. A voter of $S$ pays only for members of $W_1$ that it approves, at most $\ell - 1$ of them. So at the start of round $r$, every voter of $S$ has at least

$$\frac{k}{n} - \frac{\ell - 1}{s} \ge \frac{\ell}{s} - \frac{\ell - 1}{s} = \frac{1}{s},$$

using $s \ge \ell n / k$. Then $f_c(1/s) \ge \sum_{i \in S} \min(1/s, x_i) = s \cdot 1/s = 1$, so $c$ is affordable in round $r$ with price at most $1/s$. So round $r$ finds an affordable candidate and buys one with price at most $1/s$, which contradicts the choice of $r$.

If $W \supseteq W_1$, every voter has at least as many approved members in $W$ as in $W_1$, so $W$ satisfies EJR as well. $\square$

EJR implies proportional justified representation and justified representation. The completion by sequential Phragmen is not needed for EJR; it only fills the committee to $k$ members. The tests also check that the rule gives the D'Hondt seat counts on party lists, as Peters and Skowron proved.

## Running time

A round computes the price of at most $m$ candidates; for $c$ this sorts $|N(c)|$ budgets. So a round takes $O(\sum_c |N(c)| \log n) = O(mn \log n)$ arithmetic operations. For committees phase 1 has at most $k + 1$ rounds and the completion takes $O(kmn)$, so the total is $O(kmn \log n)$. With general costs phase 1 has at most $m + 1$ rounds, $O(m^2 n \log n)$ in total.
