
from ai.dataprovider.metadatarecognizer import MemoryDataRecognizer


def test_str_to_hex():
    val = MemoryDataRecognizer.str_to_hex("0xFF")
    assert val == 255
