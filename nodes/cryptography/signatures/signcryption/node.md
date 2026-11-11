---
tag: G5XJ7C
kind: algorithm
slug: signcryption
name: Signcryption
aliases:
- sign-and-encrypt in one step
- Zheng signcryption
area: cryptography/signatures
level: research
summary: Combined signing and encryption that costs less than sign-then-encrypt.
model: word-ram
complexity:
  vars: {k: the length of the modulus p in machine words, n: the length of the message in machine words}
  time: {worst: Θ(k^3 + n), average: Θ(k^3 + n), best: Θ(k^3 + n)}
  space: {extra: Θ(k + n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1997
  people: [Yuliang Zheng]
  note: Zheng introduced signcryption at Crypto 1997, based on shortened forms of DSA. An, Dodis and Rabin gave formal models with outsider and insider security at Eurocrypt 2002.
prereqs: [digital-signature, public-key-encryption, diffie-hellman]
see_also: [hybrid-encryption, authenticated-encryption, message-authentication-code, hmac, schnorr-signature, elgamal-encryption, designated-verifier-signature, stream-cipher]
sources:
  - paper: doi:10.1007/BFb0052234
    title: "Yuliang Zheng, Digital signcryption or how to achieve cost(signature & encryption) << cost(signature) + cost(encryption), Crypto 1997, LNCS 1294, pages 165 to 179"
    locator: the shortened signatures SDSS1 and SDSS2, the signcryption and unsigncryption algorithms, and the cost comparison with signature-then-encryption
  - paper: doi:10.1007/3-540-46035-7_6
    title: "Jee Hea An, Yevgeniy Dodis and Tal Rabin, On the security of joint signature and encryption, Eurocrypt 2002, LNCS 2332, pages 83 to 107"
    locator: outsider and insider security, the two-user and multi-user settings, and the generic compositions encrypt-then-sign, sign-then-encrypt and commit-then-encrypt-and-sign
  - paper: doi:10.1007/s00145-007-0211-0
    title: "Joonsang Baek, Ron Steinfeld and Yuliang Zheng, Formal proofs for the security of signcryption, Journal of Cryptology 20(2), 2007, pages 203 to 235"
    locator: proofs of confidentiality and unforgeability of Zheng's scheme in the random oracle model under the gap Diffie-Hellman assumption
---

Signcryption does the work of a digital signature and of public-key encryption in one step: the sender's output is a ciphertext that only the recipient can open, and the opening shows that the sender wrote the message. Zheng introduced it at Crypto 1997 with the claim in his title, that the cost of both together can be much less than the cost of a signature plus the cost of an encryption. In his scheme the sender makes one exponentiation $K = y_b^x$, uses $K$ as the key for a symmetric cipher and a keyed hash, and then signs with the same $x$ in a shortened DSA form; the recipient recovers $K$ from the signature itself. An, Dodis and Rabin (Eurocrypt 2002) gave the security models and studied how to combine an ordinary signature and encryption correctly.

## In plain words

Alice wants to send Bob a private letter that Bob can prove Alice wrote. The usual way is to sign the letter, then lock it in a box that only Bob can open, which costs two pieces of public-key work.

In signcryption Alice picks one random number. From it and Bob's public key she makes a secret that only Bob can rebuild, and uses it to lock the letter and stamp it. Then she writes a short number that ties the random number to her own secret key. Bob combines this number with his secret key and Alice's public key, gets the same secret back, opens the letter and checks the stamp. Only Alice could have written a number that gives the right secret.

## The problem

Given a sender with key pair $(x_a, y_a)$, a recipient with $(x_b, y_b)$, and a message $m$, produce a signcryptext such that:

- **correctness:** the recipient, with $x_b$ and $y_a$, recovers $m$;
- **confidentiality:** nobody else learns anything about $m$ (in the strong form, even under chosen-ciphertext attack);
- **unforgeability:** nobody else can make a signcryptext that the recipient accepts as coming from the sender;
- **efficiency:** the cost is less than signing and encrypting separately.

**Outsider security** protects the sender and recipient against third parties only. **Insider security** also protects each party against the other: confidentiality holds even if the attacker knows the sender's secret key, and unforgeability holds even if it knows the recipient's secret key. Insider unforgeability is what gives non-repudiation.

## The algorithm

$H$ splits a group element into keys $(k_1, k_2)$, $E$ is a symmetric cipher and $KH$ a keyed hash into $\mathbb{Z}_q$. The two variants come from the shortened signatures SDSS1 and SDSS2.

```pseudo id=main
SIGNCRYPT(x_a, y_b, m)                                   ▷ run by Alice
L1  x ← random in Z_q*
L2  (k_1, k_2) ← H(y_b^x)
L3  c ← E_{k_1}(m)
L4  r ← KH_{k_2}(m)
L5  s ← x / (r + x_a) mod q  (SDSS1)  or  x / (1 + x_a · r) mod q  (SDSS2); return (c, r, s)

UNSIGNCRYPT(y_a, x_b, (c, r, s))                         ▷ run by Bob
L6  K ← (y_a · g^r)^{s · x_b}  (SDSS1)  or  (g · y_a^r)^{s · x_b}  (SDSS2)
L7  (k_1, k_2) ← H(K); m ← D_{k_1}(c)
L8  accept m if KH_{k_2}(m) = r, else reject
```

If the divisor at line L5 is $0$, Alice starts again with a new $x$. Without encryption, $(r, s)$ with $g^x$ in place of $y_b^x$ is a shortened digital signature: the verifier recomputes $g^x = (y_a g^r)^s$. In signcryption only Bob can compute $y_b^x$ from $(y_a g^r)^s = g^x$, because that needs $x_b$.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. Alice has $x_a = 5$, $y_a = 1024$; Bob has $x_b = 17$, $y_b = 1458$. Alice signcrypts "hi" with $x = 77$, with SHA-512 for $H$, HMAC-SHA-256 reduced modulo $q$ for $KH$, and a SHA-256 key stream for $E$.

| line | computation | result |
|---|---|---|
| L2 | $K = 1458^{77}$ | $932$ |
| L3 | $c = $ "hi" XOR key stream | bytes e9 05 |
| L4 | $r = KH_{k_2}(\text{hi}) \bmod 1019$ | $646$ |
| L5 (SDSS1) | $s = 77 / (646 + 5) = 77 / 651 \bmod 1019$ | $285$ |
| L6 (SDSS1) | $(1024 \cdot 4^{646})^{285 \cdot 17} = 200^{769}$ | $932$ |
| L5 (SDSS2) | $s = 77 / (1 + 5 \cdot 646) = 77 / 174 \bmod 1019$ | $100$ |
| L6 (SDSS2) | $(4 \cdot 1024^{646})^{100 \cdot 17} = 1643^{681}$ | $932$ |

In both variants Bob gets $K = 932$, decrypts "hi" and recomputes $r = 646$.

## Correctness

In SDSS1, $y_a g^r = g^{x_a + r}$, so $(y_a g^r)^{s x_b} = g^{(x_a + r) \cdot x/(x_a + r) \cdot x_b} = g^{x x_b} = y_b^x$. In SDSS2, $g\, y_a^r = g^{1 + x_a r}$ and the same cancellation happens. So Bob derives the same keys, decrypts $m$ and recomputes the tag. A changed $c$, $r$ or $s$ leads to a different message or key, and the tag check fails except with the probability of guessing a tag. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Alice makes one exponentiation and Bob two (about one and a quarter with simultaneous exponentiation), plus hashing and symmetric encryption of the $n$-word message, so each side costs $\Theta(k^3 + n)$ with schoolbook arithmetic modulo $p$ of $k$ words. Signing with Schnorr and then encrypting with ElGamal-based hybrid encryption costs the sender three exponentiations and the recipient three. The overhead of a signcryptext is the tag $r$ and $s \in \mathbb{Z}_q$, about two elements of $\mathbb{Z}_q$; sign-then-encrypt sends a signature of the same size and in addition an ephemeral public key. Zheng's paper tabulates the savings for typical parameters.

## Properties

- **One random exponent.** The same $x$ serves the key agreement and the signature.
- **Key recovery from the signature.** Bob does not receive $g^x$ or $y_b^x$; he computes $y_b^x$ from $r$, $s$ and his secret key.
- **Not publicly verifiable in the original form.** Checking $r$ needs $K$, so a judge cannot verify without Bob's secret key or a further protocol. This makes the basic scheme deniable towards third parties, like a [designated verifier signature](/designated-verifier-signature/).
- **Multi-user binding.** The proved-secure form puts both parties' identities or public keys into the hash, so that a signcryptext for Bob cannot be re-addressed.

## Variants and improvements

- **Generic compositions** (An, Dodis and Rabin 2002). Encrypt-then-sign and sign-then-encrypt are secure in the right models if each step binds the other party's identity; commit-then-encrypt-and-sign lets the signature and the encryption run in parallel.
- **Publicly verifiable variants.** Bao and Deng (PKC 1998) changed Zheng's scheme so that anyone can check the signature part; this costs more and gives up the deniability.
- **Identity-based signcryption.** Malone-Lee (2002) and Boyen (Crypto 2003), among others, built schemes with keys derived from identities using pairings.
- **Signcryption key encapsulation.** Dent and others split signcryption into a signcryption KEM and a data encapsulation, as in [hybrid encryption](/hybrid-encryption/) (a public-key step that carries a key for a symmetric cipher).
- **Standard.** ISO/IEC 29150 (2011) standardizes several signcryption schemes, including a version of Zheng's.

## When to use it

Use signcryption, or a careful generic composition, when a message must be both confidential and attributable to its sender, and when bandwidth or the sender's computation is short: constrained devices, store-and-forward messaging, and key transport. If the recipient needs only authentication and not proof for third parties, an authenticated key exchange followed by [authenticated encryption](/authenticated-encryption/) (encryption with a built-in integrity tag) is the common practical choice. If third parties must verify, use a publicly verifiable variant or sign and encrypt separately, binding the identities.

## Pitfalls

- **Naive sign-then-encrypt.** If Alice signs $m$ and encrypts it to Bob, Bob can decrypt and re-encrypt the signed message to Carol, who then believes Alice wrote it to her (surreptitious forwarding, described by Davis at USENIX 2001). Put the recipient's identity inside the signed data.
- **Naive encrypt-then-sign.** If Alice encrypts and then signs the ciphertext, an attacker can strip her signature and sign the ciphertext itself, claiming the message as its own. Put the sender's identity inside the encrypted data.
- **Identities in the hash.** Zheng's original hash did not bind the public keys; the proofs of Baek, Steinfeld and Zheng use a form that does.
- **Short tags.** $r$ is used as an exponent modulo $q$ and as the integrity tag; with a toy $q$ it is guessable, and with real parameters it should be as long as $q$.
- **Reused or biased $x$.** As in DSA and Schnorr, reuse of $x$ for two messages reveals $x_a$, and bias in $x$ leaks it through lattice attacks.
- **Non-repudiation.** Bob alone can check the original scheme, so it does not give evidence to a judge without extra steps.

## Implementations

The Python code is for study only: it is not constant time, its group ($p = 2039$, $q = 1019$) has no security, and its stream cipher (SHA-256 of the key and a counter) is a teaching device. It implements Zheng's SDSS1 and SDSS2 signcryption with HMAC-SHA-256 as the keyed hash; it does not bind identities into the hash. There are no standard test vectors for Zheng's scheme in this form. The tests check the round trip for both variants, rejection of a changed ciphertext, tag or $s$, rejection with Carol's key in place of Bob's or Alice's, and rejection of random signcryptexts.

## History

Zheng introduced signcryption at Crypto 1997, with schemes built from shortened forms of DSA. Proofs came later: An, Dodis and Rabin defined the models in 2002, and Baek, Steinfeld and Zheng proved Zheng's scheme secure in 2002 (journal version 2007). Identity-based and certificateless variants followed, and ISO/IEC 29150 standardized signcryption in 2011.

## References
