---
tag: 04D162
kind: algorithm
slug: multicollision-attack
name: Multicollision attack
aliases:
- Joux multicollision
area: cryptography/hash-functions
level: research
summary: Chain t one-block collisions of an iterated hash to get 2^t messages with one digest, at the cost of t birthday attacks. It shows that H1(m) || H2(m) is barely stronger than its stronger half.
solves: [collision-finding]
model: query-model
complexity:
  vars: {n: the chaining value length in bits, t: the number of colliding block pairs}
  time: {average: Θ(t 2^(n/2))}
  space: {extra: Θ(2^(n/2) + t)}
properties: {deterministic: true}
history:
  year: 2004
  people: [Antoine Joux]
  note: Joux showed at CRYPTO 2004 that iterated hashes have cheap multicollisions, and used them to break the concatenation of two hashes and other combiners.
prereqs: [birthday-attack, merkle-damgard-construction]
see_also: [birthday-attack, merkle-damgard-construction, second-preimage-finding, chosen-prefix-collision, compression-function, sponge-construction, collision-finding, collision-resistance]
sources:
  - paper: "Antoine Joux, Multicollisions in iterated hash functions. Application to cascaded constructions, CRYPTO 2004, LNCS 3152, pages 306 to 316"
    locator: Section 3 (2^t-multicollisions in t times the cost of one collision) and Section 4 (collisions and preimages for the concatenation H1 || H2)
  - paper: "John Kelsey and Tadayoshi Kohno, Herding hash functions and the Nostradamus attack, EUROCRYPT 2006, LNCS 4004, pages 183 to 200"
    locator: the diamond structure, a tree of collisions that extends the multicollision idea
  - paper: "John Kelsey and Bruce Schneier, Second preimages on n-bit hash functions for much less than 2^n work, EUROCRYPT 2005, LNCS 3494, pages 474 to 490"
    locator: expandable messages built from collisions of a one-block and a long message, in the style of Joux
  - paper: "Stefan Lucks, A failure-friendly design principle for hash functions, ASIACRYPT 2005, LNCS 3788, pages 474 to 494"
    locator: the wide-pipe design, whose internal state is larger than the output
  - paper: "Jonathan J. Hoch and Adi Shamir, Breaking the ICE: finding multicollisions in iterated concatenated and expanded (ICE) hash functions, FSE 2006, LNCS 4047, pages 179 to 194"
    locator: multicollisions for hashes that use each message block more than once
  - paper: "Kazuhiro Suzuki, Dongvu Tonien, Kaoru Kurosawa and Koji Toyota, Birthday paradox for multi-collisions, ICISC 2006, LNCS 4296, pages 29 to 40"
    locator: the generic cost of an r-multicollision for a random function, about (r!)^(1/r) 2^(n(r-1)/r)
---

A multicollision attack finds many messages that all have the same hash. For a random function with $n$-bit output, a set of $r$ messages with one digest costs about $2^{n(r-1)/r}$ queries, which tends to $2^n$ as $r$ grows. Joux showed in 2004 that an iterated hash, such as a [Merkle-Damgård](/merkle-damgard-construction/) hash, is much weaker: $2^t$ colliding messages cost only $t$ [birthday attacks](/birthday-attack/), about $t \cdot 2^{n/2}$. Find a collision of one block, then a collision of the next block from the common chaining value, and so on. Each choice of one block from each pair gives the same digest. The main use is to break combiners: the concatenation $H_1(m) \| H_2(m)$ of an $n_1$-bit and an $n_2$-bit hash costs little more than the stronger hash alone, not the $2^{(n_1 + n_2)/2}$ its length suggests.

## In plain words

An iterated hash reads a message one block at a time, and keeps only a short running value between blocks. Find two different first blocks that give the same running value. That costs one birthday search. From that value, find two different second blocks that again agree. Do this for ten blocks.

Now build a message by picking the first or second option at each of the ten steps. There are 1024 ways to pick, and each way passes through the same running values, so all 1024 messages get the same hash. You paid for ten collisions and got a thousand colliding messages.

This kills a natural idea: put two different hashes side by side to make a stronger one. Make many messages that collide in the first hash. Among them, two will collide in the second hash by the birthday bound.

