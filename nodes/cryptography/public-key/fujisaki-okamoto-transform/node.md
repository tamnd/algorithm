---
tag: 4ZNST2
kind: technique
slug: fujisaki-okamoto-transform
name: Fujisaki-Okamoto transform
aliases:
- FO transform
area: cryptography/public-key
level: advanced
summary: Turn a weakly secure public-key scheme into an IND-CCA KEM in the random oracle model. Derive the randomness from the message, re-encrypt to check, and hash the message into the key.
prereqs: [ind-cca-security, random-oracle-model, key-encapsulation-mechanism]
see_also: [crystals-kyber, hybrid-encryption, elgamal-encryption, cramer-shoup-cryptosystem, naor-yung-paradigm, rsa-oaep, timing-attack, ecies]
sources:
  - paper: "Eiichiro Fujisaki and Tatsuaki Okamoto, How to enhance the security of public-key encryption at minimum cost, PKC 1999, LNCS 1560, pages 53 to 68"
    locator: the conversion from IND-CPA to IND-CCA2 by encrypting the message with a random string and hashing both into the randomness
  - paper: "Eiichiro Fujisaki and Tatsuaki Okamoto, Secure integration of asymmetric and symmetric encryption schemes, CRYPTO 1999, LNCS 1666, pages 537 to 554"
    locator: the hybrid conversion from a one-way public-key scheme and a one-time secure symmetric scheme
  - paper: "Dennis Hofheinz, Kathrin Hovelmanns and Eike Kiltz, A modular analysis of the Fujisaki-Okamoto transformation, TCC 2017, LNCS 10677, pages 341 to 371"
    locator: the transforms T and U with explicit and implicit rejection, correctness errors, and the bounds in the random oracle and quantum random oracle models
  - paper: "Haodong Jiang, Zhenfeng Zhang, Long Chen, Hong Wang and Zhi Ma, IND-CCA-secure key encapsulation mechanism in the quantum random oracle model, revisited, CRYPTO 2018, LNCS 10993, pages 96 to 125"
    locator: proofs of the implicit-rejection variants in the quantum random oracle model
  - url: "https://doi.org/10.6028/NIST.FIPS.203"
    title: NIST, FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, 2024
    locator: the internal encapsulation and decapsulation algorithms of ML-KEM, with re-encryption and implicit rejection
  - paper: "Alexander W. Dent, A designer's guide to KEMs, Cryptography and Coding 2003, LNCS 2898, pages 133 to 151"
    locator: KEM versions of the Fujisaki-Okamoto and REACT conversions
  - paper: "Tatsuaki Okamoto and David Pointcheval, REACT, rapid enhanced-security asymmetric cryptosystem transform, CT-RSA 2001, LNCS 2020, pages 159 to 175"
    locator: a related conversion from a one-way scheme under a plaintext-checking attack
  - paper: "Qian Guo, Thomas Johansson and Alexander Nilsson, A key-recovery timing attack on post-quantum primitives using the Fujisaki-Okamoto transformation and its application on FrodoKEM, CRYPTO 2020, LNCS 12171, pages 359 to 386"
    locator: key recovery from a non-constant-time comparison in the re-encryption check
---

The Fujisaki-Okamoto (FO) transform turns a public-key encryption scheme with weak security, such as one-wayness or [IND-CPA](/ind-cpa-security/), into an [IND-CCA](/ind-cca-security/) secure scheme or [KEM](/key-encapsulation-mechanism/), in the [random oracle model](/random-oracle-model/). It derives the encryption randomness from the message by a hash, so that the receiver can re-encrypt the decrypted message and reject any ciphertext that was not formed honestly, and it hashes the message into the final key. Fujisaki and Okamoto introduced it in 1999. In the modular form of Hofheinz, Hövelmanns and Kiltz (2017), with implicit rejection, it is the transform inside [ML-KEM](/crystals-kyber/) and most other post-quantum KEMs.

**Notation.** $\mathrm{PKE} = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ is the base scheme with message space $M$ and $\mathrm{Enc}(pk, m; r)$ its encryption with randomness $r$. $G$, $H$ and $H_{\mathrm{rej}}$ are hash functions modelled as independent random oracles. $\delta$ is the correctness error of the base scheme (the chance that an honest ciphertext decrypts wrongly), and the scheme is *$\gamma$-spread* if no single ciphertext has probability above $2^{-\gamma}$ for any message. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$ and makes $q_G$, $q_H$ and $q_D$ queries to $G$, $H$ and decapsulation, and $\mathrm{Adv}$ an advantage.

## In plain words

Many encryption schemes are safe against listeners but not against an attacker who can ask the receiver to decrypt changed ciphertexts. The FO transform fixes this with a hash function and one extra check.

