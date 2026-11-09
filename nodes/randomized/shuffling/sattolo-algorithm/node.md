---
tag: 6WKJFK
kind: algorithm
slug: sattolo-algorithm
name: Sattolo's algorithm
aliases:
- Sattolo shuffle
- Sattolo's shuffle
area: randomized/shuffling
level: core
summary: A Fisher-Yates variant that swaps A[i] only with a strictly earlier position. It gives each of the (n − 1)! permutations with one cycle of length n with probability 1/(n − 1)!.
solves: [random-cyclic-permutation]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 1986
  people: [Sandra Sattolo]
  note: Sattolo published the algorithm in Information Processing Letters in 1986.
prereqs: [fisher-yates-shuffle, permutation-cycles, random-cyclic-permutation]
see_also: [random-permutation, naive-shuffle, derangement, permutation-cycle-decomposition, cycle-leader-permutation, symmetric-group]
sources:
  - paper: doi:10.1016/0020-0190(86)90073-6
    title: Sandra Sattolo, An algorithm to generate a random cyclic permutation, Information Processing Letters 22(6), 1986
    locator: pp. 315 to 317 (the algorithm, its proof and its cost)
  - paper: doi:10.1007/BF01941134
    title: David Gries and Jinyun Xue, Generating a random cyclic permutation, BIT 28, 1988
    locator: the whole note (a proof of Sattolo's algorithm by the methods of program proving)
  - paper: doi:10.1007/s00026-009-0003-3
    title: Mark C. Wilson, Random and exhaustive generation of permutations and cycles, Annals of Combinatorics 13, 2009
    locator: the common framework for Fisher-Yates and Sattolo and the distribution of the number of moves of an item
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm P (the shuffle that Sattolo's algorithm changes)
---

Sattolo's algorithm generates a uniformly random *cyclic* permutation: a permutation of $n$ items that consists of one cycle through all $n$ positions. It is the [Fisher-Yates shuffle](/fisher-yates-shuffle/) with one change: the random index $j$ is drawn from $\{0, \ldots, i-1\}$ instead of $\{0, \ldots, i\}$. Each of the $(n-1)!$ cyclic permutations then has probability exactly $1/(n-1)!$. It solves the [random cyclic permutation](/random-cyclic-permutation/) problem in $\Theta(n)$ time and $O(1)$ extra space.

## In plain words

Think of the Fisher-Yates shuffle: go from the last place to the first, and at each place swap in a random card from the places that are not yet done. Sattolo's change is that the card at the current place is not allowed to stay there. It must swap with a card strictly before it.

The result is not a random order of the usual kind. It is a random "round": if you start at any place, look at which place its card came from, and follow these links, you visit every place once before you come back. Every such round has the same chance. No card ends where it started. This is useful when you need one big loop through all the items, for example a random tour, or a chain of pointers that visits every slot.

## The problem

The input is an array $A[0 \ldots n-1]$ with $n \ge 1$. The output rearranges it by a permutation $\sigma$ of $\{0, \ldots, n-1\}$: position $p$ gets the item from position $\sigma(p)$. The permutation $\sigma$ must be uniform on the set $C_n$ of [permutations](/permutation/) with exactly one [cycle](/permutation-cycles/), of length $n$. The set $C_n$ has $(n-1)!$ elements: write a cycle with 0 first, and order the other $n-1$ positions in any of $(n-1)!$ ways. This is the [random cyclic permutation](/random-cyclic-permutation/) problem.

If the input is $A = [0, 1, \ldots, n-1]$, the output $B$ is $\sigma$ itself, and $p \to B[p]$ is the cycle. RANDOM$(a, b)$ is uniform on $\{a, \ldots, b\}$, and the calls are independent.

## The algorithm

```pseudo id=main
SATTOLO(A)                                 ▷ A[0 .. n − 1]
L1  for i ← n − 1 downto 1 do
L2      j ← RANDOM(0, i − 1)               ▷ j < i: the item at i must move
L3      exchange A[i] and A[j]
```

The only difference from Fisher-Yates is line L2: the upper end is $i - 1$, not $i$. So the ranges have sizes $n-1, n-2, \ldots, 1$, and there are $(n-1)!$ choice sequences, as many as there are $n$-cycles. The last step, $i = 1$, has only one choice, $j = 0$.

## Example

Run SATTOLO on $A = [0, 1, 2, 3, 4, 5]$. Suppose that line L2 returns $j = 2, 0, 1, 0, 0$, from ranges of sizes 5, 4, 3, 2 and 1.

| $i$ | $j$ | $A$ after line L3 |
|---|---|---|
| start | | 0 1 2 3 4 5 |
| 5 | 2 | 0 1 5 3 4 2 |
| 4 | 0 | 4 1 5 3 0 2 |
| 3 | 1 | 4 3 5 1 0 2 |
| 2 | 0 | 5 3 4 1 0 2 |
| 1 | 0 | 3 5 4 1 0 2 |

The output is $B = [3, 5, 4, 1, 0, 2]$. Follow $p \to B[p]$ from 0: $0 \to 3 \to 1 \to 5 \to 2 \to 4 \to 0$. This is one cycle of length 6, and no item is at its start position. As in Fisher-Yates, the first choice can be read from the output: $B[5] = 2 = j$.

## Correctness

**Theorem.** If each call of RANDOM is uniform and independent, then for $n \ge 1$ the output permutation $\sigma$ is uniform on the $(n-1)!$ permutations of $\{0, \ldots, n-1\}$ with one cycle.

Let $t_i = (i\ j_i)$ be the swap of step $i$, with $j_i < i$. The output permutation is $\sigma = t_{n-1} \circ t_{n-2} \circ \cdots \circ t_1$. By induction on $n$, the product $\rho = t_{n-2} \circ \cdots \circ t_1$ is one cycle on $\{0, \ldots, n-2\}$. Composing with $(n-1\ j_{n-1})$, where $j_{n-1} \le n - 2$, inserts $n - 1$ into that cycle just before $j_{n-1}$. So $\sigma$ is one $n$-cycle. As in Fisher-Yates, $\sigma(n-1) = j_{n-1}$, so the output determines the choices, and the map from the $(n-1)!$ choice sequences to the $(n-1)!$ cycles is a bijection. Each sequence has probability $1/(n-1)!$. The full proof is below.

## Complexity

The loop runs $n - 1$ times, with one call of RANDOM and one swap each, so the time is $\Theta(n)$ in each case and the extra space is $O(1)$, as for Fisher-Yates. The ranges have sizes $n-1, \ldots, 1$, so the algorithm uses exactly $\log_2 (n-1)!$ bits of randomness in the uniform-integer model, the entropy of its output. With fair bits and rejection at each step, the expected cost is $\sum_{m=2}^{n-1} \lceil \log_2 m \rceil \, 2^{\lceil \log_2 m \rceil} / m$ bits, by the same argument as on the [Fisher-Yates page](/fisher-yates-shuffle/).

## Properties

- **Exact.** Each cycle has probability exactly $1/(n-1)!$ in the model of exact uniform integers.
- **No fixed points.** Each item moves. So the output is a [derangement](/derangement/), but not a uniform derangement: for $n \ge 4$ there are derangements with more than one cycle, and Sattolo never gives them.
- **The identity is never the output** for $n \ge 2$. For $n = 1$ the one cycle is the identity, and the loop does not run.
- **In place and a bijection with the choice sequences**, like Fisher-Yates.

## Variants and improvements

- **Shuffle, then link.** Draw a uniform order $(x_0, \ldots, x_{n-1})$ with Fisher-Yates and set $\sigma(x_k) = x_{k+1}$, with $x_n = x_0$. Each $n$-cycle comes from exactly $n$ orders, its rotations, so the cycle is uniform. This uses $n - 1$ random integers and an extra array, so Sattolo is better.
- **Ascending form.** For $i = 0$ to $n - 2$, swap $A[i]$ with $A[\text{RANDOM}(i+1, n-1)]$. This is uniform on the cycles by the mirror proof.
- **Uniform derangements.** Draw uniform permutations and reject those with a fixed point. The acceptance rate is $D_n/n! \to 1/e$, so about $e \approx 2.72$ tries are expected. Faster exact methods exist, but Sattolo is not one of them.

## When to use it

Use Sattolo's algorithm when the output must be one cycle: a random tour of all items, a "next" pointer for each slot that visits every slot (as in pointer-chasing tests of memory latency), or a random cyclic order of players. Use [Fisher-Yates](/fisher-yates-shuffle/) when you need a uniform order. Do not use Sattolo for a "secret Santa" draw that should be a uniform derangement: it gives only the single-cycle ones.

## Pitfalls

- **Using Sattolo as a shuffle.** Line L2 with RANDOM$(0, i - 1)$ is an off-by-one bug in a shuffle: the output is never the identity, and only $(n-1)!$ of the $n!$ orders are possible. If a shuffle is wanted, line L2 must be RANDOM$(0, i)$.
- **Reading the cycle the wrong way.** The output satisfies $B[p] = \sigma(p)$ when the input is the identity. For other inputs, $B[p] = A[\sigma(p)]$, so the cycle is on positions, not on the values of the items.
- **Modulo bias.** As in Fisher-Yates, line L2 must draw a uniform integer; `word mod i` is biased. See [modulo bias](/modulo-bias/).

## Implementations

## History

Sandra Sattolo published the algorithm in 1986 in Information Processing Letters, with a proof and a statistical test. Gries and Xue gave a proof by the methods of program verification in 1988. Later papers, for example by Prodinger, Mahmoud and Wilson, studied the number of times each item moves; Wilson treats Fisher-Yates and Sattolo in one framework.

## References
