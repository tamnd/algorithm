---
tag: QAX00H
kind: theorem
slug: yao-open-addressing-lower-bound
name: Yao's lower bound for open addressing
aliases:
- Yao's bound on open addressing
area: data-structures/hashing
level: research
summary: Gives lower bounds on expected probe counts for open addressing with uniform hashing.
history:
  year: 1985
  people: [Andrew Chi-Chih Yao]
  note: Ullman conjectured in 1972 that uniform probing is optimal among greedy open-addressing schemes. Yao proved it in the asymptotic sense in 1985.
prereqs: [open-addressing, uniform-hashing-assumption]
see_also: [open-addressing-expected-probes, probe-sequence, linear-probing-analysis, double-hashing, robin-hood-hashing, load-factor, hockey-stick-identity, jensens-inequality]
sources:
  - paper: doi:10.1145/3828.3836
    title: Andrew C. Yao, Uniform hashing is optimal, Journal of the ACM 32(3), 1985
    locator: pages 687 to 693 (the main theorem and its proof)
  - url: https://arxiv.org/abs/2501.02305
    title: Martín Farach-Colton, Andrew Krapivin and William Kuszmaul, Optimal Bounds for Open Addressing Without Reordering (2025)
    note: the model of greedy open addressing, Yao's theorem as Proposition 7, elastic hashing (Theorem 1), funnel hashing (Theorem 2) and the lower bounds for greedy schemes (Theorem 4)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of uniform probing
---

Yao's lower bound says that uniform probing is the best greedy [open-addressing](/open-addressing/) scheme. Take a table of $m$ slots that holds $n = \alpha m$ keys, where each key was put in the first free slot of its own random probe sequence and was never moved. Then, whatever the distribution of the probe sequences, the mean number of probes of a successful search is at least $\frac{1}{\alpha} \ln \frac{1}{1-\alpha} - o(1)$ as $m \to \infty$. Uniform probing, where each probe sequence is a uniform random permutation of the slots, has this cost, so no greedy scheme does better by more than $o(1)$. Andrew Yao proved this in 1985, which settled a conjecture of Jeffrey Ullman from 1972.

## Statement

**Model.** A table has $m$ slots. Each key $x$ has a probe sequence $\pi_x = (\pi_x(1), \ldots, \pi_x(m))$, a permutation of the slots. The sequences of different keys are independent, and each is drawn from the same distribution $P$ on permutations; $P$ can be any distribution. The keys $x_1, \ldots, x_n$ are inserted in this order into an empty table. The scheme is *greedy*: key $x_i$ goes into the first slot of $\pi_{x_i}$ that is free at that time, and keys never move. The *cost* $c(x)$ of a key is the index $j$ with $\pi_x(j)$ equal to its slot. A search for $x$ that follows $\pi_x$ makes exactly $c(x)$ probes. The *amortized expected cost* is

$$A_P(m, n) = \mathbb{E}\left[\frac{1}{n} \sum_{i=1}^{n} c(x_i)\right],$$

the expected mean cost of a successful search for a key chosen uniformly from the table. This is the model of Farach-Colton, Krapivin and Kuszmaul.

**Theorem (Yao, 1985).** Fix $0 < \alpha < 1$. For every $m$ and every distribution $P$ on probe sequences,

$$A_P(m, \lfloor \alpha m \rfloor) \ge \frac{1}{\alpha} \ln \frac{1}{1 - \alpha} - o(1),$$

where the $o(1)$ term goes to 0 as $m \to \infty$ and does not depend on $P$. Uniform probing, where $P$ is the uniform distribution on all $m!$ permutations, has

$$A_{\text{unif}}(m, n) = \frac{m+1}{n}\left(H_{m+1} - H_{m-n+1}\right) \to \frac{1}{\alpha} \ln \frac{1}{1-\alpha},$$

with $H_k = 1 + \frac{1}{2} + \cdots + \frac{1}{k}$. So uniform probing is optimal up to $o(1)$.

In the form of Farach-Colton, Krapivin and Kuszmaul (their Proposition 7), with $\delta = 1 - \alpha$: in a greedy table of capacity $m$ that holds $(1 - \delta)m$ keys, the amortized expected cost is $\Omega(\log \delta^{-1})$.

## In plain words

Each key has its own random list of slots to try. It tries them in order and takes the first free one, and it stays there. A later search for the key walks the same list, so its cost is how far down the list the key went.

When the table is nearly full, most tries hit a taken slot, so the last keys must walk far. Yao showed that no way of making the lists can avoid this. The best you can do is to make every list a fully random order of the slots, and even then the mean cost grows like the log of one over the free fraction of the table.

The theorem is about tables that never move a key after it is placed and always take the first free slot. Schemes that move keys, or that skip free slots on purpose, can do better.

## Proof

The proof has three parts. Part 1 computes the cost of uniform probing exactly, which gives the value that the theorem says is optimal. Part 2 proves, in full, a weaker lower bound that holds for every scheme, greedy or not. Part 3 is Yao's own proof of the lower bound for greedy schemes, which this page does not reproduce.

