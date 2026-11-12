---
tag: 47QEE6
kind: concept
slug: public-key-cryptography
name: Public-key cryptography
aliases:
- asymmetric cryptography
area: cryptography/public-key
level: intro
summary: Each party holds a public key and a private key, so two strangers can encrypt and sign without a shared secret. The price is arithmetic that is a thousand times slower.
prereqs: [modular-exponentiation]
see_also: [public-key-encryption, digital-signature, diffie-hellman, hybrid-encryption, trapdoor-one-way-function, rsa-cryptosystem, post-quantum-cryptography]
sources:
  - paper: "Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, November 1976"
    locator: Sections I to III (the public key distribution idea, one way authentication, and the trap door one way function that the paper asks for but does not supply)
  - url: "https://doi.org/10.1145/359340.359342"
    title: Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978
    locator: Sections 1 and 2 (the first published trapdoor one way permutation and the public-key scheme built from it)
  - url: "https://cryptocellar.org/cesg/possnse.pdf"
    title: James H. Ellis, The possibility of secure non-secret digital encryption, CESG report 3006, January 1970
    locator: the whole report (the existence argument for what is now called public-key encryption, with no construction)
  - url: "https://cryptocellar.org/cesg/notense.pdf"
    title: Clifford C. Cocks, A note on non-secret encryption, CESG, 20 November 1973
    locator: the whole note (the construction that is RSA with the public exponent equal to the modulus)
  - url: "https://cryptocellar.org/cesg/ellis.pdf"
    title: James H. Ellis, The story of non-secret encryption, CESG, 1987, released in 1997
    locator: the whole paper (the internal history of the GCHQ work of 1970 to 1974)
  - paper: "Malcolm J. Williamson, Non-secret encryption using a finite field, CESG, 21 January 1974, and Thoughts on cheaper non-secret encryption, CESG, 10 August 1976"
    locator: both notes (the key agreement method that matches the later Diffie-Hellman protocol)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the part on public-key cryptography (the setting, the key distribution problem it solves, and the hybrid argument for speed)
---

Public-key cryptography is cryptography in which each party holds two keys: a *public* key that anybody may have, and a *private* key that nobody else may have. The two keys are made together and are linked by mathematics, not by a shared secret. Whitfield Diffie and Martin Hellman proposed the idea in 1976 and asked for a function that is easy to compute and hard to invert without a secret, a [trapdoor one way function](/trapdoor-one-way-function/). [RSA](/rsa-cryptosystem/) supplied one in 1978. The same idea had been found at GCHQ between 1970 and 1974 and kept secret until 1997. Everything in this folder is a construction from that idea or an attack on one.

## In plain words

Before 1976 two people who wanted to exchange secret messages had to agree on a key first, in person or through a trusted courier. For a network of a thousand people that is half a million keys, and for two strangers on the internet it is impossible.

The new idea gives each person two matching keys. One is published, like a telephone number. The other is kept. A message locked with the published key opens only with the kept one, so anybody can write to you and only you can read it. A mark made with the kept key is checked with the published one, so only you can sign and anybody can verify.

The cost is arithmetic on numbers of hundreds of digits, which is slow. So real systems use it once, to agree on a small key, and then switch to a fast cipher.

## The idea

A public-key scheme starts from a *key generation* algorithm that outputs a pair $(pk, sk)$. The public key $pk$ fixes a function that anybody can evaluate; the private key $sk$ is the information that inverts it. Two shapes cover almost all of the field.

**Encryption.** Anybody who has $pk$ can compute $c = \mathrm{Enc}_{pk}(m)$, and only the holder of $sk$ can recover $m = \mathrm{Dec}_{sk}(c)$. The page [public-key encryption](/public-key-encryption/) gives the syntax and the security definitions.

**Signatures.** Only the holder of $sk$ can compute $\sigma = \mathrm{Sign}_{sk}(m)$, and anybody with $pk$ can check it. See [digital signature](/digital-signature/).

