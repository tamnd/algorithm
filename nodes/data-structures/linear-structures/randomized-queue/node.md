---
tag: SA6VBM
kind: abstract-type
slug: randomized-queue
name: Randomized queue
area: data-structures/linear-structures
level: intro
summary: A queue whose dequeue operation removes and returns an item chosen uniformly at random from those stored.
prereqs: [queue, bag]
see_also: [fisher-yates-shuffle, reservoir-sampling, dynamic-array, steque, deque]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), Exercise 1.3.35 (Random queue) and Exercise 1.3.34 (Random bag)
  - url: https://coursera.cs.princeton.edu/algs4/assignments/queues/specification.php
    title: Robert Sedgewick and Kevin Wayne, Princeton COS 226 programming assignment Deques and Randomized Queues
    locator: the RandomizedQueue API, its performance requirements and the independent iterators
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 3.4.2 (Random sampling and shuffling), Algorithm P (Shuffling)
  - paper: Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in Algorithms and Complexity, New Directions and Recent Results, Academic Press (1976)
    locator: the lower bound of the entropy on the expected number of random bits
---

A randomized queue is an abstract data type that holds a collection of items and whose `dequeue` removes and returns an item chosen uniformly at random from the items it holds, with a fresh random choice at each call. It also has `enqueue`, which adds an item, and often `sample`, which returns a random item without removing it. Despite the name, it keeps no order at all: it is a [bag](/bag/) with random removal, and draining it lists the items in a uniformly random order. A [dynamic array](/dynamic-array/) with the swap-with-last trick gives each operation in $\Theta(1)$ amortized time.

## In plain words

Think of raffle tickets in a hat. Anyone may drop a ticket into the hat at any time. To pick a winner, you shake the hat and pull out one ticket without looking, so each ticket in the hat has the same chance. The ticket you pulled is gone, so it cannot win again. You may also peek at a random ticket and put it back.

A randomized queue works the same way. The order in which the items went in does not matter. If you take all the items out one by one, you get them in a shuffled order, and each shuffle is equally likely. This makes it a handy tool for random sampling, for shuffling, and for tests that must try items in a random order.

## Operations

A randomized queue over a set $T$ of items is a value $R$. Its state is a finite multiset $M$ of items of $T$, with $k = |M|$ counting copies. When two equal items are stored, they count as two different *occurrences*.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to R$ | the empty collection |
| `enqueue` | $\text{enqueue}(R, x) \to R$ | $M$ becomes $M + \{x\}$ |
| `dequeue` | $\text{dequeue}(R) \to (x, R)$ | for $k \ge 1$: chooses an occurrence $y$ of $M$ with probability $1/k$, returns it, and $M$ becomes $M - \{y\}$ |
| `sample` | $\text{sample}(R) \to x$ | for $k \ge 1$: returns an occurrence chosen with probability $1/k$, and does not change $M$ |
| `is_empty`, `size` | $R \to \text{bool}$, $R \to \mathbb{N}$ | test $k = 0$; return $k$ |
| `iterator` | $R \to$ a sequence | the occurrences of $M$ in a uniformly random order; two iterators choose their orders independently |

`dequeue` and `sample` on an empty collection are errors. Each call makes its random choice independently of the earlier calls, given the current state.

### Example

The table follows the array implementation below. Each dequeue picks a random index $r$; the run shows one possible choice of the values of $r$.

| step | operation | random index $r$ | result | array after |
|---|---|---|---|---|
| 1 to 4 | enqueue a, b, c, d | | | [a, b, c, d] |
| 5 | dequeue | 1 | b | [a, d, c] |
| 6 | sample | 2 | c | [a, d, c] |
| 7 | enqueue e | | | [a, d, c, e] |
| 8 | dequeue | 0 | a | [e, d, c] |
| 9 | dequeue | 2 | c | [e, d] |
| 10 | dequeue | 1 | d | [e] |
| 11 | dequeue | 0 | e | [ ] |

At step 5, each of the four items had probability $1/4$ to come out. At step 8, each of the four stored items had probability $1/4$, whatever happened before.

## Laws

The laws of a randomized queue are statements about probabilities. Let $M$ be the state before a call, with $k = |M| \ge 1$, and let $\mathcal{H}$ be any event about the past calls and their results.

