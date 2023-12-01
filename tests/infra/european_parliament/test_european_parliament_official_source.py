from serve.infra.european_parliament_official_source import XmlEuropeanParliamentMEPSource


def test_get_updated_list_returns_correct_list_of_MEPS():
    # Given
    expected_number_of_meps = 701
    meps_source = "https://www.europarl.europa.eu/meps/en/full-list/xml"
    meps_repository = XmlEuropeanParliamentMEPSource(meps_source)
    # When
    actual_list_of_meps = meps_repository.get_updated_list()
    # Then
    assert len(actual_list_of_meps) == expected_number_of_meps
