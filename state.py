from abc import ABC, abstractmethod

class QuizState(ABC):
    def __init__(self, questions, teams, current_question=None):
        self.questions = questions
        self.teams = teams
        self.current_question = current_question

    @abstractmethod
    def accept(self, visitor):
        pass

class ContinuationState(QuizState):
    def __init__(self, previous_state):
        questions = previous_state.questions
        teams = previous_state.teams
        current_question = previous_state.current_question
        super(ContinuationState, self).__init__(questions, teams, current_question)

    @abstractmethod
    def accept(self, visitor):
        pass

class StartingState(QuizState):
    def __init__(self, questions, teams):
        super(StartingState, self).__init__(questions, teams)

    def start_quiz(self):
        return AnswerState(self, 0)

    def accept(self, visitor):
        return visitor.visit_starting_state(self)

class AnswerState(ContinuationState):
    def __init__(self, previous_state, current_question, teams_queue=()):
        super(AnswerState, self).__init__(previous_state)
        self.current_question = current_question
        self.teams_queue = teams_queue

    def queue_team(self, key):
        if key not in self.teams:
            return self
        team = self.teams[key]
        if team in self.teams_queue:
            return self
        new_queue = self.teams_queue + (team,)
        return AnswerState(self, self.current_question, new_queue)

    def answer(self):
        return ReviewState(self)

    def accept(self, visitor):
        return visitor.visit_answer_state(self)

class ReviewState(ContinuationState):
    def next_question(self):
        if self.current_question + 1 >= len(self.questions):
            return FinalState(self)
        return AnswerState(self, self.current_question+1)

    def accept(self, visitor):
        return visitor.visit_review_state(self)

class FinalState(ContinuationState):
    def accept(self, visitor):
        return visitor.visit_final_state(self)
