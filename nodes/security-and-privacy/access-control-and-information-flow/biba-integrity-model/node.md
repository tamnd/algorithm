---
tag: CA2FF8
kind: model
slug: biba-integrity-model
name: Biba integrity model
aliases:
- Biba model
- no read down no write up
area: security-and-privacy/access-control-and-information-flow
level: core
summary: The dual of Bell-LaPadula for integrity, in which a subject may not read less trusted data nor write to more trusted objects.
model: word-ram
prereqs: [bell-lapadula-model]
see_also: [bell-lapadula-model, clark-wilson-model, mandatory-access-control, denning-lattice-model, join-semilattice, noninterference, reference-monitor, chinese-wall-model]
sources:
  - url: "https://apps.dtic.mil/sti/tr/pdf/ADA039324.pdf"
    title: "K. J. Biba, Integrity Considerations for Secure Computer Systems, MITRE MTR-3153 Rev. 1 (ESD-TR-76-372), April 1977"
    locator: "the access modes observe, modify and invoke; the mandatory integrity policies: the low-water mark policy, the ring policy and the strict integrity policy (p. 32)"
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 6, Integrity Policies (the Biba integrity model and Lipner's integrity matrix model)"
  - book: isbn:9781119642787
    title: "Ross Anderson, Security Engineering, third edition, Wiley, 2020"
    locator: "Chapter 9, Multilevel Security"
---

The Biba integrity model is a mandatory model of integrity, the dual of the [Bell-LaPadula model](/bell-lapadula-model/) for confidentiality. Each subject and object has an integrity level that says how much it is trusted. A subject may not observe an object that is less trusted than itself ("no read down"), and it may not modify an object that is more trusted than itself ("no write up"). Together the two rules stop data from a low-integrity source, such as a file from the network, from reaching a high-integrity object, such as a system program, through any chain of reads and writes. K. J. Biba wrote the model at MITRE in 1975 to 1977. His report gives several policies, of which the *strict integrity policy* is the one usually called the Biba model.

## The machine

**Levels.** A finite lattice $I$ of integrity levels, for example a total order of trust and a set of categories, as in Bell-LaPadula. Each subject $s$ has a level $i(s)$ and each object $o$ a level $i(o)$.

**Order used on this page.** This page writes the order in the direction of allowed flow, as the other information flow pages do: $\ell_1 \sqsubseteq \ell_2$ means that data may flow from $\ell_1$ to $\ell_2$, so $\ell_1$ is at least as trusted as $\ell_2$. The most trusted level is the bottom. Biba writes the order the other way, with $\le$ from less to more trusted; read each $\ell_1 \sqsubseteq \ell_2$ here as $\ell_2 \le \ell_1$ in the report. The join $\ell_1 \sqcup \ell_2$ is then the most trusted level that is no more trusted than either, which Biba calls the minimum (the "low-water mark").

**Access modes.** There are three:

- *observe*: $s$ reads $o$, a flow from $o$ to $s$;
- *modify*: $s$ writes $o$, a flow from $s$ to $o$;
- *invoke*: $s_1$ calls $s_2$, a flow from $s_1$ to $s_2$.

**State and steps.** A state gives the levels and the current accesses. A step is a request for one access, which the policy allows or denies. In some policies a step also changes a level.

**Cost.** In the word RAM model, a test $\ell_1 \sqsubseteq \ell_2$ on a total order of trust and a bit set of $c$ categories costs $O(1 + c/w)$ for word size $w$, and so does a join. Every rule below is one or two such tests.

## What it counts

The model decides whether each requested access is allowed. A run is *integrity-safe* if no information moves from an object $o_1$ to an object $o_2$ unless $i(o_1) \sqsubseteq i(o_2)$, along the chains of observe, modify and invoke steps that the model sees. The adversary is an untrusted subject, or untrusted data, that tries to change a trusted object: directly, by writing it, or indirectly, by feeding data to a trusted subject that then writes it.

**Strict integrity policy** (Biba 1977). In the order of this page:

1. *Simple integrity property.* $s$ may observe $o$ only if $i(o) \sqsubseteq i(s)$: no read down in trust.
2. *Integrity \*-property.* $s$ may modify $o$ only if $i(s) \sqsubseteq i(o)$: no write up in trust.
3. *Invocation property.* $s_1$ may invoke $s_2$ only if $i(s_1) \sqsubseteq i(s_2)$.

Levels never change under the strict policy.

**Low-water mark policy for subjects.** $s$ may observe any object, and then its level becomes $i(s) \sqcup i(o)$: a subject that reads untrusted data becomes untrusted. Modify and invoke follow the strict rules for the current level. Levels of subjects only move up in the order of this page, so a long session can end at the least trusted level, after which it can modify almost nothing.

**Low-water mark policy for objects.** $s$ may modify any object, and then the level of the object becomes $i(o) \sqcup i(s)$. The data is not protected, but its label never claims more trust than its history earns.

**Ring policy.** $s$ may observe any object, and the modify and invoke rules are the strict ones. Indirect flows through a subject are not stopped: the subject itself is trusted to check what it reads.

**Example.** Take the levels system $\sqsubseteq$ user $\sqsubseteq$ web, with system the most trusted. A user process may observe system files, since system $\sqsubseteq$ user, but under the strict policy it may not observe a web download. It may modify user files and web-level files, but not system files. An installer at level system that wants to read a web download is denied under the strict policy. Under the low-water mark policy it may read it, but its level becomes web, and from then on it can no longer modify system files.

## Relation to other models

- **Bell-LaPadula.** The strict integrity policy is the simple security property and the \*-property of [Bell-LaPadula](/bell-lapadula-model/) with the order of the lattice reversed and with no trusted subjects. Bell-LaPadula keeps secret data from flowing down; Biba keeps untrusted data from flowing up in trust.
- **Lattice flow models.** In the order of this page both models are the rule "information flows only up the lattice" of the [Denning lattice model](/denning-lattice-model/). The low-water mark policies compute the label of a subject as a join, which is the same as the label of a program variable in Denning's model. The levels form a [join-semilattice](/join-semilattice/) under $\sqcup$.
- **Clark-Wilson.** The [Clark-Wilson model](/clark-wilson-model/) treats integrity as correct, well-formed change by certified programs and separation of duty, not as a level. Clark and Wilson argued that commercial integrity does not fit a lattice of trust.
- **Mandatory access control.** Biba is a [mandatory](/mandatory-access-control/) policy: the levels are set by the system, not by owners. Operating systems use integrity levels with a no-write-up rule, close to the ring policy, to keep low-trust processes from changing system files.
- **Noninterference.** Integrity is the dual of confidentiality also in the sense of [noninterference](/noninterference/): the low-integrity inputs must not affect the high-integrity outputs.

## Known results in the model

- **Transitivity** (theorem). Under the strict policy, if a chain of observe, modify and invoke steps moves information from object $o_1$ to object $o_2$, then $i(o_1) \sqsubseteq i(o_2)$. Each step of the chain is a flow from one entity to the next that the rules allow only up the order, and $\sqsubseteq$ is transitive. The same holds for the low-water mark policy for subjects, with the level of each subject taken at the time of the step.
- **Duality** (theorem). Map each integrity level to the same element of the dual lattice. Then a request is allowed by the strict integrity policy if and only if Bell-LaPadula with the reversed order and no trusted subjects allows the matching read or write. So the [basic security theorem](/basic-security-theorem/) and its proof carry over.
- **One label for both** (theorem). If a system uses one label as both the confidentiality level and the integrity level, with "higher" meaning both more secret and more trusted, then reading needs the object level to be at most and at least the subject level, so reading is allowed only at equal levels, and the same holds for writing. This is why systems that need both use two separate labels, as in the integrity matrix model of Lipner (1982), treated in Bishop, Chapter 6.
- **Label creep** (heuristic). Under the low-water mark policies, levels only move toward the least trusted level, so in long runs most subjects or objects end there. This is the main reason that the strict and ring policies are used more in practice.
- **What the model does not cover.** A label says how much a source is trusted, not that the data is correct. A trusted subject that computes a wrong value writes it with full trust. Covert flows of the kind discussed for [Bell-LaPadula](/bell-lapadula-model/) are also outside the model.

## References
