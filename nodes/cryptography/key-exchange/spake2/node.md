---
tag: KH3HNV
kind: algorithm
slug: spake2
name: SPAKE2
aliases:
- SPAKE2 PAKE
area: cryptography/key-exchange
level: advanced
summary: A balanced PAKE. Each side masks its Diffie-Hellman share with w M or w N, for a password scalar w and fixed points M and N. Abdalla and Pointcheval 2005, RFC 9382 (2023).
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order p}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2005
  people: [Michel Abdalla, David Pointcheval]
  note: Abdalla and Pointcheval defined SPAKE1 and SPAKE2 at CT-RSA 2005 with a proof in the random oracle model. RFC 9382 (2023) specifies SPAKE2 and RFC 9383 (2023) the augmented SPAKE2+.
prereqs: [password-authenticated-key-exchange, diffie-hellman, elliptic-curve-cryptography]
see_also: [cpace, encrypted-key-exchange, j-pake, opaque, secure-remote-password, ecdh, hkdf, kerberos]
sources:
  - paper: doi:10.1007/978-3-540-30574-3_14
    title: Michel Abdalla and David Pointcheval, Simple password-based encrypted key exchange protocols, CT-RSA 2005, LNCS 3376, pages 191 to 208
    locator: the protocols SPAKE1 and SPAKE2, and their security proofs in the random oracle model under the computational Diffie-Hellman assumption
  - url: "https://www.rfc-editor.org/rfc/rfc9382"
    title: Watson Ladd, RFC 9382, SPAKE2, a Password-Authenticated Key Exchange, September 2023
    locator: Section 3.2 (setup, w = MHF(pw) mod p), Section 3.3 (the protocol and the transcript TT), Section 4 (key schedule and key confirmation), Section 5 (per-user M and N, and M = N), Section 6 (ciphersuites and the points M and N), Section 7 (security), Appendix A (generation of M and N), Appendix B (test vectors)
  - url: "https://www.rfc-editor.org/rfc/rfc9383"
    title: Tim Taubert and Christopher A. Wood, RFC 9383, SPAKE2+, an Augmented Password-Authenticated Key Exchange (PAKE) Protocol, September 2023
    locator: the augmented variant, in which the server stores w0 and L = w1 P
  - paper: doi:10.1007/978-3-030-56784-2_10
    title: Michel Abdalla, Manuel Barbosa, Tatiana Bradley, Stanislaw Jarecki, Jonathan Katz and Jiayu Xu, Universally composable relaxed password authenticated key exchange, CRYPTO 2020, LNCS 12170
    locator: SPAKE2 realizes a relaxed UC PAKE functionality in the random oracle model; the variants with M = N and per-user M and N
---

SPAKE2 is a balanced [password-authenticated key exchange](/password-authenticated-key-exchange/) of Abdalla and Pointcheval (2005). It is [Diffie-Hellman](/diffie-hellman/) on an elliptic curve in which each side adds a password-dependent mask to its share: $A$ sends $p_A = wM + xP$ and $B$ sends $p_B = wN + yP$, where $w$ is a scalar derived from the password and $M$, $N$ are fixed points whose discrete logarithms nobody knows. Each side removes the other side's mask and gets $K = xyP$. The cost over plain [ECDH](/ecdh/) is small, the protocol works in any group, and it has a proof in the random oracle model. RFC 9382 (2023) specifies it, and RFC 9383 specifies the augmented variant SPAKE2+.

**Notation.** $G$ an [elliptic curve](/elliptic-curve-cryptography/) group of order $hp$ with $p$ prime and cofactor $h$, written additively, with generator $P$ of the subgroup of order $p$, and $I$ the point at infinity. $M, N$ two fixed points of order $p$ (RFC 9382, Section 6). $w = \mathrm{MHF}(pw) \bmod p$ the password scalar, where MHF is a [memory-hard function](/memory-hard-function/). $x, y$ the random scalars of $A$ and $B$. $\mathrm{len}(S)$ the length of a byte string $S$ as an 8-byte little-endian number. Hash is SHA-256, KDF is [HKDF](/hkdf/) and MAC is [HMAC](/hmac/) in the ciphersuite P256-SHA256-HKDF-HMAC used on this page.

