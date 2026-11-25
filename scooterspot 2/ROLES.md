# Roles, plan and workflow

Deadline: **Thu 10.12.2026, 23:59** (video + source code).
Presentation of the video + 5 min Q&A: **Fri 11.12.2026**.

Each role owns specific files and grading requirements, so everyone has visible work
for the contribution matrix and few people edit the same file.

## The 5 roles

### Role 1: Project lead & GitHub (name: ______)
- Creates the GitHub repo, uploads this skeleton, invites the other 4 as collaborators (write access)
- Deploys the app once on share.streamlit.io (the repo owner must do the first deploy)
- Makes sure `python check_setup.py` and `streamlit run app.py` work on every laptop
- Puts the parts together, fixes merge conflicts, runs the weekly meeting, keeps the log below
- Grading: integration, requirement 7 (contribution matrix)

### Role 2: Data, API & database (name: ______)
- Files: `scooter_api.py`, `zones.py`, `database.py`, `collector.py`
- **Today:** run `python check_setup.py`, check the API keys in step 2, fix `fetch_scooters()` if needed
- **Today:** start `python collector.py` and keep it running as much as possible
- Check the zone coordinates on a map, maybe add zones (e.g. Kantonsspital, St. Fiden)
- Commit `data/scooters.db` every few days (only you commit this file)
- Stretch goal: add a second API, e.g. weather, as an extra ML feature (a "mashup" like Assignment 6)
- Grading: requirement 2

### Role 3: Machine learning (name: ______)
- Files: `model.py`, `make_sample_data.py`
- Understand and explain the pipeline: split, train, compare, test (Assignments 10 and 11)
- Improvements: at least 5 models (Assignment 11), feature scaling with `RobustScaler`
  (Assignment 11), tune parameters, add features (e.g. weekend yes/no, weather)
- Re-run the comparison on the real data in week 3 and record the numbers for the video
- Prepare the ML explanation for the video and the Q&A (why classification, why the baseline)
- Grading: requirement 5

### Role 4: App & visualisation (name: ______)
- File: `app.py`
- Layout, texts, map, charts, user interaction
- Ideas: show the chosen zone on the map, a chart of collected data over time (Assignment 9),
  a clear recommendation ("take the bus instead")
- Grading: requirements 1, 3 and 4

### Role 5: Documentation, quality & video (name: ______)
- Reviews all code comments and the README (requirement 6)
- Tests the app like a user, reports bugs to the file owner
- Writes the video script (max. 4 min), collects the GenAI reflections, builds the
  contribution matrix slide, organises the recording. **Voice-over must be our own voices.**
- Before submission: makes sure `data/sample.db` is deleted and the app runs on real data
- Grading: requirements 6, 7 and 8

## Timeline
| Week | Dates | Goal |
|------|-------|------|
| 1 | 19.11. - 25.11. | Repo set up, everyone passes `check_setup.py`, API keys checked, **collector running**, app deployed once |
| 2 | 26.11. - 02.12. | Enough real data (>= 200 rows), model improvements, app complete, comments done |
| 3 | 03.12. - 09.12. | Final model comparison on real data, bug fixing, video recorded and edited |
| - | 10.12. 23:59 | **Submission** |
| - | 11.12. | Presentation + Q&A |

## GitHub workflow
1. Before you start: `git pull`
2. Work mainly in **your own files**
3. When something works: `git add <file>`, `git commit -m "what you changed"`, `git push`
4. If `git push` fails: `git pull`, then push again
5. Never commit passwords or API keys (`passwd.py` is in `.gitignore`)
6. Write clear commit messages (`Add RobustScaler to model.py`, not `update`)

## Meeting log
| Date | Decisions | Next steps (who) |
|------|-----------|------------------|
| | | |

## Contribution matrix (for the video)
| Task | Role 1 | Role 2 | Role 3 | Role 4 | Role 5 |
|------|--------|--------|--------|--------|--------|
| Idea & problem statement | | | | | |
| API & data collection | | | | | |
| Database | | | | | |
| ML model | | | | | |
| Streamlit app | | | | | |
| Code comments & README | | | | | |
| Testing | | | | | |
| Video script & recording | | | | | |
| GitHub & integration | | | | | |

**L** = lead, **C** = contributed, empty = not involved.

## GenAI reflection (everyone writes 2-3 sentences)
- What did you use GenAI for (e.g. starter code, explaining errors, texts)?
- What did you check, test or change yourself?
- Where was it wrong or unhelpful?

Note: the starter skeleton of this repository was generated with Claude (Anthropic)
and then tested, adapted and extended by the team.
