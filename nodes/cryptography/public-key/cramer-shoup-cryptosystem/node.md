---
tag: DP6M6E
kind: algorithm
slug: cramer-shoup-cryptosystem
name: Cramer-Shoup cryptosystem
aliases:
- Cramer-Shoup encryption
area: cryptography/public-key
level: advanced
summary: ElGamal with a second generator and a validity tag. The first practical public-key scheme proved IND-CCA2 secure in the standard model, under DDH and a hash assumption.
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of p}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Ronald Cramer, Victor Shoup]
  note: Presented at CRYPTO 1998; full version in SIAM Journal on Computing 2003. The ACE-KEM mechanism of ISO/IEC 18033-2 is based on it.
prereqs: [ind-cca-security, decisional-diffie-hellman, elgamal-encryption]
see_also: [naor-yung-paradigm, fujisaki-okamoto-transform, key-encapsulation-mechanism, hybrid-encryption, non-malleability, collision-resistance, ecies, chosen-ciphertext-attack]
sources:
  - paper: "Ronald Cramer and Victor Shoup, A practical public key cryptosystem provably secure against adaptive chosen ciphertext attack, CRYPTO 1998, LNCS 1462, pages 13 to 25"
    locator: the scheme, the variant without the hash, and the proof of IND-CCA2 security under DDH
  - paper: "Ronald Cramer and Victor Shoup, Design and analysis of practical public-key encryption schemes secure against adaptive chosen ciphertext attack, SIAM Journal on Computing 33(1), pages 167 to 226, 2003"
    locator: the full proofs with concrete bounds, the hybrid versions, and the security of the scheme without a hash under CCA1
  - paper: "Ronald Cramer and Victor Shoup, Universal hash proofs and a paradigm for adaptive chosen ciphertext secure public-key encryption, Eurocrypt 2002, LNCS 2332, pages 45 to 64"
    locator: hash proof systems, and IND-CCA2 schemes from quadratic residuosity and from Paillier's assumption
  - paper: "Kaoru Kurosawa and Yvo Desmedt, A new paradigm of hybrid encryption scheme, CRYPTO 2004, LNCS 3152, pages 426 to 442"
    locator: the shorter hybrid scheme that drops the tag v and relies on an authenticated DEM
  - url: "https://www.iso.org/standard/37971.html"
    title: ISO/IEC 18033-2:2006, Information technology, Security techniques, Encryption algorithms, Part 2, Asymmetric ciphers
    locator: the mechanism ACE-KEM
  - paper: "Victor Shoup, A proposal for an ISO standard for public key encryption, version 2.1, IACR Cryptology ePrint Archive 2001/112, 2001"
    locator: the definition of ACE-KEM and its security analysis
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: the section on the Cramer-Shoup scheme and its proof of chosen-ciphertext security
---

The Cramer-Shoup cryptosystem is the [public-key encryption](/public-key-encryption/) scheme that Ronald Cramer and Victor Shoup published in 1998. It extends [ElGamal](/elgamal-encryption/) with a second generator and a tag $v$ that lets the receiver check, with its private key, that a ciphertext was formed honestly; ciphertexts that fail the check are rejected. It was the first practical scheme proved [IND-CCA2 secure](/ind-cca-security/) in the standard model, without [random oracles](/random-oracle-model/), assuming the [decisional Diffie-Hellman problem](/decisional-diffie-hellman/) is hard and the hash is target collision resistant. A ciphertext has four group elements, and encryption costs about twice as much as ElGamal.

**Notation.** $G$ is a cyclic group of prime order $q$, here the squares modulo a [safe prime](/safe-prime/) $p = 2q + 1$, and $b$ is the number of binary digits of $p$. $g_1$ and $g_2$ are generators of $G$ whose relative discrete logarithm $w = \log_{g_1} g_2$ nobody knows. $H$ maps $G^3$ to $\mathbb{Z}_q$. A ciphertext is $(u_1, u_2, e, v)$; it is *valid* if $\log_{g_1} u_1 = \log_{g_2} u_2$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary that runs in time $t$ and makes $q_d$ decryption queries, and $\mathrm{Adv}$ an advantage. All results here are in the standard model.

