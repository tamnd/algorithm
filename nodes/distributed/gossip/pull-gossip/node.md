---
tag: 1XHB8V
kind: algorithm
slug: pull-gossip
name: Pull gossip
aliases:
- pull rumor spreading
area: distributed/gossip
level: intro
summary: In every round each node calls a random node, and an informed callee sends the rumor back. Once half the nodes know it, the uninformed fraction squares in each round.
model: random-phone-call-model
complexity:
  vars: {n: the number of nodes}
  messages: {total: O(n log n)}
  time: {rounds: O(log n)}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false}
history:
  year: 1987
  people: [Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart, Doug Terry]
  note: Demers et al. (1987) showed that pull anti-entropy squares the fraction of sites without an update per cycle; Karp et al. (2000) used this in the late phase of push-pull.
prereqs: [random-phone-call-model, rumor-spreading-problem, binomial-distribution, chernoff-bound]
see_also: [push-gossip, push-pull-gossip, anti-entropy, rumor-spreading-message-lower-bound, conductance-rumor-spreading-bound, rumor-mongering, push-rumor-spreading-time, gossip-protocol]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.3 (pull anti-entropy, p_{i+1} = p_i^2, against p_{i+1} ≈ p_i e^{-1} for push), Section 1.4 (pull rumor mongering, Table 3)
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1 (push and pull, calls are made anyway and only rumor transmissions count), proof of Theorem 2.1, phase 3 (quadratic shrinking, E[u_t/n] ≤ (u_{t-1}/n)^2)
  - paper: doi:10.4230/LIPIcs.STACS.2011.57
    title: George Giakkoupis, Tight bounds for rumor spreading in graphs of a given conductance, Proceedings of the 28th Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 9, 57-68, 2011
    locator: the remarks that push alone and pull alone can be slow on graphs of high conductance, for example the star
---

Pull gossip spreads a rumor by asking for it: in every round, every node calls a node chosen uniformly at random, and if the callee knows the rumor, it sends it back. Its strength is the end of the process: a node stays uninformed in a round only if it calls another uninformed node, so once a fraction $\varepsilon \le 1/2$ of the nodes is uninformed, one round leaves about $\varepsilon^2$, and $O(\log \log n)$ rounds finish the job (Demers et al. 1987). Its weakness is the start: the source must wait until some node happens to call it. Pull is the second half of [push-pull gossip](/push-pull-gossip/), and the pull form of [anti-entropy](/anti-entropy/).

## In plain words

Everybody phones a random person once an hour and asks "any news?". If that person knows the news, they tell it. At first, only one person knows, and they must wait for somebody to call them; that can take a while.

Near the end, things go very fast. A person who still does not know has to be unlucky enough to call another person who does not know. If half the town does not know, a caller is unlucky half the time; next hour a quarter of the town does not know, then a sixteenth, then a two hundred fifty-sixth. The number of people left out shrinks much faster than in the push method, where the last people must wait to be called.

## The problem

Solve the [rumor spreading problem](/rumor-spreading-problem/) on $n$ nodes in the [random phone call model](/random-phone-call-model/): synchronous rounds; in each round every node calls one partner uniformly at random among the other nodes, or among its neighbors on a graph. Calls are made in every round anyway, for example because many rumors are in flight, so a call that carries no rumor is free; only the transmissions of the rumor are counted. There are no failures in the analysis.

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $S_t$, $U_t$ | the informed and the uninformed nodes after round $t$ |
| $u_t$ | $\lvert U_t \rvert$ |
| $\varepsilon_t$ | $u_t / n$, the uninformed fraction |
| $T$ | the first round with $u_T = 0$ |
| $m$, $D$, $\Delta$ | the number of edges, the diameter and the maximum degree of a graph |

## The algorithm

```pseudo id=main
PULL at node p, in round t
L1  q ← a node chosen uniformly at random, other than p (on a graph: a random neighbor of p)
L2  send CALL to q
ON CALL from p received at node q in round t
L3  if q was informed at the start of round t and age(rumor) ≤ T_max then send RUMOR to p
ON RUMOR received at node p in round t
L4  if p is not informed then p becomes informed; it answers calls from round t + 1 on
```

The callee does not know whether the caller has the rumor, so it sends it on every call it receives (line L3); this is what makes pull address-oblivious. The age bound $T_{\max}$ stops the answers; with $T_{\max} = \infty$ the process is the one analysed below.

## Example

**The squaring step.** Take $n = 1000$ with 500 uninformed nodes. An uninformed node stays uninformed only if it calls one of the other 499 uninformed nodes, which has probability $499/999$. The expected number left is $500 \cdot 499 / 999 \approx 249.75$, a fraction $0.25 = 0.5^2$. Over many seeds the implementation gives a mean of 250.98. The next rounds give about $62$, then $4$, then $0$ in expectation: from half to none in four rounds.

