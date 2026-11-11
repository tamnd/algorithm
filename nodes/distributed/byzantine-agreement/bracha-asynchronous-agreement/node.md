---
tag: R0F3DQ
kind: algorithm
slug: bracha-asynchronous-agreement
name: Bracha asynchronous Byzantine agreement
aliases:
- Bracha's protocol
- asynchronous Byzantine agreement
- Bracha agreement
area: distributed/byzantine-agreement
level: advanced
summary: Randomized asynchronous binary Byzantine agreement for n > 3t over reliable broadcast with validation; with local coins, O(2^n) expected rounds.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {best: 1, expected: O(2^n)}
  messages: {expected: O(n^3 2^n)}
  space: {extra: O(n^2)}
properties: {deterministic: false, recursive: false}
prereqs: [bracha-reliable-broadcast, ben-or-consensus, asynchronous-model, byzantine-failure-model]
see_also: [ben-or-consensus, bracha-reliable-broadcast, rabin-randomized-byzantine-agreement, feldman-micali-byzantine-agreement, honeybadger-bft, flp-impossibility, threshold-signature, fair-coin-flipping]
sources:
  - paper: doi:10.1016/0890-5401(87)90054-X
    title: Gabriel Bracha, Asynchronous Byzantine agreement protocols, Information and Computation 75(2), 1987
    locator: the broadcast primitive, the validation of messages, the three-step round with local coins, and the expected number of rounds
  - paper: doi:10.1145/2611462.2611468
    title: Achour Mostéfaoui, Hamouma Moumen and Michel Raynal, Signature-free asynchronous Byzantine consensus with t < n/3 and O(n^2) messages, PODC 2014
    locator: the binary-value broadcast and the common-coin protocol with constant expected rounds
  - paper: doi:10.1145/800221.806707
    title: Michael Ben-Or, Another advantage of free choice, Completely asynchronous agreement protocols, PODC 1983
    locator: the round structure with local coins (n > 5t for Byzantine failures)
  - paper: doi:10.1007/s00145-005-0318-0
    title: Christian Cachin, Klaus Kursawe and Victor Shoup, Random oracles in Constantinople, Practical asynchronous Byzantine agreement using cryptography, Journal of Cryptology 18(3), 2005
    locator: a common coin from threshold signatures and binary agreement with constant expected rounds
  - paper: doi:10.1145/4221.214134
    title: Gabriel Bracha and Sam Toueg, Asynchronous consensus and broadcast protocols, Journal of the ACM 32(4), 1985
    locator: the bound n > 3t for asynchronous Byzantine agreement
---

Bracha's protocol solves binary Byzantine agreement in the [asynchronous model](/asynchronous-model/) with the optimal resilience $n > 3t$. It keeps the round structure of [Ben-Or's algorithm](/ben-or-consensus/) and adds two tools. Every message goes through [Bracha reliable broadcast](/bracha-reliable-broadcast/), so a faulty process cannot send different values to different processes. Every message is also *validated*: a process accepts it only if an honest process could have sent it. A process that sees no strong majority flips a local coin. The protocol is always safe and terminates with probability 1, but with local coins the expected number of rounds can be exponential in $n$. Gabriel Bracha published it in 1987.

## In plain words

A group of computers must agree on 0 or 1 over a network that can delay any message for any time. Some computers are traitors.

Each round has three steps. In each step every computer announces a value in a way that forces it to tell everyone the same thing. The others also check that an honest computer could have announced that value, given what was announced before. So a traitor can only choose which honest-looking value to send.

First the computers vote and take the majority. Then a computer that sees a large majority marks the value as strong. Then a computer that sees many strong marks decides. One that sees some strong marks takes that value. One that sees none flips a coin. Sooner or later all coins land the same way, and then everyone agrees in the next round.

## The problem

There are $n$ processes on reliable, authenticated point-to-point links in an asynchronous network: every message between honest processes arrives, after a delay that the adversary chooses. At most $t$ processes are [Byzantine](/byzantine-failure-model/), with $n > 3t$. Each process has an input bit. The protocol must give agreement (no two honest processes decide differently), validity (if all honest inputs are $v$, the decision is $v$) and termination with probability 1. By the [FLP impossibility](/flp-impossibility/) no deterministic protocol can do this, so the protocol flips coins. Termination is in the sense of a [Las Vegas algorithm](/las-vegas-algorithm/): safety never depends on the coins.

## The algorithm

Each process runs the code below. RBC-broadcast is [Bracha reliable broadcast](/bracha-reliable-broadcast/), with one instance for each sender, round $r$ and step $k$. A *valid* message is defined at line L12, and $S$ holds the values of the first $n - t$ valid messages of the step, from different senders. In step 2 a value is a bit $w$ marked as strong, written $(d, w)$, or the symbol ?.

