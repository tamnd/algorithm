---
tag: H5FM3F
kind: algorithm
slug: floyd-sampling
name: Floyd's sampling algorithm
aliases:
- Floyd's algorithm for random subsets
- Bentley-Floyd sampling
area: randomized/sampling
level: core
summary: Picks a uniform k-subset of {0, ..., n-1} with exactly k random draws and no rejections, keeping the subset in a hash set, in O(k) expected time and O(k) space.
solves: [uniform-random-subset]
model: word-ram
complexity:
  vars: {n: the size of the ground set, k: the sample size}
  time: {expected: Θ(k), worst: "O(k^2)"}
  space: {extra: Θ(k)}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1987
  people: [Robert W. Floyd, Jon Bentley]
  note: Bentley presented Floyd's sampling algorithm in his Programming Pearls column "A sample of brilliance" in Communications of the ACM in 1987.
prereqs: [hash-table, uniform-distribution, binomial-coefficient]
see_also: [selection-sampling, reservoir-sampling, uniform-random-subset, fisher-yates-shuffle, rejection-sampling]
sources:
  - paper: doi:10.1145/30401.315746
    title: Jon Bentley and Bob Floyd, Programming pearls, A sample of brilliance, Communications of the ACM 30(9), 754 to 757, 1987
    locator: Floyd's iterative and recursive sampling algorithms and the random permutation variant
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2 (the scan methods, Algorithms S and R, for comparison)
---

Floyd's sampling algorithm picks a uniform random $k$-subset of $\{0, 1, \ldots, n - 1\}$ with exactly $k$ random integers and no retries. For $j = n - k, \ldots, n - 1$ it draws $t$ uniform in $\{0, \ldots, j\}$ and adds $t$ to the set, or adds $j$ if $t$ is already there. With the set in a [hash table](/hash-table/), the expected time is $O(k)$ and the space is $O(k)$, whatever the size of $n$. Robert Floyd found it, and Jon Bentley published it in his Programming Pearls column in 1987. It is the method of choice when $k$ is small and $n$ is huge, where a scan such as [selection sampling](/selection-sampling/) costs $\Theta(n)$.

## In plain words

You want 4 different lottery numbers from 0 to 9. The plain way is to draw again whenever you get a repeat, which can take many draws. Floyd's way never draws again.

Start with a smaller lottery, from 0 to 6, and pick one number. Then widen the range by one, to 0 to 7, and draw. If the number is new, keep it. If you already have it, keep the new top number 7 instead, which you cannot have yet. Widen again to 0 to 8, and so on, until the range is 0 to 9. At each stage your set is a fair pick from the current range. The repeat rule is what keeps it fair: the top number gets exactly the extra chance it needs.

## The problem

The input is two integers $n$ and $k$ with $0 \le k \le n$, and the output is a uniform random $k$-subset of $\{0, \ldots, n - 1\}$: each of the $\binom{n}{k}$ subsets has the same probability. The ground set is given by its size, not as a list, so the method can sample from a range of $10^{18}$ numbers. To sample items from an array, sample their indices. This is the [uniform random subset](/uniform-random-subset/) problem.

## The algorithm

```pseudo id=main
FLOYD-SAMPLE(n, k)                        ▷ 0 ≤ k ≤ n
L1  S ← an empty hash set
L2  for j ← n − k to n − 1
L3      t ← a uniform random integer in {0, ..., j}
L4      if t ∉ S then insert t into S
L5      else insert j into S                   ▷ j is never in S yet
L6  return S
```

Before the round for $j$, $S$ is a subset of $\{0, \ldots, j - 1\}$, so $j \notin S$ and line L5 always adds a new element. Each round adds exactly one element. Bentley's column also gives the method in recursive form: to pick $k$ from $\{0, \ldots, n-1\}$, first pick $k - 1$ from $\{0, \ldots, n - 2\}$, then do one round with $j = n - 1$.

## Example

Take $n = 10$ and $k = 4$, so $j$ runs from 6 to 9.

| $j$ | range | $t$ drawn | $t \in S$? | added | $S$ after |
|---|---|---|---|---|---|
| 6 | 0 to 6 | 3 | no | 3 | $\{3\}$ |
| 7 | 0 to 7 | 3 | yes | 7 | $\{3, 7\}$ |
| 8 | 0 to 8 | 8 | no | 8 | $\{3, 7, 8\}$ |
| 9 | 0 to 9 | 0 | no | 0 | $\{0, 3, 7, 8\}$ |

Four draws give four distinct numbers. In round $j = 7$ the draw repeated 3, and the rule added 7 instead. In round $j = 8$ the draw was the new top number itself. The element $j$ is added in both of these cases, so it enters with probability $(|S| + 1)/(j + 1)$, which is exactly its chance of being in a uniform subset of size $|S| + 1$ of $\{0, \ldots, j\}$.

