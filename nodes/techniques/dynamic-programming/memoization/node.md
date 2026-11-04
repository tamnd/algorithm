---
tag: 1B1KF8
kind: technique
slug: memoization
name: Memoization
aliases:
- memoisation
- top-down dynamic programming
area: techniques/dynamic-programming
level: intro
summary: Cache the results of recursive calls so each subproblem is solved only once.
prereqs: [recursion, overlapping-subproblems, optimal-substructure]
see_also: [tabulation, subproblem-graph, traceback, hash-table, packrat-parsing, rod-cutting-problem, weighted-interval-scheduling, fibonacci-numbers]
sources:
  - paper: doi:10.1038/218019a0
    title: Donald Michie, "Memo" functions and machine learning, Nature 218, 1968
    locator: pp. 19 to 22
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (MEMOIZED-CUT-ROD and the top-down method) and Section 14.3 (the subsection on memoization, MEMOIZED-MATRIX-CHAIN)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 6.1 (M-Compute-Opt, memoizing the recursion for weighted interval scheduling) and Section 6.2
---

Memoization is the technique of storing the result of each call of a recursive function in a table, keyed by the arguments, so that a later call with the same arguments returns the stored result instead of computing it again. Applied to a recurrence with [overlapping subproblems](/overlapping-subproblems/), it solves each distinct subproblem once, and the running time drops from the size of the recursion tree to the size of the [subproblem graph](/subproblem-graph/). It is the top-down form of dynamic programming; the bottom-up form is [tabulation](/tabulation/). Donald Michie named it in 1968, for what he called "memo" functions.

## In plain words

A function that calls itself can end up asking the same question many times. Each time it works out the answer from scratch. Memoization adds a notebook. Before the function does any work, it looks in the notebook. If the answer is there, it returns it at once. If not, it computes the answer in the usual way, writes it in the notebook, and returns it.

You keep the recursive code as it is, and you add only the lookup at the start and the write at the end. Each different question is then answered once. The total work is the number of different questions times the work for one question, not the number of times the questions are asked.

## When it applies

Look for these signals.

- You have a correct recursive definition of the answer: a recurrence that follows from [optimal substructure](/optimal-substructure/), or a counting rule.
- The naive recursion is slow because it calls itself on the same arguments many times.
- The number of distinct argument values that can occur is small, for example polynomial in the input size.
- The function is pure: its result depends only on its arguments and on input that does not change during the run.
- The dependencies have no cycle: a call on $x$ never needs, directly or indirectly, a call on $x$ itself.

Memoization is the better choice over [tabulation](/tabulation/) when only a small part of the possible subproblems is reached from the goal, or when an order for a bottom-up loop is hard to find.

## The template

The holes are BASE, BASE-VALUE, CHOICES, SUB and COMBINE. The table *memo* starts empty, and it lives for one input only.

```pseudo id=main
MEMO-SOLVE(x)                              ▷ returns f(x); memo is shared by all calls
L1  if x ∈ memo then return memo[x]
L2  if BASE(x) then
L3      v ← BASE-VALUE(x)
L4  else
L5      v ← COMBINE over c ∈ CHOICES(x) of (c, MEMO-SOLVE(SUB(x, c)))
L6  memo[x] ← v
L7  return v
```

Lines L2 to L5 are the plain recursive algorithm. Line L1 and line L6 are the only additions. For a minimization, COMBINE takes the minimum of a cost of the choice $c$ plus the value of the subproblem; for a count, it takes a sum.

**Correctness.** Let $f$ be the function that the recurrence defines. The invariant is: whenever $memo[y]$ is set, $memo[y] = f(y)$. It holds at the start, since $memo$ is empty. Line L6 is the only write. Prove by induction on the subproblem order (each SUB$(x, c)$ is smaller than $x$, and the order has no infinite descending chain) that a call MEMO-SOLVE$(x)$ returns $f(x)$. If L1 returns, the invariant gives $f(x)$. Otherwise, each recursive call in L5 is on a smaller subproblem, so it returns the right value by the induction hypothesis, and L5 computes $v = f(x)$ by the recurrence. So the write in L6 keeps the invariant, and L7 returns $f(x)$.

