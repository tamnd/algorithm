---
tag: NRAJQ8
kind: algorithm
slug: fisher-yates-shuffle
name: Fisher-Yates shuffle
aliases:
- Knuth shuffle
- Durstenfeld shuffle
- Fisher-Yates-Knuth shuffle
- Algorithm P
area: randomized/shuffling
level: intro
summary: Put n items in a uniformly random order in place. For i from n − 1 down to 1, swap A[i] with A[j] for a uniform j in 0..i. Each of the n! orders has probability exactly 1/n!.
solves: [random-permutation]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: false, deterministic: false, recursive: false}
history:
  year: 1938
  people: [Ronald A. Fisher, Frank Yates, Richard Durstenfeld]
  note: Fisher and Yates gave a pencil-and-paper method in 1938. Durstenfeld gave the in-place computer form in 1964.
prereqs: [random-permutation, permutation, uniform-distribution]
see_also: [naive-shuffle, sattolo-algorithm, permute-by-sorting, merge-shuffle, uniform-random-integer-generation, modulo-bias, reservoir-sampling, sort-based-shuffle]
sources:
  - book: "Ronald A. Fisher and Frank Yates, Statistical Tables for Biological, Agricultural and Medical Research, Oliver and Boyd, 1938"
    locator: the introduction on the use of the tables of random numbers to put items in a random order (later editions keep the method; locator to be checked)
  - paper: doi:10.1145/364520.364540
    title: Richard Durstenfeld, Algorithm 235, Random permutation, Communications of the ACM 7(7), 1964
    locator: p. 420 (the ALGOL procedure SHUFFLE)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Random sampling and shuffling, Algorithm P (Shuffling)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 5.3, Randomized algorithms (the procedure RANDOMLY-PERMUTE and the proof by a loop invariant that it is uniform)
  - paper: doi:10.1145/3230636
    title: Daniel Lemire, Fast random integer generation in an interval, ACM Transactions on Modeling and Computer Simulation 29(1), 2019
    locator: Section 2 (the bias of the modulo method and the rejection method)
---

The Fisher-Yates shuffle puts $n$ items in a uniformly random order, so that each of the $n!$ orders has probability exactly $1/n!$. Durstenfeld's form works in place: for $i$ from $n-1$ down to $1$, it swaps $A[i]$ with $A[j]$, where $j$ is a uniform integer in $\{0, \ldots, i\}$. It uses $n - 1$ random integers and $n - 1$ swaps, so it takes $\Theta(n)$ time and $O(1)$ extra space. It is the standard solution of the [random permutation](/random-permutation/) problem, and the library shuffle of most languages.

## In plain words

Put the cards in a row. Pick one card at random from the whole row and swap it with the last card. The last place now holds a random card, and you never touch it again. Now do the same with the row without its last place: pick one of the cards that are left, at random, and swap it into the second-to-last place. Go on until one card is left.

Each step picks from the cards that are not yet placed, and each of them is equally likely. So the last place gets each card with the same chance, the next place gets each remaining card with the same chance, and so on. Every order of the cards comes out with the same chance. A common mistake is to pick from the whole row at each step. That small change makes some orders more likely than others.

## The problem

The input is an array $A[0 \ldots n-1]$. The output is the same items in an order $\sigma$ such that $\Pr[\sigma = \tau] = 1/n!$ for each of the $n!$ orders $\tau$, whatever the input order was. This is the [random permutation](/random-permutation/) problem. Equal items are allowed: the claim is about the positions, so each of the $n!$ rearrangements of positions has probability $1/n!$.

**Model of randomness.** RANDOM$(a, b)$ returns an integer that is uniform on $\{a, a+1, \ldots, b\}$ and independent of all earlier calls. On a [word RAM](/word-ram/) we count one call as $O(1)$ time. The section on cost below gives the number of random bits when RANDOM is built from fair bits.

## The algorithm

```pseudo id=main
FISHER-YATES(A)                            ▷ A[0 .. n − 1], Durstenfeld's in-place form
L1  for i ← n − 1 downto 1 do
L2      j ← RANDOM(0, i)                   ▷ uniform on {0, 1, ..., i}, j = i is allowed
L3      exchange A[i] and A[j]
```

