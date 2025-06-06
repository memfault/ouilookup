from ouilookup import OuiLookup


def test_ouilookup_query():
    OL = OuiLookup()
    data = OL.query("00:00:aa:00:00:00")

    assert type(data) is list
    assert len(data) == 1
    assert type(data[0]) is dict
    assert "0000AA000000" in data[0]
    assert data[0]["0000AA000000"] == "XEROX CORPORATION"


def test_ouilookup_query_multi():
    OL = OuiLookup()
    data = OL.query("00:00:01:00:00:00 00-00-10-00-00-00 000011000000")
    print(data)

    assert type(data) is list
    assert len(data) == 3
    assert "000001000000" in data[0]
    assert "000010000000" in data[1]
    assert "000011000000" in data[2]
    assert data[0]["000001000000"] == "XEROX CORPORATION"
    assert data[1]["000010000000"] == "SYTEK INC."
    assert data[2]["000011000000"] == "NORMEREL SYSTEMES"


def test_ouilookup_query_multi2():
    OL = OuiLookup()
    data = OL.query("00:00:01:00:00:00, 00-00-10-00-00-00,000011000000")
    print(data)

    assert type(data) is list
    assert len(data) == 3
    assert "000001000000" in data[0]
    assert "000010000000" in data[1]
    assert "000011000000" in data[2]
    assert data[0]["000001000000"] == "XEROX CORPORATION"
    assert data[1]["000010000000"] == "SYTEK INC."
    assert data[2]["000011000000"] == "NORMEREL SYSTEMES"


def test_ouilookup_query_multi3():
    OL = OuiLookup()
    data = OL.query(["00:00:01:00:00:00", "00-00-10-00-00-00,000011000000"])
    print(data)

    assert type(data) is list
    assert len(data) == 3
    assert "000001000000" in data[0]
    assert "000010000000" in data[1]
    assert "000011000000" in data[2]
    assert data[0]["000001000000"] == "XEROX CORPORATION"
    assert data[1]["000010000000"] == "SYTEK INC."
    assert data[2]["000011000000"] == "NORMEREL SYSTEMES"


def test_ouilookup_status():
    OL = OuiLookup()
    data = OL.status()

    assert type(data) is dict
    assert "data_file" in data
    assert "source_bytes" in data
    assert "vendor_count" in data


def test_ouilookup_query_locally_assigned_single():
    """Test detection of locally assigned MAC address (single query)"""
    OL = OuiLookup()
    # 06 in hex = 00000110 in binary, bit 1 is set (locally assigned)
    data = OL.query("06:00:00:00:00:00")

    assert type(data) is list
    assert len(data) == 1
    assert type(data[0]) is dict
    assert "060000000000" in data[0]
    assert data[0]["060000000000"] == "Locally Assigned"


def test_ouilookup_query_locally_assigned_multiple():
    """Test detection of locally assigned MAC addresses in multiple formats"""
    OL = OuiLookup()
    # Testing various locally assigned addresses:
    # 02 = 00000010 (bit 1 set)
    # 06 = 00000110 (bit 1 set)
    # 0A = 00001010 (bit 1 set)
    # 0E = 00001110 (bit 1 set)
    data = OL.query("02:00:00:00:00:00 06-00-00-00-00-00 0A0000000000 0E:00:00:00:00:00")

    assert type(data) is list
    assert len(data) == 4

    # Check each result
    assert "020000000000" in data[0]
    assert data[0]["020000000000"] == "Locally Assigned"

    assert "060000000000" in data[1]
    assert data[1]["060000000000"] == "Locally Assigned"

    assert "0A0000000000" in data[2]
    assert data[2]["0A0000000000"] == "Locally Assigned"

    assert "0E0000000000" in data[3]
    assert data[3]["0E0000000000"] == "Locally Assigned"


def test_ouilookup_query_mixed_local_and_universal():
    """Test mixed query with both locally assigned and universally administered addresses"""
    OL = OuiLookup()
    # Mix of locally assigned (06) and universally administered (00:00:01)
    data = OL.query("06:00:00:00:00:00 00:00:01:00:00:00")

    assert type(data) is list
    assert len(data) == 2

    # First should be locally assigned
    assert "060000000000" in data[0]
    assert data[0]["060000000000"] == "Locally Assigned"

    # Second should be normal OUI lookup
    assert "000001000000" in data[1]
    assert data[1]["000001000000"] == "XEROX CORPORATION"
