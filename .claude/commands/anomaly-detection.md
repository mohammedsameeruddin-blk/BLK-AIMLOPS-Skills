---
description: Start an interactive anomaly detection project. Guides you through every decision one menu at a time, writes ml-project.yaml, then offers to run training.
---

Read `skills/ml/anamoly-detection/SKILL.md` in full, then begin Phase 0:

Ask the user:
```
What would you like to call this project? (e.g. credit-card-fraud, sensor-anomaly)
```

After they answer, run:
```bash
python new_project.py --name <project-name>
```

Then continue with Phase 1 — ask one menu at a time in the order defined in the skill file.
