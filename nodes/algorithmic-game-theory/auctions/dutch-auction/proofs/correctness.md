---
title: The Dutch clock auction is the first-price auction on bids rounded down to the clock levels
proves: [correctness]
status: full
---

We use the pseudocode of the page, with stop prices $s_1, \ldots, s_n$, a start price $T$, a decrement $\delta > 0$ and a reserve $r \le T$. The clock levels are $g_k = T - k\delta$ for $k = 0, 1, \ldots$, as long as $g_k \ge r$. For a number $s$, let $\rho(s) = T$ if $s \ge T$, and otherwise let $\rho(s)$ be the largest level $g_k$ with $g_k \le s$ (this can be below $r$).

**Claim 1 (the outcome).** Let $p^* = \max_i \rho(s_i)$. If $p^* \ge r$, DUTCH returns the smallest index $i$ with $\rho(s_i) = p^*$, at price $p^*$. Otherwise it returns no winner. So DUTCH gives the outcome of the first-price auction with reserve $r$ on the bids $\rho(s_1), \ldots, \rho(s_n)$.

*Proof.* For a level $g_k$ and any $s$, $s \ge g_k$ if and only if $\rho(s) \ge g_k$: if $s \ge T$, both sides hold, and otherwise $\rho(s)$ is the largest level at most $s$, so a level is at most $s$ exactly when it is at most $\rho(s)$. Line L1 starts at $g_0$, and line L5 visits $g_1, g_2, \ldots$ in order while line L2 keeps the level at least $r$. At level $g_k$, line L3 computes $S_k = \{i : s_i \ge g_k\} = \{i : \rho(s_i) \ge g_k\}$. The sets grow as $k$ grows, and $S_k$ is empty exactly when $g_k > p^*$. If $p^* \ge r$, then $p^*$ is a level, the loop reaches it, all earlier sets are empty, and $S$ at $p^*$ is $\{i : \rho(s_i) = p^*\}$ because no $\rho(s_i)$ is larger. Line L4 returns its smallest index at price $p^*$. If $p^* < r$, every visited set is empty and line L6 returns no winner. The first-price rule with reserve $r$ on the bids $\rho(s_i)$ picks the smallest index with the largest bid $p^*$ if $p^* \ge r$, at price $p^*$, which is the same. $\square$

In particular, if every stop price is a clock level at most $T$, the Dutch auction and the first-price auction have the same outcome, and in general the Dutch price is at most the highest stop price and more than the highest stop price minus $\delta$ (when that stop price is at most $T$ and the price is at least $r$).

**Claim 2 (strategic equivalence).** Every strategy of a bidder in the Dutch auction gives the same outcome as a stop price. So the Dutch auction and the first-price auction on the clock levels have the same strategies and the same payoffs, and they have the same Bayes-Nash equilibria.

*Proof.* While the clock runs, a bidder sees only the current level and the fact that no one has accepted yet. When the clock stops, the auction is over. So a bidder's plan can depend only on the level: it is a rule "accept at level $g_k$ if no one has accepted before". Such a rule is fixed by the first level at which it accepts, which is a stop price. Its outcome against any stop prices of the others is the first-price outcome of Claim 1. $\square$

**Cost.** The loop visits the levels from $T$ down to $\max(p^*, r)$, that is $k \le (T - \max(p^*, r))/\delta + 1$ levels, and each visit scans the $n$ stop prices. The time is $O(nk)$ and the extra space is $O(n)$ for the set $S$.
