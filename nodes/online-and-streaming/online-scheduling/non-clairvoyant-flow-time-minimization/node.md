---
tag: 3AB28K
kind: problem
slug: non-clairvoyant-flow-time-minimization
name: Non-clairvoyant flow time minimization
aliases:
- non-clairvoyant total flow time
- nonclairvoyant scheduling
area: online-and-streaming/online-scheduling
level: advanced
summary: Flow time minimization when processing times are revealed only as jobs run.
prereqs: [online-flow-time-minimization, clairvoyant-scheduling, randomized-online-algorithm]
see_also: [round-robin, multilevel-feedback-queue, srpt, oblivious-adversary, flow-time, online-total-completion-time, yao-minimax-principle, shortest-processing-time-first]
sources:
  - paper: doi:10.1016/0304-3975(94)90151-1
    title: Rajeev Motwani, Steven Phillips and Eric Torng, Non-clairvoyant scheduling, Theoretical Computer Science 130(1), 1994 (SODA 1993)
    locator: pages 17 to 47 (round robin in the batch case, the Omega(n^(1/3)) deterministic and Omega(log n) randomized lower bounds with release times)
  - paper: doi:10.1145/1008731.1008732
    title: Luca Becchetti and Stefano Leonardi, Nonclairvoyant scheduling to minimize the total flow time on single and parallel machines, Journal of the ACM 51(4), 2004 (STOC 2001)
    locator: pages 517 to 539 (RMLF is O(log n)-competitive on one machine and O(log n log(n/m)) on m machines, against an oblivious adversary)
  - paper: doi:10.1145/347476.347479
    title: Bala Kalyanasundaram and Kirk Pruhs, Speed is as powerful as clairvoyance, Journal of the ACM 47(4), 2000
    locator: pages 617 to 643 (SETF with speed 1 + eps is (1 + 1/eps)-competitive for the total flow time)
  - paper: "Bala Kalyanasundaram and Kirk Pruhs, Minimizing flow time nonclairvoyantly, Journal of the ACM 50(4), 2003"
    locator: pages 551 to 567 (the first randomized algorithm, RMLF, with ratio O(log n log log n))
  - paper: "Jiří Sgall, On-line scheduling, in Amos Fiat and Gerhard J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    locator: Section 5.4 (non-clairvoyant scheduling with the total completion and flow time objectives)
---

Non-clairvoyant flow time minimization is [online flow time minimization](/online-flow-time-minimization/) in a model where the scheduler does not know the size of a job: it learns that a job is done only when the job completes. The scheduler sees the release of each job and the work it has given to each job so far. On one machine with [preemption](/preemptive-scheduling/), [SRPT](/srpt/) is no longer possible, no deterministic algorithm is better than $\Omega(n^{1/3})$-competitive, and the randomized multilevel feedback rule reaches the best possible $O(\log n)$. With a little extra speed, shortest elapsed time first is constant competitive.

## In plain words

An operating system runs programs, but it does not know how long each one will run. It knows only how long it has run each program so far. It still wants programs to finish soon after they start.

If it ran the program with the least work left, it would be optimal, but it cannot see the work left. A fair rule gives each waiting program an equal share of the processor. Another rule favors the programs that have run the least, on the guess that a new program is likely to be short. These rules are good when all programs start at once. When programs keep arriving, a rule without any random choice can be forced to be very bad. A rule that guesses at random when to lower the priority of a long program does much better on average.

## Definition

**Input.** A sequence $\sigma$ of $n$ jobs on one machine (or $m$ [identical machines](/identical-machines/)) of speed 1. Job $j$ has a release time $r_j$ and a processing time $p_j > 0$.

**Information.** At time $t$, the algorithm knows the jobs with $r_j \le t$, the work that each one has received, and which ones are complete. It does not know $p_j$ until job $j$ completes. This is the opposite of the [clairvoyant](/clairvoyant-scheduling/) model.

