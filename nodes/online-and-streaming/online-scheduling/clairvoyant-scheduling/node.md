---
tag: NHAKJX
kind: definition
slug: clairvoyant-scheduling
name: Clairvoyant scheduling
aliases:
- non-clairvoyant scheduling
- nclv
- clairvoyance
area: online-and-streaming/online-scheduling
level: advanced
summary: "Whether the scheduler knows job processing times on arrival; non-clairvoyant schedulers do not. For flow time this changes the best deterministic ratio from 1 to a power of n."
prereqs: [release-time, online-algorithm]
see_also: [release-time, graham-three-field-notation, non-clairvoyant-flow-time-minimization, srpt, srpt-optimality, online-flow-time-minimization, online-total-completion-time, round-robin]
sources:
  - paper: "Rajeev Motwani, Steven Phillips and Eric Torng, Non-clairvoyant scheduling, Theoretical Computer Science 130(1), 1994"
    title: Motwani, Phillips and Torng 1994
    locator: the deterministic lower bound for non-clairvoyant flow time, and the analysis of round robin for total completion time with all jobs present at time 0 (SODA 1993 version)
  - paper: "Bala Kalyanasundaram and Kirk Pruhs, Speed is as powerful as clairvoyance, Journal of the ACM 47(4), 2000"
    title: Kalyanasundaram and Pruhs 2000
    locator: the analysis of shortest elapsed time first with speed 1 + epsilon for non-clairvoyant flow time
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), the definition of the paradigm online-time-nclv and the section on non-clairvoyant flow time
---

A scheduler is *clairvoyant* if it learns the processing time $p_j$ of a job when the job arrives, and *non-clairvoyant* if it learns $p_j$ only when the job ends. In the [three-field notation](/graham-three-field-notation/) the second case is the paradigm $\mathrm{online\text{-}time\text{-}nclv}$. Clairvoyance is a property of the information, not of the jobs: the same instance can be scheduled with or without it. For some objectives it changes little, for example makespan over time, and for others it changes a great deal, for example total flow time on one machine, where it is the difference between the exact optimum and a ratio that grows with $n$.

## Definition

Jobs arrive over time, job $j$ at its [release time](/release-time/) $r_j$.

- A *clairvoyant* online algorithm knows $r_j$, $p_j$ and the other data of job $j$ (weight, deadline) at time $r_j$.
- A *non-clairvoyant* online algorithm knows at time $t$ which jobs have $r_j \le t$, which of them have ended, and how much work each has received. It learns $p_j$ only at the time when job $j$ has received $p_j$ units of work and ends.

In both models the [offline optimum](/offline-optimum/) knows everything in advance. The models only make sense over time: if a non-clairvoyant algorithm had to place jobs one by one in a list, the ratio of every algorithm for makespan would be $m$ (see the non-examples on the [notation page](/graham-three-field-notation/)), so the list model says nothing.

**What a non-clairvoyant algorithm can use.** Its decisions at time $t$ depend only on the release times and on the *elapsed* work of each job. Typical rules are:

| rule | runs at each time |
|---|---|
| [round robin](/round-robin/) (processor sharing) | every released unfinished job, at rate $\frac1k$ each when there are $k$ of them |
| shortest elapsed time first (SETF) | the jobs that have received the least work so far |
| multilevel feedback | a job in the lowest of a set of queues, where a job moves to the next queue after each doubling of its elapsed work |

## Examples and non-examples

**Makespan over time.** For $P \mid \mathrm{online\text{-}time\text{-}nclv} \mid C_{\max}$, every rule that never idles is strictly $2$-competitive; the proof on the [release time page](/release-time/) uses no sizes. A clairvoyant algorithm does better, with ratio $\frac32$ (Chen and Vestjens, cited there). So clairvoyance gives a constant factor here.

**Total completion time with all jobs at time $0$.** Take one machine and $n$ jobs with $r_j = 0$ and sizes $p_1 \le p_2 \le \cdots \le p_n$. A clairvoyant algorithm runs them in this order (shortest first), which is optimal, with cost $\mathrm{OPT} = \sum_j (n - j + 1)\, p_j$. Round robin needs no sizes. Under round robin, job $j$ ends after every smaller job has ended and after the $n - j + 1$ jobs that remain have each received $p_j$, so

$$C_j = \sum_{i < j} p_i + (n - j + 1)\, p_j, \qquad \sum_j C_j = \sum_j (2n - 2j + 1)\, p_j .$$

Each coefficient is less than twice the coefficient $n - j + 1$ of $\mathrm{OPT}$, so round robin is strictly $2$-competitive here, without knowing any size. For two jobs of sizes $1$ and $3$: round robin ends them at $2$ and $4$, cost $6$; the optimum ends them at $1$ and $4$, cost $5$.

**Total flow time with arrivals.** On one machine, [SRPT](/srpt/) is clairvoyant and optimal for $\sum_j F_j$ ([SRPT optimality](/srpt-optimality/)). Every deterministic non-clairvoyant algorithm has ratio $\Omega(n^{1/3})$ (Motwani, Phillips and Torng 1994, cited). Randomized multilevel feedback is $O(\log n)$-competitive against an oblivious adversary, and SETF with speed $1 + \varepsilon$ is $O(1 + \frac1\varepsilon)$-competitive (Kalyanasundaram and Pruhs 2000, cited). See [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).

**Non-examples.**

- A scheduler that knows only an estimate of $p_j$ is neither model; this is scheduling with predictions or with uncertain sizes.
- Knowing the release times of future jobs is not clairvoyance in this sense. That is lookahead, or the offline model.
- Not knowing the deadline of a job is a different kind of missing information; clairvoyance is about the size.

## Related definitions

- [Release time](/release-time/) and [Graham's three-field notation](/graham-three-field-notation/): the paradigms $\mathrm{online\text{-}time}$ and $\mathrm{online\text{-}time\text{-}nclv}$.
- [SRPT](/srpt/) and [online flow time minimization](/online-flow-time-minimization/): the clairvoyant side.
- [Non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/): the non-clairvoyant side.
- [Online total completion time](/online-total-completion-time/): the objective of the round robin example.

## References
