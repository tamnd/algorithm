---
tag: TDMAY5
kind: problem
slug: pinwheel-scheduling
name: Pinwheel scheduling
aliases:
- pinwheel problem
area: systems/scheduling
level: research
summary: "Given integers a1 to an, give one task each time slot so that task i appears in every window of ai slots. Density at most 5/6 is enough, and density above 1 is impossible."
prereqs: [periodic-task-model, state-space-search]
see_also: [cyclic-executive, time-triggered-scheduling, earliest-deadline-first, pspace, state-space-search, cycle-detection, strongly-connected-components, pigeonhole-principle]
sources:
  - paper: doi:10.1109/HICSS.1989.48075
    title: "Robert Holte, Aloysius Mok, Louis Rosier, Igor Tulchinsky and Donald Varvel, The pinwheel: a real-time scheduling problem, Proceedings of the 22nd Hawaii International Conference on System Sciences, volume 2 (1989), 693-702"
    locator: the definition of the problem, the density condition and the sufficient condition for density at most one half
  - paper: doi:10.1145/3618260.3649757
    title: "Akitoshi Kawamura, Proof of the density threshold conjecture for pinwheel scheduling, STOC 2024, 1816-1819"
    locator: Theorem 1 (density at most 5/6 is enough) and the survey of earlier bounds in the introduction
  - paper: doi:10.1073/pnas.2530214123
    title: "Akitoshi Kawamura, Proof of the density threshold conjecture for pinwheel scheduling, Proceedings of the National Academy of Sciences 123(32) (2026), e2530214123"
    locator: the journal version of the 5/6 theorem
---

Pinwheel scheduling asks for an infinite sequence of tasks, one per time slot, in which task $i$ appears at least once in every window of $a_i$ consecutive slots. Holte, Mok, Rosier, Tulchinsky and Varvel defined it in 1989 for a ground station that must serve several satellites without losing data. The density $\sum_i 1/a_i$ must be at most 1, but that is not enough: $(2, 3, 6)$ has density 1 and no schedule. Kawamura proved in 2024 that density at most $5/6$ is always enough, a bound that is tight.

## In plain words

A gardener has some plants. One plant must get water at least once every 2 days, another at least once every 4 days, and two more at least once every 8 days. The gardener can water only one plant each day. Can the gardener make a plan that never lets a plant go dry, forever?

Here the answer is yes: water the first plant every second day, the second plant every fourth day, and the last two in the gaps. Some lists that look easy have no plan at all. A simple measure helps: add up one over each number. If the sum is above 1, no plan exists. If it is at most five sixths, a plan always exists. Between the two, the answer depends on the numbers.

## Definition

An instance is a list of positive integers $a_1 \le a_2 \le \cdots \le a_n$. A schedule is a map $s$ from the time slots $0, 1, 2, \ldots$ to the tasks $\{1, \ldots, n\}$. It is valid if for each task $i$ and each $t \ge 0$, task $i$ is in $\{s(t), s(t+1), \ldots, s(t + a_i - 1)\}$. The instance is *schedulable* if a valid schedule exists. The *density* is $\rho = \sum_i 1/a_i$.

The task model is a set of unit-time jobs with a distance constraint: the gap between two consecutive runs of task $i$, and the time before its first run, is at most $a_i$. This is stronger than the periodic task $(C_i, T_i) = (1, a_i)$, which only asks for one run in each aligned period and so allows a gap of up to $2a_i - 1$ slots. That periodic set is feasible exactly when $\rho \le 1$, by the test of [earliest deadline first](/earliest-deadline-first/), and pinwheel scheduling is not.

A schedulable instance always has a cyclic schedule. A state of the problem is the vector of the slots left to each task, and there are at most $\prod_i a_i$ states. A valid schedule visits states forever, so by the [pigeonhole principle](/pigeonhole-principle/) it visits one state twice, and the part between the two visits can be repeated.

## Variants

- **General pinwheel.** Task $i$ needs at least $b_i$ slots in every window of $a_i$ slots. The basic problem has $b_i = 1$.
- **Several machines.** Each slot has room for $m$ tasks.
- **Windows scheduling.** The same distance constraint on several channels, studied for broadcast systems.
- **Bamboo garden trimming.** Bamboo $i$ grows at rate $h_i$, and one bamboo is cut each day. The goal is to keep the tallest one short, and good solutions come from pinwheel schedules.

## Examples

**Density 1, schedulable.** For $(2, 4, 8, 8)$, the cycle $1, 2, 1, 3, 1, 2, 1, 4$ works: task 1 every 2 slots, task 2 every 4, tasks 3 and 4 every 8.

**A tight instance.** For $(3, 4, 5, 8)$, with $\rho = 0.908\ldots$, Kawamura gives this cycle of length 8.

