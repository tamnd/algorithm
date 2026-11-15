---
tag: XS0RJ3
kind: technique
slug: proof-carrying-code
name: Proof-carrying code
aliases:
- PCC
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Ships machine code with a formal proof that it meets a safety policy, which the host checks with a small fast proof checker.
prereqs: [verification-condition-generation, type-soundness]
see_also: [curry-howard-correspondence, hoare-logic, verified-compilation, translation-validation, loop-invariant, simply-typed-lambda-calculus, design-by-contract, houdini-algorithm]
sources:
  - paper: doi:10.1145/248155.238781
    title: George C. Necula and Peter Lee, Safe kernel extensions without run-time checking, Proceedings of OSDI 1996, ACM SIGOPS Operating Systems Review 30(SI)
    locator: pp. 229 to 243, the first PCC system, for network packet filters in DEC Alpha assembly language, with a one-time proof check and no run-time checks
  - paper: doi:10.1145/263699.263712
    title: George C. Necula, Proof-carrying code, Proceedings of POPL 1997
    locator: pp. 106 to 119, the safety policy, the verification condition generator, proofs as LF terms, and proof checking by type checking
  - paper: doi:10.1145/277650.277752
    title: George C. Necula and Peter Lee, The design and implementation of a certifying compiler, Proceedings of PLDI 1998
    locator: pp. 333 to 344, the Touchstone compiler from a type-safe subset of C to optimized Alpha code, which emits the invariants and the proof
  - paper: doi:10.1145/319301.319345
    title: Greg Morrisett, David Walker, Karl Crary and Neal Glew, From System F to typed assembly language, ACM Transactions on Programming Languages and Systems 21(3), 1999
    locator: pp. 527 to 568, typed assembly language, where the certificate is a set of type annotations and the checker is a type checker
  - paper: doi:10.1109/LICS.2001.932501
    title: Andrew W. Appel, Foundational proof-carrying code, Proceedings of LICS 2001
    locator: the problem of trusting the verification condition generator, and proofs of safety stated directly over a machine semantics in higher-order logic
---

Proof-carrying code, or PCC, lets a host run machine code from a source it does not trust without run-time checks. The producer sends the code together with a formal proof that the code obeys the host's safety policy, for example "every memory read is inside the packet buffer". The host computes a [verification condition](/verification-condition-generation/) from the code it received and checks that the proof proves it, with a small and fast checker. If the logic is sound, accepted code is safe, whoever wrote it and whatever compiler or prover made the proof.

## In plain words

Imagine you load a plug-in into your kernel. Checking every memory access while it runs is slow, and trusting its author is risky. With proof-carrying code, the author must send a proof with the plug-in, a proof that it never touches memory it should not touch. Finding such a proof can be hard, but that is the author's problem. Checking a proof that is given is easy and mechanical, like checking the steps of a long sum. You check it once, when the plug-in arrives. If anybody changed the code on the way, the proof no longer fits and you reject the code, or it still fits and the changed code is safe too.

## When it applies

- A host, the *consumer*, runs code from a *producer* it does not trust, and the code must be fast: kernel extensions, packet filters, mobile code, code for small devices.
- The safety policy can be written as preconditions in a logic: memory safety, type safety, bounds on resources, or the calling conventions of an interface.
- The producer can make proofs, usually because a *certifying compiler* knows why its output is safe and writes that knowledge down as invariants and a proof.

The policy is about all runs of the code, and such properties are undecidable in general by [Rice's theorem](/rice-theorem/). PCC avoids the problem by moving the search for a proof to the producer: the consumer only checks a proof, which is decidable and fast.

## The template

```pseudo id=main
PRODUCER(C, SP)                       ▷ C: annotated code, SP: the published safety policy
L1  phi <- VCGEN(SP, C)               ▷ hole VCGEN: the verification condition generator of the policy
L2  pi <- PROVE(phi)                  ▷ hole PROVER: a certifying compiler, a theorem prover, or a person
L3  send (C, pi)

CONSUMER(C, pi, SP)
L4  phi <- VCGEN(SP, C)               ▷ computed again from the code that arrived
L5  if CHECK(pi, phi) in LOGIC then   ▷ hole LOGIC: the axioms and rules of the proof language
L6      run C with no run-time checks
L7  else reject C
```

**The parts.** The code $C$ comes with annotations: a [loop invariant](/loop-invariant/) at each loop head and a precondition and a postcondition at each function, as in [design by contract](/design-by-contract/). The policy $SP$ gives the precondition of each unsafe instruction, for example $\mathit{rd}(a)$, "address $a$ may be read", for a load from $a$, and the facts that hold on entry. $\mathrm{VCGEN}$ walks the code backwards from each annotation, as in [Hoare logic](/hoare-logic/), and gives one formula $\varphi$ that says: each annotation is preserved, and each unsafe instruction meets its precondition. The proof $\pi$ is a term in the proof language. In Necula's system it is a term of the logical framework LF, and checking it is type checking, by the [Curry-Howard correspondence](/curry-howard-correspondence/).

**Soundness chain.** Suppose that three things hold:

1. **The logic is sound:** every formula provable in LOGIC is true.
2. **The VC generator is sound for the policy:** if $\mathrm{VCGEN}(SP, C)$ is true, then every run of $C$ from a state that meets the entry facts of $SP$ obeys $SP$.
3. **The checker is correct:** $\mathrm{CHECK}(\pi, \varphi)$ succeeds only if $\pi$ is a proof of $\varphi$ in LOGIC.

Then every program that the consumer runs obeys the policy. *Proof.* If L5 succeeds, $\pi$ is a proof of $\varphi = \mathrm{VCGEN}(SP, C)$ by item 3, so $\varphi$ is true by item 1, so every run of $C$ obeys $SP$ by item 2. $\square$

Nothing in the chain mentions the producer, its compiler, its prover or the network. They can all be wrong or hostile. The *trusted computing base* is the VC generator, the checker, the axioms of the logic and the model of the machine that the VC generator uses. The annotations are not trusted either: a wrong invariant makes $\varphi$ false, and no proof of a false formula exists in a sound logic.

**Tamper-proof.** If $C$ is changed on the way to $C'$, the consumer computes $\mathrm{VCGEN}(SP, C')$. Either $\pi$ does not prove it and $C'$ is rejected, or $\pi$ proves it and $C'$ is safe by the chain above. There is no need for signatures or for trust in the sender.

