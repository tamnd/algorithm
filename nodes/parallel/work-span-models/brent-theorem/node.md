---
tag: XNKPT4
kind: theorem
slug: brent-theorem
name: Brent's theorem
aliases:
- Brent's lemma
- greedy scheduling bound
- Brent's principle
- WT scheduling principle
area: parallel/work-span-models
level: core
summary: A computation with work T_1 and span T_infinity can be run on p processors in time at most T_1/p + T_infinity, and any greedy schedule does so.
prereqs: [work-law, span-law, computation-dag]
see_also: [greedy-scheduling, parallel-slackness, parallelism, work-stealing, blumofe-leiserson-bound, list-scheduling-bound, pram-model, expression-dag]
sources:
  - paper: doi:10.1145/321812.321815
    title: "Richard P. Brent, The parallel evaluation of general arithmetic expressions, Journal of the ACM 21(2), 1974"
    locator: Lemma 2 (a computation of t steps and q operations runs in t + (q - t)/p steps on p processors) and the main theorem on expressions in n variables (pp. 201-206 for the paper)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, Theorem 27.1 (inequality (27.4)) with its proof by complete and incomplete steps, Corollaries 27.2 and 27.3, Exercise 27.1-3, and the chapter notes
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms
    locator: Chapter 1, the work-time framework and the WT scheduling principle (section number to be checked)
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the statement that any greedy schedule runs in time at most T_1/P + T_infinity
---

Brent's theorem says that a computation with work $T_1$ and span $T_\infty$ can be run on $p$ processors in time $T_p \le T_1/p + T_\infty$, and that any greedy schedule reaches this bound. Brent (1974) proved a lemma about the evaluation of arithmetic expressions: a computation of $t$ steps and $q$ operations on unbounded processors can be done in $t + (q - t)/p$ steps on $p$ processors. The scheduling form for computation DAGs is the modern reading of that lemma, and this page proves both. With the [work law](/work-law/) and the [span law](/span-law/), it pins $T_p$ between $\max(T_1/p, T_\infty)$ and $T_1/p + T_\infty$.

## Statement

The cost model is the [work-span model](/work-span-model/). The hypotheses are:

- the computation is a [computation DAG](/computation-dag/) of unit-time strands;
- there are $p \ge 1$ identical processors, and each runs at most one strand per step;
- scheduling is free: at each step the scheduler knows which strands are ready and can give them to processors at no cost;
- there is no cost for memory or communication.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work, the number of strands |
| $S$, $D$, $T_\infty$ | the span, the number of strands on a longest path |
| $T_p$ | the number of steps of a schedule on $p$ processors |
| $W/S$ | the parallelism |

A schedule is *greedy* if at each step it runs $\min(p, r)$ strands, where $r$ is the number of ready strands. A step is *complete* if it runs $p$ strands and *incomplete* otherwise (the terms of CLRS, third edition).

