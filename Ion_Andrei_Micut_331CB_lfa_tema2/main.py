# Micut Andrei-Ion
# Grupa 331CB

import sys
from nfa import NFA
from dfa import DFA
from io import StringIO
from itertools import product


def textToNFA(text):
	def build_delta(transitions):
		delta = {}
		alphabet = set()
		for transition in transitions:
			elems = transition.split()
			delta[(int(elems[0]), elems[1])] = set([int(x) for x in elems[2:]])
			alphabet.add(elems[1])

		return delta, alphabet

	lines = text.splitlines()
	final_states = set(int(s) for s in lines[1].split())
	delta, alphabet = build_delta(lines[2:])
	states = set(range(0, int(lines[0])))

	return NFA(alphabet, states, 0, final_states, delta)

def DFAtoText(dfa):
	text = StringIO()
	line = "{}\n".format(len(dfa.states))
	text.write(line)
	line = " ".join([str(x) for x in dfa.final_states]) + "\n"
	text.write(line)
	for key, value in dfa.delta.items():
		line = "{} {} {}".format(key[0], key[1], value) + "\n"
		text.write(line)
	return text.getvalue()

def NFAtoDFA(nfa):
	SINK_STATE = -1
	states = []
	dfaStates = set()
	queue = []
	delta = {}
	nfa_to_dfa_states = {}
	dfa_final_states = set()
	dfa_alphabet = nfa.alphabet
	dfa_alphabet.discard("eps")
	lastState = 0

	start_states = EpsilonClosure({nfa.start_state}, nfa, set())

	nfa_to_dfa_states[frozenset(start_states)] = lastState
	dfaStates.add(lastState)
	lastState += 1

	for final_state in nfa.final_states:
		if final_state in start_states:
			dfa_final_states.add(nfa_to_dfa_states[frozenset(start_states)])
			break

	states.append(start_states)
	queue.append(start_states)
	while bool(queue):
		nfaState = queue.pop()
		for symbol in dfa_alphabet:
			newState = set()
			for s in nfaState:
				try:
					newState = newState.union(nfa.delta[(s, symbol)])
				except:
					pass
			if not newState:
				continue
			newState = EpsilonClosure(newState, nfa, set())
			if not (newState in states):
				queue.append(newState)
				states.append(newState)
				nfa_to_dfa_states[frozenset(newState)] = lastState
				dfaStates.add(lastState)
				lastState += 1
			for orice in nfa.final_states:
				if orice in newState:
					dfa_final_states.add(nfa_to_dfa_states[frozenset(newState)])
					break;
			delta[(nfa_to_dfa_states[frozenset(nfaState)], str(symbol))] = nfa_to_dfa_states[frozenset(newState)]

	all_transitions = (product(list(dfaStates), dfa_alphabet))
	not_present_trans = filter(lambda x: x not in delta, all_transitions)
	has_sink_state = False
	for trans in not_present_trans:
		has_sink_state = True
		delta[trans] = SINK_STATE
	if has_sink_state is True:
		dfaStates.add(SINK_STATE)
		for s in dfa_alphabet:
			delta[(SINK_STATE, str(s))] = SINK_STATE

	return DFA(dfa_alphabet, dfaStates, nfa_to_dfa_states[frozenset(start_states)], dfa_final_states, delta)

def EpsilonClosure(states, nfa, known):
	res = states
	for state in states:
		try:
			next_states = nfa.delta[(state, "eps")]
		except KeyError:
			continue
		diff = next_states - known
		if bool(diff):
			res = res.union(diff)
			known = known.union(diff)
			res = res.union(EpsilonClosure(diff, nfa, known))
	return res



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Syntax: python3 {} <input-file> <output-file>".format(sys.argv[0]))
		exit(-1)

	input_filename = sys.argv[1]
	output_filename = sys.argv[2]

	with open(input_filename, "r") as file_in:
		nfa = textToNFA(file_in.read())

	dfa_text = DFAtoText(NFAtoDFA(nfa))

	with open(output_filename, "w") as file_out:
		file_out.write(dfa_text)