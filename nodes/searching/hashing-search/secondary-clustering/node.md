---
tag: 32BEVM
kind: concept
slug: secondary-clustering
name: Secondary clustering
area: searching/hashing-search
level: core
summary: Keys sharing a first probe follow the same probe sequence.
prereqs: [open-addressing, probe-sequence, quadratic-probing, primary-clustering]
see_also: [primary-clustering, double-hashing, open-addressing-expected-probes, linear-probing, uniform-hashing-assumption, cuckoo-hashing, hash-collision]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing), quadratic probing and its milder form of clustering, and double hashing
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the discussion of secondary clustering and the approximate costs of a probing scheme in which the probe sequence depends only on the first probe
---

Secondary clustering is the effect in [open addressing](/open-addressing/) where two keys with the same first probe follow the same whole [probe sequence](/probe-sequence/), so each key that collides on its home slot repeats all the probes of the keys before it. It arises in every scheme whose probe sequence is a function of the home slot alone, as in [quadratic probing](/quadratic-probing/), and it is milder than the [primary clustering](/primary-clustering/) of [linear probing](/linear-probing/), where keys with different home slots also merge into one run. [Double hashing](/double-hashing/) removes it by letting the step of the sequence depend on the key through a second hash function.

## In plain words

Suppose every driver who is told to park at spot 3 also follows the same fixed backup plan: try spot 4, then spot 7, then spot 1, and so on. The first driver gets spot 3. The second tries 3, then 4. The third tries 3, 4 and 7. Each new driver with the same start repeats every failed try of the ones before.

Drivers with other starting spots use other backup plans, so they do not join this queue the way they would on a one-way street. That is why secondary clustering hurts less than primary clustering. But all the drivers who share a start still form a small queue, and they pay for it in extra tries.

## The idea

**Definition.** An open-addressing scheme probes the slots $h(k, 0), h(k, 1), \ldots, h(k, m - 1)$ for key $k$. The scheme has *secondary clustering* if $h(k, 0) = h(k', 0)$ implies $h(k, i) = h(k', i)$ for all $i$: the whole sequence is a function of the first probe. Such a scheme has at most $m$ distinct probe sequences.

- Linear probing, $h(k, i) = (h'(k) + i) \bmod m$, has it, and it also has primary clustering.
- Quadratic probing, $h(k, i) = (h'(k) + c_1 i + c_2 i^2) \bmod m$, has it, but not primary clustering: two keys with different home slots follow different jumps after a collision.
- Double hashing, $h(k, i) = (h_1(k) + i\,h_2(k)) \bmod m$, does not have it: two keys with the same first probe $h_1$ usually have different steps $h_2$. With $m$ prime and $h_2(k) \in \{1, \ldots, m - 1\}$, it has $m(m-1)$ probe sequences.

**The cost.** The keys with one home slot form a group. If $j$ keys of the group are stored, the next key of the group repeats at least the $j$ probes that end at those keys, plus probes at slots taken by other groups. Under the model in which the first probe is uniform and the rest of the sequence is a random function of the first probe, Knuth gives the approximate costs
$$\text{unsuccessful} \approx \frac{1}{1 - \alpha} - \alpha + \ln \frac{1}{1 - \alpha}, \qquad \text{successful} \approx 1 + \ln \frac{1}{1 - \alpha} - \frac{\alpha}{2},$$
against $1/(1-\alpha)$ and $(1/\alpha)\ln(1/(1-\alpha))$ for uniform probing, whose sequences are $m!$ independent random permutations; see [expected probes in open addressing](/open-addressing-expected-probes/).

| $\alpha$ | unsuccessful, secondary clustering | unsuccessful, uniform | successful, secondary clustering | successful, uniform |
|---|---|---|---|---|
| 0.5 | 2.19 | 2 | 1.44 | 1.39 |
| 0.75 | 4.64 | 4 | 2.01 | 1.85 |
| 0.9 | 11.40 | 10 | 2.85 | 2.56 |

The extra cost is a few probes at most at practical loads, much less than the $1/(1-\alpha)^2$ of primary clustering, which gives 8.5 and 50.5 failed-search probes at the last two loads.

**Where it comes from.** Each group of keys with one home slot behaves like a small chained list stored inside the array: the $j$-th key of the group pays about $j$ probes just to pass the keys of its own group. The groups have the sizes of [balls into bins](/balls-into-bins/), and at a bounded load most groups hold only a few keys, so the extra cost per key stays small.

## Examples

**Three keys with one home.** Let $m = 11$ and let quadratic probing use $h(k, i) = (k + i^2) \bmod 11$. The keys 3, 14 and 25 all have home slot 3, so all three use the sequence 3, 4, 7, 1, 8, 6, and so on.

| key | probes | stored at | probes made |
|---|---|---|---|
| 3 | 3 | 3 | 1 |
| 14 | 3, 4 | 4 | 2 |
| 25 | 3, 4, 7 | 7 | 3 |
| 4 | 4, 5 | 5 | 2 |

The three keys of one group need $1 + 2 + 3 = 6$ probes in total. The key 4 has home slot 4, which 14 took, but its next probe is $4 + 1 = 5$, not slot 7 where the group went. A later key of the group 3, 14, 25 has to pass slots 3, 4 and 7 again before it reaches slot 1.

**The same keys under double hashing.** Use $h_1(k) = k \bmod 11$ and $h_2(k) = 1 + (k \bmod 10)$. The keys 3, 14 and 25 have steps 4, 5 and 6, so their sequences are 3, 7, 0, ... and 3, 8, 2, ... and 3, 9, 4, .... Key 14 is stored at slot 8 after 2 probes, and 25 at slot 9 after 2 probes, not 3: after the shared first probe, the group splits.

**Non-example: chaining.** In [separate chaining](/separate-chaining/), keys with the same slot share a list by design, and there is no probe sequence. The cost of a list is the length of the list, analyzed on the [chaining](/chaining-expected-search-time/) page. Secondary clustering is the open-addressing image of that shared list.

## Where it is used

- **Choosing quadratic probing.** Quadratic probing is chosen to avoid primary clustering while keeping a cheap probe sequence; secondary clustering is the cost that remains.
- **Choosing double hashing.** Double hashing is the standard way to get rid of secondary clustering, and its costs approach those of uniform probing; see the [uniform hashing assumption](/uniform-hashing-assumption/) page for the results of Guibas and Szemeredi and of Lueker and Molodowitch.
- **Bad first hash functions.** Secondary clustering makes the first hash function decisive: if many keys share a home slot, every one of them pays for the others, whatever the probe sequence. A good [hash function](/hash-function/) for the first probe matters more than the shape of the sequence.
- **Analysis of probing schemes.** Knuth uses the model with secondary clustering as the middle case between linear probing and uniform probing.

## References
