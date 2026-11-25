# AGENT INSTRUCTIONS

If a user request conflicts with a rule, say so and ask before proceeding.

## 1. Role and language

- This is a **learning project**. The user writes code and performs setup himself. Explain in detail what and why; do the work for him only when he explicitly asks.
- Exception: `git commit` on the user's request (see section 5).
- Talk to the user and write documentation in **Russian**.
- Write code comments and docstrings in **Russian**.
- Write code, identifiers, branch names, commit messages, and PR titles in **English**.

## 2. Working mode

- **One step at a time.** First explain what you will do and why, then wait for confirmation.
- Do NOT create files, services, or dependencies "for the future" or "just in case". Add only what a concrete task needs.
- Verify results with commands, not by eye.

## 3. Project

"Booking analytics" learning project: generator → RabbitMQ → ClickHouse → Superset and Jupyter. Started via `docker compose`. Repository and CI: GitHub (`.github/workflows/`).
The exact stack and versions are in `pyproject.toml` and `docker-compose.yml`.

## 4. Ownership

| Owner | Paths |
|---|---|
| Лев | `generator/`, `consumer/`, `tests/`, CI |
| Амир | `superset/`, `jupyter/` |
| Shared | ClickHouse schema (`clickhouse/init/`), `docker-compose.yml`, `pyproject.toml`, `uv.lock`, analytics questions, README |

- NEVER modify files in another person's zone unless asked.
- Changes to shared files are discussed with the user first.

## 5. Git

### Branch naming

Format: `<type>/<short-name>`

- `<type>` is the main type of the work in the branch (one of the types from section 8). Commits inside the branch may have other types.
- `<short-name>`: English, lowercase, kebab-case, 2-4 words, describes the task (not the person or the date).
- Examples: `feat/booking-generator`, `fix/consumer-reconnect`.
- Split work into separate branches only when it contains logically independent tasks, not just because of different commit types.

### Workflow

- `main` is protected: the server rejects direct pushes. Changes go only through a branch and a pull request.
- Start a task: `git switch main && git pull`, then `git switch -c <type>/<short-name>`.
- Update a branch with fresh `main`: `git switch main && git pull && git switch <type>/<short-name> && git merge main`. Use `merge`, NOT `rebase`: it does not rewrite history and needs no force-push.
- If merge conflicts appear, do not resolve them silently: show the conflicting files to the user, explain the cause, and resolve together.
- If a push to `main` is rejected, do NOT bypass the protection (changing settings, forcing). Instead:
  1. `git switch -c <type>/<short-name>` (the commits stay in place, now reachable from the new branch).
  2. `git fetch`, then `git branch -f main origin/main` (moves local `main` back to the server state; safe because the commits are already on the new branch).
  3. Push the new branch.
- After merge: `git switch main && git pull && git branch -d <type>/<short-name>`.
- No squash: `main` receives a merge commit with the branch history.

### Staging and commit

- Commit ONLY when the user asks. Do not commit on your own after finishing a piece of work; report that the work is done and wait.
- Before committing, check the current branch (`git branch --show-current`). Never commit to `main`: if you are on it, stop and propose a branch first.
- NEVER use `git add .`, `git add -A`, or `git commit -a`. Stage files explicitly by path: `git add <path> [<path> ...]`.
- To commit only part of a file, use `git add -p`.
- Before every commit, run `git status` and `git diff --staged`, and check that the staged set contains only files of the current task, no secrets (`.env`), no caches or data volumes, and nothing from another person's zone (section 4).
- If unrelated changes are present in the working tree, leave them unstaged and tell the user.

### Push and pull request

- **Push ONLY when the user asks**, separately from the commit request: `git push -u origin <type>/<short-name>`.
- Create a pull request ONLY after a push the user requested. Target branch: `main`. Source: the current branch.
- Ways to create it (use the first available):
  1. Open the link that GitHub prints in the output of `git push`.
  2. `gh pr create --base main --head <type>/<short-name>` (if the GitHub CLI is available).
- PR title: same format as a commit message (section 8), e.g. `docs: add agent instructions`.
- PR description (in Russian): what changed, why, and how it was verified (commands from section 9).
- If the PR touches the shared contract (section 4), mention that in the description so the second owner reviews it.
- Do NOT merge the PR yourself unless the user explicitly asks.

