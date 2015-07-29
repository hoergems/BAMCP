import numpy as np
from scipy.stats import rv_discrete 

class State:
    def __init__(self, name, children=None):
        self.name=name
        self.children = children
        
    def set_children(self, children):
        self.children = children
        
    def sample_child(self, model):        
        values = [i for i in xrange(len(self.children))]
        probabilities = [model.get_probability(self, self.children[i]) for i in xrange(len(self.children))]
        distrib = rv_discrete(values=(range(len(values)), probabilities))
        d = distrib.rvs(size=1)[0]
                       
        return self.children[d]       

class Model:
    def __init__(self, name):
        self.name = name
        self.prob_ = {}
        
    def set_probability(self, state1, state2, probability):
        self.prob_[(state1.name, state2.name)] = probability        
        
    def get_probability(self, state1, state2):
        return self.prob_[(state1.name, state2.name)]

class Test:
    def __init__(self):        
        self.gen_models()        
        sampled_ps = []
        self.ns = []
        
        state_count = [0, 0]  
        n = 0     
        for i in xrange(10000):
            sampled_ps.append(self.sample_model())            
            '''sampled_ps.append(self.sample_model())
            state = self.sample_state(sampled_ps[-1])            
            if state.name == "s2":
                self.ns.append(sampled_ps[-1])           
                print self.get_p_estimate(self.ns)'''
            last_state = self.sample_step(sampled_ps[-1])
            print last_state.name
                
    def sample_step(self, model):
        state1 = self.states[0].sample_child(model) 
        
        state2 = state1.sample_child(model)
        return state2
        
    def get_p_estimate(self, ns):
        sum = 0.0
        for i in xrange(len(ns)):
            if ns[i].name == "P0":
                sum += 1.0
        return sum / len(ns)
        
    def gen_models(self):
        self.models = []
        self.models.append(Model("P0"))
        self.models.append(Model("P1"))
        
        self.states = [State("root"),
                       State("s0"), 
                       State("s1"), 
                       State("s2"), 
                       State("s3"),
                       State("s4"),
                       State("s5")]
        self.states[0].set_children([self.states[1], self.states[2]])
        self.states[1].set_children([self.states[3], self.states[4]])
        self.states[2].set_children([self.states[5], self.states[6]])
        
        self.models[0].set_probability(self.states[0], self.states[1], 0.8)
        self.models[0].set_probability(self.states[0], self.states[2], 0.2)
        self.models[0].set_probability(self.states[1], self.states[3], 0.8)
        self.models[0].set_probability(self.states[1], self.states[4], 0.2)
        self.models[0].set_probability(self.states[2], self.states[5], 0.1)
        self.models[0].set_probability(self.states[2], self.states[6], 0.9)
        
        self.models[1].set_probability(self.states[0], self.states[1], 0.4)
        self.models[1].set_probability(self.states[0], self.states[2], 0.6)
        self.models[1].set_probability(self.states[1], self.states[3], 0.2)
        self.models[1].set_probability(self.states[1], self.states[4], 0.8)
        self.models[1].set_probability(self.states[2], self.states[5], 0.9)
        self.models[1].set_probability(self.states[2], self.states[6], 0.1)       
        
        
    def sample_model(self):
        values = [1, 2]
        probabilities = [0.5, 0.5]
        distrib = rv_discrete(values=(range(len(values)), probabilities))
        d = distrib.rvs(size=1)[0]        
        if d == 0:
            return self.models[0]
        return self.models[1]        
    
    def sample_state(self, model):
        values = [1, 2]
        probabilities_1 = [model.get_probability(self.states[0], self.states[1]), 
                           model.get_probability(self.states[0], self.states[1])]
        
        distrib = rv_discrete(values=(range(len(values)), probabilities))
        d = distrib.rvs(size=1)[0]        
        if d == 0:
            next_state = self.states[1]
        return self.states[2]        
        
if __name__ == "__main__":
    Test()