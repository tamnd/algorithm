---
title: NEWTON-INVERSE returns the inverse modulo x^n in at most 3M(n) + o(M(n)) operations
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, $f = \sum_{k \ge 0} f_k x^k$ with $f_0$ a unit of $R$, and $n \ge 1$. Congruences are in $R[[x]]$, or equivalently between polynomials, modulo powers of $x$.

**Lemma 1 (existence and uniqueness).** For each $m \ge 1$ there is exactly one polynomial $g$ of degree less than $m$ with $fg \equiv 1 \pmod{x^m}$.

*Proof.* Write $g = \sum_{k<m} g_k x^k$. The coefficient of $x^k$ in $fg$, for $k < m$, is $\sum_{j=0}^{k} f_j g_{k-j}$. The conditions are $f_0 g_0 = 1$ and $f_0 g_k + \sum_{j=1}^{k} f_j g_{k-j} = 0$ for $1 \le k < m$. Since $f_0$ is a unit, these determine $g_0 = f_0^{-1}$ and then each $g_k$ from $g_0, \ldots, g_{k-1}$, uniquely. $\square$

**Lemma 2 (precisions).** Let $k_0 = n$, $k_{i+1} = \lceil k_i/2 \rceil$, and let $s$ be the first index with $k_s = 1$. Then $k_0 > k_1 > \cdots > k_s = 1$, $k_{i+1} < k_i \le 2 k_{i+1}$ for $i < s$, $k_i \le n/2^i + 1$, and $s = \lceil \log_2 n \rceil$.

*Proof.* For $k \ge 2$, $\lceil k/2 \rceil < k$, so the sequence strictly decreases until it reaches $1$, and it stops there. Also $k \le 2 \lceil k/2 \rceil$. For the bound, $k_0 = n$, and if $k_i \le n/2^i + 1$ then $k_{i+1} \le (k_i + 1)/2 \le n/2^{i+1} + 1$. For $s$: $\lceil \lceil k/2 \rceil / 2 \rceil = \lceil k/4 \rceil$, so $k_i = \lceil n/2^i \rceil$, which is $1$ exactly when $2^i \ge n$. $\square$

**Lemma 3 (one step).** Let $1 \le m < m' \le 2m$, and let $g$ be a polynomial of degree less than $m$ with $fg \equiv 1 \pmod{x^m}$. Let $d = (f \bmod x^{m'}) g \bmod x^{m'}$, $t = -\sum_{j=0}^{m'-m-1} d_{m+j} x^j$, $c = g t \bmod x^{m'-m}$, and $g' = g + x^m c$. Then $\deg g' < m'$ and $f g' \equiv 1 \pmod{x^{m'}}$.

*Proof.* Since $f \equiv (f \bmod x^{m'}) \pmod{x^{m'}}$, $d \equiv fg \pmod{x^{m'}}$. By hypothesis $d_0 = 1$ and $d_1 = \cdots = d_{m-1} = 0$. So $e := 1 - fg \equiv 1 - d = x^m t \pmod{x^{m'}}$. Next, $x^m c \equiv x^m g t \pmod{x^{m'}}$, because $c \equiv gt \pmod{x^{m'-m}}$ and multiplying by $x^m$ moves the modulus to $x^{m'}$. So $g' \equiv g + g\, x^m t \equiv g + g e \pmod{x^{m'}}$. Then

$$1 - f g' \equiv 1 - fg - fg\, e = e - (1 - e)\, e = e^2 \pmod{x^{m'}}.$$

Since $e \equiv x^m t \pmod{x^{m'}}$, $e^2 \equiv x^{2m} t^2 \equiv 0 \pmod{x^{m'}}$ as $2m \ge m'$. For the degree, $\deg g < m$ and $\deg(x^m c) < m + (m' - m) = m'$. $\square$

**Theorem (correctness).** NEWTON-INVERSE$(f, n)$ returns the unique $g$ of degree less than $n$ with $fg \equiv 1 \pmod{x^n}$, as a list of $n$ coefficients.

*Proof.* We show that at the start of each iteration of line L3, and after the loop, $g$ is a list of $m$ coefficients with $fg \equiv 1 \pmod{x^m}$, where $m$ is the precision reached so far. After lines L1 and L2, $g = [f_0^{-1}]$ and $m = 1$, and $f g \equiv f_0 f_0^{-1} = 1 \pmod x$. The loop visits $m' = k_{s-1}, k_{s-2}, \ldots, k_0$ in this order, starting from $m = k_s$, so in each iteration $m = k_{i+1}$ and $m' = k_i$ for some $i$, and $m < m' \le 2m$ by Lemma 2. Lines L4 to L7 compute $d$, $t$, $c$ and $g'$ of Lemma 3, so after line L7 the claim holds for $m'$. The list $g$ then has $m + (m' - m) = m'$ entries, because $c$ is padded to $m' - m$ entries. After the last iteration $m = k_0 = n$ (if $n = 1$, there is no iteration and $m = 1 = n$). By Lemma 1, $g$ is the unique inverse modulo $x^n$. $\square$

**Theorem (cost).** Assume that multiplying a polynomial with $a$ coefficients by one with $b \le a$ coefficients costs at most $M(a)$ ring operations, and that $M(k)/k$ is nondecreasing. Then NEWTON-INVERSE$(f, n)$ uses at most $3M(n) + 2 \lceil \log_2 n \rceil\, M(n)/n + O(n)$ ring operations, plus one inversion in $R$. Since $\log n / n \to 0$, this is $3M(n) + o(M(n))$.

*Proof.* Consider the iteration with $m = k_{i+1}$ and $m' = k_i$, for $0 \le i < s$. Line L4 multiplies $k_i$ by $k_{i+1}$ coefficients, at most $M(k_i)$. Line L6 multiplies $k_{i+1}$ by $k_i - k_{i+1} \le k_{i+1}$ coefficients, at most $M(k_{i+1})$. Lines L5 and L7 and the padding cost $O(k_i)$. Since $M(k)/k$ is nondecreasing and $k_i \le n$, $M(k_i) \le (k_i / n) M(n) \le (2^{-i} + 1/n) M(n)$ by Lemma 2. So

$$\sum_{i=0}^{s-1} M(k_i) \le \Bigl(\sum_{i \ge 0} 2^{-i} + \frac{s}{n}\Bigr) M(n) \le 2M(n) + s\, \frac{M(n)}{n}, \qquad \sum_{i=0}^{s-1} M(k_{i+1}) = \sum_{i=1}^{s} M(k_i) \le M(n) + s\, \frac{M(n)}{n}.$$

The linear terms sum to $O(\sum_i k_i) = O(n)$, because $\sum_i k_i \le \sum_i (n/2^i + 1) \le 2n + s$. Adding up, with $s = \lceil \log_2 n \rceil$ from Lemma 2, gives the bound. $\blacksquare$