**A full run on 1024 nodes.** With seed 7, the informed counts after each round are 1, 2, 6, 15, 25, 58, 118, 212, 391, 637, 891, 1006, 1024. The run takes 12 rounds and 3383 transmissions. The uninformed counts after round 9 are 387, 133, 18, 0; the ratios $u_{t+1}/n$ against $(u_t/n)^2$ are 0.130 against 0.143, then 0.018 against 0.017. Compare push with the same seed: the last 51 uninformed nodes took 4 rounds with push, falling by a factor of about $e$ per round.

**The slow start.** In round 1, the source is called by nobody with probability $(1 - 1/(n - 1))^{n - 1} \approx 1/e \approx 0.37$. The implementation agrees within $0.07$. Each round in which the source waits adds one round to the run.

## Correctness

**Safety and monotonicity.** Only an informed node sends RUMOR (line L3), and a node becomes informed only on receiving it (line L4). No node becomes uninformed.

**The squaring lemma.** On the complete graph, given $U_t$ with $u_t \ge 1$,
$$u_{t+1} \sim \mathrm{Bin}\!\left(u_t,\ \frac{u_t - 1}{n - 1}\right), \qquad \mathbb{E}[\varepsilon_{t+1} \mid U_t] = \varepsilon_t \cdot \frac{u_t - 1}{n - 1} \le \varepsilon_t^2.$$

*Proof.* Fix $v \in U_t$. In round $t + 1$, $v$ receives the rumor if its own call goes to an informed node: by line L3 the callee answers. Calls made to $v$ by others do not help, because $v$ is uninformed and the rumor moves only from callee to caller. So $v \in U_{t+1}$ exactly when $v$ calls one of the other $u_t - 1$ uninformed nodes, which has probability $(u_t - 1)/(n - 1)$. The calls of different nodes are independent, so these events are independent, which gives the binomial law. Divide the mean by $n$; since $(u_t - 1)/(n - 1) \le u_t / n$, the bound follows. $\square$

**Finishing from one half.** If $u_t \le n/2$, then with high probability $u_{t+r} = 0$ for $r = \log_2 \ln n + O(1)$.

