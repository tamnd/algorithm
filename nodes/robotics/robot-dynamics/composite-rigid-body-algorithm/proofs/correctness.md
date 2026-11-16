---
title: The composite rigid body algorithm returns the joint-space inertia matrix
proves: [correctness]
status: full
---

We use the notation of the page and of the recursive Newton-Euler algorithm. Body $i$ has the parent $\lambda(i) < i$. For an ancestor $j$ of $i$ (or $j = i$), $X_{i \leftarrow j} = X_i X_{\lambda(i)} \cdots$ is the product of the joint transforms on the path, from $j$ down to $i$, with $X_{i \leftarrow i} = 1$. Write $\mathrm{anc}(i)$ for the set of $i$ and its ancestors and $\nu(i)$ for the set of $i$ and its descendants (the subtree of $i$).

**Lemma 1 (the matrix).** $M(q)$ is the matrix of the linear map $\ddot q \mapsto \tau$ of the inverse dynamics with $\dot q = 0$ and no gravity. Its entries are
$$H_{ij} = S_i^T \Big( \sum_{l \in \nu(i) \cap \nu(j)} X_{l \leftarrow i}^T I_l X_{l \leftarrow j} \Big) S_j .$$

*Proof.* Run the recursive Newton-Euler algorithm with $\dot q = 0$ and $a_0 = 0$. All velocities are 0, so $a_l = X_l a_{\lambda(l)} + S_l\ddot q_l$, and by induction $a_l = \sum_{k \in \mathrm{anc}(l)} X_{l \leftarrow k} S_k \ddot q_k$. The body wrench is $I_l a_l$, and the backward pass adds the wrenches of the subtree, so $f_i = \sum_{l \in \nu(i)} X_{l \leftarrow i}^T I_l a_l$ and $\tau_i = S_i^T f_i$. The coefficient of $\ddot q_j$ in $\tau_i$ collects the bodies $l$ with $l \in \nu(i)$ and $j \in \mathrm{anc}(l)$, that is $l \in \nu(i) \cap \nu(j)$. $\square$

**Corollary 2 (three cases).** Define the composite inertia $I^c_i = \sum_{l \in \nu(i)} X_{l \leftarrow i}^T I_l X_{l \leftarrow i}$.

- If $j \in \mathrm{anc}(i)$, then $\nu(i) \cap \nu(j) = \nu(i)$ and $X_{l \leftarrow j} = X_{l \leftarrow i} X_{i \leftarrow j}$, so $H_{ij} = S_i^T I^c_i X_{i \leftarrow j} S_j$.
- If $i \in \mathrm{anc}(j)$, then by the same argument $H_{ij} = (X_{j \leftarrow i} S_i)^T I^c_j S_j = H_{ji}$.
- Otherwise $i$ and $j$ are not on one path to the base, $\nu(i) \cap \nu(j)$ is empty, and $H_{ij} = 0$. This is branch-induced sparsity.

**Lemma 3 (the recursion of line L3).** $I^c_i = I_i + \sum_{c:\, \lambda(c) = i} X_c^T I^c_c X_c$.

*Proof.* $\nu(i)$ is the disjoint union of $\{i\}$ and the sets $\nu(c)$ of the children $c$. For $l \in \nu(c)$, $X_{l \leftarrow i} = X_{l \leftarrow c} X_c$. $\square$

**Theorem.** Line L10 returns $H = M(q)$.

*Proof.* Line L1 sets $I^c_i = I_i$ for all $i$. The loop of line L2 visits $i = n, \ldots, 1$. We claim that, when the loop reaches $i$, the variable $I^c_i$ holds the composite inertia of Lemma 3. Each child $c$ of $i$ has $c > i$, so line L3 has already added $X_c^T I^c_c X_c$ to $I^c_i$, and by induction $I^c_c$ was complete at that time. No other line changes $I^c_i$.

Line L4 sets $F = I^c_i S_i$, and line L5 sets $H_{ii} = S_i^T F$, which is the first case of Corollary 2 with $j = i$. The loop of lines L7 to L9 climbs the path to the base. We show that after line L8 has moved $j$ to its parent, $F = X_{i \leftarrow j}^T I^c_i S_i$. This holds before the first step with $j = i$. A step replaces $F$ by $X_{j}^T F$ and $j$ by $\lambda(j)$, and $X_{i \leftarrow \lambda(j)} = X_{i \leftarrow j} X_j$, so $X_{i \leftarrow \lambda(j)}^T = X_j^T X_{i \leftarrow j}^T$. Line L9 then sets $H_{ij} = S_j^T F = S_j^T X_{i \leftarrow j}^T I^c_i S_i$, which is the transpose of the scalar $S_i^T I^c_i X_{i \leftarrow j} S_j$ because $I^c_i$ is symmetric. So it is $H_{ij}$ by the first case of Corollary 2, since $j$ is an ancestor of $i$. Line L9 also stores it as $H_{ji}$, which is correct by the second case.

Every pair $(i, j)$ with one on the path of the other is written once in this way, and every other pair keeps its initial value 0, which is correct by the third case. $\blacksquare$

**Kinetic energy and definiteness.** With $v_l = \sum_{k \in \mathrm{anc}(l)} X_{l \leftarrow k} S_k \dot q_k$, Lemma 1 gives $\dot q^T H \dot q = \sum_l v_l^T I_l v_l$, which is twice the kinetic energy. If every $I_l$ is positive definite, the sum is 0 only when every $v_l = 0$. Then $S_i \dot q_i = v_i - X_i v_{\lambda(i)} = 0$ for every $i$, so $\dot q = 0$ because $S_i \ne 0$. So $H$ is symmetric positive definite.

**Cost.** Line L3 costs a fixed number of $6 \times 6$ products per body, and the climb from body $i$ costs one transform per ancestor. The total is $\Theta(n + \sum_i \mathrm{depth}(i))$, which is $O(n d)$ for a tree of depth $d$ and $\Theta(n^2)$ for a serial chain.
