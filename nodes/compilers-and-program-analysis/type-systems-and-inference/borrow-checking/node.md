---
tag: KMWYHF
kind: technique
slug: borrow-checking
name: Borrow checking
aliases:
- ownership and borrowing
- non-lexical lifetimes
area: compilers-and-program-analysis/type-systems-and-inference
level: research
summary: Checks that each reference to owned memory lives no longer than its owner and that no mutable reference is aliased, without a garbage collector.
prereqs: [control-flow-graph, live-variable-analysis, linear-types]
see_also: [region-based-memory-management, effect-system, alias-analysis, reaching-definitions, worklist-dataflow-algorithm, separation-logic, escape-analysis, subtyping]
sources:
  - url: https://rust-lang.github.io/rfcs/2094-nll.html
    title: Niko Matsakis, Rust RFC 2094, Non-lexical lifetimes, 2017
    locator: the problem cases 1 to 4, lifetimes as sets of points, liveness and outlives constraints, the solver, loans in scope, and the check of each access against the loans in scope
  - url: https://rustc-dev-guide.rust-lang.org/borrow-check/region-inference.html
    title: Rust Compiler Development Guide, MIR borrow check, region inference
    locator: region values as sets of MIR locations with end points for universal regions, liveness constraints, and the propagation of outlives constraints
  - url: https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
    title: Steve Klabnik and Carol Nichols, The Rust Programming Language, Chapter 4.2
    locator: the rules for references, one mutable reference or any number of shared references, and dangling references
  - url: https://doc.rust-lang.org/reference/
    title: The Rust Reference
    locator: the chapters on ownership-related behavior, lifetimes and lifetime elision (general; the Reference does not give the borrow checking algorithm)
  - paper: doi:10.48550/arXiv.1903.00982
    title: Aaron Weiss, Olek Gierczak, Daniel Patterson and Amal Ahmed, Oxide, the essence of Rust, arXiv:1903.00982, version 4, 2021 (version 1 of 2019 lists Aaron Weiss, Daniel Patterson, Nicholas D. Matsakis and Amal Ahmed)
    locator: lifetimes read as approximate provenances, the flow-sensitive substructural typing judgment, and the syntactic proof of type safety by progress and preservation
  - paper: doi:10.1145/3158154
    title: Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers and Derek Dreyer, RustBelt, securing the foundations of the Rust programming language, Proceedings of the ACM on Programming Languages 2(POPL), Article 66, 2018
    locator: the core language lambda-Rust, the lifetime logic, the semantic model of types in Iris, and the proofs for standard library types that use unsafe code
---

Borrow checking is the static analysis in the Rust compiler that lets a program take temporary references to memory that some variable owns, and proves that no reference outlives the memory and that no memory is changed while another reference can read it. It works on top of an affine type system, in which a value has one owner and is moved, not copied, on use ([linear types](/linear-types/) explains affine against linear). The rule it enforces at each program point is: one mutable reference, or any number of shared references, but not both. Unlike [region-based memory management](/region-based-memory-management/), it does not decide when memory is freed; the owner decides that, and the checker only rejects programs that would use a reference after that point. Unlike an [alias analysis](/alias-analysis/), it does not compute aliases of an arbitrary program; it rejects programs whose aliasing it cannot prove safe. There is no single classic paper for it: the algorithm is defined by Rust RFC 2094 and by the compiler, and the formal models are Oxide and RustBelt.

## In plain words

In Rust each value has one owner. When the owner goes away, the value is freed. You can lend the value out with a reference, in two ways: many readers at once, or a single writer alone. The borrow checker checks the loans. It looks at each place where a reference is created and each place where the reference is still going to be used later. Between those places, the loan is active. While a loan is active, the owner may not do anything that would break it: it may not free the value, move it, or change it while readers exist. When the reference is used for the last time, the loan ends, even if the variable that holds it stays in scope. The checker runs at compile time and costs nothing at run time.

## When it applies

- The language has owned values with move semantics, and reference types that carry a *lifetime* parameter, as `&'a T` and `&'a mut T` in Rust.
- Functions declare in their signatures how the lifetimes of their arguments and results are related, so the check is done one function at a time. Inside a function, the lifetimes are inferred.
- The function body is in a [control-flow graph](/control-flow-graph/) form after type checking. In rustc this is MIR, where each statement has a *point* (a location).
- Code inside `unsafe` blocks may use raw pointers, which are not checked. The safety of such code is the programmer's duty, and the formal models are needed to state what that duty is.

## The template

