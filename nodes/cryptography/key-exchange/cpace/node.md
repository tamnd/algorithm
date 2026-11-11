---
tag: RGPFSD
kind: algorithm
slug: cpace
name: CPace
aliases:
- Composable Password Authenticated Connection Establishment
area: cryptography/key-exchange
level: research
summary: The balanced PAKE selected by the CFRG in 2020. Both sides hash the password and session id to a generator g with Elligator 2, then run Diffie-Hellman with base g. One round.
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the field prime q}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2019
  people: [Björn Haase, Benoît Labrique, Michel Abdalla, Julia Hesse]
  note: Haase and Labrique introduced CPace and AuCPace at TCHES 2019. The CFRG selected CPace as its balanced PAKE in 2020. Abdalla, Haase and Hesse proved it UC secure in 2021.
prereqs: [password-authenticated-key-exchange, diffie-hellman, x25519]
see_also: [spake2, j-pake, opaque, encrypted-key-exchange, secure-remote-password, random-oracle-model, universal-composability]
sources:
  - paper: "Björn Haase and Benoît Labrique, AuCPace: efficient verifier-based PAKE protocol tailored for the IIoT, IACR Transactions on Cryptographic Hardware and Embedded Systems (TCHES) 2019, issue 2"
    locator: the balanced protocol CPace and the augmented protocol AuCPace built on it
  - url: "https://datatracker.ietf.org/doc/draft-irtf-cfrg-cpace/21/"
    title: Michel Abdalla, Björn Haase and Julia Hesse, CPace, a balanced composable PAKE, draft-irtf-cfrg-cpace-21, 23 April 2026
    locator: Section 4.1 (inputs PRS, CI, sid, ADa, ADb), Section 7.2 (protocol instructions), Section 8.1 (generator_string), Section 8.2 (G_X25519), Section 10.4 (key confirmation and forward security), Section 10.12 (quantum annoyance), Appendix A (functions), Appendix B.1 (test vectors for X25519 and SHA-512)
  - url: "https://eprint.iacr.org/2021/114"
    title: Michel Abdalla, Björn Haase and Julia Hesse, Security analysis of CPace, CRYPTO 2021 (full version IACR ePrint 2021/114)
    locator: the UC security proof in the random oracle model under the strong CDH and strong simultaneous DH assumptions, including the cofactor and single-coordinate cases
  - url: "https://www.rfc-editor.org/rfc/rfc9380"
    title: Armando Faz-Hernandez, Sam Scott, Nick Sullivan, Riad S. Wahby and Christopher A. Wood, RFC 9380, Hashing to Elliptic Curves, August 2023
    locator: Section 6.7.1 (map_to_curve_elligator2)
---

CPace is a balanced [password-authenticated key exchange](/password-authenticated-key-exchange/). Both parties hash the password together with a session identifier to a point $g$ on the curve, and then run one round of [Diffie-Hellman](/diffie-hellman/) with $g$ as the base. Nobody knows the discrete logarithm of $g$ with respect to any other point, so a share $g^y$ looks random to anyone who does not know the password. Haase and Labrique introduced CPace in 2019, the CFRG selected it as its balanced PAKE in 2020, and Abdalla, Haase and Hesse proved it secure in the [UC](/universal-composability/) framework in 2021. The specification is draft-irtf-cfrg-cpace, version 21 of April 2026.

**Notation.** Additive group notation is not used: following the draft, $\mathrm{X25519}(y, g)$ is the scalar multiplication of [X25519](/x25519/) on the u-coordinate $g$. PRS is the password-related string, CI the channel identifier, sid the session identifier, and $AD_a$, $AD_b$ associated data sent in clear. $H$ is SHA-512 with input block size 128 bytes. DSI = `"CPace255"` is the domain separation string. $\mathrm{lv\_cat}$ concatenates strings, each preceded by its length in LEB128 encoding. $I$ is the neutral element, encoded as 32 zero bytes. $y_a, y_b$ are the random scalars of $A$ and $B$; $Y_a$, $Y_b$ their shares; ISK the intermediate session key.

## In plain words

Two devices share a password and want a strong key. Each device turns the password, together with a public value unique to this session, into a secret starting point on an elliptic curve. Both devices get the same starting point if they used the same password.

Then they do an ordinary Diffie-Hellman exchange from that starting point: each picks a random number, sends its result, and combines the other's result with its own number. If the passwords match, both get the same secret. If not, the secrets are unrelated.

The values on the wire look random whatever the password is, so an eavesdropper cannot test guesses. An active attacker can test one guess per session.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/) in the balanced setting: both parties hold the same password, and they want a [session key](/session-key/) with no public key infrastructure, so that an active attacker gets one guess per run and a passive one learns nothing it can test offline. CPace targets constrained devices, for example industrial sensors, and settings with or without fixed initiator and responder roles.

## The algorithm

