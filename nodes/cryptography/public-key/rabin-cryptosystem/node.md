---
tag: 3WNX9E
kind: algorithm
slug: rabin-cryptosystem
name: Rabin cryptosystem
aliases:
- Rabin encryption
area: cryptography/public-key
level: core
summary: Encryption is squaring modulo N = pq with both primes 3 mod 4. Inverting it is provably as hard as factoring, and a decryption oracle factors N in two queries.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^2)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1979
  people: [Michael O. Rabin, Hugh C. Williams]
  note: Rabin published it as MIT/LCS/TR-212 in January 1979, the first cryptosystem with a proof of equivalence to factoring. Williams removed the four way ambiguity in 1980.
prereqs: [modular-square-root, chinese-remainder-theorem]
see_also: [rsa-cryptosystem, quadratic-residuosity-problem, rabin-signature, blum-goldwasser-cryptosystem, integer-factorization, chosen-ciphertext-attack, goldwasser-micali-cryptosystem]
sources:
  - url: "http://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-212.pdf"
    title: Michael O. Rabin, Digitalized signatures and public-key functions as intractable as factorization, MIT/LCS/TR-212, MIT Laboratory for Computer Science, January 1979
    locator: Sections 1 and 2 (the squaring function, the four roots, the redundancy, and the theorem that an inverting machine factors N)
  - paper: "Hugh C. Williams, A modification of the RSA public-key encryption procedure, IEEE Transactions on Information Theory 26(6), pages 726 to 729, 1980"
    locator: the whole paper (the p = 3 mod 8 and q = 7 mod 8 choice, the Jacobi symbol tag, and the unique decryption it gives)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.3, Algorithm 8.11, Example 8.12 and Note 8.14 (the scheme with redundancy, and why the equivalence proof is also a chosen ciphertext attack)
  - url: "https://cr.yp.to/sigs/rwsota-20080131.pdf"
    title: Daniel J. Bernstein, RSA signatures and Rabin-Williams signatures, the state of the art, 2008
    locator: Sections 2 and 6 (the Rabin-Williams tweaks, principal roots, and the tight security proofs)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the chapter on number theoretic assumptions (squaring modulo a Blum integer, the equivalence with factoring, and why a one way function is not yet an encryption scheme)
---

The Rabin cryptosystem encrypts by squaring. The public key is a modulus $N = pq$ with $p \equiv q \equiv 3 \pmod 4$, a Blum integer, and the ciphertext of a message representative $m$ is $c = m^2 \bmod N$. The private key is the pair of primes, which gives the four square roots of $c$; a redundancy in the message says which of the four was meant. Rabin's 1979 report proved what RSA cannot claim: *inverting this function is exactly as hard as factoring $N$*. The proof is short and it is also an attack, because a machine that decrypts chosen ciphertexts factors the modulus in two queries on average. So the scheme is a landmark and a warning at the same time: a proof against a passive attacker says nothing about an active one.

**Notation.** $N = pq$ with $p \equiv q \equiv 3 \pmod 4$, $b$ is the number of binary digits of $N$, $m$ a message representative with $0 \le m < N$, $c = m^2 \bmod N$, and $\mathrm{QR}_N$ the set of quadratic residues modulo $N$.

## In plain words

To lock a number, multiply it by itself and keep the remainder after dividing by a public product of two secret primes. There is no exponent to choose, so this is about as fast as encryption can be.

Undoing it needs a square root, and with this kind of modulus a number has four of them, not one. The holder of the two primes gets all four; everybody else gets none. So the message carries a short tag, and the holder keeps the one root that shows the tag.

The good part is a proof: anyone who can take these roots can split the public product, which nobody knows how to do. The bad part is the same proof read backwards. If you ever hand back a root of a number that somebody else chose, you have given away your primes.

## The problem

Rabin encryption is a [public-key encryption](/public-key-encryption/) scheme. Its one way function is

$$f_N : \mathbb{Z}_N^* \to \mathrm{QR}_N, \qquad f_N(m) = m^2 \bmod N ,$$

which is four to one on $\mathbb{Z}_N^*$ and becomes a *permutation* of $\mathrm{QR}_N$ when $N$ is a Blum integer, because then exactly one of the four roots of a residue is itself a residue. Inverting $f_N$ without the factors is the problem of [modular square roots](/modular-square-root/) with a composite modulus, and it is equivalent to [integer factorization](/integer-factorization/); this is the content of the correctness and security proof on this page. The related decision problem, telling a residue from a non-residue with Jacobi symbol 1, is the [quadratic residuosity problem](/quadratic-residuosity-problem/), and it is a different and possibly easier assumption.

