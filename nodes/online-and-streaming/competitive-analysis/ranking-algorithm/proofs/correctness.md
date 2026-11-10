---
title: Ranking is a valid online matching rule and is (1 - 1/e)-competitive against an oblivious adversary
proves: [correctness]
status: full
---

The proof follows the randomized primal-dual analysis of Devanur, Jain and Kleinberg (2013). We use the pseudocode of the page with a continuous form of the random order: each offline vertex $u \in U$ draws $y_u$ uniform in $[0, 1]$, independently, and the rank of $u$ is its position when $U$ is sorted by $y$. Ties have probability 0, and the sorted order is a uniform random permutation, so this is the same algorithm as line L1. The graph $G = (U \cup V, E)$ and the arrival order of $V$ are fixed by an oblivious adversary before the $y_u$ are drawn. $M$ is the output of Ranking and $M^*$ is a maximum matching of $G$.

**Claim 0 (validity).** $M$ is a matching of $G$, each decision uses only the past, and the free set $F$ is the set of offline vertices not covered by $M$.

*Proof.* Ranking is the greedy rule of [greedy online matching](/greedy-online-matching/) with CHOOSE = "smallest rank". The order is drawn at line L1 before any arrival, and line L7 reads only $N(v_t)$, $F$ and the ranks. The induction of that page applies without change. $\square$

**Split of each edge.** Let $g(y) = e^{y-1}$ and $F_e = 1 - 1/e$. The function $g$ is increasing with $g(0) = 1/e$ and $g(1) = 1$. When Ranking matches $v$ to $u$, set

$$\alpha_u = \frac{g(y_u)}{F_e}, \qquad \beta_v = \frac{1 - g(y_u)}{F_e}.$$

All other $\alpha$ and $\beta$ are 0. Each matched edge adds exactly $1/F_e$ to $\sum_u \alpha_u + \sum_v \beta_v$, so

$$\lvert M \rvert = F_e \Big( \sum_{u \in U} \alpha_u + \sum_{v \in V} \beta_v \Big), \qquad \alpha, \beta \ge 0. \tag{1}$$

Fix an edge $(u, v) \in E$ and fix the values $y_{-u}$ of all offline vertices other than $u$. Run Ranking on $G - u$ with the same values $y_{-u}$ and the same arrivals. Let $y^c$ be the value $y_x$ of the partner $x$ of $v$ in this run, or $y^c = 1$ if $v$ is unmatched in it. The value $y^c$ does not depend on $y_u$.

**Claim 1 (free sets).** Let $F_t$ and $F'_t$ be the free offline sets after $t$ arrivals in the run on $G - u$ and in the run on $G$, with the same $y$ values. Then for each $t$, either $F'_t = F_t$, or $F'_t = F_t \cup \{z_t\}$ for one vertex $z_t \notin F_t$.

*Proof.* By induction on $t$. At $t = 0$, $F'_0 = F_0 \cup \{u\}$. Let $w$ be arrival $t$.

- If $F'_{t-1} = F_{t-1}$, then $u \notin F'_{t-1}$, so both runs see the same free neighbours of $w$ and take the same vertex or none. So $F'_t = F_t$.
- If $F'_{t-1} = F_{t-1} \cup \{z\}$, let $x$ be the choice of the run on $G - u$ (the free neighbour of $w$ in $F_{t-1}$ with the smallest $y$), or none. The run on $G$ picks from $N(w) \cap (F_{t-1} \cup \{z\})$. If it does not pick $z$, it picks $x$ (or none, when $x$ is none), and $F'_t = F_t \cup \{z\}$. If it picks $z$ and $x$ exists, then $F'_t = F_{t-1} = F_t \cup \{x\}$. If it picks $z$ and $x$ is none, then $F'_t = F_{t-1} = F_t$. $\square$

**Claim 2.** If $y_u < y^c$, then $u$ is matched in the run on $G$.

