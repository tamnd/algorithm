---
tag: 571HZE
kind: algorithm
slug: mix-network
name: Mix network
aliases:
- mixnet
- Chaumian mix
- re-encryption mix
area: cryptography/protocols
level: advanced
summary: A chain of servers that each collect a batch of encrypted messages, change their encryption and output them in a random order, so that one honest server hides who sent what.
solves: [anonymous-communication]
model: word-ram
complexity:
  vars: {N: the number of messages in a batch, K: the number of mixes in the cascade, T: the number of trustees who decrypt}
  time: {worst: O((K + T) N), average: O((K + T) N), best: O((K + T) N)}
  space: {extra: O(N)}
properties: {deterministic: false, randomized: true}
history:
  year: 1981
  people: [David Chaum]
  note: Chaum proposed decryption mixes in 1981; Park, Itoh and Kurosawa gave re-encryption mixes in 1993, and Sako and Kilian and then Neff gave verifiable shuffles in 1995 and 2001.
prereqs: [elgamal-encryption, random-permutation]
see_also: [anonymous-communication, dining-cryptographers, decisional-diffie-hellman, threshold-cryptography, zero-knowledge-proof, cut-and-choose, fisher-yates-shuffle]
sources:
  - paper: doi:10.1145/358549.358563
    title: David Chaum, Untraceable electronic mail, return addresses, and digital pseudonyms, Communications of the ACM 24(2), 1981, pages 84 to 90
    locator: the mix, which removes one layer of public-key encryption from each message of a batch and outputs the batch in a fixed order; cascades of mixes; untraceable return addresses
  - paper: "Choonsik Park, Kazutomo Itoh and Kaoru Kurosawa, Efficient anonymous channel and all/nothing election scheme, Eurocrypt 1993, LNCS 765, pages 248 to 259"
    locator: mixes that re-encrypt ElGamal ciphertexts, so that the ciphertext does not grow with the number of mixes
  - paper: "Kazue Sako and Joe Kilian, Receipt-free mix-type voting scheme, Eurocrypt 1995, LNCS 921, pages 393 to 403"
    locator: a universally verifiable mix with a cut-and-choose proof that the output is a permuted re-encryption of the input
  - paper: doi:10.1145/501983.502000
    title: C. Andrew Neff, A verifiable secret shuffle and its application to e-voting, ACM CCS 2001, pages 116 to 125
    locator: an honest-verifier zero-knowledge proof of a shuffle of ElGamal ciphertexts with a cost linear in the number of ciphertexts
  - paper: doi:10.1109/SP.2009.15
    title: George Danezis and Ian Goldberg, Sphinx, a compact and provably secure mix format, IEEE Symposium on Security and Privacy 2009, pages 269 to 282
    locator: the packet header with one shared group element blinded at each hop, the padding that hides the position on the path, and the security proof
  - paper: "Ania M. Piotrowska, Jamie Hayes, Tariq Elahi, Sebastian Meiser and George Danezis, The Loopix anonymity system, USENIX Security Symposium 2017, pages 1199 to 1216"
    locator: continuous mixing with exponential delays, loop and drop cover traffic, and a stratified topology
  - paper: "Andrei Serjantov, Roger Dingledine and Paul Syverson, From a trickle to a flood, active attacks on several mix types, Information Hiding 2002, LNCS 2578, pages 36 to 52"
    locator: the n - 1 (flooding and trickle) attacks on threshold, timed and pool mixes
---

A mix network hides who sent which message by passing a batch of encrypted messages through a chain of servers, called mixes. Each mix changes the encryption of every message in the batch, so that its outputs look unrelated to its inputs, and sends them out in a random order. An observer who sees every link, and who runs all the other mixes, still cannot match an output to an input if one mix in the chain is honest. Chaum proposed mixes in 1981, for untraceable email; the variant on this page, a cascade of ElGamal re-encryption mixes, is the one used to shuffle votes in electronic elections, because each mix can prove that it did not drop or change a message.

**Notation.** $p = 2q + 1$ is a safe prime and $g$ generates the subgroup $\mathbb{G}$ of prime order $q$. Trustees $1, \ldots, T$ hold secret keys $x_j$, and $y = g^{x_1 + \cdots + x_T}$ is the joint public key. A ciphertext is a pair $c = (a, b) = (g^r, m y^r)$. $N$ is the number of messages in a batch and $K$ the number of mixes. $\pi$ is a permutation of $\{1, \ldots, N\}$.

## In plain words

A town votes by post. Each voter puts the ballot in a locked box that only the counting committee can open, and writes nothing else on it. The boxes go to a first clerk, who repaints each box so that it looks new, shakes them all in a sack, and passes the sack on. A second clerk repaints and shakes again, and so does a third.