## In plain words

ElGamal hides a message well against someone who only listens, but anyone can change a ciphertext so that it decrypts to a related message. If the receiver decrypts such changed ciphertexts and shows the results, an attacker learns the hidden message.

Cramer-Shoup adds a seal to each ciphertext. The sender uses one fresh random number in two parts of the ciphertext and computes the seal from the public key. Only the receiver can check the seal, using secret numbers that the public key does not fully reveal. A ciphertext that was built honestly always passes. A ciphertext that was built any other way, including a changed copy of a real one, fails except with negligible chance, because the attacker cannot predict what the receiver's secret numbers say about it. So asking the receiver to decrypt gives the attacker nothing new.

## The problem

Cramer-Shoup solves [public-key encryption](/public-key-encryption/) with security against adaptive [chosen-ciphertext attacks](/chosen-ciphertext-attack/), the standard goal for encryption used in protocols. Before 1998 the known ways to reach it were either impractical, such as the [Naor-Yung paradigm](/naor-yung-paradigm/) with general non-interactive zero-knowledge proofs, or proved only in the random oracle model, such as [RSA-OAEP](/rsa-oaep/). Cramer-Shoup costs a few exponentiations and needs only DDH in $G$ and a target collision resistant $H$: given a random input $s$, it is hard to find $s' \ne s$ with $H(s') = H(s)$. This is weaker than [collision resistance](/collision-resistance/).

## The algorithm

```pseudo id=main
CS-KEYGEN(G, q, g1, g2)
L1  x1, x2, y1, y2, z ← uniform in Z_q
L2  c ← g1^x1 · g2^x2;  d ← g1^y1 · g2^y2;  h ← g1^z
L3  return the public key (G, g1, g2, c, d, h, H) and the private key (x1, x2, y1, y2, z)

CS-ENCRYPT(pk, m)                        ▷ m ∈ G
L4  r ← uniform in Z_q
L5  u1 ← g1^r;  u2 ← g2^r
L6  e ← h^r · m
L7  α ← H(u1, u2, e)
L8  v ← c^r · d^(r·α)
L9  return (u1, u2, e, v)

CS-DECRYPT(sk, (u1, u2, e, v))
L10 if u1, u2, e or v is not in G then return ⊥
L11 α ← H(u1, u2, e)
L12 if u1^(x1 + y1·α) · u2^(x2 + y2·α) ≠ v then return ⊥
L13 return e · u1^(−z)
```

Lines L5 and L6 are ElGamal with the key $h$, plus the extra value $u_2$ with the same $r$. Line L8 is the tag. The receiver can check it in line L12 without knowing $r$, because $c^r d^{r\alpha} = u_1^{x_1 + y_1\alpha} u_2^{x_2 + y_2\alpha}$ for every valid ciphertext. Line L10 matters in $\mathbb{Z}_p^*$, where values outside $G$ exist; in $\mathbb{Z}_p^*$ the test is $a^q \equiv 1 \pmod p$. Messages are encoded into $G$ as on the ElGamal page.

## Example

Take $p = 23$, $q = 11$, $G$ the squares modulo 23, $g_1 = 4$ and $g_2 = 9$. Let $H$ be SHA-256 of the three values (one byte each) reduced modulo 11, as in the code.

