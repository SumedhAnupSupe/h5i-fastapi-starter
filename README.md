# FastAPI + h5i Starter

A small FastAPI application with a simple HTML page, designed to run inside an [h5i](https://github.com/h5i-dev/h5i) box.

The page has one button. Clicking it calls `/api/hello` and displays the returned message in the page.

## Project structure

```text
.
├── .h5i/
│   └── env.toml
├── app/
│   ├── index.html
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Linux
- h5i built from a current version that supports the profiles used below
- Python 3 with `venv` available inside the h5i box

Dependencies are installed with `pip` into a virtual environment **inside the box**. The project intentionally keeps the dependency workflow to `pip` + `venv`.

## 1. Browser workflow: process isolation

This is the convenient workflow for opening the page in your normal browser. The process-tier profile uses the host network, so the FastAPI service is available at `localhost:8000`.

From a fresh terminal, with no host project virtual environment activated:

```bash
h5i box create fastapi-demo --profile fastapi-dev
h5i box shell fastapi-demo
```

Inside the box, create the virtual environment using the system Python:

```bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Alternatively, because `service.api` is declared for this profile, the service can be started by h5i:

```bash
exit
h5i box service start fastapi-demo api
h5i box ports fastapi-demo
```

Open the displayed port, under DECLARED, normally:

```text
http://localhost:8000
```

Click **Call API**. The page calls `/api/hello` and displays the response.

### Why process isolation is used here

This workflow trades network scoping for convenience. The profile uses `net.mode = "host"`, so the box shares the host's network. This makes the FastAPI service directly reachable from the normal browser through `localhost:8000`.

## 2. Scoped workflow: supervised isolation + box share

The supervised profile keeps the server in the box's own network namespace. It also allows only the package hosts required for installing the Python dependencies:

- `pypi.org`
- `files.pythonhosted.org`

Create and enter the box:

```bash
h5i box create fastapi-demo --profile fastapi
h5i box shell fastapi-demo
```

Inside the box, create and activate the virtual environment using the system Python:

```bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run FastAPI **inside this same h5i shell**:

```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Before sharing it, the API can be checked from the same shell:

```bash
curl http://127.0.0.1:8000/api/hello
```

Expected response:

```json
{"message":"FastAPI says Hi "}
```

In another host terminal, expose the running service:

```bash
h5i box share fastapi-demo --port 8000
```

Use the ticket returned by h5i:

```bash
h5i join <ticket>
```

Then open the shared address in a browser and click **Call API**.

### Why supervised isolation is used here

Unlike the process-tier workflow, the supervised box has its own network namespace. The server therefore runs inside the same h5i shell, and `h5i box share` is used when the service needs to be reached from a real browser outside the box.

## API

### `GET /`

Serves the HTML page.

### `GET /api/hello`

Returns:

```json
{"message":"FastAPI says Hi "}
```

The HTML button calls this endpoint with JavaScript and writes the returned message into the page.

## License

MIT License. See [LICENSE](LICENSE).
