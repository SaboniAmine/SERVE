from serve.domain.vote_analysis.mep import MEPReadFromMinutes


def test_create_mep_return_correct_mep():
    # given
    expected_name = "foo"
    expected_current_group_short_name = "ECR"
    # when
    actual_deputy = MEPReadFromMinutes(name="foo", current_group_short_name="ECR")
    # then
    assert expected_name == actual_deputy.name
    assert expected_current_group_short_name == actual_deputy.current_group_short_name.value
