---
tag: 0KTA6M
kind: concept
slug: key-compromise-impersonation
name: Key compromise impersonation
aliases:
- KCI
area: cryptography/key-exchange
level: advanced
summary: In a KCI attack, an adversary who has stolen the long-term key of one party uses it to impersonate other parties to that party. A KCI-resistant protocol prevents this.
prereqs: [authenticated-key-exchange]
see_also: [unknown-key-share-attack, perfect-forward-secrecy, mqv, hmqv, sigma-key-exchange, diffie-hellman, digital-signature, tls-handshake]
sources:
  - paper: "Antoine Just and Serge Vaudenay, Authenticated multi-party key agreement, ASIACRYPT 1996, LNCS 1163, Springer, 1996, pages 36 to 49"
    locator: the attack in which a compromised long-term key is used to impersonate other parties to its owner (locator to check)
  - paper: "Simon Blake-Wilson, Don Johnson and Alfred Menezes, Key agreement protocols and their security analysis, Cryptography and Coding 1997, LNCS 1355, Springer, 1997, pages 30 to 45"
    locator: the list of desirable attributes of key agreement protocols, which includes resistance to key-compromise impersonation (locator to check)
  - paper: "Hugo Krawczyk, HMQV: a high-performance secure Diffie-Hellman protocol, CRYPTO 2005, LNCS 3621, Springer, 2005, pages 546 to 566"
    locator: the formal definition of KCI resistance in the Canetti-Krawczyk model and the proof for HMQV; full version IACR ePrint 2005/176
  - paper: "Clemens Hlauschek, Markus Gruber, Florian Fankhauser and Christian Schanes, Prying open Pandora's box: KCI attacks against TLS, USENIX Workshop on Offensive Technologies (WOOT) 2015"
    locator: KCI against TLS client authentication with static (EC)DH certificates
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.6 (key agreement based on asymmetric techniques, including static Diffie-Hellman and MTI protocols)
---

A key compromise impersonation (KCI) attack is an attack in which an adversary who has learned the long-term secret key of a party $\hat A$ uses it to make $\hat A$ accept a session with *another* party $\hat B$, while the adversary, not $\hat B$, holds the session key. Losing your own key obviously lets others impersonate *you*; a protocol is KCI resistant when it does not also let them impersonate everyone else *to you*. Just and Vaudenay (1996) described the attack, and Blake-Wilson, Johnson and Menezes (1997) listed resistance to it among the desirable attributes of a key agreement protocol.

**Notation.** $G = \langle g \rangle$ has prime order $q$. $\hat A$ has long-term key pair $(a, A = g^a)$, $\hat B$ has $(b, B = g^b)$, and the ephemeral values are $X = g^x$ and $Y = g^y$. $\mathcal{E}$ is the adversary, and $H$ a hash function.

## In plain words

Suppose a thief steals the key to your house. Of course the thief can now enter your house. But should the stolen key also let the thief put on a uniform and convince you that he is your bank?

In some key exchange protocols it does. The secret that proves "this is Bob" to Alice is something that Alice can compute herself, because Alice and Bob compute the same value from their own keys. So whoever holds Alice's key can also produce Bob's proof, and talk to Alice in Bob's name.

A protocol that resists this needs Bob to prove something that only Bob's key can produce, such as a signature, or a value that mixes Bob's key with fresh secrets in a way Alice's key alone cannot repeat.

## The idea

### Why some protocols fail

Take any protocol in which the authenticating value is symmetric between the two parties:

- **Shared symmetric keys.** If $\hat A$ and $\hat B$ authenticate with a shared long-term key $K_{AB}$, knowing $K_{AB}$ *is* being $\hat B$ to $\hat A$. KCI resistance is impossible for such protocols, so the property is studied for public key protocols.
- **Static-static Diffie-Hellman.** If the session key is $K = H(g^{ab}, X, Y)$, then $\hat A$ computes $g^{ab} = B^a$ and $\hat B$ computes $A^b$. With $a$, $\mathcal{E}$ computes $B^a$ as well, answers $\hat A$'s $X$ with her own $Y$, and knows $K$. The fresh $X$ and $Y$ only make $K$ fresh; they do not authenticate.

