---
tag: WEGK54
kind: definition
slug: parallel-efficiency
name: Parallel efficiency
aliases:
- efficiency
- processor utilization
area: parallel/work-span-models
level: intro
summary: The speedup per processor, T_1/(p T_p), equal to the work divided by the cost p T_p. It is at most 1, and the rest of the cost is idle processor time.
prereqs: [speedup, work-law]
see_also: [speedup, work-efficiency, parallel-slackness, parallelism, brent-theorem, greedy-scheduling, strong-scaling, amdahls-law]
sources:
  - book: isbn:9780201648652
    title: Ananth Grama, Anshul Gupta, George Karypis and Vipin Kumar, Introduction to Parallel Computing, second edition
    locator: Chapter 5, Section 5.2 (efficiency and cost, cost-optimal systems) and the isoefficiency metric later in Chapter 5 (subsection numbers to be checked)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1 (speedup, work law and the greedy bound from which the efficiency bounds follow)
  - paper: doi:10.1109/12.21127
    title: "Derek L. Eager, John Zahorjan and Edward D. Lazowska, Speedup versus efficiency in parallel systems, IEEE Transactions on Computers 38(3), 1989"
    locator: the trade-off between speedup and efficiency in terms of the average parallelism
---

The parallel efficiency of a computation on $p$ processors is $E_p = T_1/(p\,T_p)$, its [speedup](/speedup/) divided by $p$. The product $p \cdot T_p$ is the *cost*: the number of processor-steps that the run holds, busy or idle. So the efficiency is the fraction of the cost spent on the work, and by the [work law](/work-law/) it is at most 1.

## Definition

The cost model is the [work-span model](/work-span-model/), with unit-time strands.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the time on $p$ processors under a given scheduler |
| $W/S$ | the parallelism |
| $T_{seq}$ | the time of the best known sequential program |

- The **cost** of a run on $p$ processors is $C_p = p \cdot T_p$, the product of processors and time.
- The **parallel efficiency** is $E_p = \dfrac{T_1}{p\,T_p} = \dfrac{T_1}{C_p}$.
- The **absolute efficiency** uses $T_{seq}$ in place of $T_1$: $T_{seq}/(p\,T_p)$.
- A parallel algorithm is **cost-optimal** if its cost is $p\,T_p = O(T_{seq})$, that is, if its absolute efficiency is $\Omega(1)$ (Grama, Gupta, Karypis and Kumar, Chapter 5).

**Idle time.** In each step of a run, each of the $p$ processors either runs a strand or is idle, so $p\,T_p = T_1 + I_{idle}$, where $I_{idle}$ is the number of idle processor-steps. Then $E_p = T_1/(T_1 + I_{idle})$, and:

- $E_p \le 1$, which is the work law, and $E_p = 1$ exactly when no processor is ever idle, that is, for perfect linear speedup.
- **For a greedy schedule, $I_{idle} \le (p - 1) T_\infty$.** *Proof.* A complete step has no idle processor. An incomplete step has at most $p - 1$ idle processors. A greedy schedule has at most $T_\infty$ incomplete steps (proved on [Brent's theorem](/brent-theorem/)). $\blacksquare$ So a greedy schedule has

$$E_p \ge \frac{T_1}{T_1 + (p - 1) T_\infty}.$$

With the [parallel slackness](/parallel-slackness/) $s = T_1/(p T_\infty)$, this is at least $s/(s + 1)$, close to 1 when $s$ is large.

**Upper bound from the span.** By the [span law](/span-law/), $E_p \le T_1/(p\,T_\infty)$, the slackness. So when $p$ exceeds the [parallelism](/parallelism/), the efficiency is below 1 for every scheduler, and it drops like $1/p$ as $p$ grows further.

## Examples and non-examples

**A small DAG.** The DAG of a parallel sum of four numbers has $T_1 = 10$ and $T_\infty = 5$. A greedy schedule on 2 processors takes 6 steps, so the cost is 12 and $E_2 = 10/12 \approx 0.83$. The two idle processor-steps are in the first step, which can run only the first strand, and in the last step, which can run only the final addition.

**Parallel Fibonacci of 30.** The DAG has $T_1 = 4{,}038{,}805$ and $T_\infty = 59$. The greedy bound gives an efficiency of at least 0.985 on 1,024 processors, at least 0.511 on 65,536 processors, and only about 0.064 on $10^6$ processors, where the slackness is 0.07.

**Efficiency against the best serial program.** The [Hillis-Steele scan](/hillis-steele-scan/) of $n = 2^{20}$ numbers has $T_1 = 19{,}922{,}945$ additions, and a serial loop needs $T_{seq} = 1{,}048{,}575$. A greedy run on $p$ processors has a relative efficiency close to 1 for small $p$, but its cost is at least $T_1$, so its absolute efficiency is at most $1{,}048{,}575 / 19{,}922{,}945 \approx 0.053$ for every $p$. The algorithm is not cost-optimal. The [Blelloch scan](/blelloch-scan/) has $T_1 = 2(n - 1)$, so its absolute efficiency can stay near $1/2$.

**Non-example.** Efficiency is not the fraction of processors that the program uses at its peak. A run where all processors are busy for one step and one processor works alone for many steps has a low efficiency, even though the peak use was 100 percent.

## Related definitions

- The [speedup](/speedup/) is $p \cdot E_p$.
- [Work efficiency](/work-efficiency/) asks that $T_1 = O(T_{seq})$. A work-efficient algorithm run with high efficiency is cost-optimal. A work-inefficient algorithm cannot be cost-optimal, because its cost is at least $T_1$.
- [Strong scaling](/strong-scaling/) asks how the efficiency changes as $p$ grows for a fixed problem size. [Amdahl's law](/amdahls-law/) bounds it when a fixed fraction of the work is serial.
- Grama, Gupta, Karypis and Kumar define the *isoefficiency* of an algorithm as the rate at which the problem size must grow with $p$ to keep the efficiency fixed. In the work-span model with a greedy scheduler, keeping the slackness $T_1/(p T_\infty)$ fixed is enough.

## References
