---
title: The Jain-Vazirani solution has connection cost plus three times facility cost at most three times a feasible dual
proves: [correctness]
status: full
---

**Setting.** Facilities $i$ have costs $f_i \ge 0$, clients $j$ have connection costs $c_{ij} \ge 0$, and $c$ extends to a metric on facilities and clients, so $c_{i'j} \le c_{i'j'} + c_{ij'} + c_{ij}$ for all facilities $i, i'$ and clients $j, j'$. The dual LP is $\max \sum_j \alpha_j$ subject to $\sum_j \beta_{ij} \le f_i$ and $\alpha_j - \beta_{ij} \le c_{ij}$ with $\beta \ge 0$; for given $\alpha$ the best choice is $\beta_{ij} = \max(0, \alpha_j - c_{ij})$, and we always use it. Write $P_i(\alpha) = \sum_j \max(0, \alpha_j - c_{ij})$ for the payment to facility $i$. In phase 1, time $t$ grows from 0, every active client has $\alpha_j = t$, and every frozen client keeps the value it had when it froze. Let $t_i$ be the time at which facility $i$ becomes temporarily open, and for a frozen client $j$ let its witness $w(j)$ be a temporarily open facility with $c_{w(j) j} \le \alpha_j$ at the time $j$ froze. Let $X$ be the output of phase 2.

**Lemma 1 (phase 1 ends).** Phase 1 ends, every client freezes, and every client has a witness.

*Proof.* A client $j$ that is active at time $t \ge \min_i (c_{ij} + f_i)$ pays at least $f_i$ to the facility $i$ that attains the minimum, so that facility is open by then, and $j$ freezes at once. So every client freezes by time $\max_j \min_i (c_{ij} + f_i)$. A client freezes only in line L5, which names a temporarily open facility with $c_{ij} \le \alpha_j$ as its witness. $\square$

**Lemma 2 (dual feasibility).** At every time, $P_i(\alpha) \le f_i$ for each facility $i$. If $i$ is temporarily open, then $P_i(\alpha) = f_i$ from time $t_i$ on.

*Proof.* While $i$ is closed, $P_i$ is continuous and nondecreasing in $t$, and line L4 opens $i$ at the first time when $P_i = f_i$. So $P_i \le f_i$ before $t_i$ and $P_i = f_i$ at $t_i$. After $t_i$, consider a client $j$. If $j$ is frozen, $\alpha_j$ is fixed. If $j$ is active with $\alpha_j \ge c_{ij}$, line L5 freezes it at once, since $i$ is open. If $j$ is active with $\alpha_j < c_{ij}$, its term in $P_i$ is 0, and when $\alpha_j$ reaches $c_{ij}$, line L5 freezes it with term still 0. So no term of $P_i$ grows after $t_i$, and $P_i = f_i$ stays. $\square$

**Lemma 3 (timing).** If $\beta_{ij} > 0$ at the end and $i$ is temporarily open, then $\alpha_j \le t_i$. For each client $j$, $\alpha_j \ge t_{w(j)}$.

*Proof.* For the first claim: if $j$ were still active at some time after $t_i$, then by the proof of Lemma 2 it freezes at the first moment with $\alpha_j \ge c_{ij}$, which happens at time $\max(t_i, c_{ij})$; if $c_{ij} \ge t_i$, then $\alpha_j = c_{ij}$ and $\beta_{ij} = 0$, against the assumption. So either $j$ froze at a time at most $t_i$, giving $\alpha_j \le t_i$, or $c_{ij} < t_i$ and $j$ freezes at time $t_i$, giving $\alpha_j = t_i$. For the second claim: $j$ froze at a time when $w(j)$ was already open, so at a time at least $t_{w(j)}$, and $\alpha_j$ equals that time. $\square$

