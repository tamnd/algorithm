---
tag: 8FSV21
kind: algorithm
slug: zyzzyva
name: Zyzzyva
aliases:
- speculative BFT
- Zyzzyva speculative Byzantine fault tolerance
area: distributed/byzantine-agreement
level: research
summary: Speculative BFT replication. Replicas execute in the primary's order at once; the client completes with 3f + 1 matching replies or a commit certificate. Its view change is unsafe.
solves: [byzantine-state-machine-replication]
model: partial-synchrony
complexity:
  vars: {n: the number of replicas, f: the largest number of Byzantine replicas, d: the largest message delay after GST, L: the number of requests since the last checkpoint}
  time: {best: 3d, worst: 5d}
  messages: {best: 2n, worst: O(n)}
  space: {extra: O(L)}
properties: {deterministic: true, recursive: false}
prereqs: [byzantine-state-machine-replication, pbft, quorum-certificate, partial-synchrony]
see_also: [pbft, hotstuff, quorum-certificate, byzantine-state-machine-replication, view-change, quorum-intersection, tendermint, honeybadger-bft]
sources:
  - paper: "Ramakrishna Kotla, Lorenzo Alvisi, Mike Dahlin, Allen Clement and Edmund Wong, Zyzzyva: speculative Byzantine fault tolerance, SOSP 2007"
    locator: the protocol with the fast path, the two-phase path with commit certificates, the view change, and Zyzzyva5
  - paper: "Ramakrishna Kotla, Lorenzo Alvisi, Mike Dahlin, Allen Clement and Edmund Wong, Zyzzyva: speculative Byzantine fault tolerance, ACM Transactions on Computer Systems 27(4), 2009"
    locator: the journal version with the full view change protocol
  - url: https://arxiv.org/abs/1712.01367
    title: Ittai Abraham, Guy Gueta, Dahlia Malkhi, Lorenzo Alvisi, Rama Kotla and Jean-Philippe Martin, Revisiting fast practical Byzantine fault tolerance, arXiv 1712.01367 (2017)
    locator: Sections 2.3 and 2.4, the two runs that violate safety
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the three-phase protocol that Zyzzyva shortens
---

Zyzzyva is a protocol for [Byzantine state machine replication](/byzantine-state-machine-replication/) with $n = 3f + 1$ replicas that makes the common case fast by *speculation*. The primary orders a request and the replicas execute it at once, before they agree on the order, and reply to the client. The client, not the replicas, checks agreement. If all $3f + 1$ replies match, the request is complete after three message delays. If only $2f + 1$ match, the client sends them back as a *commit certificate* and waits for $2f + 1$ acknowledgements. Kotla, Alvisi, Dahlin, Clement and Wong published it in 2007. In 2017 Abraham, Gueta, Malkhi, Alvisi, Kotla and Martin showed that its view change can lose a completed request, so the protocol as published is not safe.

## In plain words

A group of $3f + 1$ servers runs a service, and up to $f$ of them may cheat. One server, the primary, gives each request a number. The servers do not talk to each other first: each one runs the request at once and sends the answer, with its whole list of requests so far, to the client.

If all the servers send the same answer and the same list, the client is done. If some are slow but $2f + 1$ agree, the client sends their signed answers back as proof and waits for $2f + 1$ servers to say "noted". If the primary seems faulty, the servers change to a new primary, which must rebuild the list. That last step is where the published protocol goes wrong.

## The problem

The task is [Byzantine state machine replication](/byzantine-state-machine-replication/): $n = 3f + 1$ replicas, at most $f$ [Byzantine](/byzantine-failure-model/), signed messages, and clients that send requests. Every completed request must have the same position in the history of every honest replica (safety), and every request of an honest client must complete (liveness) under [partial synchrony](/partial-synchrony/). Zyzzyva adds a weaker promise for the replicas: an honest replica may execute a request speculatively and later roll it back, but a request that a client has completed is never rolled back.

## The algorithm

Each replica keeps its view $v$, its history (the list of requests it has executed), and the longest commit certificate it has seen. The primary of view $v$ is a fixed function of $v$. Real messages carry a hash of the history, not the history.

```pseudo id=main
ZYZZYVA                                                              ▷ n = 3f + 1 replicas
L1  primary of view v, on a request m: send ⟨ORDER-REQ, v, s, hash of history + m, m⟩ to all replicas
L2  replica in view v, on ORDER-REQ that extends its history by one: execute m; send ⟨SPEC-RESPONSE, v, s, history, reply⟩ to the client
L3  client, on 3f + 1 matching SPEC-RESPONSE: complete m                     ▷ fast path
L4  client, on 2f + 1 matching SPEC-RESPONSE only: CC ← the 2f + 1 responses; send ⟨COMMIT, CC⟩ to all replicas
L5  replica, on COMMIT with a valid CC that matches its history: keep CC if it is the longest; send LOCAL-COMMIT
L6  client, on 2f + 1 LOCAL-COMMIT: complete m                               ▷ two-phase path
L7  replica, on suspecting the primary: send ⟨VIEW-CHANGE, v + 1, its CC, its history⟩
L8  primary of v + 1, on 2f + 1 VIEW-CHANGE: history ← the history of the longest CC
L9      append each request that f + 1 histories hold at the next position; send NEW-VIEW; replicas adopt the history
```

