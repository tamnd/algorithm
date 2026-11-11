---
tag: S1CRF0
kind: problem
slug: rumor-spreading-problem
name: Rumor spreading problem
aliases:
- rumour spreading
- broadcast by gossip
area: distributed/gossip
level: core
summary: One node of a graph knows a rumor. In each round every node calls a random neighbor. Make all n nodes learn it in few rounds with few transmissions.
prereqs: [random-phone-call-model, broadcast-problem, round-complexity, message-complexity]
see_also: [push-gossip, pull-gossip, push-pull-gossip, push-rumor-spreading-time, rumor-spreading-message-lower-bound, conductance-rumor-spreading-bound, graph-conductance, flooding]
sources:
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1 (the problem, time and transmissions), Theorem 2.1 (push-pull), Theorem 3.1 (median counter), Theorem 4.1 (lower bound for address-oblivious algorithms), Theorem 5.1 (lower bound in O(log n) rounds)
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the main theorem, push on the complete graph in log2 n + ln n + O(1) rounds in probability
  - paper: doi:10.1002/rsa.3240010406
    title: Uriel Feige, David Peleg, Prabhakar Raghavan and Eli Upfal, Randomized broadcast in networks, Random Structures and Algorithms 1(4), 447-460, 1990
    locator: push on general graphs, O(n log n) rounds on every connected graph, O(log n) on the hypercube and on dense random graphs
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: Theorem 1 (push-pull in O(log n / Φ) rounds w.h.p.) and the matching lower bound
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1 (push, pull and push-pull; residue, traffic and delay as the measures of a rumor mongering scheme)
---

The rumor spreading problem asks how a piece of information, the rumor, known at first by one node of a network, can reach every node when each node may call only one random neighbor per round. It is the [broadcast problem](/broadcast-problem/) in the [random phone call model](/random-phone-call-model/). An algorithm is judged by the number of rounds until all nodes know the rumor, by the number of times the rumor is transmitted, and by how many nodes it misses when nodes fail. On the complete graph the answers are $\Theta(\log n)$ rounds and $\Theta(n \log \log n)$ transmissions (Karp et al. 2000); on other graphs the number of rounds depends on the [conductance](/graph-conductance/).

## In plain words

One person in a town hears some news. Every hour, each person phones one other person picked at random from their contacts, and the two can tell each other what they know. How many hours pass until the whole town knows, and how many times must the news be repeated on the phone?

The calls are free, but repeating the news costs something. Telling it on every call is fast and wasteful. Stopping too early leaves some people who never hear it. The problem is to find the rule that decides when to tell, and to know the best possible trade-off between speed and repetition.

## Definition

**Input.** A connected graph $G = (V, E)$ with $n = |V|$ nodes, and a source node $s$ that knows the rumor at time 0. On the complete graph every node knows $n$ and every node can call every other node.

**Model.** The [random phone call model](/random-phone-call-model/): time runs in synchronous rounds; in round $t$ every node $u$ calls a neighbor $v$ chosen uniformly at random and independently of everything else. Along the call, the rumor may go from $u$ to $v$ (push) or from $v$ to $u$ (pull). A node informed in round $t$ can send the rumor from round $t + 1$ on. There are no faults in the basic problem.

**Output.** At the end, every node knows the rumor. A relaxed version asks that all but a fraction $f$ of the nodes know it.

**Measures.**

| Measure | Definition |
|---|---|
| time $T$ | the first round after which every node knows the rumor; a random variable, bounded with high probability, in probability or in expectation |
| transmissions | the number of calls along which the rumor is sent, by push or by pull; calls without the rumor are free |
| residue | the fraction of nodes that never learn the rumor, for algorithms that stop by themselves |
| robustness | the number of uninformed nodes when $F$ nodes fail, or when calls are lost |

*With high probability* (w.h.p.) means with probability at least $1 - n^{-c}$ for a constant $c > 0$.

**Notation.**

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $m$ | the number of edges of $G$ |
| $D$ | the diameter of $G$ |
| $\Delta$ | the maximum degree of $G$ |
| $\Phi$ | the [conductance](/graph-conductance/) of $G$ |
| $S_t$, $U_t$ | the informed and the uninformed nodes after round $t$ |
| $F$ | the number of faulty nodes |

## Variants

- **Direction.** [Push](/push-gossip/): only informed callers send. [Pull](/pull-gossip/): only informed callees answer. [Push-pull](/push-pull-gossip/): both.
- **Fanout.** Each node calls $k$ neighbors per round, or each informed node calls $k$ nodes once and then stops; see [gossip fanout](/gossip-fanout/).
- **Stopping rule.** The rumor is sent for a fixed number of rounds, until it is older than an age bound, or until a node meets enough nodes that know it; see [rumor mongering](/rumor-mongering/) and the median counter of [push-pull gossip](/push-pull-gossip/).
- **Asynchronous time.** Each node has a Poisson clock of rate 1 and calls a random neighbor at each tick.
- **Quasirandom.** Each node goes through a fixed list of its neighbors from a random starting point, in place of a fresh random choice per round.
- **Many rumors.** Several sources start rumors at different times, and calls carry all of them; this is the setting of [anti-entropy](/anti-entropy/) and [bimodal multicast](/bimodal-multicast/).
- **Faults.** Nodes crash, calls fail at random, or an oblivious adversary disables $F$ nodes.

## Examples

**The complete graph with 1024 nodes.** With the seeded simulators of the push, pull and push-pull pages (seed 7), the rumor reaches all 1024 nodes in 17 rounds and 7057 transmissions under push, in 12 rounds and 3383 transmissions under pull, and in 9 rounds and 5857 transmissions under push-pull run until the end. The push-pull counts of informed nodes after each round are 1, 3, 10, 34, 94, 256, 585, 928, 1020, 1024.

