---
tag: 7Q1FNH
kind: algorithm
slug: push-gossip
name: Push gossip
aliases:
- push rumor spreading
area: distributed/gossip
level: intro
summary: In every round each informed node sends the rumor to one random node. All n nodes know it after log2 n + ln n + O(1) rounds, at a cost of about n ln n messages.
model: random-phone-call-model
complexity:
  vars: {n: the number of nodes}
  messages: {total: Θ(n log n)}
  time: {rounds: log2 n + ln n + O(1)}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false}
history:
  year: 1985
  people: [Alan M. Frieze, Geoffrey R. Grimmett, Boris Pittel, Alan Demers]
  note: Frieze and Grimmett (1985) and Pittel (1987) found the exact round count on the complete graph; Demers et al. (1987) used push for replicated databases.
prereqs: [random-phone-call-model, rumor-spreading-problem, coupon-collector-problem, geometric-distribution]
see_also: [pull-gossip, push-pull-gossip, push-rumor-spreading-time, gossip-fanout, rumor-mongering, epidemic-model, conductance-rumor-spreading-bound, flooding]
sources:
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the main theorem, push in log2 n + ln n + O(1) rounds in probability on the complete graph
  - paper: doi:10.1016/0166-218X(85)90059-9
    title: Alan M. Frieze and Geoffrey R. Grimmett, The shortest-path problem for graphs with random arc-lengths, Discrete Applied Mathematics 10(1), 57-77, 1985
    locator: the result on the spreading time of push on the complete graph, log2 n + ln n + o(log n) rounds
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1 (push needs Θ(n log n) transmissions; the model and the counting of transmissions)
  - paper: doi:10.1002/rsa.3240010406
    title: Uriel Feige, David Peleg, Prabhakar Raghavan and Eli Upfal, Randomized broadcast in networks, Random Structures and Algorithms 1(4), 447-460, 1990
    locator: push on general graphs, O(n log n) rounds on every connected graph
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.3 (push anti-entropy, p_{i+1} = p_i (1 - 1/n)^{n(1 - p_i)} ≈ p_i e^{-1} at the end)
  - paper: doi:10.1109/TPDS.2003.1189583
    title: Anne-Marie Kermarrec, Laurent Massoulié and Ayalvadi J. Ganesh, Probabilistic reliable dissemination in large-scale systems, IEEE Transactions on Parallel and Distributed Systems 14(3), 248-258, 2003
    locator: the infect-and-die variant with fanout k
---

Push gossip is the simplest [gossip protocol](/gossip-protocol/) for spreading one rumor: in every round, every node that knows the rumor sends it to one node chosen uniformly at random. While few nodes know it, almost every push reaches a new node, so the informed set about doubles per round; at the end, an uninformed node must wait to be chosen by somebody, which takes about $\ln n$ more rounds. On the complete graph with $n$ nodes, all nodes know the rumor after $\log_2 n + \ln n + O(1)$ rounds (Frieze and Grimmett 1985, Pittel 1987), and the total number of messages is $\Theta(n \log n)$.

## In plain words

Someone knows a piece of news. Every hour, each person who knows it phones one person picked at random and tells them. In the first hours, nearly every call reaches somebody new, so the number of people who know doubles each hour. Near the end, most calls reach people who already know, and the last few people have to wait until somebody happens to call them. That waiting adds a few hours.

The method needs no list of who already knows, no plan, and no coordinator. If a call fails, other calls carry the news. The price is many useless calls at the end.

## The problem

Solve the [rumor spreading problem](/rumor-spreading-problem/): one node $s$ knows a rumor at time 0, and every node must learn it.

The model is the [random phone call model](/random-phone-call-model/): synchronous rounds, and in each round each node calls one partner chosen uniformly at random among all other nodes, or among its neighbors when the nodes form a graph $G$. A message sent in round $t$ arrives in round $t$, and the receiver forwards it from round $t + 1$ on. The basic analysis has no failures; crashes and lost messages are discussed under Properties.

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $S_t$ | the set of informed nodes after round $t$, with $S_0 = \{s\}$ |
| $U_t$ | the set of uninformed nodes after round $t$ |
| $T$ | the first round with $S_T$ equal to all nodes |
| $f$ | the number of nodes that crash |
| $m$, $D$, $\Delta$ | the number of edges, the diameter and the maximum degree of $G$ |

## The algorithm

