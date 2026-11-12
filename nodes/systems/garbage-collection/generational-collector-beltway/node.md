---
tag: WR1XXS
kind: algorithm
slug: generational-collector-beltway
name: Beltway collector
aliases:
- Beltway
- Beltway garbage collection framework
area: systems/garbage-collection
level: research
summary: "A copying collector framework: increments are grouped in FIFO belts and collected one at a time, which gives semi-space, generational and older-first collectors as configurations."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {k: the most objects in an increment, p: the most pointer fields in an object, r: the number of roots, E: the remembered slots of the collected increment, M: the remembered slots in all increments, I: the number of increments}
  time: {worst: O(r + E + k p), best: Θ(1)}
  space: {extra: O(M + I)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2002
  people: [Stephen M. Blackburn, Richard Jones, Kathryn S. McKinley, J. Eliot B. Moss]
  note: Blackburn, Jones, McKinley and Moss presented Beltway at PLDI 2002, implemented in the Jikes RVM for Java, together with the new configurations Beltway X.X and X.X.100.
prereqs: [generational-garbage-collection, train-algorithm]
see_also: [copying-collection, remembered-set, write-barrier, generational-hypothesis, generational-collector-pause-tradeoff, incremental-garbage-collection, garbage-first-collector]
sources:
  - paper: doi:10.1145/512529.512548
    title: Stephen M. Blackburn, Richard Jones, Kathryn S. McKinley and J. Eliot B. Moss, Beltway, getting around garbage collection gridlock, PLDI 2002, 153-164
    locator: Section 2.2 (belts and increments), Section 3.1 (BSS, BA2, BOFM and BOF), Section 3.2 (Beltway X.X and X.X.100, and completeness), Section 3.3 (the frame-based unidirectional write barrier, remembered sets, collection triggers and the copy reserve)
  - paper: doi:10.1145/320384.320425
    title: Darko Stefanovic, Kathryn S. McKinley and J. Eliot B. Moss, Age-based garbage collection, OOPSLA 1999, 370-381
    locator: the older-first collector, whose window over the heap Beltway models with two belts
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 9.11, Beltway
---

Beltway is a framework for copying collectors. The heap is divided into *increments*, regions that can be collected one at a time, and the increments are grouped into *belts*, queues in first-in, first-out order. The collector always takes the oldest increment of the lowest belt that is not empty. Survivors go to the youngest increment of the next belt, or, on the top belt, to the youngest increment of the same belt. The number of belts and the size of the increments on each belt are parameters, and the known copying collectors are settings of these parameters: one belt with one increment is a semi-space collector, two belts with one increment each is Appel's [generational collector](/generational-garbage-collection/), and one belt of many small increments is close to the older-first collector. The cars of the [train algorithm](/train-algorithm/) are increments too. Blackburn, Jones, McKinley and Moss used the framework to build new collectors that do better than any of these.

## In plain words

Picture the heap as a few conveyor belts. Each belt carries boxes, and each box holds objects. New objects go into the last box of the bottom belt. When memory is full, the collector takes the front box of the lowest belt that has boxes. It keeps the objects in that box that are still in use, puts them in the last box of the next belt up, and throws the box away.

On the top belt, the kept objects go to the back of the same belt. The collector only ever looks at one box at a time, so each pause is short. By choosing how many belts there are and how big their boxes are, the same machine acts like many different collectors.

## The problem

Collect a heap of copied objects with work per collection that is bounded by a parameter, the size of an increment, and exploit object age: collect young objects often, collect old objects rarely, and give each object some time to die before it is examined. The collector must free only garbage. A good configuration should also be *complete*: every garbage object, including garbage cycles that span increments, should be freed after a finite number of collections.

## The algorithm

Each increment has a key $(\text{belt}, \text{creation number})$, so the oldest increment of the lowest belt has the smallest key. The barrier remembers only the pointers whose target increment has a smaller key than their source increment: those targets are collected first, and a pointer the other way is not needed, because its source is collected before its target.

```pseudo id=main
COLLECT()
L1  c ← the nonempty increment with the smallest key
L2  d ← the belt above the belt of c, or the belt of c if it is the top belt
L3  for each root and each remembered slot of c that points to an object x in c do EVACUATE(x)
L4  for each copied object o, in the order of copying, and each field i of o do
L5      if o.f[i] is in c then EVACUATE(o.f[i])
L6      RECORD(o, i)
L7  RECORD each remembered slot of c again, since its target has moved
L8  free c, the objects still in it, and its remembered set

EVACUATE(x)
L9  if x is still in c then
L10     copy x to the youngest increment of belt d, or to a new increment at the end of d if that one is full or is c

WRITE(s, i, v)
L11 s.f[i] ← v; RECORD(s, i)

RECORD(s, i)                                 ▷ the unidirectional write barrier
L12 if s.f[i] lies in another increment with a smaller key than the increment of s then add (s, i) to its remembered set

ALLOCATE()
L13 while the heap is full, or the nursery trigger asks for it, do COLLECT()
L14 put the new object in the youngest increment of belt 0, or in a new increment if that one is full
```

Lines L3 to L6 are a [Cheney](/cheney-copying-collector/) scan restricted to $c$: the roots and the [remembered set](/remembered-set/) of $c$ give the starting objects, and the copies are scanned in order. Line L6 runs the barrier again for each copied object, because its key changed. A copied object has moved to an increment with a larger key, so the slots that point to it may now be remembered, which line L7 handles.

The heap holds at most $U$ objects of usable memory, and copying needs a *copy reserve* outside $U$ as large as the largest increment that can be collected. The paper computes this reserve dynamically. The configurations below give each belt a maximum increment size, as a percentage of $U$:

| configuration | belts | behaviour |
|---|---|---|
| BSS | one belt, increments of 100% | semi-space: the whole heap is one increment, collected when full |
| BA2 | two belts, 100% and 100% | Appel's collector: the nursery takes all free space, and the old belt is collected when it fills the heap |
| Beltway X.X | two belts, X% and X% | an incremental generational collector; BA2 is the case $X = 100$ |
| Beltway X.X.100 | three belts, X%, X% and 100% | X.X with a third belt that is collected whole, and so complete |
| BOF, BOFM | one or two belts of small increments | older-first: a window of older objects is collected, and the youngest objects get time to die |

## Example

Beltway X.X with $U = 8$ and increments of 2 objects. The mutator dropped its last reference to a ring of three objects, $a \to b \to c \to a$, which sits on belt 1 in increments $I_1 = [a, b]$ and $I_2 = [c]$. The slot $c.f_0$ points from $I_2$ to $I_1$, which has the smaller key, so it is in the remembered set of $I_1$. The tests run this example.

| step | collected | action | belt 1 after |
|---|---|---|---|
| 1 | $I_1$ | $a$ is remembered from $c$; it goes to $I_2$, which has room. Then $b$ follows $a$, into a new increment $I_3$ | $I_2 = [c, a]$, $I_3 = [b]$ |
| 2 | $I_2$ | $c$ is remembered from $b$, and $a$ follows $c$ | $I_3 = [b, c]$, $I_4 = [a]$ |
| ... | | the ring always spans two increments | forever |

This is why Beltway X.X is not complete. Each increment holds a part of the ring, and that part is referenced from a later increment, so it always survives. Beltway X.X.100 adds a third belt with one increment of up to 100%:

| step | collected | action | after |
|---|---|---|---|
| 1 | $I_1$ | $a$ and $b$ survive and go up to belt 2 | belt 1: $I_2 = [c]$; belt 2: $[a, b]$ |
| 2 | $I_2$ | $c$ is remembered from $b$ and goes up | belt 1 is empty; belt 2: $[a, b, c]$ |
| 3 | belt 2 | the lower belts are empty, so this is the whole heap; no root points into it | the heap is empty |

## Correctness

**Safety.** The increment $c$ has the smallest key of all nonempty increments, so every pointer into $c$ from another increment comes from a larger key and is remembered, by the barrier and lines L6 and L7. Take a reachable object $z$ in $c$ and a path from a root to $z$. The first object of the path in $c$ is pointed to by a root or by a remembered slot, so line L3 copies it, and each later object of the path in $c$ is pointed to by such an object or by a copied object, which lines L4 and L5 handle. So line L8 frees only garbage.

**Completeness of X.X.100.** The top belt has at most one increment between collections, since its collection copies into a new one and frees the old one. When the lower belts are empty, that increment is the whole heap, and lines L3 to L8 are a full copying collection, which frees all garbage. If the mutator stops allocating, each collection of a lower belt moves its survivors up a belt, so the lower belts empty after finitely many collections. Beltway X.X with $X < 100$ has no belt that is collected whole, and the example shows a cycle that it never frees. The proof file below has the details.

## Complexity

A collection handles the roots, the remembered slots of $c$ and the objects of $c$: $O(r + E + k p)$ time, where $k$ is the increment size, independent of the size of the heap. The cost of the barrier is $O(1)$ per pointer store. Beltway uses aligned *frames* of virtual memory, one per increment, so that the barrier finds the increment of an address with a shift, and each frame carries its collection order. Space: the remembered sets, one per target and source frame pair in the paper, plus the copy reserve. In X.X.100 the reserve grows to half the heap only when the top belt is nearly full.

## Properties

- **Copying.** Every survivor moves, so the pointers must be known precisely.
- **Incremental.** Each collection is bounded by the size of an increment, except for collections of a belt with increments of 100%.
- **Generational.** Lower belts hold younger objects and are collected more often.
- **Complete only in some configurations.** BSS, BA2 and X.X.100 are complete; X.X with $X < 100$ and the older-first configurations are not.

## Variants and improvements

- **Collection triggers.** The *nursery trigger* limits the nursery to one increment of at most $X\%$, and collects it when it is full. A *remembered-set trigger* collects when the remembered sets grow too large. A *time-to-die trigger* starts a second nursery increment shortly before the heap is full, so that the youngest objects are not collected at once. The paper measured only the nursery trigger.
- **Single nursery increment.** The barrier also ignores pointers whose source is in the nursery, which saves barrier work for initializing stores.
- **A mature object space as the top belt.** The paper suggests a [train](/train-algorithm/) collector in place of the third belt, to be both incremental and complete.
- **Region collectors.** [Garbage-First](/garbage-first-collector/) and similar collectors also collect the heap in independent regions with remembered sets, but they choose the regions by the amount of garbage, not in a fixed order.

## When to use it

Beltway is a research framework for exploring copying collectors, built in the Jikes RVM. Its results apply to any copying generational collector: in the paper, the new configurations gave total execution times up to 40% better, and on average 5% to 10% better, than the best generational copying collector the authors knew, for small to moderate heap sizes. The gain comes from less copying and a better use of the heap, because the copy reserve is smaller. It suits managed runtimes that copy objects and can afford a write barrier. It does not apply where pointers are not known precisely, such as for C programs, where a [conservative](/conservative-garbage-collection/) collector is needed.

## Pitfalls

- **Incompleteness.** A configuration in which no belt is ever collected whole can keep a garbage cycle forever. The tests show this for X.X.
- **The copy reserve.** A collection copies up to a whole increment, so space for the largest increment that can be collected must be kept free. A fixed reserve of half the heap wastes memory; the reserve must be computed from the increments that can still be collected.
- **Bidirectional remembering.** Remembering all pointers between increments is correct but wasteful. Only pointers to increments with an earlier collection order are needed, and the order must be the true order of collection.
- **Barrier work in the nursery.** Pointer stores into new objects are the most frequent stores, and recording them is costly.

## Implementations

## History

Generational collection divides the heap by age, and Appel's collector of 1989 gives the nursery all free memory. Hudson and Moss's mature object space of 1992 collects the old space in cars, and Stefanovic, McKinley and Moss studied older-first collection in 1999. Blackburn, Jones, McKinley and Moss presented Beltway at PLDI 2002, and showed that one framework with belts and increments describes all of these copying collectors and new ones.

## References
