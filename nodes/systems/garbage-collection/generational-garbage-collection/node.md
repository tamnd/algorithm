---
tag: JNBZA2
kind: technique
slug: generational-garbage-collection
name: Generational garbage collection
aliases:
- generational GC
- ephemeral collection
- generation scavenging
area: systems/garbage-collection
level: core
summary: "Split the heap by age. Collect the small young generation often, with old-to-young pointers as extra roots, and the old generation rarely."
prereqs: [generational-hypothesis, copying-collection, gc-roots, write-barrier]
see_also: [remembered-set, card-marking, generational-collector-pause-tradeoff, generational-collector-beltway, train-algorithm, bump-pointer-allocation, garbage-first-collector, cheney-copying-collector]
sources:
  - paper: doi:10.1145/358141.358147
    title: Henry Lieberman and Carl Hewitt, A real-time garbage collector based on the lifetimes of objects, Communications of the ACM 26(6), 419-429, 1983
    locator: the division of the heap into regions by age, with the youngest regions collected most often
  - paper: doi:10.1145/800020.808261
    title: David Ungar, Generation scavenging, a non-disruptive high performance storage reclamation algorithm, ACM SIGSOFT/SIGPLAN Software Engineering Symposium on Practical Software Development Environments, 157-167, 1984
    locator: the scavenger with new space, survivor spaces, tenuring and the remembered set
  - paper: doi:10.1002/spe.4380190206
    title: Andrew W. Appel, Simple generational garbage collection and fast allocation, Software Practice and Experience 19(2), 171-183, 1989
    locator: the nursery that takes all the free space, and the barrier that records stores into old objects
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Chapter 9 (Generational garbage collection), in particular Sections 9.4 to 9.8
  - paper: doi:10.1007/BFb0017182
    title: Paul R. Wilson, Uniprocessor garbage collection techniques, IWMM 1992, LNCS 637, 1-42
    locator: the section on generational garbage collection
---

Generational garbage collection splits the heap by the age of objects. New objects go into a small *young generation* (the *nursery*), which the collector empties often by a fast [copying](/copying-collection/) collection, a *minor collection*. Objects that survive a few minor collections are *promoted* (tenured) to the *old generation*, which is collected rarely, by a *major collection*. The technique pays off when the [weak generational hypothesis](/generational-hypothesis/) holds: then a minor collection finds mostly garbage, and its work is proportional to the few survivors. The price is a [write barrier](/write-barrier/) that records pointers from old objects to young ones in a [remembered set](/remembered-set/), because a minor collection does not look at the rest of the old generation.

## In plain words

Most things that a program makes are thrown away soon. So keep the new things in one small box, and the old things in a large box. When the small box is full, look at it only: find the few things in it that are still in use, move them out, and empty the box in one step. This is fast, because only those few things move. Things that stay in use for a while move to the large box, which you clean only now and then.

One problem remains: an old thing can hold a link to a new thing. If you look only in the small box, you miss that link and throw away something that is still in use. So each time the program stores a link into an old thing, it also writes a note. The notes tell the collector which old things to check.

## When it applies

Use a generational collector when these signals are present.

- **Most objects die young.** The program allocates many temporary objects: strings, boxed numbers, closures, iterators, the nodes of short-lived lists. Then the survivor fraction $\sigma(N)$ of a nursery of $N$ bytes is small, and a minor collection costs about $\sigma(N)$ per allocated byte.
- **Old objects rarely point to new ones.** A pointer from an old object to a young one appears only through a store into an existing old object. Initializing stores into a new object create young-to-young or young-to-old pointers, which need no record. If the program stores young pointers into old objects at a high rate, the remembered set grows and each minor collection must scan it.
- **The runtime controls the stores.** The compiler or the interpreter must run the write barrier on every store of a pointer into the heap. It must also know where the pointers are, so that objects can move: a [precise](/precise-garbage-collection/) collector, or a [mostly-copying](/mostly-copying-collection/) one when the roots are ambiguous.
- **Pause times matter.** A minor collection takes time proportional to the roots, the remembered set and the survivors, so most pauses are short. The rare major collection is still as long as a full collection, unless the old generation uses an incremental scheme such as the [train algorithm](/train-algorithm/) or a [concurrent](/concurrent-garbage-collection/) collector.

It does not help when most objects live long, as in a program that builds one large data structure and keeps it, or when lifetimes follow a memoryless model (see the non-examples in [generational hypothesis](/generational-hypothesis/)).

## The template