```pseudo id=main
BRACHA-AGREEMENT(i, x_i)                                   ▷ the code of p_i; n > 3t
L1  v ← x_i
L2  for r ← 1, 2, ... do
L3      for k ← 1 to 3 do
L4          RBC-broadcast (r, k, v)
L5          wait for n − t valid messages of step (r, k); S ← their values
L6          if k = 1 then v ← the majority bit of S (0 on a tie)
L7          if k = 2 then v ← (d, w) if more than n/2 values of S are w, else v ← ?
L8          if k = 3 and more than 2t values of S are (d, w) then decide w, if not yet decided
L9          if k = 3 and more than t values of S are (d, w) then v ← w
L10         if k = 3 and no (d, w) is in S more than t times then v ← a fair local coin
L11     if p_i decided in round r − 1 then halt
L12 VALID(j, r, k, u): in round 1, step 1, any bit; otherwise some n − t valid delivered messages of the step before, from different senders, make lines L6 to L10 give u
```

Line L11 lets a process stop after it helped one more round: all honest processes decide by then. Bracha's step-3 message carries the plain value of the process when it is not marked; the rules use only the marked values, so this page sends ? instead. For a step-1 message of round $r + 1$ that follows a coin, both bits are valid.

## Example

Take $n = 4$, $t = 1$, with $p_4$ faulty and the honest inputs $p_1 = 0$, $p_2 = 1$, $p_3 = 1$. A quorum is $n - t = 3$ messages. Step 2 marks a value seen 3 times (more than $n/2 = 2$), step 3 decides on 3 marks (more than $2t$) and adopts on 2 (more than $t$). In round 1 the scheduler picks these quorums:

| step | broadcast values | quorums | new values |
|---|---|---|---|
| 1 | $p_1{:}0$, $p_2{:}1$, $p_3{:}1$, $p_4{:}0$ | $p_1$: 0, 1, 0; $p_2$: 1, 1, 0; $p_3$: 0, 1, 0 | $p_1 = 0$, $p_2 = 1$, $p_3 = 0$ |
| 2 | $p_1{:}0$, $p_2{:}1$, $p_3{:}0$, $p_4{:}0$ | $p_1$ from $p_1, p_3, p_4$; $p_2$ from $p_2, p_3, p_4$; $p_3$ from $p_1, p_3, p_4$ | $p_1 = (d, 0)$, $p_2 = {?}$, $p_3 = (d, 0)$ |
| 3 | $p_1{:}(d,0)$, $p_2{:}?$, $p_3{:}(d,0)$, $p_4{:}(d,0)$ | $p_1$ from $p_1, p_2, p_3$; $p_2$ from $p_2, p_3, p_4$; $p_3$ from $p_1, p_3, p_4$ | $p_3$ decides 0; $p_1 = 0$, $p_2 = 0$ |

The faulty $p_4$ sends 0 in step 2. This is valid, because the quorum $p_1, p_4, p_2$ of step 1 has majority 0. If $p_4$ sent $(d, 1)$ in step 3, no process would accept it: the step-2 values hold only one 1, so no quorum has more than two. After round 1 all honest processes hold 0, so in round 2 every quorum of step 1 has a majority of 0, every valid step-2 message is 0, every valid step-3 message is $(d, 0)$, and $p_1$ and $p_2$ decide 0.

## Correctness

The full proof is below. Its main steps:

- **Reliable broadcast and validation.** Each faulty process has one value per step, and only values that an honest process could have sent are used.
- **One marked value per round.** Two marks need two sets of more than $n/2$ step-2 senders, which share a sender, and that sender has one value.
- **Unanimity.** If all honest processes start a round with $w$, then $w$ is a strict majority of every step-1 quorum, because $n - 2t > t$. So every valid later message is $w$ or $(d, w)$, and all decide $w$.
- **Agreement.** A decision on $w$ rests on more than $2t$ marks; any other quorum of $n - t$ step-3 messages meets them in more than $t$ senders, so every honest process adopts $w$, and all decide $w$ in the next round.
- **Termination.** If the marked value is fixed before the coins of a round, all coins of the round match it with probability at least $2^{-n}$.

## Complexity

- **Rounds with local coins.** Against an adversary whose actions in a round do not depend on the coins of that round, the expected number of rounds is at most $2^n + 1$, by the proof. Bracha's paper states that the expected number of rounds is exponential in $n$ in general, and constant when $t = O(\sqrt{n})$, as for Ben-Or.
- **Rounds when the inputs agree.** One round, by unanimity.
- **Messages.** A step is $n$ reliable broadcasts of $n + 2n^2$ messages each, so a round is $3n(n + 2n^2) = O(n^3)$ messages, and the expected total is $O(n^3 2^n)$ with local coins.
- **Local work.** Validation counts values of the step before. A process keeps the delivered messages of the last steps, $O(n^2)$ space per round when it keeps the reliable broadcast state.

