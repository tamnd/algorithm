---
tag: F0ZBYY
kind: concept
slug: reference-monitor
name: Reference monitor
aliases:
- security kernel
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: A component that mediates every access of a subject to an object, cannot be tampered with, and is small enough to be verified.
see_also: [inline-reference-monitor, security-automaton, em-enforceable-policies-theorem, access-control-matrix, mandatory-access-control, safety-property, noninterference, principle-of-least-privilege]
sources:
  - paper: "James P. Anderson, Computer Security Technology Planning Study, ESD-TR-73-51, Electronic Systems Division, US Air Force, October 1972"
    locator: the reference monitor concept and the three requirements on the mechanism that validates each reference
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section I (the design principles of complete mediation, economy of mechanism and fail-safe defaults)
  - paper: "Department of Defense, Trusted Computer System Evaluation Criteria, DoD 5200.28-STD, December 1985"
    locator: Section 3.3 (class B3, whose trusted computing base must meet the reference monitor requirements) and the glossary entry for the trusted computing base
  - paper: doi:10.1145/353323.353382
    title: Fred B. Schneider, Enforceable security policies, ACM Transactions on Information and System Security 3(1), 2000
    locator: pages 30 to 50 (execution monitors, security automata, and the policies that a monitor can enforce)
---

A reference monitor is the part of a system that receives every request of a subject to use an object, decides it by the policy, and lets it through or stops it. Anderson's report for the US Air Force (1972) set three requirements for the mechanism that implements it: it must be always invoked, so no access can bypass it; it must be tamperproof, so the subjects it controls cannot change it; and it must be small enough to be analyzed and tested so that one can be sure it is correct. The [access control matrix](/access-control-matrix/) and its forms say what the policy is; the reference monitor is where the policy is applied. The concept is distinct from two close pages: an [inline reference monitor](/inline-reference-monitor/) is a technique that puts the checks into the program itself by rewriting it, and a [security automaton](/security-automaton/) is the formal model of what any monitor of this kind can enforce.

## In plain words

Picture a building with one guarded entrance. Every visitor, every time, passes the guard, who checks the visitor's pass against the rules. There is no back door, no window that opens, and no way for a visitor to send the guard home or rewrite the rules.

For this to work, three things must be true. The guard must see everyone, so all other ways in are sealed. Nobody the guard checks may be able to bribe, trick or replace the guard. And the guard's rule book must be short enough that someone can read it all and be sure it says what it should. If any of the three fails, the rules on paper do not protect the building.

## The idea

**Mediation.** Model a running system as a sequence of requests $(s, o, r)$. A reference monitor sits between the subjects and the objects. For each request it computes the decision of the policy, for example $r \in A[s, o]$ in the matrix or the label test of [mandatory access control](/mandatory-access-control/), and then either performs the access or refuses it. It may also write an audit record. Complete mediation, in the words of Saltzer and Schroeder, means that every access to every object is checked; a check made once and then cached is a weaker thing, because the policy may have changed since.

**The three requirements.**

1. **Always invoked.** There is no path to an object that does not go through the monitor. In an operating system this means that user programs have no direct access to devices, memory of other processes or kernel data, and the hardware enforces this with privileged modes and memory protection.
2. **Tamperproof.** The code and data of the monitor, including the policy, are protected from the subjects that it controls. Only the trusted administrator changes the policy, through a path that the monitor itself checks.
3. **Verifiable.** The monitor is small and simple enough for analysis and tests, ideally a formal proof, to show that it applies the policy correctly. This is economy of mechanism applied to the most critical code.

The trusted computing base of the TCSEC (1985) is the set of all parts of a system that the security of the system depends on, and from class B3 up it must meet these three requirements: mediate all accesses of subjects to objects, be tamperproof, and be small enough to be subjected to analysis and tests.

**What a monitor can enforce.** A monitor sees one run of the system, one request at a time, and its only power is to stop a request. Schneider (2000) made this precise with [security automata](/security-automaton/): a policy is enforceable by such an execution monitor only if it is a [safety property](/safety-property/), one whose violations show up in a finite prefix of the run; see the [EM-enforceable policies theorem](/em-enforceable-policies-theorem/). Access control policies are safety properties, so a monitor can enforce them. Information flow policies such as [noninterference](/noninterference/) are not properties of single runs at all, so no reference monitor alone can enforce them; they need static analysis or a system with more power than stopping a request.

## Examples

- **File access in an operating system.** A process asks the kernel to open a file for writing. The kernel looks up the [access control list](/access-control-list/) of the file, checks the user of the process, and returns a handle or an error. The process cannot touch the disk except through the kernel, because the hardware stops it. Most systems check at open and not at each write, so the handle works as a cached decision: after a revoke, an open handle still works until it is closed.
- **Mandatory labels.** In a system with [mandatory access control](/mandatory-access-control/), the same kernel path also compares the labels of the process and the file. Linux places hooks at each point where the kernel accesses an object, and a security module such as SELinux decides at each hook.
- **A web browser.** The browser mediates every access of a script to the content of another page and applies the [same-origin policy](/same-origin-policy/). A flaw that lets a script reach another origin by a path the browser does not check breaks the first requirement.
- **Time of check to time of use.** A program checks that a file name points to a file the user may write, and then opens the name. Between the two steps an attacker replaces the file with a link to another file. The check and the use refer to different objects, so the access was never mediated. The fix is to check and use in one step inside the monitor.

## Where it is used

Every operating system kernel and hypervisor acts as a reference monitor for the processes or virtual machines above it. Small kernels follow the third requirement: seL4 is a microkernel whose implementation has a formal proof of correctness, and its access control is by [capabilities](/capability-list/). The concept is the basis of the evaluation criteria of the TCSEC and of later criteria, which ask how well a product meets the three requirements. Outside the kernel, the same idea appears in database engines that check each query, in API gateways that check each call, in [inline reference monitors](/inline-reference-monitor/) that put checks into untrusted code, and in [software fault isolation](/software-fault-isolation/). Combined with the [principle of least privilege](/principle-of-least-privilege/), a monitor limits each subject to the rights that its task needs and makes sure that it uses no others.

## References
