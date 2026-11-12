---
tag: 45B69W
kind: technique
slug: card-marking
name: Card marking
aliases:
- card table
- card-based remembered set
- card marking write barrier
area: systems/garbage-collection
level: advanced
summary: "Split the old generation into small cards, dirty a card byte on every pointer store, and at a minor collection scan only the dirty cards for young pointers."
prereqs: [remembered-set, write-barrier]
see_also: [generational-garbage-collection, garbage-first-collector, boehm-gc, incremental-update-barrier, bit-vector, page-fault]
sources:
  - paper: doi:10.21236/ada290169
    title: Patrick G. Sobalvarro, A lifetime-based garbage collector for LISP systems on general-purpose computers, B.S. thesis, MIT Artificial Intelligence Laboratory, Technical Report AITR-1417, 1988
    locator: the marking of small fixed-size segments of the old area on stores, and the scan of the marked segments at a collection
  - paper: doi:10.1145/74877.74882
    title: Paul R. Wilson and Thomas G. Moher, Design of the opportunistic garbage collector, OOPSLA 1989, 23-35
    locator: card marking, with the heap divided into cards and a bit or byte per card set by the store check
  - url: https://bibliography.selflanguage.org/_static/write-barrier.pdf
    title: Urs Hoelzle, A fast write barrier for generational garbage collectors, OOPSLA 1993 Workshop on Garbage Collection and Memory Management
    locator: the byte map of Chambers and Ungar, the relaxed invariant with a leeway of one card, and the two-instruction barrier that stores zero into the byte of the object
  - paper: doi:10.1145/141936.141946
    title: Antony L. Hosking, J. Eliot B. Moss and Darko Stefanovic, A comparative performance evaluation of write barrier implementations, OOPSLA 1992, 92-109
    locator: the measurements of card marking with several card sizes against remembered sets
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 11.8, the parts on cards and card tables, crossing maps and summarising cards
---

Card marking is a way to keep the [remembered set](/remembered-set/) of a [generational collector](/generational-garbage-collection/) at a coarse grain. The old generation is split into *cards* of $2^k$ bytes, and a *card table* holds one byte per card. The [write barrier](/write-barrier/) runs on every pointer store into the heap and stores DIRTY into the byte of the card that holds the written slot. It does no test on the value, so it is two or three machine instructions. At a minor collection, the collector scans the objects on the dirty cards, treats the young pointers it finds there as roots, and cleans the cards. The cost moves from the barrier to the collection: the collector scans whole cards, not single slots.

## In plain words

Think of the old part of the heap as a long street, cut into short blocks. Next to the street is a row of flags, one flag for each block. Each time the program writes a link anywhere on the street, it raises the flag of that block. It does not stop to check what it wrote. This is very fast.

When the collector cleans the young part of the heap, it walks along the row of flags. For each raised flag, it reads the whole block and looks for links to young things. Those links count as starting points. Then it lowers the flag. If a block still holds a link to a young thing after the cleaning, the flag goes up again, so that the next cleaning reads that block once more.

## When it applies

- **A generational or region-based collector needs old-to-young pointers.** Card marking is one representation of the remembered set. It also serves an [incremental update](/incremental-update-barrier/) barrier, where the dirty cards are the places to rescan at the end of a concurrent mark.
- **Pointer stores are frequent.** The barrier has no branch and does the same work for every store, so its cost is small and predictable. A [sequential store buffer](/remembered-set/) costs more per recorded store and fills fast when a program writes many young pointers into old objects.
- **The heap is parsable.** The collector must find the objects that overlap a card. It needs object headers with sizes, and a *crossing map* that gives, for each card, where an object starts. A heap where the collector cannot find object boundaries needs another scheme.
- **The old generation is not huge relative to the cards.** The collector reads the whole card table at each minor collection. With cards of 512 bytes the table is about 0.2% of the heap, and reading it is fast, but its size grows with the old generation, not with the number of stores.

## The template

