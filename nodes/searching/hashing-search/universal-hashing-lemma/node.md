---
tag: V6RF8F
kind: theorem
slug: universal-hashing-lemma
name: Universal hashing expected chain length
aliases:
- universal hashing theorem
area: searching/hashing-search
level: core
summary: With a universal family and chaining, expected unsuccessful search is O(1+alpha).
model: word-ram
prereqs: [universal-hash-family, separate-chaining, linearity-of-expectation, indicator-random-variable, load-factor]
see_also: [universal-hashing, universal-hashing-expected-chain-length, chaining-expected-search-time, simple-uniform-hashing, k-wise-independent-hashing, multiply-shift-hashing, algorithmic-complexity-attack, fks-perfect-hashing]
sources:
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2) (1979)
    locator: pages 143 to 154 (the definition of a universal class and the bound on the expected length of a chain and on the expected cost of a sequence of operations)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the part on universal hashing, with the theorem on the expected length of the list of a key and its corollary for a sequence of operations
  - paper: doi:10.1007/3-540-46766-1_5
    title: Douglas R. Stinson, Universal hashing and authentication codes, Advances in Cryptology, CRYPTO 1991, Lecture Notes in Computer Science 576 (1992)
    locator: pages 74 to 85 (the lower bound (a - b)/(b(a - 1)) on epsilon for an epsilon-almost-universal family of functions from a set of size a to a set of size b)
---

The universal hashing lemma bounds the expected length of a chain in a hash table with [separate chaining](/separate-chaining/) when the [hash function](/hash-function/) is drawn from a [universal family](/universal-hash-family/): for any fixed set of $n$ keys in $m$ slots, a search for an absent key meets at most $\alpha = n/m$ keys on average, and a search for a stored key at most $1 + \alpha$. The keys may be the worst possible set, as long as they do not depend on the random choice of the function, so the bound replaces the assumption of [simple uniform hashing](/simple-uniform-hashing/) on the input by a random choice that the algorithm makes. This page states the lemma for $\varepsilon$-universal families, gives the average over stored keys in insertion order, and shows that a collision probability of $1/m$ is close to the best that any family can reach.

## Statement

Let $U$ be a universe with $|U| = u$, let $m \ge 1$, and let $\mathcal{H}$ be a family of functions from $U$ to $\{0, \ldots, m - 1\}$. For $\varepsilon > 0$, call $\mathcal{H}$ *$\varepsilon$-universal* if $\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le \varepsilon$ for all distinct $x, y \in U$, where $h$ is uniform on $\mathcal{H}$. A *universal* family is a $(1/m)$-universal one.

Let $S = \{x_1, \ldots, x_n\} \subseteq U$ be $n$ distinct keys, fixed before $h$ is drawn, and let the table insert them in this order, each at the head of its chain. For a key $x$, let $L(x)$ be the number of keys of $S \setminus \{x\}$ in the chain of slot $h(x)$.

**Theorem.**

1. **(Exact form.)** For every key $x \in U$, $\mathrm{E}[L(x)] = \sum_{y \in S \setminus \{x\}} \Pr[h(x) = h(y)]$.
2. **(Unsuccessful search.)** If $\mathcal{H}$ is $\varepsilon$-universal and $x \notin S$, then $\mathrm{E}[L(x)] \le \varepsilon n$. For a universal family this is at most $\alpha$.
3. **(Successful search.)** If $\mathcal{H}$ is $\varepsilon$-universal, a search for $x_i$ examines at most $1 + \varepsilon(n - i)$ keys in expectation, and a search for a key chosen uniformly from $S$, independently of $h$, examines at most $1 + \varepsilon (n - 1)/2$ keys in expectation. For a universal family this is at most $1 + (n - 1)/(2m) < 1 + \alpha/2$.
4. **(Limit on $\varepsilon$.)** Every family of functions from $U$ to $\{0, \ldots, m - 1\}$ has two distinct keys $x, y$ with
$$\Pr[h(x) = h(y)] \ge \frac{u - m}{m(u - 1)}.$$

So with a universal family, every search, insertion and deletion takes $O(1 + \alpha)$ expected time on the [word RAM](/word-ram/), when computing $h$ and comparing two keys take $O(1)$ time.

