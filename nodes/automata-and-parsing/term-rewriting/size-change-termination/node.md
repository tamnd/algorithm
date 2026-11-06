---
tag: WBRKWD
kind: algorithm
slug: size-change-termination
name: Size-change termination
aliases:
- SCT
- size-change principle
area: automata-and-parsing/term-rewriting
level: research
summary: Decides termination of first-order functional programs by checking size-change graphs.
solves: [termination-decision-problem]
model: word-ram
complexity:
  vars: {F: the number of functions, p: the largest number of parameters, k: the number of size-change graphs}
  time: {worst: O(k F^2 3^(p^2) p^4)}
  space: {extra: O(F^2 3^(p^2) p^2)}
properties: {deterministic: true, recursive: false}
prereqs: [termination, dependency-pairs, well-founded-relation]
see_also: [termination-decision-problem, undecidability-of-termination, recursive-path-ordering, polynomial-interpretation, ramsey-theorem, transitive-closure, strongly-connected-components]
sources:
  - paper: doi:10.1145/360204.360210
    title: Chin Soon Lee, Neil D. Jones and Amir M. Ben-Amram, The size-change principle for program termination, 28th ACM Symposium on Principles of Programming Languages (POPL 2001)
    locator: pp. 81 to 92 (size-change graphs, the closure algorithm with idempotent graphs, and PSPACE-completeness)
  - paper: doi:10.1007/s00200-005-0179-7
    title: René Thiemann and Jürgen Giesl, The size-change principle and dependency pairs for termination of term rewriting, Applicable Algebra in Engineering, Communication and Computing 16(4) (2005)
    locator: pp. 229 to 270
  - paper: doi:10.1145/1180475.1180480
    title: Amir M. Ben-Amram and Chin Soon Lee, Program termination analysis in polynomial time, ACM Transactions on Programming Languages and Systems 29(1) (2007)
    locator: pp. 1 to 37 (the polynomial-time subclass SCP)
---

**Size-change termination** proves that a program or a rewrite system terminates by looking only at how the sizes of arguments change from one call to the next. Each call is summarized by a small graph that says which arguments of the call are smaller than, or not larger than, which parameters of the caller. The program is size-change terminating if every infinite sequence of calls would make some value decrease infinitely often, which is impossible in a well-founded order. Lee, Jones and Ben-Amram (2001) showed that this condition is decidable by a closure computation, and that deciding it is PSPACE-complete.

## In plain words

A recursive function stops if something gets smaller each time it calls itself and cannot get smaller forever, like a natural number. The hard cases are functions that swap their arguments, or call each other in turns, so that no single argument decreases in every call.

The method writes down, for each call, which arguments shrink and which stay at most the same, and where each one goes. It then combines these notes along every possible chain of calls. If every chain that can repeat forever makes some value shrink again and again, the program cannot run forever. If some repeating chain lets every value stay the same, the method reports it.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

**Size-change graphs.** A program has functions $f, g, \ldots$, each with parameters $1, \ldots, p_f$. A size-change graph $G : f \to g$ describes one call from $f$ to $g$. It has arcs $i \xrightarrow{\downarrow} j$, meaning that argument $j$ of the call is strictly smaller than parameter $i$ of $f$, and arcs $i \xrightarrow{=} j$, meaning that it is smaller or equal, in some fixed well-founded order. Between each pair $i, j$ there is at most one arc. The graphs are computed from the program by a separate analysis, which must be sound: every arc must hold in every run.

**Composition.** For $G : f \to g$ and $H : g \to h$, the graph $G ; H : f \to h$ has an arc $i \to k$ if $G$ has $i \to j$ and $H$ has $j \to k$ for some $j$; the arc is strict if, for some such $j$, one of the two arcs is strict.

**Threads.** A multipath is an infinite sequence of graphs $G_1 G_2 \cdots$ with $G_t : f_t \to f_{t+1}$, as given by an infinite sequence of calls. A thread is a sequence of parameters $x_s, x_{s+1}, \ldots$ from some $s$ on, with an arc $x_t \to x_{t+1}$ in $G_t$ for every $t \ge s$. It is **infinitely descending** if infinitely many of these arcs are strict.

**Input.** A finite set $\mathcal{G}$ of size-change graphs.

**Question.** Is $\mathcal{G}$ **size-change terminating** (SCT), that is, does every multipath built from $\mathcal{G}$ have an infinitely descending thread?

If $\mathcal{G}$ is SCT and the graphs are sound, the program terminates: an infinite run gives a multipath, its infinitely descending thread gives values $v_s \ge v_{s+1} \ge \cdots$ with infinitely many strict steps, and no [well-founded order](/well-founded-relation/) has such a chain.