The positions $i+1, \ldots, n-1$ form the *done* part: each of them holds its final item. The positions $0, \ldots, i$ hold the items that are not yet placed. Step $i$ picks one of these $i+1$ items uniformly and moves it to position $i$. The case $j = i$ leaves the item where it is, and it must stay possible. Without it the algorithm is [Sattolo's algorithm](/sattolo-algorithm/), which gives only the cyclic permutations.

**Inside-out form.** When the input is read once from a stream, or when the input must not change, the same idea runs from left to right into a new array $B$:

```pseudo id=inside-out
INSIDE-OUT(S)                              ▷ S[0 .. n − 1] is not changed
    for i ← 0 to n − 1 do
        j ← RANDOM(0, i)
        B[i] ← B[j]                         ▷ when j = i this copies a slot that is about to be set
        B[j] ← S[i]
    return B
```

After the step for $i$, the prefix $B[0 \ldots i]$ is a uniform order of $S[0 \ldots i]$. This is the same insertion step that [merge shuffle](/merge-shuffle/) uses to finish its merges.

## Example

Shuffle $A = [a, b, c, d, e, f]$, with $n = 6$. Suppose the five calls of line L2 return $j = 1, 4, 0, 2, 0$. These calls choose from 6, 5, 4, 3 and 2 values.

| $i$ | $j$ | $A$ after line L3 | done part |
|---|---|---|---|
| start | | a b c d e f | none |
| 5 | 1 | a f c d e **b** | b |
| 4 | 4 | a f c d **e** b | e b |
| 3 | 0 | d f c **a** e b | a e b |
| 2 | 2 | d f **c** a e b | c a e b |
| 1 | 0 | **f d** c a e b | all |

The output is $[f, d, c, a, e, b]$. The choices can be read back from the output. The last item, $b$, was at position 1 at the start, so the first choice was $j = 1$. Undo that swap and repeat on the first five positions. This map from the $6 \cdot 5 \cdot 4 \cdot 3 \cdot 2 = 720$ choice sequences to the $6! = 720$ orders is one to one, and this is the second proof below.

## Correctness

**Theorem.** If each call of RANDOM is uniform and independent, FISHER-YATES gives each of the $n!$ arrangements of the positions of $A$ with probability exactly $1/n!$.

The loop of line L1 keeps this [loop invariant](/loop-invariant/): before the iteration for $i$, for each sequence $(x_{i+1}, \ldots, x_{n-1})$ of distinct input positions, the probability that the done part $A[i+1 \ldots n-1]$ holds the items from these positions, in this order, is $(i+1)!/n!$. Step $i$ picks each of the $i+1$ items that are left with probability $1/(i+1)$, which gives $i!/n!$ for the longer done part. At the end $i = 0$, so each full order has probability $1/n!$. The full proof, by this induction and by the bijection with the choice sequences, is below.

## Complexity

**Time.** Lines L2 and L3 run $n - 1$ times, and each run costs $O(1)$ on a word RAM with an $O(1)$ RANDOM. So the time is $\Theta(n)$ in each case, for $n \ge 1$, and the extra space is $O(1)$: the index $i$, the choice $j$ and one temporary item for the swap. The random choices change which items move, but not the number of steps. The inside-out form also takes $\Theta(n)$ time, with $\Theta(n)$ space for $B$.

**Random integers.** The algorithm makes exactly $n - 1$ calls of RANDOM, with ranges of sizes $n, n-1, \ldots, 2$. The product of the sizes is $n!$, so no outcome is wasted: each choice sequence gives a different order.

**Random bits.** A source of fair bits gives a uniform integer in a range of size $m$ by rejection. Draw $k = \lceil \log_2 m \rceil$ bits as a number $v$ in $[0, 2^k)$, and draw again while $v \ge m$. One draw succeeds with probability $m / 2^k > 1/2$, so the number of draws is [geometric](/geometric-distribution/) with mean $2^k / m < 2$, and the expected number of bits is $k \, 2^k / m < 2k$. For the shuffle this gives
$$\mathbb{E}[\text{bits}] = \sum_{m=2}^{n} \frac{\lceil \log_2 m \rceil \, 2^{\lceil \log_2 m \rceil}}{m} < 2 \sum_{m=2}^{n} \lceil \log_2 m \rceil = O(n \log n).$$
No method can use fewer than $\log_2 n!$ bits on average, because its output has $n!$ equally likely values (the bound of Knuth and Yao, on the [uniform random integer generation](/uniform-random-integer-generation/) page).

| $n$ | 3 | 10 | 52 | 1000 |
|---|---|---|---|---|
| expected bits, rejection at each step | 3.67 | 34.41 | 355.91 | 12507.72 |
| lower bound $\log_2 n!$ | 2.58 | 21.79 | 225.58 | 8529.40 |

Methods that reuse the unused part of a rejected draw, such as Lumbroso's Fast Dice Roller or [Lemire's method](/lemire-bounded-integers/) on 64-bit words, come closer to the lower bound.

**Modulo bias.** The tempting code `j = word mod (i + 1)` is not uniform when $i + 1$ does not divide the number of word values. With $w$-bit words, the $2^w \bmod (i+1)$ smallest residues have one more preimage than the others; see [modulo bias](/modulo-bias/). A tiny case shows the effect on the shuffle. With 3-bit words, $n = 3$ and $j = \text{word} \bmod (i + 1)$, the 64 pairs of words give the orders $[0,1,2]$ and $[1,0,2]$ with probability $8/64 = 1/8$ each, and the other four orders with probability $12/64 = 3/16$ each. With 32-bit words and $i + 1 = 52$, 48 residues have probability $82595525/2^{32}$ and 4 residues have $82595524/2^{32}$. The bias is small for one draw, but it is not zero, and rejection removes it for an expected cost of less than one extra draw.

