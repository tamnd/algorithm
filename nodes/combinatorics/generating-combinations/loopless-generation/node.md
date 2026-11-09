---
tag: EMW42J
kind: concept
slug: loopless-generation
name: Loopless generation
aliases:
- Loopless algorithm
- constant-time successor generation
- loopless algorithm
- loopless generation
- worst-case constant time generation
area: combinatorics/generating-combinations
level: advanced
summary: Generation method that spends O(1) worst-case time per object, with no loop over the elements.
prereqs: [constant-amortized-time-generation, gray-code, asymptotic-notation]
see_also: [constant-amortized-time-generation, loopless-gray-code-generation, ehrlich-loopless-combinations, cool-lex-order, steinhaus-johnson-trotter, binary-reflected-gray-code, minimal-change-ordering, combinatorial-generation]
sources:
  - paper: doi:10.1145/321765.321781
    title: Gideon Ehrlich, Loopless algorithms for generating permutations, combinations, and other combinatorial configurations, Journal of the ACM 20(3), 1973, 500-513
  - paper: doi:10.1145/360336.360343
    title: James R. Bitner, Gideon Ehrlich and Edward M. Reingold, Efficient generation of the binary reflected Gray code and its applications, Communications of the ACM 19(9), 1976, 517-521
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (loopless Gray binary generation with focus pointers), Section 7.2.1.2 (loopless permutation generation) and Section 7.2.1.3 (loopless revolving-door combinations)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 1997, 605-629
    locator: Section 1 (loopless algorithms and their relation to Gray codes)
---

A generation algorithm is loopless when, after an initialization, it takes $O(1)$ time in the worst case to go from each object to the next. The name, from Gideon Ehrlich (1973), means that the code of one step contains no loop whose length depends on the size of the objects. A loopless generator is [CAT](/constant-amortized-time-generation/) and has constant delay. In the usual in-place model it needs a listing in which consecutive objects differ by $O(1)$ changes, so loopless algorithms go together with [Gray codes](/gray-code/).

## In plain words

Think of a machine that hands out the objects one at a time. A CAT machine is fast on average, but now and then it stops for a long time. A loopless machine never stops for long: the time between two objects is always below a fixed limit, whatever the size of the objects.

For this, each step can change only a few parts of the current object, and the machine must know at once which parts to change. It cannot search for them. Loopless algorithms keep a few extra arrays that point straight to the next place to change.

## The idea

**Definition.** Let a generator list the $N$ objects $x_0, \ldots, x_{N-1}$ of a class of size $n$. It is loopless if it takes $O(\mathrm{poly}(n))$ time before $x_0$ is visited, usually $O(n)$, and $O(1)$ time between the visit of $x_i$ and the visit of $x_{i+1}$, for each $i$, and after the visit of $x_{N-1}$ until it stops. In words, the delay after the start is constant.

**Loopless is stronger than CAT.** A loopless generator takes $O(n) + O(N)$ time in total, so it is CAT whenever $N$ grows at least as fast as $n$. A CAT generator can have long steps. The binary counter is CAT, but its step from $0111\cdots1$ to $1000\cdots0$ takes $\Theta(n)$ time, so it is not loopless.

**A Gray code is needed.** In the in-place model each changed entry costs one write, so a loopless step changes $O(1)$ entries. So the list must be a Gray code in a wide sense: consecutive objects differ by a bounded change. Lexicographic order of $k$-subsets is not such a list, because a step can change all $k$ entries. The [revolving door](/revolving-door-ordering/) order and [cool-lex order](/cool-lex-order/) are.

**A Gray code is not enough.** The step must also find the place of the change in $O(1)$ time. In the [binary reflected Gray code](/binary-reflected-gray-code/), step $i$ flips bit $\rho(i)$, the number of trailing zeros of $i$. A count of trailing zeros by a scan is a loop. Loopless methods keep extra data that predicts this place.

**Common techniques.**

