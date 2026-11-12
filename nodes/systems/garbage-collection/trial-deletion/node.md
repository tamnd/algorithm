---
tag: 40TJAC
kind: algorithm
slug: trial-deletion
name: Trial deletion
aliases:
- Bacon-Rajan cycle collection
- synchronous cycle collection
- trial deletion cycle collector
area: systems/garbage-collection
level: advanced
summary: "Frees dead cycles in a reference counted heap. Subtract the counts due to references inside the subgraph below candidate objects; what no outside reference holds is garbage."
solves: [cycle-collection]
model: word-ram
complexity:
  vars: {N: the number of objects that the candidates reach, E: the number of references between them}
  time: {worst: O(N + E)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: true, complete: true, moving: false}
history:
  year: 2001
  people: [David F. Bacon, V. T. Rajan]
  note: "Bacon and Rajan gave a synchronous cycle collector that handles all buffered candidates together in linear time, and a concurrent version, at ECOOP 2001. Local mark-scan methods by Martinez, Wachenchauzer and Lins (1990) and Lins (1992) came first."
prereqs: [cycle-collection, reference-counting]
see_also: [cycle-collection, reference-counting, deferred-reference-counting, tricolor-marking, mark-and-sweep, weak-reference, strongly-connected-components, tracing-garbage-collection]
sources:
  - paper: doi:10.1007/3-540-45337-7_12
    title: "David F. Bacon and V. T. Rajan, Concurrent cycle collection in reference counted systems, ECOOP 2001, LNCS 2072, 207-235"
    locator: the synchronous cycle collection algorithm (the procedures Increment, Decrement, Release, PossibleRoot, CollectCycles, MarkRoots, ScanRoots, CollectRoots, MarkGray, Scan, ScanBlack and CollectWhite, the colors, and the linear bound)
  - paper: doi:10.1016/0020-0190(90)90226-N
    title: "A. D. Martinez, R. Wachenchauzer and R. D. Lins, Cyclic reference counting with local mark-scan, Information Processing Letters 34(1) (1990), 31-35"
    locator: the whole paper (the local mark-scan after a decrement to a nonzero count)
  - paper: doi:10.1016/0020-0190(92)90088-D
    title: "Rafael D. Lins, Cyclic reference counting with lazy mark-scan, Information Processing Letters 44(4) (1992), 215-220"
    locator: the whole paper (the buffered candidates and the lazy mark-scan)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 5.5 (cyclic reference counting by trial deletion)
---

Trial deletion is a method to free the dead cycles that [reference counting](/reference-counting/) leaves in the heap. It takes the objects that might be the entry to a dead cycle, the *candidates*, and pretends to delete them: it subtracts from each count the references that come from inside the subgraph below the candidates. An object of the subgraph that still has a positive count is held by a reference from outside, so it and everything that it reaches are live; the counts of these objects are restored. All other objects of the subgraph are garbage and are freed. The synchronous algorithm of Bacon and Rajan (2001), shown here, handles all candidates in three passes and takes time linear in the size of the subgraph.

## In plain words

Reference counting cannot free a group of dead objects that refer to each other. Each of them still has a reference, from another member of the group.

Trial deletion asks a simple question: if we ignore the references that come from inside the group, which members still have a reference? Those members are held from outside, so they are alive, and so is everything that they refer to. The other members are only held by each other, so the whole group is dead.

The method does this in three passes. The first pass subtracts the inside references. The second pass finds the members with a reference left and gives the counts back to them and to what they reach. The third pass frees the rest.

## The problem

Solve [cycle collection](/cycle-collection/): in a heap with exact reference counts, free the garbage that reference counting cannot free, and never free a reachable object. Here every reference, from a root or from a heap field, is counted, and a root record that is never freed holds the roots.

## The algorithm

Each object $S$ has a count $\mathrm{rc}(S)$, a color, and a flag $\mathrm{buffered}(S)$. The colors are *black* (in use or live), *gray* (a possible member of a dead cycle), *white* (garbage), and *purple* (a candidate). The list Roots holds the candidates. The mutator's write calls INCREMENT on the new value and DECREMENT on the old one. From time to time, COLLECT-CYCLES runs MARK-ROOTS, then SCAN-ROOTS, then COLLECT-ROOTS.

