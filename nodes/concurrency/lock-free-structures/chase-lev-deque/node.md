---
tag: HJCFRC
kind: data-structure
slug: chase-lev-deque
name: Chase-Lev work-stealing deque
aliases:
- Chase-Lev deque
- dynamic circular work-stealing deque
area: concurrency/lock-free-structures
level: advanced
summary: Dynamic lock-free deque in which the owner pushes and pops at one end while thieves steal from the other.
complexity:
  vars: {n: the number of items in the deque, m: the most items held at one time, s: the size of the array}
  space: {extra: Θ(s)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [deque, circular-buffer, compare-and-swap, linearizability, lock-freedom]
see_also: [arora-blumofe-plaxton-deque, work-stealing, wait-freedom, treiber-stack, epoch-based-reclamation, hazard-pointers]
sources:
  - paper: doi:10.1145/1073970.1073974
    title: David Chase and Yossi Lev, Dynamic circular work-stealing deque, SPAA 2005, pages 21 to 28
    locator: the pseudocode of pushBottom, popBottom and steal on a circular array, the growth of the array, and the argument that top never decreases
  - paper: doi:10.1145/2442516.2442524
    title: Nhat Minh Lê, Antoniu Pop, Albert Cohen and Francesco Zappa Nardelli, Correct and efficient work-stealing for weak memory models, PPoPP 2013, pages 69 to 80
    locator: the C11 version with its fences and memory orders, and the proof of an optimized version for POWER and ARM
  - paper: doi:10.1145/277651.277678
    title: Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, SPAA 1998, pages 119 to 129
    locator: the non-blocking deque with a tag in the top word, which the Chase-Lev deque improves on
  - paper: doi:10.1145/1504176.1504186
    title: Maged M. Michael, Martin T. Vechev and Vijay A. Saraswat, Idempotent work stealing, PPoPP 2009
    locator: deques with no CAS for the owner, in which a task may be taken more than once
---

The Chase-Lev deque is the deque at the heart of most [work-stealing](/work-stealing/) schedulers. David Chase and Yossi Lev published it in 2005. Each worker thread owns one deque. The owner pushes and pops tasks at the *bottom*, like a stack, and idle threads called *thieves* steal tasks from the *top*. The items live in a [circular array](/circular-buffer/) between two indices, `top` and `bottom`, and the array grows when it is full. The owner needs no [compare-and-swap](/compare-and-swap/) except when it takes the last item, so the common path is a few plain reads and writes. A thief takes an item with one CAS on `top`. Unlike the earlier [Arora-Blumofe-Plaxton deque](/arora-blumofe-plaxton-deque/), `top` only grows, so no tag is needed against the [ABA problem](/aba-problem/), and the array is not of fixed size.

## In plain words

A cook keeps a stack of plates on a long table. The cook adds plates at one end and takes them back from the same end. Helpers with nothing to do come and take plates from the other end. The cook moves a marker for its own end, and helpers move a marker for theirs.

Most of the time the cook and the helpers work far apart and never meet. Only when one plate is left can both reach for it at the same time. Then they both try to move the helpers' marker by one, and only one of them can win. When the table is full, the cook gets a table twice as long, moves the plates over, and goes on.

## The abstract type

The object is a *work-stealing deque*: a sequence with push$(x)$ and pop() at the back, called by one owner process only, and steal() at the front, called by any number of thieves. pop and steal return EMPTY when the sequence is empty. steal may also return ABORT with no effect, when it loses a race; a thief then tries again or tries another deque. The safety condition is [linearizability](/linearizability/) with respect to this specification. Compared with a general [deque](/deque/), only one process may use the back, and nobody may push at the front.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $t$ | a value read from `top` |
| $b$ | a value read from `bottom`, or that value minus one in pop |
| $a$ | an array; $a.size$ is its length |
| $s$ | the length of the current array |
| $n$ | the number of items, `bottom` $-$ `top` |
| index $i$ | the item at index $i$ is in slot $i \bmod s$ |

There is one owner and any number of thieves. The processes are asynchronous and may crash between any two steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) on single words. The proofs assume sequential consistency; the section on weak memory gives the fences that real hardware needs. Indices do not wrap; on a machine, 64-bit indices do not wrap in practice.

### Fields

- `top`: the index of the front item. Only a successful CAS changes it, always from $t$ to $t + 1$, so it never decreases.
- `bottom`: one more than the index of the back item. Only the owner writes it.
- `array`: a pointer to the current array. Only the owner writes it, when the array grows.

**Invariant.** The deque holds the items at indices `top`, ..., `bottom` $- 1$, in the slots of `array`; it is empty when `top` $\ge$ `bottom`. Outside a pop, `top` $\le$ `bottom`, and `bottom` $-$ `top` $<$ $s$.

## Operations