## The algorithm

```pseudo id=main
RABIN-KEYGEN(b)
L1  p ← a random prime of b/2 binary digits with p ≡ 3 (mod 4)
L2  q ← a random prime of b/2 binary digits with q ≡ 3 (mod 4), q ≠ p
L3  N ← p*q; return public key N and private key (p, q)

RABIN-ENCRYPT(N, msg)
L4  m ← ENCODE(msg)                              ▷ the redundancy goes in here
L5  return m*m mod N

RABIN-DECRYPT(p, q, c)
L6  r_p ← c^((p+1)/4) mod p                       ▷ a square root modulo p
L7  r_q ← c^((q+1)/4) mod q                       ▷ a square root modulo q
L8  w_p ← q*(q^{-1} mod p) mod N; w_q ← p*(p^{-1} mod q) mod N
L9  u ← (w_p*r_p + w_q*r_q) mod N; v ← (w_p*r_p - w_q*r_q) mod N
L10 roots ← {u, N - u, v, N - v}
L11 for each m in roots: if DECODE(m) ≠ FAIL then return DECODE(m)
L12 return ERROR
```

**The walk-through.** Lines 1 and 2 draw the primes with [Miller-Rabin](/miller-rabin/) and keep only the candidates that are $3$ modulo 4; half of the primes are, so nothing is lost. Line 5 is the whole encryption: one modular squaring. An RSA encryption with $e = 65537$ takes 16 squarings and one multiplication, so this is about one seventeenth of its work, and far less than an RSA decryption.

Lines 6 and 7 are where $p \equiv 3 \pmod 4$ pays. For such a prime and a residue $c$, the exponent $(p+1)/4$ is an integer and

$$\left(c^{(p+1)/4}\right)^2 = c^{(p+1)/2} = c \cdot c^{(p-1)/2} = c \cdot 1 = c \pmod p ,$$

by Euler's criterion, so a root modulo $p$ is one exponentiation, with no [Tonelli-Shanks](/modular-square-root/) search. Lines 8 and 9 glue the roots with the [Chinese remainder theorem](/chinese-remainder-theorem/); the two sign choices $(\pm r_p, \pm r_q)$ give four roots, and $u$ and $N - u$, $v$ and $N - v$ are the two pairs. Line 11 is the only place where the redundancy enters: three of the four roots are unrelated numbers, and the encoding is built so that they fail a check.

**The encoding.** Rabin's report repeats a block of the message inside the plaintext. The code of this page uses the modern form of the same idea: the integer is $\texttt{0x01} \Vert \mathit{msg} \Vert \mathit{tag}$ with $\mathit{tag}$ the first two octets of $\mathrm{SHA}\text{-}256(\mathit{msg})$, so a wrong root passes with probability about $2^{-16}$ and the leading octet fixes the length. Any redundancy does: a fixed header, a repeated block, or a hash tag. The scheme without redundancy is unusable, because decryption cannot choose.

## Example

Take $p = 7$ and $q = 11$, so $N = 77$; both primes are $3$ modulo 4. Encrypt $m = 20$:

$$c = 20^2 \bmod 77 = 400 - 5 \cdot 77 = 15 .$$

Decryption computes $r_p = 15^{(7+1)/4} = 15^2 \equiv 1^2 = 1 \pmod 7$ and $r_q = 15^{(11+1)/4} = 15^3 \equiv 4^3 = 64 \equiv 9 \pmod{11}$. The four combinations give

$$\{13,\ 20,\ 57,\ 64\} ,$$

each of which squares to 15 modulo 77, and the pairs add to 77: $20 + 57 = 77$ and $13 + 64 = 77$. Without redundancy the receiver has no way to pick 20 out of the four.

**The factoring reduction on the same key.** Take $x = 23$, so $x^2 \bmod 77 = 67$. The roots of 67 are $\{12, 23, 54, 65\}$. If a decryption oracle answers 23 it tells us nothing, and if it answers $54 = 77 - 23$ it tells us nothing, since $\gcd(23 - 54, 77) = 1$. But

$$\gcd(23 - 12, 77) = 11 = q, \qquad \gcd(23 - 65, 77) = \gcd(-42, 77) = 7 = p .$$

Two of the four roots give a factor, so one query factors $N$ with probability $1/2$.

**The toy key in the test file.** Two primes of 256 binary digits, both $3$ modulo 4, give a modulus of 512 binary digits and room for messages up to 60 octets. The message `four roots, one message` encodes to the 26 octet string $\texttt{01666f757220726f6f74732c206f6e65206d65737361676503db}$, whose last two octets are the tag. Exactly one of the four roots of its ciphertext decodes. With the random root oracle of the test file, the reduction factored the modulus on its first query, and the chosen ciphertext attack then read a target ciphertext that the oracle had never seen.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It contains:

