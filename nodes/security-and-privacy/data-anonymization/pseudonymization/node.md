---
tag: WDMXRF
kind: technique
slug: pseudonymization
name: Pseudonymization
aliases:
- tokenization of identifiers
area: security-and-privacy/data-anonymization
level: intro
summary: Replaces direct identifiers with consistent pseudonyms, such as keyed hashes, which keeps linkability and does not stop linkage attacks.
prereqs: [hmac, quasi-identifier]
see_also: [linkage-attack, k-anonymity, pseudorandom-function, cryptographic-hash-function, privacy-preserving-record-linkage, sparse-dataset-deanonymization, generalization-and-suppression, block-cipher]
sources:
  - url: https://eur-lex.europa.eu/eli/reg/2016/679/oj
    title: "Regulation (EU) 2016/679 of the European Parliament and of the Council, the General Data Protection Regulation, 2016"
    locator: "Article 4(5), the definition of pseudonymisation, and Recital 26, which says that pseudonymised data that can be attributed to a person with additional information are still personal data"
  - url: https://www.enisa.europa.eu/publications/pseudonymisation-techniques-and-best-practices
    title: "European Union Agency for Cybersecurity (ENISA), Pseudonymisation techniques and best practices, November 2019"
    locator: "the techniques (counter, random number generator, cryptographic hash function, message authentication code, encryption), the pseudonymisation policies of Section 5.2, and the attacks by brute force, dictionary and guesswork at a general level"
  - url: https://www.rfc-editor.org/rfc/rfc2104
    title: "Hugo Krawczyk, Mihir Bellare and Ran Canetti, HMAC, keyed-hashing for message authentication, RFC 2104, 1997"
    locator: the definition of HMAC
  - paper: "Paul Ohm, Broken promises of privacy, responding to the surprising failure of anonymization, UCLA Law Review 57, 2010"
    locator: "pp. 1701 to 1777, the AOL and Netflix releases and the lesson that removing identifiers does not make data anonymous"
---

Pseudonymization replaces the direct identifiers of a data set, such as names, e-mail addresses and identity numbers, by pseudonyms. The same person gets the same pseudonym in every record, so analysts can still count events per person and join tables inside the data set. The standard construction is a keyed function such as [HMAC](/hmac/) with a secret key, or a random pseudonym kept in a lookup table. Only the holder of the key or the table can go back from a pseudonym to the person. The GDPR (Article 4(5)) defines pseudonymisation in this way, with the extra information kept apart, and it treats pseudonymised data as personal data. The reason is that pseudonymization keeps the other attributes as they are. A [linkage attack](/linkage-attack/) on the [quasi-identifiers](/quasi-identifier/) still works, and so does matching on the pattern of a person's records.

## In plain words

A hospital wants to give a study team the records of its patients, but not their names. It replaces each name by a code. The same patient always gets the same code, so the team can still see that one patient came back five times. The hospital keeps the list of codes, or the secret key that made them, locked away.

The codes hide the names, but not the rest. The records still show the birth date, the postcode, the sex and the visits. A person who knows these facts about a neighbor may find the neighbor's records. So a code in place of a name is a first step, not a full answer.

## When it applies

- The users need records that belong together to stay together: visits of one patient, purchases of one customer, or rows of one person in two tables of the same data set.
- The data owner may need to go back to the person later, for example to inform a patient about a finding. Then a reversible method or a kept lookup table is needed.
- The threat is casual identification by name or number inside the organization or at a trusted partner. Against an outside reader with background knowledge, pseudonymization alone is not enough, and the other attributes also need treatment, for example by [generalization and suppression](/generalization-and-suppression/) to reach [k-anonymity](/k-anonymity/).

## The template

The input is a data set $D$ of records, the set of direct identifiers, and a secret $K$: a key or an empty lookup table. The scope of $K$ is a policy choice. One key for all releases lets the releases be joined. One key per release or per recipient stops that.

```pseudo id=main
PSEUDONYMIZE(D, K)
L1  for each record r of D do
L2      v ← NORMALIZE(the main identifier of r)  ▷ hole: one canonical form, for example trimmed and in lower case
L3      replace the main identifier of r by PSEUDONYM(K, v)  ▷ hole: a keyed function, a lookup table, or encryption
L4      remove the other direct identifiers of r             ▷ hole: which fields are direct identifiers
L5  store K apart from D, with access control
L6  return D
```

The holes are NORMALIZE, PSEUDONYM and the list of direct identifiers. The choices for PSEUDONYM, as in the ENISA report of 2019:

- **A keyed function.** $\mathrm{PSEUDONYM}(K, v) = \mathrm{HMAC}_K(v)$, often truncated. If HMAC is a [pseudorandom function](/pseudorandom-function/), a reader without $K$ cannot tell the pseudonyms from random strings, and cannot test a guess for $v$. The holder of $K$ cannot invert the map either, but can recompute the pseudonym of a known person.
- **A lookup table.** Draw a fresh random pseudonym for each new value, or use a counter, and store the pair. The pseudonyms carry no information about $v$, and the table is the secret.
- **Encryption.** Encrypt $v$ with a deterministic mode of a [block cipher](/block-cipher/) under $K$. The holder of $K$ can decrypt and get $v$ back with no table.
- **A plain hash.** A [cryptographic hash function](/cryptographic-hash-function/) of $v$ with no key. This is weak: anyone can compute it, so it protects only an identifier with a very large number of possible values, and most identifiers do not have that.

