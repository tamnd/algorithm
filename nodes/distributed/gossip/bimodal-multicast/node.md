---
tag: A2XR3K
kind: algorithm
slug: bimodal-multicast
name: Bimodal multicast
aliases:
- pbcast
area: distributed/gossip
level: advanced
summary: An unreliable multicast followed by rounds of digest gossip and retransmission. Each message reaches almost all processes or almost none, and middle outcomes are very rare.
model: random-phone-call-model
complexity:
  vars: {n: the number of processes, L: the retransmission limit per request, G: the rounds a message stays in a buffer, ρ: the messages multicast per round}
  messages: {per_round: O(n L)}
  time: {rounds: Θ(log n)}
  space: {extra: O(G ρ)}
properties: {deterministic: false, recursive: false}
history:
  year: 1999
  people: [Kenneth P. Birman, Mark Hayden, Oznur Ozkasap, Zhen Xiao, Mihai Budiu, Yaron Minsky]
  note: Birman et al. combined an unreliable multicast with the anti-entropy of Demers et al., analysed it as a chain-binomial epidemic, and called its guarantee bimodal.
prereqs: [probabilistic-broadcast, anti-entropy, push-gossip, gossip-fanout]
see_also: [rumor-mongering, lpbcast, epidemic-broadcast-tree, epidemic-model, multicast-routing, fifo-broadcast, binomial-distribution, peer-sampling-service]
sources:
  - paper: doi:10.1145/312203.312207
    title: Kenneth P. Birman, Mark Hayden, Oznur Ozkasap, Zhen Xiao, Mihai Budiu and Yaron Minsky, Bimodal multicast, ACM Transactions on Computer Systems 17(2), 41-88, 1999
    locator: Section 3 (the properties of pbcast, the two-phase anti-entropy protocol, Optimizations 1 to 6), Appendix A (the system model with ε and τ, the abstract protocol of Figure 15, the chain-binomial recurrence), Appendix B (pseudo-code)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.3 (anti-entropy, the term used by Birman et al. for their repair phase)
---

Bimodal multicast, or pbcast, is the gossip-based multicast of Birman et al. (1999). A message is first sent by an unreliable multicast, and then the processes repair losses in rounds of [anti-entropy](/anti-entropy/): each process sends a digest of the message ids in its buffer to one random process, which asks for the ones it lacks. The guarantee is probabilistic and bimodal: with high probability a message reaches almost all processes, with low probability it reaches only a few, and an outcome in between is far less likely than either.

## In plain words

A teacher reads an announcement to a large class over a bad loudspeaker. Most students hear it, but some miss it. Then, every few minutes, each student turns to a random classmate and shows a short list of the announcements they have heard. If the classmate sees one they missed, they ask for it and get a copy.

After a few such exchanges, almost every student has every announcement. Students keep the full text of an announcement only for a while and then throw it away, so the work stays small.

If the loudspeaker fails and only the teacher knows the announcement, it spreads from student to student. It then either takes off and reaches nearly everyone, or it dies out with very few. Ending with about half the class is extremely unlikely. This is the meaning of "bimodal".

## The problem

Solve [probabilistic broadcast](/probabilistic-broadcast/) in the bimodal form, for a stream of messages from one or more senders to a group of $n$ processes, with steady throughput even when some processes are slow. Birman et al. list the properties of pbcast (Section 3): a bimodal delivery guarantee, which they call atomicity; stable throughput; FIFO order per sender; detection of stable messages; an upcall that tells the application about a message it has given up on; and costs that are constant or grow slowly with $n$.

