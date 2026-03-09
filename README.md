# SExAI — Search Engine x AI

Originally a Proof of Concept linked to [this article](https://enzolenair.fr/2025/01/19/SExAI/SExAI/), SExAI has grown into a small CLI tool that combines FOFA search engine queries with a local LLM to detect hacking tools exposed in open directories.

---

## How it works

1. **FOFA query** — The tool prompts you for a FOFA query (e.g. `product="SimpleHTTP" && title="for /" && "CVE"`). It fetches the matching IP/port pairs.

2. **HTML body retrieval** — For each result, SExAI fetches the HTTP response body of the open directory.

3. **LLM analysis** — The body is sent to a local Ollama model of your choice. The model acts as a cybersecurity specialist and identifies hacking tools, CVE files, exploits, or any suspicious content present in the directory.

---

## Requirements

- Python 3.x
- [Ollama](https://ollama.com) running locally (`ollama serve`)
- A FOFA account with API access
- Dependencies: see `requirements.txt`

---

## Usage

```bash
python3 PoC.py
```

On first run, you will be prompted for your FOFA credentials. These are stored securely in **GNOME Keyring** and never written to disk.

Each run then asks:
- **FOFA query** — the search query to run against FOFA
- **Ollama model** — the local model to use for analysis (e.g. `huihui_ai/baronllm-abliterated:latest`)

Leaving either prompt empty exits the program.

---

## Credentials

Credentials are stored in GNOME Keyring under the service name `sexai`. You can view or delete them using [Seahorse](https://wiki.gnome.org/Apps/Seahorse).
