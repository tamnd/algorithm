---
tag: 6JAF6Z
kind: algorithm
slug: ring-signature
name: Ring signature
aliases:
- AOS ring signature
- 1-out-of-n signature
area: cryptography/signatures
level: advanced
summary: Signer hides its identity within a ring of public keys while anyone can verify the ring signed.
model: word-ram
complexity:
  vars: {n: the number of public keys in the ring}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2001
  people: [Ronald L. Rivest, Adi Shamir, Yael Tauman]
  note: Rivest, Shamir and Tauman defined ring signatures in "How to leak a secret" (Asiacrypt 2001). Abe, Ohkubo and Suzuki gave the Schnorr form implemented here at Asiacrypt 2002.
prereqs: [schnorr-signature, fiat-shamir-heuristic]
see_also: [group-signature, blind-signature, designated-verifier-signature, sigma-protocol, forking-lemma, discrete-logarithm-problem, pedersen-commitment, zero-knowledge-proof]
sources:
  - paper: doi:10.1007/3-540-45682-1_32
    title: "Ronald L. Rivest, Adi Shamir and Yael Tauman, How to leak a secret, Asiacrypt 2001, LNCS 2248, pages 552 to 565"
    locator: the definition of ring signatures, the ring equation with a symmetric cipher, and the construction from RSA trapdoor permutations
  - paper: doi:10.1007/3-540-36178-2_26
    title: "Masayuki Abe, Miyako Ohkubo and Koutarou Suzuki, 1-out-of-n signatures from a variety of keys, Asiacrypt 2002, LNCS 2501, pages 415 to 432"
    locator: the ring of hash challenges for Schnorr keys, the mix of RSA and discrete-logarithm keys, and the proofs in the random oracle model
  - paper: doi:10.1007/978-3-540-27800-9_28
    title: "Joseph K. Liu, Victor K. Wei and Duncan S. Wong, Linkable spontaneous anonymous group signature for ad hoc groups, ACISP 2004, LNCS 3108, pages 325 to 335"
    locator: the LSAG scheme and its linking tag
  - paper: doi:10.5195/ledger.2016.34
    title: "Shen Noether and Adam Mackenzie, Ring confidential transactions, Ledger 1, 2016, pages 1 to 18"
    locator: MLSAG, the multilayered linkable ring signature of Monero's RingCT
  - url: "https://eprint.iacr.org/2019/654"
    title: "Brandon Goodell, Sarang Noether and Arthur Blue, Concise linkable ring signatures and forgery against adversarial keys, Cryptology ePrint Archive 2019/654"
    locator: CLSAG, which replaced MLSAG in Monero, and its security model
---

A ring signature lets one member of a set of public keys sign on behalf of the whole set, the ring, without revealing which member signed. Anyone can check that the signature was made by the owner of one of the keys in the ring. The signer forms the ring alone, from any public keys it knows, without the other members' help or consent, and there is no manager who can find the signer. Rivest, Shamir and Tauman introduced ring signatures in 2001 under the title "How to leak a secret": a cabinet member can leak a document with a signature that proves it came from a cabinet member, while every member stays deniable. The Schnorr form of Abe, Ohkubo and Suzuki (AOS, 2002) closes a cycle of $n$ hash challenges, one per key, of which the signer can close only its own.

## In plain words

Picture a circle of locked boxes, one per person in the group. Each box takes a number and gives back the next number in the circle. Anyone can open a box by brute force if they get to pick its input after seeing its output, except their own box, which they can open with their key.

The signer starts at the box after its own, fakes its way around the circle through the boxes of everyone else, and finally uses its key to make the circle close. A verifier walks the circle and sees that it closes. The circle looks the same no matter whose key closed it, so the verifier cannot tell who signed.

## The problem

Given public keys $y_0, \ldots, y_{n-1}$ and the secret key $x_s$ of one of them, sign a message $m$ so that:

- **correctness:** the signature verifies for the ring $L = (y_0, \ldots, y_{n-1})$;
- **anonymity:** nobody, not even the holders of all the other secret keys, can tell which $s$ signed;
- **unforgeability:** without a secret key of the ring, nobody can make a valid signature for a new message.

There is no setup and no group manager. Compare [group signatures](/group-signature/) (signatures in which a manager admits members and can reveal the signer), which need both.

## The algorithm

