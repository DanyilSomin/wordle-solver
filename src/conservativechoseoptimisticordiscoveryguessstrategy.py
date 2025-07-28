from choseoptimisticordiscoveryguessstrategy import ChoseOptmisticOrDiscoveryStrategy

class ConservativeChoseOptmisticOrDiscoveryStrategy(ChoseOptmisticOrDiscoveryStrategy):

    def go_optimistic(self, game_state, optimistic_guess_amount, discover_guess_amount) -> bool:
        enough_guesses = optimistic_guess_amount < 5 - len(game_state.rows)
        discover_guess_exist = discover_guess_amount > 0

        return enough_guesses or not discover_guess_exist