## In plain words

Two parties share a password and want a strong shared key. They do a normal Diffie-Hellman exchange, but each one hides its public value by adding a mask that only someone who knows the password can remove. The two sides use two different public masks, one for each direction.

If both use the same password, each removes the other's mask and both get the same Diffie-Hellman secret. Then each side proves it has the key.

A party with the wrong password removes the wrong mask and gets garbage. An eavesdropper sees values that look random for every possible password, so a list of passwords does not help it. An active attacker can test one password guess per run.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/) in the balanced setting: both parties know the same password, there is no public key infrastructure, and they want a [session key](/session-key/) such that a passive attacker learns nothing that it can test offline and an active attacker can test only one password per run.

## The algorithm

```pseudo id=main
SPAKE2(w; P, M, N, h, p)          ▷ RFC 9382, Sections 3.3 and 4
L1  A: x ← random in [1, p),  X ← x·P
L2  A: pA ← w·M + X;  A → B: pA
L3  B: y ← random in [1, p),  Y ← y·P
L4  B: pB ← w·N + Y;  B → A: pB
L5  each side: abort unless the received point decodes to a point of G
L6  A: K ← h·x·(pB − w·N);  B: K ← h·y·(pA − w·M);  abort if K = I
L7  TT ← len(A)‖A ‖ len(B)‖B ‖ len(pA)‖pA ‖ len(pB)‖pB ‖ len(K)‖K ‖ len(w)‖w
L8  Ke ‖ Ka ← Hash(TT)                              ▷ two halves of the digest
L9  KcA ‖ KcB ← KDF(Ka, nil, "ConfirmationKeys" ‖ AAD, 32)
L10 cA ← MAC(KcA, TT);  cB ← MAC(KcB, TT)          ▷ A sends cA, B sends cB
L11 B: abort unless the received cA equals its own cA
L12 A: abort unless the received cB equals its own cB;  both output Ke
```

Lines L1 to L4 are a Diffie-Hellman exchange with masks. $A$ uses the point $M$ and $B$ uses $N$; using two points stops an attacker from reflecting $A$'s message back to $A$. Line L5 is the group membership check of RFC 9382, Section 7: a point that is not on the curve can leak the secret scalar. In line L6, $A$ subtracts $B$'s mask and multiplies by its secret: $p_B - wN = Y$, so $K = hxY = hxyP$. The cofactor $h$ is 1 for P-256; on curves such as Curve25519 it maps $K$ into the prime-order subgroup.

Lines L7 to L12 are the key schedule of RFC 9382, Section 4. The transcript $TT$ binds the identities, both messages, $K$ and $w$, so any change to a message changes the keys. $K$ itself is never output. $K_e$ is the session key, and $K_a$ is used only for the two confirmation tags; RFC 9382 says that each side MUST send its tag. An empty identity is encoded as a zero-length string, which is safe only if the identities are implicit in the application; otherwise an [unknown key-share attack](/unknown-key-share-attack/) is possible.

**About the code.** The Python code is for study only. It is not constant time (the scalar multiplication branches on the bits of the scalar, which RFC 9382, Section 7, forbids), and it must not protect real data. The P-256 arithmetic and HKDF are local copies; SHA-256 and HMAC come from the standard library. For the demonstration, $w$ comes from scrypt with small parameters.

## Example

The first vector of RFC 9382, Appendix B, with the identities $A$ = `server` and $B$ = `client` and no AAD. Points are SEC1 uncompressed (`04 ‖ x ‖ y`), shortened here.