At the end the committee opens the boxes and counts. Nobody can say which ballot came from which voter, as long as one clerk shook the sack honestly and kept quiet about it. A clerk could cheat by swapping a box for one of their own, so each clerk also shows, without telling the order, that the sack holds the same ballots as before.

## The problem

$N$ senders each want to deliver one message, so that everyone can see the full set of messages but nobody can tell which sender sent which message. The adversary watches every link, may control all mixes but one, and may control some senders. It must not be able to link an output to its sender with probability better than a guess among the honest senders. In voting, the output must also be correct: no mix may drop, add or change a message without being caught. This is the relationship and sender anonymity part of [anonymous communication](/anonymous-communication/) in a setting with batches.

## The algorithm

```pseudo id=main
Setup
L1  each trustee j: x_j ← random in Z_q; publish h_j = g^(x_j); y ← h_1 · … · h_T
L2  each sender: r ← random in Z_q; post c = (g^r, m · y^r) on the bulletin board
Each mix, on the batch c_1 … c_N from the board                       ▷ re-encryption mix
L3  π ← a uniform random permutation of {1 … N}                      ▷ Fisher-Yates
L4  s_1 … s_N ← random in Z_q
L5  for i ← 1 to N: c'_π(i) ← (a_i · g^(s_i), b_i · y^(s_i))
L6  post c'_1 … c'_N, with a proof that c' is a permuted re-encryption of c; erase π and s
L7  the next mix takes c' as its input; lines L3 to L6 run once for each of the K mixes
After the last mix
L8  for each (a, b) of the final batch: each trustee j posts d_j = a^(x_j), with a proof of correct decryption
L9  m ← b / (d_1 · … · d_T)
```

**Re-encryption.** $(g^s, y^s)$ is an encryption of $1$, and multiplying a ciphertext by it (line L5) gives a new, random-looking ciphertext of the same message, because $b y^s / (a g^s)^x = b / a^x$. This is the multiplicative homomorphism of [ElGamal encryption](/elgamal-encryption/). The mixes need no key, the ciphertext does not grow, and the trustees decrypt only the final, shuffled batch (lines L8 and L9).

**Why one honest mix is enough.** Under the [decisional Diffie-Hellman](/decisional-diffie-hellman/) assumption, $(g^s, y^s)$ cannot be told from a uniform pair when $x$ is unknown, so the outputs of an honest mix look like fresh random pairs, whatever the inputs were. The overall permutation is $\pi_K \circ \cdots \circ \pi_1$, and one uniform factor makes it uniform.

**Proofs of shuffle.** A dishonest mix could replace a ciphertext by one of its own, which changes the election without being seen. So each mix proves in line L6 that its output is a permuted re-encryption of its input, in zero knowledge, without telling $\pi$. Sako and Kilian (Eurocrypt 1995) gave a cut-and-choose proof: the mix makes a second, shadow shuffle of the input, and a random bit decides whether it opens the path from the input to the shadow or from the shadow to the output. A cheating mix can answer at most one of the two, so each round catches it with probability $1/2$. Neff (CCS 2001) gave a proof with a cost linear in $N$ and no repetition, and later proofs by Furukawa and Sako, Groth, and Bayer and Groth are shorter still. With the Fiat-Shamir heuristic the proofs become non-interactive, and anyone can check the whole election from the board. The trustees in line L8 likewise prove that each $d_j$ is correct, with a Chaum-Pedersen proof, and they can use a [threshold](/threshold-cryptography/) key instead of $T$-of-$T$ shares.

**Decryption mixes.** Chaum's original mix (1981) works differently. A sender encrypts a message in layers, $E_1(E_2(\cdots E_K(m)))$, with the public keys of the $K$ mixes in order. Each mix decrypts its layer for every message in the batch, removes duplicates to stop replays, sorts or shuffles the results and sends them on. Each layer adds length, unless the format hides it, and no mix can prove its shuffle as simply. Onion routing and anonymous email use decryption mixes, and voting uses re-encryption mixes.

**Sphinx.** Danezis and Goldberg (IEEE S&P 2009) gave a compact packet format for decryption mixes. The header holds one group element $\alpha = g^x$. Each mix computes a shared secret $\alpha^{x_i}$ with its own key, derives from it the keys to remove its layer of the routing information and to check a MAC, and blinds the group element for the next hop as $\alpha^{b_i}$ with a blinding factor $b_i$ derived from the secret. The header is padded so that its length is the same at every hop, so a mix does not learn its position on the path, and the payload is encrypted with a wide-block cipher, so a changed payload becomes random. Sphinx headers are small, and the format has a security proof. Modern mix networks use it.