The model of the analysis (Appendix A) is synchronous rounds on a complete network. Each process crashes with probability at most $\tau$, and each message between correct processes is lost with probability at most $\varepsilon$, all independently. The figures of the paper use $\varepsilon = 0.05$ and $\tau = 0.001$. The real protocol runs rounds without synchronized clocks; their experiments start a round every 100 ms.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes, $N = \lvert P \rvert$ in the paper |
| $\beta$ | the probability that a process gossips to a given other process; the fanout is $\beta n$ |
| $\varepsilon$, $\tau$ | the bounds on the message loss and the process crash probability |
| $R$ | the number of gossip rounds in the analysis |
| $G$ | the number of rounds a message stays in a buffer before it is garbage collected |
| $L$ | the retransmission limit per request |
| $f$ | the number of processes that crash |
| $m$, $D$, $\Delta$ | not used: the gossip partners are uniform, as on the complete graph |

## The algorithm

```pseudo id=main
PBCAST at process p
L1  on broadcast(m) at the sender: deliver m, and send m to all processes by unreliable multicast
L2  on receipt of m (by multicast or DATA) that p has not seen: deliver m, and put m in the buffer with the round number
ANTI-ENTROPY ROUND at process p, in every round
L3      q ← a process chosen uniformly at random, other than p
L4      send DIGEST(the ids of the messages in the buffer) to q
ON DIGEST(ids) from p, at process q
L5      missing ← the ids that q has not seen; if missing is not empty then send SOLICIT(missing) to p
ON SOLICIT(ids) from q, at process p
L6      send DATA(m) to q for at most L of the requested messages in the buffer, the most recent first
END OF ROUND at process p
L7      remove from the buffer every message that has been there for G rounds
```

The repair is a pull by the process that lacks a message, started by a push of the digest from a process that has it. A process that holds a message tells one random process about it per round, so the spread of a message that the multicast missed is [push gossip](/push-gossip/) for $G$ rounds. Line L6 is two of the optimizations of the paper: the retransmission limit per round (Optimization 2) and most recent first (Optimization 4). Line L7 makes the protocol give up on old messages, so that a process that falls behind catches up on recent messages first, and the buffers stay bounded. The other optimizations are: answering a solicitation only in the round it belongs to (soft failure detection), cycling through different messages in repeated requests, letting each process number its own rounds, and choosing gossip partners from a subset of the group for scale.

**The abstract protocol of the analysis.** Appendix A analyses a simpler protocol (Figure 15) for one message whose multicast failed, so that only the sender has it. A process that receives the message gossips it only in the next round, to each other process independently with probability $\beta$, and solicitations and retransmissions are folded into the gossip message. Birman et al. argue that this is equivalent to the real protocol for the analysis, since losses are independent per message.

## Example

**The delivery distribution.** In the abstract protocol with no crashes, let $s_t$ be the number of processes that gossip in round $t$ and $r_t$ the number that have not received the message, with $s_0 = 1$, $r_0 = n - 1$. Set $p = \beta(1 - \varepsilon)$ and $q = 1 - p$. Given $s_t$ and $r_t$, each of the $r_t$ processes receives the message in round $t + 1$ with probability $1 - q^{s_t}$, independently, so $s_{t+1}$ is binomial with parameters $r_t$ and $1 - q^{s_t}$. This is the chain-binomial epidemic of Appendix A. The implementation computes the exact distribution of the number of processes that have the message after $R$ rounds. For $n = 50$, $\varepsilon = 0.05$ and $R = 12$:

| Fanout $\beta n$ | at most 5 have it | 6 to 44 | at least 45 | mean |
|---|---|---|---|---|
| 2 | 0.236 | 0.692 | 0.0725 | 28.71 |
| 3 | 0.0706 | 0.154 | 0.776 | 43.36 |
| 5 | 0.00786 | $3.2 \times 10^{-5}$ | 0.992 | 49.23 |

