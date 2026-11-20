---
tag: 5CNCPT
kind: theorem
slug: price-of-anarchy-of-load-balancing
name: Price of anarchy of selfish load balancing
aliases:
- Czumaj-Vocking bound
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: For mixed equilibria on m related machines the price of anarchy of the makespan is Theta(log m / log log log m).
prereqs: [load-balancing-game, price-of-anarchy, balls-into-bins]
see_also: [list-scheduling, list-scheduling-bound, lpt-bound, smoothness-framework, atomic-linear-congestion-price-of-anarchy, makespan-minimization, price-of-stability, mixed-strategy]
sources:
  - paper: doi:10.1145/1186810.1186814
    title: "Artur Czumaj and Berthold Vocking, Tight bounds for worst-case equilibria, ACM Transactions on Algorithms 3(1) (2007), Article 4; SODA 2002"
    locator: "the bound Gamma^(-1)(m) + Theta(1) for identical machines and the bound Theta(log m / log log log m) for related machines, with matching lower bounds"
  - paper: doi:10.1007/s00224-003-1131-5
    title: "Elias Koutsoupias, Marios Mavronicolas and Paul Spirakis, Approximate equilibria and ball fusion, Theory of Computing Systems 36(6) (2003), 683-693"
    locator: the upper bound for identical machines by reduction from weighted to unit balls (ball fusion)
  - paper: doi:10.1007/3-540-49116-3_38
    title: "Elias Koutsoupias and Christos Papadimitriou, Worst-case equilibria, STACS 1999, Lecture Notes in Computer Science 1563, 404-413"
    locator: "the coordination ratio, the bound 3/2 for two identical machines, and the first bounds for m machines"
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 20, Berthold Vocking, Selfish load balancing (the bound for pure equilibria on identical machines and the proofs of the mixed bounds)"
---

This page states how much worse than optimal the makespan of an equilibrium of the [load balancing game](/load-balancing-game/) can be. For pure equilibria on identical machines the answer is a constant below 2, with a full proof here. For mixed equilibria the answer grows with the number of machines, slowly, and the tight growth rates are due to Czumaj and Vocking. The [load balancing game](/load-balancing-game/) page defines the model; the scheduling page [list scheduling](/list-scheduling/) gives the close greedy bound $2 - 1/m$ for a schedule that a central planner builds.

## Statement

Let $m$ be the number of machines and $n$ the number of jobs, which are the players. Each job chooses a machine and pays the load of that machine; the social cost is the makespan, or the expected makespan for mixed profiles. The price of anarchy is the largest ratio of the (expected) makespan of an equilibrium to the optimal makespan. Pure equilibria exist in all the environments below ([load balancing game](/load-balancing-game/)).

**Theorem 1 (pure equilibria, identical machines).** On $m$ identical machines with any job weights, every pure Nash equilibrium has makespan at most $\left(2 - \frac{2}{m + 1}\right) \mathrm{OPT}$, and for every $m$ there is an instance where this ratio is reached.

**Theorem 2 (Czumaj and Vocking 2002; Koutsoupias, Mavronicolas and Spirakis 2003).** The price of anarchy of the makespan is

| machines | pure equilibria | mixed equilibria |
|---|---|---|
| identical | $2 - 2/(m + 1)$ | $\Theta(\log m / \log \log m)$ |
| related | $\Theta(\log m / \log \log m)$ | $\Theta(\log m / \log \log \log m)$ |

For mixed equilibria on identical machines, Czumaj and Vocking give the sharper form $\Gamma^{-1}(m) + \Theta(1)$, where $\Gamma^{-1}$ is the inverse of the gamma function, and $\Gamma^{-1}(m) = (1 + o(1)) \ln m / \ln \ln m$.

## In plain words

Jobs pick machines on their own, each one wanting to finish early. When nobody wants to move, the busiest machine can still be late. If each job picks one machine for sure and all machines run at the same speed, the busiest machine is never late by a factor of two or more. If the jobs pick at random, bad luck can pile many jobs on one machine, the same way that throwing balls into bins at random fills some bins more than others. Then the loss grows with the number of machines, but very slowly. With machines of different speeds the loss grows faster, but it is still slow.

## Proof

**Proof of Theorem 1.** Let $a$ be a pure equilibrium, and let machine $h$ have the largest load $L = L_h$. Let $W = \sum_j w_j$ be the total weight. Two lower bounds on the optimum are $\mathrm{OPT} \ge W/m$ and $\mathrm{OPT} \ge w_j$ for every job $j$.

*Case 1: machine $h$ holds one job $j$.* Then $L = w_j \le \mathrm{OPT}$.

*Case 2: machine $h$ holds two or more jobs.* Let $w$ be the smallest weight on $h$, so $w \le L/2$. That job does not gain by a move to any other machine $k$, so $L \le L_k + w$, that is $L_k \ge L - w$. Adding over all machines,

$$W = L + \sum_{k \ne h} L_k \ge L + (m - 1)(L - w) = mL - (m - 1) w \ge mL - (m - 1)\frac{L}{2} = \frac{(m + 1) L}{2}.$$

So $\mathrm{OPT} \ge W/m \ge \frac{(m + 1) L}{2m}$, that is $L \le \frac{2m}{m + 1} \mathrm{OPT} = \left(2 - \frac{2}{m + 1}\right) \mathrm{OPT}$. In case 1 the ratio is 1, which is smaller. $\blacksquare$

**Tight instance for Theorem 1.** Take two jobs of weight $m$ and $m(m - 1)$ jobs of weight 1. Put both large jobs on machine 1, and $m$ unit jobs on each of machines $2, \dots, m$.

