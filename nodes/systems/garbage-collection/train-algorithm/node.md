---
tag: GG2PBV
kind: algorithm
slug: train-algorithm
name: Train algorithm
aliases:
- Hudson-Moss train collector
- mature object space collector
- MOS collector
area: systems/garbage-collection
level: research
summary: "Collect the old generation one fixed-size car at a time. Move live objects to the train that refers to them, so a garbage cycle ends up in one train and is freed whole."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {k: the number of objects in a car, p: the most pointer fields in an object, r: the number of roots, E: the remembered slots that point into the lowest train, M: the remembered slots in all cars, C: the number of cars}
  time: {worst: O(r + E + k p), best: Θ(1)}
  space: {extra: O(M + C)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1992
  people: [Richard L. Hudson, J. Eliot B. Moss]
  note: Hudson and Moss presented the mature object space collector, now called the train algorithm, at IWMM 1992. Seligmann and Grarup implemented it in 1995 and repaired a gap in its argument for completeness.
prereqs: [generational-garbage-collection, remembered-set, copying-collection]
see_also: [generational-collector-beltway, incremental-garbage-collection, garbage-first-collector, write-barrier, generational-collector-pause-tradeoff, cheney-copying-collector]
sources:
  - paper: doi:10.1007/BFb0017203
    title: Richard L. Hudson and J. Eliot B. Moss, Incremental collection of mature objects, IWMM 1992, LNCS 637, 388-403
    locator: the cars and trains, the remembered sets from higher to lower cars, the rules for moving objects out of the lowest car, and the freeing of a train with no outside references
  - paper: doi:10.1007/3-540-49538-X_12
    title: Jacob Seligmann and Steffen Grarup, Incremental mature garbage collection using the train algorithm, ECOOP 1995, LNCS 952, 235-252
    locator: the first implementation, in the Mjolner BETA system, and the repair for futile collections that keeps an outside reference as an extra root
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 10.2, Topological collectors, Mature Object Space garbage collection
---

The train algorithm collects the old generation of a [generational collector](/generational-garbage-collection/) in small steps of bounded size. The old space is cut into *cars*, blocks of a fixed size, and the cars are grouped into *trains*. Cars are ordered: by train, then by position in the train. Each step collects only the lowest car. It moves the live objects of that car out, to the train that refers to them, and frees the car. Each car has a [remembered set](/remembered-set/) of the slots in later cars that point into it, so a step needs no scan of the rest of the heap. A plain car-by-car collector would never free a garbage cycle that spans cars; the trains fix this. Objects that refer to each other are moved into the same train, and when the lowest train has no references from outside, the whole train is freed at once, with every cycle in it.

## In plain words

Picture the old part of the heap as a row of trains. Each train is a line of small cars, and each car holds a few objects. The collector always looks at the first car of the first train, and only at that car, so each step is short.

For each object in that car, it asks who points to it. If something outside the first train points to it, the object moves to the back of that other train. If something later in the same train points to it, it moves to the back of its own train. If nothing points to it, it is garbage. Then the car is empty and goes away.

Objects that point to each other end up in the same train. When nothing outside the first train points into it, the whole train is garbage, and the collector frees it in one step.

## The problem

Collect the old generation incrementally, with a bounded amount of work per step, and be *complete*: every garbage object, including those in cycles that span many steps' worth of memory, must be freed after some number of steps. The mutator runs between steps, stores pointers, and promotes new objects into the old space. The input of a step is the heap, the roots (which include the young generation), and the remembered sets; the output is the heap with some garbage freed.

## The algorithm

Cars have a key $(\text{train}, \text{position})$, and the *lowest* car is the one with the smallest key. The write barrier records a slot $(s, i)$ in the remembered set of the car of $s.f_i$ when that car comes before the car of $s$. New objects are never placed in the lowest train.

```pseudo id=main
COLLECT()                                   ▷ one step
L1  t ← the lowest train; c ← the lowest car of t
L2  if no root, no extra root and no slot outside t points into t then
L3      free every car of t; return
L4  for each root or extra root that points to an object x in c do MOVE(x, a later train)
L5  for each remembered slot of c in another train u, pointing to x do MOVE(x, u)
L6  for each remembered slot of c in a later car of t, pointing to x do MOVE(x, t)
L7  for each moved object o, in the order of moving, and each field i of o do
L8      if o.f[i] is in c then MOVE(o.f[i], the train of o)
L9      RECORD(o, i)
L10 free c, with the objects that are still in it
L11 if t lost no object then keep one outside reference into t as an extra root
L12 else drop the extra roots

MOVE(x, u)
L13 if x is still in c then
L14     append x to the last car of u, or to a new car at the end of u if that car is full

WRITE(s, i, v)                              ▷ the mutator's store
L15 s.f[i] ← v; RECORD(s, i)

RECORD(s, i)                                ▷ the write barrier
L16 if s.f[i] lies in a car before the car of s then add (s, i) to the remembered set of that car
```

Line L2 is the train test: references into $t$ from outside can only come from the roots or from later trains, and the remembered sets hold the latter. If there are none, nothing in $t$ is reachable, and line L3 frees all of it, cycles included. Otherwise the step works on the lowest car $c$. Objects referenced from roots move to a later train, a new one if $t$ is the last (line L4). Objects referenced from another train $u$ move to the end of $u$ (line L5), and those referenced only from later in $t$ move to the end of $t$ (line L6). Lines L7 to L9 are a [Cheney](/cheney-copying-collector/) scan of the moved objects: what they reach in $c$ follows them into the same train, and their fields are recorded again at their new place. The slots of the remembered set of $c$ are also recorded again, since their targets moved. What is left in $c$ is garbage (line L10). The remembered set of $c$ goes with it.

Lines L11 and L12 are the repair of Seligmann and Grarup. A step is *futile* if the train $t$ loses no object: nothing was freed and nothing left $t$. Then the step keeps one reference into $t$ from outside as an *extra root*, held by the collector, until a step makes progress. An extra root that came from a slot in train $u$ is moved to $u$ when its car comes up; one that came from a root goes to a later train.

## Example

Cars hold 3 objects. Train 1 has car 1 with $a, b, w$ and car 2 with $x, y$. Train 2 has car 3 with $e$. The root points to $a$. The slots are $e.f_0 \to b$, $w.f_0 \to x$, $x.f_0 \to y$, $y.f_0 \to x$ and $x.f_1 \to b$. The remembered set of car 1 is $\{(e, 0), (x, 1)\}$: both sources are in later cars. The slot $w.f_0$ points forward and is not recorded. The tests run this example.

| step | lowest car | action | after |
|---|---|---|---|
| 1 | car 1 | outside refs exist (root to $a$, $e$ to $b$). L4: $a$ to train 2, into car 3. L5: $e.f_0$ is in train 2, so $b$ goes to train 2, car 3. L6: $x.f_1$ points to $b$, which has moved. L10: $w$ is freed | train 1: car 2 $[x, y]$; train 2: car 3 $[e, a, b]$ |
| 2 | car 2 | no root and no slot outside train 1 points into it ($w$ is gone, and $x.f_1 \to b$ points forward) | train 1 is freed: $x$ and $y$, a cycle |
| 3 | car 3 | the root points to $a$, and train 2 is the last train: $a$ goes to a new train 3. Nothing else refers to $e$ or $b$ from outside car 3 | $e$ and $b$ are freed; train 3: car 4 $[a]$ |

Step 2 is the point of the trains: the cycle $x \leftrightarrow y$ is freed at once. A collector that only ever looked at single cars would see the slot $x.f_0$ from a later car each time it looked at the car of $y$, and keep the cycle forever.

## Correctness

**Safety.** Before a step, every slot whose target lies in an earlier car than its source is in the remembered set of the target's car; the barrier and line L9 keep this. Let $z$ be reachable. If $z$ is in $t$, take a path from a root to $z$ and the first object on it in $t$: its predecessor is a root, or an object in a later train, whose slot is remembered. So line L2 does not free $t$. If $z$ is in $c$, take the first object of the path in $c$: its predecessor is a root, an extra root, or an object outside $c$, which lies in a later car, so its slot is remembered and lines L4 to L6 move the target. Each later object of the path in $c$ is reached either from a moved object, which lines L7 and L8 handle, or again from outside $c$. So every reachable object of $c$ is moved before line L10.

**Completeness.** Every garbage object is freed after finitely many steps, if steps keep running and the collector only places new objects in trains after the lowest. Objects never enter the lowest train from outside it, so every step that is not futile shrinks it. After a futile step, the extra root $x$ sits in a later car of $t$, and each step frees the lowest car, while new cars are added behind; so within a bounded number of steps the car of $x$ is the lowest, and $x$ leaves $t$. So $t$ is gone after finitely many steps. A garbage object only moves to a train that already holds garbage of the same structure, so the highest train that holds the structure never grows, and the structure is freed when that train is the lowest. The full proof is in the proof file below.

## Complexity

One step of lines L4 to L12 handles the roots, the remembered slots of $c$, and the objects of one car: $O(r + E + k p)$ time, where $E$ bounds the remembered slots into the lowest train. The test of line L2 needs the references into the whole train $t$; implementations keep a count per train, so that it is $O(1)$ amortized over the barrier work. The pause therefore does not depend on the size of the old generation. Space: one remembered set per car, $O(E_{total})$ entries, plus the car table. Popular objects, with many references, make $E$ large, and so make the step long.

## Properties

- **Incremental.** Each step is bounded by the car size, the roots and the remembered slots of one car.
- **Complete.** With the repair for futile steps, every garbage object, cyclic or not, is freed after finitely many steps.
- **Copying.** Live objects move, which compacts the old space but needs precise knowledge of pointers.
- **Not real-time.** A step is short but not bounded by a constant, because of the roots and of popular objects, and the time until a given piece of garbage is freed has no useful bound.

## Variants and improvements

- **Futile collections.** Seligmann and Grarup's extra root, used here, is one repair; another is to start a new train for objects referenced from roots only when the current one makes progress.
- **Popular objects.** An object with many references inflates the remembered set of its car. Implementations give it a car of its own and move the car as a whole, by relinking it, not by copying.
- **Trains in HotSpot.** The HotSpot virtual machine shipped a train collector as an optional incremental old generation, and later removed it in favour of concurrent collectors.
- **Beltway.** [Beltway](/generational-collector-beltway/) has the same increments collected in FIFO order, and treats the train algorithm as one of its configurations, with a belt of trains for the oldest objects.
- **Garbage-First.** [G1](/garbage-first-collector/) also collects the old space in regions with per-region remembered sets, but it chooses the regions by the garbage they hold, and finds that garbage by a concurrent mark, not by train order.

## When to use it

Use the train algorithm when the old generation is large and its collection must not cause long pauses, and when the system can afford a write barrier and remembered sets for many small regions. It needs a copying collector with precise pointer information. It is a poor choice when objects are very popular, when the mutator writes many pointers across cars, or when the time until garbage is reclaimed matters, because a garbage structure can wait a long time before its train comes up. Concurrent collectors such as [Garbage-First](/garbage-first-collector/) replaced it in practice.

## Pitfalls

- **Futile steps.** Without the extra root of line L11, a mutator that keeps its references into the lowest train out of the lowest car makes every step move objects to the end of the same train. The train is never freed, and garbage in the trains behind it is never reached. The tests build such a mutator.
- **Allocating into the lowest train.** If promoted objects can go into the lowest train, it can grow forever and completeness is lost.
- **Remembering only cross-train slots.** Slots from later cars of the same train must also be remembered; otherwise line L6 misses objects referenced from later in $t$, and frees them.
- **Stale entries.** A remembered slot can be overwritten, or its object freed or moved. Check that the slot still points into the car before using it.
- **Popular objects.** One object referenced from millions of slots makes one step take as long as a full collection.

## Implementations

## History

Hudson and Moss presented the algorithm in 1992 as the mature object space collector, to bound the pauses of the old generation in a generational system. Seligmann and Grarup made the first implementation, in the Mjolner BETA system in 1995, and found that the original argument for completeness has a gap: a mutator can make every collection futile. They added the extra root that this page uses. The collector was used in early versions of the HotSpot Java virtual machine. Blackburn, Jones, McKinley and Moss generalized its increments in Beltway in 2002.

## References
