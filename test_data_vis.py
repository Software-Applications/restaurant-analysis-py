import pytest
import datetime
import os
from app.data_vis import quality, savefile, float_format, send_email

def test_quality():
    assert quality(5) == "Exceptional"
    assert quality(4.5) == "Very Good"
    assert quality(4) == "Very Good"
    assert quality(3.5) == "Average"
    assert quality(3) == "Average"
    assert quality(2) == "Poor"

def test_savefile():
    assert savefile("omega.png") == os.path.join(os.getcwd(), "plot_images", "omega.png")

def test_float_format():
    assert float_format(4.57364859) == '4.57'
    assert float_format(3) == '3.00'
    assert float_format(4.567) == '4.57'

def text_send_email():
    res = send_email("abc", "xyz")
    assert res.status_code == 202













