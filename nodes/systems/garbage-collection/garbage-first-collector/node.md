---
tag: CWW6G2
kind: algorithm
slug: garbage-first-collector
name: Garbage-First collector
aliases:
- G1
- G1GC
- Garbage-First garbage collection
area: systems/garbage-collection
level: advanced
summary: "A region-based collector. Remembered sets let it collect any set of regions; concurrent SATB marking counts live data, and each pause takes the regions with the most garbage per cost."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {L: the live words in the collection set (the time bounds are for one pause), p: the pointer fields per object, E: the remembered set entries of the collection set, r: the roots, n: the objects in the heap, M: all remembered set entries}
  time: {worst: O(L p + E + r), best: Θ(r)}
  space: {extra: O(n + M)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2004
  people: [David Detlefs, Christine H. Flood, Steven Heller, Tony Printezis]
  note: Detlefs, Flood, Heller and Printezis cut the heap into equal regions with a remembered set each, so that any set of regions can be evacuated in a pause. Concurrent marking finds the garbage in each region, and each pause picks the regions with the most garbage per cost that fit a pause goal.
prereqs: [concurrent-garbage-collection, snapshot-at-the-beginning, remembered-set, generational-garbage-collection]
see_also: [card-marking, write-barrier, parallel-garbage-collection, shenandoah-collector, z-garbage-collector, train-algorithm, knapsack-problem, fractional-knapsack]
sources:
  - paper: doi:10.1145/1029873.1029879
    title: "David Detlefs, Christine Flood, Steve Heller and Tony Printezis, Garbage-first garbage collection, ISMM 2004, 37-48"
    locator: Regions and remembered sets, concurrent marking with a snapshot-at-the-beginning barrier, evacuation pauses, the choice of the collection set from a model of the pause time, and the young and partially young modes
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: The sections on Garbage-First and on snapshot-at-the-beginning barriers
  - url: https://openjdk.org/jeps/248
    title: "JEP 248: Make G1 the Default Garbage Collector"
    locator: G1 becomes the default collector of the HotSpot JVM in JDK 9
---

Garbage-First, or G1, is a collector for large heaps by Detlefs, Flood, Heller and Printezis (2004). It cuts the heap into many regions of equal size. Each region has a [remembered set](/remembered-set/) of the places outside it that point into it, kept up to date by a post-write barrier. With these sets, a pause can evacuate *any* set of regions, the *collection set*: it copies the live objects of those regions from the roots and the remembered sets, and frees the regions. Young regions are always in the collection set, which makes G1 [generational](/generational-garbage-collection/). [Concurrent marking](/concurrent-garbage-collection/) with a [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier counts the live data of each old region; after it, the pauses add the old regions with the most garbage per unit of predicted cost, while the predicted pause stays under a goal. The name says it: garbage first. G1 has been the default collector of the HotSpot JVM since JDK 9.

## In plain words

The heap is cut into many boxes of equal size. For each box, the collector keeps a list of the places in other boxes that point into it.

New objects go into a few fresh boxes. In a short stop, the collector copies the objects of those boxes that are still in use to an empty box, and the fresh boxes are free again. The lists tell it which objects are in use without a look at the whole heap.

From time to time, a helper thread runs beside the program and finds out how much of each old box is still in use. After that, each stop also takes some old boxes: first those with the most garbage for the least work, until the time set aside for the stop is used up.

## The problem

**Heap model.** The heap is a row of regions of $R$ words. An object has a size of at most $R$ words and some pointer fields. A region is free, young (new objects go there) or old (copies go there). The mutator holds a fixed set of root registers and allocates, loads, stores and copies registers. A store runs the write barriers of the page.

**Costs.** The pause time of a collection set is predicted by a linear model: each region costs a fixed amount, plus an amount per remembered set entry to scan, plus an amount per live word to copy. G1 fits the factors to the measured past pauses; the model here uses fixed factors.

**Goal.** Reclaim the unreachable objects while each pause stays near a goal set by the user. Within a pause, reclaim as much garbage as the goal allows.

## The algorithm

$\textit{RS}(c)$ is the remembered set of region $c$, a set of slots $(x, f)$. *TAMS*, the top at mark start, is the end of the used part of each region when marking starts; objects above it are new and count as live.

```pseudo id=main
WRITE(x, f, y)                                 ▷ the mutator stores y into x.f
L1  if marking and x.f ≠ nil then log x.f in the SATB queue          ▷ pre-write barrier
L2  x.f ← y
L3  if y ≠ nil and region(y) ≠ region(x) then add (x, f) to RS(region(y))   ▷ post-write barrier

MARK-STEP()                                    ▷ the concurrent marking thread
L4  take a from the SATB queue, else from the mark stack; if a is below TAMS and not marked then mark a and push its fields

PAUSE()                                        ▷ an evacuation pause; the mutator is stopped
L5  CS ← all young regions; t ← their predicted cost
L6  for each old region r in decreasing order of garbage(r) / cost(r) do
L7      if t + cost(r) > budget then stop
L8      CS ← CS ∪ {r}; t ← t + cost(r)
L9  for each root s that points into CS do s ← EVACUATE(s)
L10 for each region c in CS and each (x, f) in RS(c) with x outside CS do
L11     if x.f points into c then x.f ← EVACUATE(x.f)
L12 while the copy queue is not empty do x ← DEQUEUE()
L13     for each field f of x: if x.f is in CS then x.f ← EVACUATE(x.f); if x.f is in another region then add (x, f) to RS(region(x.f))
L14 free every region of CS

EVACUATE(a)
L15 if a is forwarded then return its new address
L16 copy a to a free region, forward a to the copy, enqueue the copy, return the copy
```

**Marking.** Marking starts with a snapshot of the roots and sets TAMS in every region. The pre-write barrier at line L1 logs each pointer that a store overwrites, so every object reachable at the start is marked, as in [snapshot-at-the-beginning](/snapshot-at-the-beginning/). A short *remark* pause drains the queues. In the *cleanup*, the live words of each old region are the marked words below TAMS plus all words above it, regions with no live data are freed at once, and the others get $\textit{garbage}(r) = \textit{used}(r) - \textit{live}(r)$.

**Pauses.** Lines L5 to L8 choose the collection set. Young regions are always in it; old regions are added only after a marking has counted their garbage, in decreasing order of garbage per cost, until the next one would pass the budget. Lines L9 to L13 are a [Cheney](/cheney-copying-collector/) copy from two kinds of roots: the registers, and the slots outside the collection set that the remembered sets list. A slot is checked at line L11 before it is used, since a remembered set may hold slots that no longer point into the region. A copy in a new region gets remembered set entries for its own pointers at line L13, and a slot fixed at line L11 gets an entry for the region of the copy.

**The choice is a knapsack.** Picking old regions to reclaim the most garbage under a cost budget is the [0-1 knapsack problem](/knapsack-problem/), which is NP-hard. Lines L6 to L8 are the greedy rule by ratio. It is fast and works well when each region is small next to the budget, but it is not optimal.

## Example

**The choice of old regions.** The young regions cost 30 and the budget is 100, so 70 is left for old regions. A marking has given these four candidates.

| region | garbage | cost | garbage per cost |
|---|---|---|---|
| A | 40 | 20 | 2.0 |
| B | 45 | 30 | 1.5 |
| C | 30 | 25 | 1.2 |
| D | 60 | 60 | 1.0 |

The rule takes A ($t = 20$), then B ($t = 50$). C would make $t = 75 > 70$, so it stops with 85 words of garbage. Here this is the best choice: every other set within 70 reclaims at most 75 (B and C).

**Where the greedy rule loses.** With a budget of 10 and two old regions, one with garbage 10 and cost 1 and one with garbage 90 and cost 10, the rule takes the first (ratio 10 before 9) and then cannot fit the second. It reclaims 10, where 90 was possible. On 2000 random instances with up to 7 old regions, the rule matched the best set in 1644. In every instance the best set reclaimed at most the greedy amount plus the garbage of the first region that did not fit.

**The remembered set at work.** An old object $o$ gets a field that points to a new object $y$, and no register holds $y$. The store adds $(o, f)$ to the remembered set of the region of $y$. In the next pause, line L10 finds this slot, $y$ is copied, and $o.f$ is set to the copy, although $o$ itself is not in the collection set and is never traced.

## Correctness

The proof in the proofs section shows three facts, which the tests check after every step of random programs.

1. **Remembered sets are complete.** Every pointer from one region into another is listed in the remembered set of the target region. The barrier at line L3 adds it at each store, and the pause adds the pointers of each copy and of each fixed slot.
2. **A pause keeps every object that is reachable or pointed to from outside the collection set.** An object of the collection set that a root or a slot outside it points to is copied (lines L9 to L11), and every field of a copy is fixed in turn (line L13). So no pointer into a freed region survives, and the graph of objects, by identity, is the same after the pause.
3. **Marking frees no reachable object.** The snapshot argument: every object reachable when marking starts is marked or is reachable from the SATB queue, and every object allocated after the start is above TAMS. So cleanup frees only regions whose objects were all unreachable at the end of marking.

Without the pre-write barrier, a program that moves the only pointer to an old object from a field into a register, and then clears the field, loses the object at cleanup; the tests show this with a directed schedule.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **A pause.** Copying $L$ live words with $p$ fields each, scanning the $E$ remembered set entries of the collection set and the $r$ roots: $O(L p + E + r)$. Garbage costs nothing to reclaim, so a region with much garbage is cheap per word freed; this is the reason for the order at line L6.
- **Choosing the collection set.** A sort of the old candidates, $O(c \log c)$ for $c$ candidates, done once per marking in practice.
- **Marking.** Proportional to the live objects, spread over the run of the mutator, with two short pauses.
- **Barriers.** Two barriers per pointer store. The post-write barrier filters stores within a region and stores of nil, and in the real system it logs a dirty card for a refinement thread.
- **Space.** The remembered sets can be large: a popular object in a region can make its set hold a slot for each pointer to it. The real system keeps the sets as cards and coarsens them to whole regions when they grow.

## Properties

- **Soft pause goal.** The goal is met only if the prediction is right and the live data fit; it is not a guarantee. A pause always takes all young regions.
- **Compacting.** Each pause copies its survivors into fresh regions, so the heap does not fragment, without one long compaction of the whole heap.
- **Generational.** Young regions are collected in every pause; old regions only after a marking.
- **Floating garbage.** Snapshot marking keeps every object that was live at its start. A remembered set entry from a dead old object also keeps its target until that old region is collected.
- **Mostly parallel.** In the real system, pauses run on many threads with [work stealing](/parallel-garbage-collection/), and marking runs on its own threads.

## Variants and improvements

- **The paper's modes.** The paper ran *fully young* pauses and, after a marking, *partially young* pauses that also take old regions. HotSpot calls the second kind *mixed* collections and spreads the old candidates over several mixed pauses.
- **Card-based remembered sets.** HotSpot records the cards of the source (see [card marking](/card-marking/)) and not single slots, and refines dirty cards on concurrent threads.
- **Humongous objects.** An object of half a region or more gets its own run of regions and is never copied.
- **Concurrent copying.** [Shenandoah](/shenandoah-collector/) and [ZGC](/z-garbage-collector/) also use regions, but copy while the mutator runs, at the price of a read barrier.
- **Better choices.** The choice could use a knapsack algorithm with a guarantee, such as the better of the greedy set and the best single region, which reclaims at least half of the optimum when each region fits the budget alone (see [fractional knapsack](/fractional-knapsack/)).

## When to use it

Use it for server programs with large heaps that want pauses near a target, such as tens to hundreds of milliseconds, and good throughput. It suits heaps where a few regions hold most of the garbage. Prefer a parallel stop-the-world collector when only throughput matters, and a concurrent compacting collector such as [ZGC](/z-garbage-collector/) or [Shenandoah](/shenandoah-collector/) when pauses must stay near a millisecond.

## Pitfalls

- **A goal that is too low.** If even the young regions cost more than the budget, the pause misses the goal; HotSpot then shrinks the young generation. A goal far below the copy time of the survivors cannot be met.
- **Evacuation failure.** If no free region is left for the copies, the pause cannot finish its copy. The real system then keeps the objects in place and fixes them later, at a high cost; this is often a sign that marking started too late.
- **Popular objects.** A few objects that very many others point to make their remembered sets huge and their regions too expensive to collect.
- **Stale entries.** A remembered set may list slots that have been overwritten or that belong to dead objects. The pause must check each slot before it uses it, as at line L11.
- **Trusting the greedy rule.** The rule is a heuristic for a knapsack; a small region with a high ratio can block a large region that would fill the budget.

## Implementations

## History

The train algorithm of Hudson and Moss (1992) already collected a mature space in fixed-size cars with remembered sets, one car at a time. Detlefs, Flood, Heller and Printezis presented Garbage-First at ISMM 2004, after the mostly concurrent collector of Printezis and Detlefs (2000). G1 shipped in HotSpot as a supported collector in JDK 7 and became the default in JDK 9 (JEP 248). Later releases made full collections parallel and changed how remembered sets are stored.

## References
