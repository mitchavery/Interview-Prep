"""Python Script for a CLI tool to automate registration into Wipeout Platform."""
from __future__ import print_function

import collections
import os
import re
import time

from google3.google.devtools.issuetracker.v1 import issuetracker_builders
from google3.google.devtools.issuetracker.v1 import issuetracker_client
from google3.privacy.wipeout.dashboard.util import wipeout_service_integration_tool_prompts
from google3.devtools.piper.contrib.python.piper_api_wrapper import piper_api_wrapper
from google3.pyglib import app
from google3.pyglib import flags
from google3.pyglib import gfile
from google3.security.ganpati.client import ganpati1_client
from google3.security.ganpati.client import names

ISSUE_TRACKER_API_KEY = 'AIzaSyCXv6IF4SxCh0N5LZ6zmM8yQifwXLepBbA'
GAIA_CONFIG_FILE = 'privacy/wipeout/dashboard/config/wipeout_config_data.gcl'
GAIA_CONFIG_FILE_DEPOT_PATH = '//depot/google3/' + GAIA_CONFIG_FILE
LINE = ('-' * 85)
BUG_ID = 98563
BUG_ASSIGNEE = 'carrb@google.com'

FLAGS = flags.FLAGS
FLAGS.set_default('ganpati_service', ganpati1_client.GANPATI_SERVICE_PROD)


class Color(object):
  """Class to store colors to be used in CLI text."""
  red_text = '\033[91m'
  bold_text = '\033[1m'
  yellow_text = '\033[93m'
  blue_text = '\033[94m'
  end_text = '\033[0m'


class PromptsValidators(object):
  """Class to store fields and prompts to user in dictionaries.

    Use this to create prompt objects stored as dict values in CLI_tool class.
  """

  def __init__(self, questions, validators):
    self._questions = questions
    self._validators = validators

  def DoPrompt(self, input_dict, field):
    """Prompts the user for input."""
    data = raw_input(self._questions).strip()
    print(LINE)
    if data.lower() == 'quit':
      exit('PROGRAM EXITED')
    input_dict[field] = data
    return all(validator(data, field) for validator in self._validators)


