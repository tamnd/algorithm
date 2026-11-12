---
title: What each step of mean-field DCA computes
proves: [correctness]
status: full
---

We use the notation of the page. Sequences are $x \in [q]^n$. For $x$, let $y(x) \in \{0, 1\}^{n(q-1)}$ be the reduced one-hot vector, $y_{(i,a)}(x) = [x_i = a]$ for $a < q$; the reference state $q$ has no coordinate. The pseudocount weight is $\lambda \ge 0$, the weights are $w_s > 0$, and $M_{\mathrm{eff}} = \sum_s w_s$.

**Lemma 1 (the correlation matrix is invertible).** Let $\alpha = \lambda / (\lambda + M_{\mathrm{eff}})$, let $P_w(x) = \sum_s w_s [X_s = x] / M_{\mathrm{eff}}$ be the weighted empirical distribution, $U$ the uniform distribution on $[q]^n$, and $Q = (1 - \alpha) P_w + \alpha U$. Then the matrix $C$ of line L4 is the covariance matrix of $y$ under $Q$. If $Q(x) > 0$ for every $x$, in particular if $\lambda > 0$, then $C$ is positive definite.

*Proof.* The marginals of $U$ are $1/q$ for one column and $1/q^2$ for two distinct columns. So $Q_i(a) = (1 - \alpha) P_{w,i}(a) + \alpha / q$, and multiplying out with $1 - \alpha = M_{\mathrm{eff}} / (\lambda + M_{\mathrm{eff}})$ gives the $f_i(a)$ of line L2. In the same way the two-column marginals of $Q$ are the $f_{ij}(a, b)$ of line L3. Now $E_Q[y_{(i,a)}] = f_i(a)$, $E_Q[y_{(i,a)} y_{(j,b)}] = f_{ij}(a, b)$ for $i \ne j$, and $E_Q[y_{(i,a)} y_{(i,b)}] = f_i(a) [a = b]$, because a column has one state. So $C_{(i,a),(j,b)} = E_Q[y_{(i,a)} y_{(j,b)}] - E_Q[y_{(i,a)}] E_Q[y_{(j,b)}]$, the covariance.

For a vector $v$, $v^{\top} C v = \mathrm{Var}_Q(v \cdot y) \ge 0$. Suppose it is 0. Since every $x$ has $Q(x) > 0$, the value $v \cdot y(x)$ is the same for all $x$. At the sequence with all states equal to $q$, $y = 0$, so the value is 0. At the sequence with state $a < q$ in column $i$ and $q$ elsewhere, $y$ has a single 1, at $(i, a)$, so $v_{(i,a)} = 0$. Hence $v = 0$, and $C$ is positive definite. If $\lambda > 0$ then $\alpha > 0$ and $Q(x) \ge \alpha q^{-n} > 0$. $\square$

So $C^{-1}$ exists, and Gaussian elimination with partial pivoting computes it in exact arithmetic.

**Lemma 2 (mean-field response).** Take a Potts model in the gauge of the page, and write $J_{ji}(b, a) = J_{ij}(a, b)$. In the naive mean-field approximation, the model is replaced by a product $\prod_i Q_i$ with

$$Q_i(a) \propto \exp\Big( h_i(a) + \sum_{j \ne i} \sum_{b} J_{ij}(a, b)\, Q_j(b) \Big),$$

the stationarity condition for the minimum of $\mathrm{KL}(\prod_i Q_i \,\|\, P)$. Let $m_{(i,a)} = Q_i(a)$ for $a < q$, and let $\chi = \partial m / \partial h$ be the response of these marginals to the fields, at a point where the map $h \mapsto m$ is a local diffeomorphism. Then $(\chi^{-1})_{(i,a),(j,b)} = -J_{ij}(a, b)$ for $i \ne j$, and $(\chi^{-1})_{(i,a),(i,b)} = [a = b] / m_{(i,a)} + 1 / Q_i(q)$.

*Proof.* Divide the condition for state $a$ by the condition for state $q$. Since $h_i(q) = 0$ and $J_{ij}(q, b) = 0$, and since $J_{ij}(a, q) = 0$ removes the term $b = q$,

$$h_i(a) = \log m_{(i,a)} - \log\Big(1 - \sum_{c < q} m_{(i,c)}\Big) - \sum_{j \ne i} \sum_{b < q} J_{ij}(a, b)\, m_{(j,b)}.$$

This writes $h$ as a function of $m$. Its derivative with respect to $m_{(j,b)}$ is $-J_{ij}(a, b)$ for $j \ne i$, and $[a = b] / m_{(i,a)} + 1 / (1 - \sum_c m_{(i,c)})$ for $j = i$. The derivative of the inverse map is the inverse matrix, so $\chi^{-1} = \partial h / \partial m$ is as stated. $\square$

