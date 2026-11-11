---
tag: 0S8S0R
kind: data-structure
slug: bitonic-counting-network
name: Bitonic counting network
aliases:
- Bitonic[w]
area: concurrency/lock-free-structures
level: advanced
summary: Counting network of width 2^k built from bitonic merge structure, with depth Θ(log² w).
complexity:
  vars: {w: "the width, a power of 2", n: "the number of tokens that have entered"}
  space: {extra: "Θ(w log^2 w)"}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [counting-network, bitonic-sort]
see_also: [bitonic-merger, bitonic-sequence, zero-one-principle, odd-even-merge-sort, diffracting-tree, quiescent-consistency, fetch-and-add, wait-freedom]
sources:
  - paper: doi:10.1145/185675.185815
    title: James Aspnes, Maurice Herlihy and Nir Shavit, Counting networks, Journal of the ACM 41(5), 1994, pages 1020 to 1048
    locator: the definitions of Bitonic[w] and Merger[w] by even and odd subsequences, the proof that Merger[2k] keeps the step property, the depth bound, and the isomorphism with Batcher's bitonic sorter
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32, 1968
    locator: pages 307 to 314, the bitonic sorter, whose shape the bitonic counting network shares
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.5 (Counting Networks), the Bitonic and Merger classes and the proof that the bitonic network counts
  - paper: doi:10.1007/s004460050019
    title: Maurice Herlihy, Nir Shavit and Orli Waarts, Linearizable counting networks, Distributed Computing 9(4), 1996, pages 193 to 203
    locator: counting networks such as the bitonic network are not linearizable, and what it costs to make them so
---

The bitonic counting network is the first [counting network](/counting-network/) of Aspnes, Herlihy and Shavit (1991, journal version 1994). It is built like Batcher's [bitonic sorter](/bitonic-sort/), with a *balancer* in place of each comparator. Bitonic$[2k]$ is two copies of Bitonic$[k]$ side by side, followed by a merging network Merger$[2k]$; Merger$[2k]$ is two copies of Merger$[k]$ on interleaved halves of its inputs, followed by one layer of balancers. With width $w = 2^m$ the depth is $m(m+1)/2 = \Theta(\log^2 w)$. In every quiescent state its outputs have the step property, so a small counter on each output turns it into a shared counter that hands out $0, 1, 2, \ldots$ with no gap. The counter is [wait-free](/wait-freedom/) and [quiescently consistent](/quiescent-consistency/), but not [linearizable](/linearizability/). This page proves that the network counts; the general theory, the counter built on top and the periodic network are on the [counting network](/counting-network/) page.

## In plain words

Think of a tournament for sorting people into lines, but where each match is not won by the stronger player. Instead, each meeting point sends the people who arrive there to the left, then the right, then the left again, in turn.

Split the doors into two halves and build a small network for each half, so that each half sends people to its exits in a fair, even way. Then add a stage that mixes the two halves: it pairs the exits of one half with the exits of the other in a careful crisscross pattern, and one last row of meeting points evens things out.

When nobody is inside, the exits have counts that differ by at most one, with the larger counts first. A small ticket roll at each exit then gives out every number once.

## The abstract type

Like every counting network, it provides getAndIncrement() on a shared counter, with values that are exactly $0, \ldots, n - 1$ in every quiescent state after $n$ calls. The counter is quiescently consistent and not linearizable; see the [counting network](/counting-network/) page for the definitions and the proof of these two facts from the step property.

## Representation

### Model and notation

Asynchronous shared memory; processes may stop at any time. Each balancer has a toggle bit with an atomic TOGGLE (read and flip); each output has a counter with an atomic fetch-and-add. The implementation uses a fetch-and-add on the balancer word and keeps only its low bit, which has the same effect.

| Symbol | Meaning |
|---|---|
| $w = 2^m$ | the width |
| $x_0, \ldots, x_{k-1}$ | counts of tokens on the wires of a sequence $x$ |
| $\Sigma x$ | $x_0 + \cdots + x_{k-1}$ |
| $x^{\mathrm{even}}, x^{\mathrm{odd}}$ | the subsequences $x_0, x_2, \ldots$ and $x_1, x_3, \ldots$ |
| step property | $0 \le y_i - y_j \le 1$ for all $i < j$ |
| $D(w)$ | the depth of Bitonic$[w]$ |

