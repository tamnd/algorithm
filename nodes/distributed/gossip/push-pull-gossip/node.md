---
tag: JCK6B9
kind: algorithm
slug: push-pull-gossip
name: Push-pull gossip
aliases:
- push-pull rumor spreading
area: distributed/gossip
level: core
summary: Along every call an informed caller pushes the rumor and an informed callee sends it back. On n nodes this takes log3 n + O(log log n) rounds and O(n log log n) messages.
model: random-phone-call-model
complexity:
  vars: {n: the number of nodes}
  messages: {total: O(n log log n)}
  time: {rounds: log3 n + O(log log n)}
  space: {extra: O(log log n)}
properties: {deterministic: false, recursive: false}
history:
  year: 2000
  people: [Richard Karp, Christian Schindelhauer, Scott Shenker, Berthold Vöcking]
  note: Demers et al. (1987) used push-pull anti-entropy; Karp et al. (2000) proved log3 n + O(log log n) rounds and O(n log log n) transmissions and gave the median counter rule.
prereqs: [push-gossip, pull-gossip, random-phone-call-model, chernoff-bound]
see_also: [push-gossip, pull-gossip, rumor-spreading-message-lower-bound, conductance-rumor-spreading-bound, graph-conductance, anti-entropy, rumor-spreading-problem, gossip-protocol]
sources:
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 2 (the push&pull scheme with an age bound, Theorem 2.1 and its four phases), Section 3 (the median counter algorithm, states A, B-m, C, D, Theorem 3.1)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.3 (push-pull anti-entropy)
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: Theorem 1 (push-pull informs all nodes of a graph of conductance Φ in O(log n / Φ) rounds w.h.p.)
---

Push-pull gossip spreads a rumor along random calls in both directions: in every round each node calls a random node, an informed caller pushes the rumor to its callee, and an informed callee sends it back to its caller. Push makes the start fast and pull makes the end fast, so on the complete graph with $n$ nodes every node is informed after $\log_3 n + O(\log \log n)$ rounds with high probability, and if every node stops at that age, the total number of transmissions is $O(n \log \log n)$ (Karp, Schindelhauer, Shenker and Vöcking 2000). The [message lower bound](/rumor-spreading-message-lower-bound/) shows that no address-oblivious algorithm does better than $\Theta(n \log \log n)$. On any graph of [conductance](/graph-conductance/) $\Phi$, push-pull needs $O(\log n / \Phi)$ rounds.

## In plain words

Everybody phones a random person once an hour. On every call, if the caller knows the news, they tell it, and if the person called knows the news, they tell it too. Early on, a person who knows tells the person they call and also anybody who calls them, so the number who know about triples each hour. Near the end, a person who does not know is unlucky only if they call somebody who does not know either and nobody who knows calls them; that gets rare very fast.

The hard part is stopping. If people keep telling for too long, there are many useless calls; if they stop too soon, some people never hear. The method below lets each person count how many of their contacts already know, and stop at the right moment without a clock.

## The problem

Solve the [rumor spreading problem](/rumor-spreading-problem/) with few rounds and few transmissions. The model is the [random phone call model](/random-phone-call-model/) on the complete graph: synchronous rounds; in each round every node calls a node chosen uniformly at random; calls are free and only transmissions of the rumor are counted; a rumor received in round $t$ is sent from round $t + 1$ on. No node knows the round in which the rumor was created unless the rumor carries its age. The analysis has no failures; Theorem 3.1 of Karp et al. adds $F$ nodes disabled by an oblivious adversary.

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $S_t$, $U_t$ | the informed and the uninformed nodes after round $t$ |
| $s_t$, $u_t$ | $\lvert S_t \rvert$ and $\lvert U_t \rvert$ |
| $T_{\max}$ | the age at which nodes stop, $\log_3 n + O(\log \log n)$ |
| $\mathit{ctr}_{\max}$ | the largest counter of the median counter rule, $O(\log \log n)$ |
| $F$ | the number of faulty nodes |
| $m$, $D$, $\Delta$, $\Phi$ | the number of edges, the diameter, the maximum degree and the conductance of a graph |

## The algorithm

