---
tag: 0D9QST
kind: algorithm
slug: steinhaus-johnson-trotter
name: Steinhaus-Johnson-Trotter algorithm
aliases:
- Johnson-Trotter algorithm
- plain changes
- bell-ringing order
- Algorithm P
area: combinatorics/generating-permutations
level: core
summary: Lists all permutations so that consecutive ones differ by one adjacent transposition.
solves: [generating-all-permutations]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n!), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1962
  people: [H. F. Trotter, Selmer M. Johnson, Hugo Steinhaus]
  note: Trotter published the method as an ALGOL procedure in 1962, and Johnson described it in 1963. English bell ringers used the order much earlier.
prereqs: [permutation, minimal-change-permutation-order, generating-all-permutations]
see_also: [heaps-algorithm, next-permutation, minimal-change-permutation-order, permutation-sign, hamiltonian-path, binary-reflected-gray-code, loopless-generation, sorting-by-adjacent-swaps]
sources:
  - paper: doi:10.1145/368637.368660
    title: H. F. Trotter, Algorithm 115, Perm, Communications of the ACM 5(8) (1962) 434-435
    locator: the whole paper (the procedure that steps through the permutations by adjacent exchanges)
  - paper: doi:10.1090/S0025-5718-1963-0159764-2
    title: Selmer M. Johnson, Generation of permutations by adjacent transposition, Mathematics of Computation 17 (1963) 282-285
    locator: the whole paper
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2, Algorithm P (plain changes) and the history of the order in change ringing
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (the Trotter-Johnson minimal change order of permutations, with its successor, rank and unrank algorithms)
---

The Steinhaus-Johnson-Trotter algorithm lists all $n!$ [permutations](/permutation/) of $n$ items so that each permutation comes from the one before it by exchanging two *adjacent* items. Each item carries a direction, left or right. At each step the largest item that can move one place in its direction, onto a smaller neighbor, does so, and all items larger than it turn around. The order is the classic [minimal-change order](/minimal-change-permutation-order/) of permutations, known to English bell ringers as *plain changes*. With a position array the method runs in constant amortized time per permutation.

## In plain words

Line up the numbers 1 to the number of items, and give each one an arrow that points left. The largest number walks one step at a time to the left, by swapping with its neighbor, until it reaches the end of the row. Then the next largest number that can still step takes one step, and the largest number turns around and walks all the way back. The rule is: always move the largest number whose arrow points at a smaller neighbor, and after the move, turn around every number that is larger than the one that moved.

Each step swaps two neighbors, so each new order is as close as possible to the last one. When no number can move, every order has appeared exactly once.

## The problem

The input is $n \ge 1$. The output is a sequence of $n!$ visits of an array $A[1 \ldots n]$, such that the arrays at the visits are the $n!$ permutations of $[n] = \{1, \ldots, n\}$, each once, and two consecutive arrays differ by the exchange of $A[p]$ and $A[p+1]$ for some $p$. The array is visited in place. To permute other items, use $A$ as a list of indices into them. This is the problem of [generating all permutations](/generating-all-permutations/) in an adjacent-transposition order.

## The algorithm

Each value $v$ has a direction $d[v] \in \{-1, +1\}$, where $-1$ means left, and a position $pos[v]$ with $A[pos[v]] = v$. A value $m$ is *mobile* when the place $q = pos[m] + d[m]$ is inside the array and $A[q] < m$.

```pseudo id=main
SJT(n)
L1  for v ← 1 to n do A[v] ← v, pos[v] ← v, d[v] ← −1
L2  visit A
L3  loop
L4      m ← n
L5      while m ≥ 2 and m is not mobile do m ← m − 1
L6      if m < 2 then return                    ▷ no mobile value: done
L7      p ← pos[m], q ← p + d[m], u ← A[q]
L8      A[p] ← u, A[q] ← m, pos[u] ← p, pos[m] ← q
L9      for v ← m + 1 to n do d[v] ← −d[v]
L10     visit A
```

Line L5 finds the largest mobile value $m$, by testing $n, n-1, \ldots$ in turn. The value 1 is never mobile, because no neighbor is smaller, so the scan stops at 2. Line L8 moves $m$ one place in its direction and keeps the position array right. Line L9 turns around all values larger than $m$.

In practice the value $n$ moves at almost every step. It walks from one end of the array to the other in $n - 1$ steps. When it reaches an end, it is no longer mobile, and one step of the same algorithm on the values $1, \ldots, n-1$ happens. That step turns $n$ around, and $n$ walks back.