class CLITool(object):
  """CLI tool class to create prompt dictionary, gather input, and create a Buganizer ticket.

    Contains validation funtions on each invidual field.
  """
  cloud_entities = {
      1: 'GAIA events',
      2: 'Cloud Projects',
      3: 'Cloud Flexible Resources',
      4: 'Cloud Folders',
      5: 'placer'
  }
  storage_systems = {
      1: 'bigtable',
      2: 'blobstore',
      3: 'chronicle',
      4: 'colussus',
      5: 'kansas',
      6: 'placer',
      7: 'sawmill',
      8: 'spanner',
      9: 'OTHER'
  }
  non_standard_accounts = {
      1: 'SIDEWINDER',
      2: 'UNICORN_CHILD',
      3: 'OFF-NETWORK'
  }

  def __init__(self, piper_wrapper=None):
    self._piper = piper_wrapper
    self.input_data = collections.OrderedDict()
    self.prompts = collections.OrderedDict()
    self.prompts['display_name'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.SERVICE_NAME, [
            self.ValidateRequiredQuestions,
            self.CorrectServiceNameAndAddIntegrationMethod
        ])
    self.prompts['retention_plan_id'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.RETENTION_PLAN,
        [self.ValidateRequiredQuestions, self.ValidateRetentionPlan])
    self.prompts['wipeout_contacts'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.WIPEOUT_CONTACTS,
        [self.ValidateRequiredQuestions, self.GetEmailsForContacts])
    self.prompts['bug_component_id'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.BUG_COMPONENT_ID,
        [self.ValidateIsNum])
    self.prompts['bug_priority'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.BUG_PRIORITY,
        [self.ValidateBugPriority])
    self.prompts['bug_hotlist_id'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.BUG_HOTLIST_ID,
        [self.ValidateIsNum])
    self.prompts['UDCS'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.UDCS,
        [self.ValidateRequiredQuestions, self.UpdateContactsForUDCS])
    self.prompts['removable_service_flag'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.REMOVABLE_SERVICE_FLAG,
        [self.AppendService])
    self.prompts['filter_by_service_flag'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.FILTER_BY_SERVICE_FLAG,
        [self.AppendService])
    self.prompts['mdb_groups'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.MDB_GROUPS,
        [self.ValidateRequiredQuestions, self.UpdateMDBForUDCS])
    self.prompts['notifier'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.NOTIFIER,
        [self.ValidateRequiredQuestions, self.ValidateYesNo])
    self.prompts['cloud_entities'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.CLOUD_ENTITIES,
        [self.ValidateCloudNotifier])
    self.prompts['blade_target'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.BLADE_TARGET,
        [self.ValidateBladeTarget])
    self.prompts['api_max_qps'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.API_MAX_QPS,
        [self.ValidateApiMaxQps])
    self.prompts['notifier_date'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.NOTIFIER_DATE,
        [self.ValidateNotifierDate])
    self.prompts['bug_assignee'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.BUG_ASSIGNEE,
        [self.ValidateBugAssignee])
    self.prompts['permitted_account_types'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.PERMITTED_ACCOUNT_TYPES,
        [self.AddNonStandard])
    self.prompts['cloud_canonical_product'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.CLOUD_CANONICAL_PRODUCT,
        [self.EmptyFunct])
    self.prompts['wipeout_policy'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.WIPEOUT_POLICY,
        [self.ValidateRequiredQuestions, self.ValidateWipeoutPolicy])
    self.prompts['reporting_mdb'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.REPORTING_MDB,
        [self.ValidateRequiredQuestions, self.CheckMDB])
    self.prompts['mail_cl'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.MAIL_CL,
        [self.ValidateRequiredQuestions, self.ValidateYesNo])
    self.prompts['reviewers_for_cl'] = PromptsValidators(
        wipeout_service_integration_tool_prompts.REVIEWERS_FOR_CL,
        [self.GetEmailsForContacts])

  def Prompt(self):
    notifier_list = [
        'cloud_entities', 'blade_target', 'api_max_qps', 'notifier_date'
    ]
    print(wipeout_service_integration_tool_prompts.PROMPT)
    print(LINE)
    for field, prompt in self.prompts.items():
      success = False
      if field in notifier_list and not self.input_data['notifier']:
        pass
      else:
        while not success:
          success = prompt.DoPrompt(self.input_data, field)
    print(wipeout_service_integration_tool_prompts.SUCCESS)

  def NotNoneOrEmpty(self, input_string):
    return input_string and input_string.lower() != 'none'

  def CorrectServiceNameAndAddIntegrationMethod(self, unused_argv,
                                                unused_argv2):
    """Adds a hyphen between spaces in service name, make sure display name is same.

    Also adds the integration method = FEED to the data entry.
    Returns:
      True
    """
    self.input_data['service_name'] = self.input_data['display_name'].lower(
    ).replace(' ', '-')
    self.input_data['integration_method'] = 'FEED'
    return True

  def ValidateApiMaxQps(self, input_string, field):
    if self.input_data['notifier']:
      if not self.NotNoneOrEmpty(input_string):
        print(Color.red_text + 'Required for Notifier' + Color.end_text)
        return False
      if not input_string.isdigit():
        print(Color.red_text + 'Please enter a number' + Color.end_text)
        return False
      else:
        self.input_data[field] = int(input_string)
        return True
    return True

  def ValidateGoogleUser(self, input_string):
    try:
      if ganpati1_client.UserExists(
          input_string.lower()) or ganpati1_client.GroupExists(
              input_string.lower()):
        return True
      print(Color.red_text + input_string + ' is invalid' + Color.end_text)
      return False
    except names.Error as e:
      print(Color.red_text + 'Error {}'.format(e) + Color.end_text)

  def ValidateIsGoogleGroupNotUser(self, input_string):
    try:
      if not ganpati1_client.UserExists(input_string.lower()):
        if ganpati1_client.GroupExists(input_string.lower()):
          return True
      print(Color.red_text + input_string + ' is invalid' + Color.end_text)
      return False
    except names.Error as e:
      print(Color.red_text + 'Error {}'.format(e) + Color.end_text)

  def ValidateBugAssignee(self, input_string, field):
    error_message = (
        Color.red_text +
        'Must include a bug assignee since no bug component ID was specified' +
        Color.end_text)
    if self.input_data['bug_component_id']:
      return True
    if not self.NotNoneOrEmpty(input_string):
      print(error_message)
      return False
    input_string = self.GetEmail(input_string)
    if self.ValidateGoogleUser(input_string):
      self.input_data[field] = input_string
      return True

  def CheckStr(self, input_string):
    """Checks required prompts are answered and answer isn't none.

    Args:
      input_string: user input data

    Returns:
      True if valid
      False if not valid
    """
    if not input_string.strip():
      return False
    else:
      return True

  def ValidateRequiredQuestions(self, input_string, unused_argv):
    """Checks required prompts are answered and answer isn't none.

    Args:
      input_string: user input data

    Returns:
      True if valid
      False if not valid
    """
    error_message = (Color.red_text + 'Required' + Color.end_text)
    if not self.NotNoneOrEmpty(input_string):
      print(error_message)
      return False
    return True

  def SplitByComma(self, input_string):
    """Ensures there is a number at retention plan URL, splits by comma, adds to list.

    Args:
      input_string: user input data

    Returns:
       input string as a list
    """
    return [s.strip() for s in input_string.split(',')]

  def GetEmailsForContacts(self, input_string, field):
    new_list = []
    input_string = self.SplitByComma(input_string)
    for ldap in input_string:
      if self.CheckMDBPrefix(ldap):
        ldap = ldap[4:]
      if not self.ValidateGoogleUser(ldap.lstrip().split('@')[0]):
        return False
      if self.ValidateIsGoogleGroupNotUser(ldap.lstrip().split('@')[0]):
        ldap = 'mdb.' + ldap
      new_list.append(ldap)
    self.input_data[field] = new_list
    return True

  def CheckNums(self, input_str):
    """Checks if the inputted string contains any digits."""
    return any(char.isdigit() for char in input_str)

  def ValidateRetentionPlan(self, input_string, field):
    """Ensures there is a number at retention plan URL, splits by comma, adds to list.

    Args:
      input_string: user input data
      field: key in dictionary

    Returns:
      True if valid
      False if not valid
    """
    error_message = (
        Color.red_text +
        'Please include full userdata.corp.google.com links to retention plans'
        + Color.end_text)
    self.input_data[field] = []
    new_list = []
    for elem in self.SplitByComma(input_string):
      match = None
      if elem.startswith(
          'https://userdata.corp.google.com/retention/plan/detail/'):
        match = re.match(
            r'(?:http(?:s)?://)?userdata.corp.google.com/retention/plan/detail/(\d+)',
            elem)
      if elem.startswith('http://go/retention-plan/'):
        match = re.match(r'(?:http(?:)?://)?go/retention-plan/(\d+)', elem)
      new_list.append(match)
    for nums in new_list:
      if not nums:
        print(error_message)
        return False
      else:
        self.input_data[field].append(int(nums.group(1)))
    return True

  def ValidateBugPriority(self, input_string, field):
    """Checks that user enters in a number for a new bug priority and correctly.

    Args:
      input_string: user input data
      field: bug priority key

    Returns:
      True if valid
      False if not valid
    """
    bug_priority = {1: 'P1', 2: 'P2', 3: 'P3'}
    if self.NotNoneOrEmpty(input_string):
      if input_string.isdigit() and int(input_string) in bug_priority:
        for num, prior in bug_priority.items():
          if num == int(input_string):
            self.input_data[field] = prior
      else:
        error_message = (
            Color.red_text +
            'Please enter one number either 1 = P1, 2 = P2 or 3 = P3' +
            Color.end_text)
        print(error_message)
        return False
    return True

  def ValidateBladeTarget(self, input_string, field):
    """Validates that the entered value for blade target is a string and starts with gslb: or blade:.

    Args:
      input_string: string for blade target entered
      field: key in dictionary

    Returns:
      True if valid, false if not
    """
    if self.input_data['notifier']:
      if not self.NotNoneOrEmpty(input_string):
        print(Color.red_text + 'Required for Notifier' + Color.end_text)
        return False
      if input_string.startswith('gslb:'):
        self.input_data[field] = input_string[5:]
      if input_string.startswith('blade:'):
        self.input_data[field] = input_string[6:]
    return True

  def ValidateNotifierDate(self, input_string, field):
    date = True
    if self.input_data['notifier']:
      if not self.NotNoneOrEmpty(input_string):
        print(Color.red_text + 'Required for Notifier' + Color.end_text)
        return False
      try:
        time.strptime(input_string, '%Y/%m/%d')
        self.input_data[field] = input_string
      except ValueError:
        print(Color.red_text + 'Date is not valid' + Color.end_text)
        date = False
    return date

  def ValidateIsNum(self, input_string, field):
    """Checks that user enters in a number, prompts them to enter one if not.

    Args:
      input_string: user input data
      field: key in dictionary

    Returns:
      True if valid
      False if not valid
    """
    error_message = (Color.red_text + 'Please enter a number' + Color.end_text)
    if self.NotNoneOrEmpty(input_string):
      if not input_string.isdigit():
        print(error_message)
        return False
      else:
        self.input_data[field] = int(input_string)
    return True

  def UpdateContactsForUDCS(self, input_string, field):
    """If answer to using UDCS is Yes, then appends proper contacts to contacts list."""

    if self.ValidateYesNo(input_string, field):
      if self.input_data['UDCS']:
        self.input_data['wipeout_contacts'].append('udcs-wipeout-alerts')
      return True

  def ValidateYesNo(self, input_string, field):
    """Ensures that input entered is either yes, no, y, n.

        If not, continously prompts user to enter until provided.
    Args:
      input_string: user input data
      field: key in dictionary

    Returns:
      True if valid
      False if not valid
    """
    if self.NotNoneOrEmpty(input_string):
      check_string_yes_no = input_string.lower()
      if check_string_yes_no not in ['yes', 'no', 'y', 'n']:
        error_message = (
            Color.red_text + 'Please enter [y/N]: ' + Color.end_text)
        print(error_message)
        return False
      else:
        self.input_data[field] = check_string_yes_no in ['yes', 'y']
    return True

  def AppendService(self, input_string, field):
    """Turns service flag field into list and appends string input to it.

    Args:
      input_string: user input data
      field: key in dictionary

    Returns:
      True to satisfy conditional while loop
    """
    if self.NotNoneOrEmpty(input_string):
      new_list = []
      new_list.append(str(input_string).upper())
      self.input_data[field] = new_list
    return True

  def UpdateMDBForUDCS(self, input_string, field):
    """"If a client team is using UDCS, we want to add the UDCS-relevant MDB groups so that the UDCS groups can write feeds on behalf of the client."""

    input_string = self.SplitByComma(input_string)
    if self.CheckAllMDBValues(input_string, field):
      if self.input_data['UDCS']:
        self.input_data['mdb_groups'].append('udcs-wipeout-prod')
      return True

  def CheckAllMDBValues(self, values, field):
    """Checks each value in list is a valid MDB group."""
    mdb = False
    new_list = []
    try:
      for mdb_group in values:
        if ' ' in mdb_group:
          mdb_group = mdb_group.replace(' ', '')
        if self.CheckMDBPrefix(mdb_group):
          mdb_group = mdb_group[4:]
        group = ganpati1_client.GroupExists(mdb_group.lower())
        if not group:
          print(Color.red_text + mdb_group + ' is not a valid group' +
                Color.end_text)
          return False
        else:
          new_list.append(mdb_group)
          mdb = True
    except names.Error as e:
      print('Error {}'.format(e))
      return False
    if mdb:
      self.input_data[field] = new_list
      return True

  def CheckMDBPrefix(self, input_string):
    return input_string.startswith('mdb/') or input_string.startswith('mdb.')

  def CheckMDB(self, mdb_group, field):
    """Checks that entered group is a valid MDB group."""
    try:
      if self.CheckMDBPrefix(mdb_group):
        mdb_group = mdb_group[4:]
      if ' ' in mdb_group:
        mdb_group = mdb_group.replace(' ', '')
      group = ganpati1_client.GroupExists(mdb_group.lower())
      if not group:
        print(Color.red_text + mdb_group + ' is not a valid group' +
              Color.end_text)
        return False
      else:
        self.input_data[field] = mdb_group
        return True
    except names.Error as e:
      print('Error {}'.format(e))
      return False

  def ValidateCloudNotifier(self, input_string, field):
    """Checks if user enters number 1-6 for cloud notifier.

    Args:
      input_string: data entered from user for cloud notifier
      field: key in dictionary

    Returns:
      True if valid number 1-6, false if not
    """
    if self.input_data['notifier']:
      if not self.NotNoneOrEmpty(input_string):
        print(Color.red_text + 'Required for Notifier' + Color.end_text)
        return False
      if input_string.isdigit() and int(input_string) in CLITool.cloud_entities:
        value = int(input_string)
        for num, cloud in CLITool.cloud_entities.items():
          if value == num:
            self.input_data[field] = cloud
      else:
        error_message = (
            Color.red_text + 'Please enter a number 1-5' + Color.end_text)
        print(error_message)
        return False
    return True

  def AddNonStandard(self, input_string, field):
    """Checks that user enters number 1-3 for a non standard account.

        If not, prompts them to enter until correct. Matches to the correct
        account.

    Args:
      input_string: user entered data for a non standard account
      field: key in dictionary

    Returns:
      True if 1-3, false if not
    """
    if self.NotNoneOrEmpty(input_string):
      input_string = self.SplitByComma(input_string)
      new_list = []
      if self.CheckNums(str(input_string)) and set(
          list(map(int, input_string))).issubset(CLITool.non_standard_accounts):
        for value in input_string:
          for num, account in CLITool.non_standard_accounts.items():
            int_value = int(value)
            if int_value == num:
              new_list.append(account)
        self.input_data[field] = new_list
      else:
        error_message = ('Please enter digits 1 -3')
        print(error_message)
        return False
    return True

  def ValidateWipeoutPolicy(self, input_string, field):
    """Checks that user enters a number 1-8 for their service's wipeout policy.

    Args:
      input_string: user entered data for their service's wipeout policy
      field: key in dictionary

    Returns:
      True if number 1-8, false if not
    """
    if input_string.isdigit() and int(input_string) in CLITool.storage_systems:
      value = int(input_string)
      for num, system in CLITool.storage_systems.items():
        if value == 9:
          print('Please enter a custom wipeout storage policy on this bug.')
          break
        elif value == num:
          self.input_data[field] = 'storage_delay_'
          self.input_data[field] += system
    else:
      error_message = (
          Color.red_text + 'Please enter a number 1 - 9' + Color.end_text)
      print(error_message)
      return False
    return True

  def EmptyFunct(self, unused_argv, unused_argv2):
    return True

  def SplitEmail(self, input_string, field):
    self.input_data[field] = self.GetEmail(input_string)
    return True

  def GetEmail(self, input_string):
    """Splits string by @symbol for username."""
    return input_string.split('@')[0]

  def GenerateGCL(self, input_dict):
    """Generates the string to be written to the GCL file.

    Args:
      input_dict: dictionary being read from

    Returns:
      Tuple pasted to GCL file
    """
    not_print = [
        'UDCS', 'api_max_qps', 'notifier', 'blade_target', 'cloud_entities',
        'notifier_date', 'reviewers_for_cl', 'mail_cl'
    ]
    first_space = '    '
    entry = first_space + '{\n'
    space = '      '
    for key, value in input_dict.items():
      if value and value != 'none' and value != 'None' and key not in not_print:
        if isinstance(value, (list, int)):
          entry += space + \
              '{}'.format(key) + ' = ' + str(value) + '\n'
        else:
          entry += space + '{}'.format(key) + ' = ' + repr(str(value)) + '\n'
    entry += first_space + '},\n'
    return entry

  def WordsAreAlphabeticallySorted(self, word1, word2):
    """Checks alphabetical order of two words.

    Args:
      word1: first word to be checked
      word2: second word to be checked

    Returns:
      True if word1 comes before word2 alphbetically, false if not
    """
    return word1.lower() < word2.lower()

  def FindInsertIndex(self, file_name):
    """Parses through GCL file and finds the index to insert to new section.

    Args:
      file_name: file to be used

    Returns:
      line number of insertion
    """
    line_num = 0
    with open(file_name) as file_object:
      for line in file_object:
        line_num += 1
        if 'display_name = ' in line:
          display_name = str(line.rstrip()[line.index("'"):]).replace("'", '')
          if self.WordsAreAlphabeticallySorted(self.input_data['display_name'],
                                               display_name):
            final_line = line_num
            break
    return final_line - 2

  def UpdateGCLFile(self, gcl_file):
    """Reads, updates, writes, and returns a local updated GCL file.

    Args:
     gcl_file: file path of GCL file to edit.

    Returns:
      Updated local file to be submitted to new workspace for changelist
    """
    output_file = None
    if not os.path.exists(gcl_file):
      print('Wipeout Config File Non-Exisistent')
      return
    self._piper.SyncWorkspace(
        self._piper.GetClientContext(os.getenv('BUILD_WORKING_DIRECTORY'))
        .piper_context.workspace_id.workspace_name)
    with gfile.Open(gcl_file, 'rt') as file_object:
      read_file = file_object.readlines()
    with gfile.Open(gcl_file, 'rt') as file_object:
      read_file_2 = file_object.read()
    final_line = self.FindInsertIndex(gcl_file)
    entry = self.GenerateGCL(self.input_data)
    read_file.insert(final_line, entry)
    with gfile.Open(gcl_file, 'wt') as file_object_write:
      read_file = ''.join(read_file)
      file_object_write.write(read_file)
    with gfile.Open(gcl_file, 'rt') as file_object_read_file:
      output_file = file_object_read_file.read()
    with gfile.Open(gcl_file, 'wt') as file_object_write_file:
      file_object_write_file.write(read_file_2)
    return output_file

  def GetWorkspace(self, bug_num):
    """Gets the current CitC workspace or creates a new one if it does not exist.

    Args:
      bug_num: number of bug associated with workspace for CL

    Returns:
      Workspace name created in Piper
    """
    try:
      return self._piper.GetClientContext(
      ).piper_context.workspace_id.workspace_name
    except piper_api_wrapper.ServerReturnedNonZeroStatusError:
      workspace_name = 'Wipeout-Registration-For-Bug-{bug}-Service-{service}'.format(
          bug=bug_num, service=self.input_data['service_name'])
      workspace_description = 'Wipeout Registration Workspace For {}'.format(
          self.input_data['display_name'])
      return self._piper.CreateWorkspace(
          name=workspace_name, description=workspace_description)

  def CreateAndMailCL(self, updated_file, bug_num):
    """Creates and Mails a CL to critique.

    Args:
      updated_file: new file to write
      bug_num: bug associated with CL

    Returns:
      Cl number
      Whether successful or not
      The temp workspace created by the Piper API
    """
    try:
      temp_workspace = self.GetWorkspace(bug_num)
      self._piper.WriteFileContent(temp_workspace, GAIA_CONFIG_FILE_DEPOT_PATH,
                                   updated_file)
      cl_number = self._piper.CreateChange(
          temp_workspace,
          'Wipeout Registration for {service_name}\n\nBUG: {bug}'.format(
              service_name=self.input_data['service_name'], bug=bug_num))
      print('Changelist created at http://cr/{}'.format(cl_number))
      self._piper.AddAllEditedFilesToChange(temp_workspace, cl_number)
      self._piper.UploadChangeToCritique(temp_workspace, cl_number)
      print(Color.yellow_text + '\n----Presubmits Running----\n' +
            Color.end_text)
      if self.input_data['mail_cl']:
        self._piper.MailChange(
            temp_workspace,
            cl_number,
            reviewers=['carrb'] + self.input_data['reviewers_for_cl'])
    except piper_api_wrapper.Error as api_err:
      print('An error: {err} occurred while creating this CL.\n\n'.format(
          err=api_err))
      return None, False, None
    return cl_number, True, temp_workspace

  def CreateBugTicket(self, input_dict, client):
    """Creates the Bug ticket for the user in Wipeout queue.

    Args:
      input_dict: dictionary to create bug text from
      client: client to build with IssueTrackerClient

    Returns:
      Response from builder, not used
    """
    builder = issuetracker_builders.CreateIssueRequestBuilder(
        component_id=BUG_ID)
    builder.SetTitle('Wipeout Automation Registration for {}'.format(
        input_dict['display_name']))
    builder.SetPriority(2)
    builder.SetAssignee(BUG_ASSIGNEE)
    builder.SetStatus(2)
    entry = wipeout_service_integration_tool_prompts.CreateBugText(input_dict)
    builder.SetComment(entry)
    issue = client.stub.CreateIssue(builder.Build())
    bug = issue.issue_id
    print('Bug created at http://b/{}'.format(str(bug)))
    return str(bug)


def main(unused_argv):
  client = issuetracker_client.BuildDefault(
      use_prod=True, api_key=ISSUE_TRACKER_API_KEY)
  cli_tool = CLITool(piper_api_wrapper.GetPiperApiWrapper())
  cli_tool.Prompt()
  bug = cli_tool.CreateBugTicket(cli_tool.input_data, client)
  updated_file = cli_tool.UpdateGCLFile(GAIA_CONFIG_FILE)
  cl_number, success, temp_workspace = cli_tool.CreateAndMailCL(
      updated_file, bug)
  if success:
    wipeout_service_integration_tool_prompts.PrintEndSuccessMessage(
        bug, cl_number, temp_workspace)
  else:
    wipeout_service_integration_tool_prompts.PrintEndFailMessage(bug, cl_number)
  wipeout_service_integration_tool_prompts.PrintSurveyMessage()


if __name__ == '__main__':
  app.run(main)