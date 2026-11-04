---
tag: MC3EJT
kind: data-structure
slug: learned-bloom-filter
name: Learned Bloom filter
aliases:
- learned index filter
area: data-structures/probabilistic-structures
level: research
summary: Bloom filter augmented by a learned classifier that screens likely keys.
model: word-ram
complexity:
  vars: {m: the bits of the Bloom filters, k: the hash functions per query, T: the time of one classifier evaluation, z: the bits of the classifier}
  time: {worst: Θ(k + T)}
  space: {extra: Θ(m + z)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bloom-filter, false-positive-rate, classification]
see_also: [approximate-membership, bloom-filter-lower-bound, logistic-regression, xor-filter, one-sided-error]
sources:
  - paper: doi:10.1145/3183713.3196909
    title: Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean and Neoklis Polyzotis, The case for learned index structures, Proceedings of the 2018 International Conference on Management of Data (SIGMOD 2018)
    locator: pages 489 to 504, Section 5 (existence indexes, a classifier with a threshold and a backup Bloom filter of its false negatives)
  - paper: "Michael Mitzenmacher, A model for learned Bloom filters, and optimizing by sandwiching, Advances in Neural Information Processing Systems 31 (NeurIPS 2018), arXiv:1901.00902"
    locator: the false positive rate with respect to a query distribution, the space condition, and the sandwiched learned Bloom filter
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the Bloom filters used as backup and initial filters)
---

A learned Bloom filter uses a trained [classifier](/classification/) as the first stage of a membership test. The classifier gives each key a score $\sigma(x) \in [0, 1]$, and the filter answers "maybe present" when the score is at least a threshold $\tau$. The stored keys that the classifier misses, its false negatives, are put in a small backup [Bloom filter](/bloom-filter/), which is asked whenever the score is below $\tau$. So no stored key is ever rejected. If the classifier separates keys from non-keys well, the backup filter holds only a few keys, and the classifier and the backup together can be smaller than a Bloom filter of the whole set. Kraska, Beutel, Chi, Dean and Polyzotis proposed it in 2018, and Mitzenmacher gave its model and the *sandwiched* form with a second Bloom filter in front.

## In plain words

A Bloom filter treats all words the same. But real sets often have a pattern: the addresses of known bad web sites may look different from good ones. A learned model can spot the pattern and say "this looks like one of the stored words" without storing the words at all.

The model makes mistakes in both directions. When it wrongly says "looks like one", the filter gives a wrong "maybe", which a filter may do. When it wrongly says "does not look like one" for a stored word, that would be a real error, which a filter may not make. So all stored words that the model misses go into a small ordinary Bloom filter, and the filter checks that one too.

The wrong "maybe" answers then depend on which words are asked, not only on the hash functions.

## The abstract type

The filter solves the static [approximate membership problem](/approximate-membership/) for a set $S$ of $n$ keys, with a weaker error guarantee. QUERY$(x)$ returns true for each $x \in S$. For non-keys, the rate is defined with respect to a *query distribution* $\mathcal{D}$ on $U \setminus S$:
$$ \varepsilon_{\mathcal{D}} = \Pr_{x \sim \mathcal{D},\ \text{hashing}}[\text{QUERY}(x) = \text{true}]. $$
This is not the per-key [false positive rate](/false-positive-rate/) of an ordinary filter: for a single non-key that the classifier accepts, the filter is wrong with probability 1.

## Representation

The filter has three parts, built in this order.

- A *classifier* $\sigma : U \to [0, 1]$ of $z$ bits, trained on $S$ and on a sample of non-keys, and a threshold $\tau$. Its false positive fraction on $\mathcal{D}$ is $F_p = \Pr_{x \sim \mathcal{D}}[\sigma(x) \ge \tau]$, and its false negative fraction is $F_n = |N|/n$, where $N = \{x \in S : \sigma(x) < \tau\}$.
- A *backup* Bloom filter $F_b$ of $m_b$ bits and $k_b$ hash functions that holds the set $N$. For a fixed non-key it has per-key rate $\varepsilon_b$, about $(1 - e^{-k_b |N|/m_b})^{k_b}$.
- In the sandwiched form, an *initial* Bloom filter $F_0$ of $m_0$ bits and $k_0$ hash functions that holds all of $S$, with per-key rate $\varepsilon_0$. Without it, $\varepsilon_0 = 1$.

