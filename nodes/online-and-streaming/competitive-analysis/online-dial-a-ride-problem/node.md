---
tag: NF66RK
kind: problem
slug: online-dial-a-ride-problem
name: Online dial-a-ride problem
aliases:
- online pickup and delivery
- online dial a ride
- OLDARP
area: online-and-streaming/competitive-analysis
level: research
summary: Ride requests with a pickup point and a delivery point appear over time, and a server of bounded capacity must carry them all, with the aim of finishing as early as possible.
prereqs: [online-traveling-salesman-problem, competitive-ratio, metric-space]
see_also: [vehicle-routing-problem, k-server-problem, scheduling-with-release-dates, yao-minimax-principle, traveling-salesman-problem, online-graph-exploration-problem]
sources:
  - paper: "Esteban Feuerstein and Leen Stougie, On-line single-server dial-a-ride problems, Theoretical Computer Science 268(1) (2001)"
    title: "Feuerstein and Stougie, On-line single-server dial-a-ride problems (2001)"
    locator: the lower bound 2 for the closed version, the 2-competitive algorithm for infinite capacity, and the bounds for the sum of completion times
  - paper: "Norbert Ascheuer, Sven O. Krumke and Joerg Rambau, Online dial-a-ride problems: minimizing the completion time, STACS 2000, Lecture Notes in Computer Science 1770"
    title: "Ascheuer, Krumke and Rambau, Online dial-a-ride problems: minimizing the completion time (2000)"
    locator: the algorithms IGNORE, REPLAN and SMARTSTART, the 2-competitive bound of SMARTSTART for every capacity, and the lower bound for unit capacity on the line
  - paper: "Antje Bjelde, Yann Disser, Jan Hackfeld, Christoph Hansknecht, Maarten Lipmann, Julie Meissner, Kevin Schewior, Miriam Schloeter and Leen Stougie, Tight bounds for online TSP on the line, SODA 2017; ACM Transactions on Algorithms 17(1) (2021)"
    title: "Bjelde et al., Tight bounds for online TSP on the line"
    locator: the lower bound 1.75 for the closed non-preemptive version on the line, the lower bound of about 2.04 for the open version, and the preemptive 2.41-competitive algorithm for the open version on the line
  - paper: "Sven O. Krumke, Willem E. de Paepe, Diana Poensgen and Leen Stougie, News from the online traveling repairman, Theoretical Computer Science 295 (2003)"
    title: "Krumke, de Paepe, Poensgen and Stougie, News from the online traveling repairman (2003)"
    locator: the (1 + sqrt 2)^2-competitive algorithm for the sum of completion times
---

The online dial-a-ride problem asks a server to carry objects or passengers from pickup points to delivery points in a metric space, when the ride requests appear over time. The server starts at an origin, moves at unit speed, and can carry at most $c$ objects at a time. Each request becomes known at its release time, and its object can be picked up only from then on. In the closed version, which is the most studied, the server must return to the origin, and the goal is to minimize the completion time. Feuerstein and Stougie (2001) proved that no online algorithm is better than $2$-competitive, and Ascheuer, Krumke and Rambau (2000) gave the algorithm SMARTSTART, which is $2$-competitive for every capacity. So the closed version has competitive ratio exactly $2$ in general metric spaces.

The problem generalizes the [online traveling salesman problem](/online-traveling-salesman-problem/), in which each pickup point equals its delivery point.

## In plain words

A minibus starts at a depot. During the day, people call and ask for rides from one place to another. The bus may pick a person up only after the call, it has a limited number of seats, and it must drop each person at the requested place. At the end, the bus returns to the depot, and the aim is to return as early as possible.

The bus does not know the later calls. If it leaves at once for every call, a call that comes a moment later may force a second long trip. If it waits for more calls, it wastes time when no calls come. A good rule is to wait at the depot until the planned trip is not longer than the time that has already passed, then drive. Such a rule never takes more than twice the best time.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(M, d)$ | a metric space in which the server can move continuously, such as the real line or a graph with edges as segments |
| $o$ | the origin, where the server is at time $0$ |
| $c$ | the capacity of the server, with $1 \le c \le \infty$ |
| $\sigma = (r_1, a_1, b_1), \ldots, (r_n, a_n, b_n)$ | the requests: request $i$ appears at time $r_i \ge 0$ and asks for a ride from $a_i$ to $b_i$ |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the completion time of the online algorithm, and of the best offline schedule |
| $L(R)$ | the length of a shortest closed schedule from $o$ that serves the set $R$, with release times ignored |

**Input.** The metric space, the origin and $c$, known in advance. The requests are revealed at their release times. The algorithm does not know $n$.

**Output.** A route of the server with speed at most $1$, together with pickup and delivery times. Object $i$ is picked up at $a_i$ at a time $t \ge r_i$ and delivered at $b_i$ later. At no time does the server carry more than $c$ objects. In the *non-preemptive* version, an object leaves the server only at its destination. In the *preemptive* version, the server may drop an object anywhere and pick it up again later.

