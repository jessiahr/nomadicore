# Nomadicore - Offline Knowledge Base

Nomadicore is a versatile, containerized project designed to provide offline access to a variety of resources, tools, and documentation. It leverages Docker to deploy and manage services such as Kiwix (for offline web content), JupyterLab (for data analysis and computation), Calibre-Web (for managing eBooks), and more. This project is ideal for environments with limited or no internet connectivity, enabling users to access essential resources and tools locally.

## Features

- **Kiwix**: Access offline versions of websites and documentation, including Stack Exchange, FreeCodeCamp, DevDocs, and more.
- **JupyterLab**: Perform data analysis and computation in an interactive environment.
- **Calibre-Web**: Manage and read eBooks offline.
- **Obsidian**: Manage and edit markdown-based notes.
- **OpenWebUI**: A web-based interface for managing AI models and tools.
- **Tileserver**: Serve map tiles for offline geographic applications.
  
## TODO
- [X] UI for discovering and managing Kiwix `.zim` files
- [X] CPU stats UI
- [ ] Setup tool
  - [ ] Download default model
  - [ ] Dowload default `.zims`
  - [ ] Show `.zim` size and mark if already downloaded
  - [ ] Ability to restart services from UI
- [ ] Authentication & ACL


## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Basic familiarity with Docker and containerized applications.

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jessiahr/nomadicore.git
   cd nomadicore
2. Start the services using Docker Compose:
```bash
docker compose up
```
3. Navigate to `http://localhost:80` for the service directory