```pseudo id=main
PUSH-PULL at node p, in round t
L1  q ← a node chosen uniformly at random, other than p
L2  if p is active then send RUMOR to q                            ▷ push
L3  if q is active then q sends RUMOR to p                         ▷ pull
L4  at the end of the round, a node that received RUMOR is informed
▷ age rule: a node is active while it is informed and age(rumor) ≤ T_max
▷ median counter rule: a node is active in states B-m and C; at the end of each round:
L5  in state A: if a partner was in C then go to C; else if a partner was in B then go to B-1
L6  in state B-m: if a partner was in C then go to C; else if more partners were in B-m′ with m′ ≥ m than in A or in B-m″ with m″ < m then go to B-(m+1), and to C when m + 1 = ctr_max
L7  in state C: after c_max rounds in C go to D, where the node stops for good
```

**The age rule** (Karp et al., Section 2). The rumor carries its age, and every informed node pushes and pulls in every round until the age exceeds $T_{\max} = \log_3 n + O(\log \log n)$. This needs every node to know $n$.

**The median counter rule** (Karp et al., Section 3). The rumor carries a counter in place of an age. A node is in one of four states: A (does not know the rumor), B-$m$ (knows it, counter $m$), C (knows it and is about to stop) and D (has stopped). The partners of a node in a round are the node it calls and the nodes that call it. The rule of line L6, as stated by Karp et al.: "If during a round a player $v$ in state B-$m$ receives $r$ from more players in state B-$m'$ with $m' \ge m$ than from players in state A and B-$m''$ with $m'' < m$, then it switches to state B-$(m + 1)$." For the count, a partner in state A has counter 0. Both $\mathit{ctr}_{\max}$ and $c_{\max}$ are $O(\log \log n)$, and a safety stop ends every node after $O(\log n)$ rounds. The counter rises only when most contacts already know the rumor, so it measures how far the spreading has gone, without a global clock.

## Example

**A run on 1024 nodes.** With seed 7, the implementation runs push-pull until all nodes are informed. The informed counts after each round are 1, 3, 10, 34, 94, 256, 585, 928, 1020, 1024. In round 1, the source pushes to its callee and is called by one other node, which pulls: 3 nodes. Rounds 2 to 5 multiply by about 3. From round 6 on, the uninformed counts are 439, 96, 4, 0. Pull alone would give about $439^2/1024 \approx 188$ and then $96^2/1024 \approx 9$; the pushes make the fall faster than squaring. The run takes 9 rounds and 5857 transmissions, against 17 rounds for push with the same seed. Over 10 seeds the mean is 7.5, 9.2 and 10.6 rounds for $n = 256$, 1024 and 4096, which is $\log_3 n$ (5.05, 6.31, 7.57) plus about $\log_2 \ln n$ (2.47, 2.79, 3.06).

**The cost of stopping.** Over the same 10 seeds, the median counter rule with $\mathit{ctr}_{\max} = 3$ and $c_{\max} = 2$ informs every node and sends 9.73, 9.70 and 9.72 transmissions per node at $n = 256$, 1024 and 4096: flat. Push run until every node is informed sends 6.94, 8.04 and 9.18 per node, which grows like $\ln n$. The constant of the median counter is large at these sizes, but it does not grow.

**A star.** On a star with $n = 200$ nodes, push-pull from a leaf takes at most 2 rounds: the leaf pushes to the center in round 1, and every leaf calls the center and pulls in round 2. Push takes 1159.5 rounds on average.

## Correctness

The bounds are those of Karp et al. (2000). The proof below gives the phases in outline, which is a sketch, and the late phase in full.

**Theorem (Karp et al., Theorem 2.1).** "The simple push&pull-scheme informs all players in time $\log_3 n + O(\ln \ln n)$ using $O(n \ln \ln n)$ messages w.h.p."

*Outline of the early phases (sketch).*

1. **Startup**, from 1 to $(\ln n)^4$ informed nodes: an informed node pushes to a new node with probability close to 1 in every round, so the informed set at least doubles within a constant number $c$ of rounds w.h.p., and this phase takes $O(\log \log n)$ rounds.
2. **Exponential growth**, from $(\ln n)^4$ to $n/\ln n$ informed nodes: in a round, each informed node informs its callee and, in expectation, about one caller, so $\mathbb{E}[s_t] = s_{t-1}(3 - O(1/\ln n))$. Chernoff bounds keep $s_t$ within a factor $1 \pm O(1/\ln n)$ of its mean while $s_t \ge (\ln n)^4$, and the phase takes $\log_3 n \pm O(\log \log n)$ rounds.
3. **From $n/\ln n$ to $n/2$ informed nodes**: while $s_t \le n/2$, the pulls alone inform each uninformed node with probability $s_t/(n - 1)$, so the expected number of new nodes is at least $s_t/2$, and a Chernoff bound gives growth by a factor $5/4$ per round w.h.p.; going from $n/\ln n$ to $n/2$ takes $O(\log \log n)$ rounds.

