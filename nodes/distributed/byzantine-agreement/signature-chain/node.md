---
tag: A5QCFM
kind: concept
slug: signature-chain
name: Signature chain
aliases:
- chain of signatures
- signed relay chain
area: distributed/byzantine-agreement
level: advanced
summary: A value with a sequence of signatures, the first by its sender and each later one on the value and the earlier signers. It proves who relayed the value, and in what order.
prereqs: [digital-signature, signed-messages-model]
see_also: [dolev-strong-algorithm, signed-messages-algorithm, quorum-certificate, aggregate-signature, hash-chain, threshold-signature, dolev-reischuk-lower-bound, byzantine-broadcast]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 4 (the notation v:i and v:0:j:k for a value signed by a sequence of generals, page 390)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (messages with sequences of distinct signatures, and the rule that a message in phase k carries k signatures)
  - url: https://elaineshi.com/docs/blockchain-book.pdf
    title: Elaine Shi, Foundations of Distributed Consensus and Blockchains, book draft
    locator: Chapter 3, Section 3.4 (a value with r distinct signatures, the first by the sender, counts in round r)
  - paper: doi:10.1145/2455.214112
    title: Danny Dolev and Rüdiger Reischuk, Bounds on information exchange for Byzantine agreement, Journal of the ACM 32(1), 1985
    locator: pages 191 to 204 (counting the signatures that authenticated algorithms must send)
---

A signature chain is a value together with an ordered list of signatures: the first by the process that created the value, and each later one by a process that relayed it, signed over the value and all earlier signers. A valid chain of length $k$ proves that $k$ distinct processes each passed the value on, in this order, and no one can remove, reorder or invent a signature of a correct process. In the [signed messages model](/signed-messages-model/), this is the data structure that lets Byzantine broadcast tolerate any number of faults. The algorithms [SM(m)](/signed-messages-algorithm/) and [Dolev-Strong](/dolev-strong-algorithm/) send signature chains and differ in how they use them, so this page treats the chain on its own.

## In plain words

A letter is passed from hand to hand. Each person who passes it on signs the bottom of the letter, under all earlier signatures. Anyone who receives the letter can read the whole list and check each signature. If an honest person's name is on the list, that person really did hold the letter and sign it at that point.

A liar can cut off the last few signatures, or add his own, but he cannot remove a name in the middle or add an honest person's name. So the number of names on the letter tells how many people already vouched for it, and how far it has travelled.

## The idea

**The structure.** Fix a sender $s$ and a value $v$. A chain of length $k$ is

$$c = (v;\ \sigma_1, \sigma_2, \ldots, \sigma_k)$$

with signers $p_1, \ldots, p_k$, where $p_1 = s$ and $\sigma_j = \mathrm{sign}_{p_j}(v, p_1, \ldots, p_{j-1})$. Each signature covers the value and the list of earlier signers. A *nested* variant signs the whole earlier chain, signatures included, as in the notation $v{:}0{:}j{:}k$ of Lamport, Shostak and Pease. A *hashed* variant signs a hash of the earlier chain. All three give the same guarantees below.

**Operations.**

| Operation | Effect | Cost |
| --- | --- | --- |
| start$(s, v)$ | $(v;\ \mathrm{sign}_s(v))$ | 1 signature |
| extend$(c, p)$ | append $\mathrm{sign}_p(v, p_1, \ldots, p_k)$ | 1 signature |
| verify$(c, s, r)$ | check $k = r$, $p_1 = s$, signers distinct, each $\sigma_j$ valid | $k$ checks |
| signers$(c)$ | the list $p_1, \ldots, p_k$ | $O(k)$ |

The size of a chain is $k$ signatures plus the value. In the algorithms, $k \le t + 1$.

**What a valid chain proves.**