## The algorithm

```pseudo id=main
SIZE-CHANGE-TERMINATES(𝒢)
L1  S ← 𝒢; W ← 𝒢                       ▷ S is the closure, W the work list
L2  while W is not empty do
L3      G ← remove a graph from W        ▷ G : f → g
L4      for each H in 𝒢 with H : g → h do
L5          K ← G ; H
L6          if K ∉ S then add K to S and to W
L7  for each G in S with G : f → f do
L8      if G ; G = G then                ▷ G is idempotent
L9          if G has no strict arc i → i then return "not SCT", with witness G
L10 return "SCT"
```

Lines L1 to L6 compute the closure $S$, the set of compositions $G_1 ; \cdots ; G_n$ of all finite walks in $\mathcal{G}$. Lines L7 to L9 look for an idempotent graph that allows a call cycle with no descent. The implementation also records, for each graph of $S$, a walk that produces it, so a negative answer comes with a concrete call sequence.

**From rewriting.** Thiemann and Giesl (2005) apply the principle to term rewriting through [dependency pairs](/dependency-pairs/). For a dependency pair $F(s_1, \ldots, s_n) \to G(t_1, \ldots, t_m)$, put $i \xrightarrow{\downarrow} j$ if $t_j$ is a proper subterm of $s_i$, and $i \xrightarrow{=} j$ if $t_j = s_i$. The subterm relation is well-founded, so SCT of these graphs, together with the conditions of the dependency pair method, proves termination.

## Example

**A permuting function.** Take $p(m, n, r) = $ if $r > 0$ then $p(m, r - 1, n)$ else if $n > 0$ then $p(r, n - 1, m)$ else $m$, on natural numbers. Its two calls give

$$G_1 : m \xrightarrow{=} m,\ r \xrightarrow{\downarrow} n,\ n \xrightarrow{=} r, \qquad G_2 : r \xrightarrow{=} m,\ n \xrightarrow{\downarrow} n,\ m \xrightarrow{=} r.$$

No single parameter decreases in both calls, and in $G_1$ the values of $n$ and $r$ swap. The closure has 22 graphs. Four are idempotent graphs $p \to p$:

| walk | arcs | strict self arc |
| --- | --- | --- |
| $G_2 G_2$ | $m \xrightarrow{=} m$, $n \xrightarrow{\downarrow} n$, $r \xrightarrow{=} r$ | $n$ |
| $G_1 G_1$ | $m \xrightarrow{=} m$, $n \xrightarrow{\downarrow} n$, $r \xrightarrow{\downarrow} r$ | $n$, $r$ |
| $G_2 G_1 G_1 G_2$ | $m \xrightarrow{\downarrow} m$, $n \xrightarrow{\downarrow} n$, $r \xrightarrow{=} r$ | $m$, $n$ |
| a walk of length 8 | $m \xrightarrow{\downarrow} m$, $n \xrightarrow{\downarrow} n$, $r \xrightarrow{\downarrow} r$ | all |

Each has a strict self arc, so the answer is SCT, and $p$ terminates. For instance, $G_1 ; G_1$ has $n \xrightarrow{=} r \xrightarrow{\downarrow} n$, so two calls of the first kind decrease $n$.

**A swap.** $f(x, y) = f(y, x)$ gives $G : x \xrightarrow{=} y,\ y \xrightarrow{=} x$. Then $G ; G = \{x \xrightarrow{=} x,\ y \xrightarrow{=} y\}$ is idempotent with no strict arc, so the answer is "not SCT", with the walk $G G$ as witness; indeed $f$ loops. With $f(x, y) = f(y, x - 1)$, the graph is $x \xrightarrow{\downarrow} y,\ y \xrightarrow{=} x$, and $G ; G = \{x \xrightarrow{\downarrow} x,\ y \xrightarrow{\downarrow} y\}$, so the answer is SCT.

**Ackermann.** The [dependency pairs](/dependency-pairs/) of $A(0, y) \to s(y)$, $A(s(x), 0) \to A(x, s(0))$, $A(s(x), s(y)) \to A(x, A(s(x), y))$ give the graphs $\{1 \xrightarrow{\downarrow} 1\}$ twice and $\{1 \xrightarrow{=} 1,\ 2 \xrightarrow{\downarrow} 2\}$. Every composition keeps an arc $1 \to 1$, strict unless only the third graph is used, and then $2 \xrightarrow{\downarrow} 2$ is there. So the system is SCT.

## Correctness

The proof has two parts; the full version is below.

