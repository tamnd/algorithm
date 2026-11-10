---
tag: VADGDP
kind: concept
slug: proof-of-stake
name: Proof of stake
aliases:
- PoS
area: distributed/consensus
level: intro
summary: A blockchain picks who proposes and votes on blocks in proportion to the coins they hold and lock up, instead of by hash work. It must deal with costless forks and with old keys rewriting history.
prereqs: [proof-of-work, nakamoto-consensus, digital-signature]
see_also: [nakamoto-consensus, proof-of-work, verifiable-random-function, byzantine-fault-tolerance, tendermint, hotstuff, pbft, quorum-intersection]
sources:
  - paper: doi:10.1007/978-3-319-63688-7_12
    title: Aggelos Kiayias, Alexander Russell, Bernardo David and Roman Oliynykov, Ouroboros, a provably secure proof-of-stake blockchain protocol, Advances in Cryptology (CRYPTO 2017), LNCS 10401, pages 357 to 388
    locator: the synchronous model with slots and epochs, slot leader election by stake with a coin-tossing protocol for the seed, and the honest majority of stake assumption
  - paper: doi:10.1145/3132747.3132757
    title: Yossi Gilad, Rotem Hemo, Silvio Micali, Georgios Vlachos and Nickolai Zeldovich, Algorand, scaling Byzantine agreements for cryptocurrencies, Proceedings of the 26th ACM Symposium on Operating Systems Principles (SOSP), 2017, pages 51 to 68
    locator: cryptographic sortition with verifiable random functions, the BA* agreement protocol, and the assumptions of more than 2/3 honest money and of weak and strong synchrony
  - url: https://arxiv.org/abs/1710.09437
    title: Vitalik Buterin and Virgil Griffith, Casper the friendly finality gadget, 2017
    locator: checkpoints, justification and finality by 2/3 of deposits, the two slashing conditions, accountable safety and plausible liveness
  - book: isbn:9780691171692
    title: Arvind Narayanan, Joseph Bonneau, Edward Felten, Andrew Miller and Steven Goldfeder, Bitcoin and Cryptocurrency Technologies, Princeton University Press, 2016
    locator: the chapter on alternative mining puzzles, which discusses proof of stake and the nothing at stake problem
---

Proof of stake is a way to run a blockchain in which the right to propose and approve blocks goes to holders of the chain's own coins, in proportion to their stake, instead of to whoever does the most hash work as in [proof of work](/proof-of-work/). A block costs only a [signature](/digital-signature/) to make, so the protocol must stop two attacks that proof of work prevents by cost: signing on every fork (the nothing at stake problem) and building a different history from far back with old keys (the long-range attack). The two main designs are longest-chain protocols with stake-weighted leaders, such as Ouroboros (Kiayias et al., 2017), and protocols in which a stake-weighted committee runs Byzantine agreement, such as Algorand (Gilad et al., 2017) and Casper FFG (Buterin and Griffith, 2017). Their security assumes that an honest majority, or two thirds, of the stake follows the protocol, together with a timing assumption on the network.

## In plain words

In proof of work, the right to add a page to the shared notebook is won by burning electricity. In proof of stake, it is won by owning coins. Someone with a tenth of the coins gets picked about a tenth of the time.

Making a page is now almost free, and that makes new kinds of cheating possible. A person could approve two different versions of the notebook at once, because it costs nothing. So the rules lock up each approver's coins as a deposit, and anyone who catches them signing two versions can take the deposit away.

Another trick is to buy old keys from people who have sold all their coins. They have nothing to lose now, and with their old keys a cheater can write a fake history from long ago. New users protect themselves by starting from a recent page that they know is real.

## The idea

**Leader selection by stake.** Time is split into slots. In each slot, the protocol picks a leader with probability proportional to stake, using randomness that nobody can bias or predict too early. Two ways are common:

- *A shared random seed.* Ouroboros runs a coin-tossing protocol among the stakeholders of one epoch to make the seed for the next epoch. The seed then picks the leader of each slot by "follow the satoshi": choose a random coin among all coins, and the owner of that coin leads.
- *Private lotteries.* Algorand and later versions of Ouroboros let each user evaluate a [verifiable random function](/verifiable-random-function/) on the seed and the slot with their secret key. A user whose output is below a threshold set by their stake is selected, and the output comes with a proof that others can check. Nobody, not even an attacker, knows who is selected until the selected user speaks.

