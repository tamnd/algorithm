---
tag: YF8AZR
kind: technique
slug: universal-hashing
name: Universal hashing
aliases:
- 2-universal hashing
- Carter-Wegman hashing
- random hashing with universal families
- universal hashing scheme
area: data-structures/hashing
level: core
summary: Choose a hash function at random from a family so that any two keys collide with low probability.
prereqs: [universal-hash-family, separate-chaining, linearity-of-expectation]
see_also: [hash-table, fks-perfect-hashing, k-wise-independent-hashing, tabulation-hashing, multiplicative-hashing, universal-string-hashing, algorithmic-complexity-attack, uniform-hashing-assumption]
sources:
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (the definition of a universal class and the expected cost of a sequence of operations with chaining)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the parts on random hashing and on universal families
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 15.3 (Universal Families of Hash Functions), including 15.3.3 (Application, Perfect Hashing)
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3), 1984
    locator: pages 538 to 544
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981
    locator: pages 265 to 279 (strongly universal classes and authentication)
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ruzic, Linear probing with constant independence, SIAM Journal on Computing 39(3), 2009
    locator: pages 1107 to 1120 (pairwise independence can give logarithmic expected time, 5-wise independence gives constant expected time)
---

Universal hashing is the technique of drawing the [hash function](/hash-function/) at random from a [universal family](/universal-hash-family/) $\mathcal{H}$ when the structure is built, so that each two distinct keys collide with probability at most $1/m$ over the draw. The keys can be any fixed set, even the worst one, as long as they are chosen without knowledge of the drawn function. With [separate chaining](/separate-chaining/), each operation then takes $O(1 + \alpha)$ expected time, where $\alpha$ is the [load factor](/load-factor/), and no assumption on the distribution of the keys is necessary. Carter and Wegman presented the technique in 1977 and published the journal version in 1979.

## In plain words

A fixed hash function always has bad inputs. If someone knows the function, they can pick many keys that all land in the same bucket, and the table becomes a slow list.

Universal hashing hides the function. The program keeps a large family of hash functions and picks one of them at random when it starts. The family is built so that, for any two different keys, only a small share of its functions sends both keys to the same bucket. A person who picks the keys in advance does not know which function the program will use. So whatever keys they pick, each pair of keys collides only rarely, on average over the random pick. The program pays for this with one random choice at the start, not with any assumption about the keys.

## When it applies

- The cost of the structure depends on the number of collisions between pairs of keys: the length of a chain, the number of colliding pairs, the error of a counter that adds the values of colliding items.
- The keys are not random, or they come from a user who can be hostile, so the [uniform hashing assumption](/uniform-hashing-assumption/) cannot be justified.
- The input is fixed before the random choice, or it does not depend on the drawn function. In the language of randomized algorithms, the adversary is [oblivious](/oblivious-adversary/).
- The analysis needs only expected values over pairs. Bounds that need a whole long run of keys to behave, such as the probe count of [linear probing](/linear-probing/) or the maximum chain length, need a stronger family (see Variations).

## The template

```pseudo id=main
UNIVERSAL-HASHING(H, S, ops)                ▷ H: a universal family into {0, ..., m − 1}
L1  draw h uniformly at random from H         ▷ hole: the family H; the draw is independent of S and ops
L2  build the structure for the key set S with h    ▷ hole: chains, counters, a second level
L3  for each operation in ops on a key x do
L4      j ← h(x)
L5      do the work of the operation in bucket j only   ▷ cost: 1 + the number of keys in bucket j
L6  if a bucket is longer than a set limit then rebuild from L1   ▷ optional: a new random h
```

**The holes.** Line L1 needs a concrete family, such as $h_{a,b}(x) = ((ax + b) \bmod p) \bmod m$ with a prime $p$ larger than every key, $a \in \{1, \dots, p-1\}$ and $b \in \{0, \dots, p-1\}$. To draw $h$ is to draw $a$ and $b$, so the function is stored in two words. Line L2 is the structure: chains for a [hash table](/hash-table/), the rows of a sketch, or the buckets of a two-level table. Line L6 turns a bound on the expected cost into a bound that always holds, at the price of an expected number of rebuilds.

**The analysis.** For a fixed key $x$ and a fixed set $S$, let $X_x = \sum_{y \in S,\, y \ne x} I_{xy}$, where $I_{xy}$ is the [indicator](/indicator-random-variable/) of the event $h(y) = h(x)$. The key $x$ is fixed and the set $S$ is fixed, so the only randomness is the choice of $h$. Universality gives $\mathbb{E}[I_{xy}] = \Pr[h(x) = h(y)] \le 1/m$, and [linearity of expectation](/linearity-of-expectation/) gives

$$\mathbb{E}[X_x] \le \frac{|S \setminus \{x\}|}{m}.$$

This holds with no independence between the events: linearity needs none. Each bound below is this one line, applied to a different sum.

### The chaining bound