The model: a heap of objects with pointer fields. The mutator allocates, stores pointers into fields, and loads them. The young generation holds at most $N$ objects. Each young object has an *age*, the number of minor collections it has survived. An object whose age reaches the *tenuring threshold* $T \ge 1$ is promoted. $R$ is the remembered set: a set of slots $(o, i)$, field $i$ of an old object $o$. The holes of the template are the size $N$, the threshold $T$, the representation of $R$ and the policy of the major collection.

```pseudo id=main
ALLOCATE(k)                                   ▷ a new object with k pointer fields
L1  if the young generation holds N objects then MINOR-COLLECT()
L2  a ← bump-allocate k fields in the nursery; age[a] ← 0
L3  return a

WRITE(src, i, ref)                            ▷ the mutator's store, with the barrier
L4  src.f[i] ← ref
L5  if src is old and ref is young then R ← R ∪ {(src, i)}

MINOR-COLLECT()
L6  Q ← an empty queue
L7  for each root slot r, and each slot (o, i) in R do
L8      if the slot holds a young object y then the slot ← EVACUATE(y)
L9  while Q is not empty do
L10     o ← dequeue Q
L11     for each field i of o that holds a young object y do
L12         o.f[i] ← EVACUATE(y)
L13         if o is old and o.f[i] is young then R ← R ∪ {(o, i)}
L14 free the old copy of the young generation; keep in R only slots that hold young objects
L15 if the old generation is full then MAJOR-COLLECT()

EVACUATE(y)
L16 if y has a forwarding address then return it
L17 age[y] ← age[y] + 1
L18 if age[y] ≥ T then y' ← a copy of y in the old generation      ▷ promotion
L19 else y' ← a copy of y in the survivor space
L20 install the forwarding address y' in y; enqueue y'; return y'
```

**Walk-through.** Allocation is a [bump of a pointer](/bump-pointer-allocation/) in the nursery, often inside a [thread-local allocation buffer](/thread-local-allocation-buffer/), and starts a minor collection when the nursery is full (lines L1 to L3). The barrier of line L5 runs on each pointer store and records the slots of old objects that now hold young pointers. A minor collection is a [Cheney](/cheney-copying-collector/) copy of the young generation. Its roots are the root slots and the remembered slots (lines L7 and L8). The scan of lines L9 to L13 copies everything young that the copies reach. Line L13 records the fields of newly promoted objects that point to young survivors: without it, the next minor collection misses those pointers. Old objects are never traced by a minor collection: a pointer to an old object is left as it is. The major collection (line L15) collects both generations, for example by [mark-sweep](/mark-and-sweep/) or [mark-compact](/mark-compact/), and then rebuilds $R$.

### Example

Run the template with $N = 4$ and $T = 2$. Objects are numbered in allocation order.

| step | action | young generation (age) | old | $R$ |
|---|---|---|---|---|
| 1 | allocate 0, 1, 2; store 0.f[0] ← 1; drop the roots of 1 and 2 | 0 (0), 1 (0), 2 (0) | | |
| 2 | allocate 3 | 0, 1, 2, 3 (all age 0) | | |
| 3 | allocate 4: the nursery is full, minor collection 1 | 0 (1), 1 (1), 3 (1) | | |
| 4 | object 4 is allocated after the collection; drop the root of 3 | 0 (1), 1 (1), 3 (1), 4 (0) | | |
| 5 | allocate 5: minor collection 2 | 4 (1) | 0, 1 | |
| 6 | object 5 is allocated | 4 (1), 5 (0) | 0, 1 | |

Collection 1 starts from the roots of 0 and 3, reaches 1 through 0, and copies 3 objects; object 2 is garbage and costs nothing. Collection 2 copies 0, 1 and 4. Objects 0 and 1 reach age 2 and are promoted; 3 is garbage. The pointer from 0 to 1 is now old-to-old, so $R$ stays empty. Two collections copied 6 objects and promoted 2. Had object 0 been promoted alone while 1 stayed young, line L13 would have put $(0, 0)$ into $R$.

### Why a minor collection is safe

**Invariant.** Outside a collection, every slot of an old object that holds a young object is in $R$. Line L5 keeps it on each store. At a collection, line L13 adds the slots of the objects promoted in it, and line L14 removes only slots that no longer hold young objects.

**Claim.** If the invariant holds when MINOR-COLLECT starts, then every young object that is reachable from the roots is copied, and every pointer to it from a root, from an old object or from another copied object is updated.

*Proof.* Let $y$ be young and reachable, by a path $r \to x_1 \to \cdots \to x_m = y$ from a root slot $r$. If no $x_j$ is old, then $x_1$ is young and is evacuated at line L8. Otherwise let $x_j$ be the last old object on the path. The edge $x_j \to x_{j+1}$ is a slot of an old object that holds a young object, so it is in $R$ by the invariant, and $x_{j+1}$ is evacuated at line L8. In both cases the rest of the path is young. Each evacuated object is enqueued once (line L20) and dequeued once, and line L12 evacuates each young object that it points to. By induction along the path, $y$ is evacuated. The pointers to $y$ from roots and from slots in $R$ are updated at line L8, and those from copied objects at line L12. Old objects that point to $y$ through a slot not in $R$ do not exist, by the invariant. $\blacksquare$

