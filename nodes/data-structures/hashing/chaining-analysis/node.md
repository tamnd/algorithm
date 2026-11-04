---
tag: 2VHRB4
kind: theorem
slug: chaining-analysis
name: Analysis of separate chaining
aliases:
- expected chain length theorem
area: data-structures/hashing
level: intro
summary: Under uniform hashing, expected successful and unsuccessful search take O(1 + alpha) time.
prereqs: [separate-chaining, simple-uniform-hashing, linearity-of-expectation, indicator-random-variable]
see_also: [hash-table, load-factor, chaining-expected-search-time, universal-hashing-expected-chain-length, balls-into-bins-max-load, linear-probing-analysis, uniform-hashing-assumption]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.2 (Hash tables), the analysis of hashing with chaining (the two theorems on unsuccessful and successful search)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the analysis of separate chaining
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), the proposition on the lengths of the lists in separate chaining
---

The analysis of [separate chaining](/separate-chaining/) gives the expected cost of a search in a chained [hash table](/hash-table/) with $n$ keys and $m$ slots, under [simple uniform hashing](/simple-uniform-hashing/). A search for an absent key examines $\alpha = n/m$ keys on average, and a search for a stored key examines $1 + \alpha/2 - \alpha/(2n)$ keys on average, where $\alpha$ is the [load factor](/load-factor/). So both kinds of search take $\Theta(1 + \alpha)$ expected time, and $O(1)$ when the table keeps $n = O(m)$. This is the result behind the claim that a hash table gives constant expected time per operation.

## Statement

Let a chained hash table have $m \ge 1$ slots, and let $n \ge 1$ distinct keys $x_1, x_2, \ldots, x_n$ be inserted in this order. Each insert puts the new key at the head of the list of its slot, so the list of a slot holds its keys from the latest inserted to the earliest. Assume **simple uniform hashing**: the slots $h(x_1), \ldots, h(x_n)$, and the slot $h(k)$ of each searched key $k$ that is not stored, are independent random variables, each uniform on $\{0, 1, \ldots, m-1\}$. Let $\alpha = n/m$. A search for key $k$ scans the list of slot $h(k)$ from the head and compares $k$ with each key until it finds $k$ or reaches the end. Count the keys it compares with.

**Theorem.**

1. **(Unsuccessful search.)** For a key $k$ that is not stored, the expected number of keys examined is exactly $\alpha$.
2. **(Successful search.)** For a key chosen uniformly at random from $x_1, \ldots, x_n$, independent of the hash values, the expected number of keys examined is exactly
$$1 + \frac{\alpha}{2} - \frac{\alpha}{2n}.$$

With $\Theta(1)$ time to compute $h(k)$ and $\Theta(1)$ time for each comparison, both searches take $\Theta(1 + \alpha)$ expected time on the [word RAM](/word-ram/).

## In plain words

Throw the keys into the slots at random. On average each slot gets the number of keys divided by the number of slots. A search for a key that is not there looks at all the keys of one slot, so it looks at this average number of keys.

A search for a key that is there stops at that key. It looks at the key itself and at the keys that came into the same slot after it, because new keys go to the front. An early key has many later keys that can land in front of it, and a late key has few. On average, a key has about half of the others after it, so the search looks at about one key plus half the average slot size.

## Proof

**Part 1.** For $j = 1, \ldots, n$, let $X_j$ be the [indicator random variable](/indicator-random-variable/) of the event $h(x_j) = h(k)$. The search scans the whole list of slot $h(k)$, because $k$ is not in it, so the number of keys examined is the length of that list, which is $\sum_{j=1}^{n} X_j$. Since $h(k)$ and $h(x_j)$ are independent and uniform,
$$\Pr[h(x_j) = h(k)] = \sum_{s=0}^{m-1} \Pr[h(k) = s] \Pr[h(x_j) = s] = m \cdot \frac{1}{m^2} = \frac{1}{m}.$$
So $E[X_j] = 1/m$. By [linearity of expectation](/linearity-of-expectation/), the expected number examined is $\sum_{j=1}^{n} 1/m = n/m = \alpha$. $\square$

