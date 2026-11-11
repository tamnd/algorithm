---
tag: 77379R
kind: definition
slug: homomorphic-encryption
name: Homomorphic encryption
aliases:
- HE
- FHE
area: cryptography/public-key
level: advanced
summary: "Encryption with a public evaluation algorithm that computes on ciphertexts, so that the result decrypts to the function of the plaintexts. Partial, somewhat, leveled and fully homomorphic."
prereqs: [public-key-encryption, ind-cpa-security, boolean-circuit]
see_also: [paillier-cryptosystem, gentry-fully-homomorphic-encryption, elgamal-encryption, goldwasser-micali-cryptosystem, ring-learning-with-errors, functional-encryption, secure-multiparty-computation, non-malleability]
sources:
  - paper: "Ronald L. Rivest, Leonard Adleman and Michael L. Dertouzos, On data banks and privacy homomorphisms, in Foundations of Secure Computation, Academic Press, 1978, pages 169 to 180"
    locator: the question of computing on encrypted data and the name privacy homomorphism
  - paper: "Craig Gentry, Fully homomorphic encryption using ideal lattices, STOC 2009, pages 169 to 178"
    locator: the definitions of compactness and of fully and leveled homomorphic encryption, and the first construction with bootstrapping
  - paper: "Zvika Brakerski, Craig Gentry and Vinod Vaikuntanathan, (Leveled) fully homomorphic encryption without bootstrapping, ITCS 2012, pages 309 to 325"
    locator: the BGV scheme from ring LWE with modulus switching, and the definition of leveled FHE
  - paper: "Craig Gentry, Amit Sahai and Brent Waters, Homomorphic encryption from learning with errors, conceptually-simpler, asymptotically-faster, attribute-based, Crypto 2013, LNCS 8042, pages 75 to 92"
    locator: the GSW scheme with the approximate eigenvector method
  - paper: "Jung Hee Cheon, Andrey Kim, Miran Kim and Yongsoo Song, Homomorphic encryption for arithmetic of approximate numbers, Asiacrypt 2017, LNCS 10624, pages 409 to 437"
    locator: the CKKS scheme for approximate arithmetic
  - paper: "Dan Boneh, Eu-Jin Goh and Kobbi Nissim, Evaluating 2-DNF formulas on ciphertexts, TCC 2005, LNCS 3378, pages 325 to 341"
    locator: a somewhat homomorphic scheme with any number of additions and one multiplication, from pairings
  - paper: "Baiyu Li and Daniele Micciancio, On the security of homomorphic encryption on approximate numbers, Eurocrypt 2021, LNCS 12696, pages 648 to 677"
    locator: the notion IND-CPA^D and the key recovery attack on CKKS from decryption results
  - url: "https://homomorphicencryption.org/standard/"
    title: Martin Albrecht and others, Homomorphic Encryption Security Standard, HomomorphicEncryption.org, November 2018
    locator: the tables of lattice dimensions and ciphertext moduli for 128, 192 and 256 bits of security for BGV, BFV and CKKS
  - paper: "ISO/IEC 18033-6:2019, IT security techniques, Encryption algorithms, Part 6, Homomorphic encryption"
    locator: the specification of exponential ElGamal and Paillier encryption with their homomorphic operations
---

Homomorphic encryption is [public-key encryption](/public-key-encryption/) with one more algorithm, Eval, that anyone can run. Eval takes a function $f$ and ciphertexts of $m_1, \ldots, m_\ell$, and outputs a ciphertext of $f(m_1, \ldots, m_\ell)$, without the secret key and without learning the $m_i$. Rivest, Adleman and Dertouzos asked for such "privacy homomorphisms" in 1978. Schemes that support one operation, such as [Paillier](/paillier-cryptosystem/) (addition), were known for decades. Craig Gentry built the first scheme that supports every function in 2009, and the schemes in use today are based on [learning with errors](/learning-with-errors/). The aliases HE and FHE (fully homomorphic encryption) name the general notion and its strongest form.

