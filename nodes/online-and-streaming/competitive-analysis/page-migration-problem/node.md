---
tag: XEZ8BD
kind: problem
slug: page-migration-problem
name: Page migration problem
aliases:
- file migration problem
- page migration
- file migration
area: online-and-streaming/competitive-analysis
level: research
summary: Move a shared memory page among processors to minimize access cost plus migration cost.
prereqs: [metrical-task-systems, competitive-ratio, metric-space]
see_also: [work-function, ski-rental-problem, k-server-problem, randomized-online-algorithm, adaptive-adversary, oblivious-adversary, online-facility-location-problem]
sources:
  - paper: "David L. Black and Daniel D. Sleator, Competitive algorithms for replication and migration problems, Technical Report CMU-CS-89-201, Carnegie Mellon University (1989)"
    title: "Black and Sleator, Competitive algorithms for replication and migration problems (1989)"
    locator: the page migration model, the 3-competitive deterministic algorithms for trees and for uniform networks, and the lower bound 3
  - paper: "Jeffery Westbrook, Randomized algorithms for multiprocessor page migration, SIAM Journal on Computing 23(5) (1994), 951-965"
    title: "Westbrook, Randomized algorithms for multiprocessor page migration (1994)"
    locator: the randomized algorithms that are 3-competitive against an adaptive online adversary and about 2.618-competitive against an oblivious adversary for large D
  - paper: "Marek Chrobak, Lawrence L. Larmore, Nick Reingold and Jeffery Westbrook, Page migration algorithms using work functions, Journal of Algorithms 24(1) (1997), 124-157"
    title: "Chrobak, Larmore, Reingold and Westbrook, Page migration algorithms using work functions (1997)"
    locator: the work function view of page migration, and the deterministic lower bound 85/27 for some metric spaces
  - paper: "Yair Bartal, Moses Charikar and Piotr Indyk, On page migration and other relaxed task systems, Theoretical Computer Science 268(1) (2001)"
    title: "Bartal, Charikar and Indyk, On page migration and other relaxed task systems (2001)"
    locator: the deterministic algorithm Move-To-Local-Min with ratio about 4.086 on every metric space
  - paper: "Marcin Bienkowski, Jaroslaw Byrka and Marcin Mucha, Dynamic beats fixed: on phase-based algorithms for file migration, ICALP 2017, LIPIcs 80"
    title: "Bienkowski, Byrka and Mucha, Dynamic beats fixed: on phase-based algorithms for file migration (2017)"
    locator: the deterministic 4-competitive algorithm for every metric space
---

In the page migration problem, one memory page (or file) of size $D$ lives at one node of a network, and the nodes ask for data from it. Each request from node $v$ costs the distance from $v$ to the page. After a request, the algorithm may move the page, which costs $D$ times the distance moved. The goal is to keep the total cost low without knowing the future requests. Black and Sleator introduced the problem in 1989 and gave 3-competitive deterministic algorithms for trees and for uniform networks, together with a lower bound of $3$ that holds already for two nodes. For general metric spaces the best deterministic ratio is known only to lie between about $3.16$ and $4$.

## In plain words

A team in several offices shares one big folder. Only one office can hold it at a time. When someone in another office needs a page of the folder, the request travels to the holder, and the cost grows with the distance. You can also move the whole folder to another office, but that costs a lot, because the folder is big.

If one office keeps asking, it is better to bring the folder there. But if you move it after every request, you pay the big cost too often. A good rule moves the folder only after an office has asked enough times to pay for about two moves. No rule that does not know the future can always pay less than about three times the best cost in hindsight.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(V, d)$ | the network: a metric space on $n$ nodes |
| $D$ | the page size, a number $D \ge 1$ |
| $\sigma = v_1, \ldots, v_m$ | the request sequence: $m$ nodes |
| $p_t$ | the node of the page after request $t$; $p_0$ is given |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the online cost and the optimal offline cost |
| $c$ | the competitive ratio |

**Input.** The network, the page size $D$, the start node $p_0$, and the requests $v_1, \ldots, v_m$, which arrive online.

**Output.** The nodes $p_1, \ldots, p_m$. The algorithm fixes $p_t$ after it sees $v_t$ and before it sees $v_{t+1}$.

**Cost.** Request $t$ is served from $p_{t-1}$, then the page may move:

$$\mathrm{cost} = \sum_{t=1}^{m} \big( d(v_t, p_{t-1}) + D \cdot d(p_{t-1}, p_t) \big).$$