```pseudo id=main
CPace(PRS, CI, sid, ADa, ADb)        ▷ draft-irtf-cfrg-cpace-21, G_X25519 with SHA-512
                                      ▷ calculate_generator, Section 8.2, by each party
L1  gen_str ← lv_cat(DSI, PRS, zero_bytes(len_zpad), CI, sid)
L2  h ← H.hash(gen_str, 32)
L3  u ← decodeUCoordinate(h, 255)    ▷ clear the top bit
L4  g ← map_to_curve_elligator2(u)    ▷ keep only the u-coordinate
                                      ▷ one party, Section 7.2
L5  y ← 32 random bytes;  Y ← X25519(y, g)
L6  K ← X25519(y, Y_peer)
L7  abort if K = I
L8  ISK ← H.hash(lv_cat(DSI ‖ "_ISK", sid, K) ‖ transcript(Ya, ADa, Yb, ADb))
                                      ▷ the run
L9  A → B: Ya, ADa
L10 B → A: Yb, ADb                    ▷ L9 and L10 can be sent at the same time
L11 A: lines L6 to L8 with ya and Yb
L12 B: lines L6 to L8 with yb and Ya
```

Lines L1 to L4 compute the password-dependent generator. The zero padding makes the password and the DSI fill the first 128-byte block of the hash, so the work of the first block does not depend on the length of a short password, and that block does not depend on sid or CI (Section 8.1). Line L4 is the Elligator 2 map of RFC 9380: a function that maps any field element to a point of the curve. Its output has no known discrete logarithm to the base point, and that is the heart of CPace. If it had one, an attacker could test passwords offline.

Lines L5 to L8 are a Diffie-Hellman exchange from $g$. Line L6 uses the X25519 function, which multiplies by the cofactor through the clamping of the scalar, so a low-order $Y_{peer}$ gives $K = I$, and line L7 aborts. Line L8 hashes $K$ with sid and the transcript. In the initiator-responder setting, $\mathrm{transcript} = \mathrm{lv\_cat}(Y_a, AD_a) \| \mathrm{lv\_cat}(Y_b, AD_b)$; in the symmetric setting, where no party is first, it is the "ordered concatenation" that puts the larger string first, with prefix `"oc"`. Both forms are in the code.

CPace has no built-in key confirmation. Section 10.4 of the draft recommends adding a MAC round with $\mathrm{mac\_key} = H(\texttt{"CPaceMac"} \| sid \| ISK)$ when perfect forward secrecy is needed.

**About the code.** The Python code is for study only. It is not constant time (Python integers are not, and the square test of Elligator 2 branches), and it must not protect real data. X25519 and Elligator 2 are local copies; SHA-512 comes from the standard library.

## Example

Appendix B.1 of the draft. PRS = `Password`, CI = `0b A_initiator 0b B_responder` (the two identities with their lengths), sid = `7e4b4791 d6a8ef01 9b936c79 fb7f2c57`, $AD_a$ = `ADa`, $AD_b$ = `ADb`.

| step | value (hex) |
|---|---|
| L1: gen_str | 170 bytes, `08 4350616365323535 08 50617373776f7264 6d 00...00 18 0b415f69... 10 7e4b4791...` |
| L2: hash | `03998087 bdb1a261 ... e4aed1d3` |
| L4: $g$ | `d04bf6d4 1f6a2896 ... 2f05a73f` |
| L5: $Y_a$ | `1d13c892 78cdadd8 ... ce0c9f32` |
| L5: $Y_b$ | `248cccf6 d5cdc364 ... 32185623` |
| L6: $K$ | `5b067eff bdc0b2a0 ... 71322c6b` |
| L8: ISK (initiator-responder) | `6e19b875 f7a561d6 ... 285f2263` |
| L8: ISK (symmetric) | `eef745e2 f6e7ae2b ... 56382be4` |

The length byte `6d` (109) in gen_str is the zero padding. Both parties compute the same $K$ from different sides. The tests check every value of Appendix B.1.1 to B.1.7 and the low-order and non-canonical points of B.1.10.

## Correctness

**Claim.** If PRS, CI and sid match, both parties compute the same $g$, the same $K$, and, with equal transcripts, the same ISK. Lines L1 to L4 are a deterministic function of (PRS, CI, sid). For X25519, $\mathrm{X25519}(y_a, \mathrm{X25519}(y_b, g)) = \mathrm{X25519}(y_b, \mathrm{X25519}(y_a, g))$, because both are the u-coordinate of $c_a c_b \cdot G$ for the clamped scalars $c_a$, $c_b$ and the point $G$ with u-coordinate $g$. If PRS differs, the two generators differ, and the keys agree only with negligible probability. See the [full proof](/cpace/proofs/correctness/).

