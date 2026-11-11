---
tag: BRDGNB
kind: algorithm
slug: boneh-franklin-ibe
name: Boneh-Franklin identity-based encryption
aliases:
- Boneh-Franklin IBE
area: cryptography/public-key
level: advanced
summary: "The first practical identity-based encryption (2001). A pairing turns the identity hash H1(ID) and P_pub = sP into an ElGamal-like key; FullIdent is IND-ID-CCA under BDH with random oracles."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the field size p}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 2001
  people: [Dan Boneh, Matthew Franklin]
  note: Boneh and Franklin presented the scheme at Crypto 2001 and the full version in SIAM Journal on Computing in 2003. Galindo found a flawed step in the proof of FullIdent in 2005 and fixed it with a looser reduction.
prereqs: [identity-based-encryption, bilinear-diffie-hellman, bilinear-pairing, random-oracle-model]
see_also: [fujisaki-okamoto-transform, miller-algorithm, ind-cca-security, elgamal-encryption, bls-signature, attribute-based-encryption, hybrid-encryption, menezes-okamoto-vanstone-reduction]
sources:
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, Crypto 2001, LNCS 2139, pages 213 to 229"
    locator: the schemes BasicIdent and FullIdent, the security theorems under BDH in the random oracle model, and the threshold PKG
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, SIAM Journal on Computing 32(3), 2003, pages 586 to 615"
    locator: the full version with the proofs, the concrete bound for BasicIdent with the factor e(1 + q_E) q_H2, and the map to the curve y^2 = x^3 + 1
  - paper: "Eiichiro Fujisaki and Tatsuaki Okamoto, Secure integration of asymmetric and symmetric encryption schemes, Crypto 1999, LNCS 1666, pages 537 to 554"
    locator: the transform that FullIdent applies to BasicIdent
  - paper: "Jean-Sebastien Coron, On the exact security of full domain hash, Crypto 2000, LNCS 1880, pages 229 to 235"
    locator: the biased coin in the simulation of the hash oracle, which gives the factor e(1 + q_E)
  - paper: "David Galindo, Boneh-Franklin identity based encryption revisited, ICALP 2005, LNCS 3580, pages 791 to 802"
    locator: the flawed step in the original security reduction for FullIdent, the fix without a change of scheme or assumption, and a variant with a more efficient reduction
  - url: "https://www.rfc-editor.org/rfc/rfc5091"
    title: "Xavier Boyen and Luther Martin, RFC 5091, Identity-Based Cryptography Standard (IBCS) #1, Supersingular curve implementations of the BF and BB1 cryptosystems, 2007"
    locator: the BF encryption and decryption on supersingular curves with embedding degree 2, the hash to the curve, and the parameter sizes
---

Boneh-Franklin IBE is the first practical [identity-based encryption](/identity-based-encryption/) scheme. Dan Boneh and Matthew Franklin published it in 2001. A key generator publishes $P_{\mathrm{pub}} = sP$ in a group with a [bilinear pairing](/bilinear-pairing/) $e$ and gives the owner of an identity $\mathsf{ID}$ the private key $d_{\mathsf{ID}} = s \cdot H_1(\mathsf{ID})$. A sender encrypts like [ElGamal](/elgamal-encryption/) with the key $e(H_1(\mathsf{ID}), P_{\mathrm{pub}})$, which it can compute without the owner's help. The basic version, BasicIdent, is IND-ID-CPA secure under the [bilinear Diffie-Hellman assumption](/bilinear-diffie-hellman/) in the [random oracle model](/random-oracle-model/). The full version, FullIdent, adds the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) and is IND-ID-CCA secure under the same assumptions.

**Notation.** $\mathbb{G}_1 = \langle P \rangle$ is a group of prime order $q$, written additively, and $e : \mathbb{G}_1 \times \mathbb{G}_1 \to \mathbb{G}_T$ is a symmetric pairing; the elements of $\mathbb{G}_T$ lie in $\mathbb{F}_{p^2}$. $s \in \mathbb{Z}_q^*$ is the master key and $P_{\mathrm{pub}} = sP$. The hash functions are $H_1 : \{0,1\}^* \to \mathbb{G}_1 \setminus \{\mathcal{O}\}$, $H_2 : \mathbb{G}_T \to \{0,1\}^n$, $H_3 : \{0,1\}^n \times \{0,1\}^n \to \mathbb{Z}_q^*$ and $H_4 : \{0,1\}^n \to \{0,1\}^n$. Messages have $n$ binary digits. $r$ is the randomness of one encryption, $q_E$ is the number of key queries of an adversary, $q_{H_2}$ its number of $H_2$ queries, and $b$ the number of binary digits of $p$.

