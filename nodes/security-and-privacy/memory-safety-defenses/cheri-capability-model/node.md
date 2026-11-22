---
tag: JYAXZ3
kind: model
slug: cheri-capability-model
name: CHERI capability model
aliases:
- CHERI
- hardware capabilities
area: security-and-privacy/memory-safety-defenses
level: research
summary: A processor model in which pointers are unforgeable capabilities with bounds and permissions, checked by hardware on every access.
prereqs: [fat-pointer]
see_also: [fat-pointer, memory-tagging, softbound, capability-list, access-control-matrix, reference-monitor, software-fault-isolation, memory-safety]
sources:
  - paper: "Jonathan Woodruff, Robert N. M. Watson, David Chisnall, Simon W. Moore, Jonathan Anderson, Brooks Davis, Ben Laurie, Peter G. Neumann, Robert Norton and Michael Roe, The CHERI capability model: revisiting RISC in an age of risk, ISCA 2014, pages 457-468"
    locator: "the capability registers, the tag bit for each capability-sized word of memory, the rule that capabilities can only shrink, and the checks on loads and stores"
  - paper: "Robert N. M. Watson, Jonathan Woodruff, Peter G. Neumann, Simon W. Moore, Jonathan Anderson, David Chisnall, Nirav Dave, Brooks Davis, Khilan Gudka, Ben Laurie, Steven J. Murdoch, Robert Norton, Michael Roe, Stacey Son and Munraj Vadera, CHERI: a hybrid capability-system architecture for scalable software compartmentalization, IEEE Symposium on Security and Privacy 2015, pages 20-37"
    url: https://doi.org/10.1109/SP.2015.9
    locator: "the sealed capabilities, the protected calls between compartments, and the hybrid use of capabilities next to ordinary pointers"
---

The CHERI capability model is a model of a processor in which a pointer is a *capability*: an address together with the bounds of the memory it may reach and the operations it allows. The hardware checks every load, store and jump against the capability that it goes through, and a program cannot make a capability out of an integer or grow an existing one. It can only derive smaller ones. A tag bit kept by the hardware, outside the memory the program can address, marks which words of memory hold valid capabilities. The model gives the spatial checks of [fat pointers](/fat-pointer/) in hardware, and since capabilities cannot be forged, it can also confine a piece of code to the memory it was given.

## The machine

The machine is an ordinary load and store processor with a second kind of register and of value.

- **Capabilities.** A capability $c$ holds an address $\mathit{addr}(c)$, a base $\mathit{base}(c)$, a top $\mathit{top}(c)$, a set of permissions $\mathit{perms}(c)$ (such as load, store, execute, load capability, store capability), an object type for sealing, and a validity tag $\mathit{tag}(c)$. In the 2014 design a capability took 256 bits; later designs compress the bounds so that a capability for a 64-bit address takes 128 bits.
- **Tagged memory.** Each aligned word of memory of capability size has one tag bit. The program cannot read or set it directly. A store of a valid capability to an aligned word sets the tag; any other store to the word clears it. A load of a capability from memory copies the tag into the register.
- **Checked access.** A load or store of $w$ bytes through $c$ succeeds only if $\mathit{tag}(c)$ is set, $c$ is not sealed, the permission for the operation is in $\mathit{perms}(c)$, and
  $$\mathit{base}(c) \le \mathit{addr}(c) \quad\text{and}\quad \mathit{addr}(c) + w \le \mathit{top}(c).$$
  Otherwise the processor traps. Jumps check the execute permission the same way.
- **Monotonic derivation.** Instructions can change the address of a capability freely, but they can only make the bounds smaller and only remove permissions. An instruction that would grow the bounds or add a permission traps, or clears the tag of its result. An integer becomes a capability only by setting the address of an existing capability, so the result is bounded by that capability.
- **Sealing.** A capability with the right permission can *seal* another capability with an object type. A sealed capability cannot be used for access or changed, only passed around, and only code with a matching capability can unseal it. This is the basis for protected calls between parts of a program.
- **Hybrid code.** Ordinary integer pointers can still be used, checked against a default capability, so old code runs next to code that uses capabilities everywhere.

At reset, the processor holds capabilities that cover all of memory. The operating system derives smaller ones from them for each process, and the allocator and the compiler derive one for each object.

## What it counts

The model does not change the cost of computation much: an access costs one check, done in parallel with the access, and derivation instructions take a constant number of steps, as in the [word RAM](/word-ram/). What it adds is a measure of *authority*: the memory that code can reach is bounded by the union of the bounds of the capabilities it holds in registers, plus those it can load, transitively, through capabilities that allow loading capabilities. Monotonic derivation means that this set can only shrink as code runs, unless another domain passes it new capabilities. Questions in the model are about this set: whether a given compartment can reach some memory, and whether a C program can run when every pointer is a capability with exact bounds.

The costs it does count are space and compatibility: capabilities are twice the size of addresses, objects must be aligned and padded so that compressed bounds are exact, and code that hides pointers in integers or computes them from integers must be changed.

## Relation to other models

- **Fat pointers.** A capability is a [fat pointer](/fat-pointer/) whose bounds the hardware checks and whose integrity the tag protects. Software fat pointers and [SoftBound](/softbound/) give spatial safety, but code that writes over the metadata can defeat them; in CHERI the metadata cannot be forged.
- **Capability systems.** The model follows the classic capability systems, in which a [capability list](/capability-list/) of unforgeable tokens is a row of the [access control matrix](/access-control-matrix/). CHERI applies the idea to every pointer of a C program, not only to operating system objects.
- **Reference monitor.** The processor acts as a [reference monitor](/reference-monitor/) for every memory access: it cannot be bypassed, and the check is the same for all code.
- **Memory tagging.** [Memory tagging](/memory-tagging/) also adds bits to memory and to pointers, but its tags are small and can repeat, so its checks are probabilistic. CHERI's tag says only "this is a valid capability", and the bounds give an exact check.
- **Software fault isolation.** [Software fault isolation](/software-fault-isolation/) confines code to a region by rewriting it; CHERI gets the same effect by giving the code only capabilities for that region, and can do so at the level of single objects.

## Known results in the model

- **Spatial safety for C.** If the compiler and the allocator derive a capability with exact bounds for every object, every access out of the bounds of the object that the pointer came from traps. This covers the case that address-based tools miss, an access that lands in another live object.
- **Unforgeability.** Because of the tag rules, no sequence of instructions can produce a valid capability with more bounds or permissions than the ones it was derived from. Later work stated and proved this property in a formal model of the instruction set.
- **Compartments.** With sealing and protected calls, a program can be split into compartments that cannot reach each other's memory, with calls between them that are cheaper than switches between processes. The 2015 paper describes this design and evaluates it on compartmentalized versions of real programs.
- **Running real software.** Large C and C++ code bases, including an operating system, have been ported to use capabilities for all pointers, with a small fraction of lines changed, mostly where code treats pointers as integers.
- **Temporal safety.** Capabilities alone do not stop a use after free, because a freed object's capability keeps its bounds. Since the tags show exactly where capabilities are in memory, a revoker can sweep memory and clear every capability to freed objects before the memory is reused, much as a [mark-and-sweep](/mark-and-sweep/) collector finds pointers without guessing.

## References
