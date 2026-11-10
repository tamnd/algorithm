---
title: Filtering and clustering cost at most F/α + 3C/(1 - α), and the best level costs at most 3/(1 - e^-3) times the LP
proves: [correctness]
status: full
---

**Setting.** Facilities $i$ have costs $f_i \ge 0$, clients $j$ have costs $c_{ij} \ge 0$, and $c$ extends to a metric on facilities and clients. Let $(x, y)$ be a feasible LP solution: $\sum_i x_{ij} = 1$, $0 \le x_{ij} \le y_i$. Write $F_{\text{LP}} = \sum_i f_i y_i$, $C_j = \sum_i c_{ij} x_{ij}$ and $C_{\text{LP}} = \sum_j C_j$. For $\alpha \in (0, 1]$, let $g_j(\alpha) = \min \{ g : \sum_{i : c_{ij} \le g} x_{ij} \ge \alpha \}$ and $N_j = \{ i : x_{ij} > 0, c_{ij} \le g_j(\alpha) \}$. The minimum exists, because the sum is a step function of $g$ that is continuous from the right and reaches $1 \ge \alpha$.

**Lemma 1 (near sets).** For each client $j$, $\sum_{i \in N_j} x_{ij} \ge \alpha$ and $\sum_{i : c_{ij} < g_j(\alpha)} x_{ij} < \alpha$. So the facilities at distance at least $g_j(\alpha)$ hold more than $1 - \alpha$ of client $j$.

*Proof.* The first claim is the definition of $g_j(\alpha)$, since the facilities with $x_{ij} = 0$ add nothing. If $\sum_{i : c_{ij} < g_j(\alpha)} x_{ij} \ge \alpha$, then the largest distance $g' < g_j(\alpha)$ with $x_{ij} > 0$ among these facilities would satisfy the condition, and it is smaller than $g_j(\alpha)$, a contradiction; if there is no such facility, the sum is 0, which is less than $\alpha$. So $\sum_{i : c_{ij} < g_j(\alpha)} x_{ij} < \alpha$, and the facilities at distance at least $g_j(\alpha)$ hold more than $1 - \alpha$. $\square$

**Lemma 2 (Markov).** For each client $j$ and each $\alpha \in (0, 1)$, $g_j(\alpha) \le C_j / (1 - \alpha)$.

*Proof.* By Lemma 1, $C_j \ge \sum_{i : c_{ij} \ge g_j(\alpha)} c_{ij} x_{ij} \ge g_j(\alpha) \sum_{i : c_{ij} \ge g_j(\alpha)} x_{ij} \ge g_j(\alpha) (1 - \alpha)$. $\square$

**Lemma 3 (the clustering).** Fix $\alpha$ and run lines L4 to L7. Let $j_1, j_2, \ldots, j_q$ be the centers in order and $i_1, \ldots, i_q$ the opened facilities. Then the sets $N_{j_1}, \ldots, N_{j_q}$ are pairwise disjoint, each client is connected to exactly one opened facility, and if client $k$ is connected to $i_s$, then $N_k \cap N_{j_s} \ne \emptyset$ and $g_{j_s} \le g_k$.

*Proof.* Each $N_j$ is nonempty by Lemma 1. When $j_s$ is chosen, line L7 removes every client of $U$ whose near set meets $N_{j_s}$, including $j_s$. A later center $j_{s'}$ was still in $U$, so $N_{j_{s'}} \cap N_{j_s} = \emptyset$. Each client is removed exactly once, at the step where it is connected. If $k$ is connected to $i_s$, then $k$ was in $U$ when $j_s$ was chosen, so $g_{j_s} \le g_k$ by line L5, and $N_k$ meets $N_{j_s}$ by line L7. $\square$

**Lemma 4 (one level).** For each $\alpha \in (0, 1)$, the solution of lines L3 to L7 has facility cost at most $F_{\text{LP}} / \alpha$ and connection cost at most $3 \sum_j g_j(\alpha) \le 3 C_{\text{LP}} / (1 - \alpha)$.

*Proof.* Facility cost: $i_s$ is the cheapest facility of $N_{j_s}$, so, using $y_i \ge x_{i j_s}$ and Lemma 1,

$$f_{i_s} \le \frac{\sum_{i \in N_{j_s}} f_i y_i}{\sum_{i \in N_{j_s}} y_i} \le \frac{1}{\alpha} \sum_{i \in N_{j_s}} f_i y_i.$$