*Proof.* Suppose that $u$ is never matched in the run on $G$. Then at each step the run on $G$ does not pick $u$, so it picks the free neighbour of smallest $y$ among the vertices other than $u$. By induction on $t$, the two runs then make the same choices: they start with the same free sets apart from $u$, and each step picks the same vertex from the same set. So when $v$ arrives, the run on $G$ has the same free neighbours as the run on $G - u$, and also $u$, which is free and adjacent to $v$. If $v$ is matched to $x$ in the run on $G - u$, then $y_u < y^c = y_x$, so the run on $G$ picks $u$ or a vertex of $y$ less than $y_u$, and not $x$; this is a contradiction. If $v$ is unmatched in the run on $G - u$, the run on $G$ still has the free neighbour $u$, so it matches $v$, again a contradiction. $\square$

**Claim 3.** For every value of $y_u$, $\beta_v \ge (1 - g(y^c))/F_e$.

*Proof.* If $y^c = 1$, the right side is 0 and $\beta_v \ge 0$. Otherwise $v$ is matched to $x$ with $y_x = y^c$ in the run on $G - u$, so $x \in F_{s-1}$, where $s$ is the step at which $v$ arrives. By Claim 1, $F_{s-1} \subseteq F'_{s-1}$, so $x$ is a free neighbour of $v$ also in the run on $G$. So $v$ is matched in the run on $G$ to a vertex $x'$ with $y_{x'} \le y_x = y^c$. Since $g$ is increasing, $\beta_v = (1 - g(y_{x'}))/F_e \ge (1 - g(y^c))/F_e$. $\square$

**Claim 4.** For each edge $(u, v) \in E$, $\mathbb{E}[\alpha_u + \beta_v] \ge 1$.

*Proof.* Condition on $y_{-u}$, so $y^c$ is fixed, and take the expectation over $y_u$ alone. If $y_u < y^c$, then $u$ is matched (Claim 2), and $\alpha_u = g(y_u)/F_e$. So

$$\mathbb{E}[\alpha_u \mid y_{-u}] \ge \frac{1}{F_e} \int_0^{y^c} e^{y-1} \, dy = \frac{e^{y^c - 1} - e^{-1}}{F_e}.$$

By Claim 3, $\mathbb{E}[\beta_v \mid y_{-u}] \ge (1 - e^{y^c - 1})/F_e$. Adding the two,

$$\mathbb{E}[\alpha_u + \beta_v \mid y_{-u}] \ge \frac{1 - e^{-1}}{F_e} = 1.$$

Take the expectation over $y_{-u}$. $\square$

**Theorem.** For every bipartite graph and every arrival order, $\mathbb{E}\lvert M \rvert \ge (1 - 1/e) \lvert M^* \rvert$.

*Proof.* The edges of $M^*$ are disjoint, so each $\alpha_u$ and each $\beta_v$ appears at most once in $\sum_{(u,v) \in M^*} (\alpha_u + \beta_v)$, and all terms are non-negative. By (1) and Claim 4,

$$\mathbb{E}\lvert M \rvert = F_e \, \mathbb{E}\Big[ \sum_u \alpha_u + \sum_v \beta_v \Big] \ge F_e \sum_{(u,v) \in M^*} \mathbb{E}[\alpha_u + \beta_v] \ge F_e \lvert M^* \rvert. \qquad \blacksquare$$

**Remarks.**

- The proof is a randomized primal-dual argument. Claim 4 says that $(\alpha, \beta)$ is feasible in expectation for the dual of the bipartite matching LP (cover each edge), and (1) says that the primal value is $F_e$ times the dual value. [Weak duality](/weak-duality/) then gives the bound. The proof above avoids the LP by summing only over the edges of $M^*$.
- The function $g$ is chosen so that $\int_0^{\theta} g + (1 - g(\theta))$ is the same for every threshold $\theta$, which needs $g' = g$, and the constant is $1 - g(0)$; with $g(1) = 1$ this gives $g(y) = e^{y-1}$ and $F_e = 1 - 1/e$.
- The bound is tight: the upper triangular instance on the [online bipartite matching](/online-bipartite-matching/) page holds every randomized algorithm to $1 - 1/e + O(1/n)$.
