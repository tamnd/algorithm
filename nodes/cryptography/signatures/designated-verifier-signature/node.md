---
tag: FAQZXV
kind: algorithm
slug: designated-verifier-signature
name: Designated verifier signature
aliases:
- DVS
- designated verifier proof
area: cryptography/signatures
level: research
summary: Only a chosen verifier can be convinced, and the verifier cannot prove the signature to others.
model: word-ram
complexity:
  vars: {k: the length of the modulus p in machine words}
  time: {worst: Θ(k^3), average: Θ(k^3), best: Θ(k^3)}
  space: {extra: Θ(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1996
  people: [Markus Jakobsson, Kazue Sako, Russell Impagliazzo]
  note: Jakobsson, Sako and Impagliazzo introduced designated verifier proofs and signatures at Eurocrypt 1996, as a simpler replacement for the interactive verification of undeniable signatures.
prereqs: [schnorr-signature, sigma-protocol]
see_also: [ring-signature, undeniable-signature, signcryption, zero-knowledge-proof, fiat-shamir-heuristic, message-authentication-code, signal-protocol, diffie-hellman]
sources:
  - paper: doi:10.1007/3-540-68339-9_13
    title: "Markus Jakobsson, Kazue Sako and Russell Impagliazzo, Designated verifier proofs and their applications, Eurocrypt 1996, LNCS 1070, pages 143 to 154"
    locator: the definition of designated verifier proofs, the proof "the statement is true or I know the verifier's secret key", and strong designated verifier proofs
  - paper: doi:10.1007/978-3-540-24691-6_4
    title: "Shahrokh Saeednia, Steve Kremer and Olivier Markowitch, An efficient strong designated verifier signature scheme, ICISC 2003, LNCS 2971, pages 40 to 54"
    locator: a strong DVS from Schnorr and Zheng signcryption in which verification needs the verifier's secret key
  - paper: doi:10.1007/978-3-540-40061-5_33
    title: "Ron Steinfeld, Laurence Bull, Huaxiong Wang and Josef Pieprzyk, Universal designated-verifier signatures, Asiacrypt 2003, LNCS 2894, pages 523 to 542"
    locator: the definition of universal DVS, where any holder of an ordinary signature can make a DVS for a verifier of its choice
---

A designated verifier signature convinces one chosen verifier, and only that verifier, that the signer signed a message. The verifier can make signatures that look exactly the same with its own secret key, so a signature proves nothing to a third party: it came from the signer or from the verifier, and nobody else can tell which. Jakobsson, Sako and Impagliazzo introduced the idea at Eurocrypt 1996. The construction here is a non-interactive proof of the statement "I know the signer's secret key or I know the verifier's secret key", made with the OR technique for Schnorr proofs.

## In plain words

Alice wants to send Bob a signed offer that Bob can trust, but that Bob cannot show to a competitor as proof of what Alice offered. Alice signs with a proof that says "this comes from Alice or from Bob". Bob knows he did not write it, so it must be from Alice. A competitor knows that Bob could have written it himself, since Bob holds one of the two keys, so the signature is worth nothing to the competitor. It works like a message authentication code, where both parties share the key, except that the parties need only each other's public keys.

## The problem

The signer has the key pair $(x_s, y_s = g^{x_s})$ and the designated verifier has $(x_v, y_v = g^{x_v})$ in a group of prime order $q$. Make a signature $\sigma$ on a message $m$ such that:

- **correctness:** the verifier accepts $\sigma$ with the public keys $y_s, y_v$;
- **unforgeability:** nobody without $x_s$ or $x_v$ can make a valid $\sigma$ on a new message, so the verifier, who did not make it, is convinced;
- **non-transferability:** with $x_v$ the verifier can simulate valid signatures that are indistinguishable from real ones, so $\sigma$ convinces no one else.

A **strong** DVS adds that a third party cannot even check that $\sigma$ is valid without $x_v$. This hides whether the signer, or anyone at all, sent a signature to $v$.

## The algorithm

$H$ hashes $(y_s, y_v, m, t_s, t_v)$ into $\mathbb{Z}_q$. The signature is a Fiat-Shamir proof with one Schnorr branch per key. The signer answers its own branch and simulates the verifier's branch; the verifier's simulator does the opposite.

```pseudo id=main
SIGN(x_s, y_v, m)
L1  k, c_v, z_v ← random in Z_q
L2  t_s ← g^k; t_v ← g^{z_v} · y_v^{c_v}                ▷ the verifier's branch is simulated
L3  c ← H(y_s, y_v, m, t_s, t_v)
L4  c_s ← c − c_v mod q; z_s ← k − c_s · x_s mod q
L5  return σ = (c_s, c_v, z_s, z_v)

VERIFY(y_s, y_v, m, σ)
L6  t_s ← g^{z_s} · y_s^{c_s}; t_v ← g^{z_v} · y_v^{c_v}
L7  return c_s + c_v ≡ H(y_s, y_v, m, t_s, t_v) (mod q)

SIMULATE(y_s, x_v, m)                                   ▷ run by the verifier
L8  k, c_s, z_s ← random in Z_q; t_s ← g^{z_s} · y_s^{c_s}; t_v ← g^k
L9  c_v ← H(y_s, y_v, m, t_s, t_v) − c_s mod q; return (c_s, c_v, z_s, k − c_v · x_v mod q)
```

The trick is the [sigma protocol](/sigma-protocol/) (a three-move proof of knowledge: commit, challenge, respond) OR composition of Cramer, Damgård and Schoenmakers (Crypto 1994). The prover may choose one of the two challenges freely, but the two must add up to the hash, so it can answer only if it knows at least one of the two secret keys. The [ring signature](/ring-signature/) of a two-key ring $\{y_s, y_v\}$ gives the same guarantee.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. The signer has $x_s = 5$, $y_s = 1024$, and the verifier has $x_v = 17$, $y_v = 1458$. The signer signs $m$ = "deal" with $k = 77$, $c_v = 200$, $z_v = 300$.

| line | computation | result |
|---|---|---|
| L2 | $t_s = 4^{77}$; $t_v = 4^{300} \cdot 1458^{200}$ | $360$; $737$ |
| L3 | $c = H(1024, 1458, \text{deal}, 360, 737)$ | $741$ |
| L4 | $c_s = 741 - 200$; $z_s = 77 - 541 \cdot 5 \bmod 1019$ | $541$; $429$ |

The signature is $(541, 200, 429, 300)$, and the verifier recomputes $t_s = 360$ and $t_v = 737$. The verifier's simulator with coins $k' = 300 + 200 \cdot 17 \bmod 1019 = 643$, $c_s = 541$, $z_s = 429$ outputs the same four numbers without using $x_s$.

## Correctness

Line L4 makes $g^{z_s} y_s^{c_s} = g^{k}$, so the verifier hashes the same tuple and gets $c = c_s + c_v$. For non-transferability, each valid signature comes from exactly one choice of signer coins, $(z_s + c_s x_s, c_v, z_v)$, and from exactly one choice of simulator coins, $(z_v + c_v x_v, c_s, z_s)$. So real and simulated signatures have the same distribution, not only close ones. Unforgeability by third parties follows, in the random oracle model, from the special soundness of the OR proof and the forking lemma. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Signing takes three exponentiations and one hash, and verifying takes four exponentiations and one hash, so with schoolbook arithmetic modulo $p$ of $k$ words each costs $\Theta(k^3)$. The signature has four elements of $\mathbb{Z}_q$; one can drop one of them by sending the hash value instead. A Schnorr signature has two elements, so the price of deniability is two more.

## Properties

- **Non-transferable.** The verifier's simulation is perfect, so a third party learns only "the signer or the verifier".
- **Not strong.** Anyone who sees $\sigma$ and knows $y_s$ and $y_v$ can check it, so the scheme does not hide that one of the two signed. A strong DVS hides that too.
- **Publicly checkable keys.** The scheme needs only ordinary discrete-logarithm key pairs and no shared secret, unlike a [message authentication code](/message-authentication-code/) (a tag made and checked with one shared key).
- **Bound to the verifier.** The verifier's key is hashed, so the signature is not valid for another verifier.

## Variants and improvements

- **Jakobsson, Sako and Impagliazzo (1996).** Their designated verifier proof shows that a Chaum [undeniable signature](/undeniable-signature/) $m^{x_s}$ is valid, or that the prover knows $x_v$, using a trapdoor commitment of the verifier. This replaces the interactive confirmation protocol of undeniable signatures. They also defined strong designated verifier proofs, which encrypt part of the proof to the verifier.
- **Strong DVS** (Saeednia, Kremer and Markowitch, ICISC 2003). The verifier computes a Diffie-Hellman value from $x_v$ and the signer's data, as in Zheng's [signcryption](/signcryption/), so only the verifier can check the signature.
- **Universal DVS** (Steinfeld, Bull, Wang and Pieprzyk, Asiacrypt 2003). The holder of an ordinary signature, not only the signer, can turn it into a DVS for a verifier of its choice, for example to show a certificate without letting the verifier pass it on.
- **Non-delegatability** (Lipmaa, Wang and Bao, ICALP 2005). Some schemes let the signer hand out a value that lets others sign for it without its secret key; a non-delegatable DVS proves knowledge of $x_s$ or $x_v$ itself, as the OR proof here does.
- **Multi-designated verifiers.** A signature that any of several chosen verifiers accepts, built like a larger ring.

## When to use it

Use a DVS when the receiver must trust the sender but the sender must stay deniable towards everyone else: offers in negotiations, receipts in electronic voting that must not let a voter prove its vote, and software licences checked by one customer. If both parties already share a key, a MAC gives the same deniability more cheaply; deniable key exchange in messaging (Off-the-Record, and the [Signal protocol](/signal-protocol/)) follows that route. If the signature must convince a court later, use an ordinary signature.

## Pitfalls

- **The verifier's key must be real.** If the "verifier" key was made by someone who does not know $x_v$, for example a hash output, nobody can simulate, and the signature becomes an ordinary transferable signature. A third party is convinced only if it is sure the verifier knows $x_v$, for example through a proof of possession when the key is registered.
- **Not strong.** In this form a third party sees that $s$ or $v$ signed, which already leaks the relation between them. Use a strong DVS if that matters.
- **Delegation.** Some proposed schemes are delegatable; check that the security proof covers non-delegatability if the application needs it.
- **Bad randomness.** Reuse of $k$ for two messages reveals $x_s$, as in Schnorr signatures.

## Implementations

The Python code is for study only: it is not constant time, and its group ($p = 2039$, $q = 1019$) has no security. It implements the two-key OR-proof form, not the undeniable-signature form of Jakobsson, Sako and Impagliazzo; there are no standard test vectors. The tests check correctness, rejection with another verifier key, and the two coin bijections that show the verifier's simulation is perfect.

## History

Chaum and van Antwerpen's undeniable signatures (1989) let the signer control who is convinced, but needed interaction for every verification and could be misused: a verifier could relay the protocol live to a third party. Jakobsson, Sako and Impagliazzo answered this at Eurocrypt 1996 with designated verifier proofs, which are non-interactive and convince only the designated verifier. Strong and universal DVS followed in 2003, and Lipmaa, Wang and Bao defined non-delegatability in 2005.

## References
