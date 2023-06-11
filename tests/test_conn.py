import pytest
from airflow.models import Connection


def test_connection():
    conn = Connection(
        conn_id="smartix_default",
        conn_type="http",
        host="https://example.com",
        login="user",
        password="s3cr3t",
    )
    assert conn.host
    assert conn.conn_type == "http"
