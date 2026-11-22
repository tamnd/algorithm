---
tag: NMGG5M
kind: technique
slug: data-oriented-programming
name: Data-oriented programming
aliases:
- DOP attack
area: security-and-privacy/memory-safety-defenses
level: research
summary: Builds Turing-complete attacks by corrupting only data, chaining gadgets along legitimate control flow, which control-flow defenses miss.
history:
  year: 2016
  people: [Hong Hu, Shweta Shinde, Sendroiu Adrian, Zheng Leong Chua, Prateek Saxena, Zhenkai Liang]
  note: Chen et al. (2005) showed that non-control-data attacks are realistic. Hu et al. (IEEE S&P 2016) showed that they can be Turing-complete, so control-flow defenses alone do not stop them.
prereqs: [control-flow-integrity, return-oriented-programming]
see_also: [control-flow-bending, code-pointer-integrity, memory-safety, reaching-definitions, cheri-capability-model, memory-tagging, turing-completeness, principle-of-least-privilege]
sources:
  - paper: "Hong Hu, Shweta Shinde, Sendroiu Adrian, Zheng Leong Chua, Prateek Saxena and Zhenkai Liang, Data-oriented programming, on the expressiveness of non-control data attacks, 2016 IEEE Symposium on Security and Privacy, pages 969-986"
    locator: the abstract and the conclusion (non-control-data attacks can be Turing-complete and work with control-flow defenses in place), and the discussion of defenses
  - paper: "Shuo Chen, Jun Xu, Emre C. Sezer, Prachi Gauriar and Ravishankar K. Iyer, Non-control-data attacks are realistic threats, 14th USENIX Security Symposium, 2005, pages 177-191"
    locator: the thesis and the classes of security-critical data (user identity data, configuration data, user input and decision-making data)
  - paper: "Miguel Castro, Manuel Costa and Tim Harris, Securing software by enforcing data-flow integrity, 7th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2006), pages 147-160"
    locator: the definition of data-flow integrity (reaching definitions computed statically and checked at run time)
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the general attack model, in which data-only attacks are a separate branch from control-flow hijacks
---

Data-oriented programming (DOP) is the class of attacks that use a memory error to change only data, never a code pointer, and still compute what the attacker wants. Every indirect call and every return goes where a correct run could go, so [control-flow integrity](/control-flow-integrity/), a [shadow stack](/shadow-stack/) and [code-pointer integrity](/code-pointer-integrity/) see nothing. The program's own legitimate code does the work: some statements on its normal paths load, store, add or compare values whose addresses come from memory, and if the attacker controls those addresses through the memory error, the statements act on memory of the attacker's choice. Chen, Xu, Sezer, Gauriar and Iyer (USENIX Security 2005) showed that such *non-control-data attacks* are realistic threats against real servers, by changing user identities, configuration values and decision flags. Hu, Shinde, Adrian, Chua, Saxena and Liang (IEEE S&P 2016) showed that they can be Turing-complete: a loop on a normal path, driven by corrupted data, can run such statements again and again in an order the attacker chooses, as the steps of a general program. Their lesson for defenders is the main point of this page: defenses that protect only control flow cannot stop a memory error from being used for general attacks. The defenses that do are those that protect data, from full [memory safety](/memory-safety/) to data-flow integrity. This page describes the class, the conditions, the history and the defenses, with no code, no gadgets and no details of real software.

## In plain words

Most defenses against memory bugs watch where the program jumps. They check that a return goes back to its caller and that a call through a pointer goes to a function that may be called there.

But a program can be made to misbehave without any strange jump. Suppose a server keeps a flag that says whether the user is an administrator, and a bug lets an attacker write that flag. The program then follows its normal path for administrators. No jump went anywhere unusual.

DOP takes this further. Normal code often copies or adds values found through pointers. If the attacker changes the pointers, that normal code copies and adds the attacker's values. With a loop that runs again for each new request, these small steps can be combined into any computation. To stop this, the defense must protect the data, not only the jumps.

## When it applies

The class needs these conditions. Each defense removes one.

- **A memory error that writes data.** An overflow or an arbitrary write lets the attacker change program variables, including pointers to data. [Memory safety](/memory-safety/) removes it.
- **Security-critical data reachable by the error.** Values that decide what the program does: identities, permissions, configuration, lengths, and pointers that statements on normal paths use. Chen et al. grouped them as user identity data, configuration data, user input and decision-making data.
- **Simple operations on normal paths.** Statements that a correct run executes, and that load, store or compute on memory through pointers. With corrupted pointers they act as the steps of the attacker's computation.
- **A way to repeat and choose them.** A loop on a normal path, such as the loop that handles requests or the loop that parses an input, whose iterations the attacker can drive with input or with corrupted data. This is what turns single changes into a general computation.
- **Control-flow defenses only.** If only control flow is protected, nothing checks the data.

## The template

The class has the shape below. Each named hole is a condition from the list, and each comment names the defense that breaks the chain at that line. It is a description of the class, not a procedure.