The table gives the measured mean number of rounds until the last honest decision, over 20 seeded runs for each cell. The inputs are $0, 1, 0, 1, \ldots$, the last $t$ processes are faulty, and each process waits for its first $n - t$ valid messages. The random scheduler delivers a random message in transit. The adversarial one delivers the messages of faulty processes first and the messages to one honest process last.

| $n$, $t$ | scheduler | silent | wrong votes | random votes | equivocation |
|---|---|---|---|---|---|
| 4, 1 | random | 1.00 | 1.55 | 1.40 | 1.00 |
| 4, 1 | adversarial | 1.00 | 1.30 | 1.35 | 1.00 |
| 7, 2 | random | 1.00 | 1.05 | 1.40 | 1.00 |
| 7, 2 | adversarial | 1.00 | 1.15 | 1.10 | 1.00 |
| 10, 3 | random | 1.00 | 1.10 | 1.15 | 1.00 |
| 10, 3 | adversarial | 1.00 | 1.00 | 1.30 | 1.00 |

These adversaries are weak, and the means are close to 1. An adversary that sees the values and gives each process a split quorum in every step forces coin flips, and then the bound $2^n + 1$ is the right order for large $t$.

## Properties

- **Las Vegas.** Agreement and validity hold in every run; only the running time is random.
- **Optimal resilience.** $n > 3t$, the bound of Bracha and Toueg for asynchronous Byzantine agreement.
- **No cryptography.** It needs only authenticated links and local randomness.
- **Binary.** It decides one bit.
- **Slow in the worst case.** With local coins and $t = \Theta(n)$ the expected time is exponential.

## Variants and improvements

- **Common coin.** If all processes see the same random bit in each round, the bit matches the marked value with probability $1/2$, so the expected number of rounds is constant. Mostéfaoui, Moumen and Raynal (2014) give such a protocol for $n > 3t$ without signatures besides the coin, with $O(n^2)$ messages per round: a *binary-value broadcast* replaces reliable broadcast and validation. [HoneyBadgerBFT](/honeybadger-bft/) uses it.
- **Cryptographic coin.** Cachin, Kursawe and Shoup (2005) build the common coin from a [threshold signature](/threshold-signature/) on the round number, which no coalition of $t$ processes can predict.
- **Coin from secret sharing.** Canetti and Rabin (1993) build a coin from asynchronous [verifiable secret sharing](/verifiable-secret-sharing/), with optimal resilience and polynomial expected time, without trusted setup.
- **Dealt coins.** [Rabin's protocol](/rabin-randomized-byzantine-agreement/) (1983) uses coins dealt in advance by a trusted dealer.

## When to use it

Use Bracha's protocol to teach how reliable broadcast and validation turn Ben-Or's crash protocol into a Byzantine one with $n > 3t$, or when no cryptographic setup is possible and the group is small. For real systems with many processes, use a common coin, as in the protocol of Mostéfaoui, Moumen and Raynal or in HoneyBadgerBFT, so that the expected number of rounds is constant. If the network is partially synchronous, a leader-based protocol such as [PBFT](/pbft/) is faster.

## Pitfalls

- **Skipping validation.** Without it, a faulty process can send $(d, 1)$ in step 3 when no quorum supports it, and push honest processes to adopt a value that breaks validity.
- **Validating with the process's own quorum.** A message is valid if *some* quorum supports it, not the quorum that the receiver used. Otherwise honest messages may never become valid at a receiver with a different quorum.
- **Halting at the decision.** A process that stops sending when it decides can block the others, which still need $n - t$ messages of the next round.
- **Non-strict thresholds.** Marking a value seen exactly $n/2$ times allows two marked values in a round.
- **Assuming a short run.** With local coins and an adversarial schedule, runs can take very many rounds.

## Implementations

## History

Ben-Or (1983) gave the first randomized asynchronous agreement protocols, for $n > 2t$ crash failures and $n > 5t$ Byzantine failures. In the same year Rabin used a coin dealt in advance. Bracha and Toueg (1985) showed that $n > 3t$ is needed in the asynchronous Byzantine model. Bracha (1987) reached $n > 3t$ with reliable broadcast and validation. Canetti and Rabin (1993) gave optimal resilience with polynomial expected time, and Cachin, Kursawe and Shoup (2005) made asynchronous agreement practical with a threshold coin. Mostéfaoui, Moumen and Raynal (2014) gave a signature-free protocol with $O(n^2)$ messages per round and a common coin.

## References
