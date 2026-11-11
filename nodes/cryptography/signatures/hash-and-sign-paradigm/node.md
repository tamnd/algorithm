---
tag: R0VXSE
kind: technique
slug: hash-and-sign-paradigm
name: Hash-and-sign paradigm
aliases:
- hash-then-sign
- hash and sign
- randomized hashing
area: cryptography/signatures
level: core
summary: Sign a short hash of the message with a scheme for fixed-length inputs. Secure if the hash is collision resistant; randomized hashing needs only target collision resistance.
prereqs: [signature-scheme, collision-resistance]
see_also: [rsa-fdh, rsa-pss, dsa, ecdsa, birthday-attack, chosen-prefix-collision, random-oracle-model, schnorr-signature]
sources:
  - paper: "Ivan Damgård, Collision free hash functions and public key signature schemes, EUROCRYPT 1987, LNCS 304, pages 203 to 216"
    locator: signing the hash of the message, and the reduction to collision freeness of the hash and the security of the signature on short inputs
  - paper: "Gideon Yuval, How to swindle Rabin, Cryptologia 3(3), pages 187 to 190, 1979"
    locator: the birthday attack on hashed signatures with many variants of a fair and an unfair message
  - paper: "Mihir Bellare and Phillip Rogaway, Random oracles are practical, a paradigm for designing efficient protocols, ACM CCS 1993, pages 62 to 73"
    locator: the full-domain hash signature, a hash onto the whole domain of a trapdoor permutation, proved in the random oracle model
  - paper: "Moni Naor and Moti Yung, Universal one-way hash functions and their cryptographic applications, STOC 1989, pages 33 to 43"
    locator: universal one-way (target collision resistant) hash families, and signatures built from them and one-way permutations
  - paper: "Mihir Bellare and Phillip Rogaway, Collision-resistant hashing, towards making UOWHFs practical, CRYPTO 1997, LNCS 1294, pages 470 to 484"
    locator: the notion of target collision resistance (TCR) and hash-and-sign with a fresh key for each message
  - paper: "Shai Halevi and Hugo Krawczyk, Strengthening digital signatures via randomized hashing, CRYPTO 2006, LNCS 4117, pages 41 to 59"
    locator: the RMX transform, enhanced target collision resistance (eTCR), and signatures that stay secure if the hash loses collision resistance
  - url: "https://csrc.nist.gov/pubs/sp/800/106/final"
    title: Quynh Dang, NIST SP 800-106, Randomized Hashing for Digital Signatures, February 2009
    locator: the standard form of the Halevi-Krawczyk randomized hashing
  - paper: "Marc Stevens, Arjen Lenstra and Benne de Weger, Chosen-prefix collisions for MD5 and colliding X.509 certificates for different identities, EUROCRYPT 2007, LNCS 4515, pages 1 to 22"
    locator: two X.509 certificates with different names and one MD5 signature
  - paper: "Marc Stevens, Alexander Sotirov, Jacob Appelbaum, Arjen Lenstra, David Molnar, Dag Arne Osvik and Benne de Weger, Short chosen-prefix collisions for MD5 and the creation of a rogue CA certificate, CRYPTO 2009, LNCS 5677, pages 55 to 69"
    locator: a rogue CA certificate whose MD5 hash equals that of a certificate signed by a commercial CA
  - paper: "Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov, The first collision for full SHA-1, CRYPTO 2017, LNCS 10401, pages 570 to 596"
    locator: two PDF files with the same SHA-1 hash, an identical-prefix collision
  - paper: "Gaëtan Leurent and Thomas Peyrin, SHA-1 is a Shambles, first chosen-prefix collision on SHA-1 and application to the PGP web of trust, USENIX Security 2020"
    locator: a chosen-prefix collision for SHA-1 and two PGP keys with the same SHA-1 certification signature
  - paper: "Gregory Neven, Nigel P. Smart and Bogdan Warinschi, Hash function requirements for Schnorr signatures, Journal of Mathematical Cryptology 3(1), pages 69 to 87, 2009"
    locator: Schnorr signatures need only weak preimage-type properties of the hash, not collision resistance
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, the hash-and-sign paradigm and its theorem with a collision-resistant hash
---

