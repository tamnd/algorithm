---
title: The generalized second-price auction ranks by bid, charges the next bid, is individually rational, and is not truthful
proves: [correctness]
status: full
---

We use the pseudocode of the page: $n$ bidders, $k$ slots with click-through rates $\alpha_1 \ge \alpha_2 \ge \cdots \ge \alpha_k \ge 0$, and a reserve $r \ge 0$. A bidder in slot $s$ with value $v$ per click and price $\pi_s$ per click gets the utility $\alpha_s (v - \pi_s)$, and a bidder with no slot gets 0. Let $R_1, R_2, \ldots$ be the eligible bidders (bid at least $r$) in the order of line L1, and write $b_{(s)}$ for the bid of $R_s$.

**Claim 1 (the output).** For $s = 1, \ldots, q = \min(k, |R|)$, slot $s$ goes to $R_s$ and its price per click is $\pi_s = b_{(s+1)}$ if $s < |R|$, and $\pi_s = r$ otherwise. No bidder gets two slots, and every slot after $q$ stays empty.

*Proof.* Line L1 lists each eligible bidder once, in a fixed order. Lines L3 and L4 give slot $s$ to the $s$-th bidder of the list, so the slots go to distinct bidders. Lines L5 and L6 set the price as stated. $\square$

**Claim 2 (no bidder pays more than its bid).** For $s \le q$, $r \le \pi_s \le b_{(s)}$. So a bidder that bids its value never gets a negative utility, and a bidder that bids at least $r$ but gets no slot pays nothing.

*Proof.* The list is sorted, so $b_{(s+1)} \le b_{(s)}$, and $b_{(s+1)} \ge r$ because $R_{s+1}$ is eligible. If $s = |R|$, the price is $r \le b_{(s)}$. A bidder that bids $v$ and gets slot $s$ gets $\alpha_s (v - \pi_s) \ge 0$. $\square$

**Claim 3 (one slot is the Vickrey auction).** If $k = 1$, the highest eligible bid wins and pays the larger of $r$ and the second-highest eligible bid. A bid below $r$ cannot win, so this is the larger of $r$ and the highest other bid, which is the price of the [Vickrey auction](/vickrey-auction/) with reserve $r$, with the same tie rule. $\square$

**Claim 4 (truthful bidding is not dominant when $k \ge 2$).** Take the example of Edelman, Ostrovsky and Schwarz (2007, Section II): values $10, 4, 2$, two slots with $\alpha_1 = 200$ and $\alpha_2 = 199$ clicks, and $r = 0$. With truthful bids, bidder 1 gets slot 1 at the price 4, so its utility is $200 \cdot (10 - 4) = 1200$. If it bids 3, it is ranked second and pays the next bid 2, so its utility is $199 \cdot (10 - 2) = 1592 > 1200$. $\square$

The general reason: the price of slot $s$ is the bid of the next bidder, and the price of slot $s + 1$ is the bid after that. A bidder trades $\alpha_s - \alpha_{s+1}$ clicks against a lower price per click on all its clicks, and when the click-through rates are close, the lower price wins.

**Claim 5 (for the same bids, GSP charges at least the VCG payments).** Let $r = 0$, let all bids be at least 0, and put $\alpha_{t} = 0$ for $t > k$ and $b_{(t)} = 0$ when $R_t$ does not exist. The VCG payment of the bidder in slot $s$, computed from the bids, is $P_s = \sum_{t=s}^{k} (\alpha_t - \alpha_{t+1})\, b_{(t+1)}$. The GSP payment of the same bidder is $\alpha_s b_{(s+1)} \ge P_s$.

*Proof.* Each factor $\alpha_t - \alpha_{t+1}$ is at least 0, and $b_{(t+1)} \le b_{(s+1)}$ for $t \ge s$. So $P_s \le b_{(s+1)} \sum_{t=s}^{k} (\alpha_t - \alpha_{t+1}) = b_{(s+1)} \alpha_s$, because the sum telescopes and $\alpha_{k+1} = 0$. $\square$

This is Remark 1 of Edelman, Ostrovsky and Schwarz (2007). It does not say that GSP earns more than VCG in equilibrium, because the bids in GSP are not truthful. The equilibrium with the VCG outcome is proved on the page [Locally envy-free equilibrium of GSP](/gsp-envy-free-equilibrium/).
