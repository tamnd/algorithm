---
tag: E75547
kind: problem
slug: confinement-problem
name: Confinement problem
aliases:
- Lampson confinement problem
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Run a borrowed program so that it cannot pass the data it reads to anyone but its caller, through storage, timing or any other channel.
prereqs: [covert-channel, noninterference]
see_also: [shared-resource-matrix, security-type-system, self-composition, secure-multi-execution, rice-theorem, software-fault-isolation, constant-time-programming, quantitative-information-flow]
sources:
  - paper: doi:10.1145/362375.362389
    title: Butler W. Lampson, A note on the confinement problem, Communications of the ACM 16(10), 1973
    locator: pp. 613 to 615; the customer and service setting, the leaks numbered 0 to 6, the three kinds of channel, and the rules of total isolation, transitivity, masking and enforcement
  - paper: doi:10.1109/SP.1982.10014
    title: Joseph A. Goguen and Jose Meseguer, Security policies and security models, Proceedings of the 1982 IEEE Symposium on Security and Privacy
    locator: pp. 11 to 20, noninterference as the statement that one group's actions have no effect on what another group sees
  - paper: doi:10.1145/357369.357374
    title: Richard A. Kemmerer, Shared resource matrix methodology, an approach to identifying storage and timing channels, ACM Transactions on Computer Systems 1(3), 1983
    locator: pp. 256 to 277, a method to find the candidate channels of a design
  - paper: doi:10.1109/RISP.1991.130770
    title: Phillip A. Porras and Richard A. Kemmerer, Covert flow trees, a technique for identifying and analyzing covert storage channels, Proceedings of the 1991 IEEE Symposium on Security and Privacy
    locator: pp. 36 to 51, covert flow trees
  - book: isbn:9780321712332
    title: Matt Bishop, Computer Security, Art and Science, second edition, Addison-Wesley, 2018
    locator: Chapter 18 (The Confinement Problem)
---

The confinement problem asks how to run a program that someone else wrote on your data so that the program cannot pass the data to anyone but you. Butler Lampson posed it in 1973. He called the caller the customer and the borrowed program the service: the customer can check that the service does not read files it was not given, but the service may still leak, that is, send the customer's input to its owner. A leak leaves no trace, unlike a wrong answer. Lampson listed the paths a service could use, from a file it writes to its effect on the system load, and gave rules that are sufficient to block them. The problem is the origin of the [covert channel](/covert-channel/) and, in modern form, the question of whether a program satisfies [noninterference](/noninterference/) towards every observer except its caller.

## In plain words

You hire a tax program from a company you do not trust. You give it your income and it gives you back a tax figure. You can stop it from opening your other files. But the program could also save your income in a file its owner reads later, send it in a message, hide it in the bill it charges you, or make the machine slow or fast in a pattern that another program of the owner can watch. The confinement problem asks for a way to run the program so that none of these paths works. Ordinary access control blocks the first few. The last ones use things that were never meant to carry messages, so they are hard to find and hard to block.

## Definition

**Setting.** A system runs a service program $S$ on behalf of a customer. The customer gives $S$ an input $d$, which may include secret data, and receives a result through a legitimate channel, for example the result value and the bill. Other subjects, including programs of the owner of $S$, run on the same system and observe what the system lets them observe: shared storage, the results of their own calls, and the times at which things happen.

**Adversary.** The owner of $S$ wrote it and may have put any code in it; $S$ is the sender. The owner also controls other subjects on the system, which act as receivers and see every observation the model gives them. The supervisor (the operating system or the runtime) is trusted.

**Input.** The system and its observable state, the service $S$, and a statement of which outputs are legitimate for the customer.

**Output.** A way to run $S$, or a proof about a given way to run it, such that $S$ is **confined**: for any two customer inputs $d$ and $d'$ that agree on what the customer chooses to release, every other subject sees the same observations, or the same distribution of observations if the system is probabilistic. This is noninterference from the customer's input to every observer except the customer.

**What counts as an observation.** The answer depends on the model. A model with storage only lets observers read values. A model with time also lets them read when events happen. A program can be confined in the first model and leak in the second, so every confinement claim must name its model.

**Lampson's rules.** Lampson first asks that a confined program be memoryless: it must not keep information from one call to the next. Then he gives four rules.
1. *Total isolation.* A confined program makes no calls on any other program, where a call is any transfer of control the program causes. This is sufficient but impractical, since even input, output, paging and time-slicing are implicit calls to the supervisor.
2. *Transitivity.* If a confined program calls another program which is not trusted, the called program must also be confined.
3. *Masking.* A program to be confined must allow its caller to determine all its inputs into legitimate and covert channels. For the bill, the customer fixes the price in advance, as with a purchase order.
4. *Enforcement.* The supervisor must ensure that a confined program's input to covert channels conforms to the caller's specifications, for example by slowing the program down or adding dummy disk references.

Lampson notes that enforcement may cost a lot, and that a cheaper option, when the customer accepts some leakage, is to bound the capacity of the covert channels.

## Variants

- **Storage only.** The observers read only values. This is the version that access control, capability systems and the [shared resource matrix](/shared-resource-matrix/) address most directly.
- **With timing.** The observers can measure time, so the running time and the resource use of $S$ must not depend on $d$. This is the version of [constant-time programming](/constant-time-programming/) and of cache partitioning.
- **Bounded leakage.** Instead of zero, ask that the leakage to other observers be at most $b$ bits, or at most $b$ bits per second, under a stated measure from [quantitative information flow](/quantitative-information-flow/). Lampson's capacity bound is this variant.
- **Termination and progress.** Whether an observer may learn that $S$ stopped or how far it got. [Termination-insensitive noninterference](/termination-insensitive-noninterference/) allows this leak.
- **Declassification.** The customer allows some function of $d$ to be released, for example an aggregate. The definition then compares only inputs with the same released value.