```pseudo id=main
INCREMENT(S)
L1  rc(S) ← rc(S) + 1; color(S) ← black

DECREMENT(S)
L2  rc(S) ← rc(S) − 1
L3  if rc(S) = 0 then                      ▷ RELEASE(S)
L4      for each child T of S do DECREMENT(T)
L5      color(S) ← black
L6      if not buffered(S) then free(S)
L7  else POSSIBLE-ROOT(S)

POSSIBLE-ROOT(S)
L8  if color(S) ≠ purple then
L9      color(S) ← purple
L10     if not buffered(S) then buffered(S) ← true; append S to Roots

MARK-ROOTS()
L11 for each S in Roots do
L12     if color(S) = purple and rc(S) > 0 then
L13         MARK-GRAY(S)
L14     else buffered(S) ← false
L15         if color(S) = black and rc(S) = 0 then
L16             free(S)
L17 remove from Roots each S that line L14 handled

SCAN-ROOTS()
L18 for each S in Roots do SCAN(S)

COLLECT-ROOTS()
L19 for each S in Roots do remove S from Roots
L20     buffered(S) ← false
L21     COLLECT-WHITE(S)

MARK-GRAY(S)
L22 if color(S) ≠ gray then
L23     color(S) ← gray
L24     for each child T of S do
L25         rc(T) ← rc(T) − 1
L26         MARK-GRAY(T)

SCAN(S)
L27 if color(S) = gray then
L28     if rc(S) > 0 then
L29         SCAN-BLACK(S)
L30     else color(S) ← white
L31         for each child T of S do SCAN(T)

SCAN-BLACK(S)
L32 color(S) ← black
L33 for each child T of S do
L34     rc(T) ← rc(T) + 1
L35     if color(T) ≠ black then SCAN-BLACK(T)

COLLECT-WHITE(S)
L36 if color(S) = white and not buffered(S) then
L37     color(S) ← black
L38     for each child T of S do COLLECT-WHITE(T)
L39     free(S)
```

A decrement to a nonzero value is the only event that can turn a live cycle into a dead one, so line L7 makes that object a candidate. The flag *buffered* keeps an object in Roots at most once, and it stops line L6 from freeing an object that Roots still names; such an object is freed by line L16. MARK-GRAY subtracts each reference inside the gray subgraph exactly once, because it scans each object only when it first turns it gray. SCAN then finds the gray objects with a positive count, and SCAN-BLACK adds the counts back below each of them. The recursion can be deep, so an implementation uses explicit stacks.

## Example

Objects $a \to b \to c \to a$ form a cycle, and the roots refer to $a$ and to $b$. The program clears the root to $a$. The count of $a$ drops from 2 to 1, so $a$ turns purple and enters Roots.

| phase | colors of $a, b, c$ | counts of $a, b, c$ |
|---|---|---|
| before | purple, black, black | 1, 2, 1 |
| after MARK-GRAY($a$) | gray, gray, gray | 0, 1, 0 |
| SCAN($a$): $a$ has count 0 | white, gray, gray | 0, 1, 0 |
| SCAN($b$): $b$ has count 1, SCAN-BLACK($b$) | black, black, black | 1, 2, 1 |
| COLLECT-WHITE($a$) | black, black, black | 1, 2, 1 |

The root to $b$ is an outside reference, so $b$ keeps a count of 1 after the subtraction. SCAN-BLACK from $b$ restores the counts of $c$ and $a$, and nothing is freed. Now the program clears the root to $b$. Its count drops from 2 to 1, and $b$ becomes a candidate. MARK-GRAY($b$) gives the counts 0, 0, 0, so SCAN colors all three objects white, and COLLECT-WHITE($b$) frees $b$, $c$ and $a$.

## Correctness

After MARK-GRAY has run from all candidates, each gray object's count equals the number of references to it from outside the gray subgraph. SCAN and SCAN-BLACK then color black exactly the gray objects that a path inside the subgraph reaches from an object with an outside reference, and restore their counts. By the internal-count test of [cycle collection](/cycle-collection/), the remaining white objects are garbage, so the algorithm is safe. COLLECT-WHITE frees all of them, and the counts of the remaining objects are exact again. Moreover, every garbage object is reached from a candidate, so each collection frees all garbage, and afterwards the unfreed objects are exactly the reachable ones. The full proof is below.

