---
tag: D0YFHB
kind: concept
slug: preemption
name: Preemption
aliases:
- process preemption
- CPU preemption
area: systems/scheduling
level: intro
summary: "The scheduler takes the CPU from a running process before its burst ends, by a timer or an event. It bounds the wait of urgent work, at the cost of switches and shared-data races."
prereqs: [cpu-scheduling]
see_also: [preemptive-scheduling, round-robin, priority-scheduling, srpt, earliest-deadline-first, race-condition, critical-section, coffman-conditions]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.1.3 (preemptive and nonpreemptive scheduling, the four decision points, race conditions and preemptive kernels) and Section 5.1.4 (the dispatcher and dispatch latency)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 6, Section 6.3 (switching between processes, the cooperative approach, the noncooperative approach with a timer interrupt, and saving and restoring context)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.1 (preemptive and nonpreemptive scheduling algorithms and the clock interrupt)
---

Preemption is the act of taking the CPU away from a running process before its CPU burst ends, so that another process can run. The preempted process goes back to the ready queue and later continues where it stopped. A scheduler that may do this is preemptive; one that waits until the running process ends its burst or blocks is nonpreemptive, or cooperative. Preemption is what lets [round robin](/round-robin/) share the CPU in quanta and lets [preemptive priority scheduling](/priority-scheduling/), [SRPT](/srpt/) and [earliest deadline first](/earliest-deadline-first/) serve urgent work at once. It needs a timer interrupt and a context switch, and it lets the kernel stop a process in the middle of an update to shared data.

## In plain words

Picture a shared kitchen with one stove. In one house rule, whoever is cooking keeps the stove until the meal is done. In the other rule, a timer rings every ten minutes, or someone with an urgent meal arrives, and the cook must step aside, set the pot down and wait for another turn.

The second rule is preemption. It keeps one long meal from holding up everyone. It also costs something: each change of cook takes time, and a cook who is stopped in the middle of a step may leave the kitchen in a half-done state that the next cook must not touch.

## The idea

**Where the scheduler can act.** A CPU scheduler can make a decision at four kinds of moments (Silberschatz, Galvin and Gagne, Section 5.1.3):

1. the running process blocks, for example on I/O;
2. the running process is interrupted and goes from running to ready, for example when its quantum expires;
3. a process goes from waiting to ready, for example when its I/O completes;
4. the running process terminates.

At points 1 and 4 the CPU is free, so every scheduler must choose. A scheduler that acts only there is *nonpreemptive*: a process keeps the CPU until it gives it up. A scheduler that may also act at points 2 and 3 is *preemptive*. These decision points are the events of the simulator on [CPU scheduling](/cpu-scheduling/).

**The mechanism.** A cooperative system gets the CPU back only when the process makes a system call or yields. A process in an endless loop then holds the CPU forever, and only a reboot helps. A preemptive system programs a hardware timer to interrupt the CPU at fixed intervals. The interrupt handler enters the kernel, and the scheduler may then save the state of the running process, its registers and program counter, in its process control block, choose another process, and restore the state of that one. This is the context switch, and the time it takes is the *dispatch latency*.

**The cost.** Each switch takes time $s$ during which no process runs. If a scheduler preempts after every quantum $q$, the fraction of time lost is $s/(q + s)$, as on [round robin](/round-robin/). After a switch, the caches and the TLB hold the data of the previous process, so the new process runs slowly for a while; this cost does not appear in $s$ and can be larger.

**The risk.** A process can be preempted between any two instructions. If two processes share data and one is preempted in the middle of an update, the other can see or change an inconsistent state: a [race condition](/race-condition/). Code that updates shared data must be a [critical section](/critical-section/), protected by locks or by disabling interrupts for a short time. The kernel has the same problem with its own data. A *nonpreemptive kernel* does not preempt a process that is running in kernel mode, which makes most kernel data safe on one CPU but delays urgent work. A *preemptive kernel*, such as Linux since version 2.6 with the preemptible-kernel option, allows preemption in kernel mode and protects kernel data with locks.

**What happens to the work done.** In the usual model, *preempt-resume*, the preempted process keeps its progress and later needs only its remaining time. In *preempt-repeat*, the work done is lost and the process must start its burst again, as with a restartable transaction or a computation without checkpoints. Preempt-repeat wastes CPU time, so a preemptive policy that is good under preempt-resume can be bad under preempt-repeat.

