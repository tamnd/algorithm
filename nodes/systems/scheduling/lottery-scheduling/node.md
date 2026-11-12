---
tag: Z4WQ0E
kind: algorithm
slug: lottery-scheduling
name: Lottery scheduling
area: systems/scheduling
level: advanced
summary: A proportional-share scheduler. Each client holds tickets, and each quantum goes to the holder of a ticket drawn at random, so the expected share of each client is its part of the tickets.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {n: the number of lotteries, c: the number of clients}
  time: {worst: O(n c)}
  space: {extra: O(c)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1994
  people: [Carl A. Waldspurger, William E. Weihl]
  note: Waldspurger and Weihl introduced lottery scheduling, with ticket transfers, inflation, currencies and compensation tickets, at the first OSDI in 1994.
prereqs: [cpu-scheduling, round-robin, binomial-distribution, geometric-distribution]
see_also: [stride-scheduling, completely-fair-scheduler, multilevel-queue-scheduling, weighted-fair-queueing, generalized-processor-sharing, alias-method, fenwick-tree, variance]
sources:
  - paper: "Carl A. Waldspurger and William E. Weihl, Lottery Scheduling: Flexible Proportional-Share Resource Management, Proceedings of the First USENIX Symposium on Operating Systems Design and Implementation (OSDI), 1994"
    title: "Lottery Scheduling: Flexible Proportional-Share Resource Management"
    locator: pages 1 to 11 (tickets and lotteries, the binomial and geometric analysis, ticket transfers, inflation, currencies and compensation tickets)
  - paper: "Carl A. Waldspurger, Lottery and Stride Scheduling: Flexible Proportional-Share Resource Management, PhD thesis, MIT, 1995, technical report MIT/LCS/TR-667"
    title: "Lottery and Stride Scheduling: Flexible Proportional-Share Resource Management"
    locator: the chapters on lottery scheduling and its implementation
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 9, Scheduling, Proportional Share (tickets, ticket currency, transfer and inflation, the list walk, and the unfairness of short runs)
---

Lottery scheduling is a proportional-share [CPU scheduling](/cpu-scheduling/) policy in which each client holds a number of tickets, and each time quantum goes to the holder of a ticket drawn uniformly at random. A client with $t_c$ of the $T$ tickets wins each lottery with probability $p_c = t_c / T$, so its expected share of the CPU is exactly $p_c$, and no client with a ticket starves. Tickets are a currency for resource rights: a client can transfer them, a trusted client can inflate them, and a client that gives up the CPU early gets a compensation ticket. The deterministic counterpart is [stride scheduling](/stride-scheduling/).

## In plain words

Each program gets some lottery tickets. More tickets means a bigger part of the processor. Before each short time slot, the scheduler draws one ticket at random, and the program that holds it runs for that slot.

Over many slots, each program gets about its fair part, because the draws are fair. Over a few slots, luck matters: a program can lose several times in a row. A program that waits for another program can hand over its tickets, so the helper runs sooner. A program that stops early, for example to wait for a disk, gets extra tickets for a while, so that its short runs do not cost it its part.

## The problem

The model is one CPU, time in quanta, and a set of $c$ clients that are always ready. Client $i$ holds $t_i \ge 0$ base tickets, and $T = \sum_i t_i > 0$. The goal is proportional share: over $n$ quanta, client $i$ should get about $n t_i / T$ of them, with no starvation and with a cheap way to change the shares at run time. The scheduler does not know the future demands of the clients, and the ticket counts can change at any time.

## The algorithm

```pseudo id=main
LOTTERY-SCHEDULE(C, n)           ▷ C: clients with base tickets t_c; n quanta
L1  for each client c do e_c ← t_c                 ▷ effective tickets
L2  for r ← 1 to n do
L3      T ← the sum of e_c over all clients
L4      w ← a uniform random integer in [0, T)
L5      s ← 0; for each client c in list order do s ← s + e_c; if w < s then stop with c
L6      run c for up to one quantum; let f ∈ (0, 1] be the part of the quantum it uses
L7      if f < 1 then e_c ← t_c / f                ▷ a compensation ticket of t_c / f − t_c
L8      else e_c ← t_c
```

The effective tickets $e_c$ can be fractions after line L7. The implementation multiplies them by the least common multiple of their denominators before line L4, so the draw stays exact.

Three more operations act on the tickets between lotteries.

- **Transfer.** A client that blocks on another client, for example on a server in a remote call, moves its tickets to it. The server then runs with the client's priority, and it returns the tickets with the reply. This solves priority inversion in a simple way.
- **Inflation.** A client creates more tickets for itself, or removes some (deflation). Among clients that trust each other, this changes the shares with no message to the others.
- **Currencies.** A user or group gets tickets in the base currency and funds its own currency with them. Its clients hold tickets in that currency, and each draw converts them back to base tickets. Inflation inside a currency changes only the shares inside that group.

## Example

Five clients hold 10, 2, 5, 1 and 2 tickets, so $T = 20$. The draw at line L4 gives $w = 15$. The walk of line L5 sees the running sums 10, 12 and 17. The first sum above 15 is 17, so the third client wins. It holds the numbers 12 to 16, which is 5 of the 20, so it wins each lottery with probability $1/4$.

Compensation: clients A and B hold 400 tickets each. A uses whole quanta, and B blocks for I/O after $1/5$ of each quantum. Without compensation, each wins half the lotteries, so A gets 1 unit of CPU for each $1/5$ unit for B. With line L7, B holds $400 / (1/5) = 2000$ effective tickets after each run, so it wins with probability $5/6$, and its expected CPU per lottery is $(5/6)(1/5) = 1/6$, the same as A's $1/6$. The tests check both ratios on 6000 seeded lotteries.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **The draw is exact.** Each integer of $[0, T)$ belongs to exactly one client, and client $c$ owns $e_c$ of them (after scaling). So client $c$ wins with probability $e_c / T$.
2. **Wins are binomial.** With fixed tickets, the number of wins of client $i$ in $n$ lotteries is [binomial](/binomial-distribution/) $\mathrm{Bin}(n, p)$ with $p = t_i / T$. Its mean is $np$ and its [variance](/variance/) is $np(1 - p)$. So the share is right in expectation, and the standard deviation of the error is $\sqrt{np(1 - p)}$, which grows like $\sqrt{n}$.
3. **Response time is geometric.** The number of lotteries up to and including the next win of client $i$ is [geometric](/geometric-distribution/) with mean $1/p$ and variance $(1 - p)/p^2$. A client with a ticket never starves: it waits more than $m$ lotteries with probability $(1 - p)^m$.
4. **Compensation keeps the share.** If client $i$ always uses the part $f_i$ of its quantum, then its expected CPU per lottery is $t_i / T'$ with $T' = \sum_j t_j / f_j$, which is proportional to its base tickets.

## Complexity

Line L5 walks the list, so one lottery takes $O(c)$ time, and $n$ lotteries take $O(nc)$. The space is $O(c)$. Keeping the clients with the most tickets near the front of the list shortens the walk. A tree of partial sums, such as a [Fenwick tree](/fenwick-tree/), finds the winner in $O(\log c)$ and updates a ticket count in $O(\log c)$. The [alias method](/alias-method/) gives $O(1)$ draws, but each change of tickets costs $O(c)$, so it does not suit tickets that change often.

## Properties

- **Randomized and online.** A client's share is correct in expectation from the first lottery; it does not depend on the past.
- **No starvation.** Each client with a ticket wins each lottery with a probability of at least $1/T$.
- **Proportional, with $O(\sqrt{n})$ error.** The absolute error of a share after $n$ quanta is about $\sqrt{np(1 - p)}$, so the relative error falls like $1/\sqrt{n}$ but is large over short times. [Stride scheduling](/stride-scheduling/) reduces the error to a constant.
- **Simple to change.** A new client, a removed client or new ticket counts take effect at the next lottery. No state such as a pass value must be fixed up.
- **Modular.** Currencies isolate groups: inflation inside one group does not change the share of another group.

## Variants and improvements

- **Stride scheduling.** The deterministic version: each client runs in turn by its pass value, with an error of less than one quantum between two clients. See [stride scheduling](/stride-scheduling/).
- **Other resources.** The paper also applies tickets to mutexes (the lock goes to a waiter by lottery, funded by the waiters' tickets) and to memory (the victim of a page eviction is drawn by inverse lottery, with probability that rises as the tickets fall).
- **Fair share in kernels.** The [Completely Fair Scheduler](/completely-fair-scheduler/) of Linux uses weights in the role of tickets and a virtual runtime in the role of the pass, with no randomness.
- **Networks.** [Weighted fair queueing](/weighted-fair-queueing/) gives the same proportional shares to flows on a link, with a deterministic order.

## When to use it

Use lottery scheduling when the shares must change often and cheaply, when clients join and leave all the time, or when the state per client must be very small, for example to divide a resource among virtual machines or users. It is also a good teaching tool, because the expected share is easy to prove. Do not use it when a client needs a tight bound on its share over short intervals, or a bound on its response time: the variance of the number of wins grows with $n$, and a long run of losses has a small but positive probability. Use stride scheduling or a virtual-time scheduler for those.

## Pitfalls

- **A biased draw.** Computing the winner as `random() * T` with floating point, or as a large random number modulo $T$, gives a small bias. Use an exact uniform integer in $[0, T)$ at line L4, as `randrange` does.
- **Rounding the compensation.** Rounding $t_c / f$ down to an integer at line L7 loses part of the compensation for small $f$. Keep the exact fraction, or use a finer ticket unit.
- **A stale total.** If line L3 uses a cached total and a ticket count changed, the walk at line L5 can run off the end of the list. Update the total with every change.
- **Expecting fairness over short times.** Two clients with equal tickets can differ by many quanta in a short run. The guarantee is in expectation and with an error of order $\sqrt{n}$.
- **Inflation between clients that do not trust each other.** Any client that can inflate its tickets can take the whole CPU. Allow inflation only inside a currency, so the damage stays in one group.

## Implementations

## History

Waldspurger and Weihl presented lottery scheduling at the first Symposium on Operating Systems Design and Implementation in 1994. They implemented it in the Mach 3.0 microkernel, gave the binomial and geometric analysis, and introduced ticket transfers, inflation, currencies and compensation tickets. In 1995 they gave the deterministic version, stride scheduling, and Waldspurger's PhD thesis at MIT treated both. Waldspurger later used ticket-based shares to manage memory in the VMware ESX Server hypervisor.

## References