The flaw also hit real deployments: Hlauschek et al. (2015) showed KCI against TLS clients that authenticate with fixed (EC)DH client certificates, where the client's static key enters the key exchange directly. An attacker who installs or steals the client certificate key can impersonate any server to that client.

### How protocols resist it

$\mathcal{E}$ has $a$, so she can compute anything $\hat A$ can compute. She must still produce a message that $\hat A$ accepts as coming from $\hat B$, or a key formula with a factor that needs $b$ or a secret ephemeral of $\hat A$ together.

- **Signatures from the peer.** In signed Diffie-Hellman, [STS](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/) and the TLS 1.3 CertificateVerify, $\hat B$ signs the ephemeral values with $b$. The key $a$ does not help to forge that signature.
- **Mixing ephemeral and static values.** In [MQV](/mqv/), $\hat A$ computes $\sigma = (Y B^e)^{x + d a}$. Expanded, this is $Y^x \cdot Y^{da} \cdot B^{ex} \cdot B^{eda}$. With $a$ and her own $y$, $\mathcal{E}$ computes $Y^x = X^y$, $Y^{da}$ and $B^{eda}$, but $B^{ex} = g^{bxe}$ is a Diffie-Hellman value of $B$ and $X$, which needs $b$ or $x$. [HMQV](/hmqv/) has the same structure, and Krawczyk (2005) proves its KCI resistance in the Canetti-Krawczyk model with the random oracle.

KCI resistance is defined in the game-based models of [authenticated key exchange](/authenticated-key-exchange/) by allowing the adversary to corrupt the *owner* of the Test session before or during it, as long as the peer is uncorrupted. The eCK model includes this case directly: it permits the reveal of the long-term key of the owner of the Test session.

### Relation to other properties

- [Forward secrecy](/perfect-forward-secrecy/) is about corruption *after* a session; KCI is about corruption *before* it. A protocol can have one and not the other: static-static DH with ephemeral nonces has neither, and plain ephemeral DH with signatures has both.
- The [unknown key-share attack](/unknown-key-share-attack/) is a different failure: there no key is stolen, but one party is wrong about who shares the key.
- Using $a$ to impersonate $\hat A$ to a third party is not KCI. That is plain impersonation of the corrupted party, and no protocol can stop it.

## Examples

**Static-static DH, toy numbers.** In the group of order 1019 in $\mathbb{Z}_{2039}^*$ with $g = 4$, let $a = 57$ and $b = 311$, so $A = 1556$ and $B = 1502$. The static secret is $g^{ab} = 661$. Eve steals $a = 57$ and computes $B^{57} \bmod 2039 = 661$. She can now answer any session that Alice starts with "Bob", with the key $H(661, X, Y)$, where she chose $Y$.

**The code.** The Python code on this page runs three protocols with Alice's key stolen:

- static-static DH, where Eve's key equals Alice's key in every run;
- signed ephemeral DH, where Eve can only sign with Alice's key, and Alice rejects;
- MQV, where honest parties agree but Eve's direct computation, which lacks the factor $B^{ex}$, gives a different key.

The MQV test shows only that one direct attempt fails; it is not a proof of KCI resistance. The code is for study only. It uses a 256-bit toy group, it is not constant time, it runs the attacks only against local simulated parties, and it must not protect real data. Use a vetted library such as libsodium, or a FIPS 140 validated module.

## Where it is used

- Design criteria for key agreement in the standards that include MQV (IEEE 1363, ANSI X9.63, NIST SP 800-56A) and in the analysis of [HMQV](/hmqv/).
- The eCK model and its successors make KCI resistance part of the definition of security.
- [TLS 1.3](/tls-handshake/) removed static (EC)DH key exchange, which also removed the fixed-DH client certificates that caused the TLS KCI attacks.
- Protocols built from the [Noise framework](/noise-protocol-framework/) state their KCI resistance for each pattern in the specification's tables of security properties.

## References