**Competitive ratio.** A deterministic algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$, with $b$ independent of $\sigma$. The upper bounds below hold with $b = 0$ unless the text says otherwise. For randomized algorithms the adversary is named in each case.

**The offline optimum.** A dynamic program over the page position computes OPT: $w_0(x) = D\,d(p_0, x)$ and $w_t(x) = \min_y \big( w_{t-1}(y) + d(v_t, y) + D\,d(y, x) \big)$, with $\mathrm{OPT} = \min_x w_m(x)$. This is the [work function](/work-function/) of the problem, and it takes $O(m n^2)$ time.

## Variants

- **File allocation.** Several copies of the page may exist. A read is served by the nearest copy, and a write must update all copies. Bartal, Fiat and Rabani, and Awerbuch, Bartal and Fiat studied this problem, which combines migration with replication.
- **Dynamic networks.** The distances change over time, for example for mobile nodes. Bienkowski, Byrka, Korzeniowski and Meyer auf der Heide studied this case.
- **Continuous spaces.** The nodes are all points of a tree or of the Euclidean space, so the page can stop anywhere. Several of the lower bounds use such spaces.
- **Relaxed task systems.** Bartal, Charikar and Indyk view page migration as a [metrical task system](/metrical-task-systems/) where the task cost of a state is its distance to the request and moves cost $D$ times the distance. The general MTS bound $2n - 1$ is far weaker than the bounds that use this structure.

## Examples

**Two nodes, a counter rule.** Let the nodes $0$ and $1$ be at distance $1$, let $D = 2$ and $p_0 = 0$. The rule COUNT keeps a counter $c$ of the requests from the other node since its last move. When $c$ reaches $2D$, it moves the page to the other node and sets $c = 0$. On $\sigma = 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0$:

| $t$ | $v_t$ | ALG pays | $c$ after | page after | ALG so far | OPT so far |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 2 | 0 | 2 | 2 |
| 3 | 0 | 0 | 2 | 0 | 2 | 2 |
| 4 | 1 | 1 | 3 | 0 | 3 | 3 |
| 5 | 1 | 1 + 2 | 0 | 1 | 6 | 3 |
| 6 | 1 | 0 | 0 | 1 | 6 | 3 |
| 7 | 0 | 1 | 1 | 1 | 7 | 4 |
| 8 | 0 | 1 | 2 | 1 | 8 | 5 |
| 9 | 0 | 1 | 3 | 1 | 9 | 5 |
| 10 | 0 | 1 + 2 | 0 | 0 | 12 | 5 |
| 11 | 0 | 0 | 0 | 0 | 12 | 5 |

COUNT pays $12$. The optimum never moves and pays $5$ for the five requests from node $1$. The ratio is $2.4 \le 3$.

**The adversary for two nodes.** If each request comes from the node without the page, COUNT pays $2D + D = 3D$ in each phase between two moves, and the optimum pays about $D$ per phase. For $D = 1, 2, 3, 5$ and $400D$ requests, the exact optimum is $1/3$ of the cost of COUNT.

## Known algorithms

- **COUNT on two nodes and on trees.** Black and Sleator move the page across an edge of a tree when the requests from the far side, counted with care, reach $2D$. On a tree this gives a deterministic ratio of $3$, which is optimal. For uniform networks, a similar rule with one counter per node is also $3$-competitive.
- **Randomized memoryless rules.** Westbrook's COINFLIP moves the page to the requesting node with a fixed probability that depends on $D$. It is $3$-competitive against an adaptive online adversary. His COUNTER algorithm uses a random start value of a counter and is $(1 + \phi)$-competitive against an oblivious adversary as $D \to \infty$, where $1 + \phi \approx 2.618$.
- **General metrics, deterministic.** Awerbuch, Bartal and Fiat (1993) gave a $7$-competitive algorithm. Bartal, Charikar and Indyk (1997, journal 2001) gave Move-To-Local-Min, with ratio about $4.086$. Bienkowski, Byrka and Mucha (2017) gave a $4$-competitive algorithm whose phases have a length that depends on the requests.
- **Work function algorithms.** Chrobak, Larmore, Reingold and Westbrook (1993, journal 1997) used work functions to design algorithms for page migration on special spaces and to prove lower bounds.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, two nodes, trees, uniform networks | 3 (Black and Sleator 1989) | 3 (Black and Sleator 1989) |
| deterministic, every metric | 3 | 4 (Bienkowski, Byrka and Mucha 2017) |
| deterministic, worst metric | $85/27 \approx 3.148$ (Chrobak, Larmore, Reingold and Westbrook 1997); about $3.164$ (Matsubayashi 2015) | 4 |
| randomized, adaptive online adversary | 3 | 3 (Westbrook 1994) |
| randomized, oblivious adversary, large $D$ | | $1 + \phi \approx 2.618$ (Westbrook 1994) |

