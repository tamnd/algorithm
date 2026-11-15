---
tag: S7XDVF
kind: data-structure
slug: hidden-classes
name: Hidden classes
aliases:
- object maps
- object shapes
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Shared descriptors of object layout for dynamic languages, so that objects with the same fields have fixed offsets for fast access.
model: word-ram
complexity:
  vars: {p: the number of own properties of an object, T: the number of shapes created, k: the bound of a load cache}
  time: {get: O(1), set: O(1), cached-load: O(k), new-shape: O(p)}
  space: {extra: O(T p)}
prereqs: [inline-caching, hash-table]
see_also: [polymorphic-inline-cache, inline-caching, type-feedback, trie, hash-consing, dictionary, just-in-time-compilation, deoptimization]
sources:
  - paper: doi:10.1145/74877.74884
    title: Craig Chambers, David Ungar and Elgin Lee, An efficient implementation of SELF, a dynamically-typed object-oriented language based on prototypes, OOPSLA 1989, 49-70
    locator: the section on maps, where clones of the same prototype share one map that describes the names and layout of their slots, so each object stores only the values of its assignable slots
  - paper: doi:10.1145/2666356.2594332
    title: Wonsun Ahn, Jiho Choi, Thomas Shull, María J. Garzarán and Josep Torrellas, Improving JavaScript performance by deconstructing the type system, PLDI 2014, 496-507
    locator: the description of hidden classes in the V8 engine, their transitions when properties are added, their use as the key of inline caches, and the extra polymorphism that comes from the prototype being part of the hidden class
  - paper: doi:10.1007/BFb0057013
    title: Urs Hölzle, Craig Chambers and David Ungar, Optimizing dynamically-typed object-oriented languages with polymorphic inline caches, ECOOP 1991, LNCS 512, 21-38
    locator: the use of SELF maps as the receiver types tested by inline caches and polymorphic inline caches
---

A hidden class, also called a map or a shape, is a descriptor of the layout of an object in a dynamic language: which properties the object has and at which offset each value is stored. Many objects share one hidden class, so each object stores only a pointer to it and an array of values. A program never sees hidden classes. The runtime makes them as the program adds properties: adding a property to an object moves it from its hidden class to a child hidden class along a *transition*, and objects that got the same properties in the same order end at the same hidden class. With that, a property read becomes a check of the hidden class and a load at a fixed offset, which an [inline cache](/inline-caching/) can remember. SELF introduced maps in 1989 for objects made by cloning, and JavaScript engines such as V8 build them by transitions.

## In plain words

In JavaScript or Python, an object is like a small dictionary: you can add a field at any time, and each object can have different fields. If every object keeps its own table of field names, a read like `p.x` must search that table each time, and every object pays for its own table.

Hidden classes share the tables. All objects that got the fields `x` and then `y` point to one shared description that says "`x` is in slot 0, `y` is in slot 1". The object itself keeps only the values. When a field is added, the object moves to the next description in a tree of descriptions, and the tree remembers each step so that other objects reuse it. A read can then check "is this object's description the one I saw last time?" and, if yes, take slot 0 at once.

## The abstract type

A runtime has classes, each with a method table and an optional parent, as in the model of the [polymorphic inline cache](/polymorphic-inline-cache/). An object belongs to a class and has a set of *own properties*, each a name with a value. The operations are:

- **NEW($C$).** A new object of class $C$ with no own properties.
- **SET($o$, $x$, $v$).** Give $o$ the own property $x$ with value $v$, adding it if it is not there.
- **DELETE($o$, $x$).** Remove the own property $x$ from $o$.
- **GET($o$, $x$).** The value of the own property $x$ of $o$ if there is one, and otherwise the method $x$ found through the chain of classes of $o$, or "missing".
- **SHAPE($o$).** The hidden class of $o$, or none.
- **LOAD(site, $o$).** GET($o$, $x$) for the fixed name $x$ of a site, through a load cache.

The required result is that GET and LOAD give the same answer as a plain dictionary per object plus a full method lookup, for every sequence of operations.

## Representation

A *shape* $S$ is an immutable record with:

- $\mathit{class}(S)$, the class of the objects that have it;
- $\mathit{parent}(S)$ and $\mathit{key}(S)$: the shape it came from and the name added, both empty for a *root shape*;
- $\mathit{offsets}(S)$: a [hash table](/hash-table/) from each property name to a slot number, equal to $\mathit{offsets}(\mathit{parent}(S))$ plus $\mathit{key}(S) \mapsto |\mathit{offsets}(\mathit{parent}(S))|$;
- $\mathit{transitions}(S)$: a table from a name $x$ to the child shape that adds $x$. Entries are added, never removed.

