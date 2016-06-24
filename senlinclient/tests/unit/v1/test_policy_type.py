# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from openstack.cluster.v1 import policy_type as sdk_policy_type
from openstack import exceptions as sdk_exc
from osc_lib import exceptions as exc

from senlinclient.tests.unit.v1 import fakes
from senlinclient.v1 import policy_type as osc_policy_type


class TestPolicyType(fakes.TestClusteringv1):
    def setUp(self):
        super(TestPolicyType, self).setUp()
        self.mock_client = self.app.client_manager.clustering


class TestPolicyTypeList(TestPolicyType):
    expected_columns = ['name']
    list_response = [
        sdk_policy_type.PolicyType({'name': 'BBB',
                                    'schema': {
                                        'foo': 'bar'}}),
        sdk_policy_type.PolicyType({'name': 'AAA',
                                    'schema': {
                                        'foo': 'bar'}}),
        sdk_policy_type.PolicyType({'name': 'CCC',
                                    'schema': {
                                        'foo': 'bar'}}),
    ]
    expected_rows = [
        ['AAA'],
        ['BBB'],
        ['CCC']
    ]

    def setUp(self):
        super(TestPolicyTypeList, self).setUp()
        self.cmd = osc_policy_type.PolicyTypeList(self.app, None)
        self.mock_client.policy_types = mock.Mock(
            return_value=self.list_response)

    def test_policy_type_list(self):
        arglist = []
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, rows = self.cmd.take_action(parsed_args)

        self.mock_client.policy_types.assert_called_with()
        self.assertEqual(self.expected_columns, columns)
        self.assertEqual(self.expected_rows, rows)


class TestPolicyTypeShow(TestPolicyType):

    response = ({'name': 'senlin.policy.deletion-1.0',
                 'schema': {
                     'foo': 'bar'}})

    def setUp(self):
        super(TestPolicyTypeShow, self).setUp()
        self.cmd = osc_policy_type.PolicyTypeShow(self.app, None)
        self.mock_client.get_policy_type = mock.Mock(
            return_value=sdk_policy_type.PolicyType(self.response)
        )

    def test_policy_type_show(self):
        arglist = ['os.heat.stack-1.0']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        self.mock_client.get_policy_type.assert_called_once_with(
            'os.heat.stack-1.0')

    def test_policy_type_show_not_found(self):
        arglist = ['senlin.policy.deletion-1.0']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.mock_client.get_policy_type.side_effect = (
            sdk_exc.ResourceNotFound())
        error = self.assertRaises(exc.CommandError, self.cmd.take_action,
                                  parsed_args)
        self.assertEqual('Policy Type not found: senlin.policy.deletion-1.0',
                         str(error))