- *Focus pointers.* Bitner, Ehrlich and Reingold (1976) keep an array $f_0, \ldots, f_n$ for the binary reflected Gray code. The step reads $j \leftarrow f_0$, sets $f_0 \leftarrow 0$, stops if $j = n$, else sets $f_j \leftarrow f_{j+1}$ and $f_{j+1} \leftarrow j + 1$, and flips bit $j$. Knuth gives this as the loopless Algorithm L in Section 7.2.1.1. See [loopless Gray code generation](/loopless-gray-code-generation/).
- *Directions and active elements.* The [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order of permutations becomes loopless when each element keeps a direction and the program keeps the largest mobile element in a list, not by a search. Ehrlich (1973) gave loopless methods of this kind.
- *A jump that predicts the next index.* The revolving door generator of Knuth's Algorithm R has a loop that searches for an index $j$. W. H. Payne showed how to predict $j$ from the last step, which makes it loopless. See [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/).
- *Prefix shifts.* In [cool-lex order](/cool-lex-order/), each step rotates a prefix of a bit string by one position. Two indices $x$ and $y$ track the prefix, and each step is a fixed sequence of assignments.
- *Word operations.* On the [word RAM](/word-ram/), a fixed number of operations on machine words can act on a whole object of up to $w$ bits. [Gosper's hack](/gospers-hack/) lists $k$-subsets in colex order with $O(1)$ word operations for each step, though each step can change many bits.

## Examples

**Focus pointers for $n = 3$.** The table shows the bits $a_2 a_1 a_0$ at each visit and the focus pointers $f_0 f_1 f_2 f_3$ at that time. Each step reads $f_0$, makes two pointer updates and flips one bit, with no loop.

| visit | $a_2 a_1 a_0$ | $f_0, f_1, f_2, f_3$ | next bit $j = f_0$ |
| --- | --- | --- | --- |
| 0 | $000$ | $0, 1, 2, 3$ | 0 |
| 1 | $001$ | $1, 1, 2, 3$ | 1 |
| 2 | $011$ | $0, 2, 2, 3$ | 0 |
| 3 | $010$ | $2, 1, 2, 3$ | 2 |
| 4 | $110$ | $0, 1, 3, 3$ | 0 |
| 5 | $111$ | $1, 1, 3, 3$ | 1 |
| 6 | $101$ | $0, 3, 2, 3$ | 0 |
| 7 | $100$ | $3, 1, 2, 3$ | 3, stop |

The bits $j$ are $0, 1, 0, 2, 0, 1, 0$, the [ruler sequence](/ruler-sequence/). A binary counter would have to scan for them.

**Cool-lex for $5$-bit strings with three ones.** The loopless cool-lex step visits $11100, 01110, 10110, 11010, 01101, 10101, 01011, 00111, 10011, 11001$. Each step does at most eight assignments and three tests, with no inner loop.

**CAT but not loopless.** The lexicographic successor of $k$-subsets is CAT for $k \le n/2$, but its step from $1, n - k + 2, \ldots, n$ to $2, 3, \ldots, k + 1$ changes $k$ entries. So no implementation of this order in the in-place model can be loopless.

## Where it is used

- **Bounded delay.** When each object must be handed on within a fixed time, for example to a consumer that runs at the same pace, the worst-case delay matters, not the average.
- **Gray code applications.** If the work for each object can be updated in $O(1)$ time from the one change, a loopless generator makes the whole program take $O(1)$ time for each object. An example is a sum over a subset when one element enters or leaves, as in [subset sum](/subset-sum-problem/) search.
- **Generation theory.** Loopless algorithms are known for subsets, $k$-subsets, permutations, multiset permutations, set partitions, binary trees and many other classes. A loopless algorithm for a class often comes with a new Gray code for that class. See Savage's survey and Knuth's Section 7.2.1.
- **Hardware and simple programs.** A loopless step is a fixed sequence of instructions, so it is easy to put in hardware or to unroll.

## References
