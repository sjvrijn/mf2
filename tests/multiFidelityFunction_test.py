from string import ascii_letters

from hypothesis import given
from hypothesis.strategies import integers, lists, text
from mf2 import MultiFidelityFunction
from pytest import raises



def test_unequal_bound_lenghts():
    with raises(ValueError):
        bounds_A, bounds_B = [0], [1, 2]
        MultiFidelityFunction('test', bounds_A, bounds_B, functions=None)
        MultiFidelityFunction('test', bounds_B, bounds_A, functions=None)


@given(integers(0, 100))
def test_ndim_matches_bounds_length(ndim):
    u_bounds, l_bounds = [1]*ndim, [0]*ndim
    mff = MultiFidelityFunction('test', u_bounds, l_bounds, functions=None)
    assert mff.ndim == ndim


def _list_of_strings(n):
    return lists(text(alphabet=ascii_letters), min_size=1, max_size=n)


@given(_list_of_strings(100).filter(lambda x: len(x) == len(set(x))))
def test_access_with_fidelity_names(fidelity_names):
    functions = [lambda x: None for _ in fidelity_names]
    mff = MultiFidelityFunction(
        'test', [0], [1],
        functions=functions,
        fidelity_names=fidelity_names
    )

    for idx, name in enumerate(fidelity_names):
        assert mff[idx] is mff[name] is getattr(mff, name)


@given(integers(1, 100))
def test_access_without_fidelity_names(num_fidelities):
    mff = MultiFidelityFunction(
        'test', [0], [1],
        functions=[lambda idx=idx: idx for idx in range(num_fidelities+1)],
    )

    with raises(AttributeError):
        _ = mff.high()
        _ = mff.low()
    with raises(IndexError):
        _ = mff['high']()
        _ = mff['low']()

    for idx in range(num_fidelities):
        assert mff[idx]() == idx
