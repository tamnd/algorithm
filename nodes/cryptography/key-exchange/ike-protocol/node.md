---
tag: FRQGKN
kind: algorithm
slug: ike-protocol
name: Internet Key Exchange
aliases:
- IKE
- IKEv2
area: cryptography/key-exchange
level: advanced
summary: The key exchange of IPsec. IKEv2 runs an authenticated Diffie-Hellman exchange in two round trips, derives keys with SKEYSEED and prf+, and sets up the first IPsec security association.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the Diffie-Hellman prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1998
  people: [Dan Harkins, Dave Carrel, Charlie Kaufman, Paul Hoffman, Yoav Nir, Pasi Eronen, Tero Kivinen]
  note: IKEv1 is RFC 2409 (1998); IKEv2 is RFC 4306 (2005), revised as RFC 5996 (2010) and RFC 7296 (2014).
prereqs: [sigma-key-exchange, diffie-hellman]
see_also: [station-to-station-protocol, perfect-forward-secrecy, hmac, key-confirmation, tls-handshake, man-in-the-middle-attack, hybrid-key-exchange, noise-protocol-framework]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7296"
    title: "C. Kaufman, P. Hoffman, Y. Nir, P. Eronen and T. Kivinen, RFC 7296, Internet Key Exchange Protocol Version 2 (IKEv2), October 2014"
    locator: Section 1.2 (the initial exchanges), Section 2.6 (cookies), Section 2.13 (prf+), Section 2.14 (SKEYSEED and the SK keys), Section 2.15 (the AUTH payload), Section 2.17 (KEYMAT)
  - url: "https://www.rfc-editor.org/rfc/rfc2409"
    title: "D. Harkins and D. Carrel, RFC 2409, The Internet Key Exchange (IKE), November 1998"
    locator: Section 5 (main mode and aggressive mode) and Section 5.4 (authentication with a pre-shared key)
  - paper: "Hugo Krawczyk, SIGMA: the SIGn-and-MAc approach to authenticated Diffie-Hellman and its use in the IKE protocols, CRYPTO 2003, LNCS 2729, Springer, 2003, pages 400 to 425"
    locator: the design behind the signature modes of IKEv1 and IKEv2
  - paper: "Dennis Felsch, Martin Grothe, Jörg Schwenk, Adam Czubak and Marcin Szymanek, The dangers of key reuse: practical attacks on IPsec IKE, 27th USENIX Security Symposium, 2018"
    locator: Bleichenbacher oracles in the IKEv1 public key encryption modes, cross-protocol use of one RSA key, and offline dictionary attacks on PSK modes (pages to check)
  - url: "https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/component-testing"
    title: "NIST CAVP, SP 800-135 key derivation function test vectors (IKEv2)"
    locator: "ikev2.rsp, [SHA-256], [g^ir length = 1024], COUNT = 0"
---

The Internet Key Exchange (IKE) is the protocol that two IPsec endpoints use to authenticate each other, agree on keys and set up IPsec security associations (SAs). IKEv2 (RFC 7296) does this in two round trips. The IKE_SA_INIT exchange carries a [Diffie-Hellman](/diffie-hellman/) exchange and nonces, and from it each side derives a key seed SKEYSEED and seven keys with the function prf+. The IKE_AUTH exchange, encrypted under these keys, carries the identities and an AUTH value that signs (or MACs) one's own first message, the peer's nonce and a MAC of one's identity. This follows the [SIGMA](/sigma-key-exchange/) design. IKEv1 (RFC 2409, 1998), with its main, aggressive and quick modes, is obsolete but still in use.

**Notation.** $I$ is the initiator and $R$ the responder. $\mathrm{prf}$ is a pseudorandom function (here HMAC-SHA-256), and $|$ is concatenation. SPIi and SPIr are 8-byte SA identifiers, Ni and Nr are nonces, $\mathrm{KE}_i = g^i$ and $\mathrm{KE}_r = g^r$ are Diffie-Hellman values, and $g^{ir}$ is the shared value. SK{...} is a payload encrypted and integrity-protected with SK_e and SK_a of the sender's direction.

## In plain words

Two computers that want to protect their traffic with IPsec first run IKE. In the first round trip they make a fresh secret together with Diffie-Hellman, and each sends a random number. From the secret and the random numbers each computes the same set of keys.

In the second round trip, which is already encrypted, each says who it is and proves it, for example with a signature over the messages it sent and the other side's random number. Then both make the keys for the protected traffic.

If the responder is under attack by a flood of fake requests, it can first ask the initiator to send back a "cookie", to prove that its address is real.

## The problem