### Fields

- One toggle word per balancer, initially 0, and one counter word per output, initially 0.
- The shape: for each wire, its balancers in layer order, and the output order. A balancer joins two wires and its outputs are the same two wires (first, then second). So the outputs of the network are the $w$ wires in an order that the construction fixes: in Bitonic$[4]$ the outputs 0, 1, 2, 3 are the wires 0, 1, 3, 2.

**Invariant.** In a quiescent state, a balancer that has seen $t$ tokens has sent $\lceil t/2 \rceil$ to its first wire and $\lfloor t/2 \rfloor$ to its second, so all wire counts depend only on the input counts.

## Operations

```pseudo id=main
BITONIC(v)                                   ▷ v: a list of 2^m wires; returns the outputs in order
L1  if |v| = 1 then return v
L2  a ← BITONIC(first half of v); b ← BITONIC(second half of v)
L3  return MERGER(a, b)

MERGER(x, x')                                ▷ x, x': lists of k wires each
L4  if k = 1 then add a balancer on (x[0], x'[0]); return (x[0], x'[0])
L5  z ← MERGER(even(x), odd(x'))
L6  z' ← MERGER(odd(x), even(x'))
L7  for i ← 0 to k - 1 do add a balancer on (z[i], z'[i])
L8  return (z[0], z'[0], z[1], z'[1], ..., z[k-1], z'[k-1])

GET-AND-INCREMENT(i)                         ▷ a token that enters on input wire i
L9  x ← i; ℓ ← 0
L10 while some balancer b on wire x is in a layer after ℓ (take the first) do
L11     t ← TOGGLE(b)
L12     if t = 0 then x ← the first wire of b else x ← the second wire of b; ℓ ← layer(b)
L13 j ← the output index of wire x; k ← FETCH-AND-ADD(c[j], 1)
L14 return j + k·w
```

The two halves at L2 and at L5 and L6 work side by side on disjoint wires, so their layers line up. Every layer of the result is a perfect matching of the $w$ wires, so a token toggles exactly one balancer per layer.

**How it differs from the counting network page.** The [counting network](/counting-network/) page defines counting networks in general, proves that the step property gives a quiescently consistent counter, and presents the periodic network, which is $\log_2 w$ equal blocks and has depth $\log_2^2 w$. This page is about one network: it is shallower, $\frac{1}{2}\log_2 w(\log_2 w + 1)$, and its proof that it counts is short enough to give in full here. Its shape is not periodic: each merger is a different size.

### Memory reclamation

None is needed. The network is built before any token enters and is never changed; nothing is allocated or freed while it runs.

### Weak memory

All shared steps are read-modify-write steps on single words (the toggles and the output counters), and the steps on one word are totally ordered in C++ and similar models, so relaxed order is enough for the counting property. A caller that uses the value to order other data needs its own acquire and release order. This is our reading, not a claim of the paper.

## Example

