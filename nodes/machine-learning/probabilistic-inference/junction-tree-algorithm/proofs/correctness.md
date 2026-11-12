---
title: After the collect and distribute passes each clique table is the joint marginal of its clique with the evidence
proves: [correctness]
status: full
---

We use the pseudocode JUNCTION-TREE-ALGORITHM and PASS of the page. Let $\Phi'$ be the factors of the model together with the evidence indicators $\lambda_v(x_v) = [x_v = e_v]$, and let
$$\tilde p(x) = \prod_{f \in \Phi'} f(x)$$
be their product, a function of all the variables $V$. For a Bayesian network, $\tilde p(x) = P(x)$ if $x$ agrees with $e$ and 0 otherwise, so $\sum_{V \setminus C} \tilde p = P(C, e)$ for each set $C$. All the entries are nonnegative.

**Setup.** Line L1 joins each two variables that share a factor. Line L2 gives, by the [junction tree](/junction-tree/) page, a tree on cliques $C_1, \ldots, C_k$ with the running intersection property, and each factor scope is a clique of the graph of line L1, so it lies in some $C_i$. Line L4 puts each factor of $\Phi'$ into exactly one clique. Let $\psi_i$ be the product of the factors put into $C_i$ (1 if none); then $\prod_i \psi_i = \tilde p$. Root the tree at $r$. For a clique $i$, let $T_i$ be the subtree below $i$ (with $i$), $V_i$ the variables of its cliques, and $\Psi_i = \prod_{j \in T_i} \psi_j$, a function of $V_i$. For an edge from $i$ to its parent $p$, write $S = C_i \cap C_p$.

**Lemma 1 (what the running intersection property gives).** (a) $V_i \cap C_p \subseteq S$. (b) For two children $c \ne c'$ of $i$, $V_c \cap V_{c'} \subseteq C_i$, and $V_c \cap C_i = C_c \cap C_i$. (c) The factors put outside $T_i$ have scopes in $W = (V \setminus V_i) \cup S$.

