---
tag: RBNB5G
kind: technique
slug: brute-force-search
name: Brute-force search
aliases:
- exhaustive search
- complete enumeration
- brute force
area: combinatorics/exhaustive-search
level: intro
summary: Enumerate every candidate solution and keep the best or first valid one.
prereqs: [search-space, asymptotic-notation]
see_also: [generate-and-test, search-space, combinatorial-explosion, generic-backtracking-algorithm, depth-first-branch-and-bound, horowitz-sahni-algorithm, power-set-enumeration, exact-exponential-algorithms]
sources:
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition
    locator: Chapter 3, Brute force and exhaustive search (Section 3.4, the traveling salesman, knapsack and assignment problems by exhaustive search)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.1, Computational tractability (brute-force search as the baseline that an efficient algorithm must beat)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the passage from the list of all candidates to the backtrack tree)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 9, Combinatorial search
---

Brute-force search solves a problem by listing every candidate in a complete [search space](/search-space/), testing each one, and keeping the first valid candidate, all valid ones, or the best one. It needs no insight into the problem beyond a way to list the candidates and a way to test them, so it is easy to write and easy to prove correct. Its cost is the size of the space times the cost of one test, and the [combinatorial explosion](/combinatorial-explosion/) of that size limits it to small inputs. It is also the reference against which faster methods are tested.

## In plain words

You lost the code of a bicycle lock with three dials. You try 000, then 001, then 002, and so on up to 999. One of them opens the lock. This is brute force: try everything, in an order that misses nothing.

The method has two parts. One part produces the candidates one by one, with no repeats and no gaps. The other part checks a candidate. If you want the best answer rather than any answer, you keep the best one seen so far and compare each new candidate with it.

Brute force always gives the right answer if the list really contains every candidate. Its problem is time: the number of candidates often doubles with each new item in the input.

## When it applies

Brute-force search applies when all three of these hold.

- **A finite complete space.** There is a finite set $S$ of candidates that contains every solution, or at least one optimal solution if the task is to optimize.
- **A generator.** There is a procedure that lists $S$ with each member once. Standard generators exist for the usual spaces: [all subsets](/power-set-enumeration/), [all $k$-subsets](/k-subset-enumeration/), [all permutations](/generating-all-permutations/), and all tuples in $D_1 \times \cdots \times D_n$.
- **A test.** For each candidate $x$ one can decide whether $x$ is valid, and compute its cost $c(x)$ if there is one.

It is the right choice when $|S|$ is small enough for the time budget, when it is used once to check a faster program, or when no better method is known and the input is small. It is the wrong choice when partial candidates can be tested: then [backtracking](/generic-backtracking-algorithm/) gives the same answers and visits far fewer nodes.

## The template

```pseudo id=main
BRUTE-FORCE(I)                       ▷ returns a valid candidate of least cost, or NONE
L1  best ← NONE
L2  for each x in S(I) do                ▷ the generator lists each candidate once
L3      if VALID(I, x) then
L4          if best = NONE or COST(I, x) < COST(I, best) then
L5              best ← x
L6  return best
```

For a search problem without costs, return $x$ at line L5 to get the first valid candidate, or output $x$ there and go on to get all of them.

**Correctness.** The loop keeps this invariant: after the candidates $x_1, \ldots, x_j$ of $S$ have been examined, $best$ is NONE if none of them is valid, and otherwise it is a valid candidate among them of least cost (the first such one, because line L4 uses a strict $<$). The invariant holds with $j = 0$, and lines L3 to L5 keep it. After the last candidate, $j = |S|$, so $best$ is a valid candidate of least cost in $S$. If $S$ is complete, it is optimal for the instance.

**Cost.** Let $t_g$ be the time to produce the next candidate and $t_v$ the time for lines L3 and L4. The time is $\Theta(|S| (t_g + t_v))$ in each case where the whole space is scanned, and the extra space is that of one candidate plus the state of the generator. With a Gray-code style generator, consecutive candidates differ by one small change, and $t_g$ and often $t_v$ become $O(1)$ amortized.

**A lower bound for black-box tests.** Suppose that the method can learn about the predicate only by calls VALID$(x)$. Then each deterministic method that decides whether some $x \in S$ is valid makes $|S|$ calls in the worst case. *Proof.* An adversary answers "not valid" to each call. If the method stops after fewer than $|S|$ calls, some $y \in S$ was never asked. The predicate that is false everywhere and the predicate that is true only at $y$ give the same answers to all calls, but they need different outputs, so the method is wrong on one of them. So brute force is optimal when nothing is known about the test, and every faster method must use the structure of the problem.