| step | computation | value |
|---|---|---|
| L1 | private key | $x_1 = 3, x_2 = 7, y_1 = 2, y_2 = 9, z = 5$ |
| L2 | $c = 4^3 \cdot 9^7 = 18 \cdot 4$, $d = 4^2 \cdot 9^9 = 16 \cdot 2$, $h = 4^5$ | $c = 3$, $d = 9$, $h = 12$ |
| L4 | message $m = 6$ (a square), randomness | $r = 4$ |
| L5 | $u_1 = 4^4$, $u_2 = 9^4$ | $3$, $6$ |
| L6 | $h^r = 12^4 = 13$, $e = 13 \cdot 6$ | $9$ |
| L7 | $\alpha = H(3, 6, 9)$ | $8$ |
| L8 | $c^r = 3^4 = 12$, $d^{r\alpha} = 9^{32 \bmod 11} = 9^{10} = 18$, $v = 12 \cdot 18$ | $9$ |
| L12 | $u_1^{(3 + 16) \bmod 11} = 3^8 = 6$, $u_2^{(7 + 72) \bmod 11} = 6^2 = 13$, product | $78 \bmod 23 = 9 = v$ |
| L13 | $u_1^{q - z} = 3^6 = 16$, then $9 \cdot 16$ | $144 \bmod 23 = 6$ |

All arithmetic is modulo 23 and exponents are modulo 11. The ElGamal attack changes $e$ to $4 \cdot 9 = 13$. Then $\alpha$ changes, line L12 fails, and decryption returns $\perp$. The variant without the check would return $13 \cdot 16 \bmod 23 = 1 = 4 \cdot 6 \bmod 23$, the related message.

## Correctness

For an honest ciphertext all four values are in $G$, and $u_1^{x_1 + y_1\alpha} u_2^{x_2 + y_2\alpha} = (g_1^{x_1} g_2^{x_2})^r (g_1^{y_1} g_2^{y_2})^{r\alpha} = c^r d^{r\alpha} = v$, so lines L10 and L12 accept. Then $e \cdot u_1^{-z} = g_1^{zr} m \, g_1^{-rz} = m$. The full proof is below.

## Complexity

Let $b$ be the number of binary digits of $p$. An exponentiation with an exponent below $q$ costs $\Theta(b^3)$ with schoolbook arithmetic.

- **Encryption**: five exponentiations ($g_1^r$, $g_2^r$, $h^r$, $c^r$, $d^{r\alpha}$), or four with a simultaneous exponentiation for $c^r d^{r\alpha}$, and one hash: $\Theta(b^3)$. ElGamal needs two.
- **Decryption**: four membership tests, one two-base exponentiation for line L12 and one exponentiation for line L13: $\Theta(b^3)$. On an elliptic curve of prime order the membership tests are cheap.
- **Ciphertext**: four group elements for one message element, against two for ElGamal.

## Properties

### IND-CCA2 security

**Theorem (Cramer and Shoup, 1998).** Let $G$ have prime order $q$. For every IND-CCA2 adversary $\mathcal{A}$ that makes $q_d$ decryption queries there are a DDH distinguisher $\mathcal{B}_1$ and a target collision finder $\mathcal{B}_2$, each running in about the time of $\mathcal{A}$ plus $O(q_d)$ exponentiations, with

$$\mathrm{Adv}^{\mathrm{ind\text{-}cca}}(\mathcal{A}) \le 2\,\mathrm{Adv}^{\mathrm{ddh}}(\mathcal{B}_1) + 2\,\mathrm{Adv}^{\mathrm{tcr}}(\mathcal{B}_2) + O(q_d / q).$$

Here $\mathrm{Adv}^{\mathrm{ind\text{-}cca}} = 2|\Pr[\mathcal{A} \text{ wins}] - \tfrac12|$. The reduction is tight: the DDH advantage is not multiplied by $q_d$, and the additive term is negligible because $q$ is exponential in $\lambda$. Cramer and Shoup (2003) give the exact constants.