The sender picks a random message and derives all other random choices of the encryption from it, by hashing. So the ciphertext is fully determined by the message. The receiver decrypts, then encrypts the result again in the same way and checks that it gets exactly the ciphertext it received. A changed or made-up ciphertext almost never passes. The shared key is a hash of the message, so only someone who knows the message knows the key. If the check fails, the receiver returns a random-looking key computed from a secret, so the attacker cannot even tell that the check failed.

## When it applies

- The base scheme is one-way under chosen-plaintext attack (OW-CPA), or IND-CPA, and every message has many possible ciphertexts ($\gamma$ large).
- The correctness error $\delta$ is negligible. Lattice and code-based schemes have $\delta > 0$, and the bounds include a term for it.
- The message space $M$ is large, at least $2^\lambda$ elements, so that nobody can guess the message.
- You accept a proof in the random oracle model, or in the quantum random oracle model for post-quantum schemes. For proofs in the standard model, see [Cramer-Shoup](/cramer-shoup-cryptosystem/) and the [Naor-Yung paradigm](/naor-yung-paradigm/).
- You want a KEM; a long message is then sent by [hybrid encryption](/hybrid-encryption/).

## The template

This is $\mathrm{FO}^{\not\perp}$ (implicit rejection) of Hofheinz, Hövelmanns and Kiltz: the derandomizing transform $T$ followed by the KEM transform $U^{\not\perp}$. Key generation runs $(pk, sk) \leftarrow \mathrm{Gen}$ and draws a secret $s$ uniformly from $M$ (or from $\{0,1\}^{256}$); the private key is $(sk, s)$, and $pk$ is kept with it for the check.

```pseudo id=main
FO-ENCAPS(pk)
L1  m ← uniform in M
L2  c ← Enc(pk, m; G(m))                  ▷ T: the randomness is G(m)
L3  return (c, K = H(m, c))

FO-DECAPS((sk, s, pk), c)
L4  m' ← Dec(sk, c)
L5  if m' ≠ ⊥ and Enc(pk, m'; G(m')) = c then
L6      return H(m', c)
L7  return H_rej(s, c)                    ▷ implicit rejection: a pseudorandom key
```

Line L2 makes encryption deterministic, which lets line L5 check the ciphertext by re-encryption. Line L7 replaces an error message by a key that looks random to anyone without $s$; the decapsulation never fails visibly.

### Why it works

**Theorem (Hofheinz, Hövelmanns and Kiltz, 2017, informal).** In the random oracle model, if the base scheme is OW-CPA secure, $\gamma$-spread and $\delta$-correct, then $\mathrm{FO}^{\not\perp}[\mathrm{PKE}, G, H]$ is an IND-CCA secure KEM. For every $\mathcal{A}$ there is an OW-CPA adversary $\mathcal{B}$ with about the same running time and

$$\mathrm{Adv}^{\mathrm{ind\text{-}cca}}_{\mathrm{KEM}}(\mathcal{A}) \le O(q_G + q_H) \cdot \mathrm{Adv}^{\mathrm{ow\text{-}cpa}}(\mathcal{B}) + O(q_G \, \delta) + O(q_D \, 2^{-\gamma}) + O\!\left(\frac{q_H}{|M|}\right).$$

From an IND-CPA base scheme the factor $q_G + q_H$ on the main term disappears and the bound is tight up to the additive terms. From OW-CPA the reduction is not tight. The paper gives exact constants for each variant.

*Proof idea.* In the random oracle model the reduction sees every query to $G$ and $H$. (1) Decapsulation can be simulated without $sk$: for a query $c$, look for an earlier query $G(m)$ with $\mathrm{Enc}(pk, m; G(m)) = c$; if there is one, answer $H(m, c)$, and otherwise the honest answer is the rejection key or a value of $H$ never asked, both random to $\mathcal{A}$. A ciphertext that passes line L5 without such a query would need $\mathcal{A}$ to hit the output of $G$ by chance, which the $\gamma$-spread property bounds, and $\delta$ bounds the chance that the check behaves differently from the simulation. (2) The challenge key $H(m^*, c^*)$ is uniform unless $\mathcal{A}$ queries $G$ or $H$ at $m^*$. In that case the reduction finds $m^*$ among the queries, which breaks one-wayness; guessing which query it is costs the factor $q_G + q_H$. $\square$

**Quantum random oracles.** A quantum adversary can query $G$ and $H$ in superposition, and the argument of step (1), which reads the adversary's queries, does not carry over. Hofheinz, Hövelmanns and Kiltz gave proofs for variants in the quantum random oracle model, and Jiang, Zhang, Chen, Wang and Ma (2018) proved the implicit-rejection variants secure there, with a loss of about the square root of the advantage of the base scheme. Later work has improved these bounds. The quantum proofs are the reason why post-quantum KEMs prefer implicit rejection.