**Schedule.** Preemption is allowed and free. The machine can also be shared: running $k$ jobs at rate $1/k$ each is the limit of fast switching, and it is allowed in the model.

**Objective.** Minimize the total [flow time](/flow-time/) $\sum_j (C_j - r_j)$. If all $r_j = 0$ (the batch case), this is the total completion time.

**Notation.** $\sigma$ is the job sequence, ALG$(\sigma)$ and OPT$(\sigma)$ are the total flow time of the online algorithm and of the best offline schedule (which knows the sizes, so OPT is the SRPT value on one machine), and $c$ is the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, with additive constant $b = 0$. For a [randomized algorithm](/randomized-online-algorithm/), the ratio is $\mathbb{E}[\text{ALG}(\sigma)] \le c \cdot \text{OPT}(\sigma)$ against an [oblivious adversary](/oblivious-adversary/), which fixes $\sigma$ before the random choices.

## Variants

- **Batch or release times.** In the batch case all jobs are present at time 0. With release times, the problem is much harder.
- **Deterministic or randomized.** The two have very different best ratios with release times.
- **Extra speed.** The online machine has speed $s = 1 + \varepsilon$ and OPT has speed 1.
- **Parallel machines.** $m$ identical machines, with preemption and migration.
- **Speedup curves.** Each job may run on several processors at a rate given by an unknown function; this generalizes the model above.

## Examples

**The batch case.** Take three jobs at time 0 with sizes 1, 2 and 3. [Round robin](/round-robin/), in its limit form where all waiting jobs share the machine equally, completes them at 3, 5 and 6, for a total of 14. SPT, which knows the sizes, completes them at 1, 3 and 6, for a total of 10. With three jobs of size 1, round robin completes all of them at time 3, for a total of 9, and SPT gets 6. The ratio $9/6 = 3/2$ is the worst ratio for three jobs (see the theorem below).

**Release times.** Take one machine and the jobs $(0, 5)$, $(1, 2)$, $(2, 4)$ and $(3, 1)$, written as (release, size).

| rule | knows sizes | flow times | total |
|---|---|---|---|
| SRPT | yes | 8, 2, 10, 1 | 21 |
| SETF, least work received so far first | no | 12, 6, 9, 1 | 28 |
| round robin, equal sharing | no | 23/2, 13/2, 10, 4 | 32 |

SETF runs each new job at once, because it has received no work, so the short job $D$ gets flow time 1. Then $A$, $B$ and $C$ have each received 1 unit and share the machine. Round robin shares the machine with the long job $A$ from the start, so the short jobs wait longer.

## Known algorithms

**Round robin in the batch case.** This result is proved here.

*Theorem.* With all jobs released at time 0 on one machine, round robin with equal sharing has total completion time $2 \cdot \text{OPT} - \sum_j p_j$. So its ratio is at most $2 - 2/(n + 1)$, with equality when all sizes are equal.

*Proof.* Sort the sizes as $p_{(1)} \le \dots \le p_{(n)}$. Under equal sharing, the jobs complete in this order, and while job $(k)$ is the shortest one left, $n - k + 1$ jobs share the machine. All unfinished jobs receive work at the same rate, so at time $C_{(i)}$ each job $(k)$ with $k \ge i$ has received exactly $p_{(i)}$. The work done by then is $\sum_{k < i} p_{(k)} + (n - i + 1) \, p_{(i)}$, and the machine never idles, so

$$C_{(i)} = \sum_{k < i} p_{(k)} + (n - i + 1) \, p_{(i)}.$$

Summing over $i$, the size $p_{(k)}$ appears once in $C_{(i)}$ for each $i > k$ and $n - k + 1$ times in $C_{(k)}$. So

$$\sum_i C_{(i)} = \sum_k (2(n - k) + 1) \, p_{(k)}.$$

