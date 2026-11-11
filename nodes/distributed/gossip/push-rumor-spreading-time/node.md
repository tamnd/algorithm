---
tag: 574C2P
kind: theorem
slug: push-rumor-spreading-time
name: Push rumor spreading time theorem
aliases:
- Frieze-Grimmett-Pittel bound
area: distributed/gossip
level: advanced
summary: On the complete graph with n nodes, push gossip from one node informs every node in log2 n + ln n + O(1) rounds in probability (Frieze and Grimmett 1985, Pittel 1987).
prereqs: [push-gossip, random-phone-call-model, chernoff-bound, union-bound, coupon-collector-problem]
see_also: [push-gossip, pull-gossip, push-pull-gossip, rumor-spreading-problem, conductance-rumor-spreading-bound, epidemic-model, high-probability-bounds, coupon-collector-problem]
sources:
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the main theorem, T_n = log2 n + ln n + O(1) in probability
  - paper: doi:10.1016/0166-218X(85)90059-9
    title: Alan M. Frieze and Geoffrey R. Grimmett, The shortest-path problem for graphs with random arc-lengths, Discrete Applied Mathematics 10(1), 57-77, 1985
    locator: the result on the spreading time of push on the complete graph, T_n / ln n tends to 1 + 1/ln 2 in probability
  - paper: doi:10.1002/rsa.3240010406
    title: Uriel Feige, David Peleg, Prabhakar Raghavan and Eli Upfal, Randomized broadcast in networks, Random Structures and Algorithms 1(4), 447-460, 1990
    locator: push on general graphs, O(log n) rounds on the hypercube and on dense random graphs, O(n log n) on every connected graph
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4 (Chernoff bounds) and Chapter 2 (the coupon collector problem)
---

The push rumor spreading time theorem says how many rounds [push gossip](/push-gossip/) needs on the complete graph: if one of $n$ nodes knows a rumor and in every round every informed node tells one node chosen uniformly at random, then all nodes are informed after $\log_2 n + \ln n + O(1)$ rounds, in probability. Frieze and Grimmett (1985) found the leading terms and Pittel (1987) the $O(1)$ error. The $\log_2 n$ term counts the rounds in which the informed set doubles, and the $\ln n$ term counts the rounds in which the last nodes wait to be chosen, as in the [coupon collector problem](/coupon-collector-problem/). This page proves the weaker bound $O(\log n)$ with high probability in full and sketches the exact form.

## Statement

**Model.** The [random phone call model](/random-phone-call-model/) on the complete graph with $n$ nodes: synchronous rounds, no failures, and in every round each informed node sends the rumor to a node chosen uniformly at random from the other $n - 1$ nodes, independently of everything else. A node informed in round $t$ sends from round $t + 1$ on. At time 0 one node is informed. Let $S_t$ be the set of informed nodes after round $t$, $s_t = |S_t|$, $u_t = n - s_t$, and let $T_n$ be the first $t$ with $s_t = n$.

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $s_t$, $u_t$ | the numbers of informed and uninformed nodes after round $t$ |
| $T_n$ | the number of rounds until all nodes are informed |
| $m$, $D$, $\Delta$ | the number of edges, the diameter and the maximum degree, for other graphs |

**Theorem (Frieze and Grimmett 1985; Pittel 1987).** As $n \to \infty$,
$$T_n = \log_2 n + \ln n + O_p(1),$$
that is, for every $\varepsilon > 0$ there is a constant $C$ such that $\Pr\left[\,|T_n - \log_2 n - \ln n| > C\,\right] < \varepsilon$ for all $n$. Frieze and Grimmett proved that $T_n / \ln n \to 1 + 1/\ln 2$ in probability; Pittel proved the $O_p(1)$ form.

**Theorem (weak form, proved below).** For every constant $c > 0$ there is a constant $C$ such that for all $n \ge 16$,
$$\Pr[T_n > C \ln n] \le n^{-c}.$$
Also $T_n \ge \log_2 n$ always.

## In plain words

At first almost every message reaches somebody new, because nearly everybody is still uninformed, so the number who know doubles every round. That takes about $\log_2 n$ rounds to reach half of the nodes. Then the problem turns around: most messages go to people who already know, and a particular uninformed person hears the news in a round only if somebody happens to pick them. That chance is about the same in every round, so the number of people still waiting goes down by a constant factor per round. Getting from half of the people to the very last one then takes about $\ln n$ more rounds, as in collecting the last few cards of a set.

