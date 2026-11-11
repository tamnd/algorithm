---
tag: 6WV622
kind: problem
slug: probabilistic-broadcast
name: Probabilistic broadcast
aliases:
- best-effort gossip broadcast
area: distributed/gossip
level: advanced
summary: Deliver each broadcast message to all correct processes with probability at least 1 - ε, never deliver a message twice or one that was not sent, and keep the cost per process small.
prereqs: [broadcast-problem, gossip-protocol, rumor-spreading-problem, gossip-fanout]
see_also: [bimodal-multicast, lpbcast, epidemic-broadcast-tree, bracha-reliable-broadcast, flooding, push-gossip, rumor-mongering, erdos-renyi-connectivity-threshold]
sources:
  - paper: doi:10.1109/MC.2004.1297243
    title: Patrick Th. Eugster, Rachid Guerraoui, Anne-Marie Kermarrec and Laurent Massoulié, Epidemic information dissemination in distributed systems, IEEE Computer 37(5), 60-67, 2004
    locator: the survey of gossip-based broadcast, its probabilistic guarantees, and the parameters of a gossip broadcast (fanout, number of rounds, membership)
  - paper: doi:10.1109/TPDS.2003.1189583
    title: Anne-Marie Kermarrec, Laurent Massoulié and Ayalvadi J. Ganesh, Probabilistic reliable dissemination in large-scale systems, IEEE Transactions on Parallel and Distributed Systems 14(3), 248-258, 2003
    locator: Section 3.1 (Theorem 1, fanout ln n + c gives success probability tending to exp(-exp(-c))), Section 3.2 (link and node failures)
  - paper: doi:10.1145/312203.312207
    title: Kenneth P. Birman, Mark Hayden, Oznur Ozkasap, Zhen Xiao, Mihai Budiu and Yaron Minsky, Bimodal multicast, ACM Transactions on Computer Systems 17(2), 41-88, 1999
    locator: Section 2 (the bimodal delivery guarantee), Section 3 (the pbcast protocol)
  - paper: doi:10.1145/945506.945507
    title: Patrick Th. Eugster, Rachid Guerraoui, Sidath B. Handurukande, Petr Kouznetsov and Anne-Marie Kermarrec, Lightweight probabilistic broadcast, ACM Transactions on Computer Systems 21(4), 341-374, 2003
    locator: the lpbcast algorithm and its analysis with partial views
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Theorem 3.1 (median counter, O(n log log n) transmissions), Theorem 4.1 (lower bound for address-oblivious algorithms)
---

Probabilistic broadcast is the problem of sending a message from one process to all processes of a large group when delivery to all of them only has to hold with high probability. Safety stays strict: no process delivers a message twice or delivers a message that was not sent. Agreement is relaxed: every correct process delivers the message with probability at least $1 - \varepsilon$, in place of always. Gossip solves it with $O(\log n)$ messages per process and no global structure; Eugster et al. (2004) survey these protocols.

## In plain words

A message must reach every member of a very large group. You can make sure that everybody gets it, but then each member must check with others and send many extra messages, and one slow member holds up the rest. Probabilistic broadcast asks for less: each member gets the message with a chance very close to one, for example 999 in 1000.

What it does not give up is honesty. Nobody gets a message twice, and nobody gets a message that was never sent.

In return, each member only passes the message to a few random members. The cost per member grows very slowly with the size of the group, and lost messages or failed members only lower the chance a little.

## Definition

**Model.** $n$ processes communicate by message passing over a complete network, in the [asynchronous model](/asynchronous-model/) or in synchronous rounds for the analysis. Up to $f$ processes [crash](/crash-failure/), and each message may be lost independently with probability $\delta$. Each process can pick random targets, from the whole group or from a partial view given by a [peer sampling service](/peer-sampling-service/).

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $f$ | the number of processes that crash |
| $\varepsilon$ | the allowed probability that some correct process misses a message |
| $\delta$ | the probability that a message is lost |
| $k$ | the fanout, the number of targets per forwarding step |
| $T$ | the number of rounds or the latency bound |
| $m$, $D$, $\Delta$ | the number of edges, the diameter and the maximum degree of the overlay, when there is one |

