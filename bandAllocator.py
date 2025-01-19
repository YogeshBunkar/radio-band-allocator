import logging

# set log level
logging.basicConfig(level=logging.INFO)


class BandAllocator:

    def __init__(self):

        self.states = []
        self.adjacents = {}

        self.max_neighbours_state = ""

        self.state_band = {}
        self.back_track_counter = 0

        self.bands = ["A", "B", "C", "D"]


    # update the possible neighbours band for legacy constraint states
    def prune_domains(self, state, band, domains):

        for adjacent_state in self.adjacents[state]:
            
            bands = domains[adjacent_state]

            if band in bands:
                bands.remove(band)
            if  len(bands) == 0:
                return []

            domains[adjacent_state] = bands

        return domains
            

    
    def forward_check(self, assigned_states, domains, available_states):


        if len(assigned_states) == len(self.states):

            return assigned_states

        most_constraint_state = self.get_most_constraint_state(available_states, domains)


        current_domain = domains[most_constraint_state]

        neighbour_domains = {}

        for neighbour in self.adjacents[most_constraint_state]:

            neighbour_domains[neighbour] = domains[neighbour][:]

        for band in current_domain:

            prunned = self.prune_domains(most_constraint_state, band, domains)

            if len(prunned) > 0:
                assigned_states.append(most_constraint_state)
                
                self.state_band[most_constraint_state] = band
                available_states.remove(most_constraint_state)
                
                result = self.forward_check(assigned_states, prunned, available_states)

                if not result:

                    available_states.append(most_constraint_state)
                    assigned_states.remove(most_constraint_state)
                    
                    self.state_band.pop(most_constraint_state)
                    self.back_track_counter +=1
                else:
                    return result

            for neighbour in neighbour_domains.keys():
                domains[neighbour] =neighbour_domains[neighbour][:]

        return False


    # returns most constraint state to do band assignement
    def get_most_constraint_state(self, available_states, domains):

        if len(available_states) == len(self.states):
            return self.max_neighbours_state

        min_domain_states = []
        min_size = 50

        for state in available_states:

            if len(domains[state]) < min_size:
                
                min_domain_states = [state]
                min_size = len(domains[state])
            elif len(domains[state]) == min_size:

                min_domain_states.append(state)

        max_neighbours_state = ""
        max_neighbours = -1

        for  state in min_domain_states:

            neighbours = self.adjacents[state]

            if max_neighbours < len(neighbours):

                max_neighbours = len(neighbours)
                max_neighbours_state = state

        return max_neighbours_state

    #checks the output and will return false if any of the state and neighbour has same frequency
    def is_consistent(self):

        output = ""

        for state in self.state_band.keys():

            band = self.state_band[state]
            
            output += "\n" + state + " " + band

            for neighbour in self.adjacents[state]:

                neighbour_band = self.state_band[neighbour]

                output += "\t" + neighbour + " " + neighbour_band

                if band == neighbour_band:
                    print("ERROR", state + " " + neighbour)
                    return False

        return True
    
    # prints solution 
    def printSolution(self):

        logging.debug("Frequency assignment is consistent : " + str(self.is_consistent()))

        with open("output.txt", "w") as file:

            for state in list(self.state_band):
                file.write("%s\n" % (state + " " + self.state_band.pop(state)))
            
        print("Number of backtracks: "+str(self.back_track_counter))





