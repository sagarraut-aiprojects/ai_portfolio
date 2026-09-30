import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


APP_NAME = "ProfSagarLocalAI.exe"
MODEL_NAME = "phi3"


def get_ollama_path():
    """Locate the Ollama executable on Windows."""

    # 1. Check PATH
    ollama_path = shutil.which("ollama")

    if ollama_path:
        return Path(ollama_path)

    # 2. Check standard per-user installation
    user_install_path = (
        Path.home()
        / "AppData"
        / "Local"
        / "Programs"
        / "Ollama"
        / "ollama.exe"
    )

    if user_install_path.exists():
        return user_install_path

    return None


def phi3_installed(ollama_path):
    """Check whether the Phi-3 model is installed."""

    if ollama_path is None:
        return False

    try:
        result = subprocess.run(
            [str(ollama_path), "list"],
            capture_output=True,
            text=True,
            check=True
        )

        return MODEL_NAME in result.stdout.lower()

    except Exception:
        return False


def download_ollama():
    """Download the official Ollama Windows installer."""

    url = "https://ollama.com/download/OllamaSetup.exe"

    download_dir = Path.home() / "Downloads"
    installer_path = download_dir / "OllamaSetup.exe"

    download_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("Downloading the official Ollama installer...")
    print()

    try:
        urllib.request.urlretrieve(url, installer_path)

        print("Ollama installer downloaded to:")
        print(installer_path)

        return installer_path

    except Exception as e:
        print(f"Failed to download Ollama: {e}")
        return None


def install_ollama(installer_path):
    """Install Ollama silently on Windows."""

    print()
    print("Installing Ollama...")
    print()

    try:
        subprocess.run(
            [
                str(installer_path),
                "/VERYSILENT",
                "/NORESTART",
                "/SUPPRESSMSGBOXES",
            ],
            check=True
        )

        print("Ollama installation completed.")

        try:
            installer_path.unlink()
            print("Temporary Ollama installer removed.")
        except Exception:
            print("Could not remove the temporary Ollama installer.")

        return True

    except subprocess.CalledProcessError as e:
        print(f"Ollama installation failed: {e}")
        return False

    except Exception as e:
        print(f"Unexpected error while installing Ollama: {e}")
        return False


def launch_app():
    """Launch the ProfSagarLocalAI desktop application."""

    if getattr(sys, "frozen", False):
        # Running as packaged bootstrapper
        base_dir = Path(sys.executable).resolve().parent
        app_path = base_dir / "ProfSagarLocalAI" / APP_NAME

    else:
        # Running bootstrap.py during development
        base_dir = Path(__file__).resolve().parent
        app_path = base_dir / "dist" / "ProfSagarLocalAI" / APP_NAME

    if not app_path.exists():
        print()
        print(f"Application not found: {app_path}")
        return False

    print()
    print("Launching ProfSagarLocalAI...")

    try:
        subprocess.Popen([str(app_path)])
        return True

    except Exception as e:
        print(f"Could not launch ProfSagarLocalAI: {e}")
        return False

def main():
    print("=" * 60)
    print("ProfSagarLocalAI - First Run Setup")
    print("=" * 60)
    print()

    # ---------------------------------------------------------
    # Check Ollama
    # ---------------------------------------------------------

    ollama_path = get_ollama_path()

    if ollama_path:
        print("✓ Ollama detected")
        print(f"  Path: {ollama_path}")

    else:
        print("Ollama is not installed.")
        print("Downloading Ollama...")

        installer_path = download_ollama()

        if installer_path is None:
            print("Could not download Ollama.")
            sys.exit(1)

        if not install_ollama(installer_path):
            print("Could not install Ollama.")
            sys.exit(1)

        # Locate Ollama again after installation
        ollama_path = get_ollama_path()

        if ollama_path is None:
            print("Ollama installation could not be verified.")
            sys.exit(1)

        print("✓ Ollama installed successfully")
        print(f"  Path: {ollama_path}")

    print()

    # ---------------------------------------------------------
    # Check Phi-3
    # ---------------------------------------------------------

    if phi3_installed(ollama_path):
        print("✓ Phi-3 detected")

    else:
        print("Phi-3 is not installed.")
        print("Downloading Phi-3...")
        print()

        try:
            subprocess.run(
                [str(ollama_path), "pull", MODEL_NAME],
                check=True
            )

        except subprocess.CalledProcessError:
            print("Phi-3 installation failed.")
            sys.exit(1)

        if not phi3_installed(ollama_path):
            print("Phi-3 installation could not be verified.")
            sys.exit(1)

        print()
        print("✓ Phi-3 installed successfully")

    print()
    print("✓ Local AI environment is ready.")

    if not launch_app():
        sys.exit(1)


if __name__ == "__main__":
    main()