The group $\langle g \rangle$ has prime order $q$, and $y_i = g^{x_i}$. $H$ hashes the ring, the message and a group element into $\mathbb{Z}_q$.

```pseudo id=main
SIGN(L = (y_0, …, y_{n−1}), s, x_s, m)
L1  α ← random in Z_q; z_i ← random in Z_q for i ≠ s
L2  e_{s+1} ← H(L, m, g^α)                              ▷ indices mod n
L3  for i ← s + 1, s + 2, …, s − 1:
L4      e_{i+1} ← H(L, m, g^{z_i} · y_i^{e_i})
L5  z_s ← α − x_s · e_s mod q                            ▷ now g^{z_s} · y_s^{e_s} = g^α
L6  return σ = (e_0, z_0, …, z_{n−1})

VERIFY(L, m, σ)
L7  e ← e_0; for i ← 0 to n − 1:
L8      e ← H(L, m, g^{z_i} · y_i^{e})
L9  return e = e_0
```

Each step $i$ is a [Schnorr](/schnorr-signature/) proof transcript (commitment $g^{z_i} y_i^{e_i}$, challenge $e_i$, response $z_i$). For every member except the signer, the transcript is made backwards: pick the response, then compute the commitment, which works for any challenge without the secret key. Only at position $s$ must the commitment $g^\alpha$ be fixed before its challenge $e_s$ is known, and then answering needs $x_s$. This is the [Fiat-Shamir](/fiat-shamir-heuristic/) (turning an interactive proof into a signature by hashing) form of the OR-composition of $n$ Schnorr proofs.

## Example

Toy group $p = 2039$, $q = 1019$, $g = 4$. Secret keys $x = (5, 17, 101)$ give the ring $L = (1024, 1458, 534)$. Member $s = 1$ signs $m$ = "hi" with $\alpha = 77$, $z_0 = 300$ and $z_2 = 500$:

| line | computation | result |
|---|---|---|
| L2 | $g^{\alpha} = 4^{77}$; $e_2 = H(L, m, 360)$ | $360$; $e_2 = 951$ |
| L4, $i = 2$ | $g^{500} \cdot 534^{951}$; $e_0 = H(L, m, 1402)$ | $1402$; $e_0 = 922$ |
| L4, $i = 0$ | $g^{300} \cdot 1024^{922}$; $e_1 = H(L, m, 733)$ | $733$; $e_1 = 642$ |
| L5 | $z_1 = 77 - 17 \cdot 642 \bmod 1019$ | $372$ |

The signature is $(922;\ 300, 372, 500)$. The verifier computes $T_0 = 733$, $e_1 = 642$, then $T_1 = g^{372} \cdot 1458^{642} = 360$ and $e_2 = 951$, then $T_2 = 1402$ and $e_0 = 922$: the ring closes. The value $360 = g^{77}$ comes back at position 1, but the verifier cannot tell that it came from a fixed $\alpha$ rather than from a random $z_1$.

## Correctness

The verifier recomputes the same chain of challenges. For $i \ne s$, step $i$ is line L4. For $i = s$, line L5 makes $g^{z_s} y_s^{e_s} = g^{\alpha - x_s e_s + x_s e_s} = g^\alpha$, whose hash line L2 already used as $e_{s+1}$. So the walk returns to $e_0$.