## The problem

Let $H$ be an iterated hash with compression function $f : \{0,1\}^n \times \{0,1\}^b \to \{0,1\}^n$, initial value $IV$, and Merkle-Damgård strengthening: the last block encodes the message length. An $r$-*multicollision* is a set of $r$ distinct messages with the same digest. The goal is a $2^t$-multicollision. The cost is the number of calls of $f$ in the [query model](/query-model/). The attack uses only the iteration: it treats $f$ as a black box.

## The algorithm

JOUX-MULTICOLLISION finds $t$ one-block collisions in a chain.

```pseudo id=main
JOUX-MULTICOLLISION(f, IV, t)
L1  h ← IV; P ← empty list
L2  for i ← 1 to t do
L3      find B ≠ B' with f(h, B) = f(h, B'); h ← f(h, B)     ▷ a birthday attack on f(h, ·)
L4      append (B, B') to P
L5  return P                                              ▷ 2^t messages: one block from each pair
```

Line L3 is a [birthday attack](/birthday-attack/) on the map $B \mapsto f(h, B)$, with $h$ fixed. The output $P = [(B_1, B'_1), \ldots, (B_t, B'_t)]$ describes the $2^t$ messages $C_1 \| C_2 \| \cdots \| C_t$ with $C_i \in \{B_i, B'_i\}$.

**Attack on $H_1 \| H_2$.** Let $H_1$ be iterated with an $n_1$-bit chaining value, and $H_2$ any hash with $n_2$-bit output.

1. Run JOUX-MULTICOLLISION on $H_1$ with $t = \lceil n_2/2 \rceil$, or a few more.
2. Hash the $2^t$ messages with $H_2$ and look for a repeat, as in a birthday attack.
3. Two messages with the same $H_2$ digest also have the same $H_1$ digest. So they collide under $H_1 \| H_2$.

The Python code for this page runs both attacks on a toy Merkle-Damgård hash with 32-bit blocks and a chaining value of 16 to 24 bits. The toy compression function is a 64-bit mixer, and two salts give two different hashes. It is for study only and it is not constant time. Do not use the toy hash. For real work, use SHA-256 or SHA-3 from hashlib, a FIPS 140 validated module, or libsodium.

## Example

**A 256-multicollision.** With $n = 24$ and $t = 8$, the code finds 8 pairs of blocks. The first three pairs are (0x2e9, 0x716), (0x417af, 0x4204d) and (0x80837, 0x80e60). All 256 messages of 8 blocks hash to 0x3244c1. The run made 35589 calls of $f$. The model predicts $t \cdot \sqrt{\pi 2^{24}/2} \approx 41068$. A random function would need about $(256!)^{1/256} \cdot 2^{24 \cdot 255/256} \approx 2^{30.5}$ calls for a 256-multicollision.

**A collision of $H_1 \| H_2$.** Let $H_1$ and $H_2$ be the toy hash with 24-bit chaining values and the salts 1 and 2, so $H_1 \| H_2$ has 48 bits. The code builds a $2^{14}$-multicollision on $H_1$ and finds two messages of 14 blocks that differ in 6 blocks. Both give $H_1$ = 0x32ec6b and $H_2$ = 0xb5559c. The whole attack made 99083 calls of the compression function. A birthday attack on a 48-bit hash needs about $1.25 \cdot 2^{24}$, about 21 million, evaluations.

## Correctness

Write $h_0 = IV$ and $h_i = f(h_{i-1}, B_i)$ for the state after round $i$. Line L3 ensures $f(h_{i-1}, B_i) = f(h_{i-1}, B'_i) = h_i$. By induction on $i$, every message $C_1 \cdots C_i$ with $C_j \in \{B_j, B'_j\}$ reaches the state $h_i$. All $2^t$ messages have $t$ blocks, so the length block is the same, and so is the digest. They are distinct because $B_i \ne B'_i$. The full proof is below.

## Complexity

- **Multicollision.** $t$ birthday attacks on $n$-bit values: about $t \cdot 1.25 \cdot 2^{n/2}$ calls of $f$ on average. Memory $O(2^{n/2})$ for one search at a time, or $O(1)$ with [Pollard rho](/pollard-rho-collision-search/). The output has size $O(t)$, although it describes $2^t$ messages.
- **Generic multicollision.** For a random function, an $r$-multicollision needs about $(r!)^{1/r} \cdot 2^{n(r-1)/r}$ queries (Suzuki and others, 2006). For $r = 2^t$ with $t \ge 2$ this is far above $t \cdot 2^{n/2}$.
- **Concatenation.** About $\lceil n_2/2 \rceil \cdot 2^{n_1/2}$ calls of $f_1$ for the multicollision, plus about $2^{n_2/2}$ evaluations of $H_2$ on messages of $n_2/2$ blocks. So $O(n_2 \cdot 2^{n_1/2} + n_2 \cdot 2^{n_2/2})$, which is polynomial factors above $2^{\max(n_1, n_2)/2}$. For two 128-bit hashes this is about $2^{71}$, not $2^{128}$.
- **Preimages of the concatenation.** Joux also gives a preimage attack on $H_1 \| H_2$ that costs about $2^{n_1} + 2^{n_2}$ up to polynomial factors, not $2^{n_1 + n_2}$.

## Properties

- **Uses only the iteration.** The attack works for each iterated hash with an $n$-bit chaining value, whatever the compression function. It even works if $f$ is a random function.
- **Fixed length.** All messages have the same length, so Merkle-Damgård strengthening does not stop it.
- **Structured output.** The messages are all choices in a product of pairs. Many attacks need exactly this freedom.
- **Bounded by the state, not the output.** The cost depends on the chaining value length $n$. A hash with a chaining value wider than the output is protected.

## Variants and improvements

- **Expandable messages.** Kelsey and Schneier collide a one-block message with a message of $2^i + 1$ blocks at each step. The result has a choice of length, and gives long [second preimages](/second-preimage-finding/).
- **Diamond structure.** Kelsey and Kohno build a binary tree of collisions in place of a chain. It lets the attacker herd $2^k$ starting values to one chaining value, for the Nostradamus attack.
- **Hoch and Shamir.** Multicollisions extend to hashes that read each block several times, in any order, as long as each block is read a bounded number of times.
- **Wide pipe and sponge.** Lucks proposed an internal state of at least $2n$ bits for an $n$-bit output. Then each internal collision costs $2^n$ or more, and multicollisions cost about as much as for a random function. A [sponge](/sponge-construction/) with capacity $c$ has internal collisions at about $2^{c/2}$, so $c \ge 2n$ plays the same role.
- **Multicollisions in practice.** With a practical collision attack on the compression function, such as for MD5, line L3 runs in seconds, and multicollisions of MD5 are cheap.

## When to use it

Use it to test a design that combines hashes or iterates a narrow state. Concatenation $H_1 \| H_2$, cascades $H_2(H_1(m))$, and hashes that read the message twice fail in this way. To get more security than one hash, choose one hash with a larger output, or a wide-pipe or sponge design with enough capacity. Use the multicollision as a building block in [second-preimage finding](/second-preimage-finding/) and herding.

## Pitfalls

- **Concatenation is not a strong combiner for collisions.** It keeps collision resistance if either hash has it, but the security does not add up. Do not count $n_1 + n_2$ bits.
- **The state is what counts.** A hash with a 512-bit output but a 256-bit chaining value has multicollisions at about $2^{128}$ each.
- **Messages are long.** The concatenation attack uses messages of $n_2/2$ blocks. A limit on the message length does not help much.
- **Different blocks per pair.** The two blocks of each pair must differ. Otherwise the $2^t$ messages are not distinct.

## Implementations

## History

Joux published the attack at CRYPTO 2004. Before then, concatenating two hashes was a common way to hedge against a break of one of them, as in the SSL 3.0 key derivation, which mixes MD5 and SHA-1. The attack showed that this gives little more than the stronger hash for collisions. It also started a line of work on generic attacks on iterated hashes: expandable messages (Kelsey and Schneier, 2005), herding (Kelsey and Kohno, 2006), and multicollisions for more general iterations (Hoch and Shamir, 2006). Lucks proposed wide-pipe hashes in 2005 as a defense. The SHA-3 competition then required resistance to such generic attacks, and Keccak, the winner, is a sponge with a large capacity.

## References
