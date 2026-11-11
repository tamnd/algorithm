---
tag: 033D0B
kind: problem
slug: second-preimage-finding
name: Second-preimage finding
aliases:
- second preimage problem
area: cryptography/hash-functions
level: core
summary: Given a message x, find a different x' with H(x') = H(x). Generic cost 2^n, but only about 2^(n-k) for a 2^k-block target in a Merkle-Damgard hash, by Kelsey and Schneier.
history:
  year: 2005
  people: [John Kelsey, Bruce Schneier]
  note: Kelsey and Schneier turned Dean's fixed point idea into a generic long-message attack with expandable messages, for every Merkle-Damgard hash.
prereqs: [second-preimage-resistance, merkle-damgard-construction]
see_also: [preimage-finding, collision-finding, multicollision-attack, chosen-prefix-collision, davies-meyer-construction, compression-function, birthday-attack, sponge-construction]
sources:
  - paper: "John Kelsey and Bruce Schneier, Second preimages on n-bit hash functions for much less than 2^n work, EUROCRYPT 2005, LNCS 3494, pages 474 to 490"
    locator: expandable messages built from multicollisions, and the attack in k 2^(n/2+1) + 2^(n-k+1) work for a 2^k-block target
  - paper: "Richard Drews Dean, Formal aspects of mobile code security, PhD thesis, Princeton University, 1999"
    locator: the chapter on hash functions, with expandable messages from fixed points of the compression function
  - paper: "John Kelsey and Tadayoshi Kohno, Herding hash functions and the Nostradamus attack, EUROCRYPT 2006, LNCS 4004, pages 183 to 200"
    locator: the diamond structure, and the herding attack on a committed digest
  - paper: "Ralph C. Merkle, One way hash functions and DES, CRYPTO 1989, LNCS 435, pages 428 to 446"
    locator: the iterated construction with the length in the last block, which stops the plain long-message attack but not the expandable one
  - paper: "Eli Biham and Orr Dunkelman, A framework for iterative hash functions: HAIFA, Second NIST Cryptographic Hash Workshop, 2006"
    locator: a block counter in each compression call, which blocks expandable messages
  - paper: "Stefan Lucks, A failure-friendly design principle for hash functions, ASIACRYPT 2005, LNCS 3788, pages 474 to 494"
    locator: the wide-pipe design, whose internal state is twice the output
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.7.1 (attacks on hash functions, including the long-message attack)
---

Second-preimage finding is the problem of finding, for a given message $x$, a different message $x'$ with $H(x') = H(x)$. A hash that resists it is [second-preimage resistant](/second-preimage-resistance/). Unlike [collision finding](/collision-finding/), the attacker does not choose $x$, so the birthday paradox does not help, and the generic cost for a random function with $n$-bit output is about $2^n$. For a [Merkle-Damgard](/merkle-damgard-construction/) hash and a long target of $2^k$ blocks, the cost falls to about $k \cdot 2^{n/2+1} + 2^{n-k+1}$. Kelsey and Schneier (2005) showed this with an expandable message, which turns the many chaining values of a long message into many targets. Kelsey and Kohno (2006) used a related structure, the diamond, to herd any prefix to a digest fixed in advance.

## In plain words

Someone gives you a message and its fingerprint. You must write a different message with the same fingerprint.

For a good hash there is no better way than to keep trying new messages, and you need about as many tries as there are fingerprints.

But a hash that reads a long message block by block passes through many middle states. If you can reach any one of them with a message of the right length, you can copy the rest of the original message and get the same fingerprint. A long target gives many chances, so the attack is cheaper.

## Definition

**Input.** A function $H : D \to \{0,1\}^n$, given as an oracle or as code, and a message $x \in D$. In the usual game, $x$ is drawn at random, often of a given length.

**Output.** A message $x' \in D$ with $x' \ne x$ and $H(x') = H(x)$.

**Measure.** The number of calls of $H$ or of its compression function, the memory, and the success probability over the choice of $x$ and $H$.

**Compared with nearby problems.** In [preimage finding](/preimage-finding/), only a digest $y$ is given, and any $x'$ with $H(x') = y$ wins. In collision finding, the attacker picks both messages. So second-preimage finding sits between them: it gives the attacker more than a preimage problem (a message to work from), and less than a collision problem.

## Variants

- **Random target.** $x$ is uniform among messages of a given length. This is the Sec notion of Rogaway and Shrimpton.
- **Every target.** The attack must work for every $x$, or for an $x$ chosen by an adversary (aSec). Generic bounds are the same.
- **Long targets.** The target has $2^k$ blocks. This is where Merkle-Damgard hashes are weaker than a random function.
- **Herding.** The attacker first publishes a digest $y$. Later, given a prefix $P$ chosen by someone else, they find a suffix $S$ with $H(P \,\|\, S) = y$. This is a chosen-target form of the problem, also called the Nostradamus attack.
- **On the compression function.** Given $(h, m)$, find $(h', m') \ne (h, m)$ with $f(h', m') = f(h, m)$. A compression function with easy fixed points, such as [Davies-Meyer](/davies-meyer-construction/), makes some steps easier.

## Examples

**Brute force on 16 bits.** The toy hash of the page's code is Merkle-Damgard with a 64-bit mixer cut to an $n$-bit state, 32-bit blocks, and a final length block. With $n = 16$, the target `[0x12345678, 0x9abcdef0]` has digest `0x7c75`. Trying one-block messages $0, 1, 2, \ldots$ found the second preimage `[0x61b]` after 3134 compression calls. That was lucky: the expected count is about $2 \cdot 2^{16}$ calls, two per try.

