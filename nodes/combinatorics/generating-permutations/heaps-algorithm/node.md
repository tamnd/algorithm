---
tag: AEJSBV
kind: algorithm
slug: heaps-algorithm
name: Heap's algorithm
aliases:
- Heap's method
- permutations by interchanges
area: combinatorics/generating-permutations
level: core
summary: Generates all permutations by one swap per step using a recursive scheme with a swap per level.
solves: [generating-all-permutations]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n!), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: true}
history:
  year: 1963
  people: [B. R. Heap]
  note: Heap published the method in The Computer Journal in 1963.
prereqs: [permutation, recursion, generating-all-permutations]
see_also: [steinhaus-johnson-trotter, next-permutation, minimal-change-permutation-order, permutation-sign, constant-amortized-time-generation, factorial]
sources:
  - paper: doi:10.1093/comjnl/6.3.293
    title: B. R. Heap, Permutations by interchanges, The Computer Journal 6(3) (1963) 293-298
    locator: the whole paper (the method and the rule for the exchanges)
  - paper: doi:10.1145/356689.356692
    title: Robert Sedgewick, Permutation generation methods, ACM Computing Surveys 9(2) (1977) 137-164
    locator: the recursive exchange methods, Heap's method, and the comparison of running times
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (generating all permutations, exchange methods such as Heap's)
---

Heap's algorithm lists all $n!$ [permutations](/permutation/) of $n$ items so that each permutation comes from the one before it by a single exchange of two items. It is recursive: to permute $k$ items, it permutes the first $k - 1$ items $k$ times, and between these rounds it exchanges the last item with another one. The item that it exchanges with depends only on whether $k$ is odd or even. It makes $n! - 1$ exchanges in total, so it runs in constant amortized time per permutation, and it is one of the fastest ways to [generate all permutations](/generating-all-permutations/). B. R. Heap published it in 1963.

## In plain words

Take a row of cards. Hold the last card still and shuffle the other cards through every order, with the same method. Then swap the last card with one of the others, and do it again. Repeat until every card has had a turn in the last place.

The hard part is to choose the swap so that each card really gets one turn at the end, and none gets two. Heap found a simple rule. If the number of cards in play is odd, always swap the last card with the first one. If it is even, swap it with the first card in the first round, the second card in the second round, and so on.

Each new order differs from the one before it by one swap of two cards. So the work per order is very small.

## The problem

The input is an array $A[0 \ldots n-1]$ of $n$ items. The output is a sequence of $n!$ *visits*: at each visit the array holds an arrangement of the items, and each arrangement of the positions occurs at exactly one visit. With distinct items, these are the $n!$ permutations. The array is visited in place; a copy costs $\Theta(n)$ more per visit. This is the problem of [generating all permutations](/generating-all-permutations/), with the extra condition that two consecutive visits differ by one transposition.

## The algorithm

The call HEAP$(A, n)$ generates all permutations of $A[0 \ldots n-1]$. The call HEAP$(A, k)$ permutes only the prefix $A[0 \ldots k-1]$ and does not touch the rest.

```pseudo id=main
HEAP(A, k)                                  ▷ visit every arrangement of A[0 .. k − 1]
L1  if k ≤ 1 then
L2      visit A
L3      return
L4  HEAP(A, k − 1)
L5  for i ← 0 to k − 2 do
L6      if k is even then exchange A[i] and A[k − 1]
L7      else exchange A[0] and A[k − 1]
L8      HEAP(A, k − 1)
```

Line L4 is the first round, with the item that is already at position $k - 1$. Each pass of the loop of line L5 brings a new item to position $k - 1$ and starts a new round. There are $k$ rounds in total. During a round, position $k - 1$ does not change, because HEAP$(A, k-1)$ only touches $A[0 \ldots k-2]$.

The rule of lines L6 and L7 is the whole trick. For even $k$, the items at positions $0, 1, \ldots, k-2$ go to the end in turn. For odd $k$, the item at position 0 goes to the end each time. In both cases the inner calls move the items between the exchanges, and the proof shows that each item reaches position $k - 1$ exactly once.

**The iterative form.** A counter $c[k]$ replaces the loop variable $i$ of level $k$. This form needs no recursion, and it is the form most programs use.

```pseudo id=iterative
HEAP-ITERATIVE(A, n)
I1  c[0 .. n − 1] ← 0
I2  visit A
I3  k ← 1
I4  while k < n do
I5      if c[k] < k then
I6          if k is odd then exchange A[c[k]] and A[k]
I7          else exchange A[0] and A[k]
I8          visit A
I9          c[k] ← c[k] + 1, k ← 1
I10     else
I11         c[k] ← 0, k ← k + 1
```

Here the index $k$ of the counter is the last position of the prefix, so the level of the recursive form is $k + 1$. An odd $k$ in line I6 is an even level in line L6. The two forms visit the same arrangements in the same order.

## Example

Run HEAP$(A, 4)$ on $A = [1, 2, 3, 4]$. The table gives the first 12 visits. The column "exchange" is the exchange made just before the visit, with 0-based positions, and "level" is the $k$ of the call that made it.

| visit | exchange | level | $A$ |
|---|---|---|---|
| 1 | none | | 1 2 3 4 |
| 2 | 0 and 1 | 2 | 2 1 3 4 |
| 3 | 0 and 2 | 3 | 3 1 2 4 |
| 4 | 0 and 1 | 2 | 1 3 2 4 |
| 5 | 0 and 2 | 3 | 2 3 1 4 |
| 6 | 0 and 1 | 2 | 3 2 1 4 |
| 7 | 0 and 3 | 4 | 4 2 1 3 |
| 8 | 0 and 1 | 2 | 2 4 1 3 |
| 9 | 0 and 2 | 3 | 1 4 2 3 |
| 10 | 0 and 1 | 2 | 4 1 2 3 |
| 11 | 0 and 2 | 3 | 2 1 4 3 |
| 12 | 0 and 1 | 2 | 1 2 4 3 |

Visits 1 to 6 are the first round of level 4, with item 4 at the end. They are all six arrangements of $1, 2, 3$. The first call HEAP$(A, 3)$ ends with $A = [3, 2, 1, 4]$: for odd $k$ the net effect of a call is the exchange of positions 0 and $k - 1$. Then level 4, which is even, exchanges positions $i = 0$ and 3, and item 3 comes to the end. The next rounds bring items 2 and then 1 to the end. The last visit is $A = [2, 3, 4, 1]$. In all, the 24 visits are the 24 permutations of $1, 2, 3, 4$, and the 23 exchanges are 12 at level 2, 8 at level 3 and 3 at level 4.

## Correctness

**Theorem.** For each $n \ge 1$, HEAP$(A, n)$ visits $n!$ arrangements of $A[0 \ldots n-1]$, one for each permutation of the positions, and two consecutive visits differ by the exchange of two positions.

The proof is by induction on $k$, with a stronger statement about the net effect $E_k$ of a call HEAP$(A, k)$ on the prefix:

- if $k$ is odd, $E_k$ exchanges positions $0$ and $k - 1$ (for $k = 1$ it does nothing);
- if $k$ is even, $E_k$ moves the items along one cycle of length $k$ through all the positions $0, \ldots, k-1$.

For even $k$, the inner calls have odd level $k - 1$ and each one exchanges positions 0 and $k - 2$. A direct trace shows that the items at position $k - 1$ in the $k$ rounds are $x_{k-1}, x_{k-2}, x_1, x_2, \ldots, x_{k-3}, x_0$, where $x_0 \ldots x_{k-1}$ is the starting prefix. For odd $k$, one round followed by the exchange of line L7 is the cycle $E_{k-1}$ followed by a transposition that joins it to position $k - 1$, which is a single cycle of length $k$. So the $k$ rounds bring the items of all $k$ positions to the end, each once. The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/): an exchange, a test and a counter update take $O(1)$ time.

