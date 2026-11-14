---
tag: P8C84R
kind: technique
slug: monomorphization
name: Monomorphization
aliases:
- template instantiation
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Compiles a polymorphic function by making one specialized copy for each set of type arguments it is used at.
prereqs: [hindley-milner-type-system, let-polymorphism]
see_also: [dictionary-passing-translation, type-classes, polymorphic-recursion-undecidability, system-f, function-inlining, partial-evaluation, defunctionalization, ml-typability-dexptime-completeness]
sources:
  - paper: doi:10.1017/S0956796898003086
    title: Andrew Tolmach and Dino P. Oliva, From ML to Ada, strongly-typed language interoperability via source translation, Journal of Functional Programming 8(4), 1998, pages 367 to 412
    locator: the translation of polymorphic ML code into monomorphic target code
  - url: http://www.mlton.org/guide/20210117/Monomorphise
    title: MLton User Guide (version 20210117), the Monomorphise pass
    locator: the pass from the XML to the SXML intermediate language, which duplicates datatypes and functions at each type they are used at; the note that the set of instances is finite because Standard ML has no polymorphic recursion
  - url: https://doc.rust-lang.org/book/ch10-01-syntax.html
    title: Steve Klabnik and Carol Nichols, The Rust Programming Language, Chapter 10.1
    locator: the section on the performance of code using generics, which describes monomorphization of generic functions and enums
  - url: https://eel.is/c++draft/temp.inst
    title: Working draft of the ISO C++ standard, section [temp.inst]
    locator: implicit instantiation of class and function templates when a specialization is used, and the implementation-defined limit on the depth of recursive instantiation
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 23 (System F, explicit type abstraction and application, and type erasure)
---

Monomorphization compiles a polymorphic program by making one copy of each polymorphic function, and of each polymorphic data type, for each list of types at which the program uses it. Each copy has plain types, so the compiler can choose the data layout for that type, call methods directly and inline them. Rust generics, C++ templates and the whole-program ML compiler MLton work this way. The method needs the whole program, it can make the code much larger, and it does not end when a function calls itself at a growing type, which is [polymorphic recursion](/polymorphic-recursion-undecidability/). The other way to compile polymorphism is one shared copy, with type classes compiled by the [dictionary-passing translation](/dictionary-passing-translation/).

## In plain words

A generic function, such as "swap the two parts of a pair", works for pairs of any types. The machine code for a pair of two bytes and for a pair of two large records is different, because the sizes differ. Monomorphization writes the generic function again for each concrete type that the program really uses. If the program swaps pairs of integers and pairs of strings, the compiler makes two copies, one for each. Each copy is fast, because it knows its types. The cost is size: many types give many copies. And if a generic function calls itself with a larger type each time, the list of copies never ends, so the compiler must stop with an error.

## When it applies

- The whole program is available, or at least every use of each polymorphic definition is, so that the set of type instances can be computed.
- Every use of a polymorphic name has known type arguments after type inference. In [Hindley-Milner](/hindley-milner-type-system/) and in [System F](/system-f/), inference or the programmer gives each use an explicit instantiation $f[\tau_1, \dots, \tau_n]$.
- The set of instances is finite. It is when no definition calls a member of its own recursive group at other type arguments (see the theorem below).
- Values do not hide their type behind a quantifier at run time. An existential package or a trait object (`dyn Trait`) has a type that is not known statically, so its methods need a dictionary.

## The template

### Instances

Let the program be a list of definitions $f = \Lambda \bar\alpha_f.\ e_f$ and a closed main expression. Each use of a definition $g$ inside $e_f$ has type arguments $\bar\theta$ whose free variables are among $\bar\alpha_f$. The *instance set* $I$ is the least set of pairs (definition, list of closed types) such that:

- every use $g[\bar u]$ in the main expression gives $(g, \bar u) \in I$;
- if $(f, \bar t) \in I$ and $e_f$ uses $g[\bar\theta]$, then $(g, [\bar t / \bar\alpha_f]\,\bar\theta) \in I$.

### The algorithm

```pseudo
MONOMORPHIZE(program)
L1  I ← ∅ ; W ← the uses g[u] in main, as pairs (g, u)
L2  while W is not empty do
L3      (f, t) ← pop(W)
L4      if (f, t) ∈ I then continue
L5      I ← I ∪ {(f, t)}
L6      b ← [t / α_f] e_f                       ▷ the body at closed types
L7      for each use g[θ] in b do                ▷ θ is closed now
L8          replace it by the name g_θ ; push (g, θ) on W
L9      emit the definition f_t = b, with type annotations erased or lowered
L10 replace each use g[u] in main by g_u
```

