---
tag: DWJN7Q
kind: problem
slug: shuffling-a-linked-list
name: Shuffling a linked list
aliases:
- linked list shuffle
- random permutation of a linked list
area: randomized/shuffling
level: intro
summary: Relink the nodes of a linked list into a uniformly random order, without random access. Linear time with an array of pointers; Θ(n log n) time with O(log n) extra space by splitting or merging.
prereqs: [linked-list, random-permutation]
see_also: [merge-shuffle, fisher-yates-shuffle, singly-linked-list, merge-sort, permute-by-sorting, sort-based-shuffle, binomial-distribution, quicksort]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm P (the array shuffle used by the first method)
  - paper: "Axel Bacher, Olivier Bodini, Alexandros Hollender and Jérémie Lumbroso, MergeShuffle, a very fast, parallel random permutation algorithm, arXiv:1508.03167, 2015"
    locator: Section 1 (the splitting methods of Rao and Sandelius) and Section 2 (the merge with fair coins)
  - paper: "C. Radhakrishna Rao, Generation of random permutations of given number of elements using random sampling numbers, Sankhya Series A 23, 1961"
    locator: pp. 305 to 307 (splitting by random digits)
  - paper: "Martin Sandelius, A simple randomization procedure, Journal of the Royal Statistical Society Series B 24, 1962"
    locator: pp. 472 to 481
---

Shuffling a linked list asks for the [random permutation](/random-permutation/) problem on a [linked list](/linked-list/): relink the $n$ nodes so that each of the $n!$ orders has probability $1/n!$. A list has no random access, so the [Fisher-Yates shuffle](/fisher-yates-shuffle/) cannot run on it directly. There are three standard answers: copy the node pointers into an array and shuffle the array, in $\Theta(n)$ time and $\Theta(n)$ extra words; split the list by random bits and recurse; or split it in halves, shuffle them, and merge with coins whose weights are the sizes of the parts. The last two take $\Theta(n \log n)$ time and $O(\log n)$ extra words. A merge with *fair* coins, the obvious idea, is biased.

## In plain words

Imagine a chain of paper clips, where you can only get to a clip by going along the chain from the start. You want to put the clips in a random order, with every order equally likely. You cannot jump to a clip in the middle, so the usual shuffle does not fit.

One way is to lay the clips out in a row, shuffle the row, and chain them again. That needs room for the row. Another way is to throw each clip on a left or right pile by a coin toss, shuffle each pile the same way, and join the piles. A third way is to cut the chain in two, shuffle both halves, and then merge them, picking the next clip from a half with a chance that matches how many clips that half still has. Picking with a plain coin toss is not fair.

## Definition

**Input.** A singly or doubly [linked list](/singly-linked-list/) of $n$ nodes. The algorithm may read and change the "next" fields and may keep a few pointers. A source of randomness, in one of the models of the [random permutation](/random-permutation/) page.

**Output.** The same nodes, relinked, in an order $\sigma$ with $\Pr[\sigma = \tau] = 1/n!$ for each order $\tau$. Usually the nodes must be relinked and not copied, because other code holds pointers to them, and the payloads may be large.

**Cost measures.** Time, the number of extra words of memory (beyond the list), and the number of random bits.

## Variants

- **Immutable lists.** In a purely functional language the list cannot be changed in place, and the output is a new list. The splitting and merging methods are the natural ones there, since they read lists from the front.
- **Doubly linked lists.** The same methods apply; the "prev" fields are fixed in one pass at the end.
- **Streams.** If the list is too long to hold, the problem becomes a shuffle in external memory; see [external permuting](/external-permuting/).

## Examples

**Fair coins in a merge are biased.** Split $[0, 1, 2]$ into $[0]$ and $[1, 2]$, shuffle the halves, and merge by fair coins until one half is empty, then append the rest. Exact enumeration of the coins gives

| output | $[0,1,2]$ | $[0,2,1]$ | $[1,0,2]$ | $[1,2,0]$ | $[2,0,1]$ | $[2,1,0]$ |
|---|---|---|---|---|---|---|
| fair coins | $1/4$ | $1/4$ | $1/8$ | $1/8$ | $1/8$ | $1/8$ |
| size-weighted coins | $1/6$ | $1/6$ | $1/6$ | $1/6$ | $1/6$ | $1/6$ |