## Proof

The proof of the weak form is complete. It has a deterministic lower bound, a growth phase and a coupon collector phase. Throughout, $n \ge 16$ and $L = \lceil 48 (c + 1) \ln n \rceil$.

**Lower bound.** Each informed node sends one message per round, so at most $s_t$ nodes are informed in round $t + 1$, and $s_{t+1} \le 2 s_t$. Hence $s_t \le 2^t$, and $s_t = n$ needs $t \ge \log_2 n$.

**A coupling for one round.** Fix round $t + 1$ and order the $s = s_t$ messages of the round in any fixed way. Call message $j$ *useful* if its target is not in $S_t$ and is not the target of an earlier message of the round. Whatever the first $j - 1$ targets are, at most $s + j - 1 \le 2s$ nodes are informed or already targeted, so given the past, message $j$ is useful with probability at least $1 - 2s/(n - 1)$. Each useful message informs a new node, so $s_{t+1} - s_t$ is the number of useful messages. By the standard sequential coupling, if $p$ is a lower bound on the conditional probability of being useful, the number of useful messages stochastically dominates $\mathrm{Bin}(s, p)$.

**Growth phase, part 1: from 1 to $L$ nodes.** While $s_t \le L$, each message is useful with probability at least $1 - 2L/(n - 1)$, which is at least $2/3$ once $n$ is large enough that $6L \le n - 1$; for smaller $n$, take $C$ large. So in each such round, $s$ grows by at least 1 with probability at least $2/3$, given the past. Let $X$ be the number of such successes in $3L$ rounds; $X$ dominates $\mathrm{Bin}(3L, 2/3)$ with mean $2L$. By the [Chernoff bound](/chernoff-bound/) $\Pr[X \le (1 - \delta)\mu] \le e^{-\delta^2 \mu/2}$ with $\delta = 1/2$, $\Pr[X < L] \le e^{-L/4} \le n^{-12(c+1)}$. So after $3L$ rounds, $s \ge L$ with probability at least $1 - n^{-(c+1)}$.

**Growth phase, part 2: from $L$ to $n/8$ nodes.** While $L \le s_t \le n/8$, each message is useful with probability at least $1 - 2(n/8)/(n - 1) \ge 2/3$ for $n \ge 4$. The number of useful messages dominates $\mathrm{Bin}(s_t, 2/3)$ with mean $\mu = 2 s_t / 3 \ge 2L/3$, and the Chernoff bound with $\delta = 1/2$ gives at least $s_t/3$ useful messages with probability at least $1 - e^{-\mu/8} \ge 1 - e^{-L/12} \ge 1 - n^{-4(c+1)}$. Then $s_{t+1} \ge \frac{4}{3} s_t$. After at most $\log_{4/3} n$ such rounds, $s_t > n/8$. By the [union bound](/union-bound/) over these rounds, this part fails with probability at most $n^{-4(c+1)} \log_{4/3} n \le n^{-(c+1)}$.

**Coupon collector phase: from $n/8$ to $n$ nodes.** Fix a node $v$ that is uninformed when $s_t \ge n/8$ for the first time. In every later round, at least $n/8$ informed nodes each send one message, and each misses $v$ with probability $1 - 1/(n - 1)$, independently. So, given the past, $v$ stays uninformed in a round with probability at most
$$\left(1 - \frac{1}{n - 1}\right)^{n/8} \le e^{-n/(8(n - 1))} \le e^{-1/8}.$$
Since $s$ never decreases, this holds in every round of the phase. After $R = \lceil 8(c + 1)\ln n \rceil$ rounds, $v$ is uninformed with probability at most $e^{-R/8} \le n^{-(c+1)}$. By the union bound over the at most $n$ such nodes, some node is uninformed after $R$ rounds with probability at most $n^{-c}$.

**Total.** The three parts take at most $3L + \log_{4/3} n + R = O(\ln n)$ rounds, and by the union bound they all succeed with probability at least $1 - 3n^{-c}$ for $n \ge 16$. Replacing $c$ by $c + 2$ gives the stated form. $\blacksquare$

