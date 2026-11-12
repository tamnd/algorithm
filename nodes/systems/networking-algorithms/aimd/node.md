---
tag: 378JCS
kind: algorithm
slug: aimd
name: Additive increase multiplicative decrease
aliases:
- AIMD
- additive increase, multiplicative decrease
area: systems/networking-algorithms
level: intro
summary: Each user adds a constant to its rate while the network is not overloaded and multiplies its rate by a factor below 1 when it is. The rates converge to a fair share.
solves: [congestion-control]
model: synchronous-model
complexity:
  vars: {n: the number of users, t: the number of steps}
  time: {worst: Θ(n t)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1989
  people: [Dah-Ming Chiu, Raj Jain]
  note: Chiu and Jain analyzed the linear increase and decrease controls with binary feedback and showed that additive increase with multiplicative decrease is the one that converges to efficiency and fairness.
prereqs: [congestion-control]
see_also: [tcp-reno, tcp-tahoe, slow-start, tcp-cubic, ecn, max-min-fairness, proportional-fairness, exponential-backoff]
sources:
  - paper: doi:10.1016/0169-7552(89)90019-6
    title: Dah-Ming Chiu and Raj Jain, Analysis of the increase and decrease algorithms for congestion avoidance in computer networks, Computer Networks and ISDN Systems 17(1), 1989
    locator: pages 1 to 14 (the binary feedback model, the vector diagram of two users, the fairness index and the conditions on the linear controls)
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, ACM SIGCOMM 1988
    locator: pages 314 to 329 (congestion avoidance, an additive increase of one segment per round trip and a cut to one half on loss)
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Section 3.1, equations 3 and 4 (the congestion avoidance increase and the ssthresh after a loss)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.7 (TCP congestion control, and TCP fairness)
---

Additive increase multiplicative decrease (AIMD) is a rule for [congestion control](/congestion-control/): each user adds a constant $a$ to its rate after a step without overload, and multiplies its rate by a factor $b < 1$ after a step with overload. Chiu and Jain proved in 1989 that, when all users get the same binary feedback, the rates converge to an equal share of the capacity, and that no other linear rule does this. TCP uses AIMD on its window in congestion avoidance: one segment more per round trip, and one half on a loss.

## In plain words

Several people share one water pipe. Nobody knows how much the others take. After each minute a light says "too much" or "fine". When the light says fine, each person opens the tap by the same small amount. When the light says too much, each person closes the tap to one half of what it is.

Why does this become fair? Opening by the same amount does not change the gap between two people. Halving cuts the gap in half. So each "too much" signal makes the gap smaller, and the gap goes to zero. The total flow goes up and down near the size of the pipe, so the pipe stays well used.

## The problem

There are $n$ users and one resource of capacity $c$. User $i$ has a rate $x_i \ge 0$. After each step, every user gets the same bit $y$: $y = 1$ if the total load $\sum_i x_i$ is above $c$, else $y = 0$. Each user changes its own rate from $y$ and its own rate only. The goals are efficiency (the load stays near $c$) and fairness (the rates become equal). This is the synchronous binary feedback model of Chiu and Jain, a small case of [congestion control](/congestion-control/).

## The algorithm

```pseudo id=main
AIMD(x, c, a, b)                           ▷ n users, a > 0, 0 < b < 1
L1  for each step t = 0, 1, 2, ...
L2      y ← [x_1 + ... + x_n > c]          ▷ the same feedback bit for all users
L3      for i ← 1 to n do
L4          if y = 0 then x_i ← x_i + a    ▷ additive increase
L5          else x_i ← b · x_i             ▷ multiplicative decrease
L6      record x
```

Line L2 is the network: it compares the load with the capacity and returns one bit. Lines L3 to L5 are the users. Each one needs only its own rate and the bit. Line L4 moves all rates by the same amount, so it moves the rate vector parallel to the line of equal rates. Line L5 moves the rate vector toward the origin, so it moves it closer to the line of equal rates in angle.

In TCP, the rate is the congestion window divided by the round-trip time, and a step is one round trip. Line L4 is the congestion avoidance increase of one segment per round trip, and line L5 is the cut to one half on a loss. [TCP Reno](/tcp-reno/) uses $a = 1$ segment and $b = 1/2$. [TCP CUBIC](/tcp-cubic/) uses $b = 0.7$ and a different increase.

## Example

Two users start at $x = (1, 7)$. The capacity is $c = 10$, $a = 1$ and $b = 1/2$. The table gives the rates at the start of each step, the total load, the feedback and Jain's index $J = (\sum x_i)^2 / (n \sum x_i^2)$, which is 1 for equal rates.

| step | $x_1$ | $x_2$ | load | $y$ | $x_2 - x_1$ | $J$ |
|---|---|---|---|---|---|---|
| 0 | 1 | 7 | 8 | 0 | 6 | 0.6400 |
| 1 | 2 | 8 | 10 | 0 | 6 | 0.7353 |
| 2 | 3 | 9 | 12 | 1 | 6 | 0.8000 |
| 3 | 3/2 | 9/2 | 6 | 0 | 3 | 0.8000 |
| 4 | 5/2 | 11/2 | 8 | 0 | 3 | 0.8767 |
| 5 | 7/2 | 13/2 | 10 | 0 | 3 | 0.9174 |
| 6 | 9/2 | 15/2 | 12 | 1 | 3 | 0.9412 |
| 7 | 9/4 | 15/4 | 6 | 0 | 3/2 | 0.9412 |
| 10 | 21/4 | 27/4 | 12 | 1 | 3/2 | 0.9846 |
| 11 | 21/8 | 27/8 | 6 | 0 | 3/4 | 0.9846 |
| 14 | 45/8 | 51/8 | 12 | 1 | 3/4 | 0.9961 |

The load runs through the cycle 8, 10, 12, 6. Each cut by one half halves the difference: 6, 3, 3/2, 3/4. The rates go to the equal share of 5 each, and the load stays between 6 and 12.

The other linear rules fail on the same start. Additive increase with additive decrease keeps the difference 6 for ever. Multiplicative increase with multiplicative decrease keeps the ratio 7. Multiplicative increase with additive decrease moves away from the equal share and drives the smaller rate to 0.

## Correctness

The key fact is about the difference of two rates: line L4 does not change it, and line L5 multiplies it by $b$. So the difference after $t$ steps is the first difference times $b^{D}$, where $D$ is the number of decrease steps. The load enters the band $(bc, c + na]$ after a finite number of steps, and it stays there. In the band, a decrease comes at least once in every $m + 1$ steps, where $m = \lceil (1-b)c/(na) \rceil$. So $D$ grows without bound, and all differences go to 0. The proof has all the cases.

The converse is from Chiu and Jain: among all linear rules $x_i \leftarrow a_I + b_I x_i$ on increase and $x_i \leftarrow a_D + b_D x_i$ on decrease, the rates converge to efficiency and fairness only if $a_I > 0$, $b_I \ge 1$, $a_D = 0$ and $0 \le b_D < 1$. So the decrease must be multiplicative.

## Complexity

Each step costs $\Theta(1)$ for each user, so $\Theta(n t)$ in total for $t$ steps, with $\Theta(1)$ extra space for each user. The network part, line L2, needs only the load.

The speed of convergence follows from the proof. After the load is in the band, the differences shrink by a factor $b$ at least once in every $m + 1$ steps, with $m = \lceil (1-b)c/(na) \rceil$. To shrink them by a factor $\varepsilon$ takes at most $(m + 1) \lceil \ln(1/\varepsilon) / \ln(1/b) \rceil$ steps. In the example, $m = \lceil 5/2 \rceil = 3$, and the decreases come exactly once in every 4 steps.

There is a trade-off in $b$. A small $b$ makes the rates fair in few cuts, but the load falls to $bc$ after each cut, so the link is less used. A $b$ close to 1 keeps the load high but needs many cuts.

## Properties

- **Distributed.** Each user needs only its own rate and the common bit. No user knows $n$ or the other rates.
- **Fair in the limit.** All rates go to $S/n$, where $S$ is the load. With equal users this is the [max-min fair](/max-min-fairness/) share of one link.
- **Efficient on average.** After the start, the load stays above $bc$ and overshoots $c$ by at most $na$.
- **Oscillates.** The load never settles. It runs through a cycle, which is how the users probe for free capacity.

## Variants and improvements

- **Window form in TCP.** The window $w$ grows by $a/w$ segments per acknowledgment, so by about $a$ per round trip, and becomes $b w$ on a loss. [TCP Reno](/tcp-reno/) and [TCP Tahoe](/tcp-tahoe/) use this. In RFC 5681 the increase is $\text{SMSS}^2/\text{cwnd}$ bytes per ACK.
- **Different round trips.** In TCP, a flow with a longer round trip increases less often, so it gets a smaller share. AIMD is fair only in the steps of the model, not in time.
- **Other $a$ and $b$.** Any pair with $a > 0$ and $0 < b < 1$ converges. TCP-friendly rate controls pick $a = 3(1-b)/(1+b)$ so that the average rate matches Reno with $b = 1/2$. CUBIC uses this formula with $b = 0.7$ in its Reno-friendly region.
- **Explicit feedback.** With [ECN](/ecn/), the bit $y$ comes from a router mark instead of a loss.

## When to use it

Use AIMD when many independent senders share a resource and get only a yes or no signal of overload. It is the base of TCP congestion avoidance and of many rate limiters and retry schemes. Do not use it when you need a steady rate, because it oscillates by design, or when the signal comes late and rarely, because the rates then move far from the share between signals.

## Pitfalls

- **An increase that grows with the rate.** If line L4 adds an amount that grows with $x_i$, the large users gain more than the small ones, and fairness is lost. The increase must be the same constant for all users.
- **A decrease that is too small.** A cut with $b$ close to 1 in line L5 converges very slowly. A subtraction instead of a multiplication does not converge to fairness at all.
- **Different feedback for different users.** The proof needs the same bit in line L2 for all users. If only some users see the loss, as with drop-tail queues and different round trips, the shares are not equal.
- **Mixing up rate and window.** Line L4 adds $a$ to a rate. On a window it must be applied once per round trip, not once per acknowledgment.

## Implementations

## History

Jacobson put an additive increase and a multiplicative decrease into TCP in 1988, with a cut to one half on a loss. In 1989 Chiu and Jain gave the analysis in the binary feedback model: they drew the two-user vector diagram, measured fairness with the index $J$, and proved that among linear controls only additive increase with multiplicative decrease converges to the efficient and fair point.

## References