*Proof.* Let $\mu = \mathbb{E}[u_{t+1} \mid U_t] \le u_t^2 / n$. While $u_t^2 / n \ge 36 \ln n$, the [Chernoff bound](/chernoff-bound/) $\Pr[X \ge \frac{3}{2} \cdot \frac{u_t^2}{n}] \le e^{-u_t^2/(12 n)} \le n^{-3}$, valid for a binomial $X$ whose mean is at most $u_t^2/n$, gives $\varepsilon_{t+1} \le \frac{3}{2} \varepsilon_t^2$. Put $\eta_t = \frac{3}{2} \varepsilon_t$; then $\eta_{t+1} \le \eta_t^2$ and $\eta_t \le 3/4$ at the start, so after $r$ rounds $\eta \le (3/4)^{2^r}$, which drops below $n^{-1/2}$ for $r = \log_2 \ln n + O(1)$. So within that many rounds $u^2/n < 36 \ln n$, that is $u < 6\sqrt{n \ln n}$. In the next round the mean is below $36 \ln n$, and Chernoff gives $u \le 72 \ln n$ with probability $1 - n^{-3}$. In the round after, $\mathbb{E}[u] \le (72 \ln n)^2 / n$, so by [Markov's inequality](/markov-inequality/) $u = 0$ with probability $1 - O(\log^2 n / n)$. A [union bound](/union-bound/) over the $O(\log \log n)$ rounds completes the proof. $\square$

**The start.** While $|S_t| = s \le n/2$, each uninformed node calls an informed one with probability $s/(n - 1)$, so $\mathbb{E}[|S_{t+1}|] = s + (n - s) s/(n - 1) \ge \frac{3}{2} s$, and $|S_t|$ grows geometrically once it is large enough for Chernoff bounds. From $|S_t| = 1$, the first success needs a geometric number of rounds with success probability about $1 - 1/e$, which is $O(1)$ in expectation and $O(\log n)$ with high probability. So pull informs all nodes in $O(\log n)$ rounds with high probability. The expected time is close to $\log_2 n + \log_2 \ln n$: about $\log_2 n$ rounds of doubling and $\log_2 \ln n$ rounds of squaring. This form follows from the two phases above; it is derived here, not quoted from a paper. The proof file has the details.

## Complexity

- **Rounds.** $O(\log n)$ with high probability on the complete graph. In the simulation the mean is within $[L - 1, L + 2.5]$ for $L = \log_2 n + \log_2 \ln n$ at $n = 256$ and $n = 1024$.
- **Transmissions.** In round $t$, the expected number of rumor transmissions is about $|S_{t-1}|$, one per call received by an informed node. Up to the round in which half the nodes are informed the sum is $O(n)$; the $O(\log \log n)$ rounds that follow cost at most $n$ each. So a run that stops exactly when all nodes are informed costs $O(n \log \log n)$ transmissions in expectation. A node cannot see that moment. With a fixed age bound that succeeds with high probability, the bound must leave room for a slow start of $\Theta(\log n)$ rounds, and the informed nodes keep answering until then, which costs $O(n \log n)$.
- **Space.** One bit and the age of the rumor per node.

## Properties

- **Fast end, slow start.** The opposite of [push](/push-gossip/), which starts fast and ends slow. Push-pull takes the good half of each.
- **Address-oblivious.** A callee answers every call, so it sends the rumor to callers that already have it.
- **Robust to lost messages.** If a call or an answer is lost with probability $\delta$, an uninformed node stays uninformed with probability $\varepsilon + (1 - \varepsilon)\delta$ per round, so the squaring becomes $\varepsilon_{t+1} \approx \varepsilon_t(\varepsilon_t + \delta)$; the end slows to a geometric rate $\delta$ once $\varepsilon_t < \delta$.
- **Slow on a star from a leaf.** If a leaf has the rumor, it is pulled only when the center calls that leaf, which takes about $n$ rounds; then all leaves pull it in one round. [Giakkoupis (2011)](/conductance-rumor-spreading-bound/) lists push and pull alone as slow on such graphs; push-pull is fast on all graphs of high [conductance](/graph-conductance/).
- **Load.** Each node makes one call per round. A callee answers all calls it receives, about one in expectation and $O(\log n / \log \log n)$ at most with high probability.

## Variants and improvements

- **Pull anti-entropy.** Demers et al. (1987) compare whole databases with the callee, which is pull for all updates at once; see [anti-entropy](/anti-entropy/). This is where $p_{i+1} = p_i^2$ first appears.
- **Pull rumor mongering.** Callees answer with their hot rumors and lose interest after useless exchanges. Demers et al. report residues of $5.8 \times 10^{-4}$ at $k = 2$ for 1000 sites, far below push; see [rumor mongering](/rumor-mongering/).
- **Push-pull.** Add push to fix the start: [push-pull gossip](/push-pull-gossip/) needs $\log_3 n + O(\log \log n)$ rounds and $O(n \log \log n)$ transmissions with high probability.
- **Pull with digests.** The caller sends a digest of what it has, and the callee sends only what is missing; see [Scuttlebutt reconciliation](/scuttlebutt-reconciliation/).

## When to use it

Use pull when nodes already call each other periodically, as in anti-entropy, so that calls are free, and when the goal is to make sure that the last nodes get an update. Combine it with push when an update must also start fast. Avoid pull alone when calls are expensive and updates are rare: every node calls in every round whether or not there is anything new.

## Pitfalls

- **Counting only useful answers.** Wrong: count the calls made by uninformed nodes only, and let informed nodes stay silent. Right: in the model every node calls; this changes nothing for spreading, but the answers to informed callers are real transmissions and must be counted.
- **Answering with fresh information.** Wrong: let a callee that learns the rumor in round $t$ answer a call in the same round. Right: the answer uses the state at the start of the round, or the squaring lemma does not hold.
- **Ignoring the start.** Wrong: bound the time by $\log_2 \log_2 n$ because of the squaring. Right: squaring starts only when half of the nodes are informed; before that, pull needs about $\log_2 n$ rounds and can wait at the source.
- **Pull on a star.** Wrong: expect pull to be fast on every graph with a small diameter. Right: from a leaf of a star it takes about $n$ rounds.

## Implementations

The Python code is a seeded lock-step simulator with two message types, CALL, which is free, and RUMOR, which is counted. In each round every node calls a partner, every callee that was informed at the start of the round answers, and the new informed set is computed at the end of the round. Partners are uniform over all other nodes or over the neighbors in a given graph. One function runs pull until all nodes are informed and returns the rounds, the transmissions and the informed counts; another runs a single round from a given number of uninformed nodes, which is what the test of the squaring lemma uses.

## History

Demers et al. (1987) compared push, pull and push-pull anti-entropy for the Clearinghouse servers at Xerox and showed that pull drives the fraction of out-of-date sites from $p_i$ to $p_i^2$ per cycle, while push only divides it by about $e$. Karp, Schindelhauer, Shenker and Vöcking (2000) used the same squaring in the third phase of their analysis of push-pull. Chierichetti, Lattanzi and Panconesi (2010) and Giakkoupis (2011) studied push-pull on graphs and noted that push or pull alone can be slow when degrees differ.

## References