**Lemma 4 (phase 2).** No client $j$ has $\beta_{ij} > 0$ for two facilities of $X$. Each temporarily open $i \notin X$ has some $i' \in X$ and some client $j'$ with $\beta_{ij'} > 0$ and $\beta_{i'j'} > 0$.

*Proof.* Line L8 adds $i$ only if no client pays both $i$ and a facility already in $X$, so no two facilities of $X$ share a paying client. If line L8 skips $i$, the reason is such a shared client $j'$ with a facility $i'$ already in $X$, and $i'$ stays in $X$. $\square$

**Lemma 5 (facility cost).** Call a client $j$ *direct* if $\beta_{ij} > 0$ for some $i \in X$, and call this facility $\phi(j)$; it is unique by Lemma 4. Then $F = \sum_{i \in X} f_i = \sum_{j \text{ direct}} \beta_{\phi(j) j}$.

*Proof.* By Lemma 2, each $i \in X$ has $f_i = \sum_j \beta_{ij}$. Each positive term $\beta_{ij}$ with $i \in X$ belongs to a direct client with $\phi(j) = i$, and by Lemma 4 each direct client gives exactly one such term. Summing over $X$ gives the claim. $\square$

**Lemma 6 (connection cost).** Let $\sigma(j)$ be the nearest facility of $X$ to $j$. If $j$ is direct, $c_{\sigma(j) j} + 3 \beta_{\phi(j) j} \le 3 \alpha_j$. If $j$ is not direct, $c_{\sigma(j) j} \le 3 \alpha_j$.

*Proof.* If $j$ is direct, $\beta_{\phi(j) j} = \alpha_j - c_{\phi(j) j} > 0$, so $c_{\sigma(j) j} + 3\beta_{\phi(j) j} \le c_{\phi(j) j} + 3(\alpha_j - c_{\phi(j) j}) = 3\alpha_j - 2 c_{\phi(j) j} \le 3\alpha_j$.

Let $j$ be not direct, and let $i = w(j)$, so $c_{ij} \le \alpha_j$ and $t_i \le \alpha_j$ by Lemma 3. If $i \in X$, then $c_{\sigma(j) j} \le c_{ij} \le \alpha_j$. Otherwise Lemma 4 gives $i' \in X$ and $j'$ with $\beta_{ij'} > 0$ and $\beta_{i'j'} > 0$, so $c_{ij'} < \alpha_{j'}$ and $c_{i'j'} < \alpha_{j'}$, and Lemma 3 gives $\alpha_{j'} \le t_i \le \alpha_j$. By the triangle inequality,

$$c_{\sigma(j) j} \le c_{i'j} \le c_{i'j'} + c_{ij'} + c_{ij} < \alpha_{j'} + \alpha_{j'} + \alpha_j \le 3\alpha_j. \qquad \square$$

**Theorem.** The output satisfies $C + 3F \le 3 \sum_j \alpha_j$, where $C = \sum_j c_{\sigma(j) j}$, and $\alpha$ with $\beta_{ij} = \max(0, \alpha_j - c_{ij})$ is a feasible dual. So $C + F \le C + 3F \le 3 \sum_j \alpha_j \le 3 \cdot \text{LP} \le 3 \cdot \text{OPT}$.

*Proof.* $X$ is not empty, since every client has a witness by Lemma 1, and the first temporarily open facility is always added to $X$. By Lemma 5,

$$C + 3F = \sum_{j \text{ direct}} \big( c_{\sigma(j) j} + 3 \beta_{\phi(j) j} \big) + \sum_{j \text{ not direct}} c_{\sigma(j) j} \le 3 \sum_j \alpha_j,$$

by Lemma 6. The dual is feasible: $\alpha_j - \beta_{ij} \le c_{ij}$ by the choice of $\beta$, $\beta \ge 0$, and $\sum_j \beta_{ij} \le f_i$ by Lemma 2. Weak duality gives $\sum_j \alpha_j \le \text{LP}$, and each integral solution is a point of the LP, so $\text{LP} \le \text{OPT}$. $\blacksquare$

**Remark (why the factor 3 on F matters).** For k-median, give every facility cost $z$. A solution with $k'$ facilities then has $C \le 3(\sum_j \alpha_j - k' z)$, and $\sum_j \alpha_j - k z$ is a lower bound on the k-median optimum with $k$ facilities, by Lagrangian duality. Jain and Vazirani combine two such solutions with $k_1 > k > k_2$ facilities and round the combination with a loss of factor 2, which gives ratio 6. That step is not proved here.
