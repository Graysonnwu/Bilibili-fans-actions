import datetime
from pathlib import Path
import tempfile
import unittest

from bilibili import BEIJING, fetch_followers, record_observation, validate_uid


class Response:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class Session:
    def __init__(self, payload):
        self.payload = payload

    def get(self, url, **kwargs):
        assert kwargs['timeout'] == (5, 20)
        assert kwargs['params']['vmid'] == '123'
        return Response(self.payload)


class ObservationTests(unittest.TestCase):
    def test_api_error_and_invalid_counts_are_not_observations(self):
        for payload in [{'code': -412, 'data': None}, {'code': 0, 'data': None},
                        {'code': 0, 'data': {'follower': -1}},
                        {'code': 0, 'data': {'follower': '123'}},
                        {'code': 0, 'data': {'follower': True}}]:
            with self.assertRaises(ValueError):
                fetch_followers('123', Session(payload))
        self.assertEqual(fetch_followers('123', Session({'code': 0, 'data': {'follower': 0}})), 0)

    def test_manual_and_scheduled_runs_use_beijing_date(self):
        moment = datetime.datetime(2026, 10, 3, 17, tzinfo=datetime.timezone.utc)
        self.assertEqual(moment.astimezone(BEIJING).date().isoformat(), '2026-10-04')

    def test_same_day_is_replaced_and_csv_newest_first(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record_observation('123', '2026-10-02', 10, root)
            record_observation('123', '2026-10-03', 12, root)
            record_observation('123', '2026-10-03', 13, root)
            self.assertEqual((root / '123.txt').read_text(), '2026-10-02,10\n2026-10-03,13\n')
            self.assertEqual((root / '123.csv').read_text(), 'date,follower\n2026-10-03,13\n2026-10-02,10\n')
            self.assertEqual(len(list(root.iterdir())), 2)

    def test_invalid_history_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '123.txt').write_text('broken record\n')
            with self.assertRaises(ValueError):
                record_observation('123', '2026-10-03', 13, root)
            self.assertEqual((root / '123.txt').read_text(), 'broken record\n')
            self.assertFalse((root / '123.csv').exists())

    def test_uid_cannot_escape_data_directory(self):
        for value in ['../secret', '', '０１２', '0', '-2']:
            with self.assertRaises(ValueError):
                validate_uid(value)


if __name__ == '__main__':
    unittest.main()
