---
tag: GNNC30
kind: technique
slug: decrease-and-conquer
name: Decrease and conquer
aliases:
- decrease-by-a-constant-factor
- decrease-by-a-constant
area: techniques/divide-and-conquer
level: core
summary: Reduce an instance by a fixed amount or factor and solve only the one smaller subproblem.
prereqs: [recursion, induction]
see_also: [divide-and-conquer-paradigm, prune-and-search, binary-search, insertion-sort, euclidean-algorithm, binary-exponentiation, quickselect, josephus-problem]
sources:
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition
    locator: Chapter 4, Decrease-and-Conquer (introduction; 4.1 Insertion Sort; 4.2 Topological Sorting; 4.3 Algorithms for Generating Combinatorial Objects; 4.4 Decrease-by-a-Constant-Factor Algorithms; 4.5 Variable-Size-Decrease Algorithms)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (binary search among the divide-and-conquer exercises), Chapter 9 (selection in expected and worst-case linear time)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2, Section 2.4 (Medians, the selection algorithm)
---

Decrease and conquer is a way to design an algorithm: reduce an instance of a problem to one smaller instance of the same problem, solve that one instance, and extend its solution to a solution of the original. The smaller instance is smaller by a constant (often 1), by a constant factor (often 2), or by an amount that changes from step to step. This three-way split follows Levitin (Chapter 4). It is the case of the [divide-and-conquer paradigm](/divide-and-conquer-paradigm/) with exactly one subproblem.

## In plain words

To solve a big task, first find a way to make it a little smaller. Solve the smaller task, then use its answer to finish the big one. Repeat until the task is tiny.

There are three ways to make the task smaller. You can remove one item, as when you sort a hand of cards by putting each new card into the cards you already sorted. You can throw away half of the items, as when you look up a word in a dictionary by opening it in the middle and keeping the half where the word must be. Or you can remove a different amount each time, as when the size of the next step depends on the numbers you see.

Removing one item at a time is often slow. Removing half each time is fast, because a few halvings bring any input down to one item.

## When it applies

- **One smaller instance is enough.** The answer for the whole input follows from the answer for one part, plus a little work. If you need the answers of two or more parts, the method is [divide and conquer](/divide-and-conquer-paradigm/).
- **A part of the input can be ruled out.** A test such as one comparison with the middle item shows that the answer is not in some part; that part is dropped.
- **An identity links the problem to a smaller one,** such as $a^n = a^{n-1} \cdot a$, $a^n = (a^{n/2})^2$ or $\gcd(m, n) = \gcd(n, m \bmod n)$.
- **The answer is built one item at a time,** such as a sorted prefix, a topological order or a list of permutations.

## The template

```pseudo id=main
SOLVE(P)                                   ▷ P an instance of size n
L1  if size(P) ≤ n₀ then return BASE(P)    ▷ hole: the small cases
L2  P' ← REDUCE(P)                         ▷ hole: one instance with size(P') < size(P)
L3  S' ← SOLVE(P')
L4  return EXTEND(P, S')                   ▷ hole: build the answer for P from the answer for P'
```

The holes are the small cases of line L1, the reduction of line L2 and the extension of line L4. When EXTEND only returns $S'$ (binary search, Euclid's algorithm), the call of line L3 is the last action, and the recursion becomes a loop; most decrease-and-conquer algorithms are written as loops for this reason. Correctness is a strong [induction](/induction/) on the size: if BASE is right for small instances, REDUCE gives a valid instance of smaller size, and EXTEND turns a right answer for $P'$ into a right answer for $P$, then SOLVE is right for every size. Termination needs the size to drop by at least 1 at each call; a size that is a natural number cannot drop forever.

Levitin (Chapter 4) names three kinds of reduction.

1. **Decrease by a constant.** The size goes from $n$ to $n - c$, usually $n - 1$.
2. **Decrease by a constant factor.** The size goes from $n$ to about $n/b$, usually $n/2$.
3. **Variable-size decrease.** The amount removed depends on the data and changes from one step to the next.

### The two recurrences

Let $f(n) \ge 0$ be the cost of REDUCE and EXTEND on an instance of size $n$.

**Claim 1 (decrease by one).** If $T(0) = c$ and $T(n) = T(n-1) + f(n)$ for $n \ge 1$, then $T(n) = c + \sum_{i=1}^{n} f(i)$ for every $n \ge 0$.

*Proof.* Induction on $n$. For $n = 0$ the sum is empty and $T(0) = c$. For $n \ge 1$, assume $T(n-1) = c + \sum_{i=1}^{n-1} f(i)$. Then $T(n) = T(n-1) + f(n) = c + \sum_{i=1}^{n} f(i)$. $\blacksquare$

So if $f(n) = \Theta(1)$, that is $d_1 \le f(n) \le d_2$ for constants $0 < d_1 \le d_2$ and all $n \ge 1$, then $c + d_1 n \le T(n) \le c + d_2 n$ and $T(n) = \Theta(n)$. If $d_1 n \le f(n) \le d_2 n$ for all $n \ge 1$, then $T(n)$ lies between $c + d_1 n(n+1)/2$ and $c + d_2 n(n+1)/2$, so $T(n) = \Theta(n^2)$. This is the worst case of [insertion sort](/insertion-sort/).

