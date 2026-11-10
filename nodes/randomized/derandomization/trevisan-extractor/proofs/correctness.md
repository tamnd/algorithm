---
title: Trevisan's extractor is an extractor when the code has small lists and the sets form a design
proves: [correctness]
status: full
---

The proof has three parts. Part 1 bounds the number of codewords near any word for a code whose codewords are almost orthogonal. Part 2 shows that the code of lines L5 to L7 has this property. Part 3 is the reconstruction argument for lines L1 to L4: if a test tells the output from uniform for many sources $x$, each such $x$ can be described with few bits, and there are not enough short descriptions.

**Notation.** A code is an injective map $C : \{0,1\}^n \to \{0,1\}^{2^\ell}$, with the positions of a codeword indexed by $z \in \{0,1\}^\ell$. For $y \in \{0,1\}^d$, $y|_S$ is the string of the bits of $y$ at the positions in $S$, in increasing order. Sets $S_1, \ldots, S_m \subseteq [d]$ form an *$(\ell, a)$ design* if $|S_i| = \ell$ and $|S_i \cap S_j| \le a$ for $i \ne j$. The extractor is

$$\mathrm{Ext}(x, y) = \big(C(x)_{y|_{S_1}}, \ldots, C(x)_{y|_{S_m}}\big).$$

The *agreement* of two words $u, v$ of the same length is the fraction of positions where they are equal.

## Part 1: few codewords near any word

**Lemma 1.** Let $C$ be a code in which any two different codewords agree on at most a fraction $\frac12 + \gamma$ of the positions, with $\gamma \ge 0$. Let $\delta > 0$ with $4\delta^2 > 2\gamma$. Then for every word $w$, at most $1/(4\delta^2 - 2\gamma)$ codewords have agreement at least $\frac12 + \delta$ with $w$.

*Proof.* Write words in $\pm 1$ form: a bit $b$ becomes $(-1)^b$, and for vectors $u, v$ of length $N = 2^\ell$ let $\langle u, v \rangle = \frac1N \sum_z u_z v_z$. Then $\langle u, v \rangle = 2\,(\text{agreement}) - 1$. Let $c_1, \ldots, c_L$ be the codewords with agreement at least $\frac12 + \delta$ with $w$. Then $\langle w, c_i \rangle \ge 2\delta$, $\langle c_i, c_i \rangle = 1$ and $\langle c_i, c_j \rangle \le 2\gamma$ for $i \ne j$. By the Cauchy-Schwarz inequality and $\langle w, w \rangle = 1$,

$$(2\delta L)^2 \le \Big\langle w, \sum_i c_i \Big\rangle^2 \le \Big\langle \sum_i c_i, \sum_i c_i \Big\rangle \le L + L(L - 1) \cdot 2\gamma.$$

Divide by $L$: $4\delta^2 L \le 1 + 2\gamma(L - 1)$, so $L(4\delta^2 - 2\gamma) \le 1 - 2\gamma \le 1$. $\square$

For the Hadamard code $C(x)_z = \langle x, z \rangle \bmod 2$, two different codewords agree on exactly half of the positions, because $\langle x \oplus x', z \rangle$ is a nonzero linear function of $z$. So $\gamma = 0$ and at most $1/(4\delta^2)$ codewords are within agreement $\frac12 + \delta$ of any word. This is the same bound that Parseval's identity gives.

## Part 2: the Reed-Solomon code concatenated with the Hadamard code

Let $t \ge 1$, let $n$ be a multiple of $t$ with $n/t \le 2^t$, and read $x$ as $n/t$ elements $x_0, x_1, \ldots$ of $\mathrm{GF}(2^t)$. Let $p_x(\alpha) = \sum_j x_j \alpha^j$. Line L5 splits $z \in \{0,1\}^{2t}$ into $\alpha, \beta \in \mathrm{GF}(2^t)$, line L6 computes $v = p_x(\alpha)$ by Horner's rule, and line L7 returns $C(x)_z = \langle v, \beta \rangle \bmod 2$, the inner product of the bit vectors. So $\ell = 2t$.

**Lemma 2.** For $x \ne x'$, the codewords $C(x)$ and $C(x')$ differ in at least $(2^t - n/t + 1) \cdot 2^{t-1}$ of the $2^{2t}$ positions. So they agree on at most a fraction $\frac12 + \gamma$ with $\gamma = (n/t - 1)/2^{t+1}$, and $C$ is injective.

