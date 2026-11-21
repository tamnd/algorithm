---
tag: GYAKDB
kind: technique
slug: inline-reference-monitor
name: Inline reference monitor
aliases:
- SASI rewriting
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Enforces a security automaton by rewriting the program so that the checks run inside it before each relevant instruction.
prereqs: [security-automaton, reference-monitor]
see_also: [em-enforceable-policies-theorem, software-fault-isolation, control-flow-integrity, addresssanitizer, partial-evaluation, proof-carrying-code, stack-canary, shadow-stack]
sources:
  - paper: doi:10.1145/335169.335201
    title: Úlfar Erlingsson and Fred B. Schneider, SASI enforcement of security policies, a retrospective, Proceedings of the New Security Paradigms Workshop 1999
    locator: pp. 87 to 95, policies as security automata, the rewriter that inserts the automaton before each instruction, partial evaluation of the inserted code, and the x86 and JVML versions
  - paper: doi:10.1109/SECPRI.2000.848461
    title: Úlfar Erlingsson and Fred B. Schneider, IRM enforcement of Java stack inspection, Proceedings of the 2000 IEEE Symposium on Security and Privacy
    locator: pp. 246 to 255, the PoET rewriter and the PSLang policy language, and Java stack inspection as an inlined monitor
  - paper: doi:10.1145/1134744.1134748
    title: Kevin W. Hamlen, Greg Morrisett and Fred B. Schneider, Certified in-lined reference monitoring on .NET, Proceedings of PLAS 2006
    locator: pp. 7 to 16, a type checker that verifies the rewritten program, so that the rewriter need not be trusted
  - paper: doi:10.1145/353323.353382
    title: Fred B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1), 2000
    locator: pp. 30 to 50, security automata and execution monitoring
  - paper: doi:10.1145/1111596.1111601
    title: Kevin W. Hamlen, Greg Morrisett and Fred B. Schneider, Computability classes for enforcement mechanisms, ACM Transactions on Programming Languages and Systems 28(1), 2006
    locator: pp. 175 to 205, the class of policies that program rewriting can enforce and its relation to execution monitors and static analysis
---

An inline reference monitor (IRM) enforces a security policy by rewriting the program it protects. The policy is given as a [security automaton](/security-automaton/). The rewriter adds the automaton's state to the program and inserts, before each instruction that can cause a security-relevant event, code that steps the automaton and stops the program if the step is not allowed. The result behaves like the original program watched by an execution monitor, but no separate monitor process or kernel change is needed, and the checks can use the program's own state. Erlingsson and Schneider built the first general IRM rewriters, SASI for x86 and Java bytecode in 1999 and PoET for Java in 2000. The idea is a direct answer to the [reference monitor](/reference-monitor/) concept: a reference monitor must see every access, be tamper-proof and be small enough to verify, and an IRM must meet the same three requirements from inside the program.

## In plain words

A reference monitor is a guard that checks every access. Usually the guard sits outside the program, in the operating system. An inline reference monitor puts the guard inside the program instead. A tool reads the program before it runs and, in front of every dangerous instruction, writes a short check: "is this allowed now, given what the program has done so far?" If not, the program stops. The tool also has to make sure the program cannot skip a check, jump into the middle of one, or change the record that the checks keep. Then the program, now carrying its own guard, can run on an ordinary system. Checks that can never fail are removed before the program runs.

## When it applies

- **The policy is a safety property of one run.** It must be expressible by a security automaton over events the program performs: "no send after a read of a secret file", "at most $n$ open sockets", "only call this function with a lock held". By the [theorem on execution monitors](/em-enforceable-policies-theorem/), a monitor that can only stop the program enforces only safety properties, and an IRM that only inserts checks and halts is such a monitor.
- **The events can be found in the code.** Each event must correspond to instructions or calls that the rewriter can recognize statically: a call to a library function, a store, an indirect jump, a system call instruction.
- **The program cannot escape the rewriting.** The code must be analyzable: no code generated at run time that skips the rewriter, and a control flow and memory model in which the program cannot reach an event without passing its check and cannot write the automaton's state. Type-safe bytecode gives this for free. Machine code needs [software fault isolation](/software-fault-isolation/) and [control-flow integrity](/control-flow-integrity/).
- **The cost of the checks is acceptable.** Each event costs a check. Partial evaluation can remove most checks when the automaton state at that point is known statically.

