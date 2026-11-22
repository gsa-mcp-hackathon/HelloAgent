"""Read-only SQLite inventory adapter for HelloAgent (fictional demo data)."""
import sqlite3
from pathlib import Path
from contextlib import closing

DEFAULT_DB = Path(__file__).resolve().with_name('inventory.db')


class SQLiteInventory:
    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path).resolve()

    def _query(self, sql, parameters=()):
        with closing(sqlite3.connect(self.path.as_uri() + '?mode=ro', uri=True)) as conn:
            conn.row_factory = sqlite3.Row
            conn.create_function('casefold', 1, lambda value: value.casefold() if value is not None else None)
            return [dict(row) for row in conn.execute(sql, parameters)]

    def get_application(self, application_name):
        rows = self._query('SELECT name, owner, status, technology, vendor, approval_status FROM applications WHERE name = ?', (application_name,))
        if not rows:
            return {'found': False, 'message': 'Application not found'}
        return {'found': True, **rows[0]}

    def list_applications(self):
        names = [row['name'] for row in self._query('SELECT name FROM applications ORDER BY rowid')]
        return {'count': len(names), 'applications': names}

    def list_approved_applications_by_vendor(self, vendor):
        rows = self._query('SELECT name FROM applications WHERE casefold(vendor) = ? AND casefold(approval_status) = ? ORDER BY rowid', (vendor.strip().casefold(), 'approved'))
        names = [row['name'] for row in rows]
        return {'vendor': vendor, 'count': len(names), 'applications': names}