**Part 1 (the cost of uniform probing).** Let each $\pi_x$ be a uniform random permutation, independent of the others. Consider the insert of $x_{i+1}$, when a set $S$ of $i$ slots is full. The set $S$ depends only on $\pi_{x_1}, \ldots, \pi_{x_i}$, so it is independent of $\pi_{x_{i+1}}$. For $0 \le j \le m$, the first $j$ entries of a uniform random permutation form a uniform random $j$-subset of the slots. The cost is more than $j$ exactly when these $j$ slots are all in $S$, so

$$\Pr[c(x_{i+1}) > j] = \binom{i}{j} \Big/ \binom{m}{j},$$

which is 0 for $j > i$. A cost is a positive integer, so $\mathbb{E}[c] = \sum_{j \ge 0} \Pr[c > j]$, and

$$\mathbb{E}[c(x_{i+1})] = \sum_{j=0}^{i} \binom{i}{j} \Big/ \binom{m}{j}.$$

Counting the pairs (an $i$-set of slots, a $j$-subset of it) in two ways gives $\binom{m}{i}\binom{i}{j} = \binom{m}{j}\binom{m-j}{i-j}$. So each term is $\binom{m-j}{i-j} / \binom{m}{i}$. With $t = i - j$ and $r = m - i$, the [hockey stick identity](/hockey-stick-identity/) gives

$$\sum_{j=0}^{i} \binom{m-j}{i-j} = \sum_{t=0}^{i} \binom{r + t}{t} = \binom{r + i + 1}{i} = \binom{m+1}{i}.$$

So $\mathbb{E}[c(x_{i+1})] = \binom{m+1}{i} / \binom{m}{i} = \frac{m+1}{m+1-i}$. By [linearity of expectation](/linearity-of-expectation/),

$$A_{\text{unif}}(m, n) = \frac{1}{n} \sum_{i=0}^{n-1} \frac{m+1}{m+1-i} = \frac{m+1}{n} \sum_{k=m-n+2}^{m+1} \frac{1}{k} = \frac{m+1}{n} \left(H_{m+1} - H_{m-n+1}\right).$$

With $n = \lfloor \alpha m \rfloor$ and $H_k = \ln k + \gamma + O(1/k)$, the difference is $\ln \frac{m+1}{m-n+1} + O\left(\frac{1}{(1-\alpha)m}\right) \to \ln \frac{1}{1-\alpha}$, and $\frac{m+1}{n} \to \frac{1}{\alpha}$. This proves the formula for uniform probing.

**Part 2 (a lower bound for every scheme).** Drop the greedy rule. Let each key end in some slot of its own probe sequence, with no two keys in the same slot; the keys may move, and a key may skip free slots. The sequences are still independent with the distribution $P$, and the cost $c(x)$ is still the index of the slot of $x$ in $\pi_x$. Then

$$A_P(m, n) \ge \frac{1}{n} \sum_{j=0}^{m-1} \max\left(0,\; n - m\left(1 - \left(1 - \tfrac{j}{m}\right)^{n}\right)\right).$$

*Proof.* Fix $j$, and let $U_j$ be the set of slots that are among the first $j$ entries of at least one of the $n$ sequences. A key with $c(x) \le j$ sits in a slot of $U_j$, and different keys sit in different slots, so the number of keys with $c(x) \le j$ is at most $|U_j|$. For a slot $s$, let $q_s$ be the probability that $s$ is among the first $j$ entries of a sequence drawn from $P$. A sequence has $j$ distinct entries among its first $j$, so $\sum_s q_s = j$. The $n$ sequences are independent, so $\Pr[s \in U_j] = 1 - (1 - q_s)^n$, and

$$\mathbb{E}|U_j| = \sum_{s} \left(1 - (1 - q_s)^n\right) \le m \left(1 - \left(1 - \tfrac{j}{m}\right)^n\right),$$