1. **Closure.** Lines L1 to L6 stop, because there are at most $3^{p^2}$ arc sets for each pair of functions, and they compute exactly the set of compositions $G_w$ of nonempty walks $w$: each new graph is a walk extended by one graph, and each walk extension is tried when its prefix is removed from $W$. By induction on the length of $w$, $G_w$ has an arc $i \to j$ iff some thread through $w$ goes from $i$ to $j$, strict iff some such thread has a strict arc.
2. **The idempotent test.** If an idempotent $G = G_w : f \to f$ has no strict arc $i \to i$, then the multipath $w w w \cdots$ has no infinitely descending thread: such a thread would return to one parameter $x$ after $k$ periods with a strict arc in between, so $G^k = G$ would have the strict arc $x \to x$. Conversely, given any multipath, color each pair of times $s < t$ by the composition of the graphs between them. By Ramsey's theorem there are times $t_0 < t_1 < \cdots$ whose pairs all have the same color $G$; then $G : f \to f$, $G ; G = G$, and its strict arc $x \to x$ gives a strict thread segment from each $t_i$ to $t_{i+1}$, which join to an infinitely descending thread.

## Complexity

Let $F$ be the number of functions, $p$ the largest number of parameters and $k = |\mathcal{G}|$.

- **Closure size.** Each pair $(i, j)$ has no arc, a non-strict arc or a strict arc, so $|S| \le F^2 \cdot 3^{p^2}$.
- **Time.** Each graph of $S$ is composed with at most $k$ graphs, and a composition of graphs with at most $p^2$ arcs costs $O(p^4)$ by the double loop of the implementation ($O(p^3)$ with arrays). The total is $O(k F^2 3^{p^2} p^4)$, exponential in $p^2$ but polynomial in the number of functions and calls for fixed $p$.
- **Space.** $O(F^2 3^{p^2} p^2)$ for the closure.
- **Hardness.** Deciding SCT is PSPACE-complete (Lee, Jones and Ben-Amram, 2001), so the exponential worst case cannot be avoided unless PSPACE = P. In practice functions have few parameters and the closures are small.

## Properties

- **Decides SCT exactly.** The answer is exact for the graphs given; the only loss of precision is in building the graphs from the program.
- **Sound for termination.** If the graphs are sound for a well-founded order, "SCT" implies termination. "Not SCT" does not imply non-termination; it means that size changes alone cannot show termination.
- **Certificate for failure.** A negative answer gives a walk $w$ such that $w w w \cdots$ has no descending thread.
- **Order independent.** The test does not need a ranking function, a lexicographic order of arguments, or an order of the functions. It finds termination by lexicographic descent and by descent on permuted arguments automatically.

## Variants and improvements

- **SCP.** Ben-Amram and Lee (2007) gave a polynomial-time sufficient condition, size-change termination in polynomial time, which covers most programs met in practice.
- **Ramsey-based antichains.** The closure can be pruned by keeping only graphs that are not subsumed by others, as in the antichain methods for Büchi automata inclusion, since SCT is an inclusion question between two Büchi automata.
- **Monotonicity constraints.** Graphs can also record relations between parameters of the same call, such as $x > y$, which gives a more precise but more expensive test.
- **Combined with dependency pairs.** Size-change graphs with orders stronger than the subterm order, such as path orders, and inside the dependency pair framework (Thiemann and Giesl, 2005).

## When to use it

Use size-change termination for first-order recursive functions, especially when the decreasing argument changes from call to call or when arguments are permuted, as in the example above. It is used in proof assistants and in partial evaluators, where it must work without user annotations. For term rewriting systems with nested calls and without a simple subterm descent, path orders and interpretations inside the dependency pair framework are stronger; SCT is one method among several in termination tools.

## Pitfalls

- **Unsound graphs.** An arc $i \xrightarrow{\downarrow} j$ must hold on every call, including calls under a guard that the analysis cannot see. A wrong strict arc gives a wrong "terminates".
- **Threads may start late.** A thread need not start at the first call. Checking only threads from the first call misses descents of values that appear later.
- **Idempotent only.** Checking every graph $f \to f$ of $S$ for a strict self arc is too strong: in the swap $f(x, y) = f(y, x - 1)$ the graph $G$ itself has no self arc, yet the program terminates. Only idempotent graphs must have one.
- **Exponential closure.** On functions with many parameters the closure can be large; bound it or use SCP.

## Implementations

## History

Lee, Jones and Ben-Amram introduced the size-change principle in 2001, with the closure algorithm and the proof that the problem is PSPACE-complete. Thiemann and Giesl (2005) combined it with the dependency pair method for term rewriting. Ben-Amram and Lee (2007) gave the polynomial-time subclass SCP.

## References