The optimum with known sizes is SPT, by [Smith's rule](/smith-rule/), with value $\text{OPT} = \sum_k (n - k + 1) \, p_{(k)}$. Hence $\sum_i C_{(i)} = 2 \, \text{OPT} - \sum_k p_{(k)}$. The coefficients $n - k + 1$ decrease and the sizes $p_{(k)}$ increase in $k$. By Chebyshev's sum inequality, $\text{OPT} \le \frac{1}{n} \sum_k (n - k + 1) \cdot \sum_k p_{(k)} = \frac{n+1}{2} \sum_k p_{(k)}$, with equality when all sizes are equal. So $\sum_k p_{(k)} \ge \frac{2}{n+1} \text{OPT}$, and the ratio is at most $2 - \frac{2}{n+1}$. $\square$

Motwani, Phillips and Torng showed that the ratio 2 of round robin in the batch case is the best possible as $n$ grows, even for randomized algorithms. This lower bound is cited here and not proved.

**Shortest elapsed time first (SETF).** At each moment, run the waiting jobs that have received the least work, sharing the machine equally among ties. It is the limit of a [multilevel feedback queue](/multilevel-feedback-queue/) with many levels. With release times and speed $1 + \varepsilon$, SETF is $(1 + 1/\varepsilon)$-competitive for the total flow time against OPT at speed 1 (Kalyanasundaram and Pruhs 2000). Without extra speed, SETF is not $O(1)$-competitive, since no deterministic algorithm is.

**Randomized multilevel feedback (RMLF).** The multilevel feedback queue moves a job to a lower priority level when its received work passes a threshold of the form $2^i$. RMLF sets each job's thresholds with a random perturbation, so that the adversary cannot predict when a job is demoted. Becchetti and Leonardi showed that RMLF is $O(\log n)$-competitive on one machine against an oblivious adversary, and $O(\log n \log(n/m))$-competitive on $m$ machines. An earlier version by Kalyanasundaram and Pruhs had ratio $O(\log n \log \log n)$. These results are cited here and not proved.

## Bounds

All bounds are for one machine with preemption and release times, unless stated otherwise. They are cited, except the round robin theorem above.

| bound | algorithms | value | source |
|---|---|---|---|
| lower | deterministic | $\Omega(n^{1/3})$ | Motwani, Phillips and Torng 1994 |
| lower | randomized, oblivious adversary | $\Omega(\log n)$ | Motwani, Phillips and Torng 1994 |
| upper | randomized, RMLF, oblivious adversary | $O(\log n)$ | Becchetti and Leonardi 2004 |
| upper | deterministic, SETF at speed $1 + \varepsilon$ | $1 + 1/\varepsilon$ | Kalyanasundaram and Pruhs 2000 |
| batch, tight | round robin, deterministic | $2 - 2/(n+1)$, about 2 | proved above |

So on one machine the randomized problem is settled up to a constant factor: $\Theta(\log n)$ against an oblivious adversary. A deterministic algorithm cannot reach a logarithmic ratio, because of the $\Omega(n^{1/3})$ bound. Lower bounds for randomized algorithms of this kind are proved with [Yao's principle](/yao-minimax-principle/): a random input on which every deterministic algorithm does badly in expectation.

## Reductions

- **From the clairvoyant problem.** A non-clairvoyant algorithm is a clairvoyant one that ignores the sizes. So each lower bound for clairvoyant online flow time holds here, and each upper bound here holds there.
- **Batch case to total completion time.** With all $r_j = 0$, flow time and completion time are equal, and the problem is the non-clairvoyant version of [shortest processing time first](/shortest-processing-time-first/).
- **Extra speed as a substitute for knowledge.** The SETF result shows that a factor $1 + \varepsilon$ in speed replaces the knowledge of the sizes, up to a factor $1 + 1/\varepsilon$ in the ratio.

## Applications

Time-sharing operating systems do not know how long a process runs, so they are non-clairvoyant. Round robin and the multilevel feedback queue of Unix and Windows schedulers are the deterministic rules studied here. The theory explains their design: favoring jobs with little received work (SETF and MLF) helps short jobs, and randomness or a small reserve of speed protects against inputs that defeat a fixed rule.

## References
