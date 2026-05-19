#!/usr/bin/env python3
"""Wait until PostgreSQL host resolves and accepts connections."""
from __future__ import annotations

import os
import socket
import sys
import time
from urllib.parse import urlparse

try:
    import psycopg2
except ImportError:
    psycopg2 = None  # type: ignore


def get_host_port() -> tuple[str, int]:
    url = os.environ.get("DATABASE_URL", "postgresql://paybuddy:paybuddy@db:5432/paybuddy")
    parsed = urlparse(url)
    host = parsed.hostname or "db"
    port = parsed.port or 5432
    return host, port


def wait_for_dns(host: str, timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            socket.getaddrinfo(host, None)
            print(f"Resolved database host: {host}")
            return
        except socket.gaierror:
            print(f"Waiting for DNS: {host} ...", flush=True)
            time.sleep(2)
    raise TimeoutError(
        f"Could not resolve database host '{host}' within {timeout}s. "
        "If you run the API on your machine (not in Docker), set "
        "DATABASE_URL=postgresql://paybuddy:paybuddy@localhost:5432/paybuddy"
    )


def wait_for_postgres(host: str, port: int, timeout: int = 60) -> None:
    if psycopg2 is None:
        print("psycopg2 not available, skipping TCP check")
        return

    url = os.environ.get("DATABASE_URL", "")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            conn = psycopg2.connect(url, connect_timeout=3)
            conn.close()
            print("PostgreSQL is ready")
            return
        except Exception as exc:
            print(f"Waiting for PostgreSQL at {host}:{port} ... ({exc})", flush=True)
            time.sleep(2)
    raise TimeoutError(f"PostgreSQL at {host}:{port} not ready within {timeout}s")


def main() -> None:
    host, port = get_host_port()
    wait_for_dns(host)
    wait_for_postgres(host, port)


if __name__ == "__main__":
    try:
        main()
    except TimeoutError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
