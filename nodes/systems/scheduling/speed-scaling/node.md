---
tag: JYGQJB
kind: problem
slug: speed-scaling
name: Speed scaling
aliases:
- Energy-aware scheduling with speed scaling
- speed scaling with deadlines
- minimum energy scheduling with deadlines
area: systems/scheduling
level: advanced
summary: Choose the speed of a processor over time so that every job meets its deadline and the energy, the integral of the power s^alpha with alpha > 1, is as small as possible.
prereqs: [deadline, convex-function]
see_also: [yds-algorithm, online-speed-scaling, avr, optimal-available, bkp-speed-scaling, jensens-inequality, earliest-deadline-first, kkt-conditions]
sources:
  - paper: "F. Frances Yao, Alan J. Demers and Scott Shenker, A Scheduling Model for Reduced CPU Energy, Proceedings of the 36th Annual Symposium on Foundations of Computer Science (FOCS), 1995"
    title: "A Scheduling Model for Reduced CPU Energy"
    locator: pages 374 to 382 (the model with release times, deadlines, work and a convex power function, the offline optimum and the online algorithms)
  - paper: "Susanne Albers, Energy-Efficient Algorithms, Communications of the ACM 53(5), 2010"
    title: "Energy-Efficient Algorithms"
    locator: pages 86 to 96 (the survey of speed scaling with deadlines, the cube-root rule, flow time and energy, and sleep states)
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed Scaling to Manage Energy and Temperature, Journal of the ACM 54(1), 2007"
    title: "Speed Scaling to Manage Energy and Temperature"
    locator: Article 3 (the convex program for the offline problem, its KKT conditions, and the online algorithm BKP)
---

Speed scaling is the problem of choosing how fast a processor runs over time so that it finishes its work on time with the least energy. In the model of Yao, Demers and Shenker (1995), each job has a release time, a [deadline](/deadline/) and an amount of work, and the processor can run at any speed $s \ge 0$. At speed $s$ it uses power $P(s) = s^\alpha$ for a constant $\alpha > 1$, and the energy is the integral of the power over time. Since $s^\alpha$ is a [convex function](/convex-function/), it is cheaper to run slowly and evenly than fast and in bursts: doing a fixed amount of work in a fixed time costs the least at a constant speed. The offline problem is solved exactly by the [YDS algorithm](/yds-algorithm/), and the version in which jobs arrive over time is [online speed scaling](/online-speed-scaling/).

## In plain words

A processor can run slow and use little power, or fast and use much more. Twice the speed costs more than twice the power, so the same work done fast costs more energy than done slowly.

Each job arrives at some time, has some work, and must be done by its deadline. The task is to choose the speed at every moment so that all jobs are done in time and the total energy is as small as possible.

The best plan avoids bursts. It runs at a steady speed for as long as the deadlines allow, and speeds up only where much work must be done in a short time.

## Definition

**Input.** Jobs $1, \ldots, n$. Job $j$ has a release time $r_j$, a deadline $d_j > r_j$ and a work $w_j > 0$. A constant $\alpha > 1$.

**Schedule.** One processor. At each time $t$ the schedule chooses a speed $s(t) \ge 0$ and at most one job to run. A job that runs for a time set $T_j$ gets $\int_{T_j} s(t)\,dt$ units of work. Jobs can be preempted and resumed at no cost. The schedule is *feasible* if each job $j$ gets exactly $w_j$ units of work during $[r_j, d_j]$.

**Goal.** Minimize the energy

$$E = \int P(s(t))\,dt, \qquad P(s) = s^\alpha.$$

