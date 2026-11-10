---
tag: A5D57E
kind: problem
slug: online-machine-minimization
name: Online machine minimization
aliases:
- online machine minimization with deadlines
- online resource minimization
area: online-and-streaming/online-scheduling
level: research
summary: "Jobs with deadlines arrive online, and the algorithm must meet every deadline with as few machines as possible. The best known ratio is O(log log m), where m is the optimal number."
prereqs: [deadline, release-time, job-migration, competitive-ratio]
see_also: [earliest-deadline-first, edf-optimality, least-laxity-first, interval-partitioning, max-flow-problem, bkp-speed-scaling, online-throughput-maximization, real-time-scheduling]
sources:
  - paper: "Cynthia A. Phillips, Clifford Stein, Eric Torng and Joel Wein, Optimal time-critical scheduling via resource augmentation, Algorithmica 32(2), 2002"
    title: Phillips, Stein, Torng and Wein 2002
    locator: the problem with extra machines, the O(log(p_max/p_min)) bound for LLF, and the constant lower bound for every online algorithm (STOC 1997 version)
  - paper: doi:10.1137/17M116032X
    title: "Lin Chen, Nicole Megow and Kevin Schewior, An O(log m)-competitive algorithm for online machine minimization, SIAM Journal on Computing 47(6), 2018"
    locator: the O(log m) algorithm and the O(1) bounds for laminar and agreeable instances (SODA 2016 version)
  - paper: "Lin Chen, Nicole Megow and Kevin Schewior, New results on online resource minimization, arXiv:1407.7998, 2014"
    title: Chen, Megow and Schewior 2014
    locator: the O(log n) algorithm, the Omega(n^(1/3)) lower bound for LLF, the results for agreeable instances, and the lower bound n without preemption
  - paper: doi:10.1145/2935764.2935786
    title: "Lin Chen, Nicole Megow and Kevin Schewior, The power of migration in online machine minimization, SPAA 2016"
    locator: the results without migration, no f(m)-competitive algorithm and the Omega(log n) lower bound
  - paper: doi:10.1016/j.orl.2017.11.013
    title: "Yossi Azar and Sarel Cohen, An improved algorithm for online machine minimization, Operations Research Letters 46(1), 2018"
    locator: pages 128 to 133, the O(log m / log log m)-competitive algorithm
  - paper: "Sungjin Im, Benjamin Moseley, Kirk Pruhs and Clifford Stein, An O(log log m)-competitive algorithm for online machine minimization, IEEE Real-Time Systems Symposium 2017, arXiv:1708.09046"
    title: Im, Moseley, Pruhs and Stein 2017
    locator: pages 343 to 350, the O(log log m)-competitive algorithm
  - paper: "Nikhil R. Devanur, Konstantin Makarychev, Debmalya Panigrahi and Grigory Yaroslavtsev, Online algorithms for machine minimization, arXiv:1403.0486, 2014"
    title: Devanur, Makarychev, Panigrahi and Yaroslavtsev 2014
    locator: the deterministic ratio e for jobs of equal length, optimal for that case
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1), 1974"
    title: Horn 1974
    locator: the flow formulation for preemptive scheduling with release times and deadlines on identical machines
---

Online machine minimization asks for a schedule that meets every [deadline](/deadline/) of jobs that arrive over time, on as few identical machines as possible. The algorithm sees each job only at its [release time](/release-time/), and it may open a new machine at any moment. On one machine, [EDF](/earliest-deadline-first/) is enough, but already on two machines no online rule uses the optimal number. The best known algorithms use $O(\log \log m)$ times the optimal number $m$ of machines, and whether a constant ratio is possible is open.

## In plain words

Tasks come in over time. Each task says how much work it needs and when it must be done. You can rent as many identical workers as you like, and each worker can switch between tasks at any moment. Every task must finish in time, and you want to rent few workers. If you knew all tasks in advance, you could compute the smallest team. Online you do not know which tasks come next. A task that looks relaxed now may later be blocked by a burst of urgent tasks, so you must decide early how much work to do on it. An opponent can always find a burst that hurts the choice you made. The question is how many more workers than the best team you need to be safe.

## Definition

**Input.** A request sequence $\sigma$ of $n$ jobs. Job $j$ has a release time $r_j$, a processing time $p_j > 0$ and a deadline $\bar d_j$, with $p_j \le \bar d_j - r_j$. Its laxity is $\bar d_j - r_j - p_j \ge 0$.

**Online rule.** The model is online-time and [clairvoyant](/clairvoyant-scheduling/): job $j$ and its values $p_j$ and $\bar d_j$ become known at time $r_j$, and not before. At each moment the algorithm decides which released jobs run on which machines, and it may open a new machine at any time. [Preemption](/preemptive-scheduling/) and [migration](/job-migration/) are allowed: a job may stop, and continue later on another machine, but it never runs on two machines at once.

