import taichi as ti
from tests import test_utils


def _test_pow_f(dt):
    z = ti.field(dt, shape=())

    @ti.kernel
    def func(x: dt, y: dt):
        z[None] = x**y

    for x in [0.5, 1, 1.5, 2, 6.66]:
        for y in [-2, -1, -0.3, 0, 0.5, 1, 1.4, 2.6]:
            func(x, y)
            assert abs(z[None] / x**y - 1) < 0.00001


def _test_pow_i(dt):
    z = ti.field(dt, shape=())

    @ti.kernel
    def func(x: dt, y: ti.template()):
        z[None] = x**y

    for x in range(-5, 5):
        for y in range(0, 4):
            func(x, y)
            assert z[None] == x**y


@test_utils.test()
def test_pow_f32():
    _test_pow_f(ti.f32)


@test_utils.test(require=ti.extension.data64)
def test_pow_f64():
    _test_pow_f(ti.f64)


@test_utils.test()
def test_pow_i32():
    _test_pow_i(ti.i32)


@test_utils.test(require=ti.extension.data64)
def test_pow_i64():
    _test_pow_i(ti.i64)


def _test_negative_exp(dt):
    z = ti.field(ti.lang.impl.get_runtime().default_fp, shape=())

    @ti.kernel
    def workload(x: dt, y: ti.template()):
        z[None] = x**y

    for x in range(-5, 5):
        for y in range(-5, -1):
            if x != 0:
                workload(x, y)
                assert test_utils.approx(z[None]) == (x**y)


@test_utils.test(default_fp=ti.f32)
def test_negative_exp_i32_f32():
    _test_negative_exp(ti.i32)


@test_utils.test(default_fp=ti.f64, exclude=[ti.metal])
def test_negative_exp_i32_f64():
    _test_negative_exp(ti.i32)


@test_utils.test(default_fp=ti.f32, require=ti.extension.data64)
def test_negative_exp_f64_f32():
    _test_negative_exp(ti.i64)


@test_utils.test(default_fp=ti.f64, require=ti.extension.data64)
def test_negative_exp_i64_f64():
    _test_negative_exp(ti.i64)
