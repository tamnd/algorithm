---
tag: P7QJJH
kind: algorithm
slug: feldman-micali-byzantine-agreement
name: Feldman-Micali Byzantine agreement
aliases:
- Feldman-Micali protocol
- Feldman-Micali algorithm
- optimal probabilistic Byzantine agreement
area: distributed/byzantine-agreement
level: research
summary: Synchronous Byzantine agreement for n ≥ 3t + 1 in constant expected rounds with no dealer. Graded consensus plus a common coin built from verifiable secret sharing.
solves: [consensus-problem]
model: synchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {best: 2, expected: O(1)}
  messages: {best: 2n(n - 1), expected: poly(n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [byzantine-failure-model, synchronous-model, verifiable-secret-sharing, rabin-randomized-byzantine-agreement]
see_also: [rabin-randomized-byzantine-agreement, phase-king-algorithm, byzantine-round-lower-bound, verifiable-secret-sharing, fair-coin-flipping, bracha-asynchronous-agreement, byzantine-resilience-bound, oral-messages-algorithm]
sources:
  - paper: doi:10.1145/62212.62225
    title: Paul Feldman and Silvio Micali, Optimal algorithms for Byzantine agreement, STOC 1988
    locator: the constant expected round protocol for n > 3t without a dealer
  - paper: doi:10.1137/S0097539790187084
    title: Pesech Feldman and Silvio Micali, An optimal probabilistic protocol for synchronous Byzantine agreement, SIAM Journal on Computing 26(4), 1997
    locator: the full protocol, with gradecast, graded verifiable secret sharing, the oblivious common coin, and the reduction of agreement to the coin
  - paper: doi:10.1109/SFCS.1983.48
    title: Michael O. Rabin, Randomized Byzantine generals, FOCS 1983
    locator: agreement in constant expected rounds from a coin dealt in advance
---

The Feldman-Micali protocol solves synchronous binary [Byzantine](/byzantine-failure-model/) agreement with optimal resilience, $n \ge 3t + 1$, in a *constant expected* number of rounds, with no trusted dealer and no signatures. It splits the work in two. A short *graded consensus* step gives each process a value and a grade, and a *common coin* breaks ties when the grades are low. The coin is the hard part: the processes make it themselves with [verifiable secret sharing](/verifiable-secret-sharing/), so it is unpredictable and, with constant probability, the same for all. Paul Feldman and Silvio Micali presented it at STOC 1988 and gave the full version in the SIAM Journal on Computing in 1997. It beat the $t + 1$ rounds that every deterministic protocol needs in the worst case.

## In plain words

A group of computers must agree on 0 or 1, and up to a third of them may lie. In each step they vote twice. After the votes, each computer knows a value and how sure it is: very sure, a little sure, or not sure.

A very sure computer decides. A computer that is a little sure keeps its value. A computer that is not sure takes the result of a shared coin flip. The liars cannot know the coin before they vote, so half the time the coin matches the value of the sure computers, and then everyone holds the same value and decides in the next step. The difficult part is to flip a fair shared coin when some of the flippers lie; Feldman and Micali showed how.

## The problem

There are $n$ processes, at most $t$ of them Byzantine, in the [synchronous model](/synchronous-model/) with private, reliable links and no signatures (the [oral messages model](/oral-messages-model/)). Each honest process has an input bit. The processes must reach agreement, validity, and termination with probability 1, against an adversary that sees all messages between faulty processes and chooses its messages after it sees those of the honest processes in the same round. Deterministic protocols need $n \ge 3t + 1$ ([the resilience bound](/byzantine-resilience-bound/)) and $t + 1$ rounds ([the round lower bound](/byzantine-round-lower-bound/)). The goal is $n \ge 3t + 1$ with a constant expected number of rounds and no trusted dealer, which [Rabin's protocol](/rabin-randomized-byzantine-agreement/) needs.

## The algorithm

The protocol repeats one iteration. Each process holds a value $v$, starting with its input.

```pseudo id=main
FELDMAN-MICALI(v)                                                    ▷ n ≥ 3t + 1, synchronous
    repeat
L1      send v to all; x ← w if some w has at least n - t copies, else ⊥
L2      send x to all; w ← the most frequent proposal other than ⊥; c ← its number of copies
L3      (y, g) ← (w, 2) if c ≥ n - t; (w, 1) if c ≥ t + 1; (v, 0) otherwise
L4      s ← COMMON-COIN()                                    ▷ cited: verifiable secret sharing and gradecast
L5      v ← y if g ≥ 1, else s
L6      if g = 2 and not decided: decide y; take part in one more iteration, then halt
```

Lines L1 to L3 are graded consensus. Its guarantees, all proved in the proof file: honest processes with grade 1 or 2 hold the same value; if one honest process has grade 2, all have grade at least 1; and if all honest processes start with $b$, all get $(b, 2)$.

**The coin (cited, not proved here).** In Feldman and Micali's coin, every process deals random secrets by verifiable secret sharing. The processes use *gradecast*, a broadcast in which every receiver also gets a grade of confidence, to agree well enough on which dealings are valid. Then the secrets are opened, and each process computes its coin from them. A faulty dealer cannot change its secret after the dealing, and the faulty processes learn nothing about the honest secrets before the opening, so with a constant probability all honest processes get the same fair bit. The coin takes a constant number of rounds. The full construction is in the 1997 paper; the implementation on this page uses a coin oracle in its place.

## Example

Take $n = 4$, $t = 1$, process 3 faulty, inputs 1, 1, 0 at processes 0, 1, 2.

**Round 1.** The honest processes see two 1s and one 0. Process 3 sends 1 to process 0 and 0 to the others. Process 0 sees three 1s, which is $n - t = 3$, and proposes 1. Processes 1 and 2 see two of each and propose $\bot$.

**Round 2.** Every honest process gets one proposal of 1 from process 0. Process 3 sends 1 to process 1 and $\bot$ to the others. Process 1 sees two proposals of 1, which is $t + 1 = 2$, and gets $(1, 1)$. Processes 0 and 2 see one and get grade 0.

**Coin.** Process 1 keeps 1. Processes 0 and 2 take the coin. If it is 1, all three hold 1 and decide 1 in the next iteration. If it is 0, the values stay split and the attack goes on. The faulty process had to choose its messages before the coin, so it wins only with probability $1/2$ per iteration.

In the tests, with $n = 10$, $t = 3$ and this attack, the mean iteration of the last decision over 300 seeded runs is 2.94 with an ideal coin (bound 3), and 4.73 with a coin that is common only half of the time (bound 5). If the adversary knows the coin in advance, nobody decides in 60 iterations.

## Correctness

The full proof of the reduction is in the proof file; the coin is cited.

- **One value can be proposed.** An honest proposal of $w$ needs $n - 2t$ honest copies of $w$, and two such sets do not fit in $n - t$ honest processes when $n > 3t$.
- **Grades are consistent.** A grade of 1 needs $t + 1$ proposals, so one from an honest process, and by the previous point there is only one such value.
- **Grade 2 forces grade 1.** $n - t$ proposals contain $n - 2t \ge t + 1$ honest ones, which every honest process receives.
- **Agreement.** At the first decision, every honest process has grade 1 or 2 for the decided value and keeps it, so the next iteration is unanimous and stays so.
- **Termination.** The value of the graded processes is fixed before the coin, and a common fair coin matches it with probability $1/2$. With a coin that is common with probability $p$, the expected iteration of the last decision is at most $2/p + 1$.

## Complexity

- **Rounds.** Two rounds of graded consensus per iteration plus the rounds of the coin, both constants; expected $O(1)$ iterations.
- **Messages.** Graded consensus sends $2n(n - 1)$ messages per iteration. The coin, with verifiable secret sharing by every process, costs a polynomial number of messages, larger than the agreement part.
- **Local work.** Polynomial, for the secret sharing.
- **Space.** $O(n)$ for the agreement part.

## Properties

- **Optimal resilience.** $n \ge 3t + 1$, the same bound as for deterministic agreement without signatures.
- **Constant expected rounds.** Independent of $n$ and $t$.
- **No dealer, no signatures.** The coin comes from the processes themselves; the model needs private channels.
- **Las Vegas.** Agreement and validity hold in every run.
- **Modular.** Any coin with the stated property can replace the one of the paper.

## Variants and improvements

- **Graded consensus and gradecast.** The two graded tools of Feldman and Micali became standard building blocks. Gradecast is a broadcast whose receivers get a grade, and graded consensus, as in lines L1 to L3, appears in many later protocols.
- **With signatures.** Katz and Koo (2006) gave a constant expected round protocol for $n \ge 2t + 1$ with signatures, using the same structure with authenticated graded tools.
- **With a dealer.** [Rabin's protocol](/rabin-randomized-byzantine-agreement/) uses coins dealt in advance; a threshold signature set up once gives the same coins today.
- **Asynchronous.** In the [asynchronous model](/asynchronous-model/), [Bracha's protocol](/bracha-asynchronous-agreement/) with a common coin and the protocol of Mostéfaoui, Moumen and Raynal play the same role.

## When to use it

Use the reduction, graded consensus plus a coin, whenever you need randomized agreement in few rounds. Use the coin of the paper when there is no trusted setup and the model has private channels. When a setup is possible, a coin from [threshold signatures](/threshold-signature/) is much cheaper.

## Pitfalls

- **A coin that the adversary can predict.** If the faulty processes learn the coin before round 2, they split the grades every iteration. The coin must be opened after the votes.
- **Wrong thresholds.** Proposals need $n - t$ copies and grade 1 needs $t + 1$; with $n = 3t$ the graded consensus fails, and the tests show two honest decisions that differ.
- **Halting at once.** A process that decides must run one more iteration so that the others, which have grade 1, can reach grade 2.
- **Counting the coin as free.** The agreement part is cheap, but the verifiable secret sharing of the coin dominates the cost.

## Implementations

## History

Rabin (1983) and Ben-Or (1983) showed that randomness beats the deterministic round bound, Rabin with coins from a trusted dealer. Paul Feldman and Silvio Micali presented "Optimal algorithms for Byzantine agreement" at STOC 1988, with $n \ge 3t + 1$, a constant expected number of rounds, and a coin made by the processes. The journal version, "An optimal probabilistic protocol for synchronous Byzantine agreement", appeared in the SIAM Journal on Computing in 1997 with the full construction of gradecast, graded secret sharing and the coin.

## References
