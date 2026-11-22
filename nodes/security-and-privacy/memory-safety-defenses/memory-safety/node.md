---
tag: KX9V19
kind: definition
slug: memory-safety
name: Memory safety
aliases:
- spatial and temporal memory safety
area: security-and-privacy/memory-safety-defenses
level: intro
summary: A program is memory safe if every access goes to a live object through a pointer derived from it and stays within its bounds.
prereqs: []
see_also: [buffer-overflow, fat-pointer, softbound, lock-and-key-temporal-checking, addresssanitizer, borrow-checking, type-soundness, safety-property]
sources:
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK: Eternal war in memory, IEEE Symposium on Security and Privacy 2013, pages 48-62"
    locator: "the general model of memory corruption, which starts from a spatial or a temporal memory error"
  - paper: "Arthur Azevedo de Amorim, Catalin Hritcu and Benjamin C. Pierce, The meaning of memory safety, POST 2018"
    url: https://arxiv.org/abs/1705.07354
    locator: "the definition of memory safety by the properties of a language, including that a program cannot reach memory it has no pointer to"
  - paper: "Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin and Steve Zdancewic, SoftBound: highly compatible and complete spatial memory safety for C, PLDI 2009, pages 245-258"
    locator: "the split of memory safety into spatial safety and temporal safety, and pointer-based checking of the spatial part"
---

Memory safety is a property of a program run: every read and every write goes to an object that is still allocated, through a pointer that was derived from that object, and stays inside that object's bounds. A language is memory safe if every run of every program it accepts has this property, or stops with an error before the first access that would break it. The property splits into two parts: *spatial* safety, which is about bounds, and *temporal* safety, which is about lifetime. Most defenses in this area enforce one part or both for languages such as C and C++, which do not guarantee either.

## Definition

Model a run as a sequence of events on a memory of addresses. An *object* $o$ is created by an allocation, which gives it a base address $\mathit{base}(o)$ and a size $\mathit{size}(o)$, and it is *live* from its allocation until it is freed. Objects that are live at the same time do not overlap.

Each pointer value $p$ has an address $\mathit{addr}(p)$ and a *provenance* $\mathit{prov}(p)$, which is an object or the value $\bot$ (no object). Provenance follows the data flow of the program:

- the pointer that an allocation of $o$ returns has provenance $o$;
- pointer arithmetic $p + i$ and the selection of a field of $p$ keep the provenance of $p$;
- a pointer stored in memory and loaded back keeps the provenance it had when it was stored;
- a pointer made from an integer, and the null pointer, have provenance $\bot$.

An access of $w$ bytes through $p$ at time $t$ is **spatially safe** if $\mathit{prov}(p) = o \ne \bot$ and

$$\mathit{base}(o) \le \mathit{addr}(p) \quad\text{and}\quad \mathit{addr}(p) + w \le \mathit{base}(o) + \mathit{size}(o).$$

It is **temporally safe** if $\mathit{prov}(p) = o \ne \bot$ and $o$ is live at time $t$. A free of $p$ is safe if $\mathit{prov}(p) = o$ is live and $\mathit{addr}(p) = \mathit{base}(o)$.

A run is **memory safe** if every access and every free in it is spatially and temporally safe. A program is memory safe if all its runs are. A run that stops with an error at the first access or free that is not safe also counts as memory safe: this is how checked languages and the run-time defenses in this area give the property.

Since an unsafe event is seen in a finite prefix of the run, memory safety is a [safety property](/safety-property/) of runs.

## Examples and non-examples

- **A loop over an array.** For an array of $n$ elements, the loop `for i in 0 .. n-1: a[i] = 0` is memory safe: every pointer $a + i$ has the provenance of the array and is in bounds.
- **One past the end.** C allows a program to compute $a + n$ and compare it with other pointers. Computing it is safe; only an access through it is a spatial error. So a definition that checks accesses, not pointer arithmetic, matches C.
- **An off-by-one write.** Writing `a[n]` is not spatially safe. It is the simplest [buffer overflow](/buffer-overflow/).
- **An access that lands in another object.** If $p$ points into object $o$ and $p + i$ happens to point into a live object $o'$ next to it, an access through $p + i$ is not safe, though the address is valid. Defenses that only test whether an address is in some live object, such as [AddressSanitizer](/addresssanitizer/), do not see this case; defenses that check the bounds of the pointer's own object, such as [SoftBound](/softbound/) or [fat pointers](/fat-pointer/), do.
- **Use after free.** An access through a pointer to an object after the object is freed is not temporally safe, even if a new object now lives at the same address.
- **Double free.** Freeing the same object twice is not safe, because at the second free the object is no longer live.
- **A pointer from an integer.** A pointer made from an integer has provenance $\bot$, so an access through it is not safe under this definition, even if the address is inside a live object. Real definitions for C differ here, and some allow such a pointer to take the provenance of the object at that address.
- **A null dereference.** An access through the null pointer is not safe. On most systems the hardware traps it at once, so a run that would do it stops with an error, which counts as safe in the checked sense.
- **A memory leak.** A program that never frees an object is memory safe. Leaks waste memory, but they do not let an access reach the wrong object.
- **A read of uninitialized memory.** It is not covered by the definition above. Some authors add a third part for it, because the read can reveal old data.

## Related definitions

- **Spatial and temporal safety.** The two parts above. Spatial checks use bounds per pointer or per object, as in [fat pointers](/fat-pointer/), [Jones and Kelly bounds checking](/jones-kelly-bounds-checking/), [baggy bounds checking](/baggy-bounds-checking/) and [SoftBound](/softbound/). Temporal checks use a key per object, as in [lock and key checking](/lock-and-key-temporal-checking/), or clear the pointers to freed objects, as in [dangling pointer nullification](/dangling-pointer-nullification/).
- **Type safety.** A language is type safe if well-typed programs do not go wrong, which is shown by a proof of [type soundness](/type-soundness/). For most languages type safety implies memory safety, since a pointer to a freed object or past the end of an array has no meaningful type.
- **Safety through ownership.** [Borrow checking](/borrow-checking/) and [region-based memory management](/region-based-memory-management/) prove temporal safety at compile time, so no check is needed at run time. Garbage collection, as with [mark and sweep](/mark-and-sweep/), gives temporal safety by never freeing an object that a pointer can still reach.
- **Memory safety as a reasoning principle.** Azevedo de Amorim, Hritcu and Pierce define memory safety by what it lets a programmer conclude: a piece of code cannot read or change memory it has no pointer to. This is close to the frame rule of [separation logic](/separation-logic/).
- **Capability safety.** In the [CHERI capability model](/cheri-capability-model/), every pointer is a capability with bounds and permissions that the hardware checks, which gives spatial safety and is the base for temporal safety.

## References
