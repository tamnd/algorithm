---
tag: D6GPVW
kind: concept
slug: hash-collision
name: Hash collision
aliases:
- collision
area: data-structures/hashing
level: intro
summary: Two distinct keys mapped to the same table slot.
prereqs: [hash-function, pigeonhole-principle]
see_also: [collision-resolution, birthday-paradox, universal-hash-family, perfect-hashing, collision-resistance, algorithmic-complexity-attack, hash-table, birthday-attack]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (Hash tables), the definition of a collision and collision resolution by chaining
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the introduction, with the birthday paradox as the reason why collisions are hard to avoid
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 5.1 (The birthday paradox)
---

A hash collision is a pair of distinct keys $x \ne y$ with $h(x) = h(y)$ for a [hash function](/hash-function/) $h$. When the universe of keys is larger than the number of slots, collisions must exist, by the [pigeonhole principle](/pigeonhole-principle/). When the keys are spread at random, collisions appear much sooner than intuition says: by the [birthday paradox](/birthday-paradox/), about $\sqrt{m}$ keys in $m$ slots are enough. So each [hash table](/hash-table/) needs a method of [collision resolution](/collision-resolution/), and the analysis of hashing is mostly a count of collisions.

## In plain words

A hash function turns a key, such as a name, into a slot number. There are many more possible names than slots, so some different names must get the same slot number. This is a collision.

A collision is not an error. It is a normal event that each hash table must handle, for example by keeping a short list of the keys in each slot. What matters is how many collisions there are. A good hash function spreads the keys so that each slot gets only a few of them. A bad one, or an unlucky set of keys, puts many keys in one slot, and then the table becomes slow.

Collisions also come sooner than people expect. With a thousand keys and a million slots, the chance that two keys share a slot is already about two in five.

## The idea

Let $U$ be the universe of keys and let $h : U \to \{0, 1, \ldots, m - 1\}$. Two keys $x, y \in U$ **collide** under $h$ when $x \ne y$ and $h(x) = h(y)$. For a set $S \subseteq U$ of keys, the number of collisions of $S$ is the number of unordered pairs $\{x, y\} \subseteq S$ that collide.

**Collisions are unavoidable.** If $|U| > m$, then some two keys of $U$ collide, by the pigeonhole principle. More precisely, if $|U| > (t - 1) m$, then some slot receives at least $t$ keys of $U$. So for a fixed $h$ and a large universe, there is a set of $t$ keys that all share one slot. This is why a fixed hash function cannot give a worst-case bound, and why an adversary who knows $h$ can slow a table down (an [algorithmic complexity attack](/algorithmic-complexity-attack/)).

**Expected number of collisions.** Assume that $h$ maps the $n$ keys of $S$ to slots independently and uniformly at random, or more weakly that $\Pr[h(x) = h(y)] \le 1/m$ for each pair of distinct keys, as for a [universal family](/universal-hash-family/). Let $X_{xy}$ be the indicator of a collision of $x$ and $y$. By [linearity of expectation](/linearity-of-expectation/), the expected number of collisions is

$$E\Big[\sum_{\{x, y\} \subseteq S} X_{xy}\Big] = \sum_{\{x, y\} \subseteq S} \Pr[h(x) = h(y)] \le \binom{n}{2} \frac{1}{m}.$$

Only pairwise independence is used here, and the bound is an equality for a uniform random function.

**Probability of at least one collision.** For a uniform random function, the $n$ keys are all in distinct slots with probability

$$\prod_{i=0}^{n-1} \Big(1 - \frac{i}{m}\Big) \le \prod_{i=0}^{n-1} e^{-i/m} = e^{-n(n-1)/(2m)},$$

using $1 - t \le e^{-t}$. So with $n \ge \sqrt{2 m \ln 2} + 1$ keys, a collision happens with probability at least $1/2$. Collisions are avoided with constant probability only when $m = \Omega(n^2)$. The two-level scheme of [FKS perfect hashing](/fks-perfect-hashing/) uses exactly this fact: a second-level table of size about $n_i^2$ for a bucket of $n_i$ keys is free of collisions with probability at least $1/2$.

**Slot collisions and hash code collisions.** In practice a key is first turned into a hash code, an integer of 32 or 64 bits, and the code is then reduced to a slot, for example by $\bmod\ m$. Two keys can collide because their codes are equal, or because different codes give the same slot. A table cannot fix the first kind by growing, because equal codes stay equal for each $m$.

## Examples

- **The division method.** With $h(k) = k \bmod 10$, the keys 12 and 42 collide in slot 2, and 7 and 97 collide in slot 7. Each key that ends in the same decimal digit collides with each other one, which is why the [division method](/division-method/) avoids a modulus such as 10 or a power of two.
- **Java strings.** `String.hashCode` computes $s_0 \cdot 31^{L-1} + \cdots + s_{L-1}$ modulo $2^{32}$. The strings `"Aa"` and `"BB"` both have code 2112, because $65 \cdot 31 + 97 = 66 \cdot 31 + 66$. Each string made of $t$ blocks, each block `"Aa"` or `"BB"`, has the same code: `"AaAa"`, `"AaBB"` and `"BBBB"` all have code 2031744. This gives $2^t$ strings with one hash code, a code collision that no table size can separate.
- **The birthday numbers.** For $n = 23$ keys in $m = 365$ slots, a uniform random function gives at least one collision with probability about 0.507, and the expected number of colliding pairs is $\binom{23}{2}/365 \approx 0.693$. For $m = 10^6$ slots, 1000 keys give a collision with probability about 0.393, and 1178 keys are the least number that make it more than $1/2$.
- **Non-example.** For a set $S$ known in advance, a [perfect hash function](/perfect-hashing/) maps $S$ to slots with no collision at all. Two keys outside $S$, or one inside and one outside, may still share a slot, but a search compares with the stored key and sees the difference.

## Where it is used

- [Collision resolution](/collision-resolution/), with [separate chaining](/separate-chaining/) or [open addressing](/open-addressing/), decides where a colliding key goes.
- The [analysis of separate chaining](/chaining-analysis/) and the [analysis of linear probing](/linear-probing-analysis/) bound the cost of a search by the expected number of collisions.
- [Universal hashing](/universal-hashing/) bounds the probability of a collision of each fixed pair by $1/m$, for any keys.
- [Perfect hashing](/perfect-hashing/) and [FKS perfect hashing](/fks-perfect-hashing/) build functions with no collision on a fixed set.
- A [Bloom filter](/bloom-filter/) has false positives because of collisions in its bit array.
- In cryptography, [collision resistance](/collision-resistance/) asks that no efficient algorithm finds a collision of a [cryptographic hash function](/cryptographic-hash-function/), and the [birthday attack](/birthday-attack/) finds one in about $2^{b/2}$ evaluations for a $b$-bit output.

## References