*Proof sketch.* $\mathcal{B}_1$ gets $(g_1, g_2, u_1^*, u_2^*)$, a DDH tuple $(g_1, g_1^w, g_1^r, g_1^{wr})$ or a random one $(g_1, g_1^w, g_1^{r}, g_1^{wr'})$ with $r' \ne r$. It picks $x_1, x_2, y_1, y_2$ and two values $z_1, z_2$, and publishes $c, d$ as in line L2 and $h = g_1^{z_1} g_2^{z_2}$. It answers decryption queries with its private key, computing $e / (u_1^{z_1} u_2^{z_2})$ in place of line L13; for valid ciphertexts this gives the same answer, since then $u_1^{z_1} u_2^{z_2} = h^r$. It builds the challenge from $(u_1^*, u_2^*)$ as $e^* = (u_1^*)^{z_1} (u_2^*)^{z_2} m_\beta$ and $v^* = (u_1^*)^{x_1 + y_1\alpha^*} (u_2^*)^{x_2 + y_2\alpha^*}$, and outputs 1 if $\mathcal{A}$ guesses $\beta$.

- *DDH tuple.* The challenge is a valid encryption of $m_\beta$ with randomness $r$, and the view of $\mathcal{A}$ is that of the real game, except when $\mathcal{A}$ submits an invalid ciphertext that passes line L12. By the lemma below this happens with probability at most $q_d / (q - q_d)$.
- *Random tuple.* Here the challenge is invalid. Look at what $\mathcal{A}$ knows about $(z_1, z_2)$: only $\log_{g_1} h = z_1 + w z_2$, as long as all its invalid queries are rejected. The value $\log_{g_1}(e^*/m_\beta) = r z_1 + w r' z_2$ is a second equation, independent of the first because $r \ne r'$. So $e^*$ is uniform in $G$ and independent of $\beta$, and $\mathcal{A}$ wins with probability exactly $\tfrac12$, unless an invalid query is accepted.

**Rejection lemma.** Consider an invalid query $(u_1, u_2, e, v)$ with $u_1 = g_1^{r_1}$, $u_2 = g_2^{r_2}$, $r_1 \ne r_2$, and with $\alpha = H(u_1, u_2, e) \ne \alpha^*$. What $\mathcal{A}$ knows about $(x_1, x_2, y_1, y_2)$ is at most three linear equations: $\log c$, $\log d$ and, in the random case, $\log v^*$. The value $\log_{g_1}$ of the expected tag, $r_1 x_1 + w r_2 x_2 + \alpha r_1 y_1 + \alpha w r_2 y_2$, is a fourth equation, independent of the three when $r_1 \ne r_2$ and $\alpha \ne \alpha^*$. So the expected tag is uniform in $G$ from the view of $\mathcal{A}$, and a guessed $v$ passes with probability $1/q$. Each rejection excludes one value, so the $i$-th query passes with probability at most $1/(q - i)$. The test file counts this exactly for $q = 11$: for every $\alpha$, every tag value is produced by exactly $q$ of the $q^2$ private keys that match $c$ and $d$.

The remaining case is a query with $(u_1, u_2, e) \ne (u_1^*, u_2^*, e^*)$ but $\alpha = \alpha^*$: that is a collision of $H$ on the random target $(u_1^*, u_2^*, e^*)$, which $\mathcal{B}_2$ outputs. A query with the same $(u_1, u_2, e)$ as the challenge and a different $v$ fails line L12, since only one tag passes. Adding these terms gives the theorem. $\square$

### Other properties

- **Non-malleable.** IND-CCA2 implies [non-malleability](/non-malleability/), so the ElGamal mauling of the example fails.
- **A tag that ignores $e$ gives CCA1 only.** "Cramer-Shoup lite" drops $d$, $y_1$, $y_2$ and $H$: the tag is $v = c^r$ and the check is $u_1^{x_1} u_2^{x_2} = v$. It is IND-CCA1 secure under DDH, but the tag does not depend on $e$, so $(u_1, u_2, t e, v)$ passes and decrypts to $t m$. It is malleable and not IND-CCA2 secure.
- **Without a hash.** Cramer and Shoup also describe a variant without $H$, with a longer public key, whose security rests on DDH alone.
- **The receiver's key is not unique.** Many private keys give the same public key; this freedom, used in the proof, is the idea behind hash proof systems.

## Variants and improvements

- **Hybrid Cramer-Shoup and ACE-KEM.** Encrypt a random key instead of a message and use it in a symmetric cipher. Cramer and Shoup (2003) analyse such [KEM](/key-encapsulation-mechanism/) versions, and ACE-KEM, standardized in ISO/IEC 18033-2, is one of them.
- **Kurosawa-Desmedt (2004).** Uses $u_1^{x_1 + y_1\alpha} u_2^{x_2 + y_2\alpha}$ itself as the symmetric key and drops $e$, $h$ and $v$: the ciphertext is $(u_1, u_2)$ and an authenticated symmetric ciphertext. The KEM part alone is not IND-CCA2 secure, but the whole [hybrid scheme](/hybrid-encryption/) is, if the DEM is authenticated.
- **Hash proof systems (2002).** Cramer and Shoup abstracted the construction into universal hash proof systems, which give IND-CCA2 schemes from quadratic residuosity and from Paillier's decisional composite residuosity assumption, also without random oracles.
- **Elliptic curves.** The scheme runs in any group of prime order where DDH is believed hard, such as an elliptic curve group without an efficient pairing.
- **Other routes to CCA security.** [Naor-Yung](/naor-yung-paradigm/) and its successors use zero-knowledge proofs; the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) and [ECIES](/ecies/) are cheaper but proved in the random oracle model.

## When to use it

Use Cramer-Shoup, usually in its KEM or Kurosawa-Desmedt form, when you want chosen-ciphertext security from DDH in the standard model and can afford four group elements per ciphertext and about twice the cost of ElGamal. Most deployed systems choose [ECIES](/ecies/), HPKE (RFC 9180) or the post-quantum [ML-KEM](/crystals-kyber/) instead, whose proofs use random oracles but which are smaller and faster. Like every scheme based on discrete logarithms, Cramer-Shoup is broken by a large quantum computer.

## Pitfalls

- **Skipping line L12, or comparing only part of the tag.** Without the check the scheme is malleable, and one decryption query recovers a message, as for ElGamal. The test file shows the related message that the variant without the check returns.
- **Skipping the membership test of line L10.** In $\mathbb{Z}_p^*$, values outside $G$ fall outside the proof, and values of small order can leak the private key modulo small factors of $p - 1$, as in the [small subgroup attack](/small-subgroup-attack/).
- **Hashing only part of the ciphertext.** $H$ must cover $u_1$, $u_2$ and $e$, with an encoding that is injective, for example fixed-length values. Otherwise two different ciphertexts share $\alpha$ and the proof fails.
- **A known relation between $g_1$ and $g_2$.** The proof uses DDH for the pair $(g_1, g_2)$; a party that knows $\log_{g_1} g_2$ is outside it. Derive $g_2$ by hashing to the group, as the code does, or let the key owner pick it at random and then forget the logarithm.
- **Messages outside $G$.** Encode messages into $G$ as for ElGamal. A message that is not in $G$ makes $e$ fail line L10 or leak its quadratic character.
- **Different error behaviour.** Return the same $\perp$ for every failure, in the same time; a decryption service that reveals why or when a ciphertext was rejected gives the attacker an oracle that the proof does not cover.

## Implementations

The Python code is for study only. It is not constant time, its default group has only 64 binary digits, and it must not protect real data. $H$ is SHA-256 reduced modulo $q$; its target collision resistance is an assumption. There are no official test vectors for the original scheme. The tests check the round trip in the toy group and in the group of the example, the rejection of every single changed component and of values outside $G$, the related message returned by the variant without the check and by the lite tag, the exact count behind the rejection lemma, and a local IND-CCA2 game in which every mauled query is rejected.

## History

Rackoff and Simon defined adaptive chosen-ciphertext security in 1991, and Dolev, Dwork and Naor gave the first non-malleable scheme the same year, using general zero-knowledge proofs that were far too slow for use. Cramer and Shoup presented their scheme at CRYPTO 1998, the first IND-CCA2 secure scheme with a cost close to ElGamal and a proof without random oracles. The full version with concrete bounds and hybrid variants appeared in SIAM Journal on Computing in 2003. Cramer and Shoup generalized the method to universal hash proof systems in 2002, Kurosawa and Desmedt shortened the hybrid version in 2004, and Shoup's ACE-KEM entered ISO/IEC 18033-2 in 2006.

## References
