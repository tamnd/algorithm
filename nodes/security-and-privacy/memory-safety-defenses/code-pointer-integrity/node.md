---
tag: 65ZWQ8
kind: technique
slug: code-pointer-integrity
name: Code-pointer integrity
aliases:
- CPI
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Keeps code pointers and the pointers that lead to them in an isolated safe region with full memory safety, at low cost.
history:
  year: 2014
  people: [Volodymyr Kuznetsov, Laszlo Szekeres, Mathias Payer, George Candea, R. Sekar, Dawn Song]
  note: Kuznetsov et al. (OSDI 2014) introduced code-pointer integrity, the weaker code-pointer separation and the safe stack. Evans et al. (2015) showed that hiding the safe region by randomization is not enough.
prereqs: [control-flow-integrity, memory-safety]
see_also: [softbound, shadow-stack, control-flow-bending, data-oriented-programming, fat-pointer, address-space-layout-randomization, software-fault-isolation, stack-smashing]
sources:
  - paper: "Volodymyr Kuznetsov, Laszlo Szekeres, Mathias Payer, George Candea, R. Sekar and Dawn Song, Code-pointer integrity, 11th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2014), pages 147-163"
    locator: the definitions of sensitive pointers, the safe region and the safe stack, the guarantees of CPI and CPS, and the evaluation on SPEC CPU2006, RIPE and FreeBSD
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the attack model in which a control-flow hijack needs a corrupted code pointer, and the policies that protect code pointers
  - paper: doi:10.1145/3054924
    title: Nathan Burow, Scott A. Carr, Joseph Nash, Per Larsen, Michael Franz, Stefan Brunthaler and Mathias Payer, Control-flow integrity, precision, security, and performance, ACM Computing Surveys 50(1), article 16, 2017, pages 1-33
    locator: the comparison of CFI with defenses that protect code pointers instead of checking targets
  - paper: doi:10.1109/SP.2015.53
    title: Isaac Evans, Sam Fingeret, Julian Gonzalez, Ulziibayar Otgonbaatar, Tiffany Tang, Howard Shrobe, Stelios Sidiroglou-Douskos, Martin Rinard and Hamed Okhravi, Missing the point(er), on the effectiveness of code pointer integrity, 2015 IEEE Symposium on Security and Privacy, pages 781-796
    locator: the abstract and the conclusion (a safe region that is only hidden, not isolated, can be located, so isolation must not rest on secrecy)
---

Code-pointer integrity (CPI) prevents control-flow hijacking by making sure that code pointers always hold the values the program stored in them. It does not check targets against a graph, as [control-flow integrity](/control-flow-integrity/) does. Instead it finds, by a static analysis on types, every *sensitive pointer*: every code pointer, and every pointer that may be used to reach a sensitive pointer, recursively. These pointers, with bounds metadata, are kept in a *safe region* of memory, and every access through them is checked for memory safety as in [SoftBound](/softbound/). Regular memory accesses cannot reach the safe region. A memory error in the regular region can then change any ordinary data, but not a code pointer, so an indirect call or return always goes where the program meant it to go. Kuznetsov, Szekeres, Payer, Candea, Sekar and Song (OSDI 2014) introduced CPI with two lighter forms: *code-pointer separation* (CPS), which protects code pointers but not the pointers that lead to them, and the *safe stack*, which moves return addresses and locals proven safe to a separate stack. On SPEC CPU2006 they measured average overheads of 2.9 percent for CPI on C programs and 8.4 percent on C and C++, and 1.2 and 1.9 percent for CPS. The strength of the guarantee rests on the isolation of the safe region: where it was only hidden at a random address, Evans et al. (2015) showed that it could be found.

## In plain words

An attacker who takes over a program by a memory error almost always changes a pointer to code: a return address or a function pointer. Full memory safety would stop every such change, but checking every access in a C program is slow.

CPI checks only the accesses that matter for control. It moves every pointer to code into a separate area of memory, and also every pointer that could be used to reach such a pointer. Only these pointers are checked. The rest of the program runs at full speed and can still have bugs.

A bug in the normal area can now change data but cannot reach the protected area. So the pointers that decide where the program jumps keep their correct values. The protection is as good as the wall around the protected area.

## When it applies

- **The threat is control-flow hijacking by memory errors** in C or C++ code: an attacker can read and write the program's regular memory through a bug.
- **Source code and a compiler pass.** The analysis works on types in the compiler's intermediate form, so the program must be rebuilt.
- **A way to isolate the safe region.** Hardware segmentation, a separate address space, memory protection keys, or [software fault isolation](/software-fault-isolation/) of regular accesses. Hiding the region at a random address is a weak form; see the pitfalls.
- **Control flow is what must be protected.** CPI protects code pointers only. If the threat includes data-only attacks, it must be combined with other defenses; see [data-oriented programming](/data-oriented-programming/).

## The template

The defense has a compile-time part that splits memory and a run-time part that checks sensitive accesses. The named holes are the choices that separate CPI, CPS and the safe stack.

```pseudo id=main
COMPILE(program P)
L1  Sens ← the types of code pointers, closed under ⟨sensitivity rule⟩          ▷ CPI: add pointer types that may point to Sens, recursively; CPS: code pointers only
L2  for each memory access through a value of a type in Sens do
L3      store and load the value in the safe region, with ⟨metadata⟩             ▷ CPI: bounds and temporal metadata, as in SoftBound
L4  for each other memory access do leave it in the regular region, unchecked
L5  put return addresses and locals that ⟨stack analysis⟩ proves safe on the safe stack; put other locals on a regular stack

RUN-TIME
L6  on each dereference of a sensitive pointer p: check p against its metadata, else fault
L7  ⟨isolation⟩: no instruction in the regular region can address the safe region or the safe stack
L8  an indirect call, jump or return uses a value read from the safe region or the safe stack
```

