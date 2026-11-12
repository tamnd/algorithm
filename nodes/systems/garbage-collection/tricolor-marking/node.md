---
tag: SZ1DX2
kind: concept
slug: tricolor-marking
name: Tricolor marking
aliases:
- tri-color abstraction
- white grey black
- tricolour invariant
area: systems/garbage-collection
level: core
summary: "Objects are white (not reached), gray (reached, fields not scanned) or black (scanned). The strong and weak tricolor invariants make marking safe while the program runs."
prereqs: [mark-and-sweep, mutator-and-collector]
see_also: [write-barrier, incremental-update-barrier, snapshot-at-the-beginning, incremental-garbage-collection, concurrent-garbage-collection, on-the-fly-garbage-collection, cheney-copying-collector, breadth-first-search]
sources:
  - paper: doi:10.1145/359642.359655
    title: Edsger W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection, an exercise in cooperation, Communications of the ACM 21(11), 966-975, 1978
    locator: the colors white, gray and black, the invariant that no black node points to a white node, and the shading of the new target by the mutator
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Section 2.2 (the tricolour abstraction) and Section 15.1 (the lost object problem, the strong and weak tricolour invariants, incremental update and snapshot-at-the-beginning solutions)
  - paper: Pekka P. Pirinen, Barrier techniques for incremental tracing, Proceedings of the First International Symposium on Memory Management (ISMM 1998), ACM, 1998
    locator: the classification of barriers by the invariant they keep
  - paper: Guy L. Steele Jr., Multiprocessing compactifying garbage collection, Communications of the ACM 18(9), 495-508, 1975
    locator: the barrier that makes the object written to gray again
  - paper: Taiichi Yuasa, Real-time garbage collection on general-purpose machines, Journal of Systems and Software 11(3), 181-198, 1990
    locator: the deletion barrier that shades the old value of an overwritten field
  - paper: Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, Springer, 1992
    locator: the section on incremental tracing, the tricolor marking and the two conditions for a lost object
---

Tricolor marking is the way to describe the state of a [tracing](/tracing-garbage-collection/) mark phase with three colors: *white* objects have not been reached, *gray* objects have been reached but their fields are not yet scanned, and *black* objects have been reached and scanned. Marking turns gray objects black until no gray is left, and then the white objects are [garbage](/garbage/). Dijkstra, Lamport, Martin, Scholten and Steffens introduced it in 1978 to reason about a collector that runs while the program changes the heap. The two *tricolor invariants* say when that is safe, and every [write barrier](/write-barrier/) of an [incremental](/incremental-garbage-collection/) or [concurrent](/concurrent-garbage-collection/) collector keeps one of them.

## In plain words

Think of the marker as a painter. At the start every object is white. The painter paints the objects that the program holds gray, which means "found, but not looked inside". Then, again and again, the painter takes a gray object, paints each white object it points to gray, and paints the object itself black, which means "found and fully looked inside". When no gray object is left, every white object is junk.

This is safe when the program is stopped. If the program runs at the same time, it can hide an object: it can put the only pointer to a white object inside a black one, which the painter never looks at again. The rules below say what the program must do on each pointer write so that this never happens.

## The idea

**The colors.** Let the heap be a directed graph whose nodes are the objects and whose edges are the pointer fields, with a set of root objects. A mark phase gives each object a color:

- **white**: not yet reached; at the end of the phase, a white object is reclaimed;
- **gray**: reached, and its fields still have to be scanned;
- **black**: reached, and all its fields have been scanned.

