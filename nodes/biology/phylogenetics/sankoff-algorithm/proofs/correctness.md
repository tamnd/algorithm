---
title: The Sankoff algorithm returns a labeling of least total cost
proves: [correctness]
status: full
---

Let $T$ be a rooted tree with leaf states $x$, and let $\delta : \Sigma \times \Sigma \to \mathbb{R}_{\ge 0} \cup \{\infty\}$. For a node $v$, write $T_v$ for its subtree. A labeling of $T_v$ is a map from the nodes of $T_v$ to $\Sigma$ that agrees with $x$ at the leaves, and its cost is the sum of $\delta(\lambda(u), \lambda(w))$ over the edges $(u, w)$ of $T_v$, with $u$ the parent. For a state $a$, let $\operatorname{OPT}_v(a)$ be the least cost of a labeling of $T_v$ with $\lambda(v) = a$, and $\infty$ if there is none. The sums use $c + \infty = \infty$.

**Lemma 1 (the tables).** After lines L1 to L4, $C_v(a) = \operatorname{OPT}_v(a)$ for every node $v$ and state $a$.

*Proof.* By induction in the postorder of line L1.

*Leaf.* $T_v$ has no edges, and its only labeling gives $v$ the state $x(v)$. So $\operatorname{OPT}_v(x(v)) = 0$ and $\operatorname{OPT}_v(a) = \infty$ for $a \ne x(v)$, which is line L2.

*Internal node.* Let $v$ have the children $w_1, \ldots, w_d$, for which the claim holds. The edges of $T_v$ are the edges $(v, w_j)$ and the edges of the subtrees $T_{w_j}$, and these subtrees share no node. So a labeling $\lambda$ of $T_v$ with $\lambda(v) = a$ is the same as a choice, for each $j$, of a labeling $\lambda_j$ of $T_{w_j}$, and

$$\operatorname{cost}(\lambda) = \sum_{j = 1}^{d} \bigl(\delta(a, \lambda_j(w_j)) + \operatorname{cost}(\lambda_j)\bigr).$$

The $j$-th term depends on $\lambda_j$ only, so the least value of the sum is the sum of the least values of its terms. For a fixed $b = \lambda_j(w_j)$, the least value of the $j$-th term is $\delta(a, b) + \operatorname{OPT}_{w_j}(b)$. So

$$\operatorname{OPT}_v(a) = \sum_{j = 1}^{d} \min_{b \in \Sigma} \bigl(\delta(a, b) + \operatorname{OPT}_{w_j}(b)\bigr),$$

which by the induction hypothesis is the value that line L4 stores. $\square$

**Lemma 2 (the score).** The value of line L5 is the least cost of a labeling of $T$.

*Proof.* Every labeling gives the root some state $a$, so the least cost is $\min_a \operatorname{OPT}_{\text{root}}(a)$, which is $\min_a C_{\text{root}}(a)$ by Lemma 1. $\square$

**Lemma 3 (the traceback).** Suppose the score is finite. Then the labeling $\lambda$ of lines L6 to L8 agrees with $x$ at the leaves, and for every node $v$, the cost of $\lambda$ on the edges of $T_v$ is $C_v(\lambda(v))$, which is finite.

*Proof.* First, $C_v(\lambda(v))$ is finite for every node $v$, by induction from the root down. At the root, $C_{\text{root}}(\lambda(\text{root}))$ is the score. Let $w$ be a child of $v$ with $C_v(\lambda(v))$ finite. The term of $w$ in line L4 for the state $\lambda(v)$ is a summand of the finite value $C_v(\lambda(v))$, so it is finite, and line L8 picks a state $b$ that reaches this term. So $\delta(\lambda(v), b)$ and $C_w(b)$ are both finite. At a leaf $w$, $C_w(b)$ is finite only for $b = x(w)$, so $\lambda(w) = x(w)$.

Second, the cost. We show by induction from the leaves up that the cost of $\lambda$ on the edges of $T_v$ is $C_v(\lambda(v))$. At a leaf both are 0. Let $v$ have children $w_1, \ldots, w_d$, and let $a = \lambda(v)$. By the choice of line L8, $\delta(a, \lambda(w_j)) + C_{w_j}(\lambda(w_j)) = \min_b (\delta(a, b) + C_{w_j}(b))$. With the induction hypothesis, the cost of $\lambda$ on $T_v$ is

$$\sum_{j = 1}^{d} \bigl(\delta(a, \lambda(w_j)) + C_{w_j}(\lambda(w_j))\bigr) = \sum_{j = 1}^{d} \min_{b} \bigl(\delta(a, b) + C_{w_j}(b)\bigr) = C_v(a). \qquad \square$$

**Theorem.** The Sankoff algorithm returns the least total cost over all labelings of $T$ that agree with $x$ at the leaves. If this cost is finite, the returned labeling agrees with $x$ at the leaves and reaches it.

*Proof.* The first claim is Lemma 2. If the score is finite, Lemma 3 at the root shows that $\lambda$ is a labeling of $T$ of cost $C_{\text{root}}(\lambda(\text{root}))$, and line L6 chose $\lambda(\text{root})$ so that this is the score. $\blacksquare$

**Remark.** The proof uses no property of $\delta$ other than its values in $\mathbb{R}_{\ge 0} \cup \{\infty\}$. Symmetry and the triangle inequality are needed only to show that the root, or a root put inside an edge, does not change the score. Negative costs would also work, since the proof never uses the sign, but they have no meaning as costs of change.