**Cost.** The completion time: the first time at which all objects are delivered and, in the closed version, the server is back at $o$.

**Competitive ratio.** An algorithm is $c'$-competitive if $\mathrm{ALG}(\sigma) \le c' \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$, with additive constant $0$. The algorithm may use unbounded time to compute offline schedules.

## Variants

- **Open version.** The server may end anywhere. On the line, the lower bound is about $2.04$ (Bjelde et al. 2017), and the best known algorithms are a preemptive $2.41$-competitive algorithm (Bjelde et al.) and non-preemptive algorithms based on SMARTSTART.
- **Capacity.** Unit capacity, finite capacity, and infinite capacity. Feuerstein and Stougie gave a best possible $2$-competitive algorithm for infinite capacity. SMARTSTART reaches $2$ for every $c$.
- **Preemption.** Dropping an object on the way can only help the server. On the line, the closed non-preemptive version has a lower bound of $1.75$ for every finite capacity (Bjelde et al.), while the preemptive version has the online TSP lower bound $(9 + \sqrt{17})/8 \approx 1.64$.
- **Sum of completion times.** The objective is the sum of the delivery times. Feuerstein and Stougie proved lower bounds of $3$ for unit capacity and $1 + \sqrt 2 \approx 2.41$ for every capacity, and a $15$-competitive algorithm on the line with infinite capacity. Krumke, de Paepe, Poensgen and Stougie gave a $(1 + \sqrt 2)^2 \approx 5.83$-competitive algorithm for unit capacity in general metric spaces.
- **Offline versions.** Without release times and with unit capacity, the problem is the stacker crane problem. With release times, it is a [vehicle routing problem](/vehicle-routing-problem/) with pickup and delivery, and Bjelde et al. showed that the non-preemptive offline problem on the line is NP-hard for every capacity $c \ge 2$.

## Examples

**SMARTSTART waits.** On the line, with $c = 1$, a ride from $1$ to $3$ appears at time $0$. The shortest closed schedule has length $L = 1 + 2 + 3 = 6$, so SMARTSTART waits at the origin until time $6$. At time $2$, a ride from $-1$ to $-2$ appears. The new schedule $0 \to 1 \to 3 \to -1 \to -2 \to 0$ has length $L = 10$, so SMARTSTART now waits until time $10$, starts, and finishes at time $20$. The optimum drives this schedule at once: it is at $-1$ at time $7$, after the release time $2$, and it finishes at time $10$. The ratio is exactly $2$, the worst case of Theorem 1.

**Waiting also costs.** If the second ride appears at time $5$ instead, SMARTSTART is still waiting at time $5$, so it recomputes $L = 10$, waits until time $10$ again, and finishes at time $20$. A server that starts the first ride at once is home at time $6$ and finishes at time $10$, which is optimal. On other inputs, starting at once is the mistake: a server that has just left on a long schedule cannot serve a new nearby ride until it is back. The start rule balances the two risks, and Theorem 1 shows that the loss is at most a factor $2$ on every input.

## Known algorithms

- **IGNORE.** When idle at the origin, compute an optimal schedule for the unserved requests and follow it, ignoring new requests until it ends. Ascheuer, Krumke and Rambau proved that it is $5/2$-competitive.
- **REPLAN.** At each new request, compute a new optimal schedule from the current position. Also $5/2$-competitive (Ascheuer, Krumke and Rambau).
- **SMARTSTART.** Ascheuer, Krumke and Rambau (2000). When idle at the origin at time $t$ with unserved set $R$, compute $L = L(R)$. If $t \ge L$, follow the schedule and ignore new requests until it ends. Otherwise wait at $o$ until time $L$, and recompute whenever a new request appears. It is $2$-competitive for every capacity (Theorem 1). With a parameter $\theta > 1$ the start rule is $t \ge L/(\theta - 1)$, and $\theta = 2$ is the best choice when the schedules are exact.
- **Feuerstein and Stougie (2001).** A $2$-competitive algorithm for infinite capacity in general metric spaces.
- **Open version on the line.** Krumke gave a non-preemptive $3.41$-competitive algorithm, and Bjelde et al. a preemptive $2.41$-competitive algorithm. Birx and Disser analyzed SMARTSTART for the open version on the line and gave an improved variant, SMARTERSTART.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| closed, general metric spaces, any $c$ | $2$ (Feuerstein and Stougie 2001) | $2$, SMARTSTART (Ascheuer, Krumke and Rambau 2000) |
| closed, line, non-preemptive, finite $c$ | $1.75$ (Bjelde et al. 2017); earlier $1.71$ for $c = 1$ (Ascheuer, Krumke and Rambau) | $2$ (SMARTSTART) |
| closed, line, preemptive | $(9 + \sqrt{17})/8 \approx 1.64$ (from online TSP) | $2$ (SMARTSTART) |
| open, line | about $2.04$ (Bjelde et al. 2017) | $2.41$ preemptive (Bjelde et al.); $3.41$ non-preemptive (Krumke) |
| sum of completion times | $3$ for $c = 1$, $1 + \sqrt 2$ for every $c$ (Feuerstein and Stougie) | $(1 + \sqrt 2)^2 \approx 5.83$ for $c = 1$ (Krumke et al. 2003); $15$ on the line with $c = \infty$ (Feuerstein and Stougie) |