**Constant speed is best.** Suppose a processor must do $w$ units of work during a time of length $L$, and runs at speed $s(t)$ with $\int_0^L s(t)\,dt = w$. By [Jensen's inequality](/jensens-inequality/) for the convex function $s^\alpha$,

$$\frac{1}{L} \int_0^L s(t)^\alpha\,dt \ \ge\ \left( \frac{1}{L} \int_0^L s(t)\,dt \right)^\alpha = \left( \frac{w}{L} \right)^\alpha,$$

so the energy is at least $L (w/L)^\alpha = w^\alpha / L^{\alpha - 1}$, with equality for the constant speed $w/L$. Because $\alpha > 1$, this bound also falls as $L$ grows: it is best to spread the work over all the time that is allowed.

**Why $s^\alpha$.** In CMOS circuits the dynamic power is about $C V^2 f$ for a capacitance $C$, a voltage $V$ and a clock rate $f$, and the clock rate that a circuit can sustain grows about linearly with the voltage. So the power grows about as the cube of the speed. This is the *cube-root rule*, and it gives $\alpha = 3$. Analyses keep $\alpha$ general.

## Variants

- **Online.** Each job becomes known only at its release time. This is [online speed scaling](/online-speed-scaling/), analyzed by the [competitive ratio](/competitive-ratio/) against the offline optimum.
- **Maximum speed.** The speed is at most $s_{\max}$. Then some instances have no feasible schedule, and an online algorithm may have to drop jobs, which leads to throughput goals.
- **Discrete speeds.** The processor offers only a few speeds, as real processors do. The best schedule then mixes the two allowed speeds next to each ideal speed.
- **Static power and sleep states.** The power is $s^\alpha + \beta$ with a static part $\beta > 0$, and the processor can sleep at a cost to wake up. Running too slowly then wastes static energy, and there is a *critical speed* below which it is better to run faster and sleep.
- **Flow time plus energy.** Jobs have no deadlines, and the goal is the total time that jobs wait in the system plus the energy. This models interactive systems.
- **Several processors.** Jobs run on $m$ processors, each with its own speed.
- **Temperature.** Minimize the peak temperature of the processor, a smoothed function of the power over time.

## Examples

**One job.** A job of work 4 has the window $[0, 8]$, and $\alpha = 3$. At the constant speed $4/8 = 1/2$ it uses energy $8 \cdot (1/2)^3 = 1$. At speed 1 for 4 time units, and then idle, it uses $4 \cdot 1^3 = 4$, four times as much. At speed 2 for 2 time units it uses $2 \cdot 2^3 = 16$.

**Three jobs.** Jobs with windows and works $(0, 2, 4)$, $(0, 8, 4)$ and $(4, 6, 3)$, with $\alpha = 3$. The first job must run at speed at least 2 during $[0, 2]$, and the third at least $3/2$ during $[4, 6]$. The second job fills the rest of the time at speed 1. This is the optimal schedule found by the [YDS algorithm](/yds-algorithm/), with energy $107/4$. Running every job at its own density $w_j / (d_j - r_j)$ at once, as the online algorithm [AVR](/avr/) does, uses $191/4$.

## Known algorithms

- **[YDS](/yds-algorithm/)** (Yao, Demers and Shenker 1995) solves the offline problem exactly. It repeatedly runs the interval of maximum work per unit of time at that speed by [EDF](/earliest-deadline-first/), removes it and compresses time. A simple version takes $O(n^3)$ time; Li, Yao and Yao gave an $O(n^2 \log n)$ version.
- **[AVR](/avr/)** (Yao, Demers and Shenker 1995) runs at the sum of the densities of the jobs whose windows contain the current time, and uses EDF.
- **[Optimal Available](/optimal-available/)** (Yao, Demers and Shenker 1995) runs, at each arrival, the optimal schedule for the work that is known and left.
- **[BKP](/bkp-speed-scaling/)** (Bansal, Kimbrel and Pruhs 2007) sets the speed from an estimate of the densest interval around the current time, and also bounds the maximum speed.

## Bounds

- **Interval lower bound.** For an interval $I$, let $g(I)$ be the work of the jobs whose windows lie inside $I$, divided by the length of $I$. Every feasible schedule does that work inside $I$, so by the constant speed bound it uses energy at least $|I| \, g(I)^\alpha$ there, and its peak speed is at least $\max_I g(I)$. YDS reaches this peak speed.
- **Offline.** The problem is solved exactly in polynomial time, by YDS.
- **Online.** No online algorithm is optimal. The bounds on the competitive ratio depend on $\alpha$; they are given on the page of [online speed scaling](/online-speed-scaling/).

## Reductions

- **Convex program.** Cut time at all release times and deadlines into elementary intervals $I_1, \ldots, I_m$. Let $x_{ji} \ge 0$ be the work of job $j$ in $I_i$, allowed only if $I_i \subseteq [r_j, d_j]$. Minimize $\sum_i |I_i| \big( \sum_j x_{ji} / |I_i| \big)^\alpha$ subject to $\sum_i x_{ji} = w_j$. Within an elementary interval a constant speed is best, and EDF can order the work, so this convex program is the whole problem. Bansal, Kimbrel and Pruhs used its [KKT conditions](/kkt-conditions/) to characterize the optimum.
- **Feasibility for given speeds.** For a fixed speed function, feasibility is a flow problem between jobs and elementary intervals. By the EDF argument it holds exactly when no interval holds more work than the work the processor can do in it.

## Applications

Speed scaling models dynamic voltage and frequency scaling (DVFS), in which an operating system lowers the clock rate and voltage of a processor when the load is light. It is used in laptops, phones and servers, and in embedded real-time systems in which tasks have deadlines, such as decoding audio and video. The same convexity drives the scheduling of wireless transmissions, where sending the same data more slowly takes less energy, and of data-center servers that trade speed for power.

## References