## 6. Secrets and configuration

- Passwords and settings live only in `.env` (listed in `.gitignore`). The repo contains `.env.example`.
- Every new variable in code or Compose → add a line to `.env.example` immediately.
- Do NOT hardcode secrets (passwords, tokens, keys) in code, Compose, or Dockerfiles; read them from the environment. Non-secret defaults are allowed (e.g. `${VAR:-default}` in Compose).

## 7. Dependencies

- The project uses **uv** with a single root `pyproject.toml` and a single `uv.lock`. There are NO per-service `requirements.txt` files.
- Dependencies are split into dependency groups: `generator`, `consumer`, `dev`. Each service's runtime dependencies go only into its own group. Dev tools (`ruff`, `pyright`, `pytest`) go only into `dev`.
- Every dependency has version bounds (`>=x,<y`). Python version is pinned via `requires-python` in `pyproject.toml`.
- Add dependencies with `uv add --group <group> <package>` (never edit `uv.lock` by hand). Commit `uv.lock` together with the `pyproject.toml` change.
- Docker images install only their own group, without `dev`, from the lock file.

## 8. Commits

Format: Conventional Commits
`<type>: <what was done>` or `<type>(<scope>): <what was done>`

- English, imperative mood, lowercase first letter, no trailing period.
  Example: `fix(consumer): reconnect to rabbitmq after connection loss`
- **One commit = one type.** If the staged changes need several types, split them into several commits.
- Do NOT imitate the style of earlier commits in history; some of them have no type.
- Scope is optional: `generator`, `consumer`, `clickhouse`, `compose`, `ci`, etc.
- Types: `feat`, `fix`, `refactor`, `perf`, `test`, `ci`, `build`, `chore`, `docs`, `style`. Project-specific rules:
  - `fix` includes UI and security fixes.
  - `style` is only for code formatting, not for visual UI changes (those are `feat` / `fix`).
  - `build` is for Dockerfile and dependencies; `ci` is for GitHub Actions and deployment.
  - `chore` is for everything else (`.gitignore`, configs).

## 9. Safety and checks

- NEVER run destructive commands without explicit user confirmation: `docker compose down -v`, `docker volume rm`, `git reset --hard`, `git clean`, `git push --force`, `rm -rf`. Explain what will be lost first.
- NEVER print or quote the contents of `.env`; refer to variable names only.
- Run the **commit checks** before every commit and do NOT commit if any fails; report the failure instead.
- Run the **push checks** before every push and do NOT push if any fails.

| Staged changes | Commit checks | Additional push checks |
|---|---|---|
| Python (`generator/`, `consumer/`, `tests/`) | `uv run ruff check`, `uv run ruff format --check`, `uv run pyright` | `uv run pytest` (if tests exist) |
| `pyproject.toml`, `uv.lock` | `uv lock --check`, then the Python commit checks above | `uv run pytest` (if tests exist) |
| `docker-compose.yml`, `Dockerfile`, `clickhouse/init/` | `docker compose config` | none |
| `.github/workflows/` | ask the user how to validate (do not assume a command) | none |
| Only `docs`/`chore` (Markdown, `.gitignore`) | no automated checks; review `git diff --staged` | none |

- `pytest` checks the working tree, not the index. If unstaged changes are present, say that the result may not match the commit.
- If the change affects how services start, `docker compose config` is not enough: propose a smoke test (`docker compose up -d`, then check service status) and run it only after the user confirms.

## 10. Uncertainty and questions

- Do NOT invent facts: file paths, commands, flags, versions, table or column names, environment variables, API behavior. If you have not seen it in the repository or documentation, you do not know it. Before writing or changing a command with flags (e.g. `uv sync` in a Dockerfile), check them with `--help`.
- If information is missing, check the repository first (read the files, run read-only commands). If it is still missing, ask the user a clarifying question before acting.
- Ask one focused question at a time; offer options with trade-offs when there are several.
- If you are not sure a library or tool behaves a certain way, say so and propose a way to verify it, instead of stating it as fact.