The hash-and-sign paradigm builds a signature scheme for messages of any length from a scheme that signs only short, fixed-length values: hash the message, then sign the hash. Damgård (1987) proved that the result is secure if the short scheme is unforgeable and the hash is collision resistant. Almost every deployed signature uses it, from [RSA signatures](/rsa-signature/) and [DSA](/dsa/) to the message hash of SPHINCS+. Its weak point is the hash: a collision of the hash is a forgery, which is how MD5 and SHA-1 signatures on certificates were broken.

**Notation.** $\Pi' = (\mathrm{KeyGen}', \mathrm{Sign}', \mathrm{Verify}')$ signs messages in a set $\{0,1\}^\ell$ or $\mathbb{Z}_N$. $H$ maps messages of any length to that set; a keyed family is written $H_k$. $\Pi$ is the hash-and-sign scheme. $A$ is an adversary with running time $t$ and $q_s$ signing queries.

## In plain words

A signature algorithm based on a hard math problem can only sign numbers of a fixed size, and it is slow. Real messages are long. So the signer first runs the message through a hash function, which turns any message into a short fingerprint, and signs only the fingerprint. The checker computes the fingerprint again and checks the signature on it.

This is safe as long as nobody can find two different messages with the same fingerprint. If someone can, they ask for a signature on the harmless message and attach it to the harmful one. A random value mixed into the hash makes the job of the attacker much harder, because the attacker no longer knows in advance what will be hashed.

## When it applies

- The base scheme $\Pi'$ signs a short value and is [EUF-CMA](/existential-unforgeability/) on its domain, and a hash $H$ into that domain is [collision resistant](/collision-resistance/). Then $\Pi$ is EUF-CMA for messages of any length (the theorem below).
- The base primitive is not a secure signature at all on its own, such as the RSA function, which is multiplicative. Then the hash has a second job: it must break the algebra. This needs more than collision resistance, usually a hash onto the whole domain modelled as a [random oracle](/random-oracle-model/), as in [RSA-FDH](/rsa-fdh/) and [RSA-PSS](/rsa-pss/).
- The hash may lose collision resistance during the life of the key. Then a random value chosen by the signer for each message, as in randomized hashing, reduces the need to target collision resistance.

## The template

```pseudo id=main
KEYGEN(1^λ)
L1  (pk, sk) ← KeyGen'(1^λ);  if H is keyed, choose its key k and add it to pk

SIGN(sk, M)
L2  r ← ⟨a fresh random value, or nothing⟩
L3  h ← ⟨the hash of the message: H(M), H_k(M), H(r ∥ M) or a randomized RMX(r, M)⟩
L4  σ' ← Sign'(sk, ⟨an encoding of h into the domain of Sign', for example a padding or a full-domain expansion⟩)
L5  return (r, σ')

VERIFY(pk, M, (r, σ'))
L6  h ← the same hash as in line L3
L7  return Verify'(pk, the same encoding of h, σ')
```

**Theorem (Damgård 1987; Katz and Lindell, Chapter 13).** Let $r$ be empty and $h = H_k(M)$ with the key $k$ in $pk$. For every adversary $A$ against $\Pi$ there are adversaries $B$ against $\Pi'$ and $C$ against the collision resistance of $H$, with about the same running time, such that

$$\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(A) \le \mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi'}(B) + \mathrm{Adv}^{\mathrm{cr}}_{H}(C).$$