## Example

The run for $n = 4$. An arrow before a value gives its direction. The column "move" is the value that moved before the visit, and "tests" is the number of values that line L5 tested.

| visit | move | tests | $A$ with directions |
|---|---|---|---|
| 1 | | | ←1 ←2 ←3 ←4 |
| 2 | 4 | 1 | ←1 ←2 ←4 ←3 |
| 3 | 4 | 1 | ←1 ←4 ←2 ←3 |
| 4 | 4 | 1 | ←4 ←1 ←2 ←3 |
| 5 | 3 | 2 | →4 ←1 ←3 ←2 |
| 6 | 4 | 1 | ←1 →4 ←3 ←2 |
| 7 | 4 | 1 | ←1 ←3 →4 ←2 |
| 8 | 4 | 1 | ←1 ←3 ←2 →4 |
| 9 | 3 | 2 | ←3 ←1 ←2 ←4 |
| 10 | 4 | 1 | ←3 ←1 ←4 ←2 |
| 11 | 4 | 1 | ←3 ←4 ←1 ←2 |
| 12 | 4 | 1 | ←4 ←3 ←1 ←2 |
| 13 | 2 | 3 | →4 →3 ←2 ←1 |

At visit 4, value 4 is at the left end and points left, so it is not mobile. Value 3 points left at 2, which is smaller, so 3 moves, and 4 turns to the right. At visit 12, neither 4 nor 3 can move: 4 is at the left end, and 3 points left at 4. Value 2 points left at 1, so 2 moves, and both 3 and 4 turn around. Visits 1, 5, 9 and 13 with 4 removed read $123$, $132$, $312$, $321$: the start of the same run for $n = 3$.

The full run has 24 visits. The moves are 18 of value 4, 4 of value 3 and 1 of value 2, and the last visit is $2\,1\,3\,4$. Line L5 makes 32 tests in total, including the 3 tests of the final scan that finds no mobile value.

## Correctness

**Theorem.** For each $n \ge 1$, SJT$(n)$ visits each permutation of $[n]$ exactly once, and two consecutive visits differ by one exchange of adjacent positions. The last visit is $2\,1\,3\,4 \cdots n$ when $n \ge 2$.

The proof is by induction on $n$, through a recursive description of the list. Let $L_1 = (1)$. For $n \ge 2$, let $L_n$ be the list that takes the permutations $\pi_1, \pi_2, \ldots$ of $L_{n-1}$ in order and, for each $\pi_t$, lists the $n$ ways to insert $n$ into $\pi_t$: from the right end to the left end when $t$ is odd, and from the left end to the right end when $t$ is even. $L_n$ holds each permutation of $[n]$ once, because removing $n$ gives back $\pi_t$, and the position of $n$ then fixes the permutation. Neighbors in $L_n$ differ by an adjacent exchange: inside a block, $n$ moves one place; between blocks, $n$ stays at the same end and $\pi_t$ changes to $\pi_{t+1}$ by an adjacent exchange.

The key invariant is that SJT$(n)$ with the value $n$ removed behaves exactly as SJT$(n-1)$. While $n$ is not at an end, it is the largest mobile value, so it moves. When $n$ is at an end, it is not mobile, and it does not change which smaller values are mobile, because it is larger than all of them. So the next move is the move of SJT$(n-1)$, and line L9 also turns $n$ around. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/). A test for mobility, a move and a direction change each take $O(1)$ time.

**Moves.** By the recursive structure, the value $m$ moves only inside the run of $L_m$, so it moves $(m - 1)(m - 1)!$ times, for $2 \le m \le n$. The sum is $\sum_{j=1}^{n-1} j \cdot j! = n! - 1$, one move between each two visits.

**Tests and turns.** A step that moves $m$ tests the $n - m + 1$ values $n, \ldots, m$ in line L5 and turns $n - m$ values around in line L9. The final scan tests $n - 1$ values. So the number of tests is

$$\sum_{m=2}^{n} (m-1)(m-1)!\,(n-m+1) + (n - 1) = n! + O((n-1)!).$$

The term $m = n$ is $(n-1)(n-1)! = n! - (n-1)!$. Each other term is at most $m! \cdot (n - m + 1)$, and the sum of these is $O((n-1)!)$, because $m!$ falls by a factor of at least $m + 1$ from one term to the one before it. The number of turns is smaller than the number of tests. So the total time is $\Theta(n!)$, and the amortized time per permutation is $\Theta(1)$: the algorithm is [CAT](/constant-amortized-time-generation/). For $n = 4, 6, 8$ the tests per permutation are $1.333$, $1.211$ and $1.147$.

