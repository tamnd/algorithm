---
title: The Smolyak collocation surrogate on nested nodes interpolates the runs, reproduces total degree L, and its quadrature is exact for total degree 2L + 1
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. For a level $l \ge 0$, let $X_l$ be the one dimensional nodes ($X_0 = \{0\}$ and $X_l = \{-\cos(\pi j / 2^l) : 0 \le j \le 2^l\}$), $m(l) = |X_l|$, $U_l$ the Lagrange interpolation operator on $X_l$, and $Q_l$ the interpolatory quadrature on $X_l$ for the uniform law on $[-1, 1]$, $Q_l f = \mathbb{E}[U_l f]$. Let $V_l = \mathbb{P}_{m(l) - 1}$, the polynomials of degree less than $m(l)$. Put $U_{-1} = 0$, $\Delta_l = U_l - U_{l-1}$, and for a multi-index $l \in \mathbb{N}^d$ write $U_l = U_{l_1} \otimes \cdots \otimes U_{l_d}$ and $\Delta_l = \Delta_{l_1} \otimes \cdots \otimes \Delta_{l_d}$, acting on functions of $d$ variables.

**Lemma 1 (one dimensional facts).** The sets $X_l$ are nested, $X_{l-1} \subseteq X_l$, and so are the spaces, $V_{l-1} \subseteq V_l$. $U_l f = f$ for $f \in V_l$. $Q_l f = \mathbb{E}[f]$ for every polynomial $f$ of degree at most $e(l)$, where $e(0) = 1$ and $e(l) = 2^l + 1$ for $l \ge 1$; in particular $e(l) \ge 2l + 1$ and $e$ is increasing.

*Proof.* The node $-\cos(\pi j / 2^{l-1})$ equals $-\cos(\pi (2j) / 2^l)$, and $0 = -\cos(\pi \cdot 2^{l-1} / 2^l)$, so $X_{l-1} \subseteq X_l$; since $m$ increases, so do the $V_l$. Interpolation on $m(l)$ distinct nodes reproduces polynomials of degree less than $m(l)$, by uniqueness of the interpolant. So $Q_l$ is exact for degree $m(l) - 1$. The node set is symmetric about 0, so the weights are symmetric, and the rule gives 0 for every odd monomial, which is the exact mean; hence $Q_l$ is exact for degree $m(l)$ when $m(l) - 1$ is even, which holds for all $l$. That is $e(0) = 1$ and $e(l) = 2^l + 1$. Finally $2^l \ge 2l$ for all $l \ge 1$, by induction. $\square$

**Lemma 2 (the combination formula is the difference form).** For $L \ge 0$,

$$\sum_{|l| \le L} \Delta_l = \sum_{L - d + 1 \le |j| \le L} (-1)^{L - |j|} \binom{d-1}{L - |j|}\, U_j,$$

where the sums run over $l, j \in \mathbb{N}^d$. The same holds with $Q$ in place of $U$.

*Proof.* Expand each $\Delta_{l_k} = U_{l_k} - U_{l_k - 1}$. The product $\Delta_l$ is $\sum_{e \in \{0,1\}^d} (-1)^{|e|} U_{l - e}$, where a term with some $l_k - e_k = -1$ vanishes. So the coefficient of $U_j$ on the left is $\sum (-1)^{|e|}$ over the $e \in \{0, 1\}^d$ with $|j + e| \le L$, that is $\sum_{t=0}^{\min(d, s)} (-1)^t \binom{d}{t}$ with $s = L - |j| \ge 0$. If $s \ge d$ this is $(1 - 1)^d = 0$. If $0 \le s \le d - 1$, the partial alternating sum is $\sum_{t=0}^{s} (-1)^t \binom{d}{t} = (-1)^s \binom{d-1}{s}$, by induction on $s$ with Pascal's rule $\binom{d}{t} = \binom{d-1}{t} + \binom{d-1}{t-1}$, because the sum telescopes. For $|j| > L$ the coefficient is 0. The quadrature case is the same algebra. $\square$

So line L4 computes $A_L q = \sum_{|l| \le L} \Delta_l q$, and line L6 computes the mean $\sum_{|l| \le L} \Delta^Q_l q$ with $\Delta^Q_l = \bigotimes_k (Q_{l_k} - Q_{l_k - 1})$, because $\sum_x w_x y_x$ regroups the same sum by node.