- **Exchanges.** There is one exchange between two consecutive visits and none after the last one. So the total is $n! - 1$, and the number of exchanges made at level $k$ is $(k - 1) \cdot n!/k!$.
- **Calls.** HEAP$(A, k)$ makes $k$ calls of level $k - 1$, so the number of calls of level $j$ is $n!/j!$, and the total is $\sum_{j=1}^{n} n!/j! < (e - 1)\, n!$.
- **Time.** Each call does $O(1)$ work besides its inner calls, so the total time is $\Theta(n!)$, and the amortized time is $\Theta(1)$ per permutation. This makes it a [CAT](/constant-amortized-time-generation/) algorithm.
- **Delay.** In the iterative form, line I11 can run up to $n - 2$ times between two visits, so the worst-case time between two visits is $\Theta(n)$. The algorithm is not [loopless](/loopless-generation/).
- **Space.** The recursion has depth $n$, or the iterative form keeps $n$ counters, so the extra space is $\Theta(n)$.

Each method that visits $n!$ arrangements needs $\Omega(n!)$ time, and two distinct arrangements differ in at least two positions. So Heap's algorithm is optimal up to a constant factor, and its number of changes per step is the least possible.

## Properties

- **One transposition per step.** Consecutive permutations differ by the exchange of two items, which is the least possible change. The two items need not be adjacent. See [minimal-change order](/minimal-change-permutation-order/).
- **Alternating sign.** Each exchange is a transposition, so the [sign](/permutation-sign/) of the visited permutation changes at each step.
- **Cyclic for odd $n$ and for $n = 2$.** For odd $n$ the net effect $E_n$ is an exchange of positions 0 and $n - 1$, so the last permutation is one exchange away from the first: for $n = 5$ the last one is $5\,2\,3\,4\,1$. For even $n \ge 4$, $E_n$ is a cycle of length $n$, so the last and the first differ in all $n$ positions; for $n = 4$ the last one is $2\,3\,4\,1$.
- **In place and without comparisons.** The algorithm never compares items, so the items need no order, and equal items give repeated arrangements.

