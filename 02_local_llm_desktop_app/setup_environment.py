import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


MODEL_NAME = "phi3"

    
def check_ollama():
    """Check whether Ollama is installed and accessible."""
    ollama_path = shutil.which("ollama")

    if ollama_path is None:
        print("Ollama is not installed.")
        return False

    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Ollama detected: {result.stdout.strip()}")
        return True

    except Exception as e:
        print(f"Ollama was found but could not be executed: {e}")
        return False


def check_phi3():
    """Check whether the Phi-3 model is installed."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        models = result.stdout.lower()

        if MODEL_NAME in models:
            print("Phi-3 model detected.")
            return True

        print("Phi-3 model is not installed.")
        return False

    except Exception as e:
        print(f"Could not check Ollama models: {e}")
        return False


def download_ollama_installer():
    """Download the official Ollama Windows installer."""
    url = "https://ollama.com/download/OllamaSetup.exe"
    installer_path = Path.home() / "Downloads" / "OllamaSetup.exe"

    installer_path.parent.mkdir(parents=True, exist_ok=True)

    print()
    print("Ollama is not installed.")
    print("Downloading the official Ollama installer...")
    print()

    try:
        urllib.request.urlretrieve(url, installer_path)

        print(f"Ollama installer downloaded to:")
        print(installer_path)

        return installer_path

    except Exception as e:
        print(f"Failed to download Ollama installer: {e}")
        return None


def main():
    print("=" * 50)
    print("ProfSagarLocalAI - Environment Check")
    print("=" * 50)
    print()

    ollama_available = check_ollama()

    if not ollama_available:
        print()
        print("Ollama is required to run ProfSagarLocalAI.")
        sys.exit(1)

    print()

    phi3_available = check_phi3()

    print()
    print("-" * 50)

    if phi3_available:
        print("Environment is ready.")
    else:
        print("Ollama is ready, but Phi-3 needs to be installed.")

    print("-" * 50)


if __name__ == "__main__":
    main()

