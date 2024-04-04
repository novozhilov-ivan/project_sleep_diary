import pytest
from flask.testing import FlaskClient
from pydantic import ValidationError

from common.pydantic_schemas.notes.sleep_diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.baseclasses.response import Response
from common.pydantic_schemas.user import User
from tests.conftest import client


@pytest.mark.sleep
class TestSleepNotes:
    ROUTE = "/api/sleep"

    STATUS_CODE_OK = 200
    STATUS_CODE_NOT_FOUND = 404
    STATUS_CODE_BAD_REQUEST = 400

    RESPONSE_MODEL_200 = SleepDiaryModel
    RESPONSE_MODEL_404 = SleepDiaryModelEmpty

    EMPTY_SLEEP_DIARY = SleepDiaryModelEmpty()

    SLEEP_PARAMS_NAMES = ['name', 'value']
    CORRECT_PARAMS_GET_NOTES_BY_USER_ID = [
        ('id', 1),
        ('id', "1"),
        ('user_id', 1),
        ('user_id', "1")
    ]
    INCORRECT_PARAMETERS_GET_NOTES_BY_USER_ID = [
        ('id', "str_not_int"),
        ('user_id', "str_not_int"),
        ('not_id', 1),
        ('not_id', 0),
        ('not_id', "1"),
        ('not_id', "0"),
        ('not_id', "str_not_int"),
        ("", "")
    ]

    @pytest.mark.sleep_200
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID
    )
    def test_get_all_sleep_notes_by_user_id_200(
            self,
            name: str,
            value: str | int,
            client: FlaskClient,
            sleep_diary: SleepDiaryModel
    ):
        response = client.get(self.ROUTE, query_string={name: value})
        response = Response(response)
        expectation = sleep_diary

        response.assert_status_code(self.STATUS_CODE_OK)
        response.validate(self.RESPONSE_MODEL_200)
        response.assert_data(expectation)

    @pytest.mark.sleep_404
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        CORRECT_PARAMS_GET_NOTES_BY_USER_ID
    )
    def test_get_all_sleep_notes_by_user_id_404(
            self,
            name: str,
            value: str | int,
            client: FlaskClient
    ):
        response = client.get(self.ROUTE, query_string={name: value})
        response = Response(response)
        response.assert_status_code(self.STATUS_CODE_NOT_FOUND)
        response.validate(self.RESPONSE_MODEL_404)
        response.assert_data(self.EMPTY_SLEEP_DIARY)

    @pytest.mark.sleep_400
    @pytest.mark.parametrize(
        SLEEP_PARAMS_NAMES,
        INCORRECT_PARAMETERS_GET_NOTES_BY_USER_ID
    )
    def test_get_all_sleep_notes_by_user_id_400(
            self,
            name: str,
            value: str | int,
            client: FlaskClient
    ):
        params = {name: value}
        response = client.get(self.ROUTE, query_string=params)
        response = Response(response)
        with pytest.raises(ValidationError) as exception_info:
            User(**params)
        errors = exception_info.value.errors(
            include_url=False,
            include_context=False,
            include_input=False
        )
        response.assert_status_code(self.STATUS_CODE_BAD_REQUEST)
        response.assert_error_data(errors)