## In plain words

A trusted server picks a secret number and publishes one public value made from it. Every name, such as an email address, is hashed to a point. The private key for a name is that point scaled by the secret, and only the server can make it. To send a message to a name, you need only the name and the public value. A pairing lets you build a one-time key from them that equals what the owner can build from its private key and your short header. The message is masked with a hash of that key. Someone with the key of another name gets a different value and learns nothing. The full version adds checks, so that a changed ciphertext is refused. The server can read every message, so it must be trusted.

## The problem

Build an [identity-based encryption](/identity-based-encryption/) scheme: algorithms Setup, Extract, Encrypt and Decrypt such that anyone can encrypt to any string $\mathsf{ID}$ with the public parameters, only the holder of $d_{\mathsf{ID}}$ can decrypt, and the scheme stays secure when the adversary holds the keys of other identities. The goal is IND-ID-CCA security, defined on the IBE page.

## The algorithm

```pseudo id=main
BF-SETUP(κ)                                 ▷ a pairing group (q, G1, GT, e, P) for κ
L1  s ← a uniform element of Z_q^*
L2  P_pub ← s·P
L3  return params = (P, P_pub, H1, H2, H3, H4) and master key s

BF-EXTRACT(s, ID)
L4  Q_ID ← H1(ID)                           ▷ a point of G1, not O
L5  return d_ID ← s·Q_ID

BASIC-ENCRYPT(params, ID, M)                ▷ M ∈ {0,1}^n
L6  r ← a uniform element of Z_q^*
L7  g_ID ← e(H1(ID), P_pub)                 ▷ can be cached per identity
L8  return (U, V) = (r·P, M ⊕ H2(g_ID^r))

BASIC-DECRYPT(d_ID, (U, V))
L9  return V ⊕ H2(e(d_ID, U))

FULL-ENCRYPT(params, ID, M)
L10 σ ← a uniform string of n binary digits, r ← H3(σ, M)
L11 g_ID ← e(H1(ID), P_pub)
L12 return (U, V, W) = (r·P, σ ⊕ H2(g_ID^r), M ⊕ H4(σ))

FULL-DECRYPT(d_ID, (U, V, W))
L13 if U ∉ G1 or U = O then return ⊥
L14 σ ← V ⊕ H2(e(d_ID, U)), M ← W ⊕ H4(σ)
L15 if U ≠ H3(σ, M)·P then return ⊥
L16 return M
```

The key relation is $e(d_{\mathsf{ID}}, U) = e(sQ_{\mathsf{ID}}, rP) = e(Q_{\mathsf{ID}}, P)^{sr} = e(Q_{\mathsf{ID}}, sP)^r = g_{\mathsf{ID}}^r$. The sender knows $r$ and $P_{\mathrm{pub}}$; the owner knows $d_{\mathsf{ID}}$ and $U$. In FullIdent, the randomness $r$ is a hash of the seed $\sigma$ and the message, so the receiver can recompute it in line L15 and check that the sender built $U$ honestly. A user can check its key with $e(d_{\mathsf{ID}}, P) = e(H_1(\mathsf{ID}), P_{\mathrm{pub}})$.

$H_1$ must map to a point whose discrete logarithm nobody knows. Boneh and Franklin use the curve $y^2 = x^3 + 1$ with $p \equiv 2 \pmod 3$, on which every $y$ gives exactly one $x$, so a hash to $y$ gives a point. The code uses $y^2 = x^3 + x$ and a toy try-and-increment hash: hash a counter and the identity to $x$, retry until $x^3 + x$ is a square, then multiply by the cofactor.

## Example

Take the curve $y^2 = x^3 + x$ over $\mathbb{F}_{59}$, with $q = 5$ and the pairing $e(A, B) = t_5(A, \phi(B))$, $\phi(x, y) = (-x, iy)$, as on the [BDH page](/bilinear-diffie-hellman/). The generator is $P = (35, 31)$, with $2P = (25, 29)$, $3P = (25, 30)$ and $4P = (35, 28)$, and $e(P, P) = 42 + 19i$. These numbers are far too small to be secure; they only show the algebra.

