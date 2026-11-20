---
title: The simultaneous ascending auction stops, and with gross substitutes it ends near a Walrasian equilibrium with welfare at least OPT minus m epsilon
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n$ bidders and a set $M$ of $m$ items. Bidder $i$ has a valuation $v_i$ with $v_i(\emptyset) = 0$, and $V = \max_i v_i(M)$; we assume $v_i$ is monotone, so $v_i(S) \le V$ for every bundle $S$. The increment is $\epsilon > 0$. In round $r$, bidder $i$ holds the set $H_i$ of items $j$ with $h_j = i$, faces the personal prices $q^i_j = p_j$ for $j \in H_i$ and $q^i_j = p_j + \epsilon$ for $j \notin H_i$, and picks a bundle $T_i$ in its demand set $D_i(q^i) = \arg\max_S \big(v_i(S) - \sum_{j \in S} q^i_j\big)$ (line L5). It bids on $T_i \setminus H_i$ (line L6).

**Claim 1 (termination).** The auction stops after at most $mV/\epsilon + 1$ rounds. Every price is at most $V$, and an item that is not sold has price 0.

*Proof.* The empty bundle gives utility 0, so $v_i(T_i) - \sum_{j \in T_i} q^i_j \ge 0$. All personal prices are at least 0, so each $q^i_j$ with $j \in T_i$ is at most $v_i(T_i) \le V$. A bid on item $j$ is made at the personal price $p_j + \epsilon$, and line L9 sets $p_j$ to this value, so after the bid $p_j \le V$. Prices never fall, so the sum of the prices is at most $mV$ at all times. Every round that does not stop has a new bid, and line L9 raises the sum by at least $\epsilon$. So there are at most $mV/\epsilon$ such rounds, and one more round stops the auction. An item that never gets a bid keeps the price 0 and the holder NIL; an item that gets a bid keeps a holder forever, because bids cannot be withdrawn. $\square$

**Claim 2 (holdings are never wanted less, under gross substitutes).** Assume every $v_i$ has gross substitutes: for prices $q \le q'$ and every $S \in D_i(q)$ there is $S' \in D_i(q')$ that contains each item $j \in S$ with $q_j = q'_j$. Then in every round, each bidder picks $T_i \supseteq H_i$.

*Proof.* By induction on the rounds. In round 1, $H_i = \emptyset$. Assume that in round $r$ bidder $i$ picked $T \supseteq H$ at the personal prices $q$, and let $H'$ and $q'$ be its holdings and personal prices in round $r + 1$.

- $H' \subseteq T$. An item that $i$ holds after round $r$ was either held before, so it is in $H \subseteq T$, or won in round $r$, so it is in $T \setminus H$.
- $q' \ge q$, with equality on $H'$. Take an item $j$. If $j \in H'$ and $j \in H$, nobody bid on $j$ in round $r$ (any new bid would take it from $i$), so $q'_j = p_j = q_j$. If $j \in H'$ and $j \notin H$, then $i$ bid on $j$ at $q_j = p_j + \epsilon$ and won, so the new price is $q_j$ and $q'_j = q_j$. If $j \notin H'$, then $q'_j$ is the new price of $j$ plus $\epsilon$. Prices do not fall, and if $j \in H$ was lost, its price rose by $\epsilon$, so $q'_j \ge q_j$ in both cases.

By gross substitutes applied to $T \in D_i(q)$, some $S' \in D_i(q')$ contains every item of $T$ whose personal price did not change, and these include $H'$. So a demanded bundle that contains $H'$ exists, and the tie rule of line L5 picks one. $\square$

**Claim 3 (the end is near a Walrasian equilibrium, under gross substitutes).** When the auction stops, each bidder holds a bundle in its demand set at its personal prices, $H_i \in D_i(q^i)$, and its utility $v_i(H_i) - \sum_{j \in H_i} p_j$ is at least 0. The welfare satisfies $\sum_i v_i(H_i) \ge \sum_i v_i(O_i) - m\epsilon$ for every allocation $(O_1, \ldots, O_n)$.

*Proof.* In the last round no bidder bids, so $T_i \setminus H_i = \emptyset$, and by Claim 2 $T_i \supseteq H_i$, hence $H_i = T_i \in D_i(q^i)$. On $H_i$ the personal prices equal the prices, and $\emptyset$ is a candidate bundle, so the utility is at least 0. For any allocation $O$, $H_i \in D_i(q^i)$ gives
$$v_i(H_i) - \sum_{j \in H_i} p_j \ge v_i(O_i) - \sum_{j \in O_i} q^i_j \ge v_i(O_i) - \sum_{j \in O_i} p_j - \epsilon |O_i|.$$
Sum over $i$. The sets $H_i$ hold every sold item, and unsold items have price 0 (Claim 1), so $\sum_i \sum_{j \in H_i} p_j = \sum_{j \in M} p_j \ge \sum_i \sum_{j \in O_i} p_j$, since the $O_i$ are disjoint and prices are at least 0. Also $\sum_i |O_i| \le m$. So $\sum_i v_i(H_i) \ge \sum_i v_i(O_i) - m\epsilon$. $\square$

As $\epsilon \to 0$, the outcome tends to a [Walrasian equilibrium](/competitive-equilibrium/), and the welfare to the optimum. This is the case of the [Kelso-Crawford process](/kelso-crawford-process/) with simultaneous bids.

**Claim 4 (without gross substitutes, a bidder can lose money).** Let bidder 1 value the pair $\{A, B\}$ at 10 and each single item at 0, let bidder 2 value $A$ at 9, and let bidder 3 value $B$ at 3, with $\epsilon = 1$. Bidder 1 holds both items at the prices $(3, 3)$ after round 3. Bidder 3 stops bidding at price 3, so bidder 1 keeps $B$ at 3, while bidders 1 and 2 raise the price of $A$ in turns. At the price 8 held by bidder 2, the pair would cost bidder 1 at least $9 + 3 = 12 > 10$, so it demands the empty set, but it cannot withdraw its bid on $B$. It ends with $B$ at price 3 and utility $-3$. Bidder 2 wins $A$ at 8. The welfare is 9, while the optimum gives $A$ to bidder 2 and $B$ to bidder 3 for 12. The valuation of bidder 1 has complements, so Claim 2 fails for it: in round 9 its only demanded bundle is $\emptyset$, which does not contain $H_1 = \{B\}$. $\square$
