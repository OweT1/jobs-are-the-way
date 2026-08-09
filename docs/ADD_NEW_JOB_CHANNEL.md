# Adding a New Job Channel

This guide documents the steps required to add a new Telegram thread (channel) that the workflow
posts jobs into. It covers both simple category threads and special cross-posting threads such as
the Big Tech thread.

## Prerequisites

- Create the topic/thread in your Telegram channel and grab its `message_thread_id`.
- Add the corresponding value to your local `.env` and to the GitHub Actions
  **variables** (`Settings > Secrets and variables > Actions > Variables`) for each environment
  that runs the workflow (e.g. `develop` and `production`).

## Steps

### 1. Add the thread ID to `.env.example`

Add a new empty variable, e.g.:

```env
BIG_TECH_THREAD_ID=
```

Do the same in your local `.env` with the actual thread ID.

### 2. Register the setting in `src/core/config.py`

Add a matching field to the `Settings` class. Pydantic maps it from the
`BIG_TECH_THREAD_ID` environment variable automatically:

```python
big_tech_thread_id: str
```

> Note: the field is **required** (no default). If it is missing from the environment,
> the app will raise a `ValidationError` at startup.

### 3. Wire the env var into the GitHub Actions workflows

All workflows that load `Settings()` must export the new variable, or CI will crash:

- `.github/workflows/hourly-message-dev.yml`
- `.github/workflows/hourly-message-prod.yml`
- `.github/workflows/daily-db-cleanup-prod.yml`

Add the line alongside the other thread IDs:

```yaml
BIG_TECH_THREAD_ID: ${{ vars.BIG_TECH_THREAD_ID }}
```

### 4. Define the routing logic

#### Simple category thread

If the channel is tied to a job category, add a mapping in
`get_job_thread_id()` in `src/utils.py`:

```python
"CUSTOM_CATEGORY": settings.custom_category_thread_id,
```

Thereafter, you will need to add a mapping in constants in `src/constants.py`, particularly `JOB_CATEGORIES` and `JOB_CATEGORIES_DESCRIPTIONS` if you want a LLM to categorise as the category.

#### Cross-posting thread (e.g. Big Tech)

If the channel aggregates jobs from other categories for a subset of companies:

1. Add the matches to the `BIG_TECH_COMPANIES` environment variable (comma-separated).
   The default lives in `DEFAULT_BIG_TECH_COMPANIES` in `src/core/config.py` and can be
   overridden via `.env` locally and via a GitHub Actions **variable** (not secret) per
   environment:

   ```env
   BIG_TECH_COMPANIES=apple,google,meta,microsoft,...
   ```

2. Keep the category filter in `src/constants.py`:

   ```python
   BIG_TECH_JOB_CATEGORIES = frozenset(["SOFTWARE_ENGINEER", ...])
   ```

3. Add a matcher helper in `src/utils.py` (reads from `settings.big_tech_company_set`):

   ```python
   def is_big_tech(company_name: str) -> bool:
       return company_name.lower().strip() in settings.big_tech_company_set
   ```

### 5. Send the messages in `src/main.py`

1. Add a batched send helper (reuse `send_tele_msg_batch`) and import the new constants.

2. In the per-company loop, after the category loop, conditionally send to the new thread.
   Use `.isin()` (not a row-wise `.apply()` with the default `axis=0`, which raises a
   `KeyError`):

   ```python
   if is_big_tech(company):
       big_tech_df = company_df[company_df["job_category"].isin(BIG_TECH_JOB_CATEGORIES)]
       await send_tele_msg_batch(
           telegram_bot=tele_bot,
           df=big_tech_df,
           company=company,
           thread_id=settings.big_tech_thread_id,
       )
   ```

3. Inside `send_tele_msg_batch`, make sure each batch sends only its slice
   (`format_company_message(company_df=temp_df, ...)`), not the full dataframe.

### 6. Lint, format, and commit

```bash
uv run ruff format src/
uv run ruff check src/
git add -A
```

## Checklist

- [ ] `BIG_TECH_THREAD_ID=` added to `.env.example` and local `.env`
- [ ] `big_tech_thread_id: str` added to `Settings`
- [ ] Workflow YAML files export the new variable
- [ ] GitHub Actions variables updated for all environments (incl. `BIG_TECH_COMPANIES`)
- [ ] Constants + matcher helper added
- [ ] `send_tele_msg_batch` logic uses the batch slice
- [ ] `.isin()` used for category filtering
- [ ] `ruff format` / `ruff check` pass