```pseudo id=main
DATA-ORIENTED-CLASS(program P under control-flow defenses)
L1  need ⟨memory error⟩: the attacker can write data of P, including pointers to data   ▷ broken by memory safety: bounds and temporal checks, capabilities
L2  need ⟨operations⟩: statements on normal paths of P that load, store or compute through such pointers   ▷ data-flow integrity: the read sees a writer it was not allowed
L3  need ⟨repetition⟩: a loop on a normal path whose iterations and choices depend on corrupted data or on input
L4  every transfer of control follows the control flow graph, and every return matches its call   ▷ CFI, shadow stack and CPI: all checks pass
L5  effect: the iterations of L3 run the statements of L2 on memory of the attacker's choice   ▷ data-space randomization: the attacker cannot predict the stored values
L6  effect: the program leaks or changes data it should protect, or prepares a later control-flow attack   ▷ least privilege and isolation limit what P can reach
```

**Walk-through.** Line L1 is the memory error; as on every page of this group, the class needs it, and only defenses of this line end it. Line L2 is the supply of operations. Its statements are correct code; what makes them dangerous is that the pointers they follow were changed. Line L3 gives repetition and choice. Line L4 is the defining property of the class: every control-flow check holds. Line L5 is where defenses that protect data, but less than full memory safety, can act. Line L6 is the effect, which [least privilege](/principle-of-least-privilege/) limits.

**What the template shows about each defense.** CFI, a shadow stack and CPI have their comments at line L4 only, and that line is satisfied by the attack. So the guarantees of those defenses, which are about control transfers, are all true during the attack. The defenses that break the chain are at lines L1, L2 and L5: memory safety, data-flow integrity and data-space randomization.

**Data-flow integrity at line L2.** Castro, Costa and Harris (OSDI 2006) proposed a check that matches this line. A static analysis computes, for each read in the program, the set of statements that may have written the value it reads, the [reaching definitions](/reaching-definitions/) of that read. At run time, each write records its statement in a table, and each read checks that the last writer of the address is in its allowed set. A memory error that writes a value where the program did not mean to is a write by a statement that is not an allowed definition for later reads, so the next read of that value faults. The cost is a table update at each write and a check at each read.

## Classic examples

- **Non-control-data attacks are realistic (2005).** Chen et al. changed only data in real server programs, such as a stored user identity or a configuration value, and obtained the same control as a code-pointer attack. Their paper is the start of the class.
- **Data-flow integrity (2006).** Castro et al. answered with a check of reaching definitions at run time, the defense at line L2.
- **Control-flow defenses become standard.** After [control-flow integrity](/control-flow-integrity/), [shadow stacks](/shadow-stack/) and [code-pointer integrity](/code-pointer-integrity/), the remaining question was how much an attacker can do with data alone. [Control-flow bending](/control-flow-bending/) (2015) used data together with the freedom inside the control flow graph.
- **Turing-complete data-only attacks (2016).** Hu et al. showed that data-only attacks can simulate general computation, and demonstrated attacks on real programs with control-flow defenses in place. The lesson: a program with a memory error and a suitable loop is as exposed under CFI as without it, for an attacker whose goal is in data.

## Variations

- **Single changes.** The simplest form changes one decision variable, such as a permission flag or a length. It needs no loop and no general computation.
- **Information leaks.** The attacker changes a pointer or a length that an output statement uses, and the program sends data it should keep, such as a key or a randomized address. A leak of a randomized address can then defeat [ASLR](/address-space-layout-randomization/) for a later attack.
- **Preparing a control-flow attack.** Data-only steps can change permissions data or memory maps so that a later attack becomes possible. Defenses at line L4 then meet a weakened system.
- **Block-oriented forms.** Later work built such attacks from whole basic blocks of normal code, chosen with an analysis, rather than from single statements. The lesson stays the same.

## Pitfalls

These are mistakes defenders make about the class.

- **Calling control-flow defenses complete.** CFI, shadow stacks and CPI make control-flow hijacking hard. They do not make memory errors harmless. Fix the bug, or use a defense of line L1.
- **Assuming the attack needs a code pointer.** Many critical values are data: identities, permissions, lengths, keys. Protect them with memory safety, or keep them in memory that a bug in parsing code cannot reach, for example in a separate process.
- **Large privileged processes.** A process that parses untrusted input and also holds keys or permissions puts the data of line L6 next to the bug of line L1. Split it, and give each part [least privilege](/principle-of-least-privilege/).
- **Partial bounds checks.** Checking only some objects, for example only arrays on the stack, leaves heap objects and pointers in structures open to line L1. Hardware capabilities ([CHERI](/cheri-capability-model/)) and [memory tagging](/memory-tagging/) cover all accesses, with different strength.

## Exercises

1. For each line L1 to L6 of the template, say whether a [shadow stack](/shadow-stack/) can detect the attack at that line. Use the theorem on the shadow stack page to justify the answer for line L4.
2. Explain, with the definition of [reaching definitions](/reaching-definitions/), why a memory error that writes a variable through an out-of-bounds pointer is detected by data-flow integrity at the next read of that variable, if the out-of-bounds write is not an allowed definition of it.
3. A server checks a permission flag at the start of each request and then handles the request. Describe an abstract model, with made-up variables, in which a single data change grants permission while every control transfer stays in the control flow graph. Which defenses of the template stop it?
4. Explain why the lesson of Hu et al. is about expressiveness: what is the difference between showing that one data-only attack exists and showing that data-only attacks are Turing-complete, for a defender who wants to know whether control-flow defenses are enough?

## References
