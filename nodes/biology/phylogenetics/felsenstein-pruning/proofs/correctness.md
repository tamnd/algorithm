---
title: The pruning algorithm returns the likelihood of the tree
proves: [correctness]
status: full
---

Let $T$ be a rooted tree with root $\rho$, let each non-root node $w$ have a $k \times k$ matrix $P_w$ with real entries, and let $\pi$ be a vector of length $k$. Each leaf $\ell$ has either a known state $x_\ell$ or the mark unknown. Write $T_v$ for the subtree of a node $v$, $E(T_v)$ for its edges, and $I_v$ for the set of nodes of $T_v$ other than $v$ that are internal nodes or leaves with an unknown state. These are the nodes whose state is summed over. For a node $v$ and a state $a$, an *assignment below* $v$ is a map $\sigma : I_v \to \{1, \ldots, k\}$. Together with $a$ at $v$ and the known leaf states, it gives a state $\sigma(u)$ to every node $u$ of $T_v$. Define

$$S_v(a) = \sum_{\sigma : I_v \to [k]} \; \prod_{(u, w) \in E(T_v)} P_w(\sigma(u), \sigma(w)),$$

where $\sigma(v) = a$. If $v$ is a leaf with a known state $x_v$, then $T_v$ has no edges and $I_v$ is empty, but the state of $v$ is fixed, so we set $S_v(a) = [a = x_v]$. If $v$ is a leaf with an unknown state, $S_v(a) = 1$ for every $a$.

The likelihood of the site is the sum of the definition,

$$L = \sum_{\sigma} \pi_{\sigma(\rho)} \prod_{(u, w) \in E(T)} P_w(\sigma(u), \sigma(w)),$$

over all maps $\sigma$ from the internal nodes and the unknown leaves to $[k]$.

**Lemma 1.** After line L5 has run for $v$, $L_v(a) = S_v(a)$ for every state $a$.

*Proof.* By induction in the postorder of line L1, which reaches every child of $v$ before $v$.

*Leaf.* Lines L2 and L3 set $L_v$ to $[a = x_v]$ for a known state and to 1 for an unknown state, which is $S_v(a)$ by definition.

*Internal node.* Let $v$ have the children $w_1, \ldots, w_d$, for which the claim holds. The edges of $T_v$ are the $d$ edges $(v, w_j)$ together with the edges of the subtrees $T_{w_j}$, and the subtrees are disjoint. So, with $v$ in state $a$, an assignment below $v$ is the same as a choice, for each $j$, of a state $b_j$ for $w_j$ (if $w_j$ is in $I_v$; otherwise $b_j = x_{w_j}$ is fixed) and an assignment $\sigma_j$ below $w_j$. The product over the edges of $T_v$ splits into $d$ factors,

$$\prod_{(u, w) \in E(T_v)} P_w(\sigma(u), \sigma(w)) = \prod_{j=1}^{d} \Bigl( P_{w_j}(a, b_j) \prod_{(u, w) \in E(T_{w_j})} P_w(\sigma_j(u), \sigma_j(w)) \Bigr),$$

and factor $j$ depends only on $b_j$ and $\sigma_j$. A sum over independent choices of a product of factors that each depend on one choice is the product of the separate sums (the distributive law). So

$$S_v(a) = \prod_{j=1}^{d} \; \sum_{b_j} \; \sum_{\sigma_j} P_{w_j}(a, b_j) \prod_{(u, w) \in E(T_{w_j})} P_w(\sigma_j(u), \sigma_j(w)) = \prod_{j=1}^{d} \; \sum_{b=1}^{k} P_{w_j}(a, b)\, S_{w_j}(b).$$

In the last step, for a child $w_j$ in $I_v$, $b_j$ runs over all states, and the inner sum over $\sigma_j$ is $S_{w_j}(b_j)$. For a leaf child with a known state, only $b_j = x_{w_j}$ occurs, and $S_{w_j}(b) = [b = x_{w_j}]$ makes the sum over all $b$ equal to the single term. By the induction hypothesis $S_{w_j} = L_{w_j}$, so the right side is the value that line L5 stores. $\square$

**Theorem.** PRUNE returns $L$.

*Proof.* Every map $\sigma$ in the definition of $L$ is a state $a = \sigma(\rho)$ at the root together with an assignment below the root. Grouping the terms of $L$ by $a$,

$$L = \sum_{a=1}^{k} \pi_a \sum_{\sigma : I_\rho \to [k]} \prod_{(u, w) \in E(T)} P_w(\sigma(u), \sigma(w)) = \sum_{a=1}^{k} \pi_a\, S_\rho(a),$$

since $T_\rho = T$. By Lemma 1, $S_\rho = L_\rho$, so this is the value of line L6. $\blacksquare$

**Remarks.** The proof uses only that $+$ and $\times$ are commutative, associative and distributive, so the result holds for any matrices and for exact rational arithmetic, which is how the implementation is tested. When each $P_w$ is the transition matrix of a Markov chain on the edge above $w$ and the leaves have known states, $S_v(a)$ is the probability of the leaf states in $T_v$ given state $a$ at $v$, and $L$ is the probability of the site pattern, as in the [phylogenetic likelihood](/phylogenetic-likelihood/).