**Preemption on this page and on the theory page.** This page is about the operating-systems mechanism: timer interrupts, context switches with a cost, kernel preemption and the races that preemption creates. The page [preemptive scheduling](/preemptive-scheduling/) is about the model of scheduling theory, written $\mathrm{pmtn}$ in the [three-field notation](/graham-three-field-notation/), where a job may be interrupted any number of times at no cost and resumed later, possibly on another machine. That model is preempt-resume with $s = 0$. It is the setting of results such as the optimality of [SRPT](/srpt-optimality/) and the bounds for preemptive makespan scheduling.

**When preemption helps.** Preemption helps when urgent or short work arrives while other work runs.

- It bounds the response time of high-priority work: with preemption at arrival, the highest-priority process waits at most about two switch times, without it up to one whole burst of another process.
- It makes some objectives easy. With arrivals, the total flow time on one machine is minimized by the preemptive rule SRPT, but without preemption the problem $1 \mid r_j \mid \sum C_j$ is strongly NP-hard.
- It does not help when all processes are present from the start and the bursts are known: by the [optimality of SJF](/sjf-optimality/), no preemptive schedule has a smaller mean waiting time than shortest-job-first.

**Resource preemption.** The word also applies to resources other than the CPU. One of the four [Coffman conditions](/coffman-conditions/) for [deadlock](/deadlock/) is "no preemption": a resource cannot be taken from the process that holds it. A system that can preempt resources, for example by rolling a process back, can break deadlocks.

## Examples

**Three models on one input.** A process A of priority 2 and burst 6 arrives at time 0, B of priority 1 (the highest) and burst 2 at time 2, and C of priority 3 and burst 3 at time 3. The scheduler always picks the ready process of highest priority.

| model | schedule | completions A, B, C | response of B | last completion |
|---|---|---|---|---|
| nonpreemptive | A $[0,6)$, B $[6,8)$, C $[8,11)$ | 6, 8, 11 | 4 | 11 |
| preempt-resume | A $[0,2)$, B $[2,4)$, A $[4,8)$, C $[8,11)$ | 8, 4, 11 | 0 | 11 |
| preempt-repeat | A $[0,2)$, B $[2,4)$, A $[4,10)$, C $[10,13)$ | 10, 4, 13 | 0 | 13 |

With preemption, B does not wait at all. Under preempt-resume the CPU finishes all work at the same time as without preemption, because the scheduler is [work-conserving](/work-conserving-scheduling/) and the switches are free. Under preempt-repeat, the 2 units that A ran before B arrived are lost, and everything after is 2 units later.

**The same input with a switch cost of 1.** Without preemption there are 3 dispatches and the last process finishes at 14. With preempt-resume there are 4 dispatches, one more because of the preemption, and the last process finishes at 15; B now waits 1 unit, the time of the switch. The gain for B is paid by A and C.

**An endless loop.** Under a cooperative scheduler, a process that runs `while true do nothing` never yields, and no other process runs again. Under a preemptive scheduler with a timer, it uses its quantum and is preempted like any other process.

## Where it is used

- **General-purpose operating systems.** Linux, Windows, macOS and other Unix systems are preemptive. Their schedulers, such as the [multilevel feedback queue](/multilevel-feedback-queue/) and the [completely fair scheduler](/completely-fair-scheduler/), preempt on timer interrupts and on the wakeup of a process of higher priority or smaller virtual run time. Older personal-computer systems, such as Windows 3.x and the classic Mac OS, used cooperative multitasking.
- **Real-time systems.** Preemptive [earliest deadline first](/earliest-deadline-first/) and [rate-monotonic scheduling](/rate-monotonic-scheduling/) need preemption to meet deadlines; their analysis also needs bounds on nonpreemptive regions and on [priority inversion](/priority-inversion/).
- **Cooperative scheduling inside programs.** Coroutines, event loops and many user-level thread libraries switch only at yield points. This avoids most races and the cost of the timer, but one task that does not yield blocks the others.
- **Scheduling theory.** The preemptive model of [preemptive scheduling](/preemptive-scheduling/) and online rules such as [SRPT](/srpt/) assume preempt-resume at zero cost.
- **Other resources.** Network links preempt the service of low-priority traffic only between packets, which is a form of limited preemption, and databases preempt transactions by aborting them, which is preempt-repeat.

## References
