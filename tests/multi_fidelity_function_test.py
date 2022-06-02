from string import ascii_letters, printable

from hypothesis import given
from hypothesis.strategies import integers, lists, text
from mf2 import MultiFidelityFunction
from pytest import raises, warns


@given(text(alphabet=printable, min_size=1, max_size=30))
def test_name(name):
    mff = MultiFidelityFunction(name, [1], [0], functions=None)
    assert mff._name == name
    assert mff.name == name.title()


def test_unequal_bound_lenghts():
    bounds_A, bounds_B = [0], [1, 2]
    with raises(ValueError):
        MultiFidelityFunction('test', bounds_A, bounds_B, functions=None)
    with raises(ValueError):
        MultiFidelityFunction('test', bounds_B, bounds_A, functions=None)


def test_inconsistent_bounds_warning():
    bounds_A, bounds_B = [1, 2], [2, 1]
    with warns(RuntimeWarning):
        MultiFidelityFunction('test', bounds_A, bounds_B, functions=None)


def test_invalid_x_opt():
    """Test that an error is raised if len(x_opt) is incorrect"""
    l_bound, u_bound = [0, 0], [1, 1]
    with raises(ValueError):
        MultiFidelityFunction('test', u_bound, l_bound, functions=None,
                              x_opt=[.5])
    with raises(ValueError):
        MultiFidelityFunction('test', u_bound, l_bound, functions=None,
                              x_opt=[.5, .5, .5])


def test_x_opt_out_of_bounds():
    l_bound, u_bound = [0, 0], [2, 2]
    with warns(RuntimeWarning):
        MultiFidelityFunction('test', u_bound, l_bound, functions=None, x_opt=[1, 5])


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
        'test', [1], [0],
        functions=functions,
        fidelity_names=fidelity_names
    )

    for idx, name in enumerate(fidelity_names):
        assert mff[idx] is mff[name] is getattr(mff, name)


@given(integers(1, 100))
def test_access_without_fidelity_names(num_fidelities):
    mff = MultiFidelityFunction(
        'test', [1], [0],
        functions=[lambda idx=idx: idx for idx in range(num_fidelities+1)],
    )

    with raises(AttributeError):
        _ = mff.high()
    with raises(AttributeError):
        _ = mff.low()

    with raises(IndexError):
        _ = mff['high']()
    with raises(IndexError):
        _ = mff['low']()

    for idx in range(num_fidelities):
        assert mff[idx]() == idx
