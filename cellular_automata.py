import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def apply_rule(rule, state, pos):
    left = state[pos - 1]
    center = state[pos]
    right = state[(pos + 1) % len(state)]
    return 1 - rule[left * 4 + center * 2 + right] 

def evolve(rule, initial_state, steps):
    state = initial_state.copy()
    history = [state.copy()]
    
    for _ in range(steps):
        new_state = np.zeros_like(state)
        for i in range(len(state)):
            new_state[i] = apply_rule(rule, state, i)
        state = new_state
        history.append(state.copy())
    
    return history

def animate_cellular_automaton(rule, initial_state, steps):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_axis_off()

    history = evolve(rule, initial_state, steps)
    
    im = ax.imshow(history, cmap="binary", interpolation="nearest", animated=True)

    def update(frame):
        im.set_array(history[:frame+5])
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(history), blit=True)
    plt.show()

rule45 = np.array([0, 0, 1, 0, 1, 1, 0, 1], dtype=int)

initial_state = np.zeros(501, dtype=int)
initial_state[250] = 1 

steps = 250

animate_cellular_automaton(rule45, initial_state, steps)
