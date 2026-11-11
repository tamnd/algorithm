---
tag: AZDCQJ
kind: problem
slug: commitment-scheme
name: Commitment scheme
aliases:
- bit commitment
- cryptographic commitment
area: cryptography/protocols
level: intro
summary: "Commit to a value now and open it later. Hiding keeps the value secret until the opening, binding stops a change. Both cannot be perfect at the same time."
prereqs: [cryptographic-hash-function, pseudorandom-generator, random-oracle-model]
see_also: [pedersen-commitment, fair-coin-flipping, zero-knowledge-proof, sigma-protocol, verifiable-secret-sharing, collision-resistance, one-way-function, non-malleability]
sources:
  - paper: doi:10.1145/1008908.1008911
    title: "Manuel Blum, Coin flipping by telephone: a protocol for solving impossible problems, ACM SIGACT News 15(1), 1983, pages 23 to 27 (first given at CRYPTO 1981)"
    locator: the coin flip over the telephone, in which one party commits to a value before the other speaks
  - paper: doi:10.1007/BF00196774
    title: Moni Naor, Bit commitment using pseudorandomness, Journal of Cryptology 4(2), 1991, pages 151 to 158
    locator: the two-move bit commitment from a generator that stretches n bits to 3n bits, and the binding error 2^(-n)
  - url: "https://cs.au.dk/~ivan/ComZK06.pdf"
    title: Ivan Damgard and Jesper Buus Nielsen, Commitment schemes and zero-knowledge protocols, lecture notes, Aarhus University
    locator: the sections on commitment schemes (the definitions of unconditional and computational hiding and binding, and why both cannot be unconditional)
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 4, the section on commitment schemes (definition, the scheme from a one-way permutation with a hard-core predicate, and Naor's scheme)
  - paper: "Mihir Bellare and Phillip Rogaway, Random oracles are practical: a paradigm for designing efficient protocols, ACM CCS 1993, pages 62 to 73"
    locator: the random oracle model, in which the hash commitment H(r || m) is analysed
  - paper: "Russell Impagliazzo and Michael Luby, One-way functions are essential for complexity based cryptography, FOCS 1989, pages 230 to 235"
    locator: the result that computationally secure bit commitment implies a one-way function
  - paper: "Iftach Haitner, Minh-Huyen Nguyen, Shien Jin Ong, Omer Reingold and Salil Vadhan, Statistically hiding commitments and statistical zero-knowledge arguments from any one-way function, SIAM Journal on Computing 39(3), 2009"
    locator: the construction of statistically hiding commitments from any one-way function
  - paper: "Johan Hastad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), 1999, pages 1364 to 1396"
    locator: the main theorem (a pseudorandom generator exists if a one-way function exists), which with Naor's scheme gives statistically binding commitments
---

A commitment scheme is a two-phase protocol in which a committer fixes a value $m$ now and reveals it later. In the *commit* phase the committer sends a commitment $c$. In the *open* phase it sends $m$ and the randomness that was used, and the receiver checks them against $c$. The scheme must be *hiding* ($c$ tells the receiver nothing about $m$) and *binding* (the committer cannot open $c$ to a different value). It is the electronic form of a sealed envelope, and it is the first step of [fair coin flipping](/fair-coin-flipping/), of [zero-knowledge proofs](/zero-knowledge-proof/) for all of NP and of [verifiable secret sharing](/verifiable-secret-sharing/).

**Notation.** $\lambda$ is the security parameter. $m$ is the message from a message space $M$, $r$ the randomness of the committer, $c = \mathrm{Com}(m; r)$ the commitment. $A$ is an adversary, $t$ its running time, and $q$ its number of queries to a hash oracle when there is one. $H$ is a hash function, here SHA-256. $G$ is a pseudorandom generator.

## In plain words

You write your guess on a sheet of paper, seal it in an envelope and hand the envelope to a friend. The friend cannot see the guess, so the envelope *hides* it. Later you open the envelope together, and you cannot change what is inside, so the envelope *binds* you.

A commitment scheme does the same with numbers. The usual way is to hash the value together with a long random string and send the hash. To open, you send the value and the random string, and the friend hashes them again. The random string matters: without it, the friend can hash every possible value and find yours.

A scheme cannot hide perfectly and bind perfectly at the same time. One of the two must rest on a problem that is only hard to solve, not impossible.

## Definition

A (non-interactive) commitment scheme is a pair of efficient algorithms. $\mathrm{Com}(m; r)$ maps a message $m \in M$ and randomness $r$ to a commitment $c$. $\mathrm{Open}(c, m, r)$ outputs accept or reject. Some schemes have a public setup value (Pedersen's $h$) or a first message of the receiver (Naor's $R$); then both algorithms also take it as input, and the definitions below hold for each fixed value of it, chosen honestly.

- **Correctness.** $\mathrm{Open}(\mathrm{Com}(m; r), m, r)$ accepts for every $m$ and $r$.
- **Hiding.** In the hiding game the adversary $A$ picks $m_0, m_1 \in M$, receives $c = \mathrm{Com}(m_b; r)$ for a uniform bit $b$ and fresh $r$, and outputs a bit $b'$. Its advantage is $\mathrm{Adv}^{\mathrm{hide}}(A) = |\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$. The scheme is *perfectly* hiding if the advantage is 0 for every $A$, *statistically* hiding if it is negligible in $\lambda$ for every $A$ with no bound on its time, and *computationally* hiding if it is negligible for every $A$ that runs in time polynomial in $\lambda$.
- **Binding.** In the binding game $A$ outputs $(c, m, r, m', r')$ and wins if $m \ne m'$ and $\mathrm{Open}$ accepts both $(c, m, r)$ and $(c, m', r')$. The scheme is *perfectly* binding if no $A$ can win, *statistically* binding if every $A$ wins with negligible probability (the probability is over the setup or the receiver's message), and *computationally* binding if every polynomial time $A$ wins with negligible probability.

