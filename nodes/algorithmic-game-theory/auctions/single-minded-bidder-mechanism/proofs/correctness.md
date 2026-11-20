---
title: The greedy mechanism for single-minded bidders is feasible, truthful and a square root of m approximation
proves: [correctness]
status: full
---

We use the pseudocode of the page. Bidder $i$ reports a nonempty bundle $S_i \subseteq M$ and a value $v_i \ge 0$, and $m = |M|$. The *key* of a bid $(S, v)$ is $v / \sqrt{|S|}$. Line L1 orders the bidders by key, highest first, with ties to the smaller index; the code compares $v_i^2 / |S_i|$ exactly, which gives the same order. We say $i$ *precedes* $j$ if $i$ comes before $j$ in this order. The greedy run of lines L2 to L4 accepts a bidder when its bundle is disjoint from the bundles accepted before it. Let $W$ be the set of accepted bidders.

**Claim 1 (feasibility).** The bundles of the bidders in $W$ are pairwise disjoint.

*Proof.* Line L4 accepts a bidder only if its bundle is disjoint from the union of the bundles accepted before it. $\square$

**Claim 2 (the approximation).** Let $O$ be a set of bidders with pairwise disjoint bundles. Then $\sum_{j \in O} v_j \le \sqrt{m} \sum_{i \in W} v_i$.

*Proof.* Take $j \in O$. If $j \in W$, put $f(j) = j$. Otherwise line L4 rejected $j$, so some accepted bidder that precedes $j$ has a bundle that meets $S_j$; let $f(j)$ be the first such bidder in the order. In both cases $f(j) \in W$, $S_{f(j)}$ meets $S_j$, and $f(j)$ precedes $j$ or equals it, so its key is at least the key of $j$: $v_j \le v_{f(j)} \sqrt{|S_j|} / \sqrt{|S_{f(j)}|}$.

For $i \in W$, let $O_i = \{j \in O : f(j) = i\}$. The bundles $S_j$ for $j \in O_i$ are disjoint and each meets $S_i$, so $|O_i| \le |S_i|$. They are also subsets of $M$, so $\sum_{j \in O_i} |S_j| \le m$. By the Cauchy-Schwarz inequality,

$$\sum_{j \in O_i} v_j \le \frac{v_i}{\sqrt{|S_i|}} \sum_{j \in O_i} \sqrt{|S_j|} \le \frac{v_i}{\sqrt{|S_i|}} \sqrt{|O_i|} \sqrt{\sum_{j \in O_i} |S_j|} \le \frac{v_i}{\sqrt{|S_i|}} \sqrt{|S_i|} \sqrt{m} = \sqrt{m}\, v_i.$$

The sets $O_i$ for $i \in W$ partition $O$, so summing over $i \in W$ gives the claim. $\square$

The bound uses only items that appear in some bundle, so $m$ can be the size of the union of the bundles.

**Claim 3 (monotonicity).** Fix the bids of all bidders except $i$. If bidder $i$ wins with the bid $(T, w)$, it also wins with every bid $(T', w')$ with $T' \subseteq T$, $T' \neq \emptyset$ and $w' \ge w$.

*Proof.* The key of $(T', w')$ is at least the key of $(T, w)$, so bidder $i$ moves to the same place or earlier in the order, and the relative order of the other bidders does not change. Line L4 treats the bidders before $i$ in the same way in every run, because their treatment does not depend on bids that come later. So the set $A$ of bidders accepted before $i$ with the bid $(T', w')$ is the set of bidders accepted before $i$ in the run with $(T, w)$ that precede the new place of $i$, a subset of the old set. The old set has no bundle that meets $T$. So no bundle in $A$ meets $T' \subseteq T$, and $i$ is accepted. $\square$

**Claim 4 (the payment is the critical value).** Fix the bids of the others and a bundle $T$ reported by bidder $i$. Run the greedy algorithm without $i$, and let $j$ be the first bidder accepted in this run whose bundle meets $T$. Put $\theta(T) = v_j \sqrt{|T| / |S_j|}$, and $\theta(T) = 0$ if no such $j$ exists. Then bidder $i$ wins with $(T, w)$ if $w > \theta(T)$ and loses if $w < \theta(T)$. Lines L6 and L7 charge a winner exactly $\theta(T)$.

*Proof.* As in Claim 3, the bidders that precede $i$ are treated the same as in the run without $i$. So bidder $i$ is accepted if and only if no bidder accepted before it in the run without $i$ has a bundle that meets $T$, that is, if and only if $i$ precedes $j$ (or $j$ does not exist). Bidder $i$ precedes $j$ when $w / \sqrt{|T|} > v_j / \sqrt{|S_j|}$, that is, $w > \theta(T)$, and does not precede $j$ when $w < \theta(T)$. At $w = \theta(T)$ the tie rule decides. Line L6 finds this $j$ for the reported bundle, and line L7 charges $\theta(T)$. $\square$

**Claim 5 (truthful bidding is a dominant strategy, and it is individually rational).** A single-minded bidder $i$ with the true bundle $S$ and value $v$ gets value $v$ from every bundle that contains $S$ and 0 from all others. For every report $(T, w)$ of bidder $i$ and every report of the others, the utility of $(S, v)$ is at least the utility of $(T, w)$ and at least 0.

*Proof.* By Claim 4, the truthful report gives $v - \theta(S)$ when it wins, which happens if $v > \theta(S)$ and fails if $v < \theta(S)$. So its utility is $\max(0, v - \theta(S))$, or 0 when $v = \theta(S)$. In every case it is $\max(0, v - \theta(S))$, which is at least 0.

Now take a report $(T, w)$. If it loses, its utility is 0. If it wins and $T \not\supseteq S$, the bidder gets value 0 and pays $\theta(T) \ge 0$, so its utility is at most 0. If it wins and $T \supseteq S$, its utility is $v - \theta(T)$. By Claim 3, every $w' > \theta(T)$ makes $(S, w')$ win, so by Claim 4 $\theta(S) \le \theta(T)$. Hence $v - \theta(T) \le v - \theta(S) \le \max(0, v - \theta(S))$. $\square$

**Claim 6 (the bound of Claim 2 is tight for this algorithm).** Let $m = q^2$, with one bidder for all of $M$ with value $q + \epsilon$, and $m$ bidders for the single items with value 1. The first bidder has key $(q + \epsilon)/q > 1$, so it is accepted first and blocks all the others. The welfare is $q + \epsilon$, while the single items give $m = q^2$. The ratio $q^2/(q + \epsilon)$ tends to $\sqrt{m}$ as $\epsilon \to 0$. $\square$