1. **The four roots.** For a Blum integer $N$ and $c \in \mathrm{QR}_N$ with $\gcd(c, N) = 1$, the set $\{u, N-u, v, N-v\}$ of lines 9 and 10 is exactly the set of square roots of $c$, and it has four elements.
2. **Decryption inverts encryption.** The encoded message is one of those four roots, and the probability that another root also passes DECODE is at most $2^{-16}$ for the tag of this page, so line 11 returns the message.
3. **Equivalence with factoring.** If a machine $\mathcal{A}$ returns some square root of $x^2 \bmod N$ for a uniform $x$, then $\gcd(x - \mathcal{A}(x^2), N)$ is a prime factor of $N$ with probability at least $1/2$. Repeating $t$ times fails with probability at most $2^{-t}$. The converse is clear: the factors give the roots by lines 6 to 10.
4. **The chosen ciphertext attack.** Part 3 is an attack whenever the attacker may send chosen ciphertexts and see the result, so bare Rabin encryption is not [IND-CCA](/ind-cca-security/) secure. It is not [IND-CPA](/ind-cpa-security/) secure either, because encryption is deterministic.

## Complexity

| operation | cost with schoolbook arithmetic |
|---|---|
| key generation | $\Theta(b^4 / \log b)$ expected, dominated by primality testing |
| encryption | one squaring and one reduction, $\Theta(b^2)$ |
| decryption | two exponentiations with $b/2$ binary digit moduli and exponents, $\Theta(b^3)$ |
| the factoring reduction | two oracle queries on average, plus $\Theta(b^2)$ per query |

Encryption is the fastest of any standard public-key scheme: one multiplication. That is the whole practical argument for Rabin, and it is why the signature variant, where the *signer* pays the cost and the *verifier* squares, is the direction that survived; see [Rabin signature](/rabin-signature/). Decryption is about the cost of an RSA decryption with the [CRT](/chinese-remainder-theorem/), because it is the same two half size exponentiations.

The space is a few values of $b$ binary digits. The best case for decryption is $\Theta(b^2)$ in the degenerate case of a tiny modulus; for real sizes it is $\Theta(b^3)$ throughout.

## Properties

- **Equivalent to factoring, in the inversion sense.** This is the property Rabin introduced and the reason the scheme is taught. For [RSA](/rsa-cryptosystem/) no such equivalence is known, and the [RSA problem](/rsa-problem/) is a separate assumption.
- **Deterministic, so not semantically secure.** Equal messages give equal ciphertexts, and the attacker can encrypt. Any real use needs randomness in the encoding, which turns the scheme into something like [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) or an [OAEP](/rsa-oaep/) style padding over the squaring map.
- **Not secure against chosen ciphertext attacks, by construction.** The security proof is the attack. A padding that makes decryption fail on all four roots except the intended one does not help: the attacker chooses its own plaintexts, so it can satisfy the padding and still learn a root.
- **Four to one, and a permutation on the residues.** Squaring modulo a Blum integer permutes $\mathrm{QR}_N$, which makes it the standard [trapdoor permutation](/trapdoor-one-way-function/) in theory papers, and the engine of the Blum-Blum-Shub generator.
- **No exponent choices and no small exponent attacks.** There is no $e$ and no $d$, so [Wiener's attack](/wiener-attack/) and the small public exponent attacks have nothing to grip. The modulus must still be large, and the primes must still be generated properly.
- **The least significant bit is hard core.** For squaring modulo a Blum integer, predicting the low bit of the principal root is as hard as factoring, which is the basis of Blum-Blum-Shub and a classic example of a [hard core predicate](/hard-core-predicate/).

## Variants and improvements

- **Williams (1980).** Choose $p \equiv 3 \pmod 8$ and $q \equiv 7 \pmod 8$. Then $\gcd(2, \varphi(N))$ behaves so that the Jacobi symbol and a small multiplier identify the right root with no redundancy at all: encryption sends $c$ together with two bits, and decryption is unique. This is the Rabin-Williams family, and it is the form used for signatures.
- **Blum-Goldwasser (1984).** Use the squaring map as a [pseudorandom generator](/pseudorandom-generator/) and encrypt with the keystream. This gives a semantically secure scheme whose security is still equivalent to factoring, and it is the right answer to the determinism of bare Rabin; see [Blum-Goldwasser](/blum-goldwasser-cryptosystem/).
- **Rabin with a hash based padding.** Composing the squaring map with an OAEP style transform, or wrapping it in the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/), gives an IND-CCA scheme in the random oracle model, with a tight reduction to factoring. This is the modern way to use the map for encryption, and the [KEM](/key-encapsulation-mechanism/) form of it is cleaner still.
- **Principal and tweaked roots.** Bernstein's survey organizes the choices: the principal root (the root that is itself a residue), the $|\pm|$ convention, and the tweaks $e \in \{1, 2, -1, -2\}$ that make the map a bijection on a set the verifier can check. These details decide whether the security proof is tight.
- **Rabin signatures.** Signing is the private operation, so the signer takes the root and the verifier squares. Verification is one multiplication, which is why Rabin-Williams signatures remain attractive for devices that verify often; see [Rabin signature](/rabin-signature/).

