---
tag: YV0EEV
kind: problem
slug: sorting-network-verification
name: Sorting network verification
aliases:
- testing a sorting network
- NONSORT
area: sorting/sorting-networks
level: advanced
summary: Decide whether a given comparator network sorts all inputs, by checking 0-1 inputs.
prereqs: [sorting-network, zero-one-principle, co-np-complete]
see_also: [minimum-size-sorting-network, minimum-depth-sorting-network, one-in-three-sat, bit-parallelism, merging-network, green-filter]
sources:
  - paper: doi:10.1016/0022-0000(89)90017-2
    title: M. J. Chung and B. Ravikumar, Strong nondeterministic Turing reduction, a technique for proving intractability, Journal of Computer and System Sciences 39(1) (1989)
    locator: pp. 2 to 20 (the verification problem is co-NP-complete)
  - paper: doi:10.1007/BFb0035109
    title: Ian Parberry, On the computational complexity of optimal sorting network verification, PARLE 91, Lecture Notes in Computer Science (1991)
    locator: Section 1 (history), Section 4 (the reduction from one-in-three 3SAT), Theorem 6.1 (single exception networks) and Theorem 7.1 (depth D(n) + 4 lg n + 7)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting, Theorem Z (the zero-one principle)
---

Sorting network verification is the problem of deciding whether a given network of [comparators](/comparator/) on $n$ wires sorts every input. By the [zero-one principle](/zero-one-principle/) it is enough to test the $2^n - n - 1$ unsorted inputs of zeros and ones, which gives an algorithm of time $O(s \, 2^n)$ for a network of size $s$. No algorithm polynomial in $n$ and $s$ is likely to exist: the problem is [co-NP-complete](/co-np-complete/) (Chung and Ravikumar, 1989), and it stays co-NP-complete for networks only $4 \lg n + O(1)$ layers deeper than optimal (Parberry, 1991).

## In plain words

Someone gives you a fixed plan of comparisons and says that it sorts. To check this, you can feed it every list of zeros and ones and look at the results. A wrong plan shows its fault on at least one such list. The trouble is that there are $2^n$ lists.

It is very likely that no fast method exists. A network can be built that sorts every list of zeros and ones except one, and finding this one list is as hard as solving a hard logic puzzle.

## Definition

**Input.** A number $n$ of wires and a comparator network $N$, given as a list of $s$ comparators $[i{:}j]$ with $0 \le i < j < n$.

**Question.** Does $N$ sort each input $x \in X^n$, for each totally ordered set $X$?

By the zero-one principle the question is equivalent to: does $N$ sort each $x \in \{0, 1\}^n$? The complement, called NONSORT, asks whether some input is not sorted. NONSORT is in [NP](/np/): a certificate is an input $x \in \{0, 1\}^n$, and running $N$ on $x$ takes $O(s + n)$ time. So verification is in co-NP.

## Variants

- **Depth-restricted networks.** The input network has depth at most $D(n) + f(n)$, where $D(n)$ is the minimum depth of a sorting network on $n$ wires. This asks whether short networks, the ones worth building, are easier to verify.
- **Merging networks.** Decide whether a network merges two sorted sequences of lengths $p$ and $q$. The same principle reduces this to the $(p + 1)(q + 1)$ pairs of sorted 0-1 sequences, so it takes polynomial time. See [merging network](/merging-network/).
- **Selection networks.** Decide whether a network puts the $t$ smallest items on its first $t$ wires. The same principle applies, and the test is that on each 0-1 input with $z$ zeros, the first $t$ outputs hold $\min(z, t)$ zeros.
- **Partial inputs.** Decide whether the network sorts each input of a given set, such as the outputs of a known prefix. Search methods for [minimum-size](/minimum-size-sorting-network/) and [minimum-depth](/minimum-depth-sorting-network/) networks solve this form many times.

## Examples

- **A network that fails.** The network $[0{:}1], [1{:}2]$ on 3 wires moves the largest item to wire 2 but does not order the first two wires. On the 4 unsorted 0-1 inputs $010, 100, 101, 110$ it gives $001, 001, 011, 101$, so the input $110$ shows that it does not sort.
- **A network that sorts.** The network $[0{:}1], [1{:}2], [0{:}1]$ gives $001, 001, 011, 011$ on the same 4 inputs, so it sorts.
- **Four wires.** The network $[0{:}1], [2{:}3], [0{:}2], [1{:}3]$ puts the minimum on wire 0 and the maximum on wire 3, but it fails on the 4 inputs $0101, 0110, 1001, 1010$, which all give $0101$. Adding $[1{:}2]$ gives a sorting network.

