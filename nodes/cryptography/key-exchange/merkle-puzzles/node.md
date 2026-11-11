---
tag: GMZJAJ
kind: algorithm
slug: merkle-puzzles
name: Merkle's puzzles
aliases:
- Merkle puzzles
area: cryptography/key-exchange
level: advanced
summary: The first public key agreement scheme. Alice sends N weakly encrypted keys, Bob opens one, and an eavesdropper must open about half of them, a quadratic gap in work.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {N: the number of puzzles, S: the size of the puzzle key space}
  time: {worst: Θ(N + S), average: Θ(N + S), best: Θ(N)}
  space: {extra: Θ(N)}
properties: {deterministic: false, randomized: true}
history:
  year: 1974
  people: [Ralph C. Merkle]
  note: Merkle proposed the idea in a 1974 student project at Berkeley. It was published in Communications of the ACM in April 1978.
prereqs: [key-agreement-problem]
see_also: [diffie-hellman, key-agreement-problem, one-way-function, random-oracle-model, public-key-cryptography, block-cipher, x25519, session-key]
sources:
  - paper: doi:10.1145/359460.359473
    title: Ralph C. Merkle, Secure communications over insecure channels, Communications of the ACM 21(4), pages 294 to 299, 1978
    locator: the puzzle method, the choice of N puzzles each of cost about N, and the work of the enemy, which grows as the square of the work of the honest parties
  - paper: doi:10.1007/978-3-642-03356-8_22
    title: Boaz Barak and Mohammad Mahmoody-Ghidary, Merkle puzzles are optimal, an O(n^2)-query attack on any key exchange from a random oracle, CRYPTO 2009, LNCS 5677, pages 374 to 390
    locator: the main theorem, an eavesdropper that makes O(n^2) oracle queries breaks any key exchange in which the parties make n queries
  - paper: doi:10.1007/978-3-540-78524-8_4
    title: Eli Biham, Yaron J. Goren and Yuval Ishai, Basing weak public-key cryptography on strong one-way functions, TCC 2008, LNCS 4948, pages 55 to 72
    locator: the proof that a variant of Merkle's scheme forces an eavesdropper to make about n^2 queries to a random oracle
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976
    locator: Section III (public key distribution) and the reference to Merkle's paper, then submitted to Communications of the ACM
---

Merkle's puzzles is a [key agreement](/key-agreement-problem/) scheme in which Alice sends many small encrypted messages, the puzzles, each of which can be opened by brute force with moderate work, and Bob opens one at random and tells Alice which one by its identifier. Alice and Bob each do about $N$ units of work, while an eavesdropper who does not know which puzzle Bob chose must open about half of them, about $N^2/4$ units. Ralph Merkle proposed it in 1974, before [Diffie-Hellman](/diffie-hellman/), and it was the first scheme for agreeing on a secret key over a public channel. The gap is only quadratic, so it is not practical, but it shows that key agreement is possible from symmetric primitives alone, and Barak and Mahmoody proved that no scheme built only from a [random oracle](/random-oracle-model/) can do better.

**Notation.** $N$ is the number of puzzles and $S$ the number of possible puzzle keys; Merkle takes $S \approx N$. $E_r$ is an encryption with the weak puzzle key $r \in \{0, \dots, S - 1\}$, and $D_r$ its decryption. $\mathrm{MAGIC}$ is a fixed known string that marks a correct decryption. $\mathrm{id}_i$ and $k_i$ are the identifier and the session key hidden in puzzle $i$. One call to $E$ or $D$ is one unit of work.

## In plain words

Alice writes a million notes. Each note has a serial number and a secret key, and each is locked in a box with a weak lock that takes a few minutes to pick. She sends all the boxes to Bob in a mixed-up order.

Bob takes one box at random and picks its lock. He sends the serial number back to Alice in the open, and keeps the key. Alice has a list of all serial numbers and keys, so she finds the same key at once.

Eve sees all the boxes and the serial number, but she does not know which box it came from. She must pick boxes one by one until she finds it, about half a million boxes. So Bob works for minutes and Eve for a very long time, but not for an impossible time.

## The problem

Alice and Bob share no secret and talk over a channel that Eve can read but not change. They want a common [session key](/session-key/) such that Eve's work to find it is much larger than theirs. Merkle's scheme needs only a symmetric cipher (or a hash function), and no number theory.

## The algorithm

```pseudo id=main
MERKLE-PUZZLES(N, S)
L1  for i ← 1 to N do                              ▷ Alice
L2      pick id_i and k_i at random, and r_i at random in {0, …, S − 1}
L3      P_i ← E_{r_i}(MAGIC ‖ id_i ‖ k_i); store T[id_i] ← k_i
L4  send P_1, …, P_N to Bob in a random order
L5  Bob picks one puzzle P_j at random
L6  for r ← 0 to S − 1 do                          ▷ Bob opens P_j by brute force
L7      if D_r(P_j) begins with MAGIC then (id, k) ← the rest; send id to Alice; keep k; stop
L8  Alice sets k ← T[id]
```

**About the code.** The toy puzzle cipher XORs the plaintext with SHA-256$(r \,\|\, \text{nonce} \,\|\, \text{counter})$, where $r$ is a small integer and each puzzle has its own public nonce; the 8-byte $\mathrm{MAGIC}$ tells a right key from a wrong one. Each cipher call adds one unit to a work counter for each party. Alice shuffles the puzzles (line L4), so their positions say nothing about their identifiers. Eve's strategy in the code opens the puzzles in a random order until she finds one with the identifier that Bob sent. The code is for study only: the gap is quadratic, so no practical choice of $N$ is secure, and nothing is constant time.

