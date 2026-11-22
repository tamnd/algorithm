---
tag: G3007J
kind: technique
slug: return-oriented-programming
name: Return-oriented programming
aliases:
- ROP
area: security-and-privacy/memory-safety-defenses
level: core
summary: Builds arbitrary computation by chaining short instruction sequences that end in a return, found in existing code.
history:
  year: 2007
  people: [Hovav Shacham]
  note: Shacham (CCS 2007) showed that short sequences ending in a return give Turing-complete computation on x86. Later work moved it to RISC machines and to code without returns.
prereqs: [return-to-libc-attack]
see_also: [shadow-stack, control-flow-integrity, address-space-layout-randomization, control-flow-bending, data-oriented-programming, code-pointer-integrity, turing-completeness, linear-sweep-disassembly]
sources:
  - paper: "Hovav Shacham, The geometry of innocent flesh on the bone, return-into-libc without function calls (on the x86), 14th ACM Conference on Computer and Communications Security (CCS 2007), pages 552-561"
    locator: the abstract, the introduction and the conclusion (the model of computation and the lesson that W xor X is not enough)
  - paper: doi:10.1145/2133375.2133377
    title: Ryan Roemer, Erik Buchanan, Hovav Shacham and Stefan Savage, Return-oriented programming, systems, languages, and applications, ACM Transactions on Information and System Security 15(1), article 2, 2012, pages 1-34
    locator: the general definition of the technique across architectures and the discussion of defenses
  - paper: doi:10.1145/1866307.1866370
    title: Stephen Checkoway, Lucas Davi, Alexandra Dmitrienko, Ahmad-Reza Sadeghi, Hovav Shacham and Marcel Winandy, Return-oriented programming without returns, CCS 2010, pages 559-572
    locator: the abstract and the conclusion (defenses that look for return instructions do not stop the class)
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the sections on code reuse and on control-flow integrity as the policy that stops it
---

Return-oriented programming (ROP) is the general form of code reuse. After a hijack of control, the attacker does not call whole functions, as in [return-to-libc](/return-to-libc-attack/), but runs a series of short instruction sequences that already exist in the program or its libraries, each of which ends in a return. The attacker controls the stack, so each return reads the address of the next sequence from memory that the attacker wrote. The stack becomes the program and the stack pointer acts as its program counter. Shacham (2007) showed that on x86 such sequences, called *gadgets*, are plentiful in any large library, including sequences that start in the middle of an intended instruction, and that a suitable set of them is Turing-complete. The lesson was that [data execution prevention](/data-execution-prevention/) cannot stop an attacker who controls the stack, and that removing a few library functions does not help either. The defenses that matter are those that check or hide control flow: [shadow stacks](/shadow-stack/), [control-flow integrity](/control-flow-integrity/), [code-pointer integrity](/code-pointer-integrity/) and randomization. This page describes the class, its history and its defenses, with no code, no gadgets and no details of real software.

## In plain words

Think of a book of ready-made sentences, and a reader who reads one sentence, then looks at a list to find which page to read next. If you can write the list, you can make the reader say almost anything, using only sentences already in the book.

In a program, the book is the code that is already loaded. The sentences are short pieces of code that each do one small thing and then return. A return reads the next address from the stack. If an attacker has written the stack, each return jumps to the next piece the attacker chose.

So the attacker needs no new code at all. Blocking the execution of data does not help. The defenses check that each return goes back to where it was called from, or hide where the pieces are.

## When it applies

The class needs these conditions. Each defense removes one of them.

- **A hijack and control of memory that returns read.** A memory error lets the attacker change a return address and write a region that later returns read as addresses, usually the stack itself, or move the stack pointer to a region the attacker wrote. Bounds checking and [code-pointer integrity](/code-pointer-integrity/) remove the hijack.
- **Enough reusable sequences in executable memory.** Large libraries supply them. On instruction sets with variable-length instructions, a sequence can start inside another instruction, which adds sequences that the compiler never meant to create; [disassembly](/linear-sweep-disassembly/) of the intended instructions does not list them.
- **Known addresses of the sequences.** The attacker must know where they are. [ASLR](/address-space-layout-randomization/) and finer randomization make this a secret; a memory leak can reveal it.
- **No check that returns go to their call sites.** A return to the middle of a function, or to a place that does not follow a call, must not fault. A [shadow stack](/shadow-stack/) and the return checks of [CFI](/control-flow-integrity/) break this.

## The template

The class has the shape below. Each named hole is a condition from the list, and each comment names the defense that breaks the chain at that line. It is a description of the class, not a procedure.

```pseudo id=main
ROP-CLASS(program P, executable code X of P and its libraries)
L1  need ⟨hijack⟩: a memory error lets the attacker set a return address of P        ▷ broken by bounds checks, safe languages, CPI
L2  need ⟨controlled stack⟩: the region that later returns read holds attacker data    ▷ stack pivots need a second hijack
L3  need ⟨sequence set⟩: X contains short sequences s₁, …, sₘ that end in a return     ▷ compilers that remove unintended returns shrink it
L4  need ⟨layout knowledge⟩: the attacker knows the address of each sᵢ it uses         ▷ ASLR and fine-grained randomization: addresses are secret
L5  each return reads the next address from the controlled stack                       ▷ shadow stack: fault at the first return, the address is not the call site
L6  control goes to the start of some sᵢ                                               ▷ CFI: the start of sᵢ is not a valid return target
L7  sᵢ runs and ends in a return, which goes back to L5                                ▷ DEP does not apply: every sᵢ is in code pages
L8  effect: the sequence of runs computes what the attacker wants                      ▷ least privilege and system call filters limit it
```

