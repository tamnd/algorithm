---
tag: 0TZ46P
kind: definition
slug: graham-three-field-notation
name: Graham's three-field notation
aliases:
- alpha|beta|gamma scheduling notation
- online three-field notation
area: online-and-streaming/online-scheduling
level: intro
summary: "The notation alpha|beta|gamma for scheduling problems, with the entries online-list, online-time and online-time-nclv that say how jobs arrive in an online problem."
prereqs: [scheduling-notation, online-algorithm, competitive-ratio]
see_also: [scheduling-notation, machine-environments, identical-machines, release-time, clairvoyant-scheduling, preemptive-scheduling, online-makespan-minimization, online-flow-time-minimization]
sources:
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), its introduction, which defines the online paradigms and the entries online-list, online-time and nclv
  - paper: "Jiri Sgall, On-line scheduling, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Sgall 1998, survey chapter
    locator: Section 1 (the taxonomy of online scheduling problems, scheduling jobs one by one and jobs arriving over time, clairvoyant and non-clairvoyant)
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: Section 2, the classification of problems by the fields alpha, beta and gamma
  - paper: "Bo Chen and Arjen P. A. Vestjens, Scheduling on identical machines: how good is LPT in an on-line setting?, Operations Research Letters 21(4), 1997"
    title: Chen and Vestjens 1997
    locator: the online-over-time LPT rule and its ratio 3/2 for makespan with release times
---

Graham's three-field notation writes a scheduling problem as $\alpha \mid \beta \mid \gamma$: the machine environment $\alpha$, the job characteristics $\beta$, and the objective $\gamma$. The [offline notation page](/scheduling-notation/) defines the fields for the classical problems. For an [online](/online-algorithm/) problem, one more entry in $\beta$ says how the jobs become known: $\mathrm{online\text{-}list}$ (one job at a time, in a list), $\mathrm{online\text{-}time}$ (each job at its release time), or $\mathrm{online\text{-}time\text{-}nclv}$ (at its release time, without its processing time). This page defines these entries and shows why the same three fields can name problems with very different [competitive ratios](/competitive-ratio/).

## Definition

**Notation used on the online scheduling pages.** There are $n$ jobs and $m$ machines. The input is a request sequence $\sigma$ of jobs. $\mathrm{ALG}(\sigma)$ is the cost of the online algorithm and $\mathrm{OPT}(\sigma)$ the cost of an optimal offline schedule of the same jobs. An online algorithm for a minimization objective is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$, with $b$ a constant independent of $\sigma$; it is strictly $c$-competitive if this holds with $b = 0$. All upper bounds on these pages are strict.

**The three fields.** $\alpha$ is $1$, $P$, $Q$ or $R$ (one machine, [identical](/identical-machines/), [uniform](/uniform-machines/) or [unrelated](/unrelated-machines/) machines), with an optional number: $Pm$ or $P3$ fixes the number of machines. $\beta$ lists the constraints, such as $r_j$ ([release times](/release-time/)), $\bar d_j$ ([deadlines](/deadline/)), $\mathrm{pmtn}$ ([preemption](/preemptive-scheduling/)) and $M_j$ ([eligible machines](/restricted-assignment/)). $\gamma$ is the objective: the [makespan](/makespan/) $C_{\max}$, the total completion time $\sum C_j$, the total [flow time](/flow-time/) $\sum F_j$ with $F_j = C_j - r_j$, and others. The full tables are on the [offline page](/scheduling-notation/).

**The online entries of $\beta$.** Pruhs, Sgall and Torng (2004) add one of these entries:

| entry | when a job becomes known | what the algorithm must decide |
|---|---|---|
| $\mathrm{online\text{-}list}$ | the jobs come one by one in a list $\sigma = (J_1, J_2, \ldots)$; the time of the schedule plays no role | when $J_j$ is shown, with all its data, the algorithm assigns it (a machine, and the time slots if it matters) before it sees $J_{j+1}$; the choice is final |
| $\mathrm{online\text{-}time}$ | job $J_j$ is unknown until time $r_j$; at $r_j$ all its data are known | at each time $t$ the algorithm decides what runs at $t$, from the jobs with $r_j \le t$; it may let a machine idle, and it may change its plans for the future, but not the past |
| $\mathrm{online\text{-}time\text{-}nclv}$ | as $\mathrm{online\text{-}time}$, but $p_j$ stays unknown until $J_j$ completes | as $\mathrm{online\text{-}time}$, from the release times and the work done so far only |

In both paradigms the number of jobs $n$ is not known in advance, and the algorithm learns that the sequence has ended only when it ends. The word "nclv" is short for [non-clairvoyant](/clairvoyant-scheduling/). The entries combine with the classical ones: $P \mid \mathrm{online\text{-}time}, \mathrm{pmtn} \mid \sum F_j$ is preemptive scheduling of jobs that arrive over time, with the total flow time as the objective. Under $\mathrm{online\text{-}time}$ the release times $r_j$ are part of the model, and some authors leave the entry $r_j$ out.

