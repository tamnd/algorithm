---
title: The approximate MMS algorithm gives every agent three quarters of its maximin share
proves: [correctness]
status: partial
---

**Setting.** There are $n \ge 1$ agents and $m$ goods with additive values $v_{ig} \ge 0$, and $\alpha = 3/4$. We refer to the lines L1 to L14 of the page. For $k$ agents and a set of goods, $\mathrm{MMS}_i$ is the maximin share of agent $i$ for $k$ bundles of that set. In an ordered instance the goods are positions $1, 2, \dots$, and position $q$ is worth the $q$-th largest value of the agent. This proof proves the transfer steps in full: the mapping back from positions to goods, the validity of rule $R_1$, the count of goods before bag filling, and normalization. It cites Garg and Taki (Lemma 3.1), restated as Lemma 1 of Akrami, Garg, Sharma and Taki, for the validity of rules $R_2$ to $R_4$, and Lemmas 8 and 14 of Akrami et al. for the success of bag filling.

**Lemma 1 (mapping back by picking).** Let every agent $i$ have values $x_i$ on a set $G$ of goods, and let $w_i(q)$ be the $q$-th largest value of $x_i$. Let the positions $1, \dots, |G|$ be split into sets $Q_i$. If the positions are taken in increasing order and the owner of each position picks its most valuable free good, then each agent $i$ gets goods with $x_i$-value at least $\sum_{q \in Q_i} w_i(q)$. Also, agent $i$ has the same maximin share under $x_i$ and under $w_i$.

*Proof.* When position $q$ comes, exactly $q - 1$ goods are taken. The owner $i$ of $q$ has $q$ goods of $x_i$-value at least $w_i(q)$, so one of them is free, and the good it picks is worth at least $w_i(q)$. Summing over $Q_i$ gives the bound. The values $w_i$ are the values $x_i$ in a different order, so the two instances have the same partitions up to renaming, and the same maximin share. $\square$

**Lemma 2 (rule $R_1$ is valid).** Let $k \ge 2$ agents remain, let agent $i$ leave with one good $g$, and let $j$ be another agent. Then the maximin share of $j$ for $k - 1$ bundles of the remaining goods is at least its share for $k$ bundles before.

*Proof.* Take a partition of the goods into $k$ bundles, each worth at least $\mathrm{MMS}_j$ to $j$. Let $B$ be the bundle that contains $g$. Remove $B$ and add $B \setminus \{g\}$ to any other bundle. This gives $k - 1$ bundles of the remaining goods, and no bundle lost value, so each is worth at least $\mathrm{MMS}_j$. $\square$

**Lemma 3 (rules $R_2$ to $R_4$; Garg and Taki, Lemma 3.1).** If rule $R_2$ or $R_3$ gives its set to an agent, or rule $R_4$ does so when $R_1$ and $R_3$ do not apply, then no other agent's maximin share for the remaining agents and goods is less than before.

This is cited, not proved here.

**Lemma 4 (enough goods for the bags).** When the loop of line L2 exits in line L6 with $k$ agents left, at least $2k$ goods remain, and every agent left has $\mathrm{MMS}_i > 0$.

*Proof.* If some agent $i$ had $\mathrm{MMS}_i = 0$, then $w_i(S_1) \ge 0 = \frac{3}{4}\mathrm{MMS}_i$, and line L4 would find rule $R_1$. So every agent left has $\mathrm{MMS}_i > 0$. Suppose fewer than $2k$ goods remain, and take an MMS partition of agent $i$ into $k$ bundles. By the pigeonhole principle, some bundle has at most one good. It is not empty, because each bundle is worth at least $\mathrm{MMS}_i > 0$. So it is one good worth at least $\mathrm{MMS}_i$, and the largest good $g_1$ is worth at least as much. Then $w_i(S_1) \ge \mathrm{MMS}_i \ge \frac{3}{4}\mathrm{MMS}_i$, and line L4 would find rule $R_1$, which is a contradiction. $\square$

**Lemma 5 (normalization).** Let $k$ agents be left after line L6, with $\mathrm{MMS}_i > 0$ by Lemma 4. Then the values $u_i$ of line L7 satisfy $w_i(S) \ge \mathrm{MMS}_i \cdot u_i(S)$ for every set $S$ of the remaining goods, and the maximin share of $u_i$ for $k$ bundles is 1.

*Proof.* Line L7 uses an MMS partition $P$ of agent $i$, so $w_i(P_j) \ge \mathrm{MMS}_i > 0$ for every bundle. For $g \in P_j$, $u_i(g) = w_i(g)/w_i(P_j) \le w_i(g)/\mathrm{MMS}_i$. Summing over $S$ gives the first claim. Each bundle $P_j$ has $u_i(P_j) = 1$, so the share of $u_i$ is at least 1. The total $u_i$-value is $k$, so no partition into $k$ bundles has all bundles above 1, and the share is exactly 1. $\square$

**Lemma 6 (bag filling succeeds; Akrami et al., Lemmas 8 and 14).** In lines L9 to L12, on the ordered normalized instance of line L8, every agent gets a bag with $u_i$-value at least $3/4$ before the free goods run out.

This is cited, not proved here. Lines L8 to L12 follow the instance $\mathrm{toOrd}(\mathrm{normalize}(\cdot))$ of their Lemma 5 and the bags $\{t, 2k + 1 - t\}$ of their Algorithm 3, and Lemmas 4 and 5 above give the conditions that their lemmas use.

**Theorem.** The allocation returned in line L14 gives every agent $i$ a bundle $A_i$ with $v_i(A_i) \ge \frac{3}{4}\mathrm{MMS}_i$, where $\mathrm{MMS}_i$ is the share for $n$ bundles of all goods, and every good goes to exactly one agent.

*Proof.* By Lemma 1, the instance $w$ of line L1 has the same shares as $v$, and it is enough to give each agent a set of positions with $w_i$-value at least $\frac{3}{4}\mathrm{MMS}_i$; the last picking step of line L13 then gives goods with at least that $v_i$-value.

By Lemmas 2 and 3 and induction on the number of rules applied, every agent still present has a share for the current agents and goods at least its share at the start. An agent that leaves in line L5 gets $S_r$ with $w_i(S_r) \ge \frac{3}{4}$ of its current share, so at least $\frac{3}{4}\mathrm{MMS}_i$.

If the loop of line L2 ends because no goods remain, the agents left have a current share of 0, so their starting share is 0 and the empty bundle is enough. If it ends because no agents remain, the free goods go to one agent and only add value.

Otherwise the loop exits in line L6, and Lemma 4 gives at least $2k$ goods, so the bags of line L9 exist. By Lemma 6, each agent $i$ left gets a bag of positions with $u_i$-value at least $3/4$ in the order of line L8. Lemma 1, applied to $u$, maps the bag to goods with $u_i$-value at least $3/4$, and Lemma 5 gives them $w_i$-value at least $\frac{3}{4}$ of the current share, which is at least $\frac{3}{4}\mathrm{MMS}_i$. The unused positions of line L13 go to one agent and only add value.

Each picking step gives each good to exactly one agent, so the result is an allocation of all goods. $\blacksquare$
