---
tag: R7NP9W
kind: abstract-type
slug: bag
name: Bag
area: data-structures/linear-structures
level: intro
summary: A collection that supports adding items and iterating over them, where the order of items does not matter and removal is not supported.
prereqs: [list]
see_also: [stack, queue, linked-list, dynamic-array, adjacency-list, randomized-queue, hash-table, list]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), the Bag API, the Stats client, and Algorithm 1.4 (Bag, a linked-list implementation); Section 4.1, the Graph class with an array of bags as adjacency lists
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, the definition of the word multiset and of the operations on multisets
---

A bag is the abstract type of a collection to which a program can add items and over which it can iterate, but from which it cannot remove items. The order of the iteration is not part of the type: a client may only rely on seeing each added item exactly once, so two bags with the same items, added in any order, are the same bag. Because the type promises so little, every implementation can make `add` cost $O(1)$, with a [linked list](/linked-list/) or a [dynamic array](/dynamic-array/). The bag is the collection of a client that only gathers items to process them all later, such as the samples of a statistic or the neighbours of a vertex in an [adjacency list](/adjacency-list/).

## In plain words

A bag is like a cloth bag of marbles. You can drop marbles in, and you can tip the bag out and look at every marble. You cannot ask for the marble you put in first or last, and you cannot take one marble out and put the rest back.

That sounds weak, but many programs need nothing more. To find the average of a list of numbers, you collect them and then go through all of them. To store the roads leaving each town, you collect them and later look at each one. Since the bag makes no promise about order, the computer can store the items in whatever way is quickest.

## Operations

The state of a bag over a set $T$ is a finite multiset $B$ of items: a set in which an item may occur more than once.

| operation | signature | result |
|---|---|---|
| new | $() \to B$ | the empty multiset $\varnothing$ |
| add | $(B, x) \to B$ | $B \uplus \{x\}$ |
| is_empty | $(B) \to \text{bool}$ | $\lvert B \rvert = 0$ |
| size | $(B) \to \mathbb{N}$ | $\lvert B \rvert$ |
| iterate | $(B) \to$ a sequence over $T$ | a sequence that contains each item of $B$ as often as it occurs in $B$ |

Here $\uplus$ is the multiset sum, which adds one to the number of copies of $x$. Iteration does not change the bag. It returns some order of the items, and two iterations of the same bag may return different orders.

## Laws

For each bag $B$ and items $x$, $y$:

$$\begin{aligned}
&(\text{B1})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{add}(B, x)) = \text{size}(B) + 1,\\
&(\text{B2})\quad \text{add}(\text{add}(B, x), y) = \text{add}(\text{add}(B, y), x),\\
&(\text{B3})\quad \text{iterate}(\text{new}()) \text{ is empty}, \qquad \text{iterate}(\text{add}(B, x)) \text{ is a permutation of } \text{iterate}(B) \text{ followed by } x,\\
&(\text{B4})\quad \text{is\_empty}(B) \iff \text{size}(B) = 0.
\end{aligned}$$

Law (B2) is what separates a bag from a [stack](/stack/) or a [queue](/queue/): the order of the adds cannot be seen. Law (B3) fixes the contents of each iteration but leaves the order open. A client that is correct for every order allowed by (B3) is correct for every implementation.

**Every count is right.** For each item $y$, the number of times $y$ appears in $\text{iterate}(B)$ equals the number of calls $\text{add}(\cdot, y)$ that built $B$.

*Proof.* By induction on the number of adds. For $\text{new}()$ both are 0 by (B3). For $\text{add}(B, x)$, by (B3) the iteration is a permutation of $\text{iterate}(B)$ with $x$ appended, so the count of $y$ is the count in $\text{iterate}(B)$, plus one if $y = x$. The number of adds of $y$ changes in the same way. $\square$

**What a bag is not.** A bag has no remove and no membership test. A collection that adds and removes items with no order promised is a [randomized queue](/randomized-queue/) when the removed item is uniform at random, or a multiset in a [hash table](/hash-table/) when items are removed by value.

## Implementations

| implementation | add | iterate | space |
|---|---|---|---|
| [singly linked list](/singly-linked-list/), add at the front | $O(1)$ worst case | $\Theta(n)$ | $n$ nodes of 2 fields |
| [dynamic array](/dynamic-array/), add at the back | $O(1)$ amortized | $\Theta(n)$ | $< 4n$ cells, or $< 2n$ without shrinking |
| fixed [array](/array/) of capacity $N$ | $O(1)$ worst case, fails when full | $\Theta(n)$ | $N$ cells |
| [hash table](/hash-table/) from items to counts | $O(1)$ expected | $\Theta(n + d)$, $d$ distinct items | $\Theta(d)$ |

Sedgewick and Wayne's Bag (Algorithm 1.4) is the [stack](/stack/) on a linked list with pop removed: add pushes at the front, so the iteration returns the items in the reverse order of the adds. That order is one of the orders (B3) allows; a client must not depend on it. The table of counts saves space when items repeat often, and it is the only form here that can answer "how many copies of $x$" in $O(1)$ expected time.

Sedgewick and Wayne store the edges of a graph as an array of bags, one per vertex, which is the [adjacency list](/adjacency-list/). Adding an edge is then $O(1)$, and the graph algorithms only iterate over the neighbours of a vertex.

## References
