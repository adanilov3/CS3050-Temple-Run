class HighScores:
    def __init__(self, filename="high_scores.txt"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, "r") as file:
                scores = [line.strip() for line in file]
            return [int(score) for score in scores]
        except FileNotFoundError:
            return [0]

    def save_scores(self):
        with open(self.filename, "w") as file:
            for score in self.scores:
                file.write(str(score) + "\n")

    def add_score(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)  # Sort in descending order
        self.scores = self.scores[:10]  # Keep only the top 10 scores
        self.save_scores()

    def get_high_score(self):
        return self.scores[0]