| step | computation | value |
|---|---|---|
| L1, L2 | $s = 2$, $P_{\mathrm{pub}} = 2P$ | $(25, 29)$ |
| L4 | say $H_1(\text{alice}) = 3P$ | $(25, 30)$ |
| L5 | $d_{\text{alice}} = 2 \cdot 3P = 6P = P$ | $(35, 31)$ |
| L7 | $g = e(3P, 2P) = e(P, P)^6 = e(P, P)$ | $42 + 19i$ |
| L6, L8 | $r = 4$, $U = 4P$, mask $H_2(g^4)$ | $U = (35, 28)$, $g^4 = 42 + 40i$ |
| L9 | $e(d_{\text{alice}}, U) = e(P, 4P) = e(P, P)^4$ | $42 + 40i$, the same mask |

Alice removes the mask and reads $M$. Bob, with $H_1(\text{bob}) = P$, holds $d_{\text{bob}} = 2P$ and computes $e(2P, 4P) = e(P, P)^8 = e(P, P)^3 = 46 + 56i$, a different value, so his mask is wrong. The tests check this table, and the same behavior on a 128-binary-digit toy curve with real hashing.

## Correctness

BasicIdent decrypts correctly because bilinearity gives $e(d_{\mathsf{ID}}, U) = g_{\mathsf{ID}}^r$, so the two masks in lines L8 and L9 are equal. In FullIdent the same equality gives back $\sigma$ in line L14, then $M$, then $r = H_3(\sigma, M)$, so the check of line L15 passes for every honest ciphertext. The proof file gives the details.

## Complexity

Let $b$ be the number of binary digits of $p$, and assume that $q$ has $\Theta(b)$ binary digits, as for a supersingular curve with embedding degree 2. With schoolbook arithmetic, a multiplication in $\mathbb{F}_p$ or $\mathbb{F}_{p^2}$ costs $\Theta(b^2)$.

- **A pairing** is a [Miller loop](/miller-algorithm/) with $\Theta(b)$ steps of $O(1)$ field operations each, then a final exponentiation of $\Theta(b)$ squarings, so $\Theta(b^3)$.
- **Extract**: one hash to the curve (an expected $O(1)$ tries with a square root each, $\Theta(b^3)$) and one scalar multiplication, $\Theta(b^3)$.
- **Encrypt**: one hash to the curve, one pairing, one exponentiation in $\mathbb{G}_T$ and one scalar multiplication, so $\Theta(b^3)$. For a repeated recipient, $g_{\mathsf{ID}}$ is cached and no pairing is needed.
- **Decrypt**: one pairing, plus one scalar multiplication in FullIdent, so $\Theta(b^3)$.
- **Size**: $U$ is one point of $\mathbb{G}_1$, and $V$ and $W$ have $n$ binary digits each.

## Properties

**BasicIdent is IND-ID-CPA secure.** Boneh and Franklin prove: if an adversary $\mathcal{A}$ has advantage $\varepsilon$ against BasicIdent with $q_E$ key queries and $q_{H_2}$ queries to $H_2$, with $H_1$ and $H_2$ random oracles, then there is an algorithm $\mathcal{B}$ for BDH with success probability at least $2\varepsilon / (e(1 + q_E) q_{H_2})$, where $e \approx 2.718$. The idea of the proof:

1. $\mathcal{B}$ gets $(P, aP, bP, cP)$ and sets $P_{\mathrm{pub}} = aP$, so the unknown $a$ plays the role of $s$.
2. For each new identity, $\mathcal{B}$ picks $x \in \mathbb{Z}_q^*$ and flips a biased coin. With probability $\delta$ it sets $H_1(\mathsf{ID}) = xP$, and can answer a key query with $x \cdot P_{\mathrm{pub}} = a \cdot xP$. Otherwise it sets $H_1(\mathsf{ID}) = x \cdot bP$, and cannot answer, so it gives up if asked.
3. If the target has $H_1(\mathsf{ID}^*) = x \cdot bP$, the challenge is $U = cP$ with a random $V$. The real mask is $H_2(e(xbP, aP)^c) = H_2(e(P, P)^{abcx})$. An adversary that tells the two messages apart must ask $H_2$ at this point, so $\mathcal{B}$ picks one of the $q_{H_2}$ queries and raises it to $x^{-1} \bmod q$.

The best $\delta$ makes $\mathcal{B}$ survive the key queries and the challenge with probability at least $1/(e(1 + q_E))$. This biased coin is Coron's technique for full domain hash signatures.

**FullIdent is IND-ID-CCA secure.** FullIdent is BasicIdent after the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/), and Boneh and Franklin prove it IND-ID-CCA secure under BDH with $H_1, \ldots, H_4$ random oracles. Galindo (2005) found a flawed step in that reduction. He fixed the proof without a change of the scheme or the assumption, but his reduction is looser. Later papers gave tighter reductions.