**Nothing at stake.** In proof of work, a miner must split its hash power to mine on two branches. In proof of stake, signing a block on every branch costs nothing, so a validator who only wants rewards should sign everything, and forks never settle. Two fixes are used. *Slashing:* validators lock a deposit, and two signed messages that contradict each other are proof of misbehavior that destroys part of the deposit. *Agreement instead of chain choice:* if a block is final only after votes from two thirds of the stake, signing two conflicting blocks is equivocation, which the agreement protocol detects.

**Long-range attacks.** A validator that has withdrawn its stake has nothing to lose, but its old keys were valid in the past. An attacker who collects enough old keys that once held a majority can build a chain that branches off far in the past, and a node that joins later sees two chains with valid signatures. Fixes: *key-evolving signatures*, where users erase old secret keys so that past blocks cannot be re-signed (Algorand and Ouroboros Praos use forward-secure keys); *weak subjectivity*, where a new node starts from a recent checkpoint that it gets from a trusted source; and *finality*, where nodes never revert a block that the agreement protocol has finalized.

**Accountable safety.** Casper FFG gives a precise form of the slashing idea. Validators vote for links between checkpoints. A checkpoint is *justified* when validators with two thirds of the deposits vote for a link to it from a justified checkpoint, and *finalized* when it is justified and validators with two thirds of the deposits vote for a link from it to its direct child checkpoint. Two rules are slashable: voting for two different targets at the same height, and casting a vote whose span surrounds the span of one's other vote. Theorem: if two conflicting checkpoints are both finalized, validators with at least one third of the deposits broke a slashing rule. The core of the proof is [quorum intersection](/quorum-intersection/): two sets of two thirds of the deposits overlap in at least one third.

**Security assumptions, stated plainly.**

| protocol | kind | safety assumption | timing assumption | adversary |
|---|---|---|---|---|
| Ouroboros | longest chain, stake-weighted slot leaders | more than half of the stake is honest in each epoch | synchronous: messages arrive within a slot | corruption takes effect only after a delay; stakeholders take part when elected |
| Algorand | committee by sortition, then Byzantine agreement (BA*) | more than 2/3 of the money is honest | safety under weak synchrony, liveness needs strong synchrony | can corrupt users at once, but each committee member speaks once with a fresh key |
| Casper FFG | finality gadget over a block proposal chain | fewer than 1/3 of the deposits act Byzantine, else at least 1/3 is slashed | liveness needs at least 2/3 of the deposits honest and online, and a working proposal mechanism | validator set and deposits are known; long-range attacks are handled by weak subjectivity |

## Examples

**Stake-weighted leaders.** Three holders have stakes A 50, B 30 and C 20. Each slot, a random coin number from 0 to 99 picks the leader: 0 to 49 is A, 50 to 79 is B, 80 to 99 is C. Over many slots A leads about half the time. If A splits its 50 coins into five accounts of 10, its share of slots stays the same, so creating many identities does not help, which is the purpose of weighting by stake.

**Nothing at stake.** A fork has branches X and Y of the same length. Validator V signs a block on X and a block on Y for the same slot. Without slashing, V loses nothing and earns the reward on whichever branch wins. With slashing, any node that sees both signed blocks can include them in a later block as evidence, and V's deposit is cut.

**Accountable safety with four validators.** Four validators each have a deposit of 25. Finalizing a checkpoint needs votes worth at least $2/3$ of 100, so at least 3 validators. If checkpoint $a$ is finalized with votes from $\{1, 2, 3\}$ and a conflicting checkpoint $b$ with votes from $\{2, 3, 4\}$, validators 2 and 3, with half of all deposits, voted for both, and their votes break a slashing rule.

**Non-example.** A protocol that picks the leader by a hash of the previous block alone lets the current leader try many candidate blocks and publish the one whose hash makes itself leader again. Leader randomness must not be grindable by the people it selects.

## Where it is used

- **Ethereum.** Since 2022, Ethereum runs proof of stake with Casper FFG for finality together with a fork-choice rule for the head of the chain.
- **Cardano.** Uses the Ouroboros family of protocols.
- **Algorand.** Uses cryptographic sortition and its BA* agreement protocol.
- **BFT chains.** Cosmos chains use [Tendermint](/tendermint/), a Byzantine agreement protocol among validators weighted by stake; other chains use [HotStuff](/hotstuff/) or [PBFT](/pbft/) variants in the same way.

## References