The algorithm of RFC 2094, as implemented in rustc, has four steps. A *lifetime* (also called a region) is a set of points of the CFG. A *loan* is the result of one borrow expression: its path (such as `v` or `x.f`), its kind (shared or mutable), and its lifetime.

```pseudo
BORROW-CHECK(cfg)
L1  for each reference type in each local variable, make a lifetime variable 'r
L2  LIVE ← live variables at each point                    ▷ backward dataflow
L3  for each point P, each variable x in LIVE(P), each 'r in the type of x
L4      add P to 'r                                       ▷ liveness constraint
L5  C ← outlives constraints 'a : 'b from subtyping at assignments, calls and reborrows
L6  repeat
L7      for each 'a : 'b in C do 'a ← 'a ∪ 'b
L8  until no lifetime changes
L9  IN-SCOPE ← forward dataflow over loans: gen a loan at its borrow,
L10     kill it at points outside its lifetime and where its path is overwritten
L11 for each point P and each access (read, write, move, free) of a path p at P
L12     for each loan l in IN-SCOPE(P) whose path overlaps p
L13         if l is mutable or the access writes, moves or frees then report an error
```

**Lifetimes from liveness.** A reference stored in a [live variable](/live-variable-analysis/) at point $P$ may still be used after $P$, so its lifetime must contain $P$ (lines L2 to L4). This is the main change from the older checker, in which a lifetime was a lexical scope.

