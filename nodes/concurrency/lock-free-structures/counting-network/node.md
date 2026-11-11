---
tag: BHV1FX
kind: data-structure
slug: counting-network
name: Counting network
aliases:
- Aspnes-Herlihy-Shavit counting network
- balancer network
- AHS counting network
area: concurrency/lock-free-structures
level: research
summary: Network of balancers that distributes tokens so that concurrent counters are produced with low contention.
complexity:
  vars: {w: "the width, the number of input and output wires", d: "the depth, the number of layers of balancers", n: "the number of tokens that have entered"}
  space: {extra: "Θ(w d)"}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [quiescent-consistency, linearizability, sorting-network]
see_also: [bitonic-counting-network, diffracting-tree, combining-tree, sloppy-counter, fetch-and-add, bitonic-sort, flat-combining, wait-freedom]
sources:
  - paper: doi:10.1145/185675.185815
    title: James Aspnes, Maurice Herlihy and Nir Shavit, Counting networks, Journal of the ACM 41(5), 1994, pages 1020 to 1048
    locator: balancers, balancing networks, the step property, the definition of a counting network and of the counter built on it, the bitonic counting network, the periodic counting network built from Block networks, and the proof that a counting network is also a sorting network when its balancers are replaced by comparators (an earlier version is in STOC 1991)
  - paper: doi:10.1145/76359.76362
    title: Martin Dowd, Yehoshua Perl, Larry Rudolph and Michael Saks, The periodic balanced sorting network, Journal of the ACM 36(4), 1989, pages 738 to 757
    locator: the sorting network made of log n identical blocks, each block a layer that compares wire i with wire n - 1 - i followed by a block on each half; the periodic counting network has the same shape
  - paper: doi:10.1007/s004460050019
    title: Maurice Herlihy, Nir Shavit and Orli Waarts, Linearizable counting networks, Distributed Computing 9(4), 1996, pages 193 to 203
    locator: counting networks are quiescently consistent but not linearizable, and the cost of making a low-contention counter linearizable
  - paper: doi:10.1145/129712.129752
    title: Michael Klugerman and C. Greg Plaxton, Small-depth counting networks, STOC 1992, pages 417 to 428
    locator: counting networks of depth smaller than the log squared depth of the bitonic and periodic networks
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.5 (Counting Networks), with the balancer class, the bitonic and periodic networks and the discussion of throughput
---

A counting network is a shared counter made of many small parts, so that many threads can take numbers at once without all of them hitting one memory word. Its parts are *balancers*: a balancer has two input wires and two output wires, and it sends the tokens that reach it to its first output, then its second, then its first again, and so on. A balancing network joins balancers into layers on $w$ wires. Aspnes, Herlihy and Shavit (1991, journal version 1994) defined a *counting network* as a balancing network in which, whenever no token is inside, the output wires have the *step property*: the first outputs have each seen one more token than the last ones, or all have seen the same number. Put a small counter on each output, and the network hands out the numbers $0, 1, 2, \ldots$ with no gap and no repeat. The counter is [wait-free](/wait-freedom/) when each balancer is one atomic step, and it is [quiescently consistent](/quiescent-consistency/), but it is not [linearizable](/linearizability/). This page covers the general idea and the *periodic* network; the [bitonic counting network](/bitonic-counting-network/) has its own page, with its full proof.

## In plain words

Picture a hall with many doors at one end and many ticket desks at the other. Between them stand small gates. Each gate has two ways out, and it sends people out one way, then the other way, then the first way again. A person walks from a door through a fixed series of gates to one desk. Each desk has its own roll of numbers, and the rolls never share a number.

If the gates are set up in the right pattern, then each time the hall is empty, the numbers given out so far have no gaps and no repeats.

Many people can walk at once, and each gate sees only a few of them, so nobody waits long at one spot. The catch is that while people are still walking, a person who starts late can get a smaller number than a person who has already left.

## The abstract type

The object is a shared counter with one operation, getAndIncrement(), which returns a value. The guarantee is weaker than that of [fetch-and-add](/fetch-and-add/) on one word.

