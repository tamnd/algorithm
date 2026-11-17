---
title: The Lander-Green recursion returns the multipoint likelihood and the posterior of the inheritance vectors
proves: [correctness]
status: full
---

**The model.** A pedigree has $k$ non-founders and so $b = 2k$ meioses. At marker $j \in \{1, \ldots, M\}$ the inheritance vector $V_j \in \{0, 1\}^b$ records, for each meiosis, whether the parent passed its paternal or its maternal gene. Each founder $i$ has two founder genes $(i, 0)$ and $(i, 1)$, and $V_j$ fixes, for each person, the two founder genes that the person carries. The assumptions are:

1. $V_1$ is uniform on $\{0, 1\}^b$ (Mendel's first law).
2. Given $V_j$, each bit of $V_{j+1}$ differs from the bit of $V_j$ with probability $\theta_j$, independently of the other bits and of $V_1, \ldots, V_{j-1}$ (no interference, the same $\theta_j$ in both sexes).
3. At marker $j$, the founder genes get independent alleles with the frequencies $q_j$, independently over markers (linkage equilibrium) and of the vectors.

Let $D_j$ be the genotypes of the typed people at marker $j$ and $e_j(v) = \Pr(D_j \mid V_j = v)$. Then $(V_j)$ is a Markov chain and $D_j$ depends only on $V_j$: a hidden Markov model. The likelihood is

$$L = \sum_{v_1, \ldots, v_M} 2^{-b} e_1(v_1) \prod_{j=2}^{M} A_{j-1}(v_{j-1}, v_j) \, e_j(v_j), \qquad A_j(u, v) = \theta_j^{h(u, v)} (1 - \theta_j)^{b - h(u, v)},$$

where $h$ is the Hamming distance.

**Lemma 1 (emission).** The function emission returns $e_j(v)$.

*Proof.* Fix $v$. By assumption 3, $e_j(v)$ is the sum over all labellings $x$ of the founder genes with alleles of $\prod_u q_j(x_u)$, restricted to the labellings under which every typed person shows its genotype. Build the graph $\Gamma$ whose nodes are the founder genes and with one edge $\{u, w\}$ for each typed person who carries $u$ and $w$, labelled with the person's unordered genotype $\{a, b\}$. A person who carries the same founder gene twice gives a loop at $u$. A labelling fits the data exactly when, for each edge, $\{x_u, x_w\} = \{a, b\}$ as multisets. This condition is a product of conditions on the components of $\Gamma$, and the founder genes outside $\Gamma$ are free. So the sum factors into a product over the components, times $\sum_a q_j(a) = 1$ for each free gene.

In one component, choose a start node $s$ with an edge labelled $\{a, b\}$. A fitting labelling has $x_s \in \{a, b\}$. Given $x_s$, each edge $\{u, w\}$ with $x_u$ known forces $x_w$: it is the other element of the multiset when $x_u$ is in it, and no labelling fits when $x_u$ is not in it. The component is connected, so the search reaches every node, and the labelling is unique if it exists. The search also checks every edge, including the loops and the edges that close cycles. So the component has at most two fitting labellings, one for each value of $x_s$, and the code adds the weight of each one that passes all checks. If a component has none, $e_j(v) = 0$. $\square$

**Lemma 2 (transition).** The function transition returns $A_j x$ for a vector $x$ of length $2^b$.

*Proof.* Write $B = \begin{pmatrix} 1 - \theta & \theta \\ \theta & 1 - \theta \end{pmatrix}$. Since $A_j(u, v) = \prod_{t=1}^{b} B(u_t, v_t)$, $A_j$ is the Kronecker product of $b$ copies of $B$, which is the product of the $b$ commuting matrices $I \otimes \cdots \otimes B \otimes \cdots \otimes I$ with $B$ at position $t$. Pass $t$ of the loop replaces each pair $(x_v, x_{v + 2^t})$ with bit $t$ of $v$ equal to 0 by $B$ times the pair, which is the action of the factor with $B$ at position $t$. $\square$

**Lemma 3 (forward pass).** For each $j$, after line L6, $c_j = \Pr(D_j \mid D_1, \ldots, D_{j-1})$ and $\alpha_j(v) = \Pr(V_j = v \mid D_1, \ldots, D_j)$.

*Proof.* By induction on $j$. For $j = 1$, line L2 gives $2^{-b} e_1(v) = \Pr(V_1 = v, D_1)$, and its sum is $c_1 = \Pr(D_1)$. Dividing by $c_1$ gives the posterior. For $j > 1$, by the Markov property and since $D_1, \ldots, D_{j-1}$ depend on $V_j$ only through $V_{j-1}$,

$$\Pr(V_j = v \mid D_{1..j-1}) = \sum_u \alpha_{j-1}(u) A_{j-1}(u, v).$$

$A_{j-1}$ is symmetric, so this is $(A_{j-1} \alpha_{j-1})(v)$, which line L4 computes by Lemma 2. Line L5 multiplies by $e_j(v) = \Pr(D_j \mid V_j = v, D_{1..j-1})$ to get $\Pr(V_j = v, D_j \mid D_{1..j-1})$, whose sum over $v$ is $c_j$. Dividing gives $\alpha_j$. $\square$

**Theorem 1.** Line L7 returns $\log L$.

*Proof.* By the chain rule $L = \Pr(D_1, \ldots, D_M) = \prod_j \Pr(D_j \mid D_{1..j-1}) = \prod_j c_j$ by Lemma 3. $\square$

If some $c_j = 0$, then $L = 0$: no inheritance vector fits the data at marker $j$, which is a Mendelian inconsistency, and the code raises an error.

**Theorem 2.** Line L9 sets $\text{post}_j(v) = \Pr(V_j = v \mid D_1, \ldots, D_M)$.

*Proof.* Let $\beta_j(v) = \Pr(D_{j+1..M} \mid V_j = v) / \prod_{i > j} c_i$, so $\beta_M = 1$. By the Markov property

$$\Pr(D_{j+1..M} \mid V_j = v) = \sum_u A_j(v, u) \, e_{j+1}(u) \Pr(D_{j+2..M} \mid V_{j+1} = u),$$

so $\beta_j = A_j (e_{j+1} \beta_{j+1}) / c_{j+1}$, with the product taken entry by entry. This is line L8, by Lemma 2 and the symmetry of $A_j$. Given $V_j$, the future data are independent of the past data, so

$$\Pr(V_j = v \mid D_{1..M}) = \frac{\Pr(V_j = v \mid D_{1..j}) \Pr(D_{j+1..M} \mid V_j = v)}{\Pr(D_{j+1..M} \mid D_{1..j})} = \alpha_j(v) \beta_j(v),$$

because $\Pr(D_{j+1..M} \mid D_{1..j}) = \prod_{i > j} c_i$ by the chain rule. $\square$

The IBD probabilities of two people at marker $j$ follow: for each $v$, the number of founder genes that they share is a function of $v$, and ibd_distribution sums $\text{post}_j(v)$ over the vectors with each count.
