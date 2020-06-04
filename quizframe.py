import wx
import strings

class StatePanelMaker:
    def __init__(self, quiz_frame):
        self.quiz_frame = quiz_frame

    def visit(self, state):
        return state.accept(self)

    def visit_starting_state(self, state):
        return StartingStatePanel(state, self.quiz_frame)

    def visit_answer_state(self, state):
        return AnswerStatePanel(state, self.quiz_frame)

    def visit_review_state(self, state):
        return ReviewStatePanel(state, self.quiz_frame)

    def visit_final_state(self, state):
        return FinalStatePanel(state, self.quiz_frame)

class StatePanel(wx.Panel):
    def __init__(self, state, quiz_frame):
        super(StatePanel, self).__init__(parent=quiz_frame)
        self.state = state
        self.quiz_frame = quiz_frame

class StartingStatePanel(StatePanel):
    def __init__(self, state, quiz_frame):
        super(StartingStatePanel, self).__init__(state, quiz_frame)
        self.start_button = wx.Button(parent=self, label=strings.START_QUIZ_BUTTON)
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button)

    def on_start_button(self, event):
        new_state = self.state.start_quiz()
        self.quiz_frame.set_state(new_state)

class AnswerStatePanel(StatePanel):
    def __init__(self, state, quiz_frame):
        super(AnswerStatePanel, self).__init__(state, quiz_frame)
        question = state.questions[state.current_question]
        self.question_label = wx.StaticText(parent=self, label=question.text)
        
        self.buttons = []
        self.buttons_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        for answer, correct in state.questions[state.current_question].answers:
            button = wx.Button(parent=self, label=answer)
            self.buttons.append(button)
            self.buttons_sizer.Add(button, flag=wx.ALIGN_CENTER)
            button.Bind(wx.EVT_BUTTON, self.on_button)

        self.teams_queue_labels = []
        self.queue_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        
        for team in self.state.teams_queue:
            label = wx.StaticText(parent=self, label=team)
            self.teams_queue_labels.append(label)
            self.queue_sizer.Add(label, flag=wx.ALIGN_CENTER)
        
        self.main_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.main_sizer.Add(self.question_label, flag=wx.ALIGN_CENTER)
        self.main_sizer.Add(self.buttons_sizer, flag=wx.ALIGN_CENTER)
        self.main_sizer.Add(self.queue_sizer, flag=wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)

        self.bind_all_descendands(wx.EVT_CHAR_HOOK, self.on_key_down, self)
        self.SetFocus()

    def on_button(self, event):
        new_state = self.state.answer()
        self.quiz_frame.set_state(new_state)

    def bind_all_descendands(self, event_binder, handler, widget):
        widget.Bind(event_binder, handler)
        for child in widget.GetChildren():
            self.bind_all_descendands(event_binder, handler, child)

    def on_key_down(self, event):
        pressed_key = chr(event.GetKeyCode())
        new_state = self.state.queue_team(pressed_key)
        self.quiz_frame.set_state(new_state)

class ReviewStatePanel(StatePanel):
    def __init__(self, state, quiz_frame):
        super(ReviewStatePanel, self).__init__(state, quiz_frame)
        question = state.questions[state.current_question]
        self.question_label = wx.StaticText(parent=self, label=question.text)
        self.correct_label = wx.StaticText(parent=self, label=strings.CORRECT_ANSWERS)
        self.continue_button = wx.Button(parent=self, label=strings.REVIEW_BUTTON)
        
        self.answer_labels = []
        for answer, correct in question.answers:
            if correct:
                label = wx.StaticText(parent=self, label=answer)
                self.answer_labels.append(label)
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.question_label, flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.correct_label, flag=wx.ALIGN_CENTER)
        for label in self.answer_labels:
            self.sizer.Add(label, flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.continue_button, flag=wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)

        self.continue_button.Bind(wx.EVT_BUTTON, self.on_continue)

    def on_continue(self, event):
        new_state = self.state.next_question()
        self.quiz_frame.set_state(new_state)


class FinalStatePanel(StatePanel):
    def __init__(self, state, quiz_frame):
        super(FinalStatePanel, self).__init__(state, quiz_frame)
        self.end_message_label = wx.StaticText(parent=self, label=strings.END_OF_QUIZ_MESSAGE)



class QuizFrame(wx.Frame):
    def __init__(self, state):
        super(QuizFrame, self).__init__(parent=None, title=strings.QUIZ_FRAME_TITLE)
        self.state_panel_maker = StatePanelMaker(self)
        self.state = state
        self.state_panel = self.state_panel_maker.visit(state)
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.state_panel, flag=wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)

    def set_state(self, state):
        self.state = state
        self.state_panel = self.state_panel_maker.visit(state)
        self.sizer.Hide(0)
        self.sizer.Remove(0)
        self.sizer.Add(self.state_panel, flag=wx.ALIGN_CENTER)
        self.sizer.Layout()
        old_size = self.GetSize()
        needed_size = self.GetBestSize()
        result_width = max(old_size.GetWidth(), needed_size.GetWidth())
        result_height = max(old_size.GetHeight(), needed_size.GetHeight())
        result_size = wx.Size(result_width, result_height)
        self.SetSize(result_size)