*Proof.* If a variable $x$ is in a clique of $T_i$ and in a clique outside $T_i$, the tree path between the two cliques passes the edge $\{i, p\}$, so by the property $x \in C_i$ and $x \in C_p$, that is $x \in S$. This gives (a) and (c), because a factor put outside $T_i$ has its scope inside a clique outside $T_i$. For (b), the path between a clique of $T_c$ and a clique of $T_{c'}$ passes through $i$, and the path from a clique of $T_c$ to $i$ passes through $c$. $\blacksquare$

**Lemma 2 (collect).** When line L5 makes $i$ send to its parent $p$, the table of $i$ is $\phi_i = \sum_{V_i \setminus C_i} \Psi_i$, and the new separator table is $\mu_{ip} = \sum_{V_i \setminus S} \Psi_i$.

*Proof.* Induction from the leaves. Line L5 visits the cliques in reverse breadth-first order, so each child of $i$ has sent before $i$ sends. During the collect pass every old separator table is the constant 1 of line L3, so line L9 only multiplies. Hence when $i$ sends, $\phi_i = \psi_i \prod_c \mu_{ci}$ over the children $c$ of $i$, and by induction $\mu_{ci} = \sum_{V_c \setminus S_c} \Psi_c$ with $S_c = C_c \cap C_i$. By Lemma 1(b), the sets $V_c \setminus S_c$ for the children are pairwise disjoint and do not meet $C_i$, and their union with $C_i$ is $V_i$. A sum over disjoint groups of variables of a product whose factors each use only one group splits into a product of sums, so
$$\sum_{V_i \setminus C_i} \Psi_i = \psi_i \prod_c \sum_{V_c \setminus S_c} \Psi_c = \psi_i \prod_c \mu_{ci} = \phi_i.$$
Line L8 then gives $\mu_{ip} = \sum_{C_i \setminus S} \phi_i = \sum_{V_i \setminus S} \Psi_i$, and line L10 stores it. $\blacksquare$

At the root $V_r = V$ and $\Psi_r = \tilde p$, so after line L5, $\phi_r = \sum_{V \setminus C_r} \tilde p$, the marginal of $\tilde p$ on $C_r$. Write $M_C = \sum_{V \setminus C} \tilde p$ for a set $C$.

**Lemma 3 (distribute).** When line L6 makes $p$ send to its child $i$, and $\phi_p = M_{C_p}$ before the pass, then $\phi_i = M_{C_i}$ after the pass.

*Proof.* Line L6 visits the cliques in breadth-first order, so $p$ has received before it sends, and $i$ has not changed since it sent in the collect pass: by Lemma 2 its table is $A = \sum_{V_i \setminus C_i} \Psi_i$ and the old separator table is $B = \sum_{V_i \setminus S} \Psi_i$. Line L8 computes $\mu^* = \sum_{C_p \setminus S} M_{C_p} = M_S$.

Write $\tilde p = \Psi_i \cdot R$, where $R$ is the product of the factors put outside $T_i$. By Lemma 1(c), $R$ is a function of $W$, and $W \cap V_i = S$. Let $\rho(s) = \sum_{W \setminus S} R$. Then, summing first over the variables outside $V_i$,
$$M_{C_i}(c) = A(c)\, \rho(s), \qquad M_S(s) = B(s)\, \rho(s),$$
where $s$ is the part of $c$ on $S$. Line L9 sets $\phi_i(c) \leftarrow A(c)\, \mu^*(s) / B(s)$ when $A(c) \ne 0$, and leaves 0 when $A(c) = 0$.

- If $B(s) > 0$, then $\rho(s) = M_S(s) / B(s)$ and $A(c)\, M_S(s) / B(s) = A(c)\, \rho(s) = M_{C_i}(c)$.
- If $B(s) = 0$, then all entries of $A$ that agree with $s$ are 0, because $B(s)$ is their sum and they are nonnegative. So $A(c) = 0$, line L9 leaves $\phi_i(c) = 0$, and $M_{C_i}(c) = A(c) \rho(s) = 0$.

The second case is the rule $0/0 = 0$, and it also shows that line L9 never divides by zero. $\blacksquare$

**Theorem.** After lines L5 and L6, $\phi_i = M_{C_i} = \sum_{V \setminus C_i} \tilde p$ for every clique $i$. For a Bayesian network, $\phi_i(c) = P(C_i = c, e)$, $\sum_c \phi_i(c) = P(e)$, and line L7 returns $P(C_i \mid e)$ when $P(e) > 0$.

*Proof.* The root holds $M_{C_r}$ after the collect pass, and it does not change in the distribute pass, as it only sends. Each other clique receives once in the distribute pass, after its parent, so by Lemma 3 and induction along the breadth-first order each clique ends with $M_{C_i}$. For a Bayesian network, $\tilde p$ is the joint distribution times the indicators of the evidence, which gives the rest. $\blacksquare$

**Calibration.** For each tree edge $\{i, j\}$ with separator $S$, $\sum_{C_i \setminus S} \phi_i = M_S = \sum_{C_j \setminus S} \phi_j$, and this is also the last separator table. So the result is calibrated.

**Messages.** Each of the $k - 1$ tree edges carries one pass in line L5 and one in line L6, so the algorithm sends $2(k - 1)$ messages.

**The Shafer-Shenoy form.** It computes the message from $i$ to $j$ as $\sum_{C_i \setminus S_{ij}} \psi_i \prod_{c \in N(i) \setminus \{j\}} m_{c \to i}$ and the final table as $\psi_i \prod_{c \in N(i)} m_{c \to i}$. The argument of Lemma 2, applied with the tree rooted at $j$, shows that $m_{i \to j} = \sum_{V' \setminus S_{ij}} \Psi'$, where $V'$ and $\Psi'$ are the variables and the factor product on the side of $i$. With Lemma 1 for all the sides around $i$, the final table is $M_{C_i}$. No division is needed. $\blacksquare$
