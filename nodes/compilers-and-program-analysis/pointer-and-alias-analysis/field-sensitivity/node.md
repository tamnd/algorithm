---
tag: XBS21W
kind: concept
slug: field-sensitivity
name: Field sensitivity
aliases:
- field-sensitive pointer analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Whether a pointer analysis keeps the fields of a structure or object apart as separate locations or merges them into one.
prereqs: [points-to-analysis, andersen-analysis]
see_also: [steensgaard-analysis, type-based-alias-analysis, alias-analysis, flow-sensitivity, context-sensitivity, cfl-reachability, scalar-replacement-of-aggregates, hybrid-cycle-detection]
sources:
  - paper: doi:10.1145/1290520.1290524
    title: David J. Pearce, Paul H. J. Kelly and Chris Hankin, Efficient field-sensitive pointer analysis of C, ACM Transactions on Programming Languages and Systems 30(1), Article 4 (2007)
    locator: the constraint language with field offsets, positive weight cycles, and the comparison of field-sensitive and field-insensitive precision and cost on C programs
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the modeling of aggregates as one of the dimensions of precision
  - paper: doi:10.1561/2500000014
    title: Yannis Smaragdakis and George Balatsouras, Pointer Analysis, Foundations and Trends in Programming Languages 2(1), 1 to 69, 2015
    locator: the field-sensitive model of a Java points-to analysis, with the load and store rules for fields
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the pointer analysis chapter (the constraints for structures and their fields)
---

A pointer analysis is *field-sensitive* when it keeps the fields of an object apart: the field `f` of an object is one abstract location, and its field `g` is another. A *field-insensitive* analysis merges all fields of an object into one location. A *field-based* analysis keeps one location per field name, shared by all objects. Field sensitivity is one of the main dimensions of precision of a [points-to analysis](/points-to-analysis/), next to [flow sensitivity](/flow-sensitivity/) and [context sensitivity](/context-sensitivity/). In a type-safe language such as Java it is cheap and is the usual default. In C it needs care, because casts and pointer arithmetic can reach one field from another.

## In plain words

An object often has several parts, such as the next link and the value of a list node. A pointer analysis has to decide how many names to give these parts. It can give the whole object one name, which is simple but mixes up what the parts point to. It can give each kind of part one name for all objects, so that every next link in the program shares a name. Or it can name each part of each object, which is the most precise choice. The last choice costs more, because there are more names to track. In C there is an extra risk: a program can move from one part to another with arithmetic, so an analysis that trusts the names of the parts must notice when that happens.

## The idea

**Three models.** Let `o` be an abstract object, such as an allocation site, and `f` a field. The three models map the field `o.f` to an abstract location:

| model | location of `o.f` | number of locations |
|---|---|---|
| field-insensitive | `o` | one per object |
| field-based | `F_f`, one per field name | one per field name |
| field-sensitive | `o.f` | one per object and field |

