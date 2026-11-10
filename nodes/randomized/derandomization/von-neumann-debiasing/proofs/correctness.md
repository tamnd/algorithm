---
title: The output of von Neumann's and Peres's procedures is exactly uniform given its length
proves: [correctness]
status: full
---

We use the notation of the page. $\Psi_\nu$ is PERES with the depth cut off at $\nu \ge 0$: $\Psi_0(x)$ is empty, and for $\nu \ge 1$, $\Psi_\nu(x)$ is empty if $|x| < 2$ and otherwise

$$\Psi_\nu(x) = w \mathbin{+\!\!+} \Psi_{\nu-1}(u) \mathbin{+\!\!+} \Psi_{\nu-1}(v),$$

where $w$ is VON-NEUMANN$(x)$ and $u$, $v$ are the strings of lines L6 and L7. $\Psi_1$ is VON-NEUMANN, and PERES without a cutoff is $\Psi_\nu$ for any $\nu$ larger than the length of $x$. A random string $Z$ is *uniform given its length* if for every $\ell$ with $\Pr[|Z| = \ell] > 0$ and every $z \in \{0,1\}^\ell$, $\Pr[Z = z \mid |Z| = \ell] = 2^{-\ell}$. $\mathcal{U}(N, k)$ is the uniform distribution on the strings of length $N$ with exactly $k$ ones.

**Lemma 1 (mixtures).** Let $Z$ be a random string and $C$ a random variable with finitely many values. If $Z$ is uniform given its length conditioned on each value $C = c$, then $Z$ is uniform given its length.

*Proof.* For $z \in \{0,1\}^\ell$, $\Pr[Z = z, |Z| = \ell] = \sum_c \Pr[C = c] \Pr[|Z| = \ell \mid C = c]\, 2^{-\ell} = 2^{-\ell}\Pr[|Z| = \ell]$. $\square$

**Lemma 2 (one level).** Let $x \sim \mathcal{U}(N, k)$ with $N = 2M$ even, and let $a$ be the number of unequal pairs of $x$. Conditioned on $a$:

1. $u$ is uniform among the strings of length $M$ with $a$ ones;
2. $w$ is uniform on $\{0,1\}^a$;
3. $v$ has the distribution $\mathcal{U}(M - a, (k - a)/2)$;
4. $u$, $w$ and $v$ are independent.

*Proof.* Fix a string $u$ of length $M$ with $a$ ones. The strings $x$ of weight $k$ whose pair XORs are $u$ are given by a choice of $01$ or $10$ for each of the $a$ unequal pairs, and a choice of $00$ or $11$ for each of the $M - a$ equal pairs. The unequal pairs contribute $a$ ones, so exactly $(k - a)/2$ of the equal pairs must be $11$. The map $x \mapsto (w, v)$ is a bijection from this set of strings onto $\{0,1\}^a \times \{v \in \{0,1\}^{M-a} : v \text{ has } (k-a)/2 \text{ ones}\}$: $w$ lists the first bit of each unequal pair, and $v$ lists the bit of each equal pair. So the set has $2^a \binom{M-a}{(k-a)/2}$ elements, a number that depends on $u$ only through $a$. Since $x$ is uniform, this gives (1). It also shows that, given $u$, the pair $(w, v)$ is uniform on the product set, so $w$ and $v$ are independent with the distributions of (2) and (3). This conditional distribution depends only on $a$, so given $a$, $(w, v)$ is independent of $u$, which gives (4). $\square$

**Theorem.** For every $\nu \ge 0$, $N \ge 0$ and $k$ with $0 \le k \le N$, if $x \sim \mathcal{U}(N, k)$ then $\Psi_\nu(x)$ is uniform given its length.

*Proof.* By induction on $N$, for all $\nu$ at once. If $N < 2$ or $\nu = 0$ the output is empty, which is uniform on $\{0,1\}^0$. Let $N \ge 2$ and $\nu \ge 1$.

*Odd $N$.* The last bit is ignored. Conditioned on the last bit $b$, the first $N - 1$ bits have the distribution $\mathcal{U}(N - 1, k - b)$, and $N - 1$ is even. So by Lemma 1, it is enough to treat even $N$.

*Even $N = 2M$.* Condition on $a$ and then on the lengths $\ell_1 = |\Psi_{\nu-1}(u)|$ and $\ell_2 = |\Psi_{\nu-1}(v)|$. The event $\ell_1 = $ const depends only on $u$, and the event $\ell_2 = $ const depends only on $v$. By Lemma 2 (4), $u$, $w$ and $v$ stay independent under these conditions. By Lemma 2 (1) and (3), $u$ and $v$ have distributions of the form $\mathcal{U}(N', k')$ with $N' \le M < N$, so by the induction hypothesis $\Psi_{\nu-1}(u)$ is uniform on $\{0,1\}^{\ell_1}$ and $\Psi_{\nu-1}(v)$ is uniform on $\{0,1\}^{\ell_2}$ under these conditions. (Strictly, the hypothesis is about $\mathcal{U}(N', k')$, and $u$ is uniform among strings of length $M$ and weight $a$, which is $\mathcal{U}(M, a)$.) By Lemma 2 (2), $w$ is uniform on $\{0,1\}^a$ and independent of the other two parts. The concatenation of independent uniform strings of fixed lengths $a$, $\ell_1$, $\ell_2$ is uniform on $\{0,1\}^{a + \ell_1 + \ell_2}$. So, conditioned on $(a, \ell_1, \ell_2)$, $\Psi_\nu(x)$ is uniform given its length, and by Lemma 1 it is uniform given its length without the conditioning. $\square$

**Corollary (the i.i.d. case).** If $x_1, \ldots, x_n$ are independent with $\Pr[x_i = 1] = p \in (0, 1)$, then for every $\nu$, $\Psi_\nu(x)$ is uniform given its length. In particular this holds for VON-NEUMANN ($\nu = 1$) and for PERES without a cutoff.

*Proof.* The probability of a string of weight $k$ is $p^k(1-p)^{n-k}$, which depends only on $k$. So, conditioned on the weight $k$, $x \sim \mathcal{U}(n, k)$. Apply the theorem and Lemma 1 with $C$ the weight. $\square$

**Direct proof for VON-NEUMANN.** The proof above covers $\nu = 1$, but there is a shorter argument for i.i.d. input. Condition on the set $I$ of indices $i$ with $x_{2i-1} \ne x_{2i}$. The pairs are independent, and for $i \in I$ the pair is $10$ with probability $pq/(pq + qp) = 1/2$ and $01$ with probability $1/2$, independently for different $i$. The output is $(x_{2i-1})_{i \in I}$ in order, so given $I$ it is uniform on $\{0,1\}^{|I|}$, and Lemma 1 removes the conditioning. $\square$

**Remark (the order of the parts).** The proof of the theorem uses only that, given the lengths, the three parts are independent and uniform. So any concatenation order of $w$, $\Psi_{\nu-1}(u)$ and $\Psi_{\nu-1}(v)$ fixed in advance also gives an exact output.