| slot mod 8 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| task | 1 | 2 | 3 | 1 | 4 | 2 | 1 | 3 |

The gaps of task 1 are 3, 3 and 2, of task 2 are 4 and 4, of task 3 are 5 and 3, and task 4 has a gap of 8. If any of the four numbers is made smaller by 1, no schedule exists. The same holds for $(3, 3, 3)$ and $(2, 4, 8, 8)$.

**Density 1, not schedulable.** $(2, 3, m)$ has no schedule for any $m$. Task 1 needs one of any two neighbouring slots, so both neighbours of a slot that is not task 1 hold task 1. Task 3 must run at some slot $t \ge 1$. Then slots $t - 1$ and $t + 1$ hold task 1, and the window $\{t - 1, t, t + 1\}$ of 3 slots has no task 2. So no schedule exists. For $m = 6$ the density is $1/2 + 1/3 + 1/6 = 1$.

## Known algorithms

The exact test below searches the graph of states. It is the algorithm of the implementation.

```pseudo id=main
PINWHEEL-DECIDE(a1, ..., an)
L1  if 1/a1 + ... + 1/an > 1 then return "not schedulable"
L2  s0 ← (a1, ..., an)                    ▷ entry i: slots left before task i must run
L3  explore all states that can be reached from s0
L4      a move gives the slot to task j: entry j becomes aj, each other entry drops by 1 and must stay ≥ 1
L5  repeat: remove each state that has no move to a state that is not removed
L6  if s0 was removed then return "not schedulable"
L7  walk from s0 along moves to states that are not removed, until a state repeats
L8  return the moves of the repeated part as a cyclic schedule
```

Line L5 keeps exactly the states from which moves can go on forever: a state that is not removed has a move to another such state, and a removed state leads only to dead ends within a bounded number of moves. So the answer is exact. With a queue of states whose number of live moves drops to 0, lines L3 to L5 take $O(n S)$ time and space for $S \le \prod_i a_i$ reachable states. The time is exponential in $n$, even when the numbers are written in unary.

Faster algorithms are known only for sufficient conditions.

- **Rounding to powers of 2.** Replace each $a_i$ by the largest power of 2 that is at most $a_i$. This at most doubles the density, and an instance of powers of 2 with density at most 1 has a simple schedule, as each number divides the next. So $\rho \le 1/2$ is enough, as Holte et al. showed.
- **Better reductions.** Chan and Chin raised the threshold to $2/3$ and then to $0.7$, and Fishburn and Lagarias to $0.75$, by rounding to more clever sets of numbers.
- **The 5/6 theorem.** Kawamura proved in 2024 that every instance with $\rho \le 5/6$ is schedulable. Together with the family $(2, 3, m)$, this settles the best threshold for density.

## Bounds

- **Necessary.** $\rho \le 1$, since task $i$ uses at least $1/a_i$ of all slots in the long run.
- **Sufficient.** $\rho \le 5/6$. This is tight: $(2, 3, m)$ has density $5/6 + 1/m$, which is as close to $5/6$ as one likes, and it is never schedulable. Chan and Chin conjectured this threshold in 1993.
- **Two distinct numbers.** An instance with only two distinct values among the $a_i$ is schedulable whenever $\rho \le 1$.
- **Schedule length.** A schedulable instance has a cyclic schedule of length at most $\prod_i a_i$, the number of states.
- **Complexity.** The decision problem is in [PSPACE](/pspace/): a nondeterministic walk through the states needs only the current state and a counter. No polynomial algorithm is known, and the exact complexity is not settled.

## Reductions

- **To a graph problem.** The instance is schedulable if and only if the start state can reach a cycle of the state graph. This is a [cycle detection](/cycle-detection/) or [strongly connected components](/strongly-connected-components/) question on an exponential graph, which is what line L5 solves.
- **From pinwheel to a static table.** A cyclic pinwheel schedule is a table for a [cyclic executive](/cyclic-executive/) whose frames are single slots and whose tasks have unit cost.
- **To and from periodic scheduling.** A pinwheel task $a_i$ is a periodic task with period $a_i$ whose jobs may be released at any time. A schedule for periods that are rounded down to a harmonic set is a valid pinwheel schedule, which is the idea of the sufficient tests.

## Applications

- **Satellite ground stations.** The original motivation: a ground station serves one satellite at a time and must contact satellite $i$ at least once in each window of $a_i$ slots, or its buffer overflows.
- **Polling and broadcast.** A sensor network polls each sensor within its maximum age, and a broadcast channel repeats each item within its maximum wait. Both are pinwheel instances.
- **Time-triggered networks.** Slot tables of [time-triggered](/time-triggered-scheduling/) buses and radio channels with a maximum gap per sender have this form.

## References
