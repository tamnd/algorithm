---
tag: 3PVRP2
kind: algorithm
slug: ehrlich-loopless-combinations
name: Ehrlich's loopless combination generation
aliases:
- loopless algorithm for combinations
- loopless revolving door algorithm
- revolving-door combinations (Algorithm R)
area: combinatorics/generating-combinations
level: advanced
summary: Generate each combination with O(1) worst-case work per step, with no inner loop.
solves: [k-subset-enumeration]
model: word-ram
complexity:
  vars: {n: the size of the ground set, k: the size of each subset, N: the number of k-subsets}
  time: {worst: Θ(N), amortized: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1973
  people: [Gideon Ehrlich, W. H. Payne]
  note: Ehrlich named and studied loopless generation in 1973. The revolving-door program here is Payne's, and Payne also found the jump that makes it loopless.
prereqs: [loopless-generation, lexicographic-combinations, revolving-door-ordering]
see_also: [revolving-door-ordering, loopless-generation, cool-lex-order, chase-sequence, eades-mckay-algorithm, binary-reflected-gray-code, combination-gray-code-generation, combinatorial-ranking-and-unranking]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Algorithm R, Revolving-door combinations, the alternating combinatorial number system, and the exercise by W. H. Payne that makes Algorithm R loopless)
  - paper: doi:10.1145/321765.321781
    title: Gideon Ehrlich, Loopless algorithms for generating permutations, combinations, and other combinatorial configurations, Journal of the ACM 20(3), 1973, 500-513
  - paper: doi:10.1145/360336.360343
    title: James R. Bitner, Gideon Ehrlich and Edward M. Reingold, Efficient generation of the binary reflected Gray code and its applications, Communications of the ACM 19(9), 1976, 517-521
  - paper: doi:10.1145/355826.355830
    title: W. H. Payne and F. M. Ives, Combination generators, ACM Transactions on Mathematical Software 5(2), 1979, 163-172
---

This algorithm lists the $k$-subsets of $\{0, \ldots, n-1\}$ in the [revolving door](/revolving-door-ordering/) order, where each step takes out one element and puts in another. It keeps the subset as $c_k > \cdots > c_1$ and changes at most two entries in each step. A search for the entry to change would be a loop, so the algorithm predicts where the search must start from the last change. With this jump the search is at most four short tests, and each step takes $O(1)$ time in the worst case. So the algorithm is [loopless](/loopless-generation/). It solves [k-subset enumeration](/k-subset-enumeration/).

## In plain words

A room holds $k$ people from a group of $n$. A door turns, and at each turn one person goes out and one comes in. The aim is to see each possible group in the room once.

The order of the groups is fixed by a simple rule. Sort the people in the room by number, largest first. The largest number goes up slowly. The second largest goes down, the third goes up, and so on, each one in the other direction from the one before it.

To make a step, find the smallest person who can still move in his direction, move him by one, and reset the people below him. In this order the reset always moves only one other person. Also, the place to look next is always close to the place of the last change, so the program never has to search far.

## The problem

Given $0 \le k \le n$, visit each $k$-subset of $\{0, \ldots, n-1\}$ once. The current subset is an array $c[1 \ldots k]$ with $c[k] > \cdots > c[1] \ge 0$, and a sentinel $c[k+1] = n$. This is [k-subset enumeration](/k-subset-enumeration/) in the revolving door order, with the extra demand that the time between two visits is $O(1)$ in the worst case.

**The order.** Call position $i$ *rising* when $k - i$ is even and *falling* when $k - i$ is odd. So position $k$ is rising, position $k - 1$ is falling, and so on. Two subsets are compared at the largest position where they differ. At a rising position the smaller value comes first, and at a falling position the larger value comes first. Knuth describes this as the lexicographic order of $c_k, -c_{k-1}, c_{k-2}, \ldots$. The same list comes from the [binary reflected Gray code](/binary-reflected-gray-code/): keep only the strings with $k$ ones, in the Gray code order.

**Ranges.** When $c[k], \ldots, c[i+1]$ are fixed, the entry $c[i]$ can take each value from $i - 1$ to $c[i+1] - 1$. Its *first* value is $i - 1$ if position $i$ is rising and $c[i+1] - 1$ if it is falling. Its *last* value is the other end of the range.

## The algorithm

This is Knuth's Algorithm R for $n > k > 1$, with the jump of line L4. The variable $j$ holds the position that changed in the last step, and $s$ says if the next test is a test to move $c[j]$ up or down.

