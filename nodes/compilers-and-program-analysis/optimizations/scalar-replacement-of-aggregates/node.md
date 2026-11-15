---
tag: 61XATE
kind: technique
slug: scalar-replacement-of-aggregates
name: Scalar replacement of aggregates
aliases:
- SROA
- scalar replacement
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Splits a local record or array that does not escape into separate scalar variables, which can then live in registers.
prereqs: [static-single-assignment-form, alias-analysis]
see_also: [escape-analysis, function-inlining, cytron-ssa-construction, register-allocation-problem, constant-folding, dead-code-elimination, loop-unrolling, field-sensitivity]
sources:
  - book: isbn:9781558603202
    title: "Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997"
    locator: Section 12.2 (Scalar Replacement of Aggregates)
  - url: "https://llvm.org/docs/Passes.html"
    title: LLVM Project, LLVM's Analysis and Transform Passes, LLVM documentation
    locator: the entry for -sroa (break up stack allocations of aggregate type into one allocation per member, then promote them to SSA registers)
---

Scalar replacement of aggregates (SROA) takes a local record or array and turns each of its fields into a separate scalar variable. A program often keeps a small record in memory only because the language says it is one object: a complex number, a pair returned by a function, a small fixed array. If the compiler can prove that no one outside the procedure can see the object, and that every access names a fixed field, the object does not need to exist in memory at all. Each field becomes a variable of its own, and later passes put it in a register, fold it, or delete it.

## In plain words

A record groups a few values under one name, like the real and imaginary parts of a complex number. In memory, the parts sit side by side, and each read or write goes to memory.

If the record is local to one function, and its address is never handed to anyone else, then nobody can tell whether the parts are really side by side. The compiler can then treat each part as its own variable. A read of the real part becomes a read of the variable for the real part, and so on.

Plain variables are much easier for a compiler than memory. They can stay in registers, constants can flow through them, and a part that is never read can be removed. Many records disappear completely after this step.

## When it applies

Fix a local aggregate $A$: a record, or an array of fixed size, created by a stack allocation in procedure $P$. Its *fields* are the record fields, or the array elements. For nested records, take the leaf fields.

SROA may replace $A$ when these conditions hold.

- **(S1) No escape.** The address of $A$, or of any part of it, is used only by the accesses below. It is not stored to memory, not returned, not passed to a call, and not converted to an integer. [Escape analysis](/escape-analysis/) checks this. A call that is known to read the object and not keep the pointer can be allowed if the call is rewritten too, for example a copy of the whole object.
- **(S2) Fixed fields.** Each access names one field at a compile-time constant offset: `A.re`, or `A[2]` with a constant index. An array access with an index that is only known at run time does not say which scalar to use.
- **(S3) Matching shapes.** Each access reads or writes exactly one whole field, with the type of that field. An access that covers two fields, part of a field, or the bytes of a field under another type, as with a union, breaks the one-to-one match between fields and variables.
- **(S4) Plain accesses.** No access is `volatile` or atomic. Such accesses must stay real memory operations.

Whole-object copies `B = A` between two candidates are fine. They become one copy per field.

## The template

1. **Find the candidates.** Collect the local allocations of record or array type. Inlining usually runs first, because a call that takes the address of a local object breaks (S1), and inlining removes the call.
2. **Check every use.** Walk the uses of the address of $A$. Each one must be a field access as in (S2) to (S4), or an address computation that leads only to such accesses. If any use fails, keep $A$ in memory, or keep only the fields that fail and split off the rest.
3. **Make the scalars.** Create one new variable $a_f$ for each field $f$ that is used. Rewrite a load of `A.f` into a read of $a_f$, a store into `A.f` into an assignment to $a_f$, and a whole-object copy into one copy per field. Delete the allocation.
4. **Promote the scalars.** The new variables are plain local variables, so [SSA construction](/cytron-ssa-construction/) turns them into SSA values. Then [constant folding](/constant-folding/), copy propagation and [dead code elimination](/dead-code-elimination/) clean up. A field that is written and never read disappears.

**Why the behavior stays the same.** Run the old and new programs side by side, and keep this invariant: at each matched point, for each field $f$ of $A$, the memory cell of $A.f$ in the old program holds the same value as $a_f$ in the new one, or neither has been written. All other variables and all other memory agree. The invariant holds when $A$ is allocated, since nothing has been written. An access to `A.f` reads or writes the cell of $A.f$ in the old program and $a_f$ in the new one, so the invariant is kept. By (S3) no access touches part of a cell, or two cells, so no other access can change the cell of $A.f$. By (S1) no instruction outside these accesses holds a pointer into $A$, so a store through another pointer or a call cannot write the cell, and no load or call can read it. So every other instruction behaves the same in both programs. A read of a field that was never written gives an undefined value in both, which a careful compiler keeps undefined and does not turn into a guess.

