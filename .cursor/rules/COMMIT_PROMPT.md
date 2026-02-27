# Git Commit Standards

## Format

`<type>(<scope>): <description>` (Conventional Commits).

## Types

`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

## Logic

1. Run `git log -n 5` to confirm existing scope naming conventions.
2. Use the imperative mood (e.g., "add connection wizard").

## Example

`feat(ui): connection wizard with test flow (fixes #12)`

## Attribution
All issues must end with a co-authorship line that credits the user and the AI assistant that created the issue. Use the handle that matches the tool you are running in:

- If you are in Cursor:
    *Co-authored-by: Cursor <cursoragent@cursor.com>*
- If you are in Claude Code:
    *Co-authored by @<github-username> and @claude*

Replace <github-username> with the repository owner or the user asking for the issue.