Two IPsec peers need mutually authenticated session keys with [perfect forward secrecy](/perfect-forward-secrecy/), an agreed set of algorithms, and protection against denial of service, over an untrusted network. Authentication can be by signatures, by a pre-shared key, or by EAP. This is an [authenticated key exchange](/authenticated-key-exchange/) with algorithm negotiation.

## The algorithm

The pseudocode shows IKEv2 with signature authentication and the optional cookie step. Each line names the party that acts.

```pseudo id=main
IKEV2(I, R)
L1  I → R: SPIi, SAi1, KEi, Ni [, COOKIE]            ▷ IKE_SA_INIT request
L2  R: if under load and COOKIE invalid then reply N(COOKIE) and keep no state
L3  R → I: SPIi, SPIr, SAr1, KEr, Nr                  ▷ IKE_SA_INIT response
L4  both: SKEYSEED ← prf(Ni | Nr, g^ir)
L5  both: SK_d | SK_ai | SK_ar | SK_ei | SK_er | SK_pi | SK_pr ← prf+(SKEYSEED, Ni | Nr | SPIi | SPIr)
L6  I → R: SK{IDi, AUTHi}, AUTHi = SIG_I(message 1 | Nr | prf(SK_pi, IDi))
L7  R: check AUTHi with IDi's key; R → I: SK{IDr, AUTHr}, AUTHr = SIG_R(message 2 | Ni | prf(SK_pr, IDr))
L8  I: check AUTHr with IDr's key
L9  both: KEYMAT ← prf+(SK_d, Ni | Nr)                 ▷ keys of the first child SA
```

At line L1, SAi1 lists the proposals (cipher, PRF, integrity and Diffie-Hellman group), and KEi is for the group that the initiator guesses the responder will choose. Line L2 is the cookie mechanism of Section 2.6: the responder answers with $\mathrm{COOKIE} = \mathrm{Hash}(\mathrm{Ni} \mid \mathrm{IP_i} \mid \mathrm{SPIi} \mid \mathit{secret})$ and stores nothing; only an initiator that receives packets at its source address can repeat message 1 with the cookie. Line L3 picks one proposal.

Line L5 is prf+ of Section 2.13: $T_1 = \mathrm{prf}(K, S \mid \texttt{0x01})$, $T_n = \mathrm{prf}(K, T_{n-1} \mid S \mid n)$, and the output is $T_1 \mid T_2 \mid \dots$. SK_d is for child SAs, SK_a and SK_e protect the IKE messages in each direction, and SK_p are for the AUTH values. At lines L6 and L7, each party signs its own first message (which contains its KE and nonce), the peer's nonce, and a MAC of its own identity under the new key. This binds the identity to the session as in SIGMA, and gives key confirmation. Line L9 gives the IPsec keys; later child SAs come from CREATE_CHILD_SA exchanges, optionally with a new Diffie-Hellman exchange.

**About the code.** The Python code implements prf, prf+ and SKEYSEED exactly as RFC 7296, and checks them against the NIST CAVP SP 800-135 IKEv2 vector. The rest is a simplified model of IKEv2, not the wire protocol: one fixed proposal, length-prefixed messages, no traffic selectors, a toy Schnorr signature, a toy encrypt-then-MAC for SK{...}, and a 256-bit safe-prime group. It is for study only. It is not constant time, and it must not protect real data. Use strongSwan or libreswan.

## Example

The CAVP vector (SHA-256, a 1024-bit $g^{ir}$) shows lines L4 and L5. The inputs are Ni = `ed80dc79912c32a9`, Nr = `35fb6d1a3feac078`, SPIi = `47c1858efc932ea4`, SPIr = `606fd05609624002`, and a 128-byte $g^{ir}$ that starts with `42968e5d`.

| step | value |
|---|---|
| L4 key of the PRF | Ni \| Nr = `ed80dc79912c32a935fb6d1a3feac078` |
| L4 SKEYSEED | `37fde90b81d63692620f67367b62092e3efdc6a03509137d731004767ff35010` |
| L5 seed | Ni \| Nr \| SPIi \| SPIr, 32 bytes |
| L5 $T_1$, the first 32 bytes | `63d018a08f7a29daa7d1f92cb63f45fa39bbaf5e5f1a78139613bb891e3e6bf9` |
| L5 output | 132 bytes, $T_1 \mid \dots \mid T_5$ cut to length |

With 32-byte keys, $T_1$ would be SK_d, and so on in the order of line L5.

## Correctness

Both parties compute the same $g^{ir}$ by the Diffie-Hellman identity, and lines L4, L5 and L9 apply deterministic functions to values that both hold, so the keys are equal. Each AUTH is computed over byte strings that the verifier also holds, so honest checks pass. The proof is below.

