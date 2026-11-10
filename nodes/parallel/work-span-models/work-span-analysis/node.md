---
tag: K2YQ9B
kind: technique
slug: work-span-analysis
name: Work-span analysis
aliases:
- work and depth analysis
area: parallel/work-span-models
level: core
summary: Method of bounding a fork-join algorithm by two recurrences, one for its work and one for its span, and solving each with the usual recurrence tools.
prereqs: [work-and-span, recurrence-relation, master-theorem]
see_also: [work-span-model, akra-bazzi-theorem, substitution-method, recursion-tree-method, parallel-merge-sort, parallel-merge, parallel-fibonacci, brent-theorem]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1 (analysis of P-FIB and of parallel loops), Section 27.2 (matrix multiplication), Section 27.3 (P-MERGE and P-MERGE-SORT, recurrences (27.8) to (27.10)), and Exercise 4.6-2 (the master theorem with a polylogarithmic factor)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Sections 26.1 to 26.3
  - paper: doi:10.1145/227234.227246
    title: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the work and depth analysis of NESL programs
---

Work-span analysis is the method of bounding a fork-join algorithm by two [recurrences](/recurrence-relation/), one for its work $W(n)$ and one for its span $S(n)$, which are then solved separately. The recurrences come from the composition rules of the [work-span model](/work-span-model/): work adds in every case, and span adds in series and takes the maximum over the branches that run in parallel. The two solutions give the [parallelism](/parallelism/) $W/S$ and, through [Brent's theorem](/brent-theorem/), the bound $T_p \le W/p + S$.

## In plain words

Think of a job that a team does. Two questions matter. How much effort does the whole job take, if you add up the effort of every person? And how long is the longest chain of tasks where each task must wait for the one before it?

For a job made of smaller jobs, both answers come from the parts. The effort of the whole is the effort of all parts added together. For the chain, it depends on how the parts are joined. If one part must wait for another, their chains add. If two parts run at the same time, only the longer chain counts. So you write one rule for the effort and one rule for the chain, and you solve each rule the way you solve any recurrence.

## When it applies

The method applies to a program whose parallel control is spawn, sync and parallel loops, so that each run gives a series-parallel [computation DAG](/computation-dag/). It needs a cost for each serial block. The cost model is the work-span model with unit-time strands.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W(n)$, $T_1(n)$ | the work on inputs of size $n$ |
| $S(n)$, $D(n)$, $T_\infty(n)$ | the span on inputs of size $n$ |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

For a deterministic algorithm, the worst-case work and the worst-case span can come from different inputs. The method then bounds each one separately, which is still correct. For a randomized algorithm, see the pitfalls.

## The template

```pseudo id=main
WORK-SPAN-ANALYSIS(P)                         ▷ P is a fork-join procedure on inputs of size n
L1  W(n) ← ⟨base work⟩, S(n) ← ⟨base span⟩ for n ≤ ⟨base size⟩
L2  for each block B of P, in program order do
L3      if B is serial code of cost c(n) then
L4          add c(n) to W(n) and c(n) to S(n)
L5      if B is spawn C1 ... spawn Ck, sync then
L6          add W(C1) + ... + W(Ck) to W(n)
L7          add max(S(C1), ..., S(Ck)) to S(n)
L8      if B is parallel for over m iterations I1 ... Im then
L9          add W(I1) + ... + W(Im) + Θ(m) to W(n)
L10         add Θ(log m) + max(S(I1), ..., S(Im)) to S(n)
L11 solve W(n) with ⟨a method for the work recurrence⟩
L12 solve S(n) with ⟨a method for the span recurrence⟩
L13 return W(n), S(n), W(n) / S(n)
```

The holes are the base case, the cost $c(n)$ of each serial block, and the two methods for solving. Lines L6 and L7 are the two composition rules. Lines L9 and L10 come from the way a parallel loop is compiled: a balanced tree of spawns with $m$ leaves, which has $\Theta(m)$ strands and depth $\Theta(\log m)$. Usual solving methods are the [master theorem](/master-theorem/), the [Akra-Bazzi theorem](/akra-bazzi-theorem/), the [recursion-tree method](/recursion-tree-method/) and the [substitution method](/substitution-method/).

## Classic examples

The recurrences below are solved on this page, except where a source is named.

**Parallel sum** ([parallel reduce](/parallel-reduce/)). Spawn the two halves, then add:

$$W(n) = 2W(n/2) + \Theta(1) = \Theta(n), \qquad S(n) = S(n/2) + \Theta(1) = \Theta(\log n).$$

The work is case 1 of the master theorem ($a = 2$, $b = 2$, $f(n) = \Theta(1) = O(n^{1 - \epsilon})$). The span is case 2 ($a = 1$, $b = 2$, $f(n) = \Theta(1) = \Theta(n^{\log_2 1})$).

**Parallel Fibonacci** ([parallel Fibonacci](/parallel-fibonacci/)). P-FIB$(n)$ spawns P-FIB$(n-1)$ and calls P-FIB$(n-2)$:

$$W(n) = W(n-1) + W(n-2) + \Theta(1), \qquad S(n) = \max(S(n-1), S(n-2)) + \Theta(1).$$

These are not of the master-theorem form. Substitution gives $W(n) = \Theta(F_n) = \Theta(\phi^n)$ with $\phi = (1+\sqrt 5)/2$ (CLRS, third edition, Section 27.1). The span is a nondecreasing function, so the maximum is $S(n-1)$, and $S(n) = S(n-1) + \Theta(1) = \Theta(n)$. The parallelism is $\Theta(\phi^n / n)$.

**Merge sort with a serial merge.** The two calls of [merge sort](/merge-sort/) run in parallel, and the merge is the serial merge:

$$W(n) = 2W(n/2) + \Theta(n) = \Theta(n \log n), \qquad S(n) = S(n/2) + \Theta(n) = \Theta(n).$$

The work is case 2. The span is case 3 ($a = 1$, $f(n) = \Theta(n)$, and $f(n/2) = f(n)/2$ meets the regularity condition with $c = 1/2$). The parallelism is $\Theta(\log n)$.

**Parallel merge** ([parallel merge](/parallel-merge/)). P-MERGE of CLRS takes the median $x$ of the larger input, finds its place in the smaller input by [binary search](/binary-search/), and merges the two sides in parallel. Each side has at most $3n/4$ items, so

$$S(n) \le S(3n/4) + \Theta(\log n) = \Theta(\log^2 n).$$

This is not covered by case 2 of the master theorem in its basic form, which asks for $f(n) = \Theta(n^{\log_b a}) = \Theta(1)$. The extended case (CLRS, third edition, Exercise 4.6-2) covers $f(n) = \Theta(n^{\log_b a} \lg^k n)$ and gives $\Theta(n^{\log_b a} \lg^{k+1} n)$. Here $k = 1$. With $a = \lg(4/3)$, a recursion tree for $S(n) = S(3n/4) + \lg n$ has about $\lg n / a$ levels, and level $i$ costs $\lg n - i a$. The sum is close to $\lg^2 n / (2a) \approx 1.2047 \lg^2 n$.

The work satisfies $W(n) = W(\alpha n) + W((1-\alpha) n) + O(\log n)$ with $1/4 \le \alpha \le 3/4$, where $\alpha$ depends on the data. *Proof that $W(n) = O(n)$, by substitution.* Let the additive term be at most $c \lg n$. Assume $W(m) \le c_1 m - c_2 \lg m$ for all $m < n$. Then

$$W(n) \le c_1 n - c_2 \big(2 \lg n + \lg(\alpha(1 - \alpha))\big) + c \lg n.$$

For $\alpha \in [1/4, 3/4]$, the product $\alpha(1-\alpha)$ is at least $3/16$, so $\lg(\alpha(1-\alpha)) \ge -2.42$. Take $c_2 = 2c$. The right side is then at most $c_1 n - c_2 \lg n$ as soon as $c \lg n \ge 4.84 c$, that is for $n \ge 29$. Pick $c_1$ large enough that the bound holds for $n < 29$. $\blacksquare$ Each item is copied once, so $W(n) = \Omega(n)$, and $W(n) = \Theta(n)$. CLRS proves the same bound (third edition, recurrence (27.9)).

**Parallel merge sort** ([parallel merge sort](/parallel-merge-sort/)). The two calls run in parallel, and P-MERGE merges:

$$W(n) = 2W(n/2) + \Theta(n) = \Theta(n \log n), \qquad S(n) = S(n/2) + \Theta(\log^2 n) = \Theta(\log^3 n).$$

The span is again the extended case 2, now with $k = 2$ (CLRS, third edition, recurrence (27.10)). With constants: if $S(1) = 1$ and $S(2^k) = S(2^{k-1}) + k^2$, then

$$S(2^k) = 1 + \sum_{j=1}^{k} j^2 = 1 + \frac{k(k+1)(2k+1)}{6}, \qquad \frac{k^3}{3} \le S(2^k) \le \frac{k^3}{3} + k^2 + 1.$$

The bounds hold because $k(k+1)(2k+1)/6 = k^3/3 + k^2/2 + k/6$. The parallelism is $\Theta(n / \log^2 n)$, far more than the $\Theta(\log n)$ of the serial merge.

**Recursive matrix multiplication** ([parallel matrix multiplication](/parallel-matrix-multiplication/)). Eight products of half size run in parallel, then a parallel addition:

$$W(n) = 8W(n/2) + \Theta(n^2) = \Theta(n^3), \qquad S(n) = S(n/2) + \Theta(\log n) = \Theta(\log^2 n).$$

The addition of two $n \times n$ matrices by nested parallel loops has span $\Theta(\log n)$ by line L10 of the template. CLRS, third edition, Section 27.2 gives the same bounds.

## Variations

- **Coarsening.** Stop the recursion at size $g$ and run a serial loop there. The work changes only by a constant factor, and the span grows by $\Theta(g)$. This lowers the cost of spawning in practice.
- **Weighted strands.** If a serial block of cost $c$ is one strand of time $c$, the rules stay the same, with $c$ added to both measures.
- **Randomized algorithms.** For a random DAG, the work is analysed in expectation, and the span is usually bounded with high probability. A high-probability bound on the depth of the recursion, times a bound on the span of each level, then bounds the span.
- **Space.** The same method gives a recurrence for the memory of the serial run, which with the span bounds the memory of a work-stealing run (see [work stealing](/work-stealing/)).

## Pitfalls

- **The maximum in the work.** The work of a spawn and sync is the sum of the work of its branches, not the maximum. Only the span takes the maximum.
- **The sum in the span.** Two spawned branches add their work, but their spans do not add. Writing $S(n) = 2S(n/2) + \Theta(1)$ for a parallel sum gives $\Theta(n)$, which is wrong. The right recurrence is $S(n) = S(n/2) + \Theta(1)$.
- **The cost of a parallel loop.** A parallel loop over $m$ iterations is not free. It adds $\Theta(\log m)$ to the span. A loop of $n$ iterations inside each of $\log n$ levels can then dominate the span.
- **The basic master theorem.** $S(n) = S(n/2) + \Theta(\log^2 n)$ is not in case 2 of the basic master theorem, and it is not in case 3 because $\log^2 n$ is not polynomially larger than $n^0$. Use the extended case or a recursion tree.
- **Expected span.** For two random branches, $\mathbb{E}[\max(X, Y)]$ can be much larger than $\max(\mathbb{E}[X], \mathbb{E}[Y])$. A span recurrence that takes the maximum of expectations is not a correct bound on the expected span.

## Exercises

1. A procedure spawns three calls on $n/3$ items each, and then runs a serial loop of $n$ steps. Give $W(n)$ and $S(n)$. *Answer:* $W(n) = 3W(n/3) + \Theta(n) = \Theta(n \log n)$ and $S(n) = S(n/3) + \Theta(n) = \Theta(n)$.
2. Replace the serial loop of exercise 1 by a parallel loop of $n$ constant-time iterations. *Answer:* the work is still $\Theta(n \log n)$. The span is $S(n) = S(n/3) + \Theta(\log n) = \Theta(\log^2 n)$.
3. Show that a parallel loop over $n$ iterations, where iteration $i$ is a serial loop of $i$ steps, has work $\Theta(n^2)$ and span $\Theta(n)$. *Answer:* the work is $\sum_i i + \Theta(n)$. The span is $\Theta(\log n) + n$ by line L10.
4. Solve $S(n) = S(n/2) + \lg n$ with $S(1) = 1$ exactly for $n = 2^k$. *Answer:* $S(2^k) = 1 + k(k+1)/2$.

## References
