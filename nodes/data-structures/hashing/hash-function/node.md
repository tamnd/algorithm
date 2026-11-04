---
tag: DWJMXJ
kind: definition
slug: hash-function
name: Hash function
aliases:
- hash map function
- hashing function
area: data-structures/hashing
level: intro
summary: Map from a key universe to table slots, ideally spreading keys evenly.
prereqs: [direct-address-table, pigeonhole-principle]
see_also: [hash-table, hash-collision, division-method, multiplicative-hashing, universal-hash-family, simple-uniform-hashing, polynomial-rolling-hash, cryptographic-hash-function]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (the hash function of a table) and Section 11.3 (Hash functions, with the division, multiplication and universal methods)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the part on hash functions (division and multiplicative hashing)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), the part on hash functions (modular hashing, hashCode, the uniform hashing assumption)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (the definition of a universal class of hash functions)
---

A hash function is a function $h : U \to \{0, 1, \ldots, m - 1\}$ from a universe $U$ of keys to the $m$ slots of a table. A [hash table](/hash-table/) stores key $k$ in slot $h(k)$, so a search for $k$ goes straight to one slot. When $|U| > m$, some two keys always have the same slot, which is a [hash collision](/hash-collision/), so a good hash function is one that spreads the keys of the actual input evenly over the slots. It must be fast to compute and must give the same value each time it sees the same key.

## Definition

Let $U$ be a set, the **universe** of keys, and let $m \ge 1$ be an integer, the number of **slots** (or buckets). Write $[m] = \{0, 1, \ldots, m - 1\}$.

A **hash function** for $U$ and $m$ is a function $h : U \to [m]$. The value $h(k)$ is the **hash value** (or hash, or home slot) of $k$. Two distinct keys $x \ne y$ with $h(x) = h(y)$ **collide**.

Being a function, $h$ is **deterministic**: each call on the same key gives the same value. When $U$ has an equality $\equiv$ that is coarser than identity (for example two string objects with the same characters), a hash function for a table must also respect it:

$$x \equiv y \implies h(x) = h(y) \quad \text{for all } x, y \in U.$$

In practice $h$ is often the composition $h = c \circ g$ of a **hash code** $g : U \to \{0, 1, \ldots, 2^w - 1\}$, which turns a key into a $w$-bit integer, and a **compression map** $c$ from $w$-bit integers to $[m]$, such as $c(z) = z \bmod m$. A language library usually gives $g$ (Java `hashCode`, Python `__hash__`), and the table gives $c$.

**What makes a hash function good.** The definition says nothing about quality. Three standard ways to state quality are:

- **Balance on the universe.** Each slot has about the same number of preimages: $|h^{-1}(i)| \in \{\lfloor |U|/m \rfloor, \lceil |U|/m \rceil\}$ for each $i \in [m]$. This is necessary but far from enough: $h(k) = k \bmod m$ is balanced on $U = \{0, \ldots, N-1\}$, yet it maps all multiples of $m$ to slot 0.
- **Simple uniform hashing.** A model, not a property of one function: each key is assumed to fall in each slot with probability $1/m$, independently of the other keys. See [simple uniform hashing](/simple-uniform-hashing/) and the [uniform hashing assumption](/uniform-hashing-assumption/).
- **Random choice from a family.** Choose $h$ at random from a family $\mathcal{H}$ of functions, after the keys are fixed. The family is [universal](/universal-hash-family/) when $\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le 1/m$ for all $x \ne y$ in $U$, and [$k$-wise independent](/k-wise-independent-hashing/) when the values of any $k$ distinct keys are independent and uniform on $[m]$. These give proved bounds for every set of keys.

No single fixed function is good for every input. If $|U| \ge (n - 1) m + 1$, then by the [pigeonhole principle](/pigeonhole-principle/) some $n$ keys of $U$ share one slot, and an input of those $n$ keys puts them all in one bucket. Random choice of $h$ from a family is the way around this bound.

