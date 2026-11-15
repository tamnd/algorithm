---
tag: 3XKRGT
kind: technique
slug: loop-unrolling
name: Loop unrolling
aliases:
- loop unwinding
area: compilers-and-program-analysis/loop-transformations
level: intro
summary: Replicates the body of a loop k times and divides the trip count by k, which cuts branch overhead and exposes instruction parallelism.
prereqs: [natural-loop, data-dependence]
see_also: [strip-mining, loop-interchange, loop-fusion, software-pipelining, vectorization, instruction-scheduling-problem, register-allocation-problem, loop-carried-dependence]
sources:
  - paper: doi:10.1002/spe.4380090307
    title: Jack J. Dongarra and A. R. Hinds, Unrolling loops in FORTRAN, Software, Practice and Experience 9(3), 1979, 219-226
    locator: the unrolled loop with a cleanup loop for the leftover iterations, and measurements of the gain on several computers and compilers
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Section 17.4.3 (Loop Unrolling), the unrolling factor and the rolled copy for the leftover iterations, as a step that gives the scheduler more freedom
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 8 (Improving Register Usage), Section 8.4 (Unroll-and-Jam) and its legality condition
---

Loop unrolling replaces the body of a loop by $k$ copies of it, for the iterations $i, i+1, \dots, i+k-1$, and steps the index by $k$. A short *remainder loop* runs the last $n \bmod k$ iterations when the trip count $n$ is not a multiple of $k$. The program runs the same body instances in the same order, so unrolling is always legal and it changes no [data dependence](/data-dependence/). What it changes is the cost: one test and one increment now serve $k$ iterations, and the $k$ copies form one long block that the [instruction scheduler](/instruction-scheduling-problem/) can overlap. The price is code size and, often, more registers. [Strip mining](/strip-mining/) has the same shape with a loop around the copies instead of written-out copies.

## In plain words

A loop does two kinds of work on each turn: the real work, and the bookkeeping of the loop itself, which is a test, a jump and an increment of the counter. If you write the real work four times in a row inside the loop, the bookkeeping happens once for every four pieces of work. The work is the same, and it happens in the same order, so the result cannot change. When the number of turns is not a multiple of four, a small second loop does the last few turns one at a time. The four copies side by side also let the processor start the next piece of work before the previous one ends. The cost is a longer program, and the short second loop.

## When it applies

Take a counted loop `for i = L to U: BODY(i)` that runs the iterations $L, L+1, \dots, U$ in this order, or none if $U < L$. Unrolling by a factor $k \ge 2$ needs three facts:

- **(U1) Fixed bounds.** $L$ and $U$ are evaluated once, before the loop, and BODY does not assign $i$. This is the meaning of a counted `for` loop. A loop written as a `while` loop must first be found as a [natural loop](/natural-loop/) and recognized as a counted loop, with [induction variable analysis](/induction-variable-analysis/).
- **(U2) No overflow.** The test $i + k - 1 \le U$ is computed without overflow. With machine integers and $U$ near the largest value, write it as $i \le U - k + 1$ and guard the case $U - k + 1 < $ the smallest value.
- **(U3) Single exit.** The only exit is the loop test. If BODY can leave the loop (a `break`, a `return`, a trap), each copy keeps its exit, and the proof below still holds, because the copies run in the original order.

No dependence test is needed. That is the point of the technique: it is a pure change of the control code.

## The template

```pseudo id=main
UNROLL(for i = L to U: BODY(i), factor k)
L1  i <- L
L2  while i + k - 1 <= U do          ▷ main loop: one test for k iterations
L3      BODY(i); BODY(i + 1); ... ; BODY(i + k - 1)
L4      i <- i + k
L5  while i <= U do                  ▷ remainder loop: at most k - 1 iterations
L6      BODY(i)
L7      i <- i + 1
```

The holes are the body BODY, the bounds $L$ and $U$, and the factor $k$. Inside line L3 each copy uses $i + c$ in place of $i$, and a compiler usually gives each copy fresh names for its temporaries, so that the copies do not reuse one register.