**Notation.** $\kappa$ is the security parameter. A function is given as a [Boolean circuit](/boolean-circuit/) or an arithmetic circuit $f$ with $\ell$ inputs, and $\mathcal{C}$ is a class of such circuits. $\mathcal{A}$ is an adversary. "Negligible" means smaller than every inverse polynomial in $\kappa$ for large enough $\kappa$.

## Definition

A **homomorphic encryption scheme** for a class $\mathcal{C}$ is a tuple of probabilistic polynomial time algorithms:

- $\mathrm{KeyGen}(1^\kappa)$ returns a public key $pk$, a secret key $sk$ and an evaluation key $ek$ (often part of $pk$).
- $\mathrm{Enc}(pk, m)$ returns a ciphertext $c$, and $\mathrm{Dec}(sk, c)$ returns a message.
- $\mathrm{Eval}(ek, f, c_1, \ldots, c_\ell)$ returns a ciphertext, for every $f \in \mathcal{C}$ with $\ell$ inputs.

**Correctness.** For every $f \in \mathcal{C}$ and all messages $m_1, \ldots, m_\ell$, with $c_i = \mathrm{Enc}(pk, m_i)$,

$$\Pr\bigl[\mathrm{Dec}(sk, \mathrm{Eval}(ek, f, c_1, \ldots, c_\ell)) = f(m_1, \ldots, m_\ell)\bigr] \ge 1 - \text{negligible}.$$

**Compactness.** There is a polynomial $s$ such that the output of Eval has at most $s(\kappa)$ binary digits for every $f \in \mathcal{C}$. Without this condition the definition is empty: Eval could output the pair $(f, c_1, \ldots, c_\ell)$ and let Dec do all the work.

**Security.** The scheme is [IND-CPA](/ind-cpa-security/) secure. Eval is public, so it gives the adversary nothing new.

The class $\mathcal{C}$ gives the usual names:

- **Partially homomorphic**: $\mathcal{C}$ is the circuits with one kind of gate, for example only additions or only multiplications, in any number.
- **Somewhat homomorphic**: $\mathcal{C}$ contains both additions and multiplications, but only for circuits of small degree or depth.
- **Leveled fully homomorphic**: $\mathrm{KeyGen}$ also takes a depth $L$, and $\mathcal{C}$ is all circuits of depth at most $L$. The output of Eval stays compact, but the keys may grow with $L$.
- **Fully homomorphic (FHE)**: $\mathcal{C}$ is all circuits, with one key pair.

**Circuit privacy.** Eval is circuit private if its output reveals nothing about $f$ beyond $f(m_1, \ldots, m_\ell)$: the output is statistically close to a distribution that depends only on $pk$ and the value $f(m_1, \ldots, m_\ell)$, for example a fresh encryption of it. Correctness and IND-CPA do not give this, because the noise or the randomness of an evaluated ciphertext can depend on $f$.

### Why IND-CPA is the ceiling

**Claim.** Suppose $\mathcal{C}$ contains a circuit $f$ with one input, and there are messages $m_0, m_1$ with $f(m_0) \ne m_0$, $f(m_1) \ne m_1$ and $f(m_0) \ne f(m_1)$. Then the scheme is not IND-CCA2. Examples are NOT on one bit, with $m_0 = 0$ and $m_1 = 1$, and $x \mapsto x + 1$ in an additive scheme.

*Proof.* The adversary submits $m_0$ and $m_1$ and gets the challenge $c^* = \mathrm{Enc}(pk, m_b)$. It computes $c' = \mathrm{Eval}(ek, f, c^*)$. Except with negligible probability, $c'$ decrypts to $f(m_b) \ne m_b$, while $c^*$ decrypts to $m_b$, so $c' \ne c^*$ and the decryption oracle accepts the query. The answer is $f(m_b)$, and since $f(m_0) \ne f(m_1)$ it tells $b$. The adversary wins with probability $1 - \text{negligible}$. $\square$

