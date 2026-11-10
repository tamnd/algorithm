---
tag: GDRFMD
kind: concept
slug: proof-of-work
name: Proof of work
aliases:
- PoW
area: distributed/consensus
level: intro
summary: A puzzle that takes many hash computations to solve and one to check, such as finding a nonce whose hash is below a target. Blockchains use it to make block proposals costly.
prereqs: [cryptographic-hash-function, geometric-distribution]
see_also: [nakamoto-consensus, proof-of-stake, cryptographic-hash-function, sha-2, geometric-distribution, poisson-distribution, merkle-tree, hash-chain]
sources:
  - paper: doi:10.1007/3-540-48071-4_10
    title: Cynthia Dwork and Moni Naor, Pricing via processing or combatting junk mail, Advances in Cryptology (CRYPTO '92), LNCS 740, 1993, pages 139 to 147
    locator: the idea of a pricing function that is moderately hard to compute and easy to check, used to make each e-mail cost some computation
  - url: http://www.hashcash.org/papers/hashcash.pdf
    title: Adam Back, Hashcash, a denial of service counter-measure, 2002
    locator: the partial hash collision puzzle (a hash whose first k bits are zero), its expected cost of 2^k tries, and its use against e-mail spam
  - url: https://bitcoin.org/bitcoin.pdf
    title: Satoshi Nakamoto, Bitcoin, a peer-to-peer electronic cash system, 2008
    locator: Section 4 (proof-of-work with a nonce in the block, the moving average target, and one CPU one vote)
  - book: isbn:9780691171692
    title: Arvind Narayanan, Joseph Bonneau, Edward Felten, Andrew Miller and Steven Goldfeder, Bitcoin and Cryptocurrency Technologies, Princeton University Press, 2016
    locator: the chapters on Bitcoin mining and on alternative mining puzzles
---

A proof of work is a piece of data that is costly to produce and cheap to check: the standard form is a nonce such that the [hash](/cryptographic-hash-function/) of a message and the nonce, read as a number, is below a target. Each try succeeds with a fixed small probability $p$, so the number of tries has a [geometric distribution](/geometric-distribution/) with mean $1/p$, while a check takes one hash. Dwork and Naor (1992) proposed such puzzles to put a price on e-mail, Back's Hashcash (1997, described in 2002) gave the hash form, and Nakamoto (2008) used it to choose who may add the next block in [Nakamoto consensus](/nakamoto-consensus/). A difficulty adjustment rule changes the target so that blocks keep a steady rate as computing power changes.

## In plain words

Think of a lottery where each ticket is free to print, but printing one takes a second of a computer's work. A ticket wins if its number is small enough. Nobody can predict which ticket wins, so the only way to win is to print many tickets.

Anyone can check a winning ticket in an instant. So a winning ticket proves that its owner most likely did a lot of work.

If tickets start to win too often because more computers join, the rule changes so that only smaller numbers win. The lottery then keeps the same pace.

## The idea

**The puzzle.** Fix a hash function $H$ with $b$ output bits, such as SHA-256 from the [SHA-2](/sha-2/) family, and a target $T$. Given data $d$, find a nonce $x$ with

$$H(d \,\|\, x) < T.$$

If $H$ behaves like a random function, each try succeeds with probability $p = T / 2^{b}$, independently of the other tries, and no method finds a solution faster than trying nonces. Back's Hashcash asks for $k$ leading zero bits, which is the case $T = 2^{b-k}$ and $p = 2^{-k}$.

```pseudo id=main
SOLVE(d, T)
L1  x ← 0
L2  while H(d ‖ x) ≥ T: x ← x + 1
L3  return x
VERIFY(d, x, T)
L4  return H(d ‖ x) < T
RETARGET, every N blocks
L5  T ← T · clamp(actual time of the last N blocks / (N · spacing), 1/4, 4), and at most T_max
```

**Expected work.** Let $N$ be the number of tries. Tries are independent [Bernoulli trials](/bernoulli-trials/) with success probability $p$, so

$$\Pr[N = k] = (1 - p)^{k-1} p, \qquad \Pr[N > k] = (1 - p)^k, \qquad k = 1, 2, \ldots$$

The mean follows from one step: the first try succeeds with probability $p$, and otherwise the search starts again, so $\mathbb{E}[N] = 1 + (1-p)\,\mathbb{E}[N]$, which gives $\mathbb{E}[N] = 1/p$. The variance is $(1-p)/p^2$, so the standard deviation is close to the mean: the work for one solution varies a lot. Checking takes one hash, so the gap between the work to solve and the work to check is a factor of about $1/p$.

**No progress.** The geometric distribution is memoryless: $\Pr[N > a + c \mid N > a] = \Pr[N > c]$. A miner that has tried a billion nonces is no closer to a solution than one that just started. So a miner with a fraction $\alpha$ of the total hash rate finds about a fraction $\alpha$ of the solutions, and many small miners together do as well as one large one. With $h$ hashes per second, the time to a solution is close to exponential with rate $h p$, and solutions form a [Poisson process](/poisson-distribution/).

**Binding the work to the data.** The data $d$ is part of the hash input, so a solution for one block is useless for any other block. In Bitcoin, $d$ is the block header, which holds the hash of the previous block (making a [hash chain](/hash-chain/)) and the root of a [Merkle tree](/merkle-tree/) of the transactions. Changing any transaction changes the header and voids the proof.

**Difficulty adjustment.** If the total hash rate is $h$, blocks come every $1/(hp)$ seconds on average. Bitcoin wants one block per 600 seconds. Every 2016 blocks, each node computes the time the last window took and multiplies the target by that time over the expected two weeks (line L5). If the blocks came too fast, the target shrinks and the puzzle gets harder. The factor is clamped to $[1/4, 4]$, so one window cannot change the difficulty by a large jump, and the target never exceeds a fixed maximum. Every node computes the same target from the same chain, so no vote is needed.

## Examples

**Toy puzzle.** With $p = 1/64$ (six leading zero bits), 2000 puzzles on random data, solved with SHA-256 in the tests, took 64.4 tries on average, against the predicted mean of 64. The fewest tries was 1 and the most was 427, which shows the spread of the geometric distribution. With $p = 1/32$, the fraction of puzzles that needed more than $k$ tries matched $(31/32)^k$ for $k$ from 8 to 128.

**Bitcoin scale.** If a puzzle needs about $2^{70}$ hashes on average and the network computes $2^{70}/600$ hashes per second, it finds a block every 600 seconds on average. A single machine with $10^{14}$ hashes per second would expect to wait $2^{70}/10^{14}$ seconds, about four and a half months, for one block.

**Difficulty after a jump.** The simulation in the tests starts at the right difficulty with one block per 600 seconds, and then the hash rate grows eight times. With a window of 50 blocks:

| blocks | mean interval (s) | difficulty |
|---|---|---|
| 450 to 499 | 475 | 1.00 |
| 500 to 549 (hash rate × 8) | 92 | 1.26 |
| 550 to 599 | 323 | 5.05 (clamped at × 4) |
| 600 to 649 | 504 | 9.39 |
| 1100 to 1499 | about 600 | about 8 |

The clamp makes the difficulty take two windows to catch up, and after that it varies around the new hash rate.

**Non-example.** A puzzle that asks for the factors of a number chosen by the solver is not a proof of work: the solver can pick a number whose factors it already knows. The puzzle must depend on data that the solver cannot choose freely after the fact, such as the previous block's hash.

## Where it is used

- **Blockchains.** Bitcoin and many other systems use proof of work to choose who proposes the next block and to make it costly to rewrite history: see [Nakamoto consensus](/nakamoto-consensus/).
- **Spam and denial of service.** Hashcash stamps on e-mail, and client puzzles that a server asks for when it is under attack, make each request cost the client some work.
- **Rate limits without identities.** Proof of work prices actions where creating many fake identities is free, since the cost is per action, not per identity.
- **Alternatives.** Memory-hard puzzles, such as scrypt, try to make special hardware less useful. [Proof of stake](/proof-of-stake/) replaces the work by locked funds.

## References