The technique does not apply to policies about two or more runs, such as noninterference, and it cannot by itself enforce liveness properties such as "every opened file is eventually closed".

## The template

The input is a program $P$ and a security automaton $A = (Q, q_0, \delta)$ with a partial transition function $\delta : Q \times \Sigma \to Q$. Undefined steps are violations.

```pseudo id=main
IRM-REWRITE(P, A)
L1  E ← EVENTS(P, A)                ▷ hole EVENTS: the instructions of P whose execution is an event in Σ
L2  P′ ← add a variable st to P, set to q0 at the entry point   ▷ hole STATE: where st lives
L3  for each instruction i of P in E do
L4      insert before i: st ← δ(st, event(i)); if δ was undefined then HALT
L5  P′ ← SPECIALIZE(P′, A)          ▷ hole PE: partial evaluation removes checks whose outcome is known
L6  P′ ← PROTECT(P′)                ▷ hole PROTECT: P′ cannot write st or reach i without its check
L7  return P′
```

The four holes are the whole design of an IRM:
- **EVENTS** decides what the policy can talk about. At the level of machine instructions it can talk about stores and jumps; at the level of a library it can talk about "open a file" or "send a message". The finer the level, the harder it is to write a high-level policy.
- **STATE** holds the automaton state. It may be a global variable, a field per object, or a word in a region of memory that the rest of the program cannot address.
- **PE** evaluates $\delta$ at rewriting time where the state is known. Erlingsson and Schneider used it to delete the inserted code at instructions where no transition of the automaton can change the state or fail.
- **PROTECT** is what makes the guarantee hold. It ensures that each path to an event passes through the check before it, that no instruction of the original program writes `st`, and that the inserted code cannot be bypassed by a jump into its middle.

**Guarantee (theorem, under the hypotheses).** Assume: every execution of an event $e$ of $P$ happens at an instruction in $E$; in $P'$, every path to such an instruction passes through the check inserted before it; no instruction of $P$ writes `st`; and HALT stops the program before the instruction after it runs. The adversary is the program $P$ itself, which may be written to break the policy, with any input. Then the event sequence of every run of $P'$ is the longest prefix of the event sequence of the matching run of $P$ that $A$ accepts. *Proof.* By induction on the number of events executed. Before the $k$-th event, `st` equals $\delta^\ast(q_0, e_1 \cdots e_{k-1})$, because only inserted code writes `st`, and it runs exactly once before each event. If $\delta(\mathit{st}, e_k)$ is defined, the check passes and the event runs, which keeps the invariant. If it is undefined, the program halts before $e_k$, so the trace is the longest accepted prefix. Partial evaluation keeps this invariant because it removes only code whose result it has computed. ∎

So the rewritten program is exactly the original program run under the execution monitor of $A$, and everything proved on the [security automaton](/security-automaton/) page applies.

## Classic examples

- **[Software fault isolation](/software-fault-isolation/).** The policy is "every store and every indirect jump stays inside the sandbox region". The rewriter masks or checks each address before the instruction. This is an IRM with a one-state automaton, where the check is on the operand, and it also provides the PROTECT hole for richer IRMs on machine code. SASI for x86 used it for that purpose.
- **[Control-flow integrity](/control-flow-integrity/).** The policy is "each indirect jump goes to a target that the control flow graph allows". The rewriter inserts a check of the target label before each indirect jump. CFI is also the standard way to fill the PROTECT hole: it ensures that no jump skips a check.
- **[AddressSanitizer](/addresssanitizer/).** The compiler inserts a check of the shadow memory before each load and store, and the policy is "no access to a byte marked unaddressable". The automaton state is the shadow memory, which the allocator updates on each allocation and free.
- **[Stack canary](/stack-canary/) and [shadow stack](/shadow-stack/).** Code inserted at function entry and before each return checks the return. A stack canary checks that a value placed next to the saved return address is unchanged. A shadow stack checks the return address against a copy saved at entry; the shadow stack is the automaton state, a stack of return addresses kept where the program cannot write it.
- **A security automaton on Java bytecode.** The policy "no network send after a read of a secret file" has two states. The rewriter inserts a state update after each call that reads a secret file and a check before each call that sends. Type safety of the bytecode fills the PROTECT hole: the program cannot name the state field or jump into the inserted code.

