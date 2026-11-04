---
tag: BRVBY1
kind: concept
slug: uniform-input-model
name: Uniform input model
aliases:
- Uniform distribution assumption
area: sorting/distribution-sorts
level: core
summary: Assumes keys are independent and uniform over an interval, the average-case setting for bucket sort.
prereqs: [uniform-distribution, independent-random-variables, average-case-analysis]
see_also: [bucket-sort, bucket-sort-expected-linear, interpolation-search-expected-time, random-permutation, balls-into-bins, simple-uniform-hashing, flashsort, inverse-transform-sampling]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.4, Bucket sort (the assumption that the input is drawn from a uniform distribution on [0, 1))
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Balls, Bins, and Random Graphs (Section 5.2, the balls and bins model, and Section 5.2.2, bucket sort)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1 (multiple list insertion on uniform keys) and Section 6.2.1 (interpolation search and its average cost)
---

The uniform input model is the assumption that the $n$ keys of an input are [independent random variables](/independent-random-variables/), each [uniform](/uniform-distribution/) on a known interval, usually $[0, 1)$. It is the setting of the [average-case analysis](/average-case-analysis/) of [bucket sort](/bucket-sort/), whose expected time is linear in this model, and of interpolation search. It is stronger than the [random permutation](/random-permutation/) model of comparison sorts: it fixes not only the relative order of the keys but also where they lie in the interval, and that is what a sort that computes positions from key values can exploit.

## In plain words

Imagine that each key is made by a fair random number generator that picks a number between 0 and 1, and that each key is made on its own, without looking at the others. Then any part of the interval gets a share of the keys that matches its length: about a tenth of the keys fall in the first tenth of the interval, and so on. So if you know the value of a key, you know roughly where it will be in the sorted output.

An algorithm that uses this idea can put each key close to its final place with one calculation. If the assumption is wrong, for example if most keys bunch together in one spot, the same algorithm can become very slow. The model is a promise about the data, not something the algorithm can check or force.

## The idea

**The model.** The input is $X_1, \ldots, X_n$, independent, each with the uniform distribution on $[0, 1)$: $\Pr[X_i \in [s, t)] = t - s$ for $0 \le s \le t \le 1$. Keys on another interval $[a, b)$ map to this one by $x \mapsto (x - a)/(b - a)$. A cost is analysed by its expectation over this distribution. The algorithm itself is deterministic.

**What the model gives.**

- *Bucket counts.* Cut $[0, 1)$ into $m$ equal parts. The number $N_j$ of keys in part $j$ is binomial with parameters $n$ and $1/m$, and the vector $(N_0, \ldots, N_{m-1})$ is multinomial. This is the [balls into bins](/balls-into-bins/) model with $n$ balls and $m$ bins. For $m = n$, $\mathbb{E}[N_j] = 1$ and $\mathbb{E}[N_j^2] = 2 - 1/n$, the fact behind [bucket sort expected linear time](/bucket-sort-expected-linear/).
- *Distinct keys.* With probability 1 all keys are distinct, because $\Pr[X_i = X_k] = 0$ for $i \ne k$.
- *A random order.* The order of the keys is a uniform random permutation: by symmetry, each of the $n!$ orders of $X_1, \ldots, X_n$ has the same probability $1/n!$. So each result of the random permutation model, such as the expected $n(n-1)/4$ inversions, also holds here.
- *Rank from value.* The number of keys below a value $x$ is binomial with mean $n x$. So $n X_i$ predicts the rank of $X_i$ with an error of order $\sqrt{n}$ for the whole input, and inside a bucket of size $O(1)$ the error is $O(1)$ in expectation.

**Other distributions.** If the keys are independent with a known continuous distribution function $F$, then $F(X_i)$ is uniform on $[0, 1)$, the reverse of [inverse transform sampling](/inverse-transform-sampling/). So an algorithm that uses $F(x)$ in place of $x$ gets the same expected cost. If $F$ is unknown, a sample of the input can estimate it, as in [sample sort](/sample-sort/).

**Discrete keys.** For integer keys, the analogue is independent keys uniform on $\{0, \ldots, U-1\}$. Then ties have positive probability. All $n$ keys are distinct with probability $\prod_{i=0}^{n-1}(1 - i/U)$, about $e^{-n(n-1)/(2U)}$, which is the [birthday paradox](/birthday-paradox/).

**Limits.** The model is a hypothesis about the data. Real data often has clusters, many equal keys, or a range that is not known in advance. A result in this model says nothing about the worst case, and an adversary that knows the algorithm can always choose a bad input. Algorithms that need a guarantee use a randomized method instead, whose expectation holds for every input, such as hashing with a [universal family](/universal-hashing/).

## Examples

**Buckets for $n = 10$.** For the ten keys $0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68$, the ten buckets of width $0.1$ have the sizes $0, 2, 3, 1, 0, 0, 1, 2, 0, 1$. Four buckets are empty. In the model the expected number of empty buckets is $10 \cdot 0.9^{10} \approx 3.49$.

**Empty and single buckets for $n = 1000$.** With $n$ keys and $n$ buckets, a bucket is empty with probability $(1 - 1/n)^n$ and holds exactly one key with probability $(1 - 1/n)^{n-1}$. For $n = 1000$ the expected numbers are $367.7$ empty buckets and $368.1$ buckets with one key, both close to $n / e \approx 367.9$.

**Interpolation search.** To search for $x$ in a sorted array of $n$ keys from the model, look first at position about $n x$, then repeat on the part that remains. The expected number of probes is about $\lg \lg n$, against $\lg n$ for binary search; see [interpolation search expected time](/interpolation-search-expected-time/). On keys $1, 2, 4, \ldots, 2^{n-1}$ the same method needs about $n$ probes.

**Distinct 32-bit keys.** For $n = 10^5$ keys uniform on $\{0, \ldots, 2^{32} - 1\}$, the probability that all are distinct is about $0.312$. So repeated keys are likely, and a sort for this model must handle ties.

**A bad input for the model.** Keys uniform on $[0, 0.001)$ fit the model for that interval, but a bucket sort that assumes $[0, 1)$ puts all of them, for $n \le 1000$, in bucket 0, and then runs in quadratic time.

## Where it is used

- **[Bucket sort](/bucket-sort/)** runs in expected $\Theta(n)$ time in this model, see [bucket sort expected linear time](/bucket-sort-expected-linear/).
- **[Flashsort](/flashsort/)** and **[proxmap sort](/proxmap-sort/)** use a linear map from key to position, which is accurate when the keys are close to uniform.
- **[Interpolation search](/interpolation-search/)** has expected $O(\log \log n)$ probes on uniform keys.
- **Hashing.** The assumption of [simple uniform hashing](/simple-uniform-hashing/) is the same model applied to hash values instead of keys.
- **The analysis of radix sorts on random strings**, such as the expected number of characters read by [MSD radix sort](/msd-radix-sort/), uses uniform independent characters, the discrete form of the model.

## References
