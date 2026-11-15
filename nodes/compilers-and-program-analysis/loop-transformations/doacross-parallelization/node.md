---
tag: GFEKBA
kind: technique
slug: doacross-parallelization
name: DOACROSS parallelization
aliases:
- DOACROSS loop
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Runs the iterations of a loop with carried dependences in parallel, and delays each sink with post and wait until its source in an earlier iteration is done.
prereqs: [doall-loop, loop-carried-dependence, dependence-distance-vector]
see_also: [parallel-for, lamport-hyperplane-method, wavefront-parallelism, software-pipelining, loop-skewing, barrier-synchronization, allen-kennedy-algorithm, critical-path]
sources:
  - paper: "Ron Cytron, Doacross: beyond vectorization for multiprocessors, Proceedings of the 1986 International Conference on Parallel Processing (ICPP), IEEE Computer Society, 1986, 836-844"
    locator: the DOACROSS execution model (each iteration starts a fixed delay after the one before), the delay computed from the carried dependences, and statement reordering to make the delay smaller
  - paper: doi:10.1145/7902.7904
    title: David A. Padua and Michael J. Wolfe, Advanced compiler optimizations for supercomputers, Communications of the ACM 29(12), 1986, 1184-1201
    locator: the sections on DOACROSS loops and on synchronization between iterations
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 6 (Creating Coarse-Grained Parallelism, the section on pipeline parallelism with DOACROSS loops and post and wait synchronization)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 11 (Section 11.8 on synchronization between parallel loops and Section 11.9 on pipelining)
---

DOACROSS parallelization runs the iterations of a loop on several processors at the same time, even though the loop carries dependences. Each iteration starts as soon as its processor is free, and before each statement that needs a value from an earlier iteration it waits for a signal that the earlier iteration sends after it computes that value. Cytron gave the model in 1986: iteration $i + 1$ starts a fixed *delay* after iteration $i$, and the delay is the smallest that keeps every carried dependence. When a loop carries no dependence it is a [DOALL loop](/doall-loop/) and needs no waiting at all; DOACROSS is the next step for loops in which only a small part of the body is a recurrence.

## In plain words

Think of a line of cooks who each make one cake. Every cake needs a little frosting that the cook before has to mix first, and the rest of the work does not depend on anyone. If each cook waits for the cook before to finish a whole cake, there is no gain. Instead, each cook starts at once, and only waits when they reach the frosting step, until the neighbour says "frosting done". If the frosting is a short step near the start of the recipe, the cooks overlap almost fully. If the frosting is mixed at the very end of the recipe and needed at the very start, each cook waits for the whole cake, and the line runs one cake at a time.

## When it applies

- The loop carries dependences, so it is not a [DOALL loop](/doall-loop/), but the carried dependences have constant [distances](/dependence-distance-vector/) at the level of the loop, so the compiler knows which earlier iteration each sink waits for.
- The iterations are long enough that a post and a wait cost little next to the work, and the machine has shared memory with a way to signal between processors.
- The part of the body between the sink of a carried dependence and its source (the recurrence part) is short next to the full body. The gain depends on this ratio, as the cost model below shows.

When the dependences are only loop independent, use a DOALL loop. When a loop nest has uniform dependences in two or more loops, the [hyperplane method](/lamport-hyperplane-method/) or [wavefronts](/wavefront-parallelism/) may give more parallelism with barriers instead of point-to-point signals.

## The template

Take a loop `for i = 1 to N` whose body is a straight sequence of statements $S_1, \dots, S_r$. Statement $S_q$ starts at time $a_q$ and ends at time $e_q$ inside one iteration, measured from the start of that iteration, and the whole body takes time $b = e_r$. Let $C$ be the set of dependences carried by this loop, each from a source statement $S_p$ in iteration $i$ to a sink statement $S_q$ in iteration $i + d$, with a constant distance $d \ge 1$.

```pseudo id=main
DOACROSS(loop i = 1 to N, body S_1 ... S_r, carried dependences C)
L1  for each (S_p -> S_q, distance d) in C do
L2      add "wait(p, i - d)" just before S_q          ▷ skip it when i - d < 1
L3      add "post(p, i)" just after S_p
L4  run the iterations on P processors, iteration i on processor (i mod P)
L5  each processor runs its iterations in increasing order, the body in text order
```

The wait in line L2 blocks until iteration $i - d$ has run its post for $S_p$. A post is a store to a flag (or a counter per source statement that holds the last iteration done), with a memory fence before it so that the data written by $S_p$ is visible first.

**Correctness.** Take any dependence pair. If it is loop independent, both instances are in one iteration, which runs in text order on one processor. If it is carried by an outer loop, the outer loop stays sequential, so the pair keeps its order. If it is carried by this loop, it is in $C$, and its sink waits for the post that follows its source. So every dependence keeps its order, and by the reordering theorem on the [legality page](/loop-transformation-legality/) every instance reads the same values as in the sequential loop. The waits cannot deadlock: each wait in iteration $i$ waits for an iteration $i - d < i$, and the iteration with the smallest number that has not ended never waits for a later one, so it always makes progress.

**The delay.** In Cytron's model every iteration starts a fixed delay $\delta$ after the one before, and runs without waiting. A carried dependence from $S_p$ to $S_q$ with distance $d$ is kept when the sink starts after the source ends:

$$(i + d - 1)\,\delta + a_q \ge (i - 1)\,\delta + e_p \quad\Longleftrightarrow\quad \delta \ge \frac{e_p - a_q}{d}.$$

