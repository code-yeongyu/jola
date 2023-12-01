import pytest

from jola.analyzer.untyped_relationship_field import find_untyped_relationship_fields


def test_find_untyped_relationship_fields__fixable(source_code):
    # when
    result = find_untyped_relationship_fields(source_code)

    # then
    fixable_results = [result for result in result if result.typed_code]
    assert len(fixable_results) == 1
    assert fixable_results[0].class_name == "Article"
    assert fixable_results[0].field_name == "user"
    assert fixable_results[0].field_type == "ForeignKey"


def test_find_untyped_relationship_fields__unfixable(source_code):
    # when
    result = find_untyped_relationship_fields(source_code)

    # then
    unfixable_results = [result for result in result if not result.typed_code]
    assert len(unfixable_results) == 1
    assert unfixable_results[0].class_name == "Article"
    assert unfixable_results[0].field_name == "related_news"
    assert unfixable_results[0].field_type == "OneToOneField"


def test_find_untyped_relationship_fields__multiline(source_code):
    # when
    result = find_untyped_relationship_fields(source_code)

    # then
    related_news_result = [result for result in result if result.field_name == "related_news"][0]
    assert related_news_result.start_line_number == 10
    assert related_news_result.end_line_number == 12


def test_find_untyped_relationship_fields__no_django_models(get_path, from_file):
    # given
    source_code = from_file(get_path(__file__, "samples/pure_helloworld.py"))

    # when
    result = find_untyped_relationship_fields(source_code)

    # then
    assert len(result) == 0


@pytest.fixture
def source_code(get_path, from_file) -> str:
    return from_file(get_path(__file__, "samples/untyped_relationship_field_sample.py"))
