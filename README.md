# SwissKnife Action Hub

Community **action packs** for [SwissKnife](https://github.com/Nemu-x/SwissKnife-for-MS-Graph) —
the cross-platform Microsoft 365 administration runtime.

Browse and install them from the app: **Settings → Action packs → Action Hub**.

| Pack | Category | Kind | What it does |
| --- | --- | --- | --- |
| [security-basics](packs/security-basics) | Security | Workflow | Compromised account response, shared-mailbox conversion, quick offboarding |
| [phishing-response](packs/phishing-response) | Security | Workflow | Block a phishing sender, report it, purge the copies; undo a false positive |
| [hr-lifecycle](packs/hr-lifecycle) | HR | Workflow | New joiner, team move, leave of absence, back from leave |
| [mailbox-delegation](packs/mailbox-delegation) | Exchange | Workflow | Assistant access (and taking it back), shared mailbox access, room setup |
| [litigation-hold](packs/litigation-hold) | Exchange | PowerShell | List mailboxes on litigation hold, turn the hold on or off |
| [teams-governance](packs/teams-governance) | Teams | Workflow | Meeting, messaging and calling policies for a department or a person |
| [intune-rollout](packs/intune-rollout) | Intune | Workflow | Roll a configuration profile and a compliance policy out to a group, or back |
| [exchange-audit](packs/exchange-audit) | Reports | PowerShell | Who can open shared mailboxes, mailboxes with auditing off, empty lists |
| [teams-audit](packs/teams-audit) | Reports | PowerShell | Users whose Teams policies differ from the org defaults |
| [license-ops](packs/license-ops) | Other | Workflow | Swap a license without a gap, move between distribution lists |

## Two kinds of packs

- **Workflows** chain the app's own actions — no code. Each step is previewed,
  confirmed once and journaled like any built-in action. Prefer these.
- **PowerShell packs** add actions the app does not have. Scripts run with the
  operator's admin connection in their own process, restricted: only the
  commands the pack declares (`cmdlets`), in ConstrainedLanguage.

Either way, an installed pack runs only when it is **signed** by a key the
operator trusts, or after the operator **reviewed and trusted** its exact files.
Installing checks every file against the digest in [`index.json`](index.json).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The pack format is documented in the
[app repository](https://github.com/Nemu-x/SwissKnife-for-MS-Graph/tree/main/packs).