## Examples

**Lampson's leaks.** His examples are, in order: a service with memory that waits for its owner to call it; a permanent file in the owner's directory; a temporary file that the owner tests for at intervals; a message by interprocess communication; the bill, and the amount of resources used if the owner pays for them; a file interlock, where a file that cannot be open for reading and writing at once acts as a shared Boolean, an example he credits to A. G. Fraser; and the effect of the service on system performance, which a concurrent process can watch. Lampson says that all of them except the bill and the system performance use storage channels. The bill is a legitimate channel, and the effect on performance is his covert channel.

**Blocking the interlock.** Lampson's fix for the interlock example: if someone tries to write a file that a confined program is reading, give the confined program a copy and let the writer go on, so that the writer receives no sign that the file was being read. The attribute "is open for reading" is no longer visible to the writer.

**A small program.** Let the service compute a result $r = f(d)$ for the customer and then run `if d > 0 then lock(F)` on a file $F$ that a receiver can also try to lock. The result channel is legitimate. The lock state is not, and a receiver that tries the lock after each call learns the sign of $d$. The service is not confined. Any of three changes makes it confined in the storage model: the supervisor gives each subject its own view of the lock state of $F$, the lock call is removed, or the analysis proves that the branch does not depend on $d$. In a model with time, the branch must also not change the running time.

## Known algorithms

There is no algorithm that decides confinement for every program (see Bounds). The methods below either build a system in which a class of channels does not exist, or check a sufficient condition.
- **Isolation by design.** Separate machines, a separation kernel that gives each partition its own resources and a fixed schedule, or a capability system that gives the service no capability to write outside. These remove channels through storage by construction. Fixed time slices and partitioned caches remove timing channels at a cost in throughput.
- **Design analysis.** The [shared resource matrix](/shared-resource-matrix/) lists the attributes that each operation references and modifies and keeps the attributes that a sender can modify and a receiver can sense; covert flow trees (Porras and Kemmerer, 1991) trace how a modification can reach an observation. Both find candidates in a specification, which an analyst then confirms or rejects.
- **Information flow analysis of code.** A [security type system](/security-type-system/) proves noninterference for programs that type-check. [Self-composition](/self-composition/) reduces noninterference of a program to a safety property of two copies of it run side by side, which a program verifier can then check.
- **Run-time methods.** [Secure multi-execution](/secure-multi-execution/) runs one copy of the program per security level, so that the low copy never sees high inputs. [Software fault isolation](/software-fault-isolation/) confines the memory accesses of untrusted code inside one process, which blocks storage paths through memory but not timing.
- **Timing.** [Constant-time programming](/constant-time-programming/) removes the dependence of running time on secrets for code that follows its rules. Padding to a fixed time and adding noise lower the capacity of what remains.
- **Measurement.** When a channel cannot be closed, its capacity is estimated or bounded, as in Lampson's cheaper option and in the TCSEC guideline on covert channels.

## Bounds

- **Undecidable in general (theorem).** Whether an arbitrary program is confined is undecidable, already in a storage model where observers see neither termination nor time. Reduction from the [halting problem](/halting-problem/): given a machine $M$ and an input $w$, let the service simulate $M$ on $w$ and, if the simulation stops, write $d$ to a file that a receiver can read. The service is confined if and only if $M$ does not halt on $w$. Confinement is a nontrivial property of the program's behavior, so [Rice's theorem](/rice-theorem/) gives the same result.
- **Sound methods reject some confined programs (theorem).** A method that always stops and never accepts a leaking program must reject some confined programs, by the result above. Type systems, for example, reject `if d > 0 then x := 1 else x := 1`.
- **Complete enumeration is not expected (heuristic).** Lampson wrote that there is not likely to be any rigorous way of identifying every channel in any system of even moderate complexity. Each design analysis is only as complete as its list of shared attributes and its model of time.
- **Noise does not close a channel (theorem).** By Shannon's coding theorem, a memoryless noisy channel with positive capacity carries information reliably at any rate below its capacity. Lampson made this point for the load channel: coding works however small the effect is, provided it is not zero.

## Reductions

- **Confinement is noninterference.** With the customer's input labeled high and every other observer labeled low, a service is confined exactly when it is noninterferent in the chosen observation model. All methods for noninterference apply.
- **Noninterference is a hyperproperty.** It compares two runs, so it is not a safety property of single runs, and an execution monitor that watches one run cannot enforce it alone; see the [theorem on execution monitors](/em-enforceable-policies-theorem/). Self-composition turns it back into a safety property of a product program.
- **From halting.** The reduction in Bounds shows that the problem is at least as hard as halting.
- **To the shared resource matrix.** For a system given as operations on shared attributes, every channel through storage between two subjects uses an attribute that some operation modifies and some operation references, possibly through indirect references. Given a complete table of references and modifications, the matrix method lists every such attribute. This is a necessary condition, not a sufficient one, so the list may include false alarms; and a table built from an informal specification may be incomplete.

## Applications

- **Multilevel secure operating systems.** A process at a high level is a service that must be confined with respect to the low levels. The TCSEC classes B2 and above required a covert channel analysis.
- **Sandboxes and plug-ins.** A browser, a mobile platform or a server runs code it did not write; confinement of storage paths is the goal of its sandbox.
- **Shared hardware.** Tenants of one cloud server share caches and memory buses, so confinement there means also bounding timing channels.
- **Proprietary services.** Lampson's original case: a customer uses a service whose owner wants to keep the program secret, and the customer wants to keep the data secret. Both sides need protection.

## References