**Claim 2 (decrease by half, constant work).** If $T(1) = c$ and $T(n) = T(\lfloor n/2 \rfloor) + d$ for $n \ge 2$, then $T(n) = c + d \lfloor \log_2 n \rfloor$ for every $n \ge 1$.

*Proof.* Strong induction on $n$. For $n = 1$, $\lfloor \log_2 1 \rfloor = 0$ and $T(1) = c$. Let $n \ge 2$ and $k = \lfloor \log_2 n \rfloor \ge 1$, so $2^k \le n < 2^{k+1}$. Then $2^{k-1} \le n/2 < 2^k$. Since $2^{k-1}$ is an integer, $2^{k-1} \le \lfloor n/2 \rfloor < 2^k$, so $\lfloor \log_2 \lfloor n/2 \rfloor \rfloor = k - 1$. By the hypothesis for $\lfloor n/2 \rfloor < n$, $T(n) = c + d(k-1) + d = c + dk$. $\blacksquare$

So $T(n) = \Theta(\log n)$ when $d > 0$. The same argument with $\lfloor n/b \rfloor$ for an integer $b \ge 2$ gives $c + d \lfloor \log_b n \rfloor$. When the work per step is not constant, write $n = b^k$ and unroll: $T(b^k) = c + \sum_{j=1}^{k} f(b^j)$. For $f(n) = n^e$ with $e > 0$ the sum is a geometric series with ratio $b^e > 1$, so it is at most $b^{ke} / (1 - b^{-e})$ and $T(n) = \Theta(n^e)$: the top step dominates. This is why [quickselect](/quickselect/) runs in linear time when each pivot halves the range: one partition of linear cost per halving gives a geometric sum.

## Classic examples

### Decrease by a constant

