---
tag: QCQRX4
kind: definition
slug: strong-unforgeability
name: Strong unforgeability
aliases:
- SUF-CMA
- sEUF-CMA
- strong existential unforgeability
area: cryptography/signatures
level: advanced
summary: "SUF-CMA: no efficient adversary with a signing oracle can output a valid pair (message, signature) that the oracle did not return, even a new signature on a message it saw signed."
prereqs: [existential-unforgeability]
see_also: [signature-malleability, ecdsa, ed25519, lamport-signature, chosen-message-attack, bls-signature, rsa-pss, signature-forgery]
sources:
  - paper: "Jee Hea An, Yevgeniy Dodis and Tal Rabin, On the security of joint signature and encryption, EUROCRYPT 2002, LNCS 2332"
    locator: the notion of strong unforgeability for signatures, used to build CCA-secure signcryption
  - paper: "Ran Canetti, Shai Halevi and Jonathan Katz, Chosen-ciphertext security from identity-based encryption, EUROCRYPT 2004, LNCS 3027"
    locator: the transform from identity-based encryption to IND-CCA2 public-key encryption with a strong one-time signature
  - paper: "Danny Dolev, Cynthia Dwork and Moni Naor, Nonmalleable cryptography, SIAM Journal on Computing 30(2), 2000 (STOC 1991)"
    locator: non-malleable encryption that signs the ciphertext with a one-time signature whose verification key selects the public keys
  - paper: "Dan Boneh, Emily Shen and Brent Waters, Strongly unforgeable signatures based on computational Diffie-Hellman, PKC 2006, LNCS 3958, pages 229 to 240"
    locator: a transform with a chameleon hash from a class of partitioned EUF-CMA schemes to SUF-CMA schemes, applied to the Waters signature
  - paper: "Ron Steinfeld, Josef Pieprzyk and Huaxiong Wang, How to strengthen any weakly unforgeable signature into a strongly unforgeable signature, CT-RSA 2007, LNCS 4377"
    locator: a generic transform from any EUF-CMA scheme to an SUF-CMA scheme with a chameleon hash function
  - paper: "Jacqueline Brendel, Cas Cremers, Dennis Jackson and Mang Zhao, The provable security of Ed25519: theory and practice, IEEE Symposium on Security and Privacy 2021"
    locator: Ed25519 with the check S < L is SUF-CMA; the variants without the check are only EUF-CMA
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), January 2017
    locator: Section 5.1.7, verification decodes S as an integer and rejects the signature if S is not below L
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0146.mediawiki"
    title: Johnson Lau and Pieter Wuille, BIP 146, Dealing with signature encoding malleability, 2016
    locator: the LOW_S rule that removes the second ECDSA signature (r, n - s) in Bitcoin transactions
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, the definition of strongly secure signature schemes, and one-time signatures in the CCA construction from IBE
---

Strong unforgeability under adaptive chosen-message attack (SUF-CMA) is a security notion for a [signature scheme](/signature-scheme/) that is stronger than [existential unforgeability](/existential-unforgeability/) (EUF-CMA). The adversary wins if it outputs any valid pair of message and signature that the signing oracle did not give it, which includes a second signature on a message that was signed. The notion matters when signatures are used as identifiers or as tags inside other protocols: a changed signature on the same message must not count as a new valid object.

