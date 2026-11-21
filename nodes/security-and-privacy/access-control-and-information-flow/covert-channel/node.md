---
tag: EADC3V
kind: concept
slug: covert-channel
name: Covert channel
aliases:
- storage channel
- timing channel
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: A path that carries information between processes through a resource not meant for communication, such as a lock, a file name or a delay.
history:
  year: 1973
  people: [Butler W. Lampson, Richard A. Kemmerer, Jonathan K. Millen]
  note: Lampson named covert channels in his 1973 note on confinement. Kemmerer gave a method to find them in 1982 and 1983, and Millen measured their capacity with information theory in 1987.
prereqs: [mandatory-access-control]
see_also: [confinement-problem, shared-resource-matrix, side-channel-attack, timing-attack, noninterference, quantitative-information-flow, bell-lapadula-model, constant-time-programming]
sources:
  - paper: doi:10.1145/362375.362389
    title: Butler W. Lampson, A note on the confinement problem, Communications of the ACM 16(10), 1973
    locator: pp. 613 to 615, the list of leaks numbered 0 to 6, the three kinds of channel (storage, legitimate and covert) and the confinement rules
  - paper: doi:10.1145/357369.357374
    title: Richard A. Kemmerer, Shared resource matrix methodology, an approach to identifying storage and timing channels, ACM Transactions on Computer Systems 1(3), 1983
    locator: pp. 256 to 277, the conditions for a channel through a shared attribute and the matrix method to find them
  - paper: doi:10.1109/SP.1987.10013
    title: Jonathan K. Millen, Covert channel capacity, Proceedings of the 1987 IEEE Symposium on Security and Privacy
    locator: the capacity of a covert channel in the sense of Shannon's information theory
  - paper: "Department of Defense, Trusted Computer System Evaluation Criteria, DoD 5200.28-STD, December 1985"
    locator: Part II, Section 8, A guideline on covert channels (the definitions of the two kinds, the bandwidth of 100 bits per second called high, the 1 bit per second called acceptable in most environments, and the audit of channels above 1 bit in 10 seconds)
  - paper: doi:10.1109/CSAC.2002.1176284
    title: Richard A. Kemmerer, A practical approach to identifying storage and timing channels, twenty years later, Proceedings of ACSAC 2002
    locator: pp. 109 to 118, Section 4 (the results on a secure network front-end)
  - book: isbn:9780321712332
    title: Matt Bishop, Computer Security, Art and Science, second edition, Addison-Wesley, 2018
    locator: Chapter 18 (The Confinement Problem), Section 18.3 on covert channels
---

A covert channel is a way for one process to send information to another through something that was never meant to carry messages: a lock on a file, the existence of a file name, the fullness of a disk, or how long an operation takes. The access control of the system may be perfect for every object it knows about and still let information through such a resource. Butler Lampson named the idea in 1973, in his note on the [confinement problem](/confinement-problem/): a program borrowed from someone else must not be able to pass its caller's data out, and covert channels are the paths that the system does not even treat as channels. Covert channels matter most in multilevel systems, where a high-level process must not signal to a low-level one, and in shared hardware such as cloud servers.

## In plain words

Two prisoners may not talk, but they share a light switch in the corridor. One flips it on or off every minute, and the other looks at it. Each minute carries one bit. No rule on letters or visits stops this, because the switch is not a letter. A computer has many such switches: whether a file is locked, whether a name is taken, how full a queue is, how busy the processor is. A covert channel needs a sender that wants to signal, usually a Trojan horse inside a trusted program, and a receiver that watches the shared thing. Closing every such path is very hard, so in practice systems find them, measure how many bits per second they carry, and make that rate small.

## The idea

**Definition.** A covert channel is a communication path between two subjects that the security policy does not allow, and that uses a resource whose purpose is not communication. Lampson (1973) distinguished three kinds of channel out of a confined program: storage that the program can write and another party can later read, such as a file; legitimate channels, such as the bill that the program returns with its result; and covert channels, which are not intended for information transfer at all. His covert example is the service's effect on the system load; a file interlock that a reader can test, an example he credits to A. G. Fraser, he counts as storage. The TCSEC (1985) later called both kinds covert channels, and most later work follows it:
- **Through storage.** One process writes a storage location, directly or indirectly, and another reads it. The location may be an attribute the system keeps for its own use, such as a lock bit, a file's existence, a quota counter or an error code. The receiver reads a value.
- **Through timing.** One process changes its own use of a resource, such as processor time, so that the response time seen by the other process changes. The receiver reads a time. A timing channel needs a clock, but any regular event, such as the progress of a third process, can serve as one.

**Conditions.** Kemmerer (1983) stated what a channel through a shared attribute needs: the sender and the receiver must have access to the same attribute, the sender must be able to change it, the receiver must be able to sense the change, and there must be a way to start the exchange and to put the events in order. A timing channel also needs a shared time reference. The [shared resource matrix](/shared-resource-matrix/) method lists, for each operation, which attributes it references and which it modifies, and keeps the attributes that both kinds of operation touch. Each such attribute is a candidate, which the analyst must then confirm or reject.

