---
tag: QX6G31
kind: algorithm
slug: honeybadger-bft
name: HoneyBadgerBFT
aliases:
- HoneyBadger BFT
- Honey Badger of BFT protocols
area: distributed/byzantine-agreement
level: research
summary: Asynchronous BFT atomic broadcast. Threshold-encrypted batches, erasure-coded reliable broadcast and n binary agreements form a common subset. O(n) bits per transaction.
solves: [byzantine-state-machine-replication]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, f: the largest number of Byzantine nodes, B: the batch size in transactions, λ: the size of a hash or a share}
  time: {expected: O(log n)}
  messages: {expected: O(n^3)}
  bits: {expected: O(n B + λ n^3 log n)}
  space: {extra: O(B + n^2)}
properties: {deterministic: false, recursive: false}
prereqs: [byzantine-reliable-broadcast, bracha-asynchronous-agreement, asynchronous-model, threshold-signature]
see_also: [bracha-reliable-broadcast, byzantine-reliable-broadcast, bracha-asynchronous-agreement, byzantine-state-machine-replication, pbft, flp-impossibility, reed-solomon-code, merkle-tree]
sources:
  - paper: doi:10.1145/2976749.2978399
    title: Andrew Miller, Yu Xia, Kyle Croman, Elaine Shi and Dawn Song, The honey badger of BFT protocols, ACM CCS 2016
    locator: the epoch with threshold encryption, the erasure-coded reliable broadcast, the common subset from N binary agreements, the communication analysis, and the censorship argument
  - paper: doi:10.1145/197917.198088
    title: Michael Ben-Or, Boaz Kelmer and Tal Rabin, Asynchronous secure computations with optimal resilience, PODC 1994
    locator: the agreement on a common subset from N reliable broadcasts and N binary agreements
  - paper: "Christian Cachin and Stefano Tessaro, Asynchronous verifiable information dispersal, SRDS 2005"
    locator: the reliable broadcast with erasure codes and Merkle branches (AVID)
  - paper: doi:10.1145/2611462.2611468
    title: Achour Mostéfaoui, Hamouma Moumen and Michel Raynal, Signature-free asynchronous Byzantine consensus with t < n/3 and O(n^2) messages, PODC 2014
    locator: the binary agreement with binary-value broadcast and a common coin
  - paper: doi:10.1007/s00145-005-0318-0
    title: Christian Cachin, Klaus Kursawe and Victor Shoup, Random oracles in Constantinople, Practical asynchronous Byzantine agreement using cryptography, Journal of Cryptology 18(3), 2005
    locator: the threshold common coin
---

HoneyBadgerBFT is an [asynchronous](/asynchronous-model/) protocol for [Byzantine state machine replication](/byzantine-state-machine-replication/) with $N = 3f + 1$ nodes. It makes no timing assumption at all, so a network that delays messages for any time can slow it down but cannot stop it. It works in epochs. In each epoch every node encrypts a batch of transactions with threshold encryption and sends the ciphertext by an erasure-coded [reliable broadcast](/byzantine-reliable-broadcast/). Then $N$ randomized binary agreements, one per node, choose a common subset of at least $N - f$ ciphertexts, which the nodes decrypt together. With large batches each transaction costs $O(N)$ bits, which is optimal up to constants. Miller, Xia, Croman, Shi and Song published it at CCS 2016.

## In plain words

A group of $3f + 1$ computers must agree on which transactions to accept, on a network where any message may be late for any time, and up to $f$ computers may cheat. No computer leads.

In each round, every computer locks a pile of transactions in a box that only $f + 1$ computers together can open, and sends the box to all, cut into pieces so that no one sends too much. Then the computers vote on each box: "did I get it?" A coin that no one can predict breaks ties. The boxes that win their votes, at least $N - f$ of them, are opened, and their transactions form the next block. Cheaters cannot block a transaction they do not like, because they cannot see inside the boxes until the vote is over.

## The problem

There are $N$ nodes, at most $f$ Byzantine, with $N \ge 3f + 1$, reliable authenticated links, and a trusted setup of threshold keys. The network is fully asynchronous: the adversary decides when each message arrives, as long as each one arrives in the end. Clients send transactions to the nodes. The protocol must give atomic broadcast, that is [total order broadcast](/total-order-broadcast/) with Byzantine faults: all honest nodes output the same sequence of blocks (agreement and total order), and every transaction that enough honest nodes hold is output in the end (censorship resilience). By the FLP result no deterministic protocol does this, so HoneyBadgerBFT uses randomness in its binary agreements.