The model: the old generation is an array $M$ of words, with an object at address $a$ laid out as a header $M[a] = n$ (the number of fields) and the fields $M[a+1 \ldots a+n]$. Cards hold $2^k$ words. $C$ is the card table, one byte per card; DIRTY is $0$ and CLEAN is $1$, so that marking is a store of zero. $F[c]$ is the crossing map: the start of the object that covers the first word of card $c$. $top$ is the end of the old generation when the collection starts. The holes are the card size, the marking rule (the card of the slot, or the card of the object) and the collector that the scan feeds.

```pseudo id=main
WRITE(o, i, v)                                ▷ the barrier, for an old object o
L1  M[o + 1 + i] ← v
L2  C[(o + 1 + i) >> k] ← DIRTY               ▷ no test on v

SCAN-DIRTY-CARDS(visit)                       ▷ at a minor collection
L3  for c ← 0 to the last card below top do
L4      if C[c] ≠ DIRTY then continue
L5      C[c] ← CLEAN
L6      a ← F[c]                              ▷ the object that covers the start of card c
L7      while a < (c + 1)·2^k and a < top do
L8          for each field slot s of the object at a with c·2^k ≤ s < (c + 1)·2^k do
L9              if M[s] is young then
L10                 M[s] ← visit(M[s])        ▷ copy or promote the target
L11                 if M[s] is still young then C[c] ← DIRTY
L12         a ← a + 1 + M[a]                  ▷ the next object

IN THE CHENEY SCAN OF A PROMOTED OBJECT
L13 when a field s of a promoted object is set to a young survivor: C[s >> k] ← DIRTY
```

**Walk-through.** The barrier of lines L1 and L2 is a store, a shift and a byte store. It also dirties a card when $v$ is nil or old: this costs a later scan of a card for nothing, but saves a test on each store. At a minor collection, line L3 reads the card table in order. Line L5 cleans a dirty card before its scan, and line L11 dirties it again if one of its slots still points to a young object after the copy, which happens when the target stays in a survivor space. Line L6 uses the crossing map to find the first object that reaches into the card, which may start on an earlier card. Lines L7 to L12 walk the objects of the card by their sizes and look only at the slots that lie on the card. Line L13 keeps the cover for the slots of objects that this collection promotes.

### Example

Use cards of 4 words ($k = 2$). The old generation holds $A$ at address 0 with 3 fields (words 0 to 3), $B$ at address 4 with 5 fields (words 4 to 9) and $C$ at address 10 with 1 field (words 10 and 11). The crossing map is $F = [0, 4, 4]$: card 2 starts at word 8, which lies inside $B$. All cards are clean.

| step | action | card table |
|---|---|---|
| 1 | allocate young $x$; store $B.f_4 \gets x$ (word 9, card 2) | clean, clean, dirty |
| 2 | store $A.f_0 \gets$ nil (word 1, card 0) | dirty, clean, dirty |
| 3 | drop the root of $x$; minor collection | |
| 3a | card 0: object $A$, slots 1 to 3, no young pointer | clean, clean, dirty |
| 3b | card 2: $F[2] = 4$, object $B$, slots 8 and 9; word 9 holds $x$; promote $x$ to address 12; then object $C$, slot 11 | clean, clean, clean |
| 3c | the promotion of $x$ adds card 3 | clean, clean, clean, clean |

The collection reads two cards and finds $x$, which is reachable only through $B$. Step 2 shows the unconditional barrier: a store of nil still dirties card 0, which the collector then scans for nothing.

### Correctness

**Invariant.** Between collections, every slot of an old object that holds a young pointer lies on a dirty card. A mutator store changes one slot, and line L2 dirties its card. A scan cleans a card at line L5, and line L11 dirties it again if any of its slots still holds a young pointer after the copy; slots that line L8 does not visit lie on other cards. A promoted object gets its fields at line L13, which dirties the card of each field that holds a survivor. Old slots that the collection does not touch keep their values, and pointers from them can only change from young to old.

**Safety.** Given the invariant, each old-to-young slot lies on a dirty card, so line L8 visits it: $F[c]$ is at or before the first word of the card, and the walk by object sizes meets every object that overlaps the card. So the slot is a root of the minor collection, and the argument of [generational collection](/generational-garbage-collection/) shows that every reachable young object survives. The tests check the invariant at the start of every minor collection, against a list of all old-to-young slots, and check the surviving object graph against a heap with no collector.

