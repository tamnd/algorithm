---
tag: JVFH6A
kind: model
slug: random-phone-call-model
name: Random phone call model
aliases:
- random phone-call model
- synchronous gossip model
area: distributed/gossip
level: core
summary: n processes run in synchronous rounds. In each round every process calls one partner chosen uniformly at random, and information can flow both ways along the call (push and pull).
prereqs: [synchronous-model, randomized-algorithm, round-complexity, message-complexity]
see_also: [gossip-protocol, rumor-spreading-problem, push-gossip, pull-gossip, push-pull-gossip, rumor-spreading-message-lower-bound, conductance-rumor-spreading-bound, synchronous-model]
sources:
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1.2 (the model, transmissions, distributed and address-oblivious algorithms), Section 2 (Theorem 2.1), Section 3 (Theorem 3.1), Section 4 (Theorem 4.1), Section 5 (Theorem 5.1)
  - paper: doi:10.1016/0166-218X(85)90059-9
    title: Alan M. Frieze and Geoffrey R. Grimmett, The shortest-path problem for graphs with random arc-lengths, Discrete Applied Mathematics 10(1), 57-77, 1985
    locator: the result on the spreading time of push on the complete graph, log2 n + ln n + o(log n) rounds
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the main theorem, push in log2 n + ln n + O(1) rounds in probability
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: the model on a graph (a uniform random neighbor per round), Theorem 1 (O(log n / Φ) rounds for push-pull)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1 (push, pull and push-pull exchanges with random partners in cycles)
---

The random phone call model is the standard model for the analysis of [gossip protocols](/gossip-protocol/). There are $n$ processes and time runs in synchronous rounds; in each round, every process calls one partner chosen uniformly at random, and along each call the two processes can exchange information in both directions. Sending from caller to callee is a *push*, and sending from callee to caller is a *pull*. Karp, Schindelhauer, Shenker and Vöcking (2000) defined it in this form, after the cycles of Demers et al. (1987), and it is the model of the bounds for [push](/push-gossip/), [pull](/pull-gossip/) and [push-pull](/push-pull-gossip/) gossip.

## The machine

**Processes and rounds.** There are $n$ processes with distinct addresses $1, \dots, n$. Each process knows $n$ and may hold random bits. Computation is in synchronous rounds $t = 1, 2, \dots$, as in the [synchronous model](/synchronous-model/).

**Calls.** At the start of round $t$, every process $u$ independently chooses a partner $v \ne u$ uniformly at random from the other $n - 1$ processes, and "$u$ calls $v$". The calls of round $t$ form a random graph $G_t$ with an edge $\{u, v\}$ for each call. A process makes exactly one call per round but can receive any number of calls: the number of calls that a fixed process receives in a round is binomial with parameters $n - 1$ and $1/(n - 1)$, so it is about Poisson with mean 1. The graphs $G_1, G_2, \dots$ are independent.

**Push and pull.** Along an edge $\{u, v\}$ of $G_t$ where $u$ called $v$, the rumor is *pushed* if $u$ sends it to $v$ and *pulled* if $v$ sends it to $u$. Information received in round $t$ cannot be forwarded in the same round: the exchanges of a round happen in parallel.

**Decisions.** An algorithm is *distributed* if the decision of a process to send the rumor along a call in round $t$ depends only on its state in round $t$. The state in round $t$ is a function of the initial state (the address, $n$ and random bits), the addresses of the neighbors in $G_1, \dots, G_t$, and the information received in rounds 1 to $t - 1$. For the lower bounds, the state may also depend on a global round number and on the round in which the rumor was created.

**Address-oblivious.** An algorithm is *address-oblivious* if the state of a process in round $t$ does not depend on the addresses of its neighbors in $G_t$, only on their number. It can depend on the addresses of neighbors in earlier rounds. In plain terms, a process decides whether to send the rumor along a call before it knows who is at the other end. Every algorithm of Demers et al. (1987) is address-oblivious.

**On a graph.** The model extends to a connected graph $G = (V, E)$ with $|V| = n$: in each round, each process calls a neighbor chosen uniformly at random. The complete graph gives the model above. This is the setting of the conductance bounds of Chierichetti, Lattanzi and Panconesi (2010) and Giakkoupis (2011).

**Faults.** The basic model has no faults. Karp et al. also study an oblivious adversary that names, before the run, up to $F$ processes that fail to exchange information in some rounds, and random call failures. Crash failures and lost messages are the usual faults in the systems the model describes.

### Notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $F$ | the number of processes the adversary may disable (Karp et al. use $F$) |
| $G_t$ | the random graph of the calls of round $t$ |
| $S_t$, $U_t$ | the informed and the uninformed processes after round $t$ |
| $m$, $D$, $\Delta$ | the number of edges, the diameter and the maximum degree, on a graph |
| $\Phi$ | the [conductance](/graph-conductance/) of the graph |

## What it counts

- **Rounds.** The number of rounds until every process knows the rumor, as a random variable. Bounds are stated with high probability, that is, with probability at least $1 - O(n^{-\alpha})$ for a constant $\alpha > 0$, or in expectation, or in probability.
- **Transmissions.** The number of times the rumor is sent along a call, by push or by pull. One exchange between two neighboring processes counts as one transmission, whatever its size. Calls that carry no rumor are not counted: in a system with many rumors the calls are made anyway, so only the extra traffic per rumor matters. The total is the *message complexity* of the rumor.
- **Robustness.** How many processes stay uninformed when $F$ processes fail, or when the partner distribution is not uniform.

The size of a transmission is not limited, so the lower bounds hold even if processes send their whole history. The upper bounds of Karp et al. add only small counters to each rumor.

## Relation to other models

- **Synchronous message passing.** It is a [synchronous model](/synchronous-model/) on the complete graph in which each process may open one connection per round, to a random address, and send along it. Without the randomness and the one-call rule, flooding informs everybody in one round with $n - 1$ messages.
- **The telephone model.** In the classic telephone model of broadcasting, the calls of a round form a matching chosen by the algorithm, and each call joins two processes. An informed process informs at most one process per round, so the informed set at most doubles, and $\lceil \log_2 n \rceil$ rounds are both needed and enough on the complete graph. The random phone call model gives up the choice of partner, which costs only constant factors in time, and gains robustness.
- **Asynchronous gossip.** In the asynchronous time model, each process has a Poisson clock of rate 1 and calls a random partner when its clock ticks. One unit of time has about $n$ calls, the same as one round. This model is the usual one for [gossip averaging](/gossip-averaging/).
- **[LOCAL](/local-model/) and [CONGEST](/congest-model/).** In those models, a process sends to all its neighbors in every round. In the random phone call model on a graph it sends to one random neighbor, so the time depends on the [conductance](/graph-conductance/) of the graph, not only on its diameter.
- **[Epidemic models](/epidemic-model/).** Push on the complete graph is a discrete-time SI epidemic: an infected process infects one random process per round.

## Known results in the model

On the complete graph with $n$ processes and no faults:

| Algorithm or bound | Rounds | Transmissions | Source |
|---|---|---|---|
| [Push](/push-gossip/) | $\log_2 n + \ln n + O(1)$ in probability | $\Theta(n \log n)$ | Frieze and Grimmett 1985, [Pittel 1987](/push-rumor-spreading-time/) |
| [Pull](/pull-gossip/) | $O(\log n)$ w.h.p.; from half informed to all informed, $O(\log \log n)$ | about $\lvert S_{t-1} \rvert$ in round $t$; the total depends on the stopping rule | Karp et al. 2000, Section 2 |
| [Push-pull](/push-pull-gossip/), stop at age $\log_3 n + O(\log \log n)$ | $\log_3 n + O(\log \log n)$ w.h.p. | $O(n \log \log n)$ | Karp et al. 2000, Theorem 2.1 |
| Median counter, any partner distribution, $F$ faults | $O(\log n)$ w.h.p., all but $O(F)$ informed | $O(n \log \log n)$ | Karp et al. 2000, Theorem 3.1 |
| Any address-oblivious algorithm, all but a fraction $f$ informed | any | $\Omega(n \log \log (1/f))$ expected | [Karp et al. 2000, Theorem 4.1](/rumor-spreading-message-lower-bound/) |
| Any distributed algorithm, all but $o(n)$ informed in $O(\log n)$ rounds | $O(\log n)$ | $\omega(n)$ expected | Karp et al. 2000, Theorem 5.1 |
| A non-oblivious algorithm: the source sends to each process the first time it calls the source or is called | $\Theta(n \log n)$ | $n - 1$ | Karp et al. 2000, Section 1.3 |

The last two lines show a trade-off: $n - 1$ transmissions are enough if time does not matter, but no algorithm is both fast and linear.

On a connected graph with conductance $\Phi$, push-pull informs all processes in $O(\log n / \Phi)$ rounds with high probability, and this is tight for some graphs (Giakkoupis 2011; see [the conductance bound](/conductance-rumor-spreading-bound/)). Push or pull alone can be slow when degrees differ: on a star, push from a leaf needs $\Omega(n \log n)$ rounds, because the center calls one random leaf per round, while push-pull needs at most 2 rounds.

## References