- Machine 1 has load $2m$, and every other machine has load $m$.
- A large job that moves pays $m + m = 2m$, no less than now. A unit job that moves pays $m + 1$ or $2m + 1$, more than $m$. So the schedule is an equilibrium with makespan $2m$.
- The total weight is $m(m + 1)$, so $\mathrm{OPT} \ge m + 1$. Put one large job and one unit job on each of machines 1 and 2, and spread the other $m(m - 1) - 2 = (m - 2)(m + 1)$ unit jobs, $m + 1$ per machine, over machines $3, \dots, m$. Every load is $m + 1$, so $\mathrm{OPT} = m + 1$.

The ratio is $2m/(m + 1) = 2 - 2/(m + 1)$. For $m = 2$ this is the instance $2, 2, 1, 1$ with ratio $4/3$; for $m = 3$ it is $3, 3$ and six unit jobs, with makespan 6 against 4.

**Lower bound for mixed equilibria on identical machines.** Take $m$ unit jobs, each of which picks a machine uniformly at random. A job pays $1 + (m - 1)/m$ on every machine, so every machine is a best response and the profile is an equilibrium. The optimum is 1. The expected makespan is the expected largest bin when $m$ balls are thrown into $m$ bins, which is $(1 + o(1)) \ln m / \ln \ln m$ ([balls into bins](/balls-into-bins/)).

| $m$ | 2 | 3 | 4 |
|---|---|---|---|
| expected makespan | $3/2$ | $17/9$ | $17/8$ |

For $m = 3$, of the 27 equally likely outcomes, 6 have loads $(1, 1, 1)$, 18 have largest load 2, and 3 have largest load 3, so the expectation is $(6 + 36 + 9)/27 = 17/9$.

**Proof sketch of the mixed upper bound on identical machines.** Let $q$ be a mixed equilibrium and let job $j$ use machine $i$. By the equilibrium condition, its expected cost is at most its cost on the machine with the least expected load from the others, so

$$\mathbb{E}[L_i] \le c_j(i, q_{-j}) \le w_j + \frac{W - w_j}{m} \le 2\, \mathrm{OPT}.$$

The same bound holds for a machine that no job uses. Each load $L_i$ is a sum of independent random variables with values in $[0, \mathrm{OPT}]$, one for each job. A Chernoff bound for such sums gives $\Pr[L_i \ge 2c\, \mathrm{OPT}] \le (e/c)^{2c}$, which is below $1/m^2$ for $c = C \ln m / \ln \ln m$ with a suitable constant $C$. A union bound over the $m$ machines and a sum over the tail give $\mathbb{E}[\max_i L_i] = O(\log m / \log \log m) \cdot \mathrm{OPT}$. Czumaj and Vocking sharpen the constant to get $\Gamma^{-1}(m) + \Theta(1)$, and the weighted case needs the ball fusion argument of Koutsoupias, Mavronicolas and Spirakis or a direct analysis.

**Related machines.** The proof of the $\Theta(\log m / \log \log \log m)$ bound for mixed equilibria and of the pure bound on related machines is a long research argument; it is in Czumaj and Vocking (2007), with a shorter account in Chapter 20 of the Algorithmic Game Theory book. The idea is to group the machines by speed and to show that the fast groups cannot all be overloaded at once, because a job on an overloaded slow machine would move to a fast one.

## Consequences

- **The two equilibrium notions differ.** On identical machines the pure bound is a constant and the mixed bound grows with $m$. So in the [load balancing game](/load-balancing-game/), randomness itself causes most of the loss. This also shows that the [smoothness framework](/smoothness-framework/) cannot apply to the makespan: a smoothness bound would be the same for pure and mixed equilibria.
- **Local search.** A pure equilibrium on identical machines is a local optimum for the moves of one job. Theorem 1 is the bound $2 - 2/(m + 1)$ on such local optima, proved by Finn and Horowitz (1979) in scheduling. It is close to the bound $2 - 1/m$ of [list scheduling](/list-scheduling/) ([list scheduling bound](/list-scheduling-bound/)) and worse than the $4/3 - 1/(3m)$ of [longest processing time first](/lpt-bound/), which also ends in an equilibrium.
- **Price of stability.** The best pure equilibrium is optimal in every environment, so the [price of stability](/price-of-stability/) is 1, and the whole loss is in the choice of equilibrium.

## Tightness

- Theorem 1 is tight for every $m$, by the instance above.
- The mixed lower bound on identical machines uses only unit jobs, so weights do not change the order of growth.
- Czumaj and Vocking give instances that reach $\Omega(\log m / \log \log \log m)$ for mixed equilibria and $\Omega(\log m / \log \log m)$ for pure equilibria on related machines.
- On unrelated machines the ratio is unbounded already for 2 machines and 2 jobs ([load balancing game](/load-balancing-game/)), so no bound in $m$ alone holds there.

## History

Koutsoupias and Papadimitriou introduced the model and the coordination ratio at STACS 1999. They proved that the ratio is $3/2$ for 2 identical machines and gave the first bounds for $m$ machines, which left a gap. Mavronicolas and Spirakis studied fully mixed equilibria in 2001. In 2002, Koutsoupias, Mavronicolas and Spirakis, and independently Czumaj and Vocking, closed the gap for identical machines at $\Theta(\log m / \log \log m)$, and Czumaj and Vocking proved the tight bound $\Theta(\log m / \log \log \log m)$ for related machines. The paper of Koutsoupias and Papadimitriou is also where the [price of anarchy](/price-of-anarchy/) as a measure began; the name came later, from Papadimitriou in 2001.

## References
