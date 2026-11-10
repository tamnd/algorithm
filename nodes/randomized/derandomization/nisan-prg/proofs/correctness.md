---
title: Nisan's generator computes its recursive definition and fools read-once branching programs
proves: [correctness]
status: full
---

This proof has two parts. Part 1 shows that the loop of lines L1 to L5 outputs the generator $G_\ell$ of the recursive definition. Part 2 shows that $G_\ell$ fools read-once branching programs, with an explicit error bound.

**Notation.** $K = 2^k$ and $\mathbb{F} = \mathrm{GF}(2^k)$. A hash function $h = (a, b) \in \mathbb{F}^2$ maps $y$ to $ay + b$. The recursive definition is

$$G_0(x) = x, \qquad G_i(x; h_1, \ldots, h_i) = G_{i-1}(x; h_1, \ldots, h_{i-1}) \circ G_{i-1}(h_i(x); h_1, \ldots, h_{i-1}),$$

where $\circ$ joins two lists of blocks. $G_i$ has $2^i$ blocks. For $j \in \{0, \ldots, 2^\ell - 1\}$ write $j = \sum_{i=1}^{\ell} j_i 2^{i-1}$ with bits $j_i \in \{0,1\}$.

## Part 1: the loop computes $G_\ell$

**Claim A.** Block $j$ of $G_\ell(x)$ is $h_1^{j_1} \circ h_2^{j_2} \circ \cdots \circ h_\ell^{j_\ell}(x)$, where $h^0$ is the identity and $h_\ell$ is applied first.

*Proof by induction on $\ell$.* For $\ell = 0$ the only block is $x$. For $\ell \ge 1$, if $j_\ell = 0$ then block $j$ is block $j$ of $G_{\ell-1}(x)$, and by induction it is $h_1^{j_1} \circ \cdots \circ h_{\ell-1}^{j_{\ell-1}}(x)$, which is the claim with $h_\ell^0$. If $j_\ell = 1$ then block $j$ is block $j - 2^{\ell-1}$ of $G_{\ell-1}(h_\ell(x))$, which by induction is $h_1^{j_1} \circ \cdots \circ h_{\ell-1}^{j_{\ell-1}}(h_\ell(x))$. $\square$

**Claim B.** After line L4 for index $j$, $B[j]$ equals block $j$ of $G_\ell(x)$.

*Proof by induction on $j$.* Line L1 sets $B[0] = x$, which is block 0 by Claim A. For $j \ge 1$, line L3 sets $i$ to the position of the lowest set bit of $j$, so $j_1 = \cdots = j_{i-1} = 0$ and $j_i = 1$. Let $j' = j - 2^{i-1}$. Then $j' < j$, $j'$ has the same bits as $j$ except $j'_i = 0$, and by induction $B[j'] = h_{i+1}^{j_{i+1}} \circ \cdots \circ h_\ell^{j_\ell}(x)$. Line L4 sets $B[j] = h_i(B[j'])$. Since $j_1, \ldots, j_{i-1}$ are 0, this is $h_1^{j_1} \circ \cdots \circ h_\ell^{j_\ell}(x)$, block $j$ by Claim A. $\square$

The loop runs over all $j$ from 1 to $2^\ell - 1$, so line L5 returns $G_\ell(x)$.

## Part 2: the generator fools read-once branching programs

**The model.** A read-once branching program of width $w$ and length $N = 2^\ell$ that reads blocks of $k$ bits has layers $0, \ldots, N$ of $w$ states each, a start state in layer 0, and for each $t \in \{1, \ldots, N\}$ a transition function $T_t : [w] \times \mathbb{F} \to [w]$ that takes a state of layer $t - 1$ and block $t$ to a state of layer $t$. Some states of layer $N$ accept. A bit-level program of width $w$ that reads $n$ bits once in a fixed order becomes such a program with $N = \lceil n/k \rceil$ by grouping $k$ consecutive layers into one.

For a segment of consecutive layers and a distribution $\mathcal{D}$ on the blocks of that segment, let $M_{\mathcal{D}}$ be the $w \times w$ matrix with entry $(u, v)$ equal to the probability that the segment, started at $u$ and fed $\mathcal{D}$, ends at $v$. Each row is a probability distribution. For two such matrices let $\|M - M'\| = \max_u \sum_v |M(u, v) - M'(u, v)|$. For stochastic matrices $A, A', B, B'$,

$$\|AB - A'B'\| \le \|A - A'\| \, \|B\| + \|A'\| \, \|B - B'\| = \|A - A'\| + \|B - B'\|, \tag{1}$$

because $\|\cdot\|$ is the norm induced by the $\ell_1$ norm on row vectors, and a stochastic matrix has norm 1.

**Lemma (mixing).** Let $A, B \subseteq \mathbb{F}$ have densities $\alpha = |A|/K$ and $\beta = |B|/K$, and let $h$ be uniform in $\mathbb{F}^2$. Then the random variable $Z = \Pr_x[x \in A \text{ and } h(x) \in B]$, with $x$ uniform in $\mathbb{F}$, has mean $\alpha\beta$ and variance $\alpha\beta(1-\beta)/K$. So for every $\varepsilon' > 0$,