**Loopix.** Piotrowska, Hayes, Elahi, Meiser and Danezis (USENIX Security 2017) replaced batches with continuous mixing: each mix delays each message by an independent exponential time, chosen by the sender, so the output order is random without a batch size to attack. Clients send at a steady rate of real and cover messages (Poisson processes), including drop messages that are thrown away and loop messages that come back to the sender and reveal active attacks. Mixes are arranged in layers. Loopix trades a latency of seconds for resistance to a global passive adversary, which Tor does not give, and is the basis of the Nym network.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data; for real use, take a reviewed implementation with a non-interactive proof of shuffle, such as Verificatum. It works in the subgroup of order $q$ modulo the toy 128-bit safe prime $p = 2^{127} + 8799$, with $g = 4$; real systems use groups of 2048 bits or elliptic curves. The trustees hold $T$-of-$T$ additive shares and do not prove their decryption shares. The proof of shuffle is the interactive cut-and-choose proof described above, with a random challenge bit in each round, not the proof of Neff. Re-encryption mixes have no official test vectors, so the tests check the properties of the next sections.

## Example

Four voters send $3$, $1$, $2$ and $3$ through two mixes. $E(s)$ is $(g^s, y^s)$, and the column "plaintexts" gives what each position of the board would decrypt to.

| Step | Line | Board | Plaintexts | Sources |
|---|---|---|---|---|
| 1 | L2 | $c_1, c_2, c_3, c_4$ from Alice, Bob, Carol and Dave | $3, 1, 2, 3$ | A, B, C, D |
| 2 | L3 to L6 | mix 1 with $\pi_1 = (3, 1, 4, 2)$: $c'_3 = c_1 E(s_1)$, $c'_1 = c_2 E(s_2)$, $c'_4 = c_3 E(s_3)$, $c'_2 = c_4 E(s_4)$ | $1, 3, 3, 2$ | B, D, A, C |
| 3 | L3 to L6 | mix 2 with $\pi_2 = (4, 1, 3, 2)$: $c''_4 = c'_1 E(\cdot)$, $c''_1 = c'_2 E(\cdot)$, $c''_3 = c'_3 E(\cdot)$, $c''_2 = c'_4 E(\cdot)$ | $3, 2, 3, 1$ | D, C, A, B |
| 4 | L8, L9 | the trustees decrypt $c''_1, \ldots, c''_4$ | $3, 2, 3, 1$ | |

No component of $c'$ or $c''$ equals one of $c$, so the board itself does not show the permutation. If mix 1 is dishonest and tells its $\pi_1$, the link is still hidden by $\pi_2$, and the other way round. The count is two votes for $3$, one for $2$ and one for $1$, as in the input.

A run of the code checks the same properties on larger batches. After a cascade of four mixes, the decrypted outputs equal the inputs as a multiset, at every stage. The input and output of one mix share no group element. Against a mix that re-encrypts but does not reorder, linking by position finds every link. Against a real mix, linking by position, or by matching the sorted order of the first components, finds about one link in eight for batches of eight, which is the rate of a guess. The cut-and-choose proof accepts an honest mix and rejects a mix that swapped one ciphertext for its own. On a threshold mix with batches of eight, an attacker who holds back all honest messages but the target's and adds seven of its own learns the target's plaintext with certainty.

## Correctness

Re-encryption keeps the plaintext: $(a g^s, b y^s)$ decrypts to $b y^s / (a^x g^{sx}) = b / a^x$. Each mix applies a bijection from input positions to output positions, so the multiset of plaintexts is the same after every mix. The joint decryption gives $a^{x_1} \cdots a^{x_T} = a^x$, so lines L8 and L9 output the multiset of the messages that the senders encrypted.

For hiding, a hybrid argument replaces the encryptions of $1$ of an honest mix, one at a time, with uniform pairs; each step is a DDH instance. After all steps, the output is a list of uniform pairs, independent of $\pi$, so an adversary links an output to its input with probability at most $1/N$ plus $N$ times its DDH advantage. The cut-and-choose proof is complete, rejects a wrong output with probability $1 - 2^{-k}$ after $k$ rounds, and reveals nothing about $\pi$ to an honest verifier. The proof page gives the full arguments, and shows that the $n - 1$ attack below works with probability $1$ against a threshold mix.

## Complexity

Each mix does two exponentiations per message, for $g^{s_i}$ and $y^{s_i}$, so a cascade of $K$ mixes costs $2KN$ exponentiations. Decryption costs $T$ exponentiations per message, and the proofs of decryption a constant number more. So the total is $O((K + T) N)$ exponentiations, each of $O(\log q)$ multiplications in the group, and a mix stores $O(N)$ ciphertexts and the witness $(\pi, s)$. A proof of shuffle adds work: the cut-and-choose proof costs $2N$ exponentiations per round for the mix and for the verifier, so $O(kN)$ for $k$ rounds, while Neff's proof and its successors cost $O(N)$ exponentiations with a small constant. The latency of the cascade is $K$ times the time of one mix, and the batch size $N$ is the anonymity set.

