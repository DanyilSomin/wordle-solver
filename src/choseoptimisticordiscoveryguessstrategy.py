from abc import ABC, abstractmethod

class ChoseOptmisticOrDiscoveryStrategy(ABC):
    @abstractmethod
    def go_optimistic(self, game_state, optimistic_guess_amount, discover_guess_amount) -> bool:
        """
        Return if the next guess has to be optimistic or discovery.
        Optimistic guess ensures green letters ane in place.
        Discovery guess goes for the best word not taking the greens into account.
        """
        pass