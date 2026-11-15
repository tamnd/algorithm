---
title: The products of length up to K give a lower and an upper bound on the joint spectral radius
proves: [correctness]
status: full
---

Let $\mathcal{M} = \{A_1, \dots, A_m\}$ be a finite set of real $n \times n$ matrices and let $\|\cdot\|$ be an induced matrix norm, so $\|PQ\| \le \|P\|\,\|Q\|$. Let $\Sigma_k$ be the set of products $A_{i_k} \cdots A_{i_1}$ of length $k$, and define

$$\hat\rho_k = \max_{P \in \Sigma_k} \|P\|^{1/k}, \qquad \bar\rho_k = \max_{P \in \Sigma_k} \rho(P)^{1/k},$$

where $\rho(P)$ is the spectral radius. The joint spectral radius is $\rho(\mathcal{M}) = \lim_{k \to \infty} \hat\rho_k$.

## Lemma 1: the limit exists and is an infimum

Let $a_k = \log \max_{P \in \Sigma_k} \|P\|$ (with $\log 0 = -\infty$). A product of length $j + k$ is a product of length $j$ times a product of length $k$, so $a_{j+k} \le a_j + a_k$. By Fekete's lemma for subadditive sequences, $a_k / k$ converges to $\inf_k a_k / k$. So $\rho(\mathcal{M}) = \inf_k \hat\rho_k$, and $\rho(\mathcal{M}) \le \hat\rho_k$ for every $k$.

All norms on $\mathbb{R}^{n \times n}$ are equivalent: $c \|P\|' \le \|P\| \le C \|P\|'$. Since $c^{1/k}$ and $C^{1/k}$ tend to 1, the limit does not depend on the norm. $\square$

## Lemma 2: every product gives a lower bound

Let $P \in \Sigma_k$. For every $j \ge 1$, $P^j \in \Sigma_{jk}$, and the spectral radius is at most any induced norm, so

$$\rho(P)^j = \rho(P^j) \le \|P^j\| \le \hat\rho_{jk}^{\,jk}.$$

Taking the root of order $jk$ gives $\rho(P)^{1/k} \le \hat\rho_{jk}$. As $j \to \infty$ the right side tends to $\rho(\mathcal{M})$. So $\bar\rho_k \le \rho(\mathcal{M})$ for every $k$. $\square$

## Theorem

`jsr_bounds(mats, K)` returns $(\ell, u)$ with $\ell = \max_{k \le K} \bar\rho_k$ and $u = \min_{k \le K} \hat\rho_k$, and $\ell \le \rho(\mathcal{M}) \le u$.

*Proof.* Loop invariant: at the start of iteration $k$, `prods` lists every product of length $k - 1$ (the identity for $k = 1$). Line L3 multiplies each of them on the left by each $A_i$, so after it `prods` lists every product of length $k$, once for each index sequence. Lines L4 and L5 then fold $\bar\rho_k$ into the maximum $\ell$ and $\hat\rho_k$ into the minimum $u$. Lemma 2 gives $\bar\rho_k \le \rho(\mathcal{M})$ for each $k$, so $\ell \le \rho(\mathcal{M})$. Lemma 1 gives $\rho(\mathcal{M}) \le \hat\rho_k$ for each $k$, so $\rho(\mathcal{M}) \le u$. $\square$

Lemma 1 also shows that $u \to \rho(\mathcal{M})$ as $K \to \infty$. The lower bound converges too: $\limsup_k \bar\rho_k = \rho(\mathcal{M})$ is the theorem of Berger and Wang. The proof here does not use it.

## Stability under arbitrary switching

Consider $x(t+1) = A_{\sigma(t)}\, x(t)$ with any switching sequence $\sigma$. Then $x(t) = P x(0)$ for a product $P \in \Sigma_t$.

- If $\rho(\mathcal{M}) < 1$, Lemma 1 gives a $k$ with $\hat\rho_k < 1$. Take $q$ with $\hat\rho_k \le q < 1$ and $q > 0$, so $\|P\| \le q^k$ for every $P \in \Sigma_k$. Write $t = sk + r$ with $0 \le r < k$. Then $\|x(t)\| \le q^{sk} B^r \|x(0)\|$ with $B = \max(1, \max_i \|A_i\|)$, which is at most $C q^{t} \|x(0)\|$ with $C = (B/q)^{k}$. The constants do not depend on $\sigma$, so the origin is globally uniformly exponentially stable (GUES) under arbitrary switching.
- If the origin is GUES, $\|P\| \le C q^t$ for all $P \in \Sigma_t$ with some $q < 1$, so $\hat\rho_t \le C^{1/t} q \to q < 1$ and $\rho(\mathcal{M}) \le q < 1$.

So $\rho(\mathcal{M}) < 1$ if and only if the switched system is GUES under arbitrary switching.

## Floating point

The code computes $\|P\|_2$ from the eigenvalues of $P^\top P$ and $\rho(P)$ from the roots of the characteristic polynomial. Both are floating point values. A multiple eigenvalue of $P$ is ill conditioned as a root, with an error near $10^{-8}$ for a double root, so $\ell$ can be above its exact value by that amount. The tests allow $10^{-7}$.

## Cost

There are $m^k$ products of length $k$. Each costs one $n \times n$ product, one norm and one characteristic polynomial, $O(n^3)$ each, plus the roots. The total for lengths $1$ to $K$ is $O(m^K n^3)$ time, and $O(m^K n^2)$ memory for the list of products of the last length.