Bitonic$[4]$ has 6 balancers. Layer 1: $(0,1)$, $(2,3)$, which are the two Bitonic$[2]$. Layers 2 and 3 are Merger$[4]$ on $x = (0, 1)$ and $x' = (2, 3)$: its two Merger$[2]$ are $(0, 3)$ (even of $x$, odd of $x'$) and $(1, 2)$ (odd of $x$, even of $x'$); its last layer is $(0, 1)$ and $(3, 2)$. The outputs in order are the wires $0, 1, 3, 2$.

Four tokens enter one after another, on wires 0, 0, 2, 0.

1. The first goes to the first wire of every balancer it meets: $(0,1)$, $(0,3)$, $(0,1)$. It leaves on wire 0, output 0, and gets 0.
2. The second finds $(0,1)$ flipped and goes to wire 1; then $(1,2)$ sends it to wire 1; then $(0,1)$ in layer 3 sends it to wire 1. Output 1, value 1.
3. The third enters on wire 2: $(2,3)$ sends it to wire 2; $(1,2)$ is flipped and sends it to wire 2; $(3,2)$ sends it to its first wire, wire 3, which is output 2. Value 2.
4. The fourth: $(0,1)$ to wire 0, $(0,3)$ flipped to wire 3, $(3,2)$ flipped to wire 2, output 3. Value 3.

The output counts after each token are $(1,0,0,0)$, $(1,1,0,0)$, $(1,1,1,0)$, $(1,1,1,1)$.

A run that is not linearizable: token $A$ enters on wire 0, passes its three balancers and stops before its fetch-and-add on output 0. Then process 1 runs four tokens one after another on wire 1. They get 1, 2 and 3, and the fourth leaves on output 0 and gets 0, before $A$ takes its value. Then $A$ gets 4. The fourth token started after the first returned 1, yet got 0.

## Correctness

Write $\mathrm{step}_k(s)$ for the sequence of length $k$ with the step property and sum $s$. It is unique: $\mathrm{step}_k(s)_i = \lceil (s - i)/k \rceil$. The full proofs are in [proofs/correctness.md](proofs/correctness.md); here is the core.

**Lemma 1.** If $x$ of even length $k$ has the step property, then $\Sigma x^{\mathrm{even}} = \lceil \Sigma x / 2 \rceil$ and $\Sigma x^{\mathrm{odd}} = \lfloor \Sigma x / 2 \rfloor$, and both subsequences have the step property.

*Proof.* Pair $x_{2i}$ with $x_{2i+1}$. By the step property each pair differs by 0 or 1, and at most one pair differs by 1 (the values drop by one at most once in the whole sequence). So $\Sigma x^{\mathrm{even}} - \Sigma x^{\mathrm{odd}} \in \{0, 1\}$, which gives the two sums. A subsequence of a step sequence keeps the condition $0 \le y_i - y_j \le 1$ for $i < j$. ∎

**Lemma 2.** If $z$ and $z'$ of length $k$ both have the step property and $|\Sigma z - \Sigma z'| \le 1$, then either $z = z'$, or they differ in exactly one position $j$, where the one with the larger sum is larger by 1, and $j = \min(\Sigma z, \Sigma z') \bmod k$.

*Proof.* From the formula for $\mathrm{step}_k(s)$: $\mathrm{step}_k(s+1)_i - \mathrm{step}_k(s)_i = 1$ exactly when $s + 1 - i \equiv 1 \pmod k$, that is $i \equiv s \pmod k$, and 0 otherwise. ∎

**Theorem 1 (the merger).** If $x$ and $x'$ of length $k$ (a power of 2) have the step property, then in a quiescent state the outputs of Merger$[2k]$ have the step property.

*Proof.* By induction on $k$. For $k = 1$ the merger is one balancer, and its outputs $\lceil t/2 \rceil, \lfloor t/2 \rfloor$ have the step property. Let $k \ge 2$. The first Merger$[k]$ gets $x^{\mathrm{even}}$ and $x'^{\mathrm{odd}}$, which have the step property by Lemma 1; by induction its output $z$ has the step property, and $\Sigma z = \lceil \Sigma x/2 \rceil + \lfloor \Sigma x'/2 \rfloor$. In the same way $z'$ has the step property and $\Sigma z' = \lfloor \Sigma x/2 \rfloor + \lceil \Sigma x'/2 \rceil$. So $|\Sigma z - \Sigma z'| \le 1$.

If $z = z'$, the last layer gives $y_{2i} = y_{2i+1} = z_i$, which has the step property because $z$ has it. Otherwise, by Lemma 2, let $u$ be the one of $z, z'$ with the smaller sum $s = qk + r$, $0 \le r < k$: then $u_i = q + 1$ for $i < r$ and $u_i = q$ for $i \ge r$, and the other sequence is $u$ with position $r$ raised by 1. Balancer $i \ne r$ of the last layer gets $2u_i$ tokens and sends $u_i$ to each output. Balancer $r$ gets $2q + 1$ and sends $q + 1$ to output $2r$ and $q$ to output $2r + 1$. So $y$ is $q + 1$ at outputs $0, \ldots, 2r$ and $q$ after: it has the step property. ∎

**Theorem 2.** Bitonic$[w]$ is a counting network for every $w = 2^m$.

*Proof.* By induction on $m$. Bitonic$[1]$ is a wire. For $w = 2k$, in a quiescent state each Bitonic$[k]$ is quiescent, so by induction its outputs have the step property, and Theorem 1 applies to the merger. ∎

