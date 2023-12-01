from jola.fixer.fix_untyped_relationship_field import fix_untyped_relationship_field
from jola.models.relationship_field import RelationshipField


def test_fix_untyped_relationship_field__fixes(get_path, from_file):
    # given
    source_code = from_file(get_path(__file__, "samples/untyped_relationship_field_sample.py"))
    original_fixable_part = "user = models.ForeignKey(User, on_delete=models.CASCADE)"
    assert original_fixable_part in source_code  # sanity check

    expected_typed_code = "user: ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)"

    # when
    fixed_source_code = fix_untyped_relationship_field(
        source_code,
        [
            RelationshipField(
                class_name="Article",
                field_name="user",
                field_type="ForeignKey",
                start_line_number=9,
                end_line_number=9,
                original_code=original_fixable_part,
                typed_code=expected_typed_code,
            )
        ],
    )

    # then
    assert original_fixable_part not in fixed_source_code


def test_fix_untyped_relationship_field_fixes_multiline_codes(get_path, from_file):
    # given
    source_code = from_file(get_path(__file__, "samples/multiline_untyped_article_user.py"))
    original_fixable_part = """written_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )  # should be fixable"""
    assert original_fixable_part in source_code  # sanity check
    expected_typed_code = "written_by: ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)"

    # when
    fixed_source_code = fix_untyped_relationship_field(
        source_code,
        [
            RelationshipField(
                class_name="Article",
                field_name="written_by",
                field_type="ForeignKey",
                start_line_number=9,
                end_line_number=12,
                original_code=original_fixable_part,
                typed_code=expected_typed_code,
            )
        ],
    )

    # then
    assert original_fixable_part not in fixed_source_code
    assert expected_typed_code in fixed_source_code
