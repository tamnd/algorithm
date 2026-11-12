---
tag: AGATQM
kind: algorithm
slug: schorr-waite-marking
name: Schorr-Waite marking
aliases:
- Deutsch-Schorr-Waite
- pointer-reversal marking
- Schorr-Waite algorithm
area: systems/garbage-collection
level: advanced
summary: "Mark the cells reachable from a root with no stack. The marker reverses each pointer on its way down to store the path back, and restores it on the way up."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {m: the number of cells that the call marks}
  time: {worst: Θ(m), best: Θ(1)}
  space: {extra: O(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1967
  people: [Herbert Schorr, William M. Waite, L. Peter Deutsch]
  note: Schorr and Waite published the method in 1967. Knuth credits Deutsch with the same idea, found independently.
prereqs: [mark-and-sweep, depth-first-search]
see_also: [mark-and-sweep, tracing-garbage-collection, list-reversal, morris-traversal, pointer, tricolor-marking, cheney-copying-collector]
sources:
  - paper: doi:10.1145/363534.363554
    title: Herbert Schorr and William M. Waite, An efficient machine-independent procedure for garbage collection in various list structures, Communications of the ACM 10(8), 501-506, 1967
    locator: the marking procedure that reverses the links on the path to the current cell
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.3.5, Lists and garbage collection (marking with link inversion, and its exercises)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 4, mark-sweep garbage collection (pointer reversal)
  - paper: Richard Bornat, Proving pointer programs in Hoare logic, Mathematics of Program Construction (MPC 2000), LNCS 1837, Springer, 2000
    locator: the proof of the Schorr-Waite algorithm
  - paper: Farhad Mehta and Tobias Nipkow, Proving pointer programs in higher-order logic, Automated Deduction (CADE-19), LNCS 2741, Springer, 2003
    locator: the Isabelle/HOL proof of the Schorr-Waite algorithm
---

Schorr-Waite marking is the mark phase of a [mark-and-sweep](/mark-and-sweep/) collector that uses no stack. It does a [depth-first search](/depth-first-search/) of the heap, and it keeps the path back to the root inside the cells of that path: each [pointer](/pointer/) that it follows down is turned around to point at the cell it came from, and it is turned back on the way up. For cells with two fields, it needs only one extra flag bit in each cell and three pointer variables. Schorr and Waite published it in 1967. It is the standard example of *pointer reversal*, and its correctness proof is a known hard case for program verification.

## In plain words

A marker normally keeps a stack of the cells it must come back to. But a collector runs when memory is full, and a long chain of cells needs a stack as long as the chain.

The trick is to keep the way back inside the cells. When the marker steps from a cell into its left child, it writes, in the left field of that cell, the address of the cell it came from. The cells on the current path then form a trail back to the root. When the left side is done, the marker puts the left field back and uses the right field for the trail. A flag in each cell says which field holds the trail. When both sides are done, it puts the right field back and climbs up along the trail.

## The problem

**Heap model.** The heap has binary cells, as in LISP. Each cell $c$ has two pointer fields $c.\mathit{left}$ and $c.\mathit{right}$ (a cell or nil), one mark bit and one flag bit. The mutator is stopped. The marker may write the fields, but it must leave them as it found them.

**Task.** Given a root cell, mark every cell reachable from it through unmarked cells, and restore all fields. With all marks clear at the start, and one call for each root, this is the mark phase of the [automatic memory reclamation](/automatic-memory-reclamation/) problem.

**What is measured.** Loop iterations, and the extra space beside the mark bits: here a constant number of words and one flag per cell, against a stack of up to the depth of the search for the plain marker.

## The algorithm

The variable $t$ is the current cell, and $p$ is its parent on the path. The path back is $p$, then the cell stored in a field of $p$, and so on up to nil. The flag of a cell on the path says which field holds the next step back: 0 for the left field, 1 for the right field.

```pseudo id=main
SW-MARK(root)
L1  t ← root, p ← nil
L2  loop
L3      if t ≠ nil and t is unmarked then             ▷ advance into t
L4          mark t, flag(t) ← 0
L5          q ← t.left, t.left ← p, p ← t, t ← q
L6      else if p = nil then return
L7      else if flag(p) = 0 then                      ▷ swing: left side of p done
L8          q ← p.right, p.right ← p.left, p.left ← t, flag(p) ← 1, t ← q
L9      else                                          ▷ retreat: both sides of p done
L10         q ← p.right, p.right ← t, t ← p, p ← q
```

There are three moves. The *advance* (lines L3 to L5) marks $t$, stores the parent $p$ in its left field, and goes down to the old left child. The *swing* (lines L7 and L8) runs when the left side of $p$ is done and $t$ is its old left child: it puts that child back in $p.\mathit{left}$, moves the path back from $p.\mathit{left}$ to $p.\mathit{right}$, and goes down to the old right child. The *retreat* (lines L9 and L10) runs when both sides of $p$ are done and $t$ is its old right child: it puts that child back in $p.\mathit{right}$ and climbs one step along the path. A cell that is already marked, or nil, is never entered, which is what stops the search on cycles and shared cells.

## Example

The cells are $0 \to (1, 2)$, $1 \to (3, 2)$, $2 \to (4, \text{nil})$, $3 \to (\text{nil}, 3)$, $4 \to (0, \text{nil})$ and $5 \to (\text{nil}, 4)$, written as (left, right). The root is $0$. The heap has the cycle $0 \to 2 \to 4 \to 0$, the self-loop at $3$, and the cell $2$ shared by $0$ and $1$. The last column lists the fields that differ from the original ones after the iteration.

| it. | move | $t$ | $p$ | fields not in their original state |
|---|---|---|---|---|
| 1 | advance 0 | 1 | 0 | 0 = (nil, 2) |
| 2 | advance 1 | 3 | 1 | 0 = (nil, 2), 1 = (0, 2) |
| 3 | advance 3 | nil | 3 | 0 = (nil, 2), 1 = (0, 2), 3 = (1, 3) |
| 4 | swing at 3 | 3 | 3 | 0 = (nil, 2), 1 = (0, 2), 3 = (nil, 1) |
| 5 | retreat from 3 | 3 | 1 | 0 = (nil, 2), 1 = (0, 2) |
| 6 | swing at 1 | 2 | 1 | 0 = (nil, 2), 1 = (3, 0) |
| 7 | advance 2 | 4 | 2 | 0 = (nil, 2), 1 = (3, 0), 2 = (1, nil) |
| 8 | advance 4 | 0 | 4 | 0 = (nil, 2), 1 = (3, 0), 2 = (1, nil), 4 = (2, nil) |
| 9 | swing at 4 | nil | 4 | 0 = (nil, 2), 1 = (3, 0), 2 = (1, nil), 4 = (0, 2) |
| 10 | retreat from 4 | 4 | 2 | 0 = (nil, 2), 1 = (3, 0), 2 = (1, nil) |
| 11 | swing at 2 | nil | 2 | 0 = (nil, 2), 1 = (3, 0), 2 = (4, 1) |
| 12 | retreat from 2 | 2 | 1 | 0 = (nil, 2), 1 = (3, 0) |
| 13 | retreat from 1 | 1 | 0 | 0 = (nil, 2) |
| 14 | swing at 0 | 2 | 0 | 0 = (1, nil) |
| 15 | retreat from 0 | 0 | nil | none |
| 16 | return | | | none |

In iteration 4 the right field of 3 points to 3 itself, which is marked, so nothing is entered. In iteration 9 the left child of 4 is 0, which is marked: the cycle stops there. In iteration 14 the right child of 0 is 2, which was marked through 1. The cells $0$ to $4$ end marked, the garbage cell $5$ stays unmarked, and every field is back in its original state. The call marked $m = 5$ cells in $3 \cdot 5 + 1 = 16$ iterations.

## Correctness

The proof is by induction on the number of unmarked cells. The key statement is a *visit lemma*: if the loop is at a state with $t = x$ and $p = y$, where $y$ is nil or marked, then after exactly $3|U|$ iterations it comes back to a state with $t = x$ and $p = y$, with every field as before and with exactly the set $U$ added to the marks, where $U$ is the set of cells reachable from $x$ through unmarked cells. For an unmarked $x$, the advance, the visit of the left child, the swing, the visit of the right child and the retreat compose to this result. The induction works because every cell on the path back is marked, so no search below it can enter it and read a reversed field. The full proof is in the proofs section.

Verifying the real program is much harder than this paper proof, because the heap changes at each step. The Schorr-Waite algorithm became a test case for proof methods for pointer programs: Bornat gave a proof in Hoare logic in 2000, and Mehta and Nipkow a machine-checked proof in Isabelle/HOL in 2003.

## Complexity

The model is the [word RAM](/word-ram/).

- **Time.** Each iteration is an advance, a swing, a retreat or the return. Each marked cell gets exactly one advance, one swing and one retreat, so a call that marks $m$ cells does exactly $3m + 1$ iterations of $O(1)$ work: $\Theta(m)$, and $\Theta(1)$ when the root is nil or already marked. Over all roots $r_1, \ldots, r_s$ the marker does $3L + s$ iterations, where $L$ is the number of reachable cells.
- **Space.** The variables $t$, $p$ and $q$, so $O(1)$ words. Each cell needs one flag bit beside its mark bit; often a spare bit of the cell header holds it. The marker with a stack needs a stack as deep as the longest path of the search, up to $L$ entries.
- **Constant factor.** Each step of the advance and the retreat writes to the heap, while the stack marker only reads the fields. So Schorr-Waite is slower in practice, and collectors use it only as a fallback.

## Properties

- **Depth-first.** The order of first visits is the preorder of a depth-first search that tries the left field before the right field.
- **The heap is broken during the mark.** While the marker runs, the fields of the cells on the path hold back pointers. The mutator cannot run at the same time, and no other thread may read the heap: this is a [stop-the-world](/stop-the-world-collection/) marker.
- **Fields are restored exactly.** After the call every field holds its original value.

## Variants and improvements

- **Cells with $k$ fields.** The same method works for cells with $k$ fields if each cell on the path keeps a counter of $\lceil \lg k \rceil$ bits that says which field holds the path back, in place of the one flag bit. The swing then moves the path back from field $i$ to field $i + 1$.
- **Wegbreit's bit stack.** Wegbreit (1972) keeps the flag bits in a separate stack with one bit per level of the path, so the cells need no flag bit.
- **Hybrid marker.** Use a fixed-size mark stack, and switch to pointer reversal only when the stack overflows. Knuth's Section 2.3.5 discusses markers with a bounded stack.
- **Pointer reversal elsewhere.** The same idea gives [list reversal](/list-reversal/) in place, the threaded compaction of Jonkers (see [mark-compact](/mark-compact/)), and tree traversals with no stack, compare [Morris traversal](/morris-traversal/), which threads through null fields instead.

## When to use it

Use Schorr-Waite marking when the collector cannot count on memory for a mark stack, for example on a small machine or as the fallback when a mark stack overflows. When memory for a stack is available, a stack marker is faster and simpler. For the order of a breadth-first search with no stack, a copying collector can use [Cheney's algorithm](/cheney-copying-collector/), which keeps its queue in the to-space.

## Pitfalls

- **Reading a reversed field.** If line L3 entered a marked cell, it would follow a field that may hold a back pointer, and the marker would wander or lose the path. The test "t is unmarked" in line L3 is what keeps the search away from the path.
- **Order of the assignments in the swing.** Line L8 must read $p.\mathit{right}$ into $q$ before it overwrites it with $p.\mathit{left}$, and it must copy the back pointer out of $p.\mathit{left}$ before it writes $t$ there. Any other order loses a pointer.
- **Forgetting the flag.** Without the flag of line L7, the marker cannot tell if it comes back from the left or the right child, and it swings a cell twice. The flag must be set to 0 in line L4 even if a previous collection left it at 1.
- **Running the mutator during the mark.** The heap is not valid until the call returns. An interrupt handler or another thread that reads the heap sees wrong pointers.

## Implementations

## History

Schorr and Waite described the method in Communications of the ACM in 1967, for the garbage collector of a list-processing system. Knuth's Volume 1 presents it with link inversion and credits L. Peter Deutsch with the same idea. Wegbreit (1972) replaced the flag bits by a bit stack. The algorithm later became a benchmark for the verification of pointer programs, with proofs by Bornat (2000) and by Mehta and Nipkow (2003).

## References