The tests check Theorem 1 for $k = 1, 2, 4, 8$ and all sums below $4k$, check that the merger can fail when its inputs lack the step property ($x' = (0, 2)$ gives outputs $(1, 0, 1, 0)$), and check Theorem 2 for $w = 2, 4, 8$ on all input vectors with entries below 8, 5 and 3, and on random inputs up to $w = 64$. The token simulator runs tokens one balancer step at a time in random orders for $w = 2, 4, 8$ and compares the outputs with the counts from the inputs. The bad run: a merger that gives each half the even outputs of *both* inputs balances but does not count; for $w = 4$ and inputs $(0, 1, 0, 1)$ it gives $(1, 0, 1, 0)$, and the explorer finds a run with values 0 and 2.

*Progress.* A call does one toggle per layer and one fetch-and-add: exactly $D(w) + 1$ steps, with no waiting and no retry. The counter is wait-free; the tests stop other tokens at random points and check the count for $w$ up to 32.

## Complexity

| quantity | bound | status |
|---|---|---|
| depth of Merger$[2k]$ | $\log_2 (2k)$ | proved, and tested |
| depth $D(2^m)$ | $m(m+1)/2$ | proved, and tested up to $m = 6$ |
| balancers | $\frac{w}{2} \cdot \frac{m(m+1)}{2}$ | proved, and tested |
| steps per call | exactly $D(w) + 1$, wait-free | proved, and tested |
| space | $\Theta(w \log^2 w)$ words | |

The depth follows from $D(2k) = D(k) + \log_2(2k)$ with $D(1) = 0$: $D(2^m) = 1 + 2 + \cdots + m$.

Each balancer of a layer sees about $2/w$ of the tokens when they enter evenly on the inputs; this estimate is ours. So the load on a single word drops, at the price of $D(w) + 1$ steps per call instead of one.

## Variants

- **Periodic counting network.** Same counter, depth $\log_2^2 w$, built from $\log_2 w$ equal blocks; on the [counting network](/counting-network/) page.
- **Bitonic sorter.** Replace each balancer by a comparator that puts the larger value on the first wire and the result sorts. AHS prove that every counting network gives a sorting network this way; the tests check it here on all 0-1 inputs for $w \le 8$, which by the [0-1 principle](/zero-one-principle/) is enough.
- **Diffracting trees.** A [diffracting tree](/diffracting-tree/) uses a tree of balancers with prisms that let pairs of tokens pass each other without touching the toggle.
- **Smaller depth.** Klugerman and Plaxton (STOC 1992) gave counting networks of smaller depth than $\Theta(\log^2 w)$, with large constants.

## When to use it

Use it as a low-contention, wait-free counter when many threads take values at once and only quiescent consistency is needed, and when $w$ is near the number of threads that call at the same time. Prefer it to the periodic network when you want the smaller depth. Do not use it when a value must be larger than every value already returned (a ticket lock, a sequence number); use a single [fetch-and-add](/fetch-and-add/) word there.

## Pitfalls

- **Swapping the halves in the merger.** The first half merger must get the *even* outputs of $x$ and the *odd* outputs of $x'$. Even with even does not count; see the bad run.
- **Ignoring the output order.** The outputs come out as $z_0, z'_0, z_1, z'_1, \ldots$ of the last merger, which in a drawing with straight wires is a permutation of the wires. A counter on wire $j$ instead of output $j$ breaks the "no gaps" promise.
- **Expecting linearizability.** See the run in the example.
- **A non-atomic toggle.** Two tokens can then take the same wire, and the counts lose the step property.
- **Width not a power of 2.** The construction needs $w = 2^m$.

## Implementations

## History

Batcher described the bitonic sorter in 1968. Aspnes, Herlihy and Shavit introduced counting networks at STOC 1991 with the bitonic counting network as the first example and showed that it is a counting network of depth $O(\log^2 w)$; the journal version appeared in the Journal of the ACM in 1994, together with the periodic network. Herlihy, Shavit and Waarts then studied the gap between quiescent consistency and linearizability for such counters, and Klugerman and Plaxton reduced the depth in 1992.

## References
