from serve.infra.european_parliament_official_source import XmlEuropeanParliamentMEPSource


def test_get_updated_list_returns_correct_list_of_MEPS():
    # Given
    expected_number_of_meps = 703
    expected_number_of_outgoing_meps = 155
    meps_source = "https://www.europarl.europa.eu/meps/en/full-list/xml"
    outgoing_meps_source = "https://www.europarl.europa.eu/meps/en/incoming-outgoing/outgoing/xml"
    meps_repository = XmlEuropeanParliamentMEPSource(meps_source, outgoing_meps_source)
    # When
    actual_list_of_meps = meps_repository.get_updated_list()
    actual_outgoing_list_of_meps = meps_repository.get_outgoing_list()
    # Then
    assert len(actual_list_of_meps) == expected_number_of_meps
    assert len(actual_outgoing_list_of_meps) == expected_number_of_outgoing_meps
