class Team:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.color

    @staticmethod
    def get_by_color(teams, color):
        return next((team for team in teams if team.color == color))