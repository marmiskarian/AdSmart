from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

class Bandit(ABC):

    @abstractmethod
    def __init__(self, p):
        self.p = p
        self.p_estimate = 0.
        self.N = 0

    @abstractmethod
    def __repr__(self):
        return f'A bandit with {self.p} win rate.'

    @abstractmethod
    def pull(self):
        return np.random.random() < self.p

    @abstractmethod
    def update(self, x):
        self.N += 1
        self.p_estimate = ((self.N - 1)*self.p_estimate + x) / self.N

    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def plot_curves(self):
        # Visualize the performance of each bandit
        pass


    @abstractmethod
    def report(self):
        # store the data in csv
        # print the average reward: using logging package
        # print average regret: using logging package
        pass




class AdPromptBandit(Bandit):
    """
    class AdPromptBandit. 
    Represents a Ad bandit running with epsilon greedy algorithm the following attributes and methods.
    
    Attributes:
        ctr (float): The true click through rate (CTR) of the bandit.
    Methods:
        pull(): Pulls a value for the bandit.
        update(x: float): Updates the estimated CTR of the bandit.
        plot_curves(): Plots the learning process of the bandits.
        experiment(bandit_ctrs: list, num_trials: int, path_to_save: str, to_save: bool): Run the experiment with given bandits, number of trials and whether to save the results or not.
        report(path_to_save: str, to_save: bool): Prints the report of the experiment.
        create_data(): Creates the dataframe for saving
        update_epsilon(): Updates the epsilon with rate 1/t.
    
    """
    def __init__(self, ctr):
        """
        Initilizes a new instance of AdPromptBandit class with the following arguments:
        
        Args:
            ctr (float): The true CTR of the bandit. 
        
        """
        self.ctr = ctr    #True CTR
        self.ctr_estimate = 0.    #CTR estimate
        self.N = 0    #Iteration count
        self.learning_process = []    #Learning process list
        self.bandits = None    #The bandits list
        self.epsilon = 1    #Starting epsilon
        
    def pull(self):
        """
        Pulls a value for the bandit based on the true CTR (the value is pulled from normal distribution with mean = "true bandit CTR" and 0.05 std).
        
        """
        return np.random.normal(self.ctr, 0.05)     #Pull a CTR with mean actual "CTR" and std 0.05
    
    def update(self, x):
        """
        Updates the estimated CTR for the bandit based on the new, pulled value.
        
        Args:
            x (float): The new value pulled for the bandit, the value to update for the estimated CTR.
        
        """
        self.N += 1    #Add 1 to the iteration count
        self.ctr_estimate = ((self.N - 1)*self.ctr_estimate + x) / self.N    #Update the CTR estimate
        self.learning_process.append(self.ctr_estimate)    #Add the updated value to the CTR list
        
    def __repr__(self):
        return f'A bandit with actual CTR: {self.ctr} and estimated CTR {self.ctr_estimate}'
    
    def plot_curves(self):
        """
        Plots the learning curves after the experiment for the existing bandits. Creates a subplot of all the bandits learning curves.
        
        """
        if self.bandits is None:    #If no experiment was done, raise exception
            raise Exception('Run the experiment first')
        fig, axs = plt.subplots(1, 3, figsize = (15, 5))    #Create the subplots
        plt.suptitle('The learning curves of all 3 AD bandits\n', size=25)    #Add the head title for all subplots
        for index, bandit in enumerate(self.bandits):    #For each bandit plot the result
            axs[index].plot(bandit.learning_process)
            axs[index].set_title(f'True CTR of "{self.bandit_names[index]}" tone: {bandit.ctr}')
        plt.tight_layout()
        plt.show()
            
    def experiment(self, bandit_ctrs, num_trials, path_to_save='', to_save=False):
        """
        The experiment function that runs the experiment with the given bandit CTRs and number of trials.
        
        Args:
            bandit_ctrs (list): The true CTRs list of bandits.
            num_trials (int): The number of iterations to run the experiment.
            path_to_save (str): The path to save the results.
            to_save (bool): Whether to save the results or not.
            
        """
        if to_save:    #If save, create the dataframe
            self.create_data()
        self.bandits = [AdPromptBandit(ctr) for ctr in list(bandit_ctrs.values())]    #Initialize the bandit objects in the list
        self.bandit_names = list(bandit_ctrs.keys())
        self.ctrs = np.zeros(num_trials)    #Create the CTRs list
        self.regret = []   #Regret list
        for i in range(num_trials):    #Run the iterations
            if np.random.random() < self.epsilon:    #If the epsilon is enough high, than choose random bandit
                index = np.random.randint(len(self.bandits))
            else:
                index = np.argmax([b.ctr_estimate for b in self.bandits])    #If the epsilon is small, then choose the optimal bandit
            selected_bandit = self.bandits[index]    #Get the selected bandit
            x = selected_bandit.pull()    #Pull a value from the selected bandit
            if to_save:    #If save, add the pulled value to the data
                new_row = {'Bandit': index, 'CTR': x, 'Algorithm': selected_bandit.__class__.__name__}
                self.data = self.data.append(new_row, ignore_index=True)             
            self.ctrs[i] = x    #Add the result to the CTRs array
            self.regret.append(selected_bandit.ctr - x)    #Get the regret value
            selected_bandit.update(x)    #Update the estimated CTR for the bandit
            self.update_epsilon(i, num_trials)    #Update the epsilon 
        self.report(path_to_save, to_save)    #Call the report function
        return self.ctrs
    
    def report(self, path_to_save, to_save=False):
        """
        The report function that prints the report for the experiment.
        
        Args:
            path_to_save (str): The path to save the results of the experiment.
            to_save (bool): Whether to save the results or not.
        
        """
        if self.bandits is None:     #If no experiment done before, raise an exception
            raise Exception('Run the experiment first')
             
        self.plot_curves()
        if to_save:
            self.data.to_csv(path_to_save, index=False)
        
        cumulative_regrets = np.cumsum(self.regret)
        cumulative_regret = cumulative_regrets[-1]
        print(f'\nThe sum of regret for the experiment is {cumulative_regret}')
        print(f'The cumulative regret for the experiment is {cumulative_regrets}')
        
    def create_data(self):
        """
        Creates the dataset for storing the data.
        
        """
        self.data = pd.DataFrame(columns=['Bandit', 'CTR', 'Algorithm'])    #Create the dataframe for storing data
        print('The dataframe for storing data is created.')
        
    def update_epsilon(self, current_trial, num_trials):
        """
        Updates the epsilon based on the current trial and overall number of trials.
        
        Args:
            current_trial: The current trial.
            num_trials: The overall number of trials the experiment is going to run.
        """
        self.epsilon = 1 - (current_trial/num_trials)    #Update the epsilon 