The converse does not hold: a slot in $R$ can belong to an old object that is itself garbage. Its young targets survive anyway. This is floating garbage, which the next major collection removes.

### Cost

Let $\rho$ be the number of root slots, $|R|$ the size of the remembered set, and $s$ the total size of the young survivors. A minor collection takes $O(\rho + |R| + s)$ time in the worst case. It does not depend on the size of the old generation or on the number of dead young objects. With one object allocated per step and a lifetime survival function $S$, a nursery of $N$ objects has $\sum_{a<N} S(a)$ expected survivors, which is the $s$ above in expectation (see [pause time and nursery size](/generational-collector-pause-tradeoff/) for the exact model). A major collection costs as much as a full collection of the heap. The barrier adds a test, and sometimes a store, to each pointer store of the mutator.

## Classic examples

- **Generation scavenging (Ungar, 1984).** Berkeley Smalltalk kept new objects in a new space with survivor spaces, promoted objects by age and recorded old objects that pointed to new ones in a remembered set of objects. This is the template with an object-precise $R$.
- **Remembered sets and card tables.** The two common forms of $R$: a [remembered set](/remembered-set/) of slots or objects, often filled through a sequential store buffer, and a [card table](/card-marking/) that marks regions of the old generation as dirty.
- **The HotSpot young generation.** An eden and two survivor spaces, an age per object, a tenuring threshold and a card table for $R$. Allocation is by [thread-local allocation buffers](/thread-local-allocation-buffer/).
- **Garbage-First.** [G1](/garbage-first-collector/) splits the heap into regions, keeps one remembered set per region and collects the young regions at each pause, together with a few old regions that hold much garbage.
- **Mature-space collectors.** The [train algorithm](/train-algorithm/) collects the old generation in small steps, and [Beltway](/generational-collector-beltway/) generalizes the generations into belts of increments.

## Variations

- **En-masse promotion ($T = 1$).** Promote every survivor of a minor collection. No survivor space is needed, but objects that are allocated just before a collection are promoted with almost no time to die.
- **Aging and survivor spaces ($T > 1$).** Keep survivors in the young generation for a few collections. Fewer objects are promoted that die soon after, but a survivor is copied up to $T$ times. HotSpot adjusts the threshold from the survivor space occupancy.
- **Appel-style nursery.** The nursery takes all the space that the old generation does not use, and shrinks as the old generation grows. A minor collection then runs as rarely as possible.
- **More than two generations.** Each generation is collected more often than the one above it, and a pointer from any older generation to a younger one is remembered.
- **Non-copying generations.** A generation can be a set of objects with an age bit, collected by mark-sweep in place. This is the "sticky mark bits" scheme, also used by conservative collectors such as the [Boehm-Demers-Weiser collector](/boehm-gc/), which finds the old objects that changed from virtual memory dirty bits.
- **Pretenuring.** Allocate objects that are known to live long, such as large arrays or objects from an allocation site that always survives, directly in the old generation.

## Pitfalls

- **A missing barrier.** A store that skips line L5, for example in native code, an intrinsic or a bulk array copy, leaves an old-to-young pointer out of $R$. The next minor collection frees a live object, and the old object then holds a dangling pointer.
- **Forgetting promoted objects.** If line L13 is missing, an object promoted in this collection that points to a young survivor is not in $R$. The error shows only at the next minor collection.
- **Nepotism.** A dead old object that is in $R$ keeps its young targets alive. They are promoted and can keep more young objects alive at the next collection. Only a major collection breaks the chain.
- **Premature tenuring.** A small nursery or a low $T$ promotes objects that die soon after. They fill the old generation and make major collections more frequent. The [pause-time model](/generational-collector-pause-tradeoff/) gives the exact rate.
- **A remembered set that grows without limit.** A program that stores young pointers into a large old array at a high rate makes $R$ large. Cards, a filter for duplicate entries, or a promotion of the targets bound the cost.
- **Assuming the old generation is never collected.** Old objects die too. A collector that never runs a major collection runs out of memory.

## Exercises

1. Redo the example with $T = 1$. Which objects are promoted, when does the second minor collection run, and what happens to object 3?
2. Prove that line L14 never removes a slot that the invariant needs.
3. Give a mutator trace in which a garbage old object keeps a young object alive for three minor collections in a row.

## References