Perfect hiding means that the distributions of $\mathrm{Com}(m_0; r)$ and $\mathrm{Com}(m_1; r)$ are equal for all $m_0, m_1$. Statistical hiding means that their statistical distance is negligible. Computational hiding means that they are [computationally indistinguishable](/computational-indistinguishability/).

## Variants

- **Bit and string commitments.** Blum and Naor commit to one bit. A string commitment commits to a whole value at once; the hash and [Pedersen](/pedersen-commitment/) schemes do this. Bit commitments to each bit of a string give a string commitment, at a cost in length.
- **Interactive and non-interactive.** Naor's scheme needs a first message from the receiver. The hash commitment and Pedersen's scheme need one message, but Pedersen's needs a setup value $h$ whose discrete log nobody knows.
- **Homomorphic commitments.** Pedersen commitments multiply to a commitment of the sum. [Sigma protocols](/sigma-protocol/) and [verifiable secret sharing](/verifiable-secret-sharing/) use this.
- **Trapdoor (equivocal) commitments.** Whoever knows a trapdoor can open a commitment to any value; the others are still bound. Pedersen's scheme with the trapdoor $\log_g h$ is the standard example. Simulators of zero-knowledge protocols use such trapdoors.
- **[Non-malleable](/non-malleability/) commitments.** Seeing a commitment to $m$ does not help an adversary to commit to a related value such as $m + 1$. Sealed-bid auctions need this, and plain hash commitments do not give it in the standard model.
- **Vector and polynomial commitments.** Commit to a long vector or a polynomial with a short value and open single positions. A [Merkle tree](/merkle-tree/) root is a vector commitment; KZG commitments (see [zk-SNARK](/zk-snark/)) commit to polynomials.

## Examples