**Kelsey and Schneier on 24 bits.** With $n = 24$ and $k = 10$, the target is a random message of $2^{10} = 1024$ blocks (seed 2005).

1. *The expandable message.* For $i = 0, \ldots, 9$, find a collision between one block and $2^i$ dummy blocks plus one block, from the current state. Each step is a two-list birthday search on 24 bits. The result is a list of ten pairs. Choosing the short or long side of each gives a message of any length from 10 to $10 + 2^{10} - 1 = 1033$ blocks, all ending in the same state `0x2ade5b`. This took 77456 calls, against the model $k \cdot 2^{n/2+1} = 81920$.
2. *The link.* Try blocks $B$ from that state until $f(\text{state}, B)$ equals one of the chaining values $h_{11}, \ldots, h_{1024}$ of the target, 1014 targets in all. It hit $h_{83}$ after 14397 calls, near the expected $2^{24}/1014 \approx 16546$.
3. *The output.* The expandable message of length 82, then $B$, then blocks 84 to 1024 of the target. It has 1024 blocks, so the length block matches, and it differs from the target in its first 83 blocks.

Both messages hash to `0xc36f0e`. The total was 91853 calls, against $2^{24} \approx 1.68 \cdot 10^7$ for brute force. The test also checks every length of an expandable message. The code is for study only and not constant time, and the hash is a toy. For real hashing use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or libsodium.

## Known algorithms

| Algorithm | Cost | Applies to |
|---|---|---|
| brute force | about $2^n$ calls | any hash |
| long-message attack without length padding | $2^n / L$ for an $L$-block target | iterated hashes with no length block |
| Dean's fixed points | about $2^{n/2}$ to build the expandable message, then $2^{n-k}$ | compression functions with easy fixed points, such as Davies-Meyer |
| Kelsey and Schneier | $k \cdot 2^{n/2+1} + 2^{n-k+1}$ for $2^k$ blocks | every Merkle-Damgard hash with length padding |
| herding with a diamond of $2^k$ leaves | about $2^{(n+k)/2+2}$ offline, then $2^{n-k+1}$ online | every Merkle-Damgard hash |
| cryptanalytic attacks | design-specific | for example MD4, for some weak messages |

**The expandable message.** A $(k, k + 2^k - 1)$ expandable message is a list of $k$ pairs. Pair $i$ is one block and $2^i + 1$ blocks that lead from one state to the same state. It is a form of [multicollision](/multicollision-attack/): $2^k$ messages of all the lengths in the range with one final state. Its cost is $k$ birthday searches.

**Herding.** A diamond structure is a binary tree of $2^k$ leaf states. Each pair of states at one level is mapped by a birthday search to one state at the next, and the root is hashed to $y$. Given the prefix $P$, the attacker finds a block from $H(P)$ to any leaf, in $2^{n-k}$ tries, and follows the tree to the root. With $k \approx n/3$ both phases cost about $2^{2n/3}$.

## Bounds

- **Generic lower bound.** For a random oracle, $q$ queries find a second preimage with probability at most $q/2^n$. So $\Omega(2^n)$ queries are needed for a short target.
- **The long-message upper bound.** For a Merkle-Damgard hash with an $n$-bit state, a target of $2^k$ blocks has a second preimage in $O(k \cdot 2^{n/2} + 2^{n-k})$ calls. For SHA-1 ($n = 160$) and a target of $2^{55}$ blocks, near the length limit of $2^{64}$ bits, that is about $2^{106}$ instead of $2^{160}$. This does not break SHA-1 in practice, since such a message cannot be stored, but it shows that the iterated structure costs security.
- **Quantum.** Grover search gives about $2^{n/2}$ quantum calls for a short target, and this is optimal for a random oracle.
- **Designs that avoid the long-message loss.** A wide-pipe hash, whose state has at least $2n$ bits (Lucks 2005); a block counter in each call (HAIFA, Biham and Dunkelman 2006), as in BLAKE2; and a [sponge](/sponge-construction/) with capacity $c \ge 2n$, as in SHA-3. For these, the generic bound is back to about $2^n$.

## Reductions

- **To collision finding.** A second preimage $x'$ of $x$ is a collision $(x, x')$. So collision finding is never harder, and a bound on collisions gives a bound on second preimages. The reverse fails: the birthday attack does not give second preimages.
- **From a compression function attack.** By the Merkle-Damgard theorem, a second preimage for the full hash gives a collision of the compression function, but not a second preimage of it. Conversely, an attack that finds, for the fixed input $IV$, a block $m' \ne M_1$ with $f(IV, m') = f(IV, M_1)$ yields a second preimage of the full hash: replace the first block of the target.
- **To preimage finding.** A preimage algorithm gives second preimages when $H$ compresses: for a random $x$, a preimage of $H(x)$ is a different message with good probability. Rogaway and Shrimpton make this precise.

## Applications

- **Forging signed data.** A second preimage of a document that someone else has signed would let an attacker swap in another document under the same signature. This is why second-preimage resistance, not only collision resistance, matters for old signatures. For MD5, no practical second preimage attack is known on a document that the attacker did not prepare: the best preimage attack costs about $2^{123.4}$.
- **Committed predictions.** The herding attack shows that publishing $H(\text{prediction})$ in advance commits to less than it seems: with $2^{2n/3}$ work, one digest can be opened to a message that starts with any prefix learned later.
- **Hash design.** The long-message attacks led to wide-pipe designs, block counters and sponges, and to the length limits of SHA-2 being treated as part of its security claim.

## References