**Theorem 1 (COUNT on two nodes).** On two nodes at distance $1$, COUNT is strictly $3$-competitive: $\mathrm{ALG}(\sigma) \le 3\,\mathrm{OPT}(\sigma)$ for every $\sigma$.

*Proof.* Compare COUNT with any offline schedule. Let $a$ be the node of the page of COUNT and $o$ the node of the offline page. Define $\Phi = 2c$ if $o = a$, and $\Phi = 3D - c$ if $o \ne a$. Then $\Phi \ge 0$, since $c \le 2D$, and $\Phi = 0$ at the start. Each event satisfies $\Delta \mathrm{ALG} + \Delta\Phi \le 3\,\Delta\mathrm{OPT}$:

- A request from node $a$: COUNT pays $0$, $c$ and $\Phi$ do not change, and the offline pays $0$ or $1$.
- A request from the other node, with $o = a$: both pay $1$, $c$ grows by $1$, and $1 + 2 \le 3$.
- A request from the other node, with $o \ne a$: COUNT pays $1$, the offline pays $0$, $c$ grows by $1$, and $1 - 1 = 0$.
- COUNT moves, at $c = 2D$, to the node $o$: it pays $D$, and $\Phi$ goes from $3D - 2D = D$ to $0$. The sum is $0$.
- COUNT moves away from $o$: it pays $D$, and $\Phi$ goes from $4D$ to $3D$. The sum is $0$.
- The offline page moves: the offline pays $D$, and $\Phi$ changes from $2c$ to $3D - c$ or back. Both changes are at most $3D$, since $0 \le c \le 2D$.

Summing over all events gives $\mathrm{ALG} + \Phi_{\mathrm{end}} \le 3\,\mathrm{OPT}$. $\square$

**Theorem 2 (lower bound 3).** On two nodes, no deterministic algorithm is $c$-competitive for any $c < 3$.

*Proof.* The adversary always requests the node where the online page is not. Split the sequence into phases at the moves of the algorithm, and let phase $i$ have $k_i$ requests. The algorithm pays $\mathrm{ALG} = K + P$, with $K = \sum k_i$ and $P = D \cdot (\text{number of moves})$. The requests of each phase come from one node, and the node alternates between phases. Three offline schedules: stay at node $0$ forever, stay at node $1$ forever, or move to the requested node at the end of each phase, ready for the next phase. The first two pay $K$ together, and the third pays at most $P + 1 + D$. So $\mathrm{OPT} \le \min(K/2, P) + 1 + D \le (K + P)/3 + 1 + D$, since $\min(x, y) \le (2x + y)/3$ for $x = K/2$ and $y = P$. If the algorithm moves only finitely often, $K$ grows without bound while OPT stays bounded. In all cases $\mathrm{ALG} \ge 3\,\mathrm{OPT} - 3(1 + D)$, and ALG grows without bound. $\square$

The proofs of the bounds for trees, for uniform networks, for general metrics and for the randomized algorithms are only cited here.

## Reductions

- **Ski rental.** For two nodes and one long run of requests from the far node, the decision "pay $1$ per request or pay $D$ once" is the [ski rental problem](/ski-rental-problem/). Page migration repeats it, and the offline optimum can also move back, which is why the ratio is $3$ and not $2$.
- **Metrical task systems.** Page migration is an MTS on the $n$ nodes with metric $D \cdot d$ and the task costs $r_t(x) = d(v_t, x)$, with a delay of one step for the service. The MTS bound $2n - 1$ applies but is weak.
- **Facility location.** A page that serves requests is a single facility that may move. The [online facility location problem](/online-facility-location-problem/) instead opens new facilities and never moves them.

## Applications

- **Shared memory multiprocessors.** In a NUMA machine, a page used by one processor should live in its local memory. The operating system can migrate pages, and the cost of a migration is proportional to the page size. This was the motivation of Black and Sleator.
- **Distributed file systems and caches.** A file or a data object in a network can follow its users, as in content delivery and in mobile data placement.
- **Virtual machines and services.** Moving a running service closer to its clients has the same structure, with the size of the state in the role of $D$.

## References