**The hash commitment.** Let $r$ be the 32 bytes $00, 01, \ldots, 1f$ (hex) and $m$ the three bytes `yes`. Then $c = \mathrm{SHA256}(r \| m)$ begins with `f45861e6 b753b170`, and for $m$ = `no` with the same $r$ it begins with `ae49f2e0 d0373a6a`. To open, the committer sends $r$ and $m$. In real use $r$ is fresh and uniform each time.

**Naor's bit commitment.** Let $G$ stretch $n$ bits to $3n$ bits. The receiver sends a uniform $R \in \{0, 1\}^{3n}$. The committer picks a uniform seed $s \in \{0,1\}^n$ and sends $c = G(s)$ for $b = 0$ or $c = G(s) \oplus R$ for $b = 1$. It opens with $(b, s)$. With the toy size $n = 8$ and $G$ built from SHA-256 in counter mode, $G(3) = $ `a665e6` and $G(200) = $ `32503b` (hex). For the receiver's message $R = $ `9435dd` $= G(3) \oplus G(200)$, the commitment `a665e6` opens to 0 with seed 3 and to 1 with seed 200. Such *bad* values of $R$ are rare: among all $2^{24}$ strings, exactly 32614 are of the form $G(s_0) \oplus G(s_1)$, a fraction of $0.0019 \le 2^{-8}$.

**Non-example: no randomness.** $c = H(m)$ is binding when $H$ is [collision resistant](/collision-resistance/), but it is not hiding when $M$ is small. For a sealed bid between 0 and 999, the receiver hashes all 1000 bids and finds the one that matches $c$.

**Non-example: a one-time pad.** $c = m \oplus k$ with a uniform key $k$ opened by $k$ is perfectly hiding, but not binding: for every $m'$ the key $k' = c \oplus m'$ opens $c$ to $m'$. The theorem in Bounds shows that every perfectly hiding scheme has this weakness against a committer with unlimited time.

## Known algorithms

| scheme | hiding | binding | assumption |
|---|---|---|---|
| hash commitment $H(r \| m)$ | statistical in the ROM | computational | [random oracle model](/random-oracle-model/); binding also from [collision resistance](/collision-resistance/) |
| Naor (1991) | computational | statistical, error $2^{-n}$ | a [pseudorandom generator](/pseudorandom-generator/) |
| from a one-way permutation $f$ with hard-core bit $\beta$: $(f(x), \beta(x) \oplus b)$ | computational | perfect | a [one-way](/one-way-function/) permutation and its [hard-core predicate](/hard-core-predicate/) |
| [Pedersen](/pedersen-commitment/) $g^m h^r$ | perfect | computational | the [discrete logarithm problem](/discrete-logarithm-problem/) |
| ElGamal-type $(g^r, g^m h^r)$ | computational | perfect | the [decisional Diffie-Hellman](/decisional-diffie-hellman/) assumption |

In the random oracle model with an oracle of 256-bit output and a 256-bit $r$, an adversary that makes $q$ oracle queries breaks hiding only by querying $r \| m_b$, with probability at most $q \cdot 2^{-256}$, and breaks binding only by finding a collision, with probability at most about $q^2 / 2^{257}$. In the standard model, collision resistance gives binding, but hiding needs more than collision resistance, because a collision resistant $H$ can leak some bits of its input.

Naor's scheme is binding with error $2^{-n}$ because a commitment opens both ways only if $R = G(s_0) \oplus G(s_1)$ for some seeds. There are at most $2^{2n}$ such strings among $2^{3n}$, so a uniform $R$ is bad with probability at most $2^{-n}$, against a committer with unlimited time. Hiding holds because a distinguisher between $G(s)$ and $G(s) \oplus R$ distinguishes $G(s)$ from uniform: both $G(s)$ and $G(s) \oplus R$ are computationally indistinguishable from a uniform string.

The code on this page implements the hash commitment and Naor's scheme. The tests check opening, a chi-square test of the first byte of commitments to two values, Naor's binding bound by exhaustive search at $n = 8$, a double opening for a bad $R$, the search attack on $H(m)$ without randomness, and a birthday double opening when the hash is cut to 20 bits. There are no official test vectors for these schemes. The code is for study only, is not constant time, and must not be used to protect real data; use a reviewed protocol on top of libsodium or a FIPS 140 validated module.