## Classic examples

- **FO for public-key encryption (PKC 1999).** Encrypt $m \| \sigma$ for a random $\sigma$ with randomness $H(m \| \sigma)$, and re-encrypt on decryption. It turns IND-CPA into IND-CCA2.
- **FO hybrid (CRYPTO 1999).** Encrypt a random $\sigma$ with the one-way scheme, with randomness $H(\sigma, c)$, where $c$ is the symmetric encryption of the message under the key $G(\sigma)$. This is the origin of the KEM form.
- **[ML-KEM](/crystals-kyber/) (FIPS 203).** The base scheme K-PKE is IND-CPA under module learning with errors. ML-KEM derives $(K, r) = G(m \| H(ek))$, encrypts $m$ with randomness $r$, re-encrypts on decapsulation, and returns $J(z \| c)$ for a secret $z$ when the check fails. This is $\mathrm{FO}^{\not\perp}$ with the key derived from $m$ and a hash of the public key.
- **Other post-quantum KEMs.** [FrodoKEM](/frodokem/), [HQC](/hqc/), [BIKE](/bike/) and [Saber](/saber/) use FO variants with re-encryption.
- **FO over ElGamal.** The Python code applies $\mathrm{FO}^{\not\perp}$ to [ElGamal](/elgamal-encryption/), which is OW-CPA under CDH and IND-CPA under DDH, with $\delta = 0$.

## Variations

- **Explicit rejection ($U^\perp$).** Line L7 returns $\perp$. Hofheinz, Hövelmanns and Kiltz prove this secure too in the random oracle model, but the implicit form has simpler proofs in the quantum random oracle model and gives a side channel less to protect.
- **Key from the message only ($U_m^{\not\perp}$, $U_m^\perp$).** $K = H(m)$ instead of $H(m, c)$. This is secure after $T$, because $T$ makes the ciphertext a function of $m$, but it is insecure without $T$ (Exercise 3).
- **Hashing the public key.** Including a hash of $pk$ in $G$, as ML-KEM does, binds the key to the recipient and helps against attacks on many keys at once.
- **REACT and GEM.** Okamoto and Pointcheval (2001) gave related conversions that need only one-wayness under a plaintext-checking attack and avoid re-encryption by hashing the ciphertext into a tag.
- **[RSA-OAEP](/rsa-oaep/)** is a different random oracle transform, specific to trapdoor permutations, with no re-encryption step.

## Pitfalls

- **Skipping the re-encryption check.** Without line L5 the base scheme's malleability comes back. For ElGamal, a rerandomized ciphertext decrypts to the same $m$; with $K = H(m)$ and no check, one decapsulation query returns the challenge key. The test file runs this attack.
- **A timing leak in the check.** The comparison of line L5 and the choice between lines L6 and L7 must run in constant time. Guo, Johansson and Nilsson (2020) recovered FrodoKEM keys from a comparison that stopped at the first differing byte. The Python code here is not constant time.
- **A small message space.** After $T$, encryption is deterministic, so anyone can test a guess $m$ by re-encrypting. $M$ must have at least $2^\lambda$ elements, and $m$ must come from a good random generator, since it is the only secret.
- **Decryption failures.** If $\delta$ is not negligible, an attacker can search for ciphertexts that fail to decrypt and learn the private key from which ones fail. Choose parameters with $\delta$ far below $2^{-\lambda}$, as ML-KEM does.
- **Hashes without domain separation.** $G$, $H$ and $H_{\mathrm{rej}}$ must behave as independent random oracles. Use distinct prefixes or distinct functions, as ML-KEM does with $G$, $H$ and $J$, and hash fixed-length encodings.
- **A rejection key that anyone can compute.** If $s$ is public or fixed, line L7 is explicit rejection in disguise, and if $s$ is reused across keys the rejection keys collide. Draw $s$ fresh with each key pair and keep it secret.

## Exercises

1. Show that $T[\mathrm{ElGamal}, G]$, ElGamal with randomness $G(m)$, is not IND-CPA secure, by giving an adversary with advantage 1. Explain why it is still one-way if CDH is hard and $G$ is a random oracle.
2. Suppose the rejection secret $s$ is public. Give an algorithm that, from $pk$, $s$, $c$ and the output of decapsulation, decides whether the check of line L5 failed, and explain why the scheme is then exactly the explicit-rejection variant $U^\perp$.
3. Let the KEM use randomized ElGamal without $T$, decapsulate with no re-encryption check, and set $K = H(m)$. Give an IND-CCA adversary with advantage close to 1 that makes one decapsulation query. Then show that the same attack fails against $\mathrm{FO}^{\not\perp}$.

## References
