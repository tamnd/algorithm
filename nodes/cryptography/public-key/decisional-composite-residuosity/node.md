---
tag: NDWVB4
kind: definition
slug: decisional-composite-residuosity
name: Decisional composite residuosity assumption
aliases:
- DCRA
- DCR assumption
area: cryptography/public-key
level: advanced
summary: "The assumption that, for an RSA modulus N, the N-th powers modulo N^2 cannot be told apart from uniform units modulo N^2. It underlies Paillier encryption and is no harder than factoring."
prereqs: [computational-hardness-assumption, carmichael-function, chinese-remainder-theorem]
see_also: [paillier-cryptosystem, quadratic-residuosity-problem, rsa-problem, integer-factorization, decisional-diffie-hellman, okamoto-uchiyama-cryptosystem, homomorphic-encryption]
sources:
  - paper: "Pascal Paillier, Public-key cryptosystems based on composite degree residuosity classes, Eurocrypt 1999, LNCS 1592, pages 223 to 238"
    locator: Section 2 (N-th residues modulo N^2, the isomorphism with Z_N x Z_N^*, the classes), Section 3 (the problems Class and D-Class, random self-reducibility, Class no harder than RSA with exponent N), and the statement of the DCR assumption
  - paper: "Ivan Damgard and Mads Jurik, A generalisation, a simplification and some applications of Paillier's probabilistic public-key system, PKC 2001, LNCS 1992, pages 119 to 136"
    locator: the proof that the security of the scheme modulo N^(s+1) follows from DCR for every s
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the section on the Paillier encryption scheme (the structure of Z_(N^2)^* and the decisional composite residuosity problem)
---

The decisional composite residuosity (DCR) assumption says that, for a random RSA modulus $N = pq$, no efficient algorithm can tell an $N$-th power modulo $N^2$ from a uniform element of $\mathbb{Z}_{N^2}^*$. Pascal Paillier stated it in 1999, and the [Paillier cryptosystem](/paillier-cryptosystem/) is [IND-CPA](/ind-cpa-security/) secure exactly under it. It is a [computational hardness assumption](/computational-hardness-assumption/) of the same family as the [quadratic residuosity problem](/quadratic-residuosity-problem/), but for residues of degree $N$ modulo $N^2$ instead of degree 2 modulo $N$. Anyone who can factor $N$ can decide it, and no converse reduction is known.

**Notation.** $\kappa$ is the security parameter (the page uses $\lambda$ for the Carmichael function, as Paillier does). GenModulus$(\kappa)$ outputs $N = pq$ with $p \ne q$ primes of $\kappa$ binary digits and $\gcd(N, (p-1)(q-1)) = 1$; on this page $q$ is a prime. $\varphi(N) = (p-1)(q-1)$ and $\lambda = \operatorname{lcm}(p-1, q-1)$. $\mathcal{A}$ is an adversary, $t$ its running time, and $\mathrm{Adv}$ its advantage.

## Definition

An element $z \in \mathbb{Z}_{N^2}^*$ is an **$N$-th residue** modulo $N^2$ if $z \equiv y^N \pmod{N^2}$ for some $y \in \mathbb{Z}_{N^2}^*$. The set of $N$-th residues is a subgroup of $\mathbb{Z}_{N^2}^*$; write it $\mathcal{R}_N$.

**DCR assumption.** For every probabilistic polynomial time adversary $\mathcal{A}$, the advantage

$$\mathrm{Adv}^{\mathrm{dcr}}(\mathcal{A}) = \Bigl|\Pr\bigl[\mathcal{A}(N, y^N \bmod N^2) = 1\bigr] - \Pr\bigl[\mathcal{A}(N, z) = 1\bigr]\Bigr|$$

is a negligible function of $\kappa$. The probabilities are over $N \leftarrow \text{GenModulus}(\kappa)$, $y$ and $z$ uniform in $\mathbb{Z}_{N^2}^*$, and the coins of $\mathcal{A}$. A concrete form states that $\mathrm{Adv}^{\mathrm{dcr}}(\mathcal{A}) \le \varepsilon$ for all $\mathcal{A}$ that run in time $t$.

### The structure behind it

**Theorem.** The map $f(x, r) = (1 + N)^x r^N \bmod N^2$ is a group isomorphism from $\mathbb{Z}_N \times \mathbb{Z}_N^*$ (addition in the first factor, multiplication in the second) onto $\mathbb{Z}_{N^2}^*$. The $N$-th residues are exactly the images $f(0, r)$, so $|\mathcal{R}_N| = \varphi(N)$ and $\mathcal{R}_N$ has index $N$.