### Cost

The barrier is $O(1)$, with no branch: two instructions on SPARC in Hoelzle's version, which marks the byte of the object, not of the slot. A minor collection reads all $m$ card bytes and scans the dirty cards: $O(m + d \cdot 2^k + w)$ time, where $d$ is the number of dirty cards and $w$ accounts for the parts of objects that start before a card. The card table takes $m = |M| / 2^k$ bytes. Smaller cards make the scan more precise and the table larger; larger cards do the opposite. With slot-precise remembered sets, the collection cost is proportional to the number of remembered slots instead.

## Classic examples

- **Sobalvarro (1988).** A lifetime-based collector for Lisp on stock hardware that marked small segments of the old area on stores and scanned only the marked segments.
- **Wilson and Moher (1989).** The opportunistic garbage collector, which used the name card marking, with a bit or a byte per card set by the store check.
- **Chambers and Ungar, then Hoelzle (1993).** The SELF system used a byte per card, so that the mark is a single byte store with no read-modify-write. Hoelzle relaxed the invariant to "byte $i$ marked means cards $i$ to $i + l$ may hold an old-to-young pointer", which lets the barrier mark the card of the object start, not of the slot: two SPARC instructions, a shift and a store of zero. With $l = 1$ and cards of 128 bytes, stores into the first fields of an object are covered.
- **HotSpot.** The Java HotSpot VM uses a card table with cards of 512 bytes and a byte per card for its young collections.
- **Garbage-First.** [G1](/garbage-first-collector/) marks cards in its barrier, and puts the dirtied cards into queues that background threads scan to update per-region remembered sets.

## Variations

- **Bits or bytes.** A bit per card makes the table eight times smaller, but marking it needs a read-modify-write, which is slower and is not atomic with other threads. Most systems use bytes.
- **Marking the object, not the slot.** Mark the card of the header. Then a scan of a dirty card must scan all fields of each object that starts on it, even those on later cards. This is the variant in the implementation with mode "object".
- **Conditional card marking.** Read the card byte first and store only if it is clean. This costs a load and a branch but avoids writes to a shared cache line when many threads store into nearby cards.
- **Summarising cards.** After a scan, record the slots of the cards that stay dirty in a remembered set, or keep a second table with one entry per group of cards, so that the next scan skips clean groups fast.
- **Virtual memory pages as cards.** A collector that cannot change the compiler can use the dirty bits of the virtual memory system, or protect pages and catch the first write with a [page fault](/page-fault/). The pages then act as large cards. The [Boehm-Demers-Weiser collector](/boehm-gc/) does this.

## Pitfalls

- **A missing or stale crossing map.** If $F[c]$ points after the start of the object that covers card $c$, the scan misses the slots of that object on card $c$. Every allocation in the old generation, including promotion and compaction, must update $F$.
- **Cleaning a card after its scan.** If the card is cleaned at the end of the scan, a store by another thread during the scan is lost. Clean first (line L5), then scan.
- **Forgetting survivors.** A card that holds a pointer to an object that stays young after the collection must stay dirty (line L11), or the next minor collection frees that object.
- **Huge objects.** A large array of pointers spans many cards. A store dirties one card, and the scan must still find the array header through the crossing map. Without it the collector scans the whole array.
- **Card size chosen badly.** Small cards make the table large and slow to read; large cards make each dirty card cost much. Measure with the program's store pattern.
- **False sharing.** Threads that store into objects on nearby cards write bytes of the same cache line in the card table, even when the card is already dirty.

## Exercises

1. In the example, add the store $C.f_0 \gets x$ before the collection. Which cards does the collector scan, and how many slots does it read?
2. The barrier marks the card of the object start, and the scan of a dirty card $i$ also scans cards $i + 1$ to $i + l$. Prove that the collector finds every old-to-young slot when each store goes into one of the slots that lie at most $l$ cards after the object start, and give a store that it misses otherwise.
3. Give a store pattern for which card marking does much more collector work than a slot-precise remembered set, and one for which it does much less.

## References