| step | value (hex) |
|---|---|
| $w$ | `2ee57912 099d3156 ... 461b1a5f` |
| L1: $x$ | `43dd0fd7 215bdcb4 ... 4a78d729` |
| L2: $p_A$ | `04 a56fa807 caaa53a4 ... 8ede5f91 2c` |
| L3: $y$ | `dcb60106 f276b026 ... 5b6e66be` |
| L4: $p_B$ | `04 06557e48 2bd03097 ... b591a1e0 b7` |
| L6: $K$ | `04 12af7e89 71785067 ... 7b715d33 25` |
| L8: $K_e$ | `0e0672dc 86f8e455 65d338b0 540abe69` |
| L8: $K_a$ | `15bdf72e 2b35b5c9 e5663168 e960a91b` |
| L9: $K_{cA}$ | `00c12546 835755c8 6d8c0db7 851ae86f` |
| L9: $K_{cB}$ | `a9fa3406 c3b781b9 3d804485 430ca27a` |
| L10: $c_A$ | `58ad4aa8 8e0b60d5 ... 1fee38f0` |
| L10: $c_B$ | `d3e2e547 f1ae04f2 ... 26dc459b` |

Both sides compute the same $K$ in line L6, so the same $TT$, $K_e$ and tags. The tests check all four vectors of the appendix, including the two with an empty identity, value by value.

## Correctness

**Claim.** With the same $w$, both sides compute $K = h\,xy\,P$, the same transcript and the same keys, and both tags verify. On $A$'s side, $p_B - wN = (wN + yP) - wN = yP$, so $K = hx(yP)$; on $B$'s side, $p_A - wM = xP$, so $K = hy(xP)$; scalar multiplication commutes. Then $TT$, $K_e$, $K_a$, $K_{cA}$ and $K_{cB}$ are equal, being functions of equal inputs. With $w' \ne w$, the transcripts differ in the field $w$ (and in $K$), so the tags differ unless the hash or the MAC collides. See the [full proof](/spake2/proofs/correctness/).

**Security.** Abdalla and Pointcheval prove SPAKE2 secure in the BPR model (see [PAKE](/password-authenticated-key-exchange/)) in the [random oracle model](/random-oracle-model/) under the [computational Diffie-Hellman](/computational-diffie-hellman/) assumption; RFC 9382, Section 7, states the reduction under the gap Diffie-Hellman assumption, in which CDH is hard even with an oracle for [decisional Diffie-Hellman](/decisional-diffie-hellman/). The bound gives an active attacker about one password guess per online run. Abdalla, Barbosa, Bradley, Jarecki, Katz and Xu (2020) showed that SPAKE2 realizes a relaxed form of the [UC](/universal-composability/) PAKE functionality, in which the attacker can make its guess after the run. The proofs need that nobody knows the discrete logarithms of $M$ and $N$; RFC 9382 generates them by hashing a seed to the curve.

## Complexity

As written, each side does four scalar multiplications: $xP$, $wM$ and $wN$ (three with a fixed base) and one with a variable base in line L6. Plain [ECDH](/ecdh/) needs two. Fixed-base multiplications with precomputed tables cost much less than a variable-base one, and $x(p_B - wN)$ can be written as $x p_B - (xw)N$, so the extra cost is close to one scalar multiplication per side. A scalar multiplication by double-and-add is $O(n)$ group operations of $O(n^2)$ word operations each, so a run is $O(n^3)$, where $n \approx 256$. There are two messages for the key ($p_A$, $p_B$, one round if sent at the same time) and two tags, so four messages in total; key confirmation needs at least one more round trip. Each side keeps $O(1)$ points and scalars, $\Theta(n)$ space.

## Properties

- **Balanced.** Both sides hold $w$. A server that stores $w$ stores a password equivalent; RFC 9382, Section 7, sends applications that need an augmented PAKE to [OPAQUE](/opaque/).
- **Explicit key confirmation** through $c_A$ and $c_B$.
- **Forward secrecy.** $K_e$ depends on the fresh $x$ and $y$, so a later leak of the password does not reveal past keys to an eavesdropper.
- **One online guess per run** for an active attacker, and no offline test for a passive one, if $\log_P M$ and $\log_P N$ are unknown.
- **Works in any prime-order group** with a fixed encoding, including finite-field groups; no hashing to the curve at run time.
- **Not quantum-safe**: an attacker who can solve discrete logarithms can find $x$ and test passwords offline.

