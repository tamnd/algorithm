---
tag: A1QY3C
kind: concept
slug: algorithmic-complexity-attack
name: Algorithmic complexity attack
aliases: [hash flooding, hash collision attack, hash DoS]
area: data-structures/hashing
level: core
summary: Attack that feeds a hash table many keys with colliding hashes, degrading operations from constant time to linear time.
prereqs: [hash-table, hash-collision, universal-hashing]
see_also: [siphash, anti-hash-tests, separate-chaining, worst-case-analysis, quicksort, redos, red-black-tree, pseudorandom-function]
sources:
  - url: https://www.usenix.org/legacy/event/sec03/tech/crosby.html
    title: Scott A. Crosby and Dan S. Wallach, Denial of Service via Algorithmic Complexity Attacks, 12th USENIX Security Symposium, 2003
    locator: the sections on hash tables and the attacks on Perl, the Squid cache and the Bro intrusion detection system
  - url: https://ocert.org/advisories/ocert-2011-003.html
    title: oCERT-2011-003, multiple implementations denial-of-service via hash algorithm collision, 2011
    locator: Description, Affected version and Credit (Alexander Klink and Julian Waelde)
  - paper: doi:10.1007/978-3-642-34931-7_28
    title: Jean-Philippe Aumasson and Daniel J. Bernstein, SipHash, a fast short-input PRF, INDOCRYPT 2012, Lecture Notes in Computer Science 7668
    locator: pp. 489 to 508 (hash flooding as the motivation)
  - url: https://peps.python.org/pep-0456/
    title: Christian Heimes, PEP 456, Secure and interchangeable hash algorithm
    locator: Rationale, and the notes on MurmurHash and CityHash
  - url: https://openjdk.org/jeps/180
    title: JEP 180, Handle Frequent HashMap Collisions with Balanced Trees
    locator: Summary and Description
  - paper: doi:10.1002/(SICI)1097-024X(19990410)29:4<341::AID-SPE237>3.0.CO;2-R
    title: M. Douglas McIlroy, A killer adversary for quicksort, Software, Practice and Experience 29(4), 1999
    locator: pp. 341 to 344
---

An algorithmic complexity attack is a denial of service attack that sends a program inputs on which its data structures hit their worst case instead of their average case. The classic target is a [hash table](/hash-table/): if the attacker can choose keys that all have the same hash value, each insert and each search walks one long chain, so $n$ inserts cost $\Theta(n^2)$ time in place of $\Theta(n)$. A small request, such as one HTTP POST with tens of thousands of form fields, can then keep a server busy for minutes. The defense is to make the hash values unknown to the attacker, with a secret random seed and a [keyed hash function](/siphash/), or to bound the worst case of each bucket.

## In plain words

A hash table is fast because the keys spread over many buckets, so each bucket holds only a few keys. This is true for normal data. It is not true for data that an enemy picks. If the enemy knows the hash function, the enemy can make many keys that all go to the same bucket. Then the table is one long list, and each new key must be compared with all the keys that came before it. The work grows with the square of the number of keys, so a small input can stop a server.

The same idea works against other algorithms that are fast on average but slow on rare inputs, such as quicksort. The fix is to stop the enemy from knowing what is slow. The program makes a secret random choice when it starts, so the enemy cannot plan the bad input.

## The idea

A data structure has a worst case cost and an average cost. The average is often over random input, or over a random choice made by the structure. An algorithmic complexity attack exists when three facts are true:

1. The average and the worst case differ by a large factor. For a hash table with [separate chaining](/separate-chaining/), a search costs $O(1 + \alpha)$ on average but $\Theta(n)$ when all $n$ keys share one bucket.
2. The attacker controls the input, for example the field names of a web form, the keys of a JSON object, or the addresses in network packets.
3. The attacker can predict which inputs are slow. For a hash table, this means that the attacker can compute the [hash function](/hash-function/), or at least find many keys that [collide](/hash-collision/) under it, without access to the running program.

If all $n$ keys go to one chain, the $i$-th insert compares its key with the $i - 1$ keys before it, to check that it is new. The total number of key comparisons is

$$0 + 1 + \cdots + (n - 1) = \frac{n(n - 1)}{2}.$$

The attacker pays $\Theta(n)$ to send the keys, and the server pays $\Theta(n^2)$. This gap is the gain of the attack. Open addressing does not help: keys with equal hash values follow the same probe sequence, so the $i$-th insert again tests $i - 1$ cells.

The defenses attack one of the three facts.

