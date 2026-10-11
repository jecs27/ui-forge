# Install

Pick your agent. No dependencies, no setup: the only executable is
`skills/ui-forge/scripts/scan_static.py` (Python 3 stdlib, read-only).

## Claude Code

Send two separate prompts:

```
/plugin marketplace add jecs27/ui-forge
```

```
/plugin install ui-forge@ui-forge
```

## Codex

```bash
codex plugin marketplace add jecs27/ui-forge
codex plugin add ui-forge@ui-forge
```

## OpenCode

From a checkout of this repo, point `opencode.json` at it:

```json
{ "plugins": ["./path/to/ui-forge"] }
```

Or copy the skill folder manually (also works for `.agents/` and
`.claude/` hosts):

```bash
git clone --depth 1 https://github.com/jecs27/ui-forge.git
cp -r ui-forge/skills/ui-forge ~/.config/opencode/skills/
```

## Any other agent (skills CLI)

```bash
npx skills add jecs27/ui-forge
```

Then reload your agent. `/ui-forge` is now available.

## Uninstall

| Host | Command |
|------|---------|
| Claude Code | `/plugin remove ui-forge` |
| Codex | `codex plugin remove ui-forge` |
| OpenCode / manual | Delete the `ui-forge` skill folder |
| Skills CLI | `npx skills remove ui-forge` |
