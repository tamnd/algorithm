---
tag: FMJ8XA
kind: algorithm
slug: type-based-alias-analysis
name: Type-based alias analysis
aliases:
- TBAA
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Decides that two references cannot alias when their declared types are incompatible under the rules of a type-safe language.
solves: [alias-analysis]
model: word-ram
complexity:
  vars: {t: the number of types, h: the height of the type tree, m: the number of statements}
  time: {worst: O(t^2 h + m log t)}
  space: {extra: O(t^2)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1998
  people: [Amer Diwan, Kathryn S. McKinley, J. Eliot B. Moss]
  note: Diwan, McKinley and Moss gave TypeDecl, FieldTypeDecl and SMTypeRefs for Modula-3 and measured them with redundant load elimination.
prereqs: [subtyping, disjoint-set-forest, alias-analysis]
see_also: [points-to-analysis, field-sensitivity, steensgaard-analysis, class-hierarchy-analysis, type-system, mod-ref-analysis, loop-invariant-code-motion, scalar-replacement-of-aggregates]
sources:
  - paper: doi:10.1145/277650.277670
    title: Amer Diwan, Kathryn S. McKinley and J. Eliot B. Moss, Type-based alias analysis, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '98), 106 to 117, 1998
    locator: whole paper (TypeDecl, FieldTypeDecl, the selective merging of SMTypeRefs, and the evaluation with redundant load elimination on Modula-3 programs)
  - paper: "ISO/IEC 9899:2011, Programming languages, C"
    locator: 6.5, paragraph 7 (the types through which the stored value of an object may be accessed, the rule that C compilers use for type-based alias analysis)
  - paper: doi:10.1561/2500000014
    title: Yannis Smaragdakis and George Balatsouras, Pointer Analysis, Foundations and Trends in Programming Languages 2(1), 1 to 69, 2015
    locator: the discussion of type information as a filter on points-to facts
---

Type-based alias analysis answers [alias analysis](/alias-analysis/) queries from the types of a program alone. In a type-safe language, a reference of declared type $T$ can only reach objects whose class is $T$ or a subtype of $T$. So two references can touch the same memory only if their types share a subtype. The analysis needs no [points-to analysis](/points-to-analysis/), costs almost nothing, and works on a part of a program. Diwan, McKinley and Moss (1998) gave three forms of growing precision: TypeDecl compares the declared types, FieldTypeDecl also compares the field names, and SMTypeRefs also looks at which types the program assigns to each other. C compilers use a form of the same idea, based on the rule of the C standard about the types through which an object may be accessed.

## In plain words

In a language where the types cannot lie, a variable that is declared to hold a car can never hold a house. So a write through a car variable cannot change a house. A compiler can use this fact to keep a value in a register, or to move a read past a write, without a costly study of the whole program. The basic form only asks whether the two declared types could describe the same object. A better form also says that two different fields of objects never overlap. The best form also notes which types the program really mixes: if the program never puts a sports car into a car variable, then a car variable and a sports car variable never meet, even though one type is a kind of the other.

## The problem

The input is a well-typed program in a language with classes and fields, and two memory references $q_1.f_1$ and $q_2.f_2$, each the field of the object that a variable holds. The question is whether some run can make them touch the same field of the same object. A "no" must be true for every run; a "yes" may be wrong. The analysis is flow-insensitive: it ignores the order of the statements, but not the statements that the control flow gives.

The toy language has a tree of classes, with $C \le D$ when $C$ is $D$ or a descendant of $D$, and $Sub(D) = \{C : C \le D\}$. Each variable $v$ has a declared class $T(v)$, and each field $f$ has a declared type $FT(f)$. The statements are `p = new C`, `p = q`, `p = q.f` and `q.f = p`, each allowed only if the type of the value is a subtype of the type of the place: an upcast is fine, a downcast is not. SMTypeRefs as a data-flow analysis:

| item | value |
|---|---|
| direction | none: one answer for the whole program |
| may or must | may |
| domain | partitions of the set of types into groups |
| order | a finer partition is lower (bottom is precise) |
| join | the finest partition coarser than both |
| bottom and top | every type in its own group, and one group for all types |
| boundary value | none, there is no entry or exit point |
| initial value | every type in its own group |
| transfer | each statement that moves a value from type $A$ to a place of type $B$ merges the groups of $A$ and $B$; monotone, and the result does not depend on the order |

## The algorithm

TypeDecl says that $q_1.f_1$ and $q_2.f_2$ may alias if $Sub(FT(f_1)) \cap Sub(FT(f_2)) \neq \emptyset$. FieldTypeDecl says so only if $f_1 = f_2$ and $Sub(T(q_1)) \cap Sub(T(q_2)) \neq \emptyset$, since different fields never overlap in a type-safe language. SMTypeRefs, or selective merging, puts the types in groups with a [disjoint-set forest](/disjoint-set-forest/), and replaces $Sub(D)$ by $TypeRefs(D)$, the subtypes of $D$ that the program can really store in a place of type $D$.

```pseudo id=main
TYPE-REFS(P)
L1  for each class C do make a group with C alone
L2  for each statement of P that moves a value of type A into a place of type B do
L3      if A is not B then UNION(A, B)
L4  for each class D do TypeRefs[D] <- {C in Sub(D) : FIND(C) = FIND(D)}
L5  return TypeRefs

SM-MAY-ALIAS(q1.f1, q2.f2)
L6  if f1 is not f2 then return false
L7  return true if TypeRefs[T(q1)] and TypeRefs[T(q2)] have a common class, else false
```

In line L2, `p = new C` moves a value of type $C$ into $p$, `p = q` moves $T(q)$ into $T(p)$, `p = q.f` moves $FT(f)$ into $T(p)$, and `q.f = p` moves $T(p)$ into $FT(f)$. Lines L6 and L7 are the field test of FieldTypeDecl with $TypeRefs$ in place of $Sub$; Diwan, McKinley and Moss call this combination SMFieldTypeRefs.

## Example

A program in a Java-like notation. The class `Object` has a field `val` of type `Object`, the class `A` has a field `next` of type `A`, and `A1` and `A2` extend `A`, and `B` extends `Object`.

```
A1 x; A2 y; A a; Object o; A t;
x = new A1;        // 0
y = new A2;        // 1
a = y;             // 2
x.next = a;        // 3
y.next = a;        // 4
o = new B;         // 5
o.val = o;         // 6
t = a.next;        // 7
```

Line L3 merges `A2` with `A` (statement 2) and `B` with `Object` (statement 5); the other statements move a value between equal types. So $TypeRefs(A) = \{A, A2\}$, $TypeRefs(A1) = \{A1\}$ and $TypeRefs(A2) = \{A2\}$. The memory references are in statements 3, 4, 6 and 7.

| references | TypeDecl | FieldTypeDecl | SMTypeRefs | some run |
|---|---|---|---|---|
| `x.next`, `y.next` (3, 4) | yes | no: $A1$ and $A2$ share no subtype | no | no |
| `x.next`, `a.next` (3, 7) | yes | yes: $A1 \le A$ | no: $A1 \notin TypeRefs(A)$ | no |
| `y.next`, `a.next` (4, 7) | yes | yes | yes: $A2$ is in both | yes |
| `o.val` and any `next` (6 with 3, 4, 7) | yes | no: different fields | no | no |

The pair (4, 7) really aliases, since `a = y`. Every form says yes for it. SMTypeRefs is exact here. FieldTypeDecl says yes for (3, 7) because `a` could hold an `A1` by its type, but no statement ever puts one there.

## Correctness

The full proof is in the proof file. Its steps:

1. **The run invariant.** At every moment of every run, an object of class $D$ held by a variable $v$ has $D \le T(v)$ and $D$ in the group of $T(v)$, and the same for the fields. The proof is by induction over the steps: each statement moves an object from a place of type $A$ to a place of type $B$, the typing rule gives $A \le B$, and line L3 put $A$ and $B$ in one group.
2. **Soundness.** If two references touch the field $f$ of one object of class $D$, then $D$ is in $TypeRefs$ of both base types, so SMTypeRefs answers yes.
3. **Each form refines the one before.** $TypeRefs(D) \subseteq Sub(D)$, and equal fields have equal declared types.

So the three answers are sound, and SMTypeRefs is the most precise of them.

## Complexity

**Proved.** With $t$ types in a tree of height $h$ and $m$ statements, lines L1 to L3 take $O(t + m \log t)$ time with path compression, and $O((t + m)\,\alpha(t + m))$ with union by rank as well. Line L4 takes $O(t^2 h)$ time and $O(t^2)$ space. A query takes $O(t)$ time with sets, or $O(1)$ with a table of all pairs of types. TypeDecl and FieldTypeDecl need no pass over the statements at all.

**Stated in the paper, not proved here.** Diwan, McKinley and Moss measured the three forms on Modula-3 programs with redundant load elimination. They report that FieldTypeDecl and SMTypeRefs are much more precise than TypeDecl, that the optimization based on them removes a useful share of the loads, and, by a limit study, that a more precise alias analysis would remove few more loads in their programs. They also discuss its use on incomplete programs, where a part of the code is not known.

**Measured, not proved.** On 200 seeded random well-typed programs of 30 statements over six classes and four fields, with 5967 pairs of references in all, TypeDecl says yes for all 5967, FieldTypeDecl for 2860, SMTypeRefs for 2852, and the runs of the test file touched one field of one object from 1950 of the pairs. The random programs mix their types a lot, so selective merging finds little to separate there.

## Properties

- **Sound for type-safe programs.** In any run, two references that touch the same location get "may alias".
- **Flow-insensitive and context-insensitive.** It uses no order of statements and no calling context.
- **Cheap and modular.** TypeDecl and FieldTypeDecl need only the declarations. SMTypeRefs needs one linear pass over the assignments.
- **Coarse for one type.** Two references of the same type and field always may alias. To tell apart two lists of the same type, a points-to analysis is needed.
- **A filter.** Points-to analyses for typed languages often use the types to drop facts that the type rules forbid, which gives both precision and speed.

## Variants and improvements

- **C and strict aliasing.** C is not type-safe, but the standard (C11, 6.5, paragraph 7) lets an object be accessed only through an lvalue of a compatible type, a signed or unsigned variant of it, a qualified version, an aggregate or union that contains such a member, or a character type. A program that breaks the rule has undefined behavior, so a compiler may assume that an `int *` and a `float *` do not point to the same object. Character types are the exception: a `char *` may alias anything. GCC and Clang use this rule, and the flag `-fno-strict-aliasing` turns it off.
- **Type trees in a compiler.** LLVM attaches type descriptors to loads and stores as metadata, in a tree whose root is the character type, and answers queries by the ancestor relation in the tree. Access to a field of a structure carries the structure type and the offset, which gives a form of FieldTypeDecl.
- **Combined with points-to analysis.** [Field sensitivity](/field-sensitivity/) gives the field test of FieldTypeDecl inside a points-to analysis, and a type filter in [Steensgaard's analysis](/steensgaard-analysis/) or in Andersen's analysis keeps apart the targets of pointers of unrelated types.
- **Class hierarchy analysis.** The same subtype sets that TypeDecl uses also give the possible targets of a virtual call in [class hierarchy analysis](/class-hierarchy-analysis/).

## When to use it

Use it as the first and cheapest alias analysis in a compiler for a type-safe language, or for C and C++ code that follows the strict aliasing rule. It helps [loop-invariant code motion](/loop-invariant-code-motion/), [scalar replacement of aggregates](/scalar-replacement-of-aggregates/), redundant load elimination and instruction scheduling, which need to know that a store does not change a value in a register. When many references have the same type, add a points-to analysis.

## Pitfalls

- **Code that breaks the type rules.** In C, code that reads a `float` through an `int *`, or that uses a cast to reinterpret memory, has undefined behavior, and type-based alias analysis can turn it into a wrong result. Use a union, `memcpy`, or a character type for such access, or compile with strict aliasing off.
- **Forgetting the character types.** A C alias analysis that treats `char` like any other type misses the aliases of `memcpy` and of byte-wise code.
- **Implicit assignments.** Selective merging must see every move of a value between types: parameters and return values, array stores, and the values that a library or unknown code writes. A missing merge makes the answer unsound.
- **Downcasts.** A checked downcast moves a value from type $A$ to a subtype $B$ and must also merge $A$ and $B$; the toy language of this page has no downcasts.
- **Same type, different objects.** The analysis cannot tell apart two objects of one type. Do not use it to show that two `next` fields of different lists never alias.

## Implementations

## History

Type information was used for alias questions in compilers for typed languages before 1998, but Diwan, McKinley and Moss (1998) gave the first careful study: three forms of the analysis, with their soundness argument for Modula-3, and their effect on redundant load elimination, measured against a limit. The C89 and later C standards had the rule about the types through which an object may be accessed, and GCC and other compilers began to use it for alias analysis around the same time, which made the strict aliasing rule widely known to C programmers. LLVM later made type-based alias information part of its intermediate representation, as metadata that the front end attaches to each memory access.

## References