*Proof.* $f$ is well defined: $(1+N)^x \equiv 1 + xN \pmod{N^2}$ by the binomial theorem, so it depends only on $x \bmod N$; and $(r + kN)^N \equiv r^N \pmod{N^2}$, because each term after the first has the factor $N \cdot N$, so $r^N$ depends only on $r \bmod N$. Both factors are units, and $f$ is a homomorphism because $(1+N)^{x}(1+N)^{x'} = (1+N)^{x + x'}$ and $r^N s^N = (rs)^N$.

$f$ is injective. Assume $(1+N)^x r^N \equiv 1 \pmod{N^2}$. Modulo $N$ this gives $r^N \equiv 1 \pmod N$. The order of $r$ in $\mathbb{Z}_N^*$ divides $\varphi(N)$ and $N$, and $\gcd(N, \varphi(N)) = 1$, so $r \equiv 1 \pmod N$. Then $r^N \equiv 1 \pmod{N^2}$ by the binomial theorem, so $(1+N)^x \equiv 1 + xN \equiv 1 \pmod{N^2}$, and $x \equiv 0 \pmod N$.

The two groups have the same order $N\varphi(N)$, so the injective map $f$ is onto. Finally, for $y = f(a, s)$ we get $y^N = f(Na \bmod N, s^N) = f(0, s^N)$, and every $f(0, r)$ is $r^N$. So $\mathcal{R}_N = f(\{0\} \times \mathbb{Z}_N^*)$, a set of $\varphi(N)$ elements. $\square$

So every $w \in \mathbb{Z}_{N^2}^*$ has a unique **class** $x = [w] \in \mathbb{Z}_N$ with $w = (1+N)^x r^N$, and DCR says that the class $0$ cannot be told apart from a uniform class. Paillier defines classes for any base $g$ whose order is a nonzero multiple of $N$; the base $1 + N$ is one such $g$.

### The problems around DCR

Paillier names three problems for a modulus $N$ and a base $g$:

- **Class$[N]$** (the composite residuosity class problem): given $w$, compute $[w]_g$. This is the one-wayness of the Paillier cryptosystem.
- **D-Class$[N]$**: given $w$ and $x$, decide whether $[w]_g = x$.
- **CR$[N]$** (decisional composite residuosity): given $w$, decide whether $w \in \mathcal{R}_N$. This is DCR.

Their relations, with each step proved here:

1. **DCR and D-Class are equivalent.** DCR is the case $x = 0$ of D-Class. Conversely, $[w]_g = x$ holds exactly when $w g^{-x} \in \mathcal{R}_N$, so one DCR query decides D-Class.
2. **D-Class is no harder than Class.** Compute $[w]_g$ and compare it with $x$.
3. **Class is no harder than RSA with exponent $N$.** For $g = 1 + N$: $w \bmod N = r^N \bmod N$, so an algorithm that inverts $s \mapsto s^N \bmod N$ gives $r \bmod N$. Then $w \cdot (r^N)^{-1} \bmod N^2 = 1 + xN$, and $x = L(\cdot)$ with $L(u) = (u-1)/N$. This is Paillier's result Class$[N] \Leftarrow$ RSA$[N, N]$.
4. **RSA with exponent $N$ is no harder than factoring.** With $p$ and $q$, invert $N$ modulo $\varphi(N)$ as in [RSA](/rsa-cryptosystem/) decryption. So all three problems are no harder than [factoring](/integer-factorization/).
5. **The direct test with the factors.** For $w = f(x, r)$, $w^\lambda = (1 + x\lambda N) r^{N\lambda} \equiv 1 + x\lambda N \pmod{N^2}$, because $r^{N\lambda} \equiv 1$. Since $\gcd(\lambda, N) = 1$, $w^\lambda \equiv 1 \pmod{N^2}$ if and only if $x = 0$. This is the trapdoor of the Paillier cryptosystem.

No reduction in the other direction is known: it is open whether DCR, or even Class, is as hard as factoring. The chain is DCR $\le$ Class $\le$ RSA$[N, N] \le$ factoring, where $\le$ means "no harder than".