- In every quiescent state (no operation in progress) after $n$ operations have completed, the values returned are exactly $0, 1, \ldots, n - 1$.
- Hence the counter is quiescently consistent: operations separated by a period with no operation in progress take effect in their real-time order.
- Operations that overlap in time with no quiescent period between them can return values out of their real-time order. The counter is not linearizable (see the example).

## Representation

### Model and notation

Asynchronous shared memory; processes may stop at any time. A token is one call of getAndIncrement() by one process, and it enters on an input wire that the process chooses (often its own number mod $w$). Each balancer has a toggle bit, and the step TOGGLE(b) reads the bit and flips it in one atomic step (fetch-and-complement). Each output wire $j$ has a counter $c[j]$ with an atomic fetch-and-add. Real hardware has no fetch-and-complement on most machines; a fetch-and-add on a word whose low bit is the toggle, or a CAS loop, does the same job. The implementation uses the fetch-and-add form.

| Symbol | Meaning |
|---|---|
| $w$ | the width, a power of 2 |
| $x_i$ | the number of tokens that have entered on input $i$ |
| $y_j$ | the number of tokens that have left on output $j$ |
| $b.\mathit{top}$, $b.\mathit{bottom}$ | the two wires of balancer $b$: the first and the second output |
| $d$ | the depth, the number of layers |
| $c[j]$ | the counter of output $j$ |

A sequence $y_0, \ldots, y_{w-1}$ has the **step property** if $0 \le y_i - y_j \le 1$ for all $i < j$. Equivalently, $y_j = \lceil (m - j) / w \rceil$ where $m = \sum_j y_j$.

### Fields

- One toggle word per balancer, initially 0 (the next token goes to the top wire).
- One counter word per output wire, initially 0.
- The shape of the network: for each wire, the list of balancers on it in layer order, and the order of the output wires. The shape is fixed and is never written while the network runs.

**Invariant.** In a quiescent state, each balancer that has received $t$ tokens has sent $\lceil t/2 \rceil$ to its top wire and $\lfloor t/2 \rfloor$ to its bottom wire, whatever wires they came in on and in whatever order. A token that leaves on output $j$ as the $k$-th one there (counting from 0) gets $j + k w$.

## Operations

```pseudo id=main
GET-AND-INCREMENT(i)                         ▷ a token that enters on input wire i
L1  x ← i; ℓ ← 0
    loop
L2      b ← the first balancer on wire x in a layer after ℓ; if there is none, leave the loop
L3      t ← TOGGLE(b)                        ▷ atomic: return the bit and flip it
L4      if t = 0 then x ← b.top else x ← b.bottom; ℓ ← layer(b)
L5  j ← the output index of wire x
L6  k ← FETCH-AND-ADD(c[j], 1)
L7  return j + k·w

BLOCK(v)                                     ▷ build Block[n] on the list v of n wires
L8  if n = 2 then add a balancer on (v[0], v[1]); return
L9  for i ← 0 to n/2 - 1 do add a balancer on (v[i], v[n - 1 - i])
L10 BLOCK(v[0 .. n/2 - 1]); BLOCK(v[n/2 .. n - 1])

PERIODIC(w)                                  ▷ build the periodic network
L11 repeat log₂ w times: BLOCK(0 .. w - 1)
```

A token does one toggle in each layer and one fetch-and-add, $d + 1$ atomic steps in all, with no loop that depends on other tokens. It never waits and never retries.

The periodic network Periodic$[w]$ is $\log_2 w$ copies of Block$[w]$ in a row. The first layer of a block joins the wires that mirror each other (0 with $w - 1$, 1 with $w - 2$, and so on), and then each half gets a block of half the width. A block has $\log_2 w$ layers, so the network has depth $\log_2^2 w$ and $\frac{w}{2}\log_2^2 w$ balancers. This is the shape of the periodic balanced sorting network of Dowd, Perl, Rudolph and Saks, with balancers in place of comparators. One block alone does not count; the tests find inputs for which one Block$[4]$ or one Block$[8]$ breaks the step property.

