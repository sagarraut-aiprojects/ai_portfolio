# ProfSagarLocalAI



A lightweight Windows desktop AI chatbot powered by **Phi-3**, **Ollama**, and **Python**.



ProfSagarLocalAI provides a ChatGPT-style local desktop interface for interacting with an LLM running on the user's own computer. Conversations are stored locally, and the application can be packaged as a standalone Windows executable and distributed through a Windows installer.



> **Version:** 1.0.0

> **Platform:** Windows

> **Model:** Phi-3

> **LLM Runtime:** Ollama

> **GUI:** Tkinter / CustomTkinter

> **Packaging:** PyInstaller

> **Installer:** Inno Setup



\---



## Features



* Local AI chat using Phi-3 through Ollama

* Streaming model responses

* Chat-style desktop interface

* Conversation history

* Create new conversations

* Load previous conversations

* Persistent local conversation storage

* Automatic conversation titles

* Enter-to-send interaction

* Automatic cursor focus in the input area

* Background model processing to keep the GUI responsive

* Windows executable packaging

* Windows installer

* No cloud database required for conversation storage



\---



## Architecture



The application follows a simple layered architecture:



```text

┌──────────────────────────────┐

│          User                │

└──────────────┬───────────────┘

&#x20;              │

&#x20;              ▼

┌──────────────────────────────┐

│       Desktop GUI            │

│     Tkinter / CustomTkinter  │

└──────────────┬───────────────┘

&#x20;              │

&#x20;              ▼

┌──────────────────────────────┐

│    Conversation Manager      │

│                              │

│ Create / Load / Save / Delete│

└──────────────┬───────────────┘

&#x20;              │

&#x20;              ▼

┌──────────────────────────────┐

│       Ollama Client          │

└──────────────┬───────────────┘

&#x20;              │

&#x20;              │ HTTP/API

&#x20;              ▼

┌──────────────────────────────┐

│           Ollama             │

│        Local Runtime         │

└──────────────┬───────────────┘

&#x20;              │

&#x20;              ▼

┌──────────────────────────────┐

│           Phi-3              │

│        Local LLM             │

└──────────────────────────────┘

```



Conversation data is stored separately from the installed application:



```text

%LOCALAPPDATA%

└── ProfSagarLocalAI

&#x20;   └── conversations

&#x20;       ├── conversation-1.json

&#x20;       ├── conversation-2.json

&#x20;       └── ...

```



This separation is important for a packaged Windows application because the installation directory may require administrator permissions.



\---



## Why This Architecture?



### Ollama



Ollama provides the local model runtime and exposes the model through a local API.



This keeps the application layer independent from the underlying model implementation.



### Phi-3



Phi-3 was selected for the first desktop version because the application was designed to operate on CPU-only hardware.



Larger models such as `gpt-oss` were tested during development but were considerably slower in the target CPU-only environment.



### Tkinter / CustomTkinter



The application uses Python's desktop GUI ecosystem rather than requiring a web browser.



This keeps the application lightweight and makes it straightforward to package for Windows.



### JSON Conversation Storage



Conversation data is stored as JSON files.



For version 1.0.0 this is intentionally simple:



* easy to inspect

* easy to debug

* no database dependency

* suitable for a single-user desktop application



A future version could replace this with SQLite or another structured persistence layer if the application's data requirements grow.



\---



## Requirements



### Hardware



The application can run without a dedicated NVIDIA GPU.



Performance depends heavily on the local hardware and the model being used.



For CPU-only systems, smaller models such as Phi-3 are more practical than substantially larger models.



### Software



For running from source:



* Windows

* Python

* `uv`

* Ollama

* Phi-3 model



For the packaged application:



* Windows

* Ollama

* Phi-3 model



> The Windows installer packages the Python application, but it does **not** package Ollama or the Phi-3 model.



\---



# Installation



## 1. Install Ollama



Install Ollama on Windows.



After installation, verify that Ollama is available:



```powershell

ollama --version

```



\---



## 2. Download Phi-3



Run:



```powershell

ollama pull phi3

```



Verify that the model is installed:



```powershell

ollama list

```



You should see a Phi-3 model listed.



\---



# Running the Packaged Application



The project provides a Windows installer generated using Inno Setup.



After installation, launch:



```text

Prof. Sagar's Local AI

```



The application communicates with the locally running Ollama service.



Make sure Ollama is installed and the required Phi-3 model is available before starting a conversation.



\---



# Running from Source



Clone the repository:



```powershell

git clone https://github.com/sagarraut-aiprojects/ai\_portfolio.git

```



Move into the project:



```powershell

cd ai\_portfolio\\02\_local\_llm\_desktop\_app

```



Install dependencies using `uv`:



