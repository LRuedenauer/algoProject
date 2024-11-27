# Definiert die Klasse Agent
# TODO für die Zukunft: muss noch geschrieben werden. erste ANsätze aus dem Bereich Dynamische Programmierung, wobei die
# Methode "some_utility_function" der Knackpunkt sein wird
# TODO: Diese Datei noch nicht raus geben


class Agent:
    # *** CONSTRUCTORS ***
    def __init__(self, id):
        """

        :param id: id of auction
        """
        self._id = id

        self.winning_bid = 0

    # *** PUBLIC SET methods ***



    # *** PUBLIC methods ***



    # *** PUBLIC GET methods ***



    # *** PUBLIC STATIC methods ***



    # *** PRIVATE methods ***

    def gebotsagent(self, n, max_budget, max_bid):
        # Initialisiere die DP-Tabelle
        dp = [[[0 for _ in range(max_budget + 1)] for _ in range(max_bid + 1)] for _ in range(n + 1)]

        # Basisfall: Am Ende der letzten Runde
        for b in range(max_bid + 1):
            for r in range(max_budget + 1):
                dp[n][b][r] = self.final_evaluation(b, r)

        # Fülle die DP-Tabelle rückwärts
        for i in range(n - 1, 0, -1):
            for b in range(max_bid + 1):
                for r in range(max_budget + 1):
                    dp[i][b][r] = dp[i + 1][b][r]  # Nicht bieten
                    for b_new in range(b + 1, max_bid + 1):
                        if r >= (b_new - b):
                            dp[i][b][r] = max(dp[i][b][r], dp[i + 1][b_new][r - (b_new - b)] + self.f(b_new, i))

        # Der optimale Startzustand
        return dp[1][0][max_budget]

    def final_evaluation(self, b, r):
        # Bewertet den Endzustand der Auktion
        return 1 if b >= self.winning_bid else 0  # 1 = gewonnen, 0 = verloren

    @staticmethod
    def f(b, i):
        # Bewertet den Nutzen eines Gebots in Runde i
        return some_utility_function(b, i)

    # *** PUBLIC methods to return class properties ***



    # *** PRIVATE variables ***


