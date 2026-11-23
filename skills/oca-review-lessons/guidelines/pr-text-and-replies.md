# Pull request text and replies to reviews

Source: rule of these skills, from review evidence (`evidence.md`).
Complements `oca-guidelines/guidelines/commits.md`.

## Pull request

- Title: `[<series>][TAG] <module>: <summary>`; the series goes in the title,
  never in the commit header ("remove `[18.0]` from the commit message").
- Description in plain text, one to three short paragraphs: what was wrong
  (a case, an error), why this fix if there was an obvious alternative, how to
  test it on runboat. A port starts with "Forward-port of #<n>" or "Backport
  of #<n>". Then the `Assisted-by:` line.
- No headings, bold, emoji, checklists, "Summary" or "Test plan" sections, no
  restatement of the diff. "Instead of the AI description, which is long, but
  not the most descriptive, please show visually with screenshots the
  problem."
- A visible change: before/after screenshots.

Tone of descriptions core maintainers write themselves:

> Forward-port of #5249
>
> The identifier doesn't matter if the invoice is simplified, as it's not sent
> and thus the rules for applying breakdown are not counting.

## Replies (drafted for the human, who posts them)

- One or two sentences per point. "Done." answers a requested change.
- A question gets the answer with its evidence: a log line, a link to the
  upstream code at a commit.
- A disagreement is argued once, technically; then the human decides.
- No quoting of the whole comment, no thanks on every point, no paragraphs of
  apology. "Concrete and concise answers is the key for getting attention."
