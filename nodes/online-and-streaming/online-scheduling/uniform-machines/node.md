---
tag: JWCGE2
kind: definition
slug: uniform-machines
name: Uniform machines
aliases:
- related machines
- Q environment
- uniformly related machines
area: online-and-streaming/online-scheduling
level: intro
summary: Machines with fixed speeds, where a job takes its work divided by the speed. Online, least load is unbounded, greedy is Theta(log m), and a constant ratio needs a guess of the optimum.
prereqs: [identical-machines, graham-three-field-notation]
see_also: [identical-machines, unrelated-machines, restricted-assignment, uniform-machine-scheduling, online-makespan-minimization, doubling-trick, machine-environments, list-scheduling]
sources:
  - paper: "James Aspnes, Yossi Azar, Amos Fiat, Serge Plotkin and Orli Waarts, On-line routing of virtual circuits with applications to load balancing and machine scheduling, Journal of the ACM 44(3), 1997"
    title: Aspnes, Azar, Fiat, Plotkin and Waarts 1997
    locator: the section on related machines (the greedy rule is Theta(log m) competitive, and the algorithm with a doubling guess of the optimum is 8-competitive)
  - paper: "Leah Epstein, John Noga, Steven Seiden, Jiri Sgall and Gerhard Woeginger, Randomized on-line scheduling on two uniform machines, Journal of Scheduling 4(2), 2001"
    title: Epstein, Noga, Seiden, Sgall and Woeginger 2001
    locator: the deterministic part, the ratio min((2s + 1)/(s + 1), 1 + 1/s) of greedy on two machines with speed ratio s and its optimality
  - paper: "Piotr Berman, Moses Charikar and Marek Karpinski, On-line load balancing for related machines, Journal of Algorithms 35(1), 2000"
    title: Berman, Charikar and Karpinski 2000
    locator: the deterministic algorithm with ratio 3 + 2 sqrt(2) and the lower bound for related machines
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 12 (load balancing), the related machines model
---

Uniform machines, also called related machines, are the machine environment $Q$ of the [three-field notation](/graham-three-field-notation/). Machine $i$ has a speed $s_i > 0$, and a job with work $p_j$ takes $p_j / s_i$ time on it. The offline problem $Q \mid\mid C_{\max}$ has a PTAS; see [uniform machine scheduling](/uniform-machine-scheduling/). Online, speeds change which rule is natural: the rule "give the job to the machine of least load" from [identical machines](/identical-machines/) has no bounded ratio, the rule "give the job to the machine where it ends first" is only $\Theta(\log m)$-competitive, and a constant ratio needs a guess of the optimum.

## Definition

There are $m$ machines with speeds $s_1 \ge s_2 \ge \cdots \ge s_m > 0$. Job $j$ has a work $p_j \ge 0$. If job $j$ runs on machine $i$, it takes time $p_{ij} = p_j / s_i$. A set $A_i$ of jobs on machine $i$, run without idle time, ends at

$$\ell_i = \frac{1}{s_i} \sum_{j \in A_i} p_j ,$$

the *load* of machine $i$ measured in time. The makespan is $\max_i \ell_i$. With all $s_i = 1$ this is the environment $P$. Uniform machines are the special case $p_{ij} = p_j / s_i$ of [unrelated machines](/unrelated-machines/).

**Two lower bounds on the optimum.** For every instance, $\mathrm{OPT} \ge \max_j p_j / s_1$, because the largest job needs at least that time on the fastest machine, and $\mathrm{OPT} \ge \sum_j p_j / \sum_i s_i$, because the machines together do at most $\sum_i s_i$ work per time unit. These bounds can be far from $\mathrm{OPT}$, which is one reason why online algorithms for $Q$ keep a guess of $\mathrm{OPT}$ instead.

**The online rules.** In the $\mathrm{online\text{-}list}$ paradigm, each job is assigned on arrival.

