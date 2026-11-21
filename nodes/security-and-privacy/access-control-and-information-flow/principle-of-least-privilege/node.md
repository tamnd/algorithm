---
tag: 8M4DNC
kind: concept
slug: principle-of-least-privilege
name: Principle of least privilege
aliases:
- least privilege
- least authority
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: The design rule that each program and user gets only the rights it needs for its task, so that a fault or a compromise does the least harm.
see_also: [capability-list, role-based-access-control, separation-of-duty, reference-monitor, software-fault-isolation, access-control-matrix, set-cover]
sources:
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section I (the eight design principles, among them least privilege, fail-safe defaults, complete mediation and separation of privilege)
  - paper: doi:10.1145/54289.871709
    title: Norm Hardy, The confused deputy, or why capabilities might have been invented, ACM SIGOPS Operating Systems Review 22(4), 1988
    locator: pages 36 to 38 (a program that uses the wrong one of its authorities)
  - paper: doi:10.1145/365230.365252
    title: Jack B. Dennis and Earl C. Van Horn, Programming semantics for multiprogrammed computations, Communications of the ACM 9(3), 1966
    locator: pages 143 to 155 (each computation runs with its own list of capabilities)
  - paper: doi:10.1109/2.485845
    title: Ravi S. Sandhu, Edward J. Coyne, Hal L. Feinstein and Charles E. Youman, Role-based access control models, IEEE Computer 29(2), 1996
    locator: pages 38 to 47 (sessions that activate only some of a user's roles, in support of least privilege)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 14 (design principles)
---

The principle of least privilege says that each program and each user should run with the smallest set of rights that its task needs, and only for as long as it needs them. Saltzer and Schroeder (1975) put it as one of their eight design principles: "Every program and every user of the system should operate using the least set of privileges necessary to complete the job." The aim is to limit damage. A bug, a mistake or an attacker who takes over a program can do only what that program was allowed to do. In terms of the [access control matrix](/access-control-matrix/), the row of each subject should hold only the cells that its task uses. The principle does not say how to find that set; mechanisms such as [capability lists](/capability-list/), sessions of [role-based access control](/role-based-access-control/) and sandboxes are ways to apply it.

## In plain words

Give each person and each program only the keys it needs for today's job, and take the keys back when the job is done. A cleaner gets the key to the offices, not to the safe. A program that shows pictures does not need the right to send e-mail or to delete files.

If something goes wrong, the harm stays small. A thief who steals the cleaner's key cannot open the safe. A program with a bug, or one that an attacker controls, can damage only what it was allowed to touch. It is also easier to check a small set of rights than a large one, so mistakes in the rights themselves are easier to find.

## The idea

Fix a task $T$ that a subject must do, and let $N(T)$ be the set of requests $(o, r)$ that some correct run of $T$ makes. A grant $G$, a set of pairs $(o, r)$, is enough for $T$ when $N(T) \subseteq G$. Least privilege asks for a grant that is enough and as small as the mechanism allows; the ideal is $G = N(T)$. The excess $G \setminus N(T)$ is the authority that an attacker who controls the subject gains for free.

Three points make the principle harder than the definition:

- **Granularity.** A mechanism can only give rights in the units it has. If the only rights are "all files of the user" or "root", the least grant is still large. Much of the work on the principle is about finer units: one file, one network port, one system call, one role in one session.
- **Time.** The needs of a program change while it runs. A server needs a privileged right to bind a low port at the start and never again. Least privilege then means dropping the right after the first step, or splitting the program into a small privileged part and a large unprivileged part.
- **Which authority is used.** A subject with two rights can use the wrong one. Hardy's confused deputy was a compiler that held the right to write a billing file, and a user asked it to write output to that file; the compiler used its own right where it should have used the user's. With [capabilities](/capability-list/), each request names the authority it uses, which keeps the rights of the caller and of the program apart. The capability community calls this form the principle of least authority.

The principle sits next to other design rules of Saltzer and Schroeder: fail-safe defaults (deny what is not granted), complete mediation (check every access, the job of a [reference monitor](/reference-monitor/)) and separation of privilege (need two conditions, or two people, for a critical act, which leads to [separation of duty](/separation-of-duty/)).

## Examples

- **Roles in a session.** In the bank of the [RBAC](/role-based-access-control/) page, alice is a manager, but she opens a session with only the role employee active. In that session she cannot approve a loan, so a mistake or a malicious program that runs in it cannot either. She activates manager only for the approval.
- **Dropping rights in a server.** A web server starts as an administrator to open port 80, then switches to an unprivileged user before it reads any request. An attacker who exploits a bug in the request parser gets the unprivileged user, not the administrator.
- **Privilege separation.** A network daemon is split into a small process that keeps the rights it needs for authentication and a large process that parses network input with almost no rights; the two talk through a narrow interface.
- **Capabilities instead of identity.** A program that converts one file is given a capability for the input and one for the output, and nothing else, instead of all the rights of the user who runs it.
- **Choosing roles.** Given the permissions $N(T)$ of a task and a fixed set of roles, picking roles that cover $N(T)$ with the fewest extra permissions is a covering problem of the kind of [set cover](/set-cover/). Administrators often give a broad role instead, which is the most common way the principle is broken.

## Where it is used

The principle is a requirement in the design of operating systems and of their evaluation, from Multics to current microkernels such as seL4, where every right of a process is a capability that it was handed. It is the reason for the sessions of RBAC and for the narrow permission scopes of cloud services and mobile apps, which ask for each right separately. Sandboxes, [software fault isolation](/software-fault-isolation/) and process isolation in browsers apply it to code that is not trusted. In organizations it joins [separation of duty](/separation-of-duty/): least privilege limits what one person can do, and separation of duty makes sure that no one person can do a critical task alone.

## References