*Proof.* Let $M_1, \ldots, M_{q_s}$ be the queries of $A$ and $(M^*, \sigma^*)$ its output, with $M^* \notin \{M_i\}$ and a valid $\sigma^*$. Either $H_k(M^*) = H_k(M_i)$ for some $i$, or $H_k(M^*)$ differs from every $H_k(M_i)$. In the first case $(M^*, M_i)$ is a collision, since $M^* \ne M_i$; $C$ gets $k$, runs $A$ with its own key pair of $\Pi'$, answers every query itself, and outputs this pair. In the second case $(H_k(M^*), \sigma^*)$ is a valid pair for $\Pi'$ on a value that $B$ never asked its own signing oracle for; $B$ gets the public key of $\Pi'$, chooses $k$, answers each query $M_i$ by asking its oracle for $H_k(M_i)$, and outputs this pair. The two events cover every success of $A$, which gives the bound. $\blacksquare$

**Collision resistance is needed.** If an adversary can find $M \ne M'$ with $H(M) = H(M')$, it asks for a signature on $M$, and the same $\sigma'$ verifies on $M'$, a message it never submitted. Yuval (1979) turned this into a practical attack: write $2^{n/2}$ variants of a harmless text and of a harmful one, for example with one or two spaces after some words, and find a pair across the two sets with the same hash of $n$ binary digits; by the [birthday bound](/birthday-attack/) about $2^{n/2}$ hashes per set suffice.

**A worked collision forgery.** The code of this page signs $H(M)$ with textbook RSA on a toy key $N = 104729 \cdot 1299709$ and with $H$ the first 24 binary digits of SHA-256. It writes $2^{14}$ variants of "I agree to pay Bob the sum of 100 dollars for the old bicycle he sold me on Monday this week" and $2^{14}$ variants of the same text with 9000 dollars, by one or two spaces after each of the first 14 words. About $2^{14} \cdot 2^{14} / 2^{24} = 16$ colliding pairs are expected; the run finds 20, and the first one has the hash value $13065352$ for both texts. The signer signs the harmless variant, the signature is $36852878657$, and it verifies on the harmful variant. With 32 binary digits of hash the same pair no longer collides. The code is for study only, is not constant time, and runs only on a toy hash and a toy key against a local signer.

## Classic examples

- **[RSA signatures](/rsa-signature/) with PKCS #1 v1.5.** $h$ is the hash, wrapped in a DigestInfo structure and a fixed padding (line L4). A proof of its security came only in 2018, from Jager, Kakvi and May, in the random oracle model.
- **[RSA-FDH](/rsa-fdh/) and [RSA-PSS](/rsa-pss/).** The encoding of line L4 spreads $h$ over all of $\mathbb{Z}_N$. PSS also uses a random salt in line L2, which gives a tight proof in the random oracle model.
- **[DSA](/dsa/) and [ECDSA](/ecdsa/).** $h$ is the leftmost $N$ binary digits of the hash, used as an integer modulo $q$. A collision of $H$, or even of $h \bmod q$, gives a forgery.
- **[Lamport](/lamport-signature/) and other one-time signatures, and [SPHINCS+](/sphincs-plus/).** The base scheme signs a fixed number of binary digits, so the message is hashed first. SPHINCS+ hashes a random value with the message, a form of randomized hashing, so that its security does not rest on plain collision resistance.
- **[Rabin signatures](/rabin-signature/).** The hash value is the number whose square root is the signature. Rabin's original scheme already appended a random string to the message before hashing.

## Variations

