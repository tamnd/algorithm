---
tag: YWVGPT
kind: data-structure
slug: arora-blumofe-plaxton-deque
name: ABP non-blocking work-stealing deque
aliases:
- ABP deque
- Arora-Blumofe-Plaxton deque
- bounded work-stealing deque
area: concurrency/lock-free-structures
level: research
summary: Fixed-size non-blocking deque for work stealing, with a tagged top index to avoid ABA.
complexity:
  vars: {N: the length of the array, n: the number of items}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [deque, compare-and-swap, aba-problem, linearizability, lock-freedom]
see_also: [chase-lev-deque, work-stealing, tagged-pointers, wait-freedom, treiber-stack]
sources:
  - paper: doi:10.1145/277651.277678
    title: Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, SPAA 1998, pages 119 to 129
    locator: the deque code (pushBottom, popBottom and popTop with the age word of tag and top), its relaxed semantics, and the bound on the running time of the work stealer in the abstract
  - paper: doi:10.1007/s00224-001-0004-z
    title: Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, Theory of Computing Systems 34(2), 2001, pages 115 to 144
    locator: the journal version, with the full analysis of the scheduler
  - paper: doi:10.1145/1073970.1073974
    title: David Chase and Yossi Lev, Dynamic circular work-stealing deque, SPAA 2005
    locator: the introduction, on the fixed size and the tag of the ABP deque
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: the chapter on scheduling and work distribution, the bounded work-stealing deque with a stamped top
---

The ABP deque, by Nimar Arora, Robert Blumofe and Greg Plaxton (1998), is the first non-blocking deque made for [work stealing](/work-stealing/). Each worker owns one deque. The owner pushes and pops tasks at the *bottom*, and other workers, the *thieves*, take tasks from the *top* with popTop. The items live in an array of fixed size. A word `age` holds the index `top` together with a *tag*, and a thief takes an item with one [compare-and-swap](/compare-and-swap/) on this word. When the deque gets empty, the owner moves both indices back to 0 and adds one to the tag, so that a slow thief cannot take an item that is no longer there: the tag stops the [ABA problem](/aba-problem/). The paper uses the deque in a scheduler for machines that run several programs at once, and proves a bound on its running time.

## In plain words

A cook keeps plates in a row of numbered spots. The cook adds and takes plates at the right end, and helpers take plates from the left end. A sign shows where the left end is.

When the row is empty, the cook starts again from spot 0. But a slow helper may still remember the old sign, which also said "spot 0", and could take the new plate as if it were the old one. So the sign also carries a counter, and the cook adds one to it each time it starts again. A helper takes a plate only if the whole sign, counter and spot, is what it remembers.

## The abstract type

The object is a *work-stealing deque*: push$(x)$ and pop() at the bottom, called only by the owner, and steal() at the top, called by any process. The paper calls them pushBottom, popBottom and popTop. pop and steal return EMPTY on an empty deque. steal may also *fail* when it loses a race: in the paper's *relaxed semantics*, popTop may return NULL if, during the call, the deque was empty or another process removed the top item. This page returns ABORT for a lost race, so that it is apart from EMPTY. The safety condition is [linearizability](/linearizability/) with respect to the work-stealing deque in which steal may return ABORT with no effect. The array has a fixed length $N$; the paper assumes that it is large enough, and pushing beyond it is an error.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $N$ | the length of the array `deq` |
| `age` | one word that holds the pair (`tag`, `top`) |
| `bot` | the index one above the bottom item |
| $n$ | the number of items, `bot` $-$ `top` when it is positive |

There is one owner and any number of thieves. The processes are asynchronous and may crash between any two steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) on single words; `age` fits in one word because `tag` and `top` are small integers. The proofs assume sequential consistency. The tag does not wrap in the model; on a machine it is a bounded counter, and the section on memory reclamation says what that means.

### Fields

- `deq[0..N-1]`: the items. The item of index $i$ is in `deq[i]`; the array is not circular.
- `age` $=$ (`tag`, `top`): `top` is the index of the top item. Thieves change `age` only by a CAS that adds one to `top`. The owner changes it only to (`tag` $+ 1$, 0).
- `bot`: written only by the owner.

**Invariant.** The deque holds the items `deq[top]`, ..., `deq[bot-1]`; it is empty when `top` $\ge$ `bot`. Each time `top` goes back to 0, the tag is new, so the pair `age` never takes a value that it had before.

