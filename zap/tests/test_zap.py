import pytest
import brownie
from brownie import Contract
from brownie import config

def test_3crv_zapper(zap_3crv, lp_3crv, y3crv, vault, accounts, yvecrv_holder):
    before_lp_3Crv = lp_3crv.balanceOf(yvecrv_holder)
    before = y3crv.balanceOf(yvecrv_holder)
    lp_3crv.approve(zap_3crv, 2 ** 256 - 1, {"from": yvecrv_holder})
    zap_3crv.zap({"from": yvecrv_holder})
    assert y3crv.balanceOf(yvecrv_holder) > before
    assert lp_3crv.balanceOf(yvecrv_holder) == 0
    assert lp_3crv.balanceOf(zap_3crv) == 0
    assert y3crv.balanceOf(zap_3crv) == 0
    print("Starting 3Crv Balance:", before_lp_3Crv, "\nStarting yVault Balance:", before, "\nEnding yVault Balance:", y3crv.balanceOf(yvecrv_holder))