**The problem.** A process can call $\text{broadcast}(m)$, and the protocol triggers $\text{deliver}(m)$ events. This page uses the following definition, with an error bound $\varepsilon$:

- **Integrity.** Every process delivers each message at most once, and only if some process broadcast it. This holds in every run.
- **Validity.** If a correct process broadcasts $m$, it delivers $m$.
- **Probabilistic agreement.** If a correct process broadcasts $m$, then with probability at least $1 - \varepsilon$ every correct process delivers $m$.
- **Latency.** In the round version, the deliveries of the last property happen within $T$ rounds.

The probability is over the random choices of the protocol and the random losses, for every fixed choice of which processes crash and when, among the choices allowed by the model. The definition is a relaxation of reliable broadcast, in which agreement must hold in every run; see [Bracha's reliable broadcast](/bracha-reliable-broadcast/) and [the broadcast problem](/broadcast-problem/). It is stronger than best-effort broadcast, which promises delivery only if the sender does not crash.

## Variants

- **Fraction form.** Ask that the expected fraction of correct processes that miss $m$ is at most $\varepsilon$. This is the residue of [rumor mongering](/rumor-mongering/), and it is much cheaper than the "all" form: with push, a residue $s$ costs about $\ln(1/s)$ messages per process, independent of $n$.
- **Bimodal delivery.** Ask that the number of correct processes that deliver $m$ is, with high probability, either almost all or almost none. A sender that needs to know which case happened can then act on it. This is the guarantee of [bimodal multicast](/bimodal-multicast/) (Birman et al. 1999).
- **Uniform form.** Ask for agreement also when the sender or the first receivers crash: if any process delivers $m$, then every correct process delivers it with probability at least $1 - \varepsilon$. A process that forwards before it delivers makes this possible.
- **Ordered forms.** Probabilistic FIFO, causal or total order on top of probabilistic delivery; see [FIFO broadcast](/fifo-broadcast/) and [causal broadcast](/causal-broadcast/) for the reliable versions.
- **Eventual delivery.** With [anti-entropy](/anti-entropy/) or retransmission requests as a backup, every correct process delivers $m$ with probability 1, and the probability bound applies to delivery within $T$ rounds.

## Examples

**Choosing a fanout for a target $\varepsilon$.** In infect and die, each process that receives $m$ for the first time sends it to $k$ random processes and never again. By the theorem of Kermarrec, Massoulié and Ganesh (2003), see [gossip fanout](/gossip-fanout/), a fanout of $\ln n + c$ reaches all processes with probability tending to $e^{-e^{-c}}$. For a target $\varepsilon$, set $e^{-e^{-c}} = 1 - \varepsilon$, that is $c = -\ln(-\ln(1 - \varepsilon))$, which is about $\ln(1/\varepsilon)$ for small $\varepsilon$. The fanout is then about $\ln(n/\varepsilon)$.

| $n$ | $\varepsilon$ | $c$ | fanout $\ln n + c$ | messages, about $n(\ln n + c)$ |
|---|---|---|---|---|
| 1000 | 0.01 | 4.60 | 11.51 | 11 508 |
| 10 000 | 0.001 | 6.91 | 16.12 | 161 176 |
| 1 000 000 | $10^{-6}$ | 13.82 | 27.63 | 27 631 021 |

The values come from the limit theorem, so for small $n$ they are an approximation. Each factor 10 in $1/\varepsilon$ costs only $\ln 10 \approx 2.3$ more messages per process.

**Losses and crashes.** If each message is lost with probability $\delta$, the messages that arrive form the same kind of random graph with mean fanout $k(1 - \delta)$, so the fanout above must be divided by $1 - \delta$; Kermarrec et al. treat this case and crashed processes in their Section 3.2. With $\delta = 0.1$ and the row for $n = 10\,000$, the fanout becomes $16.12/0.9 \approx 17.9$.

**A sender that crashes.** If the sender crashes before it sends anything, no process delivers $m$, and the definition holds because it asks for agreement only when the sender is correct. In the uniform form, the sender must not deliver $m$ before at least one copy is sent; otherwise the run "the sender delivers and crashes at once" breaks agreement with probability 1.

**The fraction form is cheap.** With push rumor mongering on 1000 sites, about 3.3 messages per site leave a residue near 0.037, and 6.7 messages leave about 0.0012 (Demers et al. 1987, Table 1). Reaching all 1000 sites with probability 0.99 by infect and die takes about 11.5 messages per site, as in the first table.

## Known algorithms

- **[Flooding](/flooding/) on an overlay.** Each process forwards $m$ to all its neighbors once. It is deterministic if the overlay stays connected, and costs $2m$ messages for an overlay with $m$ edges.
- **[Push gossip](/push-gossip/) with an age bound.** Each informed process pushes for $\log_2 n + O(\log n)$ rounds; it costs $\Theta(n \log n)$ messages.
- **Infect and die.** Each process forwards once with fanout $\ln n + c$; the analysis is on the [gossip fanout](/gossip-fanout/) page.
- **[Bimodal multicast](/bimodal-multicast/).** An unreliable multicast followed by rounds of digest gossip and retransmission requests (Birman et al. 1999).
- **[lpbcast](/lpbcast/).** Gossip with partial views that are themselves maintained by gossip (Eugster et al. 2003).
- **[Epidemic broadcast trees](/epidemic-broadcast-tree/).** Plumtree sends the message along a tree built from gossip links, and falls back on lazy gossip to repair the tree.
- **Push-pull with a median counter.** Karp et al. (2000) inform all processes w.h.p. in $O(\log n)$ rounds with $O(n \log \log n)$ messages, in the random phone call model.

## Bounds

- **Rounds.** In push gossip each informed process sends one message per round, so the informed set at most doubles per round and at least $\log_2 n$ rounds are needed. With fanout $k$ per round the bound is $\log_{k+1} n$. These are simple counting bounds, proved by induction on the rounds.
- **Messages, push only.** To inform all processes w.h.p. with push only, $\Omega(n \log n)$ messages are needed; this is proved on [the message lower bound page](/rumor-spreading-message-lower-bound/).
- **Messages, address-oblivious.** Karp et al. (2000), Theorem 4.1: in the random phone call model, every address-oblivious algorithm that leaves at most a fraction $f$ of the processes uninformed with constant probability needs $\Omega(n \ln \ln(1/f))$ transmissions in expectation. With $f < 1/n$ this is $\Omega(n \log \log n)$, which push-pull with a median counter meets. The exact statement is on [the message lower bound page](/rumor-spreading-message-lower-bound/); the bound is cited.
- **Infect and die.** With fanout $\ln n + c$, the cost is $n(\ln n + c)$ messages and the probability of reaching all tends to $e^{-e^{-c}}$ (cited). A fanout of $\ln n - \omega(1)$ fails with probability tending to 1, by the same theorem.

## Reductions

- **To random graph reachability.** In infect and die, the set of processes reached is the set reachable from the sender in a random directed graph with out-degree $k$. Probabilistic agreement for the "all" form is the event that this set is everything, a [connectivity threshold](/erdos-renyi-connectivity-threshold/) question.
- **To rumor spreading.** In synchronous rounds with random calls, probabilistic broadcast with $\varepsilon = n^{-c}$ is the [rumor spreading problem](/rumor-spreading-problem/) with a "with high probability" requirement.
- **Probabilistic to reliable, eventually.** A probabilistic broadcast plus a backup that repairs all differences, such as [anti-entropy](/anti-entropy/), gives delivery to every correct process with probability 1, as long as the process that holds the message stays up long enough. Bimodal multicast and Demers et al. use this pattern.
- **Not the other way.** Probabilistic broadcast does not give the guarantees of Byzantine or crash-tolerant reliable broadcast in every run, so protocols that need agreement in every run, such as consensus, cannot use it as a black box.

## Applications

- Spreading updates in replicated databases and name services ([rumor mongering](/rumor-mongering/), Demers et al. 1987).
- Event dissemination and publish-subscribe in large groups (lpbcast, [bimodal multicast](/bimodal-multicast/)).
- Membership and failure information in clusters, for example in [SWIM](/swim/), which piggybacks membership updates on its failure detector messages.

## References