## Operations

```pseudo id=main
PUSHBOTTOM(x)                           ▷ owner only
L1  b ← bot
L2  deq[b] ← x                          ▷ an error if b = N
L3  bot ← b + 1                         ▷ linearization point

POPTOP()                                ▷ thieves
L4  old ← age
L5  b ← bot
L6  if b ≤ old.top then return EMPTY
L7  x ← deq[old.top]
L8  new ← (old.tag, old.top + 1)
L9  if CAS(age, old, new) then return x
L10 return ABORT                        ▷ the paper returns NULL here too

POPBOTTOM()                             ▷ owner only
L11 b ← bot
L12 if b = 0 then return EMPTY
L13 b ← b − 1; bot ← b
L14 x ← deq[b]
L15 old ← age                           ▷ a full fence is needed between L13 and L15
L16 if b > old.top then return x        ▷ more than one item: no race
L17 bot ← 0
L18 new ← (old.tag + 1, 0)              ▷ a new tag: the reset
L19 if b = old.top and CAS(age, old, new) then return x
L20 age ← new; return EMPTY
```

**The race for the last item.** The owner lowers `bot` first and then reads `age`. If `top` is below the new `bot`, no thief can take the owner's item, by the same argument as in the [Chase-Lev deque](/chase-lev-deque/): a thief that read the old `bot` would need `top` to be equal to $b$, but `top` was smaller when the owner read it. If $b$ = `top`, one item is left, and the owner and the thieves race with a CAS on `age`. The owner's CAS puts `age` to (`tag` $+ 1$, 0): if it wins, it returns the item, and the deque is empty and reset. If a thief wins, the thief returns the item, and the owner writes (`tag` $+ 1$, 0) at L20. If $b <$ `top`, the deque was already empty, and the owner just resets it at L20.

**Why the tag.** After a reset, `top` is 0 again, and the next push writes `deq[0]` again. A thief that read `age` $=$ (`tag`, 0) and `deq[0]` before the reset would, without a tag, find `top` $= 0$ at its CAS and succeed, returning an item that the owner already popped. The new tag makes its CAS fail.

**Linearization points.** push at L3. pop with $b >$ `top` at L13 (the write of `bot`). pop that returns EMPTY at L12, or at L15 when $b <$ `top`. If `top` $= b$ at the owner's L13, the item goes to the winner of the CAS on `age` from (`tag`, $b$) (the owner at L19, or a thief at L9), and that operation takes effect at the owner's L13; a losing owner returns EMPTY at its failed CAS. Any other successful popTop takes effect at its CAS at L9, and a popTop that returns EMPTY at its read of `bot` at L5. ABORT has no effect.

### Memory reclamation

Nothing is allocated or freed: the array has a fixed size, and the items are pointers to threads or tasks that the scheduler owns. The memory problem is the ABA problem on the index `top`, and the tag in `age` is its fix, in the style of [tagged pointers](/tagged-pointers/). Without the tag, the bad run above happens; `test_aba_without_the_tag` finds it. On a machine the tag has a fixed number of bits, so a thief that sleeps through $2^k$ resets of the deque, with $k$ the tag bits, could still see the same `age` again. With a tag of 32 bits or more, this is taken to be impossible in practice; it is not ruled out by the algorithm.

### Weak memory

The pseudocode assumes sequential consistency. The same orders as in the Chase-Lev deque are needed: in popBottom, a full fence between the write of `bot` at L13 and the read of `age` at L15, also on x86, where a store can pass a later load; in popTop, the read of `age` before the read of `bot`; in pushBottom, the write of the item before the write of `bot`.

## Example

**A reset beats a slow thief.** The owner pushes 1, so `age` $= (0, 0)$ and `bot` $= 1$.

| step | process | action | state |
|---|---|---|---|
| 1 | thief | L4 to L8: reads `age` $= (0, 0)$, `bot` $= 1$, item 1 | |
| 2 | owner | pop: L11 to L16: $b = 0$, `bot` $= 0$, reads `age`; $b$ = `top` | `bot` $= 0$ |
| 3 | owner | L17 to L19: `bot` $= 0$, CAS `age` from $(0, 0)$ to $(1, 0)$ succeeds, returns 1 | `age` $= (1, 0)$ |
| 4 | owner | push 2: `deq[0]` $= 2$, `bot` $= 1$ | |
| 5 | thief | L9: CAS `age` from $(0, 0)$ fails, returns ABORT | |