1. *No forged links.* For each correct $p_j$ in the list, $p_j$ signed $v$ after the exact list $p_1, \ldots, p_{j-1}$. A correct process signs only a chain that it received and verified, so it held a valid chain $p_1, \ldots, p_{j-1}$ for $v$.
2. *No removal in the middle.* Every signature after position $j$ covers $p_j$, so removing or reordering $p_j$ makes a later signature invalid.
3. *Prefixes stay valid.* Any prefix $(v;\ \sigma_1, \ldots, \sigma_j)$ is again a valid chain. A faulty process can shorten a chain it received. Algorithms must not let a shorter chain help the adversary.
4. *Enough signers include a correct one.* A chain with $t + 1$ distinct signers has at least one correct signer.

**Length as a clock.** In Dolev-Strong, a chain counts in round $r$ only if it has exactly $r$ distinct signers. A correct process that accepts a chain in round $r \le t$ adds its signature and sends it on, so every correct process gets a chain of length $r + 1$ in round $r + 1$. A chain accepted in round $t + 1$ has $t + 1$ signers, so by property 4 a correct signer accepted it earlier and has already sent it to everyone. Shortening a chain does not help: it then counts only in an earlier round, which has passed. This is the core of the [Dolev-Strong correctness proof](/dolev-strong-algorithm/).

**Proof of equivocation.** Two valid chains that start with signatures of $s$ on different values prove that $s$ is faulty, to any process. SM(m) and Dolev-Strong use this: a process that holds two values for one sender outputs a default.

**A chain is not a certificate.** A [quorum certificate](/quorum-certificate/) is a set of signatures by different processes on the *same* message, with no order. It proves that many processes agreed. A signature chain has signatures on *growing* messages, in an order. It proves a path of relays. A [threshold signature](/threshold-signature/) or an [aggregate signature](/aggregate-signature/) can compress a certificate to one signature. Sequential aggregate signatures do the same for a chain.

## Examples

**One relay, four processes.** Let $s = 0$ sign the value 1. Process 2 receives $(1;\ \sigma_0)$ in round 1, verifies it, and sends $(1;\ \sigma_0, \sigma_2)$ to processes 1 and 3 in round 2, with $\sigma_2 = \mathrm{sign}_2(1, 0)$. In LSP's notation this is $1{:}0{:}2$. Process 3 checks that the chain has 2 distinct signers, that the first is 0, and both signatures. It now knows that process 2 accepted the value in round 1, if process 2 is correct.

**A failed forgery.** A faulty process 3 wants to show process 1 that the sender signed 0. It has only $(1;\ \sigma_0)$. It can add its own signature to get $(1;\ \sigma_0, \sigma_3)$, but it cannot produce $\mathrm{sign}_0(0)$ unless process 0 is faulty too. The implementations model this with a set of issued signatures: an attempt to sign for a correct process raises an error, and a chain with an unissued signature fails verification.

**A late chain.** With $n = 5$ and $t = 3$, three faulty processes can sign a second value among themselves in the order sender, helper, helper, and show the chain of length 3 to one correct process only, in round 3. Since the chain has 3 signers, it counts in round 3. The correct process adds its signature and sends a chain of length 4 to the other correct process in round 4 $= t + 1$. If the algorithm stopped after 3 rounds, the second correct process would never see the second value, and the two would decide differently. The implementation of Dolev-Strong runs this attack and shows the disagreement after 3 rounds.

## Where it is used

- **[SM(m)](/signed-messages-algorithm/).** Each lieutenant adds the values of all valid chains to its set $V_i$ and relays chains of length at most $m$.
- **[Dolev-Strong](/dolev-strong-algorithm/).** Each process relays only the first two values it accepts, and a value counts in round $r$ only with a chain of length $r$. This cuts the messages to $O(n^2)$.
- **Lower bounds on signatures.** The [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/) counts signatures, and shows $\Omega(nt)$ are needed by every authenticated algorithm.
- **Certificate chains.** In a public key infrastructure, each certificate is signed by the issuer of the previous one. The structure is similar: a path of signers that each vouch for the next step.
- **Hash-linked logs.** A [hash chain](/hash-chain/) of signed blocks, as in a blockchain or a tamper-evident log, has the same property that a later entry fixes all earlier ones.

## References