**Cost.** Lines L2 to L6 run at most once for each distinct subproblem $x$, because after the first run $x \in memo$ and later calls stop at L1. A call that stops at L1 is charged to the caller that made it. So the total time is

$$ \sum_{x \text{ reached}} O\bigl(1 + |\mathrm{CHOICES}(x)|\bigr) \cdot t, $$

where $t$ is the cost of one lookup or one write in $memo$ plus the cost of one choice. With an array indexed by the subproblem, $t$ is $O(1)$ in the worst case; with a [hash table](/hash-table/), it is $O(1)$ expected. The sum is over the subproblems that are reachable from the goal, which can be far fewer than all subproblems. The space is the size of $memo$ plus the stack, whose depth is the length of the longest chain of calls.

### Walk-through: rod cutting

Take the prices $p_1, \ldots, p_{10} = 1, 5, 8, 9, 10, 17, 17, 20, 24, 30$ of CLRS Section 14.1 and the recurrence $r_j = \max_{1 \le i \le j}(p_i + r_{j-i})$, $r_0 = 0$. The plain recursion makes $2^n$ calls. With a memo, the call on $j$ does real work once and then makes $j$ calls, so the total number of calls is $1 + \sum_{j=1}^{n} j = 1 + n(n+1)/2$, and the time is $\Theta(n^2)$.

For $n = 4$, the call on 4 calls 3, which calls 2, which calls 1, which calls 0. Each of these is the first call on its argument. On the way back, the call on 1 stores $r_1 = 1$. The call on 2 then calls 0 a second time, which is a lookup, and stores $r_2 = \max(1 + 1, 5 + 0) = 5$. The call on 3 looks up 1 and 0 and stores $r_3 = \max(1 + 5, 5 + 1, 8 + 0) = 8$. The call on 4 looks up 2, 1 and 0 and stores $r_4 = \max(1 + 8, 5 + 5, 8 + 1, 9 + 0) = 10$. There are 11 calls in all, against 16 for the plain recursion. For $n = 10$ there are 56 calls against 1024, and $r_{10} = 30$.

## Classic examples

- **[Fibonacci numbers](/fibonacci-numbers/).** The plain recursion makes $2F(n+1) - 1$ calls. With a memo, it makes $2n - 1$ calls for $n \ge 1$. For $n \ge 2$, $n + 1$ of them compute a new value and $n - 2$ are lookups. For $n = 30$ that is 59 calls against 2692537.
- **[Rod cutting](/rod-cutting-problem/).** MEMOIZED-CUT-ROD of CLRS Section 14.1, as in the walk-through. The time drops from $2^n$ to $\Theta(n^2)$.
- **[Weighted interval scheduling](/weighted-interval-scheduling/).** Kleinberg and Tardos, Section 6.1, memoize the recurrence $\mathrm{OPT}(j) = \max(v_j + \mathrm{OPT}(p(j)), \mathrm{OPT}(j - 1))$ as M-Compute-Opt. The plain recursion can take exponential time; with the memo, the time is $O(n)$ once the intervals are sorted and $p(j)$ is known.
- **[Matrix-chain multiplication](/matrix-chain-multiplication/).** MEMOIZED-MATRIX-CHAIN of CLRS Section 14.3 reduces $3^{n-1}$ calls to $O(n^3)$ time over the $\Theta(n^2)$ ranges.
- **[Text segmentation](/text-segmentation/).** "Can the suffix that starts at position $i$ be split into dictionary words?" depends only on $i$, so a memo keyed by $i$ makes a recursion with exponentially many paths run in polynomial time.
- **[Packrat parsing](/packrat-parsing/).** A recursive-descent parser for a parsing expression grammar memoizes the result of each rule at each input position. The parse then takes time linear in the input length, for a fixed grammar.

## Variations