## When to use it

For production encryption, do not. The scheme is deterministic, it has no standard, no test vectors and no widely reviewed implementation, and its equivalence proof is an active attack. Use [RSA-OAEP](/rsa-oaep/), a [KEM](/key-encapsulation-mechanism/) such as RSA-KEM or ML-KEM, or [ECIES](/ecies/).

Where it is the right tool:

- **In theory.** As the standard trapdoor permutation with a proof, it is the cleanest example of a one way permutation from a hardness assumption, and it is what the Blum-Blum-Shub generator and many textbook constructions use.
- **For teaching.** It shows in half a page that provable equivalence to a hard problem is not the same as security, which is the lesson that led to [IND-CCA](/ind-cca-security/) as the right target.
- **For verification-heavy signatures.** The Rabin-Williams form gives the cheapest verification of any classical signature scheme, one multiplication plus a comparison, and it has tight proofs.

## Pitfalls

- **No redundancy, no decryption.** A scheme that sends $m^2 \bmod N$ with a plain message cannot be decrypted, because three of the four roots are equally plausible. Any deployment that forgot this is broken in a different sense.
- **Answering a root for a chosen input.** This is handing over the private key. A decryption service, a padding error that reveals a root, or a signature on a chosen message in the bare scheme all do it.
- **Reusing the key for signatures and for encryption.** In the bare scheme, a signature *is* a square root of a chosen value, so a signing service is exactly the oracle of the reduction and it factors the shared modulus.
- **Primes that are not 3 modulo 4.** Lines 6 and 7 then need [Tonelli-Shanks](/modular-square-root/), and the four roots lose the pleasant structure that makes squaring a permutation of the residues.
- **Treating the Jacobi symbol as a secret.** The symbol $\left(\frac{c}{N}\right)$ is computable from $N$ alone with the [Jacobi symbol](/jacobi-symbol/) algorithm, so it leaks one bit of every plaintext for free. Williams' variant uses this openly instead of hoping it is hidden.
- **Thinking the equivalence protects the plaintext.** The proof says that total inversion is as hard as factoring. It says nothing about partial information, which is what semantic security asks about, and the deterministic map leaks plenty.

**The code of this page is for study only.** It is not constant time, the keys are toy keys, and the factoring reduction runs against a local oracle in the same process.

## Implementations

## History

Michael Rabin's report MIT/LCS/TR-212, "Digitalized signatures and public-key functions as intractable as factorization", appeared in January 1979, two years after [RSA](/rsa-cryptosystem/). Its point was not speed but proof. RSA's security rested on a new assumption, the hardness of extracting $e$-th roots; Rabin replaced $e$ by 2 and showed that the resulting function cannot be inverted unless factoring is easy. The report also observed the other side of the coin: the same argument lets an adversary who gets roots of chosen values factor the modulus, so it insisted on redundancy in the plaintext and warned against signing arbitrary values. This is the first appearance of what later became the chosen ciphertext attack, and of the idea that a reduction can be read as an attack.

Hugh Williams removed the ambiguity in 1980 by choosing the primes modulo 8 and using the Jacobi symbol, which gave the first scheme with both unique decryption and an equivalence to factoring. Blum, Blum and Shub used the squaring map in 1982 for their pseudorandom generator, and Blum and Goldwasser in 1984 turned it into a semantically secure encryption scheme. The low bit of the principal root became one of the first proved hard core predicates.

The encryption scheme itself never found deployment. Its weaknesses, determinism and the chosen ciphertext problem, were understood almost at once, and by the time padding methods existed that could fix them, RSA had the standards, the libraries and the hardware. What survived is the proof technique, the Rabin-Williams signature family, and the squaring map as the trapdoor permutation of choice in the theory literature.

## References
