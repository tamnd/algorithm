---
tag: 8PDJMC
kind: technique
slug: return-to-libc-attack
name: Return-to-libc attack
aliases:
- ret2libc
area: security-and-privacy/memory-safety-defenses
level: core
summary: Hijacks control by returning into existing library functions with chosen arguments, which defeats non-executable memory.
history:
  year: 1997
  people: [Solar Designer]
  note: Described in 1997 as a way around the first non-executable stack patches. Shacham (2007) generalized it to return-oriented programming, and Tran et al. (2011) showed it is Turing-complete by itself.
prereqs: [data-execution-prevention, stack-smashing]
see_also: [return-oriented-programming, address-space-layout-randomization, shadow-stack, control-flow-integrity, aslr-derandomization-attack, code-pointer-integrity, turing-completeness, call-graph]
sources:
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the general attack model (code reuse as the step after a control-flow hijack) and the defenses that stop it
  - paper: "Hovav Shacham, The geometry of innocent flesh on the bone, return-into-libc without function calls (on the x86), 14th ACM Conference on Computer and Communications Security (CCS 2007), pages 552-561"
    locator: the introduction and the related work on return-into-libc, and the argument that removing library functions does not stop code reuse
  - paper: "Minh Tran, Mark Etheridge, Tyler Bletsch, Xuxian Jiang, Vincent Freeh and Peng Ning, On the expressiveness of return-into-libc attacks, RAID 2011"
    locator: the main result (return-into-libc with whole library functions is Turing-complete) and its lesson for defenses
  - paper: "Hovav Shacham, Matthew Page, Ben Pfaff, Eu-Jin Goh, Nagendra Modadugu and Dan Boneh, On the effectiveness of address-space randomization, 11th ACM Conference on Computer and Communications Security (CCS 2004), pages 298-307"
    locator: the threat model in which return-into-libc is the payload and ASLR hides the library base
---

A return-to-libc attack hijacks a return, like [stack smashing](/stack-smashing/), but sends it to a function that already exists in a loaded library instead of to injected code. The attacker also controls the data that the function will read as its arguments, so the reused function does the attacker's work with the program's own code. Because no new code runs, [data execution prevention](/data-execution-prevention/) does not see it: the target lies in a page that is meant to run. The attack was described in 1997, the same year as the first non-executable stack patch for Linux, and it showed that W xor X stops injection but not reuse. It is the first step of the code-reuse line: Shacham (2007) replaced whole functions by short instruction sequences in [return-oriented programming](/return-oriented-programming/), and Tran et al. (2011) showed that chains of whole library functions are already Turing-complete. The defenses that work break other conditions of the class: [ASLR](/address-space-layout-randomization/) hides where functions are, a [shadow stack](/shadow-stack/) rejects a return to anywhere but its call site, and [control-flow integrity](/control-flow-integrity/) rejects a return to the entry of a function. This page describes the class and its defenses, with no code and no details of real software.

## In plain words

A program that runs on a normal system has a library of useful functions loaded next to it: functions that open files, start other programs, or change memory permissions. They are there because the program might need them.

After an attacker takes over where a function returns, there is no need to bring new code. The return can go straight to the start of one of these library functions. The attacker also arranges the values that the function will take as its inputs.

The processor sees nothing wrong. It runs code from a code page, just as it should. So blocking the execution of data does not help. What helps is to hide where the library is, or to check that each return goes back to the place it came from.

## When it applies

The class needs all of these conditions. Each defense removes one of them.

- **A hijacked return or indirect branch.** A memory error, such as a stack [buffer overflow](/buffer-overflow/), changes a saved return address or a code pointer. Bounds checking and [code-pointer integrity](/code-pointer-integrity/) remove this condition.
- **A known address of a useful function.** The attacker must know where the target function is. Without randomization, library addresses are the same in every run. [ASLR](/address-space-layout-randomization/) makes them secret, until a leak or a guessing attack reveals them.
- **Control of the arguments.** The function must find the attacker's values where it reads its arguments. On calling conventions that pass arguments on the stack, the overflow can place them. On conventions that pass them in registers, the attacker needs more code reuse to load the registers, which leads to [return-oriented programming](/return-oriented-programming/).
- **No check on the return target.** The return must be allowed to go to the start of a function. A [shadow stack](/shadow-stack/) or the return checks of [control-flow integrity](/control-flow-integrity/) forbid it.

## The template

The class has the shape below. Each named hole is a condition from the list, and each comment names the defense that breaks the chain at that line. It is a description of the class, not a procedure.

```pseudo id=main
RETURN-TO-LIBC-CLASS(program P with library L loaded, function G of P)
L1  need ⟨hijack⟩: a memory error lets the attacker set the return address A of G       ▷ broken by bounds checks, safe languages, CPI
L2  need ⟨known target⟩: the attacker knows the entry address of a function F in L      ▷ ASLR: the base of L is a secret
L3  need ⟨argument control⟩: the attacker sets the data that F reads as its arguments   ▷ register calling conventions make this harder
L4  G returns: the return reads A                                                       ▷ shadow stack: fault, A is not the call site of G
L5  control goes to the entry of F                                                      ▷ CFI: the entry of F is not a valid return site
L6  F runs with the chosen arguments; ⟨chain⟩ may repeat L2 to L5 for more functions    ▷ DEP does not apply: F is in a code page
L7  effect: F does work that the program did not intend                                 ▷ least privilege and system call filters limit it
```