**Legality.** Under (U1) to (U3), the code above runs exactly the instances $\mathrm{BODY}(L), \mathrm{BODY}(L+1), \dots, \mathrm{BODY}(U)$, in this order, and nothing else except the updates of $i$. This is proved below. Two runs that execute the same sequence of statement instances from the same state pass through the same states, so the result, the traps and the final memory are the same. Since the order of all instances is unchanged, every dependence keeps its source before its sink, and the [legality theorem](/loop-transformation-legality/) is not even needed.

**Proof.** At each arrival at line L2, the invariant is: the instances run so far are $\mathrm{BODY}(L), \dots, \mathrm{BODY}(i-1)$ in order, and $L \le i$. It holds at the start with $i = L$. If the test of L2 is true, then $i + k - 1 \le U$, so line L3 runs the next $k$ instances, all of them in the range, and line L4 restores the invariant with $i + k$. Each pass raises $i$ by $k$, so the main loop ends. When it ends, $i + k - 1 > U$, so at most $U - i + 1 \le k - 1$ instances are left. Lines L5 to L7 run them one by one, in order, with the invariant "the instances run so far are $\mathrm{BODY}(L), \dots, \mathrm{BODY}(i-1)$", and stop when $i = U + 1$. If $U < L$, both tests fail at once and nothing runs, as in the original loop. In both cases $i$ ends with the value the original loop leaves, $U + 1$ or $L$.

**Profit.** The cost model is the number of instructions executed. In the toy IR below, the original loop executes $5n + 6$ instructions for $n$ iterations. The loop unrolled by 4 executes $12q + 5r + 9$, where $q = \lfloor n/4 \rfloor$ and $r = n \bmod 4$: each main iteration does the work of four iterations in 12 instructions instead of 20. The second gain is not counted here: the four copies form one block with no branch, so a scheduler can overlap their loads and arithmetic, and a [vectorizer](/vectorization/) or [software pipelining](/software-pipelining/) can work on them.

**Costs.** The code grows by about $k$ times the body. A large body unrolled many times can stop fitting in the instruction cache. Fresh names for the temporaries of each copy raise the register pressure, and spills can cost more than the saved branches. A loop with a short trip count runs mostly in the remainder loop, and then unrolling makes it slower.

## Classic examples

**A sum in the toy IR.** The parameter is `n`. The original loop adds $0 + 1 + \dots + (n-1)$:

```
entry:
  i = 0
  s = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  s = s + i
  i = i + 1
  jump head
exit:
  ret s
```

Unrolled by 4, with the remainder loop in `head1` and `body1`:

```
entry:
  i = 0
  s = 0
  jump head4
head4:
  j = i + 3
  t = j < n
  br t body4 head1
body4:
  s = s + i
  i1 = i + 1
  s = s + i1
  i2 = i + 2
  s = s + i2
  i3 = i + 3
  s = s + i3
  i = i + 4
  jump head4
head1:
  t = i < n
  br t body1 exit
body1:
  s = s + i
  i = i + 1
  jump head1
exit:
  ret s
```

The test `i + 3 < n` is line L2 of the template for $L = 0$ and $U = n - 1$. The counts of executed instructions, with each instruction and each terminator counted as 1:

| $n$ | return value | original | unrolled by 4 |
|---|---|---|---|
| 0 | 0 | 6 | 9 |
| 3 | 3 | 21 | 24 |
| 4 | 6 | 26 | 21 |
| 10 | 45 | 56 | 43 |
| 100 | 4950 | 506 | 309 |

For $n = 10$ the main loop runs twice ($i = 0$ and $i = 4$) and the remainder loop runs twice ($i = 8$ and $i = 9$). For $n \le 3$ the unrolled loop is slower: it pays for one failed main test and does all the work in the remainder loop.

**A recurrence keeps its dependences.** In `for i = 1 to n: A[i] = A[i-1] + 1`, the instance for $i$ reads the value that the instance for $i - 1$ wrote: a [loop-carried](/loop-carried-dependence/) flow dependence with distance 1. Unrolled by 2, the body is `A[i] = A[i-1] + 1; A[i+1] = A[i] + 1` and $i$ steps by 2. The pairs of dependent instances are the same. What changes is how they are labeled: the dependence from the first copy to the second copy is now loop independent, and the dependence from the second copy to the first copy of the next iteration is carried by the new loop with distance 1. The chain of dependences is as long as before, so unrolling cannot make this loop run in parallel.

