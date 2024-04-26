# Neural-Network-Dependency-Parser
**Dependency Parser using Neural Networks**

**Introduction:**
This project involves training a feed-forward neural network to predict transitions for an arc-standard dependency parser. The input to the network is a representation of the current parser state, including words on the stack and buffer, and the output is a transition (shift, left_arc, right_arc) along with a dependency relation label.

**Objective:**
The main objective of this project is to implement the input representation for the neural network, decode the output of the network, specify the network architecture, and train the model using PyTorch.

**Overview of Files:**
1. **conll_reader.py:** Contains classes for representing dependency trees and reading CoNLL-X formatted data files.
2. **get_vocab.py:** Extracts a set of words and POS tags that appear in the training data to create vocabulary files.
3. **extract_training_data.py:** Extracts input/output matrices representing training data and modifies the input representation to the neural network.
4. **train_model.py:** Specifies and trains the neural network model, and saves the trained model.
5. **decoder.py:** Uses the trained model to parse input sentences and prints the parser output in CoNLL-X format.
6. **evaluate.py:** Evaluates the parser output against target dependency structures and computes labeled and unlabeled attachment accuracy.

**Dependencies:**
- PyTorch
- NumPy

**Implementation Details:**
- **Part 1:** Generating Vocabulary: Running `get_vocab.py` to create vocabulary files.
- **Part 2:** Extracting Input/Output Matrices: Implementation of the input representation and output representation methods in `extract_training_data.py`.
- **Part 3:** Designing the Network: Definition of the neural network architecture in `train_model.py`.
- **Part 4:** Training Loop: Training the model using the provided training data in `train_model.py`.
- **Part 5:** Greedy Parsing Algorithm: Implementation the parse_sentence method in `decoder.py` to parse sentences using the trained model.


**Conclusion:**
This project provides hands-on experience with building and training a neural network for dependency parsing using PyTorch. By following the instructions and implementing the required functionalities, you'll gain a deeper understanding of neural network-based NLP models and their applications in natural language processing tasks.