Without the tag, `age` would be $(0, 0)$ again after step 3, the CAS at step 5 would succeed, and the thief would return 1, the item that the owner already returned, while 2 stays in the deque at index 0 with `top` $= 1$ and is lost.

## Correctness

The argument has the same structure as for the Chase-Lev deque. (1) Between two resets, `top` changes only by a successful CAS that adds one, and by the tag no CAS that read `age` before a reset succeeds after it, so each index of each period between resets is taken at most once. (2) The owner takes index $b$ without a CAS only after it read `top` $< b$ after its write of `bot` $= b$, and then no thief can take index $b$. (3) A thief whose CAS succeeds read `deq[top]` after it read `bot` $>$ `top`, so after the push of that index, and the slot is not written again before a reset, which changes the tag. (4) With the points above, the abstract sequence is the items `deq[top]` to `deq[bot-1]`, and each operation returns what the specification returns at its point. The tests check linearizability on all interleavings of small cases, including a reset followed by a push, and find the ABA run when the tag is removed. This is a sketch; the paper gives its own proof of the relaxed semantics.

**Progress.** Each operation ends in a bounded number of its own steps, so the deque is [wait-free](/wait-freedom/) with respect to the specification with ABORT. A popTop that fails does so because another operation removed an item. The paper uses exactly this fact: it charges each failed popTop to a successful removal when it counts the steal attempts of the scheduler.

## Complexity

| operation | steps (shared memory accesses) |
|---|---|
| pushBottom | 3 |
| popTop | 2 when EMPTY, 4 otherwise |
| popBottom | 1 on `bot` $= 0$, 4 with more than one item, 6 for the last item when the owner wins, 7 when it loses |

These are the exact counts of the Python implementation, and the tests check the bounds in all interleavings of a small case. The space is the array of $N$ slots and two words.

**The scheduler bound (cited).** The paper's work stealer, which uses this deque and lets a process yield to others before each steal attempt, runs a multithreaded computation with work $T_1$ and critical-path length $T_\infty$ on $P$ processes in expected time $O(T_1 / P_A + T_\infty P / P_A)$, where $P_A$ is the average number of processors that the kernel gives to the computation. This page does not prove the bound; see the paper and its journal version.

## Variants

- **[Chase-Lev deque](/chase-lev-deque/).** Uses a circular array that can grow, and never moves `top` back, so it needs no tag. The two deques have the same race for the last item and the same fences. The ABP deque has a fixed array, resets the indices to 0 on empty, and needs the tag.
- **Dynamic-sized deques.** Hendler, Lev, Moir and Shavit replaced the fixed array by a list of blocks, so that the deque can grow, still with tags.
- **Locked deques.** The scheduler of Cilk-5 uses a deque with a lock for the thieves and a protocol (THE) that lets the owner avoid the lock most of the time. That deque is blocking.

## When to use it

Today it is mostly of historical and teaching value: the Chase-Lev deque does the same job without a fixed size and without a tag. The ABP deque is still a good choice when the number of tasks per worker has a known bound (for example, the depth of a recursion) and a fixed array is wanted, or on a machine where a CAS on a word with a tag is cheap and a growable array is not wanted.

## Pitfalls

- **A full array.** The deque does not grow; a push beyond $N$ overwrites memory in a C version with no check.
- **Forgetting the tag** on reset: the ABA run of the example.
- **Treating popTop's NULL as "empty".** In the paper, NULL can also mean "lost a race". A scheduler that stops stealing on NULL may leave work behind.
- **The fence in popBottom.** As in the Chase-Lev deque, without it the owner and a thief can take the same item.
- **Indices that do not go back to 0.** The array is not circular; if the owner never empties the deque while thieves keep taking from the top, `top` and `bot` both climb, and the deque fills although it holds few items.

## Implementations

## History

Blumofe and Leiserson (1994) proved bounds for randomized work stealing with deques on a dedicated machine. Arora, Blumofe and Plaxton (1998) asked what happens when the operating system gives a program a varying number of processors, and showed that a work stealer with a non-blocking deque and yields keeps a good bound; the deque of this page was their tool. The Hood library of Blumofe and Papadopoulos used it. Later deques removed its two limits: Hendler, Lev, Moir and Shavit made it grow, and Chase and Lev (2005) removed both the fixed size and the tag.

## References
