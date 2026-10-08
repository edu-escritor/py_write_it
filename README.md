# ✍️ WritΞIt

**WritΞIt** is a Python command-line tool designed to help writers organize, manage, and compile their writing projects.

It brings a structured, developer-friendly workflow to creative writing, allowing authors to focus on their manuscripts while keeping chapters, versions, and project files organized.

WritΞIt uses **Markdown** for writing and **Pandoc** for document compilation.

## 📖 Features

- **Project management:** Create, rename, and update writing projects.
- **Flexible structure:** Organize manuscripts as standalone documents, chapters, or multiple parts.
- **File management:** Create chapters and maintain different versions.
- **File normalization:** Keep filenames consistent using standardized naming conventions.
- **Multilingual support:** Generate project structures and templates in supported languages.
- **Document compilation:** Assemble Markdown files and generate formatted documents.
- **Compilation preview:** Check which files will be included before building the manuscript.

## 📦 Installation

### 🔧 Requirements

- Python 3.12 or newer
- Git
- [Pandoc](https://pandoc.org/) (for document compilation)
- [uv](https://docs.astral.sh/uv/) (recommended)

### 📥 Clone the repository

Clone the project using SSH:

```bash
git clone git@github.com:edu-escritor/py_write_it.git WriteIt
cd WriteIt
```

Alternatively, use HTTPS:

```bash
git clone https://github.com/edu-escritor/py_write_it.git WriteIt
cd WriteIt
```

### ⚡ Install with uv (recommended)

Install WritΞIt as a standalone command-line application:

```bash
uv tool install .
```

This installs the application in an isolated environment and makes the `writeit` command available system-wide through your user account.

Verify the installation:

```bash
writeit --help
```

If the command is not recognized, run:

```bash
uv tool update-shell
```

Then restart your terminal.

#### 🔄 Update

After pulling the latest changes from the repository, reinstall the application:

```bash
git pull
uv tool install --force .
```

#### 🗑️ Uninstall

```bash
uv tool uninstall writeit
```

### 🐍 Install with Python and pip

Alternatively, install WritΞIt in a Python virtual environment.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the application:

```bash
python -m pip install .
```

Verify the installation:

```bash
writeit --help
```

The `writeit` command will be available while the virtual environment is active.

### 🧑‍💻 Development

To install the project dependencies and run WritΞIt directly from the source code:

```bash
uv sync
uv run writeit --help
```

This is useful when developing or testing the application without reinstalling it after every change.

## ⌨️ Shell Autocompletion

WritΞIt supports shell autocompletion through Typer.

Autocompletion allows you to press `Tab` to complete commands and options automatically.

### 🐚 Bash

Install autocompletion:

```bash
writeit --install-completion bash
```

Restart your terminal or reload your Bash configuration:

```bash
source ~/.bashrc
```

You can now type:

```text
writeit pro<TAB>
```

To complete:

```text
writeit project
```

You can also discover available subcommands:

```text
writeit project <TAB>
writeit file <TAB>
writeit compile <TAB>
```

### 🔍 Show Completion Script

To display the generated Bash completion script:

```bash
writeit --show-completion bash
```

Typer also supports other shells, including Zsh and Fish. Replace `bash` with your preferred supported shell.

## 🗂️ Project Structure

WritΞIt supports three project types.

### 📄 Standalone

A single-document writing project, ideal for short stories, essays, or articles.

### 📚 Chaptered

A manuscript organized into individual chapters, ideal for novels and longer works.

### 🧩 Parted

A manuscript divided into multiple parts, each containing its own chapters.

### 🏷️ File Naming

WritΞIt uses structured filenames to identify chapters, their positions, and versions.

Examples:

```text
v01_introduction.md
i0010_v01_first-chapter.md
p01_i0010_v02_first-chapter.md
```

The filename segments represent:

- `p01` — Part 1
- `i0010` — Chapter index 10
- `v02` — Version 2

This convention allows WritΞIt to identify different versions of the same chapter and select the latest one during compilation.

## 💻 Commands

### 🗂️ Project Management

```bash
writeit project create
writeit project rename
writeit project update
writeit project add-part
writeit project normalize
```

### 📄 File Management

```bash
writeit file create
writeit file version
```

### 📚 Compilation

```bash
writeit compile assemble
writeit compile dry-run
writeit compile compile
writeit compile build
```

### 🛠️ Help and Debugging

Display the available commands:

```bash
writeit --help
```

Display help for a command group:

```bash
writeit project --help
writeit file --help
writeit compile --help
```

Display detailed help for a specific command:

```bash
writeit project create --help
```

Use `--debug` or `-d` to display the complete Python traceback when an error occurs:

```bash
writeit project normalize . --debug
```

---

**WritΞIt** — Manage your writing like a pro.