**Feasibility.** The schedule must give each job $p_j$ units of work inside $[r_j, \bar d_j]$.

**Cost.** $\mathrm{ALG}(\sigma)$ is the number of machines that the algorithm ever uses. $\mathrm{OPT}(\sigma)$, written $m$, is the least number of machines on which a feasible schedule exists. An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, and strictly so if $b = 0$. Here the algorithm is deterministic and the adversary may choose each job after it sees the schedule so far.

In the notation of [Graham](/graham-three-field-notation/), the offline feasibility question for fixed $m$ is $P \mid r_j, \mathrm{pmtn}, \bar d_j \mid -$.

## Variants

- **Without migration.** A job stays on the machine where it first ran. Chen, Megow and Schewior (SPAA 2016) show that then no algorithm is $f(m)$-competitive for any function $f$, and that $\Omega(\log n)$ machines can be needed (cited).
- **Without preemption.** A job runs without a break once it starts. Then the ratio can be as large as $n$ (cited in Chen, Megow and Schewior 2014). For jobs of equal length, Devanur, Makarychev, Panigrahi and Yaroslavtsev (2014) give the deterministic ratio $e$ and show that it is optimal (cited).
- **Laminar and agreeable instances.** The windows are laminar if any two of them are disjoint or nested, and agreeable if $r_j < r_k$ implies $\bar d_j \le \bar d_k$. Chen, Megow and Schewior give $O(1)$-competitive algorithms for both (cited).
- **Jobs without laxity.** If $p_j = \bar d_j - r_j$ for all $j$, each job must run during its whole window, and a greedy rule is optimal; see Reductions.
- **Speed instead of machines.** Keep $m$ machines and make them faster. EDF on $m$ machines of speed $2 - \frac1m$ meets all deadlines of every instance feasible on $m$ machines of speed $1$ (Phillips, Stein, Torng and Wein, cited on the [deadline page](/deadline/)). On one machine with a variable speed, minimizing the largest speed is the problem solved by the [BKP algorithm](/bkp-speed-scaling/), which is $e$-competitive for it (cited).

## Examples

**The adversary on two machines.** At time $0$ three jobs arrive.

| job | $r_j$ | $p_j$ | $\bar d_j$ |
|---|---|---|---|
| $x$ | 0 | 1 | 2 |
| $y$ | 0 | 1 | 2 |
| $z$ | 0 | 2 | 4 |

These three jobs fit on one machine: $x$ in $[0, 1]$, $y$ in $[1, 2]$, $z$ in $[2, 4]$. At time $1$ the adversary looks at the work that $z$ has received.

| case at time $1$ | new jobs | an optimal schedule on $2$ machines |
|---|---|---|
| $z$ got less than $1$ unit | $u, v$ with $r = 2$, $p = 2$, $\bar d = 4$ | machine 1 runs $z$ in $[0, 2]$; machine 2 runs $x$, then $y$; $u$ and $v$ run in $[2, 4]$ |
| $z$ got at least $1$ unit | $u', v'$ with $r = 1$, $p = 1$, $\bar d = 2$ | $x$ and $y$ in $[0, 1]$; $u'$ and $v'$ in $[1, 2]$; $z$ in $[2, 4]$ |

In both cases $\mathrm{OPT} = 2$. One machine is not enough: in the first case the window $[0, 4]$ contains $8$ units of work, and in the second the window $[0, 2]$ contains $4$ units. The theorem in Bounds shows that every online algorithm needs a third machine in one of the two cases.

**One machine.** If the input is known to have $\mathrm{OPT} = 1$, EDF on one machine meets all deadlines, because EDF is optimal on one machine with preemption ([EDF optimality](/edf-optimality/)). The trouble starts when the algorithm does not know whether one machine will be enough.

## Known algorithms

| algorithm | machines used | source |
|---|---|---|
| one new machine for each job | $n$; feasible since $p_j \le \bar d_j - r_j$ | trivial |
| [EDF](/earliest-deadline-first/) on one machine, when $\mathrm{OPT} = 1$ | $1$ | [EDF optimality](/edf-optimality/) |
| greedy, for jobs without laxity | $\mathrm{OPT}$ | proved on this page |
| [LLF](/least-laxity-first/), least laxity first | $O(\log(p_{\max}/p_{\min}))$ times $\mathrm{OPT}$ | Phillips, Stein, Torng and Wein 2002, cited |
| Chen, Megow and Schewior | $O(\log n)$ times $\mathrm{OPT}$ | 2014, cited |
| Chen, Megow and Schewior | $O(\log m)$ times $\mathrm{OPT}$; $O(1)$ for laminar and agreeable instances | SODA 2016, SIAM J. Comput. 2018, cited |
| Azar and Cohen | $O(\log m / \log \log m)$ times $\mathrm{OPT}$ | 2018, cited |
| Im, Moseley, Pruhs and Stein | $O(\log \log m)$ times $\mathrm{OPT}$ | RTSS 2017, cited |