## Variants and improvements

- **SPAKE1** (same paper): one mask point, proved secure only for non-concurrent sessions.
- **M = N** (RFC 9382, Section 5): one point $M = N$ for applications in which the roles $A$ and $B$ are not fixed.
- **Per-user M and N** (RFC 9382, Section 5): points hashed from the identities, so that breaking one discrete logarithm does not break every user.
- **SPAKE2+** (Cash, Kiltz and Shoup 2008; RFC 9383, 2023): an augmented variant. The server stores $w_0$ and $L = w_1 P$ rather than $w$, and the client proves knowledge of $w_1$. The Matter smart home standard uses SPAKE2+ for device setup.
- **[CPace](/cpace/)**: a balanced PAKE that hashes the password to the generator instead of using fixed $M$ and $N$; the CFRG selected it in 2020, and SPAKE2 was not selected.

## When to use it

Use SPAKE2 when two devices share a short code or password and no public key infrastructure, for example in device pairing, and you cannot hash to the curve at run time. If you can, [CPace](/cpace/) needs no trusted setup for $M$ and $N$. When a server stores the password for many clients, use an augmented PAKE (SPAKE2+ or [OPAQUE](/opaque/)) so that a stolen database is not a password equivalent.

## Pitfalls

- **No membership check.** Line L5 must reject points that are off the curve or not in the prime-order subgroup; otherwise an invalid-curve attack can reveal $x$.
- **Swapped M and N.** If $B$ uses $M$ in line L4, the protocol still runs between two honest parties that make the same error, but the two directions are no longer separated. Use $M$ for $A$ and $N$ for $B$, as in lines L2 and L4.
- **Known logarithms of M and N.** If someone knows $m = \log_P M$ and $n_0 = \log_P N$, it can play $B$, send $p_B = y'P$ and then compute $A$'s value $K = (y' - wn_0)(p_A - wmP)$ for each guess $w$, offline. Use the published points of RFC 9382, Section 6.
- **Using K as the key.** $K$ in line L6 is not uniform and does not bind the transcript. Output $K_e$ of line L8.
- **Reused x or y.** RFC 9382 says the scalars of lines L1 and L3 MUST NOT be reused.
- **A fast hash for w.** RFC 9382, Section 3.2, says $w$ SHOULD come from an MHF such as [scrypt](/scrypt/), and reduction modulo $p$ should start from a hash 64 bits longer than $p$.
- **Skipping the tags.** Without lines L10 to L12, a party does not learn that the run failed.

## Implementations

The Python code gives `start_a` (lines L1 and L2), `start_b` (lines L3 and L4), `finish` (lines L5 to L9), `confirm` (line L10) and `run` (lines L11 and L12), with local P-256 arithmetic, point decoding with an on-curve check, and HKDF. The tests check RFC 5869, the curve, all four vectors of RFC 9382, Appendix B, agreement, a wrong password, an off-curve point, and that each password guess gives a valid point to an eavesdropper.

## History

Bellovin and Merritt's [EKE](/encrypted-key-exchange/) (1992) encrypted the Diffie-Hellman shares under the password, and its security proofs need an ideal cipher. Abdalla and Pointcheval replaced the cipher by a simple mask in a group at CT-RSA 2005: SPAKE1 and SPAKE2, proved in the random oracle model. Cash, Kiltz and Shoup gave the augmented SPAKE2+ in 2008 as an application of the twin Diffie-Hellman problem. SPAKE2 was used in a Kerberos pre-authentication mechanism and in device pairing. The CFRG did not select it in its PAKE selection of 2019 and 2020, but published RFC 9382 in 2023 because of its existing use, together with RFC 9383 for SPAKE2+.

## References
