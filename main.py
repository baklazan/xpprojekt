import wx
import state
import question
import quizframe

questions = (question.Question('Koľko je dva a tri?'),
             question.Question('Ste robot?'),
             question.Question('Byť, či nebyť?'),
             question.Question('Otázka života, vesmíru a všetkého.'))

teams = {'A': 'tím 1',
         'S': 'tím 2',
         'D': 'tím 3',
         'F': 'tím 4'}

state = state.StartingState(questions, teams)
app = wx.App()
frame = quizframe.QuizFrame(state)
frame.Show()
app.MainLoop()