**Walk-through.** Line L1 is the same memory error as in stack smashing; a defense that stops it ends the class. Lines L2 and L3 are what the attacker must know and control. Line L2 is the condition that ASLR attacks: the library is at a random base, so the entry of $F$ is a secret, and the attack depends on a leak or on guessing, as in the [derandomization attack](/aslr-derandomization-attack/). Lines L4 and L5 are the two points where a check on control flow can stop the attack. A return that is checked against a protected copy fails at line L4, and a return whose target must be the instruction after a call fails at line L5, because the entry of a function is not such an instruction. Line L6 is where DEP fails as a defense, which was the lesson of the attack. Line L7 is about damage, not hijack: a process with few rights, or a filter on the system calls it may make, limits what any reused function can do.

**What the template shows about each defense.** Only a defense of lines L1, L2, L4 or L5 stops the hijack. DEP is not on the list. ASLR at line L2 is a probabilistic defense whose strength is the entropy of the base, and a single leaked address of the library removes it. Shadow stacks and CFI at lines L4 and L5 are deterministic under their assumptions.

## Classic examples

- **Around the non-executable stack (1997).** The first public description answered the non-executable stack patch: with injected code blocked, the hijacked return went to a library function instead. It is the reason that [data execution prevention](/data-execution-prevention/) is never deployed alone.
- **The payload in the ASLR study (2004).** Shacham et al. used a return into a library function as the payload against a server protected by PaX ASLR and W xor X. The question was then only how fast the library base could be found; see [address space layout randomization](/address-space-layout-randomization/) and the [derandomization attack](/aslr-derandomization-attack/).
- **The move to [return-oriented programming](/return-oriented-programming/) (2007).** One answer to return-to-libc was to remove or guard the dangerous library functions. Shacham showed that this does not help, because short sequences inside any large body of code give a Turing-complete set of operations, with no function calls at all.
- **Turing completeness with whole functions (2011).** Tran et al. showed that chaining whole library functions, without short sequences, is already Turing-complete. So a defense that allows returns into function entries but blocks short sequences still leaves a general attacker.
- **Coarse CFI.** A CFI policy that only requires returns to go to some call site, rather than to the matching one, still forbids a return to a function entry, so it stops the classic form at line L5. [Control-flow bending](/control-flow-bending/) shows what remains under such policies.

## Variations

- **Chains of functions.** The attacker arranges several returns in a row, so that one function returns into the next. This is the ⟨chain⟩ hole of line L6, and it is how the class reaches general computation.
- **Return into the procedure linkage table.** In a program built with dynamic linking, calls to library functions go through stubs at fixed places in the program image. If the program image is not randomized, these stubs give known targets even when the library is randomized. Position-independent executables, which let ASLR move the program image as well, remove this.
- **Jump and call variants.** The hijack may go through a corrupted function pointer instead of a return. Then the check point is the forward edge of [CFI](/control-flow-integrity/) rather than the shadow stack.
- **Data-only reuse.** If the attacker can change the arguments of a call that the program makes anyway, no hijack is needed. These are the non-control-data attacks of [data-oriented programming](/data-oriented-programming/), which control-flow defenses do not stop.

## Pitfalls

These are mistakes defenders make about the class.

- **Trusting DEP.** Non-executable memory does not touch this class at all. It must be combined with a defense of lines L1, L2, L4 or L5.
- **Removing dangerous functions.** Deleting or wrapping a few library functions does not end the class: other functions or short sequences give the same power (Shacham 2007; Tran et al. 2011).
- **Mapping libraries at addresses with a zero byte.** Some systems placed libraries at addresses that contain a zero byte, so that a string copy could not write them. It stops only string-based overflows, and only on 32-bit layouts. It is not a general defense.
- **Weak randomization.** ASLR with 16 bits of entropy on a 32-bit system fell to guessing in minutes against a server that restarts its workers with the same layout (Shacham et al. 2004). Use 64-bit layouts, randomize the program image as well, and treat every address leak as a full break.
- **A shadow stack without forward-edge checks.** A shadow stack stops line L4 for returns. A hijack through a function pointer reaches line L5 without a return, so it needs CFI on indirect calls.

## Exercises

1. For each line L1 to L7 of the template, name one defense that breaks it, and say whether its guarantee is deterministic or probabilistic. Which lines does DEP break?
2. A coarse CFI policy allows a return to any instruction that follows a call in the program. Explain why it stops the classic form of the attack at line L5, and why it does not stop an attacker who chains returns to instructions that follow calls.
3. A system randomizes the library base with $k$ bits of entropy but does not randomize the program image, and the program image contains linkage stubs for library functions. Which line of the template does ASLR no longer break, and why?
4. Explain, in terms of the [call graph](/call-graph/), why the return of a function $G$ to the entry of a library function $F$ is never an edge that a precise policy for returns would allow.

## References
