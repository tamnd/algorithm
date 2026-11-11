---
tag: EKXD4J
kind: algorithm
slug: regev-encryption
name: Regev encryption
aliases:
- LWE encryption
- Regev cryptosystem
area: cryptography/post-quantum
level: advanced
summary: "Encrypt one bit from LWE: add a random subset of the samples (A, As + e) and shift by q/2 for a 1. Decryption is correct while the error sum stays below q/4. IND-CPA under decision LWE."
model: word-ram
complexity:
  vars: {n: the LWE dimension, m: the number of samples in the public key}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2005
  people: [Oded Regev]
  note: Presented at STOC 2005 with the quantum reduction from worst-case lattice problems to LWE. The journal version appeared in the Journal of the ACM in 2009. Regev received the 2018 Gödel Prize for this work.
prereqs: [learning-with-errors, public-key-encryption]
see_also: [regev-lwe-hardness, leftover-hash-lemma, ind-cpa-security, lattice-based-cryptography, ring-learning-with-errors, frodokem, crystals-kyber, semantic-security]
sources:
  - paper: doi:10.1145/1060590.1060603
    title: Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, STOC 2005, pages 84 to 93
    locator: the public key cryptosystem from LWE (key generation, encryption of one bit, decryption) and its parameters
  - paper: doi:10.1145/1568318.1568324
    title: Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6), 2009, article 34
    locator: Section 5, Public key cryptosystem (the parameters q, m and alpha, the correctness lemma, and the security lemma that uses the leftover hash lemma)
  - url: "https://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf"
    title: Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), 2016
    locator: the section on LWE public-key encryption (Regev's cryptosystem, its dual, and the more compact variants)
  - paper: doi:10.1145/1374376.1374407
    title: Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008, pages 197 to 206
    locator: Section 7.1, the dual cryptosystem, in which the roles of key generation and encryption are swapped
---

Regev encryption is the first public-key encryption scheme built on the [learning with errors](/learning-with-errors/) problem. The public key is a list of $m$ noisy linear equations $b = A s + e \bmod q$ in a secret vector $s$. To encrypt one bit, the sender adds a random subset of the equations and shifts the right-hand side by about $q/2$ when the bit is 1. The receiver, who knows $s$, removes the linear part and sees the bit plus a small error. Regev introduced it in 2005, together with the proof that LWE is as hard as worst-case lattice problems for quantum algorithms (see [Regev's hardness theorem](/regev-lwe-hardness/)). Under decision LWE the scheme is [IND-CPA secure](/ind-cpa-security/). It is the ancestor of [FrodoKEM](/frodokem/), [CRYSTALS-Kyber](/crystals-kyber/) and most other lattice encryption.

**Notation.** $q$ is the modulus, $n$ the dimension of the secret and $m$ the number of samples. $\mathbb{Z}_q$ is the set $\{0, \ldots, q-1\}$ with arithmetic mod $q$. $A \in \mathbb{Z}_q^{m \times n}$ is uniform, $s \in \mathbb{Z}_q^n$ is the secret, and $e \in \mathbb{Z}^m$ is an error vector with small entries. A bit is $\mu \in \{0, 1\}$, and $x \in \{0,1\}^m$ selects a subset of the rows. For an integer $d$, the value $d \bmod q$ is taken in $[0, q-1]$.

## In plain words

The owner picks a secret list of numbers. The public key is many linear equations in these secret numbers, and each equation has a small error added, so nobody can solve them. To send a bit, you pick a random set of these equations and add them together. The result is one new equation that still has a small error. If the bit is 1, you also add half of the modulus to its right side.

The owner knows the secret, so the owner can compute the exact right side of the new equation and compare. The difference is the small error when the bit is 0, and about half of the modulus when the bit is 1. As long as the errors stay small, the owner can tell the two cases apart. Without the secret, the equations look random, so the message stays hidden.

## The problem

The scheme solves [public-key encryption](/public-key-encryption/) of one bit: key generation, encryption with the public key and decryption with the secret key, such that decryption recovers the bit with high probability, and no efficient adversary that knows the public key can tell an encryption of 0 from an encryption of 1 (IND-CPA). The assumption is decision LWE: for uniform $A$ and $s$ and small $e$, the pair $(A, A s + e)$ cannot be told apart from a uniform pair $(A, b)$.

## The algorithm

```pseudo id=main
KEYGEN()
L1  A ← uniform in Z_q^(m×n);  s ← uniform in Z_q^n
L2  e ← error distribution χ^m               ▷ small entries
L3  b ← A·s + e mod q
L4  return pk = (A, b), sk = s

ENCRYPT(pk = (A, b), μ ∈ {0, 1})
L5  x ← uniform in {0, 1}^m                  ▷ a random subset of the rows
L6  u ← xᵀ·A mod q                           ▷ a vector in Z_q^n
L7  v ← xᵀ·b + μ·⌊q/2⌋ mod q                 ▷ one number in Z_q
L8  return c = (u, v)

DECRYPT(sk = s, c = (u, v))
L9  d ← v − ⟨u, s⟩ mod q                     ▷ equals xᵀe + μ·⌊q/2⌋ mod q
L10 if ⌊q/4⌋ < d < q − ⌊q/4⌋ then return 1 else return 0
```

Line L10 rounds $d$ to the nearer of $0$ and $\lfloor q/2 \rfloor$ on the circle $\mathbb{Z}_q$. A message of $\ell$ binary digits is sent as $\ell$ ciphertexts, one per bit.

**Parameters of the paper.** Regev takes $q$ prime between $n^2$ and $2n^2$, $m = (1 + \varepsilon)(n + 1)\log q$ for a constant $\varepsilon > 0$, and the error distribution $\bar\Psi_\alpha$: a normal variable of standard deviation $\alpha q / \sqrt{2\pi}$, rounded to the nearest integer, with $\alpha = 1/(\sqrt{n} \log^2 n)$. The choice of $m$ makes the leftover hash lemma apply in the security proof, and the choice of $\alpha$ makes the error sum smaller than $q/4$ with high probability.

## Example

Take $q = 97$, $n = 2$ and $m = 4$. These numbers are far too small to be secure.

| step | value |
|---|---|
| $A$ (rows) | $(12, 40), (71, 5), (33, 88), (9, 60)$ |
| secret $s$ | $(17, 51)$ |
| error $e$ | $(1, -2, 0, 1)$ |
| $b = A s + e \bmod 97$ | $(14, 5, 5, 13)$ |
| subset $x$ | $(1, 0, 1, 1)$, so rows 1, 3 and 4 |
| $u = x^\mathsf{T} A \bmod 97$ | $(54, 91)$ |
| $v$ for $\mu = 0$ | $14 + 5 + 13 = 32$ |
| $v$ for $\mu = 1$ | $32 + 48 = 80$ |

Decryption computes $\langle u, s \rangle = 54 \cdot 17 + 91 \cdot 51 = 5559 \equiv 30 \pmod{97}$. For $\mu = 0$ it gets $d = 32 - 30 = 2$, which is not in the range $(24, 73)$, so it returns 0. For $\mu = 1$ it gets $d = 80 - 30 = 50$, which is in the range, so it returns 1. In both cases the error part is $x^\mathsf{T} e = 1 + 0 + 1 = 2$.

## Correctness

Line L9 gives $d \equiv x^\mathsf{T}(A s + e) + \mu \lfloor q/2 \rfloor - x^\mathsf{T} A s = x^\mathsf{T} e + \mu \lfloor q/2 \rfloor \pmod q$. If $|x^\mathsf{T} e| < \lfloor q/4 \rfloor$, then $d$ lies within $\lfloor q/4 \rfloor$ of $0$ when $\mu = 0$ and within $\lfloor q/4 \rfloor$ of $\lfloor q/2 \rfloor$ when $\mu = 1$, so line L10 returns $\mu$. The error sum has at most $m$ terms, each a rounded normal variable, so it is a sum of about $m/2$ small independent values; with the parameters of the paper its size is about $\alpha q \sqrt{m}$, which is $o(q)$, and a tail bound makes the failure probability negligible. The full proof, with the exact rounding rule, is in the proof file.

## Complexity

- **Key generation**: $m n$ multiplications mod $q$ to compute $A s$.
- **Encryption of one bit**: about $m n / 2$ additions mod $q$ for $u$ and $m/2$ for $v$.
- **Decryption**: $n$ multiplications mod $q$.
- **Sizes**: the public key has $m(n + 1)$ numbers mod $q$, so $\Theta(n^2 \log^2 q)$ binary digits with $m = \Theta(n \log q)$. A ciphertext of one bit has $n + 1$ numbers mod $q$, an expansion factor of about $n \log q$.

The large key and the large expansion are the reasons why practical schemes use the variants below.

## Properties

- **IND-CPA under decision LWE.** Replace $b$ by a uniform vector; an adversary that notices the change breaks decision LWE. With a uniform $b$, the matrix $[A \mid b] \in \mathbb{Z}_q^{m \times (n+1)}$ is uniform and $x$ has $m$ binary digits of entropy, so by the [leftover hash lemma](/leftover-hash-lemma/) the pair $x^\mathsf{T} [A \mid b]$ is statistically close to uniform in $\mathbb{Z}_q^{n+1}$, for $m \ge (1+\varepsilon)(n+1)\log q$. Then the shift $\mu \lfloor q/2 \rfloor$ is hidden.
- **Not IND-CCA.** The scheme is malleable: adding $\lfloor q/2 \rfloor$ to $v$ flips the bit, and adding two ciphertexts gives an encryption of the XOR of the bits with a larger error. A chosen ciphertext attacker can also learn $s$ with decryption queries on crafted $(u, v)$. Real KEMs add the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/).
- **Small decryption failure.** Correctness holds with high probability over the key and the coins, not always. The failure probability depends on the ratio of $q$ to the error size.
- **Randomized.** Encryption uses fresh coins $x$. With the same $x$, the ciphertexts of 0 and 1 differ only by $\lfloor q/2 \rfloor$ in $v$.

## Variants and improvements

- **Many bits per ciphertext.** Use a secret matrix $S \in \mathbb{Z}_q^{n \times \ell}$ instead of one vector and encode $\ell$ bits in $\ell$ values of $v$. The cost of $u$ is shared. Peikert, Vaikuntanathan and Waters (2008) analyse this form, and [FrodoKEM](/frodokem/) uses it with $\ell = 8$ columns.
- **The secret and the coins from the error distribution.** Applebaum, Cash, Peikert and Sahai (2009) showed that LWE stays hard when $s$ is drawn from the error distribution. Lindner and Peikert (2011) then replaced the subset $x$ by a short random vector with its own error terms, which removes the need for the leftover hash lemma and allows $m \approx n$. This is the form behind [FrodoKEM](/frodokem/) and, over rings, [NewHope](/newhope/) and [CRYSTALS-Kyber](/crystals-kyber/).
- **Dual Regev.** Gentry, Peikert and Vaikuntanathan (2008) swapped the roles: the public key is a syndrome $u = A^\mathsf{T} x$ of a short secret $x$, and a ciphertext is an LWE sample. It is the basis of identity-based encryption from lattices.
- **Structured lattices.** [Ring-LWE](/ring-learning-with-errors/) and [module-LWE](/module-learning-with-errors/) replace $A$ by a matrix of polynomials, which cuts the key size from $\Theta(n^2)$ to $\Theta(n)$ numbers and allows the [number-theoretic transform](/number-theoretic-transform/).

## When to use it

Use Regev encryption to learn and teach how LWE gives encryption, and as the base case when you read a security proof of a lattice scheme. Do not deploy it: its keys and ciphertexts are large, it is only IND-CPA, and its parameters predate modern estimates of attack cost. To protect data, use a standard KEM such as [ML-KEM](/crystals-kyber/), or [FrodoKEM](/frodokem/) if you want plain LWE without ring structure.

## Pitfalls

- **Too much error.** If $\alpha q \sqrt{m}$ is close to $q/4$, many bits decrypt wrongly. The test file shows this with $\sigma = 150$ and $q = 4093$.
- **Too few samples.** With $m$ below about $(n + 1)\log q$, the leftover hash lemma does not apply, and the security proof breaks.
- **No CCA security.** Used directly against an active attacker, the scheme leaks the bit by malleability and the key by decryption queries. Add the Fujisaki-Okamoto transform and check the re-encryption.
- **Bad randomness.** The subset $x$ must be uniform and fresh. A reused $x$ for two bits shows their XOR from the difference of the two $v$ values.
- **Side channels.** The comparison in line L10 and the inner product in line L9 handle the secret, and must not leak timing.

## Implementations

The Python code on this page implements the scheme with a rounded Gaussian error, one bit per ciphertext. Regev encryption has no standard test vectors, so the tests check the algebra on toy parameters: many round trips, the bound on the error sum, a run where a too large error makes decryption fail, and the fact that the ciphertexts of 0 and 1 with the same coins differ by $\lfloor q/2 \rfloor$. The code is for study only. It is not constant time, its parameters are not secure, and it must not be used to protect real data.

## History

Oded Regev defined the LWE problem and this cryptosystem in his STOC 2005 paper, which also gave a quantum reduction from worst-case lattice problems to LWE. The journal version appeared in the Journal of the ACM in 2009, and Regev received the Gödel Prize in 2018 for it. Earlier lattice encryption by Ajtai and Dwork (1997) and by Regev himself (2004) had much larger keys or worse assumptions.

Later work made the scheme practical step by step: multi-bit and dual forms (Peikert, Vaikuntanathan and Waters 2008; Gentry, Peikert and Vaikuntanathan 2008), small secrets (Applebaum, Cash, Peikert and Sahai 2009), the compact form of Lindner and Peikert (2011), and the ring and module forms that led to the NIST standard ML-KEM in 2024.

## References
