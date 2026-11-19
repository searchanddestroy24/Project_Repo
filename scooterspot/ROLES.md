# Roles, plan and workflow

Deadline: **Thu 10.12.2026, 23:59** (video + source code).
Presentation of the video + 5 min Q&A: **Fri 11.12.2026**.

Each role owns specific files and specific grading requirements, so everyone has
visible work for the contribution matrix and few people edit the same file.

## The 5 roles

### Role 1: Project lead & GitHub (name: ______)
- Creates the GitHub repository, uploads this starter code, adds the other 4 as collaborators
- Helps everyone with `git pull / add / commit / push`, fixes merge conflicts
- Puts the parts together and makes sure `streamlit run app.py` works on every laptop
- Runs the weekly meeting and keeps this file up to date
- Optional: publishes the app on Streamlit Community Cloud
- Grading: integration of all parts, requirement 7 (contribution matrix)

### Role 2: Data & API (name: ______)
- Files: `scooter_api.py`, `zones.py`, `collector.py`
- **First task, today:** run `print(scooter_api.fetch_page(0)[:2])`, check the JSON keys, fix them if needed
- Then start `collector.py` as soon as possible and keep it running (every day without data is lost training data)
- Checks the zone coordinates on a map and adjusts them
- Pushes `data/history.csv` to GitHub every few days
- Grading: requirement 2 (API)

### Role 3: Machine learning (name: ______)
- File: `model.py`
- Tests the model on the collected data, explains how training and prediction work
- Improves the model (e.g. more zones, test different `test_share` values, compare with a simple
  "always predict the overall average" baseline)
- Prepares the ML explanation for the video and the Q&A
- Grading: requirement 5 (own ML model)

### Role 4: App & visualisation (name: ______)
- File: `app.py`
- Layout, texts, charts, user interaction (only Streamlit elements from the course demos)
- Makes the problem statement in the app clear and convincing
- Grading: requirements 1, 3 and 4

### Role 5: Documentation, quality & video (name: ______)
- Reviews all comments in the code (requirement 6) and the README
- Tests the app like a user and reports bugs to the file owner
- Writes the video script (4 min max), collects the GenAI reflection from everyone,
  builds the contribution matrix slide, organises the recording
- **Voice-over must be recorded by us, not generated**
- Grading: requirements 6, 7 and 8

## Timeline
| Week | Dates | Goal |
|------|-------|------|
| 1 | 19.11. - 25.11. | Repo set up, everyone runs the app locally, API keys checked, **collector running** |
| 2 | 26.11. - 02.12. | Model trained on the first week of data, app complete, comments done |
| 3 | 03.12. - 09.12. | Final data, model evaluation, bug fixing, video recorded and edited |
| - | 10.12. 23:59 | **Submission** |
| - | 11.12. | Presentation + Q&A |

## GitHub workflow (simple version)
1. Before you start working: `git pull`
2. Work mainly in **your own files**
3. When something works: `git add <file>` then `git commit -m "what you changed"` then `git push`
4. If `git push` fails: `git pull` first, then push again
5. Never commit passwords or API keys

## Contribution matrix (fill in, for the video)
| Task | Role 1 | Role 2 | Role 3 | Role 4 | Role 5 |
|------|--------|--------|--------|--------|--------|
| Idea & problem statement | | | | | |
| API & data collection | | | | | |
| ML model | | | | | |
| Streamlit app | | | | | |
| Code comments & README | | | | | |
| Testing | | | | | |
| Video script & recording | | | | | |
| GitHub & integration | | | | | |

Use: **L** = lead, **C** = contributed, empty = not involved.

## GenAI reflection (everyone writes 2-3 sentences)
- What did you use GenAI for (e.g. explaining errors, first code draft, text)?
- What did you change or check yourself?
- Where was it wrong or unhelpful?
