---
tag: 9J2YSP
kind: problem
slug: online-traveling-salesman-problem
name: Online traveling salesman problem
aliases:
- online TSP
- OLTSP
- online TSP with release dates
- homing online TSP
- nomadic online TSP
area: online-and-streaming/competitive-analysis
level: advanced
summary: Requests appear over time at points of a metric space, and a unit speed server must visit them all, with the aim of finishing as early as possible.
prereqs: [traveling-salesman-problem, competitive-ratio, online-algorithm, metric-space]
see_also: [online-dial-a-ride-problem, online-graph-exploration-problem, online-minimum-spanning-tree-problem, k-server-problem, vehicle-routing-problem, linear-search-problem, metric-tsp, yao-minimax-principle]
sources:
  - paper: "Giorgio Ausiello, Esteban Feuerstein, Stefano Leonardi, Leen Stougie and Maurizio Talamo, Algorithms for the on-line travelling salesman, Algorithmica 29(4) (2001)"
    title: "Ausiello, Feuerstein, Leonardi, Stougie and Talamo, Algorithms for the on-line travelling salesman (2001)"
    locator: the model, the 2-competitive algorithm Plan At Home for the closed version, the lower bounds 2 and (9 + sqrt 17)/8 for the closed version, the lower bound 2 for the open version, and the algorithms with ratios 2.5, 7/3 and 1.75
  - paper: "Antje Bjelde, Yann Disser, Jan Hackfeld, Christoph Hansknecht, Maarten Lipmann, Julie Meissner, Kevin Schewior, Miriam Schloeter and Leen Stougie, Tight bounds for online TSP on the line, SODA 2017; ACM Transactions on Algorithms 17(1) (2021)"
    title: "Bjelde et al., Tight bounds for online TSP on the line"
    locator: the (9 + sqrt 17)/8-competitive algorithm for the closed version on the line, and the matching upper and lower bounds of about 2.04 for the open version on the line
  - paper: "Maarten Lipmann, On-line routing, PhD thesis, Technische Universiteit Eindhoven, 2003"
    title: "Lipmann, On-line routing (2003)"
    locator: the (1 + sqrt 2)-competitive algorithm for the open version in general metric spaces
  - paper: "Michiel Blom, Sven O. Krumke, Willem E. de Paepe and Leen Stougie, The online TSP against fair adversaries, INFORMS Journal on Computing 13(2) (2001)"
    title: "Blom, Krumke, de Paepe and Stougie, The online TSP against fair adversaries (2001)"
    locator: the best possible ratio 3/2 on the half-line, and the fair adversary model
---

The online traveling salesman problem asks a server to visit requests that appear over time in a metric space. The server starts at an origin at time $0$ and moves at unit speed. Each request is a point that becomes known at its release time, and the server must visit the point at that time or later. In the *closed* version the server must return to the origin at the end, and in the *open* version it may stop anywhere. The goal is to finish as early as possible. Ausiello, Feuerstein, Leonardi, Stougie and Talamo (AFLST) introduced the problem in 2001 and showed that the closed version has competitive ratio exactly $2$ in general metric spaces. On the real line, the best ratios are $(9 + \sqrt{17})/8 \approx 1.64$ for the closed version and about $2.04$ for the open version (Bjelde et al. 2017).

This page is about the online setting with release times. The offline problem is the [traveling salesman problem](/traveling-salesman-problem/).

## In plain words

A repair person starts at the office. During the day, calls come in from customers at different places. The repair person must visit every customer, but not before the call. At the end of the day, the repair person goes back to the office. The aim is to get back as early as possible.

The difficulty is that the repair person does not know which calls will come later. Driving far in one direction may be a mistake if the next call comes from the other side. Sometimes it is even better to wait. A simple rule works well: when at the office, plan the best round trip through the open calls. If a new call comes from farther away than the current position, go back to the office and plan again. This rule never takes more than twice the best possible time.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(M, d)$ | a metric space in which the server can move continuously, such as a graph with edges as line segments, or the real line |
| $o$ | the origin, where the server is at time $0$ |
| $\sigma = (r_1, x_1), \ldots, (r_n, x_n)$ | the requests: request $i$ appears at time $r_i \ge 0$ at point $x_i$ |
| $p(t)$ | the position of the server at time $t$ |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the completion time of the online algorithm, and of the best offline schedule that knows $\sigma$ in advance |

**Input.** The metric space and the origin, known in advance. The requests are revealed at their release times. The algorithm does not know $n$ or when the last request comes.

**Output.** A route $p(t)$ with $p(0) = o$ and speed at most $1$, such that for each $i$ there is a time $t_i \ge r_i$ with $p(t_i) = x_i$. In the closed version, the route ends at $o$.

**Cost.** The completion time: the first time at which all requests are served, and in the closed version the server is back at $o$. This is the makespan.

**Competitive ratio.** An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$, with additive constant $0$. The algorithm may use unbounded computation time. Two simple bounds on the optimum are used all the time: $\mathrm{OPT} \ge r_i + d(x_i, o)$ for each $i$ in the closed version, because the server visits $x_i$ after time $r_i$ and then returns, and $\mathrm{OPT}$ is at least the length of an optimal tour of all the request points.