```pseudo id=main
PUSH at node p, in round t
L1  if p is informed and age(rumor) ≤ T_max then
L2      q ← a node chosen uniformly at random, other than p (on a graph: a random neighbor of p)
L3      send RUMOR to q
ON RUMOR received at node q in round t
L4  if q is not informed then q becomes informed; it pushes from round t + 1 on
```

The rumor carries its age, the number of rounds since the source created it. With $T_{\max} = \infty$, every informed node pushes forever, which is the form that is analysed. A real system stops: an age bound $T_{\max} = \log_2 n + c \ln n$ with a constant $c > 1$ informs every node with high probability, by the proof on [the push rumor spreading time page](/push-rumor-spreading-time/). Other stopping rules are in [rumor mongering](/rumor-mongering/).

## Example

**A run on 1024 nodes.** The implementation, with seed 7 on the complete graph, gives the following numbers of informed nodes after each round:

| Round | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Informed | 1 | 2 | 4 | 8 | 16 | 31 | 60 | 115 | 215 | 370 |

| Round | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|
| Informed | 577 | 754 | 889 | 973 | 1006 | 1015 | 1021 | 1024 |

The first four rounds double exactly, because no two pushes hit the same node. In round 5, one of the 16 pushes hits an informed node or the same node as another push. From round 10 on, most pushes are wasted: the uninformed counts 447, 270, 135, 51, 18, 9, 3, 0 fall by a factor of about $e$ per round once almost all nodes are informed. The run takes 17 rounds and 7057 messages; $\log_2 1024 + \ln 1024 \approx 16.9$ and $1024 \ln 1024 \approx 7098$.

**Why the end is slow.** Let $u$ be an uninformed node in a round in which $s$ nodes are informed. Each informed node misses $u$ with probability $1 - 1/(n - 1)$, independently, so
$$\Pr[u \text{ stays uninformed}] = \left(1 - \frac{1}{n - 1}\right)^{s} \approx e^{-s/n}.$$
When $s$ is close to $n$ this is about $e^{-1}$, so the expected number of uninformed nodes falls only by a factor $e$ per round, and about $\ln n$ rounds are needed to go from a constant fraction to zero. This is the recurrence $p_{i+1} \approx p_i e^{-1}$ of Demers et al. (1987).

## Correctness

**Safety.** Only the rumor is sent, and a node becomes informed only on receiving it (line L4), so no node is informed of something the source did not send. The informed set only grows.

**Eventual delivery.** With $T_{\max} = \infty$ on a connected graph, every node is informed with probability 1. Take an uninformed node $u$ with an informed neighbor $v$. In every round, $v$ calls $u$ with probability $1/\deg(v) > 0$, independently of earlier rounds, so $u$ is informed after a finite number of rounds with probability 1. By induction along a shortest path from $s$, all nodes are informed.

**Time on the complete graph.** $T = \log_2 n + \ln n + O(1)$ in probability (Pittel 1987). [The push rumor spreading time page](/push-rumor-spreading-time/) proves $T = O(\log n)$ with high probability in full, in two phases: a doubling phase while $|S_t| \le n/2$, analysed with a [Chernoff bound](/chernoff-bound/), and a coupon collector phase for the rest, analysed with the [union bound](/union-bound/). The proof file adds the claims above and the exact count of messages.

## Complexity

- **Rounds.** $\log_2 n + \ln n + O(1)$ on the complete graph, in probability. On a connected graph, $O(n \log n)$ rounds with high probability (Feige et al. 1990), and the star needs $\Theta(n \log n)$.
- **Messages.** Each informed node sends one message per round, so the total is $\sum_{t=0}^{T-1} |S_t|$. In the doubling phase the sum is $O(n)$; in the last $\ln n$ rounds almost all nodes push, which gives $n \ln n + O(n)$ in total on the complete graph. Karp et al. (2000) note that push needs $\Theta(n \log n)$ transmissions with any stopping rule that informs all nodes w.h.p.
- **Space.** One bit (informed) and the age of the rumor per node.
- **Load.** Each node sends at most one message per round and receives a binomial number with mean at most 1, so the largest load in a round is $O(\log n / \log \log n)$ w.h.p.

## Properties