- **Array or hash table.** When the subproblems are indexed by small integers, an array with a sentinel for "not yet computed" is fastest. When they are tuples, strings or sets, use a [hash table](/hash-table/). A set of up to 64 items can be a bit mask, as in [bitmask DP](/bitmask-dp/).
- **Library memoization.** Python has `functools.cache` and `functools.lru_cache`. These wrap a function and key the table by its arguments. The arguments must be hashable.
- **Memoize the choice too.** Store the best choice next to the value, so that [traceback](/traceback/) can rebuild an optimal solution without a second search.
- **Explicit stack.** To avoid a deep call stack, run the same algorithm with an explicit stack of pending subproblems, or solve the subproblems in increasing order first. The second form is [tabulation](/tabulation/).
- **Memoization with pruning.** In a search for an optimum, a memo can also store bounds. This is the base of transposition tables in game-tree search.
- **Lazy tables.** In a lazy functional language, a table whose entries are defined by the recurrence is computed on demand. Each entry is evaluated at most once, which is memoization without explicit lookups.

## Pitfalls

- **A sentinel that is also a value.** If "not computed" is 0 and $f(x) = 0$ is common, each such $x$ is computed again at each call, and the time can become exponential again. Use a value that $f$ cannot take, such as `None`, or a separate flag.
- **A key with too much in it.** If the key includes an argument that does not change the answer, such as a path so far or a counter, the distinct keys can be as many as the calls, and the memo gains nothing. The key must be exactly the state of the subproblem.
- **A key with too little in it.** If the key leaves out an argument that does change the answer, two different subproblems share one entry, and the result is wrong. For a [knapsack](/knapsack-problem/), the key must hold both the item index and the remaining capacity.
- **Cycles.** If the subproblem graph has a cycle, the recursion never ends, and a memo does not help, because the value is written only after the call returns. Shortest paths in a graph with cycles need [Bellman-Ford](/bellman-ford/) or [Dijkstra's algorithm](/dijkstra/), not a memoized recursion on vertices.
- **Deep recursion.** The stack depth is the longest chain of subproblems. In CPython the default limit is 1000 frames, so a memoized Fibonacci function called once on 2000 with an empty memo raises `RecursionError`. Raise the limit with care, warm the memo in increasing order, or use tabulation.
- **A memo that outlives its input.** A global memo, or a cache on a function that reads a global input, gives wrong answers when the input changes between runs. Clear the memo for each input, or put the input in the key.
- **A cache that evicts.** A bounded cache such as `lru_cache(maxsize=128)` may evict entries that are needed again, and the time bound above no longer holds. Use an unbounded cache for DP.

## Exercises

1. Memoize the recursion for [longest common subsequence](/longest-common-subsequence/) of two strings of lengths $m$ and $n$. Prove that it makes $O(mn)$ calls, and give a pair of strings for which it reaches far fewer than $(m+1)(n+1)$ subproblems.
2. The binomial coefficient satisfies $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$. Count the calls of the plain recursion for $\binom{n}{k}$ and of the memoized one. Show that the plain recursion makes $2\binom{n}{k} - 1$ calls when the base cases are $\binom{m}{0} = \binom{m}{m} = 1$.
   <details><summary>Hint</summary>Each leaf of the recursion tree returns 1, so there are $\binom{n}{k}$ leaves, and each inner node has two children.</details>
3. Let $f(n) = f(\lfloor n/2 \rfloor) + f(\lfloor n/3 \rfloor) + f(\lfloor n/4 \rfloor)$ for $n \ge 1$, and $f(0) = 1$. Show that a memoized recursion with a hash table reaches only $O(\log^2 n)$ distinct arguments, so it runs fast for $n = 10^{18}$, while a table of size $n$ is impossible.
   <details><summary>Hint</summary>Each argument reached is $\lfloor n / (2^a 3^b) \rfloor$ for some $a$ and $b$, since $\lfloor \lfloor n/u \rfloor / v \rfloor = \lfloor n/(uv) \rfloor$.</details>
4. Write a memoized recursion for the minimum number of coins that make an amount $A$ from the values $D$. Give an input for which the recursion reaches fewer than half of the amounts $0, \ldots, A$.
5. Explain why memoizing a recursion for the longest simple path, keyed by (current vertex, target), gives wrong answers. What must the key hold instead, and how many keys does that give for $n$ vertices?

## References