```pseudo id=main
PUSH(x)                                  ▷ owner only
L1  b ← bottom; t ← top; a ← array
L2  if b − t ≥ a.size − 1 then a ← GROW(a, b, t)
L3  a[b mod a.size] ← x
L4  bottom ← b + 1                       ▷ release; linearization point

POP()                                    ▷ owner only
L5  b ← bottom − 1; a ← array
L6  bottom ← b                           ▷ thieves now see one item fewer
L7  t ← top                              ▷ a full fence is needed between L6 and L7
L8  if t > b then bottom ← b + 1; return EMPTY
L9  x ← a[b mod a.size]
L10 if t < b then return x               ▷ more than one item: no race
L11 ok ← CAS(top, t, t + 1)              ▷ the last item: race with the thieves
L12 bottom ← b + 1
L13 if ok then return x else return EMPTY

STEAL()
L14 t ← top
L15 b ← bottom                           ▷ a full fence is needed between L14 and L15
L16 if t ≥ b then return EMPTY
L17 a ← array; x ← a[t mod a.size]
L18 if not CAS(top, t, t + 1) then return ABORT
L19 return x
```

```pseudo id=grow
GROW(a, b, t)                            ▷ owner only
G1  c ← a new array of length 2 · a.size
G2  for i ← t to b − 1 do c[i mod c.size] ← a[i mod a.size]
G3  array ← c                            ▷ release
G4  return c
```

**The two races.** A thief and the owner can only meet on the last item. The owner first lowers `bottom` (L6) and then reads `top` (L7). If it sees more than one item ($t < b$), no thief can take index $b$: a thief that read the old `bottom` would need `top` $= b$ for its CAS, but `top` was below $b$ when the owner read it, after its write of `bottom`. If exactly one item is left ($t = b$), both sides CAS `top` from $b$ to $b + 1$, and the CAS picks one winner. The owner then puts `bottom` back to $b + 1$, so that `top` $=$ `bottom` again.

**Why a stale array is safe.** A thief may read `array` just before the owner grows it, and then read its item from the old array. The copy (G2) does not change the old array, and the owner writes later items only to the new one. The old slot of index $t$ is overwritten only by the item of index $t + s$, which the owner pushes only when `top` $> t + 1$. Then the thief's CAS fails and it returns ABORT.

**Linearization points.** push at L4. pop with $t < b$ at L6. pop with $t > b$ returns EMPTY at L7. If `top` $= b$ when the owner does L6, the item at index $b$ goes to the winner of the CAS on `top` from $b$ (the owner or a thief), and that operation takes effect at the owner's L6; a losing owner returns EMPTY at L11. Any other successful steal takes effect at its CAS (L18), and a steal that returns EMPTY at its read of `bottom` (L15). ABORT has no effect.

### Memory reclamation

Items are values (or pointers to tasks that the scheduler owns), so the deque frees nothing on pop or steal. The only memory problem is the old arrays. A thief may hold a pointer to an array after the owner has replaced it, so the owner cannot free the old array at once. Chase and Lev work in a garbage-collected setting. In C or C++, the usual choices are [epoch-based reclamation](/epoch-based-reclamation/) or [hazard pointers](/hazard-pointers/) on the array pointer, or simply keeping the old arrays: since each array is twice the size of the previous one, all of them together take less space than the current one. If the owner frees an old array with no scheme, a slow thief reads freed memory in L17 and may return garbage, even though its CAS succeeds. There is no ABA problem on `top`, because `top` never decreases: a CAS that expects $t$ succeeds only if no other item was taken since the read.

### Weak memory

The pseudocode is correct only under sequential consistency. Lê, Pop, Cohen and Zappa Nardelli (2013) gave a C11 version and proved an optimized version correct on POWER and ARM. The key orders are these. In pop, the write of `bottom` at L6 and the read of `top` at L7 need a sequentially consistent fence between them; x86 also reorders a store with a later load, so this fence is needed there too (an `mfence`, or an exchange for the store). In steal, the read of `top` and the read of `bottom` also need a sequentially consistent fence; on x86, loads are not reordered with loads, so this one costs nothing there. In push, the item must be visible before the new `bottom` (a release fence or a release store at L4), and the thief reads the array and the item after an acquire read. The CAS operations on `top` are sequentially consistent. The test `test_store_load_reordering_breaks_pop` models the missing fence in pop and finds a run in which one item is returned twice.

## Example

**The last item.** The deque holds one item, 7, at index 0: `top` $= 0$, `bottom` $= 1$. The owner calls pop and a thief calls steal.

| step | process | action | state |
|---|---|---|---|
| 1 | thief | L14, L15: reads $t = 0$, $b = 1$ | |
| 2 | owner | L5, L6: $b = 0$, writes `bottom` $= 0$ | `top` $= 0$, `bottom` $= 0$ |
| 3 | owner | L7: reads $t = 0$; $t = b$, so this is the last item | |
| 4 | thief | L17, L18: reads 7, CAS `top` from 0 to 1 succeeds | `top` $= 1$ |
| 5 | owner | L9, L11: reads 7, CAS `top` from 0 to 1 fails | |
| 6 | owner | L12, L13: writes `bottom` $= 1$, returns EMPTY | `top` $= 1$, `bottom` $= 1$ |
| 7 | thief | L19: returns 7 | |

The item is taken once. In the linearization, the steal takes effect at step 2 and the pop at step 5. Without the CAS in the owner's path (return $x$ at L10 even when $t = b$), the owner returns 7 too; `test_last_item_race_needs_the_cas` finds that run.

