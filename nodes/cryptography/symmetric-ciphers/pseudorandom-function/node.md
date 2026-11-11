---
tag: T4RNPC
kind: definition
slug: pseudorandom-function
name: Pseudorandom function
aliases:
- PRF
area: cryptography/symmetric-ciphers
level: advanced
summary: A keyed function family that no efficient adversary with oracle access can tell from a uniformly random function. GGM (1986) builds one from any pseudorandom generator.
prereqs: [computational-indistinguishability, pseudorandom-generator]
see_also: [pseudorandom-permutation, prp-prf-switching-lemma, luby-rackoff-theorem, block-cipher, message-authentication-code, hmac, semantic-security, hybrid-argument]
sources:
  - paper: doi:10.1145/6490.6503
    title: Oded Goldreich, Shafi Goldwasser and Silvio Micali, How to construct random functions, Journal of the ACM 33(4), 1986
    locator: the definition of a pseudorandom function family and the tree construction from a pseudorandom generator
  - paper: doi:10.1006/jcss.1999.1694
    title: Mihir Bellare, Joe Kilian and Phillip Rogaway, The security of the cipher block chaining message authentication code, Journal of Computer and System Sciences 61(3), 2000
    locator: the concrete definitions of PRF and PRP security with resources t and q
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 3.6, pseudorandom functions and the proof of the GGM construction
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the sections on pseudorandom functions, CPA-secure encryption from a PRF, and the GGM construction
---

A pseudorandom function (PRF) is a family of keyed functions $F_K : D \to R$ such that no efficient adversary, given an oracle, can tell whether the oracle computes $F_K$ for a random secret key $K$ or a function chosen uniformly from all functions $D \to R$. Goldreich, Goldwasser and Micali defined it in 1984 (journal version 1986) and built one from any [pseudorandom generator](/pseudorandom-generator/). A PRF is the basic tool of symmetric cryptography: it gives [message authentication codes](/message-authentication-code/), encryption that is [semantically secure](/semantic-security/) under chosen-plaintext attack, and key derivation. A block cipher is modeled as a [pseudorandom permutation](/pseudorandom-permutation/), and by the [switching lemma](/prp-prf-switching-lemma/) it is also a PRF up to the birthday bound.

## Definition

**Function family.** Let $F : \{0,1\}^k \times \{0,1\}^\ell \to \{0,1\}^L$ be a function that a deterministic algorithm computes in polynomial time. For a key $K$ write $F_K = F(K, \cdot)$. Let $\mathrm{Func}(\ell, L)$ be the set of all functions from $\{0,1\}^\ell$ to $\{0,1\}^L$; it has $2^{L 2^\ell}$ members.

**The PRF game.** An adversary $A$ plays against a challenger.

1. The challenger picks a bit $b$ uniformly.
2. If $b = 1$, it picks $K$ uniformly from $\{0,1\}^k$ and sets $O = F_K$. If $b = 0$, it picks $f$ uniformly from $\mathrm{Func}(\ell, L)$ and sets $O = f$. In practice $f$ is sampled lazily: on a new query $x$, choose $f(x)$ uniformly and store it; on a repeated query, return the stored value.
3. $A$ queries $O$ on inputs $x_1, x_2, \ldots$ of its choice, adaptively, and gets $O(x_i)$. It never sees $K$.
4. $A$ outputs a bit $b'$.

The advantage of $A$ is