**Constraints.** The order, the join and the least solution are those of [Andersen's analysis](/andersen-analysis/): sets ordered by $\subseteq$, union as the join, the least solution in the direction of Cousot. Only the locations change. For a load and a store of a field:

| statement | field-sensitive | field-based | field-insensitive |
|---|---|---|---|
| `p = q.f` | $pts(o.f) \subseteq pts(p)$ for each $o \in pts(q)$ | $pts(F_f) \subseteq pts(p)$ | $pts(o) \subseteq pts(p)$ for each $o \in pts(q)$ |
| `q.f = p` | $pts(p) \subseteq pts(o.f)$ for each $o \in pts(q)$ | $pts(p) \subseteq pts(F_f)$ | $pts(p) \subseteq pts(o)$ for each $o \in pts(q)$ |
| `p = &q->f` (C) | $o.f \in pts(p)$ for each $o \in pts(q)$ | $F_f \in pts(p)$ | $pts(q) \subseteq pts(p)$ |

The field-based model turns every load and store into a copy, so its constraint graph has no dereferences and is solved by reachability alone. That makes it fast, and it ignores the base pointer entirely.

**Field-sensitive is the most precise of the three.** For a type-safe program, let $\beta$ map each field-sensitive location to the coarse one ($o.f \mapsto o$, or $o.f \mapsto F_f$), and each variable and object to itself. If $S$ is a solution of the coarse constraints, then $S'(x) = \{\ell : \beta(\ell) \in S(\beta(x))\}$ is a solution of the field-sensitive constraints. For the store `q.f = p`: if $o \in S'(q)$, then $\beta(o) \in S(\beta(q))$, so the coarse store gives $S(p) \subseteq S(\beta(o.f))$, and then every $\ell \in S'(p)$ has $\beta(\ell) \in S(\beta(o.f))$, so $\ell \in S'(o.f)$. The load and the other forms are the same. So the field-sensitive least solution is below $S'$ for the coarse least solution $S$, and its image under $\beta$ is inside $S$. Field-based and field-insensitive analysis are incomparable, as the example below shows.

**Cost.** With $F$ fields per object, the number of locations grows from $N$ to at most $N F$, and the cubic bound of Andersen's analysis grows with it. The sets often get smaller, because fewer false targets flow around, which pays back part of the cost. On C programs, Pearce, Kelly and Hankin (2007) found the field-sensitive analysis more expensive to compute but much more precise.

**C needs care.** Fields in C are byte offsets in a block of memory, and the language lets a program leave the field structure.

- *Casts.* A `struct S *` can be cast to a `struct T *` and used to read a field of `T`. A sound analysis matches fields by offset rather than by name, or treats the object as one location after such a cast. Structures with a common initial sequence share the offsets of that sequence.
- *Pointer arithmetic.* `p + i` with an unknown `i` may reach any field of the object. Analyses either collapse the object to one location or add every field to the target set.
- *Positive weight cycles.* The constraint for `p = &q->f` is an edge from `q` to `p` with a weight, the offset of `f`. A cycle of such edges with a positive total weight, as in a loop over `p = &p->next` where `next` is not the first field, keeps making new offsets. The analysis must bound the offsets by the size of the object. The variables on such a cycle do not have equal sets, so they must not be merged as the cycle elimination of [hybrid cycle detection](/hybrid-cycle-detection/) and its relatives merges a cycle of copies; Pearce, Kelly and Hankin treat these cycles in the solver.
- *Unions and `memcpy`.* Overlapping fields and block copies move many fields at once.

**Arrays** are the other aggregate. Most analyses keep one location for all elements of an array object, which is the array counterpart of field insensitivity; separating elements needs index analysis.

## Examples

The toy IR has no fields, so this example is in C:

```c
struct pair { int *f; int *g; };
int a, b, c;
struct pair s, t;

s.f = &a;
s.g = &b;
t.f = &c;
int *w = s.f;
```

| model | locations | pts(w) |
|---|---|---|
| field-sensitive | `s.f` = {a}, `s.g` = {b}, `t.f` = {c} | {a} |
| field-insensitive | `s` = {a, b}, `t` = {c} | {a, b} |
| field-based | `F_f` = {a, c}, `F_g` = {b} | {a, c} |

Only `a` is right. The field-insensitive model adds `b`, from the other field of the same object. The field-based model adds `c`, from the same field of another object. Neither answer contains the other, so neither model is more precise than the other in general.

## Where it is used

- **Java and other type-safe languages.** Field-sensitive analysis with one abstract object per allocation site is the usual default of points-to frameworks for Java, including the Datalog analyses surveyed by Smaragdakis and Balatsouras (2015). Field-based analysis is used when speed matters more, for example for call graph construction of large programs.
- **C and C++.** Compilers and tools model fields by offsets and fall back to whole-object locations for unsafe casts and unknown arithmetic. Steensgaard's original analysis treated a structure as one location ([Steensgaard's analysis](/steensgaard-analysis/)); later unification analyses keep fields apart.
- **Type-based alias analysis.** References to different fields never alias, and [type-based alias analysis](/type-based-alias-analysis/) uses this with field names and declared types alone.
- **CFL-reachability.** A field-sensitive store and load of the same field act as a matched pair of parentheses, so field-sensitive points-to questions for Java can be phrased as [CFL-reachability](/cfl-reachability/).
- **Optimization.** [Scalar replacement of aggregates](/scalar-replacement-of-aggregates/) needs to know that no pointer reaches one field through another, and [alias analysis](/alias-analysis/) of `s.f` against `s.g` relies on field-sensitive facts.

## References