## Complexity

- **Mutator.** INCREMENT and DECREMENT cost $O(1)$ more than in plain reference counting: a color change, and sometimes an append to Roots.
- **One collection.** Let $N$ and $E$ be the numbers of objects and references in the subgraph that the candidates reach. MARK-GRAY visits each of these objects and references once. SCAN does work only on gray objects, and SCAN-BLACK only on objects that are not yet black, so both also take $O(N + E)$. COLLECT-WHITE frees each white object once. The total is $O(N + E)$ time, in at most three passes over the subgraph.
- **Space.** Roots holds at most one entry per object. The explicit stacks of the three passes hold $O(N)$ entries.
- **Compared with per-candidate methods.** A method that runs the three passes for each candidate on its own can visit an object once per candidate that reaches it, which is quadratic in the worst case.

## Properties

- **Complete with reference counting.** Together with reference counting, each collection frees all garbage, not only the cycles.
- **Local.** It visits only objects that the candidates reach, not the whole heap. But a candidate that reaches a large live structure makes the collector visit all of it.
- **Stop-the-world in this form.** The synchronous algorithm assumes that the mutator does not run during COLLECT-CYCLES.
- **Non-moving.** No object moves, and the counts serve both the reference counting and the cycle test.

## Variants and improvements

- **Acyclic objects.** Objects of types that cannot be part of a cycle, such as strings or arrays of numbers, get a fifth color, *green*. They never become candidates, and the passes do not trace through them. This removes much of the work.
- **Concurrent cycle collection.** Bacon and Rajan's concurrent version runs while the mutator runs. It uses the same passes, then checks each found cycle again (their Σ-test and Δ-test) before freeing it, because the mutator may have changed the subgraph.
- **Deferred counts.** With [deferred reference counting](/deferred-reference-counting/), the roots are not counted. The cycle collector then runs right after a scan of the roots, when the counts include the roots.
- **Local mark-scan.** Martinez, Wachenchauzer and Lins run the same three steps at once, below each pointer whose count drops to a nonzero value. Lins buffers the candidates and runs the steps later, but still for each candidate on its own.
- **Whole-generation test.** CPython's cycle detector applies the same subtraction of inside references to all tracked objects of a generation, instead of the subgraph below candidates.

## When to use it

Use trial deletion when a system uses reference counting, needs to free cycles, and cannot afford a trace of the whole heap. It works best when cycles are rare and the subgraphs below candidates are small, for example when most objects are marked acyclic. If the subgraphs are large and mostly live, a backup [tracing collector](/tracing-garbage-collection/) can cost less.

## Pitfalls

- **Freeing a buffered object at count zero.** An object in Roots whose count drops to 0 must not be freed by DECREMENT, or Roots names freed memory. Line L6 leaves it to line L16.
- **Subtracting a reference twice.** MARK-GRAY must decrement the children only when it first colors an object gray. Otherwise a node with two gray predecessors on paths from one candidate loses too much count and can be freed while live.
- **Running the passes per candidate.** Running MARK-GRAY, SCAN and COLLECT-WHITE for each candidate in turn is correct but quadratic. Run each pass for all candidates before the next pass.
- **Recursion depth.** A long list below a candidate makes each pass recurse once per element. Use explicit stacks.
- **Mutator activity.** If the mutator runs between MARK-GRAY and COLLECT-WHITE, a white object can become reachable again. The synchronous version must stop the mutator, and the concurrent one must check again.

## Implementations

## History

Reference counting has always lacked a way to free cycles. Martinez, Wachenchauzer and Lins (1990) proposed a local mark-scan after each decrement to a nonzero count: subtract the inside references of the subgraph below the pointer, restore the counts of the part that keeps a positive count, and free the rest. Lins (1992) made it lazy by buffering the candidates. Bacon and Rajan (2001) showed that handling the candidates one by one can take quadratic time, and gave the synchronous algorithm on this page, which runs each pass over all candidates together in linear time, and a concurrent version for their Recycler collector for Java. The method is now usually called trial deletion.

## References
