from serve.domain.vote_analysis.deputy import Deputy


def test_create_deputy_return_correct_deputy():
    # given
    expected_id = "John_Doe_ECR"
    expected_name = "John Doe"
    expected_actual_group = "ECR"
    expected_group_at_time = "Renew"
    # when
    actual_deputy = Deputy(id="John_Doe_ECR", name="John Doe", actual_group="ECR", group_at_time="Renew")
    # then
    assert expected_id == actual_deputy.id
    assert expected_name == actual_deputy.name
    assert expected_actual_group == actual_deputy.actual_group
    assert expected_group_at_time == actual_deputy.group_at_time
