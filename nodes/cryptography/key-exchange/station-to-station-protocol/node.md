---
tag: NT8D3J
kind: algorithm
slug: station-to-station-protocol
name: Station-to-station protocol
aliases:
- STS protocol
area: cryptography/key-exchange
level: advanced
summary: A three-message authenticated Diffie-Hellman exchange. Each party signs both ephemeral values and encrypts the signature under the new key, for authentication, key confirmation and forward secrecy.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1992
  people: [Whitfield Diffie, Paul C. van Oorschot, Michael J. Wiener]
  note: Diffie, van Oorschot and Wiener published the protocol in 1992 in Designs, Codes and Cryptography, together with the definition of perfect forward secrecy.
prereqs: [diffie-hellman, digital-signature, authenticated-key-exchange]
see_also: [sigma-key-exchange, unknown-key-share-attack, perfect-forward-secrecy, key-confirmation, man-in-the-middle-attack, schnorr-signature, ike-protocol, tls-handshake]
sources:
  - paper: "Whitfield Diffie, Paul C. van Oorschot and Michael J. Wiener, Authentication and authenticated key exchanges, Designs, Codes and Cryptography 2(2), 1992, pages 107 to 125"
    locator: the station-to-station protocol, its basic and full forms, and the definition of perfect forward secrecy
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.6.1, Protocol 12.57 (STS) and Remark 12.58 (key confirmation and the encrypted signatures)
  - paper: "Simon Blake-Wilson and Alfred Menezes, Unknown key-share attacks on the station-to-station (STS) protocol, PKC 1999, LNCS 1560, Springer, 1999, pages 154 to 170"
    locator: the public key substitution attack and the fixes for STS
  - paper: "Hugo Krawczyk, SIGMA: the SIGn-and-MAc approach to authenticated Diffie-Hellman and its use in the IKE protocols, CRYPTO 2003, LNCS 2729, Springer, 2003, pages 400 to 425"
    locator: Section 2 (the STS protocol, its variants and the identity misbinding attacks on them)
---

The station-to-station (STS) protocol is an authenticated [Diffie-Hellman](/diffie-hellman/) key exchange with three messages. The parties exchange ephemeral values $X = g^x$ and $Y = g^y$, each signs the pair of values with its long-term [signature](/digital-signature/) key, and each sends its signature encrypted under the new key $K$ derived from $g^{xy}$. The signatures give mutual authentication, the encryption gives [key confirmation](/key-confirmation/), and the ephemeral exponents give [perfect forward secrecy](/perfect-forward-secrecy/). Diffie, van Oorschot and Wiener published it in 1992, and it is the ancestor of the signature modes of IKE and of [SIGMA](/sigma-key-exchange/).

**Notation.** $G$ is a group of prime order $q$ with generator $g$, a subgroup of $\mathbb{Z}_p^*$ for a prime $p$ of $m$ binary digits. Party $\hat A$ has signature key pair $(sk_A, pk_A)$, and $\hat B$ has $(sk_B, pk_B)$. $\mathrm{SIG}_P(m)$ is a signature of party $P$ on $m$, and $E_K$ and $D_K$ are symmetric encryption and decryption under $K$.

## In plain words

Alice and Bob each pick a fresh random secret and swap the matching public numbers, as in plain Diffie-Hellman. From these numbers both compute the same new key.

Plain Diffie-Hellman does not say who is on the other end. So each of them also signs the two public numbers with a long-term signing key that everybody can check. A person in the middle who swaps the numbers cannot make these signatures.

Each of them then locks the signature with the new key before sending it. When Alice opens Bob's locked signature and it checks out, she knows two things: Bob signed this exchange, and Bob has the same new key.

After the session they throw the random secrets away, so a later theft of the signing keys does not open old sessions.

## The problem

Two parties, each with a long-term signature key pair whose public key the other knows (through a certificate), communicate over a network that an active adversary controls. They want a fresh shared [session key](/session-key/), known only to them, with each party sure of the identity of the other, and with forward secrecy. This is the [authenticated key exchange](/authenticated-key-exchange/) problem.

