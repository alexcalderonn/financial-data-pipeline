import subprocess
import sys
from pathlib import Path

print("=" * 50)
print("FINANCIAL DATA PIPELINE")
print("=" * 50)

scripts = [
    "extract.py",
    "transform.py",
    "transform_financials.py",
    "validate.py",
    "load.py"
]

src_folder = Path(__file__).parent

for script in scripts:

    print(f"\nRunning {script}...")

    script_path = src_folder / script

    result = subprocess.run(
        [sys.executable, str(script_path)]
    )

    if result.returncode != 0:
        print(f"\nERROR: {script} failed.")
        print("Pipeline stopped.")
        sys.exit(1)

    print(f"{script} completed successfully.")

print("\n" + "=" * 50)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 50)
