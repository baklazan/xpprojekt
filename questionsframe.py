import wx
import strings
from question import Question
from functions import load, save

QUESTIONS_FILENAME = 'questions.pickle'

class QuestionsFrame(wx.Frame):

    def __init__(self):
        super(QuestionsFrame, self).__init__(parent=None, title=strings.CREATE_QUESTION)
        self.panel = wx.Panel(self)
        self.fields = {}
        self.rows_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_btn = wx.Button(self.panel, pos=(5, 10), label=strings.ADD_QUESTION)
        self.add_btn.Bind(wx.EVT_BUTTON, self.add_question)
        self.rows_sizer.Add(self.add_btn)
        self.create_question_inputs()
        self.panel.SetSizerAndFit(self.rows_sizer, True)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel)
        self.SetSizerAndFit(self.sizer)

    def create_question_inputs(self):
        row = wx.BoxSizer(wx.HORIZONTAL)
        question_input = wx.TextCtrl(self.panel, size=(300, 25))
        question_input.SetHint(strings.QUESTION_NAME)
        question_input.SetModified(True)
        question_input.SetEditable(True)
        row.Add(question_input, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.rows_sizer.Add(row)
        self.fields['question'] = question_input
        for i in range(4):
            row = wx.BoxSizer(wx.HORIZONTAL)
            choice = wx.TextCtrl(self.panel, size=(150, 25))
            choice.SetHint(strings.ANSWER + ' ' + str(i + 1))
            choice.SetEditable(True)
            check_box = wx.CheckBox(self.panel)
            row.Add(choice, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
            row.Add(check_box, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
            self.rows_sizer.Add(row)
            self.fields['answer ' + str(i)] = (choice, check_box)

    def add_question(self, evt):
        question_text = self.fields['question'].GetValue()
        if question_text == '':
            wx.MessageBox(strings.EMPTY_QUESTION_NAME)
            return
        answers = []
        correct = []
        for key, value in list(self.fields.items())[1:]:
            choice, box = [x.GetValue() for x in value]
            answers.append(choice)
            correct.append(box)
            if answers[-1] == '':
                wx.MessageBox(strings.EMPTY_QUESTION_CHOICE)
                return
        if len(answers) != len(set(answers)):
            wx.MessageBox(strings.ANSWERS_NOT_UNIQUE)
            return
        if True not in correct:
            wx.MessageBox(strings.NO_CORRECT)
            return
        choice_tuples = list(zip(answers, correct))
        q = Question(question_text, answers=choice_tuples)

        self.fields['question'].SetValue('')
        for key, value in list(self.fields.items())[1:]:
            choice, box = value
            choice.SetValue('')
            box.SetValue(False)

        self.save_question(q)

    @staticmethod
    def save_question(q):
        try:
            data = load(QUESTIONS_FILENAME)
        except FileNotFoundError:
            data = []
        data.append(q)
        save(QUESTIONS_FILENAME, data)
