---
title: With gross substitutes valuations the process never gets stuck, stops, and ends at an approximate Walrasian equilibrium
proves: [correctness, termination]
status: full
---

Fix $n$ bidders, $m$ items and a step $\delta > 0$. Bidder $i$ has a valuation $v_i$ on bundles with $v_i(\varnothing) = 0$ and $v_i \ge 0$. Let $V$ be the largest value $v_i(S)$. For a price vector $q$, the demand set is $D_i(q) = \arg\max_S \, v_i(S) - q(S)$, where $q(S) = \sum_{j \in S} q_j$.

The valuation $v_i$ has *gross substitutes* when for all price vectors $q \le q'$ and every $S \in D_i(q)$ there is $T \in D_i(q')$ with $\{j \in S : q_j = q'_j\} \subseteq T$: raising some prices never makes a bidder drop an item whose price did not change.

During the process, $p$ is the price vector, $X_i$ is the set of items whose owner is $i$, and the *personalized prices* of bidder $i$ are $q^i_j = p_j$ for $j \in X_i$ and $q^i_j = p_j + \delta$ otherwise. A *bid* is a turn of lines L5 to L8 in which $S \ne X_i$.

**Claim 1 (basic invariants).** Prices never go down. An item has an owner if and only if its price is positive. The sets $X_i$ are disjoint. *Proof.* Line L8 is the only line that changes $p$ or an owner. It raises $p_j$ by $\delta$ and sets the owner of $j$ to $i$ at the same time. Each item has one owner entry. $\square$

**Claim 2 (right after a turn).** At the end of a turn of bidder $i$, $X_i \in D_i(q^i)$. *Proof.* Let $q$ be the vector of line L6 and $S$ the bundle of line L7, so $S \in D_i(q)$ and $X_i \subseteq S$. After line L8 the new holding is $S$. For $j \in S \setminus X_i$, the new price is $p_j + \delta = q_j$, and as $j$ is now held, the new personalized price is $q_j$. For $j \in X_i$ and for $j \notin S$, neither the price nor the holding changed, so the personalized price is still $q_j$. So the personalized prices after the turn are $q$, and the holding is $S \in D_i(q)$. $\square$

**Claim 3 (line L7 never fails under gross substitutes).** If $v_i$ has gross substitutes, then at every turn of $i$ some $T \in D_i(q^i)$ has $X_i \subseteq T$. *Proof.* At the first turn of $i$, $X_i = \varnothing$, and $D_i(q^i)$ is not empty. Otherwise, let $q$ and $S$ be the personalized prices and the holding at the end of the previous turn of $i$; by Claim 2, $S \in D_i(q)$. Between the two turns only other bidders bid. When another bidder takes item $j$, the price $p_j$ rises by $\delta$; if $j \in S$, the item also leaves the holding of $i$. So for $j$ still held by $i$ the personalized price did not change, and every other personalized price went up or stayed. Hence the current personalized prices $q' \ge q$, and the current holding $X_i \subseteq \{j \in S : q_j = q'_j\}$. Gross substitutes gives $T \in D_i(q')$ with $X_i \subseteq T$. $\square$

**Claim 4 (termination).** Every price stays at most $V$, and there are at most $mV / \delta$ bids. *Proof.* Let bidder $i$ take a new item $j$ with the bundle $S \in D_i(q)$. Then $S \setminus \{j\}$ gives utility at most that of $S$, so $q_j \le v_i(S) - v_i(S \setminus \{j\}) \le V$, using $v_i \ge 0$. The new price of $j$ is $q_j$. Each bid raises $\sum_j p_j$ by at least $\delta$, and this sum is at most $mV$. A pass of the loop L2 to L9 with no bid ends the process, so there are at most $mV/\delta + 1$ passes. $\square$

**Claim 5 (approximate equilibrium).** When the process stops, for every bidder $i$ and every bundle $T$,
$$v_i(X_i) - p(X_i) \ge v_i(T) - p(T) - \delta\,|T \setminus X_i|,$$
and every item without an owner has price $0$. *Proof.* In the last pass no bidder bid, so in her last turn bidder $i$ chose $S = X_i$, hence $X_i \in D_i(q^i)$. Then $v_i(X_i) - q^i(X_i) \ge v_i(T) - q^i(T)$, with $q^i(X_i) = p(X_i)$ and $q^i(T) = p(T) + \delta |T \setminus X_i|$. The last statement is Claim 1. $\square$

**Claim 6 (welfare).** The final allocation has total value at least $\mathrm{OPT} - m\delta$, where $\mathrm{OPT}$ is the largest total value of an allocation. If all values are integers and $\delta < 1/m$, the final allocation is optimal. *Proof.* Let $(T_i)$ be an optimal allocation. Sum Claim 5 with $T = T_i$ over all $i$:
$$\sum_i v_i(X_i) \ge \mathrm{OPT} - \sum_i p(T_i) + \sum_i p(X_i) - \delta \sum_i |T_i \setminus X_i|.$$
The sets $X_i$ cover every item of positive price (Claim 1), and the sets $T_i$ are disjoint, so $\sum_i p(X_i) \ge \sum_i p(T_i)$. The last sum is at most $m$. So the total value is at least $\mathrm{OPT} - m\delta$. With integer values both totals are integers, and $m\delta < 1$ forces equality. $\blacksquare$

The default step of the implementation is $\delta = 1/(m+1)$, so on integer gross substitutes valuations it always returns an optimal allocation. Claim 3 is the only place that uses gross substitutes; without it, line L7 can fail, and the implementation then raises `ValueError`.