```pseudo id=main
REVOLVING-DOOR-LOOPLESS(n, k)        ▷ n > k > 1; visit c[k] > … > c[1] over {0, …, n − 1}
L1  c[i] ← i − 1 for 1 ≤ i ≤ k;  c[k + 1] ← n;  j ← k + 1
L2  loop
L3      visit c[k] … c[1]
L4      if j ≥ 3 + [k odd] then j ← j − 1 − [j ≡ k (mod 2)];  s ← UP      ▷ the jump
L5      else if k odd and c[1] + 1 < c[2] then c[1] ← c[1] + 1;  j ← 1;  s ← DONE
L6      else if k even and c[1] > 0 then c[1] ← c[1] − 1;  j ← 1;  s ← DONE
L7      else j ← 2;  s ← DOWN if k is odd, else UP
L8      while s ≠ DONE                                   ▷ at most 4 passes
L9          if s = DOWN and c[j] ≥ j then c[j] ← c[j − 1];  c[j − 1] ← j − 2;  s ← DONE
L10         else if s = DOWN then j ← j + 1;  s ← UP
L11         else if c[j] + 1 < c[j + 1] then c[j − 1] ← c[j];  c[j] ← c[j] + 1;  s ← DONE
L12         else j ← j + 1;  s ← DOWN;  if j > k then return
```

Lines L5 and L6 move $c[1]$ by one. Line L9 moves a falling entry down and line L11 moves a rising entry up, and each of them also resets the entry below. Lines L10 and L12 go on to the next position when the test fails. Line L4 is the jump. It skips the positions below $j - 1 - [j \equiv k]$, which cannot move, and it starts at a rising position.

The cases $k \le 1$ and $k = n$ are trivial. For $k = 0$ and $k = n$ there is one subset. For $k = 1$ the order is $0, 1, \ldots, n-1$, which a loop over one value lists with no search.

## Example

Take $n = 6$ and $k = 4$, so $N = 15$. Positions $4$ and $2$ are rising, positions $3$ and $1$ are falling, and the jump runs when $j \ge 3$.

| visit | $c_4 c_3 c_2 c_1$ | $j$ at L4 | lines that act | out | in |
| --- | --- | --- | --- | --- | --- |
| 0 | $3210$ | 5 | L4 (to 4), L11 at 4 | 2 | 4 |
| 1 | $4310$ | 4 | L4 (to 2), L11 at 2 | 0 | 2 |
| 2 | $4321$ | 2 | L6 | 1 | 0 |
| 3 | $4320$ | 1 | L7, L12 at 2, L9 at 3 | 3 | 1 |
| 4 | $4210$ | 3 | L4 (to 2), L12 at 2, L10 at 3, L11 at 4 | 2 | 5 |
| 5 | $5410$ | 4 | L4 (to 2), L11 at 2 | 0 | 2 |
| 6 | $5421$ | 2 | L6 | 1 | 0 |
| 7 | $5420$ | 1 | L7, L11 at 2 | 0 | 3 |
| 8 | $5432$ | 2 | L6 | 2 | 1 |
| 9 | $5431$ | 1 | L6 | 1 | 0 |
| 10 | $5430$ | 1 | L7, L12 at 2, L9 at 3 | 4 | 1 |
| 11 | $5310$ | 3 | L4 (to 2), L11 at 2 | 0 | 2 |
| 12 | $5321$ | 2 | L6 | 1 | 0 |
| 13 | $5320$ | 1 | L7, L12 at 2, L9 at 3 | 3 | 1 |
| 14 | $5210$ | 3 | L4 (to 2), L12 at 2, L10 at 3, L12 at 4 | | |

Each step takes out one element and puts in one. The most passes of line L8 in one step is $3$, at visits $4$ and $14$. The last step finds that no position can move, and line L12 returns.

For $n = 5$ and $k = 3$ the list is $210, 320, 321, 310, 430, 431, 432, 420, 421, 410$.

## Correctness

The proof file has the full argument. It has three parts.

1. **The successor.** In the revolving door order, the next subset is found as in any lexicographic order: take the smallest position $i$ whose entry is not at its last value, move $c[i]$ one step in its direction, and set each entry below $i$ to its first value.
2. **One element in, one out.** If all entries below $i$ are at their last values, then $c[1], \ldots, c[i-2]$ are $0, 1, \ldots, i - 3$, and $c[i-1]$ is $i - 2$ or $c[i] - 1$. When $i$ is rising, the step is $c[i] \leftarrow c[i] + 1$ and $c[i-1] \leftarrow$ the old $c[i]$, which is line L11. When $i$ is falling, the step is $c[i] \leftarrow c[i-1]$ and $c[i-1] \leftarrow i - 2$, which is line L9. Lines L5 and L6 are the case $i = 1$. The scan of lines L8 to L12 tests the positions upward, with the right direction for each one.
3. **The jump.** After a change at position $j$, the entries below position $j - 1$ are at their smallest values $0, 1, \ldots$, and each entry below position $j - 2$ has only one possible value. When $j$ is falling, the entry at position $j - 2$ also has only one possible value. So no position below $j - 1 - [j \equiv k]$ can move, and the scan can start there. This is the property that Knuth credits to W. H. Payne (1974): the next $j$ differs from the last one by at most $2$.

