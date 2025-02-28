"""Test Spectrum I/O for different file types."""

import os
import pytest
import becquerel as bq
from h5_tools_test import TEST_OUTPUTS
from spectrum_test import make_spec
from parsers_test import SAMPLES


@pytest.mark.parametrize("extension", SAMPLES.keys())
def test_spectrum_from_file(extension):
    """Test Spectrum.from_file for the given extension."""
    filenames = SAMPLES[extension]
    assert len(filenames) >= 1
    for filename in filenames:
        spec = bq.Spectrum.from_file(filename)
        assert spec.livetime is not None


def test_spectrum_from_file_raises():
    """Test Spectrum.from_file raises error for an unsupported file type."""
    with pytest.raises(NotImplementedError):
        bq.Spectrum.from_file("foo.bar")


@pytest.mark.parametrize(
    "kind",
    [
        "uncal",
        "cal",
        "cal_new",
        "applied_energy_cal",
        "cal_cps",
        "uncal_long",
        "uncal_cps",
    ],
)
def test_write_h5(kind):
    """Test writing different Spectrums to HDF5 files."""
    spec = make_spec(kind, lt=600.0)
    fname = os.path.join(TEST_OUTPUTS, "spectrum_io__test_write_h5__" + kind + ".h5")
    spec.write(fname)


@pytest.mark.parametrize(
    "kind",
    [
        "uncal",
        "cal",
        "cal_new",
        "applied_energy_cal",
        "cal_cps",
        "uncal_long",
        "uncal_cps",
    ],
)
def test_from_file_h5(kind):
    """Test Spectrum.from_file works for HDF5 files."""
    fname = os.path.join(TEST_OUTPUTS, "spectrum_io__test_write_h5__" + kind + ".h5")
    spec = bq.Spectrum.from_file(fname)
    assert spec.livetime is not None
    if kind == "applied_energy_cal":
        assert spec.is_calibrated and spec.energy_cal is not None


@pytest.mark.parametrize("extension", SAMPLES.keys())
def test_spectrum_samples_write_read_h5(extension):
    """Test Spectrum HDF5 I/O using sample files."""
    filenames = SAMPLES[extension]
    assert len(filenames) >= 1
    for filename in filenames:
        spec = bq.Spectrum.from_file(filename)
        fname2 = os.path.splitext(filename)[0] + ".h5"
        fname2 = os.path.join(
            TEST_OUTPUTS, "spectrum_io__sample_write_h5__" + os.path.split(fname2)[1]
        )
        spec.write(fname2)
        spec = bq.Spectrum.from_file(fname2)
        assert spec.livetime is not None
