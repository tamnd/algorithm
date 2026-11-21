---
tag: 4X2QA6
kind: model
slug: chinese-wall-model
name: Chinese Wall model
aliases:
- Brewer-Nash model
area: security-and-privacy/access-control-and-information-flow
level: core
summary: A policy for conflicts of interest in which a subject who has read data of one company may not then read data of a competitor.
model: word-ram
prereqs: [bell-lapadula-model]
see_also: [bell-lapadula-model, clark-wilson-model, security-automaton, em-enforceable-policies-theorem, separation-of-duty, mandatory-access-control, denning-lattice-model, safety-property]
sources:
  - paper: doi:10.1109/SECPRI.1989.36295
    title: "David F. C. Brewer and Michael J. Nash, The Chinese Wall security policy, Proceedings of the 1989 IEEE Symposium on Security and Privacy, pages 206 to 214"
    locator: "company datasets and conflict of interest classes, the simple security rule, the *-property, sanitized information, and the theorems on the walls"
  - paper: doi:10.1109/CSAC.1989.81064
    title: "T. Y. Lin, Chinese wall security policy: an aggressive model, Proceedings of the Fifth Annual Computer Security Applications Conference, 1989, pages 282 to 289"
    locator: the conflict of interest relation as a binary relation that need not be transitive
  - paper: doi:10.1016/0167-4048(92)90131-A
    title: "Ravi S. Sandhu, Lattice-based enforcement of Chinese Walls, Computers and Security 11(8), 1992, pages 753 to 763"
    locator: the labels with one component per conflict of interest class and the reduction to a lattice-based policy
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 8, Hybrid Policies (the Chinese Wall model)"
---

The Chinese Wall model, given by Brewer and Nash in 1989, is a model of access control for conflicts of interest, as in a bank, a law firm or a consulting firm that works for competing clients. The data of each client company forms a *dataset*, and the datasets of competitors form a *conflict of interest class*. At first a subject may read anything. Once it has read the data of one company, it may no longer read the data of any competitor in the same class: a wall forms around what it has seen. A second rule on writing stops two subjects from moving data across the wall together. The model is the standard example of a *history-dependent* policy, in which the answer to a request depends on earlier accesses, not only on fixed labels.

## The machine

**Objects.** Each object $o$ belongs to one company dataset $y(o)$, and each dataset belongs to one conflict of interest (COI) class $x(o)$. The COI classes partition the datasets. A special class holds *sanitized* information, such as published reports, from which no company can be identified; it conflicts with nothing.

**State.** The state is the history matrix $N$, with $N[s, o] = \text{true}$ if subject $s$ has read object $o$. At the start $N$ is all false.

**Read rule** (simple security rule). Subject $s$ may read object $o$ if and only if, for every object $o'$ with $N[s, o'] = \text{true}$,

$$y(o') = y(o) \quad \text{or} \quad x(o') \neq x(o).$$

That is, $o$ is inside a dataset that $s$ has already read, or in a COI class from which $s$ has read nothing. If the read is granted, $N[s, o]$ becomes true.

**Write rule** (\*-property). Subject $s$ may write object $o$ if and only if $s$ may read $o$ by the read rule, and $s$ has read no object with unsanitized information in a dataset other than $y(o)$.

**Cost.** In the word RAM model, keep for each subject a hash map from COI class to the dataset it has read in that class, and one flag that says whether it has read unsanitized data from two or more datasets. The read rule is then one lookup, and the write rule one lookup and one test of the set of datasets read, so each request costs $O(1)$ expected time. The space is $O(c)$ per subject for $c$ COI classes.

## What it counts

The model decides, for each request and each history, whether the request is allowed. The adversary is an insider, such as an analyst who serves one client and wants to use what he knows to advise a competitor, and any program that runs for him and copies data. The model protects against him alone and against several insiders who pass data through objects. It does not protect against people who talk outside the system, and it does not cover [covert channels](/covert-channel/).