**The missing fence.** The deque holds 1 and 2 at indices 0 and 1. The owner's pop reads `top` $= 0$ *before* its write of `bottom` $= 1$ becomes visible. A thief steals index 0, reads `bottom` $= 2$ again, and steals index 1. The owner then sees $t = 0 < b = 1$, takes index 1 with no CAS, and returns 2: the thief also returned 2.

## Correctness

The proof file gives the full argument; this is the outline. Four facts carry it. First, `top` changes only by a successful CAS from $t$ to $t + 1$, so it never decreases, and each index is taken by at most one CAS. Second, the owner takes index $b$ without a CAS only after reading `top` $< b$ after its write of `bottom` $= b$, and then no thief can win a CAS on `top` from $b$ while `bottom` $= b$. Third, a thief that wins its CAS on `top` from $t$ read the item of index $t$: the slot was written before `bottom` passed $t$, and it is not overwritten while `top` $= t$. Fourth, with the linearization points above, the abstract sequence is the items of indices `top` to `bottom` $- 1$ at every time, and each operation returns what the specification says at its point. The tests check linearizability on all interleavings of small cases, with one or two thieves, and through a growth of the array.

**Progress.** Each operation ends in a bounded number of its own steps, whatever the other processes do, so the deque is [wait-free](/wait-freedom/) with respect to the specification with ABORT. A thief that retries on ABORT is [lock-free](/lock-freedom/): its CAS fails only when another operation took an item.

## Complexity

| operation | steps (shared memory accesses) |
|---|---|
| push, no growth | 6 |
| push with growth | $2n + 8$ |
| pop | 5 when EMPTY, 6 with more than one item, 8 for the last item |
| steal | 2 when EMPTY, 6 otherwise |

The counts are the exact counts of the Python implementation, which reads the array length as a separate step, and they hold in every interleaving; the tests check the owner's counts on all interleavings of a small case. Growth happens when $n = s - 1$; the new array has length $2s$ and holds $s - 1$ items, so the next growth needs at least $s$ more pushes, and the copying costs $O(1)$ amortized per push. A push that grows takes $\Theta(n)$ steps by itself, so the owner's worst case is linear unless the copy is spread over later pushes. The space is the current array plus the old arrays until they are freed. A growth makes $s = 2n + 2$, and the array never shrinks in this version, so $s \le \max(s_0, 2m + 2)$, where $s_0$ is the first size and $m$ is the most items held at one time.

## Variants

- **[Arora-Blumofe-Plaxton deque](/arora-blumofe-plaxton-deque/).** The earlier non-blocking work-stealing deque. Its array has a fixed size, and the owner resets `top` to 0 when the deque gets empty, so the top word needs a tag against ABA. The Chase-Lev deque removes the tag by never decreasing `top`, and removes the fixed size with the circular array.
- **Shrinking.** Chase and Lev also describe how the owner can move the items to a smaller array when the deque gets small. This page does not implement it.
- **Idempotent work stealing** (Michael, Vechev and Saraswat 2009). If a task may run twice, the owner can drop the CAS and the fence; the deque then gives each item to *at least* one taker. This is a different specification.
- **Weak memory versions.** The C11 and ARM versions of Lê et al. (2013) put the fences in the places described above.

## When to use it

Use it for the per-thread task queues of a work-stealing scheduler: the owner's push and pop are very cheap, and thieves only touch the deque when they have nothing to do. It is the default choice for fork-join runtimes. Do not use it as a general concurrent deque: only one process may push and pop. For a queue with many producers, use a [Michael-Scott queue](/michael-scott-queue/) or a bounded ring; for a shared stack, a [Treiber stack](/treiber-stack/).

## Pitfalls

- **The fence in pop.** Without a full fence between the write of `bottom` and the read of `top`, the owner and a thief can take the same item, on x86 as well as on ARM. This is the most common bug.
- **Forgetting to restore `bottom`.** After the race for the last item, and after an EMPTY pop, `bottom` must go back to $b + 1$; otherwise `bottom` $<$ `top` and the next push writes an index that a thief will never see.
- **Freeing the old array** while a thief may still read it.
- **Checking `t > b` with unsigned indices.** In pop, $b$ can be $-1$ on an empty deque that was never used; with unsigned types the test is wrong. Use signed 64-bit indices.
- **Calling pop from a thief.** Only the owner may write `bottom`. A second process that pushes or pops breaks every argument above.
- **Treating ABORT as EMPTY.** ABORT means that the deque may still have items; a scheduler that gives up on ABORT may leave work behind.

## Implementations

## History

Arora, Blumofe and Plaxton (1998) gave the first non-blocking work-stealing deque, for a scheduler on multiprogrammed machines, with a fixed array and a tagged top. Hendler, Lev, Moir and Shavit then built a deque of linked blocks that could grow. Chase and Lev (2005), at Sun Microsystems, gave the simpler circular-array deque with a top that never decreases. It became the standard deque of work-stealing runtimes. Lê, Pop, Cohen and Zappa Nardelli (2013) showed which fences it needs on weak memory and proved a version for POWER and ARM.

## References