**Part 2.** Fix $i$, and let the searched key be $x_i$. The keys in the list of slot $h(x_i)$ that come before $x_i$ are exactly the keys $x_j$ with $j > i$ and $h(x_j) = h(x_i)$, because the list holds its keys from the latest inserted to the earliest. The search compares $x_i$ with each of them and then with $x_i$ itself. For $j \ne i$, let $X_{ij}$ be the indicator of $h(x_j) = h(x_i)$. As in Part 1, $E[X_{ij}] = 1/m$, since $h(x_i)$ and $h(x_j)$ are independent and uniform. So the number examined is $1 + \sum_{j = i+1}^{n} X_{ij}$.

The searched key is $x_i$ with probability $1/n$ for each $i$, independent of the hash values. By the law of total expectation and linearity,
$$E[\text{examined}] = \frac{1}{n} \sum_{i=1}^{n} \Bigl(1 + \sum_{j=i+1}^{n} \frac{1}{m}\Bigr) = 1 + \frac{1}{nm} \sum_{i=1}^{n} (n - i).$$
The sum is $\sum_{i=1}^{n} (n - i) = 0 + 1 + \cdots + (n - 1) = n(n-1)/2$. Hence
$$E[\text{examined}] = 1 + \frac{n - 1}{2m} = 1 + \frac{\alpha}{2} - \frac{\alpha}{2n}. \qquad \square$$

**Time.** A search costs $\Theta(1)$ for the hash and the access to the slot, plus $\Theta(1)$ for each key examined. By Part 1 the expected time of an unsuccessful search is $\Theta(1) + \Theta(\alpha) = \Theta(1 + \alpha)$. By Part 2 the expected number examined in a successful search lies between $1 + \alpha/4$ (since $n \ge 2$ gives $\alpha/(2n) \le \alpha/4$, and for $n = 1$ the value is 1) and $1 + \alpha/2$, so its expected time is also $\Theta(1 + \alpha)$. $\blacksquare$

## Consequences

- **Constant expected time.** If the table keeps $n \le c\,m$ for a constant $c$, for example by [rehashing](/rehashing/) into a table of twice the size when the [load factor](/load-factor/) passes $c$, then $\alpha \le c$ and each search, insert and delete takes $O(1)$ expected time. This is the bound of the [hash table](/hash-table/) page.
- **Insert and delete.** An insert at the head of a list costs $O(1)$ after the search for a duplicate key, which is an unsuccessful search. A delete costs a successful search, or $O(1)$ with a doubly linked list and a pointer to the item.
- **Universal hashing.** The same proof works when $h$ is drawn from a [universal family](/universal-hash-family/): only $\Pr[h(x) = h(y)] \le 1/m$ is used, so the equalities become the upper bounds $\alpha$ and $1 + \alpha/2$, and they hold for each fixed set of keys. See [universal hashing and the expected chain length](/universal-hashing-expected-chain-length/).
- **Comparison with open addressing.** Under the [uniform hashing assumption](/uniform-hashing-assumption/), an unsuccessful search in [open addressing](/open-addressing/) makes at most $1/(1 - \alpha)$ probes, which grows without bound as $\alpha \to 1$. Chaining has no such limit: its cost grows linearly in $\alpha$, and $\alpha$ may exceed 1.
- The searching page [expected search time with chaining](/chaining-expected-search-time/) states the same result for the search problem.

## Tightness

Both parts are equalities, so the constants cannot improve under the hypotheses. For $n = 6$ keys in $m = 4$ slots, the average over all $4^6 = 4096$ equally likely hash assignments is exactly $3/2 = \alpha$ keys for an unsuccessful search, and exactly $13/8 = 1 + 0.75 - 0.125$ keys for a successful search.

The bounds are on the expectation only. In the worst case all $n$ keys hash to the same slot, and a search examines $n$ keys, so the worst case is $\Theta(n)$. An adversary who knows $h$ can always build such a set of keys, which is why the theorem needs random hash values that do not depend on the keys. Even under simple uniform hashing, the longest list is longer than the average: with $n = m$, it has $\Theta(\log n / \log \log n)$ keys with high probability, by the [balls-into-bins bound](/balls-into-bins-max-load/).

## History

Knuth analyzes separate chaining in Section 6.4 of Volume 3, with the average number of probes for successful and unsuccessful search. CLRS Section 11.2 gives the two results above, with the same proof by indicator variables, and Sedgewick and Wayne Section 3.4 give a related bound that the length of each list is close to $n/m$ with high probability.

## References
