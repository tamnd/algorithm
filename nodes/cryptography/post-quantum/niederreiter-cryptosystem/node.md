---
tag: 3XG2CE
kind: algorithm
slug: niederreiter-cryptosystem
name: Niederreiter cryptosystem
aliases:
- Niederreiter
- Niederreiter encryption
area: cryptography/post-quantum
level: advanced
summary: The dual form of McEliece (1986). The message is encoded as an error vector of weight t, and the ciphertext is its syndrome under a scrambled parity check matrix.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, t: the number of errors, m: "the degree of the field GF(2^m)"}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, randomized: false}
history:
  year: 1986
  people: [Harald Niederreiter]
  note: Niederreiter proposed the scheme with generalized Reed-Solomon codes, which Sidelnikov and Shestakov broke in 1992. With binary Goppa codes it is the core of Classic McEliece.
prereqs: [mceliece-cryptosystem]
see_also: [combinatorial-number-system, syndrome-decoding-problem, information-set-decoding, goppa-code, key-encapsulation-mechanism, digital-signature, code-based-cryptography]
sources:
  - paper: "Harald Niederreiter, Knapsack-type cryptosystems and algebraic coding theory, Problems of Control and Information Theory 15(2), pages 159 to 166, 1986"
    locator: the whole paper (the public parity check matrix, the message as an error vector, and the syndrome as the ciphertext)
  - paper: "Yuan Xing Li, Robert H. Deng and Xin Mei Wang, On the equivalence of McEliece's and Niederreiter's public-key cryptosystems, IEEE Transactions on Information Theory 40(1), pages 271 to 273, 1994"
    locator: the whole paper (an attacker on one form gives an attacker on the other for the same code)
  - paper: "Nicolas T. Courtois, Matthieu Finiasz and Nicolas Sendrier, How to achieve a McEliece-based digital signature scheme, Asiacrypt 2001, LNCS 2248, pages 157 to 174"
    locator: the whole paper (the CFS signature, which hashes the message with a counter until the hash is a decodable syndrome)
  - paper: "Vladimir M. Sidelnikov and Sergey O. Shestakov, On insecurity of cryptosystems based on generalized Reed-Solomon codes, Discrete Mathematics and Applications 2(4), pages 439 to 444, 1992"
    locator: the whole paper (key recovery for Niederreiter's original choice of code)
  - paper: "Nicholas J. Patterson, The algebraic decoding of Goppa codes, IEEE Transactions on Information Theory 21(2), pages 203 to 207, 1975"
    locator: the whole paper (decoding from the syndrome polynomial)
  - paper: "Jean-Charles Faugère, Valérie Gauthier-Umaña, Ayoub Otmani, Ludovic Perret and Jean-Pierre Tillich, A distinguisher for high-rate McEliece cryptosystems, IEEE Transactions on Information Theory 59(10), pages 6830 to 6844, 2013"
    locator: the whole paper (the public keys of high-rate Goppa codes, as used by CFS, can be told apart from random codes)
  - url: "https://classic.mceliece.org/"
    title: "Daniel J. Bernstein, Tung Chou, Tanja Lange and others, Classic McEliece: conservative code-based cryptography, round 4 submission, October 2022"
    locator: the cryptosystem specification (the Niederreiter form with a systematic public key, and the fixed weight vector as the encapsulated secret)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (the Niederreiter scheme, constant weight encoding, and CFS signatures)
---

The Niederreiter cryptosystem is the dual form of the [McEliece cryptosystem](/mceliece-cryptosystem/). Harald Niederreiter proposed it in 1986. The public key is a scrambled parity check matrix $H' = MHP$ of a code with a fast decoder. The message is first encoded as a binary vector $e$ of weight exactly $t$, and the ciphertext is its syndrome $s = H'e^T$, a short vector of $n - k$ bits. The owner removes $M$, finds $Pe^T$ from the syndrome with the secret decoder, removes $P$, and decodes the message from $e$. Niederreiter used generalized Reed-Solomon codes, which were broken in 1992; with binary [Goppa codes](/goppa-code/) the scheme is as secure as McEliece's (Li, Deng and Wang, 1994), and it is the form that Classic McEliece uses.

**Notation.** Vectors are over $\mathbb{F}_2$; $e^T$ is a column vector. $H \in \mathbb{F}_2^{r \times n}$ with $r = mt \ge n - k$ is a parity check matrix of the binary Goppa code $\Gamma(L, g)$, where $g \in \mathbb{F}_{2^m}[x]$ is irreducible of degree $t$ and $L = (\alpha_1, \ldots, \alpha_n)$ are distinct elements of $\mathbb{F}_{2^m}$. $M$ is an invertible $r \times r$ matrix and $P$ an $n \times n$ permutation matrix. $W_{n,t}$ is the set of vectors of length $n$ and [Hamming weight](/hamming-weight/) $t$, with $|W_{n,t}| = \binom{n}{t}$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** Encryption is deterministic, so the plain scheme is at best one-way under chosen plaintext attack (OW-CPA): an attacker who guesses the message checks the guess by encrypting it. One-wayness means that no efficient $\mathcal{A}$ finds $e \in W_{n,t}$ from $(H', H'e^T)$ with non-negligible $\mathrm{Adv}$, which is the [syndrome decoding problem](/syndrome-decoding-problem/) for the public code. Classic McEliece builds an IND-CCA2 [KEM](/key-encapsulation-mechanism/) on top of it.

## In plain words

In McEliece, the message picks a code word and some random bits are flipped. In Niederreiter, the message itself chooses which bits to flip. You turn the message into a pattern of exactly $t$ flipped bits out of $n$, and you send only a short fingerprint of that pattern, its syndrome.

Anyone can compute the fingerprint of a pattern with the public matrix. Going back from the fingerprint to the pattern is the hard decoding problem. The owner knows the hidden code and its fast decoder, so the owner finds the pattern, and then reads the message from the positions of the flipped bits.

## The problem

Public-key encryption: key generation outputs a public key and a private key; anyone can encrypt a message with the public key; only the holder of the private key can decrypt. Here a message is an integer $x$ with $0 \le x < \binom{n}{t}$, and the scheme must decrypt every ciphertext that it makes correctly.

## The algorithm

```pseudo id=main
KEYGEN(m, n, t)
L1  g ← a random monic irreducible polynomial of degree t over F_{2^m}; L ← n distinct elements of F_{2^m}
L2  H ← the mt × n binary parity check matrix of the Goppa code Γ(L, g)
L3  M ← a random invertible mt × mt matrix; P ← a random n × n permutation matrix
L4  return pk = (H' = M·H·P, t) and sk = (M, g, L, P)

ENCRYPT(pk, x)                              ▷ 0 ≤ x < C(n, t)
L5  e ← CW-ENCODE(x, n, t)                  ▷ a vector of weight t
L6  return s = H'·eᵀ

DECRYPT(sk, s)
L7  s₁ ← M⁻¹·s                              ▷ s₁ = H·(P·eᵀ)
L8  e₁ ← the vector of weight t with H·e₁ = s₁, by Patterson's algorithm on the syndrome s₁
L9  eᵀ ← P⁻¹·e₁
L10 return CW-DECODE(e)
```

**The decoder.** Column $i$ of $H$ holds the $mt$ bits of the coefficients of $(x - \alpha_i)^{-1} \bmod g$. So the bits of the syndrome $H e_1$ are the coefficients of the syndrome polynomial $S_{e_1}(x) = \sum_i e_{1,i} (x - \alpha_i)^{-1} \bmod g$, and Patterson's algorithm runs on this polynomial directly, as on the McEliece page (lines P2 to P7 there). Niederreiter decryption needs no codeword and no generator matrix.

**Constant weight encoding.** CW-ENCODE uses the [combinatorial number system](/combinatorial-number-system/): every $x$ with $0 \le x < \binom{n}{t}$ has a unique form

$$x = \binom{c_1}{t} + \binom{c_2}{t-1} + \cdots + \binom{c_t}{1}, \qquad n > c_1 > c_2 > \cdots > c_t \ge 0,$$

and CW-ENCODE returns the vector with ones at $c_1, \ldots, c_t$. It picks $c_1$ as the largest $c$ with $\binom{c}{t} \le x$, subtracts, and repeats with $t - 1$. CW-DECODE sums the binomials. The map is a bijection from $\{0, \ldots, \binom{n}{t} - 1\}$ to $W_{n,t}$, so a message carries $\log_2 \binom{n}{t}$ bits.

## Example

**Constant weight encoding.** Take $n = 7$, $t = 3$ and $x = 13$. The largest $c$ with $\binom{c}{3} \le 13$ is $c_1 = 5$ ($\binom{5}{3} = 10$, $\binom{6}{3} = 20$), and $13 - 10 = 3$. The largest $c$ with $\binom{c}{2} \le 3$ is $c_2 = 3$, and $3 - 3 = 0$. Then $c_3 = 0$, because $\binom{0}{1} = 0$. So $e$ has ones at positions 0, 3 and 5, and $\binom{5}{3} + \binom{3}{2} + \binom{0}{1} = 13$.

**A toy key.** The tests use $m = 6$, $n = 64$ and $t = 5$. The public key $H'$ is a $30 \times 64$ binary matrix (1920 bits), a ciphertext is a syndrome of 30 bits, and a message is an integer below $\binom{64}{5} = 7624512$, so almost 23 bits. In McEliece form the same code gives a 64 bit ciphertext with 34 bits of message.

**Real sizes.** The Classic McEliece parameter set mceliece348864 has $m = 12$, $n = 3488$ and $t = 64$. Its public key is the non-identity part of $H'$ in systematic form, $768 \times 2720$ bits, which is 261120 bytes, and its ciphertext is a syndrome of $mt = 768$ bits, 96 bytes (NIST IR 8545, Table 8).

## Correctness

Let $e = $ CW-ENCODE$(x)$, so $\mathrm{wt}(e) = t$, and $s = MHPe^T$. Line L7 gives $s_1 = H e_1$ with $e_1 = Pe^T$, a vector of weight $t$ because $P$ only permutes positions. The Goppa code has minimum distance at least $2t + 1$, so $e_1$ is the only vector of weight at most $t$ with syndrome $s_1$, and Patterson's algorithm returns it (see the McEliece page for the key equation). Line L9 gives back $e$, and line L10 returns $x$ because CW-DECODE inverts CW-ENCODE. The full proof is in the proof file.

## Complexity

**Key generation.** Building $H$ costs $O(nt^2)$ operations in $\mathbb{F}_{2^m}$, and the product $MHP$ costs $O((mt)^2 n)$ bit operations; with $mt \le n$ this is $O(n^3)$. Classic McEliece instead brings $H$ to systematic form $(I \mid T)$ by Gaussian elimination, also $O(n^3)$, and needs no $M$.

**Encryption.** The syndrome is the sum of $t$ columns of $H'$: $O(t(n - k))$ bit operations, much less than the $O(kn)$ of McEliece encryption. Constant weight encoding costs $O(n)$ binomial updates on numbers of $\log_2 \binom{n}{t}$ bits.

**Decryption.** $M^{-1}s$ costs $O((mt)^2)$, Patterson's algorithm $O(mt^3 + nt)$ field operations, and decoding the message $O(n)$ binomial updates. No linear system is solved.

**Space.** The public key has $(n - k) n$ bits, or $(n - k)k$ bits in systematic form, the same as McEliece.

## Properties

- **Equivalent security.** Li, Deng and Wang (1994) showed that the McEliece and Niederreiter forms of the same code are equally hard to break: a syndrome $He^T$ and a word $mG + e$ give the same decoding problem, because each can be computed from the other with public data.
- **Short ciphertexts.** The ciphertext has $n - k$ bits instead of $n$.
- **Deterministic.** The same message always gives the same ciphertext, so the plain scheme is not IND-CPA. It is also malleable: $s + H'u^T$ is the syndrome of $e + u$.
- **No decryption failures.** For every $x$ in range, decryption is correct.
- **Constant weight encoding is needed.** If the message is random and only a seed, as in a KEM, the encoding is not needed: Classic McEliece draws $e$ directly as a uniform random vector of weight $t$ and hashes it.

## Variants and improvements

- **Classic McEliece.** The Niederreiter form with binary Goppa codes, a systematic public key $(I_{n-k} \mid T)$ without $M$, and a KEM that hashes $e$ with SHAKE256 and uses implicit rejection.
- **CFS signatures (Courtois, Finiasz and Sendrier, 2001).** To sign a document $D$, hash $D$ with a counter $i = 0, 1, 2, \ldots$ until $h(D \| i)$ is the syndrome of some vector of weight at most $t$, decode it with the secret decoder to get $e$, and output $(e, i)$. The verifier checks $\mathrm{wt}(e) \le t$ and $H'e^T = h(D \| i)$. A random syndrome is decodable with probability about $1/t!$, so $t$ must be small (the paper uses $m = 16$ and $t = 9$), which forces a code of very high rate and a public key of megabytes. Faugère, Gauthier-Umaña, Otmani, Perret and Tillich (2011, journal version 2013) showed that such high-rate Goppa codes can be told apart from random codes, which removes the security argument of CFS, and generic attacks also improved, so CFS is not used in practice.
- **Other codes.** Niederreiter's generalized Reed-Solomon codes fall to Sidelnikov and Shestakov (1992). Most attempts to use codes with more structure to shrink keys have failed in the same way.

## When to use it

Use Classic McEliece, which is this scheme with binary Goppa codes inside a KEM, when you want the most conservative post-quantum KEM and can store a large public key, for example for long-lived static keys. NIST IR 8545 says that Classic McEliece is under consideration at ISO, and it is not a NIST standard. Do not use the plain scheme of this page: it is deterministic and malleable.

## Pitfalls

- **A message that is not secret enough.** Encryption is deterministic, so a message from a small set is found by trying each one. Use it only inside a KEM with a uniform random $e$.
- **Wrong weight.** The decoder must reject a syndrome when the result does not have weight exactly $t$, and the encoder must reject $x \ge \binom{n}{t}$.
- **Timing leaks in constant weight encoding.** A simple encoder, like the one here, takes time that depends on $x$. Real implementations draw $e$ with constant time sorting or rejection sampling instead.
- **Weak code families.** Generalized Reed-Solomon codes and many structured families leak the secret code. Use binary Goppa codes.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and the parameters ($m = 6$, $n = 64$, $t = 5$) give no security. Use a vetted implementation for real data, for example a FIPS 140 validated module once a standard exists, or the Classic McEliece reference code; libsodium has no code-based KEM. The code is the plain Niederreiter scheme with a real binary Goppa code, a local copy of the Patterson decoder from the McEliece page, and constant weight encoding with the combinatorial number system. It is not Classic McEliece, so the Classic McEliece KAT files do not apply, and there are no official test vectors for the toy parameters. The tests check the constant weight encoding against itertools.combinations, syndrome decoding against brute force on a Goppa code over $\mathbb{F}_{16}$, and the round trip under fixed seeds.

## History

Niederreiter published the scheme in 1986 in a paper on knapsack-type cryptosystems, with generalized Reed-Solomon codes. Sidelnikov and Shestakov recovered the secret code of that version in 1992. Li, Deng and Wang showed in 1994 that the McEliece and Niederreiter forms are equivalent in security when they use the same code. Courtois, Finiasz and Sendrier built the CFS signature on the Niederreiter form in 2001. Classic McEliece, submitted to the NIST process in 2017, uses the Niederreiter form with binary Goppa codes, and it reached the fourth round.

## References
