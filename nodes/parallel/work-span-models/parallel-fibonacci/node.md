---
tag: SX5BQA
kind: algorithm
slug: parallel-fibonacci
name: Parallel Fibonacci
aliases:
- P-FIB
area: parallel/work-span-models
level: intro
summary: Multithreaded recursive computation of Fibonacci numbers that spawns one recursive call, used to illustrate work, span and parallelism.
solves: [fibonacci-numbers]
model: work-span-model
complexity:
  vars: {n: the index of the Fibonacci number}
  time: {worst: Θ(φ^n)}
  depth: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
prereqs: [fibonacci-numbers, fork-join-model, work-and-span]
see_also: [fibonacci-fast-doubling, matrix-fibonacci, work-span-analysis, parallelism, work-stealing, determinacy-race]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1 (the procedures FIB and P-FIB, Figure 27.2 for the DAG of P-FIB(4), and the analysis of its work, span and parallelism)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (the basics of fork-join parallelism, with P-FIB as the first example)
  - paper: doi:10.1145/277650.277725
    title: "Matteo Frigo, Charles E. Leiserson and Keith H. Randall, The implementation of the Cilk-5 multithreaded language, PLDI 1998"
    locator: the fib program as an example of a Cilk procedure and as a benchmark of the spawn overhead
---

Parallel Fibonacci, called P-FIB in CLRS, computes the [Fibonacci number](/fibonacci-numbers/) $F_n$ by the naive recursion, but it [spawns](/fork-join-model/) the call for $F_{n-1}$ so that it runs in parallel with the call for $F_{n-2}$. Its work is $4F_{n+1} - 3 = \Theta(\varphi^n)$ and its span is $2n$, so its [parallelism](/parallelism/) is $\Theta(\varphi^n / n)$, where $\varphi = (1 + \sqrt 5)/2$. It is a teaching example for [work and span](/work-and-span/), not a good way to compute $F_n$: a serial method such as [fast doubling](/fibonacci-fast-doubling/) uses $O(\log n)$ arithmetic operations.

## In plain words

The slow way to get a Fibonacci number asks for the two numbers before it, and each of those asks for the two numbers before it, and so on. This makes a huge tree of small questions. The two questions at each point do not depend on each other, so two workers can answer them at the same time.

The parallel program starts the first question as a separate task, answers the second one itself, then waits for the first answer and adds the two. The total amount of work is as large as in the slow serial program. But the longest chain of steps that must happen one after the other is short: it follows one path down the tree. So many processors can share the work, and the program is a good small example of how to measure parallel cost.

## The problem

The input is an integer $n \ge 0$. The output is $F_n$, where $F_0 = 0$, $F_1 = 1$ and $F_k = F_{k-1} + F_{k-2}$ for $k \ge 2$. The cost model is the [work-span model](/work-span-model/) with the strand counting of CLRS. A call with $n \le 1$ is one unit strand. A call with $n \ge 2$ is three unit strands: $A$ up to the spawn, $B$ from the spawn to the second call, and $C$ after the sync.

| Symbol | Meaning |
|---|---|
| $n$ | the index of the Fibonacci number (the input) |
| $p$ | the number of processors |
| $W = T_1$ | the work: the number of strands |
| $S = T_\infty$ | the span: the number of strands on a longest path |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

## The algorithm

```pseudo id=main
P-FIB(n)
L1  if n ≤ 1 then return n
L2  x ← spawn P-FIB(n − 1)          ▷ may run in parallel with line L3
L3  y ← P-FIB(n − 2)
L4  sync                             ▷ wait for the spawned call
L5  return x + y
```

If the keywords spawn and sync are deleted, the result is the serial program FIB, its *serial elision*. P-FIB computes the same value as FIB. Line L3 is a plain call: spawning it too would add a task but no parallelism, because line L4 waits for it at once. The DAG of a call with $n \ge 2$ has the edges $A \to B$, $A \to$ P-FIB$(n-1)$, $B \to$ P-FIB$(n-2)$, and an edge from the end of each call to $C$.

## Example

For $n = 4$, the DAG has $W = 17$ strands: 3 for each of the 4 calls with $n \ge 2$ (P-FIB(4), P-FIB(3) and two calls of P-FIB(2)), and 1 for each of the 5 calls with $n \le 1$. Write $A_k$, $B_k$ and $C_k$ for the strands of a call P-FIB$(k)$ on the leftmost branch. A longest path is $A_4, A_3, A_2, B_2$, P-FIB(0), $C_2, C_3, C_4$, with $S = 8$ strands. It goes down through the spawned calls, takes the extra strand $B_2$ before the call of P-FIB(0), and comes back up through the three $C$ strands. So the parallelism is $17/8 = 2.125$, and by the [work law](/work-law/) and the [span law](/span-law/) no number of processors can give a [speedup](/speedup/) above 2.125 on this input.

| $n$ | $F_n$ | $W = 4F_{n+1} - 3$ | $S$ | $W/S$ |
|---|---|---|---|---|
| 2 | 1 | 5 | 4 | 1.25 |
| 3 | 2 | 9 | 6 | 1.50 |
| 4 | 3 | 17 | 8 | 2.13 |
| 6 | 8 | 49 | 12 | 4.08 |
| 10 | 55 | 353 | 20 | 17.65 |
| 20 | 6765 | 43781 | 40 | 1094.53 |
| 30 | 832040 | 5385073 | 60 | 89751.22 |