A use of a type class method at a closed type is resolved in line L8 to the code of the matching instance, so no dictionary remains. Data types are copied the same way: `list[int]` and `list[string]` become two types, each with its own layout.

### Correctness

**Meaning.** In the call-by-value semantics of the source, types are erased: $\Lambda \bar\alpha.\ e$ and $e[\bar\tau]$ step as $e$. Each emitted copy $f_{\bar t}$ erases to the erased body of $f$, and each renamed use $g_{\bar\theta}$ refers to a copy whose erased body is the erased body of $g$. So the relation "a term of the output and a term of the input are equal after erasure and after mapping each $g_{\bar\theta}$ to $g$" is preserved by each step of evaluation. Both programs take the same steps and return the same value, trap at the same point, or both run forever. Type classes add one condition: the instance selected in L8 must be the one that the dictionary translation would pass, which holds when instances do not overlap ([coherence](/type-classes/)).

**Typing.** Each copy $f_{\bar t}$ has the closed type $[\bar t / \bar\alpha_f]\,\tau_f$, by the type substitution lemma of the source system. So the output is a well-typed program with no type variables, and every later pass can treat it as monomorphic.

**Termination.** Each iteration of L2 to L9 removes one pair from $W$, and adds one new pair to $I$ or none. So the loop ends if and only if $I$ is finite, and then it runs $|I|$ times plus once per duplicate push.

**Theorem.** Group the definitions into the strongly connected components of the "uses" relation. If every use of a definition inside its own component has the component's own type variables as arguments (no polymorphic recursion), then $I$ is finite.

*Proof.* In ML-style systems, the members of one recursive group share their type variables $\bar\alpha$, because the group is typed with one monomorphic type per member and then generalized together. Order the components topologically, with main first. Induction on this order: the instances of a component $K$ come from uses in components before $K$, and from uses inside $K$. By the induction hypothesis the components before $K$ have finitely many instances, and each has finitely many uses, so they give finitely many pairs for $K$. A use inside $K$ maps $(f, \bar t)$ to $(g, [\bar t/\bar\alpha]\,\bar\alpha) = (g, \bar t)$, so it adds no new list of types, and $K$ has at most $|K|$ times as many instances as lists that come from outside. So each component has finitely many instances.

With polymorphic recursion the theorem fails: the examples show an instance set that is infinite. Compilers do not try to decide in advance whether the set is finite. They stop with an error at a fixed depth of nested instances.

### Cost

The output size is $\sum_{(f, \bar t) \in I} |e_f|$ plus the size of the copied types. The instance set can be exponential in the size of the program even without recursion, and a type in it can be doubly exponential as a tree (the second example). The same nesting of `let` definitions gives the lower bound in the proof that ML typability is [DEXPTIME-complete](/ml-typability-dexptime-completeness/). Compile time follows the output size. At run time, each copy calls its callees directly, and values need no boxing to a uniform size.

## Classic examples

**Two uses of the identity.** In `let id = fun x -> x in let both = fun y -> (id y, id true) in both 1`, inference gives `both` the scheme $\forall \beta.\ \beta \to \beta \times \mathsf{bool}$ and the uses `id[β]`, `id[bool]` inside it and `both[int]` in main. The algorithm pops `(both, int)`, emits `both_int = fun y -> (id_int y, id_bool true)`, and pushes `(id, int)` and `(id, bool)`. It then emits `id_int` and `id_bool`. The instance set has 3 elements and the result is `(1, true)` in both programs.

**Exponential growth without recursion.** Define

```text
let f0 = fun x -> (x, x)
let f1 = fun x -> f0 (f0 x)
let f2 = fun x -> f1 (f1 x)
...
let fk = fun x -> f(k-1) (f(k-1) x)
main: fk 1
```

Here $f_0 : \forall \alpha.\ \alpha \to \alpha \times \alpha$, and $f_i$ maps $\alpha$ to a full binary tree of pair types of depth $2^i$ with $\alpha$ at every leaf. One instance of $f_i$ at $t$ uses $f_{i-1}$ at $t$ and at the result type of $f_{i-1}$ on $t$, which differ. So $f_k$ has 1 copy, $f_{k-1}$ has 2, and $f_0$ has $2^k$, for $2^{k+1} - 1$ copies in all. The program has $k + 1$ definitions. For $k = 4$ the algorithm emits 31 copies, and the largest argument type of $f_0$ has 65535 nodes as a tree. The result type of $f_k$ has $2^{2^k + 1} - 1$ nodes as a tree but only $2^k + 1$ as a shared DAG, So a compiler that stores types as trees does doubly exponential work here. Sharing equal types by [hash-consing](/hash-consing/) keeps the work exponential.