**Profit.** A load or store becomes a register move, which often vanishes. Values flow through fields into later optimizations. Unused fields cost nothing. The cost is register pressure: an object with many live fields becomes many live values, and the register allocator may spill them back to the stack, now one at a time.

## Classic examples

**A complex product.**

```
struct C { double re, im; };

double f(double x, double y) {
  struct C c;
  c.re = x * x - y * y;
  c.im = 2 * x * y;
  return c.re + c.im;
}
```

The address of `c` is used only by four field accesses, each with a constant field. SROA gives two variables `c_re` and `c_im`. After SSA construction and copy propagation, the function computes `x * x - y * y + 2 * x * y` with no memory access.

**A struct returned by value, after inlining.** A function `struct C make(double a, double b)` that fills and returns a record is inlined into a caller that reads only `.re` of the result. The inlined body leaves a temporary record in the caller. SROA splits it, and dead code elimination removes the computation of `.im`.

**A small array after unrolling.**

```
int t[3];
for (int i = 0; i < 3; i++) t[i] = a[i] * k;
return t[0] + t[1] + t[2];
```

With the loop as written, `t[i]` has a variable index and (S2) fails. After full [loop unrolling](/loop-unrolling/) every index is a constant, and `t` becomes three scalars `t0`, `t1` and `t2`.

**An escape that blocks the split.**

```
struct C c;
init(&c);
return c.re;
```

If `init` is not inlined and its code is unknown, it may keep the pointer, or read and write any part of `c`. (S1) fails, and `c` stays in memory.

## Variations

- **Partial splitting.** Split only the fields that meet the conditions, and keep a smaller object in memory for the rest. LLVM's `sroa` pass works on byte ranges of a stack allocation in a similar way: it groups the accesses into slices and makes one new allocation for each slice that it can, then promotes them to SSA registers.
- **Heap objects in managed languages.** Java and other managed runtimes allocate most objects on the heap. A JIT compiler uses [escape analysis](/escape-analysis/) to find allocations that do not escape the compiled code, and replaces their fields by scalars, so the allocation also goes away. Some compilers do this on the paths where the object has not escaped yet, and build the object only on the paths where it escapes.
- **Field-sensitive analysis instead of a rewrite.** A [field-sensitive](/field-sensitivity/) pointer analysis can give some of the same precision without changing the program, but the values still live in memory.
- **Scalar replacement of array references in loops.** In loop optimization, "scalar replacement" also names a different transformation: keep an array element that is reused across loop iterations in a scalar, so it is loaded once instead of in every iteration. That transformation needs dependence analysis, not escape analysis.

## Pitfalls

- **Escape through a call.** Passing `&c` to a function that is not inlined usually blocks the split. Run inlining first, or use summaries that say the callee does not keep the pointer.
- **Variable indices.** An access `t[i]` with an unknown `i` stops the whole array from splitting. Splitting with a run-time test on `i` for each element is possible but rarely pays.
- **Overlapping and type-punned accesses.** Unions, byte copies, and reads of a field under another type do not map to one scalar. A compiler that splits anyway must insert the right bit operations, or it changes the program.
- **Large aggregates.** Splitting an array of a thousand elements makes a thousand variables. Compilers set a limit on the number of fields.
- **volatile and atomics.** These accesses must stay in memory, so an object with such a field cannot be fully split.
- **Uninitialized fields.** A field that is read before any write is undefined in the old program. The new scalar must also be undefined, not zero and not a value from another field.

## Exercises

1. In the complex product example, why may `c.re` and `c.im` not share one scalar? *Answer.* They hold different values at the same time: both are live at the `return`. One variable per field is needed for the one-to-one match in the invariant.
2. A function stores `&c` into a global variable and never reads the global again. May SROA split `c`? *Answer.* No. Another function or thread can read the global and access `c` through it, so (S1) fails. Proving that nobody reads the global is a whole-program question that the local check does not answer.
3. A record `p` has fields `x` and `y`. The code does `q = p; q.x = 1; return p.x + q.y;` with `q` another local record. What does SROA give? *Answer.* Four scalars. The copy becomes `q_x = p_x; q_y = p_y`, then `q_x = 1`, and the return reads `p_x + q_y`. Copy propagation turns it into `p_x + p_y`, and `q_x` is dead.
4. Why does SROA usually run both before and after inlining? *Answer.* Before inlining, it makes the callee bodies smaller, which helps the inlining cost model. After inlining, calls that took the address of a local object are gone, so new objects meet (S1).
5. An array `t[4]` is read only with constant indices but written with `t[i] = 0` in a loop with an unknown bound. Which elements can become scalars? *Answer.* None, under (S2). The write with an unknown index may hit any element, so every element must stay in memory unless the loop is unrolled or its bound is known.

## References