## Variations

- **SASI (1999).** Erlingsson and Schneider wrote policies as security automata and built two rewriters, one for x86 assembly produced by a compiler and one for Java virtual machine language. On x86, memory protection of the automaton state came from software fault isolation; on JVML, from the type safety of the bytecode.
- **PoET and PSLang (2000).** A rewriter for Java whose policies are written in a Java-like policy language and refer to Java-level events such as method calls. They used it to implement Java stack inspection as an IRM, which made the security policy a part of the program rather than of the virtual machine.
- **Certified IRMs (2006).** Hamlen, Morrisett and Schneider gave a type system for .NET bytecode that checks that a rewritten program does carry its monitor correctly. A verifier then checks the output of the rewriter, so the rewriter itself is not in the trusted base. This is close in spirit to [proof-carrying code](/proof-carrying-code/).
- **Rewriting beyond halting.** An IRM may do more than stop the program: it may insert or suppress actions, as edit automata do. Hamlen, Morrisett and Schneider (2006) show that program rewriting can enforce policies that no execution monitor can, and that the class of policies it enforces does not correspond to any class of the arithmetical hierarchy.
- **Compiler-inserted checks.** Many sanitizers and hardening passes are IRMs without the name: the compiler fills EVENTS from its intermediate code and PE from its optimizer.

## Pitfalls

- **Tampering.** If any instruction of the original program can write the automaton state, the program can reset it and the guarantee is gone. On machine code this needs memory isolation of the state, not just a hidden address.
- **Skipped checks.** An indirect jump, a computed return or a jump into the middle of the inserted code can reach an event without its check. Without control-flow integrity, the PROTECT hole is open.
- **Missed events.** Code loaded or generated at run time, reflection, native calls and callbacks from the system can cause events that the rewriter never saw. Each must be blocked or routed through the rewriter.
- **Wrong level of events.** A policy about files written over machine instructions must recognize every way to open a file, including system calls made through unusual paths. A policy written over library calls trusts the library.
- **Time of check and time of use.** In a program with several threads, another thread can change the state or the data between the check and the event. The check and the event must be atomic with respect to the policy, or the state must be per thread.
- **Overhead.** Without partial evaluation, a check before every instruction is expensive. With it, the remaining cost depends on how many events the policy names.
- **Wrong class of policy.** An IRM that only halts cannot enforce availability or noninterference; trying to do so either blocks good programs or misses bad ones.

## Exercises

1. A program reads a secret file and then, in a loop, sends messages. The policy is "no send after a read". What does partial evaluation leave in the rewritten program? *Answer.* After the read, the state is known to be "tainted" on every path, so the check before the first send is known to fail. The rewriter can replace that send by HALT, and the checks inside the loop are never reached.
2. Why did SASI on x86 need software fault isolation, while SASI on JVML did not? *Answer.* An x86 program can store to any address and jump to any address, so it could overwrite the automaton state or skip a check. JVML is type safe: a program cannot forge a reference to the state field, and the verifier rejects jumps into the middle of the inserted code.
3. Can an IRM that only inserts checks and halts enforce "every file the program opens is eventually closed"? *Answer.* No. A run that opens a file and then runs forever without closing it violates the policy, but every finite prefix of it can still be extended by a close, so no prefix shows the violation. The policy is not a safety property, and by the theorem on execution monitors no halting monitor enforces it. A rewriter that inserts the missing close calls before each exit enforces it on the runs that terminate, but it then changes the program's behavior rather than only stopping it.
4. Show that the order of PE and PROTECT matters for a rewriter on machine code. *Answer.* If PE runs after PROTECT and removes a check that PROTECT assumed was there, a jump target that PROTECT allowed may reach an event without a check. PE must keep every check on which the protection argument relies, or PROTECT must run last, as in the template.

## References
