---
title: The Moulin mechanism serves the unique largest affordable set and is group strategyproof
proves: [correctness]
status: full
---

**Setting.** $A$ is a finite set of $n$ players and $C : 2^A \to \mathbb{R}_{\ge 0}$ is a cost function with $C(\emptyset) = 0$. A cost-sharing method $\xi$ gives each nonempty $S \subseteq A$ and each $i \in S$ a share $\xi(i, S) \ge 0$. It is *cross-monotonic* if $\xi(i, S) \ge \xi(i, T)$ whenever $i \in S \subseteq T$. It is *$\beta$-budget balanced* if $C(S) \le \sum_{i \in S} \xi(i, S) \le \beta\, C(S)$ for every nonempty $S$; $\beta = 1$ is exact budget balance. Player $i$ has a private value $v_i$ for being served and reports a bid $b_i$. If the mechanism serves the set $S$ and charges $p_i$, the utility of player $i$ is $u_i = v_i - p_i$ if $i \in S$ and $u_i = -p_i$ otherwise.

The mechanism (lines L1 to L7) starts with $S = A$, removes every $i \in S$ with $b_i < \xi(i, S)$, repeats until nobody is removed, serves the final $S$, charges $p_i = \xi(i, S)$ for $i \in S$ and $p_i = 0$ for $i \notin S$. Assume from here that $\xi$ is cross-monotonic.

**Definition.** For bids $b$, a set $T \subseteq A$ is *affordable* if $b_i \ge \xi(i, T)$ for every $i \in T$. The empty set is affordable.

**Lemma 1.** The union of two affordable sets is affordable. So there is a unique largest affordable set $M(b)$, the union of all affordable sets.

*Proof.* Let $T_1$ and $T_2$ be affordable and $i \in T_1 \cup T_2$, say $i \in T_1$. By cross-monotonicity, $\xi(i, T_1 \cup T_2) \le \xi(i, T_1) \le b_i$. $\square$

**Lemma 2.** The mechanism stops after at most $n + 1$ rounds and serves exactly $M(b)$.

*Proof.* Each round other than the last removes at least one player, so there are at most $n + 1$ rounds. We show that $M = M(b) \subseteq S$ holds before every round. It holds at the start, since $S = A$. Assume $M \subseteq S$ and let $i \in M$. Cross-monotonicity gives $\xi(i, S) \le \xi(i, M) \le b_i$, so line L3 does not remove $i$, and $M \subseteq S$ holds after line L4. In the last round nobody is removed, so every $i \in S$ has $b_i \ge \xi(i, S)$, and $S$ is affordable. Then $S \subseteq M$, so $S = M$. $\square$

Lemma 2 also shows that the order of removals does not matter: removing one player at a time, or all at once, gives the same set.

**Lemma 3 (participation and budget).**
1. *No positive transfers:* $p_i \ge 0$ for all $i$.
2. *Voluntary participation:* a served player pays at most its bid, and an unserved player pays 0. So a truthful player has $u_i \ge 0$.
3. *Consumer sovereignty:* a player who bids $b_i \ge \xi(i, \{i\})$ is served, whatever the other bids are.
4. *Budget balance:* the payments sum to $\sum_{i \in S} \xi(i, S)$, which is between $C(S)$ and $\beta\, C(S)$ for a $\beta$-budget balanced method.

*Proof.* Items 1 and 4 hold because the payments are shares of the served set. For item 2, the served set is affordable by Lemma 2. For item 3, let $M = M(b)$. Every $j \in M$ has $\xi(j, M \cup \{i\}) \le \xi(j, M) \le b_j$, and $\xi(i, M \cup \{i\}) \le \xi(i, \{i\}) \le b_i$, both by cross-monotonicity. So $M \cup \{i\}$ is affordable, and $i \in M$ by Lemma 1. $\square$

**Theorem (group strategyproofness).** Let $v$ be the true values and let $K \subseteq A$ be a coalition. Let $b$ agree with $v$ outside $K$. Let $u_i$ be the utility of $i$ when everyone bids truthfully, and $u'_i$ the utility of $i$ under $b$. If $u'_i \ge u_i$ for every $i \in K$, then $u'_i = u_i$ for every $i \in K$. So no coalition can misreport in a way that helps one of its members and hurts none.

*Proof.* Let $F = M(v)$ be the served set under the true values and $F' = M(b)$ the served set under $b$. Assume $u'_i \ge u_i$ for all $i \in K$.

*Step 1: $F' \subseteq F$.* We show that $F \cup F'$ is affordable for the bids $v$. Let $i \in F \cup F'$.
- If $i \in F$, then $v_i \ge \xi(i, F) \ge \xi(i, F \cup F')$, because $F$ is affordable for $v$.
- If $i \in F' \setminus K$, then $v_i = b_i \ge \xi(i, F') \ge \xi(i, F \cup F')$, because $F'$ is affordable for $b$.
- If $i \in F' \cap K$, then $v_i - \xi(i, F') = u'_i \ge u_i \ge 0$ by Lemma 3, item 2. So $v_i \ge \xi(i, F') \ge \xi(i, F \cup F')$.

In each case the second inequality is cross-monotonicity. So $F \cup F'$ is affordable for $v$, and $F \cup F' \subseteq M(v) = F$ by Lemma 1. Hence $F' \subseteq F$.

*Step 2: no member gains.* Let $i \in K$.
- If $i \in F'$, then $i \in F$ by Step 1, and $\xi(i, F') \ge \xi(i, F)$ by cross-monotonicity, since $F' \subseteq F$. So $u'_i = v_i - \xi(i, F') \le v_i - \xi(i, F) = u_i$.
- If $i \notin F'$ and $i \in F$, then $u'_i = 0 \le u_i$, by Lemma 3, item 2.
- If $i \notin F'$ and $i \notin F$, then $u'_i = 0 = u_i$.

So $u'_i \le u_i$ for every $i \in K$. Together with the assumption, $u'_i = u_i$. $\square$

With $K = \{i\}$ the theorem says that truthful bidding is a dominant strategy, so the mechanism is also [dominant-strategy incentive compatible](/dominant-strategy-incentive-compatibility/).

**Cost.** By Lemma 2 there are at most $n + 1$ rounds. Each round computes the shares of one set once and compares $|S| \le n$ bids. If one call of the method takes time $t$, the total time is $O(n (n + t))$.

**Remark.** The tests in `impl/python/test_moulin_mechanism.py` compare the served set with the union of all affordable sets found by brute force on 500 random coverage cost functions with Shapley shares, check items 1 to 4 of Lemma 3, and check the theorem by brute force over every coalition and every misreport on a grid of 5 bids for an airport game with 3 players, including the bids equal to the shares. They also check that a method that is not cross-monotonic (Bird's rule on a small spanning tree game) gives a profitable lie. $\blacksquare$
