---
tag: Z4W0CQ
kind: concept
slug: row-polymorphism
name: Row polymorphism
aliases:
- row variables
- extensible records typing
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Types records and variants with a row variable for the unknown fields, so a function can accept any record that has some fields.
prereqs: [hindley-milner-type-system, most-general-unifier]
see_also: [subtyping, constraint-based-type-inference, let-polymorphism, algorithm-j, equational-unification, effect-system, recursive-types, type-classes]
sources:
  - paper: "Mitchell Wand, Complete type inference for simple objects, Second Annual IEEE Symposium on Logic in Computer Science (LICS 1987), with a corrigendum at LICS 1988"
    locator: whole paper (record types with a variable for the remaining fields, and type inference for them by unification)
  - paper: doi:10.1145/75277.75284
    title: Didier Rémy, Type checking records and variants in a natural extension of ML, Sixteenth ACM Symposium on Principles of Programming Languages (POPL 1989), pages 77 to 88
    locator: whole paper (rows with the field flags pre and abs, sorted row variables, and principal types for records and variants)
  - book: isbn:9780262162289
    title: François Pottier and Didier Rémy, The essence of ML type inference, Chapter 10 of Benjamin C. Pierce (editor), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 10, the part on rows (row terms, the equations between them, and their unification)
  - paper: "Jacques Garrigue, Programming with polymorphic variants, ACM SIGPLAN Workshop on ML, 1998"
    locator: whole paper (the polymorphic variants of OCaml and their typing with rows and bounds)
  - paper: "Didier Rémy and Jérôme Vouillon, Objective ML: An effective object-oriented extension to ML, Theory and Practice of Object Systems 4(1), 1998"
    locator: whole paper (the object types of OCaml, with a row variable for the other methods)
---

Row polymorphism types records and variants by naming the fields that a piece of code needs and putting a *row variable* for all the other fields. The function `fun r -> r.x + 1` gets the type $\forall \rho.\, \{x : \mathsf{int} \mid \rho\} \to \mathsf{int}$, and it accepts any record with an integer field `x`, whatever its other fields are. Because $\rho$ is an ordinary type variable of a new kind, the [Hindley-Milner](/hindley-milner-type-system/) machinery still works: type inference is unification, now modulo the reordering of fields, and every typable term keeps a principal type. Wand (1987) introduced row variables, and Rémy (1989) gave the form with field flags that most systems follow. Row polymorphism is the inference-friendly alternative to [subtyping](/subtyping/) for records. It types the objects and polymorphic variants of OCaml and the records of PureScript and Elm.

## In plain words

Suppose a function only reads the field called `x` of a record. It should accept any record that has an `x`, whether it has two other fields or twenty.

Row polymorphism writes the type of such a record as "a field `x` that holds a number, and then some other fields that we do not care about". The "other fields" part is a placeholder, like a blank that the type checker fills in at each call. At one call the blank stands for a field `y`. At another call it stands for nothing at all.

Because the blank is filled in, nothing is forgotten. A function that takes a record and returns it gives back a record with all of its fields. The type checker can also find these types by itself, with no help from the programmer, in the same way it finds ordinary ML types.

## The idea

**Rows.** A *row* describes the fields of a record. A row is either a row variable $\rho$, the empty row, or a field followed by a row:

```text
row ::= r | empty | (l : tau ; row)
{ row }                                    a record type
[ row ]                                    a variant type
```

Rows are equal up to the order of distinct labels, and this is the only new equation:

```text
(l : t ; l' : t' ; row)  =  (l' : t' ; l : t ; row)       when l and l' differ        Row-Swap
```

A label must occur at most once in a row. So each row variable carries a *kind*, the set of labels that it must not contain. In $\{x : \mathsf{int} \mid \rho\}$, the variable $\rho$ has a kind that excludes `x`.

**Unification.** Unification of rows extends the [most general unifier](/most-general-unifier/) algorithm with one rule for two rows that start with different labels:

```text
unify (l : t ; r) with (l' : t' ; r')
  if l = l'              unify t with t', then r with r'
  if l <> l'             r'' fresh, excluding l and l';  unify r with (l' : t' ; r''), then r' with (l : t ; r'')
  if r and r' are the same variable and l <> l'           fail, like the occurs check
```

The theory of Row-Swap is still *unitary*: two unifiable rows have a most general unifier. So [algorithm W](/algorithm-w/), [algorithm J](/algorithm-j/) and [constraint-based inference](/constraint-based-type-inference/) work unchanged, with this unification in place of the plain one, and principal types remain.