**Covert channel and side channel.** In a covert channel both ends cooperate: the sender wants to signal. In a [side channel](/side-channel-attack/) the victim does not cooperate, and the attacker learns a secret from what the victim's normal work does to time, power or a cache, as in a [timing attack](/timing-attack/). The physical mechanism can be the same. The difference is the threat model, and it changes the bandwidth: a cooperating sender can use coding to send more bits per second through the same noise.

**Capacity.** A covert channel is a communication channel in the sense of information theory, often a noisy one with memory. Lampson already noted that coding can get information reliably through a noisy load channel as long as the effect is not zero, and that a cheaper alternative to closing a channel is to bound its capacity. Millen (1987) applied Shannon's notion of channel capacity to covert channels. The capacity is the largest rate, in bits per use or per second, at which the sender and the receiver can communicate with a small error probability. For a memoryless channel, Shannon's coding theorem says that coding can reach any rate below the capacity, so a noisy channel is not a safe one. [Quantitative information flow](/quantitative-information-flow/) gives a second view: the [min-capacity](/min-entropy-leakage-bound/) of one use of the channel bounds how much one observation helps a receiver that must guess a value in one try.

**Defenses.** Each defense removes one of the conditions above, or lowers the capacity.
- *Remove the shared resource.* Give each security level its own copy of the resource: separate quotas, separate name spaces, static partitions of a cache or a disk. Then the sender cannot change what the receiver senses.
- *Make the attribute look the same.* The system can report a fixed or random answer to a low-level process, for example "the file does not exist" for every high-level file name. [Noninterference](/noninterference/) is the formal goal: low-level observations do not depend on high-level actions.
- *Remove the clock or add noise.* Coarse or randomized time sources and random delays make timing harder to read. They lower the capacity but do not remove the channel, and they cost performance.
- *Limit and audit.* The TCSEC guideline calls a bandwidth above 100 bits per second high, calls channels below 1 bit per second acceptable in most environments, and asks that the system audit the use of channels that may exceed 1 bit in 10 seconds. These are policy thresholds, not theorems.
- *Analyze the design.* The shared resource matrix, covert flow trees and information flow analysis find candidate channels in a specification or in code. The analysis is only as complete as the list of attributes it starts from.

## Examples

**A lock bit.** A high-level process H and a low-level process L share a file that either may try to lock; the system tells a process whether its lock request succeeded, but not who holds the lock. In each time slot, H locks the file to send 1 and leaves it free to send 0. L then tries to lock the file, notes success or failure, and releases it. This is a channel through storage: the attribute is "locked", H modifies it, and L senses it through the result of its own request. Without noise and with agreed time slots it carries one bit per slot. The defense is to give each level its own view of the lock state, or to report a constant result to L for objects of a higher level.

**A full disk.** H fills or frees a shared disk; L tries to create a file and sees whether the system says "no space". The attribute is the free space. Separate quotas per level remove the channel.

**A busy processor.** H runs a loop for a whole time slot to send 1 and sleeps to send 0. L counts how much work it gets done in each slot. This is a timing channel. Fixed time slices per level, as in a scheduler that does not give unused time to other levels, remove it at a cost in throughput.

**A noisy channel.** Suppose L reads each of H's bits correctly with probability 0.9 and wrongly with probability 0.1, independently: a [binary symmetric channel](/binary-symmetric-channel/). Its Shannon capacity is $1 - H(0.1) = 0.531$ bits per use, so with coding H can still send about half a bit per slot reliably. Its min-capacity is $\log_2 1.8 = 0.848$ bits per use. With 1000 slots per second, the capacity is about 531 bits per second, which is high by the TCSEC threshold.

**A measurement.** Kemmerer (2002) reports that the matrix method, applied to the design of a secure network front-end, found channels whose worst-case bandwidth was estimated at 5000 bits per second and a typical channel at 20 bits per second. The real bandwidths were lower because of noise, and the front-end was redesigned. These are estimates for one system, not general figures.

## Where it is used

- **Multilevel secure systems.** The higher TCSEC classes required a covert channel analysis: of channels through storage at B2, and of timing channels as well at B3 and A1.
- **Confinement.** A system that runs untrusted code on sensitive data, such as a sandbox or a separation kernel, must bound the covert channels between the code and the outside world; this is the [confinement problem](/confinement-problem/).
- **Shared hardware.** Virtual machines on one server share caches, memory buses and power management, and research has shown covert channels between them. Partitioning, [constant-time programming](/constant-time-programming/) and scheduler isolation are the defenses.
- **Policy models.** The [Bell-LaPadula model](/bell-lapadula-model/) controls reads and writes of named objects and says nothing about covert channels, which is why systems built on it also need a covert channel analysis.

## References