**Security.** Abdalla, Haase and Hesse (2021) prove that CPace realizes the UC functionality for PAKE (in a form with lazy extraction of the password guess) in the [random oracle model](/random-oracle-model/), under the strong computational Diffie-Hellman (sCDH) and strong simultaneous Diffie-Hellman (sSDH) assumptions. Their proof covers the X25519 cipher suite with its cofactor and single-coordinate arithmetic. The draft states that without key confirmation CPace has weak forward security, and with explicit key confirmation it has perfect forward security (Section 10.4). Barbosa, Gellert, Hesse and Jarecki (2024) cover the case without a pre-agreed sid.

## Complexity

Each party hashes about two blocks of SHA-512 in line L2, computes one Elligator 2 map (one Legendre symbol and one inversion, each a field exponentiation of $O(n)$ multiplications) and two X25519 ladders of 255 steps each. With schoolbook arithmetic on $n$-digit field elements, each costs $O(n^3)$ word operations, so a run is $O(n^3)$ with $n = 255$. Compared with plain [ECDH](/ecdh/), the extra cost is the map of line L4, which costs much less than one scalar multiplication. The protocol has one round and two messages; key confirmation, if added, is one more round. Each party keeps $O(1)$ field elements.

## Properties

- **Balanced**: both parties hold PRS.
- **One round**, and the two messages can be sent in parallel; there is no initiator-responder order unless the application wants one.
- **No trusted setup**: unlike [SPAKE2](/spake2/), there are no fixed points whose discrete logarithms could have a trapdoor.
- **Implicit authentication**: a party learns that the peer had the same password only when the keys are used, unless key confirmation is added.
- **Quantum annoying**: with a fresh sid, an attacker who can solve discrete logarithms must still solve one Diffie-Hellman problem per password guess, because each guess gives a different generator (Section 10.12; Eaton and Stebila 2021). This is not post-quantum security.
- **Associated data** $AD_a$, $AD_b$ is authenticated through the transcript.

## Variants and improvements

- **Cipher suites**: X448 with SHAKE-256, ristretto255 and decaf448 with prime order, and short Weierstrass curves such as P-256 with the hash-to-curve encodings of RFC 9380 (Sections 8.2 to 8.4).
- **Symmetric setting**: the ordered transcript, for peers with no fixed roles.
- **AuCPace** (Haase and Labrique 2019): an augmented PAKE built on CPace, in which the server stores a verifier and sends a salt.
- **SPEKE** (Jablon 1996) first derived the generator from the password; CPace adds the session identifier, the transcript hash and a proof, and avoids attacks on SPEKE found by Hao and Shahandashti.

## When to use it

Use CPace when two parties share a password or a short pairing code and want a key with no public key infrastructure, for example in device pairing or industrial networks. It is the CFRG recommendation for a balanced PAKE. If a server stores credentials for many users, use an augmented PAKE such as [OPAQUE](/opaque/), so that a stolen database is not a password equivalent.

## Pitfalls

- **A generator from the password alone.** Leaving sid out of line L1 is allowed but loses quantum annoyance and needs the extra analysis of Barbosa et al.; use a fresh sid when one is available.
- **A map with a known logarithm.** Replacing line L4 by $g = h(\mathrm{PRS}) \cdot B$ for the base point $B$ breaks the protocol: an eavesdropper computes $Y = y' \cdot B$ for each guess and tests it offline. Use a map to the curve such as Elligator 2.
- **No identity check.** Line L7 must abort on $K = I$; otherwise a low-order point from the peer fixes the key.
- **Parties not bound.** Without identities in CI or $AD_a$, $AD_b$, CPace makes a key with anyone who knows the password (Section 10.1).
- **Wrong transcript form.** The initiator-responder and the symmetric transcripts in line L8 give different keys. Both parties must use the same form.
- **Using ISK directly for many purposes.** Derive application keys from ISK with a KDF such as [HKDF](/hkdf/).

## Implementations

The Python code gives `generator_string`, `calculate_generator` (lines L1 to L4), `message` (line L5), `derive_isk` (lines L6 to L8) and `run` (lines L9 to L12), with local X25519, Elligator 2 and LEB128 helpers, and both transcript forms. The tests check RFC 7748, Section 5.2, the string helpers, every value of Appendix B.1.1 to B.1.7, the low-order points of B.1.10, a wrong password and the dependence of $g$ on sid.

## History

Jablon's SPEKE (1996) was the first PAKE that hashed the password to the generator, and the IEEE 1363.2 and ISO/IEC 11770-4 standards included variants of it. Hao and Shahandashti (2014) found impersonation and key malleability attacks on SPEKE as specified. Haase and Labrique, at Endress+Hauser, designed CPace and the augmented AuCPace for the industrial Internet of things and published them at TCHES 2019. In the CFRG PAKE selection of 2019 and 2020, CPace was chosen as the balanced PAKE and [OPAQUE](/opaque/) as the augmented one. Abdalla, Haase and Hesse proved CPace UC secure at CRYPTO 2021, and the draft reached version 21 in April 2026.

## References