**Operations.** In Wand's system a row lists only the fields that are present. Rémy made rows total: each label has a field type, either $\mathsf{pre}\,\tau$ (present with type $\tau$) or $\mathsf{abs}$ (absent), and a row variable can also stand for a flag. The basic operations then have these types:

```text
{}                    : { abs }                                       every label absent
r.l                   : forall a r. { l : pre a ; r } -> a              selection
{ r with l = v }      : forall a f r. { l : f ; r } -> a -> { l : pre a ; r }    extension or update
r \ l                 : forall f r. { l : f ; r } -> { l : abs ; r }        removal
```

The variable $f$ in extension and removal ranges over the flags, so the operations work whether the field is there or not. Wand (1987) let extension add a field that might already be present, and some terms then had no principal type. His 1988 corrigendum noted the problem. The flags of Rémy (1989) solve it.

**Rows and subtyping.** Width [subtyping](/subtyping/) also lets a function take records with extra fields, but it forgets them: `fun r -> r` at type $\{x : \mathsf{int}\} \to \{x : \mathsf{int}\}$ returns a value whose other fields the type no longer shows. With rows the type is $\forall \rho.\, \{x : \mathsf{int} \mid \rho\} \to \{x : \mathsf{int} \mid \rho\}$, and the caller keeps the fields. Rows also keep type inference decidable and complete, which subtyping makes much harder. In return, rows cannot put records with different fields in one list without a coercion, which subtyping can.

## Examples

**One field.** `fun r -> r.x + 1` has the type $\forall \rho.\, \{x : \mathsf{int} \mid \rho\} \to \mathsf{int}$. Applied to `{x = 1; y = true}`, unification sets $\rho = (y : \mathsf{bool})$. Applied to `{y = true}`, it fails: the row $(y : \mathsf{bool})$ has no field `x`, and its tail is the empty row, not a variable.

**Two fields.** In `fun r -> r.x + r.y`, the first selection gives `r` the type $\{x : \alpha \mid \rho_1\}$ and the second the type $\{y : \beta \mid \rho_2\}$. Unifying them starts with different labels, so the rule makes a fresh $\rho_3$ and sets $\rho_1 = (y : \beta ; \rho_3)$ and $\rho_2 = (x : \alpha ; \rho_3)$. With `+`, the function has the type $\forall \rho_3.\, \{x : \mathsf{int} ; y : \mathsf{int} \mid \rho_3\} \to \mathsf{int}$.

**OCaml objects.** OCaml writes the row variable of an object type as `..`:

```ocaml
let get_x o = o#x + 1
(* val get_x : < x : int; .. > -> int *)
```

The method call `o#x` is typed like the selection above. A closed object type such as `< x : int >` has the empty row.

**OCaml polymorphic variants.** The type of a variant lists the tags, and the row is written with bounds:

```ocaml
let f = function `A -> 1 | `B -> 2
(* val f : [< `A | `B ] -> int *)
let a = `A
(* val a : [> `A ] *)
```

The type `` [< `A | `B ] `` accepts any variant with at most these tags, and `` [> `A ] `` is a variant with at least the tag `` `A ``. So `f a` is typable, and its row is solved to `` [ `A | `B ] `` or a part of it. Garrigue (1998) describes the typing.

**PureScript records.** PureScript writes rows directly in its record types:

```haskell
getX :: forall r. { x :: Int | r } -> Int
getX rec = rec.x
```

Here `getX { x: 1, y: "a" }` and `getX { x: 2 }` both type check, with `r` set to `( y :: String )` and to the empty row.

## Where it is used

- **OCaml.** Object types with `..`, as designed by Rémy and Vouillon in Objective ML, and polymorphic variants, by Garrigue. Both are inferred, with no annotations.
- **PureScript.** Records are typed with rows, and rows are a kind of their own, so libraries can be generic over rows. Earlier versions also tracked effects with rows.
- **Elm.** Extensible record types such as `{ a | x : Int }` give functions that read some fields of any larger record.
- **Effect systems.** Languages such as Koka describe the effects of a function by a row of effect labels, with a row variable for the effects of callbacks, see [effect systems](/effect-system/).
- **Type inference frameworks.** Rows fit into [constraint-based type inference](/constraint-based-type-inference/) as one more equational theory. Pottier and Rémy (2005) treat them in their chapter on ML inference.
- **Variations.** Some systems, such as Leijen's scoped labels, allow a label to occur twice in a row, where the second occurrence is hidden by the first. Others add record concatenation, which is harder to type with rows.

## References