**Random self-reducibility.** Given $w$, the value $w \cdot s^N$ for a uniform $s \in \mathbb{Z}_N^*$ is a uniform element of the coset $w \mathcal{R}_N$, and it has the same class as $w$. So, for a fixed $N$, any single instance $w$ turns into a uniform instance of the same class, and a distinguisher that works on uniform inputs also works, with repeated rerandomized queries, on each fixed input. Paillier also proves that Class is random self-reducible over $w$ and over $g$, so its hardness does not depend on the choice of $g$.

**Variants.** Damgard and Jurik (2001) use the group $\mathbb{Z}_{N^{s+1}}^*$ and the $N^s$-th residues, and show that the semantic security of their scheme for every $s$ follows from DCR itself.

## Examples and non-examples

**A tiny modulus.** Take $N = 15 = 3 \cdot 5$, so $N^2 = 225$, $|\mathbb{Z}_{225}^*| = 120$, $\varphi(15) = 8$ and $\lambda = \operatorname{lcm}(2, 4) = 4$. The 15-th residues modulo 225 are the 8 values

$$\mathcal{R}_{15} = \{1, 26, 82, 107, 118, 143, 199, 224\},$$

exactly the $z$ with $z^4 \equiv 1 \pmod{225}$, as item 5 predicts. The element $16 = 1 + N$ is not a residue: $16^4 \bmod 225 = 61$. The classes with base $16$ are $[16] = 1$, $[31] = 2$, $[46] = 3$ and $[2] = 4$; for example $2 \cdot 16^{-4} \bmod 225$ lies in $\mathcal{R}_{15}$.

**The Paillier example.** For $N = 77$, $\lambda = 30$, the value $606 = 23^{77} \bmod 5929$ is a 77-th residue, and $606^{30} \bmod 5929 = 1$. The ciphertext $3840 = (1 + 42 \cdot 77) \cdot 606 \bmod 5929$ has class 42, and $3840^{30} \bmod 5929 = 2157 = 1 + 28 \cdot 77 \ne 1$. Item 3 recovers the class without $\lambda$ but with an RSA inverter: $23 = 3840^{1/77} \bmod 77$ (the inverse of 77 modulo $\varphi(77) = 60$ is 53), and $L(3840 \cdot 606^{-1} \bmod 5929) = 42$.

**Non-example: a prime modulus.** If $N$ is a prime, the same structure holds, with $\mathbb{Z}_{N^2}^* \cong \mathbb{Z}_N \times \mathbb{Z}_N^*$, but $\varphi(N) = N - 1$ is public. Then $z$ is an $N$-th residue if and only if $z^{N-1} \equiv 1 \pmod{N^2}$, a public test. For $N = 11$ the 10 residues modulo 121 are $\{1, 3, 9, 27, 40, 81, 94, 112, 118, 120\}$, and they are exactly the solutions of $z^{10} \equiv 1 \pmod{121}$. DCR needs a modulus whose factors are secret.

**Non-example: the class with the factors.** For a modulus whose factors are known, DCR is easy by item 5. So DCR is a statement about the gap between the holder of the factors and everybody else, as for every trapdoor assumption.

**Non-example: quadratic residuosity.** The [quadratic residuosity problem](/quadratic-residuosity-problem/) asks whether an element of $\mathbb{Z}_N^*$ with Jacobi symbol 1 is a square modulo $N$. It has the same shape (a subgroup membership problem with a factoring trapdoor) but another group and another degree, and it gives only one bit per ciphertext, in the [Goldwasser-Micali cryptosystem](/goldwasser-micali-cryptosystem/). No reduction between QR and DCR in either direction is known; both are no harder than factoring.

## Related definitions

- The [Paillier cryptosystem](/paillier-cryptosystem/) is IND-CPA exactly when DCR holds for its modulus; its page has the proof of the forward direction.
- The [quadratic residuosity problem](/quadratic-residuosity-problem/) is the degree 2 analogue modulo $N$.
- The [RSA problem](/rsa-problem/) with exponent $e = N$ bounds the class problem from above.
- The [decisional Diffie-Hellman assumption](/decisional-diffie-hellman/) is the analogous decisional assumption in a group of known prime order.
- The [Okamoto-Uchiyama cryptosystem](/okamoto-uchiyama-cryptosystem/) uses $N = p^2 q$ and the $p$-Sylow subgroup of $\mathbb{Z}_{p^2}^*$, with a related decisional assumption (the $p$-subgroup assumption).
- [Homomorphic encryption](/homomorphic-encryption/) lists the schemes built on DCR.

## References
