
import pytest
from ab_framework.srm import check_srm
from ab_framework.sample_size import calculate_sample_size, calculate_mde

def test_srm_ok():
    result = check_srm({"control": 10000, "treatment": 10000})
    assert result["is_srm"] == False  # Используем == вместо is
    assert result["p_value"] > 0.05

def test_srm_broken():
    result = check_srm({"control": 10000, "treatment": 11000})
    assert result["is_srm"] == True   # Используем == вместо is
    assert result["p_value"] < 0.05

def test_sample_size():
    ss_10 = calculate_sample_size(0.10, 0.10)["sample_size_per_group"]
    ss_5 = calculate_sample_size(0.10, 0.05)["sample_size_per_group"]
    assert ss_5 > ss_10

def test_mde():
    mde_small_n = calculate_mde(0.10, 10000)["mde_relative"]
    mde_large_n = calculate_mde(0.10, 50000)["mde_relative"]
    assert mde_large_n < mde_small_n