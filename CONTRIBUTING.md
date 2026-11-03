# Contributing

Thank you for your help. This file tells you how to change the content. To change the toolchain, go to [tamnd/algorithm-agent](https://github.com/tamnd/algorithm-agent).

## Rules for all content

- Write everything yourself. Do not copy text, figures, exercises or code from a book, a paper or a web site, even with a free licence. Read your sources, close them, and then write. Put each source that you used in `sources`.
- Write in plain English. Use short sentences, the active voice and simple words. We follow ASD-STE100 where we can.
- Each claim must have a proof on the page or a source.
- Each implementation follows the pseudocode. Mark each step with a `@line` comment, for example `# @line L4`.
- Each implementation file starts with the SPDX header. Copy it from a node that exists.

The [content standard](https://algorithm.tamnd.com/spec/06-content-standard/) has the full rules.

## Make a change

1. Find an issue, or open one. Say which node you want to write or change.
2. Fork the repository and make a branch from `main`.
3. Make a node with `algo new`, or change a node.
4. Run `algo check -changed origin/main`, `algo viz check` and `algo test -unsafe-local <slug>`.
5. Run `algo site serve` and read your page.
6. Open a pull request and fill in the template.

A new node gets a provisional tag `NEW-<slug>`. A maintainer gives it a real tag before the merge.

## Review

A maintainer reads each pull request. For a proof, the reviewer checks each step. For code, the reviewer checks it against the pseudocode. The review record goes into `reviews/`.

## Sign-off

Each commit must have a `Signed-off-by` line (the [Developer Certificate of Origin](https://developercertificate.org)). Use `git commit -s`. With this line, you state that you wrote the change and that you have the right to give it under the licence of its part.

## Licence

Your change is under the licence of the part that it goes into. [LICENSES/README.md](LICENSES/README.md) lists the parts.
