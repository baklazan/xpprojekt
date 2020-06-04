import os
import wx
import teamsframe
import quizframe
from functions import load

app = wx.App()

if os.path.exists(quizframe.HISTORY_FILENAME) and os.path.isfile(quizframe.HISTORY_FILENAME):
    history = load(quizframe.HISTORY_FILENAME)
    frame = quizframe.QuizFrame(history)
else:
    frame = teamsframe.TeamsFrame()
frame.Show()
app.MainLoop()