## Correctness

**Theorem (Floyd; Bentley 1987).** FLOYD-SAMPLE$(n, k)$ draws exactly $k$ integers and returns each $k$-subset of $\{0, \ldots, n - 1\}$ with probability $1/\binom{n}{k}$.

The proof is by induction on the rounds: after the round for $j$, $S$ is a uniform subset of $\{0, \ldots, j\}$ of size $i + 1$, where $i$ is the number of earlier rounds. To get a given set $B$ of size $i + 1$: if $j \in B$, the old set must be $B \setminus \{j\}$ and $t$ must be one of its $i$ elements or $j$ itself; if $j \notin B$, the old set must be $B$ minus one element $x$ and $t$ must be $x$. Both cases give $i + 1$ good values of $t$ out of $j + 1$, so $\Pr[B] = \frac{i+1}{(j+1)\binom{j}{i}} = 1/\binom{j+1}{i+1}$. The full proof is below.

## Complexity

- **Random numbers.** Exactly $k$, against about $k$ plus the expected number of repeats for the draw-and-retry method, and $n$ or up to $n$ for a scan.
- **Time.** $k$ membership tests and $k$ insertions. With a hash set this is $O(k)$ expected time. With a balanced search tree it is $O(k \log k)$ worst case, and the set comes out sorted. With a plain list, each test costs $O(k)$, for $O(k^2)$ in total.
- **Space.** $\Theta(k)$ for the set. No array of size $n$ is needed.
- **Arithmetic.** The numbers are below $n$, so they fit in a word whenever $n$ does.

## Properties

- **No rejection.** The number of draws is fixed at $k$, so the run time does not depend on luck, apart from the hash set.
- **Independent of n.** Time and space depend only on $k$. Sampling 5 numbers from $\{0, \ldots, 10^{18} - 1\}$ costs the same as from $\{0, \ldots, 9\}$.
- **Set, not sequence.** The order in which elements were inserted is not uniform: element $n - 1$ can only enter in the last round. If a uniformly random order is needed, use the permutation variant below or shuffle the result.
- **Exact.** With uniform integer draws, there is no rounding.

## Variants and improvements

- **Random permutation variant.** Keep $S$ as a sequence. If $t \notin S$, put $t$ at the front; otherwise insert $j$ right after $t$. Bentley's column gives this variant, which yields a uniformly random ordered $k$-sample.
- **Partial Fisher-Yates.** Running $k$ steps of a [Fisher-Yates shuffle](/fisher-yates-shuffle/) on an array of $n$ items gives a random ordered $k$-sample with $k$ draws, but needs the array, or a hash map that stores only the swapped entries.
- **Draw and retry.** Draw uniform numbers in $\{0, \ldots, n-1\}$ and drop repeats. For $k \le n/2$ the expected number of draws is below $2k$, but it is random and grows to about $n \ln n$ as $k$ nears $n$. This is [rejection sampling](/rejection-sampling/) in its simplest form.
- **Scans.** [Selection sampling](/selection-sampling/) and [reservoir sampling](/reservoir-sampling/) give the sample in one pass over the items, in $\Theta(n)$ time, and the first keeps input order.

## When to use it

Use Floyd's algorithm when $n$ is large or not stored, $k$ is much smaller than $n$, and you can name items by index: picking 100 random rows out of $10^9$, random test cases from a huge range, or random IDs. It uses as few random numbers as any method here and no memory beyond the sample. When the items come as a stream, use [reservoir sampling](/reservoir-sampling/). When $k$ is close to $n$, pick the complement, $n - k$ items, and output the rest, or shuffle.

## Pitfalls

- **The range of t.** The draw must be in $\{0, \ldots, j\}$, *including* $j$. Drawing from $\{0, \ldots, j - 1\}$ gives some subsets more weight than others.
- **Adding t twice.** When $t \in S$, the rule adds $j$. Skipping the round instead, or drawing again with the same $j$, breaks either the size or the uniformity.
- **Off-by-one in the loop.** The loop must start at $j = n - k$, not $n - k + 1$, to run exactly $k$ rounds.
- **Treating the insertion order as random.** It is not uniform. Sort the set or shuffle it if the order matters.
- **Biased integer draws.** The method is only as uniform as the draw in line L3. Taking a random word modulo $j + 1$ is biased; use an unbiased bounded draw.

## Implementations

## History

Robert W. Floyd devised the algorithm, and Jon Bentley presented it in his Programming Pearls column "A sample of brilliance" in Communications of the ACM in September 1987, together with a recursive form and a variant that produces a random permutation. The column contrasts it with the scan of Knuth's Algorithm S and with methods that draw and retry.

## References
