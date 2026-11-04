---
tag: MMBG5S
kind: data-structure
slug: spectral-bloom-filter
name: Spectral Bloom filter
area: data-structures/probabilistic-structures
level: advanced
summary: Counting Bloom filter that estimates multiplicities of items in a multiset.
model: word-ram
complexity:
  vars: {n: the number of distinct keys with a positive count, m: the number of counters, k: the number of hash functions}
  time: {worst: Θ(k)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [counting-bloom-filter, false-positive-rate, frequency-estimation]
see_also: [count-min-sketch, count-min-error-bound, bloom-filter, approximate-membership, frequency-vector, stable-bloom-filter]
sources:
  - paper: doi:10.1145/872757.872787
    title: Saar Cohen and Yossi Matias, Spectral Bloom filters, Proceedings of the 2003 ACM SIGMOD International Conference on Management of Data
    locator: pages 241 to 252 (minimum selection, minimal increase, recurring minimum, and the error equal to the Bloom filter false positive rate)
  - paper: doi:10.1145/633025.633056
    title: Cristian Estan and George Varghese, New directions in traffic measurement and accounting, Proceedings of ACM SIGCOMM 2002
    locator: pages 323 to 336 (conservative update of multistage filters, the same rule as minimal increase)
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75 (the partitioned form with one row for each hash function and its additive error bound)
---

A spectral Bloom filter stores a multiset and answers "how many copies of $x$ are there?" approximately. It is a [counting Bloom filter](/counting-bloom-filter/) whose counters are read as numbers, not only as zero or nonzero. INSERT$(x)$ adds 1 to the counters at the $k$ positions of $x$, and ESTIMATE$(x)$ returns the smallest of them, the *minimum selection* rule. The estimate is never too small, and it is too large only when every position of $x$ is shared with another stored key, which has the same probability as a false positive of a [Bloom filter](/bloom-filter/) with the same parameters. The *minimal increase* rule raises only the smallest counters on an insert and gives smaller errors, but it cannot delete. Cohen and Matias introduced the structure in 2003.

## In plain words

A Bloom filter only says whether a word is there. Often we also want to know how often it is there, such as how many times a search term was asked.

A spectral Bloom filter keeps a row of counters. Each word adds one to a few counters, chosen by hash functions. Other words may add to the same counters, so each counter can only be too high, never too low. The best guess for a word is the lowest of its counters, since that one has the fewest additions from other words.

The guess is exact unless every counter of the word is also used by some other word. That is rare, and exactly as rare as a wrong "maybe" in a Bloom filter of the same size. A smarter way to add makes the guesses even closer, but then words can no longer be removed.

## The abstract type

The filter keeps a multiset $f$ over a universe $U$, with $f_x \ge 0$ copies of each key $x$, as in the [frequency estimation problem](/frequency-estimation/). INSERT$(x, w)$ adds $w \ge 0$ copies of $x$. DELETE$(x, w)$ removes $w$ copies and is allowed only when $f_x \ge w$, and only with minimum selection. ESTIMATE$(x)$ returns a number $\hat f_x$ with $\hat f_x \ge f_x$ always and $\hat f_x = f_x$ with high probability. A threshold query "is $f_x \ge T$?" answers true when $\hat f_x \ge T$, so it has [one-sided error](/one-sided-error/) like the membership query of a Bloom filter, which is the case $T = 1$.

## Representation

The filter is an array $C[0 \ldots m-1]$ of integer counters and $k$ [hash functions](/hash-function/) $h_1, \ldots, h_k$ from $U$ to $\{0, \ldots, m - 1\}$. Let $H(x) = \{h_1(x), \ldots, h_k(x)\}$ be the *set* of positions of $x$; it has fewer than $k$ elements when two hash values agree, and each position is updated once.

**Invariant (M), minimum selection.** For each position $p$, $C[p] = \sum_{y : p \in H(y)} f_y$.

**Invariant (I), minimal increase.** For each key $y$ and each $p \in H(y)$, $C[p] \ge f_y$, and $C[p]$ is at most the value that minimum selection would hold for the same stream.

## Operations

```pseudo id=main
CREATE(m, k)
L1  C ← an array of m counters, all 0
L2  choose hash functions h_1, ..., h_k : U → {0, ..., m − 1};  H(x) = {h_1(x), ..., h_k(x)}

INSERT(C, x, w)                       ▷ minimum selection
L3  for each p in H(x) do C[p] ← C[p] + w

INSERT-MI(C, x, w)                    ▷ minimal increase
L4  v ← min { C[p] : p ∈ H(x) }
L5  for each p in H(x) do C[p] ← max(C[p], v + w)

DELETE(C, x, w)                       ▷ minimum selection only; needs f_x ≥ w
L6  for each p in H(x) do C[p] ← C[p] − w

ESTIMATE(C, x)
L7  return min { C[p] : p ∈ H(x) }
```

**Minimum selection.** Line L3 adds $w$ to each counter of $x$. Each counter is the total multiplicity of the keys that use it, so the counters of $x$ are $f_x$ plus *collision mass*, and line L7 returns the one with the least such mass.

**Minimal increase.** Line L4 reads the current estimate $v$ of $x$, and line L5 raises each counter of $x$ to at least $v + w$, the smallest value that keeps it at or above the new count of $x$. Counters that are already larger carry mass of other keys and are left alone. With $w = 1$ this increments only the counters that hold the minimum. Estan and Varghese (2002) gave the same rule for their multistage filters under the name *conservative update*.

**Delete.** Line L6 undoes line L3. It is not valid after minimal increase: a counter that was not raised for $x$ may still be needed by $x$'s count, and subtracting from it can make the estimate of another key too small.

## Example

Let $m = 10$ and $k = 3$ with the positions below, and insert the stream a, a, b, c, a, c, e, so $f_a = 3$, $f_b = 1$, $f_c = 2$, $f_e = 1$ and $f_d = 0$.

| key | a | b | c | d | e |
|---|---|---|---|---|---|
| $H$ | 0, 3, 7 | 3, 5, 9 | 1, 5, 7 | 0, 1, 9 | 3, 5, 7 |

| rule | $C[0 \ldots 9]$ | $\hat f_a$ | $\hat f_b$ | $\hat f_c$ | $\hat f_d$ | $\hat f_e$ |
|---|---|---|---|---|---|---|
| minimum selection | 3 2 0 5 0 4 0 6 0 1 | 3 | 1 | 2 | 1 | 4 |
| minimal increase | 3 2 0 3 0 3 0 3 0 1 | 3 | 1 | 2 | 1 | 3 |

The keys a, b and c each have one counter that no other stored key uses (0, 9 and 1), so their estimates are exact under both rules. The key d is absent, but each of its counters is used by another key, so $\hat f_d = 1$: this is a false positive of the Bloom filter that the zero pattern forms. The key e has all three counters shared. Under minimum selection its estimate is $1 + \min(4, 3, 5) = 4$, where 4, 3 and 5 are the masses of a and b, of b and c, and of a and c. Under minimal increase the last insert of e finds counters 3, 2 and 3 at positions 3, 5 and 7 and raises them all to 3, so $\hat f_e = 3$, closer to the true value 1.

Deleting e under minimum selection gives the counters 3 2 0 4 0 3 0 5 0 1 and $\hat f_e = 3$, still at least $f_e = 0$. Doing the same under minimal increase would give 3 2 0 2 0 2 0 2 0 1 and $\hat f_a = 2 < 3$, which is why that rule forbids deletes.

## Correctness

Under minimum selection, invariant (M) holds after each insert and each allowed delete, by induction. Each counter of $x$ then equals $f_x$ plus the multiplicities of the other keys that use it, which are at least 0, so $\hat f_x \ge f_x$, with equality exactly when some position of $x$ is used by no other key with a positive count. Under minimal increase, line L5 keeps each counter of $x$ at least the new $f_x$ and only raises counters, so the counters of other keys stay above their counts; and a counter that is raised to $v + w$ was at most the minimum selection value, so the counters never exceed those of minimum selection. Hence $f_x \le \hat f_x^{\mathrm{MI}} \le \hat f_x^{\mathrm{MS}}$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory probes |
|---|---|---|
| create | $\Theta(m)$ | none |
| insert, delete, estimate | $k$ hash evaluations | at most $k$ reads and writes |
| space | $m$ counters | |

**The error probability.** Assume ideal hashing, and let $n$ be the number of distinct keys with a positive count other than $x$. Then
$$ \Pr[\hat f_x \ne f_x] \le \Pr[H(x) \subseteq B] = \mathbb{E}\big[(|B|/m)^k\big] \approx \big(1 - e^{-kn/m}\big)^k, $$
where $B$ is the set of positions used by the other keys. This is the [false positive rate](/false-positive-rate/) of a Bloom filter of $m$ bits holding those $n$ keys, so $m = 10n$ and $k = 7$ make about 0.8 percent of the estimates wrong. The bound does not depend on the counts, only on the number of distinct keys, and it holds for both rules. The proof is in [the complexity proof](proofs/complexity.md).

**The size of an error.** The probability bound says nothing about how large a wrong estimate is. A key that shares all its counters with a very frequent key gets a very large estimate. For a bound on the size, the [count-min sketch](/count-min-sketch/) splits the counters into $k$ rows, one for each hash function, and then the error is at most $\varepsilon \sum_y f_y$ with probability $1 - \delta$ for $m = (e/\varepsilon)\ln(1/\delta)$, by the [count-min error bound](/count-min-error-bound/).

**Counter size.** A counter can hold up to the total count $N = \sum_y f_y$, so it needs $\lceil \log_2(N + 1) \rceil$ bits if all counters have the same width. Cohen and Matias store counters of variable length, so that the total space is close to $\sum_p \log_2(C[p] + 1)$ bits plus an index.

## Variants

- **Recurring minimum.** Cohen and Matias also propose this third rule. If the smallest counter of $x$ occurs at two or more positions, the estimate is very likely exact. Keys with a single minimum are also stored in a second, smaller spectral filter, which is asked for them. This supports deletes and gives errors close to minimal increase.
- **Count-min sketch.** One row of counters for each hash function, with the same minimum rule. It has a provable bound on the size of the error, see the [count-min sketch](/count-min-sketch/).
- **Threshold queries.** Return the keys with $\hat f_x \ge T$, for iceberg queries in a database. Since $\hat f_x \ge f_x$, no key with $f_x \ge T$ is missed.
- **Counting quotient filter.** A fingerprint filter that stores counts with each fingerprint, with errors only from fingerprint collisions; see the [quotient filter](/quotient-filter/).

## When to use it

Use a spectral Bloom filter when a multiset with many distinct keys must be summarized in a small space, most estimates must be exact, and an occasional overestimate is acceptable: counts of query terms, of network flows, or of join keys in a database. Use minimal increase when there are no deletes, and minimum selection or recurring minimum when there are. When the size of the worst error matters more than the probability of an exact answer, use a [count-min sketch](/count-min-sketch/).

## Pitfalls

- **Counting a repeated position twice.** If $h_i(x) = h_j(x)$ and the counter is incremented for each $i$, then the estimate of $x$ can be a multiple of $f_x$ even with no collision. Lines L3 to L7 use the set $H(x)$.
- **Deleting after minimal increase.** This can make estimates too small, as the example shows. The Python code refuses the delete.
- **Deleting an absent key.** Under minimum selection, deleting copies that are not there breaks invariant (M), and other estimates can fall below their true counts.
- **Fixed-width counters.** Counters of a few bits that stick at their top value, as in a counting Bloom filter, make large counts unreadable. Use counters wide enough for the largest count.
- **Reading the error rate as an error size.** One percent of wrong estimates can include estimates that are wrong by a factor of 1000.

## Implementations

The Python class has both insert rules, selected by a flag, and supports weighted inserts. It uses independent 64-bit words of BLAKE2b for the $k$ positions and the set of distinct positions in every operation.

## History

Cohen and Matias (2003) introduced spectral Bloom filters with the minimum selection, minimal increase and recurring minimum rules, and showed that the probability of a wrong estimate equals the Bloom filter error rate. They also described a compact storage of variable-length counters and uses in iceberg queries and joins. Estan and Varghese (2002) had used the minimal increase rule as conservative update in multistage filters for network measurement. The count-min sketch of Cormode and Muthukrishnan (published in 2005) is the partitioned form with a bound on the size of the error.

## References