The mathematical object behind both is a family of functions $\{f_{pk}\}$ with three properties: $f_{pk}$ is easy to evaluate, it is hard to invert given $pk$ alone, and it is easy to invert given $sk$. That is a [trapdoor one way function](/trapdoor-one-way-function/), and the existence of one is a strictly stronger assumption than the existence of a plain [one way function](/one-way-function/); Impagliazzo and Rudich showed in 1989 that no black box construction turns the second into the first. A third shape, key agreement, needs less: [Diffie-Hellman](/diffie-hellman/) builds a shared secret from a one way function with a commuting structure and no trapdoor at all.

**Why the keys cannot be independent.** The public key determines the private key in principle, because the key pair is a mathematical relation and $sk$ is a short string. Security is therefore never information theoretic; it always rests on a [computational hardness assumption](/computational-hardness-assumption/), and every public-key scheme in use can be broken by an adversary with unbounded time. That is the trade the field makes for not needing couriers.

**Why public-key operations are slow.** The private operation of RSA with a 2048 binary digit modulus is a modular exponentiation: about 2048 squarings and 1000 multiplications of 2048 digit numbers, each of which is about $(2048/64)^2 = 1024$ word multiplications, so a few million word operations even with the [Chinese remainder theorem](/chinese-remainder-theorem/) and [Montgomery multiplication](/montgomery-multiplication/). A current processor does a few thousand such operations per second. An elliptic curve operation at the same security level is about ten times cheaper, since the keys are 256 digits instead of 2048, but it is still hundreds of multiplications in a field. A symmetric cipher, by contrast, moves gigabytes per second, because [AES](/advanced-encryption-standard/) does a few table lookups and exclusive ors per 16 octets and the hardware has an instruction for it.

The ratio is about three orders of magnitude per octet, and it does not shrink with better implementations, because it comes from the structure: public-key schemes need an algebraic object rich enough to carry a trapdoor, and algebra is expensive. There is a second cost of the same origin. The message must be an element of that algebraic object, so RSA with a 2048 digit modulus encrypts at most 256 octets, and 190 after [OAEP](/rsa-oaep/) padding.

**Hybrid encryption.** The answer to both costs is to use the public-key operation only on a short key. The sender draws a fresh symmetric key $k$, sends $\mathrm{Enc}_{pk}(k)$, and encrypts the message itself with an [authenticated cipher](/authenticated-encryption/) under $k$. The cost of the public-key part is then a constant, independent of the message length, and the length limit disappears. The modern form of this is the [key encapsulation mechanism](/key-encapsulation-mechanism/), which skips the step of encrypting a chosen key and lets the public-key part *derive* a random key directly; see [hybrid encryption](/hybrid-encryption/). Every protocol that uses public-key cryptography on real data, TLS included, is hybrid.

## Examples

**The first published scheme.** Diffie and Hellman's own paper gives key agreement, not encryption: both parties exponentiate in a group, $A = g^a$ and $B = g^b$, and both compute $g^{ab}$. The security rests on the [computational Diffie-Hellman](/computational-diffie-hellman/) assumption. The paper states the trapdoor requirement for public-key *encryption* and leaves it open.

**RSA.** The public key is $(N, e)$ with $N$ a product of two primes, and the function is $m \mapsto m^e \bmod N$. The trapdoor is the factorization, which gives the inverse exponent $d$. See [RSA](/rsa-cryptosystem/) and [the RSA problem](/rsa-problem/).

**Rabin.** The public key is a modulus and the function is squaring. This one has a *proof* that inverting it is as hard as factoring, which RSA lacks; see [Rabin](/rabin-cryptosystem/).

**A broken one.** The [Merkle-Hellman knapsack](/merkle-hellman-knapsack-cryptosystem/) hid an easy subset sum instance behind a modular multiplication. It was published in 1978 and broken in 1982 and 1985. It is the standard reminder that a hard problem is not a hard assumption.

**The secret history.** At GCHQ, James Ellis argued in 1970 that secure encryption without a shared secret is possible, without finding a way to do it. Clifford Cocks wrote down in 1973 a scheme that is RSA, with the public exponent equal to the modulus and no signature application. Malcolm Williamson found the key agreement method in 1974. None of it could be published, so none of it had any effect on the field until 1997, and the schemes carry the names of the people who published them.

## Where it is used

