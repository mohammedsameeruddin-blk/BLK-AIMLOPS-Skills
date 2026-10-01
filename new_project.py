"""
Create a new anomaly detection project from the template.

Usage:
  python new_project.py --name credit-card-fraud
  python new_project.py --name sensor-anomaly --projects-dir /path/to/projects
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT         = Path(__file__).parent
TEMPLATE_DIR = ROOT / "template" / "anomaly-detection"
PROJECTS_DIR = ROOT / "projects"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9\-]", "-", name.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new anomaly detection project")
    parser.add_argument("--name", required=True, help="Project name (e.g. credit-card-fraud)")
    parser.add_argument("--projects-dir", default=None, help="Where to create the project (default: ./projects/)")
    args = parser.parse_args()

    slug = slugify(args.name)
    projects_root = Path(args.projects_dir) if args.projects_dir else PROJECTS_DIR
    dest = projects_root / slug

    if dest.exists():
        print(f"ERROR: Project already exists at {dest}")
        print(f"  Delete it first or choose a different name.")
        sys.exit(1)

    if not TEMPLATE_DIR.exists():
        print(f"ERROR: Template not found at {TEMPLATE_DIR}")
        sys.exit(1)

    # Copy template, skip artifacts content (keep the folder, not the files)
    def ignore(src, names):
        src_path = Path(src)
        if src_path.name == "artifacts":
            return [n for n in names if n != ".gitkeep"]
        return []

    shutil.copytree(TEMPLATE_DIR, dest, ignore=ignore)

    # Stamp the project name into ml-project.yaml
    yaml_path = dest / "ml-project.yaml"
    text = yaml_path.read_text()
    text = text.replace("name: my-anomaly-detection", f"name: {slug}", 1)
    yaml_path.write_text(text)

    # Stamp the project name into pyproject.toml
    toml_path = dest / "pyproject.toml"
    text = toml_path.read_text()
    text = text.replace('name = "my-anomaly-detection"', f'name = "{slug}"', 1)
    toml_path.write_text(text)

    print(f"\nProject created: {dest}/")
    print(f"\nNext steps:")
    print(f"  1. Edit  {dest}/ml-project.yaml")
    print(f"     Set data.path, data.target_column, ml_design.selected_algorithm.name")
    print(f"  2. Train:")
    print(f"     python {dest}/src/train.py")
    print(f"  3. Score:")
    print(f"     python {dest}/src/predict.py --input data.csv --output scored.csv")
    print(f"  4. Evaluate:")
    print(f"     python {dest}/src/evaluate.py --predictions scored.csv")


if __name__ == "__main__":
    main()