With fewer than $2f + 1$ matching replies, the client sends its request to all replicas. They forward it to the primary and start a timer, and if the primary does not order it they move to a new view. A Byzantine primary that orders different requests at the same position is caught by a signed proof of the two ORDER-REQ messages. Checkpoints every $L$ requests let replicas discard old history, as in [PBFT](/pbft/).

## Example

**The fast path.** With $n = 4$ and all replicas honest, the client sends 1 request, the primary sends 3 ORDER-REQ messages, and the 4 replicas send 4 SPEC-RESPONSE messages: $2n = 8$ messages in 3 message delays. The tests count exactly this.

**The two-phase path.** If replica 3 is silent, the client gets 3 matching replies, a commit certificate. It sends 3 COMMIT messages and gets 3 LOCAL-COMMIT replies: 12 messages in 5 message delays.

**The view-change bug.** With $n = 4$ and $i_1$ Byzantine (Section 2.3 of the 2017 paper):

| view | events |
|---|---|
| 1 | Primary $i_1$ orders $a$ at $i_1$, $i_2$, $i_3$ and $b$ at $i_4$. A client gets a commit certificate for $a$; its COMMIT reaches only $i_1$. |
| 2 | Primary $i_2$ hears from $i_2$ ($a$), $i_4$ ($b$) and $i_1$, which hides the certificate and says $b$. The $f + 1$ rule picks $b$. All replicas execute $b$, and a client completes $b$ at position 1 on the fast path. |
| 3 | Primary $i_3$ hears from $i_1$ (certificate for $a$), $i_3$ ($b$) and $i_4$ ($b$). The certificate wins, so $a$ is at position 1, and a client completes it. |

Two clients completed different requests at position 1. The tests replay this run and a second one (Section 2.4), in which an older, longer certificate wins over a newer one.

## Correctness

The full proof is in the proof file.

- **Within a view, safety holds.** Every completion rests on $2f + 1$ signed responses for one view and history. Two such sets share an honest replica, whose histories in a view are prefixes of each other.
- **What a new view must keep.** A fast-path completion leaves $f + 1$ honest histories among any $2f + 1$ VIEW-CHANGE messages. A two-phase completion leaves a commit certificate at one honest replica among them.
- **The published rule is unsafe.** It puts any commit certificate before the $f + 1$ histories, and the longest certificate before newer ones. Both choices ignore the view in which the evidence was formed, and each gives a run in which two clients complete different requests at one position.

## Complexity

- **Latency.** Three message delays on the fast path (client, primary, replicas, client), five on the two-phase path.
- **Messages.** $2n$ on the fast path and about $4n$ on the two-phase path: linear, because replicas do not send to each other in the normal case. [PBFT](/pbft/) needs $\Theta(n^2)$.
- **Cryptography.** Each replica signs one response per request, or per batch.
- **Space.** The history since the last checkpoint, $O(L)$ requests, plus the longest commit certificate.

## Properties

- **Speculative.** Replicas execute before agreement, so they must be able to roll back requests that a new view drops.
- **Client-driven agreement.** The client sees the matching replies and forms the certificate.
- **Fast path needs every replica.** One slow or silent replica sends every request to the slower path, so a single faulty replica can remove the gain.
- **Not safe as published.** The view change has the flaw shown above.
- **Optimal resilience.** $n = 3f + 1$.

## Variants and improvements

- **Zyzzyva5.** With $n = 5f + 1$ replicas, $4f + 1$ matching replies complete a request on the fast path, so up to $f$ slow replicas do not force the two-phase path.
- **Batching.** The primary orders a batch of requests in one ORDER-REQ, which spreads the cost of signatures.
- **A safe view change.** The new primary must rank all evidence by the view in which it was formed, as PBFT does with prepared certificates; choosing the certificate of the highest view alone fixes the second run but not the first. Later protocols with a fast path, such as SBFT, use a view change designed with this in mind.
- **Linear protocols with no speculation.** [HotStuff](/hotstuff/) has linear messages in every case through [threshold signatures](/threshold-signature/), at the cost of more phases.

## When to use it

Zyzzyva is mainly of historical and teaching value. Its idea, a fast path that the client checks and a slower path with a commit certificate, appears in later protocols. Do not deploy the view change of the original papers. For a system that must be correct today, use [PBFT](/pbft/), [HotStuff](/hotstuff/) or a fast-path protocol with a view change that has a published safety proof.

## Pitfalls

- **Trusting the published view change.** The two runs above complete two different requests at one position.
- **Mixing kinds of evidence without views.** A commit certificate and $f + 1$ matching histories each prove something, but a rule that always prefers one kind loses safety. Every piece of evidence must carry the view in which it was formed.
- **Using speculative results as final.** A replica that answers other services with a result it has not seen complete can spread a request that a new view drops.
- **Counting replies, not replicas.** Each replica counts once per view and history; the client must check signatures.
- **Expecting the fast path under faults.** One silent replica is enough to force five message delays on every request.

## Implementations

## History

Kotla, Alvisi, Dahlin, Clement and Wong presented Zyzzyva at SOSP 2007 and gave the full protocol in ACM Transactions on Computer Systems in 2009. Its speed in the normal case made it a standard point of comparison for BFT systems. Clement and others showed in 2009 that a single faulty client or replica could slow it down a great deal. In December 2017 Abraham, Gueta, Malkhi, Alvisi, Kotla and Martin, two of them authors of Zyzzyva, posted "Revisiting fast practical Byzantine fault tolerance", which gives the two runs above, showing that the view change of Zyzzyva is not safe. The same paper also reports a liveness problem in FaB Paxos.

## References
