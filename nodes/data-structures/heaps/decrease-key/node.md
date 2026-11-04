---
tag: GQYXYK
kind: concept
slug: decrease-key
name: Decrease-key
aliases:
- decrease key operation
area: data-structures/heaps
level: intro
summary: Operation that lowers the key of an element already in the queue, central to Dijkstra and Prim.
prereqs: [priority-queue, heap, binary-heap]
see_also: [heap-increase-key, indexed-priority-queue, fibonacci-heap, dijkstra, prim, lazy-deletion, handle, pairing-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues), HEAP-INCREASE-KEY and the handles of a priority queue; Chapter 22 (Single-Source Shortest Paths), Section 22.3 (Dijkstra's algorithm)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 19.3 (Decreasing a key and deleting a node)
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Section 1 (the heap operations) and Section 4 (shortest paths and minimum spanning trees)
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 6.2 (Addressable priority queues)
---

Decrease-key is the operation DECREASE-KEY$(Q, x, k)$ of a min-[priority queue](/priority-queue/) $Q$: it lowers the key of the item $x$, which is already in $Q$, to a new key $k \le \mathrm{key}(x)$. It is the main operation of [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/), which lower the tentative distance of a vertex each time they find a better edge into it. A graph with $n$ vertices and $m$ edges can cause up to $m$ decrease-keys but only $n$ extract-mins, so the cost of decrease-key decides the running time on dense graphs. The mirror operation of a max-priority queue is [heap increase-key](/heap-increase-key/).

## In plain words

A waiting list orders people by a number, and the smallest number goes first. Sometimes a person gets a better number while they wait. Decrease-key moves that person forward in the list to the place that matches the new number.

To do this, the list must be able to find the person at once. Searching the whole list is slow, so the list gives each person a ticket when they join, and the ticket points to their place. With a ticket, a simple heap moves the person up in a few steps. Some heaps only cut the person loose and put them at the top level, which is even faster.

## The idea

**The operation.** For a min-queue $Q$ that holds items with keys from a [total order](/total-order/), DECREASE-KEY$(Q, x, k)$ requires $k \le \mathrm{key}(x)$, and afterwards $Q$ holds the same items with $\mathrm{key}(x) = k$. A larger $k$ is an error, because the heaps below repair the order only in one direction. The operation is not defined for an item that is not in $Q$.

**Handles.** A heap cannot find an item by its key: the [heap property](/heap-property/) gives no order between two subtrees, so a search takes $\Theta(n)$ time. So the caller names $x$ by a [handle](/handle/): a pointer to the node of the item in a pointer-based heap, or an item index together with a position map in an array heap, as in the [indexed priority queue](/indexed-priority-queue/). A queue that offers decrease-key with handles is called an *addressable* priority queue. In an array heap the items move at each swap, so the position map must be updated at each swap.

**How heaps implement it.** In each heap-ordered tree, a smaller key at $x$ can only break the edge from $x$ to its parent, because the edges from $x$ to its children stay ordered. There are two ways to repair that edge.

1. *Move up.* Exchange $x$ with its parent while it is smaller. This is the [sift-up](/sift-up/) of the [binary heap](/binary-heap/), and it costs the depth of $x$, $O(\log n)$ in a binary, $d$-ary or [binomial heap](/binomial-heap/).
2. *Cut.* Remove the subtree of $x$ from its parent and make $x$ a new root. The cut costs $O(1)$, but the trees lose their shape, and the heap must later keep the number of trees and the degrees small. The [Fibonacci heap](/fibonacci-heap/) does this with marks and cascading cuts, for $O(1)$ amortized time. The [pairing heap](/pairing-heap/) cuts and later melds the subtree back in.

| heap | decrease-key | extract-min |
|---|---|---|
| [binary heap](/binary-heap/) | $O(\log n)$ | $O(\log n)$ |
| [d-ary heap](/d-ary-heap/) | $O(\log_d n)$ | $O(d \log_d n)$ |
| [binomial heap](/binomial-heap/) | $O(\log n)$ | $O(\log n)$ |
| [Fibonacci heap](/fibonacci-heap/) | $O(1)$ amortized | $O(\log n)$ amortized |
| [hollow heap](/hollow-heap/) | $O(1)$ amortized | $O(\log n)$ amortized |
| [Brodal queue](/brodal-queue/) | $O(1)$ | $O(\log n)$ |
| [bucket queue](/bucket-queue/), integer keys at most $C$ | $O(1)$ | $O(1)$ each plus $O(C)$ in total, when the extracted keys never decrease |

**Without decrease-key.** A queue with no handles can simulate decrease-key by *lazy deletion*: insert $x$ again with the new key and leave the old entry. When extract-min returns an entry whose key is not the current key of its item, or whose item was already taken out, skip it. The queue then holds up to one entry per decrease, so in Dijkstra's algorithm it holds up to $m$ entries, and the time is $O(m \log m) = O(m \log n)$ with a binary heap, the same as with decrease-key. The cost is the extra space. See [lazy deletion](/lazy-deletion/).

**Why $O(1)$ matters.** Dijkstra's algorithm and Prim's algorithm make $n$ inserts, $n$ extract-mins and at most $m$ decrease-keys. With a binary heap the time is $O((n + m) \log n)$. With a Fibonacci heap it is $O(m + n \log n)$, which is $O(n^2)$ on a dense graph with $m = \Theta(n^2)$, against $O(n^2 \log n)$. Fredman and Tarjan designed the Fibonacci heap for this reason.

**Delete from decrease-key.** In a heap, DELETE$(Q, x)$ is DECREASE-KEY$(Q, x, -\infty)$ followed by EXTRACT-MIN. So a heap with fast decrease-key and extract-min also has a fast delete. The page [heap delete](/heap-delete/) gives the direct method for the array heap.

## Examples

- **Binary heap.** The min-heap $[1, 3, 2, 5, 9, 8]$ (1-based) has 9 at index 5. DECREASE-KEY at index 5 to 0 writes 0, then swaps it with its parent 3 at index 2, then with the root 1. The result is $[0, 1, 2, 5, 3, 8]$, after 2 swaps.
- **Fibonacci heap.** In the heap with the one tree $17(24\ 18(38)\ 21(23\ 39(41)))$, decreasing 41 to 15 cuts 41 from 39 and makes 15 a new root, with one cut. The [Fibonacci heap](/fibonacci-heap/) page goes on with two more decreases and a cascading cut.
- **Dijkstra's algorithm.** From the source $s$ with the edges $s \to a$ of length 4, $s \to b$ of length 1 and $b \to a$ of length 2, the queue holds $a$ with key 4 and $b$ with key 1 after $s$ is taken out. Extracting $b$ finds the path $s, b, a$ of length 3, and DECREASE-KEY$(Q, a, 3)$ lowers the key of $a$ from 4 to 3.
- **Non-example, an increase.** DECREASE-KEY$(Q, x, k)$ with $k > \mathrm{key}(x)$ is an error. In a binary min-heap, a larger key must sift down instead, which a general `change-key` operation does.

## Where it is used

- Shortest paths: [Dijkstra's algorithm](/dijkstra/), [uniform-cost search](/uniform-cost-search/) and [A* search](/a-star-search/), when they keep one entry per vertex.
- Minimum spanning trees: [Prim's algorithm](/prim/).
- [Best-first search](/best-first-search/) and branch and bound with a bound that improves.
- Event simulation, when an event moves to an earlier time.
- [Dial's algorithm](/dial-algorithm/) uses a [bucket queue](/bucket-queue/), where decrease-key moves an item to a lower bucket in $O(1)$ time.

## References
