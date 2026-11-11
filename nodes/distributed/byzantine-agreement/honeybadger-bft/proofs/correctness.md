---
title: HoneyBadgerBFT outputs the same block at every honest node
proves: [correctness]
status: full
---

**Claim.** Let $N = 3f + 1$ nodes run one epoch of HoneyBadgerBFT (lines L1 to L8) in the asynchronous model, with at most $f$ Byzantine nodes, reliable links, and these components:

- (RBC) a reliable broadcast with *validity* (if the sender is honest, every honest node delivers its value), *agreement* (no two honest nodes deliver different values) and *totality* (if one honest node delivers, every honest node delivers). The erasure-coded broadcast of the epoch has these properties; the proof for the plain version is on the page [Bracha reliable broadcast](/bracha-reliable-broadcast/).
- (ABA) a binary agreement with *agreement*, *validity* (a decided bit was the input of some honest node) and *termination* (if every honest node gives an input, every honest node decides, with probability 1). The protocol of Mostéfaoui, Moumen and Raynal (2014) with a threshold common coin is used; its proof is in their paper.
- (TPKE) a threshold encryption scheme in which $f + 1$ valid decryption shares of a ciphertext give its plaintext, invalid shares are detected, and $f$ shares give no information about it.

Then, with probability 1, every honest node outputs a block, and all honest nodes output the same block. It contains the batches of at least $N - f$ nodes, and the adversary must fix which batches are in it before it can read any of them.

The epoch, at node $i$: encrypt a batch (L1) and send the ciphertext by RBC (L2); on delivery of RBC$_j$, give input 1 to ABA$_j$ if ABA$_j$ has no input (L3); when $N - f$ instances of ABA have decided 1, give input 0 to every ABA without an input (L4); when every ABA has decided, let $S$ be the set of $j$ with ABA$_j = 1$ and wait until RBC$_j$ delivered for every $j \in S$ (L5); send a decryption share of each such ciphertext (L6); decrypt each with $f + 1$ valid shares (L7); output the sorted union of the plaintexts (L8). L3 to L5 are the asynchronous common subset (ACS) of Ben-Or, Kelmer and Rabin.

## The common subset

**Lemma 1.** If an honest node sees ABA$_j$ decide 1, then every honest node delivers RBC$_j$ and gives an input to ABA$_j$, and ABA$_j$ decides 1 at every honest node.

*Proof.* By ABA validity, some honest node gave input 1 to ABA$_j$, which it does only after it delivers RBC$_j$ (L3). By RBC totality every honest node delivers RBC$_j$, and then gives ABA$_j$ an input (1 by L3 if it has none yet). So every honest node gives an input, ABA$_j$ terminates at all of them, and by ABA agreement all decide 1. $\square$

**Lemma 2.** Every honest node sees at least $N - f$ instances decide 1.

*Proof.* Suppose first that no honest node ever sees $N - f$ instances decide 1. Then no honest node gives input 0 (L4 never runs). For each of the at least $N - f$ honest senders $j$, RBC validity makes every honest node deliver RBC$_j$ and give input 1 to ABA$_j$; by termination and validity, ABA$_j$ decides 1 at every honest node. That is $N - f$ instances deciding 1, a contradiction. So some honest node sees $N - f$ instances decide 1, and by Lemma 1 every honest node sees the same $N - f$ instances decide 1. $\square$

**Lemma 3.** Every ABA instance terminates at every honest node, and all honest nodes compute the same set $S$, with $|S| \ge N - f$.

*Proof.* By Lemma 2 every honest node reaches L4 and gives input 0 to every instance without an input, so every honest node gives an input to every instance; by termination every instance decides at every honest node. By ABA agreement the decisions are the same everywhere, so $S$ is the same. By Lemma 2, $|S| \ge N - f$. $\square$

**Lemma 4.** For every $j \in S$, every honest node delivers RBC$_j$, and all deliver the same ciphertext $c_j$.

*Proof.* Delivery is Lemma 1; equality is RBC agreement. $\square$

## The block

**Theorem 1 (agreement and termination).** Every honest node outputs a block, and all output the same block.

*Proof.* By Lemmas 3 and 4 every honest node reaches L6 with the same $S$ and the same ciphertexts $c_j$ for $j \in S$. Every honest node sends a valid share for each $c_j$, and there are $N - f \ge f + 1$ honest nodes, so every honest node gets $f + 1$ valid shares of each $c_j$; invalid shares from faulty nodes are rejected. Decryption with $f + 1$ valid shares gives the unique plaintext, so all honest nodes get the same batches, and the sorted union is the same block. $\blacksquare$

**Theorem 2 (the subset is fixed before the contents are known).** No honest node sends a decryption share for $c_j$ before it knows $S$, and $S$ is decided before then.

*Proof.* L6 runs only after every ABA has decided (L5). Before that, the adversary holds at most $f$ shares of any ciphertext, its own, which by the property of TPKE tell it nothing about the batch. So the decisions of all ABA instances, which fix $S$, are made without the adversary knowing the plaintexts. $\blacksquare$

Theorem 2 is the reason for the encryption. Without it, the adversary, which controls the schedule, could read the batches as they are broadcast and delay exactly the RBCs that hold a transaction it wants to censor, so that their ABAs decide 0. The paper uses this property, together with the random choice of each batch from the front of the buffer, to show that a transaction that reaches the front of enough honest buffers is committed within a constant expected number of epochs.

## Cost of one epoch

Let $B$ be the batch size (so each node proposes $B/N$ transactions), $|tx|$ the size of a transaction, and $\lambda$ the size of a hash or a share.

- **RBC.** Each node sends a value of size $|v| = (B/N)|tx|$ cut into $N$ fragments of size $|v|/(N - 2f)$, each with a Merkle branch of $O(\lambda \log N)$. VAL sends $N$ fragments and ECHO sends $N^2$, so one RBC costs $O(N|v| + \lambda N^2 \log N)$, using $N/(N - 2f) \le 3$. All $N$ RBCs cost $O(N B |tx| + \lambda N^3 \log N)$.
- **ABA.** $N$ instances, each with $O(N^2)$ messages of size $O(\lambda)$ per round and a constant expected number of rounds: $O(\lambda N^3)$ in expectation.
- **Decryption.** Each node sends one share per ciphertext of $S$ to every node: $O(\lambda N^3)$.

The total is $O(N B |tx| + \lambda N^3 \log N)$. When $B = \Omega(\lambda N^2 \log N)$, the second term is at most a constant times the first, and the cost per transaction is $O(N |tx|)$, linear in $N$. The implementation counts bytes: with $B = 40 N^2$ and 250-byte transactions, the bytes per transaction divided by $N |tx|$ are 2.55, 2.72 and 2.80 for $N = 4, 7, 10$, close to $N^2/(N(N - 2f))$; with $B = 7$ and $N = 7$ the ratio is above 17.

## Where the assumptions are used

- $N \ge 3f + 1$: in RBC, in ABA, and in Theorem 1 ($N - f \ge f + 1$ honest decryption shares).
- Randomness: only inside ABA, through the common coin. Without it, the FLP result rules out termination.
- The order L5 before L6: Theorem 2.