The mark phase starts with the roots gray and every other object white. One *marker step* takes a gray object $x$, makes each white object that $x$ points to gray (this is called *shading*), and makes $x$ black. The phase ends when no object is gray. In [mark-and-sweep](/mark-and-sweep/) the gray objects are the ones on the mark stack; in [Cheney's collector](/cheney-copying-collector/) they are the objects between the scan and the free pointer. The color is the same idea as the white, gray and black vertices of [breadth-first](/breadth-first-search/) and [depth-first search](/depth-first-search/).

**The invariants.** Let the mutator change the edges between marker steps.

- **Strong tricolor invariant.** No black object points to a white object.
- **Weak tricolor invariant.** Every white object that a black object points to is reachable from some gray object through a path of white objects.

The strong invariant implies the weak one, because its condition is then empty.

**Theorem (safety).** Suppose the roots are not white, and that the weak invariant holds when no object is gray. Then no object reachable from the roots is white.

*Proof.* With no gray object, every object that is not white is black. Assume that some reachable object is white, and take a path from a root to it. The root is not white, so the path has a first white object $w$, and the object $u$ just before $w$ on the path is black. So the black $u$ points to the white $w$. The weak invariant then says that $w$ is reachable from a gray object, but there is none. This is a contradiction. $\square$

When the mutator is stopped, a marker step cannot break the strong invariant: it shades every child of $x$ before it makes $x$ black, and it does not make any other object black. So plain marking ends with no reachable white object.

**The lost object.** A running mutator can break both invariants. An object is lost only if two things happen together (Wilson 1992):

1. the mutator writes a pointer to a white object into a black object, and
2. every path from a gray object to that white object through white objects is destroyed.

The first condition breaks the strong invariant; the two together break the weak one. A barrier prevents one of the two conditions:

- **Incremental update (Dijkstra et al. 1978).** On a write $x.f \leftarrow y$, shade $y$. Then no write makes a black object point to a white one, and the strong invariant holds. Steele's barrier (1975) keeps the same invariant in the other direction: it makes a black $x$ gray again. See [incremental update barrier](/incremental-update-barrier/).
- **Snapshot at the beginning (Yuasa 1990).** On a write $x.f \leftarrow y$, shade the old value of $x.f$. A deleted edge can no longer cut the last white path to an object, and the weak invariant holds. See [snapshot at the beginning](/snapshot-at-the-beginning/).

## Examples

**The lost object, step by step.** The heap has three objects $A$, $B$ and $C$, with two fields each. The root is $A$, and the edges are $A.f = B$ and $B.f = C$. The marker scans $A$ first. Then the mutator runs $A.g \leftarrow C$ and $B.f \leftarrow$ nil, and then the marker continues. There is no barrier.

| step | action | $A$ | $B$ | $C$ | strong | weak |
|---|---|---|---|---|---|---|
| 0 | start: shade the root | gray | white | white | yes | yes |
| 1 | marker scans $A$ | black | gray | white | yes | yes |
| 2 | mutator: $A.g \leftarrow C$ | black | gray | white | no | yes |
| 3 | mutator: $B.f \leftarrow$ nil | black | gray | white | no | no |
| 4 | marker scans $B$ | black | black | white | no | no |

After step 4 no object is gray, so marking ends. The object $C$ is white, but it is reachable through $A.g$, so the sweep frees a live object. In step 2 the pointer from black $A$ to white $C$ breaks the strong invariant, but $C$ is still reachable from gray $B$, so the weak invariant holds. Step 3 removes that last white path.

**The same run with a barrier.**

- With the Dijkstra barrier, step 2 shades $C$ gray. The strong invariant holds at every step; step 4 scans $B$, and one more step scans $C$. Nothing is lost.
- With the Yuasa barrier, step 2 does nothing (the old value of $A.g$ is nil), and step 3 shades the old value $C$ gray. After step 2 the strong invariant fails, but the weak invariant holds at every step, and $C$ ends black.

**All interleavings.** If the marker and the two writes interleave in every possible order, with the marker scanning the gray objects in the order $A$, $B$, $C$, there are 10 runs. Without a barrier, exactly one of them loses $C$: the run of the table, where $A$ is scanned before both writes and $B$ after both. With either barrier, no run loses an object. On 600 random heaps of up to 7 objects with random interleavings, the Dijkstra barrier kept the strong invariant after every step, and the Yuasa barrier kept the weak invariant after every step; without a barrier, some runs lost objects, and every such run broke the weak invariant on the way.

## Where it is used

- **[Incremental](/incremental-garbage-collection/), [concurrent](/concurrent-garbage-collection/) and [on-the-fly](/on-the-fly-garbage-collection/) collectors.** Each one is described by the invariant its barrier keeps. The [incremental update barrier](/incremental-update-barrier/) keeps the strong invariant, the [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier the weak one. A [read barrier](/read-barrier/), as in [Baker's collector](/baker-real-time-collector/), keeps the mutator from ever holding a white object, which is another way to keep the strong invariant.
- **Mutator color.** A collector also gives the mutator a color: a black mutator holds no white references, so its roots need not be scanned again at the end; a gray mutator must be rescanned. This choice decides if the end of a mark phase needs a short [stop-the-world](/stop-the-world-collection/) pause.
- **Allocation color.** New objects can be allocated white, gray or black. A collector with a deletion barrier usually allocates black, because the snapshot does not contain the new objects.
- **Production collectors.** The concurrent mark of the [Garbage-First collector](/garbage-first-collector/) uses a snapshot-at-the-beginning barrier. Many other concurrent markers use an incremental-update barrier.
- **Copying collectors.** In a [copying collector](/copying-collection/), gray objects are the copied objects whose fields still point to from-space, and the queue of [Cheney's algorithm](/cheney-copying-collector/) is the gray set.

## References