*The late phase, in full.* Suppose $u_t \le n/2$. A node $v \in U_t$ stays uninformed in round $t + 1$ only if its own call goes to a node of $U_t$; if the call goes to $S_t$, line L3 informs $v$. So $u_{t+1} \le Y$, where $Y$ is the number of $v \in U_t$ whose call goes to $U_t \setminus \{v\}$. The calls are independent, so $Y \sim \mathrm{Bin}(u_t, (u_t - 1)/(n - 1))$: this is exactly the law of one round of [pull](/pull-gossip/). Push can only make $u_{t+1}$ smaller. Hence the squaring lemma of pull applies to push-pull, with $\mathbb{E}[u_{t+1}/n] \le (u_t/n)^2$, and the proof on [the pull page](/pull-gossip/) gives, with probability $1 - O(\log^2 n / n)$:

- while $u_t^2/n \ge 36 \ln n$, $\varepsilon_{t+1} \le \frac{3}{2} \varepsilon_t^2$ with $\varepsilon_t = u_t/n$, by the Chernoff bound with $\delta = 1/2$, so with $\eta_t = \frac{3}{2}\varepsilon_t \le 3/4$ we have $\eta_{t+1} \le \eta_t^2$, and after $\log_2 \ln n + O(1)$ rounds $u_t < 6\sqrt{n \ln n}$;
- one more round gives $u \le 72 \ln n$ by the Chernoff bound with $\delta = 1$, with probability $1 - n^{-12}$;
- one more round gives $\mathbb{E}[u] \le (72 \ln n)^2/n$, and $u = 0$ by Markov's inequality, with probability $1 - O(\log^2 n / n)$.

So the late phase takes $\log_2 \ln n + O(1)$ rounds, and with the earlier phases all nodes are informed after $\log_3 n + O(\log \log n)$ rounds w.h.p.

*Transmissions (sketch).* In round $t + 1$ each informed node pushes once and answers every call it receives, about one in expectation, so the round costs about $2 s_t$. During phases 1 and 2, $s_t$ grows by a factor close to 3, so their sum is $O(n/\ln n)$. Every other round costs at most about $2n$, and with $T_{\max} = \log_3 n + O(\log \log n)$ there are $O(\log \log n)$ such rounds, which gives $O(n \log \log n)$.

**The median counter (Karp et al., Theorem 3.1).** "Assuming an arbitrary distribution D and up to F node failures as described above, the median-counter algorithms informs all but O(F) players in O(ln n) rounds using O(n ln ln n) transmissions, w.h.p." The proof is cited, not given here. The idea: while fewer than half of the nodes know the rumor, most partners of a node in B-$m$ are in state A, so counters stay low. Once most nodes know, counters rise by about one per round, so they reach $\mathit{ctr}_{\max} = O(\log \log n)$ about when the late phase ends, and state C spreads the decision to stop in $O(\log \log n)$ more rounds. A node that stops too early is caught by pulls from other nodes, so only $O(n \log \log n)$ transmissions are spent.

The proof file has the safety and monotonicity claims and the full late phase.

## Complexity

- **Rounds.** $\log_3 n + O(\log \log n)$ w.h.p. with the age rule on the complete graph; $O(\log n)$ w.h.p. with the median counter rule, for any partner distribution. On a graph of conductance $\Phi$, $O(\log n / \Phi)$ w.h.p. (Giakkoupis 2011); see [the conductance bound](/conductance-rumor-spreading-bound/).
- **Transmissions.** $O(n \log \log n)$ w.h.p. with either rule. If every node keeps pushing and pulling until an outside observer sees that all are informed, the cost is still $O(n \log \log n)$, because only $O(\log \log n)$ rounds have more than $n/\ln n$ informed nodes. With an age bound of $(1 + \varepsilon)\log_3 n$, the cost is $\Theta(n \log n)$, and with $(1 - \varepsilon)\log_3 n$ a constant fraction stays uninformed (Karp et al., Section 3).
- **Space.** The age or the counter of the rumor, $O(\log \log n)$ bits.