## Variants

- **Open version.** Also called the nomadic version. The server does not return. The lower bound is about $2.04$ already on the line, and the best known algorithm in general metric spaces is $(1 + \sqrt 2)$-competitive (Lipmann 2003).
- **Line and half-line.** On the real line the problem is solved: $(9 + \sqrt{17})/8$ for closed and about $2.04$ for open, with matching algorithms (Bjelde et al. 2017). On the half-line $[0, \infty)$ with the origin at $0$, the closed version has best ratio $3/2$ (Blom, Krumke, de Paepe and Stougie 2001).
- **Fair adversary.** The offline server may not leave the convex hull of the requests released so far. Blom et al. get a ratio of about $1.28$ on the half-line in this model.
- **Sum of completion times.** The online traveling repairman, or online latency, problem minimizes the sum (or weighted sum) of the times at which the requests are served. Feuerstein and Stougie gave a $9$-competitive algorithm on the line, and Krumke, de Paepe, Poensgen and Stougie a $(1 + \sqrt 2)^2 \approx 5.83$-competitive algorithm for general metric spaces.
- **Maximum flow time.** The objective is the largest delay $t_i - r_i$. For the open version, no online algorithm is competitive for this objective (Krumke et al.), and a fair adversary model is needed.
- **Pickup and delivery.** Requests are rides from a source to a destination, as in the [online dial-a-ride problem](/online-dial-a-ride-problem/). Online TSP is the special case where the source and the destination are the same.
- **Several servers and precedence constraints.** Jaillet and Wagner gave $2$-competitive algorithms for the closed version that also handle several servers and precedence constraints between requests.
- **Points without release times.** If points arrive one at a time and a tour must be kept, with no time in the model, the problem is closer to the [online minimum spanning tree problem](/online-minimum-spanning-tree-problem/).

## Examples

**Going home and replanning.** On the line, a request appears at $3$ at time $0$, and another at $-2$ at time $1$. Plan At Home (see below) starts the tour $0 \to 3 \to 0$. At time $1$ the server is at $1$, and the new request is farther from the origin, at distance $2$. So it goes home, arriving at time $2$, and then follows the tour $0 \to 3 \to -2 \to 0$ of length $10$. It finishes at time $12$. The optimum goes $0 \to 3 \to -2 \to 0$ at once and finishes at time $10$. The ratio is $1.2$.

**The value of waiting.** A request at $1$ appears at time $0$, and a second request at the same point at time $2$. Plan At Home serves the first one and is home at time $2$, then goes out again and finishes at time $4$. The optimum walks to $1$, waits there until time $2$, and is home at time $3$. The ratio is $4/3$. An online algorithm cannot know whether waiting pays, which is one reason why no algorithm reaches ratio $1$.

## Known algorithms

- **Plan At Home (PAH).** AFLST. When at the origin, compute an optimal tour of the unserved requests and follow it. When a request $x$ appears while the server is at $p \ne o$ on a tour, go back to the origin if $d(x, o) > d(p, o)$, and otherwise ignore $x$ until the server is home. It is $2$-competitive for the closed version in every metric space (Theorem 1), which is best possible.
- **Open version in general metric spaces.** AFLST gave a $5/2$-competitive algorithm, and Lipmann improved the ratio to $1 + \sqrt 2$.
- **Algorithms for the line.** AFLST gave a $7/4$-competitive algorithm for the closed version and a $7/3$-competitive algorithm for the open version. Bjelde et al. gave best possible algorithms for both, with ratios $(9 + \sqrt{17})/8$ and about $2.04$. Their algorithms compare the current position with a *safe tour* that is guaranteed to keep the ratio, and they wait when moving would risk it.
- **Computation time.** PAH and Replan solve offline TSP instances, which are NP-hard in general metric spaces. With a $\rho$-approximate tour in place of the optimal one, the guarantee becomes larger, as for any online algorithm built on an offline subroutine.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| closed, general metric spaces | $2$ (AFLST) | $2$, PAH (AFLST) |
| closed, real line | $(9 + \sqrt{17})/8 \approx 1.64$ (AFLST) | $(9 + \sqrt{17})/8$ (Bjelde et al. 2017); earlier $7/4$ (AFLST) |
| closed, half-line | $3/2$ (Blom et al. 2001) | $3/2$ (Blom et al. 2001) |
| open, general metric spaces | about $2.04$ (Bjelde et al. 2017, from the line); earlier $2$ (AFLST) | $1 + \sqrt 2 \approx 2.41$ (Lipmann 2003); earlier $5/2$ (AFLST) |
| open, real line | about $2.04$ (Bjelde et al. 2017) | about $2.04$ (Bjelde et al. 2017); earlier $7/3$ (AFLST) |

All the bounds are for deterministic algorithms. The constant $2.04$ is a root of a polynomial equation, and Bjelde et al. give it to more digits. The simple lower bounds of Theorem 2 below also hold for randomized algorithms.

