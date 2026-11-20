---
title: The Vickrey auction picks the highest bid, charges the critical price and makes truthful bidding dominant
proves: [correctness]
status: full
---

We use the pseudocode of the page, with bids $b_1, \ldots, b_n$ and a reserve $r$. Call bidder $i$ *eligible* if $b_i \ge r$. Let $w^*$ be the smallest index among the eligible bidders with the largest bid, and $w^* = \mathrm{NIL}$ if no bidder is eligible. For a bidder $i$, let $m_i = \max(\{r\} \cup \{b_j : j \ne i\})$.

**Claim 1.** VICKREY returns $(w^*, m_{w^*})$ if some bidder is eligible, and $(\mathrm{NIL}, 0)$ otherwise.

*Proof.* We use this invariant of the loop of line L2.

> **(I)** Before the iteration for $i$, with $1 \le i \le n + 1$: (a) $w$ is the smallest index among the eligible bidders of $1, \ldots, i - 1$ with the largest bid, or NIL if none of them is eligible; (b) $s = \max(\{r\} \cup \{b_j : j < i, j \ne w\})$.

*Initialization.* For $i = 1$, line L1 gives $w = \mathrm{NIL}$ and $s = r$, and both sets are empty.

*Maintenance.* Assume (I) for $i \le n$.

- If line L3 is true, $b_i \ge r$ and either no earlier bidder is eligible or $b_i$ is strictly larger than the best earlier eligible bid. So $i$ is the new leader, and it is the smallest index with that bid, because every earlier bid is smaller; (a) holds for $i + 1$. If $w$ was NIL, all earlier bids are below $r$ and $s = r$ is still correct. Otherwise line L4 sets $s = b_w$. This is correct, because $b_w \ge r$, and $b_w \ge b_j$ for every earlier $j$: an earlier eligible $j$ has $b_j \le b_w$ by (a), and an earlier ineligible $j$ has $b_j < r \le b_w$. Line L5 makes $i$ the leader, so (b) holds for $i + 1$.
- If line L3 is false, either $b_i < r$, or $b_i \le b_w$. In both cases $i$ does not become the leader: an ineligible bid cannot lead, and a tie with $b_w$ goes to the smaller index $w$. So (a) holds for $i + 1$. Line L6 adds $b_i$ to the maximum, so (b) holds for $i + 1$.

*Termination.* For $i = n + 1$, (a) says $w = w^*$ and (b) says $s = m_w$. Lines L7 and L8 return the claimed pair. $\square$

**Claim 2 (truthful bidding is a weakly dominant strategy).** Fix $i$, a value $v_i$ and bids $b_{-i}$ of the others. Let $u(b_i)$ be the utility $v_i - m_i$ if $i$ wins and 0 if it loses. Then $u(v_i) \ge u(b_i)$ for every bid $b_i$, and $u(v_i) \ge 0$.

*Proof.* The value $m_i$ does not depend on $b_i$. By Claim 1, bidder $i$ wins if and only if $b_i \ge r$ and $b_i$ beats every other eligible bid with the tie rule. So there is a threshold: $i$ wins when $b_i > m_i$, loses when $b_i < m_i$, and at $b_i = m_i$ the tie rule decides, with an outcome that depends only on $b_{-i}$. When $i$ wins, it pays $m_i$, whatever its bid.

- If $v_i > m_i$, the bid $v_i$ wins and gives $v_i - m_i > 0$. Any other bid gives either $v_i - m_i$ (if it wins) or 0.
- If $v_i < m_i$, the bid $v_i$ loses and gives 0. Any winning bid gives $v_i - m_i < 0$.
- If $v_i = m_i$, every bid gives 0, as a win pays $m_i = v_i$.

In all three cases $u(v_i) = \max(0, v_i - m_i)$, which is at least $u(b_i)$ and at least 0. $\square$

**Claim 3 (efficiency).** If every bidder bids its value and $r = 0$, the winner has the largest value. With a reserve $r$, the item goes to a bidder of the largest value if that value is at least $r$, and is not sold otherwise.

*Proof.* Immediate from Claim 1 with $b = v$. $\square$

**Cost.** The loop runs $n$ times, and each iteration does at most two comparisons in line L3 and one maximum in line L6. The time is $\Theta(n)$ and the extra space is $O(1)$.