## Properties

- **Exact.** In the model of exact uniform integers, the output is exactly uniform. No bias remains for small or large $n$.
- **In place.** Only the swaps of line L3 change the array.
- **A bijection with the choice sequences.** The output determines the choices. So the shuffle can also *rank* and *unrank* permutations: the choice sequence is a number in the [factorial number system](/factorial-number-system/), close to the [Lehmer code](/lehmer-code/).
- **Any prefix of the run is useful.** After the steps for $i = n-1, \ldots, n-k$, the done part is a uniform ordered sample of $k$ distinct items. This partial shuffle costs $\Theta(k)$ time.
- **Not stable and not deterministic.** The output depends on the random choices, and equal items can change order.

## Variants and improvements

- **The ascending form.** For $i = 0$ to $n - 2$, swap $A[i]$ with $A[\text{RANDOM}(i, n-1)]$. This is RANDOMLY-PERMUTE in CLRS. It fills the array from the left and is uniform by the same proof.
- **Inside-out.** The block above. It shuffles a stream of unknown length when the output fits in memory, and it builds a shuffled copy in one pass.
- **Partial shuffle.** Stop after $k$ steps to get a uniform random $k$-permutation, as in [uniform random subset](/uniform-random-subset/) and [Floyd's sampling](/floyd-sampling/) when $k \ll n$.
- **Sattolo's algorithm.** Draw $j$ from $\{0, \ldots, i-1\}$ to get a uniform [cyclic permutation](/random-cyclic-permutation/). See [Sattolo's algorithm](/sattolo-algorithm/).
- **Knuth's Algorithm P.** The same loop with a uniform real $U$ and $k = \lfloor jU \rfloor + 1$ in 1-based indexing. With a floating point $U$ of 53 random bits, $\lfloor jU \rfloor$ is exactly uniform only when $j$ is a power of two. Each value then has probability within $2^{-53}$ of $1/j$. Use an integer method when exactness matters.
- **Parallel and cache-friendly forms.** [Merge shuffle](/merge-shuffle/) and the method of Rao and Sandelius split the array and work on the parts. They use about $n \log_2 n$ random bits, and their parts can run at the same time.

## When to use it

Use Fisher-Yates whenever the items are in an array: it is exact, linear, in place and simple. Use the inside-out form for a stream whose length is not known in advance, or [reservoir sampling](/reservoir-sampling/) when only $k$ items of the stream must be kept. Use [permute by sorting](/permute-by-sorting/) only when a sort is the only tool, for example in a database query or a sorting network. For a linked list, copy the items to an array, or see [shuffling a linked list](/shuffling-a-linked-list/). For a very large array on many cores or on disk, [merge shuffle](/merge-shuffle/) has better locality.

## Pitfalls

- **Picking from the whole array.** Line L2 must draw from $\{0, \ldots, i\}$. With RANDOM$(0, n-1)$ the result is the [naive shuffle](/naive-shuffle/), which is biased for each $n \ge 3$, because $n^n$ is not a multiple of $n!$.
- **Excluding $j = i$.** RANDOM$(0, i - 1)$ in line L2 gives [Sattolo's algorithm](/sattolo-algorithm/). Its output is never the identity and never has a fixed point.
- **Modulo instead of rejection.** `word mod (i + 1)` in line L2 is biased; see the example above and [modulo bias](/modulo-bias/).
- **A small seed.** A [pseudorandom generator](/pseudorandom-number-generator/) with a $b$-bit seed can give at most $2^b$ different shuffles from a fresh seed. A deck of 52 cards has $52! \approx 8.07 \cdot 10^{67} \approx 2^{225.6}$ orders, so a 64-bit seed reaches a tiny fraction of them. For games of chance, seed from a [cryptographically secure generator](/cryptographically-secure-prng/) with at least 226 bits of state.
- **A random comparator.** Sorting with a comparator that returns a random answer is not a shuffle. It is biased; see [sort-based shuffle](/sort-based-shuffle/).

## Implementations

## History

Ronald A. Fisher and Frank Yates described the method in 1938, in their book of statistical tables, as a pencil-and-paper procedure: write the numbers 1 to $n$, choose a random number $k$ among the numbers not yet struck out, strike out the $k$-th of them, and write it down. Each step needs a count of the numbers that are left, so the procedure takes $\Theta(n^2)$ time when it is done this way. Richard Durstenfeld published the in-place version for computers in 1964, as Algorithm 235 of the Communications of the ACM: the swap moves the chosen item out of the way in $O(1)$ time. Knuth included it as Algorithm P in Section 3.4.2 of The Art of Computer Programming, so it is also called the Knuth shuffle.

## References
