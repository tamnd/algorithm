---
title: Peeling returns the likelihood of a loop-free pedigree
proves: [correctness]
status: full
---

Let a pedigree have the individuals $I$. Each individual $i$ is a founder or has a father $f_i$ and a mother $m_i$ in $I$. The individuals with the same two parents form a nuclear family $F = (f, m; C_F)$, where $C_F$ is the set of children. Genotypes are the numbers $1, \ldots, G$. The model gives a founder prior $\pi(g)$, a transmission table $T(g \mid a, b)$ and a penetrance $\text{pen}_i(g)$ for each individual (equal to 1 for every $g$ when $i$ has no data). For an assignment $\gamma : I \to [G]$ of genotypes, put

$$\Phi(\gamma) = \prod_{i \text{ founder}} \pi(\gamma_i) \prod_{F} \prod_{c \in C_F} T(\gamma_c \mid \gamma_f, \gamma_m) \prod_{i \in I} \text{pen}_i(\gamma_i).$$

The likelihood is $L = \sum_\gamma \Phi(\gamma)$, a sum of $G^{|I|}$ terms. The proof uses only the distributive law, so it holds for any non-negative or real tables.

**The graph.** $H$ is the bipartite graph whose nodes are the individuals and the families, with an edge between a family and each of its members (both parents and all children). Each factor of $\Phi$ is *owned* by one node: an individual $i$ owns $\pi(\gamma_i)$ (if it is a founder) and $\text{pen}_i(\gamma_i)$, and a family $F$ owns the factors $T(\gamma_c \mid \gamma_f, \gamma_m)$ of its children. A factor owned by $F$ involves only members of $F$, which are the neighbours of $F$ in $H$.

**Lemma 1 (the check of line L1).** A graph with $N$ nodes, $E$ edges and $K$ connected components is a forest if and only if $E = N - K$.

*Proof.* A spanning forest of the graph, one spanning tree for each component, has $N - K$ edges. Every edge of the graph outside this forest closes a cycle with it, so the graph is a forest exactly when it has no such edge. $\square$

So line L1 fails exactly when $H$ has a cycle. Such a cycle is a marriage loop or an inbreeding loop. From now on $H$ is a forest. Line L2 roots each component at an individual. The preorder lists each node after its parent in the forest, so the reverse preorder of line L3 reaches every child of a node before the node.

**Partial sums.** For a node $v$, let $H_v$ be its subtree, $\Phi_v$ the product of the factors owned by the nodes of $H_v$, and $U_v$ the individuals of $H_v$ other than the individual that the definition fixes. For an individual $i$, define

$$W_i(g) = \sum_{\gamma \text{ on } U_i} \Phi_i(\gamma) \quad \text{with } \gamma_i = g,$$

where $U_i$ is the set of individuals of $H_i$ other than $i$. For a family $F$ whose parent in the forest is the individual $p$, define

$$M_F(g) = \sum_{\gamma \text{ on } U_F} \Phi_F(\gamma) \quad \text{with } \gamma_p = g,$$

where $U_F$ is the set of individuals of $H_F$. Note that $p \notin H_F$, but the factors owned by $F$ involve $\gamma_p$, so $M_F$ is a function of $g$.

**Claim.** A factor owned by a node of $H_v$ involves only individuals of $H_v$ and the parent of $v$ in the forest.

*Proof.* An individual owns factors in its own genotype only. A family $F$ in $H_v$ owns factors in its neighbours, which are its parent in the forest and its children in the forest. Its children are in $H_v$. Its parent is in $H_v$ too, unless $F = v$, and then the parent is the parent of $v$. $\square$

**Lemma 2.** When line L3 has processed a node, $w_i = W_i$ for an individual $i$, and $M_F$ in the code is the $M_F$ above for a family $F$.

*Proof.* By induction in the reverse preorder.

*Individual $i$ (lines L4 and L5).* The children of $i$ in the forest are the families $F_1, \ldots, F_d$ in which $i$ is a member but which are not the parent of $i$. The subtrees $H_{F_1}, \ldots, H_{F_d}$ are disjoint, and $U_i$ is the disjoint union of the sets $U_{F_t}$. The factors of $\Phi_i$ are those that $i$ owns and those of $\Phi_{F_1}, \ldots, \Phi_{F_d}$. By the claim, the factors of $\Phi_{F_t}$ involve only $U_{F_t}$ and $i$. With $\gamma_i = g$ fixed, the sum over $U_i$ is a sum over independent choices on each $U_{F_t}$ of a product of factors that each depend on one choice. By the distributive law it is the product of the separate sums:

$$W_i(g) = \text{pen}_i(g) \, \pi(g)^{[i \text{ founder}]} \prod_{t=1}^{d} M_{F_t}(g).$$

By the induction hypothesis these $M_{F_t}$ are the vectors that the code holds, so lines L4 and L5 compute $W_i$.

*Family $F = (f, m; C_F)$ with parent $p$ in the forest (lines L6 to L9).* The children of $F$ in the forest are its members other than $p$. Their subtrees are disjoint, $U_F$ is their disjoint union, and the factors of $\Phi_F$ are the $T$ factors that $F$ owns together with the factors of $\Phi_x$ for each member $x \neq p$. For a child $c \neq p$ of the family and parent genotypes $a, b$, line L7 computes

$$S_c(a, b) = \sum_{g} T(g \mid a, b) \, W_c(g),$$

which is the sum over the genotype of $c$ and over $U_c$ of the factors that involve $c$ or $U_c$, with the parents fixed at $(a, b)$.

If $p$ is a parent, say $p = f$, fix $\gamma_f = g$. The free variables are $\gamma_m$, the genotypes of the children and the sets $U_m$ and $U_c$. For a fixed $\gamma_m = b$, the remaining sum splits over the children, so

$$M_F(g) = \sum_{b} W_m(b) \prod_{c \in C_F} S_c(g, b),$$

which is line L8. The case $p = m$ is the same with the roles swapped.

If $p$ is a child, fix $\gamma_p = g$. The free variables are $\gamma_f$, $\gamma_m$, the genotypes of the other children and the sets below them. The factor $T(g \mid a, b)$ of $p$ stays, and for fixed $(a, b)$ the rest splits:

$$M_F(g) = \sum_{a, b} W_f(a) \, W_m(b) \, T(g \mid a, b) \prod_{c \in C_F, \, c \neq p} S_c(a, b),$$

which is line L9. In both cases the induction hypothesis gives the $W$ vectors that the code uses. $\square$

**Theorem.** PEEL returns $L$.

*Proof.* Let the components of $H$ have the roots $r_1, \ldots, r_K$. Every factor of $\Phi$ is owned by exactly one node, and every node is in one component, so $\Phi(\gamma) = \prod_k \Phi_{r_k}(\gamma)$. By the claim, and because a root has no parent, $\Phi_{r_k}$ involves only the individuals of the component of $r_k$. The individuals of $I$ are partitioned by the components. By the distributive law,

$$L = \sum_\gamma \prod_{k} \Phi_{r_k}(\gamma) = \prod_{k} \sum_{g} W_{r_k}(g),$$

and by Lemma 2 this is the value of line L10. $\square$

**Posterior genotypes.** Replacing $\text{pen}_i$ by $\text{pen}_i(h) [h = g]$ keeps only the terms of $L$ with $\gamma_i = g$. So the result of PEEL with this change, divided by $L$, is $\Pr(\gamma_i = g \mid \text{data})$. This is what genotype_posterior computes.