## Variants and improvements

- **Iterative form.** Given above. It uses $n$ counters instead of the call stack.
- **Unrolled bottom levels.** Most exchanges happen at the bottom levels: about half of them at level 2 and a third at level 3. A program can write the bottom levels as straight-line code, which removes most of the loop overhead.
- **Other exchange rules.** Level $k$ can choose the partner of position $k - 1$ in other ways, as long as each item reaches position $k - 1$ once. Sedgewick's survey compares several such rules, and Heap's rule is the simplest one that works for all $n$.
- **Adjacent exchanges.** If the two exchanged items must be neighbors, use the [Steinhaus-Johnson-Trotter algorithm](/steinhaus-johnson-trotter/).
- **Sorted order.** If the permutations must come in lexicographic order, use [next permutation](/next-permutation/). It makes about 1.54 exchanges per step on average, against exactly 1 here.

## When to use it

Use Heap's algorithm when you need every permutation and the order does not matter, for example in a brute-force search of a small [traveling salesman](/traveling-salesman-problem/) instance or in an exhaustive test. It is short, it never compares items, and each step costs one exchange, so the program can update a cost or a hash in $O(1)$ time per step. Do not use it when the permutations must come in sorted order, when the items have repeats and each distinct arrangement must come once, or when you need to resume from a given permutation without the counters.

## Pitfalls

- **The parity rule the wrong way round.** With line L6 for odd $k$ and line L7 for even $k$, the method repeats permutations: for $n = 3$ it visits only 4 distinct permutations out of 6, and for $n = 4$ only 12 out of 24. Exchange with position $i$ when $k$ is even, and with position 0 when $k$ is odd.
- **One exchange too many.** The loop of line L5 runs $k - 1$ times, for $i = 0$ to $k - 2$. A common wrong form runs $k$ passes, each an inner call followed by an exchange. It still visits each permutation once, but for $n = 4$ it makes 40 exchanges instead of 23, and two consecutive visits can differ in 4 positions.
- **Off by one in the iterative form.** Line I6 uses $A[c[k]]$ when $k$ is odd, and here $k$ is the last index, not the length. Mixing the two conventions gives the parity error of the first pitfall.
- **Visiting by reference.** The array changes after each visit. Code that stores the array itself, instead of a copy, ends with $n!$ references to the final arrangement.

## Implementations

## History

B. R. Heap described the method in 1963 in The Computer Journal, under the title "Permutations by interchanges". In his 1977 survey of permutation generation methods, Robert Sedgewick studied the exchange methods in detail and recommended Heap's method as the fastest simple method for listing all permutations.

## References