All bounds are for deterministic algorithms. The lower bounds of online TSP hold here as well, because online TSP is the special case $a_i = b_i$.

**Theorem 1 (SMARTSTART is 2-competitive).** For the closed version in every metric space and for every capacity $c$, non-preemptive or preemptive, SMARTSTART with exact schedules for the same version has $\mathrm{ALG}(\sigma) \le 2\,\mathrm{OPT}(\sigma)$.

*Proof.* Two facts about the optimum are used. First, $L(R) \le \mathrm{OPT}$ for every set $R$ of requests, because the optimal schedule serves $R$ and returns to $o$, and dropping the release times only allows more schedules. Second, $\mathrm{OPT} \ge r_i + d(a_i, o)$ for every $i$, because the optimum visits $a_i$ after time $r_i$ and returns to $o$ after that.

By the start rule, every schedule $S_j$ starts at a time $t_j \ge L_j$, where $L_j$ is its length. Let $S_m$ be the last schedule, so $\mathrm{ALG} = t_m + L_m$. Look at the reason why $S_m$ started at time $t_m$.

*Case 1: $t_m \le \mathrm{OPT}$.* This holds if $S_m$ started at the end of a wait, when $t_m = L_m \le \mathrm{OPT}$, or at the release time of a request, which is at most $\mathrm{OPT}$. Then $\mathrm{ALG} = t_m + L_m \le 2\,\mathrm{OPT}$.

*Case 2: $S_m$ started when $S_{m-1}$ ended.* Then $t_m = t_{m-1} + L_{m-1}$, and the set $R_m$ of $S_m$ is the set of requests released after time $t_{m-1}$. Let $q$ be the request of $R_m$ that the optimal schedule picks up first, at a time $s \ge r_q > t_{m-1}$, and let $P$ be the part of the optimal route after time $s$, of length at most $\mathrm{OPT} - s$. The route $P$ starts at $a_q$, picks up and delivers every request of $R_m$ with capacity $c$, and ends at $o$. So the schedule "go from $o$ to $a_q$, then follow $P$ and handle only the requests of $R_m$" serves $R_m$, and

$$L_m \le d(o, a_q) + \mathrm{OPT} - s < d(o, a_q) + \mathrm{OPT} - t_{m-1}.$$

Also $d(o, a_q) \le \mathrm{OPT} - r_q < \mathrm{OPT} - t_{m-1}$ by the second fact, and $L_{m-1} \le t_{m-1}$ by the start rule. So

$$\mathrm{ALG} = t_{m-1} + L_{m-1} + L_m < t_{m-1} + L_{m-1} + d(o, a_q) + \mathrm{OPT} - t_{m-1} < L_{m-1} + (\mathrm{OPT} - t_{m-1}) + \mathrm{OPT} \le 2\,\mathrm{OPT}. \qquad \square$$

A simulation on the line with $c = 1$, against the exact optimum, over a few thousand random instances with up to four rides, reaches the ratio $2$ and never exceeds it.

**Theorem 2 (a simple lower bound).** On the real line, every online algorithm for the closed version, deterministic or randomized, has ratio at least $3/2$.

*Proof.* Use rides with $a_i = b_i$, which turn the problem into online TSP. The proof of the lower bound $3/2$ on the [online traveling salesman problem](/online-traveling-salesman-problem/) page applies without change: one ride at $\pm 1$ released at time $1$, on the side away from the server, or on a random side for randomized algorithms with [Yao's principle](/yao-minimax-principle/). $\square$

The lower bound $2$ of Feuerstein and Stougie holds in general metric spaces, not on the line.

## Reductions

- **From online TSP.** Requests with $a_i = b_i$ give the [online traveling salesman problem](/online-traveling-salesman-problem/). So every lower bound for online TSP holds here, and the algorithms for dial-a-ride also solve online TSP.
- **To offline schedules.** SMARTSTART, IGNORE and REPLAN call an offline solver for dial-a-ride without release times. With a $\rho$-approximate solver, the bound of SMARTSTART grows with $\rho$, and the best choice of $\theta$ changes.
- **Relation to scheduling.** Each ride is a job with a release date, and the travel between rides acts as a setup time that depends on the order, as in [scheduling with release dates](/scheduling-with-release-dates/) with sequence dependent setup times.

## Applications

- **Paratransit and taxi services.** Minibuses for passengers who book rides by phone, which gave the problem its name.
- **Elevators.** An elevator is a server on a line with capacity $c$, and calls appear over time.
- **Warehouses and robots.** Stacker cranes and mobile robots that move items between locations as orders come in.

## References
