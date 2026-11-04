---
tag: WJYZSF
kind: problem
slug: floyd-cycle-detection
name: Cycle detection
aliases:
- cycle finding
- linked list cycle
area: data-structures/linear-structures
level: intro
summary: Decide whether a list or iterated function has a cycle, and locate where it begins.
prereqs: [linked-list, functional-graph]
see_also: [brent-cycle-detection, cycle-detection, pollard-rho, brent-pollard-rho, functional-graph, list-reversal, circular-linked-list, hash-table]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.1 (Random numbers), exercises 6 and 7 and their answers, on finding the period of an eventually periodic sequence with bounded memory, and the credit of the two-pointer method to R. W. Floyd
  - paper: "Richard P. Brent, An improved Monte Carlo factorization algorithm, BIT 20 (1980)"
    locator: Section 2, the cycle-finding method with powers of two, and the comparison with Floyd's method
  - paper: "John M. Pollard, A Monte Carlo method for factorization, BIT 15 (1975)"
    locator: the use of Floyd's cycle-finding method on the sequence x -> x^2 + c mod n
  - paper: "Robert Sedgewick, Thomas G. Szymanski and Andrew C. Yao, The complexity of finding cycles in periodic functions, SIAM Journal on Computing 11(2) (1982)"
    locator: the trade-off between memory and function evaluations, with upper and lower bounds
  - paper: "Gabriel Nivasch, Cycle detection using a stack, Information Processing Letters 90(3) (2004)"
    locator: the stack algorithm and its bounds on the stopping time and the stack size
---

Cycle detection is the problem of deciding whether the sequence $x_0, f(x_0), f(f(x_0)), \ldots$ of a function $f$ on a finite set ever repeats, and if it does, finding where the repeating part starts and how long it is. A [linked list](/linked-list/) is the case $f(v) = v.next$, where reaching NIL means there is no cycle. On a finite set the sequence always ends in a cycle, so its shape is the Greek letter $\rho$: a tail of length $\mu$ followed by a cycle of length $\lambda$. Floyd's tortoise and hare method finds both numbers in $O(\mu + \lambda)$ time with two pointers and $O(1)$ memory, and Brent's method does the same with fewer evaluations of $f$. The problem is the core of Pollard's rho methods for factoring and discrete logarithms and of collision search.

## In plain words

Two runners start at the same place on a track that may have a loop at its end. One runs one step at a time and the other runs two steps at a time. If the track has no loop, the fast runner reaches the end first. If it has a loop, both end up running around it, and the fast runner gains one step on the slow one each turn, so they must meet.

Once they meet, you can also find where the loop starts. Put one runner back at the start and let both run one step at a time. They meet again exactly at the first place of the loop. Neither runner needs to remember where it has been, which is the point.

## Definition

**Input.** A function $f : S \to S$ on a finite set $S$, given as a procedure that can only be called, and a start value $x_0 \in S$. The sequence is $x_{i+1} = f(x_i)$. Values can be compared for equality. For a linked list, $S$ is the set of nodes with NIL added, and $f(\text{NIL}) = \text{NIL}$.

**The $\rho$ shape.** Since $S$ is finite, some value repeats. Let $\mu \ge 0$ be the least index such that $x_\mu$ appears again later, and $\lambda \ge 1$ the least number with $x_{\mu + \lambda} = x_\mu$. Then

$$x_i = x_j \text{ for } i < j \iff i \ge \mu \text{ and } \lambda \mid (j - i),$$

and the values $x_0, \ldots, x_{\mu + \lambda - 1}$ are distinct. The tail is $x_0, \ldots, x_{\mu - 1}$ and the cycle is $x_\mu, \ldots, x_{\mu + \lambda - 1}$. In the [functional graph](/functional-graph/) of $f$, this is the path from $x_0$ into its cycle.

**The questions.** (1) For a list: does the walk from $x_0$ reach NIL, or does it enter a cycle? (2) In general: find $\mu$ and $\lambda$, or find $x_\mu$, the start of the cycle. (3) For collision search: find $i \ne j$ with $x_i \ne x_j$ and $f(x_i) = f(x_j)$, which exists when $\mu \ge 1$.

The cost is measured in evaluations of $f$ and in memory cells, since $f$ may be expensive and $S$ may be huge, as in the integers modulo a large number.

## Variants

- **Linked list cycle.** Decide only whether the list has a cycle, with $O(1)$ extra memory and without changing the nodes.
- **Find the start of the cycle**, $x_\mu$: the node where the list enters its cycle, or the first repeated value.
- **Find the period** $\lambda$ only, as in testing the period of a pseudo-random generator.
- **Collision finding.** Find two different inputs with the same image under $f$; for $\mu \ge 1$, they are $x_{\mu - 1}$ and $x_{\mu + \lambda - 1}$.
- **Parallel collision search.** Many processors walk from different starts and report only *distinguished points*, values with a rare easy property, to a central table.
- **Cycles in a directed graph** in general, where a vertex has many successors, is a different problem, solved by depth-first search; see [cycle detection](/cycle-detection/) in graphs.

## Examples

**A linked list.** Nodes $0, 1, \ldots, 7$ with $i.next = i + 1$ for $i < 7$ and $7.next = 3$. So $\mu = 3$ and $\lambda = 5$. Floyd's first phase moves the tortoise $t$ one step and the hare $h$ two steps:

| step | $t$ | $h$ |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 6 |
| 4 | 4 | 3 |
| 5 | 5 | 5 |