- **Domain extension.** The hash itself is built from a function with a short input, for example by the Merkle-Damgård construction, which keeps collision resistance. Hash-and-sign is then a second domain extension, from the input length of $\Pi'$ to any length.
- **Full-domain hash.** Hash onto the whole domain of a trapdoor permutation and invert the permutation there, as in RSA-FDH (Bellare and Rogaway, 1993). Collision resistance alone is not enough here; the proof models $H$ as a random oracle.
- **Target collision resistance (TCR).** Naor and Yung (1989) and Bellare and Rogaway (1997): for each message the signer picks a fresh key $r$, computes $h = H_r(M)$ and signs $(r, h)$. A forger must now find $M'$ with $H_r(M') = H_r(M)$ for a key $r$ chosen after $M$ was fixed, which is a second-preimage task, much harder than finding a collision. The key $r$ must be signed too.
- **Randomized hashing (Halevi and Krawczyk, 2006).** In its basic form, the RMX transform mixes a random value $r$ into each block of the message before an unchanged hash function, $M \mapsto (r, M_1 \oplus r, \ldots, M_L \oplus r)$, and the signer signs the hash of the result. The required property, enhanced TCR, lets $r$ be sent without being signed, so the signature format does not change. NIST published the method as SP 800-106 (2009).
- **Hash inside the proof.** Fiat-Shamir signatures such as [Schnorr signatures](/schnorr-signature/) and Ed25519 hash a fresh commitment together with the message, so the hash is part of the proof system. Neven, Smart and Warinschi (2009) showed that Schnorr signatures need only properties close to second-preimage resistance, not collision resistance. Pre-hashed variants such as Ed25519ph and HashML-DSA put a plain hash-and-sign step in front of them and so need collision resistance again.

## Pitfalls

- **A weak hash breaks every signature.** MD5 certificates fell in steps: Lenstra, Wang and de Weger (2005) built two certificates with different public keys and one signature; Stevens, Lenstra and de Weger (2007) did it for different names with a chosen-prefix collision; in 2008 Stevens and others made a rogue CA certificate whose MD5 hash equaled that of a certificate signed by a commercial CA; in 2012 the Flame malware used a new MD5 chosen-prefix collision to pass as signed by Microsoft. For SHA-1, Stevens and others (2017) published the first collision, and Leurent and Peyrin (2020) a chosen-prefix collision that let two PGP keys share one certification signature. See [chosen-prefix collision](/chosen-prefix-collision/) and [signature forgery](/signature-forgery/).
- **Predictable signed data.** All these attacks needed the attacker to predict the exact bytes that the signer would hash. Certification authorities now put an unpredictable serial number into each certificate, which works like randomized hashing.
- **Short hashes.** A hash of $n$ binary digits gives at most about $n/2$ binary digits of security against collisions. Use at least 256 binary digits for security of 128 binary digits.
- **Hash and key of mismatched strength.** A strong key does not help if the hash is weak, and a hash longer than the group order is truncated in DSA and ECDSA. Pick the hash for the security level of the whole scheme.
- **Encoding not fixed by the hash.** The verifier must rebuild and compare the whole encoding of line L4. Parsers that accept extra bytes after the hash allowed the e = 3 forgery of 2006; see [chosen-message attack](/chosen-message-attack/).
- **The hash is not enough to fix an algebraic scheme.** A collision-resistant hash with a short output under textbook RSA still allows multiplicative attacks with smooth values, as Desmedt and Odlyzko and Coron and others showed. Use a full-domain or probabilistic encoding.

## Exercises

1. In the proof of the theorem, why does $C$ need to know the secret key of $\Pi'$, while $B$ does not need anything secret about $H$? *Hint: who answers the signing queries in each reduction?*
2. Let $\Pi$ sign $h = H(r \Vert M)$ for a fresh random $r$ that is sent with the signature but not signed. Show that a forgery $(M', r', \sigma')$ that reuses a signature on a queried $(M, r)$ gives a collision $H(r \Vert M) = H(r' \Vert M')$, so the theorem still applies. Then explain why Yuval's attack becomes harder: what must the attacker know before it computes its variants?
3. With a hash of 64 binary digits, about how many variants of each text does Yuval's attack need for a success probability of about $1/2$? Compare the time with that of a second-preimage search.
4. Take textbook RSA as $\Pi'$ and let $H$ be the identity on short inputs, which is collision resistant. Show that $\Pi$ is not EUF-CMA, and say which hypothesis of the theorem fails.
5. In TCR hashing, show that a forger can win if the key $r$ is not signed, given a collision $H_{r'}(M') = H_r(M)$ for a key $r'$ of its choice.

## References