## Properties

- **Anonymity from one honest mix.** The link is hidden if at least one mix shuffles honestly and erases its permutation, and the key is not known to the adversary.
- **Universal verifiability.** With proofs of shuffle and of decryption on a public board, anyone can check that the output is the decrypted, permuted input.
- **Robustness.** A mix that fails its proof is removed and its input is passed to the next mix, so a dishonest mix can stop the run only for a short time.
- **Information hiding rests on computation.** The hiding depends on the DDH assumption; a quantum computer would break it later for recorded boards.
- **High latency.** Batches make users wait for each other, which suits voting and email, not web browsing.

## Variants and improvements

- **Decryption mixes and Sphinx.** Layered encryption, peeled by each mix. Sphinx packets have a fixed size and hide the position on the path.
- **Re-encryption and universal re-encryption.** ElGamal re-encryption needs only the trustees' public key. Universal re-encryption (Golle, Jakobsson, Juels and Syverson, 2004) re-encrypts without knowing the public key at all.
- **Batching strategies.** A threshold mix flushes after $N$ messages, a timed mix every $t$ seconds, and a pool mix keeps a random part of the batch for the next round, which makes the $n - 1$ attack slower. Stop-and-go mixes and Loopix delay each message by a random time.
- **Topologies.** A cascade sends every message through the same mixes. A free-route network lets each sender choose a path, and a stratified network has layers of mixes with any path through them. Cascades give the largest anonymity sets; free routes scale better.
- **Verifiable shuffles.** Sako and Kilian (1995) gave the first universally verifiable mix with a cut-and-choose proof. Neff (2001) and Furukawa and Sako (2001) gave proofs of linear cost, and Bayer and Groth (Eurocrypt 2012) gave proofs with sublinear communication. Verificatum implements a proof of shuffle by Terelius and Wikström.
- **Hybrid mixes.** To mix long messages, mixes use public-key encryption for a short header and symmetric encryption for the body.

## When to use it

Use a re-encryption mix cascade with proofs of shuffle when a batch of messages, such as ballots, must be made anonymous and the result must be publicly verifiable; this is the usual choice for internet voting with a mixnet. Use a decryption mix network with Sphinx packets and cover traffic, as in Loopix, for messaging that must resist a global passive adversary and can wait seconds. Use onion routing, as in Tor, when latency matters more than resistance to a global observer. For a small group that needs anonymity against any adversary, consider a [dining cryptographers](/dining-cryptographers/) network.

## Pitfalls

- **The $n - 1$ attack.** An active attacker who controls the links into a threshold mix can hold back all honest messages but one and fill the batch with its own, so it knows every output but the target's. Defend with pool mixes, cover traffic and loop messages that detect blocking, and limits on how many messages one sender may submit.
- **Copied inputs.** An attacker who submits a re-encryption of an honest voter's ciphertext as its own input sees two equal plaintexts in the output, which shows the voter's choice. Each sender must prove in zero knowledge that it knows its plaintext and randomness, and duplicate inputs must be rejected.
- **No proof of shuffle.** Without proofs, one dishonest mix can change votes. Check every proof before the decryption.
- **Bad randomness.** A permutation that is not uniform, or an exponent that repeats, gives the link away. Use Fisher-Yates with a cryptographic random source.
- **Textbook RSA in a decryption mix.** Chaum's direct use of RSA was broken by Pfitzmann and Pfitzmann (Eurocrypt 1989), who linked messages with the multiplicative property of RSA. Use randomized, authenticated layers.
- **Small batches and long-term patterns.** A batch of $N$ messages hides each sender among at most $N$; a user who sends often to one receiver is found by intersection attacks over many batches.

## Implementations

## History

David Chaum proposed the mix in 1981, in "Untraceable electronic mail, return addresses, and digital pseudonyms", together with cascades of mixes and untraceable return addresses. Park, Itoh and Kurosawa introduced re-encryption mixes for voting in 1993, and Sako and Kilian made them universally verifiable in 1995. Neff gave an efficient zero-knowledge proof of a shuffle in 2001, the same year as Furukawa and Sako. Remailer networks such as Mixmaster and Mixminion (2003) put decryption mixes into use for email, Serjantov, Dingledine and Syverson studied active attacks on batching in 2002, and Danezis and Goldberg designed Sphinx in 2009. Loopix in 2017 brought continuous mixing and cover traffic, and verifiable re-encryption mixnets are now part of internet voting systems in several countries.

## References