## Bounds

**Theorem.** No commitment scheme is both perfectly hiding and perfectly binding. More generally, if it is statistically hiding with distance $\varepsilon$, a committer with unlimited time can open with probability at least $1 - \varepsilon$ to a second value.

*Proof.* Fix the setup or the receiver's first message. Let $m_0 \ne m_1$ and let $D_0$ and $D_1$ be the distributions of $\mathrm{Com}(m_0; r)$ and $\mathrm{Com}(m_1; r)$. If the scheme is perfectly hiding, $D_0 = D_1$, so they have the same support. The honest committer outputs $c$ in the support of $D_0$, which is then also in the support of $D_1$, so there is an $r'$ with $\mathrm{Com}(m_1; r') = c$. A committer with unlimited time finds $r'$ by search and opens $c$ to $m_1$: perfect binding fails. If the statistical distance of $D_0$ and $D_1$ is $\varepsilon$, then the probability under $D_0$ of the set of $c$ outside the support of $D_1$ is at most $\varepsilon$, so with probability at least $1 - \varepsilon$ the honest $c$ also opens to $m_1$. In the other direction, perfect binding means that the supports of $D_0$ and $D_1$ are disjoint, so a receiver with unlimited time reads $m$ from $c$, and the scheme is not even statistically hiding. $\square$

So one property must be computational. Pedersen's scheme gives up computational binding for perfect hiding, and Naor's scheme gives the other choice.

**Assumptions.** Impagliazzo and Luby (1989) showed that a computationally secure bit commitment implies a one-way function. In the other direction, a [one-way function](/one-way-function/) gives a pseudorandom generator (Hastad, Impagliazzo, Levin and Luby) and so Naor's statistically binding scheme, and Haitner, Nguyen, Ong, Reingold and Vadhan (2009) built statistically hiding commitments from any one-way function. So commitments of both kinds exist if and only if one-way functions exist.

**Cost.** The hash commitment costs one hash call to commit and one to open, and $c$ has the length of the digest. Naor's scheme costs one call to $G$ and $3n$ bits of communication for each committed bit. Pedersen's scheme costs two exponentiations in the group.

## Reductions

- **Pseudorandom generator to commitment.** Naor's scheme above; the binding argument uses no assumption, and a hiding adversary is a distinguisher for $G$.
- **Discrete log to binding.** A committer who opens a Pedersen commitment two ways computes $\log_g h$ (see [Pedersen commitment](/pedersen-commitment/)).
- **Commitment to coin flipping.** One party commits to a bit, the other sends a bit in the clear, and the output is the XOR (see [fair coin flipping](/fair-coin-flipping/)).
- **Commitment to zero knowledge for NP.** The prover commits to a random recoloring of a 3-coloring and opens one edge (see [zero-knowledge proof](/zero-knowledge-proof/)).
- **Commitment from oblivious transfer** and oblivious transfer from commitments plus more structure are studied in [secure multiparty computation](/secure-multiparty-computation/); see [oblivious transfer](/oblivious-transfer/).

## Applications

- **Coin flipping and randomness beacons.** Commit then reveal, as in Blum's protocol.
- **Zero-knowledge proofs and [sigma protocols](/sigma-protocol/).** The first move of a sigma protocol acts as a commitment to the prover's randomness.
- **Sealed-bid auctions and voting.** Each bidder commits to a bid; all open after the deadline. Non-malleability matters here.
- **[Verifiable secret sharing](/verifiable-secret-sharing/).** The dealer commits to the coefficients of the sharing polynomial so that each party can check its share.
- **Succinct proofs.** [zk-SNARKs](/zk-snark/) commit to polynomials, and [zk-STARKs](/zk-stark/) commit to long vectors with a [Merkle tree](/merkle-tree/).

## References
