---
title: Any t valid partial BLS signatures combine to the signature of the shared key, and t - 1 shares reveal nothing about it
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $r$ with generator $g$ and a bilinear, non-degenerate pairing $e : G \times G \to G_T$. Let $f(z) = x + c_1 z + \dots + c_{t-1} z^{t-1}$ over $\mathbb{Z}_r$ be the dealer's polynomial of line L1, with $1 \le t \le n < r$, and $x_i = f(i)$.

**Lemma 1 (Lagrange at zero).** Let $S \subseteq \{1, \dots, n\}$ with $|S| = t$, and let $\lambda_i = \prod_{j \in S, j \ne i} j / (j - i)$ as in line L4. Then for every polynomial $h$ of degree at most $t - 1$ over $\mathbb{Z}_r$, $\sum_{i \in S} \lambda_i h(i) = h(0)$.

*Proof.* The indices in $S$ are distinct and less than $r$, so every $j - i$ with $i \ne j$ is nonzero mod $r$ and the $\lambda_i$ exist. Let $\ell_i(z) = \prod_{j \in S, j \ne i} (z - j)/(i - j)$. Then $\ell_i(i) = 1$, $\ell_i(k) = 0$ for $k \in S \setminus \{i\}$, and $\ell_i(0) = \lambda_i$. The polynomial $h - \sum_{i \in S} h(i) \ell_i$ has degree at most $t - 1$ and vanishes at the $t$ points of $S$, so it is zero, because a nonzero polynomial of degree at most $t - 1$ over a field has at most $t - 1$ roots. Evaluate at $0$. $\square$

**Lemma 2 (honest partial signatures pass line L3).** $\sigma_i = H(m)^{x_i}$ satisfies $e(\sigma_i, g) = e(H(m), y_i)$.

*Proof.* $e(H(m)^{x_i}, g) = e(H(m), g)^{x_i} = e(H(m), g^{x_i})$ by bilinearity. $\square$

**Lemma 3 (combination gives the BLS signature).** If $\sigma_i = H(m)^{x_i}$ for all $i \in S$, then line L5 outputs $H(m)^x$, which passes line L6.

*Proof.* $\prod_{i \in S} \sigma_i^{\lambda_i} = H(m)^{\sum_i \lambda_i f(i)} = H(m)^{f(0)} = H(m)^x$ by Lemma 1, since $H(m)$ has order dividing $r$. Then $e(H(m)^x, g) = e(H(m), g^x) = e(H(m), y)$. $\square$

**Lemma 4 (checked shares are honest).** If $\sigma_i \in G$ passes line L3, then $\sigma_i = H(m)^{x_i}$.

*Proof.* By Lemma 2, $H(m)^{x_i}$ passes too, and $u \mapsto e(u, g)$ is injective on $G$ (if $e(g^a, g) = e(g^b, g)$ then $e(g, g)^{a - b} = 1$, and $e(g, g)$ has order $r$, so $a \equiv b$). $\square$

So any $t$ partial signatures that pass line L3 combine to the unique valid signature; this is the robustness of the scheme.

**Lemma 5 ($t - 1$ shares are independent of the key).** For any set $T$ of $t - 1$ indices, the shares $(x_i)_{i \in T}$ are uniform on $\mathbb{Z}_r^{t-1}$ and independent of $x$.

*Proof.* Fix $x$. The map $(c_1, \dots, c_{t-1}) \mapsto (f(i))_{i \in T}$ is affine with linear part the matrix $(i^k)_{i \in T, 1 \le k \le t-1}$. This is a Vandermonde matrix times the diagonal matrix of the nonzero $i$, so it is invertible because the $i$ are distinct and nonzero mod $r$. A bijection maps the uniform coefficients to uniform shares, whatever $x$ is. $\square$

Lemma 5 shows that the $t - 1$ corrupt shares carry no information about $x$; the partial signatures of honest parties that the adversary also sees are simulated in the security proof by Lagrange interpolation in the exponent from $H(m)^x$ and the corrupt shares, which reduces the unforgeability of the threshold scheme to that of BLS. $\blacksquare$