**Walk-through.** Lines L1 and L2 are the memory error and the attacker's control of the stack. Line L3 is a property of the code base: a large library has many sequences that end in a return, and Shacham (2007) showed that the set found in a standard C library was enough for general computation. Line L4 is what randomization attacks. Lines L5 to L7 are the loop that gives the class its name: each sequence ends in a return, each return reads the next address from the stack, and so control moves through the chain. Line L5 is the earliest point where a [shadow stack](/shadow-stack/) stops it, since the first return of the chain already goes to an address other than its call site. Line L6 is where CFI stops it: the start of a sequence is almost never a valid target for that return under a precise policy. DEP has no line, because every instruction that runs is in a code page.

**What the template shows about each defense.** A shadow stack at line L5 stops every return of the chain under its assumptions; this follows from the theorem on the [shadow stack](/shadow-stack/) page. CFI at line L6 is as strong as its policy is precise: a policy that allows a return to any instruction after any call leaves sequences that start at such places. Randomization at line L4 is probabilistic and fails with a memory leak. Only a defense of line L1 removes the hijack itself.

## Classic examples

- **The original result on x86 (2007).** Shacham found sequences in the standard C library that end in a return, gave a set of them that is Turing-complete, and noted that many came from bytes inside other instructions. It answered the hope that removing library functions would stop [return-to-libc](/return-to-libc-attack/).
- **Other architectures.** Later work showed the same on RISC instruction sets with fixed-length, aligned instructions, where no unintended sequences exist (Roemer et al. 2012). So the class does not depend on the instruction encoding of x86.
- **Without returns (2010).** Checkoway et al. built the same kind of computation from sequences that end in an indirect jump instead of a return. Defenses that watch return instructions, or that count short sequences between returns, therefore miss the class; the check must apply to every indirect branch, which is what [CFI](/control-flow-integrity/) does.
- **The answer of hardware shadow stacks.** Intel CET and the shadow stacks of other processors check every return against a protected copy. They stop chains of returns at line L5, which is why later attacks moved to forward edges and to data, as in [control-flow bending](/control-flow-bending/) and [data-oriented programming](/data-oriented-programming/).
- **Randomization and leaks.** Fine-grained randomization of code was answered by attacks that read the code at run time through a memory leak and find sequences then (Snow et al. 2013). That led to execute-only memory, which hides code from reads, combined with randomization.

## Variations

- **Jump-oriented and call-oriented programming.** Sequences end in an indirect jump or an indirect call, and a dispatcher sequence moves from one to the next. A shadow stack does not see them; forward-edge CFI does.
- **Stack pivots.** If the attacker controls a region other than the stack, one sequence moves the stack pointer there, and the chain runs from that region. A defense that checks that the stack pointer stays inside the stack catches this step.
- **Sigreturn and similar entry points.** Some kernels restore a whole register set from memory on return from a signal handler. A hijack that reaches such an entry point sets every register at once. The defense is to validate the saved frame or to forbid such entries outside their intended use.
- **Blind variants against restarting servers.** If a server restarts its workers with the same layout after a crash, an attacker can learn about the layout from which requests crash, as in the [derandomization attack](/aslr-derandomization-attack/) on ASLR. The defense is to give each restart a fresh layout.

## Pitfalls

These are mistakes defenders make about the class.

- **Relying on DEP.** Non-executable memory has no line in the template.
- **Heuristics in place of policies.** Some defenses flagged long runs of short sequences or a return to a place that does not follow a call. Attackers used longer sequences and sequences that do follow calls, and such defenses were bypassed (Carlini and Wagner 2014; Goktas et al. 2014). A check with a stated policy and threat model is better than a pattern.
- **Coarse CFI.** A policy that lets every return go to any call site, or every indirect call go to any function, leaves enough targets for general computation. Precision matters, and so does a [shadow stack](/shadow-stack/) for returns.
- **Randomization without leak resistance.** One leaked code pointer reveals the base of its module, and a read of the code reveals the sequences. Randomization needs to be paired with execute-only memory or with checks that do not depend on secrets.
- **Ignoring unintended instructions.** On variable-length encodings, an audit of the intended instructions does not show all sequences that end in a return. Checks must be on control flow, not on the instruction listing.

## Exercises

1. Show, using the theorem on the [shadow stack](/shadow-stack/) page, that under the assumptions of that page the first return of a chain raises a fault unless the address it reads equals the return address of the matching call. Why does the chain then never reach line L7?
2. A CFI policy allows a return to go to any instruction that follows a call instruction in the intended code. Which sequences of line L3 remain valid targets at line L6 under this policy? Explain why the set is still large in a big library, and what a [shadow stack](/shadow-stack/) adds.
3. Explain why fixed-length, aligned instruction sets remove unintended sequences but not the class. Which line of the template does alignment weaken, and which lines does it leave?
4. In the model of the template, a defense randomizes the address of each of $m$ needed sequences independently and uniformly among $2^k$ places, and a single wrong address ends the attempt. Give the probability that a blind attempt that guesses all $m$ addresses succeeds, and explain why a leak of one address of each module changes the answer so much when the sequences of a module are not moved independently.

## References
