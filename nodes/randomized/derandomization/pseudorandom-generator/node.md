---
tag: PSZZSN
kind: definition
slug: pseudorandom-generator
name: Pseudorandom generator
aliases:
- PRG
area: randomized/derandomization
level: core
summary: A deterministic map from d-bit seeds to m-bit strings, m > d, that every test of size t tells from uniform with advantage at most ε. One bit of stretch gives any polynomial stretch.
prereqs: [computational-indistinguishability, boolean-circuit, randomized-algorithm]
see_also: [pseudorandom-generation, yao-next-bit-unpredictability, hill-prg-from-one-way-functions, nisan-wigderson-generator, nisan-prg, cryptographically-secure-prng, pseudorandom-function, one-way-function]
sources:
  - paper: doi:10.1109/SFCS.1982.45
    title: Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982
    locator: the definition of a generator that passes all polynomial-time statistical tests, and its use to save random bits
  - paper: doi:10.1137/0213053
    title: Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984
    locator: the iterated construction that outputs one hard bit per step
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 3, Pseudorandom Generators (the definition, and the amplification of the stretch from one bit to any polynomial)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (the (t, ε) definition of a generator and hybrid arguments)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 9 (secure pseudorandom generators and the stretch extension) and Chapter 20 (generators for derandomization)
---

A pseudorandom generator (PRG) is a deterministic function $G : \{0,1\}^d \to \{0,1\}^m$ with $m > d$ whose output on a uniform seed is [computationally indistinguishable](/computational-indistinguishability/) from uniform: every test of a stated size has advantage at most $\varepsilon$. The difference $m - d$ is the stretch. A generator with a stretch of only one bit already gives any polynomial stretch, with the error multiplied by the number of output bits. This page gives the definition in its concrete $(t, \varepsilon)$ form and in its asymptotic form, and proves the stretch extension; the map of the different kinds of generators is on [pseudorandom generation](/pseudorandom-generation/).

## Definition

Notation: $U_m$ is the uniform distribution on $\{0,1\}^m$. A *test* (or distinguisher) is a [Boolean circuit](/boolean-circuit/) $D : \{0,1\}^m \to \{0,1\}$, and its *advantage* on $G$ is

$$\operatorname{adv}_D(G) = \big| \Pr[D(G(U_d)) = 1] - \Pr[D(U_m) = 1] \big|.$$

**Concrete form.** $G : \{0,1\}^d \to \{0,1\}^m$ is a *$(t, \varepsilon)$-pseudorandom generator* if $\operatorname{adv}_D(G) \le \varepsilon$ for every circuit $D$ of size at most $t$. The *seed length* is $d$, the *output length* is $m$, and the *stretch* is $m - d$.

**Asymptotic form (cryptographic).** A family $G = \{G_n : \{0,1\}^n \to \{0,1\}^{\ell(n)}\}$ is a pseudorandom generator if

1. $G_n(s)$ is computable in time polynomial in $n$ by one algorithm;
2. $\ell(n) > n$ for every $n$;
3. for every probabilistic polynomial-time algorithm $D$ (or, in the non-uniform version, every family of circuits of polynomial size), $\operatorname{adv}_D(G_n)$ is a *negligible* function: smaller than $1/p(n)$ for each polynomial $p$ and all large $n$.

**Complexity-theoretic form.** For derandomization the generator may run in time $2^{O(d)}$, which is more than the tests, and it must fool circuits of size $m$ with error, say, $1/10$. This is the form of the [Nisan-Wigderson generator](/nisan-wigderson-generator/). The difference between the forms is the subject of [pseudorandom generation](/pseudorandom-generation/).

### Stretch extension

Write $G(x) = (G_0(x), G_1(x))$ for $G : \{0,1\}^n \to \{0,1\}^{n+1}$, where $G_0(x)$ is the first $n$ bits and $G_1(x)$ is the last bit. For $\ell \ge 1$ define $G^{(\ell)} : \{0,1\}^n \to \{0,1\}^\ell$ by

$$x_0 = x, \qquad b_i = G_1(x_{i-1}), \qquad x_i = G_0(x_{i-1}) \quad (i = 1, \ldots, \ell), \qquad G^{(\ell)}(x) = b_1 b_2 \cdots b_\ell,$$

and let $G^{(0)}$ have empty output.

**Theorem.** Let $G : \{0,1\}^n \to \{0,1\}^{n+1}$ be a $(t, \varepsilon)$-pseudorandom generator computed by a circuit of size $s_G$. Then for each $\ell$ with $\ell s_G < t$, $G^{(\ell)}$ is a $(t - \ell s_G, \ell \varepsilon)$-pseudorandom generator. In the asymptotic form: if a generator with $\ell(n) = n + 1$ exists, then for each polynomial $p(n) > n$ a generator with $\ell(n) = p(n)$ exists.

*Proof.* For $j = 0, \ldots, \ell$ let the hybrid $H_j$ be the distribution of $(u_1, \ldots, u_j, G^{(\ell - j)}(x))$, where $u_1, \ldots, u_j$ are uniform bits and $x$ is uniform in $\{0,1\}^n$, all independent. Then $H_0 = G^{(\ell)}(U_n)$ and $H_\ell = U_\ell$. Let $D$ be a circuit of size $t' \le t - \ell s_G$, and let $p_j = \Pr[D(H_j) = 1]$. Assume $|p_0 - p_\ell| > \ell \varepsilon$. Since $p_0 - p_\ell = \sum_{j=0}^{\ell-1} (p_j - p_{j+1})$, the triangle inequality gives a $j$ with $|p_j - p_{j+1}| > \varepsilon$.

