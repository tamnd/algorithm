---
tag: 6713FR
kind: concept
slug: permutation-cycles
name: Cycle decomposition of a permutation
aliases:
- cycle notation
- cycles of a permutation
area: sequences/inversions-and-permutations
level: intro
summary: Every permutation factors uniquely into disjoint cycles.
prereqs: [permutation]
see_also: [permutation-inverse, permutation-parity, cayley-distance, cycle-leader-permutation, permutation-power, stirling-numbers-first-kind, symmetric-group, functional-graph]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3 (applications to permutations, cycle notation, products of cycles and the canonical cycle form)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.3 (cycles and inversions, the cycle type and the Stirling numbers of the first kind)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 6.1 (Stirling numbers of the first kind as the number of permutations with k cycles)
---

The cycle decomposition writes a [permutation](/permutation/) as a product of disjoint cycles: follow $i \to \pi(i) \to \pi(\pi(i)) \to \cdots$ from any item until it comes back, and the items visited form one cycle. Every permutation of a finite set has exactly one such decomposition, up to the order of the cycles and the starting item of each cycle. The cycles give the [order](/permutation-power/) of a permutation, its [parity](/permutation-parity/), the [Cayley distance](/cayley-distance/) to the identity, and the way to [apply a permutation in place](/cycle-leader-permutation/). One pass with a visited mark finds all of them in $\Theta(n)$ time.

## In plain words

Think of a party game. Each guest holds a card with the name of another guest, and no two cards name the same guest. Start with one guest, walk to the guest named on their card, then to the guest named on that card, and so on. You can never get stuck and you never meet a guest twice before you are back at the start. So you walk in a closed loop.

Mark the guests of that loop and start again from a guest who is not marked. Each guest is in exactly one loop. The loops are the cycles of the permutation. A guest whose card names themselves is a loop of length one. Writing the loops down is a short and complete description of the whole arrangement.

## The idea

**Cycles.** Let $\pi$ be a permutation of $[n]$. A *$k$-cycle* $(a_1\ a_2\ \cdots\ a_k)$, for distinct $a_1, \ldots, a_k$, is the permutation that maps $a_1 \mapsto a_2 \mapsto \cdots \mapsto a_k \mapsto a_1$ and fixes every other item. The same cycle can be written starting at any of its $k$ items. A 1-cycle is the identity, and a 2-cycle $(a\ b)$ is a *transposition*. Two cycles are *disjoint* when they share no item. Disjoint cycles commute, because each one moves only items that the other fixes.

**Theorem.** Every permutation $\pi$ of $[n]$ is a product of disjoint cycles whose items together are all of $[n]$ (fixed points count as 1-cycles). The set of these cycles is unique.

*Proof of existence.* Fix $i$ and look at $i, \pi(i), \pi^2(i), \ldots$. The values lie in a finite set, so some value repeats. Let $b$ be the least index such that $\pi^b(i) = \pi^a(i)$ for some $a < b$. If $a \ge 1$, then $\pi(\pi^{a-1}(i)) = \pi(\pi^{b-1}(i))$, and since $\pi$ is injective, $\pi^{a-1}(i) = \pi^{b-1}(i)$, which contradicts the choice of $b$. So $a = 0$: the walk returns to $i$ first, after $k = b$ steps, and $i, \pi(i), \ldots, \pi^{k-1}(i)$ are distinct. This set is the *orbit* of $i$. Two orbits that share an item $j$ are equal, because each one is the set of items reached from $j$ by the walk. So the orbits split $[n]$. On its orbit, $\pi$ acts as the cycle $(i\ \pi(i)\ \cdots\ \pi^{k-1}(i))$, and each item is in exactly one orbit, so $\pi$ is the product of these cycles.

*Proof of uniqueness.* Take any product of disjoint cycles that equals $\pi$, and let $C$ be the cycle of the product that contains $i$. The other cycles fix $i$ and all items of $C$, so $\pi(i)$ is the successor of $i$ in $C$, $\pi^2(i)$ the next one, and so on. So $C$ is the cycle of the orbit of $i$. $\square$

**Canonical form.** To make the written form unique, write each cycle starting with its smallest item and list the cycles by increasing first item. Stanley's *standard representation* uses another rule: each cycle starts with its largest item, and the cycles are listed in increasing order of these items. In that form the parentheses can be dropped and recovered, because a new cycle starts exactly at each item that is larger than all items before it. This gives a bijection of $S_n$ onto itself, the *fundamental bijection*, that turns $c$ cycles into $c$ left-to-right maxima.

**Finding the cycles.** One pass suffices.

```pseudo
CYCLES(π[1 .. n])
1  seen[1 .. n] ← false, result ← empty list
2  for i ← 1 to n do
3      if not seen[i] then
4          C ← empty list, j ← i
5          while not seen[j] do
6              seen[j] ← true, append j to C, j ← π[j]
7          append C to result
8  return result
```

Each item is marked once and visited by line 6 once, so the time is $\Theta(n)$ and the extra space is $n$ bits. With the values used as array indices this is a [word RAM](/word-ram/) algorithm, not a comparison algorithm.

**What the cycles determine.**