**This folder, as a map.** The theory of the setting: [public-key encryption](/public-key-encryption/), [one way function](/one-way-function/), [trapdoor one way function](/trapdoor-one-way-function/), [hard core predicate](/hard-core-predicate/), [computational hardness assumption](/computational-hardness-assumption/), [probabilistic encryption](/probabilistic-encryption/), [semantic security](/semantic-security/), [IND-CPA](/ind-cpa-security/), [IND-CCA](/ind-cca-security/), [non-malleability](/non-malleability/) and [chosen ciphertext attack](/chosen-ciphertext-attack/).

| family | the hard problem | the pages |
|---|---|---|
| factoring based | [integer factorization](/integer-factorization/), the [RSA problem](/rsa-problem/) | [RSA](/rsa-cryptosystem/), [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/), [OAEP](/rsa-oaep/), [Rabin](/rabin-cryptosystem/), [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) |
| residuosity based | [quadratic residuosity](/quadratic-residuosity-problem/), [composite residuosity](/decisional-composite-residuosity/) | [Goldwasser-Micali](/goldwasser-micali-cryptosystem/), [Paillier](/paillier-cryptosystem/), [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/), [Naccache-Stern](/naccache-stern-cryptosystem/) |
| discrete logarithm based | [CDH](/computational-diffie-hellman/), [DDH](/decisional-diffie-hellman/) | [ElGamal](/elgamal-encryption/), [Cramer-Shoup](/cramer-shoup-cryptosystem/), [ECIES](/ecies/), [elliptic curve cryptography](/elliptic-curve-cryptography/) |
| pairing based | [bilinear Diffie-Hellman](/bilinear-diffie-hellman/) | [bilinear pairing](/bilinear-pairing/), [identity based encryption](/identity-based-encryption/), [Boneh-Franklin](/boneh-franklin-ibe/), [attribute based encryption](/attribute-based-encryption/) |
| lattice and code based | [learning with errors](/learning-with-errors/), decoding | [ML-KEM](/crystals-kyber/), [McEliece](/mceliece-cryptosystem/), [NTRU](/ntru-encrypt/) |
| broken | subset sum with a trapdoor | [Merkle-Hellman knapsack](/merkle-hellman-knapsack-cryptosystem/) |

**Signatures** are in their own area: [digital signature](/digital-signature/) for the definition, then [RSA signature](/rsa-signature/), [RSA-PSS](/rsa-pss/), [full domain hash](/rsa-fdh/), [Rabin signature](/rabin-signature/), [DSA](/dsa/), [ECDSA](/ecdsa/), [Schnorr](/schnorr-signature/), [Ed25519](/ed25519/), [ML-DSA](/crystals-dilithium/), [SLH-DSA](/sphincs-plus/), [Lamport](/lamport-signature/) and [blind signatures](/blind-signature/). Signatures use the same key pairs and the same assumptions, and their security notion is [existential unforgeability](/existential-unforgeability/) rather than indistinguishability.

**Key exchange** is the third branch: [Diffie-Hellman](/diffie-hellman/), [ECDH](/ecdh/) and [X25519](/x25519/). It gives a shared secret rather than a ciphertext, needs no trapdoor, and is what a [TLS handshake](/tls-handshake/) actually runs, together with a signature for authentication.

**Post-quantum cryptography** is the fourth: [Shor's algorithm](/shor-algorithm/) breaks factoring and discrete logarithms in polynomial time on a quantum computer, which ends every scheme in the first four rows of the table above. The replacements rest on [lattice](/lattice-based-cryptography/) and coding problems: [ML-KEM](/crystals-kyber/) for encapsulation, [ML-DSA](/crystals-dilithium/) and [SLH-DSA](/sphincs-plus/) for signatures. See [post-quantum cryptography](/post-quantum-cryptography/) for the state of the migration.

**Where the attacks live.** Public-key schemes are rarely broken by solving the hard problem. They are broken through the implementation and the protocol: a [padding oracle](/padding-oracle-attack/), a [timing attack](/timing-attack/), a [fault attack](/rsa-fault-attack/), a bad key such as the one [Wiener's attack](/wiener-attack/) needs, or reused randomness. The defences include [blinding](/rsa-blinding/) and constant time code.

## References
