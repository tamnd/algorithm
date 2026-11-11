---
tag: BECMKR
kind: concept
slug: unknown-key-share-attack
name: Unknown key-share attack
aliases:
- UKS attack
area: cryptography/key-exchange
level: advanced
summary: In an unknown key-share attack, two honest parties end with the same key, but one of them believes it shares the key with a third party. The attacker need not learn the key.
prereqs: [authenticated-key-exchange]
see_also: [key-compromise-impersonation, man-in-the-middle-attack, station-to-station-protocol, sigma-key-exchange, mqv, key-confirmation, tls-handshake, digital-signature]
sources:
  - paper: "Whitfield Diffie, Paul C. van Oorschot and Michael J. Wiener, Authentication and authenticated key exchanges, Designs, Codes and Cryptography 2(2), 1992, pages 107 to 125"
    locator: the first description of the attack, in the discussion of the station-to-station protocol (section to check)
  - paper: "Simon Blake-Wilson and Alfred Menezes, Unknown key-share attacks on the station-to-station (STS) protocol, PKC 1999, LNCS 1560, Springer, 1999, pages 154 to 170"
    locator: the public key substitution attack on STS when the CA does not check possession of the private key, and the fixes
  - paper: "Burton S. Kaliski Jr., An unknown key-share attack on the MQV key agreement protocol, ACM Transactions on Information and System Security 4(3), 2001, pages 275 to 288"
    locator: the attack with an on-line registered key that depends on the victim's ephemeral value
  - paper: "Hugo Krawczyk, SIGMA: the SIGn-and-MAc approach to authenticated Diffie-Hellman and its use in the IKE protocols, CRYPTO 2003, LNCS 2729, Springer, 2003, pages 400 to 425"
    locator: Section 2 and Section 3 (the identity misbinding attack on sign-only DH, and the MAC over the sender's identity)
  - paper: "Karthikeyan Bhargavan, Antoine Delignat-Lavaud, Cédric Fournet, Alfredo Pironti and Pierre-Yves Strub, Triple handshakes and cookie cutters: breaking and fixing authentication over TLS, IEEE Symposium on Security and Privacy 2014"
    locator: the synchronized session attack on TLS 1.2 resumption and renegotiation, fixed by the extended master secret of RFC 7627
---

An unknown key-share (UKS) attack is an attack on a key exchange in which two honest parties $\hat A$ and $\hat B$ end with the same session key, but at least one of them has a wrong view of who the peer is: $\hat A$ believes it shares the key with $\hat B$, while $\hat B$ believes it shares the key with a third party $\hat E$. The attacker usually does not learn the key. The harm is the misbinding: $\hat B$ credits $\hat E$ with what $\hat A$ says. Diffie, van Oorschot and Wiener described the attack in 1992, Blake-Wilson and Menezes (1999) gave UKS attacks on the station-to-station protocol, and Krawczyk (2003) calls the same failure an identity misbinding attack.

**Notation.** $X = g^x$ and $Y = g^y$ are ephemeral Diffie-Hellman values, $\mathrm{SIG}_P(m)$ a signature by party $P$, $\mathrm{MAC}_{K_m}(m)$ a MAC under a key $K_m$ derived from $g^{xy}$, and $\hat E$ the attacker, who is also a registered user.

## In plain words

Alice sends a sealed deposit slip to her bank. A crook takes the slip on the way, changes only the name on the outside envelope to his own name, and passes it on. The bank opens the envelope with no trouble, because the seal is real. The bank then credits the money to the crook.

The crook never read the slip. He did not need to. He only made the bank wrong about who sent it.

An unknown key-share attack does the same to a key exchange. The two honest sides share a good key, but one of them has the wrong name attached to it. The fix is to tie the names into what is signed, what is checked, or how the key is made, so that a changed name breaks the exchange.

## The idea

### The attack on sign-only Diffie-Hellman

Consider a signed Diffie-Hellman exchange where the signatures do not name the peer:

$$A \to B: X, \qquad B \to A: \hat B, Y, \mathrm{SIG}_B(Y, X), \qquad A \to B: \hat A, \mathrm{SIG}_A(X, Y),$$

with $K = H(g^{xy})$. The attacker $\hat E$ lets the first two messages pass. In the third, it replaces the name $\hat A$ by $\hat E$ and forwards $\mathrm{SIG}_A(X, Y)$. If $\hat B$ accepts $\mathrm{SIG}_A$ as a signature of $\hat E$, then $\hat B$ accepts with peer $\hat E$, and $\hat A$ accepts with peer $\hat B$. Two ways make $\hat B$ accept:

- **Public key substitution.** $\hat E$ registers $\hat A$'s public key under its own name at a CA that does not check that $\hat E$ knows the private key. Then $\mathrm{SIG}_A$ verifies under $\hat E$'s certificate. Blake-Wilson and Menezes (1999) applied this to [STS](/station-to-station-protocol/): STS encrypts the signatures under the new key, but the certificates travel in the clear, so $\hat E$ can still swap them.
- **Signature key substitution.** With some signature schemes, given a signature by $\hat A$, an attacker can make a *new* key pair under which the same signature verifies on the same message. This works even if the CA checks possession of the new key.

### The attack on MQV

Kaliski (2001) gave a UKS attack on [MQV](/mqv/). The attacker intercepts $\hat A$'s ephemeral $X$, makes a fresh static key pair whose public key is computed from $X$, registers it on line, and sends a related value to $\hat B$ in its own name. The MQV values work out so that $\hat B$'s key with $\hat E$ equals $\hat A$'s key with $\hat B$. The attack needs registration during the run. The fix that the standards adopted is to put the identities of both parties into the key derivation, and optionally to add [key confirmation](/key-confirmation/) that covers the identities.

### Fixes

1. **Proof of possession at registration.** The CA asks the applicant to sign a challenge with the private key. This stops plain public key substitution, but not attacks that create a fresh key pair, such as Kaliski's or signature key substitution.
2. **Identities in the key derivation.** With $K = H(g^{xy}, \hat A, \hat B)$, the two parties derive different keys when they disagree about the names, so the session fails instead of giving a silent misbinding.
3. **Identities in the authentication.** The sender authenticates its own identity under a key bound to the session. [SIGMA](/sigma-key-exchange/) sends $\mathrm{MAC}_{K_m}(\hat A)$ together with $\mathrm{SIG}_A(X, Y)$. $\hat E$ can relabel the message, but it cannot make a MAC over "$\hat E$" without $K_m$. Signing the peer's identity, as in ISO 9798-3, gives the same protection with a different structure.

Fixes 2 and 3 do not depend on the CA. The tests check all three.

### UKS in TLS

The triple handshake attack of Bhargavan et al. (2014) is a UKS on TLS 1.2: a malicious server $\hat E$ runs one handshake with client $\hat A$ and one with server $\hat B$ and makes both end with the same master secret and session id. A later resumption gives two connections with identical keys and Finished values, and renegotiation then binds $\hat A$'s client certificate to a connection that $\hat E$ controls. The fix, the extended master secret of RFC 7627, derives the master secret from a hash of the whole handshake, which is fix 2 applied to the transcript. TLS 1.3 has this binding by design.

## Examples

**The bank example.** This is the standard illustration of the harm. Alice runs a key exchange with her bank. Eve mounts the UKS. Alice sends "deposit this check" encrypted under the session key. The bank decrypts it correctly, but it believes the session is with Eve, so it credits Eve's account.

**The code.** The Python code on this page runs the sign-only exchange above with Schnorr signatures in a 256-bit toy group. The tests show that:

- an honest run gives both parties the same key with the correct peers;
- Eve registers Alice's public key as "E" and changes the name in the last message, and Bob accepts a session "with E" whose key equals Alice's key "with Bob";
- with proof of possession at the CA, Eve cannot register the key;
- with the names in the key derivation, the keys differ;
- with a SIGMA-style MAC over the sender's own identity, Bob rejects.

The code is for study only. It is not constant time, it runs the attack only against local simulated parties, and it must not protect real data. Use a vetted library such as libsodium or a FIPS 140 validated module.

## Where it is used

- The design of [SIGMA](/sigma-key-exchange/) and so of the IKEv2 signature mode, which includes the identity in the MAC.
- NIST SP 800-56A, which puts the identities of both parties into the OtherInfo of the key derivation and into the key confirmation MacData.
- The proofs of [HMQV](/hmqv/), where the identities enter the values $d$ and $e$.
- RFC 7627 (extended master secret) for TLS 1.2, and the transcript-based key schedule of [TLS 1.3](/tls-handshake/).

## References