**How it differs from the bitonic counting network.** Both are counting networks of depth $O(\log^2 w)$, and the counter on top of them is the same. The [bitonic network](/bitonic-counting-network/) is built by recursive merging and has depth $\frac{1}{2}\log_2 w(\log_2 w + 1)$, about half of the periodic depth $\log_2^2 w$. The periodic network is $\log_2 w$ copies of one block, which makes it easy to lay out and to reuse, but its proof is longer. This page gives the general theory and the periodic network; the bitonic page gives the bitonic construction and its full proof.

### Memory reclamation

None is needed. The network is built once, before any token enters, and nothing is allocated or freed while it runs. The only shared words are the toggles and the output counters, which live as long as the network.

### Weak memory

Each toggle and each output counter is a read-modify-write on one word, and in C++ and similar models all read-modify-write steps on one word are ordered, so a balancer still sends tokens out in turn with relaxed order. The step property in quiescent states needs only that. If the returned value is used to order other data, for example as an index into a shared array, the caller must add its own acquire and release order. This is our reading of the memory model, not a claim of the paper.

## Example

Take Periodic$[4]$. Its 8 balancers in layer order are $(0,3), (1,2)$; $(0,1), (2,3)$; $(0,3), (1,2)$; $(0,1), (2,3)$. Four tokens enter on wire 0 one after another.

1. The first finds every toggle at 0. It stays on wire 0 in all four layers and gets $0 + 0 \cdot 4 = 0$.
2. The second goes to wire 3 at the first balancer, then to wire 2, then to wire 1 at $(1,2)$ in layer 3, and stays on wire 1. It gets 1.
3. The third gets 2, and the fourth gets 3. The network is quiescent after each one, and the outputs are $(1,0,0,0)$, $(1,1,0,0)$, $(1,1,1,0)$, $(1,1,1,1)$: each has the step property.

Now a run that is not linearizable, on the network of width 2 (one balancer). Token $A$ of process 0 enters, toggles the balancer, and stops before it reads its counter; it will leave on output 0. Process 1 runs token $B$: it toggles to output 1 and returns $1 + 0 \cdot 2 = 1$. Then process 1 runs token $C$, which starts after $B$ has returned: it toggles to output 0, finds $c[0] = 0$, and returns 0. Then $A$ returns 2. $C$ started after $B$ ended but got a smaller value, so no sequential counter explains the run. There is no quiescent state between $B$ and $C$ ($A$ is inside), so the run is quiescently consistent, and at the end the values are $\{0, 1, 2\}$. The test `test_not_linearizable` replays it, and the explorer finds it by itself.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) is a sketch. It shows four things.

- *Counting from the step property (proved).* If a network's outputs have the step property in a quiescent state with $n$ tokens out, the values given out are exactly $0, \ldots, n - 1$. A token that starts after that state gets a value of at least $n$. Together these give quiescent consistency.
- *Balancers in a quiescent state (proved).* The output counts depend only on the input counts, not on the order of the tokens. So whether a network counts is a question about numbers: for every vector $x$, does the network's output vector have the step property?
- *The periodic network counts (cited).* Aspnes, Herlihy and Shavit prove it; their proof is longer than the one for the bitonic network and we do not repeat it. The tests check it for all inputs with $x_i < 6$ at $w = 2$, $x_i < 4$ at $w = 4$ and $x_i < 3$ at $w = 8$, and for 300 random inputs each at $w = 16$ and $w = 32$.
- *Not linearizable (proved by the example).* See the run above.

*Progress.* Every call ends after exactly $d + 1$ of its own steps, whatever the other processes do: the counter is wait-free. A process that stops inside the network does not block others, but it can keep the network from ever being quiescent again, so the "no gaps" promise is then only about the values given out so far: they are always distinct, because output $j$ gives only values $\equiv j \pmod w$ and its counter gives each $k$ once.

The tests check all interleavings of three small runs, each with three tokens, on networks of width 2 and 4, for quiescent consistency at every quiescent point. They also check 200 seeded runs on Periodic$[8]$ and Bitonic$[8]$ with up to 12 tokens, the run above, and a bug: with a toggle that is a read followed by a write, two tokens leave on the same output and the values are 0 and 2.