$$\begin{aligned}
&(\text{R1})\quad \Pr[\text{dequeue returns the occurrence } y \mid \mathcal{H}] = 1/k \text{ for each occurrence } y \in M, \text{ and then the state is } M - \{y\},\\
&(\text{R2})\quad \Pr[\text{sample returns the occurrence } y \mid \mathcal{H}] = 1/k, \text{ and the state stays } M,\\
&(\text{R3})\quad \text{enqueue}(R, x) \text{ makes the state } M + \{x\}, \qquad \text{size} = |M|, \qquad \text{is\_empty} \iff |M| = 0.
\end{aligned}$$

**Draining gives a uniform permutation.** If the collection holds $n$ occurrences and $n$ dequeues follow with no enqueue, then each of the $n!$ orders of the occurrences comes out with probability exactly $1/n!$.

*Proof.* Fix an order $y_1, \dots, y_n$. By (R1), the first dequeue returns $y_1$ with probability $1/n$. Given that, the state holds $n - 1$ occurrences, and the second dequeue returns $y_2$ with probability $1/(n-1)$, whatever the first result was. Going on in the same way, the probability of the order is $\frac{1}{n} \cdot \frac{1}{n-1} \cdots \frac{1}{1} = \frac{1}{n!}$. $\square$

So a randomized queue shuffles: enqueue the items, then dequeue them all. With the array implementation below this is the [Fisher and Yates shuffle](/fisher-yates-shuffle/), done one step per dequeue.

**Survival.** If the collection holds $k$ occurrences and $j \le k$ dequeues follow with no enqueue, a fixed occurrence $y$ is still present with probability

$$\prod_{i=0}^{j-1}\left(1 - \frac{1}{k - i}\right) = \prod_{i=0}^{j-1}\frac{k - i - 1}{k - i} = \frac{k - j}{k},$$

since the product telescopes. For example, after 3 dequeues from 4 items, each item survives with probability $1/4$.

**No order law.** The result of a dequeue does not depend on the order of the earlier enqueues, only on the current multiset. So, unlike the [queue](/queue/) and the [stack](/stack/), no equation such as $\text{dequeue}(\text{enqueue}(R, x)) = \dots$ fixes the result; two implementations agree only in distribution.

## Implementations

| implementation | enqueue | dequeue and sample | iterator | space |
|---|---|---|---|---|
| [dynamic array](/dynamic-array/), swap with the last item | $\Theta(1)$ amortized | $\Theta(1)$ amortized, $\Theta(1)$ for sample | $\Theta(n)$ to start, then $\Theta(1)$ per item | $\Theta(n)$ |
| [singly linked list](/singly-linked-list/) | $\Theta(1)$ | $\Theta(n)$ worst case, to walk to a random node | $\Theta(n)$ to start | $\Theta(n)$ |

The bounds assume that a uniform random integer in $\{0, \dots, k-1\}$ costs $O(1)$ time. The array version keeps the items in $A[0 \ldots k-1]$:

```pseudo id=main
DEQUEUE(A, k)                              ▷ k ≥ 1 items in A[0 .. k − 1]
L1  r ← a uniform random integer in {0, …, k − 1}
L2  x ← A[r]
L3  A[r] ← A[k − 1]
L4  k ← k − 1                              ▷ shrink the array when it is one quarter full
L5  return x
```

Line L1 gives each stored occurrence probability $1/k$, which is law (R1). Lines L3 and L4 fill the hole with the last item, so the stored items stay in $A[0 \ldots k-1]$ with no gap. The order inside the array changes, but no law depends on it. Enqueue appends at $A[k]$, and sample returns $A[r]$ for a random $r$. An iterator copies the array and shuffles the copy by Knuth's Algorithm P, so that two iterators are independent. The resizing rule (double when full, halve at one quarter) is the one of the [stack](/stack/) page.

## Lower bounds

A program that uses fair random bits needs at least $\lg(n!) = n \lg n - \Theta(n)$ random bits in expectation to drain $n$ distinct items. The output is a uniform permutation, so its entropy is $\lg(n!)$, and the expected number of fair bits that any procedure uses to produce a random output is at least the entropy of the output (Knuth and Yao, 1976). For $n = 52$ this is about 225.6 bits. The array implementation draws one random integer per dequeue, so it is within a constant factor of this bound when it draws each integer with $O(\log k)$ expected bits.

## References
