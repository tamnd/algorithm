---
tag: WAS1H3
kind: data-structure
slug: polymorphic-inline-cache
name: Polymorphic inline cache
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: An inline cache that holds several receiver types and their targets at a call site, and records the types seen for later optimization.
model: word-ram
complexity:
  vars: {k: the bound on the number of entries of one cache, h: the length of the longest chain of parent classes, S: the number of send sites}
  time: {hit: O(k), miss: O(k + h), invalidate: O(S k h)}
  space: {extra: O(S k)}
prereqs: [inline-caching]
see_also: [inline-caching, type-feedback, hidden-classes, adaptive-optimization, devirtualization, function-inlining, class-hierarchy-analysis, hash-table]
sources:
  - paper: doi:10.1007/BFb0057013
    title: Urs Hölzle, Craig Chambers and David Ungar, Optimizing dynamically-typed object-oriented languages with polymorphic inline caches, ECOOP 1991, LNCS 512, 21-38
    locator: the polymorphic inline cache as a stub that tests the receiver type against each cached case and is extended on a miss, and the use of the cached types by the compiler; the abstract reports a median speedup of 11% on SELF programs
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Chapter 3, Section 3.4 with Figure 3-4 (receiver types per send site), Section 3.5 (polymorphic inline caches) and Section 3.5.1 (megamorphic sends, marked after more than 10 cases)
  - paper: doi:10.1145/178243.178478
    title: Urs Hölzle and David Ungar, Optimizing dynamically-dispatched calls with run-time type feedback, PLDI 1994, 326-336
    locator: the use of the receiver types stored in polymorphic inline caches as type feedback for the optimizing compiler
  - paper: doi:10.1145/800017.800542
    title: L. Peter Deutsch and Allan M. Schiffman, Efficient implementation of the Smalltalk-80 system, POPL 1984, 297-302
    locator: the monomorphic inline cache that the polymorphic inline cache extends
---

A polymorphic inline cache (PIC) is the cache of one send site in a dynamically typed language. It holds a short list of pairs, each a receiver class and the method that a full lookup found for it, up to a fixed bound. A send compares the class of the receiver with the cached classes in turn and calls the method of the first match. On a miss it does the full lookup and adds a pair. When a site has seen more classes than the bound, the cache marks it *megamorphic* and from then on uses a slower general lookup. Hölzle, Chambers and Ungar introduced PICs in SELF in 1991. They fix the weak point of the one-entry [inline cache](/inline-caching/), which misses on every change of class at a site that sees two or more classes. They also have a second use: the list of classes is a record of the receiver types that the site has seen, which an optimizing compiler reads as [type feedback](/type-feedback/).

## In plain words

A call such as `shape.draw()` must find the right `draw` for the kind of object in `shape`. A one-entry cache remembers only the last kind. If the kinds alternate, circle, square, circle, square, the cache is wrong every time.

A polymorphic inline cache remembers a few kinds, for example up to four, each with its method. On each call it checks the list, and if the kind is there it calls the method at once. If not, it does the slow search and adds the new kind to the list. If a call place sees too many kinds, the list is no help, so the cache stops trying and always does a general search. The list has one more use: it tells the optimizing compiler which kinds really occur at that place.

## The abstract type

A *runtime* has classes, each with a method table and an optional parent, and a set of send sites. Each site has a selector $s$ and a bound $k \ge 1$. $\mathrm{LOOKUP}(K, s)$ is the full lookup: the method of the first class in the chain $K, \mathit{parent}(K), \dots$ that defines $s$, or a "not understood" marker.

- **SEND(site, $K$).** The method that a send of $s$ to a receiver of class $K$ runs. It must equal $\mathrm{LOOKUP}(K, s)$ under the current classes.
- **SETMETHOD($D$, $s$), REMOVEMETHOD($D$, $s$), SETPARENT($D$, $P$).** Change a class at run time.
- **STATE(site).** One of *uninitialized*, *monomorphic*, *polymorphic* and *megamorphic*.
- **TYPES(site).** The classes in the cache, in the order in which they were added.

## Representation

Each site holds:

- $\mathit{entries}$: a list of at most $k$ pairs $(K_i, m_i)$ with distinct classes $K_i$;
- $\mathit{mega}$: a flag, true when the site is megamorphic, and then $\mathit{entries}$ is empty;
- counters of hits and misses, for the profiler.

The state is a function of these fields, not a separate variable:

| $\mathit{mega}$ | number of entries | state |
|---|---|---|
| false | 0 | uninitialized |
| false | 1 | monomorphic |
| false | 2 to $k$ | polymorphic |
| true | 0 | megamorphic |

The runtime holds the list of all sites and a global lookup cache, a [hash table](/hash-table/) from (class, selector) to method, which only megamorphic sites use.

In SELF the entries are not a list in memory but machine code: a *stub* that the call instruction of the site jumps to, which compares the class of the receiver with each $K_i$ and jumps to $m_i$ on a match. On a miss the stub calls the lookup routine, which writes a new stub with one more case and points the call instruction at it. The list form here has the same behaviour.

## Operations

```
SEND(site, K)
L1  if site.mega then return GLOBALLOOKUP(K, s)
L2  for each (Ki, mi) in site.entries, in order
L3      if Ki = K then return mi                      ▷ hit
L4  m ← LOOKUP(K, s)                                  ▷ miss
L5  if |site.entries| < k then append (K, m) to site.entries
L6  else site.entries ← empty; site.mega ← true
L7  return m

GLOBALLOOKUP(K, s)
L8  if (K, s) is not in the global cache then global[(K, s)] ← LOOKUP(K, s)
L9  return global[(K, s)]

CHANGED(D)                                            ▷ called before D changes
L10 empty the global cache
L11 for each site: remove from site.entries each (Ki, mi) such that D is in the chain of Ki
```

SETMETHOD, REMOVEMETHOD and SETPARENT call CHANGED($D$) and then change $D$. SETPARENT first refuses a parent that would make a cycle, that is, a $P$ whose chain holds $D$. CHANGED does not reset the megamorphic flag: a megamorphic site is correct in every state of the classes, so there is no need to.

From these operations the state of a site moves only along these transitions:

| from | event | to |
|---|---|---|
| uninitialized | miss | monomorphic |
| monomorphic | miss, $k \ge 2$ | polymorphic |
| polymorphic with $j < k$ entries | miss | polymorphic with $j + 1$ entries |
| any state with $k$ entries | miss | megamorphic |
| any state that is not megamorphic | CHANGED | the same or a state with fewer entries |
| any state | hit | the same |
| megamorphic | anything | megamorphic |

## Example

Take five classes. `Object` defines `print` and `hash`. `Point`, child of `Object`, defines `x` and `print`. `ColorPoint`, child of `Point`, defines `color`. `Circle`, child of `Object`, defines `print` and `area`. `Square`, child of `Object`, defines `area`. One site sends `print` with bound $k = 3$.

| send | receiver class | result | method run | state after | entries after |
|---|---|---|---|---|---|
| 1 | Point | miss | Point.print | monomorphic | Point |
| 2 | Circle | miss | Circle.print | polymorphic | Point, Circle |
| 3 | Point | hit, 1 test | Point.print | polymorphic | Point, Circle |
| 4 | ColorPoint | miss | Point.print | polymorphic | Point, Circle, ColorPoint |
| 5 | Circle | hit, 2 tests | Circle.print | polymorphic | same |
| 6 | Square | miss | Object.print | megamorphic | none |
| 7 | Point | global cache | Point.print | megamorphic | none |

Send 6 finds three entries, the bound, so the site turns megamorphic. Send 7 would have been a hit before, but now it goes to the global cache, whose first look-up of (Point, print) is a full lookup.

Now take the same site after send 4, with entries Point, Circle and ColorPoint, and add a method `print` to `ColorPoint`. CHANGED(ColorPoint) removes only the entry for `ColorPoint`, because the chains of `Point` (Point, Object) and of `Circle` (Circle, Object) do not hold `ColorPoint`. The next send to a `ColorPoint` misses and adds (ColorPoint, ColorPoint.print). If the program then adds a method `print` to `Point`, the entry for `Point` goes, and the entry for `ColorPoint` goes too, because `Point` is in the chain of `ColorPoint`. Only `Circle` is left, and the site is monomorphic again. The implementation's tests replay both runs.

Simple cases: a site that never runs stays uninitialized. With $k = 1$ the PIC is the one-entry inline cache plus a megamorphic state, and the states go uninitialized, monomorphic, megamorphic. A site that sees exactly $j \le k$ classes, each several times, without changes to the classes, ends with $j$ entries after $j$ misses.

## Correctness

The full proof is in the proof file. It rests on one invariant and one fact about lookups.