**BasicIdent is malleable.** Flipping a binary digit of $V$ flips the same digit of $M$. So BasicIdent is not IND-ID-CCA secure, and the tests show the attack. FullIdent rejects such changes in line L15.

**Key escrow.** The PKG can compute every private key. This is part of the model of IBE, not a weakness of the scheme.

## Variants and improvements

- **Threshold PKG.** Boneh and Franklin share $s$ among $t$-of-$m$ servers with [Shamir secret sharing](/shamir-secret-sharing/). Each server returns $s_i Q_{\mathsf{ID}}$, and the user combines $t$ shares by Lagrange interpolation in the exponent, so no single server knows $s$.
- **Asymmetric pairings.** On curves such as BLS12-381, there is no distortion map. One puts $P$ and $U$ in one group and $H_1(\mathsf{ID})$ and $d_{\mathsf{ID}}$ in the other, and the security proof uses the matching asymmetric form of BDH.
- **Sakai-Kasahara IBE.** The private key is $\frac{1}{s + H(\mathsf{ID})} P$, so there is no hash to the curve, and encryption needs no pairing. Its security uses a $q$-type assumption. It is standardized as SAKKE in RFC 6508.
- **Standard-model schemes.** Boneh-Boyen (2004) and Waters (2005) remove the random oracles, under DBDH; see [identity-based encryption](/identity-based-encryption/).
- **Hierarchical IBE.** Gentry and Silverberg (2002) extend the scheme so that a user can give keys to its sub-identities.

## When to use it

Use Boneh-Franklin when a central authority already holds the trust, for example inside one company, and senders must encrypt to people who have no keys yet, or without a certificate lookup. Use FullIdent, or BasicIdent inside a KEM with an authenticated cipher, never BasicIdent alone. If key escrow is not acceptable, or if there is a working public-key infrastructure, ordinary [hybrid encryption](/hybrid-encryption/) with certified keys is simpler and needs no pairing.

## Pitfalls

- **A hash with a known discrete logarithm.** If $H_1(\mathsf{ID}) = h(\mathsf{ID}) \cdot P$ for an ordinary hash $h$ to $\mathbb{Z}_q$, then anyone computes $d_{\mathsf{ID}} = h(\mathsf{ID}) \cdot P_{\mathrm{pub}}$. $H_1$ must hash directly to the curve, as in RFC 9380 for modern curves.
- **Unchecked points.** Line L13 rejects a $U$ off the curve or outside $\mathbb{G}_1$. Without it, a crafted $U$ in a small subgroup can leak information about $d_{\mathsf{ID}}$ through the pairing values.
- **BasicIdent with a decryption service.** BasicIdent is malleable, so any service that decrypts and returns the result leaks challenge plaintexts.
- **Small fields.** For embedding degree 2, the discrete logarithm in $\mathbb{F}_{p^2}$ breaks the scheme through the [MOV reduction](/menezes-okamoto-vanstone-reduction/), so $p^2$ needs about 3072 binary digits for 128-bit security. The toy curves of the code are far smaller and are not secure.
- **Revocation and key lifetime.** A leaked $d_{\mathsf{ID}}$ stays valid for that identity forever. Encrypt to the identity with a date, so that keys expire.
- **Reused randomness.** Two BasicIdent ciphertexts to the same identity with the same $r$ have the same mask, and their XOR is $M_1 \oplus M_2$.

## Implementations

The Python code implements BasicIdent and FullIdent as above. It is for study only: the curves are toys and are not secure, the hash functions are toys, and the code is not constant time. For real use, take a maintained library, for example the BF-IBE code of the Charm framework on a pairing library, or MIRACL Core, and follow RFC 5091 or IEEE 1363.3. RFC 5091 specifies BF on other supersingular curves with other hash functions, so its values do not apply to this code, and there are no other official test vectors. The tests check the table above, that the right identity decrypts and a wrong one does not, the key check, the malleability of BasicIdent, and that FullIdent rejects changed ciphertexts and the wrong key, with fixed seeds on a toy curve with a 128-binary-digit $p$.

## History

Shamir asked for identity-based encryption in 1984 and built only signatures. Pairings entered cryptography as an attack, the MOV reduction of 1993, and Joux used them constructively for three-party key exchange in 2000. In 2001 Boneh and Franklin built IBE from the Weil pairing on $y^2 = x^3 + 1$, with BasicIdent, FullIdent and the BDH assumption, and Cocks found an independent scheme from quadratic residues. The full version appeared in SIAM Journal on Computing in 2003. Galindo corrected the proof of FullIdent in 2005, and Boyen and Martin wrote the scheme down as RFC 5091 in 2007.

## References