LLF alone is not enough in general: Chen, Megow and Schewior (2014) show a lower bound of $\Omega(n^{1/3})$ for it (cited). The $O(\log n)$ algorithm of Chen, Megow and Schewior splits the jobs into loose jobs, with a large laxity compared with $p_j$, and tight jobs, and it schedules the two groups on separate machines (cited).

## Bounds

**Theorem (no online algorithm is exact).** For every deterministic online algorithm there is an instance with $\mathrm{OPT} = 2$ on which the algorithm uses at least $3$ machines. So no deterministic online algorithm is strictly $c$-competitive for $c < \frac32$.

*Proof.* Use the instance of the Examples. Suppose that the algorithm uses at most $2$ machines on both final instances. Up to time $1$ the two instances look the same, so the schedule up to time $1$ is the same, and it does at most $2$ units of work.

If $z$ got less than $1$ unit by time $1$, the jobs $u$ and $v$ need both machines during all of $[2, 4]$, so $z$ must finish by time $2$. It needs more than $1$ unit of work in $[1, 2]$, but a job runs on at most one machine at a time, so it gets at most $1$ unit there. A deadline is missed.

If $z$ got at least $1$ unit, then $x$ and $y$ together got at most $1$ unit, so they need at least $1$ more unit in $[1, 2]$. The jobs $u'$ and $v'$ need both machines during all of $[1, 2]$, so $2$ machines must do at least $3$ units of work in an interval of length $1$. A deadline is missed.

So on one of the instances the algorithm uses at least $3$ machines, while $\mathrm{OPT} = 2$. A strictly $c$-competitive algorithm with $c < \frac32$ would use at most $2c < 3$ machines there. $\square$

| question | lower bound | upper bound | status |
|---|---|---|---|
| deterministic, with migration, strict ratio | $\frac32$ (proved here); a constant (Phillips et al., cited) | $O(\log \log m)$ | upper bound cited |
| without migration | no $f(m)$ bound; $\Omega(\log n)$ | | cited |
| jobs without laxity | $1$ | $1$ | proved here |

The proved lower bound uses $\mathrm{OPT} = 2$ and does not grow with $m$. Between a constant and $O(\log \log m)$, the right order of the ratio is open.

## Reductions

**The offline optimum is a flow problem.** Let $e_0 < e_1 < \cdots < e_K$ be the distinct values among all $r_j$ and $\bar d_j$, and let $I_k = [e_{k-1}, e_k]$. Build a network with an arc from the source to each job $j$ of capacity $p_j$, an arc from job $j$ to each $I_k \subseteq [r_j, \bar d_j]$ of capacity $|I_k|$, and an arc from each $I_k$ to the sink of capacity $m |I_k|$. Horn (1974) shows that the jobs fit on $m$ machines with preemption and migration if and only if the [maximum flow](/max-flow-problem/) is $\sum_j p_j$ (cited). Inside one interval, amounts of at most $|I_k|$ per job and at most $m |I_k|$ in total are scheduled by McNaughton's wrap-around rule. Since $1 \le \mathrm{OPT} \le n$, a binary search over $m$ finds the optimum.

**A simple lower bound.** For every interval $[a, b]$, $\mathrm{OPT} \ge \frac1{b - a} \sum_{j :\, [r_j, \bar d_j] \subseteq [a, b]} p_j$, because these jobs must do all their work inside $[a, b]$. The Examples use this bound.

**Jobs without laxity are interval partitioning.** If $p_j = \bar d_j - r_j$ for every $j$, a feasible schedule must run job $j$ at every moment of $[r_j, \bar d_j)$. So $\mathrm{OPT}$ is at least the largest number $k$ of windows that contain a common point. The greedy rule starts job $j$ at time $r_j$ on an open machine that is idle, and opens a new machine only if every open machine is busy. If it opens a machine at time $r_j$, every open machine runs a job whose window contains $r_j$, and so does job $j$, so the number of machines is at most $k$. Hence greedy uses exactly $\mathrm{OPT}$ machines, online and without migration. This is [interval partitioning](/interval-partitioning/) with intervals given in order of their left ends.

**Machines and speed.** Merge the $m$ machines of a feasible schedule into one machine of speed $m$: in each short slot, it runs the pieces of the $m$ machines one after the other. So the least maximum speed $S^*$ of one machine with variable speed satisfies $S^* \le \mathrm{OPT}$. The bound can be loose, because one fast machine may run a single job faster than speed $1$, and $m$ machines cannot. This links the problem to [speed scaling](/online-speed-scaling/).

## Applications

- Real-time systems that must meet hard deadlines and must decide how many processors to switch on ([real-time scheduling](/real-time-scheduling/)).
- Renting servers in a cloud for jobs with deadlines, where each server costs money for the whole period.
- Planning staff or vehicles for tasks with time windows that are announced over time.

## References
