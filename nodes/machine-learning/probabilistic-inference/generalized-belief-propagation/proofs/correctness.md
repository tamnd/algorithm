---
title: GBP fixed points are consistent, the CVM is valid, and GBP is exact on junction trees
proves: [correctness]
status: full
---

We use the region graph, the sets $M(R)$, $N(P, R)$, $D(P, R)$, the message update and the pseudocode of the page. All factors are positive. The outer regions are taken to be maximal (none contains another). For a region $R$, $f_R = \prod_{a \in A_R} f_a$, and $E(R)$ is $R$ with its descendants. In the CVM region graph the edges form the Hasse diagram of inclusion, so $E(R)$ is the set of regions contained in $R$; in particular $E(R) \subseteq E(P)$ when $R$ is a child of $P$.

**Lemma 1 (damping).** For $0 \le \lambda < 1$, the damped update has the same fixed points as the undamped one. The proof is that of the loopy belief propagation page: if $m = \mathrm{normalize}((1 - \lambda) m' + \lambda m)$ with $m'$ and $m$ normalized, then $m' = m$.

**Lemma 2 (validity of the CVM).** Let $S$ be a nonempty set of variables that lies in some region. Then $\sum_{R \supseteq S} c_R = 1$. In particular each variable and each factor is counted once in total.

*Proof.* Let $R_0$ be the intersection of all regions that contain $S$. It is a region, because the set is closed under intersection, and it contains $S$. A region contains $S$ if and only if it contains $R_0$ (one direction because $R_0 \supseteq S$, the other because $R_0$ is the intersection of all such regions). So $\sum_{R \supseteq S} c_R = c_{R_0} + \sum_{R \supsetneq R_0} c_R = 1$, by the definition of $c_{R_0}$. For a variable, take $S = \{i\}$; for a factor, take $S$ its scope, which lies in some outer region by assumption. $\square$

**Lemma 3 (consistency at fixed points).** At a fixed point, $\sum_{x_{P \setminus R}} b_P(x_P) = b_R(x_R)$ for every edge $(P, R)$.

*Proof.* We first split the sets of messages. Let $(I, J) \in M(P)$, so $J \in E(P)$ and $I \notin E(P)$. If $J \in E(R)$, then $I \notin E(R)$ as $E(R) \subseteq E(P)$, so $(I, J) \in M(R)$. If $J \notin E(R)$, then $(I, J) \in N(P, R)$ by definition. So $M(P)$ is the disjoint union of $C = \{(I, J) : J \in E(R), I \notin E(P)\}$ and $N(P, R)$. In the same way, an edge $(I, J) \in M(R)$ has $J \in E(R)$ and $I \notin E(R)$, and either $I \notin E(P)$, which puts it in $C$, or $I \in E(P) \setminus E(R)$, which puts it in $D(P, R)$ or makes it $(P, R)$. So $M(R)$ is the disjoint union of $C$, $D(P, R)$ and $\{(P, R)\}$.

Every message on an edge $(I, J)$ with $J \in E(R)$ is a function of $x_J$, and $J \subseteq R$. Also $A_R \subseteq A_P$, so $f_P = f_R \prod_{a \in A_P \setminus A_R} f_a$. Hence

$$\sum_{x_{P \setminus R}} f_P \prod_{M(P)} m = f_R(x_R) \prod_{C} m \cdot \sum_{x_{P \setminus R}} \prod_{a \in A_P \setminus A_R} f_a \prod_{N(P, R)} m.$$

At a fixed point the last sum is a positive constant times $m_{P \to R}(x_R) \prod_{D(P, R)} m(x_R)$, by the message rule. So the left side is a constant times $f_R \prod_{C} m \cdot m_{P \to R} \prod_{D(P, R)} m = f_R \prod_{M(R)} m$, which is the unnormalized $b_R$. Both $b_P$ and $b_R$ sum to 1, so the marginal of $b_P$ is $b_R$. $\square$

**Lemma 4 (the free energy of a junction tree).** If the true distribution factors as $p(x) = \prod_R p_R(x_R)^{c_R}$, where $p_R$ is the true marginal of $R$, then $F_K(\{p_R\}) = -\log Z$.

*Proof.* Write $F_K = \sum_R c_R \sum_{x_R} p_R \log p_R - \sum_R c_R \sum_{x_R} p_R \log f_R$. Each inner sum is an expected value under $p$, because $p_R$ is the marginal of $p$. The first part is $\mathbb{E}_p[\sum_R c_R \log p_R(x_R)] = \mathbb{E}_p[\log p(x)]$ by the assumption. The second part is $\sum_R c_R \sum_{a \in A_R} \mathbb{E}_p[\log f_a] = \sum_a \mathbb{E}_p[\log f_a] \sum_{R : a \in A_R} c_R = \sum_a \mathbb{E}_p[\log f_a]$, by Lemma 2. So $F_K = \mathbb{E}_p[\log p(x) - \sum_a \log f_a(x_a)] = \mathbb{E}_p[-\log Z] = -\log Z$. $\square$

**Theorem (two outer regions).** Let the outer regions be $C_1$ and $C_2$, with $S = C_1 \cap C_2 \ne \emptyset$, and let every factor lie in $C_1$ or in $C_2$. Then GBP converges for every $\lambda \in [0, 1)$, its beliefs at the limit are the exact marginals, and $-F_K$ there is $\log Z$.

*Proof.* The regions are $C_1$, $C_2$, $S$, with $c_S = 1 - 2 = -1$, and the edges are $(C_1, S)$ and $(C_2, S)$. No edge enters $C_1$, so $N(C_1, S) = \emptyset$, and $D(C_1, S)$ would need an edge into $S$ from $E(C_1) \setminus E(S) = \{C_1\}$ other than $(C_1, S)$, so it is empty too. So

$$m_{C_1 \to S}(x_S) \propto \sum_{x_{C_1 \setminus S}} \prod_{a \in A_{C_1} \setminus A_S} f_a(x_a),$$

which does not depend on any message; the same holds for $C_2$. With damping $\lambda$, both the old message and the new one sum to 1, so the normalization does nothing, and the distance of each message to this value is multiplied by $\lambda$ in each sweep. So the iteration converges to the fixed point.

The belief of $C_1$ is $b_{C_1} \propto f_{C_1}\, m_{C_2 \to S}$. Now $p(x_{C_1}) \propto \sum_{x_{C_2 \setminus S}} \prod_a f_a$. A factor not in $A_{C_1}$ lies in $C_2$ and not in $S$, so it is in $A_{C_2} \setminus A_S$; a factor in both $A_{C_1}$ and $A_{C_2}$ lies in $S$. Since $C_2 \setminus S$ does not meet $C_1$, the factors of $A_{C_1}$ come out of the sum, and $p(x_{C_1}) \propto f_{C_1} \sum_{x_{C_2 \setminus S}} \prod_{a \in A_{C_2} \setminus A_S} f_a \propto b_{C_1}$. The same holds for $C_2$, and $b_S$ is the marginal of $b_{C_1}$ by Lemma 3, so it is exact too.

Finally, given $x_S$, the variables of $C_1 \setminus S$ and $C_2 \setminus S$ are independent, because every factor lies inside $C_1$ or inside $C_2$. So $p = p_{C_1} p_{C_2} / p_S = \prod_R p_R^{c_R}$, and Lemma 4 gives $-F_K = \log Z$. $\blacksquare$

**Remark.** The general statement that the fixed points of the parent-to-child algorithm are the stationary points of $F_K$ under the consistency constraints is due to Yedidia, Freeman and Weiss (2005); its proof follows the Lagrangian argument of the loopy belief propagation page, with one multiplier per consistency constraint. Nothing here says that GBP converges on a graph with cycles, or that it is more accurate than loopy BP; the comparison on the page is an observation.
