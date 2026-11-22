---
tag: BDGPFB
kind: technique
slug: software-fault-isolation
name: Software fault isolation
aliases:
- SFI
- address sandboxing
area: security-and-privacy/memory-safety-defenses
level: core
summary: Rewrites untrusted machine code so that every store and jump is masked or checked to stay inside its own region of memory.
history:
  year: 1993
  people: [Robert Wahbe, Steven Lucco, Thomas E. Anderson, Susan L. Graham]
  note: Wahbe et al. (SOSP 1993) introduced fault domains, segment matching and address sandboxing on RISC processors. Native Client (2009) brought the idea to x86 code in a web browser.
prereqs: [memory-safety, reference-monitor]
see_also: [inline-reference-monitor, control-flow-integrity, data-execution-prevention, code-pointer-integrity, proof-carrying-code, security-automaton, linear-sweep-disassembly, bit-vector]
sources:
  - paper: doi:10.1145/168619.168635
    title: Robert Wahbe, Steven Lucco, Thomas E. Anderson and Susan L. Graham, Efficient software-based fault isolation, 14th ACM Symposium on Operating Systems Principles (SOSP 1993), pages 203-216
    locator: the section on the software encapsulation method (fault domains, segment matching and address sandboxing with dedicated registers, and the verifier of the object code), and the introduction for the average overhead of 4 percent on a test suite with the C SPEC92 benchmarks
  - paper: "Bennet Yee, David Sehr, Gregory Dardyk, J. Bradley Chen, Robert Muth, Tavis Ormandy, Shiki Okasaka, Neha Narula and Nicholas Fullagar, Native Client, a sandbox for portable, untrusted x86 native code, 2009 IEEE Symposium on Security and Privacy, pages 79-93"
    locator: the inner sandbox (the validator, the alignment rules for instructions and jump targets, and the use of segments for data) and the reported cost
  - paper: doi:10.1145/1609956.1609960
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, principles, implementations, and applications, ACM Transactions on Information and System Security 13(1), article 4, 2009
    locator: the section on building software fault isolation on top of CFI
---

Software fault isolation (SFI) runs untrusted code in the same address space as trusted code, but confines it to its own region of memory, called a *fault domain*, without help from the hardware's memory protection. A rewriter changes the untrusted machine code so that every store and every indirect jump uses an address that is first forced into the domain or checked against it, and a verifier checks the rewritten code before it is loaded. Wahbe, Lucco, Anderson and Graham (SOSP 1993) introduced the idea for RISC processors. A fault domain is a code segment and a data segment, each a range of addresses whose upper bits are the segment identifier. *Segment matching* checks the upper bits of each unsafe address and traps on a mismatch. *Address sandboxing* does not check: it sets the upper bits to the segment identifier with an AND and an OR, two instructions before each unsafe store or jump, so a wrong address is moved into the domain instead. The key design point is a *dedicated register* that only the sandboxing code may write: since it always holds an address in the domain, the code stays safe even if a jump lands right after the check. They measured an average overhead of 4 percent on a test suite that included the C SPEC92 benchmarks, far below the cost of switching hardware address spaces for each call. Native Client (2009) later applied the method to x86 code in a browser, and SFI is the classic example of an [inline reference monitor](/inline-reference-monitor/).

## In plain words

Suppose a program must run a plug-in that it does not trust. The usual answer is to put the plug-in in a separate process, but then every call between them is slow.

SFI keeps the plug-in in the same process and gives it one area of memory. Before the plug-in is loaded, its code is changed: in front of every instruction that writes memory or jumps through a pointer, a small step is added that forces the address into the plug-in's area. A checker then reads the changed code and refuses it if any write or jump could skip that step.

Now even a broken or hostile plug-in can only damage its own area. The checks cost a few instructions each, much less than switching between processes.

## When it applies