*Proof.* $p_x - p_{x'}$ is a nonzero polynomial of degree less than $n/t$, so it has at most $n/t - 1$ roots, and $p_x(\alpha) \ne p_{x'}(\alpha)$ for at least $2^t - n/t + 1$ values of $\alpha$. For each such $\alpha$, $\beta \mapsto \langle p_x(\alpha) \oplus p_{x'}(\alpha), \beta \rangle$ is a nonzero linear function, so it is 1 for exactly $2^{t-1}$ values of $\beta$. The agreement is then at most $1 - (2^t - n/t + 1)2^{t-1}/2^{2t} = \frac12 + (n/t - 1)/2^{t+1}$. Since $n/t \le 2^t$, the number of differing positions is positive. $\square$

## Part 3: the reconstruction argument

**Theorem.** Let $C$ be a code such that, for every word $w$, at most $L$ codewords have agreement at least $\frac12 + \varepsilon/m$ with $w$. Let $S_1, \ldots, S_m$ be an $(\ell, a)$ design in $[d]$. Let

$$A = (m - 1)2^a + m + \lceil \log_2 m \rceil + 1 \qquad\text{and}\qquad k \ge A + \log_2 L + \log_2(1/\varepsilon).$$

Then $\mathrm{Ext}$ is a $(k, 2\varepsilon)$-extractor.

*Proof.* It is enough to check flat sources, because every source of min-entropy $k$ is a convex combination of flat ones and the distance is convex (see [randomness extractor](/randomness-extractor/)). Fix a test $T : \{0,1\}^m \to \{0,1\}$. For each $x$ let

$$g(x) = \Pr_y[T(\mathrm{Ext}(x, y)) = 1] - \Pr[T(U_m) = 1],$$

with $y$ uniform in $\{0,1\}^d$. Call $x$ *bad* if $|g(x)| > \varepsilon$.

*Step 1: a predictor for each bad $x$.* Fix a bad $x$. Let $b = 0$ if $g(x) > 0$ and $b = 1$ otherwise, and let $T' = T$ if $b = 0$ and $T' = 1 - T$ if $b = 1$. Let $o = \mathrm{Ext}(x, y)$ for uniform $y$, let $u$ be uniform in $\{0,1\}^m$ and independent, and let $p_j = \Pr[T'(o_1, \ldots, o_j, u_{j+1}, \ldots, u_m) = 1]$. Then $p_m - p_0 = |g(x)| > \varepsilon$, so the sum of the $m$ differences $p_j - p_{j-1}$ is more than $\varepsilon$, and some $i$ has $p_i - p_{i-1} > \varepsilon/m$. The predictor draws $r = (r_i, \ldots, r_m)$ uniform and outputs $r_i$ if $T'(o_{<i}, r) = 1$ and $1 - r_i$ otherwise. Let $q$ be the probability that $T'(o_{<i}, 1 - o_i, r_{i+1}, \ldots, r_m) = 1$. Since $r_i$ equals $o_i$ with probability $\frac12$, $p_{i-1} = \frac12 p_i + \frac12 q$, and the predictor is right with probability

$$\tfrac12 p_i + \tfrac12 (1 - q) = \tfrac12 + p_i - p_{i-1} > \tfrac12 + \tfrac{\varepsilon}{m}.$$

*Step 2: fix everything except the bits on $S_i$.* Write $y = (z, w)$ with $z = y|_{S_i} \in \{0,1\}^\ell$ and $w$ the other $d - \ell$ bits. They are independent and uniform. The success probability is an average over $(w, r)$ of the success over $z$, so there are fixed $w^*$ and $r^*$ with

$$\Pr_z\big[\text{predictor with } w^*, r^* \text{ outputs } C(x)_z\big] > \tfrac12 + \tfrac{\varepsilon}{m}.$$

With $w^*$ fixed, output bit $j$ is $C(x)_{y|_{S_j}}$, and $y|_{S_j}$ depends on $z$ only through the bits of $z$ at the positions of $S_i \cap S_j$. So $o_j = g_j(z|_{S_i \cap S_j})$ for a function $g_j$ on at most $a$ bits, which is a table of at most $2^a$ bits.

*Step 3: a short description.* Define the word $R$ on $\{0,1\}^\ell$ by

$$R(z) = \begin{cases} r^*_i & \text{if } T'\big(g_1(z), \ldots, g_{i-1}(z), r^*\big) = 1,\\ 1 - r^*_i & \text{otherwise.}\end{cases}$$

By Step 2, $R$ has agreement more than $\frac12 + \varepsilon/m$ with $C(x)$. Given $T$ and the design, $R$ is determined by the string $\sigma = (i, b, r^*, g_1, \ldots, g_{i-1})$: $i$ takes $\lceil \log_2 m \rceil$ bits, $b$ one bit, $r^*$ at most $m$ bits, and the tables at most $(m - 1)2^a$ bits, because their sizes depend only on $i$ and the design. So there are at most $2^A$ possible words $R$. The source $x$ is not part of $\sigma$.

*Step 4: counting.* Each bad $x$ is one of the at most $L$ messages whose codeword has agreement at least $\frac12 + \varepsilon/m$ with the word $R$ of some $\sigma$, and $C$ is injective. So there are at most $2^A L$ bad $x$. Now let $X$ be flat on a set of $2^k$ strings. Then

$$\big|\Pr[T(\mathrm{Ext}(X, U_d)) = 1] - \Pr[T(U_m) = 1]\big| = \big|\mathbb{E}_X[g(X)]\big| \le \Pr[X \text{ bad}] + \varepsilon \le \frac{2^A L}{2^k} + \varepsilon \le 2\varepsilon,$$

using $|g(x)| \le 1$ for the bad $x$, $|g(x)| \le \varepsilon$ for the others, and $2^A L \le \varepsilon 2^k$. This holds for every test $T$, so $\Delta(\mathrm{Ext}(X, U_d), U_m) \le 2\varepsilon$. $\blacksquare$

**The algorithm computes this function.** Line L1 runs over the sets of the design, line L2 forms $y|_{S_i}$, and line L3 calls lines L5 to L7, which return bit $y|_{S_i}$ of $C(x)$ by the definition in Part 2. Line L4 returns the $m$ bits in order. So TREVISAN outputs $\mathrm{Ext}(x, y)$.

**Putting the parts together.** With the code of Part 2 and $\delta = \varepsilon/m$, Lemma 1 gives $L \le 1/(4\delta^2 - 2\gamma)$ as soon as $2^{t+1} \cdot 4\delta^2 > 2(n/t - 1)$. If $2^{t+1}\delta^2 \ge n/t$, then $2\gamma \le 2\delta^2$ and $L \le m^2/(2\varepsilon^2)$, so $t = \log_2(n m^2/\varepsilon^2) + O(1)$ suffices, and $\ell = 2t = O(\log(n/\varepsilon))$ when $m \le n$. The theorem then needs $k \ge (m - 1)2^a + m + O(\log(m/\varepsilon))$.
