import util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # get mdp states
        states = self.mdp.getStates()

        # iterate through iterations
        for i in range(self.iterations):
            valueCopy = self.values.copy()
            for state in states:
                # init for value
                value = None
                # get possible actions
                actions = self.mdp.getPossibleActions(state)
                #iterate through possible actions
                for action in actions:
                    # get the old computed Value
                    computedValue = self.computeQValueFromValues(state, action)
                    if value is None or value < computedValue:
                        value = computedValue
                # if values is still none set it to 0
                if value is None:
                    value = 0
                valueCopy[state] = value

            self.values = valueCopy




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        # get transition states and the probabilitess
        transitionStates = self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, probability in transitionStates:
            # qValue = prob * (reward + (discount * state value))
            qValue += probability * (self.mdp.getReward(state, action, nextState) + (self.discount * self.getValue(nextState)))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # get possible actions
        actions = self.mdp.getPossibleActions(state)
        # print(actions)
        # if actions list would be empty return none, otherwise go further
        if len(actions) == 0:
            return None

        computedAction = None
        maxValue = None
        # iterate actions
        for action in actions:
            # get calculated QValue
            calcQValue = self.computeQValueFromValues(state, action)
            # print(calcQValue)
            if maxValue is None or maxValue < calcQValue:
                maxValue = calcQValue
                computedAction = action

        # return computed action
        return computedAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