- **The threat is an untrusted module** in the same address space: a plug-in, a driver, a database extension or code from the web. The module may be buggy or hostile, and it controls every value it computes.
- **Calls across the boundary are frequent**, so separate address spaces with hardware protection would cost too much.
- **The code can be rewritten and verified** before it runs, by a compiler that emits sandboxed code, by a binary rewriter, or by a loader that rejects code that does not follow the rules.
- **The instruction set allows a reliable verifier.** On RISC processors, instructions have one length and one alignment, so the verifier sees every instruction. On x86, instructions have many lengths, so the system must restrict where jumps may land, as Native Client does with aligned bundles.
- **Code cannot be changed after verification.** The code segment is not writable and data is not executable, as [data execution prevention](/data-execution-prevention/) provides.

## The template

The defense has a rewriter that inserts the sandboxing steps and a verifier that the loader runs. The named holes are the choices of each system. The block shows the confinement of stores; indirect jumps are confined in the same way, with the code segment and a second dedicated register.

```pseudo id=main
REWRITE(module M, segment identifier g, offset bits m)
L1  reserve a dedicated register d that M does not use; the loader sets d to an address in the domain
L2  for each store through a register a in M whose address is not known to be in the domain do
L3      ⟨address sandboxing⟩: d ← (a AND (2^m - 1)) OR (g · 2^m)        ▷ two instructions, no branch
L4      or ⟨segment matching⟩: if a >> m ≠ g then trap; d ← a             ▷ a compare and a branch
L5      store through d instead of a

VERIFY(rewritten module M′)
L6  if any instruction of M′ other than a sandboxing step writes d then reject
L7  if any store goes through a register other than d, or a direct jump leaves M′, then reject
L8  accept
```

**Walk-through.** Line L1 reserves the dedicated register. Lines L2 to L5 rewrite each unsafe store. Address sandboxing at line L3 keeps the low $m$ bits of the address and replaces the upper bits by $g$, so the result is in the domain whatever the value of $a$. Segment matching at line L4 checks the upper bits instead, which costs a branch but reports the error. Line L5 makes the store use the dedicated register. Lines L6 and L7 are the verifier: it does not trust the rewriter, so a module from any source is safe once it passes. Wahbe et al. used four dedicated registers for segment matching and five for address sandboxing, for data and code addresses and their segment values.

**Correctness.** The verifier gives the invariant that $d$ always holds an address in the domain. At load time the loader sets $d$ in the domain. Only a sandboxing step may write $d$ (line L6), and every such step leaves an address in the domain or traps. Jumps change no register. So the invariant holds at every instruction, even at a store that a jump reached directly, skipping the step before it. Since every store goes through $d$ (line L7), every store writes inside the domain, whatever values the module computes. A second theorem says that the rewriting is transparent: a run of the original module whose stores were all in the domain makes the same stores after rewriting. The full proofs are in [the proof file](proofs/correctness.md).

**Example.** Take $w = 16$-bit words, $m = 10$ offset bits and segment identifier $g = 5$, so the domain is the addresses 5120 to 6143. A module sets $a \leftarrow 3$ and $b \leftarrow 7$ and stores $b$ at the address in $a$. Address 3 is outside the domain. After rewriting with address sandboxing, the store goes through $d = (3 \wedge 1023) \vee 5120 = 5123$, inside the domain; the module wrote the wrong cell of its own domain, but no cell of anyone else. With segment matching, the step at line L4 sees that $3 \gg 10 = 0 \ne 5$ and traps before the store.

**Cost.** In the [word RAM](/word-ram/) model each sandboxed store costs $O(1)$ extra operations, and the rewriter and the verifier each take $O(n)$ time for $n$ instructions. The measured cost is in the lead: an average of 4 percent in the 1993 study, on a DECstation and an Alpha. A call across the boundary costs a jump through a trusted stub, which is why SFI beats separate processes when calls are frequent.

**Code.** The Python file `impl/python/software_fault_isolation.py` has the rewriter, the verifier and an interpreter for an abstract register machine with stores, loads, direct and indirect jumps. The tests run random verified modules with random registers and check every store address against the domain, and compare rewritten and original runs.

## Classic examples