$$\Pr_h\big[|Z - \alpha\beta| > \varepsilon'\big] \le \frac{\alpha\beta(1-\beta)}{\varepsilon'^2 K} \le \frac{\alpha\beta}{\varepsilon'^2 K}.$$

*Proof.* For $a, b$ uniform and $x_1 \ne x_2$, the pair $(h(x_1), h(x_2))$ is uniform on $\mathbb{F}^2$: the map $(a, b) \mapsto (a x_1 + b, a x_2 + b)$ is a bijection, because its determinant $x_1 - x_2$ is not zero. So the indicators $I_x = [h(x) \in B]$ for $x \in A$ are [pairwise independent](/pairwise-independence/) with mean $\beta$. $Z = \frac1K \sum_{x \in A} I_x$ has mean $\frac{|A|}{K}\beta = \alpha\beta$ and variance $\frac{1}{K^2}|A| \beta(1-\beta) = \alpha\beta(1-\beta)/K$. The tail bound is [Chebyshev's inequality](/chebyshev-inequality/). $\square$

**Theorem.** Let $P$ be a program as above, with $N = 2^\ell$. For every $\varepsilon' > 0$,

$$\big|\Pr[P(G_\ell(U)) = 1] - \Pr[P(U_{\mathbb{F}^N}) = 1]\big| \le (N - 1)\Big(w^2 \varepsilon' + \frac{w}{\varepsilon'^2 K}\Big),$$

where $U$ is a uniform seed $(x, h_1, \ldots, h_\ell)$ and $U_{\mathbb{F}^N}$ is $N$ uniform blocks.

*Proof.* At level $i \in \{1, \ldots, \ell\}$, cut the layers into $2^{\ell - i}$ segments of $2^i$ consecutive layers; segment $s$ covers the steps $s 2^i + 1, \ldots, (s+1) 2^i$. Level 0 has the $N$ single steps.

For fixed $h_1, \ldots, h_i$, let $M^{G}_{i,s}$ be the matrix of segment $s$ fed with $G_i(y; h_1, \ldots, h_i)$ for $y$ uniform in $\mathbb{F}$, and $M^{U}_{i,s}$ the matrix of the same segment fed with uniform blocks.

Segment $s$ at level $i$ is the union of two segments $L = 2s$ and $R = 2s + 1$ at level $i - 1$. For states $u, v, z$ let

$$A_{uv} = \{y : L \text{ fed } G_{i-1}(y) \text{ goes from } u \text{ to } v\}, \qquad B_{vz} = \{y : R \text{ fed } G_{i-1}(y) \text{ goes from } v \text{ to } z\},$$

with densities $\alpha_{uv} = M^G_{i-1,L}(u, v)$ and $\beta_{vz} = M^G_{i-1,R}(v, z)$. These sets depend only on $h_1, \ldots, h_{i-1}$. Since $G_i(y) = G_{i-1}(y) \circ G_{i-1}(h_i(y))$,

$$M^G_{i,s}(u, z) = \sum_v \Pr_y\big[y \in A_{uv} \text{ and } h_i(y) \in B_{vz}\big].$$

Call $h_i$ *good for segment $s$* if $|\Pr_y[y \in A_{uv}, h_i(y) \in B_{vz}] - \alpha_{uv}\beta_{vz}| \le \varepsilon'$ for all $u, v, z$. By the lemma and the union bound, with $h_1, \ldots, h_{i-1}$ fixed and $h_i$ uniform,

$$\Pr[h_i \text{ is not good for } s] \le \sum_{u, v, z} \frac{\alpha_{uv}\beta_{vz}}{\varepsilon'^2 K} = \frac{1}{\varepsilon'^2 K}\sum_u \sum_v \alpha_{uv} \sum_z \beta_{vz} = \frac{w}{\varepsilon'^2 K},$$

because each row of a stochastic matrix sums to 1. There are $\sum_{i=1}^{\ell} 2^{\ell-i} = N - 1$ pairs $(i, s)$, so all $h_i$ are good for all their segments except with probability at most $(N-1) w / (\varepsilon'^2 K)$.

Now assume all are good. Then for each $u$, $\sum_z |M^G_{i,s}(u,z) - (M^G_{i-1,L} M^G_{i-1,R})(u,z)| \le w \cdot w \varepsilon'$, so $\|M^G_{i,s} - M^G_{i-1,L} M^G_{i-1,R}\| \le w^2\varepsilon'$. Also $M^U_{i,s} = M^U_{i-1,L} M^U_{i-1,R}$, because uniform blocks on $L$ and $R$ are independent. With (1), the quantity $E_i = \max_s \|M^G_{i,s} - M^U_{i,s}\|$ satisfies

$$E_i \le w^2 \varepsilon' + E_{i-1} + E_{i-1}, \qquad E_0 = 0,$$

where $E_0 = 0$ because $G_0(y) = y$ is one uniform block. So $E_\ell \le (2^\ell - 1) w^2 \varepsilon'$. Level $\ell$ has the single segment $s = 0$, fed with $G_\ell(x)$ for $x$ uniform. For fixed good hash functions, $\Pr_x[P(G_\ell(x)) = 1] = \sum_{z \text{ accepting}} M^G_{\ell,0}(u_0, z)$, and the probability for uniform blocks is the same sum with $M^U_{\ell,0}$. The two differ by at most $E_\ell$.

Averaging over the hash functions, the difference is at most $\Pr[\text{not all good}] + E_\ell \le (N-1)\big(w/(\varepsilon'^2 K) + w^2 \varepsilon'\big)$. $\square$

**Corollary.** Take $\varepsilon' = (wK)^{-1/3}$. Both terms become $w^{5/3} K^{-1/3}$, and the error is at most $2(N-1) w^{5/3} 2^{-k/3}$. It is at most $\varepsilon$ when

$$k \ge 3 \log_2(2N/\varepsilon) + 5 \log_2 w.$$

The seed has $k(2\ell + 1) = O(\log N \cdot \log(N w/\varepsilon))$ bits. For a program of width $w \le n$ that reads $n$ bits, with $\varepsilon = 1/n$, this is $O(\log^2 n)$. $\blacksquare$