## Classic examples

**0/1 knapsack.** Items with (weight, value) $(2, 3)$, $(3, 4)$, $(4, 5)$, $(5, 6)$ and capacity 5. The space is the $2^4 = 16$ subsets. Six of them fit: the empty set, $\{1\}$, $\{2\}$, $\{3\}$, $\{4\}$ and $\{1, 2\}$, with values 0, 3, 4, 5, 6 and 7. The search returns $\{1, 2\}$ with value 7. In general the time is $\Theta(2^n n)$ if each subset is summed from scratch, and $\Theta(2^n)$ if a Gray code changes one item per step and the sums are updated. Compare the [knapsack problem](/knapsack-problem/) page for the dynamic program.

**Traveling salesman.** Fix city 1 and list the $(n-1)!$ orders of the other cities, each with its tour length. The search takes $\Theta(n!)$ time. For 10 cities there are 362,880 orders, or 181,440 tours up to direction.

**Closest pair of points.** Compute the distance of each of the $\binom{n}{2}$ pairs and keep the least. This takes $\Theta(n^2)$ time, which is polynomial. Divide and conquer brings it to $\Theta(n \log n)$.

**String matching.** The [naive string matching](/naive-string-matching/) algorithm tries each of the $n - m + 1$ shifts of a pattern of length $m$ in a text of length $n$, in $O(nm)$ time.

**Key search.** An [exhaustive key search](/exhaustive-key-search/) tries all $2^k$ keys of a cipher with $k$-bit keys. The 56-bit DES key space has $2^{56} \approx 7.2 \times 10^{16}$ keys.

## Variations

- **Early exit.** For a search problem, stop at the first valid candidate. The worst case is unchanged.
- **Incremental update.** List the candidates so that neighbors differ a little, with a [Gray code](/gray-code/) for subsets or [Heap's algorithm](/heaps-algorithm/) for permutations, and update the cost instead of recomputing it.
- **Smaller space.** Encode constraints in the representation and remove symmetric copies. This changes $|S|$, not the method.
- **Pruning.** Test prefixes of candidates and cut the ones that cannot lead to a solution: [backtracking](/generic-backtracking-algorithm/). With a bound on the cost of each extension, this is [branch and bound](/depth-first-branch-and-bound/).
- **Meet in the middle.** Split the decisions into two halves, list each half, and join the two lists. [Horowitz and Sahni](/horowitz-sahni-algorithm/) solve subset sum this way in $O(2^{n/2} n)$ time.
- **Parallel search.** The candidates are independent, so the space splits into parts with no communication. Large brute-force searches, such as the search for optimal [Golomb rulers](/golomb-ruler-problem/), ran on many computers at once.

## Pitfalls

- **An incomplete space.** If the generator misses a candidate, the result can be wrong with no sign of error. Check the generator alone: count its output against the closed form, such as $2^n$ or $n!$, and check that there are no repeats.
- **A space that is far too large.** Estimate $|S|$ before the run. A program that is correct for $n = 12$ may need years for $n = 20$.
- **A full recomputation per candidate.** Computing the cost of each subset from scratch adds a factor $n$. An incremental order removes it.
- **Storing all candidates.** Do not build the list of all candidates in memory. Generate them one at a time.
- **Bit masks that overflow.** A loop over masks $0 \le m < 2^n$ with 32-bit or 64-bit integers fails silently when $n$ reaches the word size.
- **Ties.** With $<$ in line L4 the first optimal candidate wins, and with $\le$ the last one. Tests that compare with another program must use the same rule.

## Exercises

1. Write a brute-force search for the largest clique of a graph on $n$ vertices. What is its running time as a function of $n$ and of the number of edges $m$?
2. Show that brute force over all $n!$ orders of a sequence can be replaced by a search over $n!/2$ orders when the cost of an order equals the cost of its reverse. Which candidates do you keep?
3. Give a version of BRUTE-FORCE for the knapsack example that visits the 16 subsets in [binary reflected Gray code](/binary-reflected-gray-code/) order and updates the weight and the value in $O(1)$ time per step.
4. Prove that each deterministic method that finds the unique valid candidate among $N$, using only calls to VALID, makes at least $N - 1$ calls in the worst case. Why is it not $N$?

## References