**Unroll and jam.** For a nest `for i: for j: C[i] = C[i] + A[i][j] * B[j]`, unroll the outer loop by 2 and fuse the two copies of the inner loop: `for i step 2: for j: C[i] += A[i][j]*B[j]; C[i+1] += A[i+1][j]*B[j]`. Each load of `B[j]` now serves two rows. This is not plain unrolling, because the instances $(i+1, j)$ now run before $(i, j+1)$. It is a reordering, and Allen and Kennedy give its legality test. A dependence with distance $(d_1, d_2)$, $0 < d_1 < k$ and $d_2 < 0$, has its source and sink in one group of $k$ outer iterations, and the jammed order runs the sink first. Every other dependence keeps its order. So unroll and jam by $k$ is legal if no dependence has direction $(<, >)$ with an outer distance less than $k$, which holds in this example: the only dependences are on `C[i]`, with outer distance 0.

## Variations

- **Remainder first.** Run the $n \bmod k$ leftover iterations before the main loop instead of after it. Duff's device in C writes the leftover part as a `switch` that jumps into the middle of the unrolled body.
- **Complete unrolling.** If the trip count is a small constant, replace the loop by straight-line code with no test at all. This often enables [constant folding](/constant-folding/) of the index expressions.
- **Unknown trip counts.** A `while` loop whose trip count is not known can still be unrolled: keep the exit test after each copy. Only the jump back to the header is saved.
- **Unroll and jam.** Unroll an outer loop and fuse the copies of the inner loop, as in the example. It improves register reuse, and its legality is a dependence condition.
- **Partial sums.** For a reduction, some compilers give each copy its own accumulator and add the accumulators at the end. This is a separate transformation, not part of unrolling: it changes the order of the additions.

## Pitfalls

- **Off-by-one in the main test.** The main loop must stop when fewer than $k$ iterations are left. Testing $i \le U$ instead of $i + k - 1 \le U$ runs copies past the end of the range.
- **Overflow of the test.** $i + k - 1$ can overflow when $U$ is near the largest machine integer, and a wrapped value makes the test true. Compute $U - k + 1$ once, with a guard.
- **Floating-point partial sums.** Several accumulators change the result of a floating-point sum. For the values $10^{16}, 1, -10^{16}, 1$ the sum in order is $1$, because $10^{16} + 1$ rounds to $10^{16}$. With one accumulator for the even positions and one for the odd positions it is $0 + 2 = 2$. A compiler must not do this without permission to reassociate.
- **Expecting parallelism.** Unrolling does not remove a loop-carried dependence. It only moves some dependences inside the body, where they are still dependences.
- **Too large a factor.** A factor that makes the body larger than the instruction cache, or that needs more registers than the machine has, makes the loop slower. Typical factors are 2 to 8.

## Exercises

1. A loop with $L = 1$ and $U = 13$ is unrolled by 4. How many times do the main loop and the remainder loop run? *Answer.* The main loop runs for $i = 1, 5, 9$, so three times, and stops at $i = 13$, because $13 + 3 > 13$. The remainder loop runs once, for $i = 13$.
2. In the toy IR example, for which $n$ is the unrolled loop slower than the original? *Answer.* It is slower when $12q + 5r + 9 > 5n + 6$. With $n = 4q + r$ this is $3 > 8q$, so exactly when $q = 0$, that is, for $n \le 3$.
3. A loop has a flow dependence with distance 3. It is unrolled by 2. What are the distances, counted in iterations of the new loop? *Answer.* The source in the first copy (an even offset) and the sink are 3 old iterations apart, which is the second copy of the next new iteration: distance 1. A source in the second copy has its sink in the first copy two new iterations later: distance 2. The instance pairs are the same as before.
4. Why is unroll and jam of `for i: for j: A[i][j] = A[i-1][j+1] + 1` by 2 illegal? *Answer.* The dependence has distance $(1, -1)$, direction $(<, >)$, and outer distance $1 < 2$. The instance $(i+1, j)$ reads $A[i][j+1]$, which $(i, j+1)$ writes. After the jam, $(i+1, j)$ runs before $(i, j+1)$ when $i$ is the first row of a group, so it reads the old value.

## References
