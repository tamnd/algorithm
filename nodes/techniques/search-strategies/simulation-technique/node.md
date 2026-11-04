---
tag: ZHE8XG
kind: technique
slug: simulation-technique
name: Simulation (direct step-by-step)
aliases:
- Simulation
area: techniques/search-strategies
level: intro
summary: Approach to problems that directly mimics the described process step by step in code, without needing a clever formula.
prereqs: [state-space, array, hash-table]
see_also: [josephus-problem, cellular-automaton, event-driven-simulation, time-driven-simulation, cycle-detection, functional-graph, nfa-simulation, brute-force-search]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 1.3, The Josephus Problem (the process, its recurrence and the closed form for every second person)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1, Event-Driven Simulation (time-driven versus event-driven simulation of colliding particles)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 3.1, exercises 6 and 7 (the eventual period of an iterated function and the cycle-finding method of Floyd)
---

Simulation is the technique of solving a problem by running the process that the problem describes, one step at a time, on an explicit copy of its state. The program holds the state, applies the rule of one step to it, and repeats until a stop rule holds, then reads the answer from the final state. Its cost is the number of steps times the cost of one step, so it is correct by construction but fast only when the number of steps is small. When the number of steps is too large, the usual repairs are to skip ahead over a repeated state, to jump between events instead of time ticks, or to replace the run by a formula.

## In plain words

Some problems tell you a story: people stand in a circle and every third one leaves, cells live or die by a rule, balls move and bounce. Simulation means you do not look for a clever trick. You write down the situation, you follow the rules for one step, and you do it again, until the story ends. Then you read the answer.

This is often the safest way to start, because the program does what the text says. It has two dangers. The first is speed: if the story has a billion billion steps, you cannot follow them one by one. Then you look for a moment when the situation repeats, and you jump over the loops. The second is care: you must change everything at the same moment, and you must not read a value that you already changed in the same step.

## When it applies

- The problem gives a process with a precise rule for one step: who moves, what changes, in what order. The answer is a property of the state at the end or at a given time.
- The state fits in memory and one step is cheap to compute from it.
- The number of steps is small enough, often at most about $10^7$ to $10^8$ simple steps. If it is larger, the step rule is deterministic and the set of states is finite, then the run repeats, and a skip ahead over the cycle can make it small.
- No closed form is known, or the closed form is hard to find and easy to get wrong. Even when a formula exists, a direct simulation is the oracle that tests it on small inputs.

## The template

```pseudo id=main
SIMULATE(input, T)
L1  s ← INITIAL(input)                              ▷ hole: what the state holds
L2  seen ← empty map                                ▷ only for a deterministic step on a finite state set
L3  for t ← 0 to T − 1
L4      if DONE(s, t) then return ANSWER(s, t)      ▷ hole: the stop rule
L5      if s ∈ seen then                            ▷ the run is periodic from step seen[s]
L6          λ ← t − seen[s]
L7          repeat (T − t) mod λ times: s ← STEP(s)
L8          return ANSWER(s, T)
L9      seen[s] ← t
L10     s ← STEP(s)                                 ▷ hole: the new state, computed from the old state only
L11 return ANSWER(s, T)
```

The holes are the state of line L1, the stop rule of line L4 and the step of line L10. The state must hold every quantity that the step reads. If the rule depends on the time, for example on the parity of $t$, then that part of the time is part of the state. Line L10 computes the new state from the old one only, so a value written in this step is never read in the same step.

Lines L2 and L5 to L9 are the skip ahead. They are correct only when STEP is a function of the state alone and DONE never holds inside the cycle, for example when the question is the state after a fixed number $T$ of steps. Then the states $s_0, s_1, s_2, \ldots$ are the iterates of a function on a finite set, a path into a cycle in the [functional graph](/functional-graph/) of STEP.

