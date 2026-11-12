---
tag: F8JS2K
kind: algorithm
slug: jump-consistent-hash
name: Jump consistent hash
aliases:
- jump hash
- JumpConsistentHash
area: systems/load-balancing-and-hashing
level: advanced
summary: Map a 64-bit key to one of n numbered buckets with no memory, in expected O(log n) steps. Growing to n + 1 buckets moves only the keys that go to the new last bucket.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of buckets}
  time: {worst: O(n), average: Θ(log n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2014
  people: [John Lamping, Eric Veach]
  note: Lamping and Veach of Google published the algorithm on arXiv in 2014 as a consistent hash with no memory for numbered shards.
prereqs: [hash-function, linear-congruential-generator, monotonicity-property]
see_also: [consistent-hashing, rendezvous-hashing, maglev-hashing, hash-partitioning, sharding, harmonic-series]
sources:
  - url: https://arxiv.org/abs/1406.2294
    title: John Lamping and Eric Veach, A fast, minimal memory, consistent hash algorithm, arXiv:1406.2294, 2014
    locator: the C++ function JumpConsistentHash, its derivation from a random jump process, the expected O(ln n) running time, and the restriction to buckets numbered 0 to n - 1
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the definition of consistent hashing and its monotonicity and balance properties
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.2.1.2, Theorem A (the full period of a linear congruential generator)
---

Jump consistent hash maps a 64-bit key to one of $n$ buckets numbered $0$ to $n - 1$ with no memory and no table. It is a small loop that uses the key as the seed of a random number generator and "jumps" forward through bucket numbers. When the number of buckets grows from $n$ to $n + 1$, a key either stays or moves to bucket $n$, so it has the [monotonicity property](/monotonicity-property/) exactly. The expected time is $\Theta(\log n)$, but the buckets cannot have arbitrary names: only the last bucket can be added or removed.

## In plain words

Think of a key that watches the number of buckets grow one at a time. When there is one bucket, the key is in bucket 0. When a new bucket appears, the key moves to it with a chance of one in the new number of buckets, and otherwise stays. This keeps all buckets equally full at every step, and a key never moves between two old buckets.

Doing this one bucket at a time is slow. The trick is to compute, from a random number seeded by the key, the next bucket count at which the key will move. The key jumps there directly, and the gaps between jumps grow fast, so only a few jumps are needed to pass the real number of buckets. The last jump that stays below that number is the answer.

## The problem

The input is a 64-bit key, usually the hash of a longer key, and a bucket count $n \ge 1$. The output is a bucket in $\{0, \ldots, n-1\}$. The goals are those of the [dynamic partitioning problem](/dynamic-partitioning-problem/) in the special case where the servers are numbered shards: equal shares, and few moved keys when $n$ changes by one. The guarantees on balance and running time are in the ideal model, where the generator gives independent uniform numbers.

## The algorithm

```pseudo id=main
JUMP-HASH(key, n)                          ▷ key is an unsigned 64-bit integer, n ≥ 1
L1  b ← −1, j ← 0
L2  while j < n do
L3      b ← j
L4      key ← (key · 2862933555777941757 + 1) mod 2^64
L5      j ← ⌊(b + 1) · 2^31 / ((key >> 33) + 1)⌋     ▷ in double precision
L6  return b
```

Line L4 is a 64-bit [linear congruential generator](/linear-congruential-generator/) step, with the key as its state. Line L5 takes the top 31 bits $y$ of the state and sets $r = (y + 1)/2^{31}$, a number in $(0, 1]$. The next jump is $j = \lfloor (b + 1)/r \rfloor$.

**Where the jump comes from.** Suppose the key is in bucket $b$ when there are $b + 1$ buckets. It must move to bucket $i$ when the count grows to $i + 1$ with probability $1/(i+1)$, and stay otherwise. So the chance that it stays in $b$ through all counts up to $i$ is

$$\prod_{t = b + 2}^{i} \left(1 - \frac{1}{t}\right) = \frac{b + 1}{i}.$$

The next bucket $j$ where it moves therefore has $\Pr[j \ge i] = (b + 1)/i$. With $r$ uniform on $(0, 1]$, $j = \lfloor (b + 1)/r \rfloor$ has exactly this law, because $j \ge i$ if and only if $r \le (b + 1)/i$.

## Example

Take the key 256 and $n = 1000$. The loop computes the jumps

$$0 \to 1 \to 2 \to 3 \to 16 \to 137 \to 520 \to 3906.$$

The jump to 3906 passes $n$, so the loop stops and returns 520. The same sequence gives the bucket of key 256 for each $n$:

| bucket count $n$ | 1 | 2 | 3 | 4 to 16 | 17 to 137 | 138 to 520 | 521 to 3906 |
|---|---|---|---|---|---|---|---|
| bucket of key 256 | 0 | 1 | 2 | 3 | 16 | 137 | 520 |

The key moves only when the new last bucket is a member of its jump sequence, and it always moves to that new bucket.

**Regression values** of the implementation below, which follows the paper's code with 64-bit wraparound:

| key | $n$ | bucket |
|---|---|---|
| 0 | 10 | 0 |
| 1 | 10 | 6 |
| 42 | 10 | 2 |
| 256 | 1000 | 520 |
| 123456789 | 100 | 34 |
| $2^{64} - 1$ | 1000 | 313 |
| 0xDEADBEEF | 1,000,000 | 479,362 |

**Balance and movement.** For 100,000 random 64-bit keys (Python `random.Random(4)`), ten buckets get between 9,846 and 10,165 keys, and the chi-square statistic against equal shares is 8.50 with 9 degrees of freedom. Going from 10 to 11 buckets moves 9,213 keys, all to bucket 10; the expected number is $100{,}000/11 \approx 9{,}091$. Over 20,000 keys, the mean number of loop runs is 2.93 for $n = 10$, 7.50 for $n = 1000$ and 14.38 for $n = 10^6$, against the harmonic numbers $H_n$ = 2.93, 7.49 and 14.39.

## Correctness

The update of line L4 does not depend on $n$, so each key has one fixed jump sequence $0 = j_0 < j_1 < j_2 < \cdots$, and the loop returns the largest element below $n$. Each jump is at least one more than the last, because $2^{31}/(y + 1) \ge 1$. From this, two facts follow for every key, with no probabilistic assumption: the result is in $[0, n)$, and the result for $n + 1$ is either the result for $n$ or $n$ itself. In the ideal model, where the values $r$ are independent and uniform, induction on $n$ shows that each bucket gets the key with probability exactly $1/n$, and that bucket $c$ is in the jump sequence with probability $1/(c+1)$. The full proof is below.

## Complexity

- **Expected time.** The loop runs once for each element of the jump sequence below $n$. Bucket $c$ is in the sequence with probability $1/(c+1)$, so the expected number of runs is $H_n = \ln n + O(1)$ in the ideal model. Each run is a 64-bit multiply, a shift and a floating-point division.
- **Worst case.** Each jump is at least 1, so the loop runs at most $n$ times. This bound is far from what happens; it is the only bound that holds for every key.
- **Space.** $\Theta(1)$: no table, no ring and no list of buckets.
- **Movement.** Going from $n$ to $n + 1$ buckets moves a key with probability $1/(n+1)$, which is the minimum for equal shares.

A ring with [virtual nodes](/virtual-nodes/) needs memory in proportion to the number of points, and its shares are equal only up to the spread of the arc lengths. In the ideal model, jump hash has the spread of a perfect uniform assignment: the load of a bucket is binomial with $m$ trials and success probability $1/n$. The paper compares the two methods on memory, speed and the evenness of the shares.

## Properties

- **Exactly monotone** when the last bucket is added or removed (Theorem 2 of the proof).
- **Balanced** in the ideal model: each bucket gets $1/n$ of the keys.
- **No memory.** The function needs only the key and $n$. Two processes agree as soon as they agree on $n$.
- **Numbered buckets only.** The buckets are $0$ to $n - 1$. Removing bucket 3 of 10 is not supported: there is no way to make bucket 3 disappear while the others keep their keys.
- **Deterministic.** The randomness is in the key hash and the generator, not in the run.

## Variants and improvements

- **Arbitrary removals through a level of indirection.** Map the bucket number to a server with a table, and when a server fails, give its bucket number to a spare or to a replica. This is the setting of the paper: shards of a storage system, each shard a replicated group, so a shard number never disappears.
- **Strings as keys.** Hash the string to 64 bits first, with a good [hash function](/hash-function/), then call jump hash.
- **Other generators.** Any source of uniform numbers seeded by the key works, as long as all clients use the same one. The constants of the paper are what makes results agree between implementations.
- **Named servers.** When servers have names and can fail in any order, use [rendezvous hashing](/rendezvous-hashing/), a [consistent hashing](/consistent-hashing/) ring, or [Maglev hashing](/maglev-hashing/) instead.

## When to use it

Use jump hash to place keys on numbered shards when the shard count grows by adding shards at the end, for example in a storage system that splits data into $n$ replicated shards and grows $n$ over time. It is a good default for the shard function of [hash partitioning](/hash-partitioning/) that needs to grow without moving most of the data. Do not use it to pick among cache servers or backends that can fail one at a time in any order.

## Pitfalls

- **Removing a bucket in the middle.** Shrinking from $n$ to $n - 1$ always removes bucket $n - 1$. If bucket 3 fails and you renumber, the keys of many buckets move. Keep the numbering, and remap the failed number.
- **No 64-bit wraparound.** In a language with big integers, the multiply in line L4 must be reduced modulo $2^{64}$. Without it the state grows without bound and the results differ from every other implementation.
- **A different generator in one client.** Clients agree only if they use the same multiplier, the same shift of 33 and the same formula of line L5. A port that changes any of them is a different hash function.
- **Raw small integers as keys.** The keys 0, 1, 2, ... give very regular results, because the generator is linear. Hash the user key to 64 bits first.
- **Using the result as the shard count.** The function maps a key to a bucket; the count $n$ must be the same in all clients during a change, or two clients send the same key to different buckets.

## Implementations

## History

John Lamping and Eric Veach of Google published the algorithm in 2014 on arXiv, with a five-line C++ function. They derived it from the process in which each key moves to a new bucket with probability $1/(n+1)$, and made it fast by computing the next point where the key moves instead of testing each bucket count. The paper presents it as a fit for sharded data storage, where the shards are numbered, and contrasts it with the ring of Karger et al. (1997), which allows arbitrary server names.

## References
