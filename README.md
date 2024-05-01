# Google Phishield AI Extension

> Google Phishield AI Extension is a phishing detection tool created using the Google AI Gemini LLM model. It analyzes potentially phishing emails based on server configuration, email language, links analysis, and file scan analysis using the VirusTotal API.

# 📝 Features

Analyzes emails for phishing indicators that utilizes Google AI Gemini LLM model for analysis.

Integrated with VirusTotal API for file scan analysis.

# 🧾 Requirements

> To run this project, you'll need:

1. [Docker](https://docs.docker.com/get-docker/)
2. [Visual Studio Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. [Google AI API Key](https://ai.google.dev/gemini-api/docs/api-key)
4. [VirusTotal API Key](https://docs.virustotal.com/docs/please-give-me-an-api-key)

# ▶️ Getting Started

1. Clone the repository.

```
git clone git@github.com:JumpingDino/phishingAI.git
```

2. Copy the [.env.dist](https://github.com/JumpingDino/phishingAI/blob/master/.env.dist) file and create a <b>.env</b> file filling your environment variables

3. Open the project in Visual Studio Code.

4. Install the Dev Containers extension if not already installed.

5. Open your local folder containing the repo with Dev Containers

> more information about how to open with containers can be found [here](https://code.visualstudio.com/docs/devcontainers/tutorial)
>
# 💻 Usage

1. Open the repository folder with Dev Containers
2. Access the API endpoints to analyze emails for phishing indicators.

To restart the services simply use the following commands:

```bash
docker compose restart backend
```

```bash
docker compose restart worker
```

For developers who prefer to work with PM2 for managing processes, an alternative method is provided. By stopping the Docker containers and utilizing PM2, you can streamline the development process. Simply run the following commands:

```bash
pm2 start .devcontainer/pm2.json
pm2 logs
pm2 logs api
pm2 logs worker
```

# 👍 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## 🚀 Technologies

This project was built using the following technologies:

- [FastAPI](https://fastapi.tiangolo.com)
- [Google AI](https://ai.google)
- [VirusTotal API](https://docs.virustotal.com)

## 📄 Licensing

This repository is MIT licensed, as found in the [LICENSE][l] file.

[l]: https://github.com/JumpingDino/phishingAI/blob/master/LICENSE