**Why the write rule is needed.** Without it, Alice reads Bank A and writes into an object of Oil X, which is allowed since banks and oil are different classes. Bob, who has read Bank B and Oil X, then reads that object and learns the data of Bank A. The write rule forbids Alice's write, because she has read unsanitized data of Bank A, a dataset other than Oil X. In effect, a subject that has read unsanitized data of two datasets may not write at all, and a subject that has read unsanitized data of one dataset may write only into that dataset.

**Example.** Take two COI classes, banks with Bank A and Bank B, and oil with Oil X and Oil Y, and one object of each: $o_A$, $o_B$, $o_X$, $o_Y$. A subject requests reads in this order.

| request | history before | answer | reason |
|---|---|---|---|
| read $o_A$ | none | yes | no earlier access |
| read $o_X$ | $o_A$ | yes | oil is another class |
| read $o_B$ | $o_A$, $o_X$ | no | Bank B conflicts with Bank A |
| read $o_Y$ | $o_A$, $o_X$ | no | Oil Y conflicts with Oil X |
| read $o_A$ | $o_A$, $o_X$ | yes | same dataset as before |
| write $o_A$ | $o_A$, $o_X$ | no | has read Oil X data |

A subject that has read only $o_A$ may write $o_A$.

## Relation to other models

- **Bell-LaPadula.** Brewer and Nash argued that the Chinese Wall policy cannot be modeled by a fixed assignment of [Bell-LaPadula](/bell-lapadula-model/) levels, since the access a subject gets depends on what it chose to read first. Their write rule plays the part of the \*-property.
- **Lattice labels.** Sandhu (1992) showed how to enforce it with lattice labels after all. A label is a vector with one entry per COI class, each entry either empty or one company of that class. The labels form a lattice, and the rules become the Bell-LaPadula rules on these labels, with a distinction between a human user and the sessions he runs. This connects the model to the [Denning lattice model](/denning-lattice-model/).
- **Security automata.** The state of one subject is a finite record of what it has read, and a request is denied as soon as the history plus the request breaks the rules. So the policy is a [safety property](/safety-property/) that a [security automaton](/security-automaton/) enforces, as the [EM-enforceable policies theorem](/em-enforceable-policies-theorem/) describes.
- **Clark-Wilson and separation of duty.** The [Clark-Wilson model](/clark-wilson-model/) is the other main commercial model. Both limit what one person can do, but [separation of duty](/separation-of-duty/) splits a task between people, while the Chinese Wall splits clients between people.
- **Mandatory access control.** The walls are set by the system, not by the owners of the data, so the policy is [mandatory](/mandatory-access-control/), but its labels change with the history of each subject.

## Known results in the model

Each item is a theorem of Brewer and Nash (1989) unless noted.

- **Theorem 1.** Once a subject has read an object, the only other objects it can read are in the same dataset or in a different COI class. This is the read rule restated for all later steps, since $N$ only grows.
- **Theorem 2.** A subject can read objects of at most one dataset in each COI class. The first read in a class fixes the dataset, and Theorem 1 excludes the others.
- **Theorem 3.** If a COI class has $X$ datasets, then at least $X$ subjects are needed for every object of the class to be read by some subject. By Theorem 2 each subject covers at most one dataset of the class. So a firm with $X$ competing clients in one market needs at least $X$ analysts for that market.
- **Flow of unsanitized data.** Under the read and write rules, unsanitized information can flow only within its own dataset, while sanitized information can flow freely. The proof is that each write moves data from the datasets the writer has read into the dataset of the object, and the write rule allows this only if the writer has read unsanitized data of at most that one dataset.
- **Non-transitive conflicts** (Lin 1989). The model assumes that conflict is an equivalence relation, so that the classes partition the datasets. Lin argued that in practice conflict is a symmetric relation that need not be transitive: A may compete with B and B with C while A does not compete with C. He gave a variant in which the read rule uses the binary relation directly. If the read rule denies $o$ whenever the subject has read a dataset in conflict with $y(o)$, the analogue of Theorem 2 says that the datasets one subject reads form an independent set of the conflict graph.

## References