**Delay.** A step that moves value 2 tests all $n - 1$ values and turns $n - 2$ values, so the worst-case time between two visits is $\Theta(n)$. This form is not [loopless](/loopless-generation/).

**Space.** The arrays $A$, $pos$ and $d$ take $\Theta(n)$ words.

The time is optimal: a list of $n!$ objects needs $\Omega(n!)$ time, and two distinct permutations differ in at least two positions, which an adjacent exchange achieves.

## Properties

- **Adjacent transpositions.** Each step exchanges two neighbors. This is the strongest common minimal-change condition, and [Heap's algorithm](/heaps-algorithm/) does not meet it.
- **Cyclic.** For $n \ge 2$ the last permutation $2\,1\,3 \cdots n$ and the first $1\,2 \cdots n$ differ by the exchange of positions 1 and 2. So the list is a [Hamiltonian cycle](/hamiltonian-cycle/) in the graph whose vertices are the permutations and whose edges join permutations that differ by an adjacent exchange.
- **Alternating sign.** Each step is a transposition, so the [sign](/permutation-sign/) alternates. Each step also changes the number of [inversions](/inversion/) by exactly one.
- **The largest value moves most.** Value $n$ makes $(n-1)/n$ of all moves. A program can handle these moves in a tight inner loop.
- **No comparisons of items.** The test $A[q] < m$ compares values in $[n]$, not the items. The method permutes positions, so it works for items of any type.

## Variants and improvements

- **Knuth's Algorithm P.** It keeps for each value $j$ a counter $c_j$ with $0 \le c_j < j$ and a direction $o_j$. It computes the place of each exchange from these counters, so it needs no position array, and it runs in constant amortized time.
- **Loopless forms.** The scan of line L5 can be replaced by a stack of the mobile values, so that the next value to move is known in $O(1)$ time. Ehrlich (1973) gave loopless algorithms of this kind, with $O(1)$ time per step in the worst case.
- **Recursive form.** Generate $L_{n-1}$ and insert $n$ in a zigzag. This is the definition used in the proof. It is short, but it needs the list of $L_{n-1}$ or a recursion of depth $n$.
- **Ranking.** The rank of a permutation in this order can be computed from the rank of the permutation with $n$ removed and the position of $n$, in $O(n^2)$ time. Kreher and Stinson give the rank, unrank and successor functions.
- **Multisets and other objects.** The same zigzag idea gives Gray codes for many other objects, such as the [binary reflected Gray code](/binary-reflected-gray-code/) for bit strings.

## When to use it

Use the Steinhaus-Johnson-Trotter algorithm when the next permutation must differ from the last one by swapping two neighbors. This happens when a cost depends on adjacent pairs, as in the length of a tour or the number of [inversions](/inversion/), so that the cost can be updated in $O(1)$ time per step. It also happens when each step must be a physical swap of neighbors, as in change ringing. If any exchange is good enough, [Heap's algorithm](/heaps-algorithm/) is simpler and a little faster. If the order must be lexicographic, use [next permutation](/next-permutation/).

## Pitfalls

- **Turning the wrong values.** Line L9 turns the values larger than $m$. If it also turns $m$, then $m$ walks back at once, and the run goes back and forth between two permutations forever. If it turns the values smaller than $m$ instead, the run stops early: for $n = 4$ it visits only 4 permutations.
- **Searching for the mobile value by position.** Without the $pos$ array, line L5 must scan the array to find each value, which costs $\Theta(n)$ per test and $\Theta(n^2)$ per step in the worst case. Keep $pos$ up to date in line L8.
- **The wrong start.** Line L1 must set all directions to left, with the values in increasing order. If value 4 starts to the right for $n = 4$, the run stops after 21 permutations.
- **Mobility at the ends.** The test in line L5 must check that $q$ is inside the array before it reads $A[q]$.

## Implementations

## History

The order is older than computers. English change ringers of the seventeenth century rang the bells of a tower in the order of plain changes, in which two bells that are adjacent in the order of ringing exchange places at each change. Knuth gives this history in Section 7.2.1.2. Hugo Steinhaus described the order in a book of mathematical problems. H. F. Trotter published it as Algorithm 115 in Communications of the ACM in 1962, and Selmer M. Johnson published it in Mathematics of Computation in 1963. Ehrlich gave loopless versions in 1973.

## References
