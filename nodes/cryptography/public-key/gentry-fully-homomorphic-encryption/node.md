---
tag: V27SZY
kind: algorithm
slug: gentry-fully-homomorphic-encryption
name: Gentry's fully homomorphic encryption
aliases:
- Gentry FHE
area: cryptography/public-key
level: research
summary: "The 2009 blueprint for fully homomorphic encryption: a noisy somewhat homomorphic scheme, squashed and then bootstrapped by evaluating its own decryption. Shown here with DGHV over the integers."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {g: the number of binary digits of x_0 (γ), t: the number of public integers (τ)}
  time: {worst: Θ(t·g), average: Θ(t·g), best: Θ(t·g)}
  space: {extra: Θ(g)}
properties: {deterministic: false, randomized: true}
history:
  year: 2009
  people: [Craig Gentry]
  note: Presented at STOC 2009 with an ideal lattice scheme and written up in his Stanford thesis. The integer scheme DGHV of van Dijk, Gentry, Halevi and Vaikuntanathan (Eurocrypt 2010) follows the same blueprint.
prereqs: [homomorphic-encryption, lattice-based-cryptography]
see_also: [learning-with-errors, ring-learning-with-errors, boolean-circuit, paillier-cryptosystem, subset-sum-problem, ind-cpa-security, secure-multiparty-computation, functional-encryption]
sources:
  - paper: "Craig Gentry, Fully homomorphic encryption using ideal lattices, STOC 2009, pages 169 to 178"
    locator: the somewhat homomorphic scheme over ideal lattices, bootstrappable schemes, the bootstrapping theorem, squashing the decryption circuit, and the circular security assumption
  - paper: "Craig Gentry, A fully homomorphic encryption scheme, PhD thesis, Stanford University, 2009"
    locator: the full version, with the definitions of compactness and leveled FHE, the proofs of the bootstrapping theorem and the sparse subset sum assumption
  - paper: "Marten van Dijk, Craig Gentry, Shai Halevi and Vinod Vaikuntanathan, Fully homomorphic encryption over the integers, Eurocrypt 2010, LNCS 6110, pages 24 to 43"
    locator: the somewhat homomorphic public-key scheme with x_i = p q_i + r_i, the permitted circuits, the parameters ρ, ρ', η, γ, τ, squashing with a sparse subset of rationals, and the reduction from the approximate GCD problem
  - paper: "Craig Gentry and Shai Halevi, Implementing Gentry's fully-homomorphic encryption scheme, Eurocrypt 2011, LNCS 6632, pages 129 to 148"
    locator: the first implementation with bootstrapping, its key sizes and its recryption times
  - paper: "Jean-Sébastien Coron, Avradip Mandal, David Naccache and Mehdi Tibouchi, Fully homomorphic encryption over the integers with shorter public keys, Crypto 2011, LNCS 6841, pages 487 to 504"
    locator: the shorter public keys for DGHV
  - paper: "Zvika Brakerski, Craig Gentry and Vinod Vaikuntanathan, (Leveled) fully homomorphic encryption without bootstrapping, ITCS 2012, pages 309 to 325"
    locator: modulus switching, which controls noise growth without bootstrapping
  - paper: "Léo Ducas and Daniele Micciancio, FHEW, bootstrapping homomorphic encryption in less than a second, Eurocrypt 2015, LNCS 9056, pages 617 to 640"
    locator: the bootstrapping of one gate at a time
  - paper: "Ilaria Chillotti, Nicolas Gama, Mariya Georgieva and Malika Izabachène, Faster fully homomorphic encryption, bootstrapping in less than 0.1 seconds, Asiacrypt 2016, LNCS 10031, pages 3 to 33"
    locator: the TFHE gate bootstrapping
---

