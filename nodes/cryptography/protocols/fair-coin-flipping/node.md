---
tag: 5SB3X8
kind: problem
slug: fair-coin-flipping
name: Fair coin flipping
aliases:
- coin flipping over the phone
- Blum coin flipping
area: cryptography/protocols
level: advanced
summary: "Two parties who do not trust each other agree on a random bit. Blum's protocol uses a commitment; a party who aborts can bias any r-round protocol by Ω(1/r) (Cleve 1986)."
prereqs: [commitment-scheme]
see_also: [pedersen-commitment, secure-multiparty-computation, malicious-adversary-model, oblivious-transfer, verifiable-secret-sharing, rabin-randomized-byzantine-agreement, verifiable-random-function]
sources:
  - paper: doi:10.1145/1008908.1008911
    title: "Manuel Blum, Coin flipping by telephone: a protocol for solving impossible problems, ACM SIGACT News 15(1), 1983, pages 23 to 27 (first given at CRYPTO 1981, report pages 11 to 15)"
    locator: the protocol in which Alice commits to a guess, Bob flips in the clear, and Alice opens
  - paper: doi:10.1145/12130.12168
    title: Richard Cleve, Limits on the security of coin flips when half the processors are faulty, STOC 1986, pages 364 to 369
    locator: the lower bound that every r-round two-party coin flipping protocol can be biased by Ω(1/r) by a party who aborts
  - paper: doi:10.1007/978-3-642-00457-5_1
    title: Tal Moran, Moni Naor and Gil Segev, An optimally fair coin toss, TCC 2009, LNCS 5444, Springer, pages 1 to 18 (full version in Journal of Cryptology 29(3), 2016)
    locator: the r-round protocol with bias O(1/r) from oblivious transfer, and the discussion of the majority protocol with bias Θ(1/r^(1/2))
  - paper: "Itay Berman, Iftach Haitner and Aris Tentes, Coin flipping of any constant bias implies one-way functions, STOC 2014"
    locator: the main theorem (a coin flipping protocol with constant bias below 1/2 gives a one-way function)
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 7 (general cryptographic protocols), the coin tossing into the well functionality and security with abort
  - url: "https://cs.au.dk/~ivan/ComZK06.pdf"
    title: Ivan Damgard and Jesper Buus Nielsen, Commitment schemes and zero-knowledge protocols, lecture notes, Aarhus University
    locator: the sections on commitment schemes and their use in coin flipping
---

Fair coin flipping is the problem of two parties who do not trust each other and must agree on one uniform random bit over a network. Blum (1981) solved it with a [commitment](/commitment-scheme/): Alice commits to a random bit $a$, Bob sends a random bit $b$ in the clear, Alice opens $a$, and both output $a \oplus b$. Neither party can bias the result while both finish the protocol. But the party who learns the result first can abort, and Cleve (1986) proved that in every $r$-round protocol some party can bias the output by $\Omega(1/r)$ this way. Moran, Naor and Segev (2009) gave a protocol that meets this bound.

**Notation.** $\lambda$ is the security parameter. Alice and Bob are the parties; $A$ is an adversary that controls one of them, runs in time polynomial in $\lambda$ and may stop at any point. $r$ is the number of rounds. The *bias* of $A$ is $|\Pr[\text{honest party outputs } 1] - 1/2|$. $H$ is SHA-256, and $\mathrm{Com}$ the hash commitment $H(\rho \| a)$ with 32 random bytes $\rho$.

## In plain words

Alice and Bob talk on the phone and want to settle a bet with a coin toss. If Alice tosses and tells Bob the result, Bob must trust her. If Alice says her guess first, Bob can then say the result that makes her lose.

Blum's idea is to seal Alice's guess first. Alice puts her random bit in a locked box and sends the box. Bob then says his own random bit out loud. Alice opens the box, and the result is whether the two bits differ. Bob could not use Alice's bit, because the box hid it. Alice could not change her bit, because the box was sealed.

One problem remains. Alice sees the result before Bob does. If she does not like it, she can hang up. No protocol fixes this fully, but protocols with more rounds can make the gain small.

## Definition

A two-party coin flipping protocol is a pair of efficient interactive algorithms. In an honest execution both parties output the same bit, and the bit is uniform.