## Known algorithms

**All 0-1 inputs, one bit per input.** Store for each wire a word with $2^n$ bits, one for each input. A comparator on wires $i$ and $j$ replaces the two words by their bitwise AND and OR. At the end, the network sorts if and only if no bit is 1 on a wire and 0 on the next wire. With [bit-parallelism](/bit-parallelism/) on words of $w$ bits, this takes $O(s \, 2^n / w)$ word operations.

```python
def sorts(n: int, network: list[tuple[int, int]]) -> bool:
    """Return True if the comparator network sorts every 0-1 input on n wires."""
    m = 1 << n
    wires = []
    for i in range(n):
        h = 1 << i  # bit k of wire i is bit i of k: blocks of h zeros, then h ones
        block = ((1 << h) - 1) << h
        wires.append(block * (((1 << m) - 1) // ((1 << (2 * h)) - 1)))
    for i, j in network:
        wires[i], wires[j] = wires[i] & wires[j], wires[i] | wires[j]
    return all(wires[i] & ~wires[i + 1] == 0 for i in range(n - 1))
```

Python integers of any size act as long words here, so this checks a network on 16 wires, with $2^{16}$ inputs, in a few milliseconds. The multiplication repeats the block of $2h$ bits $m / 2h$ times.

**Only the outputs of a prefix.** The network sorts each input if and only if its suffix sorts each output of its prefix. So compute the set $S$ of 0-1 outputs of the first layers, and test only the elements of $S$. If the first layer is $[0{:}1], [2{:}3], \ldots$, each pair of wires holds $00$, $01$ or $11$ after it, so only $3^{\lfloor n/2 \rfloor} 2^{n \bmod 2}$ inputs are left, about $1.73^n$ instead of $2^n$.

**Special structure.** A network built from components with known behavior, such as Batcher's merges, is verified by a proof for the construction. For a merging network, $(p + 1)(q + 1)$ tests are enough.

## Bounds

**Upper bound.** $O(s \, 2^n)$ time for a network of size $s$, by the zero-one principle, and $O(s \, 3^{n/2})$ when the first layer is a perfect matching of the wires.

**The test set can not be smaller.** For each unsorted $x \in \{0, 1\}^n$, there is a comparator network that sorts each 0-1 input except $x$: a *single exception sorting network*. Chung and Ravikumar gave a recursive construction of polynomial size and depth. Parberry gave one of depth at most $D(n - 1) + 2 \lceil \lg n \rceil - 1$ (Theorem 6.1). So a test that uses only 0-1 inputs and must work for all networks has to use all $2^n - n - 1$ unsorted ones.

**Hardness.** Verification is co-NP-complete (Chung and Ravikumar, 1989). Parberry showed that NONSORT stays NP-complete for networks on $n$ wires of depth $D(n) + 4 \lg n + 7$ (Theorem 7.1). So unless P = NP, even networks close to the optimal depth can not be verified in time polynomial in their size.

## Reductions

**From one-in-three 3SAT.** Parberry's proof reduces a form of [one-in-three 3SAT](/one-in-three-sat/), in which each variable appears in exactly three clauses, to NONSORT. For $n$ clauses the network has $5n$ wires.

- Each variable has a *variable component* on 5 wires, with 6 comparators and depth 3. When its first and last outputs are equal, all 5 outputs are equal, so the three middle outputs are three copies of one truth value.
- Each clause has a *clause component*, a sorting network on 3 wires, which outputs $001$ exactly when one of its three inputs is 1.
- A final *selector* sorts each input except those whose pattern comes from a satisfying assignment. It is built from a single exception sorting network.

The network sorts each input if and only if the formula has no satisfying assignment. So NONSORT is NP-hard, and with NONSORT $\in$ NP it is NP-complete.

**To the size and depth problems.** A search for a [minimum-size](/minimum-size-sorting-network/) or [minimum-depth](/minimum-depth-sorting-network/) network must reject each candidate that does not sort, so it solves verification on each candidate. This is why such searches keep the set of 0-1 outputs of each prefix instead of the network itself.

## Applications

- **Checking published networks.** Each network in a table of the best known networks, such as [Green's network](/green-filter/) for 16 inputs, can be checked in a fraction of a second with the bit-parallel test.
- **Testing implementations.** A sorting kernel built from a fixed network can be tested on all $2^n$ 0-1 inputs, which covers each possible fault of the comparator list.
- **Hardware.** A sorter circuit with a wrong or missing comparator is detected by the same test set, and the single exception networks show that no smaller set of 0-1 tests is safe.

## References