**Theorem 1 (PAH is 2-competitive).** For the closed version in every metric space, $\mathrm{ALG}(\sigma) \le 2\,\mathrm{OPT}(\sigma)$ for PAH.

*Proof.* Let $x$ be a request with the latest release time $t$. Then $\mathrm{OPT} \ge t + d(x, o)$. For every set $U$ of requests, an optimal tour $T^*(U)$ from $o$ through $U$ has length at most $\mathrm{OPT}$, because the optimal schedule visits all points of $U$. Look at the state of PAH at time $t$, after the rule for $x$ is applied.

*Case 1: the server is at $o$.* All requests are known, so PAH finishes by $t + \lvert T^*(U) \rvert \le t + \mathrm{OPT} \le 2\,\mathrm{OPT}$.

*Case 2: the server goes home.* Suppose PAH started to go home at time $t' \le t$, because of a request $y$ with release time $t'$ and $d(y, o) > d(p(t'), o)$. The server moves straight to $o$, so it is home at time $t' + d(p(t'), o) < t' + d(y, o) \le \mathrm{OPT}$. Then it follows a tour of length at most $\mathrm{OPT}$, and no request appears later. So $\mathrm{ALG} \le 2\,\mathrm{OPT}$.

*Case 3: the server follows a tour $T_S$.* The tour started at time $t_S < t$ at $o$, and it serves a set $S$ with $\lvert T_S \rvert \le \mathrm{OPT}$. Let $R$ be the requests released in $(t_S, t]$. PAH did not go home for any of them, so each $z \in R$ has $d(z, o) \le d(p(r_z), o)$, where $r_z$ is its release time. After $T_S$, PAH follows an optimal tour of $R$ and finishes. Let $q$ be the first request of $R$ that the optimal schedule visits, at a time $s \ge r_q$, and let $L$ be the length of the optimal route after time $s$. This route starts at $q$, visits all of $R$, and ends at $o$, so $\mathrm{OPT} \ge s + L \ge r_q + L$, and $\lvert T^*(R) \rvert \le d(o, q) + L$. At time $r_q$, PAH is at $p = p(r_q)$ on $T_S$. Split $T_S$ into the part $a$ from $o$ to $p$ and the rest $b$. Then $r_q = t_S + a$, and $a \ge d(o, p) \ge d(o, q)$. So

$$\mathrm{ALG} = t_S + a + b + \lvert T^*(R) \rvert \le r_q + b + d(o, q) + L \le (r_q + L) + (a + b) \le \mathrm{OPT} + \lvert T_S \rvert \le 2\,\mathrm{OPT}. \qquad \square$$

A simulation of PAH on the line against the exact optimum, over a few thousand random instances with up to five requests, reaches the ratio $2$ and never exceeds it.

**Theorem 2 (simple lower bounds).** On the real line, every online algorithm, deterministic or randomized, has ratio at least $2$ for the open version and at least $3/2$ for the closed version.

*Proof.* No request appears before time $1$. Let $p = p(1)$. A deterministic adversary releases one request at time $1$, at $-1$ if $p \ge 0$ and at $+1$ otherwise. The optimum walks to the request and is there at time $1$, so $\mathrm{OPT} = 1$ for the open version and $\mathrm{OPT} = 2$ for the closed version. The online server is at distance at least $1$ from the request at time $1$, so it serves it at time at least $2$, and it is home at time at least $3$. The ratios are $2$ and $3/2$. For randomized algorithms, let the adversary choose $\pm 1$ uniformly at random. For every fixed $p$, the expected distance $\tfrac12 \lvert p - 1 \rvert + \tfrac12 \lvert p + 1 \rvert$ is at least $1$, so every deterministic algorithm has expected completion time at least $2$ (open) and $3$ (closed) while $\mathrm{OPT}$ is $1$ and $2$. [Yao's principle](/yao-minimax-principle/) gives the bounds for randomized algorithms. $\square$

## Reductions

- **From offline TSP.** If all requests are released at time $0$, the online algorithm knows the whole input, and the problem is the offline [traveling salesman problem](/traveling-salesman-problem/). Only the computation is hard, so an online algorithm that runs in polynomial time cannot beat the approximation hardness of [metric TSP](/metric-tsp/) on such inputs.
- **To online dial-a-ride.** Online TSP is the special case of the [online dial-a-ride problem](/online-dial-a-ride-problem/) where every ride has the same source and destination. So the lower bounds of online TSP, such as $2.04$ for the open version on the line, also hold for dial-a-ride.
- **Relation to graph exploration.** In the [online graph exploration problem](/online-graph-exploration-problem/), the unknown points are the vertices of a graph that the server discovers as it moves, while here the points are given by release times.

## Applications

- **Repair and service scheduling.** Technicians who receive calls during the day.
- **Robot and drone routing.** A robot that must inspect points that are reported while it moves.
- **Elevators and warehouse picking.** Requests on a line or on a small graph, with the aim of finishing the batch early.

## References
