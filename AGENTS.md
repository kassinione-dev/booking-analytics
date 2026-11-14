# AGENT INSTRUCTIONS

These rules are addressed to you, the AI agent working in this repository.
Follow them in every session. If a user request conflicts with a rule, say so and ask before proceeding.

## 1. Role and language

- This is a **learning project**. The user writes code and performs setup himself. Explain in detail what and why; do the work for him only when he explicitly asks.
- Talk to the user and write documentation in **Russian**.
- Write code comments and docstrings in **Russian**.
- Write code, identifiers, branch names, commit messages, and MR titles in **English**.

## 2. Working mode

- **One step at a time.** First explain what you will do and why, then wait for confirmation.
- Do NOT create files or services "for the future".
- Verify results with commands, not by eye: `docker compose config` and the checks from section 9.

## 3. Project

"Booking analytics" learning project: generator → RabbitMQ → ClickHouse → Superset and Jupyter. Started via `docker compose`. Repository and CI: GitLab (`.gitlab-ci.yml`).

Stack: Python 3.13, Docker Compose, ClickHouse, RabbitMQ, Superset, Postgres, Redis, Jupyter.

## 4. Ownership

| Owner | Paths |
|---|---|
| Лев | `docker-compose.yml`, `clickhouse/init/`, `generator/`, `consumer/`, `tests/`, CI |
| Амир | `superset/`, `jupyter/` |
| Shared | ClickHouse schema, analytics questions, README |

- NEVER modify files in another person's zone unless asked.
- Changes to the shared contract (table schemas, environment variable names, `docker-compose.yml`) must be **discussed first**: both zones depend on it.

## 5. Git

### Branch naming

Format: `<type>/<short-name>`

- `<type>` is one of the commit types from section 8 (`feat`, `fix`, `refactor`, `perf`, `test`, `ci`, `build`, `chore`, `docs`).
- `<short-name>`: English, lowercase, kebab-case, 2-4 words, describes the task (not the person or the date).
- Examples: `feat/booking-generator`, `fix/consumer-reconnect`.
- The type is the main type of the work in the branch. If the work needs several types, split it into separate branches.

### Workflow

- `main` is protected: the server rejects direct pushes. Changes go only through a branch and a merge request.
- Start a task: `git switch main && git pull`, then `git switch -c <type>/<short-name>`.
- Update a branch with fresh `main`: `git switch main && git pull && git switch <type>/<short-name> && git merge main`. Use `merge`, NOT `rebase`: it does not rewrite history and needs no force-push.
- If merge conflicts appear, do not resolve them silently: show the conflicting files to the user, explain the cause, and resolve together.
- If a push to `main` is rejected, do NOT bypass the protection (`--force`, changing settings). Move the commits to a branch: `git switch -c <type>/<short-name>` (commits stay in place), then push that branch.
- After merge: `git switch main && git pull && git branch -d <type>/<short-name>`.
- No squash: `main` receives a merge commit with the branch history.

### Staging and commit

- NEVER use `git add .`, `git add -A`, or `git commit -a`. Stage files explicitly by path: `git add <path> [<path> ...]`.
- To commit only part of a file, use `git add -p`.
- Before every commit, run `git status` and `git diff --staged`, and check that the staged set contains only files of the current task, no secrets (`.env`), no caches or data volumes, and nothing from another person's zone (section 4).
- If unrelated changes are present in the working tree, leave them unstaged and tell the user.
- One commit = one type (section 8). If the staged changes need several types, split them into several commits.

### Push and merge request

- **Push ONLY when the user asks**: `git push -u origin <type>/<short-name>`.
- Create a merge request ONLY after a push the user requested. Do not push just to open an MR.
- Target branch: `main`. Source: the current branch.
- Ways to create it (use the first available):
  1. Open the link that GitLab prints in the output of `git push`.
  2. Push with options: `git push -u origin <type>/<short-name> -o merge_request.create -o merge_request.target=main`.
- MR title: same format as a commit message (section 8), e.g. `docs: add agent instructions`.
- MR description (in Russian): what changed, why, and how it was verified (commands from section 9).
- Do NOT merge the MR yourself unless the user explicitly asks.
- If the MR touches the shared contract (section 4), mention that in the description so the second owner reviews it.

## 6. Secrets and configuration

- Passwords and settings live only in `.env` (listed in `.gitignore`). The repo contains `.env.example`.
- Every new variable in code or Compose → add a line to `.env.example` immediately.
- Do NOT hardcode default values in code; read them from the environment.

## 7. Dependencies

- Service dependencies go in that service's `requirements.txt` with version bounds (`>=x,<y`).
- Add a library only for a concrete task, never "just in case".

## 8. Commits

Format: [Conventional Commits](https://www.conventionalcommits.org/)
`<type>: <what was done>` or `<type>(<scope>): <what was done>`

- English, imperative mood, lowercase first letter, no trailing period.
  Example: `fix(consumer): reconnect to rabbitmq after connection loss`
- Do NOT imitate the style of earlier commits in history; some of them have no type.
- Scope is optional: `generator`, `consumer`, `clickhouse`, `compose`, `ci`, etc.
- The commit type should match the type in the branch name (section 5).

| Type | Use for |
|---|---|
| `feat` | new user-facing capability |
| `fix` | bug fix, including UI and security |
| `refactor` | restructuring without behavior change |
| `perf` | performance improvement |
| `test` | tests |
| `ci` | GitLab CI, deployment |
| `build` | Dockerfile, dependencies |
| `chore` | everything else (`.gitignore`, configs) |
| `docs` | documentation |

- `style` is only for code formatting, not for visual UI changes (those are `feat` / `fix`).

## 9. Safety and checks

- NEVER run destructive commands without explicit user confirmation: `docker compose down -v`, `docker volume rm`, `git reset --hard`, `git clean`, `git push --force`, `rm -rf`. Explain what will be lost first.
- NEVER print or quote the contents of `.env`; refer to variable names only.
- Checks: `ruff check`, `ruff format --check`, `pyright`, and `pytest` (if tests exist).
- Run all checks before every commit. Do NOT commit if any of them fails; report the failure instead.

## 10. Uncertainty and questions

- Do NOT invent facts: file paths, commands, flags, versions, table or column names, environment variables, API behavior. If you have not seen it in the repository or documentation, you do not know it.
- If information is missing, check the repository first (read the files, run read-only commands). If it is still missing, ask the user a clarifying question before acting.
- Ask one focused question at a time; offer options with trade-offs when there are several.
- Separate facts from assumptions in your answers: mark what you verified (file, command output) and what you are guessing.
- If you are not sure a library or tool behaves a certain way, say so and propose a way to verify it, instead of stating it as fact.
- If the user's statement looks wrong, say so with reasoning; do not agree automatically.