- **Bias with abort, the fair model.** An adversary $A$ controls one party and may deviate in any way, including stopping early. The honest party must still output a bit. The protocol has bias $\varepsilon$ if for every efficient $A$, $|\Pr[\text{honest output} = 1] - 1/2| \le \varepsilon$ (and the same for 0), up to a negligible term. This is the notion of Cleve and of Moran, Naor and Segev.
- **Security with abort.** The honest party may output a special symbol "abort" instead of a bit. The protocol is secure if, conditioned on no abort, the output is uniform up to a negligible term, and if the adversary cannot both see the output and decide to abort without being caught. In this weaker model Blum's protocol is secure: it is the standard *coin tossing into the well* used to start general [secure multiparty computation](/secure-multiparty-computation/) against a [malicious adversary](/malicious-adversary-model/).

## Variants

- **Weak and strong coin flipping.** In weak coin flipping each party has a preferred outcome and only bias toward it matters; in strong coin flipping no bias in either direction is allowed. The distinction matters most for quantum protocols; Cleve's attack on classical protocols works in either form, because the attacker picks the direction of its bias.
- **Many parties.** With an honest majority, $n$ parties can flip with no bias at all: each party shares a random bit with [verifiable secret sharing](/verifiable-secret-sharing/), and the output is the XOR of all the shared bits, which the honest parties can always reconstruct. With a dishonest majority, Cleve's lower bound applies.
- **Coins with public verification.** A [verifiable random function](/verifiable-random-function/) or a threshold signature gives a random value that anyone can check, which is how randomness beacons work.
- **Information-theoretic coin flipping.** Without any computational assumption, one party with unlimited time can bias every two-party protocol completely. Blum's protocol needs a commitment, and so a [one-way function](/one-way-function/).

## Examples

**One run of Blum's protocol.** Alice picks $a = 1$ and $\rho$ = 32 bytes of value 07. She sends $c = H(\rho \| 01)$, which begins with `842ef3c3 b4e4a5b4`. Bob picks $b = 0$ and sends it. Alice sends $(a, \rho) = (1, \rho)$. Bob checks that $H(\rho \| 01) = c$ and both output $a \oplus b = 1$. A commitment to $a = 0$ with the same $\rho$ would begin with `156324ad c0a9d53a`, so Bob cannot read $a$ from $c$ unless he finds $\rho$.

**The abort attack.** Alice wants 1. After Bob's bit she knows $a \oplus b$. If it is 0 she does not open. If Bob then outputs a fresh random bit, $\Pr[\text{output} = 1] = 1/2 + 1/2 \cdot 1/2 = 3/4$, a bias of $1/4$. In 4000 simulated runs the measured frequency is within 0.04 of 0.75. If Bob outputs a fixed default bit on abort, an Alice who wants that bit always gets it: a bias of $1/2$. So the honest party should never use a fixed default.

**Non-example: no commitment.** If Alice sends $a$ in the clear first, Bob sends $b = a \oplus w$ for the bit $w$ that he wants, and the output is always $w$.

**The majority of $r$ flips.** Run Blum's protocol $r$ times ($r$ odd) and output the majority of the coins. If Alice aborts in round $i$, Bob tosses the coins $i$ to $r$ himself. The exact success of Alice's best strategy (she may abort once, after she sees a coin) follows by dynamic programming over the round and the number of ones so far:

| $r$ | $\Pr[\text{output} = 1]$ | bias | bias $\cdot \sqrt{r}$ |
|---|---|---|---|
| 1 | 3/4 | 0.250 | 0.250 |
| 3 | 11/16 | 0.188 | 0.325 |
| 5 | 21/32 | 0.156 | 0.349 |
| 9 | 319/512 | 0.123 | 0.369 |
| 25 | | 0.0775 | 0.387 |
| 81 | | 0.0439 | 0.395 |

The bias falls like $1/\sqrt{r}$, not like $1/r$: the attack gains whenever the coin she sees decides a close vote, and a sum of $r$ fair coins is close to the middle with probability of order $1/\sqrt{r}$.

## Known algorithms

Blum's protocol, with Bob honest:

```pseudo id=main
BLUM-FLIP()
L1  Alice: a ← uniform bit;  (c, ρ) ← Com(a);  send c
L2  Bob:   b ← uniform bit;  send b
L3  Alice: send (a, ρ)
L4  Bob:   if nothing arrives then
L5             output a uniform bit of his own        ▷ never a fixed default
L6         if the opening (a, ρ) of c is wrong then treat it as an abort
L7         output a ⊕ b
```

| protocol | rounds | bias against an aborting party | assumption |
|---|---|---|---|
| Blum (1981) | 1 flip | 1/4 (1/2 with a fixed default) | a commitment scheme |
| majority of $r$ Blum flips | $r$ | $\Theta(1/\sqrt{r})$ | a commitment scheme |
| Moran, Naor and Segev (2009) | $r$ | $O(1/r)$ | [oblivious transfer](/oblivious-transfer/) |

Moran, Naor and Segev fix in advance, inside a secure computation, a round $i^*$ that neither party knows. Before $i^*$ each party receives values that are independent of the output; from $i^*$ on they receive the real output. An aborting party does not know whether $i^*$ has passed, and the protocol is built so that an abort helps only if it happens exactly at $i^*$, which is an event of probability about $1/r$.

The code on this page implements Blum's protocol with the hash commitment, honest and cheating Alices as local objects, and the exact dynamic program for the majority protocol. The tests check that an honest run is fair, that an Alice who tries to open to the other bit gains no more than an abort, the bias of $1/4$ of the abort attack, the bias of $1/2$ against a fixed default, the exact values of the table, and a simulation that agrees with them. There are no official test vectors for coin flipping. The code is for study only, is not constant time, and must not be used to protect real data.

## Bounds

- **Lower bound (Cleve 1986).** For every two-party protocol of $r$ rounds that outputs a bit, there is an efficient adversary that controls one party, aborts at a time of its choice, and biases the honest party's output by $\Omega(1/r)$. The idea of the proof: after each message, let the *backup bit* of a party be the bit it would output if the other party stopped right then. Before the first message the backup bits do not depend on the final coin, and after the last message they equal it. So over the $2r$ messages they move by a constant amount in total, and some single message moves them by $\Omega(1/r)$ on average. The party who sends that message can stop just before it when the move would go against its wish. So no protocol has negligible bias with a polynomial number of rounds.
- **Upper bound (Moran, Naor and Segev 2009).** If oblivious transfer exists, for every $r$ there is an $r$-round protocol with bias $O(1/r)$. With Cleve's result, the optimal bias is $\Theta(1/r)$.
- **The majority protocol** reaches only $\Theta(1/\sqrt{r})$, as the table shows.
- **Security with abort.** If the honest party may output "abort", Blum's protocol has negligible bias when the commitment is hiding and binding, in one round of commit, answer and open.

## Reductions

- **Commitment to coin flipping.** Blum's protocol: hiding stops Bob from choosing $b$ as a function of $a$, and binding stops Alice from choosing $a$ as a function of $b$. A bias of Bob gives a distinguisher for the hiding game, and a bias of Alice beyond aborting gives a double opening.
- **Coin flipping to one-way functions.** Berman, Haitner and Tentes (2014) showed that a two-party coin flipping protocol with any constant bias below $1/2$ against efficient adversaries implies a one-way function; so some computational assumption is necessary.
- **Coin flipping inside general protocols.** A coin flip with abort gives the joint random string that many protocols need, for example the challenge of a public-coin [zero-knowledge proof](/zero-knowledge-proof/) made secure against a malicious verifier.

## Applications

- **Joint randomness in secure computation.** Coin tossing into the well fixes common random strings and random challenges among parties who do not trust each other.
- **Online games and lotteries.** Commit and reveal schemes decide outcomes between a server and a player.
- **Leader election and Byzantine agreement.** Shared random coins break symmetry in randomized Byzantine agreement protocols such as [Rabin's](/rabin-randomized-byzantine-agreement/), where a common coin removes the need for many rounds.
- **Randomness beacons.** Commit and reveal among many parties, or threshold signatures, give public random values; the last party to reveal can still abort, which is the same problem as Cleve's.

## References