With fair coins, item 0 comes first with probability $1/2$ instead of $1/3$. With weights, the first coin takes the left item with probability $1/3$, and if it does not, the second coin takes it with probability $1/2$; so item 0 is at each of the three positions with probability $1/3$. Any procedure with only fair coins and a bounded number of them is biased for $n \ge 3$, by the argument of the [sort-based shuffle](/sort-based-shuffle/) page.

## Known algorithms

| method | time | extra words | randomness | exact |
|---|---|---|---|---|
| array of pointers, Fisher-Yates, relink | $\Theta(n)$ | $\Theta(n)$ | $n - 1$ uniform integers | yes |
| split by random bits, recurse, concatenate | $\Theta(n \log n)$ expected | $O(\log n)$ expected | about $n \log_2 n$ fair bits | yes |
| split in halves, recurse, merge with weighted coins | $\Theta(n \log n)$ | $O(\log n)$ | $\Theta(n \log n)$ coins with rational weights | yes |
| attach random keys, sort the list by merge sort | $\Theta(n \log n)$ | a key per node | $n$ keys | yes, with distinct keys |
| merge with fair coins, append the rest | $\Theta(n \log n)$ | $O(\log n)$ | fair bits | **no** |

- **Array of pointers.** Walk the list, store the node pointers in an array, run [Fisher-Yates](/fisher-yates-shuffle/) on the array, and relink the nodes in array order. This is the simplest and fastest method when $n$ extra words are available.
- **Split by random bits.** Send each node to list 0 or list 1 by a fair bit, shuffle both lists recursively, and concatenate them; stop at lists with at most one node. This is the method of Rao and Sandelius. It is exact because it sorts the nodes by infinite random binary keys, whose bits are drawn only as far as needed: the keys are distinct with probability 1, and distinct i.i.d. keys give a uniform order (see [permute by sorting](/permute-by-sorting/)). The recursion is that of a random binary trie, of expected depth $O(\log n)$.
- **Merge with weighted coins.** Cut the list into halves (by counting, or by sending nodes alternately to two lists), shuffle both recursively, and merge: while the halves have $\ell > 0$ and $r > 0$ nodes left, take the head of the left half with probability $\ell / (\ell + r)$. Each interleaving of the two halves then has probability
$$\prod_{\text{steps}} \frac{\text{nodes left in the chosen half}}{\text{nodes left in both}} = \frac{n_1! \, n_2!}{n!} = \binom{n}{n_1}^{-1},$$
because the numerators run through $n_1, n_1 - 1, \ldots, 1$ and $n_2, \ldots, 1$ in some order, and the denominators through $n, n-1, \ldots, 1$ (once one half is empty, each step has the factor $r/r = 1$). A uniform interleaving of two independent uniform orders is a uniform order. This is the list form of the inverse of the riffle in the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/).
- **MergeShuffle on a list.** The merge of [MergeShuffle](/merge-shuffle/) uses fair coins and then inserts about $\sqrt n$ leftover items at uniform positions. On an array this is cheap; on a list each insertion walks up to $n$ nodes, so the weighted merge is the better choice for lists.

## Bounds

- **Time.** $\Omega(n)$, since every link may change. The array method meets it with $\Theta(n)$ extra words.
- **Random bits.** At least $\log_2 n!$ fair bits on average for an exact method, as for arrays. The splitting method uses $n \log_2 n + O(n)$ bits on average, close to this bound.
- **With few extra words.** With $O(\log n)$ extra words, the standard exact methods above take $\Theta(n \log n)$ time. This page states no lower bound for that setting.

## Reductions

- **To the array problem** in $\Theta(n)$ time and $\Theta(n)$ space, by the array of pointers.
- **From the array problem.** An array can be viewed as a list, so a list shuffle also shuffles an array; the converse direction is the one that needs care.
- **To sorting.** With random keys, a list shuffle is a list sort; merge sort is the usual list sort, so the cost is that of [merge sort](/merge-sort/) on a list.

## Applications

- Shuffling a playlist, a deck or a queue stored as a list, without copying the payloads.
- Random orders in functional programs, where lists are the basic structure.
- Randomizing the order of a free list or of a hash chain, for example to make the input of a [randomized algorithm](/randomized-algorithm/) random.

## References