- **The original design (1993).** Wahbe et al. rewrote code for MIPS and Alpha processors, used segment matching or address sandboxing with dedicated registers, and gave a verifier that checks the rewritten object code. Their goal was fast communication between modules in one address space.
- **Native Client (2009).** Yee et al. ran untrusted x86 code in a web browser. Since x86 instructions have variable length, the validator requires that code be split into fixed-size aligned bundles, that no instruction cross a bundle boundary, and that indirect jumps go only to bundle starts. Then the validator's [disassembly](/linear-sweep-disassembly/) sees every instruction that can run. Data accesses were confined with the segment registers of 32-bit x86.
- **SFI on top of CFI.** Abadi et al. showed that [control-flow integrity](/control-flow-integrity/) makes SFI simpler: if every jump is known to follow the control flow graph, a check before a store cannot be skipped, so no dedicated register is needed for that purpose.
- **An [inline reference monitor](/inline-reference-monitor/).** SFI enforces a [safety property](/safety-property/) (no store outside the domain) by checks inserted into the code itself, which is the general pattern of inline monitors and of policies given as a [security automaton](/security-automaton/).
- **Safer extensions in other forms.** [Proof-carrying code](/proof-carrying-code/) replaces the rewriter by a proof that the code is safe, checked by the loader. The goal is the same: let untrusted code run at full speed in a trusted process.

## Variations

- **Stores and jumps only, or loads too.** Confining only stores and jumps protects integrity, which was the cheaper choice in the 1993 study. Confining loads as well also protects secrecy, at a higher cost.
- **Guard zones.** If a store adds a small constant offset to a sandboxed register, the result may fall just outside the domain. Placing unmapped guard pages around the domain makes such stores fault, so the constant need not be sandboxed.
- **Hardware assistance.** Segment registers on 32-bit x86, memory protection keys, or large reserved regions of a 64-bit address space with guard pages can replace some of the software checks.
- **Verified and formally proved sandboxes.** Later work proved the safety of an SFI design for x86 with a mechanical proof, and modern sandboxes for portable bytecode compile it to native code with the same kind of address confinement.
- **Isolation for other defenses.** [Code-pointer integrity](/code-pointer-integrity/) needs its safe region to be out of reach of regular accesses; SFI-style masking of those accesses is one way to provide it.

## Pitfalls

- **A verifier that trusts the rewriter.** The point of the design is that the loader checks the code itself. A verifier must reject any store or jump that does not use a dedicated register, whoever produced the code.
- **Jumps into the middle of instructions.** On variable-length instruction sets, a jump to an unintended offset can decode as a different instruction stream that the verifier never saw. Alignment rules for jump targets, as in Native Client, close this.
- **Writable code.** If the module can write its own code segment, it can remove the checks after verification. Code must be non-writable, and code generated at run time must be verified before it can run.
- **Forgetting the boundary.** The calls from the module into trusted code, and the values passed across, are part of the attack surface. Trusted stubs must check their arguments.
- **Leaks through loads.** A design that confines only stores lets the module read the rest of the process. If the process holds secrets, confine loads too.
- **Side channels.** SFI confines architectural accesses. Speculative execution can read outside the domain without any store or architectural load; see the [Spectre attack](/spectre-attack/).

## Exercises

1. With $w = 16$, $m = 10$ and $g = 5$, compute the result of address sandboxing at line L3 for the addresses 0, 5120, 6143, 6144 and 65535. Which of them does segment matching at line L4 accept?
2. Prove Lemma 1 of the proof file: for every word $a$, the value $(a \wedge (2^m - 1)) \vee g \cdot 2^m$ lies in the domain when $g < 2^{w - m}$.
3. A variant of the rewriter sandboxes the address into the register $a$ itself, $a \leftarrow (a \wedge (2^m - 1)) \vee g \cdot 2^m$, and then stores through $a$. Give a module and a jump that store outside the domain under this variant, and explain which line of the verifier the dedicated register replaces.
4. A store writes to $d + k$ for a constant $k$ with $0 \le k < 2^{12}$. How large must the guard zones around the domain be so that every such store either lands in the domain or faults?

## References