With fanout 5, the probabilities of exactly 1, 2, 3 and 5 processes are $7.5 \times 10^{-3}$, $3.2 \times 10^{-4}$, $2.3 \times 10^{-5}$ and $2.5 \times 10^{-7}$; of exactly 10 and 25 they are $4.4 \times 10^{-11}$ and $8.9 \times 10^{-14}$; of 45, 48, 49 and 50 they are $1.9 \times 10^{-4}$, 0.052, 0.24 and 0.69. The smallest value is about $4.2 \times 10^{-14}$, at 19 processes. This is the bimodal shape. With fanout 2 there is no deep valley: most of the mass is in the middle. The probability that nobody hears the sender is exactly $q^{n-1} = (1 - 0.095)^{49} \approx 0.0075$.

**Latency.** In the mean-field recurrence in which every process that has the message gossips in every round with fanout 1, the number that have it grows by a factor of about $1 + (1 - \varepsilon) = 1.95$ per round. For $n = 1000$, $\varepsilon = 0.05$ and $\tau = 0.001$, the round in which a correct process most likely first receives the message is round 11, against $\log_{1.95} 1000 \approx 10.34$.

**The full protocol.** The seeded simulator runs lines L1 to L7 with 50 processes and 20 messages, one multicast per round, $G = 10$ and $L = 8$, and makes the multicast of message 3 reach nobody. Every packet, including multicast copies, digests, solicitations and retransmissions, is lost with probability loss.

| loss | 0 | 0.05 | 0.2 |
|---|---|---|---|
| fewest processes that got a message | 50 | 50 | 50 |
| retransmissions | 58 | 128 | 292 |

All messages reach all 50 processes. With no loss, the retransmissions repair only message 3, which 49 processes lack; the count is 58 and not 49 because two holders can answer the same process in one round.

**Giving up.** With 100 processes, 30 messages, loss 0.2, $G = 3$, $L = 1$ and a failed multicast of message 0, message 0 reaches only the sender in this run. Only the sender holds it, for 3 rounds; each repair needs a digest, a solicitation and a retransmission to survive, and with $L = 1$ the one retransmission goes to the most recent message that the partner lacks. No copy got through before the sender dropped it. The other 29 messages reach between 91 and 100 processes. This is the "almost none" and "almost all" of the guarantee. With $G = 10$ and $L = 8$, the same run delivers every message to at least 99 processes.

## Correctness

**Integrity.** A process delivers a message only at line L2, only once, since it records the id, and only a message that the sender multicast, since DATA carries only buffered messages. This holds in every run.

**Repair with no garbage collection.** If $G = \infty$, the sender does not crash and every packet is lost with probability less than 1, then every correct process delivers every message with probability 1. Each round, a holder sends its digest to a given process with probability $1/(n - 1)$, and the digest, the solicitation and the retransmission all arrive with positive probability; so a process that lacks the message gets it in finite time with probability 1.

**The recurrence.** Given the state $(s_t, r_t)$ of the abstract protocol, the events "process $i$ receives the message in round $t + 1$" are independent with probability $1 - q^{s_t}$, so the number of new receivers is binomial. The proof file proves this and the formula $q^{n-1}$ for the case that nobody hears the sender. The distribution is then computed exactly by summing over the states.

**The bimodal shape.** Birman et al. show how to compute the distribution and bound the probability of a failed run, given a predicate for failure chosen by the application; they note that a closed form is open. The shape is computed for given parameters, as in the table above; it is not proved in general here.

## Complexity

- **Messages.** Each process sends one digest per round, so $n$ digests per round in total, plus at most one solicitation per digest and at most $L$ retransmissions per solicitation: $O(nL)$ messages per round, whatever the number of messages in the stream. The unreliable multicast costs $n - 1$ copies per message, or one IP multicast.
- **Rounds.** A message that the multicast missed spreads like push gossip from the processes that hold it, so it reaches all processes in $\log_2 n + \ln n + O(1)$ rounds without losses, with high probability, if $G$ is at least that long; see [the push rumor spreading time](/push-rumor-spreading-time/). If the multicast reached most processes, the last ones get it in $O(\log n)$ rounds by the same end phase.
- **Space.** Each process buffers each message for $G$ rounds, so the buffer holds about $G \rho$ messages for $\rho$ messages per round. A digest lists the ids in the buffer.

