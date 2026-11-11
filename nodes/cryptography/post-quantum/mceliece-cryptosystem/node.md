---
tag: 060YA3
kind: algorithm
slug: mceliece-cryptosystem
name: McEliece cryptosystem
aliases:
- McEliece
- Classic McEliece
- Goppa code cryptosystem
area: cryptography/post-quantum
level: advanced
summary: The first code-based public-key scheme (1978). The public key is a scrambled generator matrix of a binary Goppa code, a ciphertext is mG' + e, and only the owner can decode.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, t: the number of errors, m: "the degree of the field GF(2^m)"}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 1978
  people: [Robert J. McEliece]
  note: McEliece proposed the scheme in a JPL progress report in 1978, with a Goppa code of length 1024 that corrects 50 errors. Classic McEliece, its KEM form, was a round 4 candidate in the NIST process.
prereqs: [goppa-code, code-based-cryptography, syndrome-decoding-problem]
see_also: [niederreiter-cryptosystem, information-set-decoding, key-encapsulation-mechanism, reed-solomon-code, bike, hqc, polynomial-extended-euclidean-algorithm, chien-search]
sources:
  - paper: "Robert J. McEliece, A public-key cryptosystem based on algebraic coding theory, DSN Progress Report 42-44, Jet Propulsion Laboratory, pages 114 to 116, 1978"
    locator: the whole report (the key G' = SGP, encryption c = mG' + e, decryption with the Goppa decoder, and the parameters n = 1024, k = 524, t = 50)
  - paper: "Nicholas J. Patterson, The algebraic decoding of Goppa codes, IEEE Transactions on Information Theory 21(2), pages 203 to 207, 1975"
    locator: the whole paper (decoding t errors of a binary Goppa code with a square root modulo g and the key equation)
  - url: "https://classic.mceliece.org/"
    title: "Daniel J. Bernstein, Tung Chou, Tanja Lange and others, Classic McEliece: conservative code-based cryptography, round 4 submission, October 2022"
    locator: the cryptosystem specification (the Niederreiter form, the KEM with SHAKE256, and the parameter set mceliece348864 with m = 12, n = 3488, t = 64)
  - url: "https://doi.org/10.6028/NIST.IR.8545"
    title: NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025
    locator: Section 2.3 and Section 3.3 (Classic McEliece is not selected, and it is under consideration at ISO), Table 8 (an encapsulation key of 261120 bytes for mceliece348864)
  - paper: "Vladimir M. Sidelnikov and Sergey O. Shestakov, On insecurity of cryptosystems based on generalized Reed-Solomon codes, Discrete Mathematics and Applications 2(4), pages 439 to 444, 1992"
    locator: the whole paper (key recovery when the hidden code is a generalized Reed-Solomon code)
  - paper: "Jean-Charles Faugère, Ayoub Otmani, Ludovic Perret and Jean-Pierre Tillich, Algebraic cryptanalysis of McEliece variants with compact keys, Eurocrypt 2010, LNCS 6110, pages 279 to 298"
    locator: the whole paper (key recovery for quasi-cyclic and quasi-dyadic variants by solving an algebraic system)
  - paper: "Thomas A. Berson, Failure of the McEliece public-key cryptosystem under message-resend and related-message attack, Crypto 1997, LNCS 1294, pages 213 to 220"
    locator: the whole paper (the plain scheme is malleable and leaks under related messages)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Attacking and defending the McEliece cryptosystem, PQCrypto 2008, LNCS 5299, pages 31 to 46"
    locator: the whole paper (an information set decoding attack that breaks the original parameters, and new parameter proposals)
  - paper: "Yuan Xing Li, Robert H. Deng and Xin Mei Wang, On the equivalence of McEliece's and Niederreiter's public-key cryptosystems, IEEE Transactions on Information Theory 40(1), pages 271 to 273, 1994"
    locator: the whole paper (the two forms have equivalent security for the same code)
  - paper: "Kazukuni Kobara and Hideki Imai, Semantically secure McEliece public-key cryptosystems: conversions for McEliece PKC, PKC 2001, LNCS 1992, pages 19 to 35"
    locator: the whole paper (conversions of the plain scheme to IND-CCA2 security)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (Goppa codes, Patterson's algorithm, and the attacks)
---

The McEliece cryptosystem is the first public-key encryption scheme based on error-correcting codes. Robert McEliece proposed it in 1978. The private key is a binary [Goppa code](/goppa-code/) that corrects $t$ errors with a fast decoder. The public key is a generator matrix of the same code, hidden by a random change of basis $S$ and a random permutation $P$ of the positions: $G' = SGP$. To encrypt a message $m$, compute $c = mG' + e$ with a random error $e$ of weight $t$. To decrypt, undo $P$, remove the error with Patterson's algorithm, and undo $S$. An attacker who sees only $G'$ must solve the [syndrome decoding problem](/syndrome-decoding-problem/) for a code that looks random. With binary Goppa codes the scheme is still unbroken after more than 45 years; its cost is a large public key. Classic McEliece, the KEM based on it, was a round 4 candidate of the NIST process and is now under consideration at ISO.

**Notation.** All vectors are row vectors over $\mathbb{F}_2$ unless stated. $\mathbb{F}_{2^m}$ is the finite field with $2^m$ elements, $g(x) \in \mathbb{F}_{2^m}[x]$ is the Goppa polynomial of degree $t$, and $L = (\alpha_1, \ldots, \alpha_n)$ are distinct elements of $\mathbb{F}_{2^m}$, the support. The code has length $n$, dimension $k \ge n - mt$, and $G \in \mathbb{F}_2^{k \times n}$. $S$ is an invertible $k \times k$ matrix and $P$ an $n \times n$ permutation matrix. $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** The plain scheme of this page is at best one-way under chosen plaintext attack (OW-CPA): it is not IND-CPA, because $c + mG'$ has weight $t$ for the right $m$, and it is malleable. Classic McEliece adds a KEM transform and targets IND-CCA2 security, and its specification cites proofs in the random oracle model and in the [quantum random oracle model](/quantum-random-oracle-model/).

## In plain words

Think of a code that can fix any 5 flipped bits in a 64-bit word, with a fast fixing method. You keep the fast method secret. You publish only a mixed-up list of the code words, so that the code looks like a random one.

To send you a secret, someone turns it into a code word with the public list, and then flips 5 random bits on purpose. Anyone who sees the result faces the hard task of finding 5 flipped bits in a random looking code.

You undo the mixing, use your fast method to find and fix the 5 flipped bits, and read the message. The mixing hides the structure that makes the fix fast.

## The problem

Public-key encryption: key generation outputs a public key and a private key; anyone can encrypt a message with the public key; only the holder of the private key can decrypt. Here a message is a vector $m \in \mathbb{F}_2^k$, and the scheme must decrypt every ciphertext that it makes correctly.

## The algorithm

```pseudo id=main
KEYGEN(m, n, t)
L1  g ← a random monic irreducible polynomial of degree t over F_{2^m}; L ← n distinct elements of F_{2^m}
L2  G ← a k × n generator matrix of the binary Goppa code Γ(L, g)
L3  S ← a random invertible k × k matrix; P ← a random n × n permutation matrix
L4  return pk = (G' = S·G·P, t) and sk = (S, G, g, L, P)

ENCRYPT(pk, m)                              ▷ m ∈ F_2^k
L5  e ← a uniform random vector of weight t in F_2^n
L6  return c = m·G' + e

DECRYPT(sk, c)
L7  y ← c·P⁻¹                               ▷ y = (m·S)·G + e·P⁻¹
L8  e' ← PATTERSON(g, L, y)                 ▷ e' = e·P⁻¹, of weight t
L9  u ← the unique u with u·G = y + e'      ▷ u = m·S
L10 return u·S⁻¹
```

**The Goppa code.** The binary Goppa code $\Gamma(L, g)$ is the set of $c \in \mathbb{F}_2^n$ with

$$S_c(x) = \sum_{i=1}^{n} \frac{c_i}{x - \alpha_i} \equiv 0 \pmod{g(x)} .$$

Each $1/(x - \alpha_i) \bmod g$ is a polynomial of degree less than $t$, so it has $t$ coefficients in $\mathbb{F}_{2^m}$, which is $mt$ bits. Writing these bits as column $i$ gives a binary parity check matrix with $mt$ rows, so $k \ge n - mt$. Line L2 computes $G$ as a basis of its kernel. If $g$ has no repeated roots, for example if it is irreducible, the code has minimum distance at least $2t + 1$.

**Patterson's algorithm.** Let $y = c + e$ with $c \in \Gamma(L, g)$ and $\mathrm{wt}(e) \le t$, and let $\sigma(x) = \prod_{e_i = 1}(x - \alpha_i)$ be the error locator. Then $S_y = S_e$, and $\sigma$ satisfies the key equation $S_e(x)\,\sigma(x) \equiv \sigma'(x) \pmod g$. In characteristic 2, write $\sigma = a^2 + x b^2$; then $\sigma' = b^2$. Patterson solves the key equation as follows.

```pseudo id=patterson
PATTERSON(g, L, y)
P1  S ← Σ y_i / (x − α_i) mod g;  if S = 0 then return 0
P2  T ← S⁻¹ mod g
P3  if T = x then σ ← x
P4  else τ ← the square root of T + x modulo g   ▷ in F_{2^m}[x]/(g), a field of size 2^{mt}
P5       run the extended Euclidean algorithm on (g, τ) until the remainder a has degree ≤ ⌊t/2⌋; b is its cofactor, so a ≡ b·τ mod g
P6       σ ← a² + x·b²
P7  return the vector e with e_i = 1 exactly when σ(α_i) = 0
```

From $S\sigma \equiv \sigma'$ we get $(T + x) b^2 \equiv a^2$, so $\tau b \equiv a$, and the degree bounds $\deg a \le \lfloor t/2 \rfloor$ and $\deg b \le \lfloor (t-1)/2 \rfloor$ follow from $\deg \sigma \le t$. The square root exists and is unique because squaring is a bijection of a finite field of characteristic 2: $\sqrt{u} = u^{2^{mt - 1}}$. The implementation finds the roots in line P7 by evaluating $\sigma$ at every $\alpha_i$; [Chien search](/chien-search/) does the same in a faster order.

## Example

**One error.** Suppose $e$ has a single 1, at a position with support element $\alpha$. Then $S(x) = 1/(x - \alpha) = 1/(x + \alpha)$, so $T = x + \alpha$ and $T + x = \alpha$, a constant. Its square root is the constant $\tau = \sqrt{\alpha}$, which already has degree $0 \le \lfloor t/2 \rfloor$, so line P5 gives $a = \tau$ and $b = 1$. Then $\sigma = a^2 + x b^2 = \alpha + x$, whose only root is $\alpha$, and line P7 marks the right position. If $\alpha = 0$, then $T = x$ and line P3 gives $\sigma = x$ directly.

**A toy key.** The tests use $m = 6$ ($\mathbb{F}_{64}$ built with $x^6 + x + 1$), $n = 64$ and $t = 5$. The parity check matrix has $mt = 30$ rows, so $k = 34$ for the keys in the tests, and the public key is a $34 \times 64$ binary matrix (2176 bits). A ciphertext is 64 bits and carries 34 bits of message. This toy key falls to [Prange's algorithm](/prange-algorithm/) in about $\binom{64}{5}/\binom{30}{5} \approx 53$ rounds.

**Real sizes.** The original parameters were $n = 1024$, $k = 524$ and $t = 50$; Bernstein, Lange and Peters broke them in practice in 2008 with an improved [Stern](/stern-algorithm/) decoder. The Classic McEliece parameter set mceliece348864 has $m = 12$, $n = 3488$ and $t = 64$, so $k = 3488 - 12 \cdot 64 = 2720$. The public key is the non-identity part of a systematic matrix, $k(n - k) = 2720 \cdot 768$ bits, which is 261120 bytes. The ciphertext is a syndrome of $n - k = 768$ bits, 96 bytes (NIST IR 8545, Table 8).

## Correctness

Let $c = mG' + e$ with $\mathrm{wt}(e) = t$. Since $P$ is a permutation, $y = cP^{-1} = (mS)G + eP^{-1}$, where $(mS)G$ is a codeword of $\Gamma(L, g)$ and $eP^{-1}$ has weight $t$. The code has minimum distance at least $2t + 1$, so $eP^{-1}$ is the unique error of weight at most $t$, and Patterson's algorithm returns it: the error locator $\sigma$ has degree $\mathrm{wt}(e) \le t$, it satisfies the key equation, the decomposition $\sigma = a^2 + xb^2$ gives $a \equiv b\tau \pmod g$ with small degrees, and the extended Euclidean algorithm finds the pair $(a, b)$ up to a constant factor, which does not change the roots. Then $y + e' = (mS)G$, and $G$ has full rank $k$, so line L9 finds $u = mS$, and line L10 returns $uS^{-1} = m$.

## Complexity

**Key generation.** Building the $mt \times n$ parity check matrix costs $O(n t^2)$ operations in $\mathbb{F}_{2^m}$, the kernel costs $O(n^3)$ bit operations by Gaussian elimination, and the product $SGP$ costs $O(k^2 n)$. The test for irreducibility costs $O(m t^3)$ field operations. In total $O(n^3)$.

**Encryption.** $mG'$ costs $O(kn)$ bit operations.

**Decryption.** The syndrome costs $O(nt)$ field operations, the inverse and the extended Euclidean algorithm $O(t^2)$, the square root $O(m t \cdot t^2)$, and the root search $O(nt)$. Recovering $u$ costs $O(k^2 n)$ with a fresh elimination, as in the implementation, or $O(k^2)$ with a stored inverse of an information set of $G$.

**Space.** The public key has $kn$ bits, or $k(n-k)$ bits in systematic form. This is the main cost of the scheme.

## Properties

- **Not IND-CPA as it stands.** Given $c$ and two candidate messages, an attacker checks which $mG' + c$ has weight $t$. The plain scheme is also malleable: $c + m'G'$ encrypts $m + m'$. Berson (1997) showed that resending a message, or related messages, leaks it. Use a KEM transform, as Classic McEliece does.
- **Fast operations.** Encryption is a matrix product, and decryption is polynomial arithmetic of small degree. Both are fast; key generation is the slow part.
- **Large public keys.** From 261120 bytes to 1357824 bytes for the Classic McEliece parameter sets.
- **Small ciphertexts.** In the Niederreiter form of Classic McEliece the ciphertext is a syndrome of 96 to 208 bytes (NIST IR 8545, Table 8).
- **No decryption failures.** The Goppa decoder always corrects $t$ errors, so unlike BIKE and HQC there is no failure rate to analyze.

## Variants and improvements

- **[Niederreiter](/niederreiter-cryptosystem/) (1986).** Publish a parity check matrix and send the syndrome $He^T$ of a message encoded as an error vector. It has equivalent security and shorter ciphertexts.
- **Classic McEliece (round 4, 2022).** The Niederreiter form with binary Goppa codes, a systematic public key, and a KEM in which the session key is a SHAKE256 hash of the error vector and the ciphertext, with implicit rejection. The parameter sets range from mceliece348864 to mceliece6960119 and mceliece8192128.
- **Other codes.** Generalized Reed-Solomon codes (Niederreiter's original choice) fall to the attack of Sidelnikov and Shestakov (1992). Quasi-cyclic and quasi-dyadic variants with compact keys fall to the algebraic attack of Faugère, Otmani, Perret and Tillich (2010). These breaks are why Classic McEliece keeps plain binary Goppa codes.
- **CCA conversions.** Kobara and Imai (2001) gave conversions of the plain scheme to IND-CCA2 encryption; modern designs use a KEM with the Fujisaki-Okamoto style of transform.

## When to use it

Use Classic McEliece when you want the most conservative post-quantum KEM, its public key can be large and reused for a long time, and small ciphertexts matter, for example in long-lived keys of file encryption or of VPN servers with static keys. Do not use the plain scheme of this page. Classic McEliece is not a NIST standard: NIST IR 8545 says it is under consideration for standardization by ISO (it was proposed for ISO/IEC 18033-2), and NIST may consider a standard based on the ISO standard after that work ends.

## Pitfalls

- **Sending the plain scheme.** Without a KEM transform, the plain scheme leaks under related messages and is malleable.
- **Reusing the error vector.** Two ciphertexts of related messages with the same error, or of the same message with different errors, reveal information about the error positions.
- **Timing leaks in decryption.** The root search, the Euclidean algorithm and the square root have data-dependent timing in a simple implementation like this one. Real implementations use constant time additive FFT and bitsliced field arithmetic.
- **Weak code families.** Replacing binary Goppa codes by codes with more structure to save key space has failed many times. Check for structural attacks first.
- **A singular S or a dependent G.** Key generation must check that $S$ is invertible and that $G$ has full rank $k$.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and the parameters ($m = 6$, $n = 64$, $t = 5$) give no security at all. Use a vetted implementation for real data, for example a FIPS 140 validated module once a standard exists, or the Classic McEliece reference code; libsodium has no McEliece KEM. The code is the plain 1978 scheme with a real binary Goppa code and Patterson decoding. **Full Classic McEliece is not implemented.** It needs the Niederreiter form, the KEM with SHAKE256, $m = 12$ and $n \ge 3488$, an exact bit layout, and key generation with a systematic form, which would make a large and slow pure Python file; so the official KAT files of Classic McEliece are not used, and there are no official test vectors for the toy parameters. The tests check Patterson decoding against brute force on a Goppa code over $\mathbb{F}_{16}$, decoding of up to 5 errors over $\mathbb{F}_{64}$, and the round trip of encryption and decryption under fixed seeds.

## History

Goppa introduced his codes in 1970, and Patterson gave the decoding algorithm in 1975. Berlekamp, McEliece and van Tilborg proved in 1978 that general decoding is NP-complete, and in the same year McEliece proposed his cryptosystem. Niederreiter's 1986 variant with Reed-Solomon codes was broken in 1992, but Li, Deng and Wang showed in 1994 that the McEliece and Niederreiter forms have equivalent security for the same code. Bernstein, Lange and Peters broke the original 1978 parameters in 2008 with an optimized information set decoder and proposed larger ones. Classic McEliece was submitted to the NIST process in 2017 and reached the fourth round; in March 2025 NIST selected HQC instead and left Classic McEliece to the ISO process.

## References