Fix this $j$. For $u \in \{0,1\}^j$ define the circuit $C_u(y, b) = D(u, b, G^{(\ell - j - 1)}(y))$ on $y \in \{0,1\}^n$ and a bit $b$. If $(y, b) = G(x) = (G_0(x), G_1(x))$, the string $(u, G_1(x), G^{(\ell - j - 1)}(G_0(x)))$ equals $(u, G^{(\ell - j)}(x))$ by the definition of the iteration. So with $u$ uniform, $C_u(G(U_n))$ has the distribution of $D(H_j)$. If $(y, b)$ is uniform in $\{0,1\}^{n+1}$, then $(u, b, G^{(\ell - j - 1)}(y))$ has the distribution $H_{j+1}$. Hence

$$\Big| E_u\big[\Pr[C_u(G(U_n)) = 1] - \Pr[C_u(U_{n+1}) = 1]\big] \Big| = |p_j - p_{j+1}| > \varepsilon,$$

and some fixed $u$ has $\operatorname{adv}_{C_u}(G) > \varepsilon$. The circuit $C_u$ is $D$ with $u$ built in and $\ell - j - 1$ copies of the circuit of $G$, so its size is at most $t' + \ell s_G \le t$. This contradicts the hypothesis on $G$. So $|p_0 - p_\ell| \le \ell \varepsilon$ for every $D$ of size at most $t - \ell s_G$.

For the asymptotic form, take $\ell = p(n)$. The circuit of $G_n$ has polynomial size, so a polynomial-size test of $G^{(\ell)}$ gives a polynomial-size test of $G$ with advantage larger by a factor of at most $p(n)$. A negligible function times a polynomial is negligible. $\blacksquare$

The same proof works for a uniform test $D$: the reduction picks $j$ and $u$ at random instead of fixing them, and its advantage is $|p_0 - p_\ell| / \ell$ on average.

## Examples and non-examples

**Example (conditional).** Let $f$ be a [one-way](/one-way-function/) permutation of $\{0,1\}^n$. Then $G(x, r) = (f(x), r, \langle x, r \rangle)$, with $\langle x, r \rangle = \sum_i x_i r_i \bmod 2$, is a generator from $2n$ to $2n + 1$ bits. The first $2n$ bits are exactly uniform, and the last bit is the Goldreich-Levin [hard-core predicate](/hard-core-predicate/). The proof is on [HILL](/hill-prg-from-one-way-functions/). Stretch extension then gives the Blum-Micali-Yao generator.

**A trace of the stretch extension.** Take the toy $G_0(x) = (3x + 1) \bmod 8$ and $G_1(x) = $ the parity of the three bits of $x$, and start at $x_0 = 5$. This toy is not secure; it only shows the shape of the iteration.

| $i$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $x_{i-1}$ | 5 | 0 | 1 | 4 | 5 |
| $b_i = G_1(x_{i-1})$ | 0 | 0 | 1 | 1 | 0 |
| $x_i = G_0(x_{i-1})$ | 0 | 1 | 4 | 5 | 0 |

The state comes back to 5 after four steps, so the output has period 4. The state of any iteration has only $2^n$ values, so the period is at most $2^n$. This is one reason why a real seed must be long.

**Non-examples.**

- $G(s) = (s, \bigoplus_i s_i)$, the seed followed by its parity. The test "is the parity of all $n+1$ bits even?" is a circuit of size $O(n)$, accepts $G(U_n)$ always and $U_{n+1}$ with probability $1/2$. Advantage $1/2$.
- $G(s) = (s, s)$. The test "are the two halves equal?" has advantage $1 - 2^{-n}$.
- A [linear congruential generator](/pseudorandom-number-generator/) or the [Mersenne Twister](/mersenne-twister/). Their outputs are linear functions of the state over $\mathbb{Z}_M$ or over $\mathrm{GF}(2)$, so a few outputs determine all later ones by linear algebra. They pass many statistical tests, but they are not pseudorandom generators in this sense.
- Any $G$ with $m > d$, against all tests with no size bound: the test "is $z$ in the image of $G$?" has advantage at least $1 - 2^{d - m} \ge 1/2$. A generator is always pseudorandom only against a bounded class.

**A consequence.** If a cryptographic generator exists, then P $\ne$ NP: the image test "is there a seed $s$ with $G(s) = z$?" is in NP, so if P = NP it runs in polynomial time and has advantage at least $1/2$.

## Related definitions

- [Computational indistinguishability](/computational-indistinguishability/) is the general notion. A generator is a function whose output is indistinguishable from uniform.
- [Yao's theorem](/yao-next-bit-unpredictability/): pseudorandom is equivalent to next-bit unpredictable, with a loss of a factor $m$.
- [Pseudorandom generation](/pseudorandom-generation/) is the problem of building generators, with the kinds that differ in the tests and the run time.
- A [cryptographically secure PRNG](/cryptographically-secure-prng/) is the engineering object: it also asks for security after a leak of the state and for reseeding. Its formal core is the asymptotic form above.
- A [pseudorandom function](/pseudorandom-function/) gives exponentially many outputs with random access. The construction of Goldreich, Goldwasser and Micali builds one from a generator with stretch $2n$.
- A [hitting-set generator](/hitting-set-generator/) is the one-sided relative.
- A [randomness extractor](/randomness-extractor/) is the statistical relative: it fools all tests, but needs a weak random source as an extra input.

## References