**The star.** One center and $n - 1$ leaves. Under push from a leaf, the leaf tells the center in round 1, and then the center tells one random leaf per round, so the last leaf waits for a coupon collector over $n - 1$ leaves: about $n \ln n$ rounds. Under push-pull, every leaf calls the center in every round, so all leaves pull the rumor in round 2. In the simulation with $n = 200$, push takes 1159.5 rounds on average and push-pull 2.

**The cycle.** Each node has two neighbors, and the rumor moves at most one step in each direction per round. Push-pull needs at least $n/2$ rounds, because the diameter is $\lfloor n/2 \rfloor$. In the simulation with $n = 64$ it takes 42.55 rounds on average.

## Known algorithms

| Algorithm | Graph | Rounds | Transmissions |
|---|---|---|---|
| [Push](/push-gossip/) | complete | $\log_2 n + \ln n + O(1)$ in probability (Frieze and Grimmett 1985, Pittel 1987) | $\Theta(n \log n)$ |
| [Pull](/pull-gossip/) | complete | $O(\log n)$ w.h.p.; the uninformed fraction squares in each round once it is below $1/2$ | at most $n$ per round |
| [Push-pull](/push-pull-gossip/) with an age bound | complete | $\log_3 n + O(\log \log n)$ w.h.p. | $O(n \log \log n)$ |
| Push-pull with the median counter | complete, any partner distribution | $O(\log n)$ w.h.p., all but $O(F)$ informed | $O(n \log \log n)$ |
| Push | any connected graph | $O(n \log n)$ w.h.p. (Feige et al. 1990) | $O(n^2 \log n)$ |
| Push | hypercube, dense random graphs | $O(\log n)$ w.h.p. (Feige et al. 1990) | $O(n \log n)$ |
| Push-pull | any connected graph with conductance $\Phi$ | $O(\log n / \Phi)$ w.h.p. (Giakkoupis 2011) | $O(n \log n / \Phi)$ if run for the whole time |
| [Rumor mongering](/rumor-mongering/) | complete | $O(\log n)$ cycles; about 17 at $n = 1000$ (Demers et al. 1987) | $mn$ for a traffic of $m$ per node, with a residue of about $e^{-m}$ |

## Bounds

**Time on the complete graph.** In a round, an informed node can inform at most one node by its own call, plus the nodes that call it. The number of calls a node receives is binomial with mean about 1, so $\mathbb{E}[|S_{t+1}|] \le 3 |S_t|$, hence $\mathbb{E}[|S_t|] \le 3^t$. By [Markov's inequality](/markov-inequality/), $\Pr[|S_t| = n] \le 3^t / n$, so any algorithm needs at least $\log_3 n - O(1)$ rounds to finish with constant probability. Push-pull meets this bound up to the $O(\log \log n)$ term. Push alone informs at most one node per informed node per round, so it needs at least $\log_2 n$ rounds, and Pittel's theorem shows that it needs $\ln n$ more for the coupon collector at the end.

**Transmissions.** Every node except the source must receive the rumor at least once, so $n - 1$ transmissions are needed. An algorithm that is allowed $\Theta(n \log n)$ rounds can meet this: the source sends the rumor to each node the first time the two are joined by a call. The cost of speed is in the lower bounds of Karp et al. (2000), proved on [the message lower bound page](/rumor-spreading-message-lower-bound/):

- every address-oblivious algorithm that informs all but a fraction $f$ of the nodes with constant probability needs $\Omega(n \log \log (1/f))$ transmissions in expectation, whatever its number of rounds (Theorem 4.1);
- every distributed algorithm that informs all but $o(n)$ nodes in $O(\log n)$ rounds with constant probability needs $\omega(n)$ transmissions in expectation (Theorem 5.1);
- push alone needs $\Theta(n \log n)$ transmissions to inform all nodes.

**Time on general graphs.** The diameter $D$ is a lower bound for every algorithm, since the rumor moves one hop per round. Conductance gives a lower bound too: $\Omega(\log n / \Phi)$ rounds are needed on some graphs of conductance $\Phi$, and $O(\log n / \Phi)$ rounds are enough for push-pull on all of them (Giakkoupis 2011). Push or pull alone can be much slower than push-pull when degrees differ; the star is the example.

## Reductions

- **To broadcast.** Rumor spreading is a randomized solution of the [broadcast problem](/broadcast-problem/). [Flooding](/flooding/) solves broadcast in $D$ rounds with $2m$ messages by sending to all neighbors; rumor spreading sends along one edge per node per round, which is what a node with many neighbors and limited bandwidth can do.
- **To epidemics.** Push on the complete graph is the discrete SI epidemic; rumor mongering is an SIR epidemic. The [epidemic model](/epidemic-model/) gives the fluid limits.
- **To first passage percolation.** In continuous time, the time at which a node learns the rumor is its distance from the source when every edge gets an independent exponential length. Frieze and Grimmett used this view.
- **To averaging.** Spreading the maximum of the values is rumor spreading of the largest value, and [gossip averaging](/gossip-averaging/) uses the same call pattern.

## Applications

- Update propagation in replicated databases, by [rumor mongering](/rumor-mongering/) and [anti-entropy](/anti-entropy/).
- Reliable broadcast to many receivers: [probabilistic broadcast](/probabilistic-broadcast/), [bimodal multicast](/bimodal-multicast/) and [epidemic broadcast trees](/epidemic-broadcast-tree/).
- Spreading membership and failure information in clusters, as in [SWIM](/swim/).
- Models of how news and opinions spread in social networks.

## References
