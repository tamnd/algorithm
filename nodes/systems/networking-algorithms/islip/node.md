---
tag: QBWMZS
kind: algorithm
slug: islip
name: iSLIP
aliases:
- iterative SLIP
- SLIP scheduling algorithm
area: systems/networking-algorithms
level: advanced
summary: "Crossbar scheduler with round-robin grant and accept pointers that move only on an accepted first-round grant. The pointers spread out, giving 100% throughput under uniform Bernoulli traffic."
solves: [switch-scheduling]
model: word-ram
complexity:
  vars: {n: the number of ports, k: the number of iterations per slot}
  time: {worst: O(k n^2)}
  space: {extra: Θ(n^2)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1999
  people: [Nick McKeown]
  note: McKeown introduced SLIP in his 1995 thesis and published iSLIP, its iterative form, in IEEE/ACM Transactions on Networking in 1999.
prereqs: [switch-scheduling, parallel-iterative-matching]
see_also: [maximal-matching, round-robin, birkhoff-von-neumann-decomposition, maximum-weight-matching, deficit-round-robin, packet-scheduling]
sources:
  - paper: doi:10.1109/90.769767
    title: "Nick McKeown, The iSLIP scheduling algorithm for input-queued switches, IEEE/ACM Transactions on Networking 7(2) (1999), 188-201"
    locator: the RRM and iSLIP algorithms, the 2 x 2 example in which RRM pointers synchronize, the RRM limit near 63% under uniform Bernoulli traffic, the pointer update rule of iSLIP, desynchronization and 100% throughput under uniform i.i.d. Bernoulli traffic, and the iterative form
  - paper: doi:10.1145/161541.161736
    title: "Thomas E. Anderson, Susan S. Owicki, James B. Saxe and Charles P. Thacker, High-speed switch scheduling for local-area networks, ACM Transactions on Computer Systems 11(4) (1993), 319-352"
    locator: PIM, the randomized request, grant and accept scheme that iSLIP makes deterministic
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 13, the sections on PIM and iSLIP
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 19, allocation (separable allocators with round-robin arbiters, iSLIP)
---

iSLIP is a deterministic scheduler for an input-queued crossbar switch. It finds a matching of inputs to outputs in each time slot with the same request, grant and accept steps as [parallel iterative matching](/parallel-iterative-matching/), but each port picks with a round-robin pointer instead of a coin. The key rule is when a pointer moves: a grant pointer moves to one past the input it granted only if that grant is accepted, and only in the first iteration. With this rule the grant pointers of different outputs drift apart, and under uniform i.i.d. Bernoulli traffic one iteration per slot gives 100% throughput (McKeown 1999). The same scheme with pointers that move on every grant, called RRM, saturates near 63%.

## In plain words

Each output has a list of inputs in a circle and a marker that says which input comes first this time. Each input has the same kind of marker over the outputs. In a slot, every input asks for all outputs it has cells for. Each output says yes to the first asker at or after its marker. Each input that gets several yes answers takes the first one at or after its marker.

When a yes is taken, the output moves its marker to just past that input, so that input goes to the back of the line. When a yes is turned down, the output does not move its marker. This small rule makes the outputs point at different inputs after a while. Then every input gets one yes in every slot, and nothing is wasted.

## The problem

The input of one slot is the request matrix $req \in \{0,1\}^{N \times N}$ of an $N \times N$ switch with virtual output queues ($req[i][j] = 1$ when input $i$ has a cell for output $j$), plus the pointer state. The output is a matching of requests. Over many slots, the aim is the throughput goal of [switch scheduling](/switch-scheduling/): bounded queues for the given traffic.

## The algorithm

The state is a grant pointer $g[j] \in \{0, \ldots, N-1\}$ at each output $j$ and an accept pointer $a[i]$ at each input $i$. "First from $p$" means the first port in the circular order $p, p+1, \ldots, N-1, 0, \ldots, p-1$.

```pseudo id=main
iSLIP-SLOT(req, g, a, K)                      ▷ K = the number of iterations
L1  for it ← 1 to K do
L2      each unmatched input i requests each unmatched output j with req[i][j] = 1
L3      for each unmatched output j with requests, in parallel do
L4          grant the requesting input that is first from g[j]
L5      for each input i with grants, in parallel do
L6          accept the granting output j that is first from a[i]
L7          match i to j
L8          if it = 1 then                    ▷ pointers move only in the first iteration
L9              a[i] ← (j + 1) mod N
L10             g[j] ← (i + 1) mod N         ▷ only for an accepted grant
L11 return the matched pairs
```

Lines L9 and L10 run only for accepted grants, because they sit inside the accept step. A grant that is not accepted leaves $g[j]$ where it was, so that output offers the same input again in the next slot. RRM differs in two places: every output that grants moves $g[j]$ past the granted input, accepted or not, and the pointers move in every iteration.

## Example

Take $N = 4$ with every input holding cells for every output (saturation), and start with all pointers at 0. The table gives the matching ($m[i]$ is the output of input $i$, or $-1$) and the grant pointers after each slot, with one iteration per slot.

| slot | all outputs grant | matching $m$ | $g$ after the slot |
| --- | --- | --- | --- |
| 1 | out 0 to 3 grant in 0 | $[0, -1, -1, -1]$ | $[1, 0, 0, 0]$ |
| 2 | out 0 grants in 1; out 1 to 3 grant in 0 | $[1, 0, -1, -1]$ | $[2, 1, 0, 0]$ |
| 3 | out 0 grants in 2, out 1 grants in 1, out 2 and 3 grant in 0 | $[2, 1, 0, -1]$ | $[3, 2, 1, 0]$ |
| 4 | each output grants a different input | $[3, 2, 1, 0]$ | $[0, 3, 2, 1]$ |
| 5 | each output grants a different input | $[0, 3, 2, 1]$ | $[1, 0, 3, 2]$ |

In slot 1, all four outputs grant input 0, which accepts output 0 (its accept pointer is 0). Only output 0 moves its pointer. Outputs 1, 2 and 3 were turned down, so they keep pointer 0 and grant input 0 again in slot 2, where input 0 now prefers output 1. Each slot peels one more output off the crowd. After $N - 1 = 3$ slots the grant pointers are all different, and from slot 4 on every slot is a perfect matching, a rotating time-division schedule.

Under RRM, all four outputs would move their pointers to 1 after slot 1, since all four granted input 0. They stay equal forever, so each slot matches one pair and the throughput is $1/4$ per port. For $N = 2$ this is the 50% of McKeown's two-port example.

## Correctness

Each slot yields a matching, because an output grants at most one input and an input accepts at most one output, and matched ports drop out of later iterations. Each iteration that starts with an open request adds a pair, so $N$ iterations always give a maximal matching.

The desynchronization result: under saturation, from any pointer state and for any number of iterations, the grant pointers become pairwise distinct within $N - 1$ slots, and then every slot is a perfect matching. Let $s_v$ be the number of outputs whose pointer is $v$. In the first iteration those outputs all grant input $v$, exactly one is accepted and moves to $v+1$, and the others stay. So $s'_v = \max(s_v - 1, 0) + [s_{v-1} \ge 1]$. An empty position after a slot needs an empty left neighbor before it, so an empty position after $N - 1$ slots traces back to an empty point that moves right by one per slot. A counting argument relative to that moving point shows that the $N$ outputs cannot fit, which is a contradiction. The full proof is below. For $N = 4$, a run over all $4^4$ grant pointer states (with three accept pointer states each) takes at most 3 slots, which is $N - 1$.

## Complexity

- **Per slot, sequential model.** An iteration reads each request once: $O(N^2)$ work. With $K$ iterations, $O(K N^2)$ time on the word RAM, and $\Theta(N^2)$ space for the request lists, plus $2N$ pointers kept between slots.
- **In hardware.** Each arbiter is a programmable priority encoder over $N$ request lines, which a tree circuit evaluates in $O(\log N)$ gate delays. All $N$ grant arbiters run in parallel, then all $N$ accept arbiters. So one iteration costs $O(\log N)$ gate delays.
- **Iterations.** Each iteration adds a pair while the matching is not maximal, so at most $N$ iterations are needed. McKeown reports from simulation that about $\log_2 N$ iterations suffice on average; this is a measured number, not a proved bound.
- **Throughput, measured.** With $N = 16$, one iteration and Bernoulli arrivals of rate 1.0 per input with uniform outputs (seed 3), iSLIP sends 0.932 cells per port per slot in the first 3000 slots and 0.970 in the next 3000; longer runs keep rising (0.977, 0.980, 0.983 in later blocks), and the grant pointers end up all distinct. At load 0.7 (seed 3, 3000 slots), iSLIP sends 33460 of 33746 cells, while RRM sends only 27107 and leaves 6639 queued.

## Properties

- **Deterministic and fair.** No random numbers are needed. A requested output serves its inputs in round-robin order, and the pointer of an output that was turned down stays on the same input.
- **Desynchronization.** The update rule spreads the grant pointers, which is the source of the high throughput under uniform load.
- **No guarantee for all admissible loads.** iSLIP has 100% throughput for uniform i.i.d. Bernoulli traffic. For nonuniform admissible traffic a maximal matching scheduler without speedup can be unstable, so iSLIP has no general guarantee. A [maximum-weight matching](/maximum-weight-matching/) or speedup 2 gives one.
- **Maximal with enough iterations.** With $N$ iterations the matching is maximal; with one, it may not be.

## Variants and improvements

- **SLIP.** The single-iteration form, from McKeown's 1995 thesis.
- **RRM.** Round-robin matching, the naive form whose pointers move on every grant. It is unstable above a load near 63% under uniform Bernoulli traffic, according to McKeown, because the pointers move in lock step.
- **FIRM.** A variant in which an output whose grant is turned down moves its pointer to the granted input, not past it, which improves fairness (Serpanos and Antoniadis, 2000).
- **Weighted and prioritized iSLIP.** Separate pointers per priority level, or weights in the arbiters, to give classes of traffic different shares.
- **Separable allocators in on-chip routers.** The same input-first and output-first round-robin arbitration assigns switch ports and virtual channels in network-on-chip routers.

## When to use it

Use iSLIP when the scheduler must be a small, fast circuit and the traffic is close to uniform, which is the common case in a router line card. It is simpler in hardware than [PIM](/parallel-iterative-matching/), since it needs no random numbers, and one iteration already gives high throughput under uniform load. Use more iterations, or speedup, when the load is bursty or nonuniform. Use a [Birkhoff-von Neumann](/birkhoff-von-neumann-decomposition/) schedule when rates are known and fixed, and a maximum-weight matching only in analysis or in slow switches.

## Pitfalls

- **Moving the grant pointer on every grant.** Writing line L10 outside the accept step turns iSLIP into RRM. The pointers then synchronize, and the throughput drops to about 63% under uniform load, or to $1/N$ under saturation.
- **Moving pointers in later iterations.** Lines L9 and L10 must run only when it = 1. McKeown shows that updates in later iterations can starve a queue, because a connection matched in a later iteration may push a pointer past an input that has waited.
- **Moving to the accepted port instead of one past it.** Setting $g[j] \leftarrow i$ in line L10 keeps the same input first forever and breaks the round-robin order.
- **Expecting 100% throughput for every load.** The 100% result is for uniform i.i.d. Bernoulli traffic. For other admissible loads iSLIP can be unstable.

## Implementations

## History

McKeown introduced SLIP in his 1995 thesis at the University of California, Berkeley, and published iSLIP with its analysis and simulations in IEEE/ACM Transactions on Networking in 1999. The scheme was a deterministic answer to the randomized [PIM](/parallel-iterative-matching/) of Anderson, Owicki, Saxe and Thacker (1993). According to McKeown, schedulers of this kind were used in the Tiny Tera prototype and in commercial router fabrics such as the Cisco 12000 series.

## References