because $f(q) = 1 - (1-q)^n$ is concave on $[0, 1]$ and [Jensen's inequality](/jensens-inequality/) gives $\frac{1}{m} \sum_s f(q_s) \le f\left(\frac{1}{m} \sum_s q_s\right)$. So the expected number of keys with $c(x) > j$ is at least $n - m(1 - (1 - j/m)^n)$, and it is also at least 0. A cost is at most $m$, so $\sum_x c(x) = \sum_{j=0}^{m-1} \#\{x : c(x) > j\}$. Take expectations and divide by $n$. $\square$

With $n = \alpha m$ and $j$ fixed, $(1 - j/m)^{\alpha m} \to e^{-\alpha j}$, and $(1 - j/m)^{\alpha m} \le e^{-\alpha j}$ for all $j$. The term for $j$ is at most $n \max(0, 1 - (1 - e^{-\alpha j})/\alpha)$, which is 0 as soon as $e^{-\alpha j} \le 1 - \alpha$, so only a fixed finite set of $j$ counts, and the bound tends to

$$c(\alpha) = \sum_{j \ge 0} \max\left(0,\; 1 - \frac{1 - e^{-\alpha j}}{\alpha}\right).$$

This is a constant: $c(1) = \sum_{j \ge 0} e^{-j} = \frac{e}{e-1} \approx 1.582$. So the counting argument alone does not give a bound that grows as $\alpha \to 1$. The growth to $\ln \frac{1}{1-\alpha}$ needs the greedy rule, and Part 2 shows why it must: the bound of Part 2 holds for all schemes, and some non-greedy schemes do have $O(1)$ cost (see Consequences).

**Part 3 (Yao's lower bound for greedy schemes).** The proof that every distribution $P$ has $A_P(m, \lfloor \alpha m \rfloor) \ge \frac{1}{\alpha} \ln \frac{1}{1-\alpha} - o(1)$ under the greedy rule is in Yao's paper, Journal of the ACM 32(3), pages 687 to 693. Farach-Colton, Krapivin and Kuszmaul report that its techniques build on those of Ajtai. This page does not reproduce it, so for the general lower bound the reader must rely on that paper; Parts 1 and 2 above are complete.

## Consequences

- **Uniform probing is optimal among greedy schemes.** No choice of probe sequences, for example [double hashing](/double-hashing/) or [quadratic probing](/quadratic-probing/), can beat the mean successful search cost of uniform probing by more than $o(1)$ when keys are never moved.
- **Linear probing is not optimal.** Its mean successful cost is about $\frac{1}{2}\left(1 + \frac{1}{1-\alpha}\right)$ (see [the analysis of linear probing](/linear-probing-analysis/)), which at $\alpha = 0.9$ is 5.5 against the optimal 2.56. Linear probing is not a scheme with i.i.d. random permutations, but it is greedy, and the gap is the cost of [primary clustering](/primary-clustering/).
- **Moving keys helps.** The bound of Part 2 is a constant even for a full table. Farach-Colton, Krapivin and Kuszmaul note that schemes that reorder keys, such as the one of Brent and the one of Gonnet and Munro, reach $O(1)$ amortized expected cost even when the table is full.
- **Skipping free slots helps.** Farach-Colton, Krapivin and Kuszmaul give *elastic hashing*, which never moves a key but may skip free slots. It has $O(1)$ amortized expected cost and $O(\log \delta^{-1})$ worst-case expected cost for $\delta = 1 - \alpha$ (their Theorem 1). So the greedy condition in Yao's theorem cannot be dropped.
- **The worst case of one insert.** Yao also conjectured in 1985 that in a greedy scheme some insert has expected cost at least $(1 - o(1))\delta^{-1}$, as in uniform probing. Farach-Colton, Krapivin and Kuszmaul disprove this with *funnel hashing*, a greedy scheme with $O(\log^2 \delta^{-1})$ worst-case expected cost (their Theorem 2), and prove that $\Omega(\log^2 \delta^{-1})$ is optimal for greedy schemes (their Theorem 4, whose proof uses Yao's theorem).

## Tightness

The bound is tight: by Part 1, uniform probing meets it, and its cost is $\frac{m+1}{n}(H_{m+1} - H_{m-n+1})$ for every $m$, not only in the limit. The table compares this exact value at $m = 1000$ with the limit of the theorem and with the weak bound of Part 2.

| $\alpha$ | uniform probing, $m = 1000$ | $\frac{1}{\alpha} \ln \frac{1}{1-\alpha}$ | Part 2 bound, $m = 1000$ | $c(\alpha)$ |
|---|---|---|---|---|
| 0.5 | 1.3847 | 1.3863 | 1.2128 | 1.2131 |
| 0.75 | 1.8443 | 1.8484 | 1.2963 | 1.2965 |
| 0.9 | 2.5461 | 2.5584 | 1.4127 | 1.4132 |
| 0.99 | 4.5162 | 4.6517 | 1.5446 | 1.5455 |
| 1.0 | 6.4930 | · | 1.5810 | 1.5820 |

For a full table, $n = m$, uniform probing has cost $\frac{m+1}{m}(H_{m+1} - 1) = \ln m + O(1)$, so the cost of a greedy scheme is unbounded as the table fills. The $o(1)$ term cannot be dropped in general: at $\alpha = 0.99$ and $m = 1000$ the exact cost 4.5162 is below the limit 4.6517.

## History

Jeffrey Ullman studied open addressing with arbitrary probe sequences in 1972, in "A note on the efficiency of hashing functions" (Journal of the ACM 19(3), pages 569 to 575), and conjectured that uniform probing is optimal among greedy schemes. Knuth later posed a weaker form, for single-hashing schemes, and Ajtai proved it. Andrew Yao proved Ullman's conjecture in the asymptotic form above in "Uniform hashing is optimal", Journal of the ACM, July 1985. In 2025 Farach-Colton, Krapivin and Kuszmaul showed how much the greedy condition matters, with elastic hashing and funnel hashing and matching lower bounds.

## References