Security rests on the SIGMA argument: each party signs its own ephemeral value and the peer's nonce, which gives authentication and freshness, and the MAC under SK_p of its own identity binds the identity to the keys. Canetti and Krawczyk analysed the basis of the signature mode. Formal analyses of the full protocol have found weaknesses in some modes (for example in IKEv1 and in combinations of authentication methods), and the attacks below come from such details, not from the core exchange.

## Complexity

Each side does one exponentiation for its KE value and one for $g^{ir}$, plus one signature and one verification: $\Theta(m^3)$ bit operations with schoolbook arithmetic, and $\Theta(m)$ space. The exchange needs two round trips, or three with a cookie. prf+ costs one HMAC per 32 bytes of keys.

## Properties

- **Mutual authentication** by signatures, a pre-shared key, or EAP for the initiator.
- **Forward secrecy** from the ephemeral Diffie-Hellman exchange, and for child SAs if each CREATE_CHILD_SA includes a new exchange.
- **Identity protection** for the initiator against passive attackers: the identities are sent under SK{...}.
- **Denial-of-service resistance** with stateless cookies: at line L2 the responder keeps no state and does no exponentiation for an initiator that has not returned a valid cookie.
- **Algorithm negotiation** in the SA payloads.

## Variants and improvements

- **IKEv1 main mode.** Six messages: SA negotiation, Diffie-Hellman with nonces, then identities and authentication under encryption. It has four authentication methods (signatures, public key encryption, revised public key encryption, pre-shared key).
- **IKEv1 aggressive mode.** Three messages with no identity protection.
- **IKEv1 quick mode.** Makes IPsec SAs under the protection of the phase 1 SA.
- **IKEv2 with EAP.** The initiator authenticates through an EAP method, the responder with a certificate.
- **Post-quantum additions.** RFC 8784 mixes a post-quantum pre-shared key into SK_d and SK_p, and RFC 9370 adds further key exchanges (for example ML-KEM) in IKE_INTERMEDIATE messages, which gives a [hybrid key exchange](/hybrid-key-exchange/).

## When to use it

Use IKEv2 to set up IPsec tunnels and transport mode, for site-to-site VPNs and remote access. Do not use IKEv1 for new systems. For key exchange outside IPsec, TLS 1.3 or the [Noise framework](/noise-protocol-framework/) are simpler.

## Pitfalls

- **Weak pre-shared keys.** In IKEv1 aggressive mode with a pre-shared key, $\mathrm{SKEYID} = \mathrm{prf}(\mathrm{PSK}, \mathrm{Ni} \mid \mathrm{Nr})$ and the responder's HASH_R in message 2 depend only on the PSK and values sent in clear, so a passive eavesdropper can test guesses of the PSK offline. Felsch et al. (2018) showed that an active attacker can do offline guessing against PSK main mode and IKEv2 as well. In the model this corresponds to replacing the signatures of lines L6 and L7 with a MAC under a low-entropy key. Use long random PSKs, or certificates.
- **Key reuse across modes.** Felsch et al. used Bleichenbacher oracles in the IKEv1 public key encryption modes to forge signatures with the same RSA key, which broke IKEv1 and IKEv2 signature authentication in several products. Do not share one RSA key between IKEv1 encryption modes and signature modes.
- **Unchecked KE values.** Without the group check of the received KE (done before line L4 in the code), small-subgroup values can leak bits of a reused private exponent; see [small subgroup attack](/small-subgroup-attack/).
- **Work before the cookie check.** Line L2 helps only if the responder checks the cookie before it makes state or computes anything with KEi. Cookies prove only that the initiator can receive at its address; they do not stop a flood from many real addresses.
- **AUTH over the wrong message.** The AUTH value must cover the message 1 or message 2 exactly as sent (with the cookie, if any). Signing a parsed or changed copy breaks interoperability or lets an attacker change fields at lines L1 and L3.

## Implementations

## History

IKE grew out of Oakley (Orman, RFC 2412) and the SKEME protocol of Krawczyk, inside the ISAKMP framework (RFC 2408). Harkins and Carrel published IKEv1 as RFC 2409 in 1998; its complexity drew criticism, including from Ferguson and Schneier. IKEv2 (RFC 4306, Kaufman, 2005) simplified the exchanges to four messages, based on the SIGMA design that Krawczyk described in 2003. It was revised as RFC 5996 in 2010 and as RFC 7296 (Internet Standard 79) in 2014. Felsch et al. presented their cross-mode and dictionary attacks at USENIX Security 2018. RFC 9370 (2023) added multiple key exchanges for post-quantum security.

## References