## In plain words

A universal family is a large supply of hash functions with one promise: if you pick one of them at random, any two different keys land in the same slot with chance at most one in the number of slots. Nothing else is promised.

That one promise is enough for chained tables. The keys in the chain of a searched key are the keys that collide with it. Each other key collides with small chance, so on average the chain holds at most the number of keys divided by the number of slots. This holds for every set of keys, even one picked to be bad, because the bad luck comes from the random pick of the function, not from the keys. The last part says that no family can promise a much smaller chance of collision, so universal families are close to the best possible.

## Proof

For distinct keys $x$ and $y$, let $I_{xy}$ be the [indicator](/indicator-random-variable/) of the event $h(x) = h(y)$, so $\mathrm{E}[I_{xy}] = \Pr[h(x) = h(y)]$.

**Part 1.** The chain of slot $h(x)$ holds exactly the keys $y \in S$ with $h(y) = h(x)$. So $L(x) = \sum_{y \in S \setminus \{x\}} I_{xy}$, and [linearity of expectation](/linearity-of-expectation/) gives the formula. It needs no independence between the indicators. The set $S$ must not depend on $h$; otherwise the sum would run over a random set.

**Part 2.** If $x \notin S$, the sum of Part 1 has $n$ terms, each at most $\varepsilon$.

**Part 3.** With head insertion, the chain of $x_i$ lists, before $x_i$, the keys of its slot that were inserted after $x_i$. A search for $x_i$ examines these keys and then $x_i$, so it examines $1 + \sum_{j > i} I_{x_i x_j}$ keys, with expectation at most $1 + \varepsilon (n - i)$. Averaging over $i$,
$$\frac{1}{n} \sum_{i=1}^{n} \bigl(1 + \varepsilon (n - i)\bigr) = 1 + \frac{\varepsilon}{n} \cdot \frac{n(n-1)}{2} = 1 + \frac{\varepsilon(n-1)}{2}.$$
With $\varepsilon = 1/m$ this is $1 + (n-1)/(2m)$, and $(n-1)/(2m) < n/(2m) = \alpha/2$.

**Part 4.** Fix one function $h$ of the family, and let $c_j$ be the number of keys of $U$ that $h$ maps to slot $j$, so $\sum_j c_j = u$. The number of ordered pairs $(x, y)$ of distinct keys with $h(x) = h(y)$ is $\sum_j c_j (c_j - 1) = \sum_j c_j^2 - u$. By the Cauchy-Schwarz inequality, $\sum_j c_j^2 \ge (\sum_j c_j)^2 / m = u^2/m$. So each $h$ has at least $u^2/m - u$ colliding ordered pairs. Sum over the family and divide by $|\mathcal{H}|$ and by the $u(u - 1)$ ordered pairs: the average over all pairs of $\Pr[h(x) = h(y)]$ is at least
$$\frac{u^2/m - u}{u(u - 1)} = \frac{u - m}{m(u - 1)}.$$
Some pair has a probability at least the average.

**The time bound.** A search for $x$ costs $O(1)$ for the hash plus $O(1)$ per key it examines, which is at most $1 + L(x)$ keys. By Parts 2 and 3 with $\varepsilon = 1/m$, this is $O(1 + \alpha)$ in expectation. An insertion or a deletion first searches the chain and then does $O(1)$ more work. $\blacksquare$

## Consequences

**A worked family.** Let $p = 7$ and $m = 3$, and let $\mathcal{H}$ hold the 42 functions $h_{a,b}(x) = ((a x + b) \bmod 7) \bmod 3$ with $a \in \{1, \ldots, 6\}$ and $b \in \{0, \ldots, 6\}$, on $U = \{0, \ldots, 6\}$. Counting over the 42 functions, every pair of distinct keys collides under exactly 10 of them, so $\Pr[h(x) = h(y)] = 5/21 \approx 0.238$ for all pairs, below $1/m = 1/3$. Part 4 gives the lower limit $(7 - 3)/(3 \cdot 6) = 2/9 \approx 0.222$. For $S = \{1, 2, 4, 6\}$, Part 1 gives $\mathrm{E}[L(0)] = 4 \cdot 5/21 = 20/21$, against the universal bound $\alpha = 4/3$. With $S$ inserted in this order, a successful search examines $1 + (5/21)(3 + 2 + 1 + 0)/4 = 19/14 \approx 1.357$ keys on average, against the bound $1 + 3/6 = 1.5$ of Part 3.