**Sketch of the exact form (cited, not proved here).** The constants above are loose. The exact terms come from sharper versions of the same two phases.

1. While $s_t \le n / \ln^2 n$, a message is useless with probability at most $2 s_t / n$, so $s_{t+1} = 2 s_t (1 - O(s_t/n))$ up to small deviations, and the product of the factors $1 - O(s_t/n)$ over the phase is a constant. So the phase ends after $\log_2 n - O(1)$ rounds.
2. In the middle, the fluid recurrence $i_{t+1} = 1 - (1 - i_t)e^{-i_t}$ for the informed fraction $i_t = s_t/n$ goes from $1/\ln^2 n$ to $1 - 1/\ln^2 n$ in $O(\log \log n)$ rounds, and those rounds also count toward $\log_2 n$ and $\ln n$; the careful accounting gives $O(1)$ extra rounds.
3. At the end, an uninformed node stays uninformed with probability $(1 - 1/(n - 1))^{s_t} = e^{-1 + o(1)}$, so $\mathbb{E}[u_{t+1}] \approx u_t / e$, and from $u_t = \Theta(n)$ it takes $\ln n + O(1)$ rounds until $\mathbb{E}[u_t] < 1$. A second moment argument shows that $u_t > 0$ with probability close to 1 until $\ln n - O(1)$ rounds have passed.

Frieze and Grimmett (1985) did this in a continuous time version as a first passage percolation problem; Pittel (1987) carried out the discrete analysis with $O(1)$ error.

## Consequences

- **The cost of push.** All informed nodes send in every round, so the number of messages is $\sum_{t < T_n} s_t$. The coupon collector phase has $(1 - o(1))\ln n$ rounds in which more than half of the nodes send, so push sends $\Theta(n \log n)$ messages, about $n \ln n$. This is the $\Theta(n \log n)$ of Karp et al. (2000), against $O(n \log \log n)$ for [push-pull](/push-pull-gossip/).
- **An age bound.** A push protocol that stops when the rumor is $\log_2 n + c' \ln n$ rounds old, for a large enough constant $c'$, informs all nodes with high probability; with an age of $\log_2 n$ only, a constant fraction of the nodes is still uninformed.
- **Pull and push-pull.** The slow end is the weak point of push. [Pull](/pull-gossip/) squares the uninformed fraction per round, and push-pull needs $\log_3 n + O(\log \log n)$ rounds.
- **The simulation.** The implementation of push gossip gives mean round counts over 30 seeds of 14.8, 18.1 and 21.2 for $n = 256$, 1024 and 4096, against $\log_2 n + \ln n = 13.55$, 16.93 and 20.32; the difference is the $O(1)$ term.

## Tightness

- **Both terms are needed.** The deterministic bound $s_{t+1} \le 2 s_t$ forces $\log_2 n$ rounds. The $\ln n$ term is forced by the end phase: once $s_t \ge n/2$, a fixed uninformed node stays uninformed in a round with probability at least $(1 - 1/(n - 1))^{n} \ge e^{-1 - 2/n}$, so the expected number of uninformed nodes falls by at most a factor of about $e$ per round.
- **The complete graph matters.** On a star, push from the center informs one random leaf per round, so it needs about $n \ln n$ rounds, the time of a coupon collector over $n - 1$ leaves. On every connected graph, push needs $O(n \log n)$ rounds with high probability, and on the hypercube $O(\log n)$ (Feige et al. 1990).
- **Asynchronous time.** If each informed node pushes at the ticks of a Poisson clock of rate 1, the informed fraction follows the logistic curve $\dot i = i(1 - i)$, which takes about $\ln n$ time to reach one half and $\ln n$ more to reach all; see [the epidemic model](/epidemic-model/).

## History

Frieze and Grimmett (1985) studied the spread of push on the complete graph as part of their work on shortest paths in graphs with random arc lengths, and showed that $T_n / \ln n \to 1 + 1/\ln 2$ in probability. Pittel (1987) sharpened this to $\log_2 n + \ln n + O(1)$. Demers et al. (1987) met the same process in the push form of anti-entropy for replicated databases. Feige, Peleg, Raghavan and Upfal (1990) extended the analysis to other graphs, and Karp, Schindelhauer, Shenker and Vöcking (2000) used the slow end of push to motivate push-pull.

## References