Anonymity is perfect: for a valid signature, each member $j$ has exactly one choice of coins that produces it (the $z_i$ for $i \ne j$, and $\alpha = z_j + x_j e_j$), so the signature has the same distribution for every signer. Unforgeability holds in the random oracle model under the discrete logarithm assumption, by a rewinding argument at the query that closes the ring. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Signing and verifying each take $n$ hashes and about $2n$ exponentiations in the group (one for the signer's own position), so $\Theta(n)$ group operations. The signature has $n + 1$ elements of $\mathbb{Z}_q$, and the verifier must also know the $n$ public keys. On a 256-bit elliptic curve a ring of 11 keys gives a signature of 384 bytes. Logarithmic-size ring signatures exist (Groth and Kohlweiss, Eurocrypt 2015), and so do constant-size ones with a trusted setup.

## Properties

- **Spontaneous.** No setup, no manager and no cooperation: the signer picks any public keys.
- **Perfect anonymity.** Even an attacker with all secret keys cannot tell the signer, if the signer's randomness is good.
- **No revocation.** Nobody can open a signature, unlike a group signature.
- **Mixed keys.** AOS allows a ring of RSA keys and discrete-logarithm keys together.
- **Unlinkable.** Two signatures by the same member cannot be linked, which is a problem for e-cash and voting; linkable ring signatures add a tag for this.

## Variants and improvements

- **Rivest, Shamir and Tauman (2001).** The first scheme uses RSA trapdoor permutations and a keyed symmetric permutation $E_k$ to form the ring equation $E_k(y_{n-1} \oplus E_k(\cdots E_k(y_0 \oplus v))) = v$; the signer inverts its own permutation to close it.
- **Linkable ring signatures** (Liu, Wei and Wong, ACISP 2004). LSAG adds a tag $\tilde y = h^{x_s}$ with $h = H(L)$ and proves that it has the same discrete logarithm as the signer's key. Two signatures by one key on the same ring have the same tag and can be linked, but the signer stays hidden.
- **Monero.** The CryptoNote whitepaper (2013, signed with the pseudonym Nicolas van Saberhagen) used a ring signature with a key image $I = x \cdot H_p(P)$ that does not depend on the ring, so that a coin spent twice shows the same image. Monero's RingCT (2017) uses MLSAG (Noether and Mackenzie), which signs for a matrix of keys to cover the amount commitments too; the October 2020 network upgrade replaced it with CLSAG (Goodell, Noether and Blue), which is about 25 percent smaller.
- **Threshold ring signatures.** $t$ members of the ring sign together, and any $t$ of the $n$ could have signed.
- **Logarithmic size.** One-out-of-many proofs (Groth and Kohlweiss 2015) give signatures of $O(\log n)$ group elements.
- **Definitions.** Bender, Katz and Morselli (TCC 2006) gave strong definitions: anonymity when all secret keys leak, and unforgeability when the attacker adds its own keys to rings.

## When to use it

Use a ring signature when a member of a set must authenticate a statement as coming from the set, with no central party and no way to undo the anonymity: whistle-blowing, anonymous authentication to a server from a set of known keys, and the sender privacy of cryptocurrency transactions (with linkability against double spending). If someone must be able to find the signer later, use a [group signature](/group-signature/). If the goal is that only one verifier is convinced, a two-member ring of the signer and that verifier is a [designated verifier signature](/designated-verifier-signature/).

## Pitfalls

- **Bad randomness.** If $\alpha$ is reused for two messages, $z_s$ reveals $x_s$, as in Schnorr signatures. If $\alpha$ is predictable, the verifier can find the position whose $g^{z_i} y_i^{e_i}$ equals $g^\alpha$.
- **Ring choice leaks.** Anonymity is only among plausible signers. If the other keys are dead, or are chosen in a way that only one real user would choose, the ring hides little. Chain analysis of early Monero transactions found many inputs whose real spend could be deduced, partly through rings with zero-value or already-spent decoys.
- **Bind the ring.** The hash must include the whole ring in a fixed order; otherwise a signature can be moved to another ring.
- **Validate keys.** Check that each $y_i$ lies in the prime-order group; in Monero, an unchecked key image outside the prime-order subgroup allowed a double spend before it was fixed in 2017.
- **Linkability is a choice.** A plain ring signature cannot stop double voting or double spending; a linkable one leaks that two signatures came from the same key.

## Implementations

The Python code is for study only: it is not constant time, and its group ($p = 2039$, $q = 1019$) has no security. It implements the AOS ring signature for Schnorr keys with SHA-256. Ring signatures have no standard test vectors. The tests check that every member of rings of size 1, 2 and 5 can sign, that a changed message or ring order fails, that a signature by member 2 is reproduced exactly by every other member with the coins computed by `coins_for`, and that a non-member cannot sign.

## History

Rivest, Shamir and Tauman defined ring signatures at Asiacrypt 2001, with an RSA construction and the leak of a secret as the motivating story. Abe, Ohkubo and Suzuki (Asiacrypt 2002) gave the efficient Schnorr form and showed that RSA and discrete-logarithm keys can mix in one ring. Liu, Wei and Wong (ACISP 2004) made them linkable, and the CryptoNote design of 2013 brought linkable ring signatures to cryptocurrencies. Monero has used them since its launch in 2014, with MLSAG from January 2017 and CLSAG from October 2020.

## References
