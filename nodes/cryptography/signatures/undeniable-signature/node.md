---
tag: PHAD4A
kind: algorithm
slug: undeniable-signature
name: Undeniable signature
aliases:
- Chaum-van Antwerpen signature
- invisible signature
area: cryptography/signatures
level: research
summary: Verification needs the signer's interactive cooperation, so the signer cannot be forced to confirm.
model: word-ram
complexity:
  vars: {k: the length of the modulus p in machine words}
  time: {worst: Θ(k^3), average: Θ(k^3), best: Θ(k^3)}
  space: {extra: Θ(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [David Chaum, Hans van Antwerpen]
  note: Chaum and van Antwerpen introduced undeniable signatures at Crypto 1989. Boyar, Chaum, Damgård and Pedersen made them convertible to ordinary signatures at Crypto 1990.
prereqs: [digital-signature, diffie-hellman]
see_also: [designated-verifier-signature, zero-knowledge-proof, sigma-protocol, blind-signature, discrete-logarithm-problem, ring-signature, group-signature, signcryption]
sources:
  - paper: doi:10.1007/0-387-34805-0_20
    title: "David Chaum and Hans van Antwerpen, Undeniable signatures, Crypto 1989, LNCS 435, pages 212 to 216"
    locator: the signature s = m^x, the confirmation protocol and the disavowal protocol
  - paper: doi:10.1007/3-540-38424-3_14
    title: "Joan Boyar, David Chaum, Ivan Damgård and Torben Pedersen, Convertible undeniable signatures, Crypto 1990, LNCS 537, pages 189 to 205"
    locator: undeniable signatures that the signer can later turn into ordinary signatures, one at a time or all at once
  - paper: doi:10.1007/3-540-46877-3_41
    title: "David Chaum, Zero-knowledge undeniable signatures (extended abstract), Eurocrypt 1990, LNCS 473, pages 458 to 464"
    locator: confirmation and disavowal protocols that are zero knowledge against a dishonest verifier
  - paper: doi:10.1007/3-540-46416-6_19
    title: "Yvo Desmedt and Moti Yung, Weaknesses of undeniable signature schemes, Eurocrypt 1991, LNCS 547, pages 205 to 220"
    locator: attacks in which a verifier relays the confirmation protocol to a third party in real time
---

An undeniable signature can be checked only with the signer's help. The signer and a verifier run a confirmation protocol, after which the verifier is convinced that the signature is valid; if the signature is false, a disavowal protocol lets the signer prove that. The signer cannot deny a valid signature, because the disavowal protocol fails for it, but nobody can check the signature without the signer, so the signer controls who learns that it signed. Chaum and van Antwerpen introduced the idea at Crypto 1989, for example for software that a vendor signs only for its paying customers. In their scheme the signature on a hashed message $h$ is $s = h^a$ in a group of prime order.

## In plain words

A company signs a confidential offer to you. You cannot check the signature alone, so a leaked copy convinces nobody. To check it, you ask the company a riddle made from the signature and two random numbers that you keep secret. Only the true signer can solve the riddle, and only if the signature is real; a guess is right with chance about one in the size of the group.

If the company claims "that is not our signature", it must solve two such riddles in a special way. A real forgery lets it do this. If it lies about a real signature, its two answers do not fit together, and you see that it cheated.

## The problem

The signer has secret $a$ and public key $y = g^a$. Produce a signature $s$ on a message $m$, and two protocols between the signer and a verifier, such that:

- **unforgeability:** without $a$ nobody can make a valid signature;
- **invisibility:** without the signer's help nobody can tell a valid signature from a random group element;
- **confirmation:** a valid signature is always confirmed, and a false one is confirmed with negligible probability;
- **non-repudiation:** a false signature is always disavowed, and a valid one is disavowed with negligible probability, even if the signer cheats.

## The algorithm

$h$ is the hash of $m$ into the subgroup of order $q$. In both protocols the verifier V draws its exponents uniformly from $\mathbb{Z}_q^*$ and keeps them secret, and the signer S answers with $a^{-1}$ taken modulo $q$.

```pseudo id=main
SIGN(a, m)
L1  h ← hash of m into ⟨g⟩
L2  return s ← h^a

CONFIRM(y, m, s)
L3  V: e_1, e_2 ← random; send c ← s^{e_1} · y^{e_2}
L4  S: return d ← c^{a^{−1}}
L5  V: accept if d = h^{e_1} · g^{e_2}

DISAVOW(y, m, s)
L6  V: e_1, e_2 ← random; send c ← s^{e_1} · y^{e_2}; S: return d ← c^{a^{−1}}
L7  if d = h^{e_1} · g^{e_2}: return "valid"
L8  V: f_1, f_2 ← random; send C ← s^{f_1} · y^{f_2}; S: return D ← C^{a^{−1}}
L9  if D = h^{f_1} · g^{f_2}: return "valid"
L10 if (d · g^{−e_2})^{f_1} = (D · g^{−f_2})^{e_1}: return "forgery" else return "signer cheated"
```

The check at line L10 tests that both answers were made with the same exponent: for an honest signer and a false $s$, both sides equal $s^{e_1 f_1 / a}$.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. The signer has $a = 5$, $y = 1024$, and $a^{-1} = 204$ modulo $1019$. The message "deal" hashes to $h = 1564$, and the signature is $s = 1564^5 = 1262$.

Confirmation with $e_1 = 10$, $e_2 = 20$: V sends $c = 1262^{10} \cdot 1024^{20} = 71$; S answers $d = 71^{204} = 546$; V computes $1564^{10} \cdot 4^{20} = 546$ and accepts.

Disavowal of the false signature $s' = 1152$: with the same $e_1, e_2$, V sends $c = 427$ and S answers $d = 757 \ne 546$. With $f_1 = 30$, $f_2 = 40$, V sends $C = 1805$ and S answers $D = 857$, while $h^{30} g^{40} = 588$. Line L10 gives $(757 \cdot 4^{-20})^{30} = 869$ and $(857 \cdot 4^{-40})^{10} = 869$, so V concludes that $s'$ is a forgery.

## Correctness

For a valid $s = h^a$, $d = (h^{a e_1} g^{a e_2})^{a^{-1}} = h^{e_1} g^{e_2}$. For a false $s$, the map from $(e_1, e_2)$ to the pair (challenge, expected answer) is a bijection in the exponents, so the challenge leaves at least $q - 2$ equally likely expected answers, and any answer is right with probability at most $1/(q-2)$. In disavowal, a signer that denies a valid signature fixes, by its first wrong answer, a "message" $h_0 \ne h$, and must then pass a confirmation of $s$ for $h_0$, which is false; so it is caught except with probability at most $1/(q-2)$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Signing costs one exponentiation. Confirmation costs the verifier four exponentiations and the signer one; disavowal costs twice that and a few more. With schoolbook arithmetic modulo $p$ of $k$ words each costs $\Theta(k^3)$. The signature is one group element; on an elliptic curve with 256-bit order that is 33 bytes in compressed form. Each verification needs a round trip to the signer.

## Properties

- **Invisible.** Deciding whether $s = h^a$ from $(g, y, h, s)$ is the decisional Diffie-Hellman problem.
- **Interactive.** Every verification needs the signer online, and the signer can refuse; refusal is not a disavowal.
- **Non-transferable in the zero-knowledge version.** A transcript of a zero-knowledge confirmation proves nothing to others. The basic protocol here is not zero knowledge: a verifier that picks $c$ without knowing $e_1, e_2$ learns $c^{a^{-1}}$.
- **Unforgeable.** Making $h^a$ for a new hashed message is the computational Diffie-Hellman problem in the random oracle model.

## Variants and improvements

- **Zero-knowledge undeniable signatures** (Chaum, Eurocrypt 1990). The signer first commits to its answer, the verifier then reveals $e_1, e_2$, and the signer opens the commitment; a dishonest verifier then learns nothing.
- **Convertible undeniable signatures** (Boyar, Chaum, Damgård and Pedersen, Crypto 1990). The signer can release a value that turns one signature, or all of its signatures, into ordinary publicly verifiable ones, for example when a contract becomes public.
- **Designated confirmer signatures** (Chaum, Eurocrypt 1994). A confirmer other than the signer runs the protocols, so verification does not depend on the signer being online or honest.
- **Designated verifier proofs** (Jakobsson, Sako and Impagliazzo, Eurocrypt 1996). A non-interactive [designated verifier signature](/designated-verifier-signature/) (a signature that only one chosen verifier can trust) replaces the interactive confirmation and stops the relay attack.
- **RSA-based undeniable signatures** (Gennaro, Krawczyk and Rabin, Crypto 1997), for signers that already have RSA keys.

## When to use it

Use an undeniable signature when the signer must be bound to a statement but wants to decide who can check it: confidential offers, software licences checked only by paying customers, and documents that must not be shown to the press as signed. If any verifier should be able to check alone, use an ordinary [digital signature](/digital-signature/). If exactly one known verifier should be convinced without interaction, a designated verifier signature is simpler.

## Pitfalls

- **Relay attacks.** A verifier can pass each challenge from a third party to the signer in real time, so the third party is convinced too (Desmedt and Yung, Eurocrypt 1991). Designated verifier proofs prevent this.
- **The basic protocol is not zero knowledge.** A verifier that sends chosen values gets the signer to raise them to $a^{-1}$, which may help it later; use the zero-knowledge version.
- **Validate group elements.** Reject $s$ and $c$ outside the prime-order subgroup; otherwise answers can leak $a$ modulo small factors.
- **Refusal versus disavowal.** A signer that does not answer has not disavowed; protocols and contracts must say what refusal means.
- **Hash the message into the group.** Signing raw messages lets an attacker combine signatures, since $(m_1 m_2)^a = m_1^a m_2^a$; Desmedt and Yung also pointed out this multiplicative weakness of the first schemes.

## Implementations

The Python code is for study only: it is not constant time, its group ($p = 2039$, $q = 1019$) has no security, and the signer is a local function that the tests replace by cheating signers. It implements the basic confirmation and disavowal protocols, not the zero-knowledge version. There are no standard test vectors. The tests check that true signatures confirm, that false ones (another key, another message, random) are disavowed, and that signers that answer at random or with the wrong key are caught.

## History

Chaum and van Antwerpen introduced undeniable signatures at Crypto 1989. In 1990 Chaum made the protocols zero knowledge, and Boyar, Chaum, Damgård and Pedersen made the signatures convertible. Desmedt and Yung showed relay attacks in 1991. Chaum proposed designated confirmers in 1994, and Jakobsson, Sako and Impagliazzo proposed designated verifier proofs in 1996 as a way to give the verifier conviction without the transferability problems.

## References