**Walk-through.** A packet filter reads the bytes $p[0], \ldots, p[n - 1]$ of a packet of length $\mathit{len}$. The policy says that a load from $p + i$ needs $0 \le i < \mathit{len}$, and that $n \le \mathit{len}$ holds on entry. The loop $i := 0;\ \mathbf{while}\ i < n\ \mathbf{do}\ (\ldots\ \mathrm{load}\ p[i]\ \ldots;\ i := i + 1)$ carries the invariant $0 \le i \wedge n \le \mathit{len}$. The VC has three parts: the invariant holds on entry ($0 \le 0$ and $n \le \mathit{len}$); the load is safe ($0 \le i \wedge n \le \mathit{len} \wedge i < n \Rightarrow 0 \le i < \mathit{len}$); and the invariant is preserved ($0 \le i \Rightarrow 0 \le i + 1$). The proof is a few steps of linear arithmetic, and the loop then runs with no bounds checks.

## Classic examples

- **Packet filters.** Necula and Lee wrote network packet filters in hand-tuned Alpha assembly language and shipped them with proofs of memory safety. The kernel checked each proof once, in about 1 to 3 milliseconds, and the filters then ran faster than interpreted or sandboxed filters.
- **Certifying compilers.** Touchstone compiled a type-safe subset of C to optimized Alpha code and emitted the loop invariants and the proof of type and memory safety with it. The compiler knows why its output is safe, so it can write the proof; this is the opposite of [translation validation](/translation-validation/), where a separate tool must rediscover why the output is right.
- **Typed assembly language.** Morrisett, Walker, Crary and Glew compile System F, an extension of the [simply typed lambda calculus](/simply-typed-lambda-calculus/), to an assembly language with type annotations. The certificate is the annotations, the checker is a type checker, and [type soundness](/type-soundness/) of the assembly language plays the role of the soundness of the logic.
- **Bytecode verification.** A virtual machine that checks the types of loaded bytecode before it runs it applies the same idea with no explicit proof. Type annotations that the compiler adds at branch targets make the check a single pass, as in PCC.
- **Annotation inference.** The loop invariants of the annotations can come from an inference tool, such as the [Houdini algorithm](/houdini-algorithm/), since the checker does not need to trust them.

## Variations

- **Foundational PCC.** Appel removes the VC generator from the trusted base. The policy is stated directly as a property of the machine semantics in a higher-order logic, and the proof covers the step from the code to the policy too. The trusted base becomes the logic, the machine model and the checker.
- **Small proofs.** LF proofs can be much larger than the code. Later systems send only the choices that a deterministic proof search would make, or let the checker run a decision procedure for simple arithmetic, which trades checker size for proof size.
- **Types instead of proofs.** Typed assembly language and bytecode verification ship types instead of formulas. The checker is a type checker, and the proof of safety is done once, for the type system, instead of once for each program.
- **Verified compilers.** A [verified compiler](/verified-compilation/) proves once that every output is correct, so its outputs need no certificates. PCC proves less, a safety policy and not full correctness, but it does not ask the consumer to trust any compiler.

## Pitfalls

- **The chain is only as strong as its weakest link.** A bug in the VC generator or an unsound axiom breaks safety for every program. An inconsistent set of axioms proves every formula, so every program is accepted.
- **The policy is what is proved.** PCC proves that code obeys the policy, not that it does what the user wants. A policy that forgets an unsafe instruction, or a machine model that differs from the real processor, makes the proof worthless.
- **The consumer must compute the VC.** If the consumer accepts a formula from the producer, a producer can send a true formula that has nothing to do with the code, such as $\mathit{true}$.
- **Proofs can be big.** Proof size and check time are the practical costs. Plan for proof compression or a checker with built-in decision procedures.
- **Safety, not liveness.** The usual policies are safety properties. A proof of memory safety says nothing about termination or running time unless the policy includes a resource bound.

## Exercises

1. Why must the consumer compute the VC itself, instead of receiving it with the code? *Answer.* A received VC need not be the VC of the received code. A producer could send unsafe code with a proof of $\mathit{true}$.
2. In the walk-through, the producer forgets the conjunct $n \le \mathit{len}$ of the invariant. Which part of the VC fails? *Answer.* The safety of the load: from $0 \le i \wedge i < n$ alone, $i < \mathit{len}$ does not follow, so no proof exists and the consumer rejects the code.
3. An attacker changes the loop guard to $i \le n$ after the proof is made. What does the consumer do? *Answer.* It computes the VC of the changed code, whose load condition is $0 \le i \wedge n \le \mathit{len} \wedge i \le n \Rightarrow i < \mathit{len}$. This is false for $i = n = \mathit{len}$, so the old proof does not prove it, no proof exists, and the code is rejected.
4. Which parts of a PCC system are trusted, and which does foundational PCC remove? *Answer.* The VC generator, the proof checker, the axioms of the logic and the machine model. Foundational PCC removes the VC generator.

## References