**Theorem (Brent's theorem, scheduling form).** Each greedy schedule of a computation DAG with work $T_1$ and span $T_\infty$ on $p$ processors takes

$$T_p \le \frac{T_1 - T_\infty}{p} + T_\infty \le \frac{T_1}{p} + T_\infty.$$

In particular, such a schedule exists for each DAG and each $p$.

**Brent's lemma (the original form, Brent 1974, Lemma 2).** If a computation can be done in $t$ steps with $q$ operations in total on a machine with enough processors, then it can be done in $t + (q - t)/p$ steps with $p$ processors.

**PRAM form.** An algorithm in the work-time framework of the [PRAM](/pram-model/) that does $W$ operations in $t$ parallel steps can be run on a $p$-processor PRAM in at most $\lfloor W/p \rfloor + t$ steps, if processor allocation is free, that is, if each processor can find out at no cost which operations it does in each step. JáJá calls this the WT scheduling principle.

The three statements share one idea, but they are not the same theorem. The original lemma and the PRAM form start from a given schedule with unbounded processors and slow it down. The scheduling form speaks of any greedy schedule of a DAG. Brent's paper is about arithmetic expressions and does not use the words work, span or greedy.

## In plain words

A team works on a project where some tasks wait for others. The rule is simple: never let a worker sit idle while some task is ready.

At each moment one of two things is true. Either every worker is busy, and then the team gets through a full share of the work. Or some worker is idle, and then every ready task is being done at that moment, so the longest chain of waiting tasks gets one task shorter. The first kind of moment can happen only so often, because the total work is limited. The second kind can happen only as often as the length of the longest chain. So the time is at most the work shared by the workers, plus the length of the longest chain.

## Proof

**The scheduling form, by complete and incomplete steps.** Fix a greedy schedule on $p$ processors. Let $C$ be the number of complete steps and $I$ the number of incomplete steps, so $T_p = C + I$.

For $t \ge 1$, let $G_t$ be the sub-DAG of the strands that have not run before step $t$, so $G_1 = G$. A strand is ready at step $t$ exactly when it is a source of $G_t$, that is, when all its predecessors have run.

*Incomplete steps.* At an incomplete step $t$ the scheduler runs fewer than $p$ strands, and since it is greedy, it runs all ready strands, which are all the sources of $G_t$. Let $P$ be any path of $G_{t+1}$, and let $v$ be its first strand. Then $v$ was not a source of $G_t$, because all those sources ran at step $t$. So $v$ has a predecessor $u$ in $G_t$, and $u$ followed by $P$ is a path of $G_t$. So each path of $G_{t+1}$ has at most $S(G_t) - 1$ strands, and

$$S(G_{t+1}) \le S(G_t) - 1.$$

At a complete step, $G_{t+1}$ is a sub-DAG of $G_t$, so $S(G_{t+1}) \le S(G_t)$. The span starts at $S(G_1) = T_\infty$, it never grows, it drops by at least one at each incomplete step, and it is at least 1 before each step, because $G_t$ is not empty while strands are left. So $I \le T_\infty$.

*Complete steps.* Each complete step runs $p$ strands and each incomplete step runs at least one, and each strand runs once, so $pC + I \le T_1$. Then

$$T_p = C + I \le \frac{T_1 - I}{p} + I = \frac{T_1}{p} + \Big(1 - \frac{1}{p}\Big) I \le \frac{T_1}{p} + \Big(1 - \frac{1}{p}\Big) T_\infty = \frac{T_1 - T_\infty}{p} + T_\infty,$$

where the last inequality uses $I \le T_\infty$ and $1 - 1/p \ge 0$. The right side is at most $T_1/p + T_\infty$. A greedy schedule exists for each DAG: at each step, run any $\min(p, r)$ of the $r$ ready strands, and there is always a ready strand while strands are left, because a nonempty DAG has a source. $\blacksquare$

This is the proof of CLRS, third edition, Theorem 27.1, with the sharper count $pC + I \le T_1$ of Exercise 27.1-3 in place of $C \le \lfloor T_1/p \rfloor$.

**Brent's lemma, level by level.** Take the schedule with enough processors, and let $s_i$ be the number of operations in step $i$, so $\sum_{i=1}^{t} s_i = q$ and each $s_i \ge 1$ (a step with no operation can be dropped). On $p$ processors, run the $s_i$ operations of step $i$ in $\lceil s_i/p \rceil$ steps, after all operations of earlier steps and before all operations of later steps. Each operation still runs after the operations it needs, so this is a valid schedule. Since $\lceil s/p \rceil \le (s - 1)/p + 1$ for each integer $s \ge 1$,

$$\sum_{i=1}^{t} \Big\lceil \frac{s_i}{p} \Big\rceil \le \sum_{i=1}^{t} \Big( \frac{s_i - 1}{p} + 1 \Big) = \frac{q - t}{p} + t. \qquad \blacksquare$$

For a computation DAG, take the schedule that runs each strand $v$ at step $d(v)$, the number of strands on a longest path that ends at $v$. It has $t = T_\infty$ steps and $q = T_1$ operations, so the lemma gives the same bound $T_\infty + (T_1 - T_\infty)/p$ by a schedule that goes level by level. That schedule need not be greedy: it can leave a processor idle at the end of a level while a strand of the next level is ready.

**The PRAM form.** Step $i$ of the work-time algorithm has $W_i$ operations. If processor allocation is free, $p$ processors do them in $\lceil W_i/p \rceil \le \lfloor W_i/p \rfloor + 1$ steps. The sum over the $t$ steps is at most $\sum_i \lfloor W_i/p \rfloor + t \le \lfloor W/p \rfloor + t$. $\blacksquare$

## Consequences

- **Within a factor 2 of optimal.** Each schedule has $T_p \ge \max(T_1/p, T_\infty)$ by the work law and the span law, and $T_1/p + T_\infty \le 2\max(T_1/p, T_\infty)$. So each greedy schedule is within a factor 2 of the best schedule (CLRS, third edition, Corollary 27.2). The sharper factor $2 - 1/p$ and the link with Graham's list scheduling are on [greedy scheduling](/greedy-scheduling/).
- **Near linear speedup with slackness.** If $p \ll T_1/T_\infty$, then $T_\infty \ll T_1/p$, so $T_p \approx T_1/p$ and the speedup is close to $p$ (CLRS, Corollary 27.3). The page [parallel slackness](/parallel-slackness/) makes this exact: the efficiency is at least $1 - 1/s$ for slackness $s$.
- **Design with unbounded processors.** One can design an algorithm for unbounded processors, bound its work and span, and get a time bound for any $p$ from the theorem. This is how the [work-span model](/work-span-model/) and the work-time framework of the PRAM separate the algorithm from the processor count.
- **Arithmetic expressions.** Brent's main theorem uses the lemma to show that an arithmetic expression in $n$ variables with addition, multiplication and division can be evaluated in time $4 \log_2 n + 10(n - 1)/p$ on $p$ processors (Brent 1974). This page does not prove that result.
- **Work stealing.** A real scheduler does not know the ready set for free. Randomized [work stealing](/work-stealing/) reaches $\mathbb{E}[T_p] \le T_1/p + O(T_\infty)$ in expectation (see the [Blumofe-Leiserson bound](/blumofe-leiserson-bound/)). That bound is cited, not proved here.

## Tightness

**For greedy schedules, the bound is exact.** Take a chain of $k$ strands and $pk$ other strands with no edges. Then $T_1 = k + pk$ and $T_\infty = k$, so the bound is $(T_1 - T_\infty)/p + T_\infty = 2k$. A greedy schedule that always prefers the independent strands runs $p$ of them in each of the first $k$ steps, and the chain waits, so the chain needs $k$ more steps. The schedule takes $2k$ steps, which is the bound. A better greedy schedule runs one chain strand in each step and finishes in $k + \lceil k/p \rceil$ steps.

**For the best schedule, the bound is tight up to less than one step.** Take a chain of $k$ strands, followed by $pk$ strands that each depend on the last strand of the chain. Then $T_1 = k + pk$ and $T_\infty = k + 1$. Each schedule needs $k$ steps for the chain and then at least $k$ steps for the $pk$ strands, so it takes at least $2k$ steps, and the bound is $(T_1 - T_\infty)/p + T_\infty = 2k + 1 - 1/p$.

**The term $T_\infty$ cannot be dropped, and neither can the term $T_1/p$**, by the span law on a chain and the work law on an antichain.

## History

Brent (1974) proved the lemma as a step toward fast parallel evaluation of arithmetic expressions. The paper restructures an expression to depth $O(\log n)$ and then uses the lemma to bound the time on $p$ processors. Graham (1966, 1969) had proved that any list schedule of tasks with precedence constraints on $m$ machines has makespan at most $(2 - 1/m)$ times the optimum (see [Graham's bound](/list-scheduling-bound/)). For unit-time strands, a greedy schedule is a list schedule, so Graham's work gives the same kind of bound. The chapter notes of CLRS, third edition, say that Graham and Brent showed that schedulers exist that reach the bound of Theorem 27.1, and that Blumofe and Leiserson showed that any greedy scheduler reaches it. JáJá (1992) states the PRAM form as the WT scheduling principle. The name "Brent's theorem" for the scheduling form $T_p \le T_1/p + T_\infty$ is the modern usage, not the title of a result in Brent's paper.

## References