- **Remove fact 3 with a secret.** The program draws a random seed at start and uses a hash function $h_s$ that depends on it. If $h_s$ is drawn from a [universal family](/universal-hashing/), then each fixed pair of distinct keys collides with probability at most $1/m$ over the choice of $s$, so keys that the attacker chose without knowing $s$ act like random keys. This argument needs the seed to stay secret: an attacker who can see hash values or iteration order may learn it. A [pseudorandom function](/pseudorandom-function/) such as [SipHash](/siphash/) is built so that outputs do not reveal the key.
- **Remove fact 1 with a better worst case.** Each bucket can hold a [balanced search tree](/red-black-tree/) instead of a list when it grows long. Then a bucket with $n$ keys costs $O(\log n)$ per search, and the attack gains only a factor of $\log n$.
- **Remove fact 2 with limits.** The program caps the number of fields, keys or parameters that one request can create. This bounds $n$, and so bounds the damage, but it does not fix the table.

## Examples

**Java strings.** The method `String.hashCode` of Java computes $s[0] \cdot 31^{L-1} + s[1] \cdot 31^{L-2} + \cdots + s[L-1]$ modulo $2^{32}$, with no seed. The strings `Aa` and `BB` collide: $65 \cdot 31 + 97 = 66 \cdot 31 + 66 = 2112$. Because the hash of a concatenation depends only on the hash and the length of each part, every string made of $k$ blocks, each block `Aa` or `BB`, has the same hash. For $k = 3$, the 8 strings `AaAaAa`, `AaAaBB`, ..., `BBBBBB` all hash to 1952508096. For $k = 16$, there are $2^{16} = 65536$ strings of 32 characters with one hash value. Inserting them into a chained table costs $65536 \cdot 65535 / 2 = 2147450880$ key comparisons, against about 65536 for keys that spread well. This is the family of keys that Klink and Wälde used in 2011 against web frameworks in Java and other languages.

**Python integers.** CPython hashes an integer $x$ to $x \bmod (2^{61} - 1)$ on 64-bit machines, with the sign kept, and it adds no seed to integers; the random seed covers only strings, bytes and a few other types. So the keys $0, M, 2M, 3M, \ldots$ with $M = 2^{61} - 1$ all have hash 0. A program that builds a `dict` from 1000 such keys does 499500 equality tests, which is $1000 \cdot 999 / 2$. Also $\text{hash}(-1) = \text{hash}(-2) = -2$, because CPython uses $-1$ as an error code.

**Perl, Squid and Bro, 2003.** Crosby and Wallach showed the attack on the hash tables of Perl, of the Squid web cache and of the Bro intrusion detection system. Against Bro, a stream of packets with chosen addresses made the program slow down until it dropped packets, so the attack also blinded the monitor.

**Other worst cases.** The same pattern works for other algorithms with a gap between average and worst case.

- A [quicksort](/quicksort/) with a fixed pivot rule takes $\Theta(n^2)$ time on some inputs. McIlroy's adversary builds such an input for a large class of quicksort codes by watching the comparisons that the sort makes.
- A [backtracking regular expression](/backtracking-regex-matching/) engine can take exponential time on a short string. For the pattern `(a+)+$` and a string of $n$ letters `a` and then one `b`, the engine can try all $2^{n-1}$ ways to split the run of `a` into groups before it fails. This is [ReDoS](/redos/).
- In programming contests, [anti-hash tests](/anti-hash-tests/) are inputs built to make a fixed string hash or a fixed integer hash collide.

## Where it is used

- **Language runtimes.** After the 2011 advisory, PHP, Ruby, Python and Java web servers added fixes. Python 2.7.3 and 3.2.3 added an opt-in random seed for string hashes, and Python 3.3 made it the default. Python 3.4 replaced the string hash by [SipHash](/siphash/) (PEP 456), because the seeded hash of 3.3 let an attacker recover the seed. Rust's standard `HashMap` uses a randomly seeded SipHash by default. Java 8 kept `String.hashCode` without a seed, since its formula is part of the API specification, and instead turned long buckets of `HashMap` into balanced trees, which help most when the keys are comparable (JEP 180).
- **Choice of hash function.** A fast non-cryptographic hash with a seed is not enough. PEP 456 records that MurmurHash3 and CityHash have collision families that do not depend on the seed, found by Aumasson, Bernstein and Boßlet. A keyed pseudorandom function closes this gap at a small cost in speed.
- **Input limits.** PHP added a cap on the number of input variables of a request. Parsers for JSON, XML and HTTP headers often bound the number of keys for the same reason.
- **Design of data structures.** The attack is a reason to prefer structures whose guarantees hold for every input, or whose random choices are made by the structure and hidden from the user: [universal hashing](/universal-hashing/), [cuckoo hashing](/cuckoo-hashing/) with random functions, [randomized quicksort](/randomized-quicksort/) or [introsort](/introsort/). [Worst case analysis](/worst-case-analysis/) is the right model when the input may come from an enemy.

## References