$$\mathrm{Adv}^{\mathrm{prf}}_F(A) = \Bigl| \Pr_K\bigl[A^{F_K} = 1\bigr] - \Pr_f\bigl[A^{f} = 1\bigr] \Bigr| = \bigl| 2 \Pr[b' = b] - 1 \bigr|.$$

**Security.** In the asymptotic form, with $k$ the security parameter and $\ell, L$ polynomial in $k$, $F$ is a PRF if $\mathrm{Adv}^{\mathrm{prf}}_F(A)$ is negligible in $k$ for every probabilistic polynomial-time $A$. In the concrete form of Bellare, Kilian and Rogaway, $F$ is a $(t, q, \varepsilon)$-PRF if every $A$ that runs in time at most $t$ and makes at most $q$ queries has advantage at most $\varepsilon$. Concrete statements are the ones used for fixed ciphers such as AES, where no asymptotic parameter exists.

**The GGM construction.** Let $G : \{0,1\}^n \to \{0,1\}^{2n}$ be a length-doubling pseudorandom generator, and write $G(s) = G_0(s) \| G_1(s)$ with halves of $n$ bits. For a key $K \in \{0,1\}^n$ and an input $x = x_1 x_2 \cdots x_\ell$, define

$$F_K(x) = G_{x_\ell}\bigl(\cdots G_{x_2}(G_{x_1}(K)) \cdots\bigr).$$

This is a walk down a binary tree of depth $\ell$: the root holds $K$, each node with label $s$ has children $G_0(s)$ and $G_1(s)$, and $F_K(x)$ is the label of leaf $x$.

**Theorem (Goldreich, Goldwasser and Micali).** If $G$ is a $(t, \varepsilon)$-secure PRG, then the GGM family is a $(t', q, \ell q \varepsilon)$-PRF, where $t' = t - O(\ell q \cdot T_G)$ and $T_G$ is the time to evaluate $G$.

*Proof sketch.* Define hybrids $H_0, \ldots, H_\ell$. In $H_i$, the labels at depth $i$ are uniform and independent, sampled lazily, and deeper labels follow the GGM rule from them. $H_0$ is the real GGM function with a random root, and $H_\ell$ is a uniformly random function, because then the leaves themselves are independent and uniform. An adversary that tells $H_i$ from $H_{i+1}$ with advantage $\delta$ gives a distinguisher $B$ that receives $q$ strings of $2n$ bits, each either $G(s_j)$ for a fresh uniform $s_j$ or uniform. $B$ runs $A$, and when $A$'s query needs the children of a new node at depth $i$, $B$ uses its next string as the pair of children labels; it computes the rest of the path with $G$. With PRG outputs, $A$ sees $H_i$, and with uniform strings, $H_{i+1}$. At most $q$ nodes at depth $i$ are touched. A second [hybrid argument](/hybrid-argument/) over the $q$ strings turns $B$ into a distinguisher for one output of $G$ with advantage $\delta/q$. So $\delta \le q\varepsilon$, and summing over the $\ell$ levels gives $\mathrm{Adv}^{\mathrm{prf}} \le \ell q \varepsilon$. $\square$

So one-way functions imply PRFs, since they imply PRGs by the theorem of Håstad, Impagliazzo, Levin and Luby. GGM is slow, one PRG call per input bit, and is used in theory and in puncturable PRFs rather than in practice.

## Examples and non-examples

- **A block cipher, used as a PRF.** If $E$ is a $(t, q, \varepsilon)$-secure PRP on $n$-bit blocks, then $E$ is a $(t, q, \varepsilon + q(q-1)/2^{n+1})$-PRF by the [switching lemma](/prp-prf-switching-lemma/). For AES with $n = 128$, the extra term stays below $2^{-32}$ for $q \le 2^{48}$.
- **HMAC.** HMAC-SHA-256 is assumed to be a PRF with key and input of any length. It is the standard PRF of TLS 1.3 and HKDF.
- **The GGM tree.** A PRF from any PRG, as above.
- **Non-example: XOR with the key.** $F_K(x) = x \oplus K$. Two queries $x, x'$ give $F_K(x) \oplus F_K(x') = x \oplus x'$, which a random function satisfies with probability $2^{-L}$. Advantage $1 - 2^{-L}$.
- **Non-example: a function that ignores part of its input.** $F_K(x) = G(K)$ for a PRG $G$. Two different queries give equal answers. Advantage $1 - 2^{-L}$.
- **Non-example: a sum of block cipher calls.** $F_K(x \| y) = E_K(x) \oplus E_K(y)$. The query $x \| x$ always gives 0. Advantage $1 - 2^{-n}$.
- **Non-example: a permutation with a small block.** Any family of permutations on $n$ bits is told apart from a random function by $q \approx 2^{n/2}$ queries: a collision $f(x) = f(x')$ with $x \ne x'$ appears with constant probability for a random function and never for a permutation. So a 64-bit block cipher is a poor PRF after about $2^{32}$ queries.
- **Non-example: a public function.** $F_K(x) = \mathrm{SHA\text{-}256}(x)$, which does not use $K$. The adversary computes $\mathrm{SHA\text{-}256}(x)$ itself and compares.

## Related definitions

- **[Pseudorandom permutation](/pseudorandom-permutation/).** The same game with a random permutation in place of a random function, and $F_K$ a permutation. The strong form also gives the inverse oracle.
- **Pseudorandom generator.** A PRG $G : \{0,1\}^n \to \{0,1\}^{m}$ is a PRF with an input space of one point and a long output. A PRF gives a PRG by $G(K) = F_K(1) \| F_K(2) \| \cdots$.
- **Weak PRF.** The adversary sees $F_K$ only at uniformly random inputs that it does not choose. Weaker, and enough for some uses.
- **Message authentication code.** A PRF with $L \ge 80$ or so is a secure MAC: $\mathrm{Tag}_K(m) = F_K(m)$, and a forgery succeeds with probability at most $\varepsilon + 2^{-L}$.
- **CPA-secure encryption.** $\mathrm{Enc}_K(m) = (r, F_K(r) \oplus m)$ for a uniform $r$ is IND-CPA secure if $F$ is a PRF; the loss is about $q^2/2^{\ell}$ for repeated $r$.
- **Key derivation and puncturable PRFs.** HKDF uses HMAC as a PRF. A puncturable PRF, such as GGM, allows a key that evaluates $F$ at all points but one.

## References