## Example

Take $N = S = 64$. Alice makes 64 puzzles, 64 cipher calls. Bob picks one; its puzzle key is, say, $r = 37$, so he tries $r = 0, 1, \dots, 37$ and succeeds at the 38th call. He sends the 16-byte identifier, and Alice looks it up. Eve, on average, opens $(N + 1)/2 = 32.5$ puzzles at $(S + 1)/2 = 32.5$ calls each, about 1,056 calls, against Bob's 32.5 on average. With $N = S = 2^{30}$, honest work is about $2^{30}$ each, and Eve needs about $2^{58}$, which is large but feasible today.

Merkle's 1978 paper gives the general rule: if the honest parties do about $N$ work, the enemy does about $N^2$.

## Correctness

Bob decrypts the puzzle he chose with every key in $\{0, \dots, S - 1\}$, so he reaches $r_j$ and gets $\mathrm{MAGIC} \,\|\, \mathrm{id}_j \,\|\, k_j$. He stops early only if a wrong key also gives a plaintext that begins with $\mathrm{MAGIC}$; if the cipher's outputs under different keys behave like independent random strings, this happens with probability at most $S \cdot 2^{-8|\mathrm{MAGIC}|}$, where $|\mathrm{MAGIC}|$ is in bytes. If all identifiers are distinct, which fails with probability at most $N^2 2^{-8|\mathrm{id}| - 1}$, then $T[\mathrm{id}_j] = k_j$ and Alice and Bob hold the same key. The full proof, with Eve's expected work for the strategy above, is below.

## Complexity

Alice does $N$ encryptions and stores a table of $N$ entries, so $\Theta(N)$ time and space. Bob does at most $S$ decryptions, $(S + 1)/2$ on average, and the best case is one. Alice sends $\Theta(N)$ data, which is the main practical cost: with $N = 2^{30}$ puzzles of 40 bytes, that is about 40 gigabytes. Eve's expected work with the natural strategy is about $NS/4$; with $S = N$, that is $\Theta(N^2)$ against $\Theta(N)$ for each honest party.

**Lower and upper bounds.** In the [random oracle model](/random-oracle-model/), Biham, Goren and Ishai (2008) proved that a variant of the scheme forces Eve to make about $N^2$ oracle queries. In the other direction, Barak and Mahmoody (2009) proved that any key agreement in which the parties make $n$ queries to a random oracle can be broken with $O(n^2)$ queries. So the quadratic gap is the best possible from a random oracle alone, and [public key cryptography](/public-key-cryptography/) with a larger gap needs structure, such as the [discrete logarithm problem](/discrete-logarithm-problem/).

## Properties

- **Needs no number theory.** Any cipher or hash function works; the security is only as good as the gap $N$ to $N^2$.
- **Randomized**, with a failure probability that the sizes of $\mathrm{MAGIC}$ and the identifiers make negligible.
- **Passive security only.** Like plain Diffie-Hellman, it gives no authentication, so a [man in the middle](/man-in-the-middle-attack/) can run it with each side.
- **Not forward-secure against more computing power.** The gap is fixed when the puzzles are sent, so a recording can be broken later with enough work.

## Variants and improvements

- **Birthday form with a hash.** Alice and Bob each evaluate a hash function $H$ on about $\sqrt{N}$ random inputs from a set of size $N$ and publish the outputs. By the [birthday paradox](/birthday-attack/) they expect a common output, and its input is the key; Eve must invert $H$ on a set of size $N$. Biham, Goren and Ishai analyse hash-based variants of this kind.
- **Quantum versions.** With Grover's search, Eve can open puzzles faster, and quantum variants of the scheme have been studied that restore part of the gap.
- **Merkle's later work.** Merkle went on to work on public key systems with Hellman (the Merkle-Hellman knapsack, later broken) and on hash trees.

## When to use it

Not in practice: [Diffie-Hellman](/diffie-hellman/) and [X25519](/x25519/) give an exponential gap with 32-byte messages. Merkle's puzzles are used in teaching, as the simplest proof that public key agreement is possible, and in theory, as the benchmark for key agreement from [one-way functions](/one-way-function/) in an idealized model.

## Pitfalls

- **Small gap.** Eve's work is only about $N^2/4$; a reader who sees "about $2^{60}$" must remember that this is within reach of large computing budgets.
- **Wrong positions.** If Alice does not shuffle the puzzles, or if the identifier reveals the position, Eve opens only one puzzle.
- **Predictable puzzle keys.** If $r_i$ is not uniform in the full space, Bob and Eve both try the likely keys first, and Eve gains as much as Bob.
- **Short markers.** A short $\mathrm{MAGIC}$ lets a wrong key pass as right, and the two parties end with different keys.

## Implementations

## History

Ralph Merkle wrote the idea as a project proposal for a computer security course at Berkeley in 1974; the instructor did not accept it, and the journal at first rejected the paper as well. Diffie and Hellman, who found public key distribution independently, cite his work in "New directions in cryptography" (1976). Merkle's paper appeared in Communications of the ACM in April 1978. Impagliazzo and Rudich (1989) showed that key agreement from a random oracle alone cannot have a super-polynomial gap, and Barak and Mahmoody (2009) proved the exact quadratic bound, so the title of their paper says "Merkle puzzles are optimal".

## References