## The algorithm

$\hat A$ is the initiator and $\hat B$ the responder. In the full protocol the parties also send their certificates with the second and third messages.

```pseudo id=main
STS(A, B)                                       ▷ group G = ⟨g⟩ of prime order q
L1  A: x ← uniform in [1, q − 1]; X ← g^x; send (A, X) to B
L2  B: if A is unknown or X ∉ G then fail
L3  B: y ← uniform in [1, q − 1]; Y ← g^y; K ← KDF(X^y)
L4  B: send (B, Y, c_B = E_K(SIG_B(Y, X))) to A
L5  A: if B is unknown or Y ∉ G then fail; K ← KDF(Y^x); erase x
L6  A: if VERIFY(pk_B, (Y, X), D_K(c_B)) fails then fail
L7  A: send c_A = E_K(SIG_A(X, Y)) to B; accept K with peer B
L8  B: if VERIFY(pk_A, (X, Y), D_K(c_A)) fails then fail
L9  B: erase y; accept K with peer A
```

Lines L1 to L4 are ordinary Diffie-Hellman plus $\hat B$'s signed and encrypted reply. Each party signs the pair with its *own* value first, and so each signature covers the peer's fresh value; this stops replay of old messages. A party accepts only after it checks the peer's signature under the new key: $\hat A$ at line L6, $\hat B$ at line L8. Line L2 and line L5 validate the received group elements, as for plain Diffie-Hellman. The code sends both encrypted signatures under the same $K$, so it uses a different nonce for each direction.

**About the code.** The Python code of this page uses Schnorr signatures in the same 256-bit toy group and a toy stream cipher (SHA-256 in counter mode) for $E_K$. It is for study only. It is not constant time, and the parameters are far too small. Use IKEv2 or TLS 1.3 through a vetted library such as strongSwan, OpenSSL or BoringSSL, or a FIPS 140 validated module.

## Example

Take the toy group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$.

| step | Alice | Bob |
|---|---|---|
| L1 | $x = 57$, sends $X = 4^{57} \bmod 2039 = 1556$ | |
| L2, L3 | | $1556 \in G$; $y = 311$, $Y = 1502$; $Z = 1556^{311} \bmod 2039 = 661$ |
| L4 | | sends $(1502, E_K(\mathrm{SIG}_B(1502, 1556)))$ with $K = \mathrm{KDF}(661)$ |
| L5 | $1502 \in G$; $Z = 1502^{57} \bmod 2039 = 661$; erases 57 | |
| L6 | decrypts and checks $\mathrm{SIG}_B(1502, 1556)$ | |
| L7, L8 | sends $E_K(\mathrm{SIG}_A(1556, 1502))$ | decrypts and checks it; erases 311 |

Now suppose Mallory replaces $X = 1556$ by her own $X' = 4^{100} \bmod 2039 = 1153$. Bob signs $(1502, 1153)$, but Alice checks a signature on $(1502, 1556)$ at line L6, so she rejects. Mallory cannot make Bob's signature on the pair Alice expects.

## Correctness

If both parties are honest and the messages arrive unchanged, then $X^y = g^{xy} = Y^x$, so both compute the same $K$. $E_K$ followed by $D_K$ with the same key and nonce gives back the signature, and a correct signature verifies under the signer's public key, so lines L6 and L8 pass and both parties accept the same $K$, each with the other as peer. The proof is below.

Security against an active adversary is a separate claim. If $X$ or $Y$ is changed, an honest party sees a signature on a pair that its peer did not sign, and rejects unless the adversary forges a signature. If the adversary only records, the key is a Diffie-Hellman value of $X$ and $Y$. STS has no proof in the Canetti-Krawczyk model as originally given; Krawczyk (2003) analyses its variants and shows that they suffer from identity misbinding (below), which SIGMA fixes.

## Complexity