The hash functions of $F_0$ and $F_b$ are independent of each other and of the classifier.

## Operations

```pseudo id=main
BUILD(S, σ, τ, m_0, m_b)
L1  if m_0 > 0 then F_0 ← a Bloom filter of m_0 bits holding S
L2  N ← { x ∈ S : σ(x) < τ }                   ▷ the false negatives of the classifier
L3  F_b ← a Bloom filter of m_b bits holding N

QUERY(x)
L4  if m_0 > 0 and F_0 rejects x then return false
L5  if σ(x) ≥ τ then return true
L6  return F_b.QUERY(x)
```

**Without the sandwich** ($m_0 = 0$), a query asks the classifier first and the backup filter only for low scores. **With the sandwich**, the initial filter removes most non-keys before the classifier sees them, which lowers the cost of the classifier's own false positives.

**Choosing the threshold.** A higher $\tau$ lowers $F_p$ but raises $F_n$, and so the size of the backup filter for a given $\varepsilon_b$. The threshold and $F_p$ must be measured on non-keys that were not used to train the classifier, because $F_p$ on the training data is too small.

## Example

Let $U = \{0, \ldots, 99\}$, $S = \{7, 10, 13, 20, 30, 40, 50\}$, and let the classifier give score 0.9 to multiples of 10 and 0.2 to all other numbers, with $\tau = 0.5$. It has learned the pattern "multiples of 10" but misses 7 and 13, so $N = \{7, 13\}$, $F_n = 2/7$. Let the backup filter have $m_b = 8$ bits and $k_b = 2$, with positions 7 → (1, 4), 13 → (4, 6), 25 → (1, 6), 33 → (2, 4), 60 → (0, 3). After the build its bits 1, 4 and 6 are set.

| query | in $S$ | score | step that decides | answer |
|---|---|---|---|---|
| 20 | yes | 0.9 | classifier | true |
| 13 | yes | 0.2 | backup, bits 4 and 6 set | true |
| 60 | no | 0.9 | classifier | true, a false positive |
| 25 | no | 0.2 | backup, bits 1 and 6 set | true, a false positive |
| 33 | no | 0.2 | backup, bit 2 is 0 | false |

If $\mathcal{D}$ is uniform on the 93 non-keys, the classifier accepts 0, 60, 70, 80 and 90, so $F_p = 5/93 \approx 0.054$. Each of these five keys is a false positive every time it is asked, whatever the hash functions are. A workload that asks for 60 again and again sees a rate of 1.

## Correctness

A key $x \in S$ is in the initial filter, so line L4 does not reject it. If $\sigma(x) \ge \tau$, line L5 accepts it. Otherwise $x \in N$, so the backup filter holds it and line L6 accepts it, since a Bloom filter has no false negatives. For a non-key drawn from $\mathcal{D}$ independently of the hash functions,
$$ \varepsilon_{\mathcal{D}} = \varepsilon_0 \big(F_p + (1 - F_p)\, \varepsilon_b\big), $$
with $\varepsilon_0 = 1$ without the sandwich. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| build | $n$ classifier evaluations and $\Theta(n k_0 + |N| k_b)$ bit writes, plus training |
| query | at most $k_0 + k_b$ hash evaluations and one classifier evaluation, $\Theta(k + T)$ |
| space | $m_0 + m_b$ bits and the $z$ bits of the classifier |

