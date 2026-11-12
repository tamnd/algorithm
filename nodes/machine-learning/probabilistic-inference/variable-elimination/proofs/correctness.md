---
title: Variable elimination returns P(Q | e), and each product it forms has at most w + 1 variables
proves: [correctness, time.worst]
status: full
---

We use the pseudocode of the page. The input is a set $\Phi_0$ of factors over the variables $X_1, \ldots, X_n$, query variables $Q$, evidence $E = e$, and an order $\pi = (z_1, \ldots, z_k)$ of the other variables. Write $\tilde P(x) = \prod_{\phi \in \Phi_0} \phi(x)$ for the unnormalized product. For a [Bayesian network](/bayesian-network/) $\tilde P$ is the joint distribution; for a [Markov random field](/markov-random-field/) it is $Z$ times the joint distribution. In both cases $P(q \mid e) = \tilde P(q, e) / \sum_{q'} \tilde P(q', e)$, where $\tilde P(q, e)$ is the sum of $\tilde P$ over all $x$ that agree with $q$ and $e$.

**Claim 1 (correctness).** If $\sum_{q} \tilde P(q, e) > 0$, the output of line L8 is $P(q \mid e)$ for each assignment $q$ of $Q$.

*Proof.* Let $Y_j = \{z_{j+1}, \ldots, z_k\} \cup Q$ be the variables still present after step $j$. Let $\Phi_j$ be the set of factors after the loop of line L2 has run $j$ times. We prove this invariant.

> **(I)** For $0 \le j \le k$ and each assignment $y$ of $Y_j$: $\displaystyle \prod_{\phi \in \Phi_j} \phi(y) = \sum_{z_1, \ldots, z_j} \tilde P(y, z_1, \ldots, z_j, e)$, and no factor of $\Phi_j$ mentions $z_1, \ldots, z_j$ or a variable of $E$.

*Initialization.* Line L1 replaces each factor $\phi$ by its reduction $\phi[E = e]$, the factor over the variables of $\phi$ outside $E$ with $\phi[E=e](u) = \phi(u, e)$. The unit factors added for the query variables have the value 1. So $\prod_{\phi \in \Phi_0'} \phi(y) = \tilde P(y, e)$ for each assignment $y$ of $Y_0$, which is (I) for $j = 0$ with an empty sum. No reduced factor mentions $E$.

*Maintenance.* Assume (I) for $j - 1$ and let $z = z_j$. Line L3 splits $\Phi_{j-1}$ into $\Psi$, the factors that mention $z$, and the rest $R$. No factor of $R$ mentions $z$. Lines L4 and L5 form $\tau(u) = \sum_{z} \prod_{\psi \in \Psi} \psi(u, z)$. By the distributive law,
$$\sum_{z} \prod_{\phi \in \Phi_{j-1}} \phi = \prod_{\phi \in R} \phi \cdot \sum_{z} \prod_{\psi \in \Psi} \psi = \prod_{\phi \in R} \phi \cdot \tau = \prod_{\phi \in \Phi_j} \phi,$$
where the last step is line L6. Apply $\sum_{z_j}$ to both sides of (I) for $j - 1$: the left side becomes $\prod_{\phi \in \Phi_j} \phi(y)$ and the right side becomes $\sum_{z_1, \ldots, z_j} \tilde P(y, z_1, \ldots, z_j, e)$. The new factor $\tau$ does not mention $z_j$, and no factor mentions an earlier $z_i$ or $E$. If $\Psi$ is empty, $\tau$ is the constant 1 and the sum over $z$ multiplies by the domain size of $z$; this constant cancels in line L8, so we may treat it as part of the normalization. This proves (I) for $j$.

*Termination.* The loop runs $k$ times. At the end $Y_k = Q$, and by (I) the product of line L7 is $\phi^*(q) = \sum_{z_1, \ldots, z_k} \tilde P(q, z_1, \ldots, z_k, e) = \tilde P(q, e)$, up to the constant of empty steps. Line L8 divides by $\sum_q \phi^*(q) > 0$ and returns $\tilde P(q, e) / \sum_{q'} \tilde P(q', e) = P(q \mid e)$. $\blacksquare$

**Claim 2 (size of the products).** Let $G$ be the interaction graph of the reduced factors: one vertex per variable, and an edge between two variables that share a factor. Let $w$ be the induced width of $G$ along $\pi$. Then each product $\psi$ of line L4 has a scope of at most $w + 1$ variables, and each $\tau$ of line L5 has at most $w$.

*Proof.* Let $G_0 = G$, and let $G_j$ be the graph that we get from $G_{j-1}$ when we connect all neighbours of $z_j$ to each other (the fill edges) and delete $z_j$. The induced width is $w = \max_j \deg_{G_{j-1}}(z_j)$. We show by induction on $j$ that the scope of each factor of $\Phi_j$ is a clique of $G_j$. For $j = 0$ this is the definition of $G$. Assume it for $j - 1$. Each $\psi \in \Psi$ mentions $z_j$, and its scope is a clique of $G_{j-1}$, so its scope lies in $\{z_j\} \cup N_{G_{j-1}}(z_j)$. Hence the scope of the product in line L4 has at most $1 + \deg_{G_{j-1}}(z_j) \le w + 1$ variables, and the scope of $\tau$ lies in $N_{G_{j-1}}(z_j)$, which is a clique of $G_j$ because of the fill edges. A factor of $R$ has a scope that was a clique of $G_{j-1}$ without $z_j$, and $G_j$ keeps all edges among the other vertices, so it stays a clique. $\blacksquare$

**Cost.** Each factor, original or created, enters exactly one set $\Psi$ and then leaves $\Phi$, and there are at most $m + k$ such factors, plus $|Q|$ unit factors. A product of line L4 over a scope of at most $w + 1$ variables with domains of size at most $d$ has at most $d^{w+1}$ entries, and each factor in $\Psi$ costs one multiplication per entry. The sum of line L5 costs one addition per entry. So the loop does $O((m + n) d^{w+1})$ arithmetic operations. Lines L7 and L8 work on tables over $Q$. $\blacksquare$