For the exact model the response is the covariance: $\partial P_i(a) / \partial h_j(b) = \mathrm{Cov}_P(y_{(i,a)}, y_{(j,b)})$, since $P_i(a) = \partial \log Z / \partial h_i(a)$ and the second derivatives of $\log Z$ are covariances. Mean-field DCA sets $\chi$ equal to the observed covariance $C$ and reads $e_{ij}(a, b) = -(C^{-1})_{(i,a),(j,b)}$, which is line L5. The approximation is in this step: the exact covariance is not the mean-field response. The two agree to first order in $J$, and the tests observe an error that falls by a factor of about 4 when the couplings are halved.

**Proposition 3 (independent columns).** If $f_{ij}(a, b) = f_i(a) f_j(b)$ for all $i \ne j$ and all $a, b$, and $C$ is invertible, then $e_{ij} = 0$ for every pair.

*Proof.* The off-diagonal blocks of $C$ are then 0, so $C$ is block diagonal with blocks $C_{ii}$. The inverse of a block-diagonal matrix is block diagonal, with blocks $C_{ii}^{-1}$, so every off-diagonal block of $C^{-1}$, and of $e$, is 0. $\square$

**Proposition 4 (the zero-sum gauge).** For a real $q \times q$ matrix $M$, let $G(M) = \{ M + u \mathbf{1}^{\top} + \mathbf{1} v^{\top} : u, v \in \mathbb{R}^q \}$, the gauge-equivalent forms of a coupling block, and let $Z(M) = \Pi M \Pi$ with $\Pi = I - \mathbf{1}\mathbf{1}^{\top} / q$. Entry by entry, $Z(M)_{ab}$ is $M_{ab}$ minus the mean of row $a$ minus the mean of column $b$ plus the mean of all entries, the matrix of line L6. Then $Z(N) = Z(M)$ for all $N \in G(M)$, $Z(M) \in G(M)$, and $\|Z(M)\|_F \le \|N\|_F$ for all $N \in G(M)$.

*Proof.* Since $\Pi \mathbf{1} = 0$ and $\Pi$ is symmetric, $\Pi (u \mathbf{1}^{\top} + \mathbf{1} v^{\top}) \Pi = 0$, so $Z$ takes the same value on all of $G(M)$. Expanding, $M - Z(M) = \mathbf{1}\mathbf{1}^{\top} M / q + M \mathbf{1}\mathbf{1}^{\top} / q - (\mathbf{1}^{\top} M \mathbf{1}) \mathbf{1}\mathbf{1}^{\top} / q^2$, and each term has the form $u \mathbf{1}^{\top}$ or $\mathbf{1} v^{\top}$, so $Z(M) \in G(M)$. Finally $Z(M) \mathbf{1} = 0$ and $\mathbf{1}^{\top} Z(M) = 0$, so for the Frobenius inner product $\langle Z(M), u \mathbf{1}^{\top} + \mathbf{1} v^{\top} \rangle = u^{\top} Z(M) \mathbf{1} + \mathbf{1}^{\top} Z(M) v = 0$. Any $N \in G(M)$ is $Z(M) + D$ with $D$ of that form, and then $\|N\|_F^2 = \|Z(M)\|_F^2 + \|D\|_F^2$. $\square$

A change of the reference state, or of any gauge, changes each block $e_{ij}$ only within $G(e_{ij})$, with compensating changes of the fields that leave the Potts distribution unchanged. By Proposition 4, the score $F_{ij}$ of line L6 is therefore the same in every gauge.

**Theorem.** For $\lambda > 0$, lines L1 to L8 are well defined and return all $n(n-1)/2$ pairs, ordered by the average-product-corrected Frobenius norm of the least-norm form of the mean-field couplings $e_{ij} = -(C^{-1})_{ij}$. The ranking does not depend on the choice of the reference state.

*Proof.* Every weight in line L1 is at most 1 and positive, because each sequence is close to itself. Lines L2 to L4 compute $C$, which is invertible by Lemma 1. Line L5 is then defined, and Lemma 2 gives its meaning. Line L6 is gauge free by Proposition 4. Line L7 needs $F_{\cdot\cdot} > 0$; if all $F_{ij}$ are 0, every pair has score 0 and the order is the tie order. Line L8 sorts the pairs. $\square$

What the theorem does not say is that the top pairs are contacts. That is an empirical fact about protein families, and it fails when the alignment has too few or too similar sequences.