## Complexity

**Each step.** After a change at a rising position $i \ge 3$, position $i - 2$ can always move, so the scan makes one test. After a change at a falling position $i$, the next position to move is $\max(i - 1, 1)$, $i + 1$ or $i + 2$, so the scan makes at most four tests. When there is no jump, $j \le 3$ and the scan reaches at most position $5$. So the loop of line L8 makes at most $4$ passes in each step, and each step takes $O(1)$ time in the worst case. Knuth states this as: R4 and R5 are performed at most twice for each visit.

**Total.** The initialization takes $\Theta(k)$ time and the $N - 1$ steps take $O(N)$, so the total is $\Theta(N)$, and $\Theta(1)$ for each subset. For $n = 20$ and $k = 10$, a test run makes at most $4$ passes in each of the $184755$ steps.

**Space.** The array and two variables. There are no extra arrays.

## Properties

- **Loopless.** The worst-case time between two visits is $O(1)$, see [loopless generation](/loopless-generation/).
- **Revolving door.** Each step takes out one element and puts in one. The step at position $1$ changes $c[1]$ by $1$. Other steps can replace an element by one that is far from it. The [Chase sequence](/chase-sequence/) and the [Eades-McKay](/eades-mckay-algorithm/) order have stronger closeness properties.
- **Rank.** Knuth shows that $c_k \cdots c_1$ is visited after exactly $\binom{c_k + 1}{k} - \binom{c_{k-1} + 1}{k - 1} + \cdots + (-1)^{k-1} \binom{c_1 + 1}{1} - [k \text{ odd}]$ other subsets. This is the alternating combinatorial number system, see [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).
- **Cyclic.** The last subset, $\{0, 1, \ldots, k-2, n-1\}$, differs from the first, $\{0, \ldots, k-1\}$, by one exchange. So the list is a cycle.
- **Not lexicographic.** The order is genlex, so all subsets with the same largest elements are next to each other, but it is not the lexicographic order.

## Variants and improvements

- **Algorithm R without the jump.** Remove line L4. Then the scan starts at position $1$ every time, and one step can test about $k$ positions, so the program is not loopless.
- **Bit strings.** The same order on bit strings $a_{n-1} \ldots a_0$ is the weight-$k$ part of the binary reflected Gray code. Bitner, Ehrlich and Reingold (1976) gave a loopless program for it.
- **Other loopless orders.** [Cool-lex order](/cool-lex-order/) is loopless with a simpler step on bit strings. The [Chase sequence](/chase-sequence/) and the [Eades-McKay algorithm](/eades-mckay-algorithm/) give orders with stronger closeness properties. See [combination Gray code generation](/combination-gray-code-generation/).
- **Multisets.** Through the stars and bars string, the algorithm lists [combinations with repetition](/combinations-with-repetition/) with the same cost.

## When to use it

Use it when the work for each subset can be updated in $O(1)$ time from one element that leaves and one that enters, and when the time for each step must have a fixed bound. Examples are sums and products over the subset, and tests on all $k$-subsets of a set of vectors. If you only need a fast average, the [lexicographic successor](/lexicographic-combinations/) for $k \le n/2$ is simpler. On machine words, cool-lex order or [Gosper's hack](/gospers-hack/) give shorter programs.

## Pitfalls

- **The range of the main code.** The program needs $n > k > 1$. For $k = 1$, line L7 sets $j = 2 > k$, and line L9 then treats the sentinel $c[2]$ as an entry of the subset. Handle $k \le 1$ and $k = n$ apart.
- **The parity of $k$.** Lines L4 to L7 depend on the parity of $k$. A program written for odd $k$ gives a wrong order, with repeats, for even $k$.
- **The initial $j$.** Set $j \leftarrow k + 1$ in line L1, and $j \leftarrow 1$ after lines L5 and L6. A wrong $j$ makes the jump skip a position that can move.
- **The sentinel.** Line L11 reads $c[j+1]$, so $c[k+1] = n$ must be in the array.
- **Shared state.** The visit sees the array that the next step changes. Copy it if you store it.

## Implementations

## History

Gideon Ehrlich (1973) named loopless algorithms and gave loopless generators for permutations, combinations and other objects. Knuth credits the revolving door order to D. T. Tang and C. N. Liu (1973), who found its properties in the Gray code, and he notes that Bitner, Ehrlich and Reingold (1976) gave a loopless program for it. Knuth gives the index form as Algorithm R and credits it to W. H. Payne, published by Payne and Ives in 1979. He credits the jump that makes Algorithm R loopless to Payne (1974), as an exercise in Section 7.2.1.3. The page keeps the name "Ehrlich's loopless combination generation" because Ehrlich's paper started the study of such generators.

## References