**Walk-through.** Line L1 decides what is protected. CPI includes every pointer type that may lead to a code pointer, for example a pointer to a structure that holds a function pointer, so that an attacker cannot redirect such a pointer to a fake structure. CPS stops at code pointers themselves, which is cheaper but lets an attacker swap one valid code pointer for another stored elsewhere. Lines L2 to L4 split the accesses: only sensitive ones are instrumented. Line L5 is the safe stack: a return address is always safe, and so are locals whose address never escapes and whose accesses are proven in bounds, so all of them go to a stack that regular accesses cannot reach. Line L6 gives the sensitive pointers full spatial and temporal safety, so a sensitive pointer cannot be moved out of its object even by legal code. Line L7 is the isolation on which the rest depends. Line L8 is the result: every indirect transfer uses a protected value.

**The guarantee, as a statement in a model.** Assume that line L7 holds, that the analysis of line L1 is sound for the program's use of types, and that the checks of line L6 enforce memory safety for sensitive pointers. Then a memory error in the regular region cannot change any value in the safe region, and a sensitive pointer can only be loaded from the safe region with a value that the program stored there through a checked access. So every indirect transfer goes to a code address that the program itself stored as that pointer's value. Control-flow hijacking through corrupted code pointers is impossible. For CPS the statement is weaker: every code pointer holds some value that the program stored as a code pointer, but not necessarily at that place. For the safe stack alone, return addresses are exact, as with a [shadow stack](/shadow-stack/), and forward edges are not protected.

**Cost.** Each sensitive access costs $O(1)$ extra operations in the [word RAM](/word-ram/) model for the lookup of the safe region and the metadata check, and the safe region uses memory in proportion to the number of sensitive pointers. Measured overheads are in the lead; the paper also reports that CPI stopped every attack of the RIPE benchmark suite and that a full FreeBSD system with more than 100 packages was built with the protection.

## Classic examples

- **Return addresses on the safe stack.** A [stack smashing](/stack-smashing/) overflow of a local array writes the regular stack, where the array lives. The return address is on the safe stack, out of reach, so line L8 returns to the right place. This is the cheapest part of CPI and is the part most widely adopted.
- **Function pointers in heap objects.** A heap overflow changes a function pointer inside an object. Under CPI, the function pointer is stored in the safe region; the overflow changes the regular copy of the object, which is not used for the call.
- **The difference from CFI.** Under [control-flow integrity](/control-flow-integrity/), a corrupted pointer may still go to any allowed target, which [control-flow bending](/control-flow-bending/) exploits. Under CPI, the pointer holds the exact value the program stored, so the choice among allowed targets is not available to the attacker.
- **The difference from full memory safety.** Full checks on every access, as with [SoftBound](/softbound/) and its temporal extension, cost much more. CPI applies the same checks to a small part of the program, chosen so that control flow is safe.
- **Finding a hidden safe region (2015).** On x86-64 the first implementation hid the safe region at a random address in a large address space instead of isolating it by hardware. Evans et al. showed that an attacker with a memory read could locate it through a timing side channel, so isolation must not rest on secrecy alone. Later designs isolate it by hardware or by instrumentation of regular accesses.

## Variations

- **CPS.** Protect code pointers only. It stops all direct corruption of code pointers but not the substitution of one stored code pointer for another through a corrupted data pointer.
- **Safe stack only.** Protect return addresses and safe locals. It costs almost nothing and gives the return guarantee of a [shadow stack](/shadow-stack/), without any protection of forward edges.
- **Isolation mechanisms.** Hardware segment limits on 32-bit x86, memory protection keys on newer processors, a separate process, or the address masking of [software fault isolation](/software-fault-isolation/) on regular accesses. The choice sets the cost and the threat model.
- **Pointer authentication.** Some processors can add a cryptographic tag to a code pointer and check it before use. This protects code pointers in place, with a different threat model: the attacker must not be able to forge or reuse tags.

## Pitfalls

- **Isolation by randomization.** A region that is only hidden can be found with a memory read and a side channel. Treat hiding as a layer, not as isolation, as with [ASLR](/address-space-layout-randomization/).
- **Unsound type information.** C code that casts between unrelated types, or stores pointers in integers, can hide a code pointer from the analysis of line L1. Such a pointer stays in the regular region, unprotected.
- **Data-only attacks.** CPI says nothing about regular data. An attacker can change decision variables or the arguments of a legitimate call; see [data-oriented programming](/data-oriented-programming/).
- **Code without the instrumentation.** Libraries built without CPI store code pointers in the regular region, where a memory error can change them.

## Exercises

1. A structure type holds an integer and a function pointer. Another type holds a pointer to that structure. Under the sensitivity rule of CPI, which of the three types (the function pointer type, the structure pointer type, the pointer to it) are sensitive? Which are sensitive under CPS?
2. Give an abstract scenario, with made-up names, in which CPS lets an attacker make an indirect call go to a function other than the one the program stored at that place, while every code pointer still holds a value the program once stored. Explain why CPI prevents it.
3. Explain why a local array whose address is passed to another function cannot be put on the safe stack by the stack analysis of line L5.
4. Compare the guarantee of the safe stack with the theorem on the [shadow stack](/shadow-stack/) page. Which assumptions of that theorem correspond to line L7?

## References