## Properties

- **Stable throughput.** Since repair is spread over random partners with a limit per round, one slow process does not slow down the others; Birman et al. show this in experiments where virtually synchronous multicast loses throughput.
- **Recent messages first.** The protocol aims at a common suffix of the message histories, not a common prefix.
- **Rare losses are reported.** A process that gives up on a message gets an upcall, so the application knows about the gap.
- **Not reliable broadcast.** A message can reach only a few processes, with a probability that the fanout and $G$ make small but not zero.
- **Needs membership.** Each process must know the group, or a random subset of it, to pick partners.

## Variants and improvements

- **Fanout per round.** A process can gossip to more than one process per round; the paper notes that in its experiments the load was smallest with one partner per round. The product of the number of rounds and the partners per round is the fanout of the analysis.
- **Partial views.** Optimization 6 lets each process gossip with a subset of the group. [lpbcast](/lpbcast/) and [peer sampling](/peer-sampling-service/) take this further.
- **Ordered delivery.** pbcast delivers in FIFO order per sender; total order can be layered on top.
- **Tree plus gossip.** [Epidemic broadcast trees](/epidemic-broadcast-tree/) send the payload along a tree and use gossip only for repair and for ids, which lowers the cost of the first phase when no IP multicast is available.
- **Rumor mongering in place of the multicast.** Demers et al. use [rumor mongering](/rumor-mongering/) for the first spread, with anti-entropy as a backup.

## When to use it

Use bimodal multicast for high-rate streams to large groups when a rare, reported loss is acceptable and steady throughput matters more than all-or-nothing delivery, for example when slow processes must not slow down the group. Use a reliable or virtually synchronous multicast when every message must reach every correct process in every run, and use [Bracha's reliable broadcast](/bracha-reliable-broadcast/) under Byzantine faults.

## Pitfalls

- **Oldest first.** Wrong: retransmit the oldest missing message first. Right: retransmit the most recent first; otherwise a process that was briefly slow can stay behind for good.
- **A buffer that is too short.** Wrong: pick $G$ smaller than the time push gossip needs to reach everybody. Right: $G$ must exceed about $\log_2 n + \ln n$ rounds, or a message that the multicast missed is dropped before it spreads, as in the "giving up" example.
- **Reading the guarantee as "all".** Wrong: assume that pbcast delivers every message to every correct process. Right: the "almost none" outcome has a small positive probability, and the application must handle the upcall.
- **Fanout below the threshold.** Wrong: use fanout 2 and expect a bimodal outcome. Right: with fanout 2 in the example most of the probability is in the middle; the fanout must be large enough for the epidemic to take off, see [the epidemic threshold](/epidemic-threshold/).

## Implementations

The Python code has a seeded lock-step simulator of the full protocol and an exact computation for the abstract protocol. In the simulator, process 0 multicasts one message per round, each copy is lost with the given probability, and then every process sends a DIGEST to a random process; SOLICIT and DATA messages are processed in the same round, which models the rule that a solicitation is answered only within its round. Every packet can be lost. A process buffers a message for $G$ rounds. The function returns, for each message, the number of processes that delivered it, and the number of retransmissions. The module also computes the chain-binomial distribution, samples the abstract protocol to check it, and evaluates the mean-field latency recurrence. The code does not order deliveries; it delivers on receipt.

## History

Birman, Hayden, Ozkasap, Xiao, Budiu and Minsky published bimodal multicast in ACM TOCS in 1999. They took the term anti-entropy and the idea of gossip repair from Demers et al. (1987), analysed the protocol as a chain-binomial epidemic, and compared it in experiments with virtually synchronous multicast and with SRM. They called the protocol pbcast, for probabilistic broadcast, because "bimodal multicast" had no short form.

## References