**Outlives constraints.** Copying a reference of type `&'b T` into a place of type `&'a T` needs `&'b T` to be a [subtype](/subtyping/) of `&'a T`, that is, `'b: 'a` ("`'b` outlives `'a`"). As sets of points this means $'b \supseteq 'a$. The RFC states these constraints at a point, so that `'b` must include only the points of `'a` that are reachable from the assignment. rustc uses the simpler form without the point: it adds all of `'a` to `'b`. A lifetime parameter of the function signature, such as `'r` in `fn f<'r>(x: &'r T)`, is a *universal* lifetime. It contains every point of the body and an element $\mathrm{end}('r)$ that stands for the caller's code after the return.

**Solving.** Lines L6 to L8 compute the least lifetimes that satisfy the constraints, by [fixed-point iteration](/worklist-dataflow-algorithm/). Each lifetime only grows and is a subset of a finite set of points, so the loop ends after at most (number of lifetimes) times (number of points) additions.

**Loans in scope.** A loan is in scope at $Q$ if $Q$ can be reached from the borrow along points of the loan's lifetime, and the borrowed path is not assigned again on the way. This is a gen and kill problem, like [reaching definitions](/reaching-definitions/).

**Conflicts.** Two paths overlap if one is a prefix of the other: `x` and `x.f` overlap, `x.f` and `x.g` do not. A shared loan forbids writes, moves and frees of overlapping paths. A mutable loan forbids every access to them that does not go through the loan. Moves are checked by a separate "maybe moved" dataflow, which rejects a use of a value after it was moved.

**Why accepted programs are safe.** Suppose a reference `r` from a loan of `x` is dereferenced at $Q$, and `x` is freed or moved at $F$ on a path from the borrow to $Q$. Then `r` (or a reference copied from it) is live at $F$, since it is used later at $Q$. So the lifetime of the loan contains $F$ by the liveness and outlives constraints, the loan is in scope at $F$, and the free at $F$ conflicts with it. The same argument shows that a write through `x` cannot happen while a shared reference is still to be used, and that two mutable references to overlapping paths are never both live. This is an argument about the analysis, not a proof about the whole language. The formal results are in two models. Oxide (Weiss et al.) gives a flow-sensitive substructural type system, in which a lifetime is an approximate *provenance* (a set of loans), and proves syntactic type safety by progress and preservation. RustBelt (Jung et al. 2018) gives a semantic model of a core of Rust in the Iris separation logic and proves that the type system is sound, and that some standard library types built with `unsafe` code are safe to use. Neither model is the code of rustc.

## Classic examples

**A loan that ends at the last use.**

```rust
let mut v = vec![1, 2, 3];   // P0
let r = &v;                  // P1: loan L of v, shared, r : &'a Vec<i32>
println!("{}", r[0]);        // P2: last use of r
v.push(4);                   // P3: mutable borrow of v for push
```

`r` is live after P1 up to P2, so `'a` contains the points P1 and P2 and not P3. The loan L is not in scope at P3, and `push` is accepted. If the `println!` is moved after `v.push(4)`, then `r` is live at P3, L is in scope at P3, and the mutable borrow of `v` conflicts with the shared loan L: rustc reports error E0502. A checker with lexical lifetimes gives `'a` the whole block in which `r` is declared, and rejects both versions.

**Mutable references are not aliased.**

```rust
let mut x = 0;
let a = &mut x;
let b = &x;        // error: x is mutably borrowed by a, which is used below
*a += 1;
```

The use of `a` on the last line keeps the mutable loan in scope at the line of `b`, and a shared borrow of `x` is an access that does not go through the loan. Removing the last line, or moving it above `let b`, makes the program correct.

**A dangling reference.**

```rust
fn dangle() -> &'static String {
    let s = String::from("hi");
    &s                 // error: returns a reference to a local variable
}
```

The result has lifetime `'static`, which contains every point of the body and the caller's code after the return. So the loan of `s` is in scope at the end of the function, where `s` is freed, and that free conflicts with the loan.

**Problem case 3 of the RFC, still rejected.**

```rust
fn get_default<'r, K: Hash + Eq + Copy, V: Default>(map: &'r mut HashMap<K, V>, key: K) -> &'r mut V {
    match map.get_mut(&key) {
        Some(value) => value,
        None => {
            map.insert(key, V::default());   // error: map is still mutably borrowed
            map.get_mut(&key).unwrap()
        }
    }
}
```

In the `Some` arm, the loan from the first `get_mut` flows into the result, so its lifetime must be at least `'r`. `'r` is universal and contains every point of the body, so the loan is also in scope in the `None` arm, where no reference from it exists. The program is safe, but rustc rejects it. Polonius, a newer formulation in which a lifetime is a set of loans computed per point, accepts it.

## Variations

- **Lexical lifetimes.** Before the 2018 edition, rustc gave each lifetime a lexical scope (a subtree of the block structure). The analysis was simpler and rejected the first example above.
- **Two-phase borrows.** `v.push(v.len())` desugars to `Vec::push(&mut v, Vec::len(&v))`. The mutable borrow is first *reserved* and becomes active only at the call, so the shared borrow for `len` in between is accepted (Rust RFC 2025).
- **Polonius.** Lifetimes are computed as sets of loans at each point, by Datalog rules over the CFG. It is location-sensitive and accepts problem case 3, at a higher cost.
- **Dynamic models of aliasing.** Stacked Borrows and Tree Borrows define which raw pointer accesses in `unsafe` code are allowed, so that the compiler can rely on the absence of aliasing. The Miri interpreter checks them at run time.
- **Other languages.** Cyclone checked region lifetimes of pointers earlier. Swift enforces exclusive access to variables during a modification, statically where it can and with run-time checks for the rest.

## Pitfalls

- **Lifetime is not scope.** A reference's lifetime ends at its last use, not at the end of its block. The value it points to lives until its owner is dropped, which is a different event.
- **The check is conservative.** It rejects safe programs, such as problem case 3, a struct that holds a reference into itself, or a graph with cycles. The usual workarounds are indices into a vector, reference counting with `Rc` and run-time borrow checks with `RefCell`, which move the check to run time.
- **Signatures cut the analysis.** A function body is checked against the lifetimes in its signature, not against its callers. A signature that ties two lifetimes together (`fn f<'a>(x: &'a mut T, y: &'a U) -> &'a V`) forces callers to keep both borrows for as long as the result lives, even if the body only uses one.
- **Unsafe code is trusted.** The checker does not look inside raw pointer operations. A wrong `unsafe` block can break every guarantee, which is why RustBelt proves libraries such as `Vec`, `Rc` and `Mutex` separately.
- **Moves are a different analysis.** "Use of moved value" comes from the maybe-moved dataflow, not from loans. A moved value has no loans and no lifetimes to inspect.

## Exercises

1. Is this accepted? `let mut x = 5; let a = &mut x; *a += 1; let b = &x; println!("{} {}", b, x);` *Answer.* Yes. `a` is dead after `*a += 1`, so its mutable loan is not in scope at `let b`. Shared loans allow reads, so reading `x` while `b` is live is fine.
2. In the first classic example, list the points in `'a` for the version that is rejected. *Answer.* The point of the borrow, the point of `v.push(4)` and the point of the `println!`, which now comes last. Since the `push` is in `'a`, the loan is in scope there.
3. Why does a borrow that flows into the result of a function stay in scope in all branches? *Answer.* The result has a universal lifetime from the signature, which contains every point of the body. The outlives constraint makes the loan's lifetime contain it, and rustc's constraints are not tied to the point of the assignment.
4. `let s = String::from("a"); let t = s; println!("{}", s);` fails. Which part of the template rejects it? *Answer.* The maybe-moved dataflow: `s` is moved into `t`, and the later read of `s` is a use of a moved value. No loan is involved.

## References
