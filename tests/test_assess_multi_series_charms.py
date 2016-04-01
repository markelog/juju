"""Tests for assess_multi_series_charms module."""

import logging
from mock import Mock, patch
import os
import StringIO
import yaml

from assess_multi_series_charms import (assess_multi_series_charms,
                                        parse_args,
                                        main,
                                        make_charm, )
from tests import (parse_error, TestCase, )
from utility import temp_dir


class TestParseArgs(TestCase):
    def test_common_args(self):
        args = parse_args(["an-env", "/bin/juju", "/tmp/logs", "an-env-mod"])
        self.assertEqual("an-env", args.env)
        self.assertEqual("/bin/juju", args.juju_bin)
        self.assertEqual("/tmp/logs", args.logs)
        self.assertEqual("an-env-mod", args.temp_env_name)
        self.assertEqual(False, args.debug)

    def test_help(self):
        fake_stdout = StringIO.StringIO()
        with parse_error(self) as fake_stderr:
            with patch("sys.stdout", fake_stdout):
                parse_args(["--help"])
        self.assertEqual("", fake_stderr.getvalue())
        self.assertNotIn("TODO", fake_stdout.getvalue())


class TestMain(TestCase):
    def test_main(self):
        argv = ["an-env", "/bin/juju", "/tmp/logs", "an-env-mod", "--verbose"]
        env = object()
        client = Mock(spec=["is_jes_enabled"])
        with patch("assess_multi_series_charms.configure_logging",
                   autospec=True) as mock_cl:
            with patch("assess_multi_series_charms.BootstrapManager."
                       "booted_context",
                       autospec=True) as mock_bc:
                with patch("jujupy.SimpleEnvironment.from_config",
                           return_value=env) as mock_e:
                    with patch("jujupy.EnvJujuClient.by_version",
                               return_value=client) as mock_c:
                        with patch("assess_multi_series_charms."
                                   "assess_multi_series_charms",
                                   autospec=True) as mock_assess:
                            main(argv)
        mock_cl.assert_called_once_with(logging.DEBUG)
        mock_e.assert_called_once_with("an-env")
        mock_c.assert_called_once_with(env, "/bin/juju", debug=False)
        self.assertEqual(mock_bc.call_count, 1)
        mock_assess.assert_called_once_with(client)


class TestAssess(TestCase):
    def test_multi_series_charms(self):
        mock_client = Mock(spec=["juju", "wait_for_started"])
        assess_multi_series_charms(mock_client)
        mock_client.juju.assert_called_once_with('deploy',
                                                 ('local:trusty/my-charm', ))
        mock_client.wait_for_started.assert_called_once_with()
        self.assertNotIn("TODO", self.log_stream.getvalue())


class TestMakeCharm(TestCase):
    def test_make_charm(self):
        with temp_dir() as charm_dir:
            make_charm(charm_dir, "2.0", name="foo")
            metadata = os.path.join(charm_dir, 'metadata.yaml')
            with open(metadata, 'r') as f:
                content = yaml.load(f)
        self.assertEqual(content['name'], 'foo')
        self.assertEqual(content['min-juju-version'], '2.0')
        self.assertEqual(content['summary'], 'summary')
