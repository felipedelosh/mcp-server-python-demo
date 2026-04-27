<h1 align="center"> FelipedelosH </h1>
<br>
<h4>MCP SERVER DEMO</h4>

![Banner](Docs/banner.png)
<br>
:construction: Status of project :construction:
<br><br>
This project is a small example of an MCP server (Model Context Protocol) written in Python.
The server runs inside a Docker container and gives Claude Desktop. 
Claude Desktop can call this tool by talking to the Docker container through a standard input/output connection (stdio).
The server does not use the internet or a web server – it just waits for Claude to send a message and replies with a greeting.

This is the first step to build bigger tools, like managing users or points.

## :hammer:Funtions:

- `Function 1`: Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.<br>
- `Function 2`: Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.<br>
- `Function 3`: Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.<br>
- `Function 3a`: Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.<br>
- `Function 4`: Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.<br>

# Architecture

```
rappi_mcp_project/
│
├── Docs/                           # Documentation and other files
│   └── init.sql                    # Table creation script
│   └── (other files: diagrams, explanations, etc.)
│
├── mcp-server/
│   ├── Dockerfile                   # To containerize the Python MCP server
│   ├── pyproject.toml               # Project configuration (dependencies, script)
│   └── main.py                      # MCP server code (tools)
│
├── docker-compose.yml               # Only for the Python service (your database runs separately)
├── .env                             # Environment variables (Postgres connection)
└── README.md                        # Full instructions
```

## :play_or_pause_button:How to execute a project

0. Prepare the database (First, start a PostgreSQL container and create tables Docs/DATABASE/init.sql)

1. Make sure you have Docker installed and running on your machine.

2. Build and start the MCP server container from the project root:
```
docker-compose up --build
```
3. Configure Claude Desktop to talk to the MCP server:
```
%APPDATA%\Claude\claude_desktop_config.json
```

```
{
  "mcpServers": {
    "rappi-demo": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "C:\\full\\path\\to\\your\\docker-compose.yml",
        "run",
        "--rm",
        "-i",
        "mcp-server"
      ]
    }
  }
}
```

4. Test the connection by asking Claude:
```
Use the saludar tool with the name 'Claude'.
```
You should receive a response like: "¡Hola, Claude!"

## :hammer_and_wrench: Tech.

- Python 3.11+
- Docker & Docker Compose
- MCP & FastMCP 
- PostgreSQL
- psycopg2-binary

## :warning:Warning.

- Claude Desktop dependency – The server only works with Claude Desktop via stdio. It cannot be used as a standalone web API or with other MCP clients without modification.
- Windows‑specific paths – Configuration examples are written for Windows (%APPDATA%\Claude); users on macOS or Linux need to adapt the configuration file location.
- Manual configuration – The user must manually edit claude_desktop_config.json; there is no automated setup script.
- No multi‑server support – The demo connects only one MCP server to Claude Desktop.

## Autor

| [<img src="https://avatars.githubusercontent.com/u/38327255?v=4" width=115><br><sub>Andrés Felipe Hernánez</sub>](https://github.com/felipedelosh)|
| :---: |