```powershell

uv sync

```



Run the application:



```powershell

uv run python app.py

```



\---



# Project Structure



```text

02\_local\_llm\_desktop\_app/

│

├── app.py

│       Main desktop application and GUI

│

├── conversation.py

│       Conversation creation, loading, saving and deletion

│

├── ollama\_client.py

│       Communication with the local Ollama API

│

├── pyproject.toml

│       Project configuration and dependencies

│

├── uv.lock

│       Locked Python dependency versions

│

├── ProfSagarLocalAI.spec

│       PyInstaller build configuration

│

├── ProfSagarLocalAI.iss

│       Inno Setup installer configuration

│

└── README.md

&#x20;       Project documentation

```



\---



# Conversation Persistence



Conversation files are stored in:



```text

%LOCALAPPDATA%\\ProfSagarLocalAI\\conversations

```



Each conversation is represented by a JSON file.



A conversation contains information such as:



```json

{

&#x20;   "id": "...",

&#x20;   "title": "Example conversation",

&#x20;   "created\_at": "...",

&#x20;   "messages": \[]

}

```



The application creates the required directory automatically.



This design also prevents the application from attempting to write user data into the Windows Program Files installation directory.



\---



# Building the Windows Executable



The project uses PyInstaller.



Install the development dependencies:



```powershell

uv sync

```



Build using the included specification file:



```powershell

uv run pyinstaller ProfSagarLocalAI.spec

```



The resulting application is generated under:



```text

dist\\ProfSagarLocalAI\\

```



The executable is:



```text

dist\\ProfSagarLocalAI\\ProfSagarLocalAI.exe

```



\---



# Building the Windows Installer



The project uses Inno Setup to create the Windows installer.



The installer configuration is stored in:



```text

ProfSagarLocalAI.iss

```



The installer packages the PyInstaller output into a standard Windows installation.



The generated installer is placed in:



```text

installer\\

```



The `installer/` directory is intentionally excluded from Git because generated binaries should not be stored in the source repository.



\---



# Version 1.0.0



## Release



**v1.0.0 — ProfSagarLocalAI**



Git commit:



```text

cf7eef8

```



Git tag:



```text

v1.0.0

```



### Included in v1.0.0



* Local Phi-3 chatbot

* Ollama integration

* Streaming responses

* Persistent conversation history

* New conversation functionality

* Previous conversation loading

* Local JSON persistence

* Windows executable

* PyInstaller build configuration

* Inno Setup installer configuration

* AppData-based conversation storage



\---



# Known Limitations



### 1. Ollama is required



The application currently relies on Ollama for local model execution.



### 2. Phi-3 must be installed separately



The model is not bundled with the Windows installer.



This avoids distributing a multi-gigabyte model with the application.



### 3. CPU performance varies



Local LLM performance depends on the computer's CPU, available memory, model size and Ollama configuration.



### 4. Single-user local storage



Conversation data is stored locally as JSON files.



There is currently no multi-user account system or cloud synchronization.



### 5. No GPU requirement, but GPU acceleration may improve performance



The application is designed to work without a dedicated NVIDIA GPU, but systems capable of GPU acceleration may provide faster model responses depending on the Ollama/model configuration.



\---



# Development Decisions



This project was intentionally developed incrementally rather than starting with a large framework.



The development sequence included:



1\. Basic local LLM communication

2\. Desktop GUI

3\. Streaming responses

4\. Conversation state

5\. Persistent conversation storage

6\. Conversation history

7\. UI interaction improvements

8\. Error handling

9\. Windows executable packaging

10\. Windows installer

11\. Release tagging



This progression demonstrates the transition from a simple LLM API experiment to a distributable desktop application.



\---



# Future Improvements



Potential future versions could introduce:



* Additional local models

* Model selection from the GUI

* SQLite-based conversation storage

* Search across conversation history

* Conversation export

* Markdown rendering

* File/document interaction

* Retrieval-Augmented Generation (RAG)

* Custom system prompts

* Model configuration controls

* GPU-aware model selection

* Application auto-update functionality



These features are intentionally outside the scope of version 1.0.0.



\---



# Portfolio Context



ProfSagarLocalAI is part of a larger AI engineering portfolio focused on building practical AI applications.



The project demonstrates several important concepts:



* Python application development

* LLM API integration

* Local model deployment

* Conversation state management

* Persistent application data

* GUI development

* asynchronous/background processing

* executable packaging

* Windows software distribution

* Git/GitHub version control



The broader portfolio progressively moves from simple LLM applications toward RAG systems, data-analysis agents, forecasting systems and multi-tool AI agents.



\---



# License



This project is intended primarily as a personal academic and professional portfolio project.



See the repository for the applicable licensing terms.




