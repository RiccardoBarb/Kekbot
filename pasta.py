import numpy as np


def update_pasta(pasta_list, chosen_id):
    pasta_list.pop(chosen_id)
    new_pasta_id = np.asarray([i for i in range(len(pasta_list))])

    return pasta_list, new_pasta_id


def chose_pasta(pasta_list, pasta_id):
    chosen_id = np.random.choice(pasta_id)
    chosen_pasta = pasta_list[chosen_id]
    updated_list, new_pasta_id = update_pasta(pasta_list, chosen_id)

    return chosen_pasta, updated_list, new_pasta_id