**Reading rule.** The optimum $\mathrm{OPT}(\sigma)$ is always the offline optimum of the same class without the online entry: the best schedule that knows all of $\sigma$ in advance, and that obeys the same $\alpha$, the same other entries of $\beta$, and the release times when there are any.

## Examples and non-examples

**Examples.**

- $P \mid \mathrm{online\text{-}list} \mid C_{\max}$ is [online makespan minimization](/online-makespan-minimization/). [List scheduling](/list-scheduling/) is strictly $(2 - \frac1m)$-competitive ([Graham's bound](/list-scheduling-competitive-ratio/)). For $m = 2$, three jobs of sizes $1, 1, 2$ force every online algorithm to a ratio of at least $\frac32$, so $P2 \mid \mathrm{online\text{-}list} \mid C_{\max}$ has optimal ratio $\frac32$ ([the lower bound page](/online-makespan-lower-bound/)).
- $P \mid \mathrm{online\text{-}list}, M_j \mid C_{\max}$ is [online restricted assignment](/online-restricted-assignment-load-balancing/), where the optimal deterministic ratio is $\Theta(\log m)$.
- $1 \mid \mathrm{online\text{-}time}, \mathrm{pmtn} \mid \sum F_j$ is solved exactly by [SRPT](/srpt/): the online rule gives the offline optimum, so its ratio is $1$.
- $1 \mid \mathrm{online\text{-}time} \mid C_{\max}$: any rule that never idles while a job waits is optimal. After the last moment $t_0$ at which the machine is idle and a job arrives, all remaining jobs have $r_j \ge t_0$ and run without a gap, so $\mathrm{ALG} = t_0 + \sum p_j$ over these jobs, and every schedule needs at least that. The [release time page](/release-time/) gives the details.

**A worked reading.** $P \mid \mathrm{online\text{-}time\text{-}nclv}, \mathrm{pmtn} \mid \sum F_j$ means: identical machines, jobs that arrive over time, sizes unknown until each job ends, preemption allowed, and total flow time as the objective. This is the setting of [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).

**The paradigm changes the answer.** The two strings $P \mid \mathrm{online\text{-}list} \mid C_{\max}$ and $P \mid \mathrm{online\text{-}time} \mid C_{\max}$ differ only in the online entry. In the first, the best known deterministic ratio for large $m$ is about $1.9201$, and no deterministic algorithm is better than about $1.88$; see [online makespan minimization](/online-makespan-minimization/). In the second, an algorithm can wait and see which jobs arrive, and the rule "when a machine is idle, start the longest waiting job" is $\frac32$-competitive (Chen and Vestjens 1997). These results are cited, not proved here.

**Non-examples.**

- $P \mid \mathrm{online} \mid C_{\max}$ is not a complete class: the word "online" alone does not say whether jobs arrive in a list or over time, and the example above shows that the ratios differ.
- $\mathrm{online\text{-}list}$ with $\mathrm{nclv}$ is not a standard combination. If the algorithm must place a job on a machine before it knows the size, the adversary can give $m^2$ jobs, find a machine with at least $m$ of them, and give those jobs size $1$ and the others size $0$. Then $\mathrm{ALG} \ge m$ while $\mathrm{OPT} = 1$, and every algorithm has $\mathrm{ALG} \le \sum_j p_j \le m \cdot \mathrm{OPT}$. The ratio $m$ says nothing about the algorithm, so non-clairvoyant models are studied over time.
- Online machine minimization does not fit the scheme: its objective is the number of machines, which is the field $\alpha$ itself. Papers describe it in words; see [online machine minimization](/online-machine-minimization/).
- A semi-online class, for example jobs in a list sorted by non-increasing size, is not $\mathrm{online\text{-}list}$: the order is a promise about the future. With that promise, list scheduling is LPT, and its ratio is $\frac43 - \frac1{3m}$ ([LPT bound](/lpt-bound/)).

## Related definitions

- [Three-field notation (offline)](/scheduling-notation/): the full tables of $\alpha$, $\beta$ and $\gamma$.
- [Machine environments](/machine-environments/), and the online view of [identical](/identical-machines/), [uniform](/uniform-machines/) and [unrelated](/unrelated-machines/) machines and of [restricted assignment](/restricted-assignment/).
- [Release time](/release-time/) and [deadline](/deadline/): the time data of a job, and what they mean when jobs arrive over time.
- [Clairvoyant scheduling](/clairvoyant-scheduling/): the difference between $\mathrm{online\text{-}time}$ and $\mathrm{online\text{-}time\text{-}nclv}$.
- [Preemptive scheduling](/preemptive-scheduling/) and [job migration](/job-migration/): the entry $\mathrm{pmtn}$ in the online setting.
- [Competitive ratio](/competitive-ratio/) and [offline optimum](/offline-optimum/): how an online class is measured.

## References
