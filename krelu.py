from elina_scalar import *
from elina_dimension import *
from elina_linexpr0 import *
from elina_abstract0 import *
from fppoly import *
from fconv import *

import numpy as np
import time
import itertools
import multiprocessing
import math

from config import config


def encode_kactivation_cons(nn, man, element, offset, layerno, length, lbi, ubi, constraint_groups, need_pop, domain, activation_type, K=3, s=-2, approx=True):
    import deepzono_nodes as dn
    if need_pop:
        constraint_groups.pop()

    lbi = np.asarray(lbi, dtype=np.double)
    ubi = np.asarray(ubi, dtype=np.double)

    if activation_type == "ReLU":
        kact_args = sparse_heuristic_with_cutoff(length, lbi, ubi, K=K, s=s)
    else:
        kact_args = sparse_heuristic_curve(length, lbi, ubi, activation_type == "Sigmoid", s=s)

    kact_cons = []
    tdim = ElinaDim(offset+length)
    if domain == 'refinezono':
        element = dn.add_dimensions(man,element,offset+length,1)

    KAct.man = man
    KAct.element = element
    KAct.tdim = tdim
    KAct.length = length
    KAct.layerno = layerno
    KAct.offset = offset
    KAct.domain = domain
    KAct.type = activation_type

    start = time.time()

    if domain == 'refinezono':
        with multiprocessing.Pool(config.numproc) as pool:
            input_hrep_array = pool.map(get_ineqs_zono, kact_args)
    else:
        total_size = 0
        for varsid in kact_args:
            size = 3**len(varsid) - 1
            total_size = total_size + size

        linexpr0 = elina_linexpr0_array_alloc(total_size)
        i = 0
        for varsid in kact_args:
            for coeffs in itertools.product([-1, 0, 1], repeat=len(varsid)):
                if all(c == 0 for c in coeffs):
                    continue

                linexpr0[i] = generate_linexpr0(offset, varsid, coeffs)
                i = i + 1
        upper_bound = get_upper_bound_for_linexpr0(man,element,linexpr0, total_size, layerno)
        i=0
        input_hrep_array = []
        for varsid in kact_args:
            input_hrep = []
            for coeffs in itertools.product([-1, 0, 1], repeat=len(varsid)):
                if all(c == 0 for c in coeffs):
                    continue
                input_hrep.append([upper_bound[i]] + [-c for c in coeffs])
                i = i + 1
            input_hrep_array.append(input_hrep)
    end_input = time.time()

    # kact_results = list(map(make_kactivation_obj, input_hrep_array))

    # end1 = time.time()

    with multiprocessing.Pool(config.numproc) as pool:
        # kact_results = pool.map(make_kactivation_obj, input_hrep_array)
        kact_results = pool.starmap(make_kactivation_obj, zip(input_hrep_array, len(input_hrep_array) * [approx]))

    # end2 = time.time()

    # if end2-end_input>10:
    #     print(f"list(map()) time: {end1-end_input:.3f}, multiprocessing time: {end2-end1:.3f}")

    gid = 0
    for inst in kact_results:
        varsid = kact_args[gid]
        inst.varsid = varsid
        kact_cons.append(inst)
        gid = gid+1
    end = time.time()

    if config.debug:
        print(f'total k-activation time: {end-start:.3f}. Time for input: {end_input-start:.3f}. Time for k-activation constraints {end-end_input:.3f}.')
    if domain == 'refinezono':
        element = dn.remove_dimensions(man, element, offset+length, 1)

    constraint_groups.append(kact_cons)
