---
tag: FZMWQ7
kind: problem
slug: uniform-random-subset
name: Uniform random subset
aliases:
- sampling without replacement
- random k-subset
- simple random sampling
- random combination
area: randomized/sampling
level: intro
summary: Choose k distinct items from n so that every k-subset is equally likely.
prereqs: [binomial-coefficient, linearity-of-expectation, harmonic-series]
see_also: [floyd-sampling, selection-sampling, reservoir-sampling, fisher-yates-shuffle, stream-sampling, systematic-sampling, stratified-sampling, combinatorial-number-system]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 3.4.2 (Random Sampling and Shuffling), Algorithm S (selection sampling), Algorithm R (reservoir sampling) and Algorithm P (shuffling)
  - paper: doi:10.1145/30401.315746
    title: Jon Bentley and Bob Floyd, Programming pearls, A sample of brilliance, Communications of the ACM 30(9), 754 to 757, 1987
    locator: Floyd's sampling algorithm with exactly k random integers, and the variant that gives a random permutation of the sample
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: Algorithm R and the methods with skips for the case of unknown n
---

The uniform random subset problem asks for $k$ distinct items out of $n$ such that each of the $\binom{n}{k}$ possible $k$-subsets is chosen with the same probability $1/\binom{n}{k}$. Statisticians call it *simple random sampling without replacement*. It is one of the most common uses of randomness in programs, and the right method depends on the sizes and on what is known: whether $n$ is known in advance, whether the items are in an array that may be changed, whether $k$ is tiny or close to $n$, and whether the output must be sorted. This page states the problem and gives a map of the methods; each method has its own page.

## In plain words

You have $n$ names and must pick $k$ of them, with no name picked twice, and every group of $k$ names must have the same chance. A lottery draw is an example.

There are many correct ways, and some that look correct but are not. Drawing and drawing again on repeats works, but gets slow when you want most of the names. Shuffling and taking the first $k$ works, but changes the list. Going down the list and keeping each name with the right chance gives the names in order. When you do not know how many names will come, keep a small pool and let each new name in with a falling chance.

## Definition

**Input.** Integers $0 \le k \le n$. The items are either the integers $0, \ldots, n - 1$ (they can stand for positions in any list) or an array of $n$ items. A source of independent uniform random integers, as from `randrange(m)`, or of uniform reals in $[0, 1)$, or of fair random bits.

**Output.** A set $S$ of $k$ distinct items with
$$\Pr[S = A] = \binom{n}{k}^{-1} \quad \text{for every } A \text{ with } |A| = k.$$

**Costs.** Time, extra space, and the amount of randomness used. The output can be required in a given form: as a set in any order, in sorted order, or as an *ordered sample*, a uniform sequence of $k$ distinct items in which each of the $n(n-1)\cdots(n-k+1)$ sequences is equally likely.

## Variants

- **Ordered sample.** A uniform sequence of $k$ distinct items. Forgetting the order gives a uniform subset, and putting a uniform subset in a uniform random order gives an ordered sample.
- **Sorted output.** The subset is wanted in increasing order, for example to read the chosen records of a file in one pass. [Selection sampling](/selection-sampling/) gives this directly.
- **Unknown n.** The items come as a stream and $n$ is only known at the end. This is the [stream sampling](/stream-sampling/) problem, solved by [reservoir sampling](/reservoir-sampling/).
- **With replacement.** Draw $k$ independent uniform items, so repeats are allowed. This is easy, but it is a different distribution.
- **Random size.** Keep each item independently with probability $p$, as in [Bernoulli sampling](/bernoulli-sampling/). The size is binomial, not fixed.
- **Unequal probabilities.** Items have weights. See [weighted sampling](/weighted-sampling/) and [probability proportional to size sampling](/probability-proportional-to-size-sampling/).
- **Designs that are not uniform on purpose.** [Systematic sampling](/systematic-sampling/) and [stratified sampling](/stratified-sampling/) give each item the same inclusion probability $k/n$ but not each subset the same probability. They trade uniformity of subsets for lower variance or simpler fieldwork.

## Examples

**Small case.** For $n = 5$ and $k = 2$, each of the 10 pairs must have probability $1/10$. Each item is then in the sample with probability $2/5$, and each pair of items is in it with probability $1/10$.

**Draw again on repeats.** Draw uniform items and throw away repeats until $k$ distinct ones are found. When $i$ items are already chosen, a draw is new with probability $(n - i)/n$, so the expected number of draws is
$$\sum_{i=0}^{k-1} \frac{n}{n - i} = n\,(H_n - H_{n-k}).$$
For $n = 5$, $k = 2$ this is $9/4$. For $n = 100$ it is about $10.5$ draws for $k = 10$, $68.8$ for $k = 50$, $225.8$ for $k = 90$, and $518.7$ for $k = 100$, which is the [coupon collector](/coupon-collector-problem/) case. So for $k > n/2$, choose the $n - k$ items to leave out instead.

**Wrong methods.**

- *Keep each item with probability $k/n$.* The size is random. For $n = 5$ and $p = 2/5$, the sample has exactly 2 items with probability only $216/625 \approx 0.35$.
- *A random start and $k$ items in a row (around a circle).* For $n = 5$, $k = 2$ only 5 of the 10 pairs can occur, such as $\{0, 1\}$ but never $\{0, 2\}$.
- *Draw $k$ times with replacement and remove repeats.* The result can have fewer than $k$ items.
- *Draw with `rand() % n`.* When the range of the generator is not a multiple of $n$, small values are more likely. See [modulo bias](/modulo-bias/).

