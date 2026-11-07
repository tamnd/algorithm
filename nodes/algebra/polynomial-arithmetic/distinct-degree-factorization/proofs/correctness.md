---
title: DISTINCT-DEGREE returns the products of the irreducible factors of each degree
proves: [correctness]
status: full
---

Let $p$ be a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, and $f \in \mathbb{F}_p[x]$ monic and square-free of degree $n$. Write $f = q_1 \cdots q_s$ with distinct monic irreducible $q_j$.

**Lemma 1 (Frobenius).** Let $q \in \mathbb{F}_p[x]$ be monic irreducible of degree $d$ and $i \ge 1$. Then $x^{p^i} \equiv x \pmod q$ if and only if $d \mid i$.

*Proof.* $K = \mathbb{F}_p[x]/(q)$ is a field with $p^d$ elements, and $\alpha = x \bmod q$ generates it over $\mathbb{F}_p$. The map $\varphi(y) = y^p$ is a ring homomorphism of $K$, since $(y + z)^p = y^p + z^p$ in characteristic $p$, and it fixes $\mathbb{F}_p$ by Fermat's little theorem. The nonzero elements form a group of order $p^d - 1$, so $y^{p^d} = y$ for all $y \in K$, that is, $\varphi^d = \mathrm{id}$. For $1 \le k < d$, the polynomial $y^{p^k} - y$ has at most $p^k < p^d$ roots in $K$, so $\varphi^k \ne \mathrm{id}$. Hence $\varphi$ has order exactly $d$ as an element of the group of automorphisms of $K$. A ring homomorphism that fixes $\mathbb{F}_p$ and $\alpha$ fixes every polynomial expression in $\alpha$, which is all of $K$. So $\alpha^{p^i} = \alpha$ if and only if $\varphi^i = \mathrm{id}$, if and only if $d \mid i$. $\square$

**Lemma 2.** For $i \ge 1$ and a monic square-free $r$ whose irreducible factors all have degree at least $i$, $\gcd(x^{p^i} - x, r)$ is the product of the irreducible factors of $r$ of degree exactly $i$.

*Proof.* The polynomial $x^{p^i} - x$ has derivative $p^i x^{p^i - 1} - 1 = -1$, so it is square-free. Each irreducible factor $q$ of $r$ divides $x^{p^i} - x$ exactly when $\deg q \mid i$, by Lemma 1. As $r$ is square-free, the gcd is the product of the factors of $r$ with $\deg q \mid i$. Since $\deg q \ge i$, $\deg q \mid i$ means $\deg q = i$. $\square$

**Invariant.** Before the test at line L2, with the current $i$ (the number of completed iterations):

1. $r$ is the product of the $q_j$ with $\deg q_j \ge i + 1$;
2. $h \equiv x^{p^i} \pmod r$ and $\deg h < \deg r$ (or $h = 0$ when $r = 1$);
3. the output so far is the list of pairs $(g_k, k)$, $k \le i$, with $g_k \ne 1$, where $g_k$ is the product of the $q_j$ of degree $k$.

*Initialization.* With $i = 0$, $r = f$ contains all factors, which have degree at least $1$, $h = x \bmod f = x^{p^0} \bmod r$, and the output is empty.

*Maintenance.* Line L3 sets $i \leftarrow i + 1$; now $r$ is the product of the factors of degree at least $i$ and $h \equiv x^{p^{i-1}}$. Line L4 gives $h \equiv (x^{p^{i-1}})^p = x^{p^i} \pmod r$. Since $h - x \equiv x^{p^i} - x \pmod r$, line L5 computes $g = \gcd(x^{p^i} - x, r)$, which by Lemma 2 is the product $g_i$ of the factors of degree $i$. If $g \ne 1$, line L6 outputs $(g_i, i)$ and removes these factors from $r$, so $r$ becomes the product of the factors of degree at least $i + 1$; since the new $r$ divides the old one, $h \bmod r$ is still $\equiv x^{p^i}$. If $g = 1$, there are no factors of degree $i$ and $r$ is already the product of those of degree at least $i + 1$. So the invariant holds again.

**Termination.** Every iteration increases $i$, and the loop stops when $2(i + 1) > \deg r$, which happens for $i \ge n/2$ at the latest. So there are at most $\lfloor n/2 \rfloor$ iterations.

**The rest.** When the loop stops, every factor of $r$ has degree at least $i + 1$ by part 1, and $\deg r < 2(i + 1)$. If $r$ had two or more factors, $\deg r$ would be at least $2(i + 1)$. So $r = 1$ or $r$ is irreducible of degree $\deg r \ge i + 1$. In the second case $r$ is the only factor of $f$ of its degree, so $g_{\deg r} = r$, and line L7 outputs $(r, \deg r)$. Together with part 3, the output lists every $g_k \ne 1$ exactly once, in increasing order of $k$. $\blacksquare$