**Approximate universality is enough.** A family with $\varepsilon = c/m$ for a constant $c$ gives $O(1 + \alpha)$ with the constant $c$. The multiply-shift scheme of [multiply-shift hashing](/multiply-shift-hashing/) has $\varepsilon = 2/m$ and costs one multiplication and one shift, so it is the usual choice in practice.

**Sequences of operations.** For a sequence of operations fixed in advance, the set of keys in the table before each operation depends only on the sequence, so Parts 2 and 3 apply to each operation in turn, and a sequence of $s$ operations on at most $n$ keys costs $O(s(1 + n/m))$ in expectation. This is the main theorem of Carter and Wegman, and the [universal hashing](/universal-hashing/) page gives its proof.

**Protection against chosen inputs.** The bound holds for every $S$ that is chosen without knowledge of $h$. A table that draws $h$ at start-up from a secret seed thus resists an [algorithmic complexity attack](/algorithmic-complexity-attack/) by an adversary who knows the code but not the seed. It does not resist an adversary who can see where keys land and adapt to it.

**Same mean as the random-function model.** For a universal family, the bounds of Parts 2 and 3 are the exact means of [expected search time with chaining](/chaining-expected-search-time/) under simple uniform hashing. So for the mean search cost, a family of $O(\log u)$-bit functions does as well as a truly random function.

## Tightness

**The value $1/m$ is nearly optimal.** Part 4 shows that $\varepsilon \ge (u - m)/(m(u - 1)) = \frac{1}{m} \cdot \frac{1 - m/u}{1 - 1/u}$. When $u$ is much larger than $m$, this tends to $1/m$, so no family improves the guarantee of a universal family by more than a factor close to 1. The bound is reached exactly. Let $q$ be a prime, $U = \mathbb{Z}_q^2$ with $u = q^2$, $m = q$, and let the family hold the $q + 1$ functions $h_a(x_1, x_2) = (x_1 + a x_2) \bmod q$ for $a \in \mathbb{Z}_q$ and $h_\infty(x_1, x_2) = x_2$. Each function sends the points of one parallel class of lines of the plane over $\mathbb{Z}_q$ to one slot per line. Two distinct points lie on exactly one common line, so they collide under exactly one of the $q + 1$ functions, with probability $1/(q + 1) = (q^2 - q)/(q(q^2 - 1))$.

**The exact form is tight for each set.** Part 1 is an equality, so the bound of Part 2 is reached by every family in which each collision probability equals $\varepsilon$, as in the two families above.

**What the lemma does not give.** The lemma bounds a mean. It gives no useful bound on the probability that one chain is long beyond [Markov's inequality](/markov-inequality/), and it bounds the expected longest chain only by about $\sqrt{n}$ when $m = n$, as shown on the [universal hashing](/universal-hashing/) page. Bounds of the order $\log n / \log \log n$ on the longest chain need more independence, as in [k-wise independent hashing](/k-wise-independent-hashing/). The lemma also says nothing about [open addressing](/open-addressing/), whose cost depends on runs of occupied slots, not on pairwise collisions.

**The keys must not depend on $h$.** If the adversary chooses $S$ after seeing $h$, it can put all $n$ keys in one chain whenever $u \ge (n-1)m + 1$, by the pigeonhole principle, and the expected cost becomes $\Theta(n)$.

## History

Carter and Wegman introduced universal classes of hash functions in a conference paper of 1977 and in the journal paper of 1979, with the bound on the expected chain length and its consequence for any sequence of operations. CLRS presents the lemma in its section on universal hashing as the theorem on the expected length of the list of a key, with the corollary for a sequence of operations. Stinson, in 1991, proved the lower bound on $\varepsilon$ for $\varepsilon$-almost-universal families in his study of authentication codes.

## References