**Example.** Take the made-up key `demo-key-1`, HMAC-SHA256 truncated to 16 hex digits, and NORMALIZE that trims spaces and changes to lower case.

| identifier in the record | pseudonym |
|---|---|
| `ana.ruiz@example.org` | `fbfdd962459c61ef` |
| `Ana.Ruiz@Example.org ` | `fbfdd962459c61ef` |
| `ben.okafor@example.org` | `0e5341defd8bb724` |

The first two rows are the same person, and the same pseudonym links them. Without line L2, the second row gets `701490df30c6c409`, and the data set shows two people. With the key `demo-key-2`, the first person gets `7bcf71eb2ee25930`, so two releases with different keys cannot be joined on the pseudonym.

## Classic examples

- **Keyed hashing with [HMAC](/hmac/).** The common method for research data and logs. The security rests on the secrecy of the key and on HMAC as a [pseudorandom function](/pseudorandom-function/).
- **Pseudonyms for [record linkage](/privacy-preserving-record-linkage/).** Two data owners pseudonymize with a shared key, and a third party joins the records on equal pseudonyms. This needs exact equality of the normalized identifiers. Privacy-preserving record linkage with Bloom filters relaxes this to similar identifiers.
- **The AOL and Netflix releases.** Both releases replaced user names by numbers. Ohm (2010) describes how the AOL search log of 2006 let reporters identify a user from her queries, and how the Netflix ratings were matched to public reviews (see [sparse dataset de-anonymization](/sparse-dataset-deanonymization/)). In both cases the pseudonym worked as designed, and the other data identified the person.
- **Linkage on quasi-identifiers.** A pseudonymized medical table that keeps the postcode, the birth date and the sex can be joined with a public list that has the same fields and names, which is the [linkage attack](/linkage-attack/) that motivated [k-anonymity](/k-anonymity/).

## Variations

- **Deterministic, document-randomized and fully randomized.** The ENISA report (Section 5.2) names three policies. A deterministic policy always gives a value the same pseudonym. A fully randomized policy gives a new pseudonym at each occurrence, so even records inside one data set cannot be linked. The document-randomized policy lies between the two, and the report defines it by the scope in which the pseudonyms of a value can be related.
- **Domain separation.** Derive the pseudonym for project $j$ as $\mathrm{HMAC}_K(j \,\|\, v)$ with an unambiguous encoding of the pair. One master key then gives independent pseudonyms per project, if HMAC is a pseudorandom function.
- **Reversible and one-way.** Encryption and lookup tables allow the owner to go back. A keyed hash is one-way, and going back needs a list of the people.
- **Pseudonymization by a trusted third party.** The data owners send identifiers to a party that holds the key and returns pseudonyms, so no data owner holds the key.

## Pitfalls

- **A plain hash of a small identifier space.** A staff number of 4 digits has $10^4$ values, and a phone number or a national identity number has a set of possible values that a computer can list in full. With an unkeyed hash, anyone can hash every possible value and compare. The ENISA report lists this among the brute-force and dictionary attacks. A salt that is stored with the data does not help. Use a secret key.
- **Key reuse across releases.** The same key in two releases lets anyone with both releases join them on the pseudonym, even without the key. Use a key per release or per recipient, unless joining is the goal.
- **Missing normalization at line L2.** Different forms of the same identifier give different pseudonyms, as in the example, and the data then counts one person twice.
- **Truncation collisions.** For a random function to $b$ bits and $n$ people, the expected number of pairs that share a pseudonym is $\binom{n}{2} / 2^b$. For $n = 10^5$ and $b = 32$ this is about 1.16, so a 32-bit pseudonym merges two people by accident. For $b = 64$ it is about $2.7 \times 10^{-10}$.
- **Calling the result anonymous.** The quasi-identifiers, the dates and the pattern of records stay. The release is still personal data under the GDPR (Recital 26) and still open to linkage. Treat the other attributes, or use a method with a formal guarantee such as [differential privacy](/differential-privacy-definition/).
- **The key next to the data.** If the key or the lookup table is stored with the data or in the same access group, line L5 fails and the pseudonyms give no protection.

## Exercises

1. Show that the expected number of colliding pairs for $n$ values under a uniformly random function to $\{0, 1\}^b$ is $\binom{n}{2} 2^{-b}$, and find the least $b$ that makes it below $10^{-6}$ for $n = 10^7$.
2. Show that deterministic pseudonymization keeps the number of records per person, and that a fully randomized policy does not let an analyst compute it.
3. Assume that $F_K$ is a pseudorandom function. Prove that the pseudonyms $F_K(1 \,\|\, v)$ and $F_K(2 \,\|\, v)$ of one value in two projects cannot be linked by a reader without $K$ with a non-negligible advantage.
4. A data set keeps the month of birth, the postcode and the sex after pseudonymization. Explain which of the steps of the template protects against a linkage on these fields, and which method from the see-also list could.

## References