**Polymorphic recursion does not end.** With a declared signature, Haskell and OCaml accept

```text
f : forall a. int -> a -> int
f = fun n -> fun x -> if n == 0 then 0 else 1 + f (n - 1) (x, x)
main: f 3 1
```

The instance $(f, \mathsf{int})$ uses $f$ at $\mathsf{int} \times \mathsf{int}$, which uses $f$ at $(\mathsf{int} \times \mathsf{int}) \times (\mathsf{int} \times \mathsf{int})$, and so on. The argument types have 1, 3, 7, 15, 31 nodes, and the set $I$ is infinite, although a run of `f 3 1` needs only 4 of these types. The number a run needs depends on the value of `n`, which the compiler does not know. The same function in Rust, `fn f<T: Clone>(n: u32, x: T) -> u32` with the call `f(n - 1, (x.clone(), x))`, passes the type checker and then stops the build when the nesting of instances reaches the compiler's recursion limit. With dictionary passing, one copy of `f` runs for every `n`.

**Rust generics and trait objects.** A function `fn largest<T: PartialOrd + Copy>(xs: &[T]) -> T` called on a slice of `i32` and a slice of `char` compiles to two functions, each with a direct comparison. A `&dyn Display` argument instead carries a pointer to a table of methods, and one compiled copy serves all types. A trait with a generic method cannot be used as `dyn Trait`: the table has a fixed number of entries, but the method would need one entry per type.

## Variations

- **Run-time specialization.** The .NET runtime makes a specialized copy of a generic method when a call at a new type first runs. It shares one copy among all reference types and specializes for value types, whose sizes differ. Since copies are made only on demand, polymorphic recursion makes only the copies that the run needs.
- **Specialization by shape.** Go 1.18 generics make one copy per "GC shape" (types with the same layout share a copy) and pass a dictionary for the rest. Swift compiles generics with witness tables, which are dictionaries, and specializes as an optimization.
- **Partial monomorphization.** A compiler can keep dictionary passing in general and specialize only hot functions or known calls. This is [partial evaluation](/partial-evaluation/) on type and dictionary arguments.
- **Whole-program pipelines.** MLton runs monomorphization, then converts closures to a first-order form that is close to [defunctionalization](/defunctionalization/), so that the later passes see a first-order, monomorphic program.

## Pitfalls

- **Code growth.** Each new type argument copies the whole body, and the callees of the body. The exponential example is small, but heavy generic code in real Rust and C++ programs also makes large binaries and long builds. Factoring the part that does not depend on the type into a non-generic helper reduces it.
- **Separate compilation.** Two compilation units that use `vec<int>` both make a copy. The linker must merge them (C++ vague linkage and COMDAT sections), or the toolchain must share instances across units.
- **Errors at the copy.** C++ checks a template body mostly at each use, so a type error appears at the instance, far from the template. Rust and ML check the generic body once, so monomorphization of a well-typed program cannot fail with a type error, only with the depth limit.
- **Polymorphic recursion.** The compiler cannot accept it with monomorphization alone. It needs a depth limit, an error, or a fallback to a uniform representation.
- **Do not confuse it with inlining.** [Function inlining](/function-inlining/) copies a body into each call site. Monomorphization makes one copy per type list and shares it among all calls at that type.

## Exercises

1. List the instance set of `let k = fun x -> fun y -> x in (k 1 true, k false 2, k 3 4)`. *Answer.* $k$ has the scheme $\forall \alpha \beta.\ \alpha \to \beta \to \alpha$. The uses are $k[\mathsf{int}, \mathsf{bool}]$, $k[\mathsf{bool}, \mathsf{int}]$ and $k[\mathsf{int}, \mathsf{int}]$, so there are 3 copies.
2. In the exponential example with $k = 3$, how many copies of $f_0$ and how many copies in all? *Answer.* $2^3 = 8$ copies of $f_0$ and $2^4 - 1 = 15$ in all.
3. Change the polymorphic recursion example so that it recurses at the same type, `f (n - 1) x`. What is the instance set for `main: f 3 1`? *Answer.* $\{(f, \mathsf{int})\}$: the recursive use maps $\mathsf{int}$ to $\mathsf{int}$.
4. Why does the theorem need that the members of a recursive group share their type variables? *Answer.* If a member $g$ of the group could use $f$ at a type built from its own variables in a new way, a cycle $f \to g \to f$ could grow the type argument on each turn. That is polymorphic recursion through two definitions.

## References
