import wx
import strings
import state
import quizframe
from functions import load


class TeamsFrame(wx.Frame):
    def __init__(self):
        self.teams = []
        self.waitingTeamForKey = None
        super(TeamsFrame, self).__init__(parent=None, title=strings.TEAMS_SETTINGS)
        self.panel = wx.Panel(self)

        self.first_row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self.panel, label=strings.ADD_TEAM_BUTTON)
        self.add_button.Bind(wx.EVT_BUTTON, lambda x: self.addRow())
        self.add_button.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.first_row_sizer.Add(self.add_button)
        self.confirm_button = wx.Button(self.panel, label=strings.CONFIRM_TEAMS_BUTTON)
        self.confirm_button.Bind(wx.EVT_BUTTON, self.start)
        self.first_row_sizer.Add(self.confirm_button)

        self.rows_sizer = wx.BoxSizer(wx.VERTICAL)
        self.rows_sizer.Add(self.first_row_sizer)

        self.panel.SetSizer(self.rows_sizer, True)
        self.addDefaultRows()

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.panel)
        self.SetSizerAndFit(self.main_sizer)

        self.SetFocus()

    def start(self, event):
        answer, warning = self.team_names_entered()
        if answer:
            self.Destroy()
            s = state.StartingState(load(), self.getTeams())
            frame = quizframe.QuizFrame(s)
            frame.Show()
        else:
            wx.MessageBox(warning)

    def team_names_entered(self):
        names = [item[0].GetValue() for item in self.teams]
        if '' in names:
            return False, strings.EMPTY_TEAM_NAME_WARNING
        if len(names) != len(set(names)):
            return False, strings.TEAM_NAME_DUPLICITY_WARNING
        return True, None

    def addDefaultRows(self):
        for i in range(3):
            self.addRow()

    def addRow(self):
        team_char = self.getUnusedChar()
        team_index = len(self.teams)
        row = wx.BoxSizer(wx.HORIZONTAL)
        team_name_input = wx.TextCtrl(self.panel, size=(300, 25))
        team_name_input.SetValue(strings.TEAM_PLACEHOLDER + str(team_index))
        team_name_input.SetHint(strings.EMPTY_NAME_PLACEHOLDER)
        team_name_input.SetModified(True)
        team_name_input.SetEditable(True)
        team_char_id = wx.StaticText(self.panel, label=strings.TEAM_CHAR_SHOW + team_char)
        assign_key_button = wx.Button(self.panel, label=strings.ASSIGN_KEY)
        assign_key_button.Bind(wx.EVT_BUTTON, lambda x: self.getCharForTeam(team_index))
        row.Add(team_name_input, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        row.Add(assign_key_button, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        row.Add(team_char_id, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.teams.append((team_name_input, team_char_id, team_char))
        self.rows_sizer.Add(row)
        self.panel.SetSizerAndFit(self.rows_sizer, True)
        self.Fit()

    def getCharForTeam(self, team_index):
        team_name_input, team_char_id, team_char = self.teams[team_index]
        busy = wx.BusyInfo(f'{strings.PRESS_KEY_MESSAGE} {team_name_input.GetValue()}\n{strings.PRESS_KEY_INFO}', self)
        self.waitingTeamForKey = team_index
        self.add_button.SetFocus()

    def getUnusedChar(self):
        for char in range(ord('A'), ord('Z') + 1):
            if not self.isUsedChar(chr(char)):
                return chr(char)
        raise RuntimeError(strings.NOT_EXIST_FREE_CHARACTER)

    def isUsedChar(self, input_char):
        for _, _, team_char in self.teams:
            if team_char == input_char:
                return True
        return False

    def on_key_down(self, event):
        pressed_key = chr(event.GetKeyCode()).upper()
        if self.waitingTeamForKey is not None:
            self.tryAssignKey(self.waitingTeamForKey, pressed_key)
            self.waitingTeamForKey = None

    def tryAssignKey(self, team_index, new_team_char):
        if not self.isUsedChar(new_team_char):
            team_name_input, team_char_id, team_char = self.teams[team_index]
            team_char = new_team_char
            team_char_id.SetLabelText(strings.TEAM_CHAR_SHOW + team_char)
            self.teams[team_index] = (team_name_input, team_char_id, team_char)
            wx.MessageBox(strings.CHAR_CHANGE_SUCCESS, "Oznam", wx.OK)
            return
        wx.MessageBox(strings.CHAR_CHANGE_ABORT, "Oznam", wx.OK)

    def getTeams(self):
        teams = {}
        for team_name_input, team_char_id, team_char in self.teams:
            teams[team_char] = team_name_input.GetValue()
        return teams
