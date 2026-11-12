---
tag: 93SCFK
kind: algorithm
slug: rabin-randomized-byzantine-agreement
name: Rabin randomized Byzantine agreement
aliases:
- Rabin 1983 common-coin agreement
- Rabin's randomized Byzantine generals
- Rabin's protocol
area: distributed/byzantine-agreement
level: research
summary: Binary Byzantine agreement in constant expected rounds with a common coin that a trusted dealer shares in advance. The coin picks one of two thresholds each round.
solves: [consensus-problem]
model: synchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes}
  time: {best: 1, expected: O(1)}
  messages: {best: 2n(n - 1), expected: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [byzantine-failure-model, synchronous-model, verifiable-secret-sharing, fair-coin-flipping]
see_also: [feldman-micali-byzantine-agreement, ben-or-consensus, bracha-asynchronous-agreement, phase-king-algorithm, byzantine-round-lower-bound, threshold-signature, honeybadger-bft, fair-coin-flipping]
sources:
  - paper: doi:10.1109/SFCS.1983.48
    title: Michael O. Rabin, Randomized Byzantine generals, 24th Annual Symposium on Foundations of Computer Science (FOCS), 1983
    locator: pages 403 to 409 (agreement in a constant expected number of rounds with coins shared in advance by Shamir's method, in the synchronous and the asynchronous case)
  - paper: doi:10.1145/800222.806744
    title: Sam Toueg, Randomized Byzantine agreements, PODC 1984
    locator: pages 163 to 178; the introduction states that the algorithms of Rabin tolerate up to (n - 1)/10 faults in asynchronous systems and (n - 1)/4 in synchronous ones
  - paper: doi:10.1145/359168.359176
    title: Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979
    locator: the threshold scheme that the dealer uses to share each coin
  - paper: doi:10.1145/800221.806707
    title: Michael Ben-Or, Another advantage of free choice, Completely asynchronous agreement protocols, PODC 1983
    locator: randomized agreement with local coins, published in the same year
---

Rabin's randomized Byzantine agreement solves binary [Byzantine](/byzantine-failure-model/) agreement in a *constant expected* number of rounds, however many processes fail, with a *common coin*: a random bit per round that all honest processes see and that the adversary cannot predict. A trusted dealer makes the coins before the run and gives each process a share of every coin by Shamir's secret sharing, so $t$ shares reveal nothing and $t + 1$ rebuild the coin. In each round the processes exchange values, and the coin picks one of two thresholds; a process keeps the majority value only if its count reaches the threshold. Michael Rabin published it in 1983, in the same year as Ben-Or's local-coin protocol, and it broke the $t + 1$ round lower bound of deterministic protocols.

## In plain words

A group of computers must agree on 0 or 1, and some may lie. Each round, every computer says its value to all the others and counts the votes. Liars can make one computer count a little more than another, but at most $t$ more.

Before the run, a trusted dealer flipped one coin for each round and gave every computer a sealed piece of each coin. After the votes of a round, the computers open the coin. Heads means "keep the majority if it has at least $H$ votes"; tails means "at least $L$ votes". Liars do not know which bar is used, so half the time they cannot leave the computers on both sides of it. Then all agree.

## The problem

There are $n$ processes, at most $t$ of them Byzantine, in the [synchronous model](/synchronous-model/) with reliable links. Each honest process has an input bit. The processes must reach agreement (no two honest processes decide differently), validity (if all honest inputs are $b$, the decision is $b$) and termination with probability 1. Deterministic protocols need $t + 1$ rounds in the worst case ([the round lower bound](/byzantine-round-lower-bound/)); the goal here is a constant expected number of rounds. Before the run, a trusted dealer, which is not one of the processes, can send each process private data.

## The algorithm

This page gives a synchronous version with $n \ge 8t + 1$, chosen so that the proof is short. Let $L = \lfloor n/2 \rfloor + t + 1$, $H = L + t$ and $G = L + 2t$. For every round $r$ the dealer picks a random bit $s_r$ and gives process $i$ a signed share of it.

```pseudo id=main
RABIN-AGREEMENT(v)                                                   ▷ process i, input bit v
    for r = 1, 2, ...
L1      send v to all processes; receive one value from each process
L2      maj ← the value with more than half of the received copies (0 if none); tally ← its number of copies
L3      send my share of s_r to all; s ← the coin rebuilt from t + 1 valid shares
L4      T ← L if s = 0, else H
L5      if tally ≥ T then v ← maj else v ← 0
L6      if tally ≥ G and not decided: decide maj; take part in round r + 1, then halt
```

The shares are sent only after the values of the round, so the faulty processes choose their votes without knowing $s_r$.

**What Rabin's paper gives.** Rabin's paper uses the same idea, a dealer's coin shared by Shamir's method and thresholds chosen by the coin, and covers both the synchronous and the asynchronous model. According to Toueg (1984), Rabin's protocols tolerate $t \le (n - 1)/10$ faults in the asynchronous model, that is $n > 10t$ or $n \ge 10t + 1$, and $t \le (n - 1)/4$ in the synchronous model. The thresholds above are this page's own, and need $n \ge 8t + 1$.

## Example

Take $n = 17$ and $t = 2$, so $L = 11$, $H = 13$, $G = 15$. Processes 15 and 16 are faulty. Ten honest processes start with 1 and five with 0.

**Round 1.** Every honest process counts 10 honest votes for 1. The faulty processes send 1 to some honest processes and 0 to the others, so the tallies for 1 are 10 at some processes and 12 at others: they straddle $L = 11$. If the coin says $T = L$, the first group sets 0 and the second keeps 1, and the honest processes stay split. If the coin says $T = H = 13$, no tally reaches it, all honest processes set 0, and in round 2 all count 15 votes for 0, which is $G$, and decide 0.

The faulty processes cannot straddle 11 and 13 at once, because their votes move a tally by at most 2. In the tests, with this start and the straddle attack in every round, the mean round of the last decision over 300 seeded runs is 2.79, under the bound of 3 from the proof. With other strategies (silent, random, wrong votes) the mean is between 2.0 and 2.2.

**No coin.** With $T = L$ in every round, the same adversary keeps exactly 10 honest processes at 1 in every round, and nobody decides in 60 rounds. The tests show this too.

## Correctness

The full proof is in the proof file.

- **Spread.** Every honest process gets every honest vote, so two honest tallies of a value differ by at most $t$.
- **One value can pass $L$.** $2L > n + t$, so two different values cannot both reach $L$ at honest processes.
- **Unanimity decides.** If all honest processes hold $x$, each counts $n - t \ge G$ votes for $x$; this is where $n \ge 8t + 1$ is used.
- **A decision forces unanimity.** A tally of $G$ at one process means at least $G - t = H$ at every honest process, which passes either threshold.
- **The coin.** The honest tallies of the leading value lie in an interval of width $t$, which can contain $L$ or $H = L + t$ but not both. The coin avoids the split threshold with probability at least $1/2$, so the expected number of rounds until unanimity is at most 2, and the last decision comes at most one round later.

## Complexity

- **Rounds.** Expected at most 3 rounds to the last decision, and 4 to the last halt, for every $n$ and $t$. A unanimous start decides in round 1.
- **Messages.** Per round, $n(n - 1)$ value messages and $n(n - 1)$ coin shares: $O(n^2)$ messages in expectation.
- **Dealer.** The dealer sends $n$ shares per round in advance, so a run that may need $R$ rounds needs $R$ coins dealt before it starts.
- **Space.** $O(n)$ per round for the received values and shares.

## Properties

- **Randomized, Las Vegas.** Agreement and validity hold in every run; only the number of rounds is random.
- **Constant expected rounds.** Independent of $n$ and $t$.
- **Trusted setup.** It needs a dealer that is honest and that knows how many rounds to prepare.
- **Not optimal resilience.** This version needs $n \ge 8t + 1$, against $n \ge 3t + 1$ for deterministic agreement.

## Variants and improvements

- **Without a dealer.** [Feldman and Micali](/feldman-micali-byzantine-agreement/) (1988) made the coin inside the protocol with [verifiable secret sharing](/verifiable-secret-sharing/) and reached $n \ge 3t + 1$ with constant expected rounds.
- **Asynchronous.** Rabin's paper also treats the asynchronous model. [Bracha](/bracha-asynchronous-agreement/) reached $n \ge 3t + 1$ there with local coins, and later protocols use a common coin made from [threshold signatures](/threshold-signature/), as in [HoneyBadgerBFT](/honeybadger-bft/).
- **Local coins.** Ben-Or's protocol of the same year uses a private coin per process and needs an exponential expected number of rounds when $t$ is large.

## When to use it

Use the idea when a trusted setup is acceptable: today a threshold signature scheme set up once by a dealer or by distributed key generation gives an unbounded supply of common coins, which is Rabin's dealer in modern form. When no trusted setup is possible, use a protocol that makes its own coin.

## Pitfalls

- **Revealing the coin too early.** If the faulty processes see $s_r$ before they vote, they straddle the chosen threshold every round.
- **Thresholds closer than $t$.** If $H - L < t$, one spread can contain both thresholds and the coin does not help.
- **Unsigned shares.** A faulty process that sends a false share can change the rebuilt coin; shares must be checkable, as in [verifiable secret sharing](/verifiable-secret-sharing/).
- **Halting at once.** A process that halts in the round it decides takes its vote away from the next round, where the others need it.
- **Too few coins.** The dealer prepares coins for a fixed number of rounds; the run fails, with small probability, if it needs more.

## Implementations

## History

Michael Rabin presented "Randomized Byzantine generals" at FOCS 1983. In the same year Michael Ben-Or showed that randomization avoids the FLP impossibility with local coins. Rabin's common coin, shared in advance with Shamir's 1979 scheme, gave a constant expected number of rounds. Bracha (PODC 1984, journal version 1987) reached optimal resilience in the asynchronous model, and Feldman and Micali (1988) removed the dealer in the synchronous model with verifiable secret sharing.

## References