Gentry's fully homomorphic encryption is the construction, published by Craig Gentry at STOC 2009 and in his thesis, that first made [homomorphic encryption](/homomorphic-encryption/) work for every function. It is a blueprint in three steps. First, build a somewhat homomorphic scheme whose ciphertexts carry noise, so that additions and multiplications work until the noise is too large. Second, "squash" the decryption algorithm into a circuit of low depth. Third, bootstrap: evaluate the decryption circuit homomorphically on an encryption of the secret key, which refreshes a noisy ciphertext. Gentry's own scheme used ideal lattices. This page runs the blueprint with the simpler DGHV scheme over the integers (van Dijk, Gentry, Halevi and Vaikuntanathan, 2010), and the code implements its somewhat homomorphic part only.

**Notation.** The plaintext is one bit $m$. $p$ is the secret odd integer of $\eta$ binary digits. For an integer $z$, $[z]_p$ is the remainder in $(-p/2, p/2]$. The public key is $x_0, \ldots, x_\tau$ with $x_i = p q_i + r_i$, where the $q_i$ have about $\gamma - \eta$ binary digits and $|r_i| < 2^\rho$. A fresh ciphertext has extra noise below $2^{\rho'}$. The **noise** of a ciphertext $c$ is $[c]_p$. In the front matter $g = \gamma$ and $t = \tau$.

## In plain words

The secret key is a large odd number. A ciphertext of a bit is a multiple of the key, plus a small even error, plus the bit. Whoever knows the key divides it out, looks at what is left, and reads the bit from whether it is even or odd.

Adding two ciphertexts adds the bits modulo 2, and multiplying them multiplies the bits, because the multiples of the key stay multiples. But the errors add and multiply too. After a few multiplications the error is as large as the key, and the bit is lost.

Gentry's idea is to clean a ciphertext before that happens. The decryption steps are themselves a small circuit of additions and multiplications. Run that circuit on encrypted pieces of the key and on the dirty ciphertext, and the output is a fresh encryption of the same bit, with a small error again.

## The problem

The goal is a public-key scheme with an Eval algorithm that works for all circuits and outputs short ciphertexts: fully homomorphic encryption, as defined on the [homomorphic encryption](/homomorphic-encryption/) page. Before 2009, schemes could do one operation without limit ([Paillier](/paillier-cryptosystem/) adds) or both operations only a little (Boneh, Goh and Nissim allow one multiplication). The hard part is that every known way to hide data with both operations adds noise, and multiplication makes noise grow fast.

## The algorithm

```pseudo id=main
DGHV-KEYGEN(η, ρ, γ, τ)
L1  p ← a random odd integer of η binary digits
L2  for i ← 0 to τ: q_i ← uniform in [0, 2^γ/p); r_i ← uniform in (−2^ρ, 2^ρ); x_i ← p·q_i + r_i
L3  sort so that x_0 is the largest; if x_0 is even or [x_0]_p is odd then go to L2
L4  return the public key (x_0, …, x_τ) and the secret key p

DGHV-ENCRYPT((x_0, …, x_τ), m)             ▷ m ∈ {0, 1}
L5  S ← a random subset of {1, …, τ}; r ← uniform in (−2^ρ', 2^ρ')
L6  return c ← (m + 2r + 2·Σ_(i ∈ S) x_i) mod x_0

DGHV-EVAL(f, c_1, …, c_ℓ)                    ▷ f a circuit of XOR and AND gates on bits
L7  XOR gate on c_a, c_b: c ← c_a + c_b       ▷ over the integers
L8  AND gate on c_a, c_b: c ← c_a · c_b

DGHV-DECRYPT(p, c)
L9  return [c]_p mod 2
```

Every ciphertext has the form $c = \nu + p k$ for an integer $k$ and a noise $\nu \equiv m \pmod 2$. If $|\nu| < p/2$, then $[c]_p = \nu$ and line L9 returns $m$. Sums and products keep the form $\nu + pk$ and act on $\nu$ as XOR and AND act on $m$ modulo 2, but $|\nu|$ grows: it at most doubles under XOR and it is the product of the two noises under AND. That is the whole "somewhat": a circuit is permitted while its noise stays below $p/2$.

### Squashing and bootstrapping

Bootstrapping refreshes a ciphertext $c$ of $m$ whose noise is large but still below $p/2$. The public key gets encryptions $\langle sk \rangle$ of the bits of the secret key under the same key.

```pseudo
RECRYPT(pk, ⟨sk⟩, c)                       ▷ ⟨sk⟩: encryptions of the bits of sk under pk
1  for each binary digit c_j of c
2      c̄_j ← c_j, read as a ciphertext of the bit c_j with noise c_j
3  return EVAL(pk, DECRYPT, ⟨sk⟩, c̄)      ▷ an encryption of DECRYPT(sk, c) = m

BOOTSTRAPPED-NAND(pk, ⟨sk⟩, c_1, c_2)
4  D ← the circuit (s, x, y) ↦ NOT(DECRYPT(s, x) AND DECRYPT(s, y))
5  return EVAL(pk, D, ⟨sk⟩, the digits of c_1 and c_2)
```

The output of RECRYPT has the noise of one evaluation of the decryption circuit on fresh encryptions, whatever the noise of $c$ was. A scheme is **bootstrappable** if it can evaluate D, the decryption circuit followed by one NAND gate. Then any circuit can be evaluated one NAND gate at a time, with a refresh in each gate.

The decryption of DGHV, $[c]_p \bmod 2 = (c - p \lfloor c/p \rceil) \bmod 2$, needs a division by $p$, which is a circuit of too high a degree. **Squashing** removes it. The public key gets rationals $y_1, \ldots, y_\Theta$ with $\kappa$ binary digits after the point, such that a secret sparse subset of them, of size $\theta$, sums to $1/p$ modulo 2. Anyone can compute the expanded ciphertext $z_i = c \cdot y_i \bmod 2$ from the public $y_i$, keeping only a few binary digits after the point. Then $m = (c - \lfloor \sum_i s_i z_i \rceil) \bmod 2$, where the new secret key is the bit vector $s$ with $\theta$ ones. Adding $\theta$ numbers of a few binary digits is a circuit of low degree, and the scheme becomes bootstrappable. The price is a second assumption, the sparse subset sum problem: given the $y_i$, finding the sparse subset is hard. Publishing $\langle sk \rangle$ under the key $pk$ itself needs a third assumption, circular security. Without it, a chain of $L$ key pairs, each encrypting the previous secret key, gives leveled FHE for depth $L$.

## Example

This is a hand-sized key with $p = 1001$ (so $p/2 = 500.5$), $\rho = 3$ and $\tau = 2$. It is far too small for any security.

| step | computation | value |
|---|---|---|
| L2, L3 | $x_0 = 1001 \cdot 999 + 4$, $x_1 = 1001 \cdot 523 + 3$, $x_2 = 1001 \cdot 377 - 1$ | 1000003, 523526, 377376 |
| L3 | $x_0$ is odd and $[x_0]_p = 4$ is even | accepted |
| L5, L6 | $m = 1$, $r = 2$, $S = \{1, 2\}$: $(1 + 4 + 2 \cdot 900902) \bmod x_0$ | $c_1 = 801806$, noise $1 + 4 + 2(3 - 1) - 4 = 5$ |
| L5, L6 | $m = 1$, $r = -1$, $S = \{1\}$: $(1 - 2 + 2 \cdot 523526) \bmod x_0$ | $c_2 = 47048$, noise 1 |
| L7 | $c_1 + c_2$ | 848854, noise 6, decrypts to $0 = 1 \oplus 1$ |
| L8 | $c_1 \cdot c_2$ | 37723368688, noise 5, decrypts to $1 = 1 \wedge 1$ |
| L8 | $c_1 \cdot c_1$ | 642892861636, noise 25, decrypts to 1 |
| L8 | $(c_1 c_1) \cdot (c_1 c_1)$ | 413311231542525040596496, true noise $5^4 = 625$ |
| L9 | $625 > 500.5$, so $[c]_p = 625 - 1001 = -376$ | decrypts to 0, which is wrong |

The noise went $5, 25, 625$ through two levels of AND, and the second level passed $p/2$. With the toy parameters of the code ($\eta = 192$ and fresh noise of about 33 binary digits), the noise of a product of 4 fresh ciphertexts has about 130 binary digits and decrypts correctly, and a product of 8 has about 260 and does not.

## Correctness

Each ciphertext is $c = \nu + pk$ with $\nu \equiv m \pmod 2$. A fresh ciphertext has $\nu = m + 2r + 2\sum_{i \in S} r_i - j r_0$, where $j$ is the number of times line L6 subtracts $x_0$; $r_0 = [x_0]_p$ is even by line L3, so $\nu \equiv m \pmod 2$. For two ciphertexts, $c_1 + c_2 = (\nu_1 + \nu_2) + p(k_1 + k_2)$ and $c_1 c_2 = \nu_1 \nu_2 + p(\nu_1 k_2 + \nu_2 k_1 + p k_1 k_2)$, and $\nu_1 + \nu_2 \equiv m_1 \oplus m_2$, $\nu_1 \nu_2 \equiv m_1 m_2 \pmod 2$. By induction over the circuit, the output has the form $\nu + pk$ with $\nu \equiv f(m_1, \ldots, m_\ell) \pmod 2$, and line L9 is right whenever $|\nu| < p/2$. The proof file gives the bound on fresh noise and the depth that the toy parameters allow, and proves that RECRYPT refreshes.

## Complexity

- **Sizes in the paper.** For security parameter $\lambda$, DGHV takes $\rho = \lambda$, $\rho' = 2\lambda$, $\eta = \tilde{O}(\lambda^2)$, $\gamma = \tilde{O}(\lambda^5)$ and $\tau = \gamma + \lambda$. The public key then has $\tau \gamma = \tilde{O}(\lambda^{10})$ binary digits. Coron, Mandal, Naccache and Tibouchi (2011) made it shorter.
- **Encryption.** A sum of up to $t$ integers of $g$ binary digits and one reduction modulo $x_0$: $\Theta(t g)$ bit operations.
- **Evaluation.** An XOR gate is an addition, $\Theta(g)$. An AND gate is a multiplication, $\Theta(g^2)$ with schoolbook arithmetic. Without reduction modulo $x_0$ ciphertexts grow with the degree of the circuit; reducing modulo $x_0$ keeps them at $g$ binary digits but adds $j r_0$ to the noise.
- **Decryption.** One reduction modulo $p$: $\Theta(g \eta)$.
- **Bootstrapping.** One refresh evaluates the squashed decryption circuit, which costs thousands of homomorphic gates. Gentry and Halevi (2011) reported recryption times from 30 seconds to 30 minutes and public keys from about 70 megabytes to 2.3 gigabytes for their implementation of Gentry's lattice scheme. FHEW (2015) and TFHE (2016) later bootstrapped one gate in under a second and under 0.1 seconds.

## Properties

- **Compact and fully homomorphic with bootstrapping.** With squashing and bootstrapping, any circuit can be evaluated and ciphertexts have a fixed size.
- **Semantic security.** DGHV is IND-CPA under the approximate GCD assumption: given many near multiples $p q_i + r_i$ of a secret $p$, finding $p$ is hard. Gentry's original scheme rests on a worst-case problem over ideal lattices. Squashing adds the sparse subset sum assumption and bootstrapping with one key adds circular security.
- **Not IND-CCA2.** No homomorphic scheme can be IND-CCA2; see [homomorphic encryption](/homomorphic-encryption/).
- **Noise is the central quantity.** It adds under XOR and multiplies under AND, so the depth of AND gates, not the number of gates, sets the limit.

## Variants and improvements

- **Gentry's ideal lattice scheme (2009).** The secret key is a short basis of an ideal lattice $J$ in a ring $\mathbb{Z}[x]/(f(x))$, a ciphertext is a message vector plus a small error, shifted by a public bad basis of $J$, and decryption reduces modulo the good basis. The structure of the blueprint is the same as on this page.
- **Leveled FHE without bootstrapping (BGV 2012).** Brakerski, Gentry and Vaikuntanathan scale the ciphertext down to a smaller modulus after each multiplication (modulus switching), so noise grows linearly in the depth instead of exponentially, from [ring LWE](/ring-learning-with-errors/). Bootstrapping is then needed only for circuits deeper than the parameters allow.
- **Scale invariance (Brakerski 2012, BFV).** The message is put in the high-order digits, so noise growth does not depend on the modulus.
- **GSW (2013), FHEW (2015) and TFHE (2016).** Ciphertexts are matrices with the message as an approximate eigenvalue, and noise grows slowly enough that one gate can be bootstrapped at a time.
- **CKKS (2017).** Approximate arithmetic on real numbers, where noise is part of the rounding error.

## When to use it

Use fully homomorphic encryption when a party must compute on data it may not see, and when the cost (thousands to millions of times a computation in the clear) is acceptable: private queries, private inference with a small model, or statistics on encrypted records. Use a maintained library such as OpenFHE, Microsoft SEAL, HElib, Lattigo or TFHE-rs, with parameters from the HomomorphicEncryption.org Security Standard. Do not use DGHV or Gentry's lattice scheme in new systems; the second and third generation schemes are much faster. If only additions are needed, an additive scheme such as [Paillier](/paillier-cryptosystem/) is simpler. If the parties are online, [secure multiparty computation](/secure-multiparty-computation/) may be cheaper.

## Pitfalls

- **Noise overflow is silent.** A ciphertext whose noise passed $p/2$ decrypts to a random-looking bit with no error message, as in the last row of the example. The application must track the depth of each value.
- **Circular security is an assumption.** Publishing an encryption of the secret key under its own public key is not covered by IND-CPA. For the schemes in use no attack is known, but it is not proved.
- **Results that leak noise.** If decrypted results of approximate schemes are shared, the noise inside them can reveal the key (Li and Micciancio 2021).
- **No integrity.** Any party can change an encrypted value by a homomorphic operation. Combine with signatures, proofs or a trusted evaluator as the application needs.
- **Toy parameters.** The parameters of the example and the code ($\eta = 192$, $\gamma = 2048$, $\tau = 24$) give no security; the sizes in the paper grow as $\gamma = \tilde{O}(\lambda^5)$.

## Implementations

The Python code is DGHV, not Gentry's ideal lattice scheme, and it does not bootstrap: it has no squashing and no homomorphic decryption, so it evaluates only circuits of small multiplicative depth. Bootstrapping is described above in prose and pseudocode only. The code is for study only, it is not constant time, and it must not protect real data; use OpenFHE, Microsoft SEAL or TFHE-rs instead. There are no official test vectors for DGHV or for Gentry's scheme. The tests check the example above, round trips, the truth tables of XOR and AND, a homomorphic full adder, the growth of the noise under addition and multiplication, and the failure of decryption once the noise passes $p/2$, with a fixed seed.

## History

Rivest, Adleman and Dertouzos asked for computation on encrypted data in 1978, and for thirty years only schemes with one operation, or with very limited depth, were known. Gentry's STOC 2009 paper and his Stanford thesis gave the first fully homomorphic scheme, from ideal lattices, with the bootstrapping theorem as the key idea. In 2010 van Dijk, Gentry, Halevi and Vaikuntanathan showed that the blueprint works over the integers. Smart and Vercauteren (2010) and then Gentry and Halevi (2011) implemented variants of the lattice scheme, the second one with bootstrapping. Brakerski and Vaikuntanathan (2011) and Brakerski, Gentry and Vaikuntanathan (2012) moved FHE to learning with errors and made it practical. Gentry, Sahai and Waters (2013), FHEW (2015), TFHE (2016) and CKKS (2017) followed.

## References
