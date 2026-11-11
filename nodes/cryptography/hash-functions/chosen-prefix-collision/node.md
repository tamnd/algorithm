---
tag: 41PGVW
kind: concept
slug: chosen-prefix-collision
name: Chosen-prefix collision
aliases:
- chosen-prefix collision attack
area: cryptography/hash-functions
level: research
summary: Given two different prefixes P and P', find suffixes S and S' with H(P || S) = H(P' || S'). It is stronger than an identical-prefix collision and broke MD5 and SHA-1 in practice.
prereqs: [collision-finding, merkle-damgard-construction]
see_also: [md5, sha-1, birthday-attack, collision-resistance, multicollision-attack, differential-cryptanalysis, second-preimage-finding, length-extension-attack]
sources:
  - paper: "Marc Stevens, Arjen K. Lenstra and Benne de Weger, Chosen-prefix collisions for MD5 and colliding X.509 certificates for different identities, EUROCRYPT 2007, LNCS 4515, pages 1 to 22"
    locator: the first chosen-prefix collision for MD5, with a birthday phase and a series of near-collision blocks, and two certificates with different names
  - paper: "Marc Stevens, Alexander Sotirov, Jacob Appelbaum, Arjen Lenstra, David Molnar, Dag Arne Osvik and Benne de Weger, Short chosen-prefix collisions for MD5 and the creation of a rogue CA certificate, CRYPTO 2009, LNCS 5677, pages 55 to 69"
    locator: the rogue CA certificate built from a real certificate signed by a commercial CA, and the shorter MD5 attack used for it
  - paper: "Marc Stevens, Counter-cryptanalysis, CRYPTO 2013, LNCS 8042, pages 129 to 146"
    locator: the detection of collision attacks from one message, and the analysis of the new MD5 chosen-prefix variant in the Flame malware
  - paper: "Gaetan Leurent and Thomas Peyrin, SHA-1 is a Shambles: first chosen-prefix collision on SHA-1 and application to the PGP web of trust, USENIX Security 2020, pages 1839 to 1856"
    locator: the first SHA-1 chosen-prefix collision, at about 2^63.4 SHA-1 calls, and two PGP keys with different user IDs
  - paper: "Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov, The first collision for full SHA-1, CRYPTO 2017, LNCS 10401, pages 570 to 596"
    locator: the identical-prefix SHA-1 collision, for comparison with the chosen-prefix case
  - paper: "Xiaoyun Wang and Hongbo Yu, How to break MD5 and other hash functions, EUROCRYPT 2005, LNCS 3494, pages 19 to 35"
    locator: the identical-prefix MD5 collision that the chosen-prefix attacks extend
---

A chosen-prefix collision is a pair of messages $P \,\|\, S$ and $P' \,\|\, S'$ with the same hash, where the attacker chose the two different prefixes $P$ and $P'$ first, and then computed the suffixes $S$ and $S'$. An identical-prefix collision is the weaker case $P = P'$: the two messages share a start and differ only in the colliding blocks. For a [Merkle-Damgard](/merkle-damgard-construction/) hash, a chosen-prefix attack must cancel an arbitrary difference between two chaining values, so it is harder to build, but it lets the attacker put any content, such as two different names in two certificates, in front of the collision. Stevens, Lenstra and de Weger found the first one for [MD5](/md5/) in 2007. In 2009 Stevens and others used it to make a rogue certificate authority, the Flame malware used it in 2012, and in 2020 Leurent and Peyrin found one for [SHA-1](/sha-1/) at about $2^{63.4}$ calls.

## In plain words

A plain collision is two messages that start the same and differ only in a block of strange bytes in the middle. That is useful, but the attacker cannot change what the readable part says.

In a chosen-prefix collision, the attacker writes two completely different starts, such as two certificates with different owners. Then they compute a block of extra bytes for each, so that both full messages get the same fingerprint.

So anything signed for the first message is also a valid signature for the second.

## The idea

**Identical prefix against chosen prefix.** In a Merkle-Damgard hash, after the prefixes the chaining values are $h = f^*(IV, P)$ and $h' = f^*(IV, P')$. In the identical-prefix case $h = h'$, and the attack only needs two block sequences that start from one state and end at one state. In the chosen-prefix case $h \ne h'$ is a random difference, and the attack must remove it. Once the states are equal, any common tail keeps them equal, so the collision survives appended text.