**Theorem.** Let $\mathcal{H}$ be a universal family of functions from $U$ to $\{0, \dots, m-1\}$, let $S \subseteq U$ with $|S| = n$, and store $S$ with separate chaining under $h$ drawn uniformly from $\mathcal{H}$. Let $\alpha = n/m$. For each key $x \in U$, let $L(x)$ be the length of the chain of slot $h(x)$.

1. If $x \notin S$, then $\mathbb{E}[L(x)] \le \alpha$.
2. If $x \in S$, then $\mathbb{E}[L(x)] \le 1 + (n-1)/m < 1 + \alpha$.
3. A sequence of $s$ operations (search, insert, delete) that starts from an empty table and never holds more than $n$ keys takes $O(s(1 + n/m))$ expected time, when each operation costs $O(1)$ plus the length of the chain that it scans.

*Proof.* The chain of slot $h(x)$ holds exactly the keys $y \in S$ with $h(y) = h(x)$. (1) If $x \notin S$, then $L(x) = \sum_{y \in S} I_{xy}$, a sum of $n$ indicators, each with expectation at most $1/m$, so $\mathbb{E}[L(x)] \le n/m = \alpha$. (2) If $x \in S$, then $x$ itself is in the chain, so $L(x) = 1 + \sum_{y \in S \setminus \{x\}} I_{xy}$, and the same step gives $\mathbb{E}[L(x)] \le 1 + (n-1)/m$. (3) The sequence is fixed in advance. Before operation $t$, the table holds a set $S_t$ that depends only on the sequence, not on $h$, because chaining stores each key whatever its slot is. So (1) and (2) apply to operation $t$ with the set $S_t$, $|S_t| \le n$, and the operation costs $O(1 + n/m)$ in expectation. Linearity of expectation over the $s$ operations gives $O(s(1 + n/m))$. $\square$

When the table grows with $n$ so that $m = \Omega(n)$, each operation takes $O(1)$ expected time. Part (3) is the main theorem of Carter and Wegman: the bound is on the expected time of every fixed sequence, not on the average over random inputs.

### The number of collisions and the second moment

Let $C = \sum_{\{x, y\} \subseteq S,\, x \ne y} I_{xy}$ be the number of colliding pairs. By linearity, $\mathbb{E}[C] \le \binom{n}{2}/m$. Two facts follow.

