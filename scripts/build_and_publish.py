import subprocess
import sys
from pathlib import Path


def run_command(command):
    """Run a shell command and print output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return False


def main():
    """Build and publish the package."""
    # Clean previous builds
    print("Cleaning previous builds...")
    run_command("rm -rf dist/ build/ *.egg-info")

    # Build the package
    print("\nBuilding package...")
    if not run_command("python -m build"):
        return

    # Upload to TestPyPI first
    print("\nUploading to TestPyPI...")
    if not run_command(
        "python -m twine upload --repository testpypi --config-file ~/.pypirc dist/*"
    ):
        return

    # Confirm before uploading to PyPI
    response = input("\nDo you want to upload to PyPI? (y/N): ")
    if response.lower() == "y":
        print("\nUploading to PyPI...")
        if not run_command("python -m twine upload --config-file ~/.pypirc dist/*"):
            return
        print("\nPackage successfully published to PyPI!")
    else:
        print("\nSkipping PyPI upload.")


if __name__ == "__main__":
    main()