**Claim.** If $s_t = s_{t'}$ with $t' < t$ and $\lambda = t - t'$, then $s_T = s_{t + ((T - t) \bmod \lambda)}$ for each $T \ge t$.

*Proof.* Since $s_{u+1} = \mathrm{STEP}(s_u)$, induction on $i$ gives $s_{t+i} = s_{t'+i}$, that is, $s_{u + \lambda} = s_u$ for each $u \ge t'$. Write $T - t = q\lambda + r$ with $0 \le r < \lambda$. Applying the period $q$ times gives $s_T = s_{t + r}$. $\square$

The first repeat is found at the step $t = \mu + \lambda$, where $\mu$ is the length of the path before the cycle and $\lambda$ the length of the cycle. So the template runs at most $\min(T, \mu + 2\lambda)$ steps instead of $T$, with one table operation for each step. If the states are too large to store, the [cycle detection](/cycle-detection/) methods of [Floyd](/floyd-cycle-detection/) and [Brent](/brent-cycle-detection/) find $\mu$ and $\lambda$ with a constant number of stored states.

## Classic examples

- **The [Josephus problem](/josephus-problem/).** People $1$ to $n$ stand in a circle, and counting goes round so that each $k$-th person leaves. With $n = 7$ and $k = 3$, a direct simulation on a [circular linked list](/circular-linked-list/) gives this run:

| round | circle before the round, from the first person counted | leaves |
| --- | --- | --- |
| 1 | 1 2 3 4 5 6 7 | 3 |
| 2 | 4 5 6 7 1 2 | 6 |
| 3 | 7 1 2 4 5 | 2 |
| 4 | 4 5 7 1 | 7 |
| 5 | 1 4 5 | 5 |
| 6 | 1 4 | 1 |

The survivor is 4. The list simulation makes $(n - 1)(k - 1)$ moves of the pointer, so it costs $O(nk)$. An [order-statistic tree](/order-statistic-tree/) finds each next person by rank and costs $O(n \log n)$ for the whole order of leaving. If only the survivor is needed, the recurrence $J(1) = 1$, $J(m) = ((J(m - 1) + k - 1) \bmod m) + 1$, which follows from renumbering the circle after the first person leaves, costs $O(n)$. It gives $1, 2, 2, 1, 4, 1, 4$ for $m = 1$ to $7$, the same survivor. For the original story with $n = 41$ and $k = 3$, the survivor is 31.
- **A [cellular automaton](/cellular-automaton/).** In the Game of Life, a cell is born with exactly 3 live neighbours and survives with 2 or 3. One step reads the old grid and writes a new grid. The blinker, the three live cells $(2,1), (2,2), (2,3)$, becomes $(1,2), (2,2), (3,2)$ and then returns, so it has period 2.
- **[Time-driven](/time-driven-simulation/) and [event-driven simulation](/event-driven-simulation/).** A time-driven simulation of moving particles advances all of them by a fixed $\Delta t$ and then checks for overlaps. An event-driven simulation keeps the predicted collisions in an [event queue](/event-queue/), a [priority queue](/priority-queue/) on time, and jumps from one event to the next. The second does work in proportion to the number of events, not the number of ticks, and it does not miss a collision between two ticks. See [collision prediction and resolution](/collision-prediction-and-resolution/).
- **[NFA simulation](/nfa-simulation/).** The state of the run of a nondeterministic automaton is the set of its states that the input read so far can reach. The step maps this set and the next symbol to the next set. The run takes $O(nm)$ time for a text of length $n$ and an automaton with $m$ states and $O(m)$ transitions, such as the automaton of Thompson's construction, without building the deterministic automaton.
- **Skip ahead on an iterated function.** Let $f(x) = (x^2 + 1) \bmod 255$ and $x_0 = 3$. The run is $3, 10, 101, 2, 5, 26, 167, 95$, and then $f(95) = 101$. So $\mu = 2$ and $\lambda = 6$. For $T = 10^{18}$, the claim gives $x_T = x_{2 + ((10^{18} - 2) \bmod 6)} = x_4 = 5$, after 8 steps instead of $10^{18}$.

## Variations

- **Event-driven instead of time-driven.** When most ticks change nothing, store the next times at which something happens and jump there. The step becomes "remove the earliest event and process it", and the cost depends on the number of events.
- **Skip ahead by a cycle.** The template above. It needs the full state as the key and a deterministic step.
- **Doubling.** If the step is a fixed function on a set of $N$ states, a table of $f^{2^j}$ for $j < \log_2 T$ gives $f^T(x)$ for each start $x$ in $O(\log T)$ lookups after $O(N \log T)$ preprocessing. This is [binary lifting](/binary-lifting/).
- **Linear steps.** If the step is a linear map on a vector of numbers, $T$ steps are the matrix power $A^T$, which [matrix exponentiation](/matrix-exponentiation/) computes with $O(\log T)$ products.
- **A better data structure for the step.** Keep the process but make each step cheap: an order-statistic tree for the Josephus circle, a priority queue for events, a set of only the live cells for a sparse grid.
- **Simulation as an oracle.** Run the slow simulation on small inputs and compare it with a formula or a fast algorithm. This is the use of simulation in tests, in the same way as [brute-force search](/brute-force-search/).

## Pitfalls

- **Updating in place.** If the Game of Life step writes into the grid that it reads, in row-major order, the blinker $(2,1), (2,2), (2,3)$ becomes the four cells $(1,2), (1,3), (2,1), (2,3)$ instead of the vertical line. Read from the old state and write a new one, or swap two buffers.
- **Too many steps.** A run with $T = 10^{18}$ steps never ends, even if each step is fast. Estimate the number of steps before writing the code, and plan a skip ahead or a formula.
- **A state that is not complete.** The skip ahead compares states. If the step also depends on the time, a counter, a direction or a random generator, and the key leaves it out, two equal keys do not give equal futures, and the jump is wrong.
- **Off by one in the rule.** The text says whether the counting starts at the person who just left or at the next one, whether time starts at 0 or 1, and whether the answer is wanted before or after the last step. Check each on a hand example such as the table above.
- **Ties and order of events.** When two events have the same time, the rule must say which is first, or that they happen together. A priority queue alone breaks ties in an arbitrary order.
- **Fixed time steps that miss events.** In a time-driven simulation, two fast particles can cross each other between two ticks, and no overlap is seen at either tick. A smaller $\Delta t$ costs more, and only an event-driven simulation removes the problem.
- **Floating-point drift.** Positions that are updated by adding small increments many times collect rounding errors. Prefer exact integer state where the problem allows it, and compare with a tolerance where it does not.

## Exercises

1. Simulate the Josephus process for $n = 41$ and $k = 3$ and check that the survivor is 31. Then check it with the recurrence.
2. For $k = 2$, prove the closed form $J(2^m + \ell) = 2\ell + 1$ for $0 \le \ell < 2^m$ from Concrete Mathematics, Section 1.3. Use it to show $J(100) = 73$ and check it by simulation.
3. Prove that the order-statistic tree version of the Josephus simulation outputs the whole order of leaving in $O(n \log n)$ time.
4. For $f(x) = (x^2 + 1) \bmod 255$ and $x_0 = 3$, find $x_T$ for $T = 10^{18}$ with Floyd's method in place of the map of line L2, and check that both give 5.
5. Show that the first repeat of the template is found at step $\mu + \lambda$, and that Floyd's method finds a meeting point after at most $\mu + \lambda$ steps of the slow pointer.
6. Explain with the blinker why an in-place update of the Game of Life depends on the order in which the cells are visited, and show that two buffers remove this dependence.

## References