The parallelism grows fast with $n$. At $n = 30$ it is about 90000, so the program has enough parallel slackness for any machine.

## Correctness

P-FIB$(n)$ returns $F_n$ by strong induction on $n$: line L1 handles $n \le 1$, lines L2 and L3 give $F_{n-1}$ and $F_{n-2}$ by the hypothesis, and the sync of line L4 makes sure that $x$ is final before line L5 adds it. The program has no [determinacy race](/determinacy-race/): the two calls touch only their own locals, and the caller reads $x$ and $y$ only after the sync. So every schedule gives the same result. The full proof is below.

## Complexity

The work satisfies $W(0) = W(1) = 1$ and $W(n) = W(n-1) + W(n-2) + 3$, and the solution is

$$W(n) = 4F_{n+1} - 3 = \frac{4\varphi}{\sqrt 5}\,\varphi^n + O(1) = \Theta(\varphi^n).$$

The span satisfies $S(0) = S(1) = 1$ and $S(n) = \max(S(n-1) + 2,\ S(n-2) + 3)$ for $n \ge 2$, because a path through the spawned call passes $A$ and $C$, and a path through the second call passes $A$, $B$ and $C$. The solution is $S(n) = 2n$ for $n \ge 2$. So the parallelism is

$$\frac{W(n)}{S(n)} = \frac{4F_{n+1} - 3}{2n} = \Theta\!\left(\frac{\varphi^n}{n}\right).$$

The proofs of both closed forms are in the proof file. By [Brent's theorem](/brent-theorem/), a greedy scheduler runs P-FIB$(n)$ in $T_p \le W/p + S = \Theta(\varphi^n/p + n)$ steps, and [work stealing](/work-stealing/) does so in expectation up to the constant of the $S$ term. This is linear speedup for each $p = O(\varphi^n/n)$. The extra space on one processor is $\Theta(n)$ for the stack.

## Properties

- **Deterministic.** The result does not depend on the schedule, because the program has no determinacy race.
- **Work-inefficient against the best serial method.** The work is the same as that of the naive serial recursion, $\Theta(\varphi^n)$, but the best serial methods use $O(\log n)$ arithmetic operations. Compared with them, P-FIB is exponentially wasteful.
- **Unit-cost arithmetic.** The analysis counts an addition as one step. $F_n$ has about $0.694\,n$ binary digits, so this is right only while $F_n$ fits in a machine word. That holds for all $n \le 93$ with 64-bit unsigned words, and P-FIB is already too slow long before $n$ is large.
- **Another strand count.** Some pages count two strands for a call with $n \ge 2$, one up to the spawn and one after the sync, as on the [fork-join model](/fork-join-model/). Then $W(n) = 3F_{n+1} - 2$ and $S(n) = 2n - 1$ for $n \ge 1$, so for $n = 30$ the DAG has 4,038,805 strands and span 59. The asymptotic forms do not change.
- **Two calls of unequal size.** The spawned call P-FIB$(n-1)$ is larger than the called one, so the spawned side is on the critical path.

## Variants and improvements

- **Coarsening.** Below a cut-off $k$, call the serial FIB. This cuts the number of spawns by a factor of about $\varphi^k$, and the span becomes $\Theta(n + \varphi^k)$. Practical fork-join code usually coarsens its base case in this way.
- **Fast serial methods.** [Fast doubling](/fibonacci-fast-doubling/) and the [matrix method](/matrix-fibonacci/) compute $F_n$ with $O(\log n)$ multiplications. In the unit-cost model, the matrix method by [repeated squaring](/matrix-power/) has work and span both $\Theta(\log n)$, which is far better than P-FIB in both measures.
- **Memoized recursion.** A table of $F_0, \ldots, F_n$ gives $\Theta(n)$ work, but each entry depends on the two before it, so its span is also $\Theta(n)$: it has no parallelism.

## When to use it

Use P-FIB to teach and to test: it shows spawn, sync, the DAG model and the work and span recurrences in five lines, and it is a standard stress test for the spawn overhead of a fork-join runtime. Do not use it to compute Fibonacci numbers.

## Pitfalls

- **Taking the example as a good algorithm.** Its high parallelism comes from its exponential work. A large parallelism says nothing about speed when the work is far above the work of the best serial method.
- **Spawning both calls.** Spawning line L3 too adds overhead, and the sync of line L4 follows at once, so the span does not drop.
- **Reading x before the sync.** If line L5 ran before the sync, $x$ could still be missing. This is a determinacy race, and the result would depend on the schedule.
- **No coarsening.** Without a serial base case of a reasonable size, almost all of the time goes to the overhead of the spawns, and the measured speedup is poor.
- **Mixing cost conventions.** With the strand counting of CLRS the span is exactly $2n$ for $n \ge 2$. A model that charges each spawn, call and return separately gives $cn + d$ with other constants. Compare exact counts only within one convention.

## Implementations

## History

The naive recursive Fibonacci program, with the first recursive call spawned, was an example program and a benchmark of the spawn overhead in the Cilk-5 paper of Frigo, Leiserson and Randall (1998). CLRS used it as P-FIB, the first example of its chapter on multithreaded algorithms, in the third edition (2009), and again in the fourth edition (2022).

## References