- **[Insertion sort](/insertion-sort/)** (Levitin 4.1). Sort the first $n-1$ items, then insert the last one. $T(n) = T(n-1) + O(n)$; for 10 items in decreasing order it makes $10 \cdot 9 / 2 = 45$ comparisons.
- **[Topological sort](/topological-sort/) by source removal** (Levitin 4.2). A directed acyclic graph has a vertex with no incoming edge. Output it, delete it with its edges, and sort the rest. With in-degree counts and a queue of sources this is [Kahn's algorithm](/kahns-algorithm/) and runs in $O(V + E)$ time.
- **[Generating permutations](/generating-all-permutations/)** (Levitin 4.3). Generate the $(n-1)!$ permutations of $n - 1$ items, then insert item $n$ in each of the $n$ positions of each one. The [Johnson-Trotter algorithm](/steinhaus-johnson-trotter/) orders the result so that two neighbours differ by one swap of adjacent items.
- **[Exponentiation](/integer-exponentiation/) by $a^n = a^{n-1} \cdot a$.** This uses $n - 1$ multiplications, the same as the brute-force product.

### Decrease by a constant factor

- **[Binary search](/binary-search/)** (Levitin 4.4). Compare the key with the middle item of a sorted array and keep one half. In the worst case it makes $\lfloor \log_2 n \rfloor + 1$ three-way comparisons: 10 for $n = 1000$ and 20 for $n = 10^6$.
- **[Exponentiation by squaring](/binary-exponentiation/).** Use $a^n = (a^{\lfloor n/2 \rfloor})^2$ for even $n$ and $a^n = (a^{\lfloor n/2 \rfloor})^2 \cdot a$ for odd $n$, with $a^1 = a$. Each level with $n \ge 2$ costs one squaring, plus one more product when $n$ is odd, so the count is $\lfloor \log_2 n \rfloor$ squarings plus (the number of 1 bits of $n$, less one) products. For $a^{13}$ the chain is $13 \to 6 \to 3 \to 1$, which uses 3 squarings and 2 products, 5 multiplications in all instead of 12; $3^{13} = 1{,}594{,}323$.
- **Fake coin** (Levitin 4.4; see the [counterfeit coin problem](/counterfeit-coin-problem/)). Among $n$ coins one is lighter. Put the coins in two equal piles on a balance, with one coin set aside when $n$ is odd, and keep the lighter pile (or the coin set aside, if the piles balance). The worst case satisfies $W(n) = W(\lfloor n/2 \rfloor) + 1$ with $W(1) = 0$, so by Claim 2 it uses $\lfloor \log_2 n \rfloor$ weighings: 6 for $n = 100$.
- **[Russian peasant multiplication](/russian-peasant-multiplication/)** (Levitin 4.4). Use $n \cdot m = (n/2) \cdot 2m$ for even $n$ and $n \cdot m = \lfloor n/2 \rfloor \cdot 2m + m$ for odd $n$. For $50 \cdot 65$ the rows are $(50, 65)$, $(25, 130)$, $(12, 260)$, $(6, 520)$, $(3, 1040)$ and $(1, 2080)$; the rows with an odd first number add up to $130 + 1040 + 2080 = 3250$.
- **[Josephus problem](/josephus-problem/)** (Levitin 4.4). With $n$ people in a circle and every second one eliminated, the survivor $J(n)$ satisfies $J(1) = 1$, $J(2k) = 2J(k) - 1$ and $J(2k+1) = 2J(k) + 1$. For $n = 41$ the chain $41, 20, 10, 5, 2, 1$ gives $J = 1, 1, 3, 5, 9, 19$ from the bottom up, so $J(41) = 19$.

### Variable-size decrease

- **[Euclid's algorithm](/euclidean-algorithm/)** (Levitin, Chapter 4 introduction). $\gcd(m, n) = \gcd(n, m \bmod n)$, and the size of the drop depends on the numbers. For $\gcd(1071, 462)$ the pairs are $(1071, 462)$, $(462, 147)$, $(147, 21)$ and $(21, 0)$, so the answer is 21. The number of steps is $O(\log \min(m, n))$ by [Lamé's theorem](/lames-theorem/).
- **[Quickselect](/quickselect/)** (Levitin 4.5). Partition around a pivot and continue in the one side that holds the $k$-th smallest item. The size of that side depends on the pivot: $\Theta(n)$ expected time with a random pivot, $\Theta(n^2)$ in the worst case. [Median of medians](/median-of-medians/) picks the pivot so that the worst case is $\Theta(n)$ (CLRS, Chapter 9).
- **[Interpolation search](/interpolation-search/)** (Levitin 4.5). Guess the position of the key from its value by linear interpolation between the end values, and keep the side that holds it. For keys drawn uniformly at random the expected number of probes is $O(\log \log n)$ ([interpolation search expected time](/interpolation-search-expected-time/)); in the worst case it is $\Theta(n)$.
- **[Search in a binary search tree](/bst-search/)** (Levitin 4.5). Compare with the root and go to one subtree. The size of the subtree depends on the shape of the tree, so the cost is the height: $O(\log n)$ in a balanced tree, $n$ in a path.

## Variations

- **Decrease and conquer versus divide and conquer.** Levitin keeps the two apart: decrease and conquer solves one smaller instance, divide and conquer solves several and combines them. Other authors put binary search under divide and conquer: CLRS place it among the exercises of the divide-and-conquer section (Section 2.3). Both views give the same algorithm and the same recurrence; only the name differs.
- **[Prune and search](/prune-and-search/).** A decrease-by-a-constant-factor method in which each round spends linear time to discard a constant fraction of the input. The cost $O(n + cn + c^2 n + \cdots) = O(n)$ for a fraction $c < 1$ is linear, not logarithmic, because each round looks at all the items that remain.
- **Iterative form.** When EXTEND only passes the answer up, the method is a loop with an invariant: binary search keeps the key inside the current range, Euclid's algorithm keeps the gcd of the current pair.
- **Bottom-up form.** Decrease by one can run from the small end: insertion sort grows a sorted prefix, and a generator of permutations grows the list from 1 item to $n$.
- **Decrease by more than half.** Splitting into three piles, as in the exercise on fake coins, reduces the size to about $n/3$ per weighing.

## Pitfalls

- **A reduction that does not reduce.** In a binary search on the range $[lo, hi]$ with the update $lo \leftarrow mid$, a range of two items can stay the same forever. The new range must exclude the middle item, or the size must drop in some other way.
- **Decrease by one where a factor is possible.** Computing $a^n$ by $a^{n-1} \cdot a$ costs $n - 1$ multiplications; squaring costs $O(\log n)$. Reading a sorted array item by item finds a key in $O(n)$; binary search does it in $O(\log n)$.
- **Deep recursion.** Decrease by one makes $n$ nested calls. Python stops at about 1000 frames by default. Write such algorithms as loops.
- **Treating a variable-size decrease as a fixed one.** Quickselect is not $O(\log n)$ steps of halving: a bad pivot removes only one item, and interpolation search can take $\Theta(n)$ probes when the keys are far from uniform. State the case (worst, expected) and the input model with each bound.
- **The recurrence of the wrong form.** $T(n) = T(n/2) + \Theta(1)$ is logarithmic, but $T(n) = T(n/2) + \Theta(n)$ is linear and $T(n) = T(n-1) + \Theta(n)$ is quadratic. The work per step matters as much as the size of the drop.

## Exercises

1. Prove Claim 2 for $T(n) = T(\lceil n/2 \rceil) + d$, $T(1) = c$, and show that the solution is $c + d \lceil \log_2 n \rceil$.
2. Among $n$ coins one is lighter. Show that a balance can find it in $\lceil \log_3 n \rceil$ weighings by splitting into three piles, and that no method that uses only the balance can do it with fewer weighings in the worst case. (Each weighing has three outcomes.)
3. Prove that $J(n) = 2(n - 2^{\lfloor \log_2 n \rfloor}) + 1$ for the Josephus problem with every second person eliminated, from the recurrence above. Check it for $n = 41$.
4. Write exponentiation by squaring as a loop that reads the bits of $n$ from the least significant bit. State a loop invariant and use it to prove the loop correct.
5. Give the recurrence for the number of comparisons of insertion sort on a sorted input and on an input in decreasing order, and solve both with Claim 1.

## References
