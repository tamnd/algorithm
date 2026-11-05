---
tag: HYWX9G
kind: problem
slug: time-dependent-shortest-paths
name: Time-dependent shortest paths
aliases:
- time-dependent routing
area: graphs/shortest-paths
level: advanced
summary: Shortest paths where edge travel time depends on the departure time.
prereqs: [single-pair-shortest-path, dijkstra, shortest-path-optimal-substructure]
see_also: [dijkstra, single-pair-shortest-path, temporal-graph, contraction-hierarchies, alt-algorithm, a-star-search, dynamic-graph, shortest-path-optimal-substructure]
sources:
  - paper: doi:10.1287/opre.17.3.395
    title: Stuart E. Dreyfus, An appraisal of some shortest-path algorithms, Operations Research 17(3), 395 to 412 (1969)
    locator: the section on time-dependent arc lengths, where Dijkstra is run on arrival times
  - paper: "Kenneth L. Cooke and Eric Halsey, The shortest route through a network with time-dependent internodal transit times, Journal of Mathematical Analysis and Applications 14(3), 493 to 498 (1966)"
    locator: the first statement of the problem, in discrete time
  - paper: "David E. Kaufman and Robert L. Smith, Fastest paths in time-dependent networks for intelligent vehicle-highway systems application, IVHS Journal 1(1), 1 to 11 (1993)"
    locator: the FIFO (consistency) condition and the proof that Dijkstra is correct under it
  - paper: "Ariel Orda and Raphael Rom, Shortest-path and minimum-delay algorithms in networks with time-dependent edge-length, Journal of the ACM 37(3), 607 to 625 (1990)"
    locator: the waiting policies (no waiting, waiting at the source, waiting anywhere) and the algorithms for each
  - paper: "Luca Foschini, John Hershberger and Subhash Suri, On the complexity of time-dependent shortest paths, Algorithmica 68(4), 1075 to 1097 (2014)"
    locator: the n^(Theta(log n)) bound on the number of breakpoints of a travel-time profile with piecewise linear functions
  - paper: "Gernot Veit Batz, Robert Geisberger, Peter Sanders and Christian Vetter, Minimum time-dependent travel times with contraction hierarchies, ACM Journal of Experimental Algorithmics 18, article 1.4 (2013)"
    locator: time-dependent contraction hierarchies and profile queries on road networks
---