- **Cycle type.** The multiset of cycle lengths, a partition of $n$. Two permutations are conjugate in the [symmetric group](/symmetric-group/), $\sigma = \rho\pi\rho^{-1}$ for some $\rho$, exactly when they have the same cycle type.
- **Order.** A $k$-cycle returns to the identity after exactly $k$ applications. So the least $t \ge 1$ with $\pi^t = \iota$ is the [least common multiple](/least-common-multiple/) of the cycle lengths. See [applying a permutation $k$ times](/permutation-power/).
- **Transpositions.** A $k$-cycle is a product of $k - 1$ transpositions: $(a_1\ a_2\ \cdots\ a_k) = (a_1\ a_k)(a_1\ a_{k-1}) \cdots (a_1\ a_2)$, applied from the right. So $\pi$ with $c$ cycles is a product of $n - c$ transpositions, and no fewer: this is the [Cayley distance](/cayley-distance/) from $\pi$ to the identity. The [parity](/permutation-parity/) of $\pi$ is the parity of $n - c$.
- **Inverse.** The inverse has the same cycles, each written in reverse: $(a_1\ a_2\ \cdots\ a_k)^{-1} = (a_k\ \cdots\ a_2\ a_1)$. See [inverse permutation](/permutation-inverse/).

**Counting.** The number of permutations of $[n]$ with exactly $c$ cycles is the unsigned [Stirling number of the first kind](/stirling-numbers-first-kind/) ${n \brack c}$, with $\sum_c {n \brack c} x^c = x(x+1)\cdots(x+n-1)$. For a uniform random permutation:

- the expected number of cycles is the harmonic number $H_n = 1 + \frac12 + \cdots + \frac1n$;
- the cycle that contains a given item has length $\ell$ with probability exactly $1/n$, for each $\ell = 1, \ldots, n$;
- the expected number of fixed points is 1.

*Proof of the second fact.* The permutations in which item 1 lies in a cycle of length $\ell$ are built by choosing the other $\ell - 1$ items of the cycle in order, in $(n-1)(n-2)\cdots(n-\ell+1)$ ways, and any permutation of the remaining $n - \ell$ items, in $(n - \ell)!$ ways. The product is $(n-1)!$, the same for each $\ell$, so the probability is $(n-1)!/n! = 1/n$. $\square$ The first fact follows: the item $i$ lies in a cycle of length $\ell$, and that cycle contributes $1/\ell$ to the sum $\sum_i 1/(\text{length of the cycle of } i)$, which counts each cycle once. Its expectation is $n \cdot \sum_{\ell=1}^{n} \frac1n \cdot \frac1\ell = H_n$.

## Examples

**One permutation.** Let $\sigma = 2\,4\,1\,3\,6\,5$. From 1 the walk is $1 \to 2 \to 4 \to 3 \to 1$, and from 5 it is $5 \to 6 \to 5$. So

$$\sigma = (1\ 2\ 4\ 3)(5\ 6).$$

It has 2 cycles of lengths 4 and 2, so its cycle type is $(4, 2)$, its order is $\operatorname{lcm}(4, 2) = 4$, it is a product of $6 - 2 = 4$ transpositions, and it is even. Its powers are $\sigma^2 = 4\,3\,2\,1\,5\,6$, $\sigma^3 = 3\,1\,4\,2\,6\,5$ and $\sigma^4 = 1\,2\,3\,4\,5\,6$. In $\sigma^2$ the 4-cycle has split into the two 2-cycles $(1\ 4)(2\ 3)$, and the 2-cycle has become two fixed points.

**One long cycle.** $\pi = 3\,1\,4\,5\,2 = (1\ 3\ 4\ 5\ 2)$ is a single 5-cycle. Its order is 5.

**The cycle counts for $n = 4$.** Of the 24 permutations, 6 have one cycle, 11 have two, 6 have three and 1 has four. These are ${4 \brack 1}, \ldots, {4 \brack 4}$, and the mean is $(6 + 22 + 18 + 4)/24 = 25/12 = H_4$. In each of the 24, item 1 lies in a cycle of length 1, 2, 3 or 4, and each length occurs in exactly 6 permutations.

**Non-example.** The array $2\,2\,1$ is not a permutation, and the walk from 3 goes $3 \to 1 \to 2 \to 2 \to \cdots$, which never returns to 3. The uniqueness of the walk back needs a bijection. For a general function the walk ends in a cycle after a tail, which is the structure of a [functional graph](/functional-graph/).

## Where it is used

- **[Cycle-leader permutation](/cycle-leader-permutation/).** Rearranging an array by a permutation in place follows each cycle once and needs only one spare item.
- **[Cycle sort](/cycle-sort/).** It writes each item directly into its final place, one cycle at a time, which minimizes the number of writes.
- **[Parity](/permutation-parity/) and [Cayley distance](/cayley-distance/).** Both are $n$ minus the number of cycles, or its parity, and both take $O(n)$ time from the cycles.
- **[Powers of a permutation](/permutation-power/).** $\pi^k$ maps each item $k$ steps along its cycle, so all powers can be computed in $O(n)$ time from the cycles.
- **Random permutations.** The number of cycles of a uniform permutation has the same distribution as the number of records, which is the [hiring problem](/hiring-problem/).
- **Group theory.** Conjugacy classes of the [symmetric group](/symmetric-group/) are the cycle types.
- **[Succinct permutations](/succinct-permutation/).** A data structure for $\pi$ and $\pi^{-1}$ stores shortcuts along each cycle.

## References