AHS also prove that if a balancing network counts, then the same network with comparators in place of balancers sorts. The converse is false: a sorting network need not count.

## Complexity

| quantity | bound | status |
|---|---|---|
| steps per call | exactly $d + 1$, wait-free | proved, and tested |
| depth of Periodic$[w]$ | $\log_2^2 w$ | proved (from the construction), and tested |
| balancers of Periodic$[w]$ | $\frac{w}{2}\log_2^2 w$ | proved, and tested |
| depth of Bitonic$[w]$ | $\frac{1}{2}\log_2 w(\log_2 w + 1)$ | proved on its page, and tested |
| depth $O(\log w)$ | possible in theory, with large constants | cited (Klugerman and Plaxton, 1992) |
| space | $\Theta(w d)$ words: one per balancer, plus $w$ counters | |

Each layer has $w/2$ balancers. When the tokens enter on all inputs evenly, each balancer sees about $2/w$ of the tokens, so the load on one word drops by a factor of about $w/2$ compared with one shared counter. That is the point of the design; this estimate is ours and ignores bursts. The price is latency: a call takes $d + 1$ steps on different words instead of one. A counting network pays off when $w$ is about the number of processes that call at the same time and the single counter is a hot spot; with few processes, the walk through the layers costs more than it saves.

## Variants

- **Bitonic counting network.** Same counter, a different network built from merging networks; see its [page](/bitonic-counting-network/).
- **Diffracting trees.** Shavit and Zemach replaced the layers by a binary tree of balancers, each with a "prism" in which pairs of tokens cancel and pass without touching the toggle; see [diffracting tree](/diffracting-tree/). It is also quiescently consistent.
- **Linearizable counting.** Herlihy, Shavit and Waarts studied networks that are linearizable, and showed that this costs either contention or extra waiting.
- **Smaller depth and other widths.** Klugerman and Plaxton gave networks of depth close to $O(\log w)$. Later work, for example Busch and Herlihy (SPAA 1999), built counting networks for widths that are not powers of 2.
- **Other combining counters.** A [combining tree](/combining-tree/) is linearizable but blocking; a [sloppy counter](/sloppy-counter/) is cheap but only approximate between flushes.

## When to use it

Use a counting network when many threads take numbers at the same time and need only unique values that fill a range once things calm down: tickets for load balancing, slots in a shared pool, ids. Do not use it when a later call must see a larger value than an earlier call that has finished, as in a ticket lock or a sequence number that orders events; then you need a linearizable counter such as one [fetch-and-add](/fetch-and-add/) word. On modern hardware, one fetch-and-add word is fast up to moderate thread counts, so measure before you choose the network.

## Pitfalls

- **Expecting linearizability.** The counter is only quiescently consistent; see the example.
- **A toggle that is not atomic.** A read and a write let two tokens take the same output; the test shows values 0 and 2 after two tokens.
- **Too few blocks.** Periodic$[w]$ needs all $\log_2 w$ blocks; one block balances but does not count.
- **Wrong output order.** In the bitonic network the outputs are not in wire order after the last merger; the counter must use the order that the construction defines.
- **A width that is not a power of 2.** These constructions need $w = 2^k$.
- **Stopped tokens.** A process that dies inside the network leaves the counter never quiescent, so the gap that its value would fill stays open.

## Implementations

## History

Aspnes, Herlihy and Shavit introduced counting networks at STOC 1991 and published the journal version in 1994, with the bitonic network, whose shape is that of Batcher's bitonic sorter, and the periodic network, whose shape is that of the periodic balanced sorting network of Dowd, Perl, Rudolph and Saks (1989). They showed that counting networks are sorting networks when balancers become comparators. Klugerman and Plaxton (1992) found counting networks of smaller depth. Herlihy, Shavit and Waarts studied linearizable counting (FOCS 1991, journal 1996). Shavit and Zemach's diffracting trees (1996) took the idea toward trees with randomized combining.

## References
