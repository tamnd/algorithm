---
tag: MD60D5
kind: algorithm
slug: frodokem
name: FrodoKEM
aliases:
- Frodo
area: cryptography/post-quantum
level: advanced
summary: "A conservative KEM built on plain LWE with no ring or module structure. Keys and ciphertexts are about 10 to 22 kB, in exchange for fewer structural assumptions than Kyber."
model: word-ram
complexity:
  vars: {n: "the LWE dimension (640, 976 or 1344)", m: the number of columns of S (8)}
  time: {worst: Θ(n^2 m), average: Θ(n^2 m), best: Θ(n^2 m)}
  space: {extra: Θ(n m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2016
  people: [Joppe Bos, Craig Costello, Léo Ducas, Ilya Mironov, Michael Naehrig, Valeria Nikolaenko, Ananth Raghunathan, Douglas Stebila]
  note: Frodo, a key exchange from plain LWE, appeared at ACM CCS 2016. FrodoKEM was submitted to NIST in 2017 and was a round 3 alternate; it was then proposed for ISO/IEC 18033-2.
prereqs: [regev-encryption, learning-with-errors, key-encapsulation-mechanism, fujisaki-okamoto-transform]
see_also: [crystals-kyber, newhope, saber, lattice-based-cryptography, shake, ind-cca-security, inverse-transform-sampling, nist-pqc-standardization]
sources:
  - paper: doi:10.1145/2976749.2978425
    title: Joppe Bos, Craig Costello, Léo Ducas, Ilya Mironov, Michael Naehrig, Valeria Nikolaenko, Ananth Raghunathan and Douglas Stebila, Frodo, take off the ring! Practical, quantum-secure key exchange from LWE, ACM CCS 2016, pages 1006 to 1018
    locator: the case for plain LWE, the matrix A generated from a seed, the error distribution from a small table, and the reconciliation of the 2016 key exchange
  - url: "https://frodokem.org/"
    title: Erdem Alkim, Joppe Bos, Léo Ducas, Patrick Longa, Ilya Mironov, Michael Naehrig, Valeria Nikolaenko, Chris Peikert, Ananth Raghunathan and Douglas Stebila, FrodoKEM, learning with errors key encapsulation, NIST round 3 specification, June 2021
    locator: "the components Frodo.Encode, Decode, Pack, Sample, SampleMatrix and Gen, the algorithms of FrodoPKE and FrodoKEM, the parameter table, the CDF tables, and the failure rates"
  - url: "https://github.com/microsoft/PQCrypto-LWEKE"
    title: Microsoft Research, the FrodoKEM repository, known answer test files
    locator: "eFrodoKEM/KAT/PQCkemKAT_19888_shake.rsp, count = 0 (the seed and the digests of pk, sk and ct are copied in the tests)"
  - paper: "ISO/IEC 18033-2:2006/Amd 2, Information technology, Security techniques, Encryption algorithms, Part 2, Asymmetric ciphers, Amendment 2"
    title: ISO/IEC 18033-2 amendment 2 (ISO project 86890), which adds FrodoKEM together with ML-KEM and Classic McEliece
    locator: the FrodoKEM section; the publication in 2026 is reported by secondary sources and was not checked against the ISO text
  - paper: doi:10.6028/NIST.IR.8413-upd1
    title: NIST, IR 8413 (update 1), Status report on the third round of the NIST post-quantum cryptography standardization process, 2022
    locator: the section on FrodoKEM (an alternate, its conservative design, and the reasons it was not selected)
---

FrodoKEM is a key encapsulation mechanism whose security rests on the plain [learning with errors](/learning-with-errors/) problem, with no ring or module structure. It is a matrix version of [Regev encryption](/regev-encryption/): the public key is $B = A S + E$ for a random square matrix $A$ of size $n \times n$ with $n$ in the hundreds, generated from a short seed, and a secret matrix $S$ with $\bar n = 8$ columns, so that one encryption carries 64 entries with $B$ bits each. A [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) with implicit rejection makes it IND-CCA secure. Because it avoids the algebraic structure of [Kyber](/crystals-kyber/) and [NewHope](/newhope/), FrodoKEM is about ten times larger and slower, and it is the scheme that some national agencies recommend for long-term, conservative use. This page implements FrodoKEM-640-SHAKE of round 3.

**Notation.** $q = 2^{D}$ is a power of two ($D = 15$ or 16), so arithmetic modulo $q$ is a mask of the low $D$ bits. $n$ is the LWE dimension and $\bar n = 8$. $A \in \mathbb{Z}_q^{n \times n}$. $S, E \in \mathbb{Z}^{n \times \bar n}$ and $S', E' \in \mathbb{Z}^{\bar n \times n}$, $E'' \in \mathbb{Z}^{\bar n \times \bar n}$ have small entries from the error distribution $\chi$. Encode maps a string of $B \bar n^2$ bits to a matrix in $\mathbb{Z}_q^{\bar n \times \bar n}$ by placing each $B$-bit chunk $k$ at $k \cdot q / 2^B$, and Decode rounds each entry to the nearest multiple of $q/2^B$. SHAKE is SHAKE128 for the 640 set and SHAKE256 for the others; $len$ is the length of keys and seeds in bytes (16, 24 or 32).

## In plain words

FrodoKEM lets two parties agree on a secret key over a public channel. The public key is a large table of numbers, made from a random table and a small secret with a little noise added. Without the secret, the public table looks fully random.

To send a key, the sender makes up a random message, mixes it with a fresh small secret and the public table, and hides the message in the top part of some numbers. The receiver uses the secret to remove almost all of the mix. Only a little noise is left, so the receiver rounds it away and gets the message.

The receiver then repeats the sender's work to check the ciphertext. FrodoKEM uses plain tables instead of polynomials, which costs more space but trusts fewer assumptions.

## The problem

A [key encapsulation mechanism](/key-encapsulation-mechanism/) has KeyGen, Encaps, which returns a ciphertext and a shared secret, and Decaps, which recovers the shared secret from the ciphertext with the secret key. FrodoKEM targets [IND-CCA](/ind-cca-security/) security: even an adversary who can decapsulate other ciphertexts cannot tell the shared secret from random. The hardness assumption is decision LWE with the matrix $A$, which has no structure beyond being pseudorandom from its seed.

## The algorithm

```pseudo id=main
KEYGEN()
L1  s, seedSE, z ← random strings of len bytes
L2  seedA ← SHAKE(z, len);  A ← Frodo.Gen(seedA)      ▷ n × n, from AES-128 or SHAKE128
L3  r ← SHAKE(0x5F ‖ seedSE);  Sᵀ, E ← Frodo.SampleMatrix(r)    ▷ entries from χ by a CDF table
L4  B ← A·S + E  (mod q)
L5  pk ← seedA ‖ Pack(B);  pkh ← SHAKE(pk, len)
L6  return pk, sk = s ‖ pk ‖ Sᵀ ‖ pkh

ENCAPS(pk)
L7  μ ← random string of len bytes
L8  (seedSE, k) ← SHAKE(pkh ‖ μ, 2·len)
L9  r ← SHAKE(0x96 ‖ seedSE);  S', E', E'' ← Frodo.SampleMatrix(r)
L10 B' ← S'·A + E';  V ← S'·B + E''
L11 C ← V + Encode(μ)
L12 ct ← Pack(B') ‖ Pack(C)
L13 return ct, ss = SHAKE(ct ‖ k, len)

DECAPS(sk, ct)
L14 M ← C − B'·S
L15 μ' ← Decode(M)
L16 (seedSE', k') ← SHAKE(pkh ‖ μ', 2·len)
L17 B'', C' ← lines L9 to L11 again with seedSE' and μ'
L18 if B' = B'' and C = C' then return SHAKE(ct ‖ k', len)
L19 return SHAKE(ct ‖ s, len)                         ▷ implicit rejection
```

**The matrix A.** Line L2 expands $A$ from a seed of 16 bytes, so the public key does not carry $n^2$ entries. Row $i$ comes from SHAKE128 on the 2-byte index $i$ and the seed, or from AES-128 in counter mode keyed with the seed; the AES variant is faster on processors with AES instructions. Each user has a fresh $A$, which rules out the precomputation attacks that a fixed matrix would allow.

**The error distribution.** Lines L3 and L9 read 16-bit values from SHAKE and turn each into a small integer with a table: the top 15 bits are compared with the cumulative table and the low bit is the sign. For FrodoKEM-640 the table has 13 entries, from 4643 to 32767, so errors are in $[-12, 12]$ and close to a rounded Gaussian with $\sigma = 2.8$. This is [inverse transform sampling](/inverse-transform-sampling/); the reference code scans the whole table so that it runs in constant time.

**Parameter sets** (round 3 specification):

| set | $n$ | $q$ | $B$ | $\sigma$ | pk | ct | ss | category |
|---|---|---|---|---|---|---|---|---|
| FrodoKEM-640 | 640 | $2^{15}$ | 2 | 2.8 | 9616 | 9720 | 16 | 1 |
| FrodoKEM-976 | 976 | $2^{16}$ | 3 | 2.3 | 15632 | 15744 | 24 | 3 |
| FrodoKEM-1344 | 1344 | $2^{16}$ | 4 | 1.4 | 21520 | 21632 | 32 | 5 |

Sizes are in bytes. The secret keys are 19888, 31296 and 43088 bytes. Each set comes with A from AES (FrodoKEM-640-AES and so on) or from SHAKE.

## Example

**Encode and Decode.** For FrodoKEM-640, $q = 2^{15} = 32768$ and $B = 2$, so a 2-bit chunk $k$ is placed at $k \cdot 2^{13}$. The chunk $k = 3$ becomes 24576. After noise $+4000$ the entry is 28576; Decode computes $\lfloor (28576 + 4096) / 8192 \rfloor = 3$, so the chunk survives. After noise $-4097$ the entry is 20479, and Decode returns 2, which is wrong. So Decode is correct for noise in $[-4096, 4095]$, that is $|\text{noise}| < q / 2^{B+1}$ up to the one border value.

**The sampler.** The 16-bit value $r = 9288$ has top part $p = 4644$ and sign bit 0. It is larger than the first table entry 4643 and not larger than the second, so the sample is $+1$. The value $r = 9289$ gives $-1$.

**An official vector.** The known answer file `PQCkemKAT_19888_shake.rsp` (FrodoKEM-640-SHAKE), count 0, starts from the DRBG seed `061550234D158C5E...` and gives the shared secret `729780FC51657E21357F03A338116569`. The code on this page reproduces this secret and the SHA-256 digests of the official pk, sk and ct.

## Correctness

Write $M = C - B' S$. By lines L4, L10 and L11,
$$M = S'(A S + E) + E'' + \mathrm{Encode}(\mu) - (S' A + E') S = \mathrm{Encode}(\mu) + S' E - E' S + E''.$$
The products $S' A S$ cancel because matrix multiplication is associative. Decode returns $\mu$ when every entry of the noise $S' E - E' S + E''$ lies in $[-q/2^{B+1}, q/2^{B+1})$. Then line L16 recomputes the same seed and key, line L17 recomputes the same ciphertext, because SHAKE and SampleMatrix are deterministic, and line L18 returns the shared secret of line L13. Each entry of the noise is a sum of $2n$ products of small values plus one small value, so it is far below $q/8$ with very high probability; the specification computes the exact failure rate, about $2^{-138.7}$ for FrodoKEM-640. The full proof is in the proof file.

## Complexity

The cost is in the matrix products of lines L4 and L10: $\Theta(n^2 \bar n)$ multiplications modulo $q$, about 3.3 million for $n = 640$, plus the generation of $A$, which is $n^2$ values from SHAKE or AES. Decapsulation does the same work again for the re-encryption, plus the $\Theta(n \bar n^2)$ product of line L14. The code can generate $A$ one row at a time, so the extra memory is $\Theta(n \bar n)$ for $S$, $E$ and $B$. Keys and ciphertexts have $\Theta(n \bar n)$ entries of $D$ bits.

## Properties

- **IND-CCA security.** FrodoPKE (lines L1 to L11 without hashing) is IND-CPA secure under decision LWE by a hybrid argument: $B$ is replaced by a random matrix, and then $(B', V)$ is too. The FO transform with implicit rejection gives IND-CCA in the random oracle model, and in the quantum random oracle model with a looser bound.
- **No algebraic structure.** Attacks that use the structure of rings or modules do not apply. The concrete security comes from the best known attacks on plain LWE, mainly BKZ lattice reduction (the primal and dual attacks).
- **Simple arithmetic.** With $q$ a power of two, reduction is a mask, and no NTT is needed.
- **Large.** Each key and ciphertext is about 10 to 22 kB, compared with about 1 kB for Kyber.

## Variants and improvements

- **Frodo (2016)** was an unauthenticated key exchange with a reconciliation step in the style of Peikert; FrodoKEM (2017) replaced it with the encryption and the FO transform.
- **eFrodoKEM and FrodoKEM.** The current FrodoKEM documents name the round 3 scheme eFrodoKEM and say that it should be used only with ephemeral keys. The standard FrodoKEM, proposed for ISO, adds a random salt to the ciphertext and hashes it into the seed, which gives better multi-target security when one key is used many times. The code on this page is eFrodoKEM-640-SHAKE, which matches the round 3 vectors.
- **ISO standard.** FrodoKEM was proposed for an amendment to ISO/IEC 18033-2 together with ML-KEM and Classic McEliece. Secondary sources say that the amendment was published in 2026; this page could not check the ISO text.
- **Lindner-Peikert encryption** (2011) is the matrix form of Regev encryption that FrodoPKE follows, with a square $A$ and small secrets on both sides.

## When to use it

Use FrodoKEM when you want the most conservative lattice KEM and can afford about 20 kB per exchange, for example for long-term secrets in a [hybrid key exchange](/hybrid-key-exchange/) with a classical scheme. BSI in Germany and other agencies list it as a recommended KEM. For most uses, [ML-KEM](/crystals-kyber/) is smaller, faster, and a NIST standard.

## Pitfalls

- **Timing in the sampler or the comparison.** The table lookup must scan all entries, and the check of line L18 must compare all bytes in constant time, or decapsulation leaks information on the secret key.
- **Reusing keys with eFrodoKEM.** The ephemeral variant is meant for one-time keys; for static keys use the salted FrodoKEM.
- **Generating A with the wrong order.** The AES and SHAKE variants fill $A$ in a fixed order of indices; a different order gives a different scheme, and the test vectors fail.
- **Memory.** Storing all of $A$ takes $2n^2$ bytes, about 3.6 MB for $n = 1344$; generate it row by row on small devices.

## Implementations

The Python code on this page implements FrodoKEM-640-SHAKE of round 3 (eFrodoKEM): Gen with SHAKE128, the CDF sampler, Pack, Encode and Decode, and the three KEM algorithms. The tests run the NIST AES-256 CTR_DRBG to reproduce the official known answer vector `PQCkemKAT_19888_shake.rsp`, count 0, and compare the shared secret and the SHA-256 digests of pk, sk and ct, copied by hand from the official file. They also check implicit rejection, the sampler table, and the noise range of Decode. The AES variant, the larger sets and the salted FrodoKEM are not implemented. The code is for study only: it is not constant time and it is slow. Use the reference code of the FrodoKEM team or liboqs.

## History

Regev (2005) defined LWE and a bit encryption scheme, and Lindner and Peikert (2011) gave the matrix form with small secrets. Ring-LWE schemes such as [NewHope](/newhope/) were much smaller, but Bos, Costello, Ducas, Mironov, Naehrig, Nikolaenko, Raghunathan and Stebila argued at CCS 2016 that plain LWE was practical enough, in the paper "Frodo, take off the ring!". The KEM version was submitted to NIST in 2017, reached round 3 as an alternate in 2020, and was not selected in 2022, with NIST noting that it remains a conservative choice. Several European agencies recommend it.

## References