They meet at step 5, at $x_5$; the index 5 is a multiple of $\lambda$. The second phase puts $t$ back at node 0 and moves both by one: after 3 steps both are at node 3, so $\mu = 3$. The third phase walks $h$ around the cycle from node 3 until it returns, which takes $\lambda = 5$ steps. The three phases use $15 + 6 + 5 = 26$ evaluations of $f$.

**A function.** Take $f(x) = (x^2 + 1) \bmod 255$ and $x_0 = 3$. The sequence is $3, 10, 101, 2, 5, 26, 167, 95, 101, \ldots$, so $\mu = 2$ and $\lambda = 6$: the cycle is $101, 2, 5, 26, 167, 95$.

**No cycle.** On the list $0 \to 1 \to 2 \to \text{NIL}$, the hare reaches NIL after two double steps, and the answer is "no cycle".

## Known algorithms

- **Hash set of visited values.** Insert $x_0, x_1, \ldots$ in a [hash table](/hash-table/) with their indices until a value repeats. It finds $\mu$ and $\lambda$ with exactly $\mu + \lambda$ evaluations, but uses $\Theta(\mu + \lambda)$ memory.
- **Floyd's tortoise and hare.** Phase 1: set $t = f(x_0)$ and $h = f(f(x_0))$, and while $t \ne h$, set $t = f(t)$ and $h = f(f(h))$. They meet at $x_\nu = x_{2\nu}$, where $\nu$ is the least multiple of $\lambda$ with $\nu \ge \max(\mu, 1)$, so $\nu \le \mu + \lambda$. Phase 2: set $t = x_0$ and step both $t$ and $h$ by one until $t = h$; the number of steps is $\mu$, since $x_{\mu + \nu} = x_\mu$. Phase 3: step $h$ alone from $t$ until it returns; the count is $\lambda$. It uses $O(1)$ memory and at most $3\nu + 2\mu + \lambda \le 6(\mu + \lambda)$ evaluations. For a list, phase 1 stops with "no cycle" when $h$ meets NIL.
- **[Brent's algorithm](/brent-cycle-detection/).** Keep a saved value and compare it with the walking pointer; at each power of two, move the saved value to the pointer's place. This finds $\lambda$ directly, then $\mu$ with a second walk. It uses $O(1)$ memory and fewer evaluations of $f$ than Floyd's method, since each step evaluates $f$ once, not three times.
- **Gosper's algorithm.** Keep $O(\log(\mu + \lambda))$ saved values, chosen by the binary representation of the index, and compare each new value with them. It finds $\lambda$ soon after the cycle is entered, but does not find $\mu$ directly.
- **Nivasch's stack algorithm (2004).** Keep a stack of the values smaller than all later values seen so far, and stop when a value equals the top of the stack. It stops after at most $\mu + 2\lambda$ steps, with a stack of expected size $O(\log(\mu + \lambda))$ for a random function.
- **Sedgewick, Szymanski and Yao (1982).** With $M$ memory cells, an algorithm that keeps values at a spacing chosen from $M$ uses $(\mu + \lambda)(1 + O(1/\sqrt{M}))$ evaluations.
- **List reversal.** For a linked list that may be changed, [reversing the list](/list-reversal/) in place returns to the original head exactly when there is a cycle, and a second reversal restores it.

## Bounds

**Evaluations.** Every algorithm needs at least $\mu + \lambda$ evaluations to see the first repeat: before that, the values seen are distinct and consistent with a longer tail. The hash set method meets this bound with $\Theta(\mu + \lambda)$ memory. With $O(1)$ memory, Floyd's and Brent's methods use $O(\mu + \lambda)$ evaluations, a constant factor more. Sedgewick, Szymanski and Yao studied the exact trade-off between memory and evaluations and proved lower bounds of the same form as their upper bound.

**Random functions.** If $f$ is a uniform random function on a set of $N$ elements, the expected tail length and the expected cycle length are both $\sqrt{\pi N / 8} + O(1) \approx 0.627\sqrt{N}$, and the expected $\rho$ length $\mu + \lambda$ is about $\sqrt{\pi N / 2} \approx 1.253\sqrt{N}$. This $\Theta(\sqrt{N})$ is the birthday bound, and it is why Pollard's rho method finds a factor $p$ of $n$ in about $\sqrt{p}$ steps.

## Reductions

- **[Pollard's rho factorization](/pollard-rho/).** Iterate $f(x) = x^2 + c \bmod n$. Modulo an unknown prime factor $p$ of $n$, the sequence has a $\rho$ of length about $\sqrt{p}$. Floyd's method, with the test $\gcd(x_{2i} - x_i, n) > 1$ in place of equality, finds the factor. Brent's version, [Brent-Pollard rho](/brent-pollard-rho/), uses his cycle method.
- **Pollard's rho for discrete logarithms** finds a collision of a walk in a cyclic group, which gives the logarithm.
- **Collision search for hash functions.** For $f$ a hash function cut to $b$ bits, a collision is found in $O(2^{b/2})$ evaluations and $O(1)$ memory.
- **Structure of functional graphs.** Every component of the [functional graph](/functional-graph/) of $f$ is a cycle with trees hanging off it; cycle detection finds the cycle of one component.

## Applications

- **Corrupt or circular linked lists**: checking that a walk will stop before running it, in memory managers and in kernel lists.
- **The period of a pseudo-random generator**, or of any deterministic simulation, to detect that it has fallen into a loop.
- **Integer factoring and discrete logarithms**, through the rho methods above.
- **Cryptanalysis**: collision and meet-in-the-middle attacks with small memory.
- **Puzzles and iterated maps**, such as the happy numbers or the aliquot sequences, where each value determines the next.

## References
