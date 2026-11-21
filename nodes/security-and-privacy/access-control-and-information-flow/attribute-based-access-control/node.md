---
tag: 5YM4Z5
kind: model
slug: attribute-based-access-control
name: Attribute-based access control
aliases:
- ABAC
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Decides access by evaluating rules over attributes of the subject, the object, the action and the environment.
model: word-ram
prereqs: [role-based-access-control]
see_also: [role-based-access-control, relationship-based-access-control, access-control-matrix, mandatory-access-control, reference-monitor, sat, trust-management, authorization-logic]
sources:
  - paper: doi:10.6028/NIST.SP.800-162
    title: Vincent C. Hu, David Ferraiolo, Rick Kuhn, Adam Schnitzer, Kenneth Sandlin, Robert Miller and Karen Scarfone, Guide to attribute based access control (ABAC) definition and considerations, NIST Special Publication 800-162, January 2014, updated 2019
    locator: the definition of ABAC, its functional components, and the comparison with access lists and roles
  - paper: doi:10.1007/978-3-642-31540-4_4
    title: Xin Jin, Ram Krishnan and Ravi Sandhu, A unified attribute-based access control model covering DAC, MAC and RBAC, Data and Applications Security and Privacy XXVI (DBSec 2012), LNCS 7371
    locator: pages 41 to 55 (the model ABAC alpha and its configurations for DAC, MAC and RBAC)
  - url: "https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html"
    title: OASIS, eXtensible Access Control Markup Language (XACML) Version 3.0, OASIS Standard, 22 January 2013
    locator: Appendix C (the combining algorithms, among them deny-overrides, permit-overrides and first-applicable)
  - paper: doi:10.1109/2.485845
    title: Ravi S. Sandhu, Edward J. Coyne, Hal L. Feinstein and Charles E. Youman, Role-based access control models, IEEE Computer 29(2), 1996
    locator: pages 38 to 47 (roles as the model that ABAC generalizes)
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section I (the design principle of fail-safe defaults)
---

Attribute-based access control (ABAC) decides each request by evaluating rules over attributes: properties of the subject (its department, its clearance, its roles), of the object (its owner, its type, its label), of the action, and of the environment (the time, the network the request comes from). NIST SP 800-162 (2014) describes it as a method where authorization is determined by evaluating such attributes against a policy of rules. No matrix is stored: a cell of the [access control matrix](/access-control-matrix/) is computed when a request comes, and it changes as soon as an attribute changes. [Role-based access control](/role-based-access-control/) is the special case where the rules test only the roles of the user; ABAC adds the attributes of objects and of the context, which lets one rule cover many objects that no single role would describe.

## The machine

**State.** Finite sets of subjects $S$, objects $O$ and actions (the rights $R$), and:

- for each subject, object and for the environment, a finite map from attribute names to values: $\mathrm{att}(s)$, $\mathrm{att}(o)$ and $\mathrm{env}$;
- a policy: a finite list of rules $(c, e)$, where the condition $c$ is a Boolean formula over tests on attributes, such as $\mathrm{att}(s).\mathrm{dept} = \mathrm{att}(o).\mathrm{dept}$ or $\mathrm{env}.\mathrm{hour} \le 19$, and the effect $e$ is permit or deny;
- a combining rule that resolves rules that disagree.

**Decision.** A request is a triple $(s, o, a)$, evaluated in the current environment. With the combining rule deny-overrides, any applicable deny rule wins, and the default is deny:

```pseudo id=main
DECIDE(s, o, a, env)
L1  permit ← false
L2  for each rule (c, e) of the policy do
L3      if c holds on att(s), att(o), a and env then
L4          if e = deny then return deny
L5          permit ← true
L6  if permit then return permit else return deny
```

XACML, the OASIS standard language for ABAC policies, also defines permit-overrides, where a permit wins, and first-applicable, where the first rule whose condition holds decides. The deny at line L6 is the fail-safe default of Saltzer and Schroeder: what no rule permits is denied.

**Transitions.** Administrators change the policy. Other parties change attributes: the human resources system moves a user to a new department, an owner sets the type of a document, the clock moves. Each such change can change many cells of the implied matrix at once, with no edit of any access list.

**Example.** A hospital has the rules

1. permit read when $\mathrm{att}(s).\mathrm{job} = \text{doctor}$ and $\mathrm{att}(s).\mathrm{ward} = \mathrm{att}(o).\mathrm{ward}$;
2. permit write when $\mathrm{att}(s).\mathrm{job} = \text{doctor}$ and $\mathrm{att}(o).\mathrm{patient\_doctor} = s$;
3. deny any action when $\mathrm{env}.\mathrm{network} = \text{external}$ and $\mathrm{att}(o).\mathrm{type} = \text{record}$.

Doctor alice of the heart ward asks to read the record of a heart patient whose doctor is bob, from inside the hospital: rule 1 applies, rule 3 does not, and the answer is permit. Her request to write the same record is denied, because rule 2 needs her to be the patient's doctor. The same read from home is denied by rule 3. When alice moves to another ward, rule 1 stops applying to every record of the heart ward at once.

## What it counts

**The access decision.** Lines L2 to L5 evaluate each rule once. With attribute lookups in hash tables, the time is linear in the total size of the conditions, $O(|\text{policy}|)$, so the decision is polynomial. Real systems index the rules by action or by object type, so that only a few conditions are evaluated for each request.

**Policy analysis.** The harder questions are about all requests at once: does any request get permit from this rule? Does a change of the policy allow anything new? When conditions are arbitrary Boolean formulas over Boolean attributes, "is there an assignment of attributes that a rule permits?" is the [satisfiability problem](/sat/), so it is NP-complete, and comparing two policies is as hard. Tools for policy analysis reduce such questions to SAT or SMT solvers.

## Relation to other models

- **RBAC.** Make the set of roles an attribute of the subject and write one rule for each role and permission: the rule permits the permission when the role is in the attribute. This is [RBAC](/role-based-access-control/) without sessions. Hierarchies and separation of duty need more attributes or more rules.
- **MAC and DAC.** With a label as an attribute of subjects and objects and a rule that tests *dom*, ABAC gives lattice [mandatory access control](/mandatory-access-control/). With the owner as an attribute of each object and a list of allowed users as another, it gives [discretionary access control](/discretionary-access-control/). Jin, Krishnan and Sandhu (2012) defined a small model, ABAC alpha, and showed how to configure it to cover DAC, MAC and RBAC.
- **ReBAC.** [Relationship-based access control](/relationship-based-access-control/) uses relations between subjects and objects in a graph instead of attributes of single entities. Rule 2 of the example, "the requester is the patient's doctor", is a relationship stored as an attribute.
- **Trust management.** In [trust management](/trust-management/) and [authorization logics](/authorization-logic/), the attributes come as signed credentials from other parties, and the policy is a logic program over them.

## Known results in the model

- **Decision.** For a fixed policy with conditions of bounded size, a decision takes time linear in the size of the policy.
- **Expressiveness.** ABAC alpha can be configured to express DAC, MAC and RBAC (Jin, Krishnan and Sandhu 2012).
- **Analysis.** Asking whether some request is permitted is NP-complete when conditions are propositional formulas over Boolean attributes, by the plain reduction from SAT and back, since a guessed assignment is checked in polynomial time.
- **No single model.** NIST SP 800-162 gives a definition and a guide, not one formal model, and ABAC alpha is one of several formal models. Results about safety under changes of attributes depend on who may change which attribute, in the same way as for the [HRU model](/harrison-ruzzo-ullman-model/).

## References