## Examples and non-examples

**The division method.** $h(k) = k \bmod m$ for integer keys. With $m = 13$, the keys 100, 2024, 7, 20 and 33 have the hash values 9, 9, 7, 7 and 7. With $m = 16$ they have 4, 8, 7, 4 and 1: a power of two keeps only the low 4 bits of the key. See the [division method](/division-method/).

**The multiplicative method.** $h(k) = \lfloor m \cdot \{kA\} \rfloor$, where $\{x\} = x - \lfloor x \rfloor$ and $0 < A < 1$. With $m = 2^{14} = 16384$, $A = 2654435769 / 2^{32}$ (close to $(\sqrt 5 - 1)/2$) and $k = 123456$, the value $k \cdot 2654435769 \bmod 2^{32}$ is 17612864, and its top 14 bits give $h(k) = 67$. See [multiplicative hashing](/multiplicative-hashing/).

**A polynomial string hash.** For a string $s_0 s_1 \cdots s_{L-1}$ of character codes, $g(s) = \sum_{i=0}^{L-1} s_i \cdot 31^{L-1-i} \bmod 2^{32}$ is the hash code of Java's `String.hashCode`. It gives 98262 for "cat", 96402 for "act" and 114582 for "tac", and with $m = 13$ the slots are 8, 7 and 0. See the [polynomial rolling hash](/polynomial-rolling-hash/).

**A bad hash code that is still a hash function.** The sum of the character codes gives 312 for each of "cat", "act" and "tac", since they are anagrams. It is a valid hash function, and all three keys collide.

**A constant function.** $h(k) = 0$ is a hash function. With it, a hash table becomes one list, and each operation takes $\Theta(n)$ time.

**Non-example: a value that changes between calls.** A function that returns a fresh random slot on each call is not a hash function: a search would look in a different slot from the one where the insert put the key. The random choice must happen once, when $h$ is chosen from a family, and then $h$ is fixed.

**Non-example: a hash that ignores equality.** If a type defines two objects as equal when their fields are equal, but $g$ returns the memory address of the object, then two equal keys can get different slots. This breaks the rule $x \equiv y \implies h(x) = h(y)$, and a search for an equal copy of a key fails. See [hash codes for user-defined types](/hash-code-for-user-defined-types/).

**Non-example: a value outside the range.** In Python, `hash(-2)` is $-2$, and `hash(-1)` is also $-2$, since $-1$ is reserved as an error code in the C layer. The hash code can be negative, so it is not yet a slot. The compression $c(z) = z \bmod m$ with a non-negative result (Python's `%`) turns it into one; in C or Java, `z % m` can be negative and is not a valid slot.

## Related definitions

- [Hash collision](/hash-collision/): two distinct keys with the same hash value.
- [Hash table](/hash-table/): the data structure that stores key $k$ in slot $h(k)$, with a method of [collision resolution](/collision-resolution/).
- [Universal hash family](/universal-hash-family/) and [universal hashing](/universal-hashing/): a random choice of $h$ with collision probability at most $1/m$.
- [$k$-wise independent hashing](/k-wise-independent-hashing/): a stronger random family, used by [linear probing](/linear-probing/) and [cuckoo hashing](/cuckoo-hashing/).
- [Perfect hash function](/perfect-hash-function/): a hash function with no collision on a given set $S$; it is minimal when $m = |S|$.
- [Probe sequence](/probe-sequence/): in [open addressing](/open-addressing/), a hash function of two arguments $h(k, i)$, which gives the $i$-th slot to try.
- [Cryptographic hash function](/cryptographic-hash-function/): a different notion. It maps strings to long digests and must make collisions hard to find for an adversary. A table hash needs speed and spread, not this property, though a keyed hash such as [SipHash](/siphash/) is used against an [algorithmic complexity attack](/algorithmic-complexity-attack/).
- [Direct-address table](/direct-address-table/): the case $U = [m]$ with $h(k) = k$, where no collision can happen.

## References
