---
tag: MQYKYZ
kind: data-structure
slug: chtholly-tree
name: Chtholly tree
aliases:
- ODT
- old driver tree
- interval set
area: data-structures/range-query-structures
level: advanced
summary: Ordered set of constant-valued intervals that gives amortized efficient range assignment.
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {n: the length of the array, m: the number of operations, k: the number of runs inside the range of an operation; the amortized bound is for assignments}
  time: {amortized: O(log n), worst: O(k + log n)}
  space: {extra: O(n)}
prereqs: [ordered-set, amortized-cost, range-assignment-query]
see_also: [range-assignment-and-sum-query, lazy-propagation, segment-tree, potential-method, interval-tree, segment-tree-beats, square-root-decomposition, balanced-binary-search-tree]
sources:
  - url: https://codeforces.com/problemset/problem/896/C
    title: Codeforces Round 449, Problem 896C, Willem, Chtholly and Seniorious
    locator: the problem statement (range add, range assign, k-th smallest and sum of powers on random data)
  - url: https://oi-wiki.org/misc/odt/
    title: OI Wiki, 珂朵莉树/颜色段均摊 (Chtholly tree, amortized colour segments)
    locator: the sections split 操作, assign 操作 and perform 操作, and the section 复杂度分析 (complexity analysis)
  - url: https://codeforces.com/blog/entry/56135
    title: Codeforces Round 449, Editorial
    locator: the solution of problem 896C (one std::set of runs of equal values, and assignment that destroys the runs in its range), and the origin of the name
---

A Chtholly tree keeps an array of $n$ items as a sorted set of maximal or non-maximal *runs*, intervals $[s, e)$ on which every item has the same value. Two primitive steps do all the work: SPLIT$(x)$ cuts the run that contains position $x$ so that a run starts at $x$, and ASSIGN$(l, r, v)$ splits at $l$ and $r$, deletes all runs in between, and inserts the single run $[l, r)$ with value $v$. Each assignment adds at most three runs and deletes every run it covers, so with a [balanced search tree](/balanced-binary-search-tree/) of runs it costs $O(\log n)$ amortized. Any other range operation, such as range add, range sum or the $k$-th smallest in a range, visits the runs in the range one by one, which is fast only when assignments keep the number of runs small.

## In plain words

Picture a fence of $n$ boards, painted in stripes. Instead of writing down the colour of every board, you write down the stripes: "boards 0 to 4 are red, boards 5 to 11 are blue", and so on.

Painting a stretch of the fence in one colour is cheap in this notebook. You cross out the stripes that the new paint covers, cut the two stripes at its edges if they stick out, and write one new line. Since you can only cross out lines that you wrote before, the crossing out costs nothing in the long run. Other jobs, like "add 1 to every board's number from 3 to 50", must touch each stripe in the stretch, so they are fast only while the fence has few stripes.

## The abstract type

The structure keeps an array $A[0 \ldots n-1]$ of values. The core operations are:

- $\textsc{assign}(l, r, v)$: set $A[k] \leftarrow v$ for $l \le k < r$;
- $\textsc{each}(l, r, f)$: call $f(s, e, v)$ for each run $[s, e)$ of value $v$ that tiles $[l, r)$, from left to right, where $f$ may change $v$.

Range add, range sum, range sum of powers, and the $k$-th smallest value of a range are all instances of EACH: the sum adds $v \cdot (e - s)$ over the runs, and the $k$-th smallest sorts the runs of the range by value and walks the lengths.

## Representation

An [ordered set](/ordered-set/) of runs $(s, e, v)$, keyed by $s$, with the invariant

> **(C)** The runs are disjoint, their union is $[0, n)$, each run is non-empty, and $A[k] = v$ for each run $(s, e, v)$ and each $s \le k < e$.

Adjacent runs may have equal values; the structure does not merge them. In C++ the set is a `std::set` or `std::map`; in other languages any balanced search tree, a skip list, or a sorted array with binary search works.

## Operations

```pseudo id=main
SPLIT(x)                                    ▷ 0 ≤ x ≤ n; return the run that starts at x
L1  if x = n then return END
L2  (s, e, v) ← the run with the largest s ≤ x
L3  if s = x then return (s, e, v)
L4  replace (s, e, v) by (s, x, v) and (x, e, v)
L5  return (x, e, v)

ASSIGN(l, r, v)                             ▷ 0 ≤ l < r ≤ n
L6  hi ← SPLIT(r)                           ▷ split at r first
L7  lo ← SPLIT(l)
L8  delete the runs from lo up to, but not including, hi
L9  insert (l, r, v)
```

The other operations split in the same order and then walk the runs.

```pseudo id=each
EACH(l, r, f)                               ▷ visit the runs that tile [l, r)
L10 hi ← SPLIT(r)
L11 lo ← SPLIT(l)
L12 for each run (s, e, v) from lo up to, but not including, hi do
L13     f(s, e, v)                          ▷ for range add: v ← v + d
```

With `std::map` the split at $r$ must come before the split at $l$: the split at $l$ may cut the run that contains $r$ in two, and an iterator taken before would point to the wrong run.

## Example

Take $n = 10$ and $A = [1, 1, 2, 2, 2, 3, 3, 3, 3, 1]$, which is the four runs $[0, 2) = 1$, $[2, 5) = 2$, $[5, 9) = 3$ and $[9, 10) = 1$.