Each party performs one exponentiation to make its ephemeral value, one to compute $g^{xy}$, one for the subgroup check, one to sign and two to verify (Schnorr). Each exponentiation costs $\Theta(m)$ multiplications of $m$-digit numbers modulo $p$, so $\Theta(m^3)$ bit operations with schoolbook multiplication, and $\Theta(m)$ extra space. The protocol has three messages (one and a half round trips). With an elliptic curve group such as Curve25519 and Ed25519 signatures, each operation costs tens of microseconds.

## Properties

- **Mutual explicit authentication.** Each party accepts only after the peer's signature on both fresh values.
- **Key confirmation.** The signatures are encrypted under $K$, so a correct decryption shows that the peer holds $K$ (HAC Remark 12.58).
- **Perfect forward secrecy.** The long-term keys only sign; the key comes from ephemeral values that are erased. The 1992 paper that gave STS also gave the definition of the property.
- **No identity protection from active attacks.** In the basic form the identities and certificates travel in the clear.
- **Not resistant to unknown key-share attacks** when the CA does not check proof of possession (see Pitfalls).

## Variants and improvements

- **Basic STS and STS-MAC.** In the forms that Krawczyk (2003) and Blake-Wilson and Menezes (1999) study, the encryption of the signature is replaced by a MAC under a key derived from $g^{xy}$; both still suffer from the misbinding attack unless identities are added.
- **Identities in the signature.** Signing $(Y, X, \hat A)$, as in ISO/IEC 9798-3, fixes the unknown key-share problem at the cost of revealing the peer's identity in the signed data.
- **SIGMA.** [SIGMA](/sigma-key-exchange/) keeps the signature on the ephemeral values and adds a MAC over the sender's own identity under a separate key. This is the form in IKEv2 and, in spirit, in the TLS 1.3 handshake.
- **Photuris and IKEv1.** Photuris (RFC 2522) was based on STS, and the signature mode of IKEv1 follows the same idea.

## When to use it

STS is a teaching and design reference. In new systems, use a protocol with a security proof that also binds identities: [SIGMA](/sigma-key-exchange/) as in IKEv2, the [TLS 1.3 handshake](/tls-handshake/), or a [Noise](/noise-protocol-framework/) pattern.

## Pitfalls

- **Unknown key share by public key substitution.** At lines L6 and L8, a party checks the signature against the key in the *claimed* certificate. Blake-Wilson and Menezes (1999) showed that $\hat E$ can register $\hat A$'s public key under the name $\hat E$, replace $\hat A$'s certificate with its own in the third message, and make $\hat B$ accept at line L9 with peer $\hat E$, while $\hat A$ accepted at line L7 with peer $\hat B$. The keys are equal, and $\hat E$ does not know them. A CA that demands proof of possession, or identities in the signed data or the MAC, prevents this. The tests run this attack.
- **Session key used before it is handed over.** In the original form, $K$ itself encrypts the signatures at lines L4 and L7, so $K$ is used inside the protocol. Derive a separate key for the encryption, as SIGMA does.
- **Missing group checks.** Without the checks at lines L2 and L5, a value of small order can force $K$ into a small set; see [small subgroup attack](/small-subgroup-attack/).
- **No erasure.** If $x$ or $y$ is kept after lines L5 and L9, a later compromise of the device opens the session; forward secrecy needs the erasure.
- **Stream cipher nonce reuse.** Both encrypted signatures use the same $K$. With a stream cipher, the two messages need different nonces, or the XOR of the two signatures leaks.

## Implementations

## History

Diffie, van Oorschot and Wiener, then at Bell-Northern Research, presented STS in *Authentication and authenticated key exchanges* (Designs, Codes and Cryptography, 1992). The same paper defined perfect forward secrecy and discussed the attacks that motivated the design. The Handbook of Applied Cryptography (1996) lists it as Protocol 12.57. Photuris and the signature modes of IKE followed its pattern. In 1999 Blake-Wilson and Menezes showed unknown key-share attacks on it, and in 2003 Krawczyk's SIGMA gave the variant with a proof in the Canetti-Krawczyk model that IKEv2 adopted.

## References