## The algorithm

Each node keeps a buffer of transactions. One epoch at node $i$, with batch size $B$:

```pseudo id=main
HONEYBADGER-EPOCH(i)                                                 ▷ N = 3f + 1 nodes, asynchronous
L1  x ← B/N transactions chosen at random from the first B in the buffer; c ← TPKE.Enc(pk, x)
L2  RBC_i(c): cut c into N fragments with a Reed-Solomon code and a Merkle root; VAL, ECHO, READY
L3  on delivering RBC_j: if ABA_j has no input: input 1 to ABA_j
L4  when N - f instances ABA_j have decided 1: input 0 to every ABA_j with no input
L5  S ← {j : ABA_j decided 1}; wait until RBC_j delivered c_j for every j in S
L6  for each j in S: send my decryption share of c_j to all
L7  on f + 1 valid shares of c_j: x_j ← TPKE.Dec(c_j)
L8  block ← the sorted union of x_j for j in S; remove its transactions from the buffer
```

**Reliable broadcast with erasure codes (AVID).** The sender encodes $c$ with a [Reed-Solomon code](/reed-solomon-code/) into $N$ fragments, any $N - 2f$ of which rebuild $c$, and builds a [Merkle tree](/merkle-tree/) over them. It sends fragment $j$ with its Merkle branch to node $j$ (VAL). Each node forwards its own fragment to all (ECHO). On $N - f$ valid ECHO messages for a root, a node rebuilds $c$, encodes it again, and checks that it gets the same root; if so it sends READY. On $f + 1$ READY it sends READY too, and on $2f + 1$ READY and $N - 2f$ fragments it delivers $c$. This is the structure of [Bracha's broadcast](/bracha-reliable-broadcast/) with fragments in place of full copies.

**Binary agreement (ABA).** Each ABA$_j$ is the protocol of Mostéfaoui, Moumen and Raynal: in each round a node sends its estimate (EST), relays a value that $f + 1$ nodes sent, adds to $bin\_values$ a value that $2f + 1$ nodes sent, sends one value of $bin\_values$ (AUX), waits for $N - f$ AUX messages with values in $bin\_values$, and then opens a threshold common coin $s$. If the AUX values are a single $b$, the estimate becomes $b$, and the node decides $b$ if $b = s$; otherwise the estimate becomes $s$. A node that decides tells the others (TERM) and keeps taking part until $2f + 1$ nodes have said TERM.

## Example

Take $N = 4$, $f = 1$, node 3 faulty and silent, and $B = 40$, so each node proposes 10 transactions.

1. Nodes 0, 1 and 2 encrypt their batches and broadcast them. Node 3 sends nothing.
2. Every honest node delivers RBC$_0$, RBC$_1$ and RBC$_2$ in some order, and gives input 1 to ABA$_0$, ABA$_1$, ABA$_2$.
3. The three instances decide 1. That is $N - f = 3$, so each honest node gives input 0 to ABA$_3$, which decides 0.
4. $S = \{0, 1, 2\}$. Each honest node sends three decryption shares to all, decrypts the three ciphertexts with 2 shares each, and outputs a block of 30 transactions.

If instead node 0 is slow, the adversary can make ABA$_0$ decide 0 when nodes 1, 2 and the faulty node 3 finish first. The block then has the batches of 1, 2 and 3. At least $N - f$ batches are always in, but which ones depends on the schedule.

The tests run every set of faulty nodes for $N = 4$ and $N = 7$, with silence, equivocation in the broadcast, an encoding that does not match its root, votes for both values in every binary agreement, and forged fragments, coin shares and decryption shares, with and without a slow honest node. All honest nodes always output the same block. The mean number of rounds of a binary agreement in these runs is 1.6.

## Correctness

The full proof is in the proof file.

- **Every ABA gets an input.** The $N - f$ honest broadcasts deliver everywhere, so their ABAs decide 1 unless some node gave 0, which it does only after $N - f$ ABAs decided 1. Either way all nodes reach line L4, so every ABA gets an input from every honest node and terminates.
- **The same subset.** ABA agreement gives every honest node the same $S$, with $|S| \ge N - f$.
- **The same ciphertexts.** If ABA$_j$ decides 1, some honest node delivered RBC$_j$, so by totality every honest node does, and by RBC agreement all get the same $c_j$.
- **The same block.** $N - f \ge f + 1$ honest decryption shares open each $c_j$.
- **Censorship resilience.** No honest node sends a decryption share before $S$ is fixed, so the adversary chooses which broadcasts to slow down without knowing what is in them.

## Complexity

- **Bits.** Erasure coding makes one broadcast of a value $v$ cost $O(N|v| + \lambda N^2 \log N)$ instead of $O(N^2|v|)$. With $N$ batches of $B/N$ transactions, the epoch sends $O(N B |tx| + \lambda N^3 \log N)$ bits. For $B = \Omega(\lambda N^2 \log N)$, that is $O(N)$ bits per transaction. The tests measure 2.55, 2.72 and 2.80 times $N |tx|$ bytes per transaction for $N = 4, 7, 10$ with $B = 40 N^2$.
- **Messages.** $O(N^3)$ in expectation per epoch: $N$ broadcasts with $O(N^2)$ messages each, and $N$ agreements with $O(N^2)$ messages per round.
- **Time.** Each binary agreement takes a constant expected number of rounds. The epoch waits for the slowest of $N$ of them, which gives $O(\log N)$ expected rounds.
- **Cryptography.** Each node computes $O(N)$ decryption shares and checks $O(N^2)$ shares per epoch, which in practice dominates the running time.

## Properties

- **Asynchronous.** Safe and live with no timing assumption; no timeouts to tune.
- **Leaderless.** Every node proposes in every epoch, so a slow or faulty leader cannot stall it.
- **Randomized.** Only the binary agreements use randomness, through the common coin.
- **Optimal resilience.** $N \ge 3f + 1$.
- **High throughput, high latency.** Large batches make it efficient, but every epoch has many rounds of messages.

## Variants and improvements

- **The common subset with fewer agreements.** Later protocols, such as Dumbo, run fewer binary agreements per epoch than the $N$ of HoneyBadgerBFT, which lowers the latency.
- **DAG-based asynchronous protocols.** Protocols that build a graph of reliable broadcasts and order it with a coin, such as DAG-Rider, reach agreement without a separate common subset in each epoch.
- **Without threshold encryption.** Dropping the encryption keeps agreement but loses censorship resilience.
- **Fixes to the binary agreement.** Later work reported that the binary agreement of 2014, used as in the first HoneyBadgerBFT, can fail to terminate against an adversary that controls the schedule, and newer versions add a confirmation step before the coin. The simulator on this page uses a scheduler that does not adapt to the coin.

## When to use it

Use HoneyBadgerBFT, or one of its descendants, when the network may be slow or under attack for long periods, as in a wide-area deployment across organisations, and when throughput matters more than latency. When the network is usually timely, a partially synchronous protocol such as [PBFT](/pbft/) or [HotStuff](/hotstuff/) has much lower latency in the normal case.

## Pitfalls

- **Decrypting before the subset is fixed.** This gives the adversary the contents in time to censor them.
- **Small batches.** The $\lambda N^3 \log N$ overhead dominates unless $B$ is about $N^2 \log N$ or more; the tests show 17 times the linear cost with $B = N$.
- **Skipping the re-encoding check.** A sender can make fragments that decode to different values from different subsets; checking the root of the re-encoded value makes all honest nodes deliver the same value or none.
- **Halting an agreement at once.** A node that stops right after it decides can leave others without the $N - f$ messages they need; it must keep taking part until $2f + 1$ nodes have said TERM.
- **A predictable coin.** The binary agreement is live only if the adversary cannot learn the coin of a round before it fixes the messages of that round.

## Implementations

## History

Ben-Or, Kelmer and Rabin gave the agreement on a common subset in 1994, as a step of asynchronous secure computation. Cachin, Kursawe, Petzold and Shoup (2001) built asynchronous atomic broadcast from threshold cryptography, and Cachin and Tessaro (2005) made reliable broadcast cheaper with erasure codes. In 2016 Miller, Xia, Croman, Shi and Song put these pieces together with threshold encryption and the binary agreement of Mostéfaoui, Moumen and Raynal, as a practical protocol for cryptocurrencies. They called it HoneyBadgerBFT, after the animal that does not care about the network.

## References
