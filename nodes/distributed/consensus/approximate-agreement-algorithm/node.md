---
tag: 11RC2B
kind: algorithm
slug: approximate-agreement-algorithm
name: Approximate agreement algorithm
area: distributed/consensus
level: advanced
summary: Each round, every process sends its value to all, drops the t smallest and t largest values it gets and moves to the midpoint of the rest. With n > 3t the spread halves each round.
solves: [approximate-agreement]
model: synchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes, Δ: a known bound on the spread of the correct inputs, ε: the allowed spread of the outputs}
  time: {best: Θ(log(Δ/ε))}
  messages: {best: Θ(n² log(Δ/ε))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [Danny Dolev, Nancy A. Lynch, Shlomit S. Pinter, Eugene W. Stark, William E. Weihl]
  note: Dolev, Lynch, Pinter, Stark and Weihl defined approximate agreement and gave synchronous and asynchronous algorithms that drop extreme values and average the rest, in the Journal of the ACM in 1986.
prereqs: [approximate-agreement, synchronous-model, byzantine-failure-model]
see_also: [approximate-agreement, byzantine-fault-tolerance, k-set-agreement, consensus-problem, floodset, clock-synchronization]
sources:
  - paper: doi:10.1145/5925.5931
    title: Danny Dolev, Nancy A. Lynch, Shlomit S. Pinter, Eugene W. Stark and William E. Weihl, Reaching approximate agreement in the presence of faults, Journal of the ACM 33(3), 1986, pages 499 to 516
    locator: the synchronous algorithm with its reduce and select functions and its convergence rate, and the asynchronous algorithm for n > 5t
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 7.2 (approximate agreement, the synchronous algorithm, its convergence and the number of rounds)
  - paper: doi:10.1007/11516798_17
    title: Ittai Abraham, Yonatan Amit and Danny Dolev, Optimal resilience asynchronous approximate agreement, Proceedings of the 8th International Conference on Principles of Distributed Systems (OPODIS), LNCS 3544, 2004, pages 229 to 239
    locator: the asynchronous algorithm for n > 3t
---

The approximate agreement algorithm lets $n$ processes, up to $t$ of them [Byzantine](/byzantine-failure-model/), reach values within $\varepsilon$ of each other and inside the range of the correct inputs, which is the [approximate agreement](/approximate-agreement/) problem. In each [synchronous](/synchronous-model/) round, every process sends its value to all, removes the $t$ smallest and $t$ largest of the $n$ values it receives, and takes the midpoint of what is left. With $n > 3t$ this halves the spread of the correct values in every round, whatever the faulty processes send, so $\lceil \log_2(\Delta/\varepsilon) \rceil$ rounds are enough. It follows Dolev, Lynch, Pinter, Stark and Weihl (1986), who use a finer averaging rule that converges faster when $n$ is large compared to $t$.

## In plain words

Some thermometers measure the same room, and a few of them may be broken or even lie. The goal is not one exact number, but numbers that are very close to each other and inside the range of the honest readings.

Each round, every thermometer tells its reading to all the others. Each one sorts what it heard, throws away the few highest and the few lowest readings, because a liar could hide there, and moves to the middle of what remains.

Every honest thermometer keeps an honest middle value in what it keeps, so their new readings can differ by at most half of what they differed by before. After enough rounds the gap is as small as needed.

## The problem

There are $n$ processes in the synchronous model: in each round every process sends a message to every other process, and every message from a correct process arrives in the same round. At most $t$ processes are Byzantine: they can send anything, and different values to different processes. Each correct process $p$ has a real input $x_p$. Given $\varepsilon > 0$ and a known bound $\Delta$ on the spread $\max_p x_p - \min_p x_p$ of the correct inputs, every correct process must output a value so that:

- **Agreement.** Any two correct outputs differ by at most $\varepsilon$.
- **Validity.** Every correct output lies in $[\min_p x_p, \max_p x_p]$, the range of the correct inputs.
- **Termination.** Every correct process outputs a value.

The algorithm needs $n > 3t$. Its arithmetic is exact: the implementation uses fractions.

## The algorithm

```pseudo id=main
APPROXIMATE AGREEMENT, at correct process p, with n > 3t
L1  x ← x_p; R ← ⌈log₂(Δ/ε)⌉ (R ← 0 if Δ ≤ ε)
L2  for rounds 1 to R: send x to all processes
L3      receive one value from each process; a missing value counts as x
L4      sort the n values and drop the t smallest and the t largest
L5      x ← (smallest kept value + largest kept value) / 2
L6  output x
```

**Why drop $t$ at each end.** At most $t$ of the $n$ values are from faulty processes. Any value below all correct values is faulty, so at most $t$ values lie below the smallest correct value, and line L4 removes at least as many values from the bottom. The same holds at the top. So every kept value lies in the range of the correct values: a liar cannot drag the result outside.

**Why the midpoint halves the spread.** Let $u_1 \le u_2 \le \cdots$ be the values of the correct processes at the start of a round. Every correct process receives all of them, plus at most $t$ others. The $(t+1)$-th smallest correct value $u_{t+1}$ lies in the kept range of every correct process: at least $t + 1$ received values are at most $u_{t+1}$, and at least $t + 1$ received values are at least $u_{t+1}$ (this uses $n > 3t$). So every kept range contains the common point $c = u_{t+1}$, and lies inside $[u_{\min}, u_{\max}]$. Two kept ranges $[a, b]$ and $[a', b']$ then have $a, a' \in [u_{\min}, c]$ and $b, b' \in [c, u_{\max}]$, and their midpoints differ by at most $\frac{(c - u_{\min}) + (u_{\max} - c)}{2}$, half the old spread.

**A missing value.** If a faulty process sends nothing, line L3 uses the receiver's own value. A faulty process could have sent that value, so this case is covered by the proof.

## Example

$n = 4$, $t = 1$. The correct processes $p_0$, $p_1$, $p_2$ start with 0, 4 and 8, so $\Delta = 8$; with $\varepsilon = 1$ the algorithm runs $R = 3$ rounds. The faulty process $p_3$ sends $-1000$ to every correct process whose value is at most the middle of the correct range, and $+1000$ to the others, to pull them apart.

| round | received by $p_0$ | kept by $p_0$ | $p_0$ | $p_1$ | $p_2$ | spread |
|---|---|---|---|---|---|---|
| start | | | 0 | 4 | 8 | 8 |
| 1 | $-1000, 0, 4, 8$ | 0, 4 | 2 | 2 | 6 | 4 |
| 2 | $-1000, 2, 2, 6$ | 2, 2 | 2 | 2 | 4 | 2 |
| 3 | $-1000, 2, 2, 4$ | 2, 2 | 2 | 2 | 3 | 1 |

In round 1, $p_2$ receives $0, 4, 8, 1000$, keeps $4, 8$ and moves to 6. In every round the spread halves exactly, and all values stay in $[0, 8]$. The outputs 2, 2 and 3 are within $\varepsilon = 1$.

## Correctness

Each correct process keeps only values inside the current range of correct values, so the values never leave the range of the correct inputs, which gives validity. Every kept range contains the $(t+1)$-th smallest correct value, so two midpoints differ by at most half the old spread. After $R$ rounds the spread is at most $\Delta/2^R \le \varepsilon$, which gives agreement, and termination is by the fixed round count. The bound $n > 3t$ is used in exactly one step, and the algorithm fails without it (see Pitfalls). The full proof is below.

## Complexity

The algorithm runs $R = \lceil \log_2(\Delta/\varepsilon) \rceil$ rounds. In each round every process sends one value to each other process, so it sends $n(n-1)$ messages per round and $\Theta(n^2 \log(\Delta/\varepsilon))$ in all. Each process stores the $n$ values of one round and sorts them, in $O(n \log n)$ time per round. The exact values are fractions whose denominators can double in each round, so with exact arithmetic a value needs $O(R)$ more bits than an input.

## Properties

- Deterministic, and tolerates $t$ Byzantine processes when $n > 3t$.
- Convergence factor $1/2$ in each round. The bound is tight for this rule: the test with $n = 4$, $t = 1$ and correct values $0, 1, 1$ halves the spread exactly.
- Validity holds in every round, not only at the end, so a process can stop early and still output a value inside the correct range.
- Needs a known bound $\Delta$ on the input spread to fix $R$ in advance, or a first round that estimates it (see Variants).

## Variants and improvements

- **Faster averaging (DLPSW).** Dolev et al. keep the trimmed multiset, choose every $t$-th value of it, and output the mean of the chosen values. In the synchronous model this shrinks the spread by a factor of about $1/(\lfloor (n - 2t - 1)/t \rfloor + 1)$ in each round, which is better than $1/2$ when $n$ is much larger than $3t$.
- **Unknown $\Delta$.** In DLPSW, each process computes the number of rounds from the range of the values it kept in the first round. Processes may then compute different counts, so a process that finishes keeps sending its final value, and the others use it.
- **Asynchronous model.** Without rounds, a process can wait only for $n - t$ values, and the faulty values can be different for different processes. The asynchronous algorithm of DLPSW needs $n > 5t$ and has convergence factor about $1/(\lfloor (n - 3t - 1)/(2t) \rfloor + 1)$. Abraham, Amit and Dolev (2004) reach the optimal $n > 3t$ by having processes send their values with [reliable broadcast](/byzantine-reliable-broadcast/) and report which values they used, so that faulty processes cannot show different values to different processes.
- **Crash failures only.** With crash failures the same idea works with fewer processes, since crashed processes never send wrong values.
- **Multidimensional approximate agreement.** Values are vectors, and outputs must lie in the convex hull of the correct inputs. The trimmed midpoint has no direct analogue there, and the bounds on $n$ depend on the dimension.

## When to use it

Use it when processes must agree on a real number, such as a clock correction, a sensor reading or a rate, and exact agreement is not needed. It is deterministic and needs no leader, no signatures and no randomness, and unlike exact [consensus](/consensus-problem/), the asynchronous version is solvable. It is the core of fault-tolerant [clock synchronization](/clock-synchronization/) algorithms, which drop extreme clock readings and average the rest. If the values must be equal, use a consensus protocol such as [PBFT](/pbft/) instead.

## Pitfalls

- **$n \le 3t$.** With $n = 3$ and $t = 1$, correct processes with values 0 and 1, and a faulty process that sends $-10$ to the first and $10$ to the second, each correct process keeps its own value forever: the spread stays 1. The test reproduces this run. No algorithm can do better: approximate agreement with Byzantine faults needs $n > 3t$.
- **Trimming fewer than $t$ values.** A single faulty value outside the correct range then survives, and both validity and convergence break.
- **Changing the rule without a new proof.** The mean of all kept values also stays in the correct range, but the halving argument above is for the midpoint only. Use a rule whose convergence is proved, such as the midpoint or the DLPSW select and average rule.
- **Floating point.** Rounding can move a value slightly outside the correct range. Use exact arithmetic, or account for the rounding in $\varepsilon$.

## Implementations

## History

Dolev, Lynch, Pinter, Stark and Weihl introduced approximate agreement in 1986 as a problem that, unlike consensus, can be solved in an asynchronous system with faults. They gave a synchronous algorithm for $n > 3t$ and an asynchronous one for $n > 5t$, both based on the reduce and select functions, and proved the convergence rates. Fischer, Lynch and Merritt showed in the same year that $n > 3t$ is necessary. Abraham, Amit and Dolev closed the asynchronous gap in 2004 with an algorithm for $n > 3t$. The idea of dropping extreme values reappears in fault-tolerant clock synchronization.

## References