Each class has one root shape. The shapes and transitions form a tree under each root, with an edge labelled by a property name, which is a [trie](/trie/) of the orders in which properties were added. The names of $S$, read from the root down, are the order in which they were added, and $\mathit{offsets}(S)$ maps them to $0, 1, \dots$ in that order.

An object $o$ holds its class, a shape $\mathit{shape}(o)$, and an array $\mathit{slots}(o)$. After a deletion it moves to *dictionary mode*: its shape is empty and it holds its own properties in a private hash table.

A *load cache* at a site that reads the name $x$ is a polymorphic inline cache keyed by shapes. Each entry is one of:

- $(S, \text{field}, i)$: objects of shape $S$ hold $x$ at slot $i$;
- $(S, \text{class}, a)$: objects of shape $S$ have no own $x$, and the class chain of $\mathit{class}(S)$ gives the answer $a$.

## Operations

```
NEW(C)
L1  return an object with class C, shape root(C), empty slots

TRANSITION(S, x)
L2  if x is not in transitions(S) then transitions(S)[x] ← a new shape with parent S and key x
L3  return transitions(S)[x]

SET(o, x, v)
L4  if o is in dictionary mode then o.dict[x] ← v; return
L5  if x is in offsets(shape(o)) then slots(o)[offsets(shape(o))[x]] ← v
L6  else shape(o) ← TRANSITION(shape(o), x); append v to slots(o)

DELETE(o, x)
L7  if o is not in dictionary mode and x is in offsets(shape(o)) then
L8      o.dict ← the pairs (y, slots(o)[i]) for (y, i) in offsets(shape(o)); shape(o) ← none
L9  if o is in dictionary mode then remove x from o.dict

GET(o, x)
L10 if o is in dictionary mode and x is in o.dict then return o.dict[x]
L11 if o is not in dictionary mode and x is in offsets(shape(o)) then return slots(o)[offsets(shape(o))[x]]
L12 return LOOKUP(class(o), x)                       ▷ walk the class chain

LOAD(site, o)
L13 if site is megamorphic or o is in dictionary mode then return GET(o, x)
L14 for each entry (S, kind, d) of the site: if S = shape(o) then
L15     if kind = field then return slots(o)[d] else return d
L16 compute the entry for shape(o) as in L11 and L12, add it as in a polymorphic inline cache, and return the answer
```

Changing a method of a class $D$ removes the class entries $(S, \text{class}, a)$ whose $\mathit{class}(S)$ has $D$ in its chain, exactly as for a [polymorphic inline cache](/polymorphic-inline-cache/). Field entries never need invalidation, because a shape never changes: an object that gets a new property moves to another shape instead.

## Example

Take a class `Point`, child of `Object`, with a method `norm`. Make three objects and add properties in these orders:

- `p`: `x = 3`, then `y = 4`;
- `q`: `y = 5`, then `x = 6`;
- `r`: `x = 7`, then `y = 8`.

The shape tree under the root $S_0$ of `Point` grows to

```
S0  {}
├── x → S1  {x: 0}
│         └── y → S2  {x: 0, y: 1}
└── y → S3  {y: 0}
          └── x → S4  {y: 0, x: 1}
```

`p` creates $S_1$ and $S_2$, `q` creates $S_3$ and $S_4$, and `r` follows the transitions that `p` made and creates nothing. So `p` and `r` share $S_2$, with slots $[3, 4]$ and $[7, 8]$, and `q` has $S_4$ with slots $[5, 6]$. With the root shape of `Object`, the runtime has made 6 shapes in total.

A load site `o.x` with bound 2 reads `p`, `q`, `r`, `p`:

| read | shape | result | entry used or added | answer |
|---|---|---|---|---|
| `p.x` | $S_2$ | miss | add $(S_2, \text{field}, 0)$ | 3 |
| `q.x` | $S_4$ | miss | add $(S_4, \text{field}, 1)$ | 6 |
| `r.x` | $S_2$ | hit | $(S_2, \text{field}, 0)$ | 7 |
| `p.x` | $S_2$ | hit | $(S_2, \text{field}, 0)$ | 3 |

The site ends polymorphic, with 2 hits and 2 misses. The entry for $S_2$ answers for `r` although it was made for `p`, because both have the same layout. A site `o.norm` gets the entries $(S_2, \text{class}, \text{Point.norm})$ and $(S_4, \text{class}, \text{Point.norm})$, and loses both if a method `norm` is added to `Point` or changed in `Object`.

If the program now deletes `y` from `q`, then `q` goes to dictionary mode with the table $\{x: 6\}$, and no load cache stores anything for it.

## Correctness

The full proof is in the proof file. Its main steps:

1. **Shapes are immutable and describe exact layouts.** By line L2, a new shape has its parent's offsets plus one new name at the next slot, and line L6 calls TRANSITION only for a name that is not in the offsets yet. So $\mathit{offsets}(S)$ is a one-to-one map from the names of $S$ onto $0, \dots, |S| - 1$.
2. **Object invariant.** For an object $o$ not in dictionary mode, the own property names of $o$ are exactly the names of $\mathit{shape}(o)$, the value of each name $y$ is $\mathit{slots}(o)[\mathit{offsets}(\mathit{shape}(o))[y]]$, and the class of the shape is the class of $o$. Lines L5 and L6 keep it, and line L8 copies the exact properties into the private table before the shape is dropped.
3. **Sharing.** The shape of an object not in dictionary mode is found from the root of its class by following the transitions for its names in the order of addition. Transitions are deterministic and never removed, so objects of the same class with the same order have the same shape, and a shape determines the class and the order, so different classes or orders give different shapes.
4. **GET and LOAD.** GET is right by the object invariant. A field entry $(S, \text{field}, i)$ stays right forever, because $S$ is immutable and every object of shape $S$ holds $x$ at slot $i$. A class entry depends on the class chain, and the invalidation keeps it right by the same locality argument as for the polymorphic inline cache.

## Complexity

GET, and SET of an existing property, cost one hash-table look-up in the offsets, so $O(1)$ expected, plus the walk of the class chain when the name is not an own property. SET of a new property follows a transition in $O(1)$ expected time, and costs $O(p)$ once, when it creates a new shape, to copy the offsets. A load cache hit costs at most $k$ comparisons of shape pointers and one array access, with no hashing at all, which is the reason for the whole design.

The space for shapes is $O(T p)$ with copied offset tables. Engines lower it by sharing one array of property descriptors between a shape and its descendants on the same path. Each object costs one pointer and its values, instead of a hash table of its own. The number $T$ of shapes is the number of distinct pairs of a class and an order of addition that the program creates, counted with all their prefixes. A program that adds properties in many orders makes many shapes.

## Variants

- **SELF maps.** In SELF, objects are made by cloning a prototype, and all clones share the map of the prototype. A map also holds the constant slots, such as methods, so they are not stored in each object.
- **The prototype in the shape.** In V8 the prototype of an object is part of its hidden class, so objects with the same properties but different prototypes have different shapes. Ahn and others show that this causes extra polymorphism at inline caches in real web code.
- **Dictionary mode.** After a deletion, or with very many properties, an engine gives up on shapes for the object and uses a private hash table, as in lines L7 to L9.
- **Field types in the shape.** A shape can also record that a field has always held a small integer or a double, so that compiled code can skip a type check. When a store breaks that, the engine makes a new shape and must [deoptimize](/deoptimization/) code that relied on the old one.
- **In-object slack.** An engine can reserve a few slots inside each new object, guessed from the constructor, so that the first properties need no separate array.
- **Hidden classes for arrays.** The kind of elements of an array, such as only small integers, can be part of its hidden class in the same way.

## When to use it

Use hidden classes in the runtime of a language whose objects can gain properties at any time, when many objects in fact get the same properties in the same order, as objects made by one constructor do. They pay off together with inline caches and a [JIT compiler](/just-in-time-compilation/), which turn a cached shape check into a compare and a load. For a language with fixed records declared ahead, a static layout is simpler. For objects used as general dictionaries with many keys, a plain hash table is better, which is why engines have dictionary mode.

## Pitfalls

- **Order matters.** `{x, y}` and `{y, x}` are different shapes. Code that adds properties in a different order on different paths makes sites polymorphic. Constructors that set all fields in a fixed order avoid that.
- **Deletion.** Deleting a property moves an object to dictionary mode, where load caches do not help. Setting a property to an empty value instead keeps the shape.
- **Forgetting the class part.** A cached method entry depends on the class chain, not only on the shape. It needs invalidation when a method in the chain changes, while a field entry does not.
- **Mutating a shape.** Shapes are shared. Changing one in place, for example to add a property to one object, changes the layout of every object that has it. Always move the object to a new shape.
- **Too many shapes.** Properties named by data, such as keys read from input, make one shape per distinct order. Engines limit the number of transitions per shape and switch such objects to dictionary mode.

## Implementations

## History

Chambers, Ungar and Lee introduced maps in their 1989 implementation of SELF, a language with prototypes and no classes. All clones of a prototype share one map, which gives the compiler and the inline caches something that behaves like a class. Hölzle, Chambers and Ungar used maps as the types in polymorphic inline caches in 1991. JavaScript engines took up the idea for a language where objects are often built by adding properties one at a time. V8 builds its hidden classes by transitions from an empty root, and Ahn and others described this design in 2014 when they studied its effect on inline caches.

## References