- **No collision at all in a table of size $n^2$.** If $m \ge n^2$, then $\mathbb{E}[C] \le n(n-1)/(2n^2) < 1/2$. By [Markov's inequality](/markov-inequality/), $\Pr[C \ge 1] < 1/2$. So a random $h$ is injective on $S$ with probability more than $1/2$, and an expected number of fewer than 2 draws finds one.
- **Linear total of squares in a table of size $n$.** Let $L_j$ be the number of keys in slot $j$. Each slot with $L_j$ keys holds $\binom{L_j}{2}$ colliding pairs, so $\sum_j L_j^2 = \sum_j (L_j + 2\binom{L_j}{2}) = n + 2C$. Hence $\mathbb{E}\big[\sum_j L_j^2\big] \le n + n(n-1)/m$, which is less than $2n$ for $m = n$.

These two facts are the two levels of [FKS perfect hashing](/fks-perfect-hashing/): a first table of size $n$ whose slot $j$ gets its own collision-free table of size $L_j^2$, with $O(n)$ total space in expectation.

### What universality does not give

The longest chain $L_{\max} = \max_j L_j$ also has $\binom{L_{\max}}{2} \le C$. With $m = n$ this gives $\mathbb{E}[L_{\max}(L_{\max} - 1)] \le n - 1$. Since $\mathbb{E}[L_{\max}]^2 \le \mathbb{E}[L_{\max}^2]$ (the variance is not negative), we get $\mathbb{E}[L_{\max}]^2 - \mathbb{E}[L_{\max}] \le n - 1$, so $\mathbb{E}[L_{\max}] < 1 + \sqrt{n}$. This is far weaker than the $\Theta(\log n / \log \log n)$ of a fully random function in the [balls into bins](/balls-into-bins/) model, and universality alone does not give the stronger bound. Bounds on the longest chain or on runs of occupied slots need more independence.

### A worked example

Take the prime $p = 97$, $m = 10$ slots, and the ten keys $0, 10, 20, \dots, 90$. The fixed function $h(x) = x \bmod 10$ puts all ten keys in slot 0, so a search for 0 can scan ten keys. Now draw $h_{a,b}(x) = ((ax + b) \bmod 97) \bmod 10$ with $a \in \{1, \dots, 96\}$ and $b \in \{0, \dots, 96\}$, all $96 \cdot 97 = 9312$ choices equally likely. Over these choices, the expected number of other keys in the chain of key 0 is $1269/1552 \approx 0.818$, below the bound $(n-1)/m = 0.9$ of part (2). The expected longest chain is about $2.34$. The same keys that defeat the fixed function are harmless for the random one.

## Classic examples

- **[Separate chaining](/separate-chaining/).** The theorem above: $O(1 + \alpha)$ expected time for each operation of each fixed sequence.
- **[Hash tables](/hash-table/) under attack.** A table whose function is known can be filled with keys of one bucket, an [algorithmic complexity attack](/algorithmic-complexity-attack/). A function drawn at start-up from a universal family, with a seed the attacker does not see, removes the bad input.
- **[FKS perfect hashing](/fks-perfect-hashing/).** The two collision counts above give a static dictionary with $O(1)$ worst-case search and $O(n)$ expected space. Fredman, Komlos and Szemeredi built it in 1984; it is the base of [perfect hashing](/perfect-hashing/).
- **[Count-min sketch](/count-min-sketch/).** Each row uses a pairwise independent function. The error of a counter is the sum of the counts of the items that collide with the query, and its expectation is bounded by the same linearity argument.
- **[Universal string hashing](/universal-string-hashing/).** A polynomial with the characters as coefficients, evaluated at a random point modulo a prime $p$, makes two different strings of the same length $\ell$ collide with probability at most $(\ell - 1)/p$, because their difference is a nonzero polynomial of degree at most $\ell - 1$. [Rabin-Karp](/rabin-karp/) string matching can use this as its fingerprint.
- **[Message authentication](/message-authentication-code/).** Wegman and Carter (1981) used strongly universal families with a secret function to build authentication tags. For a message tagged with a fresh secret function, the forgery probability is bounded without any assumption on the computing power of the attacker. [Poly1305](/poly1305/) follows this design.

## Variations

- **Strong universality.** A family is strongly universal (pairwise independent) when each pair of distinct keys gets a uniform pair of hash values. This also bounds the variance of the sums above, which [Chebyshev's inequality](/chebyshev-inequality/) turns into concentration. See [universal hash family](/universal-hash-family/).
- **Approximate universality.** A collision probability of $c/m$ for a constant $c$ changes each bound above by the factor $c$ only. The multiply-shift scheme of [multiplicative hashing](/multiplicative-hashing/) has $c = 2$ and costs one multiplication and one shift.
- **Higher independence.** [$k$-wise independent](/k-wise-independent-hashing/) families bound the moments of order $k$. Pagh, Pagh and Ruzic showed in 2007 that 5-wise independence gives expected constant time for each operation of [linear probing](/linear-probing/).
- **Tabulation.** [Tabulation hashing](/tabulation-hashing/) is 3-wise independent and fast, and it gives many of the guarantees of a fully random function.
- **Rehash on bad luck.** Line L6 bounds the cost in all cases. If a chain gets longer than a constant times its expected length, draw a new $h$ and rebuild. By Markov's inequality each draw fails with probability at most a constant, so the expected number of rebuilds is constant. This makes the structure a [Las Vegas algorithm](/las-vegas-algorithm/).

## Pitfalls

- **Keys that depend on the function.** The bound needs $S$ and the operations to be independent of $h$. If the program prints the table in slot order, or its timing shows which searches are slow, an [adaptive adversary](/adaptive-adversary/) can learn about $h$ and choose colliding keys. Keep the seed secret and do not reveal the order of the buckets.
- **A seed fixed at build time.** Line L1 must run at each start of the program, from a real source of randomness. A constant seed in the code makes the family one fixed function again.
- **Universal is not uniform.** Universality bounds the probability of a collision of two keys. It does not say that one key is uniform over the slots, and it does not bound the longest chain by more than about $\sqrt{n}$. Do not quote the bounds of the [uniform hashing assumption](/uniform-hashing-assumption/) for a universal family.
- **Keys outside the field.** The family $((ax + b) \bmod p) \bmod m$ is universal only for keys in $\{0, \dots, p-1\}$. The keys $x$ and $x + p$ collide under every $a$ and $b$. Choose $p$ larger than every key, or hash longer keys with a string family first.
- **The value $a = 0$.** If line L1 draws $a$ from $\{0, \dots, p-1\}$, the functions with $a = 0$ are constant. For $p = 17$ and $m = 6$, the worst pair then collides with probability $49/289 \approx 0.170$, more than $1/6$, so the family is not universal.
- **Universal hashing for open addressing.** The probe count of linear probing depends on runs of many keys, not on pairs. Pagh, Pagh and Ruzic showed that some pairwise independent families make linear probing take logarithmic expected time per operation. Use a 5-wise independent family or tabulation hashing there.

## Exercises

1. Show that if $\Pr[h(x) = h(y)] \le 1/m$ for each pair, then for each fixed set $S$ of $n$ keys there is a slot whose chain has at least $n/m$ keys, for every $h$. Why does this not contradict part (1) of the theorem?
2. Prove that the family of all functions from $U$ to $\{0, \dots, m-1\}$ is universal, and that for this family $\mathbb{E}[C] = \binom{n}{2}/m$ exactly. How many words does it take to store one function of this family when $|U| = 2^{32}$?
3. With $m = n^2$, prove that the probability that $h$ is injective on $S$ is more than $1/2$, and compute the expected number of draws of line L1 until $h$ is injective.
4. Prove that $\mathbb{E}[\sum_j L_j^2] < 2n$ when $m = n$, and use it to bound the expected cost of searching for a random key of $S$.

## References