In the language of [non-malleability](/non-malleability/), homomorphism is malleability on purpose. Weaker goals remain possible: IND-CCA1 (no decryption queries after the challenge) is not ruled out by this argument, although many somewhat homomorphic schemes lose their secret key to such queries. Targeted malleability (Prabhakaran and Rosulek 2008) allows only the intended operations. For approximate schemes such as CKKS, Li and Micciancio (2021) showed that IND-CPA is not enough when decrypted results are shared, because the result carries the noise. Their notion IND-CPA$^D$ gives the adversary such results, and they used it to recover keys from implementations.

## Examples and non-examples

**Textbook RSA (multiplicative, not IND-CPA).** With $N = 3233$ and $e = 17$, $2^{17} \bmod N = 1752$, $3^{17} \bmod N = 1211$, and $1752 \cdot 1211 \bmod N = 824 = 6^{17} \bmod N$. The product of ciphertexts encrypts the product of messages. Textbook [RSA](/rsa-cryptosystem/) is deterministic, so this is a partially homomorphic function but not a secure scheme.

**ElGamal (multiplicative).** In [ElGamal](/elgamal-encryption/), $(g^{r_1}, m_1 h^{r_1}) \cdot (g^{r_2}, m_2 h^{r_2}) = (g^{r_1 + r_2}, m_1 m_2 h^{r_1 + r_2})$, componentwise. Exponential ElGamal encrypts $g^m$ instead of $m$ and becomes additive, but decryption then needs a discrete logarithm of $m$, so $m$ must be small. It is IND-CPA under [DDH](/decisional-diffie-hellman/).

**Goldwasser-Micali (XOR).** With $N = 77$ and the non-residue $y = 6$, $\mathrm{Enc}(1) = 6 \cdot 4^2 \bmod 77 = 19$ and $\mathrm{Enc}(0) = 5^2 \bmod 77 = 25$. The product $19 \cdot 25 \bmod 77 = 13$ is a non-residue modulo 7 ($13 \equiv 6$ and $6^3 \equiv -1 \pmod 7$), so it decrypts to $1 = 1 \oplus 0$. See [Goldwasser-Micali](/goldwasser-micali-cryptosystem/).

**Paillier (additive).** With $N = 77$, the ciphertexts 3840 of 42 and 3442 of 15 multiply to $1539 \bmod 5929$, which decrypts to 57. A ciphertext raised to $k$ encrypts $k$ times the message. See [Paillier](/paillier-cryptosystem/).

**Boneh-Goh-Nissim (somewhat).** Any number of additions and one multiplication, from a [bilinear pairing](/bilinear-pairing/) on a group of composite order. It evaluates quadratic formulas, for example 2-DNF formulas.