**Notation.** $\Pi = (\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ is a signature scheme and $\lambda$ the security parameter. $A$ is an adversary with running time $t$ that makes $q_s$ signing queries. $S = \{(m_1, \sigma_1), \ldots, (m_{q_s}, \sigma_{q_s})\}$ is the set of query and answer pairs, and $Q = \{m_1, \ldots, m_{q_s}\}$ the set of queried messages. For elliptic-curve schemes, $n$ or $L$ is the prime order of the base point.

## Definition

**The game $\mathrm{Exp}^{\mathrm{suf\text{-}cma}}_{\Pi, A}(\lambda)$.**

1. The challenger runs $(pk, sk) \leftarrow \mathrm{KeyGen}(1^\lambda)$ and sets $S \leftarrow \emptyset$.
2. The challenger runs $A(pk)$. For each message $m$ that $A$ submits, adaptively, the challenger computes $\sigma \leftarrow \mathrm{Sign}(sk, m)$, adds $(m, \sigma)$ to $S$ and returns $\sigma$.
3. $A$ outputs a pair $(m^*, \sigma^*)$.
4. The game outputs 1 if $\mathrm{Verify}(pk, m^*, \sigma^*) = 1$ and $(m^*, \sigma^*) \notin S$, and 0 otherwise.

$\mathrm{Adv}^{\mathrm{suf\text{-}cma}}_{\Pi}(A) = \Pr[\mathrm{Exp}^{\mathrm{suf\text{-}cma}}_{\Pi, A}(\lambda) = 1]$. $\Pi$ is SUF-CMA secure if this advantage is negligible for every probabilistic polynomial-time $A$, and $(t, q_s, \varepsilon)$-SUF-CMA secure if it is at most $\varepsilon$ for every $A$ with time $t$ and $q_s$ queries. The only change from the EUF-CMA game is step 4, where $m^* \notin Q$ becomes $(m^*, \sigma^*) \notin S$. Signatures are compared as strings, so the notion depends on the exact encoding that Verify accepts.

**Strong one-time signatures.** With the limit $q_s \le 1$ the notion is strong one-time unforgeability, the property that the encryption transforms below need.

**SUF-CMA implies EUF-CMA.** A winning pair in the EUF-CMA game has $m^* \notin Q$, so $(m^*, \sigma^*) \notin S$ and the same pair wins the SUF-CMA game. Hence $\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(A) \le \mathrm{Adv}^{\mathrm{suf\text{-}cma}}_{\Pi}(A)$ for every $A$.

**Unique signatures close the gap.** Suppose that for each $pk$ and $m$ at most one $\sigma$ verifies. Then a pair $(m^*, \sigma^*) \notin S$ that verifies has $m^* \notin Q$: if $m^* = m_i$, then $\sigma^* = \sigma_i$ by uniqueness, and the pair would be in $S$. So EUF-CMA and SUF-CMA are the same for such schemes. Deterministic signing alone is not enough, because the verifier may still accept other strings, as in the RSA example below.

**Why the notion matters.**

- **Identifiers that include signatures.** Bitcoin computed the transaction identifier as a hash of the whole transaction, signatures included. An ECDSA signature $(r, s)$ can be changed to $(r, n - s)$ by anyone, which gives a valid transaction with a new identifier. BIP 146 (2016) requires the low value of $s$, and the segregated witness change moved signatures out of the identifier. See [signature malleability](/signature-malleability/).
- **CCA-secure encryption from one-time signatures.** Canetti, Halevi and Katz (2004) encrypt with an identity-based scheme under the identity $vk$ of a fresh one-time key pair and sign the ciphertext with it. The proof of IND-CCA2 security fails if the adversary can take the challenge ciphertext, make a new signature on the same ciphertext under the same $vk$, and submit the result to the decryption oracle, which then returns the plaintext. So the one-time signature must be strongly unforgeable. The non-malleable encryption of Dolev, Dwork and Naor (1991) has the same need.
- **[Signcryption](/signcryption/) and signed protocol messages.** An, Dodis and Rabin (2002) used strong unforgeability to get CCA security for combinations of signatures and encryption, where the signature is part of the ciphertext.

**Generic transforms.** Boneh, Shen and Waters (PKC 2006) turn a class of EUF-CMA schemes whose signatures split into two parts into SUF-CMA schemes: the signer passes the message and the part of the signature that could be changed through a chameleon hash, and signs the result. They applied it to the Waters signature to get an SUF-CMA scheme under the computational Diffie-Hellman assumption in the standard model. Steinfeld, Pieprzyk and Wang (CT-RSA 2007) removed the condition and gave a transform with a chameleon hash for every EUF-CMA scheme.

## Examples and non-examples

- **RSA with a range check is unique.** For [RSA signatures](/rsa-signature/) with PKCS #1 v1.5 or [FDH](/rsa-fdh/) encoding, RSA is a permutation of $\mathbb{Z}_N$, so with the check $s < N$ each message has one valid signature, and EUF-CMA implies SUF-CMA. Without the check the scheme is not SUF-CMA. With the toy key $N = 3233$, $e = 17$, $d = 2753$, the signature of the encoded value $m = 65$ is $588$, and $588 + 3233 = 3821$ also satisfies $3821^{17} \bmod 3233 = 65$. A verifier that skips the range check accepts both.
- **ECDSA is not SUF-CMA.** Verification uses only the $x$-coordinate of a point $R$, and $R$ and $-R$ have the same $x$-coordinate. So if $(r, s)$ is valid, $(r, n - s)$ is also valid, and anyone can compute it from the public signature. A verifier that accepts only $s \le n/2$ removes this particular second signature. See [ECDSA](/ecdsa/) and [signature malleability](/signature-malleability/).
- **Ed25519 depends on one check.** A signature is $(R, S)$ with $S$ an integer modulo $L$. RFC 8032, Section 5.1.7, rejects $S \ge L$. Brendel, Cremers, Jackson and Zhao (2021) proved that [Ed25519](/ed25519/) with this check is SUF-CMA, under the discrete logarithm assumption in the random oracle model. Without the check, $(R, S + L)$ is a second valid signature, and some older implementations accepted it.
- **Lamport one-time signatures are strong one-time.** A [Lamport](/lamport-signature/) signature reveals one fixed preimage per binary digit of the hash, so each message has exactly one signature. Unforgeability for one message is therefore strong, which is why such schemes fit the CHK transform.
- **BLS signatures are unique.** A [BLS](/bls-signature/) signature is $H(m)^x$, one group element per message, so EUF-CMA in the ROM gives SUF-CMA if the verifier accepts only the canonical encoding of the element.
- **Randomized schemes need an argument.** [RSA-PSS](/rsa-pss/) has many signatures per message, one per salt. A second signature on a signed message needs a new salt, and therefore a new hash point, so the random oracle proof covers it as well.

## Related definitions

- **[Existential unforgeability](/existential-unforgeability/).** The weaker notion: only signatures on new messages count.
- **[Signature malleability](/signature-malleability/).** The practical name for the failure of SUF-CMA: someone without the key changes a valid signature into another valid one on the same message.
- **[Chosen-message attack](/chosen-message-attack/).** The attack model of both notions. A strong variant under a key-only attack is rarely studied, because the key-only adversary has no signature to change.
- **Unique signatures.** For each message at most one signature verifies. Such schemes are SUF-CMA as soon as they are EUF-CMA.
- **Strong one-time signatures.** SUF-CMA with one query. They are the building block of the CHK and DDN constructions.
- **Beyond unforgeability.** Properties such as exclusive ownership, where a signature must not verify under a second public key, are separate from both notions and are needed in some protocols.

## References