**The amount of randomness.** For $n = 100$ and $k = 10$, there are $\binom{100}{10} = 17\,310\,309\,456\,440$ subsets, so about $43.98$ random bits are needed on average. Ten independent draws from $\{0, \ldots, 99\}$ use about $66.4$ bits.

## Known algorithms

| Method | Time | Extra space | Random numbers | Output |
| --- | --- | --- | --- | --- |
| Draw again on repeats, with a [hash table](/hash-table/) | $O(k)$ expected for $k \le n/2$ | $O(k)$ | $n(H_n - H_{n-k})$ expected, at most $2k$ for $k \le n/2$ | ordered sample |
| Partial [Fisher-Yates shuffle](/fisher-yates-shuffle/) on the array | $O(k)$ | none, the array is changed | $k$ | ordered sample |
| Partial Fisher-Yates with a hash map of moved entries | $O(k)$ expected | $O(k)$ | $k$ | ordered sample |
| [Floyd's algorithm](/floyd-sampling/) | $O(k)$ expected | $O(k)$ | exactly $k$ | set |
| [Selection sampling](/selection-sampling/) | $O(n)$ | $O(1)$ | up to $n$ | sorted |
| Sequential sampling with skips (Vitter) | $O(k)$ expected | $O(1)$ | $O(k)$ | sorted |
| [Reservoir sampling](/reservoir-sampling/) | $O(n)$ | $O(k)$ | $n - k$ | set, $n$ unknown |
| Random keys, keep the $k$ least | $O(n \log k)$ | $O(k)$ | $n$ | set |
| Unrank one integer with the [combinatorial number system](/combinatorial-number-system/) | $O(n)$ big number steps | $O(k)$ | one integer below $\binom{n}{k}$ | sorted |

Rules of thumb. If $k$ is much smaller than $n$, use Floyd's algorithm or draw again on repeats. If the items are in an array that may be changed, use a partial shuffle. If the output must be sorted, use selection sampling or a method with skips. If $n$ is unknown, use reservoir sampling.

## Bounds

**Time.** Writing the output takes $\Omega(k)$ time, and the hashing methods and the sequential method with skips reach $O(k)$ expected time. Without a hash table or an array of size $n$, Floyd's algorithm with a balanced search tree takes $O(k \log k)$ time.

**Random bits.** An algorithm that uses fair coin flips and outputs a uniform $k$-subset needs at least $\log_2 \binom{n}{k}$ flips on average, because the output has this entropy (Knuth and Yao 1976). Methods that draw $k$ uniform integers in $\{0, \ldots, n-1\}$ use about $k \log_2 n$ bits, which is more by about $\log_2 k!$ bits.

**No bounded number of coin flips.** If $\binom{n}{k}$ is not a power of 2, no algorithm that always stops after at most $b$ fair coin flips is exactly uniform. Each run of $b$ flips has probability $2^{-b}$, so the probability of each output is a multiple of $2^{-b}$, and $1/\binom{n}{k}$ is not. For example, $\binom{5}{2} = 10$. So an exact algorithm must have runs of unbounded length with probability 0, as in the rejection step inside `randrange`.

**Correctness of the main methods.** Each method has its own proof on its page. Most reduce to one of two facts. First, by symmetry, the $k$ least of $n$ independent continuous keys fall on a uniform $k$-subset. Second, a uniform ordered sample, as from a partial shuffle, gives a uniform subset after the order is forgotten, since each $k$-subset comes from exactly $k!$ sequences.

## Reductions

- **From random permutations.** The first $k$ items of a uniform [random permutation](/random-permutation/) are a uniform ordered sample. A partial Fisher-Yates shuffle stops the shuffle after $k$ steps.
- **To uniform integers.** The combinatorial number system is a bijection between the integers $0, \ldots, \binom{n}{k} - 1$ and the $k$-subsets. So the problem is the same as drawing one uniform integer below $\binom{n}{k}$ and unranking it, which is practical only for small $\binom{n}{k}$.
- **To stream sampling.** A method for stream sampling solves this problem when the items are read in order, and with known $n$ selection sampling solves the stream version.
- **Complements.** Choosing the $n - k$ items to leave out is the same problem. Methods whose cost grows with $k$ should be run on $\min(k, n - k)$.

## Applications

- **Surveys and audits.** Simple random sampling is the base design of survey sampling. The other designs, such as stratified and systematic sampling, are compared with it.
- **Randomized algorithms.** Random samples choose pivots and splitters, as in [sample sort](/sample-sort/), and random subsets of edges or constraints in sparsification and in random sampling algorithms for linear programming.
- **Experiments.** Split subjects into a treatment group of size $k$ and a control group, or choose the test set and the folds in [cross-validation](/cross-validation/).
- **Games and lotteries.** Deal a hand of $k$ cards or draw $k$ lottery numbers; for 5 cards from 52 there are $2\,598\,960$ hands.
- **Testing.** Choose random inputs, random records or random users for a check, without repeats.

## References