**Gentry, BGV, BFV, GSW, TFHE, CKKS (fully or leveled).** See the table below and [Gentry's FHE](/gentry-fully-homomorphic-encryption/).

**Non-example: the trivial scheme.** Let Eval output $(f, c_1, \ldots, c_\ell)$, and let Dec decrypt each $c_i$ and apply $f$. This is correct and IND-CPA for every $f$, but it is not compact, and it is not circuit private either, since it shows $f$.

**Non-examples: authenticated and CCA2 secure encryption.** RSA-OAEP, ECIES and AES-GCM are built so that a changed ciphertext is rejected. By the claim above, no IND-CCA2 scheme can be homomorphic for a non-trivial function.

### Schemes, operations and assumptions

| scheme | year | operations on plaintexts | type | assumption |
|---|---|---|---|---|
| RSA (textbook) | 1977 | multiplication modulo $N$ | partial, not IND-CPA | RSA (one-wayness only) |
| [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) | 1982 | XOR of bits | partial | [quadratic residuosity](/quadratic-residuosity-problem/) |
| [ElGamal](/elgamal-encryption/) | 1985 | multiplication in the group; addition in the exponent version | partial | [DDH](/decisional-diffie-hellman/) |
| [Naccache-Stern](/naccache-stern-cryptosystem/) | 1998 | addition modulo $\sigma$ | partial | higher residuosity |
| [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/) | 1998 | addition modulo $p$ | partial | $p$-subgroup |
| [Paillier](/paillier-cryptosystem/) | 1999 | addition modulo $N$, scalar multiplication | partial | [DCR](/decisional-composite-residuosity/) |
| Boneh-Goh-Nissim | 2005 | additions and one multiplication | somewhat | subgroup decision in a pairing group |
| Gentry | 2009 | any circuit (with bootstrapping) | fully | ideal lattices, sparse subset sum, circular security |
| DGHV | 2010 | any circuit (with bootstrapping) | fully | approximate GCD, sparse subset sum, circular security |
| BGV | 2012 | additions and multiplications modulo $t$, in SIMD slots | leveled, fully with bootstrapping | [ring LWE](/ring-learning-with-errors/) |
| BFV | 2012 | additions and multiplications modulo $t$, in SIMD slots | leveled, fully with bootstrapping | ring LWE |
| GSW | 2013 | additions and multiplications with slow noise growth | leveled, fully with bootstrapping | [LWE](/learning-with-errors/) |
| FHEW, TFHE | 2015, 2016 | Boolean gates, each followed by a fast bootstrapping | fully | LWE and ring LWE, circular security |
| CKKS | 2017 | approximate additions and multiplications of real or complex vectors | leveled, fully with bootstrapping | ring LWE |

## Related definitions

- **Generations of FHE.** The first generation is Gentry (STOC 2009 and his thesis) and DGHV (Eurocrypt 2010), with noise that grows fast and bootstrapping as the only way out. The second generation (Brakerski and Vaikuntanathan 2011, BGV 2012, Brakerski 2012 and Fan and Vercauteren 2012, called BFV) is based on LWE and ring LWE, controls noise by modulus switching or scale invariance, and packs many plaintexts in one ciphertext. The third generation (GSW 2013, then FHEW by Ducas and Micciancio 2015 and TFHE by Chillotti, Gama, Georgieva and Izabachène 2016) has slow noise growth and bootstraps one gate in milliseconds. CKKS (Cheon, Kim, Kim and Song 2017) treats noise as part of an approximate result and is often called the fourth generation.
- **Bootstrapping.** A scheme that can evaluate its own decryption circuit, plus one more gate, can refresh a noisy ciphertext by running Dec homomorphically on an encryption of the secret key. This turns a somewhat homomorphic scheme into a fully homomorphic one, under a circular security assumption. See [Gentry's FHE](/gentry-fully-homomorphic-encryption/).
- **Multi-key and threshold FHE.** Ciphertexts under the keys of several parties can be combined, and the result decrypted only by all of them together. This is one way to build [secure multiparty computation](/secure-multiparty-computation/) and [threshold cryptography](/threshold-cryptography/).
- **[Functional encryption](/functional-encryption/).** A key for $f$ reveals $f(m)$ in the clear. Homomorphic encryption reveals nothing to the evaluator, and the result stays encrypted.
- **[Non-malleability](/non-malleability/) and [IND-CCA security](/ind-cca-security/).** The opposite goal: no useful transformation of a ciphertext is possible.
- **Standards.** The HomomorphicEncryption.org Security Standard (2018) gives lattice parameters for BGV, BFV and CKKS at 128, 192 and 256 bits of security. ISO/IEC 18033-6:2019 specifies exponential ElGamal and Paillier. Work on an ISO/IEC standard for fully homomorphic encryption (ISO/IEC 28033) started later. Microsoft SEAL, OpenFHE, HElib, Lattigo and TFHE-rs are maintained libraries.

## References
