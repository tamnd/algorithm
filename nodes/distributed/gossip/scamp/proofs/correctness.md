---
title: SCAMP keeps consistent views, adds d + c + 1 arcs per join, has mean view a_n0 + (c + 1)(H_n - H_n0), and leases remove crashed nodes
proves: [correctness]
status: full
---

**Setting.** Nodes run SCAMP-SUBSCRIBE (lines L1 to L3), ON-FORWARDED-SUBSCRIPTION (lines L4 to L6) and SCAMP-UNSUBSCRIBE (lines L7 to L9). Each join, each unsubscription and each lease expiry runs to the end before the next one starts. An arc $j \to s$ means that $s$ is in PartialView($j$). $M$ is the number of arcs out of the present nodes, so the mean view is $a = M / n$. A forwarded copy is *lost* if it is never kept, for example because every node it reaches already holds $s$, or because it reaches its hop limit.

**Claim.**

1. *Consistent views.* At all times, no node is in its own PartialView, and $j \in$ InView($s$) if and only if $s \in$ PartialView($j$).
2. *Arcs of one join.* If the contact has $d$ nodes in its PartialView, a join of a new node $s$ with no lost copy adds exactly $d + c + 1$ arcs.
3. *Mean view.* If every join uses a contact that is uniform over the present nodes and no copy is lost, then for $n \ge n_0$, $\mathbb{E}[a_n] = a_{n_0} + (c + 1)(H_n - H_{n_0})$, where $H_n = \sum_{k=1}^{n} 1/k$. From one node with an empty view, $\mathbb{E}[a_n] = (c + 1)(H_n - 1) = (c + 1) \ln n + O(c)$.
4. *Unsubscription.* After SCAMP-UNSUBSCRIBE($s$), no node holds $s$, and the number of arcs falls by $|$PartialView($s$)$|$ plus at least $\min(l', c + 1)$, where $l' = |$InView($s$)$|$.
5. *Leases.* If every subscription expires once in each lease period, every contact is a live node, and no node unsubscribes during the period, then after one full lease period no live node holds a node that crashed before the period started.

**Proof of 1.** By induction over the steps. Every arc is added together with its InView entry, and every arc is removed together with its InView entry: the removals in lines L8 and L9 run over InView($s$), and the out arcs of $s$ are removed from the InViews of their targets. A lease expiry removes $s$ from PartialView($j$) for every $j \in$ InView($s$) and then empties InView($s$). So the two relations match. No self arc is added: line L4 checks $s \ne j$; in line L1 the contact is an old node and $s$ is new, and at a resubscription the contact is taken from the PartialView of $s$, which does not hold $s$ by induction; line L8 skips the case where $j$ is the replacement node itself. $\square$

**Proof of 2.** Line L1 adds the arc $s \to$ contact, which is new because $s$ is new. Lines L2 and L3 send $d + c$ copies. A copy is kept at node $j$ only if $s \notin$ PartialView($j$) (line L4), so each kept copy adds a new arc $j \to s$, and a copy that is kept stops (line L5). No other arc changes. With no lost copy, all $d + c$ copies are kept, so $1 + d + c$ arcs are added. $\square$

**Proof of 3.** By claim 2, $M_{n+1} = M_n + d + c + 1$, where $d$ is the view size of the contact. A uniform contact has $\mathbb{E}[d \mid M_n] = M_n / n$, so

$$\mathbb{E}[M_{n+1}] = \mathbb{E}[M_n] \cdot \frac{n + 1}{n} + c + 1.$$

Divide by $n + 1$:

$$\mathbb{E}[a_{n+1}] = \frac{\mathbb{E}[M_n]}{n} + \frac{c + 1}{n + 1} = \mathbb{E}[a_n] + \frac{c + 1}{n + 1}.$$

Summing from $n_0$ to $n - 1$ gives $\mathbb{E}[a_n] = a_{n_0} + (c + 1) \sum_{k = n_0 + 1}^{n} 1/k = a_{n_0} + (c + 1)(H_n - H_{n_0})$. With $n_0 = 1$ and $a_1 = 0$ this is $(c + 1)(H_n - 1)$, and $H_n = \ln n + O(1)$ (see the [harmonic series](/harmonic-series/)). $\square$

**Proof of 4.** Lines L8 and L9 run over all of InView($s$). Each $j_k$ removes $s$; in line L8 it may add one other node instead, which is not $s$, because $s$ is not in its own PartialView (claim 1). By claim 1, InView($s$) holds every node that holds $s$, so afterwards no node holds $s$. The out arcs of $s$ go away with $s$. The last $\min(l', c + 1)$ nodes of InView($s$) only remove an arc, and each of the others removes one arc and adds at most one. So the count falls by $|$PartialView($s$)$|$ plus at least $\min(l', c + 1)$. $\square$

**Proof of 5.** Let $x$ be a crashed node. The only steps that add an arc into a node $y$ are lines L5 and L8 and line L1. Line L5 adds an arc into the subscriber, and line L1 adds an arc into the contact; a subscriber is live, because a crashed node takes no steps, and a contact is live by assumption. Line L8 runs only at an unsubscription, and there is none during the period. So no arc into $x$ is added during the period. When the subscription of $x$ expires, every node in InView($x$) removes $x$, and by claim 1 these are all the nodes that hold $x$. $x$ cannot subscribe again. So after the expiry no node holds $x$, and this stays true until the end of the period. $\square$

**What is not proved.** The claims do not bound the spread of view sizes around the mean, the number of lost copies in small groups, or the probability that gossip over the views reaches every node. Claim 3 assumes uniform contacts; indirection makes the contact close to uniform, but this is not proved here. These properties are measured on the page.