So the smallest legal delay is $\delta = \max\bigl(0, \max_{C} \lceil (e_p - a_q) / d \rceil\bigr)$ with integer times. With $P$ processors and iteration $i$ on processor $i \bmod P$, iteration $i$ starts at $s_i = \max(s_{i-1} + \delta,\ s_{i-P} + b)$, and the loop ends at $s_N + b$. With $P \ge \lceil b / \delta \rceil$ processors this is $(N - 1)\,\delta + b$. Without waits, the sequential loop takes $N b$. So the speedup tends to $b / \delta$ for long loops, and DOACROSS gains nothing when $\delta = b$.

## Classic examples

**A short recurrence at the top.**

```
for i = 2 to N:
  S1: A[i] = A[i-1] * 2 + B[i]
  S2: C[i] = A[i] + D[i]
  S3: E[i] = C[i] * C[i] + E[i]
```

The only carried dependence is the flow dependence of $S_1$ on itself, with distance 1. Give each statement one time unit, so $a_1 = 0$, $e_1 = 1$ and $b = 3$. Then $\delta = e_1 - a_1 = 1$. For $N = 100$ iterations, the times are:

| processors | time | sequential time |
|---|---|---|
| 1 | 300 | 300 |
| 2 | 151 | 300 |
| 3 | 102 | 300 |
| 100 | 102 | 300 |

Three processors are enough, because $\lceil b / \delta \rceil = 3$. The DOACROSS code is:

```
doacross i = 2 to N:
  wait(S1, i - 1)
  S1: A[i] = A[i-1] * 2 + B[i]
  post(S1, i)
  S2: C[i] = A[i] + D[i]
  S3: E[i] = C[i] * C[i] + E[i]
```

**The recurrence spans the body.**

```
for i = 2 to N:
  S1: B[i] = A[i-1] + 1
  S2: C[i] = B[i] * 2
  S3: A[i] = C[i] + D[i]
```

The carried dependence goes from $S_3$ in iteration $i - 1$ to $S_1$ in iteration $i$, so $\delta = e_3 - a_1 = 3 = b$, and the time is $3N$ with any number of processors. The cycle $S_1 \to S_2 \to S_3 \to S_1$ is a true recurrence; no reordering of the body can shorten it.

**Reordering helps.**

```
for i = 2 to N:
  S1: X[i] = B[i] + 1
  S2: Y[i] = A[i-1] + X[i]
  S3: A[i] = B[i] * 2
```

The carried dependence goes from $S_3$ in iteration $i - 1$ to $S_2$ in iteration $i$, so with unit times $\delta = e_3 - a_2 = 3 - 1 = 2$. No dependence inside one iteration involves $S_3$, so $S_3$ can move to the top of the body. In the order $S_3, S_1, S_2$, the delay is $\max(0, 1 - 2) = 0$: the source ends before the sink of the next iteration could start, and the iterations need no delay at all. A self-dependence, as in the first example, gives the length of the statement whatever its place. Cytron's paper studies this choice of statement order.

## Variations

- **Post and wait against a fixed delay.** The fixed delay of the cost model assumes equal times in every iteration. Real code uses post and wait, which adapts to iterations of different length; the delay formula then gives the time when all iterations take the same time.
- **Counters instead of flags.** One counter per source statement that holds the last iteration posted uses $O(1)$ memory. It needs the posts of one source to happen in iteration order, which holds when each source posts in order or when the loop is split among processors in order.
- **Pipeline parallelism.** Split the body into stages and give each stage its own processor; the iterations flow through the stages. Allen and Kennedy treat DOACROSS and this split together in their chapter on coarse-grained parallelism. It is the thread-level analogue of [software pipelining](/software-pipelining/).
- **Alignment and skewing.** When all carried distances can be made zero by shifting statements across iterations (loop alignment) or by [loop skewing](/loop-skewing/) in a nest, the loop becomes DOALL and needs no waits.
- **Wavefronts.** In a nest with distances $(1, 0)$ and $(0, 1)$, a DOACROSS outer loop with waits on the neighbour row runs the same diagonals as the [hyperplane method](/lamport-hyperplane-method/), but with point-to-point signals instead of a barrier per front.

## Pitfalls

- **A missing fence.** On a machine with a weak memory model, a post that becomes visible before the data of the source lets the sink read a stale value. Put a release fence before the post and an acquire fence after the wait.
- **A wait that is never posted.** If the source statement is under a condition that may be false, its post must still run on every path, or the sink waits forever.
- **A distance that is not constant.** The template needs to know which earlier iteration to wait for. If the distance depends on $i$ or is unknown, wait for every earlier iteration, which makes the loop sequential.
- **Expecting a speedup from a long recurrence.** The speedup is at most $b / \delta$. When the carried dependence goes from the end of the body to its start, $\delta = b$ and DOACROSS runs the loop sequentially, with extra synchronization cost.
- **Too many processors.** More than $\lceil b / \delta \rceil$ processors gives no gain in the cost model, because each iteration still starts $\delta$ after the one before.

## Exercises

1. In the first example, give $S_1$ a time of 2 units and the others 1. Find $\delta$, the number of processors that is enough, and the time for $N = 100$.
2. A loop has carried dependences $S_3 \to S_1$ with distance 2 and $S_2 \to S_2$ with distance 1, with unit times. Find $\delta$.
3. Show that if every carried dependence has distance at least $d_0$ and the body takes time $b$, then $\delta \le \lceil b / d_0 \rceil$.
4. Explain why the waits cannot deadlock even when two different source statements post in different orders.

## References