| operation | runs after | note |
|---|---|---|
| $\textsc{assign}(3, 7, 5)$ | $[0,2){=}1$, $[2,3){=}2$, $[3,7){=}5$, $[7,9){=}3$, $[9,10){=}1$ | SPLIT(7) cuts $[5,9)$, SPLIT(3) cuts $[2,5)$, then $[3,5)$ and $[5,7)$ go |
| $\textsc{sum}(1, 8)$ | unchanged except a cut at 1 and 8 | $1 \cdot 1 + 2 \cdot 1 + 5 \cdot 4 + 3 \cdot 1 = 26$ |
| $\textsc{add}(0, 4, 1)$ | $[0,1){=}2$, $[1,2){=}2$, $[2,3){=}3$, $[3,4){=}6$, $[4,7){=}5$, ... | SPLIT(4) cuts $[3,7)$ |
| $k$-th smallest of $[0, 10)$, $k = 5$ | unchanged | the values sorted are $1, 2, 2, 3, 3, 3, 5, 5, 5, 6$, so 3 |

After these operations $A = [2, 2, 3, 6, 5, 5, 5, 3, 3, 1]$. The sum and the add each made new cuts and created runs with equal neighbours, which the structure keeps.

## Correctness

SPLIT keeps (C): the run $(s, e, v)$ with $s < x < e$ is replaced by two non-empty runs with the same union and the same value, and line L2 finds the run that contains $x$ because the starts are sorted and the runs tile $[0, n)$. After the two splits of ASSIGN, a run starts at $l$ and a run starts at $r$ (or $r = n$), so the runs from lo to hi tile exactly $[l, r)$. Deleting them and inserting $(l, r, v)$ keeps the tiling and gives every position of $[l, r)$ the value $v$. The [proof](proofs/correctness.md) gives the details and the amortized bound.

## Complexity

Let $R$ be the number of runs, at most $n$. A split is one predecessor search and at most one replacement, $O(\log R)$. An assignment that deletes $k$ runs costs $O((k + 1) \log R)$, or $O(k + \log R)$ when the deleted runs are removed as one block. With the [potential](/potential-method/) $\Phi = c \cdot R \log n$, the two splits raise $\Phi$ by at most $2 c \log n$ and the assignment changes $R$ by $1 - k$, so the amortized cost of ASSIGN is $O(\log n)$. In total, $m$ assignments on an array of $R_0$ initial runs take $O((R_0 + m) \log n)$ time, because each run is deleted at most once and each operation creates at most three.

EACH costs $O(k + \log R)$ for the $k$ runs in its range and adds at most two runs. Nothing bounds $k$ except $R$, so a sequence of range adds without assignments can cost $\Theta(n)$ each, and an adversary that first makes $n$ runs and then asks for sums over $[0, n)$ forces $\Theta(n m)$ time. On random operations, as in the original problem, assignments keep the number of runs small; OI Wiki states a proof that the `std::set` version then runs in $O(n \log \log n)$ total time. The space is $O(R) = O(n)$.

## Variants

- **With merging.** After an assignment, merge the new run with equal neighbours. This keeps the runs maximal, so $R$ is the number of value changes plus one, but it does not change the worst case.
- **Linked list of runs.** If the positions of the operations are known as list nodes, splits and deletions need no search; OI Wiki gives this form and its $O(n \log n)$ bound on random data.
- **Colour sets.** Keeping runs of a "colour" with a counter per colour answers "how many positions have colour $c$" in $O(1)$ after each assignment, which is the classic use in painting problems.
- **Inside other structures.** Runs of equal values appear as the "colour segment amortization" inside solutions with segment trees, for example to bound the number of changes of a value over time.

## When to use it

Use a Chtholly tree when range assignments dominate, either because the problem guarantees random operations or because every range operation is followed by an assignment of the same range, so that the runs it visits are deleted right after. It is short to write and handles operations that a [segment tree](/segment-tree/) with [lazy propagation](/lazy-propagation/) cannot combine, such as the sum of $x$-th powers modulo $y$ of a range, or the $k$-th smallest. When the input can be adversarial and there are non-assigning range operations, use a lazy segment tree for sums and assignments, see the [range assignment and sum query](/range-assignment-and-sum-query/).

## Pitfalls

- **Splitting at $l$ before $r$.** With iterators into a `std::map` or `std::set`, the split at $r$ can invalidate the iterator from the split at $l$ when both fall into the same run. Split at $r$ first.
- **Adversarial input.** Without assignments, or with assignments of tiny ranges, the number of runs grows to $n$, and each range query becomes a linear scan. The amortized bound covers assignments only.
- **Overflow of the run length.** In the sum of powers, $v^x \cdot (e - s)$ must be reduced modulo $y$ after each step, and the exponentiation should use fast modular powering.
- **The end sentinel.** SPLIT$(n)$ must return the end of the set, not cut a run; a sentinel run $[n, n + 1)$ is a common alternative.
- **Equal keys.** The set is keyed by the start alone. Inserting a run with a start that already exists replaces or fails silently, depending on the container.

## Implementations

## History

The structure became widely known through Codeforces problem 896C, *Willem, Chtholly and Seniorious*, of Codeforces Round 449 in 2017, whose operations on random data were meant to be solved with it. In the editorial of the round, the problem author, whose Codeforces handle is ODT, writes that the structure was first named "Old Driver Tree" after that handle and later called it Chtholly Tree, after the character Chtholly in the statement. OI Wiki describes it as a technique, "amortized colour segments", rather than a new data structure.

## References