- **Invariant.** At each site, the classes in the entries are distinct, there are at most $k$ of them, and each pair satisfies $m_i = \mathrm{LOOKUP}(K_i, s)$ under the current classes. Each pair in the global cache satisfies the same equation.
- **Locality of lookup.** $\mathrm{LOOKUP}(K, s)$ reads only the parent links and method tables of the classes in the chain of $K$. So if a class $D$ is not in the chain of $K$, a change of $D$ does not change the chain of $K$ or the result of the lookup.

A hit at line L3 returns $m_i = \mathrm{LOOKUP}(K_i, s) = \mathrm{LOOKUP}(K, s)$, because the guard $K_i = K$ holds. A miss returns $\mathrm{LOOKUP}(K, s)$ directly, and the pair it adds satisfies the invariant. It is added only if $K$ is not in the list yet, since the loop found no match. A megamorphic send returns a global cache entry, which is right by the invariant. Line L10 empties the global cache, and line L11 removes exactly the entries whose result can change, by locality. So every send returns the result of the full lookup, in every state, for every sequence of sends and changes. The transitions in the table above follow from lines L5 and L6 and from the fact that CHANGED only removes entries.

## Complexity

A hit costs one comparison per entry up to the match, so $O(k)$, and $O(1)$ for the first entry. A miss costs the $k$ comparisons plus a full lookup, which visits at most $h$ classes, each with a hash-table look-up of expected $O(1)$ time, so $O(k + h)$ expected. A megamorphic send costs one global hash-table look-up, plus a full lookup the first time a pair is seen. CHANGED walks all sites and, for each entry, the chain of its class, so it costs $O(S k h)$. That is acceptable because classes change rarely, and a system can trade precision for speed by emptying every site with the selector.

A site uses $O(k)$ space. Bounds in practice are small: SELF marked a site megamorphic after more than 10 cases (Hölzle 1994, Section 3.5.1), and JavaScript engines use a bound of a few entries.

## Variants

- **Order of the tests.** The list keeps the order of first use. A system can move the most frequent class to the front, or sort by the counts that the stub keeps. SELF tried a move-to-front scheme and dropped it (Hölzle 1994, Section 3.5.1).
- **What happens at the bound.** The variant here switches to a global cache and stays megamorphic. SELF instead kept the stub and replaced a random case. Some systems clear the cache and start again from uninitialized.
- **Keys.** The key can be a class, a SELF map, or a [hidden class](/hidden-classes/), and the stored answer can be a field offset instead of a method, as in property-access caches of JavaScript engines.
- **Caches in an interpreter.** A bytecode interpreter can keep the entries next to the send instruction instead of in a stub of machine code.
- **Counts for type feedback.** Each entry can count its hits, so that the compiler knows not only which classes occur but how often. The optimizing compiler of SELF-93 inlines the frequent cases behind type tests and keeps a dynamic send for the rest, which is [type feedback](/type-feedback/).

## When to use it

Use a PIC at send sites of a language with dynamic dispatch, when most sites see one class and a minority see a few, which is what Hölzle measured in SELF programs. Use it together with a profiler, because the PICs are a cheap source of type information for an optimizing compiler. If [class hierarchy analysis](/class-hierarchy-analysis/) proves that a site has one possible target, a direct call is better, and if the language has a static type for the receiver, a virtual method table gives dispatch in constant time without a cache.

## Pitfalls

- **Testing a superclass.** Each entry must test the exact class. A test "is a subclass of $K_i$" returns the wrong method when a subclass overrides it.
- **Forgetting invalidation.** Without CHANGED, a site keeps calling an old method after the program redefines it. The removal must use the chain as it was before the change, so CHANGED runs before the change.
- **Resetting the megamorphic flag on every change.** It is not wrong, but a site that is truly megamorphic then climbs the states again and pays for several misses each time.
- **A bound that is too large.** A long chain of tests can be slower than a global hash-table look-up, and a large stub uses code memory.
- **Reading the types as complete.** TYPES(site) holds only the classes seen so far, and is empty after a megamorphic switch. A compiler that inlines from it must keep a fallback send for other classes.

## Implementations

## History

Deutsch and Schiffman introduced the one-entry inline cache in their Smalltalk-80 system in 1984. Hölzle, Chambers and Ungar introduced the polymorphic inline cache for SELF in 1991, at ECOOP, and reported a median speedup of 11% on their SELF programs, a measured result on the machines and programs of that paper. They also noted that the cached types are information for the compiler. Hölzle and Ungar built on that in 1994 with type feedback, where the optimizing compiler of SELF-93 reads the PICs to inline the common cases. Hölzle's 1994 thesis gives the design in full, with megamorphic sends and measurements of the number of types per site.

## References