The sets $N_{j_s}$ are disjoint by Lemma 3, so the sum over $s$ is at most $\frac{1}{\alpha} \sum_i f_i y_i = F_{\text{LP}} / \alpha$. Connection cost: if $k$ is connected to $i_s$, take $h \in N_k \cap N_{j_s}$ by Lemma 3. Then $c_{hk} \le g_k$, $c_{h j_s} \le g_{j_s}$ and $c_{i_s j_s} \le g_{j_s}$, since $h$ and $i_s$ lie in the near sets. By the triangle inequality and $g_{j_s} \le g_k$,

$$c_{i_s k} \le c_{hk} + c_{h j_s} + c_{i_s j_s} \le g_k + 2 g_{j_s} \le 3 g_k.$$

Summing over $k$ and using Lemma 2 gives the bound. $\square$

**Lemma 5 (the quantile integral).** For each client $j$, $\int_0^1 g_j(\alpha) \, d\alpha = C_j$.

*Proof.* Sort the facilities with $x_{ij} > 0$ by distance as $i_1, \ldots, i_p$, with $c_{i_1 j} \le \cdots \le c_{i_p j}$, and let $a_0 = 0$ and $a_t = a_{t-1} + x_{i_t j}$, so $a_p = 1$. For $\alpha \in (a_{t-1}, a_t]$, the least ball holding $\alpha$ is reached at $i_t$, possibly at an earlier facility with the same distance, so $g_j(\alpha) = c_{i_t j}$. So $\int_0^1 g_j = \sum_t (a_t - a_{t-1}) c_{i_t j} = \sum_t x_{i_t j} c_{i_t j} = C_j$. $\square$

**Theorem.** The algorithm returns a solution of cost at most $\frac{3}{1 - e^{-3}} (F_{\text{LP}} + C_{\text{LP}})$. With an optimal LP solution, this is at most $\frac{3}{1 - e^{-3}} \, \text{OPT} < 3.1573 \, \text{OPT}$. With the single level $\alpha = 1/4$, the cost is at most $4 (F_{\text{LP}} + C_{\text{LP}})$.

*Proof.* Let $\text{cost}(\alpha)$ be the cost of the solution for level $\alpha$. By Lemma 4, $\text{cost}(\alpha) \le F_{\text{LP}} / \alpha + 3 \sum_j g_j(\alpha)$ for each $\alpha \in (0, 1)$; at $\alpha = 1/4$ this with Lemma 2 gives $4 F_{\text{LP}} + 4 C_{\text{LP}}$. Let $\beta = e^{-3}$ and average over $\alpha$ uniform on $(\beta, 1)$:

$$\frac{1}{1 - \beta} \int_\beta^1 \frac{d\alpha}{\alpha} = \frac{\ln(1/\beta)}{1 - \beta} = \frac{3}{1 - e^{-3}}, \qquad \frac{3}{1 - \beta} \int_\beta^1 g_j(\alpha) \, d\alpha \le \frac{3}{1 - \beta} \int_0^1 g_j(\alpha) \, d\alpha = \frac{3 C_j}{1 - e^{-3}},$$

using $g_j \ge 0$ and Lemma 5. So the average of the bound over $(\beta, 1)$ is at most $\frac{3}{1 - e^{-3}} (F_{\text{LP}} + C_{\text{LP}})$, and some $\alpha^* \in (\beta, 1)$ has $\text{cost}(\alpha^*)$ at most this, since $\text{cost}(\alpha)$ is at most the bound for each $\alpha$ and a function cannot be above its average everywhere. ($\text{cost}$ is a step function with finitely many pieces, so it is integrable.)

It remains to show that line L2 tries a level with the same solution as $\alpha^*$. By the proof of Lemma 5, each $g_j$ is constant on each interval $(a_{t-1}, a_t]$ of its own breakpoints. Let $b_0 = 0 < b_1 < \cdots < b_r = 1$ be all breakpoints of all clients. On each interval $(b_{u-1}, b_u]$, all $g_j$ are constant, so all $N_j$ are constant, and lines L3 to L7 make the same choices, since they depend only on the $g_j$, the $N_j$, the costs and fixed tie-breaking. So $\text{cost}(\alpha^*) = \text{cost}(b_u)$ for the $b_u$ with $\alpha^* \in (b_{u-1}, b_u]$, and line L2 tries $b_u$. The kept solution costs at most $\text{cost}(b_u)$. Finally, $F_{\text{LP}} + C_{\text{LP}} = \text{LP} \le \text{OPT}$ for an optimal LP solution, since every solution gives a 0-1 point of the LP, and $3 / (1 - e^{-3}) = 3.15719\ldots$ $\blacksquare$