## Properties

- **Optimal in two ways.** The time $\log_3 n + O(\log \log n)$ matches the lower bound $\log_3 n - O(1)$ for every algorithm in the model, which comes from the fact that the informed set can at most triple in expectation per round. The cost $O(n \log \log n)$ matches the [lower bound](/rumor-spreading-message-lower-bound/) for address-oblivious algorithms.
- **Robust to the graph.** On a star, push or pull alone is slow, and push-pull is fast. On every graph of conductance $\Phi$, push-pull needs $O(\log n / \Phi)$ rounds.
- **Sensitive to the stopping time.** The age rule needs $n$ and a shared notion of the rumor's age. The median counter needs neither.
- **Address-oblivious.** Every node decides to send before it knows its partner.

## Variants and improvements

- **Median counter.** Stop without knowing $n$ and under any partner distribution, at a cost of $O(\log n)$ rounds; above.
- **On graphs.** Push-pull on a graph of conductance $\Phi$ takes $O(\log n / \Phi)$ rounds, and $O(\log^2 n / \alpha)$ on a graph of vertex expansion $\alpha$ (Giakkoupis 2014); see [the conductance bound](/conductance-rumor-spreading-bound/).
- **Anti-entropy.** Push-pull of whole states, for all updates at once, is push-pull [anti-entropy](/anti-entropy/).
- **Rumor mongering.** Stop after $k$ useless contacts in place of an age bound; see [rumor mongering](/rumor-mongering/).
- **Averaging.** Exchange values in both directions and replace both by the mean; see [gossip averaging](/gossip-averaging/).

## When to use it

Use push-pull when nodes call each other periodically anyway and a rumor should reach everybody fast and cheaply. It is the right default for spreading updates: it is never much slower than push or pull alone and is much faster on graphs with unequal degrees. Use the age rule when $n$ is known and partners are uniform, and a counter rule when they are not.

## Pitfalls

- **Stopping on a fixed age that is too short.** Wrong: stop at $\log_3 n$ because the informed set triples. Right: the late phase needs $O(\log \log n)$ more rounds; stopping at $(1 - \varepsilon)\log_3 n$ leaves a constant fraction uninformed.
- **Stopping too late.** Wrong: keep spreading for $c \log n$ rounds with a large $c$ to be safe. Right: each extra round costs about $2n$ transmissions, so the total becomes $\Theta(n \log n)$, no better than push.
- **Pulling fresh information.** Wrong: let a node informed by a push in round $t$ answer a pull in the same round. Right: the state at the start of the round decides, as in the analysis.
- **Comparing with partners in D.** Wrong: count stopped nodes as partners in the median rule. Right: a node in D does not take part; counting it as a node in A keeps counters low and the rumor alive.

## Implementations

The Python code is a seeded lock-step simulator. One function runs push, pull or push-pull until all nodes are informed, on the complete graph or on a given graph, and returns the rounds, the transmissions and the informed counts. Another runs push-pull with an age bound. A third runs the median counter rule with states A, B-$m$, C and D, with $\mathit{ctr}_{\max}$ and $c_{\max}$ of order $\log \log n$, and returns the rounds, the transmissions and the number of informed nodes. The file also builds small graphs (stars, cycles, barbells and two stars joined by a path) and computes their conductance by brute force and the eigenvalues of their normalized Laplacian by the Jacobi method, which the tests use to check the conductance bound and Cheeger's inequality.

## History

Demers et al. (1987) introduced push-pull anti-entropy for the Clearinghouse servers at Xerox and saw that it is faster than push and pull alone. Karp, Schindelhauer, Shenker and Vöcking (2000) analysed push-pull in the random phone call model, proved the $\log_3 n + O(\log \log n)$ bound and the $O(n \log \log n)$ cost, gave the median counter rule, and proved that address-oblivious algorithms need $\Omega(n \log \log n)$ transmissions. Chierichetti, Lattanzi and Panconesi (2010) bounded push-pull on graphs by the conductance, and Giakkoupis (2011) gave the tight bound $O(\log n / \Phi)$.

## References