- **Randomized and oblivious.** The decision to push does not depend on the partner, so push is address-oblivious in the sense of Karp et al.
- **Robust.** If each message is lost independently with probability $\varepsilon$, the process is push with a success rate $1 - \varepsilon$ per call: the doubling becomes growth by a factor $2 - \varepsilon$, and the end phase slows by a factor $1/(1 - \varepsilon)$. If $f$ nodes crash, the rumor still reaches every live node w.h.p., as long as the source is live long enough to make its first pushes.
- **Even load.** No node sends more than one message per round.
- **Slow on irregular graphs.** On a star, a push from the center reaches one random leaf per round, so push needs about $n \ln n$ rounds. [Push-pull](/push-pull-gossip/) needs 2.
- **Same as the SI epidemic.** On the complete graph, push is a discrete SI epidemic in which each infective infects one random node per round; see [the epidemic model](/epidemic-model/).

## Variants and improvements

- **Fanout $k$.** Each informed node pushes to $k$ random nodes per round. The informed set grows by a factor up to $k + 1$, and the rounds drop to about $\log_{k+1} n + \ln n / k$.
- **Infect and die.** Each node pushes to $k$ random nodes once, when it first learns the rumor, and then stops. Kermarrec, Massoulié and Ganesh (2003) showed that with $k = \ln n + c$ the probability that all nodes are reached tends to $e^{-e^{-c}}$; see [gossip fanout](/gossip-fanout/).
- **Stopping by feedback.** Stop pushing after a number of calls to nodes that already know; this is [rumor mongering](/rumor-mongering/).
- **Pull and push-pull.** [Pull](/pull-gossip/) finishes the last nodes fast: the uninformed fraction squares per round. [Push-pull](/push-pull-gossip/) uses both and needs $\log_3 n + O(\log \log n)$ rounds and $O(n \log \log n)$ messages.
- **Quasirandom push.** Each node calls its neighbors in the order of a fixed list, from a random starting point. On the complete graph the time stays $O(\log n)$, with less randomness.

## When to use it

Use push when a node has new information and wants to spread it at once without knowing who needs it, when messages are small, and when a cost of about $\ln n$ messages per node is acceptable. Use it as the "hot rumor" path next to [anti-entropy](/anti-entropy/), which repairs what push misses. Prefer push-pull when nodes already call each other periodically, since pulls finish the last nodes much faster. Avoid push on graphs with very unequal degrees.

## Pitfalls

- **Forwarding in the same round.** Wrong: let a node that has just received the rumor forward it in the same round. Right: the model forwards from the next round on; otherwise the round count is not $\log_2 n + \ln n$.
- **Stopping at $\log_2 n$.** Wrong: stop after $\log_2 n$ rounds because the informed set doubles. Right: about $\ln n$ more rounds are needed to reach the last nodes; after $\log_2 n$ rounds a constant fraction is still uninformed.
- **A fixed age bound.** Wrong: keep $T_{\max}$ fixed while the system grows. Right: $T_{\max}$ must grow like $\log_2 n + c \ln n$; with a fixed bound, the fraction of nodes that never learn the rumor grows with $n$.
- **Counting only useful messages.** Wrong: report the cost as $n - 1$ messages. Right: every push is sent whether or not the target knows the rumor, so the cost is about $n \ln n$.
- **Assuming a uniform view.** Wrong: pick partners from a small fixed list and expect $O(\log n)$ rounds. Right: the time then depends on the [conductance](/graph-conductance/) of the graph that the lists form; use a [peer sampling service](/peer-sampling-service/).

## Implementations

The Python code is a seeded lock-step simulator. Each node has the state informed or not and one message type, RUMOR. In each round, informed nodes pick a partner, all messages are delivered, and then the new informed set is computed, so a rumor received in round $t$ is forwarded from round $t + 1$ on. Partners are uniform over all other nodes or over the neighbors in a given graph. The function returns the number of rounds, the number of messages and the informed count after each round. A second function runs the infect-and-die variant with fanout $k$.

## History

Frieze and Grimmett (1985) studied push as a first passage problem and showed that the time on the complete graph is $\log_2 n + \ln n + o(\log n)$. Pittel (1987) sharpened this to $\log_2 n + \ln n + O(1)$ in probability. Demers et al. (1987) used push, pull and push-pull for the Clearinghouse name service at Xerox and noted that push is slow at the end. Feige, Peleg, Raghavan and Upfal (1990) studied push on general graphs. Karp, Schindelhauer, Shenker and Vöcking (2000) showed that push needs $\Theta(n \log n)$ transmissions and that push-pull does better.

## References
