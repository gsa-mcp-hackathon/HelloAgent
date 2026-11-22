import sqlite3
from contextlib import closing
import pytest
from init_database import initialize_database
from inventory_repository import SQLiteInventory
import mcp_server as server


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / 'inventory.db'
    initialize_database(path)
    monkeypatch.setenv('HELLOAGENT_BACKEND', 'sqlite')
    monkeypatch.setenv('HELLOAGENT_DB', str(path))
    return path


def test_list(database):
    assert server.list_applications() == {'count': 2, 'applications': ['HR Portal', 'Legacy Reports']}


def test_lookup(database):
    assert server.get_application('HR Portal')['approval_status'] == 'Approved'
    assert server.get_application('Unknown')['found'] is False


@pytest.mark.parametrize('vendor', ['Microsoft', ' microsoft ', 'MICROSOFT'])
def test_approved(database, vendor):
    assert server.list_approved_applications_by_vendor(vendor)['applications'] == ['HR Portal']


@pytest.mark.parametrize('vendor', ['Oracle', "Microsoft' OR 1=1 --"])
def test_no_match(database, vendor):
    assert server.list_approved_applications_by_vendor(vendor)['count'] == 0


def test_missing_approval(database):
    with closing(sqlite3.connect(database)) as conn:
        with conn:
            conn.execute('INSERT INTO applications (name, vendor) VALUES (?, ?)', ('Unknown Approval', 'Microsoft'))
    assert server.list_approved_applications_by_vendor('Microsoft')['applications'] == ['HR Portal']


def test_read_only(database):
    with pytest.raises(sqlite3.OperationalError, match='readonly'):
        SQLiteInventory(database)._query('DELETE FROM applications')
    assert server.list_applications()['count'] == 2


def test_idempotent_initialization(database):
    initialize_database(database)
    assert server.list_applications()['count'] == 2


def test_missing_database(database, monkeypatch):
    monkeypatch.setenv('HELLOAGENT_DB', str(database.with_name('missing.db')))
    with pytest.raises(sqlite3.OperationalError):
        server.list_applications()


def test_backend_parity(database, monkeypatch):
    sqlite_results = [server.list_applications(), server.get_application('HR Portal'), server.list_approved_applications_by_vendor('Microsoft')]
    monkeypatch.setenv('HELLOAGENT_BACKEND', 'memory')
    assert sqlite_results == [server.list_applications(), server.get_application('HR Portal'), server.list_approved_applications_by_vendor('Microsoft')]
