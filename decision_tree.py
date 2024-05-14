import csv
import math
import json
from collections import Counter


# Class that defines a decision tree, with learning algorithm
class DecisionTree:

    def __init__(self):
        self.attributes = ["Alt", "Bar", "Fri", "Hun", "Pat", "Price", "Rain", "Res", "Type", "Est"]

    # Performs the decision tree algorithm, based on the input examples, attributes
    def learn_decision_tree(self, examples, attributes, parent_examples):
        if len(examples) == 0:
            return plurality_value(parent_examples)

        elif same_classification(examples):
            return examples[0][-1]
        
        elif len(attributes) == 0:
            plurality_value(examples)

        else:
            a_attribute = importance(examples, attributes, self.attributes)
            print("Splitting by : " + self.attributes[a_attribute])
            tree = {self.attributes[a_attribute]: {}}

            examples_a = [] # a list of values from the examples based on a_attribute
            for example in examples:
                if example[a_attribute] not in examples_a:
                    examples_a.append(example[a_attribute])

            for value in examples_a:
                # examples with the same value from a_attribute
                exs = [example for example in examples if example[a_attribute] == value]

                # getting subtree using examples with same value for a_attribute, using attributes minus a_attribute
                subtree = self.learn_decision_tree(exs, [attribute for attribute in attributes if attribute
                                                         != a_attribute], examples)
                tree[self.attributes[a_attribute]][value] = subtree
            return tree


# Function that checks the most important attribute among a group of attributes
def importance(examples, attributes, attribute_names):
    importance_map = {}
    output_importance_map = []
    for attribute in attributes:
        importance_map[attribute] = information_gain(examples, attribute)

    for key in importance_map:
        output_importance_map.append(str(attribute_names[key]) + ": " + str(importance_map[key]))

    print("\n" + ", ".join(output_importance_map))

    return max(importance_map, key=importance_map.get)


# Calculates the information gain of a single attribute
def information_gain(examples, attribute):
    entropy = 0.0
    attribute_values = {}
    # print(attribute)
    # print(examples)
    for example in examples:
        if example[attribute] not in attribute_values:
            attribute_values[example[attribute]] = []
            attribute_values[example[attribute]].append(example)
        else:
            attribute_values[example[attribute]].append(example)
    # print(attribute_values.keys())
    for key in attribute_values:
        q = len(attribute_values[key]) / len(examples)
        outputs = [example[-1] for example in attribute_values[key]]
        output_count = Counter(outputs)
        entropy += (q * get_entropy(output_count["Yes"] / len(attribute_values[key])))

    return 1 - entropy


# Calculates the entropy of a boolean variable
def get_entropy(q):
    if q <= 0 or q >= 1:
        return 0  # Return 0 for q outside the valid range
    return -1 * ((q * math.log(q, 2)) + ((1 - q) * math.log(1 - q, 2)))


# Calculates the plurality value, or the most common output from the examples
def plurality_value(examples):
    outputs = {}
    for example in examples:
        if example[-1] not in outputs:
            outputs[example[-1]] = 1
        else:
            outputs[example[-1]] += 1

    return max(outputs.values())


# Checks if all the examples have the same classification
def same_classification(examples):
    classification = examples[0][-1]
    for example in examples:
        if classification != example[-1]:
            return False
    return True


# Prints the decision tree in a formatted way
def print_tree(tree):
    print("\nFinal Tree:")
    print(json.dumps(tree, indent=2, sort_keys=True))


# Parses the .csv file into a list of examples
def parse_file(input_filename):
    examples = []
    with open(input_filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            example = []
            for value in row:
                example.append(value.strip())
            examples.append(example)

    return examples


if __name__ == "__main__":
    input_examples = parse_file("restaurant.csv")   # parsing .csv file
    decision_tree = DecisionTree()  # creating decision tree
    result_tree = decision_tree.learn_decision_tree(input_examples, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], None)
    print_tree(result_tree)
