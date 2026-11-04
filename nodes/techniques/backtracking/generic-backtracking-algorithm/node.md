---
tag: BD5KA9
kind: algorithm
slug: generic-backtracking-algorithm
name: Generic backtracking algorithm
aliases:
- backtracking template
- backtrack procedure
area: techniques/backtracking
level: intro
summary: The recursive template that extends candidates, checks feasibility, records complete solutions and undoes each extension.
model: word-ram
complexity:
  vars: {n: the number of decisions in a complete solution, d: the largest number of candidates for one decision, T: the number of partial solutions that pass the test}
  time: {worst: O(T d), best: O(d)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1960
  people: [R. J. Walker, Solomon W. Golomb, Leonard D. Baumert]
  note: Walker described the method in 1960; Golomb and Baumert gave a general account under the name backtrack programming in 1965.
prereqs: [recursion, depth-first-search, partial-solution]
see_also: [state-space-tree, search-tree-pruning, chronological-backtracking, n-queens-problem, constraint-satisfaction-problem, generate-and-test, depth-first-branch-and-bound, dancing-links]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2
    locator: Section 7.2.2, Backtrack programming (Algorithm B, basic backtrack)
  - paper: doi:10.1145/321296.321300
    title: Solomon W. Golomb and Leonard D. Baumert, Backtrack programming, Journal of the ACM 12(4), 1965
    locator: pp. 516 to 524
  - paper: doi:10.1090/psapm/010/0121306
    title: R. J. Walker, An enumerative technique for a class of combinatorial problems, Combinatorial Analysis, Proceedings of Symposia in Applied Mathematics 10, AMS, 1960
    locator: pp. 91 to 94
  - paper: doi:10.1090/S0025-5718-1975-0373371-6
    title: Donald E. Knuth, Estimating the efficiency of backtrack programs, Mathematics of Computation 29(129), 1975
    locator: pp. 122 to 136
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 7, Backtracking
---

The generic backtracking algorithm finds all solutions of a problem whose solutions are sequences of decisions $x_1, x_2, \ldots, x_n$. It builds a [partial solution](/partial-solution/) one decision at a time, tests each new prefix, goes deeper when the test passes, and undoes the last decision when it fails or when all choices below it are done. It is a [depth-first search](/depth-first-search/) of the [state space tree](/state-space-tree/) that never enters a subtree whose root fails the test. Its cost is the number of prefixes that pass the test, times the work per prefix, and this number can be anything from linear to exponential.

## In plain words

You must make a fixed number of choices in a row, and some combinations of choices are not allowed. You make the first choice, then the second, and so on. After each choice you check whether the choices so far can still lead to a valid answer. If they can, you make the next choice. If they cannot, you take back the last choice and try the next option for it. When you run out of options for a choice, you take back the choice before it.

When all the choices are made and the check still passes, you have found an answer. You write it down and go on, so that in the end you have seen every answer. The check is what makes the method fast: one failed check throws away every combination that starts with the same choices.

## The problem

A problem fits the template when it has these parts.

- A number $n$ of decisions. A *complete candidate* is a sequence $x_1 \ldots x_n$.
- For each $k$ with $0 \le k < n$ and each prefix $x_1 \ldots x_k$, a finite ordered set of candidates $D_{k+1}(x_1 \ldots x_k)$ for the next decision.
- For each $k$ with $1 \le k \le n$, a test $P_k(x_1 \ldots x_k)$. A prefix that satisfies its test is *alive*.

The task is to output each sequence $x_1 \ldots x_n$ such that $x_{k} \in D_{k}(x_1 \ldots x_{k-1})$ and $P_k(x_1 \ldots x_k)$ hold for each $k$ from 1 to $n$. In the useful case the tests are *prefix-closed*: $P_{k+1}(x_1 \ldots x_{k+1})$ implies $P_k(x_1 \ldots x_k)$. Then the output is exactly the set of candidates that satisfy $P_n$, and $P_n$ is the condition of the problem. Each $P_k$ for $k < n$ must then be a *necessary* condition: it is false only on prefixes that no solution extends. This is the soundness condition of [search tree pruning](/search-tree-pruning/).

For the $n$-queens problem, $x_k$ is the column of the queen in row $k$, $D_{k+1}$ is the set of all $n$ columns, and $P_k$ says that the queen of row $k$ attacks none of the queens of rows 1 to $k-1$.

## The algorithm

The call BACKTRACK$(x, 0)$, with $x$ empty, outputs all solutions.

```pseudo id=main
BACKTRACK(x, k)                           ▷ x[1 .. k] is alive
L1  if k = n then
L2      OUTPUT(x[1 .. n])
L3      return
L4  for each c in D_{k+1}(x[1 .. k]) do       ▷ in the given order
L5      x[k + 1] ← c                          ▷ extend
L6      if P_{k+1}(x[1 .. k + 1]) then
L7          BACKTRACK(x, k + 1)
L8      remove x[k + 1]                       ▷ undo
```

Line L1 checks whether the prefix is complete. Line L4 runs through the candidates of the next decision. Line L5 extends the prefix and line L6 tests it. A prefix that passes the test becomes the root of a recursive call. A prefix that fails is dropped with all its extensions: this is the pruning. Line L8 restores the state of the caller, so the same array $x$ serves all calls. When the program keeps extra data for fast tests, such as the set of used columns in $n$-queens, line L5 updates that data and line L8 restores it.

Knuth's Algorithm B in Section 7.2.2 of *The Art of Computer Programming* is the same method written as a loop with an explicit level counter instead of recursion.

## Example

Run BACKTRACK on the 4-queens problem, with the candidates in the order of the columns 1, 2, 3, 4. A prefix is written as the string of its columns, so `241` means queens at columns 2, 4 and 1 of rows 1, 2 and 3.

| step | alive prefixes visited, in order | prefixes rejected by line L6 after it |
|---|---|---|
| 1 | (empty), `1` | `11`, `12` |
| 2 | `13` | `131`, `132`, `133`, `134` |
| 3 | `14`, `142` | `1421` to `1424`, then `143`, `144` |
| 4 | `2` | `21`, `22`, `23` |
| 5 | `24`, `241`, `2413` (solution) | `2411`, `2412`, then `2414`, `242`, `243`, `244` |
| 6 | `3`, `31` | `311`, `312`, `313` |
| 7 | `314`, `3142` (solution) | `3141`, then `3143`, `3144`, `32`, `33`, `34` |
| 8 | `4`, `41` | `411`, `412` |
| 9 | `413` | `4131` to `4134`, then `414` |
| 10 | `42` | `421` to `424`, then `43`, `44` |

The search visits 17 alive prefixes: 1 of length 0, 4 of length 1, 6 of length 2, 4 of length 3 and 2 of length 4. Line L6 runs 60 times. The two solutions are `2413` and `3142`. Without the test, the tree of all prefixes has $1 + 4 + 16 + 64 + 256 = 341$ nodes.

For 8 queens the search visits 2057 alive prefixes and runs the test 15720 times, and it finds the 92 solutions. The full tree has $\sum_{k=0}^{8} 8^k = 19173961$ nodes.

## Correctness

Call a sequence $x_1 \ldots x_k$ *reachable* when $x_j \in D_j(x_1 \ldots x_{j-1})$ and $P_j(x_1 \ldots x_j)$ hold for each $j \le k$. The claim is that BACKTRACK$(x, 0)$ makes exactly one call BACKTRACK$(x, k)$ for each reachable sequence $x_1 \ldots x_k$ with $k \le n$, in lexicographic order of the candidate orders, and outputs exactly the reachable sequences of length $n$. The proof is by induction on $n - k$: the call for a reachable prefix of length $k < n$ makes one call for each reachable child, in candidate order, and line L8 gives each call the same $x[1 \ldots k]$ on return. With prefix-closed tests, the reachable sequences of length $n$ are exactly the solutions. The full proof is below.

## Complexity

Let $T$ be the number of reachable prefixes, that is, the number of calls, and let $d$ bound the number of candidates of one decision. Each call runs line L6 at most $d$ times. If one test and one extension cost $O(1)$, as with the column and diagonal arrays of $n$-queens, the time is $O(T d)$.

- **Worst case.** If each test passes, $T = \sum_{k=0}^{n} d^k$, which is $\Theta(d^n)$ for $d \ge 2$. No useful general bound is better: the output itself can have $d^n$ sequences.
- **Best case.** If each candidate of the first decision fails its test, there is one call and the time is $O(d)$. If only one solution is wanted and the first candidate passes at each level, the search stops after $n + 1$ calls, in $O(n)$ time.
- **Space.** The recursion has depth $n$ and keeps one candidate position at each level, so the extra space is $O(n)$ besides the data of the tests.
- **Output-sensitive view.** The time is not bounded by a function of the number of solutions. The $n$-queens search for $n = 3$ visits 6 prefixes and finds no solution, and for a hard instance of a [constraint satisfaction problem](/constraint-satisfaction-problem/) the search can visit exponentially many dead ends.

Since $T$ depends on the instance in ways that are hard to predict, Knuth (1975) gave a way to estimate it before a long run. Walk one random path from the root: at each alive node with $c_j$ alive children, pick one of them with probability $1/c_j$, and stop at a node with no alive child. Return

$$X = 1 + c_0 + c_0 c_1 + c_0 c_1 c_2 + \cdots .$$

Then $\mathbb{E}[X] = T$. *Proof.* A node $u$ at depth $k$ with ancestors of $c_0, \ldots, c_{k-1}$ alive children is on the path with probability $1/(c_0 \cdots c_{k-1})$, and then it adds the term $c_0 \cdots c_{k-1}$ to $X$. So each node adds 1 to $\mathbb{E}[X]$ by [linearity of expectation](/linearity-of-expectation/). On 4 queens, $X$ takes values from 13 to 21 with mean 17. The estimate is unbiased but its variance can be large on unbalanced trees.

## Properties

- **Depth-first.** It visits the alive prefixes in preorder of the [state space tree](/state-space-tree/), so it outputs the solutions in lexicographic order of the candidate orders.
- **Small memory.** It stores only the current path, not the tree. This is the main advantage over a breadth-first search of the same tree.
- **Exhaustive.** It finds all solutions. To find one, stop at the first OUTPUT.
- **Deterministic.** The order of the output depends only on the candidate orders.

## Variants and improvements

- **Variable length.** Replace the test $k = n$ of line L1 by a test "is $x[1 \ldots k]$ complete?", and do not return after OUTPUT when longer solutions can extend a shorter one. Subsets with a given property and paths in a graph fit this form.
- **Dynamic order.** Let line L4 choose which variable to assign next, as in [variable ordering heuristics](/variable-ordering-heuristics/). The tree then depends on the prefix.
- **Look-ahead.** Make the test of line L6 stronger, with [forward checking](/forward-checking/) or [arc consistency](/arc-consistency/), so that fewer prefixes pass.
- **Smarter return.** Return past several levels when the failure does not depend on the last ones, as in [conflict-directed backjumping](/conflict-directed-backjumping/). The plain version is [chronological backtracking](/chronological-backtracking/).
- **Optimization.** Keep the best complete solution so far and add a bound test to line L6. This is [depth-first branch and bound](/depth-first-branch-and-bound/).
- **Dancing links.** For [exact cover](/exact-cover/) problems, [dancing links](/dancing-links/) makes the extend and undo steps $O(1)$ list operations.

## When to use it

Use backtracking when the answer is a sequence of choices with constraints that can be checked on a prefix, and when you need all solutions or any one solution of a hard problem. If the constraints can be checked only on a complete candidate, the method is no better than [generate and test](/generate-and-test/). If the subproblems below different prefixes repeat, [memoization](/memoization/) of the [overlapping subproblems](/overlapping-subproblems/) can be much faster. For an optimum rather than a list, use branch and bound.

## Pitfalls

- **A test that is too strict.** If $P_k$ rejects a prefix that some solution extends, line L6 loses solutions. Each $P_k$ with $k < n$ must be a necessary condition for extension.
- **A missing undo.** If line L5 changes shared data, such as a set of used columns, and line L8 does not restore it, the next candidate is tested against a wrong state. Undo in the reverse order of the changes.
- **Output of a reference.** OUTPUT$(x)$ must copy $x$. If it stores the array itself, all stored solutions change when the search goes on.
- **Deep recursion.** The depth is $n$. In a language with a small call stack, such as Python, use an explicit stack when $n$ can be large.

## Implementations

## History

R. J. Walker described the method as an enumerative technique for combinatorial problems in 1960. Golomb and Baumert gave a general account in 1965 under the name *backtrack programming*, with the test on each prefix as the central idea. Knuth's 1975 paper gave the random-path estimate of the size of the tree, and Section 7.2.2 of Volume 4B of *The Art of Computer Programming* treats the method in depth.

## References
