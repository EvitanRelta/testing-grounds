import itertools
import multiprocessing
import time

import deepzono_nodes as dn
import numpy as np
from elina_scalar import *
from elina_dimension import *
from elina_linexpr0 import *
from elina_abstract0 import *
from fppoly import *
from fconv import *

from config import config


def encode_kactivation_cons(nn, man, element, offset, layerno, length, lbi, ubi, constraint_groups, need_pop, domain,
                            activation_type, K=3, s=-2, approx=True):
    if need_pop:
        constraint_groups.pop()

    lbi = np.asarray(lbi, dtype=np.double)
    ubi = np.asarray(ubi, dtype=np.double)

    if activation_type == "ReLU":
        kact_args = sparse_heuristic_with_cutoff(length, lbi, ubi, K=K, s=s)
    else:
        kact_args = sparse_heuristic_curve(length, lbi, ubi, activation_type == "Sigmoid", s=s)

    kact_cons = []
    tdim = ElinaDim(offset + length)
    if domain == "refinezono":
        element = dn.add_dimensions(man, element, offset + length, 1)

    KAct.man = man
    KAct.element = element
    KAct.tdim = tdim
    KAct.length = length
    KAct.layerno = layerno
    KAct.offset = offset
    KAct.domain = domain
    KAct.type = activation_type

    if domain == "refinezono":
        with multiprocessing.Pool(config.numproc) as pool:
            input_hrep_array = pool.map(get_ineqs_zono, kact_args)
        with multiprocessing.Pool(config.numproc) as pool:
            kact_results = pool.starmap(
                make_kactivation_obj,
                zip(input_hrep_array, [approx] * len(input_hrep_array)),
            )
    else:
        total_size = 0
        for var_ids in kact_args:
            size = 3 ** len(var_ids) - 1
            total_size = total_size + size

        linexpr0 = elina_linexpr0_array_alloc(total_size)
        i = 0
        for var_ids in kact_args:
            for coeffs in itertools.product([-1, 0, 1], repeat=len(var_ids)):
                if all(c == 0 for c in coeffs):
                    continue
                linexpr0[i] = generate_linexpr0(offset, var_ids, coeffs)
                i += 1
        upper_bounds = get_upper_bound_for_linexpr0(man, element, linexpr0, total_size, layerno)

        i = 0
        input_hrep_array = []
        for var_ids in kact_args:
            input_hrep = []
            for coeffs in itertools.product([-1, 0, 1], repeat=len(var_ids)):
                if all(c == 0 for c in coeffs):
                    continue
                input_hrep.append([upper_bounds[i]] + [-c for c in coeffs])
                i += 1
            input_hrep_array.append(input_hrep)
        with multiprocessing.Pool(config.numproc) as pool:
            kact_results = pool.starmap(
                make_kactivation_obj,
                zip(input_hrep_array, [approx] * len(input_hrep_array)),
            )

    for gid, inst in enumerate(kact_results):
        inst.varsid = kact_args[gid]
        kact_cons.append(inst)

    if domain == "refinezono":
        element = dn.remove_dimensions(man, element, offset + length, 1)

    constraint_groups.append(kact_cons)
