from bandAllocator import BandAllocator


adjacent_states_file_name = "adjacent-states.txt"
constraint_file_name = "legacy-constraints.txt"

# reads adjacent state file and append all the states in band_allocator object with adjacent states and maximum neighbouring state name
def read_adjacent_state_file(band_allocator):

    max_neighbours_state = ""
    max_neighbours = 0

    with open(adjacent_states_file_name, "r") as file:
        
        for adjacent_states_line in file:

            states = adjacent_states_line.split()
            key = states.pop(0)

            band_allocator.states.append(key)
            values = states
            band_allocator.adjacents[key] = values

            if max_neighbours < len(values):
                
                max_neighbours = len(values)
                max_neighbours_state = key

    #state with maximum adjacent states
    band_allocator.max_neighbours_state = max_neighbours_state
    


def read_legacy_constraint_file(band_allocator, domains, assigned_states):

    with open(constraint_file_name, "r") as file:

        for constraint_line in file:

            if not constraint_line.strip():
                break
            
            constraint =constraint_line.split()

            state = constraint[0]
            band = constraint[1]

            band_allocator.state_band[state] = band
            domains[state] = [band]
            assigned_states.append(state)
            



def main():

    band_allocator = BandAllocator()

    read_adjacent_state_file(band_allocator)


    # mapping each state will all possible bands
    domains = {state: ['A', 'B', 'C', 'D'] for state in band_allocator.states}
    
    assigned_states = []

    read_legacy_constraint_file(band_allocator, domains, assigned_states)

    for state in list(band_allocator.state_band):
        band_allocator.prune_domains(state, band_allocator.state_band[state], domains)

    result = band_allocator.forward_check(assigned_states, domains, list(set(band_allocator.states[:]) - set(assigned_states)))

    if result:
        band_allocator.printSolution()
    else:
        print("No assignment possible")        


if __name__ == "__main__":
    main()