**When it saves space.** A Bloom filter for rate $\varepsilon$ takes $1.44\, n \log_2(1/\varepsilon)$ bits. Without the sandwich, the learned filter meets the same rate on $\mathcal{D}$ when $F_p < \varepsilon$ and $\varepsilon_b = (\varepsilon - F_p)/(1 - F_p)$, with $z + 1.44\, F_n n \log_2(1/\varepsilon_b)$ bits. For example, let $n = 10^6$ and $\varepsilon = 0.01$. A Bloom filter needs $9.59 \cdot 10^6$ bits. A classifier with $F_p = 0.005$ and $F_n = 0.5$ needs a backup with $\varepsilon_b = 0.00503$, which takes $5.51 \cdot 10^6$ bits. So the learned filter is smaller only if the classifier takes less than about $4.08 \cdot 10^6$ bits, or 510 kilobytes. Mitzenmacher (2018) states this condition in general: the classifier must be smaller than the space it saves, and a classifier that is only a little better than chance never pays.

**The sandwich.** Mitzenmacher shows that splitting the bits between an initial and a backup filter is better than a backup filter alone. For a fixed classifier and an optimal split, the size of the backup filter depends only on $F_p$ and $F_n$, and each further bit of the budget goes to the initial filter.

**The lower bound does not apply.** The [space lower bound](/bloom-filter-lower-bound/) of $\log_2(1/\varepsilon)$ bits per key is for a per-key rate that holds for every non-key. A learned filter has no such guarantee, which is how it can go below the bound on a favorable distribution.

## Variants

- **Sandwiched learned Bloom filter.** An initial Bloom filter of all keys in front of the classifier, as in lines L1 and L4.
- **Partitioned learned Bloom filters.** Several thresholds split the score range into regions, each with its own backup filter and its own rate, tuned so that regions with many keys get more bits. This was proposed after the papers on this page.
- **Learned filters with other backups.** The backup can be any filter with one-sided error, such as an [xor filter](/xor-filter/), since $N$ is a static set.
- **Simple classifiers.** A [logistic regression](/logistic-regression/) or a small neural network is common. The classifier must be fast, since it runs on every query that passes the initial filter.

## When to use it

Use a learned Bloom filter when the set is static, the keys have a pattern that a small model can learn, the queries come from a known and stable distribution, and the model is much smaller than the space it saves. A typical case is a list of malicious URLs checked by a browser. Do not use it when the queries can be chosen by an adversary or when the distribution of queries can change: then use an ordinary filter, whose rate holds for every key.

## Pitfalls

- **Treating $\varepsilon_{\mathcal{D}}$ as a per-key rate.** The rate holds only on average over $\mathcal{D}$. An adversary who finds one non-key with a high score can query it for ever and get a false positive each time.
- **Distribution shift.** If the queries change, $F_p$ changes, and the bound is lost. Measure $F_p$ again from time to time.
- **Measuring $F_p$ on training data.** This underestimates it. Use a held-out set of non-keys from the query distribution.
- **Forgetting the classifier in the space.** The model's size $z$ is part of the filter. A large model can cost more than a plain Bloom filter.
- **Updating the set.** A new key may get a low score and must go to the backup filter; a new classifier changes $N$ and needs a new backup filter. The structure is meant for static sets.
- **Correlation with the hash functions.** The analysis needs the hash functions to be independent of the classifier and of $\mathcal{D}$. With ordinary seeded hash functions this holds.

## Implementations

The Python class takes the classifier as a function and the threshold as a number, and builds the backup filter and the optional initial filter with BLAKE2b and independent salts. It keeps the list $N$ of false negatives for inspection.

## History

Kraska, Beutel, Chi, Dean and Polyzotis (2018) proposed learned index structures, which replace parts of classic index structures by models, and gave the learned Bloom filter with a backup filter as their example for existence indexes. Mitzenmacher (2018) pointed out that its guarantee is with respect to a query distribution, gave a model to compare its size with that of a Bloom filter, and introduced the sandwiched learned Bloom filter with its optimal split of bits. Later work tuned the thresholds and the backup filters further.

## References
