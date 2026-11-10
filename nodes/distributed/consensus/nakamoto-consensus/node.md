---
tag: XQ55B7
kind: algorithm
slug: nakamoto-consensus
name: Nakamoto consensus
aliases:
- longest-chain rule
area: distributed/consensus
level: advanced
summary: Miners extend the chain with the most proof of work. A block z deep is reversed with a probability that falls exponentially in z while honest miners hold most of the hash power.
solves: [consensus-problem, total-order-broadcast]
model: synchronous-model
complexity:
  vars: {n: the number of miners, z: the confirmation depth in blocks, L: the length of the chain}
  time: {best: Θ(z)}
  messages: {best: Θ(n)}
  space: {extra: Θ(L)}
properties: {deterministic: false, recursive: false}
history:
  year: 2008
  people: [Satoshi Nakamoto]
  note: Nakamoto described the protocol and its double-spend analysis in the Bitcoin white paper of 2008, and the Bitcoin network started in January 2009.
prereqs: [proof-of-work, consensus-problem, byzantine-failure-model, hash-chain]
see_also: [proof-of-work, proof-of-stake, byzantine-fault-tolerance, pbft, tendermint, hotstuff, merkle-tree, poisson-distribution]
sources:
  - url: https://bitcoin.org/bitcoin.pdf
    title: Satoshi Nakamoto, Bitcoin, a peer-to-peer electronic cash system, 2008
    locator: Section 4 (proof-of-work and the longest chain as the majority decision), Section 5 (the network steps) and Section 11 (calculations, the gambler's ruin and the Poisson formula, with tables)
  - paper: doi:10.1007/978-3-662-46803-6_10
    title: Juan Garay, Aggelos Kiayias and Nikos Leonardos, The Bitcoin backbone protocol, analysis and applications, Advances in Cryptology (EUROCRYPT 2015), LNCS 9057, pages 281 to 310
    locator: the synchronous model with a bounded number of hash queries per round, the common prefix and chain quality properties, and the honest majority assumption
  - paper: doi:10.1007/978-3-662-45472-5_28
    title: Ittay Eyal and Emin Gün Sirer, Majority is not enough, Bitcoin mining is vulnerable, Financial Cryptography and Data Security (FC 2014), LNCS 8437, pages 436 to 454
    locator: the selfish mining strategy, its revenue as a function of the pool share and of the tie-breaking parameter γ, and the threshold of 1/3 for γ = 0
  - url: https://arxiv.org/abs/1402.2009
    title: Meni Rosenfeld, Analysis of hashrate-based double spending, 2014
    locator: the exact model of the race with the negative binomial distribution, compared with the Poisson approximation of the white paper
  - book: isbn:9780691171692
    title: Arvind Narayanan, Joseph Bonneau, Edward Felten, Andrew Miller and Steven Goldfeder, Bitcoin and Cryptocurrency Technologies, Princeton University Press, 2016
    locator: the chapters on how Bitcoin achieves decentralization and on mining
---

Nakamoto consensus is the agreement protocol of Bitcoin: anyone may propose the next block of a chain, but only by solving a [proof of work](/proof-of-work/) puzzle, and every node follows the valid chain with the most total work. Two blocks found at about the same time cause a fork, which ends when one branch grows longer, so a block becomes more certain as blocks are added after it, but it is never final with certainty. Nakamoto (2008) showed with a gambler's ruin argument that an attacker with a fraction $q < 1/2$ of the hash power rewrites a block $z$ blocks deep with a probability that falls exponentially in $z$. Garay, Kiayias and Leonardos (2015) proved the common prefix and chain quality properties in a synchronous model with an honest majority of hash power, and Eyal and Sirer (2014) showed that a miner with less than half the power can still gain from deviating, by selfish mining.

## In plain words

Picture a public notebook that many people copy. Anyone can add a page, but only after winning a hard lottery, which takes a lot of computing. Each page names the page before it, so the pages form a chain.

Sometimes two people win at almost the same time and add different pages. For a while there are two versions. Everyone keeps the version that has had the most lottery work put into it, and works on top of it. Soon one version is ahead, and the other one is dropped.

A cheater who wants to change an old page must redo the lottery for that page and all the pages after it, and then overtake everyone else. If the honest people do most of the computing, the chance of that gets tiny as more pages pile up on top.

## The problem

The goal is [total-order broadcast](/total-order-broadcast/) of transactions among an open set of nodes: anyone can join or leave without permission, and nobody knows how many nodes there are. Voting by identity does not work in that setting, since an attacker can create many identities at no cost. Instead, the right to propose comes from computing power, which is costly.

The model of Garay, Kiayias and Leonardos is [synchronous](/synchronous-model/): time runs in rounds, a message sent by an honest node reaches all honest nodes by the next round, and each node can compute a fixed number of hashes per round. The hash function is modelled as a random oracle. A fraction of the hash power, below one half, is controlled by a [Byzantine](/byzantine-failure-model/) adversary that can deviate in any way and can reorder the messages of each round. The requirements are probabilistic: properties hold except with a probability that falls exponentially in a parameter $k$.

- **Common prefix.** For any two honest nodes, the chain of one, with its last $k$ blocks removed, is a prefix of the chain of the other.
- **Chain quality.** In any $\ell$ consecutive blocks of an honest node's chain, for $\ell$ large enough, a positive fraction of the blocks were made by honest nodes.
- **Chain growth.** The chain of every honest node grows by at least a fixed number of blocks per round, on average over long enough periods.

## The algorithm

```pseudo id=main
NAKAMOTO CONSENSUS, at miner p
L1  chain ← genesis block
L2  repeat: build a block B on the tip of chain with new valid transactions, and try nonces
L3      if H(B) < target: chain ← chain + B; send B to all
L4  upon receiving a valid chain C: if work(C) > work(chain) then chain ← C
L5  a user treats a block as confirmed once it has z blocks after it in chain
```

**Blocks and work.** A block holds the hash of the previous block, a [Merkle tree](/merkle-tree/) root of its transactions, a target and a nonce. It is valid if its hash is below its target, its target follows the [difficulty adjustment](/proof-of-work/) rule, and its transactions are valid given the chain before it. The work of a block with target $T$ is about $2^{256}/T$, the expected number of hashes needed to find it, and the work of a chain is the sum over its blocks.

**Most work, not most blocks.** Line L4 compares total work. If targets could differ freely between two chains, a longer chain of easy blocks could beat a shorter chain of hard ones, which would let an attacker win with many cheap blocks. The test builds a chain of five blocks of work 10 and one of two blocks of work 40; the second one wins. With a fixed target, as in the white paper's analysis, the rule is the longest chain.

**Forks.** If two miners find blocks on the same tip before they hear of each other's block, the nodes split between two branches. Each node keeps the branch it saw first (line L4 needs strictly more work), and the tie breaks when the next block is found on one branch. The blocks of the losing branch are orphaned, and their transactions go back to the pool.

**Confirmation.** A user that receives a payment waits until the block with it has $z$ blocks after it (line L5). The deeper the block, the less likely a fork replaces it.

## Example

Three miners, A, B and C. A message takes one step to arrive.

| step | event | chain of A | chain of B | chain of C |
|---|---|---|---|---|
| 1 | A finds block 1 on the genesis block G | G 1 | G | G |
| 2 | B and C get block 1 | G 1 | G 1 | G 1 |
| 3 | A finds 2a and C finds 2b, both on block 1 | G 1 2a | G 1 | G 1 2b |
| 4 | B gets 2a first, then 2b, and keeps 2a (same work) | G 1 2a | G 1 2a | G 1 2b |
| 5 | B finds block 3 on 2a | G 1 2a | G 1 2a 3 | G 1 2b |
| 6 | A and C get block 3; C switches, since its chain has less work | G 1 2a 3 | G 1 2a 3 | G 1 2a 3 |

Block 2b is orphaned. At step 4, the last block of each chain was not yet agreed, but the chains with the last block removed agreed: this is common prefix with $k = 1$. A user who had accepted a payment in block 2b after zero confirmations would have lost it.

## Correctness

The protocol does not reach agreement with certainty. What it gives is a bound on the chance that a confirmed block is replaced. Let $p$ and $q = 1 - p$ be the shares of hash power of the honest miners and the attacker. In the race after a payment, each new block is honest with probability $p$ and the attacker's with probability $q$, so the attacker's deficit is a random walk. By the gambler's ruin, the attacker ever catches up from $z$ blocks behind with probability

$$q_z = \begin{cases} 1 & \text{if } p \le q, \\ (q/p)^z & \text{if } p > q. \end{cases}$$

The attacker mines in secret from the time of the payment. While the honest miners find $z$ blocks, the attacker finds $k$ blocks; Nakamoto takes $k$ as [Poisson](/poisson-distribution/) with mean $\lambda = z q/p$, and the attacker then needs to catch up from $z - k$ blocks behind. This gives the white paper's formula

$$P(q, z) = 1 - \sum_{k=0}^{z} \frac{\lambda^k e^{-\lambda}}{k!}\left(1 - (q/p)^{z-k}\right).$$

The proof derives $q_z$ from the first-step equations of the walk, and $P(q, z)$ from it, and notes what the analysis leaves out. The full proof is below.

The tests check $P$ against the tables of the white paper to seven decimals, for example $P(0.1, 5) = 0.0009137$ and $P(0.3, 10) = 0.0416605$, and the smallest $z$ with $P < 0.001$ for $q$ from 0.10 to 0.45 (5, 8, 11, 15, 24, 41, 89 and 340). A seeded simulation of the race in the paper's model agrees with $P$, and a simulation that plays every block agrees with the exact version, in which $k$ has a negative binomial distribution; the two versions differ a little, for example 0.2046 and 0.2000 for $q = 0.1$, $z = 1$.

The common prefix, chain quality and chain growth properties need an argument about all strategies of the adversary and about forks among honest miners. Garay, Kiayias and Leonardos (2015) proved them, and this page cites them without proof. Their condition is that the honest hash power exceeds the adversary's by a margin that grows with the chance of a block per round, that is, with the network delay measured in block intervals.

## Complexity

A block is found every $1/(hp)$ seconds on average, where $h$ is the total hash rate and $p$ the success chance of one hash; difficulty adjustment keeps this near a set interval, 600 seconds in Bitcoin. A confirmation at depth $z$ takes $z$ block intervals on average, $\Theta(z)$. Each block is flooded to all $n$ nodes, so it costs $\Theta(n)$ messages, or one per edge of the peer network. Each node stores the whole chain, $\Theta(L)$ blocks, though it may prune old transaction data. The energy cost is the hash work itself, which is the price of security in this design.

## Properties

- Open membership: no list of nodes is needed, and no node knows $n$.
- Probabilistic finality: the chance of a reversal at depth $z$ falls exponentially in $z$, but never reaches zero.
- Safety needs an honest majority of hash power, with a margin for network delay; with $q \ge 1/2$, $q_z = 1$ and the attacker can rewrite any block.
- Randomized: who proposes the next block is decided by the proof-of-work lottery.
- Not incentive compatible: by selfish mining, a pool with share $\alpha > 1/3$ gets more than its share of the blocks, even with no help in ties.

## Variants and improvements

- **Selfish mining (Eyal and Sirer, 2014).** A pool keeps its blocks private and publishes them to orphan honest blocks. With $\gamma$ the fraction of honest miners that mine on the pool's block during a tie, the pool's share of the main chain is
$$R(\alpha, \gamma) = \frac{\alpha(1-\alpha)^2(4\alpha + \gamma(1 - 2\alpha)) - \alpha^3}{1 - \alpha(1 + (2 - \alpha)\alpha)},$$
which exceeds $\alpha$ when $\alpha > (1 - \gamma)/(3 - 2\gamma)$: $1/3$ for $\gamma = 0$ and $1/4$ for $\gamma = 1/2$. The tests simulate the strategy and check $R$ to within 0.01.
- **GHOST and inclusive rules.** Choose the branch whose subtree has the most work, counting orphaned blocks, so that fast block rates waste less honest work.
- **Proof of stake chains.** Replace the work lottery by a lottery weighted by stake, with a longest-chain rule as in Ouroboros: see [proof of stake](/proof-of-stake/).
- **Finality gadgets.** Run a Byzantine agreement protocol, such as Casper FFG, over the chain to make blocks final with certainty once enough validators vote.
- **Committee-based protocols.** Use proof of work only to choose a committee, which then runs a classic protocol such as [PBFT](/pbft/), [Tendermint](/tendermint/) or [HotStuff](/hotstuff/).

## When to use it

Use it when the set of participants is open and unknown, there is no trusted way to give out identities, and a delay of several block intervals for confirmation is acceptable. If the participants are known, a Byzantine fault-tolerant protocol such as [PBFT](/pbft/) or [HotStuff](/hotstuff/) gives final decisions in a few message delays at far lower energy cost. If they are trusted not to lie, [Raft](/raft/) or [Paxos](/paxos/) is simpler still.

## Pitfalls

- **Zero confirmations.** A transaction that is not yet in a block, or is only in the last block, can be replaced. The example above loses a payment in block 2b.
- **Fixed confirmation depth for all values.** The safe depth depends on the attacker's share: 5 blocks give $P < 0.001$ for $q = 0.10$, but 24 blocks are needed for $q = 0.30$. Large payments need more depth.
- **Longest chain instead of most work.** With varying difficulty, counting blocks lets a chain of easy blocks win.
- **Honest majority is not enough for fairness.** Selfish mining shows that the protocol rewards deviation above a pool share of about 1/3, or less when the pool wins ties.
- **Network delay.** If blocks take long to spread compared to the block interval, honest miners waste work on forks, and the share an attacker needs falls below one half. The test with a delay of 10 rounds and a block chance of 0.2 per miner per round shows chains that disagree deeply.
- **The Poisson model is an approximation.** The exact count of attacker blocks is negative binomial, and the attacker can also prepare blocks in advance. Use the exact model to set confirmation depths.

## Implementations

## History

Satoshi Nakamoto published the Bitcoin white paper in October 2008 and released the software in January 2009. The paper combined three older ideas: the hash puzzle of Back's Hashcash, a chain of timestamps linked by hashes, and agreement by following the chain with the most work, and it bounded the success of a double spend with a gambler's ruin argument. Eyal and Sirer showed in 2013, published in 2014, that mining is not incentive compatible. Garay, Kiayias and Leonardos gave the first proof of the protocol's properties in 2015, in a synchronous model, and later work extended it to networks with bounded delay and to chains with changing difficulty.

## References