- *Least load* gives job $j$ to a machine with the least $\ell_i$, as in [list scheduling](/list-scheduling/). It ignores the speeds.
- *Greedy*, also called post-greedy, gives job $j$ to a machine with the least $\ell_i + p_j / s_i$: the machine where the job would end first.
- *Assign with a guess* (Aspnes, Azar, Fiat, Plotkin and Waarts 1997) keeps a guess $\Lambda$ of the optimum. It gives job $j$ to the slowest machine $i$ with $\ell_i + p_j / s_i \le 2\Lambda$, and doubles $\Lambda$ when no machine qualifies. This is the [doubling trick](/doubling-trick/), and it gives a ratio of 8.

## Examples and non-examples

**Least load is unbounded.** Take two machines with speeds $s$ and $1$, with $s \ge 2$, and two jobs of work $s$. Least load puts the first job on the fast machine (load 1). For the second job the loads are $1$ and $0$, so it goes to the slow machine and ends at time $s$. The optimum puts both jobs on the fast machine and ends at $2$. The ratio is $s / 2$, which grows without bound with $s$. Greedy compares $1 + 1 = 2$ with $0 + s = s$ and also ends at $2$.

**Greedy on two machines.** Take speeds $2$ and $1$ and the list of works $(1, 2)$. Greedy puts the first job on the fast machine, where it ends at $\frac12$ (instead of $1$ on the slow one). For the second job it compares $\frac12 + 1 = \frac32$ with $0 + 2 = 2$, and again uses the fast machine: the makespan is $\frac32$. The optimum puts the job of work 2 on the fast machine and the job of work 1 on the slow one, and ends at $1$. So the ratio is $\frac32$. For two machines with speed ratio $s \ge 1$, greedy has ratio exactly $\min\{\frac{2s+1}{s+1}, 1 + \frac1s\}$, and no deterministic online algorithm does better (Epstein, Noga, Seiden, Sgall and Woeginger 2001). For $s = 2$ the two terms are $\frac53$ and $\frac32$, so the bound is $\frac32$ and the example reaches it. The bound is largest at $s = \phi = \frac{1 + \sqrt5}2$, where both terms equal $\phi \approx 1.618$.

**Greedy is $m$-competitive at worst.** The proof on the [unrelated machines](/unrelated-machines/) page shows that greedy on unrelated machines has $\mathrm{ALG} \le m \cdot \mathrm{OPT}$, so the same bound holds for $Q$. The true ratio of greedy on $Q$ is $\Theta(\log m)$ (Aspnes et al. 1997), and the speed vectors that reach it have many groups of machines whose speeds differ by constant factors.

**Known bounds for $Q \mid \mathrm{online\text{-}list} \mid C_{\max}$.** These are cited, not proved here.

| bound | value | source |
|---|---|---|
| greedy | $\Theta(\log m)$ | Aspnes et al. 1997 |
| deterministic, with a guess of $\mathrm{OPT}$ | 8 | Aspnes et al. 1997 |
| deterministic, best known | $3 + 2\sqrt2 \approx 5.828$ | Berman, Charikar and Karpinski 2000 |
| lower bound, deterministic | about $2.438$ | Berman, Charikar and Karpinski 2000 |

**Non-examples.**

- If the time of a job on a machine is not $p_j$ divided by a speed of the machine, for example $p_{1,1} = 1, p_{1,2} = 2$ and $p_{2,1} = 2, p_{2,2} = 1$, the machines are [unrelated](/unrelated-machines/). No speeds $s_1, s_2$ fit, because the first job says that machine 1 is faster and the second job says that machine 2 is faster.
- A machine that may not run a job at all is [restricted assignment](/restricted-assignment/), not a machine with speed 0.
- Speed scaling, where the algorithm chooses the speed over time and pays for energy, is a different model; see [online speed scaling](/online-speed-scaling/).

## Related definitions

- [Machine environments](/machine-environments/) and [uniform machine scheduling](/uniform-machine-scheduling/): the offline view.
- [Identical machines](/identical-machines/): the case of equal speeds.
- [Unrelated machines](/unrelated-machines/): the general case, where the online ratio is $\Theta(\log m)$.
- [Online makespan minimization](/online-makespan-minimization/): the problem on identical machines.
- [Doubling trick](/doubling-trick/): the technique behind the constant ratios for $Q$.

## References