In a time-dependent network, the time to travel along an arc depends on when you start along it. The time-dependent shortest path problem asks for the earliest arrival at $t$ when leaving $s$ at a given time $\tau_0$, or, in the *profile* version, for the earliest arrival as a function of $\tau_0$. If every arc has the *FIFO property*, that leaving later never makes you arrive earlier, the problem keeps the [optimal substructure](/shortest-path-optimal-substructure/) of ordinary shortest paths, and [Dijkstra's algorithm](/dijkstra/) on arrival times solves it with $O(m + n \log n)$ evaluations of the travel-time functions. Without FIFO and without waiting, the best route may contain cycles, and the problem becomes hard. Road networks with rush hours and timetables are the main applications.

## In plain words

On a real road, a trip takes longer at rush hour than at night. So the best route depends on when you leave.

Usually, leaving a road later never gets you to its end sooner: the cars ahead of you stay ahead. With this rule, the usual method still works. Keep, for each place, the earliest time you can be there, and always continue from the place you can reach the earliest. Without the rule, it can pay to drive around a block and enter a road later, and the problem becomes much harder.

## Definition

Let $G = (V, E)$ be a directed graph with $n$ vertices and $m$ arcs. Each arc $e$ has a *travel-time function* $f_e : \mathbb{R} \to \mathbb{R}_{\ge 0}$: leaving the tail of $e$ at time $\tau$ means arriving at its head at time $a_e(\tau) = \tau + f_e(\tau)$. For a path $p = \langle v_0, \ldots, v_k \rangle$ and a start time $\tau$, the arrival time is the composition

$$A_p(\tau) = a_{e_k}(\cdots a_{e_2}(a_{e_1}(\tau)) \cdots),$$

if no waiting is allowed at the vertices. Given $s$, $t$ and a departure time $\tau_0$, the *earliest arrival problem* asks for

$$\mathrm{EA}(s, t, \tau_0) = \inf \{ A_p(\tau_0) : p \text{ is a walk from } s \text{ to } t \},$$

and a walk that attains it. The *profile problem* asks for the function $\tau_0 \mapsto \mathrm{EA}(s, t, \tau_0) - \tau_0$, the least travel time for each departure time.

**The FIFO property.** An arc $e$ is FIFO if $a_e$ is nondecreasing: $\tau \le \tau'$ implies $\tau + f_e(\tau) \le \tau' + f_e(\tau')$. Then every $A_p$ is nondecreasing too.

**Weight assumptions.**

- Travel times are nonnegative, $f_e \ge 0$. So arrival times never go back in time, and there is no analogue of a [negative cycle](/negative-cycle/) in a FIFO network: a cycle can only make the arrival later.
- The travel times are real numbers, or functions given by a finite description, usually piecewise linear. Integer values are only needed for the discrete-time algorithms.
- The basic algorithm needs the FIFO property. In a non-FIFO network without waiting, a cycle can make the arrival *earlier*, which plays the role of a negative cycle: optimal walks may not be simple, and with infinitely many cycles the infimum may not be reached.
- If waiting at a vertex is allowed, every arc can be replaced by its FIFO hull $\tilde{a}_e(\tau) = \inf_{\tau' \ge \tau} a_e(\tau')$, and the network becomes FIFO.

**Unreachable.** If no walk from $s$ reaches $t$, then $\mathrm{EA}(s, t, \tau_0) = +\infty$ for every $\tau_0$.

## Variants

- **Earliest arrival from one departure time.** The basic query, solved by time-dependent Dijkstra.
- **Profile queries.** The travel time as a function of the departure time over a whole day.
- **Latest departure.** The latest time to leave $s$ so as to reach $t$ by a deadline; under FIFO it is an earliest arrival problem on the reverse graph with the inverse arrival functions.
- **Waiting policies.** No waiting, waiting only at the source, or waiting anywhere (Orda and Rom). Waiting anywhere makes every network FIFO.
- **Discrete time.** Time takes the values $0, 1, \ldots, T$; the time-expanded graph has a copy of each vertex for each time step and is acyclic, so [DAG shortest paths](/dag-shortest-paths/) applies.
- **Timetables.** In public transport, arcs exist only at given departure times. This is the scheduled case of the problem, often modeled by a [temporal graph](/temporal-graph/).
- **Stochastic travel times.** The travel times are random, and one minimizes the expected arrival or the chance of being late; optimal policies may then depend on what was observed on the way.

## Examples

**The best route depends on the departure time.** Take the arcs $s \to a$ with constant travel time 1, $s \to b$ with 2, $b \to t$ with 3, and $a \to t$ with

$$f(\tau) = 6 - \tau \text{ for } 0 \le \tau \le 4, \qquad f(\tau) = 2 \text{ for } \tau \ge 4.$$

So $a_{a t}(\tau) = 6$ up to time 4 and $\tau + 2$ afterward; it is nondecreasing, so the arc is FIFO. It models a road that is jammed until time 4.

| departure from $s$ | via $a$ | via $b$ | best |
|---|---|---|---|
| $\tau_0 = 0$ | at $a$ at 1, at $t$ at 6 | at $b$ at 2, at $t$ at 5 | 5, via $b$ |
| $\tau_0 = 3$ | at $a$ at 4, at $t$ at 6 | at $b$ at 5, at $t$ at 8 | 6, via $a$ |

The travel time is 5 when leaving at 0 and 3 when leaving at 3, and the best path changes in between. Time-dependent Dijkstra from $\tau_0 = 0$ settles $s$ (0), $a$ (1), $b$ (2) and then $t$ (5), relaxing $a \to t$ with $f(1) = 5$ on the way.

**Non-FIFO: a cycle helps.** Take $s \to a$ with time 1, a cycle $a \to c$ and $c \to a$ with time $0.5$ each, and $a \to t$ with $f(\tau) = 10$ for $\tau < 2$ and $f(\tau) = 1$ for $\tau \ge 2$. This arc is not FIFO: leaving at time 1 arrives at 11, leaving at 2 arrives at 3. Leaving $s$ at 0, the simple path $s a t$ arrives at 11, but the walk $s a c a t$ reaches $a$ again at 2 and arrives at 3. Dijkstra settles $a$ at 1 and never uses the second visit, so it gives the wrong answer 11. If waiting at $a$ is allowed, the FIFO hull of $a \to t$ gives 3 directly.

**Unreachable.** Add a vertex $u$ with no incoming arc. For every departure time, $\mathrm{EA}(s, u, \tau_0) = +\infty$, and Dijkstra leaves its label at $+\infty$.

## Known algorithms

| algorithm | setting | cost |
|---|---|---|
| time-dependent Dijkstra (Dreyfus 1969; Kaufman and Smith 1993) | FIFO, one departure time | $O(m + n \log n)$ time and $m$ function evaluations |
| time-expanded graph | discrete time $0, \ldots, T$ | $O(T(n + m))$ |
| Cooke and Halsey (1966) | discrete time, Bellman-Ford style | $O(T n m)$ |
| Orda and Rom (1990) | waiting allowed, any network | label-correcting on arrival functions |
| label-correcting profile search | FIFO, piecewise linear | output-sensitive, can be superpolynomial |
| time-dependent [contraction hierarchies](/contraction-hierarchies/) (Batz et al.) | FIFO road networks | milliseconds per query after preprocessing |
| time-dependent A* or [ALT](/alt-algorithm/) | FIFO, lower bounds from free-flow times | heuristic speed-up of Dijkstra |

**Time-dependent Dijkstra.** Keep a label $d(v)$, the earliest known arrival time at $v$, with $d(s) = \tau_0$ and $d(v) = +\infty$ otherwise. Extract the vertex $u$ with the least label, and for each arc $(u, v)$ set $d(v) \leftarrow \min(d(v), a_{uv}(d(u)))$. The proof is the proof of Dijkstra with "earlier arrival" in place of "shorter": by FIFO, a later arrival at $u$ can never give an earlier arrival at $v$, so it is safe to use only the earliest arrival at each vertex, and by $f \ge 0$, extending a walk never gives an earlier time.

## Bounds

- **One departure time, FIFO.** The same as static SSSP up to the cost of evaluating the functions: $O(m + n \log n)$ with a Fibonacci heap.
- **Profile complexity.** With piecewise linear travel-time functions, the profile from $s$ to $t$ can have $n^{\Theta(\log n)}$ breakpoints in total, even when each arc has a constant number of pieces (Foschini, Hershberger and Suri). So any algorithm that writes out the exact profile needs superpolynomial time in the worst case. Approximate profiles with few breakpoints can be computed in polynomial time.
- **Non-FIFO without waiting.** Finding the best simple path is NP-hard in general, and a best walk need not exist. These cases are excluded by FIFO or by allowing waiting.

## Reductions

- **To static shortest paths.** If every $f_e$ is constant, the problem is ordinary [single-pair shortest path](/single-pair-shortest-path/).
- **Waiting to FIFO.** Replace each arrival function by its FIFO hull.
- **Discrete time to DAG shortest paths.** The time-expanded graph has the vertices $(v, \tau)$ and an arc $(u, \tau) \to (v, \tau + f_{uv}(\tau))$; it is acyclic because $f \ge 0$, provided zero travel times do not form a cycle.
- **Latest departure to earliest arrival.** Reverse the graph and use the inverse of each nondecreasing arrival function.

## Applications

- **Car navigation.** Travel-time predictions by time of day, from historical traffic data, give the functions $f_e$; the route planner answers time-dependent queries.
- **Public transport.** Timetable queries ask for the earliest arrival given a departure time, and profile queries ask for all good connections over a day.
- **Logistics and vehicle routing.** Delivery routes with time-dependent travel times and time windows.
- **Networks with time-varying delays.** Packet routing where link delays change over time, the setting of Orda and Rom.

## References