**Lemma 3 (polynomial exactness).** If $f = f_1 \otimes \cdots \otimes f_d$ with $f_k \in V_{\beta_k}$ and $|\beta| \le L$, then $A_L f = f$. By linearity, $A_L$ reproduces every function in $\sum_{|\beta| \le L} V_{\beta_1} \otimes \cdots \otimes V_{\beta_d}$, which contains all polynomials of total degree at most $L$.

*Proof.* By Lemma 1, $U_l f_k = f_k$ for $l \ge \beta_k$, so $\Delta_l f_k = 0$ for $l > \beta_k$. Hence $\Delta_l f = \prod_k \Delta_{l_k} f_k$ is 0 unless $l \le \beta$ in every entry, and all such $l$ satisfy $|l| \le |\beta| \le L$. Then $A_L f = \sum_{l \le \beta} \bigotimes_k \Delta_{l_k} f_k = \bigotimes_k \sum_{l_k = 0}^{\beta_k} \Delta_{l_k} f_k = \bigotimes_k U_{\beta_k} f_k = f$, by the telescoping sum. A monomial $\xi^\beta$ of total degree $|\beta| \le L$ has $\xi_k^{\beta_k} \in V_{\beta_k}$, because $m(l) - 1 \ge l$ for every $l$. $\square$

**Lemma 4 (interpolation at the nodes).** For every node $x$ of the sparse grid $H$, $A_L q(x) = q(x)$.

*Proof.* The node $x$ lies in the tensor grid of some $l^\circ$ with $|l^\circ| \le L$; put $\beta_k$ as the smallest level with $x_k \in X_{\beta_k}$, so $\beta \le l^\circ$ and $|\beta| \le L$. By nestedness, $x_k \in X_l$ for all $l \ge \beta_k$, so $(U_l g)(x_k) = g(x_k)$ for $l \ge \beta_k$, and $(\Delta_l g)(x_k) = 0$ for $l > \beta_k$. A tensor product operator applied to $q$ and evaluated at $x$ depends only on the one dimensional values, so $(\Delta_l q)(x) = 0$ unless $l \le \beta$. As in Lemma 3, $A_L q(x) = \sum_{l \le \beta} (\Delta_l q)(x) = (U_\beta q)(x) = q(x)$, the last step because $x$ is a node of the tensor grid of $\beta$. $\square$

**Lemma 5 (quadrature exactness).** The mean of line L6 is exact for every polynomial of total degree at most $2L + 1$.

*Proof.* Take a monomial $\xi^\beta$ with $|\beta| \le 2L + 1$, and let $\gamma_k$ be the smallest level with $e(\gamma_k) \ge \beta_k$. Since $e(l) \ge 2l + 1$, $\gamma_k \le \lceil (\beta_k - 1)/2 \rceil \le \beta_k / 2$ for $\beta_k \ge 1$, and $\gamma_k = 0$ for $\beta_k = 0$. So $|\gamma| \le |\beta| / 2 \le L + 1/2$, and as $|\gamma|$ is an integer, $|\gamma| \le L$. Since $e$ is increasing, $Q_l \xi_k^{\beta_k} = \mathbb{E}[\xi_k^{\beta_k}]$ for $l \ge \gamma_k$, and the differences vanish for $l > \gamma_k$. The argument of Lemma 3 with $Q$ in place of $U$ gives the value $\prod_k Q_{\gamma_k} \xi_k^{\beta_k} = \prod_k \mathbb{E}[\xi_k^{\beta_k}] = \mathbb{E}[\xi^\beta]$, by independence. $\square$

**Theorem.** STOCHASTIC-COLLOCATION stops after exactly $|H|$ model runs. Its surrogate $A_L q$ equals $q$ at every node of $H$ and equals $q$ everywhere when $q$ is a polynomial of total degree at most $L$. Its mean is exact when $q$ is a polynomial of total degree at most $2L + 1$, and its variance is exact when $q$ has total degree at most $L$.

*Proof.* Termination: line L1 lists finitely many multi-indices, each tensor grid is finite, and line L3 runs the model once per distinct node of the finite set $H$. The surrogate statements are Lemmas 2, 3 and 4. The mean is Lemma 5. If $q$ has total degree at most $L$, then $q^2$ has total degree at most $2L \le 2L + 1$, so both $Q_L[q]$ and $Q_L[q^2]$ are exact by Lemma 5, and so is their combination. $\blacksquare$

The theorem says nothing about the rate for a general smooth $q$. The bounds of Barthelmann, Novak and Ritter and of Nobile, Tempone and Webster, which the page quotes, need regularity of $q$ and the growth of the Lebesgue constants of the Clenshaw-Curtis nodes, and are not proved here.
