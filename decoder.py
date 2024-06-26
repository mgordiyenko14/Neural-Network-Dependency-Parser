import sys
import copy

import numpy as np
import torch

from conll_reader import DependencyStructure, DependencyEdge, conll_reader
from extract_training_data import FeatureExtractor, State
from train_model import DependencyModel

class Parser(object):

    def __init__(self, extractor, modelfile):
        self.extractor = extractor

        # Create a new model and load the parameters
        self.model = DependencyModel(len(extractor.word_vocab), len(extractor.output_labels))
        self.model.load_state_dict(torch.load(modelfile))
        sys.stderr.write("Done loading model") #why stderr?

        # The following dictionary from indices to output actions will be useful
        # same infor as in extractor.output_labels, but keys and values are swapped: (relation, transition)
        self.output_labels = dict([(index, action) for (action, index) in extractor.output_labels.items()])

    def parse_sentence(self, words, pos):

        state = State(range(1,len(words)))
        state.stack.append(0)

        # TODO: Write the body of this loop for part 5
        while state.buffer:
            features = self.extractor.get_input_representation(words, pos, state) # these are the features, right?
            # print("features ",features)
            tensor = torch.tensor(features)
            tensor_probs = self.model(tensor)# retrieve the predictions
            probs = tensor_probs.detach().numpy()[0]
            # print(len(probs))
            indexed_probs = list(enumerate(probs))
            sorted_probs = sorted(indexed_probs, key=lambda x: x[1], reverse=True) # sorts in decreasing ordder based on the probaility
            for action_ind, prob in sorted_probs: 
                action = self.output_labels[action_ind][0]
                if (self.islegal(state, action, pos)==True):
                    label = self.output_labels[action_ind][1]
                    self.executeAction(state, action, label)
                    break

        result = DependencyStructure()
        for p,c,r in state.deps:
            result.add_deprel(DependencyEdge(c,words[c],pos[c],p, r))
        return result
    
    def islegal(self, state, action, pos):
        if action== "shift": # shifting with the correct label always
            if (len(state.buffer) == 1 and len(state.stack) != 0):
                # print("false shift")
                return False
        elif action == "left_arc":
            if len(state.stack) == 0 or (state.stack[-1]==0): #
                # print("false left")
                return False
        elif action== "right_arc":
            if len(state.stack) == 0 or len(state.buffer)==0:
                # print("false right")
                return False
        return True

    def executeAction(self, state, action, label):#try label-1
        if action == "shift":
            state.shift()
        elif action == "left_arc":
            state.left_arc(label)
        elif action == "right_arc":
            state.right_arc(label)

if __name__ == "__main__":

    WORD_VOCAB_FILE = 'data/words.vocab'
    POS_VOCAB_FILE = 'data/pos.vocab'

    try:
        word_vocab_f = open(WORD_VOCAB_FILE,'r')
        pos_vocab_f = open(POS_VOCAB_FILE,'r')
    except FileNotFoundError:
        print("Could not find vocabulary files {} and {}".format(WORD_VOCAB_FILE, POS_VOCAB_FILE))
        sys.exit(1)

    extractor = FeatureExtractor(word_vocab_f, pos_vocab_f)
    parser = Parser(extractor, sys.argv[1])

    with open(sys.argv[2],'r') as in_file:
        for dtree in conll_reader(in_file):
            words = dtree.words()
            pos = dtree.pos()
            deps = parser.parse_sentence(words, pos)
            print(deps.print_conll())
            print()