**The generic cost is the same.** With no weakness in the hash, a chosen-prefix collision is a claw between $x \mapsto H(P \,\|\, x)$ and $y \mapsto H(P' \,\|\, y)$, which a [birthday attack](/birthday-attack/) finds in about $2^{n/2}$ calls. The difference shows up in cryptanalysis. The best identical-prefix attacks on MD5 take seconds, while chosen-prefix MD5 attacks took about $2^{39}$ to $2^{50}$ calls. For SHA-1, Leurent and Peyrin give about $2^{61.2}$ calls for an identical-prefix collision and $2^{63.4}$ for a chosen-prefix one.

**The two phases of the real attacks.**

1. *Birthday phase.* Append random blocks to both prefixes until the difference between the two chaining values lies in a small set of differences that the next phase can handle. This is a birthday search on part of the state, so it costs about the square root of the size of the condition.
2. *Near-collision phase.* Append pairs of blocks. Each pair follows a differential path through the compression function that cancels part of the remaining difference. After a few pairs, the difference is zero.

The scheme of the attack, with the page's code lines:

```pseudo id=main
CHOSEN-PREFIX-COLLISION(P, P')
L1  h ← f*(IV, P); h' ← f*(IV, P')                         ▷ prefixes padded to the same length
L2  find blocks s, s' such that f(h, s) and f(h', s') differ only in a handled set   ▷ birthday phase
L3  while h ≠ h' do
L4      find blocks b, b' with a near-collision path that removes part of h ⊕ h'
L5      append b to S and b' to S'; update h and h'
L6  return S, S'
```

**A toy with a planted weakness.** Real near-collision blocks need a differential path for MD5 or SHA-1, which takes thousands of lines and much computing. The page's code instead uses a toy 32-bit hash whose weakness is put there on purpose, so that both phases fit in a few lines. The state is $(t, u)$, with $t$ the top 8 bits and $u$ the low 24 bits. The new $u$ depends only on $u$ and the block, never on $t$. The new $t$ is $t$ XOR a value that depends only on $u$ and the block, XOR two bits from the top byte of the block, placed in one of four 2-bit windows chosen by the state. So:

- the birthday phase makes $u = u'$, a 24-bit birthday problem with two lists;
- each near-collision pair uses the same low block bits on both sides, so the shared part of the update cancels, and a chosen difference in the top byte clears one nonzero window of $t \oplus t'$.

This toy says nothing about the cost of real attacks. It only shows the shape of the method. The code is for study only and not constant time. Do not use the toy hash for anything. For real hashing use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or libsodium.

## Examples

**The toy, step by step.** The two prefixes are `Certificate: CN=good.example ` and `Certificate: CN=evil.example `, each split into 8 blocks of 32 bits.

- After the prefixes the states are `0x143cae71` and `0xc9f5ddf2`.
- The birthday phase finds blocks `0x1432` and `0x937`, giving `0x2fbc28f7` and `0xa9bc28f7`. The low 24 bits agree, and the top bytes differ by `0x86` = `10000110` in binary, which has three nonzero 2-bit windows. This took 10341 calls of the compression function.
- Three near-collision pairs clear the three windows: `0x0` with `0x1000000`, `0x10003` with `0x2010003`, and `0x20005` with `0x2020005`.
- Both messages, with the final length block, hash to `0x7a9cd1ac`. The total is 10352 calls.

Over 50 random pairs of 3-block prefixes, the mean cost was 7427 calls, close to the $2\sqrt{\pi 2^{24}/4} \approx 7260$ of a two-list birthday on 24 bits. A generic attack on the full 32-bit state would need about $2^{16}$ calls per list. The tests check that the collision holds, that it survives a common tail, that each near-collision block clears a window, and that the identical-prefix case needs no birthday phase at all.

**MD5, 2007.** Stevens, Lenstra and de Weger built two X.509 certificates with different names and the same MD5 hash. Their birthday phase made the difference fit a family of differential paths, and then a series of near-collision blocks removed it.

**The rogue CA, 2009.** Stevens, Sotirov, Appelbaum and others obtained a normal website certificate from a commercial certificate authority that still signed with MD5. They had chosen its contents in advance so that it collided with a second certificate, which said it was itself a certificate authority. The signature on the first was valid for the second, so they could issue certificates trusted by browsers. They had to predict the serial number and the time of signing, and the collision was computed on a cluster of about 200 PlayStation 3 consoles. The certificate was made to expire at once, and browsers and CAs then retired MD5.

**Flame, 2012.** The Flame malware carried a code signing certificate that chained to Microsoft. Its authors made it with an MD5 chosen-prefix collision against a Terminal Server licensing certificate. Stevens's counter-cryptanalysis showed that it used a new variant of the attack, not the published one.

**SHA-1, 2020.** Leurent and Peyrin found a chosen-prefix collision for SHA-1 at about $2^{63.4}$ calls, with GPUs costing about 45000 US dollars to rent at the time. They made two PGP keys with different user IDs and the same SHA-1 fingerprint, so that a signature on one key in the web of trust also certifies the other. GnuPG then stopped trusting SHA-1 signatures on keys made after 2019.

## Where it is used

- **Attacks on signatures.** Any system that signs $H(\text{data})$, where the attacker can choose part of the data and predict the rest, falls to a chosen-prefix collision: certificates, signed software, PGP keys and document formats.
- **Defense by unpredictability.** Certificate authorities must put at least 64 random bits in serial numbers, so that the attacker cannot predict the prefix that will be signed. This is a defense in depth, not a fix.
- **Detection.** Stevens's counter-cryptanalysis checks a single message for the traces of known near-collision paths. Git and GitHub use such a check, `sha1collisiondetection`, on SHA-1.
- **The fix.** Stop using MD5 and SHA-1 for signatures. Use SHA-256, SHA-512 or SHA-3, through the standard library or a FIPS 140 validated module.
- **Relation to other attacks.** A chosen-prefix collision is a collision, not a [second preimage](/second-preimage-finding/): the attacker controls both messages. It does not help against a message that someone else wrote. Together with [multicollisions](/multicollision-attack/) and herding, it shows that an iterated hash gives the attacker more freedom than a random function.

## References
